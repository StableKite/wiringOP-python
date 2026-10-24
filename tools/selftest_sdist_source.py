#!/usr/bin/env python3
"""Fail-closed tests of self-contained integrated-fork sdist preparation."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import zipfile
from pathlib import Path

from prepare_wiringop import (
    ARCHIVE_PATH,
    ARCHIVE_SHA256,
    MARKER,
    UpstreamContractError,
    prepare,
)


def rejected(label: str, action) -> None:
    try:
        action()
    except UpstreamContractError:
        print(f"PASS_REJECT {label}")
        return
    raise AssertionError(f"fail-open case: {label}")


def run() -> None:
    trusted = Path(__file__).resolve().parents[1] / ARCHIVE_PATH
    assert (
        trusted.is_file()
        and hashlib.sha256(trusted.read_bytes()).hexdigest() == ARCHIVE_SHA256
    )
    with tempfile.TemporaryDirectory(prefix="wiringop-sdist-selftest-") as directory:
        temp = Path(directory)
        root = temp / "sdist-source"
        (root / ARCHIVE_PATH.parent).mkdir(parents=True)
        archive = root / ARCHIVE_PATH
        shutil.copyfile(trusted, archive)
        output = temp / "extracted"
        built = prepare(root, output)
        assert built.samefile(output), (
            "prepared output must resolve to the same filesystem directory"
        )
        assert (
            json.loads((built / ".stablekite-prepared-source.json").read_text())
            == MARKER
        )
        with zipfile.ZipFile(trusted) as files:
            members = {
                item.filename: files.read(item)
                for item in files.infolist()
                if not item.is_dir()
            }
        selected = {
            p.relative_to(output).as_posix(): p.read_bytes()
            for p in output.rglob("*")
            if p.is_file() and p.name != ".stablekite-prepared-source.json"
        }
        assert selected == members, (
            "all 214 archived files must exactly match extracted bytes"
        )
        print("PASS exact-214-vendored-fork-files-no-git")
        prepare(root, output)
        print("PASS safe-repeat-after-exact-marker")
        broken = temp / "refuse-preexisting"
        broken.mkdir()
        rejected("unmarked-output", lambda: prepare(root, broken))
        (broken / ".stablekite-prepared-source.json").write_text('{"unreviewed":true}')
        rejected("wrong-marker", lambda: prepare(root, broken))
        rejected("output-is-project-root", lambda: prepare(root, root))
        rejected("output-inside-project-source", lambda: prepare(root, root / "extern"))
        git = root / ".git"
        git.mkdir()
        rejected(
            "git-checkout-does-not-fallback-to-archive",
            lambda: prepare(root, temp / "git-missing-link"),
        )
        git.rmdir()
        contents = bytearray(archive.read_bytes())
        contents[-1] ^= 1
        archive.write_bytes(contents)
        rejected(
            "one-byte-archive-corruption", lambda: prepare(root, temp / "tampered")
        )
        archive.unlink()
        rejected("archive-missing", lambda: prepare(root, temp / "missing"))
    print("SDIST_SOURCE_SELFTEST_PASS")


if __name__ == "__main__":
    run()
