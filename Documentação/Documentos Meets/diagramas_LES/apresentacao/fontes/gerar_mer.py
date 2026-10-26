"""Gera os recortes do MER conceitual (notação de Chen) de cada capítulo, em Mermaid.
Entidade = retângulo, relacionamento = losango, atributo = elipse (chave sublinhada,
derivado tracejado, multivalorado com borda dupla). Uso: python3 gerar_mer.py && ./render.sh mer-*.mmd
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

CORES = {  # mesmas cores das tabelas no DER
    'USUARIO': ('#fdf4ff', '#c026d3'), 'PERFIL': ('#fff7ed', '#ea580c'), 'CONFIG': ('#f8fafc', '#64748b'),
    'EVENTO': ('#f0fdf4', '#16a34a'), 'POST': ('#ecfeff', '#0891b2'), 'APRES': ('#f5f3ff', '#7c3aed'),
    'NOTIF': ('#fffbeb', '#d97706'), 'DENUNCIA': ('#fefce8', '#ca8a04'), 'ACAO': ('#fef2f2', '#dc2626'),
    'COMENT': ('#f0f9ff', '#0284c7'),
}
NOMES = {'USUARIO': 'USUÁRIO', 'PERFIL': 'PERFIL', 'CONFIG': 'CONFIGURAÇÃO', 'EVENTO': 'EVENTO', 'POST': 'POST',
         'APRES': 'APRESENTAÇÃO', 'NOTIF': 'NOTIFICAÇÃO', 'DENUNCIA': 'DENÚNCIA', 'ACAO': 'AÇÃO ADMINISTRATIVA',
         'COMENT': 'COMENTÁRIO'}


def mer(arquivo, entidades, rels, direcao='TB'):
    """entidades: {ENT: [atributos]}; atributo com '*' = chave, '~' = derivado, '+' = multivalorado.
    rels: [(id, rótulo, [(ENT, cardinalidade), (ENT, cardinalidade)], [atributos do relacionamento])].
    O 1º lado de cada relacionamento fica acima do losango e o 2º abaixo."""
    L = ['---', 'config:', '  look: neo', '  theme: redux-color', '  themeVariables:', '    fontSize: 22px',
         '    edgeLabelBackground: "#ffffff"', '  flowchart:', '    nodeSpacing: 26', '    rankSpacing: 46', '---',
         f'flowchart {direcao}']
    estilos = []
    segundos = {lados[1][0] for _r, _t, lados, _a in rels}
    n = 0

    def atributo(texto_bruto):
        nonlocal n
        n += 1
        nid = f'a{n}'
        texto = texto_bruto.lstrip('*~+')
        if texto_bruto.startswith('*'):
            texto = f'<u>{texto}</u>'
        L.append(f'  {nid}(["{texto}"])')
        estilos.append(f'  class {nid} atr')
        if texto_bruto.startswith('~'):
            estilos.append(f'  style {nid} stroke-dasharray:6 4')
        if texto_bruto.startswith('+'):
            estilos.append(f'  style {nid} stroke-width:5px')
        return nid

    for ent, atributos in entidades.items():
        L.append(f'  {ent}["{NOMES[ent]}"]')
        fundo, traco = CORES[ent]
        estilos.append(f'  style {ent} fill:{fundo},stroke:{traco},stroke-width:3px')
        for a in atributos:
            nid = atributo(a)
            L.append(f'  {ent} --- {nid}' if ent in segundos else f'  {nid} --- {ent}')
    for rid, rotulo, lados, atributos in rels:
        L.append(f'  {rid}{{"{rotulo}"}}')
        estilos.append(f'  class {rid} rel')
        (e1, c1), (e2, c2) = lados
        L.append(f'  {e1} ---|"{c1}"| {rid}')
        L.append(f'  {rid} ---|"{c2}"| {e2}')
        for a in atributos:
            L.append(f'  {rid} --- {atributo(a)}')
    L += ['  classDef atr fill:#ffffff,stroke:#475569,color:#0f172a',
          '  classDef rel fill:#fefce8,stroke:#a16207,color:#0f172a'] + estilos
    with open(os.path.join(AQUI, arquivo), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')


# Cap. 1 — #015 Lembrar Avaliação Pendente
mer('mer-015-lembrete.mmd',
    {'USUARIO': ['*id', 'nome'], 'CONFIG': ['notificações ligadas'], 'EVENTO': ['*id', 'título', 'data', 'horário de fim'],
     'APRES': ['data', 'horário de fim'], 'NOTIF': ['*id', 'título', 'alvo', 'lida em']},
    [('r1', 'define', [('USUARIO', '1'), ('CONFIG', '1')], []),
     ('r2', 'participa', [('USUARIO', 'N'), ('EVENTO', 'N')], ['situação']),
     ('r3', 'acontece em', [('APRES', 'N'), ('EVENTO', '1')], []),
     ('r4', 'recebe', [('USUARIO', '1'), ('NOTIF', 'N')], [])])
# Cap. 2 — #005 Avaliar Evento
mer('mer-005-avaliar-evento.mmd',
    {'USUARIO': ['*id', 'nome', 'e-mail'], 'EVENTO': ['*id', 'título', 'data', 'horário de fim', 'local', '~média de estrelas']},
    [('r1', 'organiza', [('USUARIO', '1'), ('EVENTO', 'N')], []),
     ('r2', 'participa', [('USUARIO', 'N'), ('EVENTO', 'N')], ['situação (host / confirmada)']),
     ('r3', 'avalia', [('USUARIO', 'N'), ('EVENTO', 'N')], ['estrelas (1–5)', 'comentário', 'visibilidade'])])
# Cap. 3 — #006 Avaliar Apresentador
mer('mer-006-avaliar-apresentador.mmd',
    {'USUARIO': ['*id', 'nome'], 'APRES': ['*id', 'título', 'data', 'horário de fim'], 'EVENTO': ['*id', 'título']},
    [('r1', 'apresenta', [('USUARIO', 'N'), ('APRES', 'N')], []),
     ('r2', 'acontece em', [('APRES', 'N'), ('EVENTO', '1')], []),
     ('r3', 'participa', [('USUARIO', 'N'), ('EVENTO', 'N')], ['situação']),
     ('r4', 'avalia', [('USUARIO', 'N'), ('APRES', 'N')], ['estrelas (1–5)', '+atributos (6, de 0 a 99)', 'comentário', 'visibilidade'])])
# Cap. 4 — #007 Ranking
mer('mer-007-ranking.mmd',
    {'USUARIO': ['*id', 'nome', 'situação', '~pontuação geral', '~posição no ranking'], 'PERFIL': ['cargo', 'foto'],
     'APRES': ['*id', 'título']},
    [('r1', 'possui', [('USUARIO', '1'), ('PERFIL', '1')], []),
     ('r2', 'apresenta', [('USUARIO', 'N'), ('APRES', 'N')], []),
     ('r3', 'avalia', [('USUARIO', 'N'), ('APRES', 'N')], ['estrelas', '+atributos (6)', 'data'])])
# Cap. 5 — #008 Dashboards
mer('mer-008-dashboards.mmd',
    {'USUARIO': ['*id', 'tipo', 'situação'], 'POST': ['*id', 'data'], 'EVENTO': ['*id', 'data', 'horário de fim'],
     'COMENT': ['*id'], 'DENUNCIA': ['*id', 'situação']},
    [('r1', 'publica', [('USUARIO', '1'), ('POST', 'N')], []),
     ('r2', 'organiza', [('USUARIO', '1'), ('EVENTO', 'N')], []),
     ('r3', 'curte / compartilha', [('USUARIO', 'N'), ('POST', 'N')], []),
     ('r4', 'escreve', [('USUARIO', '1'), ('COMENT', 'N')], []),
     ('r5', 'sobre', [('COMENT', 'N'), ('POST', '1')], []),
     ('r6', 'participa / avalia', [('USUARIO', 'N'), ('EVENTO', 'N')], ['estrelas']),
     ('r7', 'denuncia', [('USUARIO', '1'), ('DENUNCIA', 'N')], [])])
# Cap. 6 — #013 Analisar Denúncias
mer('mer-013-denuncias.mmd',
    {'USUARIO': ['*id', 'tipo (usuário / admin)', 'situação'], 'DENUNCIA': ['*id', 'motivo', 'detalhes', 'situação', 'ação', 'justificativa'],
     'ACAO': ['*id', 'ação', 'alvo', 'data'], 'POST': ['*id'], 'EVENTO': ['*id']},
    [('r1', 'denuncia', [('USUARIO', '1'), ('DENUNCIA', 'N')], []),
     ('r2', 'analisa', [('USUARIO', '0..1 (admin)'), ('DENUNCIA', 'N')], []),
     ('r3', 'é alvo de', [('DENUNCIA', 'N'), ('POST', '0..1')], []),
     ('r4', 'é alvo de', [('DENUNCIA', 'N'), ('EVENTO', '0..1')], []),
     ('r5', 'realiza', [('USUARIO', '1 (admin)'), ('ACAO', 'N')], [])])
print('ok')
