"""Compatibility entrypoint for the isolated behavior suite (no global installs)."""
import io
import os
import sys
import unittest
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "tests"))
    suite = unittest.defaultTestLoader.discover(str(root / "tests"), pattern="test_*.py")

    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=2)
    result = runner.run(suite)

    output = stream.getvalue()
    sys.stdout.write(output)
    sys.stdout.flush()

    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        try:
            with open(summary_file, "a", encoding="utf-8") as f:
                f.write("### Test Results\n```\n" + output + "\n```\n")
        except Exception:
            pass

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
