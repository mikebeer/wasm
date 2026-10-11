# cREXX on WebAssembly (experiment)

`rxvm.wasm` is the cREXX virtual machine built with WASI SDK 24 (1.9 MB). It runs ordinary `.rxbin` files,
compiled on the host with `rxc` and `rxas`.

    node run.js ../dist/rxvm.wasm DIR program [-a args]     # DIR is mounted as the file system root

The `.rxbin` library modules (`library.rxbin`, `rxfnsb`, ...) must be in DIR. Verified: hello world, the xBase
interpreter (`xbase.rxbin`) running DBF/index programs, stdin prompts. About 2.6x slower than native `rxvm`.

What it took: `-DCREXX_VM_HANDLER_PANEL=1`, `-D__linux__` for platform.c, `shim/shim.h` (ENOSYS stubs for
sockets/fork/signals) and `stubs.c` (no-op pthread, failing dlopen). Not done: `rxc`/`rxas` in WASM, plugins
loaded by dlopen (static ones such as decimal work), threads, a browser WASI shim.

## Update: assembler and float plugin

- `build_rxas.sh` builds `rxas.wasm` (0.9 MB) with the same shims; it needs only a stderr hook (`rxas_stubs.c`).
  Together with `rxvm.wasm` it runs the Pascal and PL/M compilers end to end: compile on the VM, assemble with `rxas.wasm`, run.
- `rxfloat` (used by BASIC and SNOBOL4) is a dynamic plugin natively. `build.sh` now compiles `rxfloat.c` with
  `-DPLUGIN_ID=rxfloat` and links it in; its constructors register it, so no `dlopen` is needed.
- Under Node 22, two Pascal programs that allocate with `new` (`pointers`, `tree`) crash the Node process intermittently
  (segfault inside Node's WASI layer); the same programs run correctly in Chromium.
