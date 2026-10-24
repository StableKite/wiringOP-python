#!/bin/sh
# Executed INSIDE alpine:3.24, on a native matching-arch Linux GitHub runner.
set -eu
: "${GITHUB_SHA:?missing exact checkout sha}"
: "${WIRINGOP_MUSL_TARGET:?missing exact musllinux architecture tag}"
: "${WIRINGOP_OUTPUT_DIR:?missing bind-mounted output path}"
export PYTHON_GIL=0
export PYTHON_JIT=1
apk add --no-cache bash build-base ca-certificates cmake curl git jq linux-headers \
  make musl-dev patchelf binutils python3 py3-pip
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="/root/.local/bin:$PATH"
# Derive strict final numeric X.Y.Z from uv's actual musl architecture inventory.
# A prerelease, guessed 3.14 fallback or JIT-motivated downgrade is forbidden.
LATEST_VERSION="$(uv python list '>=3.14+freethreaded' \
  --all-versions --only-downloads --output-format json | jq -er '
  [ .[] | select(.implementation == "cpython")
          | select(.variant == "freethreaded")
          | select(.version | test("^[0-9]+\\.[0-9]+\\.[0-9]+$"))
          | .version ]
  | sort_by(split(".") | map(tonumber)) | last // empty')"
if [ -z "$LATEST_VERSION" ]; then
  echo 'FAIL_CLOSED: no final free-threaded musl CPython in uv inventory' >&2;exit 1
fi
PYTHON_SPEC="${LATEST_VERSION}+freethreaded"
echo "Using latest final musl CPython: $PYTHON_SPEC"
uv python install "$PYTHON_SPEC"
# The venv is created ONCE at its final path and is never moved.
uv venv --managed-python --seed --python "$PYTHON_SPEC" /tmp/wiringop-ft-venv
export PATH="/tmp/wiringop-ft-venv/bin:/root/.local/bin:$PATH"
python -m pip install --disable-pip-version-check 'auditwheel>=6' patchelf
python .github/scripts/ci_platform.py \
  --kind musl --platform "$WIRINGOP_MUSL_TARGET" --sha "$GITHUB_SHA" \
  --scratch /tmp/wiringop-native-build \
  --artifacts "$WIRINGOP_OUTPUT_DIR"
