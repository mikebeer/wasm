#!/bin/bash
## Build rxas.wasm (the cREXX assembler), needed by the Pascal and PL/M pages.
set -e
# WASI_SDK  wasi-sdk-24.0 directory;  CREXX_SRC  the cREXX src/ directory;  CREXX_BUILD  a native CMake build tree
# (it holds generated/ and assembler/rxasgrmr.c, rxasscan.c produced by lemon and re2c)
: "${WASI_SDK:?}"; : "${CREXX_SRC:?}"; : "${CREXX_BUILD:?}"
S=$CREXX_SRC; B=$CREXX_BUILD; GEN=$B/generated; AG=$B/assembler
W=$WASI_SDK; H=$(cd "$(dirname "$0")" && pwd)
INC="-I$GEN -I$S/assembler -I$AG -I$S/platform -I$S/binutils/include -I$S/avl_tree -I$S/inc -I$S/utf8"
CC="$W/bin/clang --sysroot=$W/share/wasi-sysroot --target=wasm32-wasi -O2 -DNDEBUG -D__linux__=1 -D_WASI_EMULATED_SIGNAL -D_WASI_EMULATED_PROCESS_CLOCKS -D_WASI_EMULATED_MMAN -std=gnu11 -w -include $H/shim/shim.h -I$H/shim $INC"
mkdir -p obj/rxas
SRCS="$S/assembler/rxastoke.c $S/assembler/rxaseror.c $AG/rxasscan.c $S/assembler/rxas_opt.c $S/assembler/rxas_flow.c $S/assembler/rxas_flow_batch.c $S/assembler/rxas_flow_pass.c $S/assembler/rxas_flow_graph.c $S/assembler/rxas_flow_analysis.c $S/assembler/rxas_flow_rewrite.c $S/assembler/rxas_flow_signal.c $S/assembler/rxas_flow_ssa.c $S/assembler/rxas_flow_use.c $S/assembler/rxas_flow_proof.c $AG/rxasgrmr.c $S/assembler/rxasassm.c $S/binutils/rxopmeta.c $S/assembler/rxaslib.c $S/assembler/rxas_dsl.c $S/assembler/rxasmain.c $S/avl_tree/avl_tree.c $S/platform/platform.c $S/platform/platform_tso.c $S/platform/platform_native.c $S/platform/text_codec.c $S/platform/oom.c $S/platform/rxinteger.c $S/binutils/rxbin.c $S/binutils/rxbin007.c $S/binutils/rxsignature.c $S/binutils/rxsha256.c $S/binutils/rxgraph.c"
echo $SRCS | tr ' ' '\n' | xargs -P4 -I{} sh -c "$CC -c {} -o obj/rxas/\$(basename {} .c).o"
$CC -c $H/rxas_stubs.c -o obj/rxas/zstubs.o
$CC obj/rxas/*.o -o $H/../dist/assets/rxas.wasm -lm -Wl,-z,stack-size=8388608 -lwasi-emulated-signal -lwasi-emulated-process-clocks -lwasi-emulated-mman
ls -la $H/../dist/assets/rxas.wasm
