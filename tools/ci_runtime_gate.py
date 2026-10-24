#!/usr/bin/env python3
"""Fail-closed newest-stable free-threaded process + installed wheel test gate.

The same interpreter imports all 54 compiled modules and executes every mirror
pytest test.  GIL/JIT checks occur before imports, during tests, and afterward.
This script is not a substitute for platform-specific native build/ABI gates.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import re
import subprocess
import sys
import sysconfig
from dataclasses import dataclass, field
from importlib.machinery import EXTENSION_SUFFIXES
from pathlib import Path
from typing import Any

MIN_PYTHON = (3, 14)
MIN_TESTS = 324
EXPECTED_MODULES = 54


class RuntimeGateError(RuntimeError):
    """A required runtime property was absent or failed closed."""


def snapshot(stage: str) -> dict[str, object]:
    version = sys.version_info
    if (
        sys.implementation.name != "cpython"
        or version[:2] < MIN_PYTHON
        or version.releaselevel != "final"
    ):
        raise RuntimeGateError("runtime is not final supported CPython >=3.14")
    if sysconfig.get_config_var("Py_GIL_DISABLED") != 1:
        raise RuntimeGateError(f"{stage}: interpreter was not built free-threaded")
    gil_status = getattr(sys, "_is_gil_enabled", None)
    if not callable(gil_status) or gil_status():
        raise RuntimeGateError(f"{stage}: GIL reenabled or cannot be verified")
    if os.environ.get("PYTHON_GIL") != "0" or os.environ.get("PYTHON_JIT") != "1":
        raise RuntimeGateError(f"{stage}: missing required GIL/JIT environment policy")
    jit = getattr(sys, "_jit", None)
    if jit is None:
        jit_mode = "unavailable"
    else:
        available = getattr(jit, "is_available", None)
        enabled = getattr(jit, "is_enabled", None)
        if not callable(available) or not callable(enabled):
            raise RuntimeGateError(f"{stage}: JIT API is incomplete")
        if available():
            if not enabled():
                raise RuntimeGateError(f"{stage}: JIT available but disabled")
            jit_mode = "enabled"
        else:
            jit_mode = "unavailable"
    return {
        "stage": stage,
        "python": f"{version.major}.{version.minor}.{version.micro}",
        "free_threaded": True,
        "gil_off": True,
        "jit": jit_mode,
        "pid": os.getpid(),
    }


def exact_git_head(expected: str) -> str:
    if not re.fullmatch(r"[0-9a-f]{40}", expected):
        raise RuntimeGateError("missing/invalid expected event source SHA")
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode or result.stdout.strip() != expected:
        raise RuntimeGateError("checked-out source differs from exact GitHub event SHA")
    return expected


def mirror_test_paths(manifest: dict[str, Any]) -> set[str]:
    entries = manifest.get("headers")
    if not isinstance(entries, list) or len(entries) != EXPECTED_MODULES:
        raise RuntimeGateError("exact 54-header manifest missing")
    result: set[str] = set()
    for item in entries:
        if not isinstance(item, dict) or not isinstance(item.get("path"), str):
            raise RuntimeGateError("malformed manifest entry")
        result.add((Path("tests") / Path(item["path"]).with_suffix(".py")).as_posix())
    if len(result) != EXPECTED_MODULES:
        raise RuntimeGateError("duplicate mirrored test path in manifest")
    return result


def installed_extension_origins(manifest: dict[str, Any]) -> dict[str, str]:
    names = [h.get("python_module") for h in manifest["headers"]]
    if (
        len(names) != EXPECTED_MODULES
        or any(not isinstance(n, str) for n in names)
        or len(set(names)) != EXPECTED_MODULES
    ):
        raise RuntimeGateError("invalid 54-module name inventory")
    prefix = Path(sys.prefix).resolve()
    result: dict[str, str] = {}
    for name in names:
        module = importlib.import_module(name)
        origin_text = getattr(module, "__file__", None)
        if not isinstance(origin_text, str) or not any(
            origin_text.endswith(ext) for ext in EXTENSION_SUFFIXES
        ):
            raise RuntimeGateError(
                f"{name}: extension was not loaded from a native binary"
            )
        origin = Path(origin_text).resolve()
        if not origin.is_relative_to(prefix):
            raise RuntimeGateError(
                f"{name}: extension loaded outside installed interpreter environment"
            )
        snapshot(f"after_import:{name}")
        result[name] = str(origin)
    return result


@dataclass
class PytestRecorder:
    collected: list[str] = field(default_factory=list)
    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)
    runtime_checks: int = 0

    def pytest_collection_finish(self, session: Any) -> None:
        self.collected = [item.nodeid for item in session.items]

    def pytest_runtest_setup(self, item: Any) -> None:
        snapshot(f"pytest_setup:{item.nodeid}")
        self.runtime_checks += 1

    def pytest_runtest_logreport(self, report: Any) -> None:
        # Pytest defaults to treating XPASS (non-strict xfail) as success.
        # Any xfail marker would weaken the mandatory all-tests-pass contract.
        if hasattr(report, "wasxfail"):
            self.failed.append(report.nodeid)
        elif report.skipped:
            self.skipped.append(report.nodeid)
        elif report.failed:
            self.failed.append(report.nodeid)
        elif report.when == "call" and report.passed:
            self.passed.append(report.nodeid)


def validate_test_results(
    recorder: PytestRecorder, result: int, expected_paths: set[str]
) -> None:
    if result != 0 or recorder.failed or recorder.skipped:
        raise RuntimeGateError(
            "pytest failed, skipped, xfailed, or reported setup/teardown errors"
        )
    if len(recorder.collected) < MIN_TESTS or len(recorder.collected) != len(
        set(recorder.collected)
    ):
        raise RuntimeGateError("required full test count/uniqueness missing")
    if len(recorder.passed) != len(recorder.collected) or set(recorder.passed) != set(
        recorder.collected
    ):
        raise RuntimeGateError("not every collected test passed exactly once")
    if recorder.runtime_checks != len(recorder.collected):
        raise RuntimeGateError("GIL/JIT policy not checked at every test setup")
    tested_paths = {
        name.split("::", 1)[0].replace("\\", "/") for name in recorder.collected
    }
    if not expected_paths.issubset(tested_paths):
        raise RuntimeGateError("not all 54 mirrored test files were collected")


def execute(args: argparse.Namespace) -> dict[str, object]:
    head = exact_git_head(args.source_sha)
    before = snapshot("before_all_imports")
    report: dict[str, object] = {
        "schema": 1,
        "status": "UNVERIFIED",
        "head_sha": head,
        "before": before,
    }
    if not args.installed:
        report["status"] = "RUNTIME_PREFLIGHT_PASS"
        return report
    if args.wheel is None or not args.wheel.is_file():
        raise RuntimeGateError("installed test gate requires exact wheel bytes")
    wheel = args.wheel.resolve()
    report["wheel"] = {
        "name": wheel.name,
        "bytes": wheel.stat().st_size,
        "sha256": hashlib.sha256(wheel.read_bytes()).hexdigest(),
    }
    manifest = json.loads(Path("api_manifest.json").read_text(encoding="utf-8"))
    expected_paths = mirror_test_paths(manifest)
    origins = installed_extension_origins(manifest)
    report["modules"] = {"count": len(origins), "origins": origins}
    report["after_all_imports"] = snapshot("after_all_imports")
    import pytest

    recorder = PytestRecorder()
    result = int(
        pytest.main(
            [
                "tests",
                "-q",
                "--import-mode=importlib",
                "--strict-config",
                "--strict-markers",
            ],
            plugins=[recorder],
        )
    )
    report["after_pytest"] = snapshot("after_pytest")
    report["pytest"] = {
        "exit_code": result,
        "collected": len(recorder.collected),
        "passed": len(recorder.passed),
        "failed": recorder.failed,
        "skipped": recorder.skipped,
        "runtime_checks": recorder.runtime_checks,
    }
    validate_test_results(recorder, result, expected_paths)
    report["status"] = "INSTALLED_WHEEL_SAME_PROCESS_TEST_PASS"
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--installed", action="store_true")
    parser.add_argument("--wheel", type=Path)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = execute(args)
    except (
        OSError,
        RuntimeError,
        ValueError,
        TypeError,
        ImportError,
        AssertionError,
    ) as exc:
        result = {
            "schema": 1,
            "status": "FAIL",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
        rc = 1
    else:
        rc = 0
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        result["status"],
        json.dumps(
            {k: v for k, v in result.items() if k not in ("modules",)}, sort_keys=True
        ),
    )
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
