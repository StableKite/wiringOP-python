#!/usr/bin/env python3
"""Positive and fail-closed tests for the 54-module documentation audit."""

from __future__ import annotations

import contextlib
import io
import json
import tempfile
from collections.abc import Callable
from pathlib import Path
from unittest.mock import patch

import audit_docs as audit


def reject(action: Callable[[], object], reason: str) -> None:
    try:
        action()
    except (TypeError, ValueError, SystemExit) as exc:
        if not str(exc):
            raise AssertionError(f"{reason}: missing rejection diagnostic") from exc
        print("PASS_REJECT", reason)
    else:
        raise AssertionError(f"unsafe documentation accepted: {reason}")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="wiringop-doc-audit-") as temp:
        root = Path(temp)
        documents = root / "docs" / "wiringPi"
        documents.mkdir(parents=True)
        names = ["wiringPi/wiringSerial.h"] + [
            f"wiringPi/module{index}.h" for index in range(53)
        ]
        headers: list[dict[str, object]] = [
            {
                "path": name,
                "functions": [
                    {"c_name": f"c_func{index}", "python_name": f"py_func{index}"}
                ],
                "structs": [],
                "variables": [],
                "macros": [],
            }
            for index, name in enumerate(names)
        ]
        manifest = root / "api_manifest.json"
        valid = {"headers": headers}

        def write_manifest(data: object) -> None:
            manifest.write_text(json.dumps(data), encoding="utf-8")

        write_manifest(valid)
        for index, name in enumerate(names):
            doc = documents / Path(name).with_suffix(".md").name
            text = f"c_func{index} py_func{index}"
            if index == 0:
                text += " " + " ".join(audit.SERIAL_TOPICS)
            doc.write_text(text, encoding="utf-8")

        with patch.object(audit, "ROOT", root):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                assert audit.main() == 0
            assert "DOC_AUDIT_OK headers=54 symbol_references=108" in output.getvalue()
            print("PASS all 54 documented headers and exact original reference count")

            first = documents / "wiringSerial.md"
            original = first.read_text(encoding="utf-8")
            first.write_text(original.replace("py_func0", ""), encoding="utf-8")
            reject(lambda: audit.verify_documents(root), "undocumented-function")
            first.write_text(original.replace("cancel_read", ""), encoding="utf-8")
            reject(lambda: audit.verify_documents(root), "missing-serial-topic")
            first.unlink()
            reject(lambda: audit.verify_documents(root), "missing-document")
            first.write_text(original, encoding="utf-8")

            write_manifest({"headers": [headers[0]] * 54})
            reject(lambda: audit.verify_documents(root), "duplicate-manifest-header")
            write_manifest({"headers": [{"path": "../unsafe.h"}] * 54})
            reject(lambda: audit.verify_documents(root), "unsafe-manifest-path")
            write_manifest({"headers": "invalid"})
            reject(lambda: audit.verify_documents(root), "non-list-headers")
            write_manifest({"headers": [None] * 54})
            reject(lambda: audit.verify_documents(root), "non-mapping-header")
            write_manifest(valid)

            bad = [dict(item) for item in headers]
            bad[0]["functions"] = "invalid"
            write_manifest({"headers": bad})
            reject(lambda: audit.verify_documents(root), "non-list-functions")
            bad[0]["functions"] = [{"c_name": 42, "python_name": "py_func0"}]
            write_manifest({"headers": bad})
            reject(lambda: audit.verify_documents(root), "wrong-symbol-type")
            bad[0]["functions"] = headers[0]["functions"]
            bad[0]["structs"] = [
                {
                    "c_name": "struct0",
                    "python_name": "Class0",
                    "fields": [{"name": 42, "python_name": "field0"}],
                }
            ]
            write_manifest({"headers": bad})
            reject(lambda: audit.verify_documents(root), "malformed-struct-field")
            write_manifest(valid)

            # Preserve original auditing of struct fields, variables and macros.
            modified = [dict(item) for item in headers]
            modified[1]["structs"] = [
                {
                    "c_name": "CSensor",
                    "python_name": "Sensor",
                    "fields": [{"name": "bus", "python_name": "bus_address"}],
                }
            ]
            modified[1]["variables"] = [
                {"c_name": "gpio_mode", "python_name": "gpioMode"}
            ]
            modified[1]["macros"] = [{"c_name": "GPIO_INPUT"}]
            write_manifest({"headers": modified})
            second = documents / "module0.md"
            baseline = second.read_text(encoding="utf-8")
            reject(
                lambda: audit.verify_documents(root),
                "missing-struct-variable-macro-docs",
            )
            second.write_text(
                baseline
                + " CSensor Sensor bus bus_address gpio_mode gpioMode GPIO_INPUT",
                encoding="utf-8",
            )
            assert audit.verify_documents(root) == (54, 115)
            second.write_text(baseline, encoding="utf-8")
            write_manifest(valid)
            assert audit.verify_documents(root) == (54, 108)

    print("DOC_AUDIT_SYNTHETIC_SELFTESTS_PASS")


if __name__ == "__main__":
    main()
