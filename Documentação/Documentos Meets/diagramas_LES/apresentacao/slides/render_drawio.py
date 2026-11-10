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

def escala_para(css_w, css_h):
    """Escala do PNG em alta: lado maior até LADO_MAX px e no máximo AREA_MAX pixels."""
    lado = float(os.environ.get('LADO_MAX', 0))
    if not lado:
        return 2
    area = float(os.environ.get('AREA_MAX', 20e6))
    return min(lado / max(css_w, css_h), (area / (css_w * css_h)) ** 0.5)


def main():
    out = os.path.abspath(sys.argv[1]); os.makedirs(out, exist_ok=True)
    sufixo = os.environ.get('SUFIXO', '')
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
            bb = el.bounding_box()
            esc = escala_para(bb['width'], bb['height'])
            name = os.path.splitext(os.path.basename(f))[0]
            if esc != 2:
                ctx = b.new_context(viewport={'width': 1000, 'height': 800}, device_scale_factor=esc)
                p2 = ctx.new_page()
                p2.goto('file://' + html)
                p2.evaluate('x=>go(x)', open(f, encoding='utf-8').read())
                p2.wait_for_function('window.__done==1', timeout=20000)
                p2.wait_for_timeout(400)
                p2.query_selector('#g svg').screenshot(path=os.path.join(out, name + sufixo + '.png'))
                ctx.close()
            else:
                el.screenshot(path=os.path.join(out, name + sufixo + '.png'))
            print('ok', name, round(esc, 2))
        b.close()
main()
