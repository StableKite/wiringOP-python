#!/usr/bin/env python3
"""Adversarial, offline contract tests for binding and stub inventory audits."""

from __future__ import annotations

import copy
import json
import tempfile
from collections.abc import Callable
from pathlib import Path

import audit_bindings
import audit_stubs


def reject(action: Callable[[], object], description: str) -> None:
    try:
        action()
    except (TypeError, ValueError, FileNotFoundError, SystemExit) as exc:
        if not str(exc):
            raise AssertionError(
                f"missing rejection explanation: {description}"
            ) from exc
        print("PASS_REJECT", description)
    else:
        raise AssertionError(f"bad audit input was accepted: {description}")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="wiringop-surface-audit-") as tmp:
        root = Path(tmp)
        headers: list[dict[str, object]] = []
        names = ["version.h", "wiringPi/wiringSerial.h"] + [
            f"wiringPi/module{n}.h" for n in range(52)
        ]
        assert len(names) == 54
        for index, header_name in enumerate(names):
            special = index == 2
            record: dict[str, object] = {
                "path": header_name,
                "functions": [{"python_name": "read_pin"}],
                "structs": (
                    [
                        {
                            "python_name": "PortState",
                            "fields": [{"python_name": "voltage_address"}],
                        }
                    ]
                    if special
                    else []
                ),
                "variables": (
                    [
                        {"python_name": "global_ptr", "c_type": "int *"},
                        {
                            "python_name": "global_struct",
                            "c_type": "struct State",
                            "storage": "static",
                        },
                        {"python_name": "value", "c_type": "int"},
                    ]
                    if special
                    else []
                ),
                "macros": (
                    [
                        {"python_name": "GPIO_INPUT", "bindable": True},
                        {"python_name": "NOT_EXPORTED", "bindable": False},
                    ]
                    if special
                    else []
                ),
            }
            headers.append(record)
            relative = Path(header_name)
            for directory, suffix in (
                ("src", ".cpp"),
                ("tests", ".py"),
                ("stubs", ".pyi"),
            ):
                target = root / directory / relative.with_suffix(suffix)
                target.parent.mkdir(parents=True, exist_ok=True)
                data = "read_pin\n"
                if directory == "stubs":
                    data = "def read_pin() -> int: ...\n"
                if special:
                    extra = (
                        "PortState voltage_address get_global_ptr_address "
                        "set_global_ptr_address get_global_struct set_global_struct "
                        "value GPIO_INPUT\n"
                    )
                    if directory == "stubs":
                        extra = "class PortState:\n    voltage_address: int\n" + extra
                    data += extra
                if index == 1 and directory == "stubs":
                    data += "class SerialPort:\n    pass\n" + " ".join(
                        audit_stubs.SERIAL_STUB_TOKENS
                    )
                target.write_text(data, encoding="utf-8")

        manifest_path = root / "api_manifest.json"
        valid: dict[str, object] = {"headers": headers}

        def write(data: object) -> None:
            manifest_path.write_text(json.dumps(data), encoding="utf-8")

        def both() -> tuple[
            tuple[int, int, int, int, int], tuple[int, int, int, int, int]
        ]:
            return audit_bindings.verify_bindings(root), audit_stubs.verify_stubs(root)

        write(valid)
        expected = (54, 1, 1, 3, 1)
        assert both() == (expected, expected)
        print(
            "PASS all 54 synthetic mirrors and function/struct/field/variable/macro modes"
        )

        func = root / "src/version.cpp"
        func.write_text("function_removed\n", encoding="utf-8")
        reject(lambda: audit_bindings.verify_bindings(root), "binding-function-missing")
        func.write_text("read_pin\n", encoding="utf-8")

        function_test = root / "tests/version.py"
        function_test.write_text("function_removed\n", encoding="utf-8")
        reject(lambda: audit_bindings.verify_bindings(root), "binding-test-missing")
        function_test.write_text("read_pin\n", encoding="utf-8")

        special_cpp = root / "src/wiringPi/module0.cpp"
        original_cpp = special_cpp.read_text(encoding="utf-8")
        special_cpp.write_text(
            original_cpp.replace("set_global_ptr_address", ""), encoding="utf-8"
        )
        reject(
            lambda: audit_bindings.verify_bindings(root),
            "pointer-setter-binding-missing",
        )
        special_cpp.write_text(
            original_cpp.replace("set_global_struct", ""), encoding="utf-8"
        )
        reject(
            lambda: audit_bindings.verify_bindings(root), "static-struct-setter-missing"
        )
        special_cpp.write_text(original_cpp.replace("GPIO_INPUT", ""), encoding="utf-8")
        reject(
            lambda: audit_bindings.verify_bindings(root),
            "exported-macro-binding-missing",
        )
        special_cpp.write_text(original_cpp, encoding="utf-8")

        special_stub = root / "stubs/wiringPi/module0.pyi"
        original_stub = special_stub.read_text(encoding="utf-8")
        special_stub.write_text(
            original_stub.replace("def read_pin", "def other"), encoding="utf-8"
        )
        reject(lambda: audit_stubs.verify_stubs(root), "stub-function-def-missing")
        special_stub.write_text(
            original_stub.replace("class PortState", "class Other"), encoding="utf-8"
        )
        reject(lambda: audit_stubs.verify_stubs(root), "stub-struct-class-missing")
        special_stub.write_text(
            original_stub.replace("get_global_ptr_address", ""), encoding="utf-8"
        )
        reject(lambda: audit_stubs.verify_stubs(root), "stub-pointer-surface-missing")
        special_stub.write_text(original_stub + "\narg41\n", encoding="utf-8")
        reject(lambda: audit_stubs.verify_stubs(root), "stub-accidental-argN")
        special_stub.write_text(original_stub, encoding="utf-8")

        serial_stub = root / "stubs/wiringPi/wiringSerial.pyi"
        original_serial = serial_stub.read_text(encoding="utf-8")
        serial_stub.write_text(
            original_serial.replace("cancel_write", ""), encoding="utf-8"
        )
        reject(lambda: audit_stubs.verify_stubs(root), "serial-advanced-stub-missing")
        serial_stub.write_text(original_serial, encoding="utf-8")

        special_stub.unlink()
        reject(lambda: audit_stubs.verify_stubs(root), "stub-file-missing")
        special_stub.write_text(original_stub, encoding="utf-8")

        write(["not", "a", "mapping"])
        reject(both, "manifest-not-mapping")
        write({"headers": "wrong type"})
        reject(both, "headers-not-list")
        write({"headers": [None] * 54})
        reject(both, "header-not-mapping")
        write({"headers": [headers[0]] * 54})
        reject(both, "duplicate-header-path")
        malformed = copy.deepcopy(headers)
        malformed[0]["path"] = "../outside.h"
        write({"headers": malformed})
        reject(both, "unsafe-header-path")
        malformed = copy.deepcopy(headers)
        malformed[0]["functions"] = "not-list"
        write({"headers": malformed})
        reject(both, "functions-not-list")
        malformed = copy.deepcopy(headers)
        malformed[2]["structs"] = [{"python_name": "PortState", "fields": [None]}]
        write({"headers": malformed})
        reject(both, "field-not-mapping")
        malformed = copy.deepcopy(headers)
        malformed[2]["macros"] = [{"python_name": "GPIO_INPUT", "bindable": "true"}]
        write({"headers": malformed})
        reject(both, "macro-bindable-not-boolean")
        malformed = copy.deepcopy(headers)
        malformed[2]["variables"] = [{"python_name": "bad", "c_type": 24}]
        write({"headers": malformed})
        reject(both, "variable-c-type-not-string")

        write(valid)
        assert both() == (expected, expected)
    print("SURFACE_AUDITS_SYNTHETIC_SELFTESTS_PASS")


if __name__ == "__main__":
    main()
