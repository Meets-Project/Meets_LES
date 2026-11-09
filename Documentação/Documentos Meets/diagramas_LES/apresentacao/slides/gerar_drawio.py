"""Gera os diagramas do Meets em draw.io (.drawio, XML mxGraph editável) a partir das fontes
Mermaid em ../fontes-elk (mesmos textos, nomes e numeração).

- classe, DER e MER: usam a posição dos nós e das arestas do layout ELK do Mermaid
  (../fontes-drawio/_geometria-mermaid.json, gerado por geometria_mermaid.py);
- sequência: layout próprio (linhas de vida, mensagens numeradas, quadros alt/opt/loop/par e
  notas FP/FA/FE);
- atividade (negócio e casos de uso): diagrama UML com raias verticais, uma por ator.
Uso: python3 gerar_drawio.py [nome ...]   →  ../fontes-drawio/*.drawio
"""
import html
import json
import os
import re
import sys
from xml.sax.saxutils import quoteattr

from PIL import ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTES = os.path.join(AQUI, '..', 'fontes-elk')
SAIDA = os.path.join(AQUI, '..', 'fontes-drawio')
GEO = os.path.join(SAIDA, '_geometria-mermaid.json')
FONTE = '/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-regular.otf'
FONTE_B = '/usr/share/texmf/fonts/opentype/public/tex-gyre/texgyreheros-bold.otf'
VINHO = '#b4383b'
TINTA = '#292524'
_fontes = {}


def largura(txt, tam=14, negrito=False):
    k = (tam, negrito)
    if k not in _fontes:
        _fontes[k] = ImageFont.truetype(FONTE_B if negrito else FONTE, tam)
    return _fontes[k].getlength(txt)


def quebra(txt, larg, tam=14, negrito=False):
    """Quebra o texto em linhas que caibam em `larg` px."""
    linhas = []
    for par in txt.split('\n'):
        atual = ''
        for p in par.split(' '):
            t = (atual + ' ' + p).strip()
            if atual and largura(t, tam, negrito) > larg:
                linhas.append(atual)
                atual = p
            else:
                atual = t
        linhas.append(atual)
    return linhas


def esc(t):
    return html.escape(t, quote=False)


def br(t):
    """Texto do Mermaid (com <br/>, <b>, <u>) para o HTML do rótulo do draw.io."""
    partes = re.split(r'<br\s*/?>', t)
    out = []
    for p in partes:
        p = esc(p)
        p = re.sub(r'&lt;(/?)(b|u|i)&gt;', r'<\1\2>', p)
        out.append(p)
    return '<br>'.join(out)


def sem_tags(t):
    return re.sub(r'<[^>]+>', '', re.sub(r'<br\s*/?>', '\n', t))


class Diagrama:
    def __init__(self, nome):
        self.nome = nome
        self.cel = []
        self.geo = {}
        self.n = 1

    def pontas(self, a, b, ends):
        if not ends:
            return ''
        return fixo(self.geo[a], ends[0], 'exit') + fixo(self.geo[b], ends[1], 'entry')

    def novo_id(self):
        self.n += 1
        return f'c{self.n}'

    def v(self, valor, estilo, x, y, w, h, pai='1', id=None):
        id = id or self.novo_id()
        self.geo[id] = (x, y, w, h)
        self.cel.append(f'<mxCell id="{id}" value={quoteattr(valor)} style={quoteattr(estilo)} vertex="1" '
                        f'parent="{pai}"><mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
                        f'as="geometry"/></mxCell>')
        return id

    def e(self, valor, estilo, origem=None, destino=None, p0=None, p1=None, pontos=(), pai='1', id=None,
          rel_x=None, offset=None):
        id = id or self.novo_id()
        a = f'<mxCell id="{id}" value={quoteattr(valor)} style={quoteattr(estilo)} edge="1" parent="{pai}"'
        if origem:
            a += f' source="{origem}"'
        if destino:
            a += f' target="{destino}"'
        g = '<mxGeometry relative="1" as="geometry"' + (f' x="{rel_x}"' if rel_x is not None else '') + '>'
        if p0:
            g += f'<mxPoint x="{p0[0]:.1f}" y="{p0[1]:.1f}" as="sourcePoint"/>'
        if p1:
            g += f'<mxPoint x="{p1[0]:.1f}" y="{p1[1]:.1f}" as="targetPoint"/>'
        if pontos:
            g += '<Array as="points">' + ''.join(f'<mxPoint x="{x:.1f}" y="{y:.1f}"/>' for x, y in pontos) + '</Array>'
        if offset:
            g += f'<mxPoint x="{offset[0]}" y="{offset[1]}" as="offset"/>'
        g += '</mxGeometry>'
        self.cel.append(a + '>' + g + '</mxCell>')
        return id

    def rotulo_aresta(self, aresta, valor, rel_x, dx=0, dy=-12, estilo=''):
        id = self.novo_id()
        st = ('edgeLabel;html=1;align=center;verticalAlign=middle;resizable=0;points=[];fontSize=13;'
              'labelBackgroundColor=#ffffff;' + estilo)
        self.cel.append(f'<mxCell id="{id}" value={quoteattr(valor)} style={quoteattr(st)} vertex="1" '
                        f'connectable="0" parent="{aresta}"><mxGeometry x="{rel_x}" relative="1" as="geometry">'
                        f'<mxPoint x="{dx}" y="{dy}" as="offset"/></mxGeometry></mxCell>')

    def xml(self):
        corpo = '\n'.join(self.cel)
        return (f'<mxfile host="Meets" type="device">\n<diagram id="{self.nome}" name="{self.nome}">\n'
                f'<mxGraphModel grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" '
                f'page="0" pageScale="1" math="0" shadow="0" background="#ffffff">\n<root>\n'
                f'<mxCell id="0"/>\n<mxCell id="1" parent="0"/>\n{corpo}\n</root>\n</mxGraphModel>\n</diagram>\n</mxfile>\n')

    def salvar(self):
        with open(os.path.join(SAIDA, self.nome + '.drawio'), 'w', encoding='utf-8') as f:
            f.write(self.xml())


def ler(nome):
    txt = open(os.path.join(FONTES, nome + '.mmd'), encoding='utf-8').read()
    return re.sub(r'^---\n.*?\n---\n', '', txt, flags=re.S)


# ----------------------------------------------------------------------------------------------
# Estilos (style / classDef) do Mermaid
# ----------------------------------------------------------------------------------------------
def estilos_mermaid(txt):
    defs, por_no = {}, {}
    for m in re.finditer(r'^\s*classDef\s+(\w+)\s+(.+)$', txt, re.M):
        defs[m.group(1)] = m.group(2)
    for m in re.finditer(r'^\s*class\s+([\w,]+)\s+(\w+)\s*$', txt, re.M):
        for n in m.group(1).split(','):
            por_no.setdefault(n, []).append(defs.get(m.group(2), ''))
    for m in re.finditer(r'^\s*style\s+(\w+)\s+(.+)$', txt, re.M):
        por_no.setdefault(m.group(1), []).append(m.group(2))
    res = {}
    for n, lst in por_no.items():
        d = {}
        for s in lst:
            for par in s.split(','):
                if ':' in par:
                    k, v = par.split(':', 1)
                    d[k.strip()] = v.strip()
        res[n] = d
    return res


def cores(d, fill='#ffffff', stroke='#44403c'):
    s = f'fillColor={d.get("fill", fill)};strokeColor={d.get("stroke", stroke)};'
    if 'stroke-dasharray' in d:
        s += 'dashed=1;dashPattern=6 4;'
    return s


# ----------------------------------------------------------------------------------------------
# Geometria do Mermaid
# ----------------------------------------------------------------------------------------------
_geo = None


def geometria(nome):
    global _geo
    if _geo is None:
        _geo = json.load(open(GEO))
    return _geo[nome]


def no_proximo(nos, p):
    def dist(n):
        x, y, w, h = n['x'], n['y'], n['w'], n['h']
        dx = max(x - p[0], 0, p[0] - (x + w))
        dy = max(y - p[1], 0, p[1] - (y + h))
        return dx * dx + dy * dy
    return min(nos, key=dist)


def arestas_geo(geo, chave):
    """Lista (origem, destino, pontos internos) de cada aresta, com origem/destino = nó mais próximo."""
    res = []
    for e in geo['edges']:
        pts = e['pts']
        a = chave(no_proximo(geo['nodes'], pts[0]))
        b = chave(no_proximo(geo['nodes'], pts[-1]))
        res.append([a, b, pts])
    return res


def casar(rels, geo_arestas):
    """Associa cada relação (a, b, ...) do texto à aresta do SVG com as mesmas pontas."""
    livres = list(geo_arestas)
    out = []
    for r in rels:
        a, b = r[0], r[1]
        achou = None
        for g in livres:
            if (g[0], g[1]) == (a, b):
                achou, inv = g, False
                break
        if achou is None:
            for g in livres:
                if (g[0], g[1]) == (b, a):
                    achou, inv = g, True
                    break
        if achou is None:
            out.append((r, [], None))
            continue
        livres.remove(achou)
        pts = achou[2]
        if inv:
            pts = pts[::-1]
        out.append((r, simplificar(pts[1:-1]), (pts[0], pts[-1])))
    return out


def fixo(geo_cel, p, pref):
    """Ponto de conexão fixo (exitX/entryX) no lugar onde o ELK ligou a aresta."""
    x, y, w, h = geo_cel
    fx = min(max((p[0] - x) / w, 0), 1)
    fy = min(max((p[1] - y) / h, 0), 1)
    return f'{pref}X={fx:.3f};{pref}Y={fy:.3f};{pref}Dx=0;{pref}Dy=0;'


def simplificar(pts):
    """Remove pontos colineares/repetidos para deixar a aresta editável no draw.io."""
    res = []
    for p in pts:
        p = (round(p[0], 1), round(p[1], 1))
        if res and abs(res[-1][0] - p[0]) < 1 and abs(res[-1][1] - p[1]) < 1:
            continue
        res.append(p)
    i = 1
    while i < len(res) - 1:
        a, b, c = res[i - 1], res[i], res[i + 1]
        if (abs(a[0] - b[0]) < 1 and abs(b[0] - c[0]) < 1) or (abs(a[1] - b[1]) < 1 and abs(b[1] - c[1]) < 1):
            res.pop(i)
        else:
            i += 1
    return res


# ----------------------------------------------------------------------------------------------
# Diagrama de classe
# ----------------------------------------------------------------------------------------------
def classe(nome):
    txt = ler(nome)
    geo = geometria(nome)
    est = estilos_mermaid(txt)
    classes = {}
    for m in re.finditer(r'^\s*class\s+(\w+)\s*\{(.*?)\n\s*\}', txt, re.M | re.S):
        corpo = [l.strip() for l in m.group(2).strip().split('\n') if l.strip()]
        ester = [l[2:-2] for l in corpo if l.startswith('<<')]
        membros = [l for l in corpo if not l.startswith('<<')]
        classes[m.group(1)] = (ester[0] if ester else '', membros)
    rels = []
    for l in txt.split('\n'):
        m = re.match(r'^\s*(\w+)\s*(?:"([^"]*)")?\s*(\*--|o--|<\|--|-->|\.\.>|\.\.|--)\s*(?:"([^"]*)")?\s*(\w+)\s*(?::\s*(.+))?$', l)
        if m and m.group(1) in classes and m.group(5) in classes:
            rels.append((m.group(1), m.group(5), m.group(3), m.group(2), m.group(4), (m.group(6) or '').strip()))
    pos = {}
    for n in geo['nodes']:
        k = re.match(r'my-svg-classId-(.+)-\d+$', n['id']).group(1)
        pos[k] = n
    d = Diagrama(nome)
    ids = {}
    for k, (ester, membros) in classes.items():
        n = pos[k]
        atr = [x for x in membros if '(' not in x]
        met = [x for x in membros if '(' in x]
        topo = 50
        linhas = len(atr) + len(met)
        sep = 8 if atr and met else 0
        h = max(n['h'], topo + linhas * 22 + sep + 6)
        rowh = (h - topo - sep - 6) / max(linhas, 1)
        w = max(n['w'], max([largura(x, 14) for x in membros] + [largura(k, 15, True), largura(ester, 13)]) + 24)
        x = n['x'] + n['w'] / 2 - w / 2
        y = n['y'] + n['h'] / 2 - h / 2
        c = est.get(k, {})
        cab = (f'<font style="font-size:12px" color="#57534e">«{esc(ester)}»</font><br><b>{esc(k)}</b>' if ester
               else f'<b>{esc(k)}</b>')
        st = ('swimlane;fontStyle=0;align=center;verticalAlign=top;childLayout=stackLayout;horizontal=1;'
              f'startSize={topo};horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=0;'
              'marginBottom=0;html=1;whiteSpace=wrap;rounded=1;arcSize=6;absoluteArcSize=1;fontSize=15;'
              f'fontFamily=Helvetica;strokeWidth=1.5;swimlaneFillColor=#ffffff;{cores(c)}fontColor={TINTA};')
        cid = d.v(cab, st, x, y, w, h)
        ids[k] = cid
        yy = topo
        for i, mbr in enumerate(atr + met):
            if met and i == len(atr) and atr:
                d.v('', 'line;strokeWidth=1;fillColor=none;align=left;verticalAlign=middle;spacingTop=-1;'
                    'spacingLeft=3;spacingRight=3;rotatable=0;labelPosition=right;points=[];portConstraint=eastwest;'
                    f'strokeColor={c.get("stroke", "#44403c")};', 0, yy, w, sep, pai=cid)
                yy += sep
            d.v(esc(mbr), 'text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=8;'
                f'spacingRight=4;overflow=hidden;rotatable=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;'
                f'html=1;fontSize=14;fontFamily=Helvetica;fontColor={TINTA};', 0, yy, w, rowh, pai=cid)
            yy += rowh
    chave = lambda n: re.match(r'my-svg-classId-(.+)-\d+$', n['id']).group(1)
    for (a, b, tipo, ma, mb, rot), pts, ends in casar(rels, arestas_geo(geo, chave)):
        st = 'html=1;rounded=1;arcSize=12;fontSize=13;fontFamily=Helvetica;strokeColor=#44403c;strokeWidth=1.5;' \
             'labelBackgroundColor=#ffffff;fontColor=#292524;'
        if tipo == '..>':
            st += 'dashed=1;endArrow=open;endSize=10;startArrow=none;'
        elif tipo == '..':
            st += 'dashed=1;endArrow=none;startArrow=none;'
        elif tipo == '-->':
            st += 'endArrow=open;endSize=10;startArrow=none;'
        elif tipo == '*--':
            st += 'startArrow=diamondThin;startFill=1;startSize=16;endArrow=none;'
        elif tipo == 'o--':
            st += 'startArrow=diamondThin;startFill=0;startSize=16;endArrow=none;'
        elif tipo == '<|--':
            st += 'startArrow=block;startFill=0;startSize=12;endArrow=none;'
        else:
            st += 'endArrow=none;startArrow=none;'
        eid = d.e(esc(rot), st + d.pontas(ids[a], ids[b], ends), ids[a], ids[b], pontos=pts)
        if ma:
            d.rotulo_aresta(eid, esc(ma), -0.8, 0, -12)
        if mb:
            d.rotulo_aresta(eid, esc(mb), 0.8, 0, -12)
    d.salvar()


# ----------------------------------------------------------------------------------------------
# DER (modelo físico)
# ----------------------------------------------------------------------------------------------
PONTA_E = {'||': 'ERmandOne', '|o': 'ERzeroToOne', '}|': 'ERoneToMany', '}o': 'ERzeroToMany'}
PONTA_D = {'||': 'ERmandOne', 'o|': 'ERzeroToOne', '|{': 'ERoneToMany', 'o{': 'ERzeroToMany'}


def der(nome):
    txt = ler(nome)
    geo = geometria(nome)
    est = estilos_mermaid(txt)
    ents = {}
    for m in re.finditer(r'^\s*(\w+)\s*\{(.*?)\n\s*\}', txt, re.M | re.S):
        cols = []
        for l in m.group(2).strip().split('\n'):
            p = l.split('"')[0].split()
            if len(p) >= 2:
                cols.append((p[0], p[1], p[2] if len(p) > 2 else ''))
        ents[m.group(1)] = cols
    rels = []
    for m in re.finditer(r'^\s*(\w+)\s+(\|\||\|o|\}\||\}o)(--|\.\.)(\|\||o\||\|\{|o\{)\s+(\w+)\s*:\s*"?([^"\n]*)"?', txt, re.M):
        rels.append((m.group(1), m.group(5), m.group(2), m.group(4), m.group(6).strip(), m.group(3)))
    pos = {re.match(r'my-svg-entity-(.+)-\d+$', n['id']).group(1): n for n in geo['nodes']}
    d = Diagrama(nome)
    ids = {}
    for k, cols in ents.items():
        n = pos[k]
        topo = 36
        h = max(n['h'], topo + len(cols) * 24)
        rowh = (h - topo) / max(len(cols), 1)
        wk = 62
        wn = max([largura(c[1], 14, 'PK' in c[2]) for c in cols] + [60]) + 16
        wt = max([largura(c[0], 13) for c in cols] + [40]) + 16
        w = max(n['w'], wk + wn + wt, largura(k, 15, True) + 30)
        wn = w - wk - wt
        x = n['x'] + n['w'] / 2 - w / 2
        y = n['y'] + n['h'] / 2 - h / 2
        c = est.get(k, {})
        st = (f'shape=table;startSize={topo};container=1;collapsible=0;childLayout=tableLayout;fixedRows=1;'
              'rowLines=0;fontStyle=1;align=center;resizeLast=1;html=1;whiteSpace=wrap;fontSize=15;'
              f'fontFamily=Helvetica;strokeWidth=1.5;swimlaneFillColor=#ffffff;{cores(c)}fontColor={TINTA};')
        tid = d.v(esc(k), st, x, y, w, h)
        ids[k] = tid
        for i, (tipo, col, chave) in enumerate(cols):
            pk = 'PK' in chave
            lin = ('shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;'
                   'collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;'
                   f'right=0;bottom={1 if pk and (i + 1 == len(cols) or "PK" not in cols[i + 1][2]) else 0};'
                   f'html=1;strokeColor={c.get("stroke", "#44403c")};')
            rid = d.v('', lin, 0, topo + i * rowh, w, rowh, pai=tid)
            cel = ('shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;html=1;'
                   'overflow=hidden;whiteSpace=wrap;fontFamily=Helvetica;')
            d.v(esc(chave), cel + f'fontSize=12;fontStyle=1;align=center;fontColor={c.get("stroke", "#57534e")};',
                0, 0, wk, rowh, pai=rid)
            d.v(esc(col), cel + f'fontSize=14;align=left;spacingLeft=6;fontColor={TINTA};'
                + ('fontStyle=5;' if pk else ''), wk, 0, wn, rowh, pai=rid)
            d.v(esc(tipo), cel + 'fontSize=13;align=left;spacingLeft=4;fontColor=#78716c;', wk + wn, 0, wt, rowh,
                pai=rid)
    chave = lambda n: re.match(r'my-svg-entity-(.+)-\d+$', n['id']).group(1)
    for (a, b, pe, pd, rot, linha), pts, ends in casar(rels, arestas_geo(geo, chave)):
        st = (f'html=1;rounded=1;arcSize=12;fontSize=13;fontFamily=Helvetica;strokeColor=#57534e;strokeWidth=1.5;'
              f'startArrow={PONTA_E[pe]};endArrow={PONTA_D[pd]};startFill=0;endFill=0;startSize=14;endSize=14;'
              f'labelBackgroundColor=#ffffff;fontColor=#57534e;' + ('dashed=1;' if linha == '..' else ''))
        d.e(esc(rot), st + d.pontas(ids[a], ids[b], ends), ids[a], ids[b], pontos=pts)
    d.salvar()


# ----------------------------------------------------------------------------------------------
# MER conceitual (notação de Chen)
# ----------------------------------------------------------------------------------------------
def mer(nome):
    txt = ler(nome)
    geo = geometria(nome)
    est = estilos_mermaid(txt)
    nos = {}
    for m in re.finditer(r'^\s*(\w+)(\(\[|\[|\{)"([^"]*)"(\]\)|\]|\})\s*$', txt, re.M):
        forma = {'([': 'atr', '[': 'ent', '{': 'rel'}[m.group(2)]
        nos[m.group(1)] = (forma, m.group(3))
    rels = []
    for m in re.finditer(r'^\s*(\w+)\s+---(?:\|"([^"]*)"\|)?\s+(\w+)\s*$', txt, re.M):
        rels.append((m.group(1), m.group(3), m.group(2) or ''))
    pos = {re.match(r'my-svg-flowchart-(.+)-\d+$', n['id']).group(1): n for n in geo['nodes']}
    d = Diagrama(nome)
    ids = {}
    for k, (forma, rot) in nos.items():
        n = pos[k]
        c = est.get(k, {})
        base = f'html=1;whiteSpace=wrap;fontFamily=Helvetica;fontColor={TINTA};'
        if forma == 'ent':
            st = base + f'rounded=0;fontSize=17;fontStyle=1;strokeWidth=2.5;{cores(c)}'
        elif forma == 'rel':
            st = base + f'rhombus;fontSize=15;strokeWidth=1.5;{cores(c, "#fefce8", "#a16207")}'
        else:
            st = base + f'ellipse;fontSize=14;strokeWidth=1.2;{cores(c, "#ffffff", "#475569")}'
        ids[k] = d.v(br(rot), st, n['x'], n['y'], n['w'], n['h'])
    chave = lambda n: re.match(r'my-svg-flowchart-(.+)-\d+$', n['id']).group(1)

    def ponta(k, p, viz, pref):
        """Losango/elipse: liga na ponta (topo, base, esquerda, direita) e alinha o ponto vizinho."""
        x, y, w, h = d.geo[ids[k]]
        if nos[k][0] == 'ent':
            return fixo((x, y, w, h), p, pref)
        q = viz if viz is not None else p
        if q[1] > y + h - 1:
            lado = 'b'
        elif q[1] < y + 1:
            lado = 't'
        elif q[0] < x + 1:
            lado = 'l'
        elif q[0] > x + w - 1:
            lado = 'r'
        else:
            lados = {'t': abs(p[1] - y), 'b': abs(p[1] - y - h), 'l': abs(p[0] - x), 'r': abs(p[0] - x - w)}
            lado = min(lados, key=lados.get)
        fx, fy = {'t': (0.5, 0), 'b': (0.5, 1), 'l': (0, 0.5), 'r': (1, 0.5)}[lado]
        if viz is not None:
            if lado in 'tb':
                viz[0] = x + w / 2
            else:
                viz[1] = y + h / 2
        return f'{pref}X={fx};{pref}Y={fy};{pref}Dx=0;{pref}Dy=0;'
    for (a, b, rot), pts, ends in casar(rels, arestas_geo(geo, chave)):
        st = ('html=1;endArrow=none;startArrow=none;strokeColor=#57534e;strokeWidth=1.3;fontSize=15;fontStyle=1;'
              'fontFamily=Helvetica;labelBackgroundColor=#ffffff;fontColor=#292524;rounded=1;')
        pts = [list(q) for q in pts]

        def dentro(k, q, f=1.5):
            x, y, w, h = d.geo[ids[k]]
            return x - f <= q[0] <= x + w + f and y - f <= q[1] <= y + h + f
        while pts and dentro(a, pts[0]):
            pts.pop(0)
        while pts and dentro(b, pts[-1]):
            pts.pop()
        if ends:
            st += ponta(a, ends[0], pts[0] if pts else None, 'exit')
            st += ponta(b, ends[1], pts[-1] if pts else None, 'entry')
        d.e(esc(rot), st, ids[a], ids[b], pontos=[tuple(q) for q in pts])
    d.salvar()


# ----------------------------------------------------------------------------------------------
# Diagrama de sequência
# ----------------------------------------------------------------------------------------------
ICONE = {'actor': 'umlActor', 'boundary': 'umlBoundary', 'control': 'umlControl', 'entity': 'umlEntity',
         'database': 'cylinder'}
COR_FLUXO = {'FE': ('#fef2f2', '#dc2626', '#b91c1c'), 'FA': ('#eff6ff', '#2563eb', '#1d4ed8'),
             'FP': ('#f0fdf4', '#16a34a', '#15803d')}
FS = 15


def fluxo(txt):
    m = re.match(r'\s*(FE|FA|FP)', txt)
    return m.group(1) if m else None


def parse_seq(txt):
    parts, ordem, itens = {}, [], []
    num = 0
    pilha = []
    for l in txt.split('\n'):
        s = l.strip()
        if not s or s.startswith('%%') or s in ('sequenceDiagram', 'autonumber'):
            continue
        m = re.match(r'(actor|participant)\s+(\w+)(?:@\{\s*"type":\s*"(\w+)"\s*\})?\s*(?:as\s+(.+))?$', s)
        if m:
            tipo = 'actor' if m.group(1) == 'actor' else (m.group(3) or 'participant')
            parts[m.group(2)] = (tipo, (m.group(4) or m.group(2)).strip())
            ordem.append(m.group(2))
            continue
        m = re.match(r'Note\s+over\s+(\w+)(?:\s*,\s*(\w+))?\s*:\s*(.+)$', s)
        if m:
            itens.append(('nota', m.group(1), m.group(2) or m.group(1), m.group(3)))
            continue
        m = re.match(r'(\w+)\s*(-->>|->>)\s*(\w+)\s*:\s*(.*)$', s)
        if m:
            num += 1
            itens.append(('msg', m.group(1), m.group(3), m.group(4), m.group(2) == '-->>', num))
            continue
        m = re.match(r'(alt|opt|loop|par|critical|break)\b\s*(.*)$', s)
        if m:
            itens.append(('abre', m.group(1), m.group(2)))
            pilha.append(m.group(1))
            continue
        m = re.match(r'(else|and)\b\s*(.*)$', s)
        if m:
            itens.append(('senao', m.group(1), m.group(2)))
            continue
        if s == 'end':
            itens.append(('fecha',))
            pilha.pop()
            continue
        raise ValueError('linha não reconhecida: ' + s)
    return parts, ordem, itens


def sequencia(nome):
    parts, ordem, itens = parse_seq(ler(nome))
    idx = {p: i for i, p in enumerate(ordem)}
    n = len(ordem)
    larg_p = [max(largura(parts[p][1], FS, True) + 24, 90) for p in ordem]
    rot_msg = lambda it: f'{it[5]}  {it[3]}'
    # colunas
    c = [0.0] * n
    reqs = {}
    for it in itens:
        if it[0] == 'msg':
            a, b = sorted((idx[it[1]], idx[it[2]]))
            w = largura(rot_msg(it), FS) + (14 if a != b else 0)
            if a == b:
                if b + 1 < n:
                    reqs[(a, b + 1)] = max(reqs.get((a, b + 1), 0), w + 70)
            else:
                reqs[(a, b)] = max(reqs.get((a, b), 0), w + 36)
        elif it[0] == 'nota':
            a, b = sorted((idx[it[1]], idx[it[2]]))
            w = max(largura(sem_tags(x), 14) for x in re.split(r'<br\s*/?>', it[3])) + 28
            if a != b:
                reqs[(a, b)] = max(reqs.get((a, b), 0), w - 120)
    for j in range(1, n):
        c[j] = c[j - 1] + (larg_p[j - 1] + larg_p[j]) / 2 + 30
        for (a, b), w in reqs.items():
            if b == j:
                c[j] = max(c[j], c[a] + w)
    x0 = 40 + larg_p[0] / 2 + 110
    c = [x0 + v for v in c]
    # linhas: primeiro passe calcula as alturas e os quadros
    TOPO = 40
    y = TOPO + 100
    lin = []         # (tipo, dados, y)
    quadros = []     # dicionários dos quadros alt/opt/...
    abertos = []
    prof = 0

    def envolve(*ps):
        for q in abertos:
            q['ps'].update(ps)

    for it in itens:
        if it[0] == 'msg':
            a, b = idx[it[1]], idx[it[2]]
            envolve(a, b)
            if a == b:
                lin.append(('self', it, y + 10))
                for q in abertos:
                    q['dir'] = max(q.get('dir', 0), c[a] + 50 + largura(rot_msg(it), FS))
                y += 54
            else:
                lin.append(('msg', it, y + 26))
                y += 40
        elif it[0] == 'nota':
            a, b = sorted((idx[it[1]], idx[it[2]]))
            envolve(a, b)
            partes = re.split(r'<br\s*/?>', it[3])
            h = len(partes) * 19 + 14
            lin.append(('nota', it, y + 8, h))
            y += h + 18
        elif it[0] == 'abre':
            q = {'tipo': it[1], 'cond': it[2], 'y0': y + 6, 'ps': set(), 'senoes': [], 'prof': len(abertos)}
            abertos.append(q)
            quadros.append(q)
            y += 44
        elif it[0] == 'senao':
            abertos[-1]['senoes'].append((it[2], y + 4))
            y += 36
        else:
            q = abertos.pop()
            q['y1'] = y + 4
            for qq in abertos:
                qq['ps'].update(q['ps'])
                qq['dir'] = max(qq.get('dir', 0), q.get('dir', 0))
            y += 18
    yfim = y + 30
    d = Diagrama(nome)
    # linhas de vida
    for i, p in enumerate(ordem):
        tipo, rot = parts[p]
        if tipo in ICONE and tipo != 'database':
            st = (f'shape=umlLifeline;participant={ICONE[tipo]};perimeter=lifelinePerimeter;html=1;container=0;'
                  'collapsible=0;recursiveResize=0;verticalAlign=top;spacingTop=50;size=46;outlineConnect=0;'
                  f'whiteSpace=nowrap;fontSize={FS};fontStyle=1;fontFamily=Helvetica;fontColor={TINTA};'
                  'labelBackgroundColor=#ffffff;strokeColor=#44403c;strokeWidth=1.5;fillColor=#ffffff;'
                  'dashed=0;lifelineDashed=1;')
            if tipo == 'database':
                st += 'fillColor=#f5f5f4;'
            d.v(esc(rot), st, c[i] - 23, TOPO, 46, yfim - TOPO)
        else:
            st = ('shape=umlLifeline;perimeter=lifelinePerimeter;html=1;container=0;collapsible=0;'
                  f'recursiveResize=0;size=46;outlineConnect=0;fontSize={FS};fontStyle=1;fontFamily=Helvetica;'
                  f'strokeColor=#44403c;fillColor={"#f5f5f4" if tipo == "database" else "#ffffff"};'
                  f'fontColor={TINTA};strokeWidth=1.5;')
            if tipo == 'database':
                rot = '«database»<br>' + esc(rot)
                d.v(rot, st, c[i] - larg_p[i] / 2, TOPO + 4, larg_p[i], yfim - TOPO - 4)
                continue
            d.v(esc(rot), st, c[i] - larg_p[i] / 2, TOPO, larg_p[i], yfim - TOPO)
    # quadros (atrás das mensagens)
    for q in sorted(quadros, key=lambda q: q['prof']):
        ps = q['ps'] or {0}
        mg = 92 - 16 * q['prof']
        x1 = c[min(ps)] - mg
        x2 = max(c[max(ps)] + mg, q.get('dir', 0) + 20 - 16 * q['prof'])
        f = fluxo(q['cond'])
        fill, stroke, txtc = COR_FLUXO.get(f, ('#f5f5f4', '#78716c', '#44403c'))
        rotq = q['tipo']
        wq = largura(rotq, 14, True) + 26
        d.v(rotq, f'shape=umlFrame;whiteSpace=wrap;html=1;width={wq:.0f};height=26;boundedLbl=1;fontSize=14;'
                  f'fontStyle=1;fontFamily=Helvetica;strokeColor={stroke};strokeWidth=1.5;fillColor={fill};'
                  f'swimlaneFillColor=none;fontColor={txtc};container=0;',
            x1, q['y0'], x2 - x1, q['y1'] - q['y0'])
        if q['cond']:
            d.v('[' + esc(q['cond']) + ']', f'text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;'
                f'fontFamily=Helvetica;fontColor={txtc};spacingLeft=4;whiteSpace=nowrap;',
                x1 + wq + 4, q['y0'], x2 - x1 - wq - 8, 26)
        for cond, ys in q['senoes']:
            d.e('', f'endArrow=none;dashed=1;dashPattern=8 5;html=1;strokeColor={stroke};strokeWidth=1.5;',
                p0=(x1, ys), p1=(x2, ys))
            f2 = fluxo(cond)
            t2 = COR_FLUXO.get(f2, (0, 0, txtc))[2]
            if cond:
                d.v('[' + esc(cond) + ']', f'text;html=1;align=left;verticalAlign=middle;fontSize=14;fontStyle=1;'
                    f'fontFamily=Helvetica;fontColor={t2};spacingLeft=4;whiteSpace=nowrap;',
                    x1 + 6, ys + 2, x2 - x1 - 12, 26)
    # mensagens e notas
    for item in lin:
        tipo, it, yy = item[0], item[1], item[2]
        if tipo == 'msg':
            a, b = idx[it[1]], idx[it[2]]
            ret = it[4]
            st = ('html=1;verticalAlign=bottom;labelBackgroundColor=none;fontSize=15;fontFamily=Helvetica;'
                  f'fontColor={TINTA};strokeColor=#292524;strokeWidth=1.3;endSize=9;'
                  + ('dashed=1;dashPattern=6 4;endArrow=open;' if ret else 'endArrow=block;endFill=1;'))
            d.e(f'<b>{it[5]}</b>&nbsp; {esc(it[3])}', st, p0=(c[a], yy), p1=(c[b], yy))
        elif tipo == 'self':
            a = idx[it[1]]
            st = ('html=1;endArrow=block;endFill=1;endSize=9;strokeColor=#292524;strokeWidth=1.3;rounded=0;'
                  + ('dashed=1;' if it[4] else ''))
            d.e('', st, p0=(c[a], yy), p1=(c[a], yy + 26), pontos=[(c[a] + 36, yy), (c[a] + 36, yy + 26)])
            d.v(f'<b>{it[5]}</b>&nbsp; {esc(it[3])}', f'text;html=1;align=left;verticalAlign=middle;fontSize={FS};'
                f'fontFamily=Helvetica;fontColor={TINTA};whiteSpace=nowrap;labelBackgroundColor=#ffffff;',
                c[a] + 42, yy - 2, largura(f'{it[5]}  {it[3]}', FS) + 20, 30)
        else:
            h = item[3]
            a, b = sorted((idx[it[1]], idx[it[2]]))
            txt = it[3]
            f = fluxo(txt)
            legenda = txt.startswith('FP = ')
            w = max(largura(sem_tags(x), 14) for x in re.split(r'<br\s*/?>', txt)) + 30
            xa, xb = c[a] - 60, c[b] + 60
            if xb - xa < w:
                m = (xa + xb) / 2
                xa, xb = m - w / 2, m + w / 2
            if legenda:
                fill, stroke = '#faf6f4', VINHO
            else:
                fill, stroke, _t = COR_FLUXO.get(f, ('#fffbeb', '#d97706', ''))
            d.v(br(txt), f'shape=note;size=12;whiteSpace=wrap;html=1;align=left;spacingLeft=10;fontSize=14;'
                f'fontFamily=Helvetica;fontColor={TINTA};fillColor={fill};strokeColor={stroke};strokeWidth=1.3;'
                + ('fontStyle=1;' if legenda else ''), xa, yy, xb - xa, h)
    d.salvar()


# ----------------------------------------------------------------------------------------------
# Diagrama de atividade com raias (UML)
# ----------------------------------------------------------------------------------------------
OBJETOS = {   # nós de objeto: (de, para, rótulo)  — a aresta de→para passa pelo objeto (seta tracejada)
    'negocio-1-evento': [('s3', 'p1', 'e : Evento [publicado]'), ('s4', 'cA1', 'p : Participação [confirmada]'),
                         ('s7', 'fim', 'a : Avaliação [registrada]')],
    'negocio-2-conteudo': [('s3', 'm1', 'p : Post [publicado]'), ('s5', 's4', 'c : Compartilhamento [registrado]')],
    'negocio-3-moderacao': [('s3', 'd1', 'd : Denúncia [pendente]'), ('d1', 'cA1', 'd : Denúncia [em análise]'),
                            ('s5', 's6', 'd : Denúncia [decidida]')],
    'negocio-4-analise': [('s1', 'u5', 'i : Indicadores [calculados]'), ('s2', 'u7', 'r : Ranking [ordenado]')],
    'atividade-005-avaliar-evento': [('a4', 'a6', 'a : AvaliaçãoEvento [atualizada]'),
                                     ('a5', 'a6', 'a : AvaliaçãoEvento [registrada]')],
    'atividade-006-avaliar-apresentador': [('a4', 'a5', 'a : AvaliaçãoApresentação [registrada]')],
    'atividade-007-ranking': [('s3', 's4', 'r : Ranking [ordenado]')],
    'atividade-008-dashboards': [('s1', 'd3', 'p : Painéis [calculados]')],
    'atividade-013-denuncias': [('a3', 'cA1', 'd : Denúncia [em análise]'), ('s4', 's5', 'd : Denúncia [decidida]')],
    'atividade-015-lembrete': [('a3', 'a5', 'n : Notificação [não lida]')],
    'sem-sistema': [('E', 'F', 'l : Lista de presença [planilha]')],
}
RAIA_DE = {'Usuário ou Administrador': 'Usuário', 'Todos': None}
ORDEM_RAIAS = {
    'negocio-4-analise': ['Usuário', 'Administrador', 'Sistema'],
    'atividade-008-dashboards': ['Usuário', 'Administrador', 'Sistema'],
    'atividade-015-lembrete': ['Agendador', 'Sistema', 'Participante'],
}
NOME_RAIA = {'Sistema': 'Sistema (Meets)', 'Usuário': 'Usuário'}
FUNDO_RAIA = ['#fdf7f6', '#ffffff']


def parse_atividade(txt):
    nos, arestas, partes = {}, [], []
    parte = None
    for l in txt.split('\n'):
        s = l.strip()
        m = re.match(r'subgraph\s+(\w+)', s)
        if m:
            parte = m.group(1)
            partes.append(parte)
            continue
        m = re.match(r'^(\w+)(\(\(\(|\(\(|\{|\[)"([^"]*)"(\)\)\)|\)\)|\}|\])$', s)
        if m:
            forma = {'(((': 'fim', '((': 'circ', '{': 'dec', '[': 'acao'}[m.group(2)]
            nos[m.group(1)] = {'forma': forma, 'txt': m.group(3), 'parte': parte}
            continue
        if '~~~' in s or s.startswith(('class ', 'classDef', 'style', 'direction', 'end', 'flowchart')):
            continue
        # cadeia: a --> b -- rot --> c -.-> d
        toks = re.split(r'\s*(-- [^-]+ -->|-->|-\.->)\s*', s)
        if len(toks) >= 3:
            for i in range(0, len(toks) - 2, 2):
                op = toks[i + 1]
                rot = op[3:-4].strip() if op.startswith('-- ') else ''
                arestas.append((toks[i], toks[i + 2], rot, op == '-.->'))
    return nos, arestas, partes


def corta(p, q, r, folga=4):
    """O segmento p-q atravessa o retângulo r=(x, y, w, h)?"""
    x, y, w, h = r[0] - folga, r[1] - folga, r[2] + 2 * folga, r[3] + 2 * folga
    for i in range(1, 40):
        t = i / 40
        px, py = p[0] + (q[0] - p[0]) * t, p[1] + (q[1] - p[1]) * t
        if x < px < x + w and y < py < y + h:
            return True
    return False


def ator(no):
    m = re.match(r'<b>([^<]+)</b><br/>(.*)$', no['txt'])
    return (m.group(1), m.group(2)) if m else (None, no['txt'])


def atividade(nome):
    txt = ler(nome)
    nos, arestas, partes = parse_atividade(txt)
    sem_sistema = nome == 'sem-sistema'
    if sem_sistema:
        problemas = {k: v for k, v in nos.items() if k.startswith('P')}
        for k in problemas:
            del nos[k]
        for v in nos.values():
            v['parte'] = 'X'
        partes = ['X']
    # conectores A: viram ponte entre as partes
    # raias
    for k, v in nos.items():
        a, t = ator(v)
        v['ator'] = RAIA_DE.get(a, a) if a else None
        v['texto'] = t
        if a in RAIA_DE and RAIA_DE[a] is None:
            v['todas'] = True
    saida = {k: [] for k in nos}
    entrada = {k: [] for k in nos}
    for a, b, r, tr in arestas:
        saida[a].append(b)
        entrada[b].append(a)
    # nós de objeto
    for i, (a, b, rot) in enumerate(OBJETOS.get(nome, [])):
        k = f'obj{i}'
        nos[k] = {'forma': 'obj', 'texto': rot, 'parte': nos[a]['parte'], 'ator': nos[a]['ator']}
        novo = []
        for (x, y, r, tr) in arestas:
            if (x, y) == (a, b):
                novo += [(x, k, r, True), (k, y, '', True)]
            else:
                novo.append((x, y, r, tr))
        if not any(x == a and y == k for x, y, _, _ in novo):
            novo.append((a, k, '', True))
        arestas = novo
    saida = {k: [] for k in nos}
    entrada = {k: [] for k in nos}
    for a, b, r, tr in arestas:
        saida[a].append(b)
        entrada[b].append(a)
    # ator de decisões, início, fim e conectores: herda do vizinho
    for _ in range(4):
        for k, v in nos.items():
            if v.get('ator') or v.get('todas'):
                continue
            viz = (entrada[k] + saida[k]) if v['forma'] in ('fim', 'obj') else (saida[k] + entrada[k])
            if v['forma'] == 'dec':
                suc = {nos[o].get('ator') for o in saida[k] if nos[o]['forma'] in ('acao', 'dec')}
                viz = (saida[k] + entrada[k]) if len(suc) == 1 and None not in suc else (entrada[k] + saida[k])
            if v['forma'] == 'circ' and k.startswith('cA2'):
                viz = saida[k]
            if v['forma'] == 'circ' and k.startswith('cA1'):
                viz = entrada[k]
            for o in viz:
                if nos[o].get('ator'):
                    v['ator'] = nos[o]['ator']
                    break
    raias = []
    for k, v in nos.items():
        if v.get('ator') and v['ator'] not in raias:
            raias.append(v['ator'])
    if nome in ORDEM_RAIAS:
        raias = [r for r in ORDEM_RAIAS[nome] if r in raias] + [r for r in raias if r not in ORDEM_RAIAS[nome]]
    # níveis (caminho mais longo, ignorando retornos), por parte
    ordem_txt = list(nos)
    nivel = {}
    retorno = set()

    def dfs(k, pilha, vis):
        vis.add(k)
        pilha.add(k)
        for o in saida[k]:
            if o in pilha:
                retorno.add((k, o))
            elif o not in vis:
                dfs(o, pilha, vis)
        pilha.discard(k)
    vis = set()
    for k in ordem_txt:
        if k not in vis and not entrada[k]:
            dfs(k, set(), vis)
    for k in ordem_txt:
        if k not in vis:
            dfs(k, set(), vis)
    grau = {k: sum(1 for a in entrada[k] if (a, k) not in retorno) for k in nos}
    fila = [k for k in ordem_txt if grau[k] == 0]
    topo = []
    while fila:
        k = fila.pop(0)
        topo.append(k)
        for o in saida[k]:
            if (k, o) in retorno:
                continue
            grau[o] -= 1
            if grau[o] == 0:
                fila.append(o)
    ocup = {}
    col = {}
    for k in topo:
        v = nos[k]
        if v['forma'] == 'circ' and k.startswith('cA2'):
            nivel[k] = 0
        else:
            nivel[k] = max([nivel[a] + 1 for a in entrada[k] if (a, k) not in retorno and nos[a]['parte'] == v['parte']]
                           + [0])
        raia = 'TODAS' if v.get('todas') else v['ator']
        while True:
            chave = (v['parte'], raia, nivel[k])
            usados = ocup.get(chave, [])
            if v.get('todas'):
                livre = all(not ocup.get((v['parte'], r, nivel[k])) for r in raias)
                if livre:
                    break
                nivel[k] += 1
                continue
            if len(usados) < 4 and not any(ocup.get((v['parte'], 'TODAS', nivel[k]), [])):
                if not usados or (v['forma'] == 'obj') == all(nos[u]['forma'] == 'obj' for u in usados):
                    break
            nivel[k] += 1
        if v.get('todas'):
            ocup.setdefault((v['parte'], 'TODAS', nivel[k]), []).append(k)
            for r in raias:
                ocup.setdefault((v['parte'], r, nivel[k]), []).append(k)
            col[k] = 0
        else:
            ocup.setdefault(chave, []).append(k)
            col[k] = len(ocup[chave]) - 1
            if v['forma'] == 'obj':
                src = entrada[k][0]
                if nos[src].get('ator') == raia and col.get(src, 0) not in [col[u] for u in usados]:
                    col[k] = col.get(src, 0)
    # dimensões
    W_ACAO = 230
    sub = {}
    for (p, r, nv), lst in ocup.items():
        if r != 'TODAS':
            sub[(p, r)] = max(sub.get((p, r), 1), len(lst))
    tam = {}

    def larg_acao(v):
        return W_ACAO if sub.get((v['parte'], v.get('ator')), 1) <= 2 else 180
    for k, v in nos.items():
        f = v['forma']
        if f == 'acao':
            wa = larg_acao(v)
            ls = quebra(sem_tags(v['texto']), wa - 24, 14)
            tam[k] = (wa if not v.get('todas') else 0, len(ls) * 18 + 20)
        elif f == 'dec':
            ls = quebra(sem_tags(v['texto']), 150, 13)
            tam[k] = (190, max(70, len(ls) * 17 + 40))
        elif f == 'obj':
            tam[k] = (max(largura(v['texto'], 13) + 22, 170), 40)
        elif f == 'fim':
            tam[k] = (34, 34)
        else:
            tam[k] = (30, 30) if k == 'ini' or not k.startswith('cA') else (34, 34)
    alt_nivel = {}
    for k in nos:
        p = nos[k]['parte']
        alt_nivel[(p, nivel[k])] = max(alt_nivel.get((p, nivel[k]), 0), tam[k][1])
    d = Diagrama(nome)
    GAP_Y = 26
    CAB = 44
    x_parte = 30
    pos = {}
    caixas = {}
    for p in partes:
        rs = [r for r in raias if any(v['parte'] == p and v.get('ator') == r for v in nos.values())]
        if any(v['parte'] == p and v.get('todas') for v in nos.values()):
            rs = raias
        larg_r = {r: max(250, sub.get((p, r), 1) * ((W_ACAO if sub.get((p, r), 1) <= 2 else 180) + 24) + 26) for r in rs}
        for k, v in nos.items():
            if v['parte'] == p and v['forma'] == 'obj':
                larg_r[v['ator']] = max(larg_r[v['ator']], tam[k][0] + 40)
        niveis = sorted({nivel[k] for k in nos if nos[k]['parte'] == p})
        ys = {}
        y = CAB + 24
        for nv in niveis:
            ys[nv] = y
            y += alt_nivel[(p, nv)] + GAP_Y
        altura = y + 6
        x = x_parte
        xr = {}
        for i, r in enumerate(rs):
            xr[r] = x
            d.v(esc(NOME_RAIA.get(r, r)),
                f'swimlane;html=1;startSize={CAB};horizontal=1;fontSize=17;fontStyle=1;fontFamily=Helvetica;'
                f'fontColor=#ffffff;fillColor={VINHO};strokeColor=#5f1d1f;strokeWidth=3;'
                f'swimlaneFillColor={FUNDO_RAIA[i % 2]};collapsible=0;container=1;',
                x, 20, larg_r[r], altura)
            x += larg_r[r]
        caixas[p] = (x_parte, x)
        for k, v in nos.items():
            if v['parte'] != p:
                continue
            w, h = tam[k]
            yc = ys[nivel[k]] + alt_nivel[(p, nivel[k])] / 2 + 20
            if v.get('todas'):
                x1, x2 = xr[rs[0]] + 20, x - 20
                pos[k] = (x1, yc - h / 2, x2 - x1, h)
                continue
            r = v['ator']
            nsub = len(ocup[(p, r, nivel[k])])
            nmax = sub.get((p, r), 1)
            larg_util = larg_r[r]
            slot = larg_util / nmax
            if nmax == 1:
                cx = xr[r] + larg_util / 2
            else:
                cx = xr[r] + slot * (col[k] + 0.5)
            pos[k] = (cx - w / 2, yc - h / 2, w, h)
        x_parte = x + 60
    # desenha os nós
    ids = {}
    for k in ordem_txt + [k for k in nos if k not in ordem_txt]:
        v = nos[k]
        x, y, w, h = pos[k]
        f = v['forma']
        base = 'html=1;whiteSpace=wrap;fontFamily=Helvetica;'
        if f == 'acao':
            st = base + ('rounded=1;arcSize=24;align=left;spacingLeft=12;spacingRight=8;fontSize=14;'
                         f'fontColor={TINTA};fillColor=#ffffff;strokeColor=#44403c;strokeWidth=1.5;')
            if sem_sistema and '⚠' in v['texto']:
                st += 'strokeColor=#dc2626;'
            if v.get('todas'):
                st += 'align=center;'
                ids[k] = d.v('<b>Todos:</b> ' + br(v['texto']), st, x, y, w, h)
                continue
            ids[k] = d.v(br(v['texto']), st, x, y, w, h)
        elif f == 'dec':
            ids[k] = d.v(br(v['texto']), base + f'rhombus;fontSize=13;fontColor={TINTA};fillColor=#fefce8;'
                         'strokeColor=#a16207;strokeWidth=1.5;spacing=18;', x, y, w, h)
        elif f == 'obj':
            ids[k] = d.v(esc(v['texto']), base + f'rounded=0;fontSize=13;fontColor={TINTA};fillColor=#ffffff;'
                         'strokeColor=#44403c;strokeWidth=1.3;', x, y, w, h)
        elif f == 'fim':
            ids[k] = d.v('', 'ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;strokeWidth=1.5;',
                         x, y, w, h)
            if v['txt'] not in ('Fim',):
                d.v(esc(v['txt']), 'text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=2;'
                    f'fontFamily=Helvetica;fontColor=#57534e;whiteSpace=wrap;', x + w + 6, y - 4, 130, h + 8)
        else:
            if k.startswith('cA'):
                ids[k] = d.v('A', 'ellipse;html=1;fontSize=15;fontStyle=1;fontFamily=Helvetica;fillColor=#ffffff;'
                             f'strokeColor=#44403c;strokeWidth=1.5;fontColor={TINTA};', x, y, w, h)
            else:
                ids[k] = d.v('', 'ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#000000;',
                             x, y, w, h)
                if v['txt'] not in ('Início',):
                    d.v(esc(v['txt']), 'text;html=1;align=left;verticalAlign=middle;fontSize=13;fontStyle=2;'
                        f'fontFamily=Helvetica;fontColor=#57534e;', x + w + 6, y, 110, h)
    # arestas
    for a, b, rot, tr in arestas:
        if a not in ids or b not in ids:
            continue
        st = ('html=1;endArrow=open;endSize=10;strokeColor=#292524;strokeWidth=1.3;fontSize=13;fontFamily=Helvetica;'
              'labelBackgroundColor=#ffffff;fontColor=#292524;')
        if tr:
            st += 'dashed=1;dashPattern=6 4;'
        pts = []
        ax, ay, aw, ah = pos[a]
        bx, by, bw, bh = pos[b]
        bloqueia = [o for o in pos if o not in (a, b) and corta((ax + aw / 2, ay + ah / 2), (bx + bw / 2, by + bh / 2), pos[o])]
        frente = not ((a, b) in retorno or by + bh / 2 < ay + ah / 2 - 5)
        ym = (ay + ah + by) / 2
        cot = [(ax + aw / 2, ay + ah), (ax + aw / 2, ym), (bx + bw / 2, ym), (bx + bw / 2, by)]
        cotovelo_livre = by > ay + ah + 10 and not any(
            corta(cot[i], cot[i + 1], pos[o], 2) for i in range(3) for o in pos if o not in (a, b))
        if bloqueia and frente and cotovelo_livre:
            st += ('edgeStyle=orthogonalEdgeStyle;rounded=1;exitX=0.5;exitY=1;exitDx=0;exitDy=0;entryX=0.5;entryY=0;'
                   'entryDx=0;entryDy=0;')
            pts = [(ax + aw / 2, ym), (bx + bw / 2, ym)]
        elif bloqueia and frente:
            xm = max([ax + aw, bx + bw] + [pos[o][0] + pos[o][2] for o in bloqueia]) + 22
            st += ('edgeStyle=orthogonalEdgeStyle;rounded=1;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;'
                   'entryDx=0;entryDy=0;')
            pts = [(xm, ay + ah / 2), (xm, by + bh / 2)]
        elif (a, b) in retorno or by + bh / 2 < ay + ah / 2 - 5:
            # retorno (laço): contorna pelo lado, em ângulo reto
            st += 'edgeStyle=orthogonalEdgeStyle;rounded=1;'
            if bx + bw < ax - 10:      # destino à esquerda: sai pela esquerda e entra pela direita
                st += 'exitX=0;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;'
            elif bx > ax + aw + 10:    # destino à direita: sobe e entra pela esquerda
                st += 'exitX=0.5;exitY=0;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;'
            else:                      # mesma coluna: contorna pela direita
                xm = max(ax + aw, bx + bw) + 22
                st += 'exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=1;entryY=0.5;entryDx=0;entryDy=0;'
                pts = [(xm, ay + ah / 2), (xm, by + bh / 2)]
        valor = f'[{esc(rot)}]' if rot else ''
        eid = d.e('', st, ids[a], ids[b], pontos=pts)
        if valor:
            d.rotulo_aresta(eid, valor, -0.45, 0, 0, 'fontStyle=1;fontColor=#57534e;')
    if sem_sistema:
        # coluna de problemas como notas
        x1 = caixas['X'][1] + 50
        y = 70
        for k, v in problemas.items():
            t = sem_tags(v['txt'])
            ls = quebra(t, 330, 14)
            h = len(ls) * 18 + 22
            nid = d.v(esc(t), 'shape=note;size=14;whiteSpace=wrap;html=1;align=left;spacingLeft=10;fontSize=14;'
                      f'fontFamily=Helvetica;fontColor={TINTA};fillColor=#fef2f2;strokeColor=#dc2626;',
                      x1, y, 370, h)
            y += h + 28
        d.v('Problemas do processo atual', 'text;html=1;fontSize=17;fontStyle=1;fontFamily=Helvetica;'
            f'fontColor={VINHO};align=left;', x1, 26, 370, 34)
    d.salvar()


# ----------------------------------------------------------------------------------------------
def todos():
    nomes = sorted(f[:-4] for f in os.listdir(FONTES) if f.endswith('.mmd'))
    return [n for n in nomes if n not in ('der-008a-dashboards-conteudo', 'der-008b-dashboards-avaliacoes')]


def gerar(nome):
    if nome.startswith('classe-'):
        classe(nome)
    elif nome.startswith('der-'):
        der(nome)
    elif nome.startswith('mer-'):
        mer(nome)
    elif nome.startswith('sequencia-'):
        sequencia(nome)
    else:
        atividade(nome)


if __name__ == '__main__':
    for n in sys.argv[1:] or todos():
        gerar(n)
        print('ok', n)
