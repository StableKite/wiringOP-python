# R5 CI review — `StableKite/wiringOP-python` — 2026-10-22

**Status: PRE-CI / NO COMMIT / NO PUSH / NO DEVPI UPLOAD / NOT RELEASED.**

## User-approved devpi endpoint change

On 2026-10-22 the user explicitly replaced the old `https://stablekite.com:4438/` address with **`https://devpi.stablekite.com/`** (HTTPS without port 4438). The repository CI uses `https://devpi.stablekite.com/StableKite/index/` as the *candidate* index path; it is not yet authorized/verified for token upload. The authoritative shared Google Drive CI baseline and bridge requirements were updated in place and read back. This change does **not** authorize re-releasing unchanged version `0.1.0`.

Windows GDrive Bridge command `wiringop_R5_A01_devpi_new_endpoint_readonly_20261022.ps1` used .NET's certificate-validated default HTTPS client, without a token. HEAD `/` and `/StableKite/index/` both returned HTTP **302 redirect to `/+login`**, no TLS exception. This establishes TLS reachability, but **not token authentication, write permission, file transfer, or devpi API schema**. Redirects to login are NOT success. Auth must be proven in the publish-only path without exposing the token; release and byte-for-byte download verification remain blocked.

**Deferred:** once the current package/dependency CI work is complete, separately inventory and migrate older StableKite repository workflows and documentation to the new endpoint under their own exact-head/review/push safety controls. Do not silently mutate SKLint, DMA, pycrsf, pybetaflight, pelco_d or other repositories during R5; historical signed logs remain unchanged.

## Exact source and implementation scope

R5 starts from exact GitHub `main` HEAD `48dab399b560cd71e77280f4cd7cbbfe0181aebe` and restores all 27 reviewed R4B source files, independently checking each previous Git blob, current SHA256 and Git blob ID before edits. Pinned integrated wiringOP submodule Gitlink remains `53fe570936ebca007d6d76f26ef21ba9f2609ca6`. Canonical version remains **0.1.0**. A detailed before/after source manifest accompanies the R5 review archive.

R5's CI-only additions:

- `.github/workflows/native-ci.yml`: **5 explicit native validation jobs** (Windows x86_64, glibc x86_64/aarch64, musl x86_64/aarch64) and a **sixth dependent, version-aware publisher**. Windows validates real native mock `.pyd` and **never uploads a physical Windows wheel**. glibc and musl jobs build separate platform-specific physical Linux wheels and full 324+ Python tests via independently built mock native wheels.
- `.github/scripts/ci_platform.py`: builds a PEP 517 `sdist`, reassembles wheel without Git/submodule source override, validates 54 native imports and 324+ tests in the same free-threaded process with `PYTHON_GIL=0` / `PYTHON_JIT=1`, then uses `auditwheel repair` for physical Linux artifact candidates and audits the **single** shared C GPIO backend. Requires exact source commit and fails on unsupported architecture, missing platform tags, damaged wheel RECORD, or unsupported backend. This is **not yet executed in Actions**.
- `.github/scripts/ci_musl_entry.sh`: uses strict numeric latest-final free-threaded CPython reported by Alpine uv inventory; does not downgrade for JIT and never relocates the completed venv.
- `.github/scripts/ci_release_policy.py` plus negative selftests: canonical version `pyproject.toml` and `python/wiringop/__init__.py` agreement; usable previous Git commit and monotonic changes; unchanged push is validation-only; explicit manual `publish=true` required on dispatch; exact **four Linux physical wheels plus one SHA-pinned sdist**, no Windows mock wheel; native ABI/RECORD checking; reject unauthenticated HTML/SSO page, unknown project JSON and existing or newer version collision.
- `tools/ci_runtime_gate.py` strengthened from minimum 321 to **minimum 324** tests, preserving GIL/JIT runtime assertions and all 54 module-path coverage. Corresponding negative tests updated.
- `tools/audit_production_backend.py`: when called with `--require-free-threaded` checks GIL/JIT **before, after each of the 54 real physical extension imports, and afterward**. This supplements existing physical shared-global ELF audit; the older Python 3.13 normal-build audit is still supported without this new mandatory CI flag.
- Generator `tools/generate_project.py` now reproduces current `pyproject.toml`, preserving pinned vendor archive inclusion and build-junk exclusions. Added `[tool.sklint] strict=true` and `pyrightconfig.json` (`typeCheckingMode=strict`). Quality gates also call SKLint, Ruff check/format, Pyright, Pylint, Flake8/Wemake and CSpell; their actual tool results are **not yet known** and must not be presented as passed.

## Static/offline evidence obtained in R5

- `selftest_ci_release_policy.py`: positive version/validation-only cases and fail-closed negative cases for missing/wrong SHA, source duplicate version mismatch, version downgrade, Windows mock wheel contamination, malformed platform tags, damaged zip/RECORD, auth HTML, collision and empty/unknown project JSON: PASS.
- `selftest_ci_workflow.py`: Python YAML structure, exact 5+1 needs, only Linux production upload artifacts, correct new endpoint, setup-python v7 FT settings, Alpine uv selection, no validator secrets, no unreviewed upload, generated `pyproject` reproduction: PASS.
- Existing `selftest_ci_runtime_gate.py`, `selftest_sdist_source.py`, source syntax, Linux production ELF audit with existing ordinary CPython 3.13 wheel, and negative ELF tests: PASS.
- Real new R5 scikit-build-core 1.1.1 `sdist` constructed *locally* (not on GH Actions) and validated: 54 C++, 54 tests, 54 stubs, 54 mock C units, one byte-pinned integrated fork archive; see evidence report. It was not a release.
- GDrive Bridge TLS probe returned 302 to login for the new host/index path and generated a SHA-verified report, then was ACKed according to the protocol.

## Explicit blockers, NOT accepted

1. **Five GitHub Actions jobs have never been run for R5**. Static YAML verification is not GitHub execution. Auditwheel/manylinux and musllinux policies have not passed four physical FT Linux wheels. In particular, auditwheel may relocate the GPIO shared backend: if the resulting artifact has an unreviewed layout, the strict audit must FAIL instead of silently allowing split state.
2. Physical Orange Pi 5 device GPIO/UART/ISR concurrency behavior remains unproven under FT Linux; local Linux physical ABI smoke previously ran under ordinary Python 3.13.5 with no hardware. Mock FT tests are not hardware proof.
3. **Sixth publish job intentionally fail-closes on a positive publish request BEFORE auth or upload**, even if the exact publish set is good. The new endpoint's token-login/API compatibility and SHA-256 byte-identical post-download of every artifact require a separate implementation and acceptance before allowing any upload. An anonymous 302 to `/+login` must never be accepted as success. This is an incomplete publisher by design, not a completed release CI pipeline.
4. Strict quality lint tools have not been executed on Actions; their failures cannot be skipped or silenced. `nanobind==2.14.0` remains exact. Version remains 0.1.0.
5. No review commit, guarded push, workflow dispatch, artifact publishing, version bump or devpi credential use has been performed. Do not claim completed 5+1 acceptance.

## Follow-up order

First review R5 source manifest and unpushed diff against exact HEAD. Then resolve live native Linux FT, musl/aarch64, auditwheel policy, strict linters and Orange Pi hardware concurrency. In a separate guarded phase, prove new devpi token API and post-download byte-verified publish logic; only then consider one reviewed non-force fast-forward push, monitor exact GitHub SHA/run/event and validate all five platform jobs plus the sixth validation-only/publish outcome. After current dependencies are finished, schedule per-repository endpoint migrations for older StableKite packages; do not rewrite their historical evidence.

Authoritative docs:

- https://docs.google.com/document/d/1j2tvwmKPejO-VYkHAj09bdziXYlxMpEt__4A56SwrVE/edit
- https://docs.google.com/document/d/1GRDanxtOHiJtRkpid-y0VZk5isg2x4pGN0kxHmLodek/edit

Historic R4B handoff (immutable older endpoint text is superseded by this user instruction): https://drive.google.com/drive/folders/1ZxYxs5xWFfmKNUvuq1i_jvSLGN_oRNj0
