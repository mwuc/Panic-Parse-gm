"""Architecture resolution from target code and device model."""

import re

from . import data


def resolve_architecture(target, model) -> str:
    """Map (target_code, device_model) to an architecture key.

    The product string is authoritative for device identity:

    1. Exact product match in PRODUCT_MAP_ROUTING wins (e.g. "iPhone15,4").
    2. An iPhone product not in the map routes by major number:
       <= 10 -> DEFAULT_GENERIC (old iPhone, no bitmask table),
       >= 11 -> NOT_SUPPORTED (routing-data gap — add the product entry).
    3. A non-iPhone Apple product (iPad / Watch / ...) -> NOT_SUPPORTED:
       only iPhone 11 and later are supported.
    4. An unidentifiable model ("Unknown", garbage text) falls back to a
       known iPhone target code; without one it is NOT_SUPPORTED.
    """
    arch = data.PRODUCT_MAP_ROUTING.get(model)
    if arch:
        return arch

    model_lower = model.lower()
    iphone_match = re.search(r"iphone(\d+)", model_lower)
    if iphone_match:
        if int(iphone_match.group(1)) <= 10:
            return "DEFAULT_GENERIC"
        return data.NOT_SUPPORTED

    # Non-iPhone Apple product: authoritative Not Supported, even if a
    # stray iPhone target code appears in the panic string.
    if re.search(r"ipad|watch|ipod|appletv", model_lower):
        return data.NOT_SUPPORTED

    # Unidentifiable model: a known iPhone target code can still route.
    target_lower = target.lower()
    for code, arch in data.TARGET_CODE_ROUTING.items():
        if code in target_lower:
            return arch

    return data.NOT_SUPPORTED
