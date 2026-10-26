"""Gera os 4 diagramas de casos de uso da apresentação (Mermaid).

O Mermaid não tem diagrama de casos de uso; usamos um flowchart com o ator UML
desenhado em SVG (imagem embutida) e os casos de uso em formato de cápsula.
Uso: python3 gerar_casos_de_uso.py && ./render.sh uc-*.mmd
"""
import base64
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

CORES = {  # traço, preenchimento
    'visitante': ('#64748b', '#f8fafc'),
    'usuario': ('#c026d3', '#fdf4ff'),
    'admin': ('#0d9488', '#f0fdfa'),
}


def ator(cor):
    traco, fundo = CORES[cor]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="60" height="90" viewBox="0 0 60 90">'
           f'<g fill="none" stroke="{traco}" stroke-width="4" stroke-linecap="round">'
           f'<circle cx="30" cy="14" r="11" fill="{fundo}"/><line x1="30" y1="25" x2="30" y2="58"/>'
           f'<line x1="8" y1="38" x2="52" y2="38"/><line x1="30" y1="58" x2="12" y2="86"/>'
           f'<line x1="30" y1="58" x2="48" y2="86"/></g></svg>')
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


def relogio():
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 80 80">'
           '<g fill="none" stroke="#ea580c" stroke-width="4" stroke-linecap="round">'
           '<circle cx="40" cy="40" r="32" fill="#fff7ed"/><line x1="40" y1="40" x2="40" y2="20"/>'
           '<line x1="40" y1="40" x2="56" y2="48"/></g></svg>')
    return 'data:image/svg+xml;base64,' + base64.b64encode(svg.encode()).decode()


CABECALHO = """---
config:
  look: neo
  theme: redux-color
  themeVariables:
    labelBackground: '#ffffff'
    edgeLabelBackground: '#ffffff'
    mainBkg: '#ffffff'
    fontSize: 20px
  flowchart:
    nodeSpacing: 26
    rankSpacing: 140
    wrappingWidth: 420
    subGraphTitleMargin:
      top: 14
      bottom: 22
---
flowchart LR
"""

ESTILO = """
  classDef ator fill:transparent,stroke:transparent,color:#1f2937
  classDef basico fill:#f1f5f9,stroke:#475569,color:#0f172a
  classDef analise fill:#dbeafe,stroke:#2563eb,color:#0f172a
  classDef conducao fill:#ffedd5,stroke:#ea580c,color:#0f172a
  classDef capitulo stroke-width:4px
"""


def no_ator(nid, nome, img):
    return f'  {nid}@{{ img: "{img}", label: "{nome}", pos: "b", w: 56, h: 84, constraint: "on" }}\n'


def caso(cid, nome, tipo, capitulo=False):
    linhas = f'    {cid}(["{nome}"])\n    class {cid} {tipo}\n'
    if capitulo:
        linhas += f'    class {cid} capitulo\n'
    return linhas


def salvar(nome, corpo):
    with open(os.path.join(AQUI, nome), 'w') as f:
        f.write(CABECALHO + corpo + ESTILO)


# 1a) Acesso e conteúdo
c = no_ator('VIS', 'Visitante', ator('visitante'))
c += no_ator('USR', 'Usuário', ator('usuario'))
c += '  subgraph S1["Sistema Meets — acesso e conteúdo"]\n'
for cid, nome in [('c014', '#014 Cadastrar Usuário'), ('c001', '#001 Fazer Login'), ('c002', '#002 Visualizar Feed'),
                  ('c009', '#009 Manter Posts'), ('c003', '#003 Interagir com Posts'), ('c010', '#010 Manter Perfil')]:
    c += caso(cid, nome, 'basico')
c += '  end\n'
c += '  VIS --- c014\n  VIS --- c001\n'
for cid in ['c002', 'c009', 'c003', 'c010']:
    c += f'  USR --- {cid}\n'
c += '  class VIS,USR ator\n'
salvar('uc-1-acesso-conteudo.mmd', c)

# 1b) Rede, comunicação e utilidades
c = no_ator('USR', 'Usuário', ator('usuario'))
c += '  subgraph S1["Sistema Meets — rede, comunicação e utilidades"]\n'
lista = [('c017', '#017 Conectar-se a Usuários'), ('c018', '#018 Conversar'), ('c019', '#019 Visualizar Notificações'),
         ('c020', '#020 Pesquisar'), ('c021', '#021 Consultar Histórico'), ('c022', '#022 Gerenciar Configurações'),
         ('c016', '#016 Denunciar Conteúdo')]
for cid, nome in lista:
    c += caso(cid, nome, 'basico')
c += '  end\n'
for cid, _ in lista:
    c += f'  USR --- {cid}\n'
c += '  class USR ator\n'
salvar('uc-2-rede-utilidades.mmd', c)

# 2) Eventos, avaliação e análise (5 dos 6 capítulos + automação)
c = no_ator('USR', 'Usuário', ator('usuario'))
c += f'  AGD@{{ img: "{relogio()}", label: "Agendador do Sistema", pos: "b", w: 70, h: 70, constraint: "on" }}\n'
c += '  subgraph S2["Sistema Meets — eventos, avaliação e análise"]\n'
c += caso('c011', '#011 Manter Eventos', 'basico')
c += caso('c004', '#004 Interagir com Eventos', 'basico')
c += caso('c005', '#005 Avaliar Evento', 'analise', True)
c += caso('c006', '#006 Avaliar Apresentador', 'analise', True)
c += caso('c007', '#007 Visualizar Ranking de Apresentadores', 'analise', True)
c += caso('c008', '#008 Visualizar Dashboards', 'analise', True)
c += caso('c015', '#015 Lembrar Avaliação Pendente', 'conducao', True)
c += caso('c019', '#019 Visualizar Notificações', 'basico')
c += '  end\n'
for cid in ['c011', 'c004', 'c005', 'c006', 'c007', 'c008']:
    c += f'  USR --- {cid}\n'
c += '  AGD --- c015\n  USR ~~~ c015\n'
c += '  c015 -. "«include»" .-> c019\n'
c += '  class USR,AGD ator\n'
salvar('uc-3-eventos-avaliacao-analise.mmd', c)

# 3) Administração e moderação
c = no_ator('USR', 'Usuário', ator('usuario'))
c += no_ator('ADM', 'Administrador', ator('admin'))
c += '  ADM -- "generalização" --> USR\n'
c += '  subgraph S3["Sistema Meets — administração e moderação"]\n'
c += caso('c013', '#013 Analisar Denúncias', 'analise', True)
c += caso('c023', '#023 Remover Conteúdo Impróprio', 'basico')
c += caso('c012', '#012 Manter Usuários', 'basico')
c += caso('c008', '#008 Visualizar Dashboards (plataforma)', 'analise', True)
c += '  end\n'
for cid in ['c013', 'c023', 'c012', 'c008']:
    c += f'  ADM --- {cid}\n'
c += '  c023 -. "«extend»" .-> c013\n'
c += '  class USR,ADM ator\n'
salvar('uc-4-administracao.mmd', c)
print('ok')
