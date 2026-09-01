#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import subprocess
import tarfile
import tempfile
from pathlib import Path

EXPECTED_ARCHIVE_SHA256 = "2e7723127e679af9a32b5910e5932a952b65f664b5624839ed3fd69853acb6f8"
EXPECTED_OUTPUT = "AARCH64_QEMU_SELFTEST_OK 1122334455667788"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("archive", type=Path)
    ap.add_argument("--expected-sha256", default=EXPECTED_ARCHIVE_SHA256)
    ns = ap.parse_args()
    archive = ns.archive.resolve()
    actual = sha256(archive)
    if actual != ns.expected_sha256:
        raise SystemExit(f"QEMU archive SHA256 mismatch: {actual} != {ns.expected_sha256}")
    with tempfile.TemporaryDirectory(prefix="wiringop-qemu-") as td:
        root = Path(td)
        with tarfile.open(archive, "r:gz") as tf:
            tf.extractall(root, filter="data")
        dirs = [p for p in root.iterdir() if p.is_dir()]
        if len(dirs) != 1:
            raise SystemExit(f"unexpected QEMU archive roots: {dirs}")
        bundle = dirs[0]
        qemu = bundle / "bin/qemu-aarch64-static"
        sysroot = bundle / "sysroot"
        selftest = bundle / "selftest/hello_aarch64"
        cp = subprocess.run(
            [str(qemu), "-L", str(sysroot), str(selftest)],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        out = cp.stdout.strip()
        if out != EXPECTED_OUTPUT:
            raise SystemExit(f"unexpected QEMU selftest output: {out!r}")
    print(f"QEMU_AARCH64_ACCEPTANCE_OK sha256={actual} output={EXPECTED_OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
