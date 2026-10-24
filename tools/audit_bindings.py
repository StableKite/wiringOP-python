#!/usr/bin/env python3
"""Fail-closed audit of native bindings and tests for all 54 manifest headers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import cast

from audit_layout import paths_for

ROOT = Path(__file__).resolve().parents[1]


def _mapping(value: object, description: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise TypeError(f"{description} must be a mapping")
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


def _bindable(record: dict[str, object], context: str) -> bool:
    value = record.get("bindable", False)
    if not isinstance(value, bool):
        raise TypeError(f"{context}.bindable must be a boolean")
    return value


def _header_rows(root: Path) -> list[dict[str, object]]:
    raw: object = json.loads((root / "api_manifest.json").read_text(encoding="utf-8"))
    headers = _rows(_mapping(raw, "api_manifest.json"), "headers", "api_manifest.json")
    if len(headers) != 54:
        raise ValueError("api_manifest.json must contain exactly 54 headers")
    paths = [_name(header, "path", "header") for header in headers]
    if len(set(paths)) != len(paths):
        raise ValueError("api_manifest.json contains duplicate header paths")
    for path in paths:
        paths_for(path)  # The canonical R12 path guard, including root-level version.h.
    return headers


def _variable_tokens(variable: dict[str, object], context: str) -> list[str]:
    name = _name(variable, "python_name", context)
    c_type = _name(variable, "c_type", context)
    storage = variable.get("storage")
    if storage is not None and not isinstance(storage, str):
        raise TypeError(f"{context}.storage must be a string")
    if "*" in c_type and "[" not in c_type:
        return [f"get_{name}_address", f"set_{name}_address"]
    if storage == "static" and "struct " in c_type and "[" not in c_type:
        return [f"get_{name}", f"set_{name}"]
    return [name]


def verify_bindings(root: Path) -> tuple[int, int, int, int, int]:
    """Check unchanged token coverage; reject malformed paths/manifest shapes."""
    errors: list[str] = []
    functions = structs = fields = variables = macros = 0
    for header in _header_rows(root):
        path = _name(header, "path", "header")
        relative = Path(path)
        cpp_path = root / "src" / relative.with_suffix(".cpp")
        test_path = root / "tests" / relative.with_suffix(".py")
        cpp = cpp_path.read_text(encoding="utf-8")
        test = test_path.read_text(encoding="utf-8")
        for function in _rows(header, "functions", path):
            functions += 1
            public = _name(function, "python_name", path)
            if public not in cpp:
                errors.append(f"{path}: function binding missing {public}")
            if public not in test:
                errors.append(f"{path}: function test missing {public}")
        for structure in _rows(header, "structs", path):
            structs += 1
            structure_name = _name(structure, "python_name", path)
            if structure_name not in cpp:
                errors.append(f"{path}: class missing {structure_name}")
            for field in _rows(structure, "fields", path):
                fields += 1
                # Manifest python_name is the final public name, including _address.
                public = _name(field, "python_name", path)
                if public not in cpp:
                    errors.append(f"{path}: field missing {structure_name}.{public}")
                if public not in test:
                    errors.append(
                        f"{path}: field test missing {structure_name}.{public}"
                    )
        for variable in _rows(header, "variables", path):
            variables += 1
            public = _name(variable, "python_name", path)
            tokens = _variable_tokens(variable, path)
            for token in tokens:
                if token not in cpp:
                    errors.append(f"{path}: variable binding missing {token}")
            if not any(token in test for token in tokens):
                errors.append(f"{path}: variable test missing {public}")
        for macro in _rows(header, "macros", path):
            if not _bindable(macro, path):
                continue
            macros += 1
            public = _name(macro, "python_name", path)
            if public not in cpp:
                errors.append(f"{path}: macro binding missing {public}")
            if public not in test:
                errors.append(f"{path}: macro test missing {public}")
    if errors:
        raise SystemExit("BINDING AUDIT FAILED\n- " + "\n- ".join(errors[:100]))
    return functions, structs, fields, variables, macros


def main() -> int:
    functions, structs, fields, variables, macros = verify_bindings(ROOT)
    print(
        f"BINDING_AUDIT_OK functions={functions} structs={structs} "
        f"fields={fields} variables={variables} macros={macros}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
