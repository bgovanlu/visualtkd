"""Render chosen figures of a form large, side by side, to check new poses.

usage: python3 tools/check/figs.py keumgang 8,9,11,15 keumgang-poses.png   (ids as shown on the board; 준비 = ready)
"""
import os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "shots"); os.makedirs(OUT, exist_ok=True)
slug, ids, out = sys.argv[1], sys.argv[2].split(","), sys.argv[3]
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={"width": 1900, "height": 1200}, device_scale_factor=2)
    pg.goto(f"file://{ROOT}/site/{slug}/index.html"); pg.wait_for_timeout(800)
    pg.evaluate("""ids=>{const box=document.createElement('div');box.id='strip';
      box.style.cssText='display:flex;flex-wrap:wrap;gap:6px;background:#fff;padding:10px;position:fixed;inset:0;z-index:99;align-content:flex-start';
      ids.forEach(id=>{const el=[...document.querySelectorAll('#board .fig')].find(b=>b.querySelector('.no').textContent===id);if(!el)return;
        const c=document.createElement('div');c.style.cssText='width:220px;text-align:center;font:12px monospace';
        const svg=el.querySelector('svg.body').cloneNode(true);svg.style.height='260px';c.appendChild(svg);
        c.append(id+' '+el.querySelector('.en').textContent);box.appendChild(c)});document.body.appendChild(box)}""", ids)
    pg.locator("#strip").screenshot(path=f"{OUT}/{out}")
    br.close()
print("->", f"shots/{out}")
