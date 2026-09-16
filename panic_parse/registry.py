"""External panic-type registry: load, validate and compile panic_types.json.

The registry is the extension point for new panic types: adding a type is a
pure JSON edit (no Python logic changes). Validation is deliberately strict
and fails at import time so a malformed registry breaks the test suite
immediately rather than silently mis-diagnosing logs.
"""

import json
import re
from pathlib import Path

from . import data

DEFAULT_REGISTRY_PATH = Path(__file__).resolve().parent.parent / "panic_types.json"

# Placeholders in a subtype's "type" are expanded at match time with the
# capture groups of its "match_re": {1} is a numbered group, {name} a named
# group. Exposed because the analysis engine performs the expansion.
TYPE_PLACEHOLDER_RE = re.compile(r"\{(\d+|[A-Za-z_][A-Za-z0-9_]*)\}")

_VALID_SCOPES = ("header", "body")


def component_keys():
    """Component keys that have a repair-suggestion template."""
    return {key for key, _ in data.SUGGESTION_TEMPLATES}


def known_architectures():
    """Architecture keys the routing layer can actually produce."""
    return (
        set(data.TARGET_CODE_ROUTING.values())
        | set(data.PRODUCT_MAP_ROUTING.values())
        | set(data.SMC_BITMASK_ARCHITECTURES)
    )


def validate_registry(raw, keys, architectures):
    """Validate a parsed registry document; return normalized entries.

    Pure function over already-parsed data — no file I/O, so it is directly
    unit-testable with in-memory documents.
    """
    if not isinstance(raw, dict) or not isinstance(raw.get("types"), list):
        raise ValueError(
            "panic_types: top level must be an object with a 'types' array"
        )

    seen = set()
    entries = []
    for index, node in enumerate(raw["types"]):
        where = f"types[{index}]"
        entry = _validate_node(node, where, seen, keys, architectures, is_entry=True)
        entry["architectures"] = _validate_architectures(
            node.get("architectures"), where, architectures
        )
        entry["scope"] = _validate_scope(node.get("scope"), where)
        subtypes = []
        for sub_index, sub in enumerate(node.get("subtypes", [])):
            sub_where = f"{where}.subtypes[{sub_index}]"
            subtype = _validate_node(
                sub, sub_where, seen, keys, architectures, is_entry=False
            )
            subtype["architectures"] = _validate_architectures(
                sub.get("architectures"), sub_where, architectures
            )
            subtype["scope"] = _validate_scope(sub.get("scope"), sub_where)
            subtypes.append(subtype)
        entry["subtypes"] = subtypes
        entries.append(entry)
    return entries


def _validate_scope(value, where):
    if value is None:
        return None
    if value not in _VALID_SCOPES:
        raise ValueError(
            f"{where}: 'scope' must be one of {list(_VALID_SCOPES)} or omitted "
            "(default: header — first line of the panic string only)"
        )
    return value


def _validate_node(node, where, seen, keys, architectures, is_entry):
    if not isinstance(node, dict):
        raise ValueError(f"{where}: entry must be an object")

    type_name = node.get("type")
    if not isinstance(type_name, str) or not type_name:
        raise ValueError(f"{where}: missing or non-string 'type'")
    if type_name in seen:
        raise ValueError(f"{where}: duplicate type '{type_name}'")
    seen.add(type_name)

    has_literal = "match" in node
    has_regex = "match_re" in node
    if has_literal == has_regex:
        raise ValueError(
            f"{where} ({type_name}): provide exactly one of 'match' or 'match_re'"
        )
    if has_regex:
        raw_pattern = node["match_re"]
        if not isinstance(raw_pattern, str):
            raise ValueError(f"{where} ({type_name}): 'match_re' must be a string")
        try:
            pattern = re.compile(raw_pattern, re.IGNORECASE)
        except re.error as exc:
            raise ValueError(
                f"{where} ({type_name}): invalid regex {raw_pattern!r} — {exc}"
            ) from exc
    else:
        literal = node["match"]
        if not isinstance(literal, str) or not literal:
            raise ValueError(f"{where} ({type_name}): 'match' must be a non-empty string")
        pattern = re.compile(re.escape(literal), re.IGNORECASE)

    is_hardware = node.get("is_hardware")
    if is_entry:
        if not isinstance(is_hardware, bool):
            raise ValueError(f"{where} ({type_name}): 'is_hardware' must be a boolean")
    elif is_hardware is not None and not isinstance(is_hardware, bool):
        raise ValueError(f"{where} ({type_name}): 'is_hardware' must be a boolean")

    dynamic_type = _validate_type_placeholders(
        type_name, pattern, where, is_entry, has_regex
    )
    description = _validate_text(node.get("description"), where, "description")
    note = _validate_text(node.get("note"), where, "note")
    _reject_placeholders(description, where, "description")
    _reject_placeholders(note, where, "note")

    return {
        "type": type_name,
        "pattern": pattern,
        "dynamic_type": dynamic_type,
        "is_hardware": is_hardware,
        "description": description,
        "components": _validate_components(
            node.get("components"), where, type_name, keys, architectures
        ),
        "note": note,
    }


def _validate_type_placeholders(type_name, pattern, where, is_entry, uses_regex):
    """Validate {N}/{name} placeholders in a 'type'; return True when present.

    Placeholders are only meaningful on subtypes (the entry emits its own
    declared name) and require a regex with a matching capture group.
    """
    placeholders = TYPE_PLACEHOLDER_RE.findall(type_name)
    if not placeholders:
        return False
    if is_entry:
        raise ValueError(
            f"{where} ({type_name}): 'type' placeholders are only supported on subtypes"
        )
    if not uses_regex:
        raise ValueError(
            f"{where} ({type_name}): 'type' placeholders require 'match_re' "
            "with capture groups"
        )
    for key in placeholders:
        if key.isdigit():
            index = int(key)
            if index < 1 or index > pattern.groups:
                raise ValueError(
                    f"{where} ({type_name}): placeholder '{{{key}}}' has no matching "
                    f"capture group (match_re defines {pattern.groups})"
                )
        elif key not in pattern.groupindex:
            raise ValueError(
                f"{where} ({type_name}): placeholder '{{{key}}}' has no matching "
                "named group in 'match_re'"
            )
    return True


def _reject_placeholders(text, where, field):
    if text and TYPE_PLACEHOLDER_RE.search(text):
        raise ValueError(
            f"{where}: placeholders are only supported in a subtype 'type'; "
            f"remove the placeholder from '{field}'"
        )


def _validate_text(value, where, field):
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{where}: '{field}' must be a string")
    return value


def _validate_architectures(value, where, architectures):
    if value is None:
        return None
    if not isinstance(value, list) or not value:
        raise ValueError(f"{where}: 'architectures' must be a non-empty array or null")
    for arch in value:
        if arch not in architectures:
            raise ValueError(
                f"{where}: unknown architecture '{arch}' — known: "
                f"{sorted(architectures)}; add routing entries in data.py first"
            )
    return set(value)


def _validate_components(value, where, type_name, keys, architectures):
    if value is None:
        return None
    if isinstance(value, str):
        candidates = [value]
    elif isinstance(value, list):
        candidates = value
        for item in candidates:
            if not isinstance(item, str):
                raise ValueError(
                    f"{where} ({type_name}): 'components' array items must be strings, "
                    f"got {type(item).__name__}"
                )
    elif isinstance(value, dict):
        candidates = []
        for arch, arch_value in value.items():
            if arch != "default" and arch not in architectures:
                raise ValueError(
                    f"{where} ({type_name}): unknown architecture '{arch}' — known: "
                    f"{sorted(architectures)}; add routing entries in data.py first"
                )
            if isinstance(arch_value, str):
                candidates.append(arch_value)
            elif isinstance(arch_value, list):
                for item in arch_value:
                    if not isinstance(item, str):
                        raise ValueError(
                            f"{where} ({type_name}): components['{arch}'] array items "
                            f"must be strings, got {type(item).__name__}"
                        )
                candidates.extend(arch_value)
            else:
                raise ValueError(
                    f"{where} ({type_name}): components['{arch}'] must be a string or "
                    f"an array of strings, got {type(arch_value).__name__}"
                )
    else:
        raise ValueError(
            f"{where} ({type_name}): 'components' must be a string, array or object"
        )

    for key in candidates:
        if key not in keys:
            raise ValueError(
                f"{where} ({type_name}): unknown component key '{key}' — known: "
                f"{sorted(keys)}; add a SUGGESTION_TEMPLATES entry in data.py first"
            )
    return value


def load_registry(path=None):
    """Read, validate and compile the registry file (default: repo root)."""
    registry_path = Path(path) if path else DEFAULT_REGISTRY_PATH
    if not registry_path.is_file():
        raise FileNotFoundError(
            f"panic type registry not found at {registry_path}; "
            "create panic_types.json or pass an explicit path"
        )
    raw = json.loads(registry_path.read_text(encoding="utf-8"))
    return validate_registry(raw, component_keys(), known_architectures())


REGISTRY = load_registry()
