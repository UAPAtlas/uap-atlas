#!/usr/bin/env python3
from pathlib import Path
from playwright.sync_api import sync_playwright
import argparse, json, time

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--html',default=str(ROOT/'atlas-mobile.html'))
parser.add_argument('--url')
parser.add_argument('--out',default=str(ROOT/'qa'/'atlas-mobile'))
args=parser.parse_args()
URL=args.url or Path(args.html).resolve().as_uri()+f'?qa={int(time.time())}'
OUT=Path(args.out).resolve()
OUT.mkdir(parents=True,exist_ok=True)
results={}

def audit(page,label):
    errors=[]
    page.on('pageerror',lambda e: errors.append('pageerror:'+str(e)))
    page.on('console',lambda m: errors.append('console:'+m.text) if m.type=='error' else None)
    page.goto(URL,wait_until='load')
    page.wait_for_timeout(900)
    metrics=page.evaluate('''() => {
      const vis=e=>{const s=getComputedStyle(e),r=e.getBoundingClientRect();return s.display!=='none'&&s.visibility!=='hidden'&&r.width>0&&r.height>0};
      const small=[...document.querySelectorAll('body *')].filter(vis).map(e=>({tag:e.tagName,cls:String(e.className?.baseVal||e.className||''),text:(e.textContent||'').trim().slice(0,50),size:parseFloat(getComputedStyle(e).fontSize)})).filter(x=>x.size<10&&x.text);
      const targets=[...document.querySelectorAll('button,a[href],input,select,[role="button"]')].filter(vis).map(e=>{const r=e.getBoundingClientRect();return {tag:e.tagName,cls:String(e.className||''),w:r.width,h:r.height,text:(e.textContent||e.getAttribute('aria-label')||'').trim().slice(0,40)}}).filter(x=>x.w<40||x.h<40);
      return {page:document.body.dataset.mobilePage,sw:document.documentElement.scrollWidth,cw:document.documentElement.clientWidth,sh:document.documentElement.scrollHeight,ch:document.documentElement.clientHeight,small,targets,nav:[...document.querySelectorAll('.mobile-nav button')].map(b=>({page:b.dataset.page,h:b.getBoundingClientRect().height,w:b.getBoundingClientRect().width}))};
    }''')
    results[label]={'metrics':metrics,'errors':errors}
    return metrics,errors

with sync_playwright() as p:
    launch={'headless':True}
    system_chrome=Path('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome')
    if system_chrome.exists(): launch['executable_path']=str(system_chrome)
    browser=p.chromium.launch(**launch)
    portrait=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
    m,e=audit(portrait,'portrait-map')
    assert m['page']=='map' and m['sw']==m['cw'] and not e
    icon_audit=portrait.evaluate('''() => [...document.querySelectorAll('.mobile-nav button')].map(btn=>({page:btn.dataset.page,svg:btn.querySelectorAll(':scope > svg').length,before:getComputedStyle(btn,'::before').content}))''')
    assert all(x['svg']==1 and x['before'] in ('none','normal') for x in icon_audit), icon_audit
    portrait.screenshot(path=str(OUT/'01-map-portrait.png'),full_page=True)

    # marker selection updates peek and dossier CTA routes to page 3
    portrait.locator('.atlas-marker').first.dispatch_event('click')
    portrait.wait_for_timeout(350)
    peek=portrait.locator('#peekTitle').inner_text()
    assert peek and peek!='Tap a map marker'
    portrait.locator('#peekOpen').click()
    portrait.wait_for_timeout(500)
    assert portrait.evaluate("document.body.dataset.mobilePage")=='dossier'
    assert portrait.locator('.case-drawer .case-title').count()==1
    assert portrait.locator('.mobile-dossier-home').is_visible()
    portrait.screenshot(path=str(OUT/'03-dossier-portrait.png'),full_page=True)
    # dossier tabs
    assert portrait.locator('.drawer-tab').all_text_contents()==['BRIEF','TIMELINE','FILES / SOURCES']
    assert portrait.locator('.mobile-status').count()==1
    assert portrait.locator('[data-panel="brief"] .mobile-brief-context .drawer-box').count()==2
    for tab in ['timeline','sources']:
        portrait.locator(f'[data-tab="{tab}"]').click()
        assert portrait.locator(f'[data-panel="{tab}"].active').count()==1
    # Carousel or empty state must exist
    assert portrait.locator('.drawer-evidence').count()==1

    # cases page, search, row routing
    portrait.locator('.mobile-nav [data-page="cases"]').click()
    portrait.wait_for_timeout(300)
    assert portrait.evaluate("document.body.dataset.mobilePage")=='cases'
    cases_layout=portrait.evaluate('''() => {
      const s=document.querySelector('.stack-banner-right').getBoundingClientRect();
      const f=document.querySelector('.filter-chips').getBoundingClientRect();
      return {searchTop:s.top,filterTop:f.top,filterLeft:f.left,filterWidth:f.width,filterClientWidth:document.querySelector('.filter-chips').clientWidth,filterScrollWidth:document.querySelector('.filter-chips').scrollWidth,chipWidths:[...document.querySelectorAll('.filter-chips .fchip')].map(x=>x.getBoundingClientRect().width),viewport:innerWidth};
    }''')
    title_top=portrait.locator('#stackTitle').bounding_box()['y']
    assert title_top < cases_layout['searchTop'] < cases_layout['filterTop']
    assert cases_layout['filterLeft'] >= 0 and cases_layout['filterWidth'] <= cases_layout['viewport']
    assert cases_layout['filterScrollWidth'] > cases_layout['filterClientWidth']
    assert len(cases_layout['chipWidths'])==4 and min(cases_layout['chipWidths'][:3])>=112 and cases_layout['chipWidths'][3]>=146
    portrait.locator('#caseSearch').fill('Roswell')
    portrait.wait_for_timeout(250)
    assert portrait.locator('.case-row').count()>=1
    portrait.screenshot(path=str(OUT/'02-cases-portrait.png'),full_page=True)
    selected_id=portrait.locator('.case-row').first.get_attribute('data-id')
    portrait.locator('.case-row').first.click()
    portrait.wait_for_timeout(650)
    focused=portrait.evaluate('''id => ({
      page:document.body.dataset.mobilePage,
      selected:state.selectedCaseId,
      drawer:document.getElementById('drawerBackdrop').classList.contains('open'),
      zoom:state.zoom,
      view:svg.getAttribute('viewBox'),
      peek:document.getElementById('peekTitle').textContent,
      caseTitle:cases.find(c=>c.id===id)?.title
    })''',selected_id)
    assert focused['page']=='map' and focused['selected']==selected_id and not focused['drawer'],focused
    assert focused['zoom']>1 and focused['view']!='0 0 100 62',focused
    assert focused['peek']==focused['caseTitle'],focused
    portrait.locator('#peekOpen').click()
    portrait.wait_for_timeout(450)
    assert portrait.evaluate("document.body.dataset.mobilePage")=='dossier'
    assert selected_id in portrait.locator('.drawer-heading .eyebrow').inner_text()

    # Cortana banner returns home: map reset, no selected case, no dossier/hash state.
    portrait.locator('.mobile-dossier-home').click()
    portrait.wait_for_timeout(650)
    home=portrait.evaluate('''() => ({
      page:document.body.dataset.mobilePage,
      selected:state.selectedCaseId,
      event:state.selectedEventId,
      view:svg.getAttribute('viewBox'),
      drawer:document.getElementById('drawerBackdrop').classList.contains('open'),
      hash:location.hash,
      selectedMarkers:document.querySelectorAll('.atlas-marker.selected').length,
      beacon:document.querySelectorAll('.selection-beacon').length,
      peek:document.getElementById('peekTitle').textContent
    })''')
    assert home=={'page':'map','selected':None,'event':None,'view':'0 0 100 62','drawer':False,'hash':'#page=map','selectedMarkers':0,'beacon':0,'peek':'Tap a map marker'},home

    # fresh page for post-interaction metric audit
    portrait2=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,is_mobile=True,has_touch=True)
    m,e=audit(portrait2,'portrait-audit')
    assert m['sw']==m['cw'] and not e
    # Ignore intrinsic SVG shapes; meaningful CSS text is >=10px.
    meaningful_small=[x for x in m['small'] if x['tag'] not in ('svg','g','text','path','circle')]
    assert not meaningful_small, meaningful_small[:10]
    # Explicit rails can contain compact non-primary controls; primary mobile chrome must pass.
    bad_primary=[x for x in m['targets'] if any(k in x['cls'] for k in ('mobile-nav','peek-open','iconbtn','case-search','fchip','drawer-tab','drawer-navbtn'))]
    assert not bad_primary,bad_primary

    landscape=browser.new_page(viewport={'width':844,'height':390},device_scale_factor=1,is_mobile=True,has_touch=True)
    m,e=audit(landscape,'landscape-map')
    assert m['page']=='map' and m['sw']==m['cw'] and not e
    assert landscape.locator('.map-panel').is_visible()
    assert not landscape.locator('.mobile-nav').is_visible()
    landscape.screenshot(path=str(OUT/'04-map-landscape.png'),full_page=True)

    for width,height,label in [(375,812,'05-map-narrow.png'),(430,932,'06-map-large.png'),(768,1024,'07-tablet-portrait.png')]:
        extra=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1,is_mobile=True,has_touch=True)
        m,e=audit(extra,f'{width}x{height}-map')
        assert m['page']=='map' and m['sw']==m['cw'] and not e
        labels=extra.locator('.legend span').all_text_contents()
        assert labels==['Exact','Unresolved','Redacted','Orbital','Institutional']
        extra.screenshot(path=str(OUT/label),full_page=True)
        extra.close()
    browser.close()

(OUT/'audit.json').write_text(json.dumps(results,indent=2))
print(json.dumps({'status':'PASS','screenshots':7,'audit':str(OUT/'audit.json'),'results':results},indent=2))