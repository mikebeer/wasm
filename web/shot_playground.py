import sys, time
from playwright.sync_api import sync_playwright
out=sys.argv[1] if len(sys.argv)>1 else '/tmp'
only=sys.argv[2:] 
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1180,'height':820})
    errs=[]; pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m: errs.append(m.text) if m.type=='error' else None)
    pg.goto('http://localhost:8765/playground.html')
    pg.wait_for_function("!document.getElementById('run').disabled",timeout=30000)
    ids=pg.eval_on_selector_all('#chips button','els=>els.map(e=>e.dataset.id)')
    for i in ids:
        if only and i not in only: continue
        pg.click(f'#chips button[data-id="{i}"]')
        pg.click('#run')
        t=time.time()
        try:
            pg.wait_for_function("!document.getElementById('run').disabled",timeout=120000)
        except Exception as e:
            print(i,'TIMEOUT'); pg.click('#stop'); continue
        pg.wait_for_timeout(250)
        o=pg.inner_text('#out')
        print(f'== {i}  [{pg.inner_text("#stat")}]  {pg.input_value("#sel")}\n'+o[:260].rstrip())
        pg.screenshot(path=f'{out}/pg_{i}.png')
    print('ERRORS',errs[:5])
    b.close()
