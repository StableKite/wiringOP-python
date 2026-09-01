#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWN_GAPS = {
    "digitalRead8",
    "digitalWrite8",
    "getResponce",
    "wiringPiSetupPiFace",
    "wiringPiSetupPiFaceForGpioProg",
}


def run(cmd: list[str], *, cwd: Path | None = None) -> str:
    cp = subprocess.run(cmd, cwd=cwd, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return cp.stdout


def production_sources(upstream: Path) -> list[Path]:
    result = sorted((upstream / "wiringPi").glob("*.c"))
    result += [p for p in sorted((upstream / "devLib").glob("*.c")) if p.name != "piFaceOld.c"]
    result += [p for p in sorted((upstream / "wiringPiD").glob("*.c")) if p.name != "wiringpid.c"]
    if len(result) != 48:
        raise SystemExit(f"expected exactly 48 production C files, got {len(result)}")
    return result


def compile_backend(name: str, sources: list[Path], upstream: Path, out_root: Path) -> Path:
    obj_dir = out_root / name
    obj_dir.mkdir(parents=True, exist_ok=True)
    includes = [
        upstream,
        upstream / "wiringPi",
        upstream / "devLib",
        upstream / "wiringPiD",
    ]
    objs: list[Path] = []
    for index, source in enumerate(sources):
        obj = obj_dir / f"{index:03d}.o"
        cmd = [
            "gcc", "-std=gnu11", "-fPIC", "-D_GNU_SOURCE", "-DCONFIG_ORANGEPI",
            *(f"-I{x}" for x in includes),
            "-Wno-unused-result", "-Wno-format-security",
            "-c", str(source), "-o", str(obj),
        ]
        subprocess.run(cmd, check=True)
        objs.append(obj)
    linked = out_root / f"{name}_backend.o"
    subprocess.run(["ld", "-r", *(str(x) for x in objs), "-o", str(linked)], check=True)
    return linked


def defined_symbols(path: Path) -> set[str]:
    out = run(["nm", "-g", "--defined-only", str(path)])
    return {line.split()[-1] for line in out.splitlines() if line.split()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--upstream", type=Path, default=ROOT / "build/upstream/wiringOP")
    ap.add_argument("--build-dir", type=Path, default=ROOT / "build/backend-audit")
    ns = ap.parse_args()
    upstream = ns.upstream.resolve()
    out_root = ns.build_dir.resolve()
    if not (upstream / "wiringPi/wiringSerial.c").is_file():
        raise SystemExit(f"prepared upstream missing: {upstream}")
    if out_root.exists():
        shutil.rmtree(out_root)
    out_root.mkdir(parents=True)

    manifest = json.loads((ROOT / "api_manifest.json").read_text())
    functions = {f["c_name"] for h in manifest["headers"] for f in h.get("functions", [])}
    mocks = sorted((ROOT / "support/mock_backend").rglob("*.c"))
    if len(mocks) != 54:
        raise SystemExit(f"expected 54 mock C files, got {len(mocks)}")
    prod = production_sources(upstream)

    results = []
    for name, sources in (("mock", mocks), ("prod", prod)):
        linked = compile_backend(name, sources, upstream, out_root)
        symbols = defined_symbols(linked)
        missing = functions - symbols
        unexpected = missing - KNOWN_GAPS
        lost_known = KNOWN_GAPS - missing
        if unexpected:
            raise SystemExit(f"{name}: unexpected missing functions: {sorted(unexpected)}")
        # If an upstream gap gets implemented, force an explicit allowlist review rather than silently hiding it.
        if lost_known:
            raise SystemExit(f"{name}: known-gap allowlist is stale; now defined: {sorted(lost_known)}")
        results.append((name, len(sources), len(symbols), sorted(missing)))

    for name, count, symbols, missing in results:
        print(f"{name.upper()}_BACKEND_OK c_files={count} defined_globals={symbols} known_gaps={','.join(missing)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
