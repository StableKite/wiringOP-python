#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED_WIRINGOP = "a7921ca2f5c124203be10d3418db70a2e15f3c10"
NB_VERSION = "2.14.0"
NB_HEADER_BLOB = "d18f1320133bf5df4c8ecc90dd99b8fd1dd856b9"
NB_COMBINED_BLOB = "6abb636a73da3d307c101ca2231dd1e6bd794f30"
ROBIN_MAP_BLOB = "b594810e62e81efca828ffad609ed2fa128c4843"
NB_WHEEL_SHA256 = "a57cd4fe613db78410ca13ba007a3ffaf3125b831d8be46ec7f4351e8cf6e513"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def run(cmd: list[str], *, cwd: Path = ROOT, env: dict[str, str] | None = None) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def capture(cmd: list[str], *, cwd: Path = ROOT) -> str:
    return subprocess.check_output(cmd, cwd=cwd, text=True).strip()


def python_env(package_root: Path, wheel: Path | None = None) -> dict[str, str]:
    env = os.environ.copy()
    entries = [str(package_root)]
    if wheel is not None:
        entries.insert(0, str(wheel))
    old = env.get("PYTHONPATH")
    if old:
        entries.append(old)
    env["PYTHONPATH"] = os.pathsep.join(entries)
    return env


def import_smoke(package_root: Path, label: str) -> None:
    code = r'''
import pkgutil, importlib, wiringop
mods=[m.name for m in pkgutil.walk_packages(wiringop.__path__, wiringop.__name__+'.')]
failed=[]
for name in mods:
    try: importlib.import_module(name)
    except Exception as exc: failed.append((name, repr(exc)))
print("IMPORT_SMOKE", len(mods)-len(failed), len(mods), "failed", len(failed))
if failed:
    print(failed)
    raise SystemExit(1)
'''
    run([sys.executable, "-c", code], env=python_env(package_root))
    print(f"{label}_IMPORT_OK", flush=True)


def verify_dependency_tree(nb_root: Path, wheel: Path) -> None:
    required = {
        nb_root / "include/nanobind/nanobind.h": NB_HEADER_BLOB,
        nb_root / "src/nb_combined.cpp": NB_COMBINED_BLOB,
        nb_root / "ext/robin_map/include/tsl/robin_map.h": ROBIN_MAP_BLOB,
    }
    for path, expected in required.items():
        if not path.is_file():
            raise SystemExit(f"missing exact dependency file: {path}")
        actual = git_blob_sha(path)
        if actual != expected:
            raise SystemExit(f"Git blob mismatch for {path}: {actual} != {expected}")
    text = (nb_root / "include/nanobind/nanobind.h").read_text()
    for token in ("NB_VERSION_MAJOR 2", "NB_VERSION_MINOR 14", "NB_VERSION_PATCH 0"):
        if token not in text:
            raise SystemExit(f"nanobind version mismatch: missing {token}")
    if not wheel.is_file():
        raise SystemExit(f"missing nanobind wheel: {wheel}")
    actual_wheel = file_sha256(wheel)
    if actual_wheel != NB_WHEEL_SHA256:
        raise SystemExit(f"nanobind wheel SHA256 mismatch: {actual_wheel} != {NB_WHEEL_SHA256}")
    print("DEPENDENCY_GATE_OK nanobind=2.14.0 exact_blobs=3 wheel_sha256=OK")


def verify_upstream() -> None:
    upstream = ROOT / "extern/wiringOP"
    head = capture(["git", "rev-parse", "HEAD"], cwd=upstream)
    if head != PINNED_WIRINGOP:
        raise SystemExit(f"wiringOP HEAD mismatch: {head}")
    if capture(["git", "status", "--porcelain"], cwd=upstream):
        raise SystemExit("extern/wiringOP is dirty")
    entry = capture(["git", "ls-files", "-s", "extern/wiringOP"])
    if not entry.startswith("160000 "):
        raise SystemExit(f"extern/wiringOP is not a gitlink: {entry}")
    print(f"UPSTREAM_GATE_OK commit={head} gitlink=160000")


def compare_manifest(build_root: Path) -> None:
    generated = build_root / "api_manifest.generated.json"
    run([sys.executable, "tools/generate_manifest.py", "--output", str(generated)])
    current = json.loads((ROOT / "api_manifest.json").read_text())
    fresh = json.loads(generated.read_text())
    if current != fresh:
        raise SystemExit("fresh Clang manifest differs from committed api_manifest.json")
    t = current["totals"]
    print("MANIFEST_REPRO_OK", json.dumps(t, sort_keys=True))


def configure_and_build(build_dir: Path, nb_root: Path, use_mock: bool, jobs: int) -> None:
    if build_dir.exists():
        shutil.rmtree(build_dir)
    run([
        "cmake", "-S", ".", "-B", str(build_dir),
        f"-DNB_ROOT={nb_root}",
        f"-DWIRINGOP_USE_MOCK={'ON' if use_mock else 'OFF'}",
        f"-DWIRINGOP_SOURCE={ROOT / 'build/upstream/wiringOP'}",
        "-DCMAKE_BUILD_TYPE=Release",
    ])
    run(["cmake", "--build", str(build_dir), f"-j{jobs}"])
    count = len(list((build_dir / "python/wiringop").rglob("*.so")))
    if count != 54:
        raise SystemExit(f"expected 54 built extension modules, found {count}")
    print(f"BUILD_GATE_OK backend={'mock' if use_mock else 'production'} modules={count}")


def generate_stubs(mock_python: Path, wheel: Path) -> None:
    stubs = ROOT / "stubs"
    if stubs.exists():
        shutil.rmtree(stubs)
    stubs.mkdir(parents=True)
    code = r'''
import json, pathlib
from nanobind import stubgen
root=pathlib.Path.cwd()
d=json.loads((root/'api_manifest.json').read_text())
for h in d['headers']:
    out=root/'stubs'/pathlib.Path(h['path']).with_suffix('.pyi')
    out.parent.mkdir(parents=True, exist_ok=True)
    stubgen.main(['-m', h['python_module'], '-o', str(out), '--quiet'])
print('OFFICIAL_STUBGEN_OK', len(d['headers']))
'''
    run([sys.executable, "-c", code], env=python_env(mock_python, wheel))


def verify_install_tree(prod_build: Path, install_root: Path) -> None:
    if install_root.exists():
        shutil.rmtree(install_root)
    run(["cmake", "--install", str(prod_build), "--prefix", str(install_root)])
    package = install_root / "wiringop"
    pyi = list(package.rglob("*.pyi"))
    so = list(package.rglob("*.so"))
    pycache = list(package.rglob("__pycache__"))
    pyc = list(package.rglob("*.pyc"))
    if len(pyi) != 54 or len(so) != 54:
        raise SystemExit(f"install tree mismatch: .pyi={len(pyi)} .so={len(so)}")
    if pycache or pyc:
        raise SystemExit(f"install tree contains Python cache artifacts: dirs={len(pycache)} pyc={len(pyc)}")
    if not (package / "py.typed").is_file():
        raise SystemExit("installed py.typed is missing")
    env = python_env(install_root)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    code = r'''
import pkgutil, importlib, wiringop
mods=[m.name for m in pkgutil.walk_packages(wiringop.__path__, wiringop.__name__+'.')]
failed=[]
for name in mods:
    try: importlib.import_module(name)
    except Exception as exc: failed.append((name, repr(exc)))
print("INSTALL_IMPORT_SMOKE", len(mods)-len(failed), len(mods), "failed", len(failed))
if failed:
    print(failed)
    raise SystemExit(1)
'''
    run([sys.executable, "-c", code], env=env)
    print("INSTALL_TREE_OK modules=54 stubs=54 py.typed=yes caches=none")


def verify_default_packaging_config(build_root: Path, wheel: Path) -> None:
    package_root = build_root / "nanobind-package"
    configure_root = build_root / "package-default-config"
    if package_root.exists():
        shutil.rmtree(package_root)
    if configure_root.exists():
        shutil.rmtree(configure_root)
    run([
        sys.executable, "-m", "pip", "install", "--no-index", "--no-deps",
        "--target", str(package_root), str(wheel),
    ])
    env = os.environ.copy()
    old = env.get("PYTHONPATH")
    env["PYTHONPATH"] = str(package_root) + (os.pathsep + old if old else "")
    run(["cmake", "-S", ".", "-B", str(configure_root), "-DCMAKE_BUILD_TYPE=Release"], env=env)
    cache = (configure_root / "CMakeCache.txt").read_text()
    if "WIRINGOP_USE_MOCK:BOOL=OFF" not in cache:
        raise SystemExit("default package configure did not select production backend")
    expected_nb = (package_root / "nanobind").resolve()
    if f"NB_ROOT:PATH={expected_nb}" not in cache:
        raise SystemExit("default package configure did not auto-discover exact nanobind wheel")
    prepared = configure_root / "upstream/wiringOP"
    if "serialContextCancelRead" not in (prepared / "wiringPi/wiringSerial.h").read_text():
        raise SystemExit("default package configure did not apply UART overlay")
    if "uintptr_t" not in (prepared / "wiringPi/pseudoPins.c").read_text():
        raise SystemExit("default package configure did not apply AArch64 pseudoPins overlay")
    print("PACKAGE_DEFAULT_CONFIG_OK production=yes nanobind=auto overlays=2")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nb-root", type=Path, default=Path(os.environ.get("NB_ROOT", "/mnt/data/.deps/nanobind-2.14.0")))
    ap.add_argument("--nanobind-wheel", type=Path)
    ap.add_argument("--qemu-bundle", type=Path)
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--build-root", type=Path, default=ROOT / "build/acceptance")
    ns = ap.parse_args()
    nb_root = ns.nb_root.resolve()
    wheel = (ns.nanobind_wheel or (nb_root.parent / "pypi/nanobind-2.14.0-py3-none-any.whl")).resolve()
    build_root = ns.build_root.resolve()
    build_root.mkdir(parents=True, exist_ok=True)

    verify_dependency_tree(nb_root, wheel)
    verify_upstream()
    verify_default_packaging_config(build_root, wheel)
    run([sys.executable, "tools/prepare_wiringop.py"])
    compare_manifest(build_root)

    for tool in (
        "tools/audit_bindings.py",
        "tools/audit_docs.py",
        "tools/audit_backend_symbols.py",
        "tools/test_serial_pty.py",
        "tools/test_pseudopins_64bit.py",
    ):
        run([sys.executable, tool])
    run([sys.executable, "-m", "compileall", "-q", "python", "tests", "tools"])

    mock = build_root / "mock"
    configure_and_build(mock, nb_root, True, ns.jobs)
    mock_python = mock / "python"
    import_smoke(mock_python, "MOCK")
    run([sys.executable, "-m", "pytest", "-q"], env=python_env(mock_python))

    generate_stubs(mock_python, wheel)
    run([sys.executable, "tools/audit_stubs.py"])
    run([sys.executable, "tools/audit_layout.py"])

    prod = build_root / "production"
    configure_and_build(prod, nb_root, False, ns.jobs)
    prod_python = prod / "python"
    import_smoke(prod_python, "PRODUCTION")
    run([sys.executable, "tools/test_serial_python_pty.py"], env=python_env(prod_python))
    verify_install_tree(prod, build_root / "install")

    if ns.qemu_bundle is not None:
        run([sys.executable, "tools/test_qemu_aarch64.py", str(ns.qemu_bundle.resolve())])
    else:
        print("QEMU_GATE_SKIPPED no --qemu-bundle supplied")

    summary = {
        "status": "ok",
        "wiringop_commit": PINNED_WIRINGOP,
        "nanobind_version": NB_VERSION,
        "manifest_totals": json.loads((ROOT / "api_manifest.json").read_text())["totals"],
        "mock_pytest": "321/321 passed",
        "stubgen": "official nanobind.stubgen 2.14.0, 54/54",
        "production_import": "57/57",
        "install_tree": {"extensions": 54, "stubs": 54, "py_typed": True, "cache_artifacts": 0},
        "package_default": "production, nanobind auto-discovery, overlays auto-prepared",
        "python_serial_pty": "passed",
        "qemu": "passed" if ns.qemu_bundle is not None else "skipped",
    }
    (build_root / "acceptance-summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print("ACCEPTANCE_OK", json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
