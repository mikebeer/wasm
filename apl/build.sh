#!/bin/sh
# Build apl.wasm from mikebeer/apl (single-file apl_all.c).
#   WASI_SDK=/path/to/wasi-sdk-24.0-x86_64-linux  APL_SRC=/path/to/apl  sh build.sh
# setjmp/longjmp: wasi-sdk 24's clang lowers them to calls into three JS imports
# (saveSetjmp, testSetjmp, getTempRet0) plus wasm exception handling. sjlj.js supplies
# those imports; malloc/realloc must be exported for it.
set -e
: "${WASI_SDK:?set WASI_SDK}"; : "${APL_SRC:?set APL_SRC}"
HERE=$(cd "$(dirname "$0")" && pwd)
"$WASI_SDK/bin/clang" --sysroot="$WASI_SDK/share/wasi-sysroot" -O2 \
  -mexception-handling -mllvm -wasm-enable-sjlj \
  -D_WASI_EMULATED_PROCESS_CLOCKS -Wno-deprecated-declarations \
  -o "${OUT:-$HERE/../dist/apl.wasm}" "$APL_SRC/apl_all.c" "$HERE/wasm_stubs.c" \
  -lm -lwasi-emulated-process-clocks -lsetjmp \
  -Wl,-z,stack-size=4194304 -Wl,--export=realloc -Wl,--export=malloc
