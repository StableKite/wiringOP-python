#!/usr/bin/env python3
"""Fail-closed audit of a Linux-installed physical wiringOP backend layout.

Run under the same CPython ABI used to build the extensions. No GPIO/UART
functions are invoked: the audit imports modules and inspects ELF symbols only.
"""

from __future__ import annotations

import argparse
import ctypes
import hashlib
import importlib
import json
import re
import subprocess
import sys
import sysconfig
from pathlib import Path


def command(*args: str) -> str:
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT)


def fail(message: str) -> None:
    raise RuntimeError("PRODUCTION_SHARED_BACKEND_AUDIT_FAILED: " + message)


def _safe_origin_paths(
    dynamic: str, *, label: str, nested: bool, has_sidecar: bool
) -> list[str]:
    # auditwheel can replace DT_RUNPATH with DT_RPATH and graft system
    # dependencies into a dist-name.libs sibling directory. Both ELF tags
    # resolve relative $ORIGIN locations; absolute/foreign paths are banned.
    entries = re.findall(r"Library (?:runpath|rpath): \[([^]]+)\]", dynamic)
    if len(entries) != 1:
        fail("missing relocatable RPATH or RUNPATH: " + label)
    paths = entries[0].split(":")
    allowed = {"$ORIGIN", "$ORIGIN/.."}
    if has_sidecar:
        allowed.add(
            "$ORIGIN/../../wiringop_nanobind.libs"
            if nested
            else "$ORIGIN/../wiringop_nanobind.libs"
        )
    required = "$ORIGIN/.." if nested else "$ORIGIN"
    if (
        required not in paths
        or not paths
        or len(paths) != len(set(paths))
        or any(x not in allowed for x in paths)
    ):
        fail("unsafe/non-relative RUNPATH or RPATH: " + label)
    return paths


def _audit_sidecar(root: Path, native: list[Path]) -> dict[str, str]:
    """Allow only used, SHA-hashed auditwheel-grafted system libraries."""
    sidecar = root.parent / "wiringop_nanobind.libs"
    if not sidecar.exists():
        return {}
    if not sidecar.is_dir() or sidecar.is_symlink():
        fail("auditwheel sidecar is not an ordinary directory")
    members = list(sidecar.iterdir())
    if not members or any(not f.is_file() or f.is_symlink() for f in members):
        fail("auditwheel sidecar contains missing/unsafe file")
    needed = set()
    for path in native:
        dyn = command("readelf", "-d", str(path))
        needed.update(re.findall(r"Shared library: \[([^]]+)\]", dyn))
    # A bundled DSO can itself require another bundled DSO. Count only the
    # reachable dependency closure, not merely the first-level DT_NEEDED set.
    by_name = {f.name: f for f in members}
    pending = list(needed)
    traversed = set()
    while pending:
        item = pending.pop()
        if item in traversed:
            continue
        traversed.add(item)
        if item in by_name:
            extra = command("readelf", "-d", str(by_name[item]))
            deps = re.findall(r"Shared library: \[([^]]+)\]", extra)
            needed.update(deps)
            pending.extend(deps)
    hashes = {}
    for f in members:
        if "wiringop_backend" in f.name.lower() or not re.fullmatch(
            r"lib[A-Za-z0-9_+.-]+-[0-9a-f]{8}\.so(?:\.[0-9.]+)?", f.name
        ):
            fail("unexpected or duplicated GPIO backend in auditwheel sidecar")
        if f.name not in needed:
            fail("unreferenced auditwheel-grafted sidecar library: " + f.name)
        if not f.read_bytes().startswith(b"\x7fELF"):
            fail("auditwheel-grafted library is not ELF")
        hashes[f.name] = hashlib.sha256(f.read_bytes()).hexdigest()
    return hashes


def audit(
    package: Path,
    manifest: Path,
    *,
    with_imports: bool,
    require_free_threaded: bool = False,
) -> dict[str, object]:
    """Do not accept a separate physical C singleton per nanobind module."""
    checkpoints = []
    if require_free_threaded:
        if not with_imports:
            fail("free-threaded verification requires installed wheel imports")
        from ci_runtime_gate import snapshot

        checkpoints.append(snapshot("physical_before_all_imports"))
    root = package.resolve(strict=True)
    if sys.platform != "linux":
        fail("physical wiringOP artifact validation requires Linux")
    if not root.is_dir() or root.name != "wiringop":
        fail("expected installed wiringop/ package directory")
    if any(p.is_symlink() for p in root.rglob("*")):
        fail("installed artifact contains symlink")
    data = json.loads(manifest.read_text(encoding="utf-8"))
    modules = sorted({h["python_module"] for h in data["headers"]})
    if len(modules) != 54 or len(data["headers"]) != 54:
        fail("expected exactly 54 manifest modules")
    suffix = sysconfig.get_config_var("EXT_SUFFIX")
    if not suffix or not suffix.endswith(".so"):
        fail("current Python ABI is not a native Linux extension ABI")
    backend = root / "libwiringop_backend.so"
    if not backend.is_file():
        fail("single physically shared C library missing from wheel")
    libraries = sorted(root.rglob("libwiringop_backend*"))
    if libraries != [backend]:
        fail("extra backend copies or variants inside installed artifact")
    all_native = sorted(root.rglob("*.so"))
    sidecar_hashes = _audit_sidecar(root, all_native)
    has_sidecar = bool(sidecar_hashes)
    expected_native = {backend}
    needed = []
    unneeded = []
    hashes = {}
    for name in modules:
        if not name.startswith("wiringop."):
            fail("foreign Python module in manifest")
        p = root.joinpath(*name.split(".")[1:]).with_suffix(suffix)
        if not p.is_file():
            fail("missing ABI-matched extension: " + name)
        expected_native.add(p)
        dyn = command("readelf", "-d", str(p))
        _safe_origin_paths(
            dyn, label=name, nested=p.parent != root, has_sidecar=has_sidecar
        )
        defs = command("nm", "-D", "--defined-only", str(p))
        for physical_global in ("wiringPiNodes", "_wiringPiGpio", "wiringPiSetup"):
            if re.search(r"\b" + physical_global + r"\s*$", defs, re.MULTILINE):
                fail("extension embeds native C state: " + name)
        if "Shared library: [libwiringop_backend.so]" in dyn:
            needed.append(name)
        else:
            unneeded.append(name)
        hashes[p.relative_to(root).as_posix()] = hashlib.sha256(
            p.read_bytes()
        ).hexdigest()
    if set(all_native) != expected_native:
        fail("unexpected/duplicate native libraries")
    if has_sidecar:
        backend_dyn = command("readelf", "-d", str(backend))
        backend_paths = re.findall(
            r"Library (?:runpath|rpath): \[([^]]+)\]", backend_dyn
        )
        if backend_paths != ["$ORIGIN/../wiringop_nanobind.libs"]:
            fail("shared GPIO backend cannot resolve auditwheel sidecar safely")
    if (
        "wiringop.wiring_pi.wiring_pi" not in needed
        or "wiringop.wiring_pi.wiring_pi_i2c" not in needed
    ):
        fail("core C API modules do not depend on one shared backend")
    if len(needed) < 2:
        fail("shared physical backend has fewer than two C API consumers")
    exported = command("nm", "-D", "--defined-only", str(backend))
    for symbol in ("wiringPiNodes", "_wiringPiGpio", "wiringPiSetup"):
        if not re.search(r"\b" + symbol + r"\s*$", exported, re.MULTILINE):
            fail("physical shared backend lacks required state symbol " + symbol)
    if with_imports:
        if str(root.parent) not in sys.path:
            sys.path.insert(0, str(root.parent))
        for name in modules:
            imported = importlib.import_module(name)
            if Path(imported.__file__).resolve() != root.joinpath(
                *name.split(".")[1:]
            ).with_suffix(suffix):
                fail("module origin not installed artifact: " + name)
            if require_free_threaded:
                checkpoints.append(snapshot("physical_imported:" + name))
        # Inspect the storage address of the C global, not the pointer value.
        a = ctypes.CDLL(
            str(root / ("wiring_pi/wiring_pi" + suffix)), mode=ctypes.RTLD_LOCAL
        )
        b = ctypes.CDLL(
            str(root / ("wiring_pi/wiring_pi_i2c" + suffix)), mode=ctypes.RTLD_LOCAL
        )
        addr_a = ctypes.addressof(ctypes.c_void_p.in_dll(a, "wiringPiNodes"))
        addr_b = ctypes.addressof(ctypes.c_void_p.in_dll(b, "wiringPiNodes"))
        if addr_a != addr_b:
            fail("C global wiringPiNodes has split storage between extensions")
    if require_free_threaded:
        checkpoints.append(snapshot("physical_after_all_imports"))
        if len(checkpoints) != 56:
            fail("all 54 GIL OFF checkpoints were not recorded")
    hashes[backend.name] = hashlib.sha256(backend.read_bytes()).hexdigest()
    return {
        "result": "PRODUCTION_SHARED_BACKEND_ABI_LAYOUT_PASS",
        "platform": sys.platform,
        "python": sys.version.split()[0],
        "physical_backend": "shared, one installed ELF library",
        "native_extensions": 54,
        "backend_consumers": len(needed),
        "no_direct_backend_needed": unneeded,
        "all_module_origins_validated": with_imports,
        "single_gpio_state_verified": with_imports,
        "files_sha256": hashes,
        "auditwheel_grafted_libraries_sha256": sidecar_hashes,
        "elf_loader_path_policy": "relative-only RUNPATH/RPATH, optional SHA-tracked auditwheel .libs",
        "hardware_runtime_tested": False,
        "free_threaded_runtime_tested": require_free_threaded,
        "free_threaded_checkpoints": len(checkpoints),
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--installed-package", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--import-all", action="store_true")
    p.add_argument("--require-free-threaded", action="store_true")
    p.add_argument("--report", type=Path, required=True)
    ns = p.parse_args()
    result = audit(
        ns.installed_package,
        ns.manifest,
        with_imports=ns.import_all,
        require_free_threaded=ns.require_free_threaded,
    )
    ns.report.write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        result["result"],
        "54 modules",
        result["backend_consumers"],
        "physical ABI consumers",
    )


if __name__ == "__main__":
    main()
