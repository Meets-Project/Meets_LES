"""Gera os slides da versão "padrão" (3 slides por caso de uso), com os diagramas em ELK.

Abertura: 1 necessidade · 2 sem o sistema · 3-6 atividade de negócio · 7 casos de uso.
Para cada caso de uso:
  A) tela + descrição curta + RF, RN e RNF   (a tela entra no Canva como recorte da imagem original)
  B) diagrama de classe + DER
  C) diagrama de sequência + trecho do código + passos
  D) tela do app em tamanho grande (para ir e voltar a partir do slide C)
Uso: CHROMIUM=... python3 gerar_padrao.py   →  png-padrao/
"""
import html
import os
import sys

from PIL import Image

import gerar_slides as g
from codigo import CODIGO
from codigo_curto import CURTO
from fluxos import FLUXOS

TOTAL = 31
g.TOTAL = TOTAL
ELK = os.path.join(g.DIAG, 'elk')
SAIDA = os.path.join(g.AQUI, 'png-padrao')
sys.path.insert(0, g.GERADOR)
from casos_de_uso import UC  # noqa: E402

UC_ID = {u['id']: u for u in UC}
CAP = {c[1]: c for c in g.CAPITULOS}
ARQ = {
    '#015': ('classe-015-lembrete', 'der-015-lembrete', 'sequencia-015-lembrete'),
    '#005': ('classe-005-avaliar-evento', 'der-005-avaliar-evento', 'sequencia-005-avaliar-evento'),
    '#006': ('classe-006-avaliar-apresentador', 'der-006-avaliar-apresentador', 'sequencia-006-avaliar-apresentador'),
    '#007': ('classe-007-ranking', 'der-007-ranking', 'sequencia-007-ranking'),
    '#008': ('classe-008-dashboards', 'der-008-dashboards', 'sequencia-008-dashboards'),
    '#013': ('classe-013-denuncias', 'der-013-denuncias', 'sequencia-013-denuncias'),
}
UM_CELULAR = {'#015', '#007'}

CSS = g.CSS + """
.lado { position: absolute; left: 80px; top: 168px; width: 600px; }
.lado2 { position: absolute; left: 710px; top: 168px; width: 590px; }
.desc { font-size: 18px; line-height: 1.42; color: #292524; margin-bottom: 14px; }
.lado h3, .lado2 h3 { font-size: 12.5px; font-weight: 800; letter-spacing: 2.2px; color: #b4383b; margin: 0 0 7px; }
.fp { margin: 0 0 12px 0; padding-left: 22px; font-size: 15.8px; line-height: 1.36; color: #292524; }
.fp li { margin-bottom: 3px; }
.fl { display: grid; grid-template-columns: 44px 1fr; gap: 8px; margin-bottom: 6px; font-size: 15.8px; line-height: 1.36; color: #292524; }
.fl b { color: #fff; background: #2563eb; border-radius: 6px; text-align: center; font-size: 12px; padding: 2px 0; height: fit-content; }
.fl.fe b { background: #dc2626; }
.lado2 .rf { position: static; padding: 12px 18px; border-radius: 12px; margin-bottom: 14px; }
.lado2 .rf .k { font-size: 11.5px; }
.lado2 .rf h2 { font-size: 19px; margin: 4px 0 3px; }
.lado2 .rf p { font-size: 15.6px; line-height: 1.38; }
.lado2 .item { grid-template-columns: 62px 1fr; gap: 8px; margin-bottom: 7px; font-size: 15.2px; line-height: 1.35; }
.bloco { margin-bottom: 12px; }
.par { position: absolute; left: 52px; right: 52px; top: 82px; bottom: 44px; display: flex; gap: 22px; }
.par.col { flex-direction: column; }
.cel { flex: 1; min-width: 0; min-height: 0; background: #fff; border: 1px solid #ede7e4; border-radius: 18px;
       display: flex; flex-direction: column; padding: 10px 14px 12px; }
.cel .rot { font-size: 13px; font-weight: 800; letter-spacing: 2.2px; color: #b4383b; text-transform: uppercase; margin-bottom: 4px; }
.cel .img { flex: 1; min-height: 0; display: flex; align-items: center; justify-content: center; }
.cel img { max-width: 100%; max-height: 100%; object-fit: contain; }
.seq { position: absolute; left: 40px; top: 82px; width: 1230px; bottom: 44px; }
.cod { position: absolute; left: 1288px; top: 82px; right: 40px; bottom: 228px; background: #1e1f29; border-radius: 16px; padding: 14px 18px; overflow: hidden; }
.cod .abas { flex-wrap: wrap; gap: 6px; margin-bottom: 10px; }
.cod .aba { font-size: 11.5px; padding: 3px 8px; }
.cod pre { font: 12px/1.45 'DejaVu Sans Mono', monospace; }
.passos2 { position: absolute; left: 1288px; right: 40px; bottom: 44px; height: 170px; }
.passos2 h3 { font-size: 13px; font-weight: 800; letter-spacing: 2.2px; color: #b4383b; margin-bottom: 10px; }
.passos2 .grade { display: grid; grid-template-columns: 1fr 1fr; gap: 8px 14px; }
.passos2 .p { display: grid; grid-template-columns: 56px 1fr; gap: 8px; font-size: 13px; line-height: 1.3; color: #292524; }
.passos2 .pilula { font-size: 13px; padding: 3px 0; }
.dica { position: absolute; left: 92px; bottom: 60px; font-size: 18px; color: #57534e; }
"""


def pagina(corpo, n, secao):
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head>'
            f'<body><div class="barra"></div>{corpo}<div class="rodape"><span>Meets · Projeto Integrador ADS · '
            f'{html.escape(secao)}</span><span>{n} / {TOTAL}</span></div></body></html>')


def cab(caso, titulo, selo):
    num, _c, nome, *_ = CAP[caso]
    return (f'<div class="cab"><span class="kicker">Cap. {num} · {caso} {html.escape(nome)}</span>'
            f'<span class="titulo">{html.escape(titulo)}</span></div><div class="selo">{html.escape(selo)}</div>')


def slide_a(n, caso):
    num, _c, nome, rf_id, rnfs = CAP[caso]
    _id, _g, rf_nome, prio, esp, rns, _uc = g.RF_ID[rf_id]
    desc = UC_ID[caso]['descricao']
    itens_rn = ''.join(f'<div class="item"><b>{r}</b><span>{html.escape(g.RN_ID[r][1])}</span></div>' for r in rns)
    itens_rnf = ''.join(f'<div class="item"><b>{r}</b><span>{html.escape(g.RNF_ID[r][3])}</span></div>' for r in rnfs)
    fl = FLUXOS[caso]
    fp = ''.join(f'<li>{html.escape(p.rstrip(";."))}</li>' for p in UC_ID[caso]['fluxo'])
    fa = ''.join(f'<div class="fl"><b>{k}</b><span>{html.escape(t)}</span></div>' for k, t in fl['fa'])
    fe = ''.join(f'<div class="fl fe"><b>{k}</b><span>{html.escape(t)}</span></div>' for k, t in fl['fe'])
    corpo = (f'<div class="cab2" style="top:44px"><div class="kicker">Capítulo {num} · Caso de uso {caso}</div>'
             f'<div class="titulo" style="font-size:46px">{html.escape(nome)}</div></div>'
             f'<div class="selo selo2" style="top:48px">Tela, fluxos e requisitos</div>'
             f'<div class="lado"><div class="desc">{html.escape(desc)}</div>'
             f'<h3>FLUXO PRINCIPAL (FP)</h3><ol class="fp">{fp}</ol>'
             f'<h3>FLUXOS ALTERNATIVOS (FA)</h3><div class="bloco">{fa}</div>'
             f'<h3>EXCEÇÕES (FE)</h3><div class="bloco">{fe}</div></div>'
             f'<div class="lado2"><div class="rf"><div class="k">REQUISITO FUNCIONAL · {rf_id} · PRIORIDADE {prio.upper()}</div>'
             f'<h2>{html.escape(rf_nome)}</h2><p>{html.escape(esp)}</p></div>'
             f'<div class="bloco"><h3>REGRAS DE NEGÓCIO</h3>{itens_rn}</div>'
             f'<div class="bloco"><h3>REQUISITOS NÃO FUNCIONAIS</h3>{itens_rnf}</div></div>')
    return pagina(corpo, n, caso)


def proporcao(arq):
    w, h = Image.open(os.path.join(ELK, arq + '.png')).size
    return w / h


def slide_b(n, caso):
    classe, der, _seq = ARQ[caso]
    W, H, gap = 1816, 954 - 30, 22  # área útil (descontando o rótulo)
    ra, rb = proporcao(classe), proporcao(der)

    def escala(lado_a_lado):
        if lado_a_lado:
            cw, ch = (W - gap) / 2 - 28, H - 22
        else:
            cw, ch = W - 28, (H - gap) / 2 - 52
        return min(min(cw / (ch * r), 1) * ch * r * ch for r in (ra, rb))  # menor área exibida
    lado = escala(True) >= escala(False)
    cel = lambda rot, arq: (f'<div class="cel"><div class="rot">{rot}</div><div class="img">'
                            f'<img src="file://{os.path.join(ELK, arq + ".png")}"></div></div>')
    corpo = (cab(caso, 'Diagrama de classe e DER', 'Classes e banco de dados') +
             f'<div class="par{"" if lado else " col"}">{cel("Diagrama de classe", classe)}'
             f'{cel("DER — recorte do caso (PostgreSQL)", der)}</div>')
    return pagina(corpo, n, caso)


def slide_c(n, caso):
    _classe, _der, seq = ARQ[caso]
    c = CURTO[caso]
    abas = ''.join(f'<span class="aba">{html.escape(a)}</span>' for a in c['arquivos'])
    passos = ''.join(f'<div class="p"><span class="pilula">{p}</span><span>{html.escape(t)}</span></div>'
                     for p, t in CODIGO[caso]['passos'])
    corpo = (cab(caso, 'Sequência e código', 'Diagrama de sequência ↔ código') +
             f'<div class="cel seq"><div class="rot">Diagrama de sequência — métodos do código (FP / FA / FE)</div>'
             f'<div class="img"><img src="file://{os.path.join(ELK, seq + ".png")}"></div></div>'
             f'<div class="cod"><div class="abas">{abas}</div><pre>{g.realce(c["codigo"])}</pre></div>'
             f'<div class="passos2"><h3>PASSOS DO DIAGRAMA</h3><div class="grade">{passos}</div></div>')
    return pagina(corpo, n, caso)


def slide_d(n, caso):
    num, _c, nome, *_ = CAP[caso]
    corpo = (f'<div class="cab2"><div class="kicker">Capítulo {num} · Caso de uso {caso}</div>'
             f'<div class="titulo">Tela — {html.escape(nome)}</div></div><div class="selo selo2">Tela do app</div>'
             f'<div class="dica">A tela correspondente ao diagrama de sequência do slide anterior.</div>')
    return pagina(corpo, n, caso)


def abertura():
    s = [(1, g.necessidade(1))]
    E = lambda a: os.path.join(ELK, a + '.png')
    s.append((2, g.diagrama(2, 'Visão geral', 'Como funciona sem o sistema', 'Processo atual', E('sem-sistema'), 'Visão geral')))
    for n, arq, tit in [(3, 'negocio-1-evento', 'Atividade de negócio 1 — Organização e realização de evento'),
                        (4, 'negocio-2-conteudo', 'Atividade de negócio 2 — Publicação de conteúdo e interação'),
                        (5, 'negocio-3-moderacao', 'Atividade de negócio 3 — Moderação e controle de qualidade'),
                        (6, 'negocio-4-analise', 'Atividade de negócio 4 — Análise do desempenho da comunidade')]:
        s.append((n, g.diagrama(n, 'Visão geral', tit, 'Diagrama de atividades', E(arq), 'Visão geral')))
    return s


def standby():
    corpo = """<div class="cab2"><div class="kicker">Fora do roteiro</div><div class="titulo">Em stand-by</div></div>
<div class="selo selo2">Para atualizar depois</div>
<div style="position:absolute;left:92px;right:150px;top:260px">
<div class="secao"><h3>OS SLIDES A SEGUIR NÃO FAZEM PARTE DA APRESENTAÇÃO</h3>
<p>MER e DER completos · recortes do MER de cada caso · diagramas de atividade dos casos #015, #005 e #006 ·
sequências coloridas (visão geral) do #005 e do #006. Ficam guardados aqui para serem revisados depois;
a numeração deles ainda é a da versão anterior.</p></div></div>"""
    g_total = g.TOTAL
    return g.pagina(corpo, '—', 'Stand-by').replace(f'— / {g_total}', '')


def slides():
    s = abertura()
    n = 8
    for caso in ['#015', '#005', '#006', '#007', '#008', '#013']:
        s += [(n, slide_a(n, caso)), (n + 1, slide_b(n + 1, caso)), (n + 2, slide_c(n + 2, caso)),
              (n + 3, slide_d(n + 3, caso))]
        n += 4
    s.append(('standby', standby()))
    return s


def main(apenas=None):
    from playwright.sync_api import sync_playwright
    g.TOTAL = TOTAL
    os.makedirs(SAIDA, exist_ok=True)
    os.makedirs(os.path.join(g.AQUI, 'tmp'), exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=os.environ.get('CHROMIUM'), args=['--allow-file-access-from-files'])
        pag = nav.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1.5)
        lista = slides()
        for n, conteudo in lista:
            if apenas and str(n) not in apenas:
                continue
            nome = f'slide-{n:02d}' if isinstance(n, int) else f'slide-{n}'
            arq = os.path.join(g.AQUI, 'tmp', f'padrao-{nome}.html')
            with open(arq, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            pag.goto('file://' + arq)
            pag.wait_for_load_state('networkidle')
            pag.screenshot(path=os.path.join(SAIDA, nome + '.png'))
        nav.close()
    print(f'{len(lista)} slides em {SAIDA}')


if __name__ == '__main__':
    main(sys.argv[1:] or None)
