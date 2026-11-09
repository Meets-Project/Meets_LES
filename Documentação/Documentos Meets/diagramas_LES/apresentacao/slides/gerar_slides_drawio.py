"""Slides da versão draw.io: os mesmos slides da versão "padrão", com os diagramas redesenhados
no draw.io (PNGs em ../drawio, fontes em ../fontes-drawio).

Gera só os slides que têm diagrama:
  padrão 2-6 (sem o sistema e atividades de negócio), B e C de cada caso de uso;
  stand-by: MER/DER gerais, recortes do MER e atividades #015/#005/#006 (numeração antiga).
Uso: CHROMIUM=... python3 gerar_slides_drawio.py   →  png-drawio/
"""
import os

from playwright.sync_api import sync_playwright

import gerar_padrao as gp
import gerar_slides as g
import gerar_slides_elk as gse

DRAWIO = os.path.join(g.DIAG, 'drawio')
SAIDA = os.path.join(g.AQUI, 'png-drawio')
gp.ELK = DRAWIO
gse.ELK = DRAWIO
STANDBY = [8, 9, 10, 11, 14, 21, 30, 44, 51, 16, 24, 33]   # numeração da versão anterior (55 slides)


def lista():
    s = []
    g.TOTAL = gp.TOTAL
    for n, html in gp.slides():
        if n in (2, 3, 4, 5, 6) or (isinstance(n, int) and n >= 8 and (n - 8) % 4 in (1, 2)):
            s.append((f'p{n:02d}', html))
    g.TOTAL = 55
    for n, html in gse.slides():
        if n in STANDBY:
            s.append((f'sb{n:02d}', html))
    return s


def main():
    os.makedirs(SAIDA, exist_ok=True)
    os.makedirs(os.path.join(g.AQUI, 'tmp'), exist_ok=True)
    itens = lista()
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=os.environ.get('CHROMIUM'), args=['--allow-file-access-from-files'])
        pag = nav.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1.5)
        for nome, html in itens:
            arq = os.path.join(g.AQUI, 'tmp', f'drawio-{nome}.html')
            with open(arq, 'w', encoding='utf-8') as f:
                f.write(html)
            pag.goto('file://' + arq)
            pag.wait_for_load_state('networkidle')
            pag.screenshot(path=os.path.join(SAIDA, f'drawio-{nome}.png'))
        nav.close()
    print(len(itens), 'slides em', SAIDA)


if __name__ == '__main__':
    main()
