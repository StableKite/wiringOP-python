#!/usr/bin/env python3
"""Prepare the exact reviewed wiringOP fork, from Git or a pinned sdist archive.

A developer checkout MUST prove its real Gitlink and initialized clean fork.
The self-contained sdist has no Git metadata; it MUST carry the exact byte-for-
byte git archive of the same integrated fork. Neither path fetches network data,
uses an unverified preexisting copy, or reapplies historical patches.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import stat
import zipfile
from pathlib import Path, PurePosixPath

from upstream_contract import (
    INTEGRATION_SHA,
    UpstreamContractError,
    assert_no_legacy_patch_application,
    verify_integrated_features,
    verify_upstream,
)

ARCHIVE_SHA256 = "ab7f6deaf06b7d800e447294d1c28c178c63f884cfddf64591bf948545f47c9c"
ARCHIVE_FILE_COUNT = 214
ARCHIVE_PATH = Path("support/upstream") / f"wiringOP-{INTEGRATION_SHA}-git-archive.zip"
MARKER = {"integration_sha": INTEGRATION_SHA, "source": "StableKite/wiringOP"}


def _trusted_archive(root: Path) -> Path:
    archive = root / ARCHIVE_PATH
    if (
        archive.is_symlink()
        or not archive.is_file()
        or not archive.resolve().is_relative_to(root)
    ):
        raise UpstreamContractError("missing or escaped exact integrated fork archive")
    if hashlib.sha256(archive.read_bytes()).hexdigest() != ARCHIVE_SHA256:
        raise UpstreamContractError(
            "pinned git archive SHA-256 differs from reviewed bytes"
        )
    return archive


def _extract_archive(archive: Path, dest: Path) -> None:
    with zipfile.ZipFile(archive) as zipped:
        if zipped.testzip() is not None:
            raise UpstreamContractError("integrated fork archive has corrupted CRC")
        entries = zipped.infolist()
        names = [info.filename for info in entries]
        if len(names) != len(set(names)):
            raise UpstreamContractError(
                "integrated fork archive contains duplicate names"
            )
        files = 0
        for info in entries:
            name = info.filename
            path = PurePosixPath(name)
            if (
                not name
                or name.startswith("/")
                or "\\" in name
                or ":" in name
                or any(
                    part in ("", ".", "..", ".git", "__pycache__")
                    for part in path.parts
                )
            ):
                raise UpstreamContractError(
                    "integrated fork archive contains unsafe path"
                )
            mode = info.external_attr >> 16
            if stat.S_IFMT(mode) not in (0, stat.S_IFDIR, stat.S_IFREG):
                raise UpstreamContractError(
                    "integrated fork archive contains link or special file"
                )
            target = dest.joinpath(*path.parts)
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zipped.read(info))
                files += 1
        if files != ARCHIVE_FILE_COUNT:
            raise UpstreamContractError(
                "integrated fork archive file count is not exact"
            )


def prepare(root: Path, requested: Path) -> Path:
    """Prepare a new, safely marked copy, never using an unverified fork."""
    root = root.resolve(strict=True)
    git_checkout = (root / ".git").exists()
    archive = _trusted_archive(root)
    source = None
    if git_checkout:
        source = verify_upstream(root)
        verify_integrated_features(source)
        assert_no_legacy_patch_application(root)

    if requested.is_symlink():
        raise UpstreamContractError("prepared source destination may not be a symlink")
    dest = requested.resolve()
    if (
        dest == root
        or (
            source is not None
            and (
                dest == source
                or source.is_relative_to(dest)
                or dest.is_relative_to(source)
            )
        )
        or (dest.is_relative_to(root) and not dest.is_relative_to(root / "build"))
    ):
        raise UpstreamContractError("unsafe prepared source output destination")
    expected_marker = {**MARKER, "integration_sha": INTEGRATION_SHA}
    marker = dest / ".stablekite-prepared-source.json"
    if dest.exists():
        if not marker.is_file() or marker.is_symlink():
            raise UpstreamContractError(
                "refusing to replace an unmarked preexisting directory"
            )
        try:
            recorded = json.loads(marker.read_text(encoding="utf-8"))
        except (ValueError, OSError) as exc:
            raise UpstreamContractError("invalid prepared source marker") from exc
        if recorded != expected_marker:
            raise UpstreamContractError("preexisting prepared source marker mismatch")
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if git_checkout:
        assert source is not None
        shutil.copytree(
            source, dest, ignore=shutil.ignore_patterns(".git"), symlinks=False
        )
    else:
        dest.mkdir()
        _extract_archive(archive, dest)
    verify_integrated_features(dest)
    marker.write_text(
        json.dumps(expected_marker, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(
        f"PREPARED_INTEGRATION_FORK_PASS {dest} source={'gitlink' if git_checkout else 'pinned-archive'}"
    )
    return dest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    parser.add_argument("--output", type=Path)
    ns = parser.parse_args()
    root = ns.project_root.resolve(strict=True)
    requested = ns.output or root / "build/upstream/wiringOP"
    prepare(root, requested)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
