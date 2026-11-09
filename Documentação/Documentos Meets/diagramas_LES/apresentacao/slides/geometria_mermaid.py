"""Extrai do SVG gerado pelo Mermaid (layout ELK) a posição dos nós e os pontos das arestas.
Serve de base de layout para os diagramas de classe, DER e MER redesenhados no draw.io.
Uso: python3 geometria_mermaid.py svg_dir saida.json arquivo.svg [...]"""
import json
import os
import sys

from playwright.sync_api import sync_playwright

JS = r"""() => {
  const svg = document.querySelector('svg');
  const vb = svg.viewBox.baseVal;
  svg.setAttribute('width', vb.width); svg.setAttribute('height', vb.height);
  svg.style.maxWidth = 'none';
  const r0 = svg.getBoundingClientRect();
  const nodes = [];
  svg.querySelectorAll('g.node').forEach(g => {
    const r = g.getBoundingClientRect();
    nodes.push({id: g.id, x: r.x - r0.x, y: r.y - r0.y, w: r.width, h: r.height});
  });
  const edges = [];
  svg.querySelectorAll('path[data-points]').forEach(p => {
    const pts = JSON.parse(atob(p.getAttribute('data-points')));
    const m = p.getScreenCTM();
    const out = pts.map(q => { const s = svg.createSVGPoint(); s.x = q.x; s.y = q.y; const t = s.matrixTransform(m); return [t.x - r0.x, t.y - r0.y]; });
    edges.push({id: p.id, pts: out});
  });
  return {w: vb.width, h: vb.height, nodes, edges};
}"""


def main():
    saida = sys.argv[2]
    res = json.load(open(saida)) if os.path.exists(saida) else {}
    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=os.environ.get('CHROMIUM'))
        pg = b.new_page(viewport={'width': 1200, 'height': 900})
        for f in sys.argv[3:]:
            pg.goto('file://' + os.path.abspath(f))
            res[os.path.splitext(os.path.basename(f))[0]] = pg.evaluate(JS)
        b.close()
    json.dump(res, open(saida, 'w'), indent=0)


if __name__ == '__main__':
    main()
