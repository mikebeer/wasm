import { WASI, File, Directory, PreopenDirectory, ConsoleStdout, OpenFile } from "@bjorn3/browser_wasi_shim";
window.__wasi = { WASI, File, Directory, PreopenDirectory, ConsoleStdout, OpenFile };
