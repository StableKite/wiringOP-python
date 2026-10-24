#!/usr/bin/env python3
"""Verify every documented C/Python API symbol against the pinned manifest.

The manifest path inventory is checked by the strict layout audit before any
file access; missing files, invalid schemas and undocumented tokens fail closed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from audit_layout import paths_for

ROOT = Path(__file__).resolve().parents[1]
SERIAL_TOPICS = (
    "SerialPort",
    "RS-485",
    "RK3588",
    "cancel_read",
    "cancel_write",
    "rx_trigger",
)


def _mapping(value: object, description: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{description} must be a mapping")
    return cast(dict[str, object], value)


def _rows(
    record: dict[str, object], key: str, description: str
) -> list[dict[str, object]]:
    value = record.get(key, [])
    if not isinstance(value, list):
        raise TypeError(f"{description}.{key} must be a list")
    return [
        _mapping(item, f"{description}.{key}[{index}]")
        for index, item in enumerate(cast(list[object], value))
    ]


def _name(record: dict[str, object], key: str, description: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise TypeError(f"{description}.{key} must be a nonempty string")
    return value


def _required_symbols(header: dict[str, object], path: str) -> list[str]:
    required: list[str] = []
    for function in _rows(header, "functions", path):
        required.extend(
            (_name(function, "c_name", path), _name(function, "python_name", path))
        )
    for structure in _rows(header, "structs", path):
        required.extend(
            (_name(structure, "c_name", path), _name(structure, "python_name", path))
        )
        for field in _rows(structure, "fields", path):
            required.extend(
                (_name(field, "name", path), _name(field, "python_name", path))
            )
    for variable in _rows(header, "variables", path):
        required.extend(
            (_name(variable, "c_name", path), _name(variable, "python_name", path))
        )
    for macro in _rows(header, "macros", path):
        required.append(_name(macro, "c_name", path))
    return required


def verify_documents(root: Path) -> tuple[int, int]:
    """Return validated (header count, unique-per-header symbol references)."""
    manifest_path = root / "api_manifest.json"
    raw: object = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest = _mapping(raw, "api_manifest.json")
    headers = _rows(manifest, "headers", "api_manifest.json")
    if len(headers) != 54:
        raise ValueError("manifest must declare exactly 54 documented headers")
    names = [_name(header, "path", "manifest header") for header in headers]
    if len(set(names)) != 54:
        raise ValueError("manifest must declare 54 distinct documented headers")
    # Reuse the R11 strict path policy, not a looser document-specific variant.
    for name in names:
        paths_for(name)

    errors: list[str] = []
    symbol_count = 0
    for path, header in zip(names, headers, strict=True):
        document_path = root / "docs" / Path(path).with_suffix(".md")
        if not document_path.is_file():
            errors.append(f"{path}: missing documentation file")
            continue
        documentation = document_path.read_text(encoding="utf-8")
        # The original audit counts distinct symbol references per header.
        for symbol in dict.fromkeys(_required_symbols(header, path)):
            symbol_count += 1
            if symbol not in documentation:
                errors.append(f"{path}: undocumented {symbol}")
        if path == "wiringPi/wiringSerial.h":
            for topic in SERIAL_TOPICS:
                if topic not in documentation:
                    errors.append(f"wiringSerial docs missing advanced topic {topic}")

    if errors:
        raise SystemExit("DOC AUDIT FAILED\n- " + "\n- ".join(errors[:100]))
    return len(headers), symbol_count


def main() -> int:
    headers, symbols = verify_documents(ROOT)
    print(f"DOC_AUDIT_OK headers={headers} symbol_references={symbols}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
