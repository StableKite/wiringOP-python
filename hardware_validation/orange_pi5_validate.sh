#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'

ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PAYLOAD_ROOT="$(cd -- "$ROOT_DIR/.." && pwd)"
PROJECT="$PAYLOAD_ROOT/project"
DEPS="$PAYLOAD_ROOT/deps"
RESULTS="$PAYLOAD_ROOT/results"
WORK="$PAYLOAD_ROOT/work"
mkdir -p "$RESULTS"
rm -rf "$WORK"
mkdir -p "$WORK"

exec > >(tee "$RESULTS/orangepi5-validation.log") 2>&1

# Always package partial results as well: the Windows runner retrieves this archive
# even when a later gate fails, which makes the first hardware run diagnosable.
pack_results() {
  tar -C "$PAYLOAD_ROOT" -czf "$PAYLOAD_ROOT/results.tar.gz" results >/dev/null 2>&1 || true
}
trap pack_results EXIT

fail() { echo "VALIDATION_ERROR: $*" >&2; exit 1; }
need() { command -v "$1" >/dev/null 2>&1 || fail "required command not found: $1"; }
section() { printf '\n========== %s ==========\n' "$*"; }

section "Platform"
[[ ${EUID:-$(id -u)} -eq 0 ]] || fail "run as root"
MODEL_FILE=""
for f in /proc/device-tree/model /sys/firmware/devicetree/base/model; do
  [[ -r "$f" ]] && MODEL_FILE="$f" && break
done
[[ -n "$MODEL_FILE" ]] || fail "device-tree model file not found"
MODEL="$(tr -d '\000' < "$MODEL_FILE")"
ARCH="$(uname -m)"
echo "MODEL=$MODEL"
echo "ARCH=$ARCH"
[[ "$MODEL" == *"Orange Pi 5"* ]] || fail "expected Orange Pi 5 family, got: $MODEL"
[[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]] || fail "expected AArch64, got: $ARCH"

for c in bash gcc g++ make cmake python3 python3-config git patch tar sha256sum grep sed awk find tee tr wc head cp ln; do need "$c"; done

echo "GCC=$(gcc --version | head -1)"
echo "GXX=$(g++ --version | head -1)"
echo "CMAKE=$(cmake --version | head -1)"
echo "PYTHON=$(python3 --version)"
echo "CPU=$(grep -m1 -E 'model name|Hardware' /proc/cpuinfo || true)"

# Python development headers are needed by the nanobind production build.
PY_INCLUDE_DIR="$(python3 - <<'PY'
import sysconfig
print(sysconfig.get_path('include') or '')
PY
)"
[[ -n "$PY_INCLUDE_DIR" && -f "$PY_INCLUDE_DIR/Python.h" ]] || \
  fail "Python.h not found; install the matching python3-dev package"
echo "PYTHON_INCLUDE=$PY_INCLUDE_DIR"

# wiringOP's drcNet backend uses crypt(3). Check both the development header and
# the linkable library up front so a missing libcrypt/libxcrypt package produces
# an actionable error instead of failing halfway through the strict build.
if ! printf '#include <crypt.h>\nint main(void){ return crypt("x", "xx") == 0; }\n' | \
     gcc -x c - -Werror -lcrypt -o "$WORK/.crypt-probe" >/dev/null 2>&1; then
  fail "crypt.h/libcrypt development files are required (for Debian/Ubuntu install libcrypt-dev or libxcrypt-dev as appropriate)"
fi
rm -f "$WORK/.crypt-probe"
echo "LIBCRYPT_DEV_OK"

BASE="$PROJECT/extern/wiringOP"
PR1_PATCH="$PROJECT/upstream_prs/PR1-werror-cleanup.patch"
PR2_SEQ_PATCH="$PROJECT/patches/wiringOP/0002-wiringSerial-extended-UART.patch"
NB_ROOT="$DEPS/nanobind-2.14.0"
[[ -d "$BASE/wiringPi" ]] || fail "missing upstream source"
[[ -s "$PR1_PATCH" ]] || fail "missing PR1 patch"
[[ -s "$PR2_SEQ_PATCH" ]] || fail "missing PR2 integration patch"
[[ -f "$NB_ROOT/include/nanobind/nanobind.h" ]] || fail "missing exact nanobind source"
[[ -f "$DEPS/NANOBIND_SHA256SUMS.txt" ]] || fail "missing nanobind checksum manifest"
section "Verify exact nanobind dependency tree"
( cd "$NB_ROOT" && sha256sum -c "$DEPS/NANOBIND_SHA256SUMS.txt" ) >/dev/null
echo "NANOBIND_TREE_SHA256_OK"

grep -q 'NB_VERSION_MAJOR 2' "$NB_ROOT/include/nanobind/nanobind.h" || fail "wrong nanobind major"
grep -q 'NB_VERSION_MINOR 14' "$NB_ROOT/include/nanobind/nanobind.h" || fail "wrong nanobind minor"
grep -q 'NB_VERSION_PATCH 0' "$NB_ROOT/include/nanobind/nanobind.h" || fail "wrong nanobind patch"

if [[ -f "$PROJECT/hardware_validation/UPSTREAM_BASE_SHA256SUMS.txt" ]]; then
  section "Verify pinned upstream source"
  (cd "$BASE" && sha256sum -c "$PROJECT/hardware_validation/UPSTREAM_BASE_SHA256SUMS.txt") >/dev/null
  echo "UPSTREAM_BASE_SHA256_OK"
fi

JOBS="$(nproc 2>/dev/null || echo 4)"
[[ "$JOBS" =~ ^[0-9]+$ ]] || JOBS=4
(( JOBS > 8 )) && JOBS=8
VERSION="$(cat "$BASE/VERSION")"
COMMON_DEBUG='-O3 -DNDEBUG -Werror -mcpu=native'
COMMON_CC='gcc -flto'
STRICT_FLAGS=(-O3 -DNDEBUG -Werror -Wall -Wextra -Wformat=2 -Winline -flto -mcpu=native -D_GNU_SOURCE)

build_upstream_makefiles() {
  local src="$1" label="$2" log="$3"
  section "$label"
  {
    make -C "$src/wiringPi" clean || true
    make -C "$src/wiringPi" -j"$JOBS" V=1 CC="$COMMON_CC" DEBUG="$COMMON_DEBUG"
    make -C "$src/devLib" clean || true
    make -C "$src/devLib" -j"$JOBS" V=1 CC="$COMMON_CC" DEBUG="$COMMON_DEBUG" INCLUDE='-I. -I../wiringPi'
    ln -sf "libwiringPi.so.$VERSION" "$src/wiringPi/libwiringPi.so"
    ln -sf "libwiringPiDev.so.$VERSION" "$src/devLib/libwiringPiDev.so"
    make -C "$src/gpio" clean || true
    make -C "$src/gpio" -j"$JOBS" V=1 CC="$COMMON_CC" DEBUG="$COMMON_DEBUG" INCLUDE='-I../wiringPi -I../devLib' LDFLAGS='-L../wiringPi -L../devLib'
  } 2>&1 | tee "$log"
  grep -q -- '-Werror' "$log" || fail "$label did not compile with -Werror"
  grep -q -- '-O3' "$log" || fail "$label did not compile with -O3"
  grep -q -- '-flto' "$log" || fail "$label did not compile/link with -flto"
  grep -q -- '-mcpu=native' "$log" || fail "$label did not compile with -mcpu=native"
  echo "${label// /_}_OK"
}

section "PR1: strict warning-clean upstream"
PR1="$WORK/wiringOP-pr1"
cp -a "$BASE" "$PR1"
( cd "$PR1" && patch -p1 --forward --batch < "$PR1_PATCH" )
build_upstream_makefiles "$PR1" "PR1_NATIVE_WERROR_BUILD" "$RESULTS/pr1-build.log"

# Compile every non-example C translation unit too, not only the default ./build subset.
section "PR1: all 52 non-example C translation units"
OBJDIR="$WORK/pr1-strict-objects"
mkdir -p "$OBJDIR"
COUNT=0
while IFS= read -r rel; do
  COUNT=$((COUNT+1))
  case "$rel" in
    wiringPi/*) INC=(-I"$PR1/wiringPi") ;;
    devLib/*) INC=(-I"$PR1/devLib" -I"$PR1/wiringPi") ;;
    gpio/*) INC=(-I"$PR1/gpio" -I"$PR1/wiringPi" -I"$PR1/devLib" -I"$PR1") ;;
    wiringPiD/*) INC=(-I"$PR1/wiringPiD" -I"$PR1/wiringPi" -I"$PR1") ;;
  esac
  gcc -std=gnu11 -c "$PR1/$rel" "${INC[@]}" "${STRICT_FLAGS[@]}" -fPIC -o "$OBJDIR/${rel//\//_}.o"
done < <(cd "$PR1" && find devLib gpio wiringPi wiringPiD -type f -name '*.c' | sort)
[[ "$COUNT" -eq 52 ]] || fail "expected 52 non-example C translation units, got $COUNT"
echo "PR1_STRICT_TRANSLATION_UNITS_OK 52/52"

section "PR2: UART integration"
INTEGRATION="$WORK/wiringOP-integration"
cp -a "$PR1" "$INTEGRATION"
# Remove build products before patching/copying into CMake.
make -C "$INTEGRATION/wiringPi" clean >/dev/null 2>&1 || true
make -C "$INTEGRATION/devLib" clean >/dev/null 2>&1 || true
make -C "$INTEGRATION/gpio" clean >/dev/null 2>&1 || true
( cd "$INTEGRATION" && patch -p1 --forward --batch < "$PR2_SEQ_PATCH" )
build_upstream_makefiles "$INTEGRATION" "PR1_PR2_NATIVE_WERROR_BUILD" "$RESULTS/pr1-pr2-build.log"
python3 "$PROJECT/tools/test_serial_pty.py" --wiringop-source "$INTEGRATION" | tee "$RESULTS/serial-c-pty.log"
grep -q 'WIRING_SERIAL_EXT_PTY_OK' "$RESULTS/serial-c-pty.log" || fail "C UART PTY regression failed"

section "Production nanobind build with local optimization layer"
PYBUILD="$WORK/python-prod"
rm -rf "$PYBUILD"
cmake -S "$PROJECT" -B "$PYBUILD" \
  -DCMAKE_BUILD_TYPE=Release \
  -DNB_ROOT="$NB_ROOT" \
  -DWIRINGOP_USE_MOCK=OFF \
  -DWIRINGOP_SOURCE="$INTEGRATION" \
  2>&1 | tee "$RESULTS/cmake-configure.log"
grep -q 'Orange Pi 5 native build: enabling -mcpu=native' "$RESULTS/cmake-configure.log" || fail "CMake did not detect Orange Pi 5 native tuning"
cmake --build "$PYBUILD" --parallel "$JOBS" --verbose 2>&1 | tee "$RESULTS/cmake-build.log"
grep -q -- '-O3' "$RESULTS/cmake-build.log" || fail "production CMake build missing -O3"
grep -Eq -- '-flto([= ][^ ]*)?' "$RESULTS/cmake-build.log" || fail "production CMake build missing LTO flag"
grep -q -- '-mcpu=native' "$RESULTS/cmake-build.log" || fail "production CMake build missing -mcpu=native"
SO_COUNT="$(find "$PYBUILD/python/wiringop" -type f -name '*.so' | wc -l | tr -d ' ')"
[[ "$SO_COUNT" -eq 54 ]] || fail "expected 54 extension modules, got $SO_COUNT"
echo "PRODUCTION_EXTENSIONS_OK 54/54"

PYTHONPATH="$PYBUILD/python" python3 - "$PROJECT/api_manifest.json" <<'PY'
import importlib, json, pathlib, sys
manifest=json.loads(pathlib.Path(sys.argv[1]).read_text())
mods=sorted({h['python_module'] for h in manifest['headers']})
for name in mods:
    importlib.import_module(name)
print(f'PRODUCTION_IMPORT_OK {len(mods)}/{len(mods)}')
PY
PYTHONPATH="$PYBUILD/python" python3 "$PROJECT/tools/test_serial_python_pty.py" | tee "$RESULTS/serial-python-pty.log"
grep -q 'PYTHON_SERIAL_PROD_PTY_OK' "$RESULTS/serial-python-pty.log" || fail "Python UART PTY regression failed"

section "Installed package layout"
INSTALL="$WORK/install"
rm -rf "$INSTALL"
cmake --install "$PYBUILD" --prefix "$INSTALL" | tee "$RESULTS/cmake-install.log"
INSTALL_SO="$(find "$INSTALL" -type f -name '*.so' | wc -l | tr -d ' ')"
INSTALL_PYI="$(find "$INSTALL" -type f -name '*.pyi' | wc -l | tr -d ' ')"
INSTALL_TYPED="$(find "$INSTALL" -type f -name 'py.typed' | wc -l | tr -d ' ')"
[[ "$INSTALL_SO" -eq 54 ]] || fail "installed .so count: $INSTALL_SO"
[[ "$INSTALL_PYI" -eq 54 ]] || fail "installed .pyi count: $INSTALL_PYI"
[[ "$INSTALL_TYPED" -eq 1 ]] || fail "installed py.typed count: $INSTALL_TYPED"
PYTHONPATH="$INSTALL" python3 - "$PROJECT/api_manifest.json" <<'PY'
import importlib, json, pathlib, sys
manifest=json.loads(pathlib.Path(sys.argv[1]).read_text())
mods=sorted({h['python_module'] for h in manifest['headers']})
for name in mods:
    importlib.import_module(name)
print(f'INSTALL_IMPORT_OK {len(mods)}/{len(mods)}')
PY

git --version > "$RESULTS/toolchain.txt"
gcc --version | head -1 >> "$RESULTS/toolchain.txt"
g++ --version | head -1 >> "$RESULTS/toolchain.txt"
cmake --version | head -1 >> "$RESULTS/toolchain.txt"
python3 --version >> "$RESULTS/toolchain.txt" 2>&1
printf '%s\n' "$MODEL" > "$RESULTS/board-model.txt"
printf '%s\n' "$ARCH" > "$RESULTS/architecture.txt"
cat > "$RESULTS/SUMMARY.txt" <<EOF_SUMMARY
ORANGEPI5_ACCEPTANCE_OK
model=$MODEL
arch=$ARCH
pr1_werror=OK
pr1_all_translation_units=52/52
pr2_uart_c_pty=OK
production_extensions=54/54
production_import=54/54
python_uart_pty=OK
install_so=54
install_pyi=54
py_typed=1
optimization=-O3 -DNDEBUG -flto -mcpu=native
EOF_SUMMARY
cat "$RESULTS/SUMMARY.txt"

tar -C "$PAYLOAD_ROOT" -czf "$PAYLOAD_ROOT/results.tar.gz" results
printf '\nORANGEPI5_ACCEPTANCE_OK\n'
