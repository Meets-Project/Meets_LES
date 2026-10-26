"""Gera os recortes do DER de cada capítulo a partir de esquema.txt
(colunas extraídas do PostgreSQL com todas as migrações aplicadas: tabela|coluna|tipo|nulo|PK|FK>tabela).
Uso: python3 gerar_der.py && ./render.sh der-*.mmd
"""
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

TIPOS = {'character varying': 'varchar', 'timestamp with time zone': 'timestamptz',
         'time without time zone': 'time'}

# cor por tabela (mesma cor da entidade nos diagramas de classe e no MER)
CORES = {
    'users': ('#fdf4ff', '#c026d3'), 'profiles': ('#fff7ed', '#ea580c'), 'settings': ('#f8fafc', '#64748b'),
    'events': ('#f0fdf4', '#16a34a'), 'event_participants': ('#f7fee7', '#65a30d'),
    'posts': ('#ecfeff', '#0891b2'), 'presentation_speakers': ('#f5f3ff', '#7c3aed'),
    'event_ratings': ('#eff6ff', '#2563eb'), 'presentation_ratings': ('#eef2ff', '#4f46e5'),
    'notifications': ('#fffbeb', '#d97706'), 'reports': ('#fefce8', '#ca8a04'),
    'admin_actions': ('#fef2f2', '#dc2626'), 'post_likes': ('#f0f9ff', '#0284c7'),
    'post_comments': ('#f0f9ff', '#0284c7'), 'content_shares': ('#f0f9ff', '#0284c7'),
}


def ler_esquema():
    tabelas = {}
    for linha in open(os.path.join(AQUI, 'esquema.txt'), encoding='utf-8'):
        t, col, tipo, _nulo, pk, fk = linha.rstrip('\n').split('|')
        tabelas.setdefault(t, []).append((col, TIPOS.get(tipo, tipo), pk == 'PK', fk[3:] if fk.startswith('FK>') else None))
    return tabelas


ESQ = ler_esquema()


def der(nome, titulo, tabelas, colunas=None, extra_rel=(), direcao='TB'):
    """tabelas: lista; colunas: {tabela: [colunas a mostrar]} (padrão: todas)."""
    colunas = colunas or {}
    linhas = ['---', 'config:', '  look: neo', '  theme: redux-color', '  themeVariables:', '    fontSize: 22px',
              '  er:', '    entityPadding: 18', '---', 'erDiagram', f'  direction {direcao}']
    for t in tabelas:
        linhas.append(f'  {t} {{')
        for col, tipo, pk, fk in ESQ[t]:
            if t in colunas and col not in colunas[t]:
                continue
            chave = ','.join(x for x in (['PK'] if pk else []) + (['FK'] if fk else []))
            linhas.append(f'    {tipo} {col} {chave}'.rstrip())
        linhas.append('  }')
    for t in tabelas:  # relacionamentos pelas FKs reais
        for col, _tipo, pk, fk in ESQ[t]:
            if fk and fk in tabelas and not (t == 'users' and fk == 'users'):
                if t in colunas and col not in colunas[t]:
                    continue
                um_para_um = pk and len([c for c in ESQ[t] if c[2]]) == 1
                card = '||--||' if um_para_um else '||--o{'
                linhas.append(f'  {fk} {card} {t} : "{col}"')
    linhas += [f'  {r}' for r in extra_rel]
    for t in tabelas:
        fundo, traco = CORES.get(t, ('#ffffff', '#334155'))
        linhas.append(f'  style {t} fill:{fundo},stroke:{traco}')
    with open(os.path.join(AQUI, nome), 'w', encoding='utf-8') as f:
        f.write('\n'.join(linhas) + '\n')


U_BASE = ['id', 'name', 'email', 'account_type', 'status']

# Cap. 1 — #015 Lembrar Avaliação Pendente
der('der-015-lembrete.mmd', '#015', ['users', 'settings', 'events', 'event_participants', 'posts', 'notifications'],
    {'users': U_BASE, 'settings': ['user_id', 'notifications_enabled'],
     'events': ['id', 'author_id', 'title', 'event_date', 'event_end_time', 'share_token'],
     'posts': ['id', 'author_id', 'type', 'title', 'presentation_id', 'mentioned_event_id', 'event_date', 'event_end_time', 'share_token']})
# Cap. 2 — #005 Avaliar Evento
der('der-005-avaliar-evento.mmd', '#005', ['users', 'events', 'event_participants', 'event_ratings'],
    {'users': U_BASE, 'events': ['id', 'author_id', 'title', 'event_date', 'event_time', 'event_end_time', 'location', 'visibility']}, direcao='LR')
# Cap. 3 — #006 Avaliar Apresentador
der('der-006-avaliar-apresentador.mmd', '#006', ['users', 'posts', 'presentation_speakers', 'presentation_ratings', 'events', 'event_participants'],
    {'users': U_BASE, 'posts': ['id', 'author_id', 'type', 'title', 'presentation_id', 'mentioned_event_id', 'event_date', 'event_end_time'],
     'events': ['id', 'author_id', 'title', 'event_date', 'event_end_time']},
    extra_rel=['posts ||--o{ presentation_speakers : "presentation_id (lógico)"'], direcao='LR')
# Cap. 4 — #007 Ranking
der('der-007-ranking.mmd', '#007', ['users', 'profiles', 'presentation_ratings'],
    {'users': U_BASE, 'profiles': ['user_id', 'role', 'avatar']}, direcao='LR')
# Cap. 5 — #008 Dashboards (2 partes)
der('der-008a-dashboards-conteudo.mmd', '#008', ['users', 'posts', 'post_likes', 'post_comments', 'content_shares', 'events', 'event_participants'],
    {'users': ['id', 'name', 'status'], 'posts': ['id', 'author_id', 'type', 'title', 'created_at'],
     'events': ['id', 'author_id', 'title', 'event_date', 'event_end_time', 'created_at']})
der('der-008b-dashboards-avaliacoes.mmd', '#008', ['users', 'events', 'posts', 'event_ratings', 'presentation_ratings', 'reports'],
    {'users': ['id', 'name', 'account_type', 'status', 'created_at'], 'events': ['id', 'author_id', 'title'],
     'posts': ['id', 'author_id', 'title'], 'reports': ['id', 'status', 'created_at']}, direcao='LR')
# Cap. 6 — #013 Analisar Denúncias
der('der-013-denuncias.mmd', '#013', ['users', 'reports', 'admin_actions', 'notifications'],
    {'users': U_BASE + ['deactivated_at', 'deactivated_by', 'deactivation_reason']})
print('ok')
