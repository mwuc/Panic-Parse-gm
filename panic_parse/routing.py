"""Architecture resolution from target code and device model."""

from . import data


def resolve_architecture(target, model) -> str:
    """Map (target_code, device_model) to an architecture key.

    Target-code match wins; exact product string (e.g. "iPhone15,4") via
    PRODUCT_MAP_ROUTING is the fallback. The product-map number does not
    track the marketing generation, so no major-number matching.
    """
    target_lower = target.lower()
    for code, arch in data.TARGET_CODE_ROUTING.items():
        if code in target_lower:
            return arch

    return data.PRODUCT_MAP_ROUTING.get(model, "DEFAULT_GENERIC")
