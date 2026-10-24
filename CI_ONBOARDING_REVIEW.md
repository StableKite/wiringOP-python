# R4B production ABI milestone — 2026-10-22 (PRE-CI / NOT ACCEPTED)

This paragraph supersedes the historical *pre-native-build* claims in the R1 review below; the original audit trail remains unchanged.

- **Windows CPython 3.15.0t mock ABI:** R4 W10 built the real native wheel from a self-contained source distribution and imported 54/54 extensions. The installed wheel passed **324/324** tests, including added parallel ISR callback and serial-close tests; **1,029 GIL-off assertions**, no failures/skips, JIT unavailable without Python downgrade. This is **mock hardware**, not a production device/hardware proof.
- **Production Linux glibc x86_64:** R4B corrected a serious prior defect where 54 physical native extensions each embedded a separate static copy of upstream wiringOP's mutable C globals. R4B now uses one installed **`libwiringop_backend.so`** for physical C functions while leaving the mock ABI statically linked. **54/54** production `.so` modules compile, install and import under ordinary **CPython 3.13.5** with Release/LTO. **46** physically call the shared backend; the remaining eight have no direct C dependency. Both `wiring_pi` and `wiring_pi_i2c` resolve `wiringPiNodes` to the *same address* in one process. All native module ELF `RUNPATH` values are relative (`$ORIGIN:$ORIGIN/..`) and there are no embedded copies of `wiringPiNodes`/`_wiringPiGpio`.
- **Real PEP 517 packaging:** `scikit-build-core==1.1.1` built `wiringop_nanobind-0.1.0-cp313-cp313-linux_x86_64.whl` (2,320,383 bytes; SHA256 `51c4aa5cd1213b00820cc7e5328fc0236b8edc45299905d4f91bf5f70c9ba441`). All **118 RECORD entries** and 54 native extensions plus one shared backend were verified byte-for-byte. After `pip --no-index --no-deps` isolated installation, all 54 imported and the physical shared-global ABI audit passed. **This is a raw `linux_x86_64` wheel, not audited manylinux/musllinux and NOT ready to publish.**
- **Fail-closed negative tests:** New `tools/audit_production_backend.py` checks exact ELF set, dynamic binding, relocatable RUNPATH, installed module import origins and common C-global storage. `tools/selftest_production_backend.py` confirms it rejects missing/duplicated shared backends and a legacy static extension. `tools/run_acceptance.py` was updated to require 54 native `.so` **plus one** shared C library, an exact 54-import set and these ELF/negative gates; the isolated `verify_install_tree` stage passed. **The entire run_acceptance command has not been re-executed.**
- Source identity remains parent HEAD `48dab399b560cd71e77280f4cd7cbbfe0181aebe`, pinned fork `53fe570936ebca007d6d76f26ef21ba9f2609ca6`, package `0.1.0`; **NO COMMIT / NO PUSH / NO DEVPI**.
- **Still required:** production ARM64/glibc and both musl platforms, newest final CPython free-threaded runtime per platform, physical Orange Pi device/real UART/GPIO concurrency safety, `auditwheel`/manylinux/musllinux relocatability, all original/strict quality gates, GitHub Actions 5+1 and authenticated devpi release verification. Do not claim acceptance or skip unavailable hardware tests.

---

# wiringOP-python 0.1.0 — next CI stages (review-only, no push)

**Review date:** 2026-10-21. **Status:** SOURCE-CONTRACT REVIEW; release not accepted.

## Proven source identity

- Current checked GitHub `main`: `48dab399b560cd71e77280f4cd7cbbfe0181aebe` (no newer head claimed).
- Historical OrangePi upstream base: `a7921ca2f5c124203be10d3418db70a2e15f3c10`.
- Current StableKite integrated fork and exact Gitlink: `53fe570936ebca007d6d76f26ef21ba9f2609ca6`.
- The base is an ancestor of the integrated fork (5 additional commits). No historical PR overlay is to be reapplied to the integrated source.
- A read-only GDrive Bridge check with fresh Git and initialized submodule proved index/tree/link/clean state and the UART, pseudoPins, and Release optimization markers. Exact Git archive from that fork was independently re-parsed with Clang. The resulting *entire* API manifest matches the reviewed manifest metadata+entries: 54 public headers, 260 functions, 19 structs, 207 fields, 26 globals, 664 macros.
- A fresh backend check using the same committed source passes for 54 mock C files and 48 production C files; C UART PTY and 64-bit pseudoPins C regressions pass on the local Linux environment. This does **not** establish compatibility with free-threaded CPython or Windows.

## Review-only patch boundaries

This patch touches only provenance checks, non-runtime docs/metadata, and a new runtime-policy verifier. No API binder `.cpp`, Python library, mirrored test, stub, upstream commit, package version, or `CMakeLists.txt` is changed. `tools/prepare_wiringop.py` now copies only the exact reviewed integrated fork, after strict verification, and never reapplies the two historical PR patch files.

`tools/ci_runtime_gate.py` is a **guard**, not evidence that the current binary is compatible with free threading. It rejects non-final/non-free-threaded interpreters, enabled GIL, missing JIT policy, an available-but-disabled JIT, stale commit SHA, a non-installed extension origin, fewer than 54 binary modules, fewer than 321 collected tests, a missing mirrored test, and any failed/skipped/xfailed test. A same-process GIL/JIT check is performed at every pytest setup. Synthetic tests only confirm the negative/positive validation logic; they do not prove a successful platform run.

## Mandatory unfinished implementation — no shortcuts

**1. Real native free-threaded extensions.** Migrate 54 manually configured `NB_MODULE` targets to an upstream-supported nanobind `FREE_THREADED` build configuration for exact nanobind 2.14.0. The nanobind runtime and every extension must have coherent FT build/link flags. Audit global state, C callbacks, GIL acquisition/release, object ownership, background threads and mutable global C structures for proper locking. Do not just compile `NB_FREE_THREADED` into wrappers and claim thread safety. Confirm on newest stable/final CPython t-build that `sys._is_gil_enabled()` remains false before/after every imported module and every pytest test.

**2. Windows-native backend.** Current C++ wrappers use `<unistd.h>`, `<dlfcn.h>` and POSIX APIs; CMake links `dl` and `m`, and upstream headers/C ABI are Linux-centric. Implement actual Windows x86_64 native C ABI mock shims for all 54 extension modules and correct pointer/buffer/thread/callback behavior. Keep 321+ tests and all 54 mirror files, plus negative/PTY/serial checks with honest Windows equivalents. No Linux-in-Windows substitution, no disabling modules, no placeholder return values to make tests pass.

**3. Five mandatory validator jobs.** Windows x86_64, Linux glibc x86_64/aarch64, Linux musl x86_64/aarch64. On Win/glibc use `actions/setup-python@v7` (`python-version: '3.x'`, `freethreaded: true`, `allow-prereleases: false`, `check-latest: true`). On Alpine/musl select numeric newest final free-threaded uv CPython, create venv at final path, never move it. Everywhere `PYTHON_JIT=1`, `PYTHON_GIL=0`; if JIT is available it must be enabled, otherwise retain latest t-build. Each platform must **build a real native wheel from the same exact source**, install it in an isolated environment, run all mirrored tests in the same FT/GIL-off process, use official nanobind.stubgen, verify headers/API docs/stubs/backend ABI, callbacks/buffers/serial, packaging/metadata, and exact module origins. Linux glibc x86_64 additionally runs SKLint strict/format, Ruff, Pyright strict, Pylint, Flake8/Wemake and CSpell without weakening checks. Release version remains 0.1.0.

**4. Native wheel publication policy.** Sixth job depends on all five successful validators. For normal pushes where `previous_version == current_version`, it must be validation-only: skip all devpi authentication, collision checks, artifact downloads for upload, upload and postverify. For explicit `workflow_dispatch publish=true` (or approved version increment), verify the exact platform/ABI wheels and one sdist, fail closed on collision with existing version, use only publish-job `DEVPI_TOKEN`, upload to approved `https://devpi.stablekite.com/StableKite/index/`, then redownload **every** artifact and verify exact bytes, size, SHA-256. Native wheels are not universal `py3-none-any`; wheel set and binary compatibility must be tested, including Linux manylinux/musllinux physical wheels; Windows win_amd64 is an isolated mock-only validation artifact and is excluded from any production publish set. No republish and no arbitrary version bump. A timed-out devpi endpoint is a STOP, not a reason to redirect credentials.

**5. Guarded Git lifecycle.** First get true Windows native/FT build and review exact patch paths. Then a separate reviewed commit **NO PUSH**, followed by exact origin/branch/HEAD/parent/clean-index and reviewed blob guards, fresh remote main recheck, and one ordinary non-force fast-forward push only after explicit approval. Monitor exact GH run/event/attempt and all logs. Do not label this package accepted before exact 5/5 platform success and sixth publish job (for real release, actual devpi SHA-256 postverify).

## Current evidence scope

- 14/14 source-contract unit scenarios succeeded, including output-copy safety, archival patch integrity and negative mismatch cases.
- 13/13 runtime policy synthetic positive/negative scenarios succeeded; actual installed-wheel free-threaded test was *not* performed.
- Local Clang entire manifest reproducibility succeeded against exact fork archive.
- Source-level native Linux backend symbols/PTY/pseudoPins checks succeeded.
- A03 GDrive Bridge Windows CPython 3.15.0t structural review passed all 9 checks, including exact 13-file SHA-256 overlay, initialized real submodule, upstream/negative tests, 54 layout checks, binding/stub/docs audits, and copy-only fork preparation. **No `.pyd` was compiled or tested on Windows**.
- None of the above proves a Windows native `.pyd`, installed free-threaded wheel, 321/321 runtime pytest on the five platforms, official current stubgen, GitHub 5+1 CI, or devpi upload.

Historical acceptance logs and archived patches remain unchanged as audit trail. Previous `pelco_d` real publication also remains OPEN due to devpi TCP timeout.


## R5 endpoint authority and native CI draft (2026-10-22)

The user explicitly replaced the devpi endpoint with `https://devpi.stablekite.com/` (no port 4438). Use `https://devpi.stablekite.com/StableKite/index/` as the candidate target index only after authenticated proof. The new endpoint answers anonymous HEAD with HTTP 302 redirect to `/+login`, **not** a verified token login. The strict 5+1 workflow in `.github/workflows/native-ci.yml` is a **no-push, unrun draft**: version-unchanged events are validation-only, positive publish is intentionally fail-closed before auth/upload until byte-exact authenticated postdownload is implemented. Hardware FT/manylinux/musllinux quality remain blockers. Older packages are scheduled for separate URL updates after this package finishes; this R5 does not modify them. See `CI_R5_ENDPOINT_AND_NATIVE_MATRIX_REVIEW.md`.
