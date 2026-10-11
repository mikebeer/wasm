import { WASI, File, Directory, PreopenDirectory, ConsoleStdout, OpenFile } from "@bjorn3/browser_wasi_shim";
globalThis.__wasi = { WASI, File, Directory, PreopenDirectory, ConsoleStdout, OpenFile };
