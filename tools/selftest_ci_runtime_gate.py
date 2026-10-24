#!/usr/bin/env python3
"""Offline negative cases; NOT a substitute for actual free-threaded Python."""

from __future__ import annotations

import os
from collections import namedtuple
from types import SimpleNamespace
from unittest import mock

import ci_runtime_gate as gate


def expect_reject(
    message: str, recorder: gate.PytestRecorder, result: int, paths: set[str]
) -> None:
    try:
        gate.validate_test_results(recorder, result, paths)
    except gate.RuntimeGateError:
        print("PASS_REJECT", message)
    else:
        raise AssertionError("invalid evidence was accepted: " + message)


def main() -> int:
    paths = {f"tests/module_{n}.py" for n in range(54)}
    collected = [f"tests/module_{i % 54}.py::test_{i}" for i in range(324)]
    r = gate.PytestRecorder(
        collected=collected, passed=collected.copy(), runtime_checks=324
    )
    gate.validate_test_results(r, 0, paths)
    print("PASS simulated-positive-reporter-shape-only")
    expect_reject(
        "rejected-323-tests",
        gate.PytestRecorder(
            collected=collected[:-1], passed=collected[:-1], runtime_checks=323
        ),
        0,
        paths,
    )
    expect_reject(
        "rejected-skipped",
        gate.PytestRecorder(
            collected=collected,
            passed=collected,
            skipped=[collected[0]],
            runtime_checks=324,
        ),
        0,
        paths,
    )
    xp = gate.PytestRecorder(
        collected=collected, passed=collected[1:], runtime_checks=324
    )
    xp.pytest_runtest_logreport(
        SimpleNamespace(
            nodeid=collected[0],
            when="call",
            passed=True,
            skipped=False,
            failed=False,
            wasxfail="known issue",
        )
    )
    expect_reject("rejected-xpass-even-when-pytest-exits-zero", xp, 0, paths)
    expect_reject("rejected-bad-exit-code", r, 1, paths)
    expect_reject("rejected-missing-mirror", r, 0, paths | {"tests/missing.py"})
    expect_reject(
        "rejected-runtime-check-missing",
        gate.PytestRecorder(collected=collected, passed=collected, runtime_checks=323),
        0,
        paths,
    )
    Info = namedtuple("Info", ("major", "minor", "micro", "releaselevel", "serial"))
    final = Info(3, 15, 1, "final", 0)
    with (
        mock.patch.object(gate.sys, "version_info", final),
        mock.patch.object(gate.sysconfig, "get_config_var", return_value=1),
        mock.patch.object(gate.sys, "_is_gil_enabled", lambda: False, create=True),
        mock.patch.dict(os.environ, {"PYTHON_GIL": "0", "PYTHON_JIT": "1"}),
    ):
        with mock.patch.object(
            gate.sys,
            "_jit",
            SimpleNamespace(is_available=lambda: True, is_enabled=lambda: True),
            create=True,
        ):
            good = gate.snapshot("synthetic-test")
            assert good["jit"] == "enabled" and good["gil_off"]
        print("PASS synthetic-jit-enabled-shape-only")
        with mock.patch.object(
            gate.sys,
            "_jit",
            SimpleNamespace(is_available=lambda: False, is_enabled=lambda: False),
            create=True,
        ):
            unavailable = gate.snapshot("synthetic-test")
            assert unavailable["jit"] == "unavailable"
        print("PASS synthetic-jit-unavailable-shape-only")
        with mock.patch.object(
            gate.sys,
            "_jit",
            SimpleNamespace(is_available=lambda: True, is_enabled=lambda: False),
            create=True,
        ):
            try:
                gate.snapshot("synthetic-test")
            except gate.RuntimeGateError as exc:
                assert "JIT available but disabled" in str(exc)
            else:
                raise AssertionError("disabled available JIT accepted")
        print("PASS_REJECT disabled-available-JIT")
        with mock.patch.object(gate.sys, "_is_gil_enabled", lambda: True, create=True):
            try:
                gate.snapshot("synthetic-test")
            except gate.RuntimeGateError as exc:
                assert "GIL reenabled" in str(exc)
            else:
                raise AssertionError("re-enabled GIL accepted")
        print("PASS_REJECT gil-reenabled")
        with mock.patch.object(gate.sysconfig, "get_config_var", return_value=0):
            try:
                gate.snapshot("synthetic-test")
            except gate.RuntimeGateError as exc:
                assert "not built free-threaded" in str(exc)
            else:
                raise AssertionError("normal GIL CPython accepted")
        print("PASS_REJECT normal-build")
    with mock.patch.object(gate.sys, "version_info", Info(3, 15, 1, "candidate", 1)):
        try:
            gate.snapshot("selftest")
        except gate.RuntimeGateError as exc:
            assert "not final supported" in str(exc)
        else:
            raise AssertionError("RC/pre-release must fail")
    print("PASS_REJECT prerelease-Python")
    with mock.patch.object(gate.sys, "version_info", Info(3, 13, 5, "final", 0)):
        try:
            gate.snapshot("selftest")
        except gate.RuntimeGateError as exc:
            assert "not final supported" in str(exc)
        else:
            raise AssertionError("noneligible Python must fail")
    print("PASS_REJECT noneligible-Python")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
