#!/usr/bin/env python3
"""Browser smoke/layout checks and optional PDF export. Requires Playwright Chromium."""
import argparse
import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--pdf',action='store_true')
parser.add_argument('--screenshots',action='store_true')
args=parser.parse_args()
out=HERE/'.validation';out.mkdir(exist_ok=True)

with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1280,'height':720},device_scale_factor=1)
    errors=[]; page.on('pageerror',lambda e:errors.append(str(e)))
    page.goto((HERE/'index.html').as_uri())
    page.wait_for_function('document.querySelectorAll("#toc button").length === 56')
    issues=[]
    for width,height in [(1280,720),(1440,900),(1920,1080),(390,844)]:
        page.set_viewport_size({'width':width,'height':height})
        for i in range(56):
            page.evaluate('(i)=>show(i)',i)
            check=page.evaluate('''()=>{
              const s=document.querySelector('.slide:not([hidden])');
              const content=s.querySelector('.slide-content').getBoundingClientRect();
              const copy=s.querySelector('.copy').getBoundingClientRect();
              const sr=s.getBoundingClientRect();
              const src=s.querySelector('.sources').getBoundingClientRect();
              const svg=s.querySelector('svg');
              const outside=[...svg.querySelectorAll('text')].filter(t=>{const b=t.getBBox();return b.x < -1 || b.x+b.width > 681 || b.y < -1 || b.y+b.height > 436}).map(t=>t.textContent);
              return {horizontal:document.documentElement.scrollWidth>innerWidth+1,
                      slideScroll:s.scrollHeight-s.clientHeight,
                      copyOutside:copy.top<content.top-2 || copy.bottom>content.bottom+2,
                      sourceOutside:src.bottom>sr.bottom+1,svgOutside:outside};
            }''')
            if check['horizontal'] or (width>900 and (check['slideScroll']>2 or check['copyOutside'] or check['sourceOutside'])) or check['svgOutside']:
                issues.append({'viewport':[width,height],'slide':i+1,**check})
            if args.screenshots and width==1280:page.screenshot(path=str(out/f'slide-{i+1:02d}.png'))
    # Navigation, modal, speaker notes, deep links and range-key isolation.
    page.set_viewport_size({'width':1280,'height':720})
    page.evaluate('show(0)');page.keyboard.press('ArrowRight');assert page.locator('#slide-2').is_visible()
    page.keyboard.press('o');assert page.locator('#toc-dialog').is_visible()
    page.keyboard.press('Escape');assert not page.locator('#toc-dialog').is_visible()
    # Focus returns to the overview button: single-key shortcuts still work there.
    page.keyboard.press('n');assert page.locator('#notes').is_visible()
    assert len(page.locator('#note-text').inner_text())>100
    page.keyboard.press('Escape');assert not page.locator('#notes').is_visible()
    page.goto((HERE/'index.html').as_uri()+'#slide-13');assert page.locator('#slide-13').is_visible()
    page.locator('#gamma').focus();page.keyboard.press('ArrowRight')
    assert page.locator('#gamma').input_value()=='2.1';assert page.locator('#slide-13').is_visible()
    page.locator('#gamma').fill('0.2');page.locator('#gamma').dispatch_event('input')
    assert '10.0000' in page.locator('#wa-result').inner_text()
    page.evaluate('show(19)');page.locator('#target').fill('0.8');page.locator('#target').dispatch_event('input')
    assert 'O = 0.0000' in page.locator('#density-result').inner_text()
    page.evaluate('show(29)')
    for _ in range(15):page.locator('#opt-step').click()
    assert '迭代 15 / 40' in page.locator('#opt-result').inner_text()
    page.locator('#opt-reset').click();assert '迭代 0 / 40' in page.locator('#opt-result').inner_text()
    page.evaluate('show(42)');page.locator('#congestion').fill('2');page.locator('#congestion').dispatch_event('input')
    assert 'r = 3.0000' in page.locator('#inflation-result').inner_text()
    # Mobile swipe and horizontal layout.
    page.set_viewport_size({'width':390,'height':844});page.evaluate('show(0)')
    page.evaluate('''()=>{
      const target=document.getElementById('slides');
      const first=new Touch({identifier:1,target,clientX:320,clientY:300});
      const last=new Touch({identifier:1,target,clientX:80,clientY:300});
      target.dispatchEvent(new TouchEvent('touchstart',{touches:[first],bubbles:true}));
      target.dispatchEvent(new TouchEvent('touchend',{changedTouches:[last],bubbles:true}));
    }''')
    assert page.locator('#slide-2').is_visible()
    if args.screenshots:page.screenshot(path=str(out/'mobile.png'))
    # Print all hidden slides in a stable teaching state and test physical-page layout.
    page.set_viewport_size({'width':1280,'height':720});page.emulate_media(media='print')
    page.evaluate('printBaseline()')
    print_issues=page.evaluate('''()=>[...document.querySelectorAll('.slide')].flatMap((s,i)=>{
       const sr=s.getBoundingClientRect(),c=s.querySelector('.copy').getBoundingClientRect(),f=s.querySelector('.sources').getBoundingClientRect();
       return f.bottom>sr.bottom || c.bottom>f.top ? [{slide:i+1,copyBottom:c.bottom,sourceTop:f.top,slideBottom:sr.bottom}] : [];
    })''')
    issues.extend({'print':v} for v in print_issues)
    if args.pdf:
        page.pdf(path=str(HERE/'gpl-deep-dive.pdf'),print_background=True,prefer_css_page_size=True,tagged=True,outline=True)
        pdf=(HERE/'gpl-deep-dive.pdf').read_bytes()
        assert len(re.findall(rb'/Type\s*/Page\b',pdf))==56
        assert b'/FontFile' in pdf
    # Reading artifacts do not depend on JS and must be locally reachable.
    for filename in ['notes.html','source-index.html']:
        page.goto((HERE/filename).as_uri());assert page.locator('h1').count()==1
    browser.close()
    result={'slides':56,'viewports':4,'console_errors':errors,'layout_issues':issues,'interactive_checks':'passed'}
    (out/'report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))
    if errors or issues:raise SystemExit(1)
