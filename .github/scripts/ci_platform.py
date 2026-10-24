#!/usr/bin/env python3
"""R5 five-platform native validation runner, fail closed on every stage.

Windows builds and tests a REAL native mock wheel, never uploaded as physical.
Linux also builds the shared physical C ABI wheel, repairs platform tags with
`auditwheel`, installs the repaired wheel in a fresh venv, and audits all 55 ELF
objects/54 imported Python modules under selected free-threaded Python.

Requires newest stable `t` already selected by workflow, PYTHON_GIL=0 and
PYTHON_JIT=1. No devpi secret/access and no publication in this script.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path

_THIS = Path(__file__).resolve()
_ROOT = _THIS.parents[2]
sys.path.insert(0, str(_THIS.parent))
import ci_release_policy as policy


def run(
    args: list[str], *, cwd: Path = _ROOT, env: dict[str, str] | None = None
) -> None:
    print("REQUIRED_COMMAND", json.dumps(args), flush=True)
    subprocess.run(args, cwd=cwd, env=env, check=True)


def require(condition: bool, msg: str) -> None:
    if not condition:
        raise RuntimeError("CI_NATIVE_FAIL_CLOSED: " + msg)


def exactly_one(folder: Path, glob: str) -> Path:
    a = sorted(folder.glob(glob))
    require(len(a) == 1, "exactly one " + glob + " expected in " + str(folder))
    return a[0]


def python_executable(venv: Path) -> Path:
    return venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--kind", choices=("windows", "glibc", "musl"), required=True)
    p.add_argument(
        "--platform",
        required=True,
        help="win_amd64, manylinux_2_35_*, or musllinux_1_2_*",
    )
    p.add_argument("--sha", required=True, help="Exact GitHub event sha")
    p.add_argument(
        "--artifacts",
        type=Path,
        required=True,
        help="Final artifact folder; no relative paths",
    )
    p.add_argument(
        "--scratch",
        type=Path,
        required=True,
        help="Separate workspace outside checkout",
    )
    opt = p.parse_args()
    require(
        opt.artifacts.is_absolute() and opt.scratch.is_absolute(),
        "absolute artifact/temp paths mandatory",
    )
    require(
        not opt.scratch.resolve().is_relative_to(_ROOT),
        "scratch must be outside checkout",
    )
    require(
        opt.scratch != opt.artifacts,
        "scratch and published artifact dirs must be separate",
    )
    require(
        sys.implementation.name == "cpython"
        and sys.version_info.releaselevel == "final"
        and sys.version_info[:2] >= (3, 14)
        and sysconfig.get_config_var("Py_GIL_DISABLED") == 1
        and hasattr(sys, "_is_gil_enabled")
        and not sys._is_gil_enabled(),
        "actual runtime must be stable CPython t, GIL OFF",
    )
    require(
        os.environ.get("PYTHON_GIL") == "0" and os.environ.get("PYTHON_JIT") == "1",
        "PYTHON_GIL=0 and PYTHON_JIT=1 required",
    )
    require(
        policy.command("git", "rev-parse", "HEAD", cwd=_ROOT) == opt.sha,
        "event source HEAD mismatch",
    )
    machine = platform.machine().lower()
    require(machine in ("x86_64", "amd64", "aarch64", "arm64"), "unknown architecture")
    if opt.kind == "windows":
        require(
            sys.platform == "win32"
            and machine in ("x86_64", "amd64")
            and opt.platform == "win_amd64",
            "Windows validator needs x86_64 native MSVC",
        )
    else:
        require(sys.platform == "linux", "Linux physical validation only on Linux")
        arch = "aarch64" if machine in ("aarch64", "arm64") else "x86_64"
        require(
            opt.platform
            == f"{'manylinux_2_35' if opt.kind == 'glibc' else 'musllinux_1_2'}_{arch}",
            "validator target mismatch",
        )
        libc = platform.libc_ver()[0]
        if opt.kind == "glibc":
            require(libc == "glibc", "glibc host required")
        if opt.kind == "musl":
            require(libc != "glibc", "musl host required")
    opt.scratch.mkdir(parents=True, exist_ok=False)
    opt.artifacts.mkdir(parents=True, exist_ok=True)
    report = {
        "schema": 1,
        "package": policy.PROJECT,
        "version": policy.project_version(_ROOT),
        "git_sha": opt.sha,
        "kind": opt.kind,
        "platform": opt.platform,
        "python": sys.version.split()[0],
        "gil_off": True,
        "status": "IN_PROGRESS",
        "mock_tests": "PENDING",
        "physical_backend": "PENDING" if opt.kind != "windows" else "NOT_APPLICABLE",
    }
    try:
        for source_test in (
            "tools/upstream_contract.py",
            "tools/selftest_upstream_contract.py",
            "tools/selftest_sdist_source.py",
            "tools/selftest_audit_layout.py",
            "tools/selftest_audit_docs.py",
            "tools/audit_layout.py",
            "tools/selftest_audit_surfaces.py",
            "tools/audit_bindings.py",
            "tools/audit_stubs.py",
            "tools/audit_docs.py",
            "tools/selftest_ci_runtime_gate.py",
            ".github/scripts/selftest_ci_release_policy.py",
        ):
            run([sys.executable, source_test])
        run(
            [
                sys.executable,
                "tools/ci_runtime_gate.py",
                "--source-sha",
                opt.sha,
                "--report",
                str(opt.scratch / "runtime_preflight.json"),
            ]
        )
        run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--disable-pip-version-check",
                "scikit-build-core==1.1.1",
                "nanobind==2.14.0",
                "pytest==9.1.1",
            ]
        )
        import scikit_build_core.build as builder

        source_dist = opt.scratch / "source"
        source_dist.mkdir()
        name = builder.build_sdist(str(source_dist))
        sdist = source_dist / name
        policy.verify_sdist(sdist, report["version"])
        report["sdist"] = {
            "name": sdist.name,
            "sha256": hashlib.sha256(sdist.read_bytes()).hexdigest(),
        }
        wheel_build = opt.scratch / "mock-wheel"
        wheel_build.mkdir()
        run(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                "--no-deps",
                "--no-cache-dir",
                "--disable-pip-version-check",
                "--no-input",
                "-w",
                str(wheel_build),
                "-C",
                "cmake.define.WIRINGOP_USE_MOCK=ON",
                "-C",
                "cmake.define.WIRINGOP_ENABLE_IPO=ON",
                str(sdist),
            ]
        )
        mock_wheel = exactly_one(wheel_build, "*.whl")
        report["mock_record"] = policy.verify_mock_wheel(
            mock_wheel,
            report["version"],
            "win_amd64"
            if opt.kind == "windows"
            else "linux_"
            + ("aarch64" if machine in ("aarch64", "arm64") else "x86_64"),
        )
        require(
            mock_wheel.name.endswith("-" + opt.platform + ".whl")
            if opt.kind == "windows"
            else mock_wheel.name.endswith(
                "-linux_"
                + ("aarch64" if machine in ("aarch64", "arm64") else "x86_64")
                + ".whl"
            ),
            "mock wheel native platform tag unexpected",
        )
        run(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "--no-index",
                "--no-deps",
                "--disable-pip-version-check",
                str(mock_wheel),
            ]
        )
        run(
            [
                sys.executable,
                "tools/ci_runtime_gate.py",
                "--source-sha",
                opt.sha,
                "--installed",
                "--wheel",
                str(mock_wheel),
                "--report",
                str(opt.scratch / "mock_runtime.json"),
            ]
        )
        evidence = json.loads((opt.scratch / "mock_runtime.json").read_text())
        require(
            evidence.get("status") == "INSTALLED_WHEEL_SAME_PROCESS_TEST_PASS"
            and evidence.get("pytest", {}).get("passed", 0) >= 324
            and not evidence.get("pytest", {}).get("skipped"),
            "real mock wheel must pass 324+ tests with GIL OFF",
        )
        report["mock_tests"] = {
            "count": evidence["pytest"]["passed"],
            "gil_checks": evidence["pytest"]["runtime_checks"],
            "wheel_sha256": hashlib.sha256(mock_wheel.read_bytes()).hexdigest(),
        }
        if opt.kind != "windows":
            physical_dir = opt.scratch / "physical-unrepaired"
            physical_dir.mkdir()
            run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "wheel",
                    "--no-deps",
                    "--no-cache-dir",
                    "--disable-pip-version-check",
                    "--no-input",
                    "-w",
                    str(physical_dir),
                    "-C",
                    "cmake.define.WIRINGOP_USE_MOCK=OFF",
                    "-C",
                    "cmake.define.WIRINGOP_ENABLE_IPO=ON",
                    str(sdist),
                ]
            )
            raw = exactly_one(physical_dir, "*.whl")
            run([sys.executable, "-m", "auditwheel", "show", str(raw)])
            repaired = opt.scratch / "physical-repaired"
            repaired.mkdir()
            run(
                [
                    sys.executable,
                    "-m",
                    "auditwheel",
                    "repair",
                    "--plat",
                    opt.platform,
                    "-w",
                    str(repaired),
                    str(raw),
                ]
            )
            physical = exactly_one(repaired, "*.whl")
            require(
                physical.name.endswith("-" + opt.platform + ".whl"),
                "repair did not give exact policy tag",
            )
            # Validate repaired bytes here, not only when a future publisher
            # downloads the artifact. auditwheel adds optional ZIP directories.
            wheel_proof = policy.verify_physical_wheel(
                physical, report["version"], opt.platform
            )
            require(
                wheel_proof["record_files"] >= 118,
                "repaired physical wheel RECORD is incomplete",
            )
            expected_abi = (
                "cp" + str(sys.version_info.major) + str(sys.version_info.minor)
            )
            require(
                physical.name.split("-")[2:4] == [expected_abi, expected_abi + "t"],
                "repaired physical ABI does not match actual newest-final t Python",
            )
            run([sys.executable, "-m", "auditwheel", "show", str(physical)])
            clean = opt.scratch / "installed-physical-env"
            run([sys.executable, "-m", "venv", str(clean)])
            py = str(python_executable(clean))
            run([py, "-m", "pip", "install", "--no-index", "--no-deps", str(physical)])
            # Do not trust guesses about Python minor layout; ask the actual environment.
            site = subprocess.check_output(
                [py, "-c", 'import sysconfig;print(sysconfig.get_path("purelib"))'],
                text=True,
            ).strip()
            installed = Path(site) / "wiringop"
            env = os.environ.copy()
            run(
                [
                    py,
                    "tools/audit_production_backend.py",
                    "--installed-package",
                    str(installed),
                    "--manifest",
                    str(_ROOT / "api_manifest.json"),
                    "--import-all",
                    "--require-free-threaded",
                    "--report",
                    str(opt.scratch / "physical_audit.json"),
                ],
                env=env,
            )
            run(
                [
                    py,
                    "tools/ci_runtime_gate.py",
                    "--source-sha",
                    opt.sha,
                    "--report",
                    str(opt.scratch / "physical_ft_preflight.json"),
                ],
                env=env,
            )
            run(
                [
                    py,
                    "tools/selftest_production_backend.py",
                    "--installed-package",
                    str(installed),
                    "--manifest",
                    str(_ROOT / "api_manifest.json"),
                ],
                env=env,
            )
            shutil.copy2(physical, opt.artifacts / physical.name)
            report["physical_backend"] = {
                "wheel": physical.name,
                "sha256": hashlib.sha256(physical.read_bytes()).hexdigest(),
                "record": wheel_proof,
                "elf_report": json.loads(
                    (opt.scratch / "physical_audit.json").read_text()
                ),
            }
        if opt.kind == "glibc" and opt.platform == "manylinux_2_35_x86_64":
            shutil.copy2(sdist, opt.artifacts / sdist.name)
        report["status"] = "PLATFORM_NATIVE_VALIDATION_PASS"
        print(
            "PLATFORM_NATIVE_VALIDATION_PASS",
            json.dumps(
                {"kind": opt.kind, "tag": opt.platform, "tests": report["mock_tests"]},
                sort_keys=True,
            ),
        )
    except Exception as exc:
        report["status"] = "FAILED_CLOSED"
        report["error_type"] = type(exc).__name__
        report["error"] = str(exc)
        raise
    finally:
        (opt.artifacts / "platform-validation-report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
