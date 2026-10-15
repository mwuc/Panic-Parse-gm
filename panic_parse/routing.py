"""Architecture resolution from target code and device model."""

import re

from . import data


def resolve_architecture(target, model) -> str:
    """Map (target_code, device_model) to an architecture key.

    The product string is authoritative for device identity:

    1. Exact product match in PRODUCT_MAP_ROUTING wins (iPhone or iPad).
    2. An iPhone product not in the map routes by major number:
       <= 10 -> DEFAULT_GENERIC (old iPhone, no bitmask table),
       >= 11 -> the newest PRODUCT_GENERATION_FALLBACK generation at or
       below its major; uncovered majors -> NOT_SUPPORTED.
    3. An iPad product not in the map routes the same way through
       IPAD_PRODUCT_GENERATION_FALLBACK.
    4. iPod / Watch / AppleTV -> NOT_SUPPORTED.
    5. An unidentifiable model falls back to a known target code (checked
       longest-key-first, so a longer code is never shadowed by a shorter
       prefix); without one it is NOT_SUPPORTED.
    """
    arch = data.PRODUCT_MAP_ROUTING.get(model)
    if arch:
        return arch

    model_lower = model.lower()
    iphone_match = re.search(r"iphone(\d+)", model_lower)
    if iphone_match:
        major = int(iphone_match.group(1))
        if major <= 10:
            return "DEFAULT_GENERIC"
        return _generation_fallback(major, data.PRODUCT_GENERATION_FALLBACK)

    ipad_match = re.search(r"ipad(\d+)", model_lower)
    if ipad_match:
        return _generation_fallback(
            int(ipad_match.group(1)), data.IPAD_PRODUCT_GENERATION_FALLBACK
        )

    # iPod / Watch / AppleTV are not supported at this stage.
    if re.search(r"watch|ipod|appletv", model_lower):
        return data.NOT_SUPPORTED

    # Unidentifiable model: a known target code can still route. Longest key
    # first so "j717" is not shadowed by its prefix "j71".
    target_lower = target.lower()
    for code in sorted(data.TARGET_CODE_ROUTING, key=len, reverse=True):
        if code in target_lower:
            return data.TARGET_CODE_ROUTING[code]

    return data.NOT_SUPPORTED


def _generation_fallback(major, floor_table):
    """Newest generation at or below `major`, else NOT_SUPPORTED.

    The table key is a threshold, so a single entry also covers later
    generations; majors no entry covers keep the data-gap signal.
    """
    floors = [k for k in floor_table if k <= major]
    if floors:
        return floor_table[max(floors)]
    return data.NOT_SUPPORTED
