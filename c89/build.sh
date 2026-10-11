#!/bin/sh
# Build a C89 interpreter (apl, python or smalltalk) to WASM.
#   WASI_SDK=/path/to/wasi-sdk-24.0-x86_64-linux sh build.sh apl  /path/to/apl/apl_all.c
#   WASI_SDK=...                                   sh build.sh py   /path/to/python/c/py_all.c
#   WASI_SDK=...                                   sh build.sh st   /path/to/smalltalk/c/st_all.c
# Output: ../dist/assets/<name>.wasm
# setjmp/longjmp: wasi-sdk 24's clang lowers them to calls into three JS imports
# (saveSetjmp, testSetjmp, getTempRet0) plus wasm exception handling. sjlj.js supplies
# those imports; malloc/realloc must be exported for it.
set -e
: "${WASI_SDK:?set WASI_SDK}"
NAME=${1:?name: apl, py or st}; SRC=${2:?path to the single-file C source}
HERE=$(cd "$(dirname "$0")" && pwd)
if [ "$NAME" = py ]; then
  # py_all.c's numpy.random module assumes `unsigned long` has 64 bits (xoshiro256**). On wasm32 it has 32,
  # so default_rng().integers() loops forever and randn is wrong. Build from a copy that uses `unsigned long long`.
  PATCHED=$(mktemp "${TMPDIR:-/tmp}/py_all_wasm.XXXXXX.c")
  sed -e 's/^typedef unsigned long u64;/typedef unsigned long long u64;/' \
      -e 's/lim = ULONG_MAX - (ULONG_MAX % n);/lim = (~(u64)0) - ((~(u64)0) % n);/' "$SRC" > "$PATCHED"
  SRC=$PATCHED
fi
"$WASI_SDK/bin/clang" --sysroot="$WASI_SDK/share/wasi-sysroot" -O2 \
  -mexception-handling -mllvm -wasm-enable-sjlj \
  -D_WASI_EMULATED_PROCESS_CLOCKS -D_WASI_EMULATED_SIGNAL -D_WASI_EMULATED_MMAN \
  -Wno-deprecated-declarations -w \
  -o "$HERE/../dist/assets/$NAME.wasm" "$SRC" "$HERE/wasm_stubs.c" \
  -lm -lwasi-emulated-process-clocks -lwasi-emulated-signal -lwasi-emulated-mman -lsetjmp \
  -Wl,-z,stack-size=4194304 -Wl,--export=realloc -Wl,--export=malloc
ls -la "$HERE/../dist/assets/$NAME.wasm"
