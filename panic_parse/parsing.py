"""Input normalization for .ips panic logs.

Real .ips files are two concatenated JSON documents: a one-line metadata
header, then the pretty-printed body. Whole-file json.loads therefore fails;
split the first line off before parsing.
"""

import json
import re


def extract_metadata(log_content):
    """Return {"panic_string", "device_model", "target_code"} from raw content."""
    panic_string = log_content
    device_model = "Unknown"

    stripped = log_content.strip()
    if stripped.startswith("{"):
        body = _load_body(stripped)
        if body is not None:
            panic_string = body.get("panicString") or log_content
            device_model = body.get("product") or body.get("build") or "Unknown"

    target_code = "Unknown"
    target_match = re.search(r"target/([a-zA-Z0-9_]+)", panic_string, re.IGNORECASE)
    if target_match:
        target_code = target_match.group(1).lower()

    if device_model == "Unknown":
        hw_match = re.search(
            r"Hardware model:\s*([a-zA-Z0-9,_]+)", panic_string, re.IGNORECASE
        )
        if hw_match:
            device_model = hw_match.group(1)

    return {
        "panic_string": panic_string,
        "device_model": device_model,
        "target_code": target_code,
    }


def _load_body(stripped):
    """Parse the JSON body of an .ips file, skipping a one-line header if present.

    Real-world .ips files are occasionally malformed (bare newlines inside
    strings, truncation). When the body JSON fails to parse, recover the
    panicString/product fields directly from the raw text: their literals are
    still well-formed because their special characters are escaped. Returns
    None when nothing is recoverable (caller falls back to raw-text mode).
    """
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    if "\n" in stripped:
        try:
            return json.loads(stripped.split("\n", 1)[1])
        except json.JSONDecodeError:
            pass
        return _recover_fields(stripped)
    return None


def _recover_fields(content):
    """Extract panicString/product literals from a corrupt .ips body."""
    recovered = {}
    match = re.search(
        r'"panicString"\s*:\s*"((?:[^"\\]|\\.)*)"', content, re.DOTALL
    )
    if match:
        try:
            recovered["panicString"] = json.loads(
                '"' + match.group(1) + '"', strict=False
            )
        except json.JSONDecodeError:
            pass
    match = re.search(r'"product"\s*:\s*"([^"\\]*)"', content)
    if match:
        recovered["product"] = match.group(1)
    return recovered or None
