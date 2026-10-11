const { WASI } = require('node:wasi'); const fs=require('fs'); const makeEnv=require('./sjlj.js');
const [,, wasm, dir, ...args]=process.argv;
const wasi=new WASI({version:'preview1',args:['prog',...args],env:{},preopens:{'/':dir},returnOnExit:true});
let ex; const imp=Object.assign({wasi_snapshot_preview1:wasi.wasiImport},makeEnv(()=>ex));
const inst=new WebAssembly.Instance(new WebAssembly.Module(fs.readFileSync(wasm)),imp); ex=inst.exports;
process.exit(wasi.start(inst));
