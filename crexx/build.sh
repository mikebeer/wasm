#!/bin/bash
# Build rxvm.wasm (the cREXX virtual machine) with WASI SDK 24.
# Usage: WASI_SDK=/path/to/wasi-sdk-24.0 CREXX_SRC=/path/to/CREXX/src GEN=/path/to/build/generated ./build.sh
set -e
: "${WASI_SDK:?}"; : "${CREXX_SRC:?}"; : "${GEN:?}"
H=$(cd "$(dirname "$0")" && pwd); mkdir -p "$H/obj"
S=$CREXX_SRC
INC="-I$GEN -I$S/interpreter -I$S/interpreter/rxvmplugin -I$S/assembler -I$S/binutils/include -I$S/rxpa -I$S/platform -I$S/avl_tree -I$S/utf8 -I$S/inc -I$S/interpreter/rxvmplugin/rxvmplugins/mc_decimal/decnumber -I$S/interpreter/rxvmplugin/rxvmplugins/mc_decimal"
# CREXX_VM_HANDLER_PANEL=1 (all handlers out of line): the default panel makes one 400k-line function
# that the WebAssembly backend cannot compile. __linux__ selects the POSIX code paths in platform.c.
CC="$WASI_SDK/bin/clang --sysroot=$WASI_SDK/share/wasi-sysroot --target=wasm32-wasi -O2 -DNDEBUG -DCREXX_VM_HANDLER_PANEL=1 -DNTHREADED=1 -D__linux__=1 -D_WASI_EMULATED_SIGNAL -D_WASI_EMULATED_PROCESS_CLOCKS -D_WASI_EMULATED_MMAN -std=gnu11 -w -include $H/shim/shim.h -I$H/shim $INC"
# srcs.txt: the sources of the rxbvm target (take them from `make -n -B rxbvm`), paths relative to $S
sed "s#/home/claude/crexx-src/src#$S#" "$H/srcs.txt" | xargs -P4 -I{} sh -c "$CC -c {} -o $H/obj/\$(basename {} .c).o"
$CC -c "$H/stubs.c" -o "$H/obj/zstubs.o"
# rxfloat is a dynamic plugin natively; link it in statically (its constructors register it). BASIC and SNOBOL4 need it.
$CC -DPLUGIN_ID=rxfloat -I$S/lib/plugins/float -c $S/lib/plugins/float/rxfloat.c -o "$H/obj/rxfloat.o"
$CC $H/obj/*.o -o "$H/../dist/rxvm.wasm" -lm -Wl,-z,stack-size=8388608 -lwasi-emulated-signal -lwasi-emulated-process-clocks -lwasi-emulated-mman
ls -la "$H/../dist/rxvm.wasm"
