const { WASI } = require('node:wasi');
const fs = require('fs');
const [,, wasm, dir, ...args] = process.argv;
const wasi = new WASI({ version: 'preview1', args: ['rxvm', ...args], env: {}, preopens: { '/': dir }, returnOnExit: true });
const mod = new WebAssembly.Module(fs.readFileSync(wasm));
const inst = new WebAssembly.Instance(mod, wasi.getImportObject());
process.exit(wasi.start(inst));
