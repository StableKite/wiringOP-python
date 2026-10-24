#!/usr/bin/env python3
"""Fail-closed static stub audit for every pinned native API surface."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import cast

from audit_layout import paths_for

ROOT = Path(__file__).resolve().parents[1]
SERIAL_STUB_TOKENS = (
    "class SerialPort",
    "cancel_read",
    "cancel_write",
    "read_into",
    "readinto",
    "rs485_mode",
    "rx_trigger",
)


def _mapping(value: object, context: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{context} must be a mapping")
    return cast(dict[str, object], value)


def _rows(record: dict[str, object], key: str, context: str) -> list[dict[str, object]]:
    value = record.get(key, [])
    if not isinstance(value, list):
        raise TypeError(f"{context}.{key} must be a list")
    return [
        _mapping(item, f"{context}.{key}[{index}]")
        for index, item in enumerate(cast(list[object], value))
    ]


def _name(record: dict[str, object], key: str, context: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value:
        raise TypeError(f"{context}.{key} must be a nonempty string")
    return value


def _bindable(macro: dict[str, object], context: str) -> bool:
    value = macro.get("bindable", False)
    if not isinstance(value, bool):
        raise TypeError(f"{context}.bindable must be a boolean")
    return value


def _headers(root: Path) -> list[dict[str, object]]:
    raw: object = json.loads((root / "api_manifest.json").read_text(encoding="utf-8"))
    headers = _rows(_mapping(raw, "api_manifest.json"), "headers", "api_manifest.json")
    if len(headers) != 54:
        raise ValueError("api_manifest.json must contain exactly 54 headers")
    names = [_name(header, "path", "header") for header in headers]
    if len(set(names)) != 54:
        raise ValueError("api_manifest.json contains duplicate header paths")
    for path in names:
        paths_for(path)
    return headers


def _variable_tokens(variable: dict[str, object], path: str) -> list[str]:
    public = _name(variable, "python_name", path)
    c_type = _name(variable, "c_type", path)
    storage = variable.get("storage")
    if storage is not None and not isinstance(storage, str):
        raise TypeError(f"{path}.storage must be a string")
    if "*" in c_type and "[" not in c_type:
        return [f"get_{public}_address", f"set_{public}_address"]
    if storage == "static" and "struct " in c_type and "[" not in c_type:
        return [f"get_{public}", f"set_{public}"]
    return [public]


def verify_stubs(root: Path) -> tuple[int, int, int, int, int]:
    """Keep the existing public symbol matching and reject malformed metadata."""
    errors: list[str] = []
    functions = classes = fields = variables = macros = 0
    for header in _headers(root):
        path = _name(header, "path", "header")
        stub_path = root / "stubs" / Path(path).with_suffix(".pyi")
        if not stub_path.is_file():
            errors.append(f"missing {stub_path.relative_to(root)}")
            continue
        source = stub_path.read_text(encoding="utf-8")
        if re.search(r"\barg\d+\b", source):
            errors.append(f"{path}: accidental argN name")
        for function in _rows(header, "functions", path):
            functions += 1
            public = _name(function, "python_name", path)
            if not re.search(rf"\bdef\s+{re.escape(public)}\s*\(", source):
                errors.append(f"{path}: missing def {public}")
        for structure in _rows(header, "structs", path):
            classes += 1
            name = _name(structure, "python_name", path)
            if not re.search(rf"\bclass\s+{re.escape(name)}\b", source):
                errors.append(f"{path}: missing class {name}")
            for field in _rows(structure, "fields", path):
                fields += 1
                public = _name(field, "python_name", path)
                if public not in source:
                    errors.append(f"{path}: missing field {name}.{public}")
        for variable in _rows(header, "variables", path):
            variables += 1
            for token in _variable_tokens(variable, path):
                if token not in source:
                    errors.append(f"{path}: missing variable surface {token}")
        for macro in _rows(header, "macros", path):
            if not _bindable(macro, path):
                continue
            macros += 1
            name = _name(macro, "python_name", path)
            if name not in source:
                errors.append(f"{path}: missing macro {name}")
        if path == "wiringPi/wiringSerial.h":
            for token in SERIAL_STUB_TOKENS:
                if token not in source:
                    errors.append(f"wiringSerial stub missing {token}")
    if errors:
        raise SystemExit("STUB AUDIT FAILED\n- " + "\n- ".join(errors[:120]))
    return functions, classes, fields, variables, macros


def main() -> int:
    functions, classes, fields, variables, macros = verify_stubs(ROOT)
    print(
        f"STUB_AUDIT_OK functions={functions} classes={classes} "
        f"fields={fields} variables={variables} macros={macros}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
