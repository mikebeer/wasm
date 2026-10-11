"""Build the self-contained demo pages in dist/.
   python3 build_pages.py [apl|xbase]   (needs: npm i @bjorn3/browser_wasi_shim esbuild, run once in web/)"""
import base64, gzip, json, os, subprocess, sys
H=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(H,'..','dist')
def gz(p): return base64.b64encode(gzip.compress(open(p,'rb').read(),9)).decode()
def shim():
    out=os.path.join(H,'shim.js')
    if not os.path.exists(out):
        subprocess.check_call(['npx','esbuild','entry.js','--bundle','--minify','--format=iife','--outfile=shim.js'],cwd=H)
    return open(out).read()
def make(name,assets,progs,extra=''):
    t=open(os.path.join(H,name+'.template.html')).read()
    t=t.replace('/*SHIM*/',shim()).replace('/*ASSETS*/','const ASSETS='+json.dumps(assets)+';const PROGS='+json.dumps(progs)+';'+extra)
    open(os.path.join(D,name+'.html'),'w').write(t); print(name,round(len(t)/1e6,2),'MB')
which=sys.argv[1] if len(sys.argv)>1 else 'all'
if which in('apl','all'):
    A=os.environ.get('APL_SRC','/home/claude/mikebeer/apl')+'/examples/'
    inputs={'ask':'\'Mike\'\n41\n','guess':'50\n25\n37\n43\n40\n42\n'}
    progs=[{'name':f,'src':open(A+f).read(),'stdin':inputs.get(f[:-4],'')} for f in sorted(os.listdir(A)) if f.endswith('.apl')]
    seed=['v <- iota 12','v times v','reduce plus v','(2 3 rho iota 6) plus 10']
    make('apl',{'wasm':gz(os.path.join(D,'apl.wasm'))},progs,'const SEED='+json.dumps(seed)+';')
if which in('xbase','all'):
    X=os.environ.get('XBASE_SRC','/home/claude/xbase')+'/examples/'
    B=os.environ.get('RXBIN_DIR','/tmp/wasi/w')+'/'   # dir with xbase.rxbin, library.rxbin, classlib.rxbin
    assets={'wasm':gz(os.path.join(D,'rxvm.wasm'))}
    for m in ['xbase','library','classlib']: assets[m]=gz(B+m+'.rxbin')
    inputs={'guess':'50\n25\n37\n43\n40\n42\n','ask':'Mike\n41\n'}
    order=['hello','primes','bank','addrbook','guess','ask','errors','form']
    progs=[{'name':n+'.prg','src':open(X+n+'.prg').read(),'stdin':inputs.get(n,'')} for n in order]
    make('xbase',assets,progs)
