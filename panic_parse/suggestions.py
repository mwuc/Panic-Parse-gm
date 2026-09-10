"""Repair suggestions driven by matched component keys."""

from . import data


def build_suggestions(components, is_hardware_panic):
    """Render numbered suggestion text for matched component keys, in fixed order."""
    if not is_hardware_panic:
        return ""
    matched = set(components)
    parts = [text for key, text in data.SUGGESTION_TEMPLATES if key in matched]
    if not parts and is_hardware_panic:
        parts.append(data.FALLBACK_SUGGESTION)
    return " ".join(parts)
