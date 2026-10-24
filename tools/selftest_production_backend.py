#!/usr/bin/env python3
"""Negative ELF layout cases: reject missing, split, or duplicate native GPIO state."""

from __future__ import annotations

import argparse
import shutil
import tempfile
from pathlib import Path

from audit_production_backend import _safe_origin_paths, audit


def must_reject(func, marker: str) -> None:
    try:
        func()
    except RuntimeError as exc:
        assert marker in str(exc), (marker, str(exc))
        print("PASS_REJECT", marker)
    else:
        raise AssertionError("audit silently accepted unsafe layout: " + marker)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--installed-package", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--old-static-module", type=Path, default=None)
    args = parser.parse_args()
    source = args.installed_package.resolve(strict=True)
    manifest = args.manifest.resolve(strict=True)
    old_static = (
        args.old_static_module.resolve(strict=True) if args.old_static_module else None
    )
    with tempfile.TemporaryDirectory(
        prefix="wiringop-production-layout-negative-"
    ) as temp:
        base = Path(temp) / "wiringop"
        shutil.copytree(source, base)
        sidecar_source = source.parent / "wiringop_nanobind.libs"
        if sidecar_source.is_dir():
            shutil.copytree(sidecar_source, Path(temp) / sidecar_source.name)
        audit(base, manifest, with_imports=False)
        print("PASS original-production-layout")
        backend = base / "libwiringop_backend.so"
        backend_copy = backend.read_bytes()
        backend.unlink()
        must_reject(
            lambda: audit(base, manifest, with_imports=False),
            "single physically shared C library missing",
        )
        backend.write_bytes(backend_copy)
        extra = base / "wiring_pi" / "libwiringop_backend-copy.so"
        extra.write_bytes(backend_copy)
        must_reject(
            lambda: audit(base, manifest, with_imports=False), "extra backend copies"
        )
        extra.unlink()
        if sidecar_source.is_dir():
            sidecar = Path(temp) / sidecar_source.name
            external = next(iter(sidecar.iterdir()))
            imposter = sidecar / "libwiringop_backend-12345678.so.1"
            imposter.write_bytes(external.read_bytes())
            must_reject(
                lambda: audit(base, manifest, with_imports=False),
                "unexpected or duplicated GPIO backend in auditwheel sidecar",
            )
            imposter.unlink()
            extra_file = sidecar / "libunreferenced-12345678.so.1"
            extra_file.write_bytes(external.read_bytes())
            must_reject(
                lambda: audit(base, manifest, with_imports=False),
                "unreferenced auditwheel-grafted sidecar library",
            )
            extra_file.unlink()
        if old_static is not None:
            mod = base / "wiring_pi" / old_static.name
            if not mod.is_file():
                raise RuntimeError("unexpected legacy extension filename")
            original = mod.read_bytes()
            shutil.copy2(old_static, mod)
            must_reject(
                lambda: audit(base, manifest, with_imports=False),
                "missing relocatable RPATH",
            )
            mod.write_bytes(original)
        audit(base, manifest, with_imports=False)
        print("PASS restored-production-layout")
        must_reject(
            lambda: _safe_origin_paths(
                "Library runpath: [/tmp/foreign-build:$ORIGIN/..]",
                label="malicious-relocation",
                nested=True,
                has_sidecar=False,
            ),
            "unsafe/non-relative RUNPATH or RPATH",
        )
    print("PRODUCTION_SHARED_BACKEND_NEGATIVE_SELFTESTS_PASS")


if __name__ == "__main__":
    main()
