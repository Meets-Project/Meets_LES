"""Gera as imagens dos slides de diagrama para a cópia do deck original (55 slides)
com os diagramas em layout ELK (fontes em ../fontes-elk, PNGs em ../elk).
O diagrama de casos de uso, os slides de texto/especificação e as sequências
coloridas de visão geral (slides 25 e 34) continuam com a imagem original.
Uso: CHROMIUM=... python3 gerar_slides_elk.py [n ...]
"""
import os
import sys

import gerar_slides as g

g.TOTAL = 55
ELK = os.path.join(g.DIAG, 'elk')
SAIDA = os.path.join(g.AQUI, 'png-elk')
CAP = {c[1]: c for c in g.CAPITULOS}


def E(nome):
    return os.path.join(ELK, nome + '.png')


def k(caso):
    num, _c, nome, *_ = CAP[caso]
    return f'Cap. {num} · {caso} {nome}'


def slides():
    s = []
    d = g.diagrama
    s.append((2, d(2, 'Visão geral', 'Como funciona sem o sistema', 'Processo atual', E('sem-sistema'), 'Visão geral')))
    for n, arq, tit in [(3, 'negocio-1-evento', 'Atividade de negócio 1 — Organização e realização de evento'),
                        (4, 'negocio-2-conteudo', 'Atividade de negócio 2 — Publicação de conteúdo e interação'),
                        (5, 'negocio-3-moderacao', 'Atividade de negócio 3 — Moderação e controle de qualidade'),
                        (6, 'negocio-4-analise', 'Atividade de negócio 4 — Análise do desempenho da comunidade')]:
        s.append((n, d(n, 'Visão geral', tit, 'Diagrama de atividades', E(arq), 'Visão geral')))
    s.append((8, d(8, 'Visão geral', 'MER conceitual', 'Modelo entidade-relacionamento', E('mer-geral'), 'Visão geral')))
    for n, arq, tit in [(9, 'der-geral-1-usuarios-rede-comunicacao', 'DER — Usuários, perfil, rede e comunicação'),
                        (10, 'der-geral-2-conteudo-interacoes', 'DER — Conteúdo e interações'),
                        (11, 'der-geral-3-avaliacao-moderacao', 'DER — Avaliação, moderação e auditoria')]:
        s.append((n, d(n, 'Visão geral', tit, 'Modelo físico', E(arq), 'Visão geral')))
    mer = 'MER — recorte do caso de uso'
    der = 'DER — recorte do caso de uso'
    plano = {
        '#015': [(14, 'mer', 'mer-015-lembrete'), (15, 'der', 'der-015-lembrete'), (16, 'ativ', 'atividade-015-lembrete'),
                 (17, 'seq', 'sequencia-015-lembrete'), (18, 'cod', None)],
        '#005': [(21, 'mer', 'mer-005-avaliar-evento'), (22, 'der', 'der-005-avaliar-evento'), (23, 'cls', 'classe-005-avaliar-evento'),
                 (24, 'ativ', 'atividade-005-avaliar-evento'), (26, 'seq', 'sequencia-005-avaliar-evento'), (27, 'cod', None)],
        '#006': [(30, 'mer', 'mer-006-avaliar-apresentador'), (31, 'der', 'der-006-avaliar-apresentador'),
                 (32, 'cls', 'classe-006-avaliar-apresentador'), (33, 'ativ', 'atividade-006-avaliar-apresentador'),
                 (35, 'seq', 'sequencia-006-avaliar-apresentador'), (36, 'cod', None)],
        '#007': [(39, 'cls', 'classe-007-ranking'), (40, 'seq', 'sequencia-007-ranking'), (41, 'cod', None)],
        '#008': [(44, 'mer', 'mer-008-dashboards'), (45, 'der2', ('der-008a-dashboards-conteudo', 'der-008b-dashboards-avaliacoes')),
                 (46, 'cls', 'classe-008-dashboards'), (47, 'seq', 'sequencia-008-dashboards'), (48, 'cod', None)],
        '#013': [(51, 'mer', 'mer-013-denuncias'), (52, 'der', 'der-013-denuncias'), (53, 'cls', 'classe-013-denuncias'),
                 (54, 'seq', 'sequencia-013-denuncias'), (55, 'cod', None)],
    }
    for caso, itens in plano.items():
        nome = CAP[caso][2]
        for n, tipo, arq in itens:
            if tipo == 'mer':
                s.append((n, d(n, k(caso), mer, 'Modelo conceitual (Chen)', E(arq), caso)))
            elif tipo == 'der':
                s.append((n, d(n, k(caso), der, 'Modelo físico (PostgreSQL)', E(arq), caso)))
            elif tipo == 'der2':
                s.append((n, d(n, k(caso), der, 'Modelo físico (PostgreSQL)', None, caso, dupla=(E(arq[0]), E(arq[1])))))
            elif tipo == 'cls':
                s.append((n, d(n, k(caso), 'Diagrama de classe', 'Classes do domínio e do código', E(arq), caso)))
            elif tipo == 'ativ':
                s.append((n, d(n, k(caso), f'Diagrama de atividades — {nome}', 'Diagrama de atividades', E(arq), caso)))
            elif tipo == 'seq':
                s.append((n, d(n, k(caso), 'Diagrama de sequência — métodos do código', 'Sequência com os métodos do código', E(arq), caso)))
            else:
                s.append((n, g.sequencia_codigo(n, CAP[caso])))
    return s


def main(apenas=None):
    from playwright.sync_api import sync_playwright
    os.makedirs(SAIDA, exist_ok=True)
    os.makedirs(os.path.join(g.AQUI, 'tmp'), exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=os.environ.get('CHROMIUM'), args=['--allow-file-access-from-files'])
        pag = nav.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1.5)
        lista = slides()
        for n, conteudo in lista:
            if apenas and n not in apenas:
                continue
            arq = os.path.join(g.AQUI, 'tmp', f'elk-{n:02d}.html')
            with open(arq, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            pag.goto('file://' + arq)
            pag.wait_for_load_state('networkidle')
            pag.screenshot(path=os.path.join(SAIDA, f'slide-{n:02d}.png'))
        nav.close()
    print(f'{len(lista)} slides em {SAIDA}')


if __name__ == '__main__':
    main([int(a) for a in sys.argv[1:]] or None)
