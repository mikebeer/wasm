// JS side of LLVM's setjmp table runtime (saveSetjmp/testSetjmp/getTempRet0)
function makeEnv(getExports){
  let id=0, ret=0;
  const H=()=>new Int32Array(getExports().memory.buffer);
  function save(env,label,table,size){
    let h=H(); id++; h[env>>2]=id;
    for(let i=0;i<size;i++){
      if(h[(table>>2)+i*2]===0){h[(table>>2)+i*2]=id;h[(table>>2)+i*2+1]=label;h[(table>>2)+i*2+2]=0;ret=size;return table;}
    }
    const n=size*2; table=getExports().realloc(table,8*(n+1));
    h=H(); for(let i=size*2;i<n*2+2;i++)h[(table>>2)+i]=0;
    table=save(env,label,table,n); ret=n; return table;
  }
  return {env:{
    saveSetjmp:save,
    testSetjmp:(id2,table,size)=>{const h=H();for(let i=0;i<size;i++){const c=h[(table>>2)+i*2];if(c===0)break;if(c===id2)return h[(table>>2)+i*2+1];}return 0;},
    getTempRet0:()=>ret
  }};
}
if(typeof module!=='undefined')module.exports=makeEnv;
