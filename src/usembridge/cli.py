from __future__ import annotations

import argparse
import platform
import sys

from . import __version__
from .schema import load_and_validate
from .solvers.semantic_gap import run_semantic_gap_demo


def _doctor() -> int:
    print(f"U-SemBridge {__version__}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {platform.platform()}")
    try:
        import z3

        print(f"Z3: {z3.get_version_string()}")
    except Exception as exc:
        print(f"Z3: ERROR ({exc})")
        return 1
    print("Core environment: OK")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(prog="usembridge")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    validate = sub.add_parser("validate-cir")
    validate.add_argument("path")
    sub.add_parser("semantic-gap-demo")
    args = parser.parse_args()

    if args.command == "doctor":
        raise SystemExit(_doctor())
    if args.command == "validate-cir":
        load_and_validate(args.path)
        print("CIR valid")
        return
    if args.command == "semantic-gap-demo":
        print(run_semantic_gap_demo())
        return
