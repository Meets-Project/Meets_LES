"""Renderiza .drawio em PNG usando viewer-static.min.js do draw.io (offline) no Playwright.
Uso: python3 render.py saida_dir arquivo.drawio [...]  (escala 2)"""
import json, os, sys
from playwright.sync_api import sync_playwright
VIEWER = os.environ.get('DRAWIO_VIEWER', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'viewer-static.min.js'))
PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>body{margin:0;background:#fff} .mxgraph{display:inline-block}</style>
<script>window.STYLE_PATH='';window.STENCIL_PATH='';window.mxLoadResources=false;window.mxImageBasePath='';</script>
<script src="file://%s"></script></head><body><div id="g"></div>
<script>
function go(xml){var d=document.getElementById('g');
var doc=mxUtils.parseXml(xml);var v=new GraphViewer(d,doc.documentElement,{highlight:'none',nav:false,toolbar:'',resize:false,border:20});
window.__done=1;}
</script></body></html>""" % VIEWER

def main():
    out = os.path.abspath(sys.argv[1]); os.makedirs(out, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get("CHROMIUM"), args=['--allow-file-access-from-files'])
        pg = b.new_page(viewport={'width': 1000, 'height': 800}, device_scale_factor=2)
        pg.on('console', lambda m: print('console:', m.text) if m.type == 'error' else None)
        html = os.path.join(out, '_r.html'); open(html, 'w').write(PAGE)
        for f in sys.argv[2:]:
            pg.goto('file://' + html)
            pg.evaluate('x=>go(x)', open(f, encoding='utf-8').read())
            pg.wait_for_function('window.__done==1', timeout=20000)
            pg.wait_for_timeout(400)
            el = pg.query_selector('#g svg')
            name = os.path.splitext(os.path.basename(f))[0]
            el.screenshot(path=os.path.join(out, name + '.png'))
            print('ok', name)
        b.close()
main()
