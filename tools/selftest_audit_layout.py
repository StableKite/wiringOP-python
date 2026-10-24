#!/usr/bin/env python3
"""Synthetic positive/negative tests for strict 54-module layout checks.

The upstream contract is mocked ONLY inside these isolated selftests; the
production audit's real upstream guard is never weakened or replaced.
"""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import audit_layout as layout
from upstream_contract import UpstreamContractError


def reject(action: Callable[[], object], message: str) -> None:
    try:
        action()
    except (TypeError, ValueError, SystemExit) as exc:
        if not str(exc):
            raise AssertionError("audit rejected without a diagnostic") from exc
        print("PASS_REJECT", message)
    else:
        raise AssertionError("unsafe layout was accepted: " + message)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="wiringop-layout-selftest-") as temp:
        root = Path(temp)
        # version.h is an actual root-level member of the production manifest.
        names = ["version.h"] + [f"wiringPi/module{i}.h" for i in range(53)]
        for directory in layout.MIRRORS:
            (root / directory / "wiringPi").mkdir(parents=True)
        with patch.object(layout, "ROOT", root):
            for name in names:
                for path in layout.paths_for(name):
                    path.write_text("fixture\n", encoding="utf-8")

            manifest = root / "api_manifest.json"
            manifest.write_text(
                json.dumps({"headers": [{"path": name} for name in names]}),
                encoding="utf-8",
            )
            (root / "pyproject.toml").write_text(
                '[tool.pytest.ini_options]\npython_files = ["*.py"]\n'
                'addopts = ["--import-mode=importlib"]\n',
                encoding="utf-8",
            )
            # Synthetic fixtures have no Git checkout. Real production code uses
            # the unmodified exact upstream verification call at this location.
            with (
                patch.object(layout, "verify_upstream", return_value=root),
                patch.object(layout, "verify_integrated_features"),
                patch.object(layout, "assert_no_legacy_patch_application"),
            ):
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    assert layout.main([]) == 0
                assert "LAYOUT_AUDIT_OK headers=54" in output.getvalue()
                print("PASS strict 54/54 source-test-doc-stub mirrors")
                assert layout.paths_for("version.h") == (
                    root / "src/version.cpp",
                    root / "tests/version.py",
                    root / "docs/version.md",
                    root / "stubs/version.pyi",
                )
                print("PASS root-level version.h mirrors")

                reject(lambda: layout.paths_for("./version.h"), "dot-prefix")
                reject(
                    lambda: layout.paths_for("wiringPi//module1.h"),
                    "duplicate-path-separator",
                )
                reject(lambda: layout.paths_for("../escape.h"), "relative-traversal")
                reject(lambda: layout.paths_for("/abs/escape.h"), "absolute-path")
                reject(lambda: layout.paths_for("wiringPi/a.py"), "non-header")

                missing = root / "tests" / "wiringPi/module0.py"
                missing.unlink()
                reject(lambda: layout.main([]), "missing-test-mirror")
                missing.write_text("fixture\n", encoding="utf-8")

                extra = root / "docs" / "wiringPi/foreign.md"
                extra.write_text("unexpected\n", encoding="utf-8")
                reject(lambda: layout.main([]), "extra-document")
                extra.unlink()

                stub = root / "stubs" / "wiringPi/module0.pyi"
                stub.unlink()
                reject(lambda: layout.main([]), "missing-stub")
                with contextlib.redirect_stdout(io.StringIO()) as optional_output:
                    assert layout.main(["--allow-missing-stubs"]) == 0
                assert "stubs=optional" in optional_output.getvalue()
                stub.write_text("fixture\n", encoding="utf-8")

                manifest.write_text(
                    json.dumps({"headers": [{"path": names[0]}] * 54}),
                    encoding="utf-8",
                )
                reject(lambda: layout.main([]), "duplicate-manifest-path")
                manifest.write_text(
                    json.dumps({"headers": [{"path": name} for name in names]}),
                    encoding="utf-8",
                )

                manifest.write_text(json.dumps(["not an object"]), encoding="utf-8")
                reject(lambda: layout.main([]), "manifest-not-mapping")
                manifest.write_text(
                    json.dumps({"headers": "not an array"}), encoding="utf-8"
                )
                reject(lambda: layout.main([]), "headers-not-array")
                manifest.write_text(
                    json.dumps({"headers": [None] * 54}), encoding="utf-8"
                )
                reject(lambda: layout.main([]), "header-not-mapping")
                manifest.write_text(
                    json.dumps({"headers": [{"path": 3}] * 54}), encoding="utf-8"
                )
                reject(lambda: layout.main([]), "header-path-not-string")
                manifest.write_text(
                    json.dumps({"headers": [{"path": name} for name in names]}),
                    encoding="utf-8",
                )

                with patch.object(
                    layout,
                    "verify_upstream",
                    side_effect=UpstreamContractError("pinned gitlink changed"),
                ):
                    reject(lambda: layout.main([]), "upstream-origin-mismatch")
                with contextlib.redirect_stdout(io.StringIO()) as output:
                    assert layout.main([]) == 0
                assert "LAYOUT_AUDIT_OK" in output.getvalue()
    print("LAYOUT_AUDIT_SYNTHETIC_SELFTESTS_PASS")


if __name__ == "__main__":
    main()
