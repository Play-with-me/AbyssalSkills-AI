"""Compatibility entrypoint for the isolated behavior suite (no global installs)."""
import os
import sys
import unittest
from pathlib import Path

# Force UTF-8 on Windows stdout/stderr to prevent cp1252 charmap UnicodeEncodeError on CI runners
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "tests"))

    loader = unittest.TestLoader()
    suite = loader.discover(str(root / "tests"), pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout)
    result = runner.run(suite)

    if not result.wasSuccessful():
        print("\n" + "=" * 70)
        print("FAILED TESTS BREAKDOWN:")
        for test, err in result.failures:
            print(f"FAILURE: {test}\n{err}\n")
        for test, err in result.errors:
            print(f"ERROR: {test}\n{err}\n")
        print("=" * 70)

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
