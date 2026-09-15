"""Panic-string analysis: SMC array codes, missing sensors, assertions."""

import re

from . import data, registry


def analyze(panic_string, architecture):
    """Extract codes/sensors and decompose bitmasks for the given architecture."""
    out = {
        "is_hardware_panic": False,
        "panic_type": "UNKNOWN",
        "detected_codes": [],
        "missing_sensors": [],
        "suspected_hardware": [],
        "components": [],
        "note": None,
    }

    # Non-iPhone devices are outside the supported range: no registry
    # matching, no SMC decoding — the result is "Not Supported", full stop.
    if architecture == data.NOT_SUPPORTED:
        out["panic_type"] = data.NOT_SUPPORTED_MESSAGE
        out["note"] = data.NOT_SUPPORTED_MESSAGE
        return out

    smc_bitmasks = data.SMC_BITMASK_ARCHITECTURES[architecture]
    arch_exact_codes = data.ARCHITECTURE_EXACT_CODES.get(architecture, {})

    if not _analyze_registry(panic_string, architecture, out):
        _analyze_smc_array(panic_string, smc_bitmasks, arch_exact_codes, out)
        _analyze_missing_sensors(panic_string, out)
        _analyze_smc_assertions(panic_string, out)

    out["suspected_hardware"] = sorted(set(out["suspected_hardware"]))
    out["components"] = sorted(set(out["components"]))
    return out


def _parse_value(token):
    token = token.strip()
    if token.lower().startswith("0x"):
        return int(token, 16)
    return int(token)


def _analyze_registry(panic_string, architecture, out, entries=None):
    """Match the declarative panic-type registry; first match wins.

    Matching is scoped to the panic header (the first line of the panic
    string): broad substring rules (bare "pmgr", i2c tokens) would otherwise
    hit kext-inventory boilerplate ("com.apple.driver.AppleT8110PMGR") that
    most modern panic logs carry deep in the body. The registry patterns are
    line-oriented by construction (_WORD = spaces/tabs only), so the header
    is their natural matching domain; every real signature lives on line 1.

    Returns True when an entry matched — the caller then skips the SMC
    branches entirely. `entries` defaults to the loaded registry and exists
    so the engine can be unit-tested with in-memory registries.
    """
    if entries is None:
        entries = registry.REGISTRY

    header = panic_string.split("\n", 1)[0]
    for entry in entries:
        architectures = entry["architectures"]
        if architectures and architecture not in architectures:
            continue
        if not entry["pattern"].search(header):
            continue

        matched = entry
        for subtype in entry["subtypes"]:
            # A subtype's architectures gate narrows within the entry's gate:
            # gated-out subtypes are skipped, later subtypes still tried.
            subtype_architectures = subtype["architectures"]
            if subtype_architectures and architecture not in subtype_architectures:
                continue
            if subtype["pattern"].search(header):
                matched = subtype
                break

        out["panic_type"] = matched["type"]
        is_hardware = matched["is_hardware"]
        out["is_hardware_panic"] = (
            entry["is_hardware"] if is_hardware is None else is_hardware
        )

        description = matched["description"] or entry["description"]
        if description:
            out["suspected_hardware"].append(description)

        components = matched["components"]
        if components is None:
            components = entry["components"]
        out["components"].extend(_resolve_components(components, architecture))

        # Notes are per-node: a subtype hit does NOT inherit the entry's
        # note (a hardware subtype under a software entry must still get
        # template suggestions, not the software note).
        if matched["note"]:
            out["note"] = matched["note"]
        return True
    return False


def _resolve_components(components, architecture):
    """Resolve a components declaration (str / list / per-arch dict) to keys."""
    if components is None:
        return []
    if isinstance(components, str):
        return [components]
    if isinstance(components, list):
        return list(components)
    value = components.get(architecture, components.get("default"))
    if value is None:
        return []
    return [value] if isinstance(value, str) else list(value)


def _analyze_smc_array(panic_string, smc_bitmasks, arch_exact_codes, out):
    array_match = re.search(
        r"S\.sensor array.*?is\s+((?:0x[0-9a-fA-F]+|\d+)(?:\s*,\s*(?:0x[0-9a-fA-F]+|\d+))*)",
        panic_string,
        re.DOTALL | re.IGNORECASE,
    )
    if array_match:
        values = [
            _parse_value(tok)
            for tok in array_match.group(1).split(",")
        ]
    else:
        # The {5,8} digit range is deliberate: broadening to \d+ would
        # false-match line numbers in paths like target.cpp:250. Decimal
        # forms of sub-byte exact codes (65/161/169) are therefore
        # unreachable on this fallback path; hex forms work.
        assert_match = re.search(
            r"SMC PANIC - ASSERT.*?:?\s*(0x[0-9a-fA-F]+|\b\d{5,8}\b)",
            panic_string,
            re.IGNORECASE,
        )
        values = [_parse_value(assert_match.group(1))] if assert_match else []

    for code_val in values:
        if code_val <= 0:
            continue
        out["is_hardware_panic"] = True
        if out["panic_type"] == "UNKNOWN":
            out["panic_type"] = "SMC_ARRAY_BITMASK"
        hex_str = hex(code_val)
        if hex_str not in out["detected_codes"]:
            out["detected_codes"].append(hex_str)

        # Priority: global exact codes (cross-generational, sub-byte) ->
        # architecture-scoped exact codes (generation fault signatures) ->
        # bitwise decomposition.
        if code_val in data.EXACT_CODES:
            description, key = data.EXACT_CODES[code_val]
            out["suspected_hardware"].append(description)
            out["components"].append(key)
        elif code_val in arch_exact_codes:
            description, key = arch_exact_codes[code_val]
            out["suspected_hardware"].append(description)
            out["components"].append(key)
        else:
            for mask, info in smc_bitmasks.items():
                if code_val & mask:
                    out["suspected_hardware"].append(
                        f"{info['description']} [{hex(mask)}]"
                    )
                    out["components"].append(info["key"])


def _record_sensor(sensor, out):
    s_lower = sensor.lower()
    if s_lower not in out["missing_sensors"]:
        out["missing_sensors"].append(s_lower)
    if s_lower in data.SENSOR_HARDWARE_MAP:
        description, key = data.SENSOR_HARDWARE_MAP[s_lower]
        out["suspected_hardware"].append(f"{s_lower.upper()} -> {description}")
        out["components"].append(key)


def _analyze_missing_sensors(panic_string, out):
    missing_match = re.search(
        r"missing\s+sensor\(s\):\s*([a-zA-Z0-9\s_]+?)(?=\n|\\n|\"|$)",
        panic_string,
        re.IGNORECASE,
    )
    if missing_match:
        out["is_hardware_panic"] = True
        if out["panic_type"] == "UNKNOWN":
            out["panic_type"] = "WATCHDOG_MISSING_SENSOR"
        for sensor in missing_match.group(1).strip().split():
            _record_sensor(sensor, out)


def _analyze_smc_assertions(panic_string, out):
    for sensor in re.findall(
        r"(\b[a-zA-Z0-9_]+\b)\s*!=\s*SMC_VAL_ABSENT", panic_string, re.IGNORECASE
    ):
        out["is_hardware_panic"] = True
        if out["panic_type"] == "UNKNOWN":
            out["panic_type"] = "SMC_ASSERTION_ABSENT"
        _record_sensor(sensor, out)
