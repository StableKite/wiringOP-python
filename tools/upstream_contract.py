"""Exact two-layer provenance contract for the wiringOP integration fork.

The historical upstream baseline is retained for provenance.  Production builds
consume the exact reviewed StableKite integration commit, *not* the baseline
plus an independently reapplied patch queue.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

BASE_SHA = "a7921ca2f5c124203be10d3418db70a2e15f3c10"
INTEGRATION_SHA = "53fe570936ebca007d6d76f26ef21ba9f2609ca6"
FORK_URL = "https://github.com/StableKite/wiringOP.git"
SUBMODULE = Path("extern/wiringOP")


class UpstreamContractError(RuntimeError):
    """An upstream provenance guard failed closed."""


def _git(cwd: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(cwd), *args],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise UpstreamContractError(
            f"git {' '.join(args)} failed (exit {result.returncode})"
        )
    return result.stdout.strip()


def verify_upstream(root: Path) -> Path:
    """Require exact index/HEAD gitlink, initialized clean fork, and base ancestry.

    No fetch, submodule init, patching, or other mutation occurs here.
    """
    root = root.resolve(strict=True)
    source = (root / SUBMODULE).resolve()
    if not source.is_dir() or not source.is_relative_to(root):
        raise UpstreamContractError("missing/escaped wiringOP submodule directory")
    if Path(_git(root, "rev-parse", "--show-toplevel")).resolve() != root:
        raise UpstreamContractError("project root does not match its Git repository")
    config = root / ".gitmodules"
    if not config.is_file():
        raise UpstreamContractError("missing .gitmodules")
    path = _git(
        root, "config", "-f", str(config), "--get", "submodule.extern/wiringOP.path"
    )
    url = _git(
        root, "config", "-f", str(config), "--get", "submodule.extern/wiringOP.url"
    )
    if path != SUBMODULE.as_posix() or url != FORK_URL:
        raise UpstreamContractError("wrong submodule path or authorized fork origin")

    indexed = _git(root, "ls-files", "-s", "--", SUBMODULE.as_posix())
    committed = _git(root, "ls-tree", "HEAD", "--", SUBMODULE.as_posix())
    expected_index = f"160000 {INTEGRATION_SHA} 0\t{SUBMODULE.as_posix()}"
    expected_tree = f"160000 commit {INTEGRATION_SHA}\t{SUBMODULE.as_posix()}"
    if indexed != expected_index or committed != expected_tree:
        raise UpstreamContractError(
            "Git index/HEAD gitlink mismatch with exact integration SHA"
        )

    # An uninitialized submodule directory would otherwise inherit the parent
    # repository's rev-parse HEAD, incorrectly giving a positive result.
    if not (source / ".git").exists():
        raise UpstreamContractError("wiringOP submodule is not initialized")
    if Path(_git(source, "rev-parse", "--show-toplevel")).resolve() != source:
        raise UpstreamContractError(
            "submodule Git context resolved to the wrong repository"
        )
    if _git(source, "rev-parse", "HEAD") != INTEGRATION_SHA:
        raise UpstreamContractError(
            "wiringOP checkout differs from pinned integration SHA"
        )
    if _git(source, "remote", "get-url", "origin") != FORK_URL:
        raise UpstreamContractError(
            "initialized submodule origin differs from approved fork"
        )
    if _git(source, "status", "--porcelain=v1", "--untracked-files=all"):
        raise UpstreamContractError("wiringOP submodule is dirty")
    _git(source, "cat-file", "-e", f"{BASE_SHA}^{{commit}}")
    _git(source, "cat-file", "-e", f"{INTEGRATION_SHA}^{{commit}}")
    relation = subprocess.run(
        [
            "git",
            "-C",
            str(source),
            "merge-base",
            "--is-ancestor",
            BASE_SHA,
            INTEGRATION_SHA,
        ],
        check=False,
        capture_output=True,
    )
    if relation.returncode != 0:
        raise UpstreamContractError(
            "pinned historical upstream is not an ancestor of integration fork"
        )
    return source


def verify_integrated_features(source: Path) -> None:
    """Protect required prior UART, warning, pseudoPins and LTO fixes."""
    markers = {
        "wiringPi/wiringSerial.h": (
            "serialContextCancelRead",
            "serialContextCancelWrite",
        ),
        "wiringPi/pseudoPins.c": ("uintptr_t",),
        "devLib/lcd.h": ("__attribute__((format(printf",),
        "devLib/scrollPhat.h": ("__attribute__((format(printf",),
        "Optimized.mk": (
            "WIRINGOP_OPT_FLAGS ?= -O3",
            "WIRINGOP_LTO_FLAGS ?= -flto=auto",
        ),
    }
    for filename, tokens in markers.items():
        candidate = source / filename
        if not candidate.is_file():
            raise UpstreamContractError(
                f"fork missing mandatory integrated source {filename}"
            )
        data = candidate.read_text(encoding="utf-8")
        if any(token not in data for token in tokens):
            raise UpstreamContractError(
                f"fork missing approved integrated implementation in {filename}"
            )


def assert_no_legacy_patch_application(root: Path) -> None:
    """Retain the patch files for audit, never execute against integrated fork."""
    required = {"0001-werror-cleanup.patch", "0002-wiringSerial-extended-UART.patch"}
    patch_folder = root / "patches/wiringOP"
    names = {p.name for p in patch_folder.glob("*.patch")}
    if names != required:
        raise UpstreamContractError(
            "archived provenance patch set changed unexpectedly"
        )
    for name in sorted(required):
        path = patch_folder / name
        if not path.is_file() or not path.stat().st_size:
            raise UpstreamContractError(f"missing nonempty archival patch {name}")
        # The active build never applies these. Still require their historical
        # bytes to match the source commit (no silent patch rewrites).
        committed_oid = _git(root, "rev-parse", f"HEAD:patches/wiringOP/{name}")
        present_oid = _git(root, "hash-object", "--", str(path))
        if present_oid != committed_oid:
            raise UpstreamContractError(
                f"archived provenance patch was modified: {name}"
            )


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    source = verify_upstream(root)
    verify_integrated_features(source)
    assert_no_legacy_patch_application(root)
    print(
        f"UPSTREAM_CONTRACT_PASS base={BASE_SHA} integration={INTEGRATION_SHA} source=StableKite/wiringOP overlays=already-integrated"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
