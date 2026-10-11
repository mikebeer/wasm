"""Run every example of every language in the playground (needs: python3 -m http.server in dist/)."""
import sys, time
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1180,'height':820})
    pg.goto('http://localhost:8765/playground.html')
    pg.wait_for_function("!document.getElementById('run').disabled",timeout=30000)
    ids=pg.eval_on_selector_all('#chips button','els=>els.map(e=>e.dataset.id)')
    bad=0; total=0
    for i in ids:
        pg.click(f'#chips button[data-id="{i}"]')
        names=pg.eval_on_selector_all('#sel option','os=>os.map(o=>o.value)')
        for n in names:
            pg.select_option('#sel',n); pg.click('#run'); total+=1; t=time.time()
            try: pg.wait_for_function("!document.getElementById('run').disabled",timeout=45000); to=False
            except Exception: pg.click('#stop'); to=True
            pg.wait_for_timeout(100)
            st=pg.inner_text('#stat'); o=pg.inner_text('#out').strip()
            flag = 'TIMEOUT' if to else ('' if st.startswith('exit 0') else 'NONZERO')
            if not flag and not o: flag='EMPTY'
            if not flag and any(k in o for k in ('Traceback','ERROR','[vm error]','panic','PANIC')): flag='ERRTEXT'
            if flag: bad+=1; print(f'{flag:8} {i}/{n} [{st}] {o[:140]!r}')
    print(f'{total} examples, {bad} flagged')
    b.close()
