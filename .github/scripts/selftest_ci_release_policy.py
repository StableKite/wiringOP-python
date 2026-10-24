#!/usr/bin/env python3
"""No-network release-policy tests; one behavior per positive/negative case."""

from __future__ import annotations

import base64
import csv
import hashlib
import importlib.util
import io
import json
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path

REF = "refs/heads/main"
REPO = "StableKite/wiringOP-python"

spec = importlib.util.spec_from_file_location(
    "policy", Path(__file__).with_name("ci_release_policy.py")
)
assert spec and spec.loader
policy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy)


def run(repo: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(repo), *args], text=True).strip()


def commit(repo: Path, message: str) -> str:
    run(repo, "add", "-A")
    run(
        repo,
        "-c",
        "user.name=CI Selftest",
        "-c",
        "user.email=ci@example.invalid",
        "commit",
        "-q",
        "-m",
        message,
    )
    return run(repo, "rev-parse", "HEAD")


def reject(func, why):
    try:
        func()
    except (
        policy.PolicyError,
        KeyError,
        ValueError,
        FileNotFoundError,
        zipfile.BadZipFile,
    ):
        print("PASS_REJECT", why)
    else:
        raise AssertionError("unsafe result accepted: " + why)


def sdist(path: Path, version: str):
    with tarfile.open(path, "w:gz") as t:
        roots = {
            "src": (".cpp", "src"),
            "tests": (".py", "tests"),
            "stubs": (".pyi", "stubs"),
            "mock": (".c", "support/mock_backend"),
        }
        entries = []
        for suffix, prefix in roots.values():
            entries.extend(
                [
                    f"{policy.DISTRIBUTION}-{version}/{prefix}/module{i}{suffix}"
                    for i in range(54)
                ]
            )
        entries.append(
            f"{policy.DISTRIBUTION}-{version}/support/upstream/{policy.PINNED_FORK_ARCHIVE_NAME}"
        )
        entries.append(f"{policy.DISTRIBUTION}-{version}/pyproject.toml")
        for name in entries:
            if name.endswith(policy.PINNED_FORK_ARCHIVE_NAME):
                root = Path(__file__).resolve().parents[2]
                data = (
                    root / "support/upstream" / policy.PINNED_FORK_ARCHIVE_NAME
                ).read_bytes()
            elif name.endswith("/pyproject.toml"):
                data = (
                    f'[project]\nname="{policy.PROJECT}"\nversion="{version}"\n'
                ).encode()
            else:
                data = b"content"
            info = tarfile.TarInfo(name)
            info.size = len(data)
            t.addfile(info, io.BytesIO(data))


def wheel(
    path: Path,
    version: str,
    platform: str,
    wrong_tag=False,
    wrong_record=False,
    extra_files: dict[str, bytes] | None = None,
    wrong_name=False,
    wrong_version=False,
    wrong_dist_info=False,
):
    basename = path.name[:-4].split("-", 2)[-1]
    files = {
        f"wiringop/wiring_pi/m{i}.cp315t-x86_64-linux-gnu.so": b"ELF" for i in range(54)
    }
    files["wiringop/libwiringop_backend.so"] = b"ELF_BACKEND"
    files.update(extra_files or {})
    metadata = (
        f"foreign_name-{version}.dist-info"
        if wrong_dist_info
        else f"{policy.DISTRIBUTION}-{version}.dist-info"
    )
    files[metadata + "/WHEEL"] = (
        "Wheel-Version: 1.0\nGenerator: test\nRoot-Is-Purelib: false\nTag: "
        + ("py3-none-any" if wrong_tag else basename)
        + "\n"
    ).encode()
    meta_name = "unrelated-other-package" if wrong_name else policy.PROJECT
    meta_version = "99.99.99" if wrong_version else version
    files[metadata + "/METADATA"] = (
        f"Metadata-Version: 2.3\nName: {meta_name}\nVersion: {meta_version}\n"
    ).encode()
    record_name = metadata + "/RECORD"
    rows = []
    for k, v in sorted(files.items()):
        digest = (
            base64.urlsafe_b64encode(hashlib.sha256(v).digest()).rstrip(b"=").decode()
        )
        if wrong_record and k.endswith("/WHEEL"):
            digest = "WRONG"
        rows.append([k, "sha256=" + digest, str(len(v))])
    rows.append([record_name, "", ""])
    buf = io.StringIO()
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerows(rows)
    files[record_name] = buf.getvalue().encode()
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for k, v in files.items():
            z.writestr(k, v)


def main():
    assert policy.HOST == "https://devpi.stablekite.com/"
    assert "4438" not in policy.TARGET
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        r = root / "repo"
        r.mkdir()
        run(r, "init", "-q")
        (r / "pyproject.toml").write_text(
            '[project]\nname="wiringop-nanobind"\nversion="0.1.0"\n'
        )
        pkg = r / "python/wiringop"
        pkg.mkdir(parents=True)
        (pkg / "__init__.py").write_text('__version__="0.1.0"\n')
        before = commit(r, "base")
        (pkg / "__init__.py").write_text('__version__="0.1.2"\n')
        reject(lambda: policy.project_version(r), "mismatched-duplicate-python-version")
        (pkg / "__init__.py").write_text('__version__="0.1.0"\n')
        (r / "ci.yml").write_text("test")
        head = commit(r, "CI-only")
        p = policy.intent(
            root=r,
            event="push",
            before=before,
            head=head,
            manual_publish="false",
            ref=REF,
            repository=REPO,
        )
        assert (
            p["should_publish"] == "false"
            and p["reason"] == "VALIDATION_ONLY_VERSION_UNCHANGED"
        )
        print("PASS validation-only push never publishes")
        reject(
            lambda: policy.intent(
                root=r,
                event="push",
                before="0" * 40,
                head=head,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            ),
            "missing-parent-sha",
        )
        reject(
            lambda: policy.intent(
                root=r,
                event="push",
                before="f" * 40,
                head=head,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            ),
            "unavailable-parent-object",
        )
        reject(
            lambda: policy.intent(
                root=r,
                event="push",
                before=before,
                head="f" * 40,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            ),
            "wrong-head",
        )
        reject(
            lambda: policy.intent(
                root=r,
                event="push",
                before=before,
                head=head,
                manual_publish="true",
                ref=REF,
                repository=REPO,
            ),
            "push-cannot-claim-manual",
        )
        reject(
            lambda: policy.intent(
                root=r,
                event="pull_request",
                before=before,
                head=head,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            ),
            "foreign-event",
        )
        assert (
            policy.intent(
                root=r,
                event="workflow_dispatch",
                before="",
                head=head,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            )["should_publish"]
            == "false"
        )
        assert (
            policy.intent(
                root=r,
                event="workflow_dispatch",
                before="",
                head=head,
                manual_publish="true",
                ref=REF,
                repository=REPO,
            )["should_publish"]
            == "true"
        )
        reject(
            lambda: policy.intent(
                root=r,
                event="workflow_dispatch",
                before="",
                head=head,
                manual_publish="true",
                ref="refs/heads/unreviewed",
                repository=REPO,
            ),
            "manual-nonmain-ref",
        )
        reject(
            lambda: policy.intent(
                root=r,
                event="workflow_dispatch",
                before="",
                head=head,
                manual_publish="true",
                ref=REF,
                repository="evil/project",
            ),
            "wrong-repository",
        )
        print("PASS explicit manual-only publication flag")
        (r / "pyproject.toml").write_text(
            '[project]\nname="wiringop-nanobind"\nversion="0.1.1"\n'
        )
        (pkg / "__init__.py").write_text('__version__="0.1.1"\n')
        bump = commit(r, "version bump")
        assert (
            policy.intent(
                root=r,
                event="push",
                before=head,
                head=bump,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            )["should_publish"]
            == "true"
        )
        print("PASS version bump guarded publish intent")
        outsider = root / "other"
        outsider.mkdir()
        run(outsider, "init", "-q")
        (outsider / "pyproject.toml").write_text(
            '[project]\nname="different"\nversion="1.0.0"\n'
        )
        stray = commit(outsider, "unrelated root")
        reject(
            lambda: policy.intent(
                root=r,
                event="push",
                before=stray,
                head=bump,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            ),
            "nonancestor-before-ref",
        )
        (r / "pyproject.toml").write_text(
            '[project]\nname="wiringop-nanobind"\nversion="0.1.0"\n'
        )
        (pkg / "__init__.py").write_text('__version__="0.1.0"\n')
        downgrade = commit(r, "downgrade")
        reject(
            lambda: policy.intent(
                root=r,
                event="push",
                before=bump,
                head=downgrade,
                manual_publish="false",
                ref=REF,
                repository=REPO,
            ),
            "downgrade",
        )
        dist = root / "dist"
        dist.mkdir()
        version = "0.1.0"
        name = f"wiringop_nanobind-{version}.tar.gz"
        sdist(dist / name, version)
        for plat in sorted(policy.PLATFORMS):
            wheel(
                dist / f"wiringop_nanobind-{version}-cp315-cp315t-{plat}.whl",
                version,
                plat,
            )
        valid = policy.verify_publish_set(dist, version)
        assert valid["status"] == "PUBLISH_SET_EXACT_PASS" and len(valid["wheels"]) == 4
        print("PASS exact 4 Linux physical wheels and sdist sha256 record")
        extra = dist / f"wiringop_nanobind-{version}-cp315-cp315t-win_amd64.whl"
        extra.write_bytes(b"MOCK")
        reject(lambda: policy.verify_publish_set(dist, version), "reject-windows-mock")
        extra.unlink()
        one = next(dist.glob("*.whl"))
        old = one.read_bytes()
        one.write_bytes(old[:-3])
        reject(lambda: policy.verify_publish_set(dist, version), "damaged-wheel")
        one.write_bytes(old)
        plat = next(iter(policy.PLATFORMS))
        p = dist / f"wiringop_nanobind-{version}-cp315-cp315t-{plat}.whl"
        wheel(p, version, plat, wrong_record=True)
        reject(lambda: policy.verify_publish_set(dist, version), "damaged-record")
        wheel(p, version, plat, wrong_tag=True)
        reject(lambda: policy.verify_publish_set(dist, version), "wrong-abi-tag")
        wheel(p, version, plat, wrong_name=True)
        reject(
            lambda: policy.verify_publish_set(dist, version),
            "foreign-project-metadata-even-with-valid-record",
        )
        wheel(p, version, plat, wrong_version=True)
        reject(
            lambda: policy.verify_publish_set(dist, version),
            "wrong-version-metadata-even-with-valid-record",
        )
        wheel(p, version, plat, wrong_dist_info=True)
        reject(
            lambda: policy.verify_publish_set(dist, version),
            "wrong-dist-info-even-with-valid-record",
        )
        wheel(p, version, plat)
        assert (
            policy.verify_publish_set(dist, version)["status"]
            == "PUBLISH_SET_EXACT_PASS"
        )
        wheel(
            p,
            version,
            plat,
            extra_files={"wiringop_nanobind.libs/libcrypt-12345678.so.1.1.0": b"ELF"},
        )
        assert (
            policy.verify_publish_set(dist, version)["status"]
            == "PUBLISH_SET_EXACT_PASS"
        )
        print("PASS auditwheel hashed sidecar native library verified through RECORD")
        wheel(
            p,
            version,
            plat,
            extra_files={
                "wiringop_nanobind.libs/libwiringop_backend-12345678.so.1.1.0": b"ELF"
            },
        )
        reject(
            lambda: policy.verify_publish_set(dist, version),
            "extra-gpio-backend-hidden-in-sidecar",
        )
        wheel(p, version, plat, extra_files={"unrelated/foreign.so": b"ELF"})
        reject(
            lambda: policy.verify_publish_set(dist, version),
            "arbitrary-native-shared-object",
        )
        wheel(p, version, plat)
        # auditwheel adds optional *empty directory* ZIP entries that RECORD
        # correctly does not list. These must not invalidate file-level hashes.
        with zipfile.ZipFile(p, "a") as z:
            z.writestr("wiringop/", b"")
            z.writestr(f"{policy.DISTRIBUTION}-{version}.dist-info/sboms/", b"")
        assert (
            policy.verify_publish_set(dist, version)["status"]
            == "PUBLISH_SET_EXACT_PASS"
        )
        print("PASS auditwheel empty ZIP directories omitted from RECORD")
        with zipfile.ZipFile(p, "a") as z:
            z.writestr("wiringop/extra_unrecorded_file.py", b"foreign")
        reject(
            lambda: policy.verify_publish_set(dist, version),
            "unlisted-real-file-after-auditwheel",
        )
        wheel(p, version, plat)
        (root / "project.json").write_text(
            json.dumps({"result": {"0.1.0": {"files": []}}})
        )
        reject(
            lambda: policy.validate_project_json(
                root / "project.json", "0.1.0", post=False
            ),
            "prepublish-version-collision",
        )
        assert (
            policy.validate_project_json(root / "project.json", "0.1.0", post=True)[
                "status"
            ]
            == "DEVPI_POSTVERSION_PRESENT"
        )
        (root / "project.json").write_text(json.dumps({"result": {"0.1.1": {}}}))
        reject(
            lambda: policy.validate_project_json(
                root / "project.json", "0.1.0", post=False
            ),
            "newer-existing-version",
        )
        (root / "project.json").write_text("<html>login redirect</html>")
        reject(
            lambda: policy.validate_project_json(
                root / "project.json", "0.1.0", post=False
            ),
            "redirect-html-not-auth-json",
        )
        (root / "project.json").write_text("{}")
        reject(
            lambda: policy.validate_project_json(
                root / "project.json", "0.1.0", post=False
            ),
            "empty-project-json",
        )
        (root / "project.json").write_text(json.dumps({"result": {"0.0.9": {}}}))
        assert (
            policy.validate_project_json(root / "project.json", "0.1.0", post=False)[
                "status"
            ]
            == "DEVPI_PREVERSION_ABSENT"
        )
    print("R5_PUBLISH_POLICY_NEGATIVE_SELFTESTS_PASS")


if __name__ == "__main__":
    main()
