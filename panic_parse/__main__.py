"""Enables `python -m panic_parse <file.ips>`."""

import sys

from .cli import main

if __name__ == "__main__":
    sys.exit(main())
