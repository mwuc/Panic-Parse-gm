"""iPhone panic-full log parser: maps SMC sensor-array codes to hardware."""

from . import analysis, parsing, routing, suggestions

__all__ = ["parse_iphone_panic_log"]


def parse_iphone_panic_log(log_content):
    """Parse raw .ips content into a structured diagnosis dict."""
    meta = parsing.extract_metadata(log_content)
    arch = routing.resolve_architecture(meta["target_code"], meta["device_model"])
    result = analysis.analyze(meta["panic_string"], arch)

    result["device_model"] = meta["device_model"]
    result["target_code"] = meta["target_code"]
    result["matched_architecture"] = arch
    # Registry notes (software-class panics) are emitted verbatim and bypass
    # the component-keyed templates; everything else goes through them.
    result["repair_suggestion"] = result["note"] or suggestions.build_suggestions(
        result["components"], result["is_hardware_panic"]
    )

    # Stable key order matching the historical output shape
    return {
        "is_hardware_panic": result["is_hardware_panic"],
        "panic_type": result["panic_type"],
        "device_model": result["device_model"],
        "target_code": result["target_code"],
        "matched_architecture": result["matched_architecture"],
        "detected_codes": result["detected_codes"],
        "missing_sensors": result["missing_sensors"],
        "suspected_hardware": result["suspected_hardware"],
        "components": result["components"],
        "repair_suggestion": result["repair_suggestion"],
    }
