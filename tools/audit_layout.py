#!/usr/bin/env python3
"""Fail-closed validation of the 54 mirrored wiringOP source/API trees."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
from typing import cast

from upstream_contract import (
    UpstreamContractError,
    assert_no_legacy_patch_application,
    verify_integrated_features,
    verify_upstream,
)

ROOT = Path(__file__).resolve().parents[1]
MIRRORS = ("src", "tests", "docs", "stubs")
SUFFIXES = (".cpp", ".py", ".md", ".pyi")


def paths_for(header: str) -> tuple[Path, Path, Path, Path]:
    """Map only an ordinary, relative .h path into the four mirror trees."""
    parsed = PurePosixPath(header)
    if (
        not header
        or header.startswith("/")
        or "\\" in header
        or parsed.suffix != ".h"
        or not parsed.parts
        or parsed.as_posix() != header
        or "\0" in header
        or any(part in ("", ".", "..") for part in parsed.parts)
    ):
        raise ValueError(f"unsafe or non-header manifest path: {header!r}")
    relative = Path(*parsed.parts).with_suffix("")
    return (
        ROOT / "src" / relative.with_suffix(".cpp"),
        ROOT / "tests" / relative.with_suffix(".py"),
        ROOT / "docs" / relative.with_suffix(".md"),
        ROOT / "stubs" / relative.with_suffix(".pyi"),
    )


def _header_paths(manifest_path: Path) -> list[str]:
    raw: object = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError("api_manifest.json must be a mapping")
    manifest = cast(dict[str, object], raw)
    rows = manifest.get("headers")
    if not isinstance(rows, list):
        raise TypeError("api_manifest.json must contain a headers array")

    headers: list[str] = []
    for row in cast(list[object], rows):
        if not isinstance(row, dict):
            raise TypeError("each manifest header must be a mapping")
        entry = cast(dict[str, object], row)
        path = entry.get("path")
        if not isinstance(path, str):
            raise TypeError("manifest header path must be a string")
        paths_for(path)
        headers.append(path)
    if len(headers) != 54 or len(set(headers)) != 54:
        raise ValueError("manifest must contain exactly 54 distinct header paths")
    return headers


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--allow-missing-stubs", action="store_true")
    options = parser.parse_args(argv)
    headers = _header_paths(ROOT / "api_manifest.json")
    errors: list[str] = []
    expected: dict[str, set[str]] = {directory: set() for directory in MIRRORS}

    for header in headers:
        for kind, path in zip(MIRRORS, paths_for(header), strict=True):
            relative = path.relative_to(ROOT).as_posix()
            expected[kind].add(relative)
            if kind == "stubs" and options.allow_missing_stubs:
                continue
            if not path.is_file():
                errors.append(f"missing {kind}: {relative}")

    # Preserve the established exact-inventory policy for source/tests/docs.
    for kind, suffix in zip(MIRRORS[:3], SUFFIXES[:3], strict=True):
        actual = {
            path.relative_to(ROOT).as_posix()
            for path in (ROOT / kind).rglob(f"*{suffix}")
            if path.is_file() and "__pycache__" not in path.parts
        }
        extra = sorted(actual - expected[kind])
        missing = sorted(expected[kind] - actual)
        if extra:
            errors.append(f"extra {kind}: {extra[:10]}")
        if missing:
            errors.append(f"missing mirrored {kind}: {missing[:10]}")

    prefixed = sorted((ROOT / "tests").rglob("test_*.py"))
    if prefixed:
        names = ", ".join(str(path.relative_to(ROOT)) for path in prefixed)
        errors.append("test_ prefix files: " + names)

    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    if 'python_files = ["*.py"]' not in pyproject:
        errors.append('pytest python_files must be ["*.py"]')
    if "--import-mode=importlib" not in pyproject:
        errors.append("pytest must use --import-mode=importlib")

    try:
        source = verify_upstream(ROOT)
        verify_integrated_features(source)
        assert_no_legacy_patch_application(ROOT)
    except (UpstreamContractError, OSError) as exc:
        errors.append(f"upstream contract failed: {exc}")

    if errors:
        raise SystemExit("LAYOUT AUDIT FAILED\n- " + "\n- ".join(errors))
    stub_count: str | int = "optional" if options.allow_missing_stubs else 54
    print(
        f"LAYOUT_AUDIT_OK headers={len(headers)} "
        f"src=54 tests=54 docs=54 stubs={stub_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
