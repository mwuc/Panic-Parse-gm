"""Compatibility shim for `python panic_parse.py`.

Implementation lives in the panic_parse/ package, which shadows this
module name on sys.path, so a plain import from here resolves to the
package. With a file argument this delegates to the real CLI; without
one it prints the hard-coded smoke case.
"""

import json
import sys

from panic_parse import parse_iphone_panic_log

__all__ = ["parse_iphone_panic_log"]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        from panic_parse.cli import main

        sys.exit(main(sys.argv[1:]))

    log_ip15 = """
    {
        "product" : "iPhone16,1",
        "panicString" : "panic(...): SMC PANIC - ASSERT: target/d84/target.cpp:250: 0, SMC BSC failure\\nS.sensor array 0 - 7 is 0, 0x180000, 0, 0"
    }
    """
    print("=== Smoke: iPhone 15 Pro (Target d84) ===")
    print(json.dumps(parse_iphone_panic_log(log_ip15), indent=2, ensure_ascii=False))
