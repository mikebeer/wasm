# cREXX on WebAssembly (experiment)

`rxvm.wasm` is the cREXX virtual machine built with WASI SDK 24 (1.8 MB). It runs ordinary `.rxbin` files,
compiled on the host with `rxc` and `rxas`.

    node run.js ../dist/rxvm.wasm DIR program [-a args]     # DIR is mounted as the file system root

The `.rxbin` library modules (`library.rxbin`, `rxfnsb`, ...) must be in DIR. Verified: hello world, the xBase
interpreter (`xbase.rxbin`) running DBF/index programs, stdin prompts. About 2.6x slower than native `rxvm`.

What it took: `-DCREXX_VM_HANDLER_PANEL=1`, `-D__linux__` for platform.c, `shim/shim.h` (ENOSYS stubs for
sockets/fork/signals) and `stubs.c` (no-op pthread, failing dlopen). Not done: `rxc`/`rxas` in WASM, plugins
loaded by dlopen (static ones such as decimal work), threads, a browser WASI shim.
