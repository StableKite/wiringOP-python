#!/usr/bin/env python3
"""Fail-closed GitHub version intent and devpi artifact metadata guards.

The validator never accesses devpi or secrets. Credentials are available only
in the dependent publish job after five native validation jobs succeed.
"""

from __future__ import annotations

import argparse
import ast
import base64
import csv
import hashlib
import io
import json
import os
import re
import stat
import subprocess
import sys
import tarfile
import zipfile
from email.parser import Parser
from pathlib import Path, PurePosixPath

import tomllib

HOST = "https://devpi.stablekite.com/"
TARGET = HOST + "StableKite/index/"
PROJECT = "wiringop-nanobind"
DISTRIBUTION = "wiringop_nanobind"
PINNED_FORK_ARCHIVE_SHA256 = (
    "ab7f6deaf06b7d800e447294d1c28c178c63f884cfddf64591bf948545f47c9c"
)
PINNED_FORK_ARCHIVE_NAME = (
    "wiringOP-53fe570936ebca007d6d76f26ef21ba9f2609ca6-git-archive.zip"
)
PLATFORMS = frozenset(
    {
        "manylinux_2_35_x86_64",
        "manylinux_2_35_aarch64",
        "musllinux_1_2_x86_64",
        "musllinux_1_2_aarch64",
    }
)
RE_SHA = re.compile(r"^[0-9a-f]{40}$")
RE_FINAL_VERSION = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
RE_WHEEL = re.compile(
    r"^wiringop_nanobind-(?P<version>[0-9]+\.[0-9]+\.[0-9]+)-"
    r"(?P<interpreter>cp3[0-9]{2,3})-(?P<abi>cp3[0-9]{2,3}t)-"
    r"(?P<platform>manylinux_2_35_(?:x86_64|aarch64)|musllinux_1_2_(?:x86_64|aarch64))\.whl$"
)


class PolicyError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PolicyError(message)


def command(*argv: str, cwd: Path) -> str:
    p = subprocess.run(argv, cwd=cwd, text=True, capture_output=True, check=False)
    require(p.returncode == 0, "Git proof unavailable: " + " ".join(argv[:3]))
    return p.stdout.strip()


def read_version(raw: str) -> str:
    obj = tomllib.loads(raw)
    version = obj["project"]["version"]
    require(
        isinstance(version, str) and RE_FINAL_VERSION.fullmatch(version) is not None,
        "canonical project.version must be final X.Y.Z",
    )
    return version


def project_version(root: Path) -> str:
    canonical = read_version((root / "pyproject.toml").read_text(encoding="utf-8"))
    module = root / "python/wiringop/__init__.py"
    require(module.is_file(), "versioned Python package module missing")
    syntax = ast.parse(module.read_text(encoding="utf-8"))
    versions = [
        node.value.value
        for node in syntax.body
        if isinstance(node, ast.Assign)
        and any(isinstance(k, ast.Name) and k.id == "__version__" for k in node.targets)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    ]
    require(
        versions == [canonical],
        "package __version__ not identical to canonical project.version",
    )
    return canonical


def intent(
    *,
    root: Path,
    event: str,
    before: str,
    head: str,
    manual_publish: str,
    ref: str,
    repository: str,
) -> dict[str, str]:
    require(
        ref == "refs/heads/main",
        "publication intent requires refs/heads/main; other refs rejected",
    )
    require(
        repository == "StableKite/wiringOP-python", "unexpected GitHub event repository"
    )
    require(RE_SHA.fullmatch(head) is not None, "invalid exact GitHub event head SHA")
    require(
        command("git", "rev-parse", "HEAD", cwd=root) == head,
        "checkout HEAD does not equal GitHub event SHA",
    )
    current = project_version(root)
    require(
        manual_publish in ("true", "false"),
        "manual_publish must be exactly true or false",
    )
    if event == "push":
        require(manual_publish == "false", "manual publish flag not permitted on push")
        require(
            RE_SHA.fullmatch(before) is not None and before != "0" * 40,
            "push before commit is unavailable: fail-closed",
        )
        command("git", "cat-file", "-e", f"{before}^{{commit}}", cwd=root)
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", before, head],
            cwd=root,
            check=False,
            capture_output=True,
        )
        require(
            ancestry.returncode == 0,
            "push before SHA must be an ancestor of exact HEAD",
        )
        old = command("git", "show", f"{before}:pyproject.toml", cwd=root)
        previous = read_version(old)
        publish = current != previous
        if publish:
            require(
                tuple(map(int, current.split(".")))
                > tuple(map(int, previous.split("."))),
                "downgrade/non-increasing package version rejected",
            )
    elif event == "workflow_dispatch":
        previous = "manual"
        publish = manual_publish == "true"
    else:
        raise PolicyError("unsupported publish event: " + event)
    return {
        "current_version": current,
        "previous_version": previous,
        "should_publish": "true" if publish else "false",
        "reason": (
            "MANUAL_EXPLICIT_PUBLISH"
            if event == "workflow_dispatch" and publish
            else "VERSION_CHANGED_PUBLISH"
            if publish
            else "VALIDATION_ONLY_VERSION_UNCHANGED"
            if event == "push"
            else "VALIDATION_ONLY_MANUAL_NO_PUBLISH"
        ),
    }


def _safe_archive_name(name: str) -> bool:
    p = PurePosixPath(name)
    return bool(
        name
        and not name.startswith("/")
        and "\\" not in name
        and len(p.parts) >= 2
        and all(part not in ("", ".", "..") for part in p.parts)
    )


def verify_core_metadata(raw: bytes, version: str) -> dict[str, str]:
    """Verify wheel distribution identity, not merely a filename/RECORD hash.

    RECORD hashes prove integrity of the wheel ZIP, not that it declares the
    expected project/version. A foreign or incorrectly versioned METADATA is
    rejected before the publish job can pass its exact-set gate.
    """
    try:
        metadata = Parser().parsestr(raw.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise PolicyError("wheel core METADATA is not UTF-8") from exc
    identity = {}
    for field, expected in (("Name", PROJECT), ("Version", version)):
        values = metadata.get_all(field, [])
        require(
            values == [expected],
            "wheel METADATA " + field + " must occur once and match " + expected,
        )
        identity[field.lower()] = values[0]
    require(
        len(metadata.get_all("Metadata-Version", [])) == 1,
        "wheel core METADATA missing/duplicate Metadata-Version",
    )
    return identity


def verify_sdist_identity(
    arc: tarfile.TarFile, member: str, version: str
) -> dict[str, str]:
    """Check canonical pyproject inside the uploaded sdist itself."""
    f = arc.extractfile(member)
    require(f is not None, "sdist pyproject.toml missing")
    try:
        doc = tomllib.loads(f.read().decode("utf-8"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise PolicyError("sdist canonical pyproject.toml is invalid") from exc
    project = doc.get("project", {})
    require(
        project.get("name") == PROJECT and project.get("version") == version,
        "sdist pyproject Name/Version differs from expected release identity",
    )
    return {"name": project["name"], "version": project["version"]}


def verify_sdist(path: Path, version: str) -> dict[str, object]:
    expect = f"{DISTRIBUTION}-{version}.tar.gz"
    require(path.name == expect, f"wrong sdist name: {path.name} expected {expect}")
    with tarfile.open(path, "r:gz") as arc:
        all_members = arc.getmembers()
        require(
            all(m.isfile() or m.isdir() for m in all_members),
            "sdist contains symlink, special file or unsafe member type",
        )
        all_names = [m.name.rstrip("/") for m in all_members]
        require(
            len(all_names) == len(set(all_names))
            and all(_safe_archive_name(n) for n in all_names),
            "sdist invalid/duplicate/unsafe path",
        )
        members = [m for m in all_members if m.isfile()]
        names = [m.name for m in members]
        dirs = {k: 0 for k in ("src", "tests", "stubs", "mock", "pinned_archive")}
        for name in names:
            rel = "/".join(PurePosixPath(name).parts[1:])
            require(
                not any(
                    part
                    in (
                        ".git",
                        "__pycache__",
                        "CMakeFiles",
                        "build",
                        "dist",
                        "_r2_native_build",
                    )
                    for part in PurePosixPath(rel).parts
                ),
                "sdist contains build/Git junk",
            )
            for key, prefix, suffix in [
                ("src", "src/", ".cpp"),
                ("tests", "tests/", ".py"),
                ("stubs", "stubs/", ".pyi"),
                ("mock", "support/mock_backend/", ".c"),
            ]:
                if rel.startswith(prefix) and rel.endswith(suffix):
                    dirs[key] += 1
            if rel.startswith("support/upstream/") and rel.endswith("-git-archive.zip"):
                require(
                    rel == "support/upstream/" + PINNED_FORK_ARCHIVE_NAME,
                    "unreviewed integrated source archive name in sdist",
                )
                contents = arc.extractfile(arc.getmember(name))
                require(
                    contents is not None
                    and hashlib.sha256(contents.read()).hexdigest()
                    == PINNED_FORK_ARCHIVE_SHA256,
                    "sdist integrated source archive bytes differ from pinned source",
                )
                dirs["pinned_archive"] += 1
        require(
            all(dirs[k] == 54 for k in ("src", "tests", "stubs", "mock"))
            and dirs["pinned_archive"] == 1,
            "sdist mirror/pinned-source inventory mismatch",
        )
        pyproject_name = f"{DISTRIBUTION}-{version}/pyproject.toml"
        require(
            names.count(pyproject_name) == 1,
            "sdist canonical pyproject.toml missing/duplicate",
        )
        identity = verify_sdist_identity(arc, pyproject_name, version)
        return {
            "sdist": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "identity": identity,
            "counts": dirs,
            "bytes": path.stat().st_size,
        }


def verify_record(z: zipfile.ZipFile, record_name: str) -> int:
    try:
        rows = list(csv.reader(io.StringIO(z.read(record_name).decode("utf-8"))))
    except KeyError as exc:
        raise PolicyError("wheel RECORD not found") from exc
    # auditwheel repair legitimately creates empty ZIP directory entries.
    # PEP 427's RECORD enumerates *files*, not those optional ZIP placeholders.
    # All regular files, including metadata/SBOMs, must still be hashed exactly.
    entries = z.infolist()
    require(
        len({i.filename for i in entries}) == len(entries),
        "duplicate ZIP entries in wheel",
    )
    actual = set()
    for member in entries:
        require(
            _safe_archive_name("pkg/" + member.filename),
            "unsafe wheel member path: " + member.filename,
        )
        mode = stat.S_IFMT(member.external_attr >> 16)
        if member.is_dir():
            require(
                member.file_size == 0 and mode in (0, stat.S_IFDIR),
                "wheel directory entry has invalid type/content",
            )
        else:
            require(
                mode in (0, stat.S_IFREG),
                "wheel contains symlink or special-file member",
            )
            actual.add(member.filename)
    names = [r[0] for r in rows]
    require(
        len(names) == len(set(names)) and set(names) == actual,
        "wheel RECORD file inventory mismatch",
    )
    for row in rows:
        require(len(row) == 3, "invalid wheel RECORD row shape")
        filename, spec, size = row
        require(_safe_archive_name("pkg/" + filename), "unsafe wheel member path")
        data = z.read(filename)
        if filename == record_name:
            require(not spec and not size, "RECORD must not hash itself")
        else:
            require(spec.startswith("sha256="), "missing SHA-256 RECORD hash")
            digest = (
                base64.urlsafe_b64encode(hashlib.sha256(data).digest())
                .rstrip(b"=")
                .decode()
            )
            require(
                spec == "sha256=" + digest and str(len(data)) == size,
                "wheel file hash/length differs from RECORD: " + filename,
            )
    return len(rows)


def verify_mock_wheel(
    path: Path, version: str, expected_platform: str
) -> dict[str, object]:
    """Prove mock wheel is a genuine ABI-specific binary, never publish it."""
    require(
        expected_platform in ("win_amd64", "linux_x86_64", "linux_aarch64"),
        "unexpected native mock platform",
    )
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate wheel members")
        expected_ext = ".pyd" if expected_platform == "win_amd64" else ".so"
        binaries = [n for n in names if n.endswith(expected_ext)]
        require(
            len(binaries) == 54 and all(n.startswith("wiringop/") for n in binaries),
            "mock wheel must have 54 native package modules",
        )
        require(
            not any("libwiringop_backend" in n or n.endswith(".dll") for n in names),
            "mock wheel contains physical backend/foreign native library",
        )
        wheel = [n for n in names if n.endswith(".dist-info/WHEEL")]
        record = [n for n in names if n.endswith(".dist-info/RECORD")]
        dist_info = f"{DISTRIBUTION}-{version}.dist-info"
        require(
            wheel == [dist_info + "/WHEEL"] and record == [dist_info + "/RECORD"],
            "mock wheel metadata directory does not match canonical distribution/version",
        )
        interpreter = "cp" + str(sys.version_info.major) + str(sys.version_info.minor)
        # Name/tag check is version-agnostic: newest final FT changes as provider changes.
        m = re.fullmatch(
            r"wiringop_nanobind-([0-9]+\.[0-9]+\.[0-9]+)-"
            r"(cp3[0-9]{2,3})-(cp3[0-9]{2,3}t)-"
            + re.escape(expected_platform)
            + r"\.whl",
            path.name,
        )
        require(
            m is not None and m[1] == version and m[3] == m[2] + "t",
            "mock wheel filename not an exact platform free-threaded ABI",
        )
        require(
            m[2] == interpreter,
            "mock wheel ABI differs from executing newest final interpreter",
        )
        tags = [
            v.split(": ", 1)[1].strip()
            for v in z.read(wheel[0]).decode().splitlines()
            if v.startswith("Tag: ")
        ]
        require(
            tags == [f"{m[2]}-{m[3]}-{expected_platform}"],
            "mock WHEEL metadata ABI mismatch",
        )
        count = verify_record(z, record[0])
        core = [n for n in names if n.endswith(".dist-info/METADATA")]
        require(
            core == [dist_info + "/METADATA"],
            "mock wheel core METADATA is outside canonical dist-info directory",
        )
        identity = verify_core_metadata(z.read(core[0]), version)
    return {
        "status": "MOCK_WHEEL_NATIVE_RECORD_PASS",
        "modules": 54,
        "record_files": count,
        "identity": identity,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
    }


def verify_physical_wheel(
    path: Path, version: str, expected_platform: str
) -> dict[str, object]:
    """Verify one repaired native FT release wheel including ALL RECORD bytes.

    This runs inside each Linux validator, not only before publication.
    """
    require(expected_platform in PLATFORMS, "unexpected physical platform")
    m = RE_WHEEL.fullmatch(path.name)
    require(
        m is not None
        and m["version"] == version
        and m["platform"] == expected_platform,
        "not exact reviewed physical platform wheel: " + path.name,
    )
    require(m["abi"] == m["interpreter"] + "t", "wheel is not free-threaded ABI")
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        require(len(names) == len(set(names)), "duplicate wheel ZIP entries")
        binary = [n for n in names if n.endswith(".so")]
        extensions = [
            n
            for n in binary
            if n.startswith("wiringop/") and not n.endswith("/libwiringop_backend.so")
        ]
        require(
            len(extensions) == 54 and all(n.count("/") >= 1 for n in extensions),
            "wheel not exactly 54 native package extensions",
        )
        require(
            sum(n == "wiringop/libwiringop_backend.so" for n in binary) == 1,
            "physical Linux wheel must have single direct shared GPIO backend",
        )
        # auditwheel may add system dependencies under the dedicated .libs
        # directory. These are NOT extra nanobind extensions. Still reject
        # alternate GPIO backends, unhashed names and arbitrary native paths.
        for native in binary:
            if native in extensions or native == "wiringop/libwiringop_backend.so":
                continue
            require(
                native.startswith("wiringop_nanobind.libs/")
                and re.fullmatch(
                    r"lib[A-Za-z0-9_+.-]+-[0-9a-f]{8}\.so", native.split("/", 1)[1]
                )
                is not None
                and "wiringop_backend" not in native.lower(),
                "untrusted auditwheel native sidecar in release wheel",
            )
        for native in names:
            if native.startswith("wiringop_nanobind.libs/") and not native.endswith(
                "/"
            ):
                base = native.split("/", 1)[1]
                require(
                    re.fullmatch(
                        r"lib[A-Za-z0-9_+.-]+-[0-9a-f]{8}\.so(?:\.[0-9.]+)?", base
                    )
                    is not None
                    and "wiringop_backend" not in base.lower(),
                    "untrusted auditwheel sidecar file in release wheel",
                )
        require(
            not any(n.endswith(".pyd") for n in names),
            "Windows mock wheel in publish set",
        )
        wheel = [n for n in names if n.endswith(".dist-info/WHEEL")]
        dist_info = f"{DISTRIBUTION}-{version}.dist-info"
        require(
            wheel == [dist_info + "/WHEEL"],
            "physical WHEEL is missing or outside canonical dist-info directory",
        )
        tags = [
            s[5:].strip()
            for s in z.read(wheel[0]).decode().splitlines()
            if s.startswith("Tag: ")
        ]
        require(
            len(tags) == 1
            and tags[0] == path.name[len(f"{DISTRIBUTION}-{version}-") : -4],
            "WHEEL platform/ABI tag not identical to artifact name",
        )
        record = [n for n in names if n.endswith(".dist-info/RECORD")]
        require(
            record == [dist_info + "/RECORD"],
            "physical RECORD is missing or outside canonical dist-info directory",
        )
        count = verify_record(z, record[0])
        core = [n for n in names if n.endswith(".dist-info/METADATA")]
        require(
            core == [dist_info + "/METADATA"],
            "physical wheel core METADATA is outside canonical dist-info directory",
        )
        identity = verify_core_metadata(z.read(core[0]), version)
    return {
        "filename": path.name,
        "platform": expected_platform,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "identity": identity,
        "record_files": count,
    }


def verify_publish_set(dist: Path, version: str) -> dict[str, object]:
    require(RE_FINAL_VERSION.fullmatch(version) is not None, "version invalid")
    require(dist.is_dir() and not dist.is_symlink(), "dist does not exist")
    files = sorted(p for p in dist.iterdir() if p.is_file())
    require(
        len(files) == 5 and not any(p.is_symlink() for p in files),
        "publish set must be EXACTLY 4 physical wheels and 1 sdist",
    )
    by_name = {p.name: p for p in files}
    require(
        len(by_name) == 5 and f"{DISTRIBUTION}-{version}.tar.gz" in by_name,
        "exact canonical sdist missing",
    )
    sdist = verify_sdist(by_name[f"{DISTRIBUTION}-{version}.tar.gz"], version)
    platforms = set()
    wheels = []
    for p in files:
        if p.name.endswith(".tar.gz"):
            continue
        m = RE_WHEEL.fullmatch(p.name)
        require(
            m is not None and m["version"] == version,
            "unknown/mock/foreign wheel in publication: " + p.name,
        )
        require(m["platform"] not in platforms, "duplicate target platform")
        platforms.add(m["platform"])
        wheels.append(verify_physical_wheel(p, version, m["platform"]))

    require(
        platforms == PLATFORMS,
        "one or more required physical Linux wheel platforms absent",
    )
    return {
        "status": "PUBLISH_SET_EXACT_PASS",
        "package": PROJECT,
        "version": version,
        "new_devpi_index": TARGET,
        "sdist": sdist,
        "wheels": wheels,
    }


def validate_project_json(path: Path, version: str, *, post: bool) -> dict[str, object]:
    """Require authenticated devpi JSON, no HTML/302 gateway as success."""
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), "devpi project JSON must be an object")
    result = data.get("result", data)
    require(isinstance(result, dict), "devpi result must be object")
    versions = [k for k in result if RE_FINAL_VERSION.fullmatch(str(k))]
    require(
        bool(result) and bool(versions),
        "empty/unrecognized devpi project JSON is not proof of authentication",
    )
    require(
        (version in versions) == post,
        "expected version collision before upload or missing version after upload",
    )
    if not post:
        require(
            not any(
                tuple(map(int, k.split("."))) >= tuple(map(int, version.split(".")))
                for k in versions
            ),
            "newer/equal devpi version already exists",
        )
    return {
        "status": "DEVPI_POSTVERSION_PRESENT" if post else "DEVPI_PREVERSION_ABSENT",
        "count_known_versions": len(versions),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    p = parser.add_subparsers(dest="op", required=True)
    a = p.add_parser("intent")
    a.add_argument("--root", type=Path, default=Path.cwd())
    a.add_argument("--event", required=True)
    a.add_argument("--before", default="")
    a.add_argument("--head", required=True)
    a.add_argument("--manual-publish", default="false")
    a.add_argument("--ref", required=True)
    a.add_argument("--repository", required=True)
    a = p.add_parser("publish-set")
    a.add_argument("--dir", type=Path, required=True)
    a.add_argument("--version", required=True)
    a = p.add_parser("verify-json")
    a.add_argument("--json", type=Path, required=True)
    a.add_argument("--version", required=True)
    a.add_argument("--post", action="store_true")
    args = parser.parse_args()
    try:
        if args.op == "intent":
            report = intent(
                root=args.root,
                event=args.event,
                before=args.before,
                head=args.head,
                manual_publish=args.manual_publish,
                ref=args.ref,
                repository=args.repository,
            )
            output = os.environ.get("GITHUB_OUTPUT")
            if output:
                with open(output, "a", encoding="utf-8") as fh:
                    fh.writelines(
                        f"{key}={report[key]}\n"
                        for key in (
                            "should_publish",
                            "current_version",
                            "previous_version",
                        )
                    )
        elif args.op == "publish-set":
            report = verify_publish_set(args.dir, args.version)
        else:
            report = validate_project_json(args.json, args.version, post=args.post)
        print(json.dumps(report, sort_keys=True))
        return 0
    except (
        PolicyError,
        OSError,
        KeyError,
        ValueError,
        zipfile.BadZipFile,
        tarfile.TarError,
        subprocess.CalledProcessError,
    ) as ex:
        print("FAIL_CLOSED_RELEASE_POLICY: " + str(ex), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
