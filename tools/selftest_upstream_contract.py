#!/usr/bin/env python3
"""Isolated negative/positive cases for fail-closed upstream fork provenance."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

import prepare_wiringop as preparation
import upstream_contract as target


def git(where: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(where), *args],
        text=True,
        stderr=subprocess.DEVNULL,
    ).strip()


def make_repo(where: Path) -> None:
    where.mkdir(parents=True, exist_ok=True)
    git(where, "init", "-q")
    git(where, "config", "user.email", "ci-selftest@example.invalid")
    git(where, "config", "user.name", "CI selftest")


def commit(where: Path, msg: str) -> str:
    git(where, "add", "-A")
    git(where, "commit", "-qm", msg)
    return git(where, "rev-parse", "HEAD")


def make_fixture(root: Path) -> tuple[Path, str, str]:
    make_repo(root)
    submodule = root / target.SUBMODULE
    make_repo(submodule)
    git(submodule, "remote", "add", "origin", target.FORK_URL)
    (submodule / "BASE.txt").write_text(
        "historical upstream baseline\n", encoding="utf-8"
    )
    base = commit(submodule, "historical baseline")
    files = {
        "wiringPi/wiringSerial.h": "serialContextCancelRead serialContextCancelWrite\n",
        "wiringPi/pseudoPins.c": "uintptr_t\n",
        "devLib/lcd.h": "__attribute__((format(printf\n",
        "devLib/scrollPhat.h": "__attribute__((format(printf\n",
        "Optimized.mk": "WIRINGOP_OPT_FLAGS ?= -O3\nWIRINGOP_LTO_FLAGS ?= -flto=auto\n",
    }
    for name, content in files.items():
        path = submodule / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    integration = commit(submodule, "integration of source contracts")
    (root / ".gitmodules").write_text(
        '[submodule "extern/wiringOP"]\n'
        "\tpath = extern/wiringOP\n"
        f"\turl = {target.FORK_URL}\n",
        encoding="utf-8",
    )
    archive = root / "patches/wiringOP"
    archive.mkdir(parents=True)
    for name in ("0001-werror-cleanup.patch", "0002-wiringSerial-extended-UART.patch"):
        (archive / name).write_text(
            "historical patch, never reapply\n", encoding="utf-8"
        )
    # The real release archive is mandatory in both checkout and sdist modes.
    embedded = root / preparation.ARCHIVE_PATH
    embedded.parent.mkdir(parents=True)
    shutil.copyfile(
        Path(preparation.__file__).resolve().parents[1] / preparation.ARCHIVE_PATH,
        embedded,
    )
    commit(root, "exact gitlink, provenance patches and submodule metadata")
    return submodule, base, integration


@contextmanager
def identity(base: str, integration: str):
    with (
        mock.patch.object(target, "BASE_SHA", base),
        mock.patch.object(target, "INTEGRATION_SHA", integration),
    ):
        yield


def expect_failed(root: Path, description: str, marker: str) -> None:
    try:
        target.verify_upstream(root)
    except target.UpstreamContractError as exc:
        if marker not in str(exc):
            raise AssertionError(f"{description}: wrong failure: {exc}") from exc
    else:
        raise AssertionError(f"{description}: missing required fail-closed rejection")
    print(f"PASS {description}")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="wiringop-upstream-selftest-") as temporary:
        root = Path(temporary) / "repo"
        sub, base, integration = make_fixture(root)
        with identity(base, integration):
            assert target.verify_upstream(root) == sub.resolve()
            target.verify_integrated_features(sub)
            target.assert_no_legacy_patch_application(root)
            print("PASS exact-index-tree-checkout-clean-ancestry-origin-features")
            archive = root / "patches/wiringOP/0001-werror-cleanup.patch"
            data = archive.read_text(encoding="utf-8")
            archive.write_text("modified archival patch\n", encoding="utf-8")
            try:
                target.assert_no_legacy_patch_application(root)
            except target.UpstreamContractError as exc:
                assert "archived provenance patch was modified" in str(exc)
            else:
                raise AssertionError("modified archival patch accepted")
            print("PASS_REJECT archival-patch-hash-drift")
            archive.write_text(data, encoding="utf-8")
            with mock.patch.object(preparation, "INTEGRATION_SHA", integration):
                out = root / "build/upstream/wiringOP"
                with mock.patch.object(
                    sys,
                    "argv",
                    [
                        "prepare_wiringop",
                        "--project-root",
                        str(root),
                        "--output",
                        str(out),
                    ],
                ):
                    assert preparation.main() == 0
                    assert (
                        json.loads(
                            (out / ".stablekite-prepared-source.json").read_text()
                        )["integration_sha"]
                        == integration
                    )
                    assert not (out / ".git").exists()
                    assert preparation.main() == 0
                print("PASS prepare-exact-copy-and-safe-rerun")
                unsafe = root / "build/unmarked-source"
                unsafe.mkdir(parents=True)
                sentinel = unsafe / "user-owned.txt"
                sentinel.write_text("keep\n", encoding="utf-8")
                with mock.patch.object(
                    sys,
                    "argv",
                    [
                        "prepare_wiringop",
                        "--project-root",
                        str(root),
                        "--output",
                        str(unsafe),
                    ],
                ):
                    try:
                        preparation.main()
                    except target.UpstreamContractError as exc:
                        assert "unmarked preexisting directory" in str(exc)
                    else:
                        raise AssertionError("unsafe overwrite accepted")
                assert sentinel.read_text() == "keep\n"
                print("PASS_REJECT unmarked-output-preexisting")
            with mock.patch.object(target, "INTEGRATION_SHA", "0" * 40):
                expect_failed(root, "gitlink-wrong-sha", "gitlink mismatch")
            with mock.patch.object(target, "BASE_SHA", "1" * 40):
                expect_failed(root, "missing-historical-base-object", "cat-file")
            changed = sub / "BASE.txt"
            changed.write_text("dirty\n", encoding="utf-8")
            expect_failed(root, "dirty-tracked", "dirty")
            git(sub, "checkout", "--", "BASE.txt")
            untracked = sub / "added.log"
            untracked.write_text("dirty\n", encoding="utf-8")
            expect_failed(root, "dirty-untracked", "dirty")
            untracked.unlink()
            git(
                sub,
                "remote",
                "set-url",
                "origin",
                "https://example.invalid/foreign.git",
            )
            expect_failed(root, "wrong-origin", "approved fork")
            git(sub, "remote", "set-url", "origin", target.FORK_URL)
            cfg = root / ".gitmodules"
            original_cfg = cfg.read_text(encoding="utf-8")
            cfg.write_text(
                original_cfg.replace(
                    target.FORK_URL, "https://example.invalid/foreign.git"
                ),
                encoding="utf-8",
            )
            expect_failed(root, "wrong-gitmodules-url", "authorized fork origin")
            cfg.write_text(original_cfg, encoding="utf-8")
            (sub / "wiringPi/wiringSerial.h").write_text(
                "removed approved API\n", encoding="utf-8"
            )
            try:
                target.verify_integrated_features(sub)
            except target.UpstreamContractError as exc:
                assert "missing approved integrated implementation" in str(exc), exc
            else:
                raise AssertionError("missing required features accepted")
            print("PASS missing-mandatory-fork-feature")
            git(sub, "checkout", "--", "wiringPi/wiringSerial.h")
            # An absent .git must not accidentally inherit the parent HEAD.
            dotgit = sub / ".git"
            hidden = sub / ".git.tmp"
            dotgit.rename(hidden)
            expect_failed(root, "uninitialized-submodule", "not initialized")
            hidden.rename(dotgit)
            # A different valid local checkout must not be accepted for a pinned gitlink.
            (sub / "late.txt").write_text("later change\n", encoding="utf-8")
            commit(sub, "unreviewed late commit")
            expect_failed(root, "unreviewed-submodule-head", "checkout differs")
            git(sub, "checkout", "--detach", integration)
            assert target.verify_upstream(root) == sub.resolve()
            print("PASS restored-clean-committed-sha")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
