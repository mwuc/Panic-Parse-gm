# panic_parse

Parse iPhone panic-full logs (`.ips`) into a hardware repair diagnosis.

iPhone panic logs often contain SMC sensor-array error codes. These bitmasks mean *different things on different iPhone generations* — the same bit that flags a charging-port flex failure on an iPhone 14 can flag a completely different component on an iPhone 15. `panic_parse` decodes them against the right device architecture and turns them into a list of suspect components and concrete repair suggestions.

Useful for repair-shop triage: point it at a panic log, get "which flex/board component most likely failed" instead of a raw hex code.

## Features

- **`.ips` format handling** — real panic logs are two concatenated JSON documents (a one-line metadata header, then the pretty-printed body); the parser splits and extracts `product` and `panicString` correctly.
- **Architecture-aware bitmask decoding** — maps `(target code, device model)` to the right SMC bitmask table per device family (iPhone 11/12, 13, 14, 14 Pro, 15, 15 Pro, 16/17), with a generic fallback for everything else.
- **Multiple detection branches** — SMC sensor-array bitmask codes (hex or decimal, multi-value), exact-match codes (battery gas-gauge faults), `missing sensor(s)` text, and `SMC_VAL_ABSENT` assertions. Newer iOS versions report codes in decimal (e.g. `1048576`); all values are normalized to hex (`0x100000`) before decomposition.
- **Component-level diagnosis** — every matched entry is reduced to a component key (`charging`, `front_als`, `wireless`, `battery`, `interposer`, `board`), and repair suggestions are driven by exactly those keys — no keyword guessing.
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

> **Numbering quirk:** suggestion templates are fixed strings `"1. …"` through `"5. …"`, emitted in fixed order *for matched components only*. Output can therefore skip numbers — a wireless + front-sensor failure produces `"2. … 3. …"` with no `"1."`. This is intentional; don't "fix" it.

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
```

| Module | Responsibility |
|---|---|
| `data.py` | **All domain knowledge**: per-architecture bitmask tables, exact codes, sensor→hardware map, target/product routing, suggestion templates. Pure data. |
| `parsing.py` | Input normalization: `.ips` header split, body JSON parse, `panicString` / `device_model` / `target_code` extraction, raw-text fallbacks. |
| `routing.py` | `(target_code, device_model)` → architecture key. Target-code match wins; exact product-string lookup (`PRODUCT_MAP_ROUTING`, e.g. `iPhone15,4`) is the fallback. |
| `analysis.py` | Panic-string analysis: sensor-array value extraction, exact-code check, bitwise decomposition, missing-sensor and assertion branches. |
| `suggestions.py` | Component keys → repair text. |
| `cli.py` / `__main__.py` | argparse entry (`python -m panic_parse`). |
| `panic_parse.py` (root) | Compat shim: with a file argument delegates to the CLI; without one prints the smoke case. |

### Diagnosis pipeline

```
raw .ips content
  → parsing.extract_metadata      → panic_string, device_model, target_code
  → routing.resolve_architecture  → e.g. ARCH_IPHONE_15_16_17
  → analysis.analyze              → codes, sensors, suspected hardware, component keys
  → suggestions.build_suggestions → repair text for matched keys
  → result dict (10 keys, stable order)
```

### The core domain invariant

**SMC array bitmask meanings are device-architecture-specific.** The same bit (`0x080000`) maps to different components on iPhone 11/12 vs 13/14 vs 15/16/17 — which is why routing runs *before* any decomposition. Exact-match codes take priority over decomposition in two tiers:

- **Global exact codes** (`EXACT_CODES`: battery gas-gauge faults `0x41`/`0xA1`/`0xA9`) are sub-byte values that can never collide with bitmask combinations.
- **Architecture-scoped exact codes** (`ARCHITECTURE_EXACT_CODES`) are generation fault signatures that *may* overlap bitmask bits — e.g. `0x300000` means a single charging-port-flex fault on iPhone 15 Pro and 16/17, while the same value on the base iPhone 15 decomposes into its ALS + wireless bits. Priority: global exact → architecture exact → bitwise decomposition.

## Adding a new device generation

Edit `data.py` only:

1. Add a bitmask table to `SMC_BITMASK_ARCHITECTURES` (each entry: `description`, `component`, `key`).
2. Add the generation's target codes to `TARGET_CODE_ROUTING`.
3. Add its product strings (e.g. `iPhone17,2`) to `PRODUCT_MAP_ROUTING`. Note the product-map number does not track the marketing generation — `iPhone13,x` is the iPhone 12 family — so always route by full product string.
4. If the generation has known multi-bit fault signatures (values whose full meaning isn't the OR of their bits), add them to `ARCHITECTURE_EXACT_CODES`.

No logic changes anywhere else. Component `key`s drive suggestion emission; reuse the existing keys where the template applies.

## Testing

```bash
python -m unittest          # 41 tests, ~0.1s
```

The suite covers the three real panic logs in `logs/` end-to-end (filenames encode the scenario, e.g. `panic-full-iphone14pro-0x1c0000.ips` = iPhone 14 Pro log with code `0x1c0000`), plus synthetic cases for every branch: decimal codes, multi-value arrays, missing sensors, assertions, exact codes, null JSON values, and routing precedence. Run it after any change.

## Repository layout

```
panic_parse/            # the package (see Architecture)
panic_parse.py          # compat shim (CLI delegate + smoke)
tests/                  # unittest suite
logs/                   # real .ips fixtures (iPhone 14 Pro, iPhone 15, iPhone 17)
docs/superpowers/       # design spec and implementation plan
```

## Limitations

- Diagnosis is heuristic — suggestions indicate the *most likely* failed component, not a guarantee. Always confirm with diode-mode/continuity measurements before replacing parts.
- `logs/` fixtures are the authoritative sample of real-world formats; untested panic layouts may route to `DEFAULT_GENERIC`.
- Exact codes match hex form only on the `SMC PANIC - ASSERT` fallback path (decimal two-digit forms are unreachable there by design — see the comment in `analysis.py`).
