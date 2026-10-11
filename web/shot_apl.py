import sys
from playwright.sync_api import sync_playwright
out=sys.argv[1] if len(sys.argv)>1 else '.'
html=open('../dist/apl.html').read()
open('/tmp/apl_full.html','w').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+html+'</body></html>')
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1100,'height':760})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto('file:///tmp/apl_full.html')
    pg.wait_for_function("!document.getElementById('cmd').disabled",timeout=60000)
    pg.wait_for_timeout(500)
    for l in ['x <- 3 4 rho iota 12','x','1 divide 0','reduce plus x']:
        pg.fill('#cmd',l); pg.press('#cmd','Enter'); pg.wait_for_timeout(300)
    print(pg.inner_text('#sout'))
    pg.screenshot(path=out+'/apl_session.png')
    pg.click('#t-scr'); pg.click('#run'); pg.wait_for_function("!document.getElementById('run').disabled"); pg.wait_for_timeout(300)
    print(pg.inner_text('#stat')); print(pg.inner_text('#out')[:400])
    pg.screenshot(path=out+'/apl_script.png'); print(errs)
    b.close()
