"""Versão em alta definição dos slides draw.io.

O diagrama deixa de ficar "assado" no fundo do slide:
  1. gera o fundo de cada slide SEM o diagrama (moldura, títulos e textos), em png-drawio-hd/;
  2. grava em png-drawio-hd/posicoes.json a área exata (em px do slide 1920×1080) onde cada
     diagrama aparece, para inserir o diagrama no Canva como elemento de imagem separado;
  3. os diagramas são renderizados à parte em alta resolução (render_drawio.py --escala).
Uso: CHROMIUM=... python3 gerar_slides_drawio_hd.py
"""
import json
import os

from playwright.sync_api import sync_playwright

import gerar_slides as g
import gerar_slides_drawio as gd

SAIDA = os.path.join(g.AQUI, 'png-drawio-hd')
JS = """() => [...document.querySelectorAll('img')].filter(i => i.src.includes('/drawio/')).map(i => {
  const r = i.getBoundingClientRect(), nw = i.naturalWidth, nh = i.naturalHeight;
  const s = Math.min(r.width / nw, r.height / nh), w = nw * s, h = nh * s;
  const nome = decodeURIComponent(i.src.split('/').pop()).replace('.png', '');
  i.style.visibility = 'hidden';
  return {nome, left: r.x + (r.width - w) / 2, top: r.y + (r.height - h) / 2, width: w, height: h};
})"""


def main():
    os.makedirs(SAIDA, exist_ok=True)
    pos = {}
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=os.environ.get('CHROMIUM'), args=['--allow-file-access-from-files'])
        pag = nav.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=2)
        for nome, html in gd.lista():
            arq = os.path.join(g.AQUI, 'tmp', f'drawio-hd-{nome}.html')
            with open(arq, 'w', encoding='utf-8') as f:
                f.write(html)
            pag.goto('file://' + arq)
            pag.wait_for_load_state('networkidle')
            pos[nome] = pag.evaluate(JS)
            pag.screenshot(path=os.path.join(SAIDA, f'fundo-hd-{nome}.png'))
        nav.close()
    json.dump(pos, open(os.path.join(SAIDA, 'posicoes.json'), 'w'), indent=1, ensure_ascii=False)
    print(len(pos), 'fundos em', SAIDA)


if __name__ == '__main__':
    main()
