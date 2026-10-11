# C89 interpreters on WebAssembly

Three single-file C89 interpreters from mikebeer, built with WASI SDK 24, no source changes:

| Name | Source | wasm |
|---|---|---|
| `apl.wasm` | [mikebeer/apl](https://github.com/mikebeer/apl) `apl_all.c` | 600 KB |
| `py.wasm` | [mikebeer/python](https://github.com/mikebeer/python) `c/py_all.c` (library files in `pylib/`) | 1.1 MB |
| `st.wasm` | [mikebeer/smalltalk](https://github.com/mikebeer/smalltalk) `c/st_all.c` (class library in `lib/`) | 550 KB |

    WASI_SDK=... sh build.sh apl ~/apl/apl_all.c
    node run.js ../dist/assets/apl.wasm DIR script.apl     # DIR is the root of the in-memory file system
    node run.js ../dist/assets/py.wasm  DIR prog.py        # DIR must hold pylib/
    node run.js ../dist/assets/st.wasm  DIR -L lib prog.st # DIR must hold lib/

- `wasm_stubs.c`: `tmpfile()` returning NULL (WASI has none; apl only uses it for `)COPY` of named objects)
  and `system()` returning -1 (Smalltalk's shell escape).
- `sjlj.js`: these interpreters recover from errors with `setjmp`/`longjmp`. The compiler turns those into calls to
  `saveSetjmp`, `testSetjmp` and `getTempRet0`, which the host provides (about 20 lines). The runtime needs the
  WebAssembly exception-handling proposal (Node 22, current Chrome, Firefox and Safari). `malloc` and `realloc` are
  exported for it.
