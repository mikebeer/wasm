"""Assemble dist/languages.json and dist/playground.html.
Run from anywhere:  python3 web/build_playground.py
Sources of the example programs are the sibling checkouts of the language repos (see REPOS)."""
import json, os, re
H=os.path.dirname(os.path.abspath(__file__)); D=os.path.join(H,'..','dist')
R=os.environ.get('REPOS','/home/claude')          # parent of the checkouts
def rd(p): return open(p,encoding='utf-8').read()
def ex(dirpath, exts, stdin=None, skip=(), label=None):
    out=[]
    for f in sorted(os.listdir(dirpath)):
        n,e=os.path.splitext(f)
        if e not in exts or n in skip: continue
        out.append({'name':f,'src':rd(os.path.join(dirpath,f)),'stdin':(stdin or {}).get(n,'')})
    return out
def sib(p,*alts):
    for q in (p,)+alts:
        if os.path.exists(os.path.join(R,q)): return os.path.join(R,q)
    raise SystemExit('missing '+p)
# cREXX programs are shipped as base64 of gzip in .txt files (static hosts serve text; the page unpacks them).
# To refresh them from freshly compiled programs: RXBIN_DIR=dir_with_*.rxbin python3 web/build_playground.py
import base64, gzip
RXBIN_DIR=os.environ.get('RXBIN_DIR')
if RXBIN_DIR:
    for f in os.listdir(RXBIN_DIR):
        if f.endswith('.rxbin'):
            open(os.path.join(D,'assets','rxbin',f[:-6]+'.txt'),'w').write(base64.b64encode(gzip.compress(open(os.path.join(RXBIN_DIR,f),'rb').read(),9)).decode())
RX=lambda *n:[{'url':'assets/rxbin/%s.txt'%x,'path':'%s.rxbin'%x,'gz64':True} for x in n]
COMMON=RX('library','classlib')
def bundle(srcdir,name,root):
    """pack a text library directory into one JSON file {relative path: text}"""
    d={}
    for dp,dn,fn in os.walk(srcdir):
        dn[:]=[x for x in dn if x!='__pycache__']
        for f in sorted(fn):
            if f.endswith(('.py','.st')): d[os.path.relpath(os.path.join(dp,f),srcdir)]=rd(os.path.join(dp,f))
    json.dump(d,open(os.path.join(D,'assets',name+'.json'),'w'),separators=(',',':'))
    return [{'bundle':'assets/%s.json'%name,'root':root}]
pas=sib('pascal/tests'); plm=sib('plm/examples')
langs=[
 {'id':'python','name':'Python','repo':'python','kind':'C89 to WASM','ext':'py','desc':'A Python 3 subset with a numpy, pandas and scipy subset.',
  'files':bundle(sib('mikebeer/python/pylib'),'pylib','pylib'),'steps':[{'engine':'py','args':['prog.py']}],
  'examples':ex(sib('mikebeer/python/tests'),{'.py'},skip=('15_import',))},
 {'id':'smalltalk','name':'Smalltalk','repo':'smalltalk','kind':'C89 to WASM','ext':'st','desc':'Smalltalk-80 core and class library, GNU Smalltalk bracket syntax.',
  'files':bundle(sib('mikebeer/smalltalk/lib'),'stlib','lib'),'steps':[{'engine':'st','args':['-L','lib','prog.st']}],
  'examples':ex(sib('mikebeer/smalltalk/examples'),{'.st'},stdin={'wordfreq':'the quick brown fox jumps over the lazy dog\nthe dog barks and the fox runs\n'})},
 {'id':'apl','name':'APL','repo':'apl','kind':'C89 to WASM','ext':'apl','desc':'Word-glyph APL: iota, rho, reduce plus. Nested arrays, lambdas, user operators.',
  'files':[],'steps':[{'engine':'apl','args':['prog.apl']}],
  'examples':ex(sib('mikebeer/apl/examples'),{'.apl'},stdin={'ask':"'Mike'\n41\n",'guess':'50\n25\n10\n5\n3\n'})},
 {'id':'lisp','name':'Lisp','repo':'lisp','kind':'cREXX on WASM','ext':'lisp','desc':'A Common Lisp subset.',
  'files':COMMON+RX('lisp'),'steps':[{'engine':'rxvm','args':['lisp','-a','prog.lisp']}],
  'examples':ex(sib('lisp/examples'),{'.lisp'})},
 {'id':'logo','name':'LOGO','repo':'logo','kind':'cREXX on WASM','ext':'logo','desc':'Turtle graphics; the drawing is an SVG shown beside the output.',
  'files':COMMON+RX('logo'),'steps':[{'engine':'rxvm','args':['logo','-a','prog.logo','out.svg']}],'result':'out.svg',
  'examples':ex(sib('logo-repo/examples','logo/examples'),{'.logo'})},
 {'id':'basic','name':'BASIC','repo':'basic','kind':'cREXX on WASM','ext':'bas','desc':'GW-BASIC and QuickBASIC style, with parts of FreeBASIC.',
  'files':COMMON+RX('basic'),'steps':[{'engine':'rxvm','args':['basic','-a','prog.bas']}],
  'examples':ex(sib('mikebeer/basic/examples'),{'.bas'},stdin={'guess':''.join('%d\n'%i for i in range(1,101))})},
 {'id':'snobol','name':'SNOBOL4','repo':'snobol','kind':'cREXX on WASM','ext':'sno','desc':'SNOBOL4 with the full pattern repertoire, tables and EVAL.',
  'files':COMMON+RX('snobol'),'steps':[{'engine':'rxvm','args':['snobol','-a','prog.sno']}],
  'examples':ex(sib('mikebeer/snobol/examples'),{'.sno'},stdin={'calc':'1+2*3\n(4+5)*6\n'})},
 {'id':'xbase','name':'xBase','repo':'xbase','kind':'cREXX on WASM','ext':'prg','desc':'Harbour and Clipper style language with DBF tables and indexes (kept in memory).',
  'files':COMMON+RX('xbase'),'steps':[{'engine':'rxvm','args':['xbase','-a','prog.prg']}],
  'examples':ex(sib('xbase/examples'),{'.prg'},stdin={'guess':'50\n25\n37\n43\n40\n42\n','ask':'Mike\n41\n'})},
 {'id':'pascal','name':'Pascal','repo':'pascal','kind':'cREXX on WASM','ext':'pas','desc':'Compiles to cREXX assembler; the assembler and VM both run in your browser.',
  'files':COMMON+RX('pascal','pasrt'),
  'steps':[{'engine':'rxvm','args':['pascal','-a','prog.pas','prog.rxas']},{'engine':'rxas','args':['prog']},{'engine':'rxvm','args':['prog','pasrt','-a'],'stdin':True}],
  'examples':ex(pas,{'.pas'},stdin={'input':rd(os.path.join(pas,'input.in'))})},
 {'id':'plm','name':'PL/M-80','repo':'PLM','kind':'cREXX on WASM','ext':'plm','desc':'Intel PL/M-80 compiled to cREXX assembler, then run.',
  'files':COMMON+RX('plm','plmrt'),
  'steps':[{'engine':'rxvm','args':['plm','-a','prog.plm','prog.rxas']},{'engine':'rxas','args':['prog']},{'engine':'rxvm','args':['prog','plmrt','-a'],'stdin':True}],
  'examples':ex(plm,{'.plm'},stdin={'sum':rd(os.path.join(plm,'sum.in'))})},
]
for l in langs:
    assert l['examples'],l['id']
    if len(l['steps'])==1: l['steps'][0]['stdin']=True
    l['default']=l['examples'][0]['name']
pref={'python':'01_basics.py','smalltalk':'hello.st','apl':'life.apl','lisp':'primes.lisp','logo':'star.logo','basic':'hanoi.bas','snobol':'roman.sno','xbase':'addrbook.prg','pascal':'sieve.pas','plm':'sieve.plm'}
for l in langs:
    if pref[l['id']] in [e['name'] for e in l['examples']]: l['default']=pref[l['id']]
manifest={'engines':{k:'assets/%s.wasm'%k for k in ('rxvm','rxas','apl','py','st')},'languages':langs}
json.dump(manifest,open(os.path.join(D,'languages.json'),'w'),separators=(',',':'))
print('languages.json',round(os.path.getsize(os.path.join(D,'languages.json'))/1e3),'KB')
page=rd(os.path.join(H,'playground.template.html')).replace('/*SHIM_JSON*/',json.dumps(rd(os.path.join(H,'shim.js'))))
open(os.path.join(D,'playground.html'),'w').write('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1">\n</head>\n<body>\n'+page+'\n</body>\n</html>\n'); print('playground.html',round(len(page)/1e3),'KB')
