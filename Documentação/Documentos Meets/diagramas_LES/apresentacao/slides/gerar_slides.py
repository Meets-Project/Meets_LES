"""Gera as imagens (1920x1080) dos slides da apresentação "Meets — Casos de Uso",
no mesmo padrão visual da apresentação original da equipe.

Os slides de especificação (com as telas do app) não são gerados: continuam com a
imagem original no Canva. Uso: python3 gerar_slides.py   (requer Playwright + Chromium)
"""
import html
import os
import sys

from codigo import CODIGO

AQUI = os.path.dirname(os.path.abspath(__file__))
DIAG = os.path.dirname(AQUI)                       # diagramas_LES/apresentacao
COLORIDOS = os.path.join(os.path.dirname(DIAG), 'coloridos')
GERADOR = os.path.join(os.path.dirname(os.path.dirname(DIAG)), 'gerador')
sys.path.insert(0, GERADOR)
from dados import RF, RNF, RN  # noqa: E402

SAIDA = os.path.join(AQUI, 'png')
TOTAL = 61

RF_ID = {r[0]: r for r in RF}
RN_ID = {r[0]: r for r in RN}
RNF_ID = {r[0]: r for r in RNF}

CAPITULOS = [
    # (número, caso, nome, RF, RNFs escolhidos)
    (1, '#015', 'Lembrar Avaliação Pendente', 'RF26', ['RNF10', 'RNF03']),
    (2, '#005', 'Avaliar Evento', 'RF24', ['RNF04', 'RNF01']),
    (3, '#006', 'Avaliar Apresentador', 'RF25', ['RNF04', 'RNF08']),
    (4, '#007', 'Visualizar Ranking de Apresentadores', 'RF27', ['RNF05', 'RNF08']),
    (5, '#008', 'Visualizar Dashboards', 'RF28', ['RNF01', 'RNF05']),
    (6, '#013', 'Analisar Denúncias', 'RF35', ['RNF11', 'RNF01']),
]

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1920px; height: 1080px; }
body { background: #faf6f4; font-family: 'Inter', sans-serif; color: #1c1917; position: relative; overflow: hidden; }
.barra { position: absolute; left: 0; top: 0; bottom: 0; width: 22px; background: #9b1f23; }
.cab { position: absolute; left: 52px; right: 260px; top: 20px; height: 40px; display: flex; align-items: baseline; gap: 22px; white-space: nowrap; }
.kicker { font-size: 15px; font-weight: 800; letter-spacing: 2.6px; color: #b4383b; text-transform: uppercase; }
.titulo { font-size: 31px; font-weight: 800; letter-spacing: -0.4px; }
.selo { position: absolute; right: 52px; top: 20px; background: #fff; border: 1.5px solid #e9e2df; border-radius: 999px; padding: 6px 18px; font-size: 15px; font-weight: 600; color: #44403c; }
.cartao { position: absolute; left: 52px; right: 52px; top: 70px; bottom: 44px; background: #fff; border: 1px solid #ede7e4; border-radius: 20px; box-shadow: 0 1px 3px rgba(0,0,0,.04); display: flex; align-items: center; justify-content: center; padding: 18px; }
.cartao img { max-width: 100%; max-height: 100%; object-fit: contain; }
.cartao.dupla { gap: 28px; }
.cartao.dupla img { max-width: calc(50% - 14px); }
.legenda { position: absolute; left: 76px; bottom: 56px; font-size: 15px; color: #57534e; background: rgba(255,255,255,.92); padding: 4px 10px; border-radius: 8px; }
.rodape { position: absolute; left: 52px; right: 52px; bottom: 13px; display: flex; justify-content: space-between; font-size: 14px; color: #8a817c; }
/* slides de texto */
.cab2 { position: absolute; left: 92px; right: 92px; top: 60px; }
.cab2 .kicker { font-size: 17px; letter-spacing: 3px; }
.cab2 .titulo { font-size: 54px; margin-top: 8px; letter-spacing: -1px; }
.selo2 { position: absolute; right: 92px; top: 62px; }
.rf { position: absolute; left: 92px; right: 92px; top: 205px; background: #fff; border: 1px solid #ede7e4; border-left: 7px solid #9b1f23; border-radius: 16px; padding: 26px 34px; }
.rf .k { font-size: 15px; font-weight: 800; letter-spacing: 2.4px; color: #b4383b; }
.rf h2 { font-size: 34px; font-weight: 800; margin: 8px 0 8px; }
.rf p { font-size: 24px; line-height: 1.45; color: #292524; }
.colunas { position: absolute; left: 92px; right: 92px; top: 470px; display: grid; grid-template-columns: 1.25fr 1fr; gap: 70px; }
.colunas h3 { font-size: 15px; font-weight: 800; letter-spacing: 2.4px; color: #b4383b; margin-bottom: 18px; }
.item { display: grid; grid-template-columns: 84px 1fr; gap: 12px; margin-bottom: 22px; font-size: 22px; line-height: 1.4; color: #292524; }
.item b { color: #9b1f23; font-weight: 800; }
.secao { margin-bottom: 44px; }
.secao h3 { font-size: 18px; font-weight: 800; letter-spacing: 2.4px; color: #b4383b; margin-bottom: 10px; }
.secao p { font-size: 31px; line-height: 1.5; color: #292524; }
/* código */
.codigo { position: absolute; left: 52px; top: 190px; bottom: 44px; width: 1300px; background: #1e1f29; border-radius: 18px; padding: 22px 26px; overflow: hidden; }
.abas { display: flex; gap: 10px; margin-bottom: 14px; }
.aba { background: #2e3040; color: #cbd5e1; font: 600 14px 'DejaVu Sans Mono', monospace; padding: 5px 12px; border-radius: 8px; }
pre { font: 13.4px/1.42 'DejaVu Sans Mono', monospace; color: #e2e8f0; white-space: pre; }
pre .c { color: #8fa3b8; font-style: italic; }
pre .s { color: #a5d6a7; }
pre .k { color: #f0a6ca; }
.passos { position: absolute; left: 1384px; right: 52px; top: 190px; }
.passos h3 { font-size: 15px; font-weight: 800; letter-spacing: 2.4px; color: #b4383b; margin-bottom: 22px; }
.passo { display: grid; grid-template-columns: 82px 1fr; gap: 14px; margin-bottom: 24px; font-size: 19px; line-height: 1.38; color: #292524; }
.pilula { background: #9b1f23; color: #fff; font-weight: 800; font-size: 16px; border-radius: 999px; text-align: center; padding: 4px 0; height: fit-content; }
"""


def pagina(corpo, n, secao):
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="barra"></div>{corpo}
<div class="rodape"><span>Meets · Projeto Integrador ADS · {html.escape(secao)}</span><span>{n} / {TOTAL}</span></div></body></html>"""


def img(caminho):
    return 'file://' + caminho


def diagrama(n, kicker, titulo, selo, imagem, secao, legenda=None, dupla=None):
    imgs = (f'<img src="{img(dupla[0])}"><img src="{img(dupla[1])}">' if dupla else f'<img src="{img(imagem)}">')
    corpo = (f'<div class="cab"><span class="kicker">{html.escape(kicker)}</span><span class="titulo">{html.escape(titulo)}</span></div>'
             f'<div class="selo">{html.escape(selo)}</div>'
             f'<div class="cartao{" dupla" if dupla else ""}">{imgs}</div>')
    if legenda:
        corpo += f'<div class="legenda">{legenda}</div>'
    return pagina(corpo, n, secao)


def necessidade(n):
    corpo = """<div class="cab2"><div class="kicker">Visão geral</div><div class="titulo">Necessidade do negócio</div></div>
<div class="selo selo2">Documento de Visão</div>
<div style="position:absolute;left:92px;right:150px;top:240px">
<div class="secao"><h3>PERFIL DO CLIENTE</h3><p>Comunidades acadêmicas, corporativas e grupos sociais que organizam com frequência encontros, palestras, workshops e compartilhamento de conhecimento.</p></div>
<div class="secao"><h3>SITUAÇÃO ATUAL (COMO É FEITO HOJE)</h3><p>A organização de eventos e a divulgação de conteúdos ocorrem de forma informal e fragmentada, com convites pessoa a pessoa, grupos de mensagens instantâneas e planilhas dispersas. Isso causa perda de dados, falta de histórico, ausência de métricas de engajamento e dificuldade para avaliar a qualidade dos eventos e dos apresentadores.</p></div>
<div class="secao"><h3>SOLUÇÃO PROPOSTA</h3><p>O Meets substitui essa informalidade por um ecossistema digital integrado e persistente: a comunidade encontra e interage com eventos, acompanha um feed, avalia os apresentadores por atributos, consulta o ranking e acompanha estatísticas em dashboards; a moderação recebe e trata denúncias.</p></div>
</div>"""
    return pagina(corpo, n, 'Visão geral')


def requisitos(n, cap):
    num, caso, nome, rf_id, rnfs = cap
    _id, _g, rf_nome, prio, esp, rns, _uc = RF_ID[rf_id]
    itens_rn = ''.join(f'<div class="item"><b>{r}</b><span>{html.escape(RN_ID[r][1])}</span></div>' for r in rns)
    itens_rnf = ''.join(f'<div class="item"><b>{r}</b><span>{html.escape(RNF_ID[r][3])}</span></div>' for r in rnfs)
    corpo = f"""<div class="cab2"><div class="kicker">Capítulo {num} · Caso de uso {caso}</div><div class="titulo">{html.escape(nome)}</div></div>
<div class="selo selo2">Requisitos</div>
<div class="rf"><div class="k">REQUISITO FUNCIONAL · {rf_id} · PRIORIDADE {prio.upper()}</div><h2>{html.escape(rf_nome)}</h2><p>{html.escape(esp)}</p></div>
<div class="colunas"><div><h3>REGRAS DE NEGÓCIO</h3>{itens_rn}</div><div><h3>REQUISITOS NÃO FUNCIONAIS</h3>{itens_rnf}</div></div>"""
    return pagina(corpo, n, caso)


def realce(codigo):
    out = []
    for linha in html.escape(codigo).split('\n'):
        if '//' in linha and not linha.strip().startswith('`'):
            i = linha.index('//')
            if 'http' not in linha[:i]:
                linha = linha[:i] + f'<span class="c">{linha[i:]}</span>'
        out.append(linha)
    return '\n'.join(out)


def sequencia_codigo(n, cap):
    num, caso, nome, *_ = cap
    c = CODIGO[caso]
    abas = ''.join(f'<span class="aba">{html.escape(a)}</span>' for a in c['arquivos'])
    passos = ''.join(f'<div class="passo"><span class="pilula">{p}</span><span>{html.escape(t)}</span></div>' for p, t in c['passos'])
    corpo = f"""<div class="cab2"><div class="kicker">Capítulo {num} · Caso de uso {caso}</div><div class="titulo">Sequência ↔ código</div></div>
<div class="selo selo2">Código · {html.escape(nome)}</div>
<div class="codigo"><div class="abas">{abas}</div><pre>{realce(c['codigo'])}</pre></div>
<div class="passos"><h3>PASSOS DO DIAGRAMA</h3>{passos}</div>"""
    return pagina(corpo, n, caso)


def D(nome):
    return os.path.join(DIAG, nome)


def slides():
    """Lista (número, html) na ordem do documento no Canva. Os de especificação ficam de fora."""
    s = []
    leg_uc = ('Borda grossa = caso apresentado nos capítulos · <b style="color:#2563eb">azul</b> = Análise · '
              '<b style="color:#ea580c">laranja</b> = Condução (automação) · cinza = Básico')
    s.append((1, necessidade(1)))
    s.append((2, diagrama(2, 'Visão geral', 'Como funciona sem o sistema', 'Processo atual', D('sem-sistema.png'), 'Visão geral')))
    ativ = [('negocio-1-evento.png', 'Atividade de negócio 1 — Organização e realização de evento'),
            ('negocio-2-conteudo.png', 'Atividade de negócio 2 — Publicação de conteúdo e interação'),
            ('negocio-3-moderacao.png', 'Atividade de negócio 3 — Moderação e controle de qualidade'),
            ('negocio-4-analise.png', 'Atividade de negócio 4 — Análise do desempenho da comunidade')]
    for i, (arq, tit) in enumerate(ativ):
        s.append((3 + i, diagrama(3 + i, 'Visão geral', tit, 'Diagrama de atividades', D(arq), 'Visão geral')))
    uc = [('uc-1-acesso-conteudo.png', 'Diagrama geral de casos de uso (1/4) — Acesso e conteúdo'),
          ('uc-2-rede-utilidades.png', 'Diagrama geral de casos de uso (2/4) — Rede e utilidades'),
          ('uc-3-eventos-avaliacao-analise.png', 'Diagrama geral de casos de uso (3/4) — Eventos, avaliação e análise'),
          ('uc-4-administracao.png', 'Diagrama geral de casos de uso (4/4) — Administração e moderação')]
    for i, (arq, tit) in enumerate(uc):
        s.append((7 + i, diagrama(7 + i, 'Casos de uso', tit, 'Casos de uso', D(arq), 'Casos de uso', legenda=leg_uc)))

    arquivos = {
        '#015': ('mer-015-lembrete', ['der-015-lembrete'], 'classe-015-lembrete', 'atividade-015-lembrete', 'sequencia-015-lembrete'),
        '#005': ('mer-005-avaliar-evento', ['der-005-avaliar-evento'], 'classe-005-avaliar-evento', 'atividade-005-avaliar-evento', 'sequencia-005-avaliar-evento'),
        '#006': ('mer-006-avaliar-apresentador', ['der-006-avaliar-apresentador'], 'classe-006-avaliar-apresentador', 'atividade-006-avaliar-apresentador', 'sequencia-006-avaliar-apresentador'),
        '#007': ('mer-007-ranking', ['der-007-ranking'], 'classe-007-ranking', 'atividade-007-ranking', 'sequencia-007-ranking'),
        '#008': ('mer-008-dashboards', ['der-008a-dashboards-conteudo', 'der-008b-dashboards-avaliacoes'], 'classe-008-dashboards', 'atividade-008-dashboards', 'sequencia-008-dashboards'),
        '#013': ('mer-013-denuncias', ['der-013-denuncias'], 'classe-013-denuncias', 'atividade-013-denuncias', 'sequencia-013-denuncias'),
    }
    coloridos = {'#005': 'diagrama de sequencia Avaliar Evento.png', '#006': 'diagrama de sequencia Avaliar Apresentador.png'}
    n = 11
    for cap in CAPITULOS:
        num, caso, nome, *_ = cap
        kicker = f'Cap. {num} · {caso} {nome}'
        mer, ders, classe, atividade, seq = arquivos[caso]
        n += 1                                   # n-1 = especificação (imagem original)
        s.append((n, requisitos(n, cap))); n += 1
        s.append((n, diagrama(n, kicker, 'MER — recorte do caso de uso', 'Modelo conceitual (Chen)', D(mer + '.png'), caso))); n += 1
        for i, der in enumerate(ders):
            sufixo = f' ({i + 1}/{len(ders)})' if len(ders) > 1 else ''
            s.append((n, diagrama(n, kicker, f'DER — recorte do caso de uso{sufixo}', 'Modelo físico (PostgreSQL)', D(der + '.png'), caso))); n += 1
        s.append((n, diagrama(n, kicker, 'Diagrama de classe', 'Classes do domínio e do código', D(classe + '.png'), caso))); n += 1
        s.append((n, diagrama(n, kicker, f'Diagrama de atividades — {nome}', 'Diagrama de atividades', D(atividade + '.png'), caso))); n += 1
        if caso in coloridos:
            metades = (os.path.join(AQUI, 'tmp', f'col-{caso[1:]}-1.png'), os.path.join(AQUI, 'tmp', f'col-{caso[1:]}-2.png'))
            s.append((n, diagrama(n, kicker, 'Diagrama de sequência — visão geral', 'Visão geral (continua à direita →)', None, caso, dupla=metades))); n += 1
        s.append((n, diagrama(n, kicker, 'Diagrama de sequência — métodos do código', 'Sequência com os métodos do código', D(seq + '.png'), caso))); n += 1
        s.append((n, sequencia_codigo(n, cap))); n += 1
    assert n - 1 == TOTAL, n
    return s, coloridos


def dividir_coloridos(coloridos):
    from PIL import Image
    os.makedirs(os.path.join(AQUI, 'tmp'), exist_ok=True)
    for caso, arq in coloridos.items():
        im = Image.open(os.path.join(COLORIDOS, arq)).convert('RGB')
        w, h = im.size
        meio = h // 2
        im.crop((0, 0, w, meio + 40)).save(os.path.join(AQUI, 'tmp', f'col-{caso[1:]}-1.png'))
        im.crop((0, meio - 40, w, h)).save(os.path.join(AQUI, 'tmp', f'col-{caso[1:]}-2.png'))


def main(apenas=None):
    from playwright.sync_api import sync_playwright
    lista, coloridos = slides()
    dividir_coloridos(coloridos)
    os.makedirs(SAIDA, exist_ok=True)
    with sync_playwright() as p:
        nav = p.chromium.launch(executable_path=os.environ.get('CHROMIUM'), args=['--allow-file-access-from-files'])
        pag = nav.new_page(viewport={'width': 1920, 'height': 1080}, device_scale_factor=1.5)
        for n, conteudo in lista:
            if apenas and n not in apenas:
                continue
            arq_html = os.path.join(AQUI, 'tmp', f'slide-{n:02d}.html')
            with open(arq_html, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            pag.goto('file://' + arq_html)
            pag.wait_for_load_state('networkidle')
            pag.screenshot(path=os.path.join(SAIDA, f'slide-{n:02d}.png'))
        nav.close()
    print(f'{len(lista)} slides gerados em {SAIDA}')


if __name__ == '__main__':
    main([int(a) for a in sys.argv[1:]] or None)
