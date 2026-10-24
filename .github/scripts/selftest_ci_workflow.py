#!/usr/bin/env python3
"""Structural review of unpushed 5+1 workflow, without any GitHub execution."""

from __future__ import annotations

import sys
from pathlib import Path

import tomllib

try:
    import yaml
except ImportError as exc:
    raise SystemExit("FAIL_CLOSED: review tooling PyYAML is missing") from exc

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / ".github/workflows/native-ci.yml"
EXPECTED = (
    "windows_x86_64",
    "glibc_x86_64",
    "glibc_aarch64",
    "musl_x86_64",
    "musl_aarch64",
)
text = CONFIG.read_text(encoding="utf-8")
data = yaml.load(text, Loader=yaml.BaseLoader)
assert data["on"]["push"]["branches"] == ["main"]
assert data["on"]["workflow_dispatch"]["inputs"]["publish"]["default"] == "false"
assert list(data["jobs"]) == [*EXPECTED, "publish"]
assert set(data["jobs"]["publish"]["needs"]) == set(EXPECTED)
assert data["permissions"] == {"contents": "read"}
assert data["env"]["PYTHON_JIT"] == "1" and data["env"]["PYTHON_GIL"] == "0"
assert data["env"]["DEVPI_SERVER"] == "https://devpi.stablekite.com/"
assert (
    data["env"]["DEVPI_TARGET_INDEX"]
    == "https://devpi.stablekite.com/StableKite/index/"
)
assert ":4438" not in text and not any(
    s in text for s in ("continue-on-error", "|| true", "force-push")
)
assert all(data["jobs"][k]["timeout-minutes"] == "110" for k in EXPECTED)
for target in EXPECTED:
    job = data["jobs"][target]
    steps = job["steps"]
    assert any(
        s.get("uses") == "actions/checkout@v7"
        and s.get("with", {}).get("submodules") == "recursive"
        for s in steps
    ), target
    assert not any("DEVPI_TOKEN" in str(s) or "secrets." in str(s) for s in steps), (
        target
    )
    if not target.startswith("musl"):
        ps = [s for s in steps if s.get("uses") == "actions/setup-python@v7"]
        assert len(ps) == 1, target
        p = ps[0]["with"]
        assert p == {
            "python-version": "3.x",
            "freethreaded": "true",
            "allow-prereleases": "false",
            "check-latest": "true",
        }, target
    else:
        assert all(s.get("uses") != "actions/setup-python@v7" for s in steps)
        assert any("alpine:3.24" in s.get("run", "") for s in steps)
    assert any(
        "ci_platform.py" in s.get("run", "") or "ci_musl_entry.sh" in s.get("run", "")
        for s in steps
    ), target
    if target != "windows_x86_64":
        assert any(
            s.get("uses") == "actions/upload-artifact@v7"
            and s.get("with", {}).get("if-no-files-found") == "error"
            for s in steps
        )
    else:
        assert not any("wiringop-production" in str(s) for s in steps), (
            "mock leaked into production artifacts"
        )
steps = data["jobs"]["publish"]["steps"]
assert any("ci_release_policy.py intent" in s.get("run", "") for s in steps)
assert any(
    '--ref "$GITHUB_REF"' in s.get("run", "")
    and '--repository "$GITHUB_REPOSITORY"' in s.get("run", "")
    for s in steps
), "publisher must bind intent to exact main and repository"
assert any(
    "VALIDATION_ONLY_VERSION_UNCHANGED" in s.get("run", "")
    and s.get("if") == "steps.intent.outputs.should_publish == 'false'"
    for s in steps
)
assert any(
    s.get("uses") == "actions/download-artifact@v8"
    and s.get("if") == "steps.intent.outputs.should_publish == 'true'"
    and s.get("with", {}).get("pattern") == "wiringop-production-*"
    for s in steps
)
assert any("ci_release_policy.py publish-set" in s.get("run", "") for s in steps)
assert any(
    "FAIL_CLOSED: New devpi host SSO/token upload" in s.get("run", "")
    and s.get("if") == "steps.intent.outputs.should_publish == 'true'"
    for s in steps
)
assert not any(
    "devpi upload" in str(s) or "twine upload" in str(s) or "DEVPI_TOKEN:" in str(s)
    for s in steps
), "unreviewed publish operation present"
ci_musl = (ROOT / ".github/scripts/ci_musl_entry.sh").read_text()
assert (
    "uv python list" in ci_musl
    and "--all-versions" in ci_musl
    and "--only-downloads" in ci_musl
)
assert "uv python install" in ci_musl and "freethreaded" in ci_musl
assert "PYTHON_JIT=1" in ci_musl and "PYTHON_GIL=0" in ci_musl
assert (
    "uv venv --managed-python --seed" in ci_musl and " /tmp/wiringop-ft-venv" in ci_musl
)
assert ":4438" not in ci_musl
config = tomllib.loads((ROOT / "pyproject.toml").read_text())
assert config["project"]["version"] == "0.1.0"
assert config["tool"]["sklint"]["strict"] is True
assert config["tool"]["scikit-build"]["sdist"]["include"]
assert '"strict"' in (ROOT / "pyrightconfig.json").read_text()
sys.path.insert(0, str(ROOT / "tools"))
from generate_project import pyproject_text

assert pyproject_text() == (ROOT / "pyproject.toml").read_text(), (
    "generator would corrupt sdist/quality configuration"
)
print("CI_WORKFLOW_5_PLUS_1_STATIC_PASS")
print("DEVPI_NEW_ENDPOINT_REVIEWED_STATIC_PASS")
print("UNREVIEWED_PUBLICATION_FAIL_CLOSED_PASS")
print("GENERATOR_SDIST_AND_LINT_CONFIG_REPRODUCIBILITY_PASS")
