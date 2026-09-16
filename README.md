# panic_parse

Parse iPhone panic-full logs (`.ips`) into a hardware repair diagnosis.

iPhone panic logs often contain SMC sensor-array error codes. These bitmasks mean *different things on different iPhone generations* — the same bit that flags a charging-port flex failure on an iPhone 14 can flag a completely different component on an iPhone 15. `panic_parse` decodes them against the right device architecture and turns them into a list of suspect components and concrete repair suggestions.

Useful for repair-shop triage: point it at a panic log, get "which flex/board component most likely failed" instead of a raw hex code.

## Features

- **`.ips` format handling** — real panic logs are two concatenated JSON documents (a one-line metadata header, then the pretty-printed body); the parser splits and extracts `product` and `panicString` correctly.
- **Architecture-aware bitmask decoding** — maps `(target code, device model)` to the right SMC bitmask table per device family (iPhone 11/12, 13, 14, 14 Pro, 15, 15 Pro, 16/17). **Supported range: iPhone 11 and later** — older iPhones route to a generic table; non-iPhone products (iPad/Watch) and unmapped modern iPhones report `Not Supported` without any decoding.
- **Declarative panic-type registry** — non-SMC panic types (display-coprocessor, AOP sensor bus, SEP, I2C bus faults, baseband/Wi-Fi-BT port-enable, NAND boot failure, power-management timeouts, SoC watchdog, kernel software abort) are declared in an external `panic_types.json`; **adding a new panic type is a pure data edit with no code changes**. Supports per-type subtypes, platform gating, and per-platform hardware attribution. Works for iPads too.
- **Multiple detection branches** — SMC sensor-array bitmask codes (hex or decimal, multi-value), exact-match codes (battery gas-gauge faults), `missing sensor(s)` text, and `SMC_VAL_ABSENT` assertions. Newer iOS versions report codes in decimal (e.g. `1048576`); all values are normalized to hex (`0x100000`) before decomposition.
- **Component-level diagnosis** — every matched entry is reduced to a component key (`charging`, `front_als`, `wireless`, `battery`, `interposer`, `board`, `gyro`, `display`, `sep`, `rf`, `storage`, `audio`), and repair suggestions are driven by exactly those keys — no keyword guessing.
- **Zero dependencies** — Python 3.13, standard library only. No build, no install.

## Quick start

Requirements: Python 3.13 (tested). Nothing else.

### Command line

```bash
python -m panic_parse <file.ips>     # or equivalently: python panic_parse.py <file.ips>
```

Example, using a real iPhone 17 panic log containing `0x300000`:

```bash
python -m panic_parse logs/panic-full-2026-06-29-161152.0002.ips
```

```json
{
  "is_hardware_panic": true,
  "panic_type": "SMC_ARRAY_BITMASK",
  "device_model": "iPhone17,2",
  "target_code": "d94",
  "matched_architecture": "ARCH_IPHONE_16_17",
  "detected_codes": [
    "0x300000"
  ],
  "missing_sensors": [],
  "suspected_hardware": [
    "Charging Port Flex Assembly fault (0x300000)"
  ],
  "components": [
    "charging"
  ],
  "repair_suggestion": "1. Re-seat or replace the Charging Port Flex Assembly."
}
```

`0x300000` on iPhone 15 Pro / 16 / 17 is a generation-specific fault signature (charging-port flex), not the OR of its bits — see [exact codes](#the-core-domain-invariant).

Passing a **directory** batch-processes every top-level `*.ips` file (sorted by name) and prints a single JSON object mapping filename → diagnosis. Unreadable or corrupt files map to `{"error": ...}` and don't stop the batch:

```bash
python -m panic_parse logs/
```

### As a library

```python
from panic_parse import parse_iphone_panic_log

with open("panic-full.ips", encoding="utf-8") as f:
    result = parse_iphone_panic_log(f.read())

if result["is_hardware_panic"]:
    print(result["repair_suggestion"])
```

There is also a smoke command (`python panic_parse.py`) that prints one synthetic iPhone 15 Pro diagnosis; it exists for quick eyeballing only.

## Output reference

| Field | Type | Meaning |
|---|---|---|
| `is_hardware_panic` | bool | True if any hardware-failure branch matched |
| `panic_type` | str | `SMC_ARRAY_BITMASK`, `WATCHDOG_MISSING_SENSOR`, `SMC_ASSERTION_ABSENT`, or `UNKNOWN` (first matching branch wins, in that order) |
| `device_model` | str | e.g. `iPhone15,4` (from the log's `product` field, or `Hardware model:` text fallback) |
| `target_code` | str | internal Apple target identifier, e.g. `d37` — used for architecture routing |
| `matched_architecture` | str | which bitmask table was applied, e.g. `ARCH_IPHONE_15_16_17` |
| `detected_codes` | list | normalized hex codes from the sensor array, e.g. `["0x300000"]` |
| `missing_sensors` | list | sensor IDs from `missing sensor(s)` lines or `!= SMC_VAL_ABSENT` assertions |
| `suspected_hardware` | list | human-readable description of each suspected failure, with the responsible bit |
| `components` | list | matched component keys — the machine-readable diagnosis |
| `repair_suggestion` | str | numbered repair suggestions for the matched components (see note below) |

> **Numbering quirk:** suggestion templates are fixed strings `"1. …"` through `"12. …"`, emitted in fixed order *for matched components only*. Output can therefore skip numbers — a wireless + front-sensor failure produces `"2. … 3. …"` with no `"1."`. This is intentional; don't "fix" it.

## Architecture

Pure-stdlib package with a one-way dependency chain — every module can be understood (and unit-tested) in isolation:

```
                 cli.py / __main__.py
                        |
                   __init__.py            (orchestrator: parse_iphone_panic_log)
                   /    |    |    \
            parsing  routing  analysis  suggestions
                  \      |        /          |
                    data.py  (all domain tables, no logic)
                              ^
              registry.py  (loads/validates panic_types.json)
```

| Module | Responsibility |
|---|---|
| `data.py` | **All domain knowledge**: per-architecture bitmask tables, exact codes, sensor→hardware map, target/product routing, suggestion templates. Pure data. |
| `parsing.py` | Input normalization: `.ips` header split, body JSON parse, `panicString` / `device_model` / `target_code` extraction, raw-text fallbacks. |
| `routing.py` | `(target_code, device_model)` → architecture key. Target-code match wins; exact product-string lookup (`PRODUCT_MAP_ROUTING`, e.g. `iPhone15,4`) is the fallback. |
| `registry.py` | Loads, validates and compiles the external `panic_types.json` registry. Fails fast at import time on any schema error, with repair guidance in the error text. |
| `analysis.py` | Panic-string analysis: missing-sensor marker (first — strongest evidence), then registry signature matching, then sensor-array value extraction, exact-code check, bitwise decomposition, and assertion branches. |
| `suggestions.py` | Component keys → repair text. |
| `cli.py` / `__main__.py` | argparse entry (`python -m panic_parse`). |
| `panic_parse.py` (root) | Compat shim: with a file argument delegates to the CLI; without one prints the smoke case. |

### Diagnosis pipeline

```
raw .ips content
  → parsing.extract_metadata      → panic_string, device_model, target_code
  → routing.resolve_architecture  → e.g. ARCH_IPHONE_16_17 (or NOT_SUPPORTED)
  → analysis.analyze:
       1. "Missing sensor(s): …" marker   ← strongest hardware evidence
       2. registry match (panic_types.json, first match wins)
       3. SMC branches: array codes / assertions   ← fallback
  → suggestions.build_suggestions → repair text for matched keys
                                    (registry `note` bypasses this for software types)
  → result dict (10 keys, stable order)
```

The missing-sensor marker runs first because real logs pair it with a generic `userspace watchdog timeout` header — letting the registry claim those logs would mask the concrete sensor (and its `SENSOR_HARDWARE_MAP` component).

### The core domain invariant

**SMC array bitmask meanings are device-architecture-specific.** The same bit (`0x080000`) maps to different components on iPhone 11/12 vs 13/14 vs 15/16/17 — which is why routing runs *before* any decomposition. Exact-match codes take priority over decomposition in two tiers:

- **Global exact codes** (`EXACT_CODES`: battery gas-gauge faults `0x41`/`0xA1`/`0xA9`) are sub-byte values that can never collide with bitmask combinations.
- **Architecture-scoped exact codes** (`ARCHITECTURE_EXACT_CODES`) are generation fault signatures that *may* overlap bitmask bits — e.g. `0x300000` means a single charging-port-flex fault on iPhone 15 Pro and 16/17, while the same value on the base iPhone 15 decomposes into its ALS + wireless bits. Priority: global exact → architecture exact → bitwise decomposition.

## Adding a panic type (the five-fact workflow)

New panic types are **pure data edits** in `panic_types.json` — no Python changes. Supply:

1. **Type name** — e.g. `"PNP"`;
2. **Match string or regex** — `"match": "PNP Panic"` (literal, punctuation-safe) or `"match_re": "PNP Panic.*USB"`;
3. **Optional subtypes** — each with its own `type` + `match`/`match_re`, matched in order after the entry matches; the subtype's `type` is emitted as `panic_type`. Subtypes may also carry `is_hardware` / `components` / `note` / `architectures` of their own;
4. **Platform relevance** — `"architectures": ["ARCH_IPHONE_16_17"]` (absent = all platforms, including iPads on `DEFAULT_GENERIC`). The value is a **JSON array of architecture keys, OR semantics**: the entry (or subtype) participates whenever the resolved architecture matches *any* listed key — e.g. `["ARCH_IPHONE_14", "ARCH_IPHONE_15_PRO"]` admits both the iPhone 14 and iPhone 15 Pro families. Keys are case-sensitive (`ARCH_IPHONE_15_PRO`, not `ARCH_IPHONE_15_pro`) and must be producible by the routing tables — the loader rejects unknown keys, non-array forms (a `"A|B"` string is not accepted), and empty arrays at import time. A subtype's `architectures` narrows within the entry's gate: gated-out subtypes are skipped, later subtypes still tried, and the entry-level fallback applies when none match;
5. **Hardware** — `"components": "battery"`, a list, or `{"default": "board", "ARCH_IPHONE_16_17": "display"}` for per-platform attribution.

Also available: `"is_hardware": false` + `"note": "..."` for software-class panics (the note becomes `repair_suggestion` verbatim), and `"description"` for the `suspected_hardware` text. Entries are evaluated in declaration order — put more specific ones first. A subtype may carry its own `note` / `is_hardware` / `components` / `architectures`; a subtype hit does **not** inherit the entry's `note` (so a hardware subtype under a software entry still gets template suggestions — see the `Userspace-Panic` entry in `panic_types.json` for a real example), and a subtype's `architectures` gate narrows within the entry's gate (gated-out subtypes are skipped; the entry-level fallback applies when none match). Matching runs against the **panic header** (the first line of `panicString`) by default, case-insensitively: broad substring rules would otherwise hit kext-inventory boilerplate deep in the log body.

**Matching scope (`scope`).** A node may set `"scope": "body"` to match against the **whole** `panicString` instead of just the first line — needed when the signature lives deeper in the log (e.g. the `SCMController … global-errors = N` handler dump). A subtype inherits the entry's scope unless it declares its own; the default stays `header` for every existing type. Because body scope sees the whole log, keep those patterns anchored and specific.

**Dynamic subtype names (capture-group placeholders).** A subtype's `type` may contain `{1}` (numbered group) or `{name}` (named group `(?P<name>…)`) placeholders, expanded from its own `match_re` when it matches — so one rule can name a diagnosis after whatever the log reports. Placeholders require `match_re` (not literal `match`) and are **only** allowed in a subtype's `type`; entries, `description` and `note` reject them at load time.

**Per-controller descriptions (static subtypes before a dynamic catch-all).** Because `description` is static per node, controllers that need distinct `suspected_hardware` text each get their own static subtype; a dynamic `{1}` subtype placed **last** catches any controller name not yet enumerated. Declaration order is the priority order:

```json
{
  "type": "AOP-Panic",
  "match": "AOP PANIC - ",
  "is_hardware": true,
  "description": "Always-On Processor: sensor co-processor (SCM) i2c bus failure",
  "components": "board",
  "subtypes": [
    {
      "type": "AOP-SCM-i2cscm0",
      "scope": "body",
      "match_re": "SCMController[ \\t]+i2cscm0[ \\t]+\\[[^\\]]*\\][ \\t]*:[ \\t]*global-errors[ \\t]*=[ \\t]*[1-9][0-9]*",
      "description": "SCM controller i2cscm0 reports non-zero global errors — <i2cscm0 hardware meaning>",
      "components": "board"
    },
    {
      "type": "AOP-SCM-{1}",
      "scope": "body",
      "match_re": "SCMController[ \\t]+(\\S+)[ \\t]+\\[[^\\]]*\\][ \\t]*:[ \\t]*global-errors[ \\t]*=[ \\t]*[1-9][0-9]*",
      "description": "SCM controller reports non-zero global errors — sensor bus fault",
      "components": "board"
    }
  ]
}
```

A log whose handler dump says `SCMController i2cscm1 [0x11c3548] : global-errors = 4` is diagnosed as `AOP-SCM-i2cscm1`; `i2cscm0` as `AOP-SCM-i2cscm0` (with its own `suspected_hardware` text); an unlisted controller such as `i2cm3` still gets its name via the dynamic catch-all (`AOP-SCM-i2cm3`) with the generic description. A log where every controller reports `global-errors = 0` (or has no handler dump at all) falls back to the entry-level `AOP-Panic`. The `[1-9][0-9]*` tail is what excludes zero, and only the **first** matching subtype in declaration order is reported.

```json
{
  "types": [
    {
      "type": "PNP",
      "match": "PNP Panic",
      "is_hardware": true,
      "description": "PNP subsystem panic (unclassified variant)",
      "components": "board",
      "subtypes": [
        {
          "type": "PNP_USB",
          "match_re": "PNP Panic.*USB",
          "description": "PNP USB port enumeration failure — dock flex / USB circuit",
          "architectures": ["ARCH_IPHONE_16_17"],
          "components": "charging"
        },
        {
          "type": "PNP_LEGACY",
          "match_re": "PNP Panic.*USB",
          "description": "PNP USB failure on older hardware — display-adjacent rail",
          "architectures": ["ARCH_IPHONE_13", "ARCH_IPHONE_14", "ARCH_IPHONE_14_PRO"],
          "components": "display"
        }
      ]
    }
  ]
}
```

With this entry, the same `PNP Panic ... USB` header resolves to `PNP_USB` (→ `charging`) on an iPhone 16/17, to `PNP_LEGACY` (→ `display`) on any of the iPhone 13 / 14 / 14 Pro families (the multi-value OR gate), and to the entry-level `PNP` (→ `board`) on any other architecture — one signature, three platform-specific diagnoses, all in pure JSON.

**Hand-editing gotchas:** backslashes must be doubled in JSON (`i2c\d+::` → `"i2c\\d+::"`) — prefer literal `match` when no pattern syntax is needed; the file must be UTF-8; every component key must have a `SUGGESTION_TEMPLATES` entry in `data.py` first; `architectures` entries must be producible by the routing tables. The loader validates all of this at import time and fails the test suite immediately with repair guidance — run `python -m unittest` after every registry edit.

## Adding a new device generation

Edit `data.py` only:

1. Add a bitmask table to `SMC_BITMASK_ARCHITECTURES` (each entry: `description`, `component`, `key`).
2. Add the generation's target codes to `TARGET_CODE_ROUTING`.
3. Add its product strings (e.g. `iPhone17,2`) to `PRODUCT_MAP_ROUTING`. Note the product-map number does not track the marketing generation — `iPhone13,x` is the iPhone 12 family — so always route by full product string.
4. If the generation has known multi-bit fault signatures (values whose full meaning isn't the OR of their bits), add them to `ARCHITECTURE_EXACT_CODES`.

No logic changes anywhere else. Component `key`s drive suggestion emission; reuse the existing keys where the template applies.

## Testing

```bash
python -m unittest          # 141 tests (+3 auto-skipped golden tests when mclogs/ is empty), ~1s
```

The suite covers the real AOP panic logs in `logs/` end-to-end (dynamic `AOP-SCM-<controller>` naming from the handler dump, zero-error and no-handler fallbacks — asserted for whichever fixtures are present), and, when the `mclogs/` corpus is present, all of its files as a golden mapping (filename → expected `panic_type`; the golden tests auto-skip while the directory is empty). Plus synthetic cases for every branch: registry subtypes / platform gating / matching scope / capture-group names / per-platform components, corrupt-JSON field recovery, decimal codes, multi-value arrays, missing sensors, assertions, exact codes, null JSON values, routing precedence, and registry validation errors. Run it after any change — especially after editing `panic_types.json`.

## Repository layout

```
panic_parse/            # the package (see Architecture)
panic_parse.py          # compat shim (CLI delegate + smoke)
panic_types.json        # declarative panic-type registry (edit this to add types)
tests/                  # unittest suite
logs/                   # real .ips fixtures (iPhone14,6 routing + iPad14,4 Not Supported)
mclogs/                 # golden-mapping corpus location (currently empty; tests skip)
docs/superpowers/       # design specs and implementation plans
```

## Limitations

- Diagnosis is heuristic — suggestions indicate the *most likely* failed component, not a guarantee. Always confirm with diode-mode/continuity measurements before replacing parts.
- Only iPhone 11 and later are supported: older iPhones get generic (DEFAULT_GENERIC) decoding; iPads/Watches and unmapped modern iPhones report `Not Supported` with no decoding.
- Exact codes match hex form only on the `SMC PANIC - ASSERT` fallback path (decimal two-digit forms are unreachable there by design — see the comment in `analysis.py`).
