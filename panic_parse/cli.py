"""Command-line interface: python -m panic_parse <file.ips | directory>"""

import argparse
import json
import sys
from pathlib import Path

from . import parse_iphone_panic_log


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="panic_parse",
        description="Parse an iPhone panic-full .ips log into a hardware diagnosis.",
    )
    parser.add_argument(
        "ips_file",
        help="Path to an .ips panic log file, or a directory of .ips logs",
    )
    args = parser.parse_args(argv)

    path = Path(args.ips_file)
    if path.is_dir():
        _emit(_scan_directory(path))
    else:
        _emit(parse_iphone_panic_log(path.read_text(encoding="utf-8")))
    return 0


def _scan_directory(path):
    """Parse every top-level *.ips file in the directory, sorted by name.

    Unreadable or corrupt files map to {"error": ...}; the batch continues.
    """
    results = {}
    for file in sorted(path.glob("*.ips")):
        try:
            results[file.name] = parse_iphone_panic_log(
                file.read_text(encoding="utf-8")
            )
        except (OSError, ValueError) as exc:
            results[file.name] = {"error": str(exc)}
    return results


def _emit(result):
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
