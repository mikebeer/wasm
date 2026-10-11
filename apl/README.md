# APL on WebAssembly

`apl.wasm` is [mikebeer/apl](https://github.com/mikebeer/apl) (portable C89, word-glyph APL) built with
WASI SDK 24. 600 KB. No source changes.

    WASI_SDK=... APL_SRC=... sh build.sh
    node run.js ../dist/apl.wasm script.apl      # or pipe lines on stdin for the REPL

- `wasm_stubs.c`: `tmpfile()` returning NULL. WASI has none; apl only uses it for `)COPY` of named objects
  and reports "cannot create a temporary file".
- `sjlj.js`: apl recovers from errors with `setjmp`/`longjmp`. The compiler turns those into calls to
  `saveSetjmp`, `testSetjmp` and `getTempRet0`, which the host provides (this file, about 20 lines).
  The runtime needs engines with the WebAssembly exception-handling proposal (Node 22, current Chrome,
  Firefox and Safari).
