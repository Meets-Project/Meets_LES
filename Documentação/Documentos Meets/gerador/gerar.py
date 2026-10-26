"""Gera os documentos Word do Meets (Visão, Atividades do Negócio, Requisitos, Casos de Uso
e Modelagem). Requer python-docx, Pillow, LibreOffice (soffice) e pdftotext.

    cd "Documentação/Documentos Meets/gerador" && python3 gerar.py
"""
import os
import sys

from meetsdoc import DOCS, MeetsDoc
from dados import RF, RNF, RN, rfs_do_caso, rns_do_caso, RN_POR_ID
from casos_de_uso import UC


def saida(nome):
    return os.path.join(DOCS, nome)


# ---------------------------------------------------------------- Visão
def visao():
    d = MeetsDoc('Documento de Visão', saida('Documento Visão Meets.docx'))
    d.indice()
    d.h1('Objetivo')
    d.p('O projeto **Meets** tem como objetivo disponibilizar uma aplicação social multiplataforma para a divulgação e participação em eventos, a publicação de conteúdos e a interação entre usuários e apresentadores. A solução centraliza em um único ambiente a criação de posts e apresentações, o gerenciamento de eventos presenciais, a avaliação gamificada de apresentadores com ranking, dashboards analíticos e ferramentas de moderação administrativa.')

    d.h1('Necessidade do Negócio')
    d.p('**Perfil do Cliente / Histórico:** a solução atende comunidades acadêmicas, corporativas e grupos sociais que organizam com frequência encontros, palestras, workshops e compartilhamento de conhecimento.')
    d.p('**Situação Atual (como é feito hoje):** a organização de eventos e a divulgação de conteúdos ocorrem de forma informal e fragmentada, com convites pessoa a pessoa, grupos de mensagens instantâneas e planilhas dispersas. Isso causa perda de dados, falta de histórico, ausência de métricas de engajamento e dificuldade para avaliar a qualidade dos eventos e dos apresentadores.')
    d.p('**Solução Proposta:** o Meets substitui essa informalidade por um ecossistema digital integrado e persistente. A comunidade encontra e interage com eventos, acompanha um feed, avalia os apresentadores por atributos, consulta o ranking e acompanha estatísticas em dashboards; a moderação recebe e trata denúncias.')

    d.h1('Descrição do Escopo')
    d.h2('Módulos e Funcionalidades Inclusas no Escopo')
    d.p('O produto é composto pelos módulos e casos de uso abaixo (especificados no documento "Casos de Uso Meets"):')
    tipo = {u['id']: u['tipo'] for u in UC}
    nome = {u['id']: u['nome'] for u in UC}

    def item(uc, texto):
        return f'{uc} – {nome[uc]} ({tipo[uc]}): {texto}'
    d.bullets([
        ('**Módulo de Conta e Perfil:**', [
            item('#014', 'criação de conta com verificação do e-mail por código.'),
            item('#001', 'acesso por e-mail e senha e saída do aplicativo.'),
            item('#010', 'edição do perfil, visualização e compartilhamento de perfis e desativação da própria conta.'),
            item('#022', 'notificações, modo escuro e troca de senha.'),
        ]),
        ('**Módulo de Conteúdo e Feed:**', [
            item('#002', 'feed com posts, apresentações e eventos visíveis ao usuário.'),
            item('#009', 'criação, edição e exclusão de posts com visibilidade (público, seguidores, selecionados ou link).'),
            item('#003', 'curtir, comentar, compartilhar (com contagem), salvar e favoritar.'),
            item('#020', 'busca de usuários e posts.'),
            item('#021', 'histórico de atividades do usuário.'),
        ]),
        ('**Módulo de Eventos e Participação:**', [
            item('#011', 'criação, edição e exclusão de eventos e apresentações vinculadas, e calendário.'),
            item('#004', 'curtir, comentar, compartilhar, salvar e marcar/cancelar presença.'),
        ]),
        ('**Módulo de Rede e Comunicação:**', [
            item('#017', 'seguir e deixar de seguir usuários.'),
            item('#018', 'conversa privada entre dois usuários.'),
            item('#019', 'central de notificações.'),
        ]),
        ('**Módulo de Avaliação e Gamificação:**', [
            item('#005', 'avaliação de eventos encerrados com 1 a 5 estrelas e comentário.'),
            item('#006', 'avaliação do apresentador com estrelas e seis atributos de 0 a 99 (clareza, domínio do conteúdo, engajamento, storytelling, gestão de tempo e recursos visuais).'),
            item('#007', 'ranking público pela pontuação geral, com filtro de período.'),
            item('#015', 'automação que avisa os participantes quando um evento ou apresentação termina.'),
        ]),
        ('**Módulo Analítico (Dashboards):**', [
            (item('#008', 'indicadores com filtro de período; o usuário vê os próprios dados e o administrador também a visão da plataforma:'), [
                '**Posts:** volume, curtidas, comentários, compartilhamentos e mais engajados;',
                '**Eventos:** volume, realizados, participantes e satisfação;',
                '**Avaliações:** distribuição das notas e evolução mensal;',
                '**Apresentadores:** médias por atributo e destaques.',
            ]),
        ]),
        ('**Módulo de Administração e Moderação:**', [
            item('#012', 'gestão de contas pelo administrador (criar, editar, promover, desativar e reativar), com registro das ações.'),
            item('#016', 'denúncia de posts, apresentações, eventos e usuários.'),
            item('#013', 'fila de moderação com decisão e ação (remover conteúdo, advertir ou desativar a conta).'),
            item('#023', 'remoção direta de post ou evento pelo administrador.'),
        ]),
    ])
    d.h2('Itens Fora do Escopo')
    d.p('Para delimitar a versão atual, não estão incluídos:')
    d.bullets([
        'Pagamentos, venda de ingressos, monetização ou marketplace;',
        'Salas ao vivo, videoconferência ou transmissão de áudio e vídeo (streaming) — retiradas do escopo pela equipe;',
        'Rascunhos de posts e eventos;',
        'Exclusão definitiva de conta: a conta é sempre desativada e pode ser reativada por um administrador;',
        'Moderação automática por Inteligência Artificial;',
        'Integração com mapas, calendários externos ou notificações push de terceiros (a consulta de CEP é a única integração externa).',
    ])

    d.h1('Equipe')
    d.p('A equipe é composta por alunos do curso de **Análise e Desenvolvimento de Sistemas (ADS)**, responsáveis de forma colaborativa por todas as etapas: requisitos, modelagem UML, desenvolvimento mobile e backend, banco de dados, testes e documentação.')
    d.tabela(['Integrante', 'Formação', 'Papéis e Responsabilidades'], [
        ['Gabriel Silva', 'ADS', 'Engenharia de Requisitos, Modelagem UML, Desenvolvimento Frontend/Mobile e Backend REST.'],
        ['Leonam Candido', 'ADS', 'Análise de Sistemas, Modelagem de Banco de Dados PostgreSQL, Desenvolvimento Mobile e Testes.'],
        ['Matheus Ferrari', 'ADS', 'Especificação de Casos de Uso, Desenvolvimento da API REST em Node.js, Integração e Documentação.'],
        ['Matheus Marinho', 'ADS', 'Arquitetura de Software, Desenvolvimento Frontend React Native/Expo, Testes e Segurança HTTP.'],
        ['Nicolas Carvalho', 'ADS', 'Modelagem Conceitual/Lógica de Dados, Repositórios SQL, API REST e Moderação.'],
        ['Samuel Aranha', 'ADS', 'Desenvolvimento Mobile, Regras de Negócio, Gamificação e Testes Automatizados.'],
    ], [3.8, 2.2, 11.0])

    d.h1('Especificações Técnicas')
    d.p('Arquitetura cliente-servidor: um aplicativo multiplataforma consome uma API REST que acessa um banco relacional.')
    d.bullets([
        '**Aplicativo:** React Native com Expo (Android, iOS e web), React Navigation e AsyncStorage para o token de sessão. A versão web é publicada na Vercel.',
        '**API REST:** Node.js 20+ com Express 5, organizada em camadas — rotas (app.js e routes/), serviços (services/: moderação, pontuação e relógio) e repositórios SQL. Publicada no Render (Dockerfile com Node 22).',
        '**Banco de dados:** PostgreSQL, com migrações SQL versionadas (pasta migrations/) e script de desfazer para cada uma (migrations/rollback/).',
        '**Segurança:** JWT para sessão, bcrypt para senhas, Zod para validação, Helmet e CORS configurável; perfis "usuário" e "administrador".',
        '**Fuso horário:** variável APP_TIMEZONE (padrão America/Sao_Paulo) usada para decidir se um evento já terminou.',
        '**Automação:** rotina na API que roda a cada minuto e gera os lembretes de avaliação (#015).',
        '**E-mail:** Nodemailer (SMTP) para o código de verificação.',
        '**Testes:** Vitest e Supertest com banco em memória pg-mem.',
        '**Fluxo:** Aplicativo → API REST (rotas → serviços → repositórios) → PostgreSQL.',
    ])

    d.h1('Riscos')
    d.tabela(['Risco', 'Prob.', 'Impacto', 'Nível', 'Plano de Contingência / Mitigação'], [
        ['Falha de conexão com o PostgreSQL', 'Média', 'Alto', 'Alto', 'Rota /health, logs de erro, migrações automáticas na inicialização e rollback por migração.'],
        ['Token JWT inválido ou expirado', 'Média', 'Alto', 'Alto', 'Tratar 401/403 no aplicativo, voltar ao login e manter JWT_SECRET em variável de ambiente.'],
        ['Inconsistência entre aplicativo, API e documentação', 'Média', 'Alto', 'Alto', 'Esquemas Zod, testes automatizados a cada alteração e documentação gerada a partir de dados conferidos com o código.'],
        ['Servidor fora do fuso de Brasília', 'Média', 'Médio', 'Médio', 'Cálculo de "evento realizado" com APP_TIMEZONE, independente do relógio do servidor.'],
        ['Conteúdo abusivo na comunidade', 'Média', 'Alto', 'Alto', 'Denúncias, fila de moderação, desativação de contas e registro de ações administrativas.'],
        ['Imagem acima do limite', 'Média', 'Médio', 'Médio', 'Corte e qualidade reduzida na escolha da imagem, validação de tamanho na API e limite de payload de 20 MB.'],
        ['Hospedagem gratuita suspensa (Render)', 'Média', 'Médio', 'Médio', 'O aplicativo chama /health ao abrir para acordar o servidor; a API também pode ser executada localmente.'],
    ], [4.0, 1.4, 1.6, 1.4, 8.6])

    d.h1('Cronograma de Marcos Resumido')
    d.tabela(['Marco do Projeto', 'Data / Período'], [
        ['Início e definição do escopo', '03/08/2026'],
        ['Levantamento e especificação de requisitos', '04/08/2026 a 08/08/2026'],
        ['Modelagem UML e modelo de banco de dados', '09/08/2026 a 12/08/2026'],
        ['Implementação da aplicação mobile e API REST', '13/08/2026 a 20/08/2026'],
        ['Persistência PostgreSQL e testes automatizados', '17/08/2026 a 21/08/2026'],
        ['Documentação e diagramas', '22/08/2026 a 24/08/2026'],
        ['Entrega parcial e apresentação', '07/09/2026 a 14/09/2026'],
        ['Auditoria, decisões de escopo e alinhamento documentação × código', '10/2026'],
    ], [11.0, 6.0])

    d.h1('Orçamento Resumido')
    d.p('Estimativa acadêmica fictícia para fins de planejamento, conforme permitido pela disciplina:')
    d.tabela(['Categoria de Custo / Item', 'Estimativa (R$)'], [
        ['Hardware e equipamentos (infraestrutura pré-existente)', 'R$ 0,00'],
        ['Licenças de software (ferramentas open source)', 'R$ 0,00'],
        ['Infraestrutura e serviços em nuvem', 'R$ 600,00'],
        ['Esforço de desenvolvimento, testes e documentação (6 alunos ADS)', 'R$ 15.000,00'],
        ['Margem de contingência para riscos (10%)', 'R$ 1.560,00'],
        ['**Total Estimado do Projeto**', '**R$ 17.160,00**'],
    ], [12.0, 5.0])
    return d


# ---------------------------------------------------------------- Atividades
ATIVIDADES = [
    ('Atividade 1 - Organização e Realização de Evento', 'atividade-negocio-1-evento.png',
     'Ciclo de vida de um evento, da criação à avaliação dos apresentadores e atualização do ranking.', [
        '**Criação do evento:** o Organizador (Usuário) preenche título, descrição, imagem, data, horário de início e de fim, local (CEP, UF e número) e visibilidade, e pode publicar apresentações vinculadas ao evento com os apresentadores. O sistema valida e publica. *Quebra de fluxo:* campos obrigatórios em falta, data passada, fim antes do início ou UF diferente do perfil — o sistema destaca os campos e não publica.',
        '**Divulgação:** o evento aparece no feed e no calendário de quem pode vê-lo; os participantes curtem, comentam, compartilham e salvam.',
        '**Confirmação de presença:** o Participante toca em "Marcar presença"; o sistema registra e avisa o organizador. Tocar de novo cancela a presença.',
        '**Realização:** o evento acontece. Quando a data e o horário de fim passam, o sistema passa a considerá-lo "Realizado" (situação calculada no fuso de Brasília).',
        '**Lembrete automático:** a cada minuto o sistema identifica eventos e apresentações encerrados e avisa cada participante para avaliar (caso de uso de condução #015).',
        '**Avaliação:** o Participante avalia o evento (1 a 5 estrelas e comentário) e o apresentador (estrelas e seis atributos de 0 a 99), de forma pública ou anônima.',
        '**Ranking:** o sistema recalcula a pontuação geral do apresentador (média dos atributos) e o ranking.',
    ]),
    ('Atividade 2 - Publicação de Conteúdo e Interação na Comunidade', 'atividade-negocio-2-conteudo.png',
     'Dinâmica diária de compartilhamento de informações entre os membros.', [
        '**Publicação:** o Usuário escreve o post, anexa imagem (com corte) e escolhe a visibilidade: público, seguidores, pessoas selecionadas ou somente com link. *Quebra de fluxo:* texto vazio ou acima do limite — o sistema bloqueia o envio.',
        '**Distribuição:** o sistema coloca o post no feed das pessoas autorizadas.',
        '**Interação:** outros usuários curtem (alternância), comentam, compartilham (o sistema registra e conta), salvam ou favoritam.',
        '**Manutenção pelo autor:** o autor edita ou exclui o post; o sistema confere a autoria e registra no histórico.',
        '**Denúncia:** se o conteúdo for impróprio, qualquer usuário pode denunciá-lo, iniciando a Atividade 3.',
    ]),
    ('Atividade 3 - Moderação e Controle de Qualidade', 'atividade-negocio-3-moderacao.png',
     'Garante a segurança e a integridade do conteúdo da plataforma.', [
        '**Denúncia:** o Usuário escolhe "Denunciar" em um post, apresentação, evento ou perfil, seleciona o motivo e descreve. O sistema impede denunciar o próprio conteúdo ou repetir uma denúncia aberta, registra como "Pendente" e notifica os administradores.',
        '**Início da análise:** o Administrador abre a fila e inicia a análise; a denúncia passa a "Em análise".',
        '**Decisão — improcedente:** o conteúdo permanece e os denunciantes são avisados.',
        '**Decisão — procedente:** o Administrador escolhe a ação: remover o conteúdo, advertir o autor ou desativar a conta do autor. O sistema executa, avisa o autor e encerra as demais denúncias abertas sobre o mesmo alvo.',
        '**Auditoria:** o sistema registra administrador, ação, alvo, data e justificativa.',
        '**Reativação:** uma conta desativada só volta a funcionar se um administrador a reativar.',
    ]),
    ('Atividade 4 - Análise do Desempenho da Comunidade', 'atividade-negocio-4-analise.png',
     'Acompanhamento de uso, engajamento e qualidade das apresentações.', [
        '**Dashboards:** o Usuário abre o dashboard e vê os indicadores do próprio conteúdo; o Administrador pode alternar para a visão da plataforma. São quatro painéis: posts, eventos, avaliações e apresentadores.',
        '**Período:** no dashboard o usuário escolhe tudo, 7, 30 ou 90 dias; o sistema recalcula os indicadores.',
        '**Ranking:** o usuário consulta o ranking; o sistema ordena os apresentadores pela pontuação geral e mostra o pódio.',
        '**Detalhe do apresentador:** ao tocar em um apresentador, o sistema mostra as médias por atributo e as avaliações recebidas.',
    ]),
]


def atividades():
    d = MeetsDoc('Atividades do Negócio', saida('Atividades do Negócio Meets.docx'))
    d.indice()
    d.h1('Objetivo')
    d.p('Descrever as principais atividades de negócio sustentadas pelo Meets, com a sequência de interações entre os atores — Organizador/Apresentador, Participante, Administrador e o próprio Sistema — e o diagrama de atividades UML de cada uma.')
    d.h1('Atividades do Negócio')
    d.p('Para substituir a informalidade na organização de eventos e no compartilhamento de conteúdos, foram identificadas quatro atividades principais:')
    for i, (titulo, img, intro, passos) in enumerate(ATIVIDADES, 1):
        if i > 1:
            d.page_break()
        d.h2(titulo)
        d.p(intro)
        d.numerada(passos)
        d.page_break()
        d.h3('Diagrama de Atividades')
        d.imagem(img, legenda=f'Figura {i} – {titulo}', altura_max_cm=19.5)
    return d


# ---------------------------------------------------------------- Requisitos
def requisitos():
    d = MeetsDoc('Documento de Requisitos', saida('Requisitos_Sistema_Meets.docx'))
    d.indice()
    d.h1('Objetivo')
    d.p('Definir de forma verificável as funções, restrições e regras de negócio do Meets. Cada requisito foi conferido com a implementação (API em Código/backend e aplicativo em Código/snack) e aponta o caso de uso que o realiza.')
    d.h1('Técnicas Utilizadas na Elucidação de Requisitos')
    d.bullets([
        'Reuniões da equipe e documento de decisões de escopo;',
        'Análise do código-fonte, das telas do aplicativo e dos endpoints REST;',
        'Inspeção do esquema PostgreSQL e das migrações;',
        'Execução dos testes automatizados como verificação das regras;',
        'Validação cruzada entre funcionalidades implementadas e documentação exigida pela disciplina.',
    ])
    d.h1('Requisitos Funcionais')
    grupo = None
    linhas = []
    for (rid, g, nome, prio, esp, rns, uc) in RF:
        if g != grupo:
            linhas.append(g)  # linha de grupo
            grupo = g
        linhas.append([rid, nome, prio, esp, uc])
    d.tabela(['ID', 'Requisito', 'Prior.', 'Especificação', 'Caso de uso'], linhas, [1.4, 3.2, 1.3, 9.3, 1.8])
    d.h1('Requisitos Não Funcionais')
    d.tabela(['ID', 'Grupo', 'Prior.', 'Descrição'], [list(r) for r in RNF], [1.6, 2.8, 1.3, 11.3])
    d.h1('Regras de Negócio')
    d.tabela(['ID', 'Regra'], [list(r) for r in RN], [1.6, 15.4])
    d.page_break()
    d.h1('Matriz RF x RN')
    d.p('Relação entre cada requisito funcional e as regras de negócio que o restringem ("X" indica relação).')
    rn_ids = [r[0] for r in RN]
    metade = (len(rn_ids) + 1) // 2
    for parte, ids in enumerate((rn_ids[:metade], rn_ids[metade:]), 1):
        if parte == 2:
            d.page_break()
        cab = ['RF'] + [i.replace('RN', '') for i in ids]
        linhas = []
        for r in RF:
            linhas.append([r[0]] + ['X' if i in r[5] else '' for i in ids])
        d.p(f'**Parte {parte}: RN{ids[0][2:]} a RN{ids[-1][2:]}** (colunas = número da RN)', align='left')
        larg = [1.5] + [15.5 / len(ids)] * len(ids)
        d.tabela(cab, linhas, larg, fonte=7)
    d.page_break()
    d.h1('Rastreabilidade RF x Caso de Uso')
    ucs = {}
    for r in RF:
        ucs.setdefault(r[6], []).append(r[0])
    nomes = {u['id']: u['nome'] for u in UC}
    d.tabela(['Caso de uso', 'Requisitos funcionais'],
             [[f'{k} – {nomes[k]}', ', '.join(v)] for k, v in sorted(ucs.items())], [8.0, 9.0])
    return d


# ---------------------------------------------------------------- Casos de uso
def casos_de_uso():
    d = MeetsDoc('Especificação de Casos de Uso', saida('Casos de Uso Meets.docx'))
    d.indice()
    d.h1('Objetivo')
    d.p('Especificar os casos de uso do Meets: atores, permissões, fluxos e regras, em correspondência com a implementação.')
    d.p('O Meets é uma plataforma para divulgação e participação em eventos, publicação de conteúdos e interação entre usuários e apresentadores. Os usuários publicam posts, apresentações e eventos, interagem com curtidas, comentários, compartilhamentos e presença, avaliam eventos (1 a 5 estrelas) e apresentadores (estrelas e seis atributos de 0 a 99), consultam ranking e dashboards. Administradores gerenciam contas e tratam denúncias.')
    d.p('Os casos de uso são classificados em três tipos: **Básico** (cadastro, consulta e manutenção de dados e interações simples), **Análise** (o sistema processa dados para gerar informação ou apoiar decisão) e **Condução** (automação conduzida pelo próprio sistema, disparada por tempo ou evento).')
    d.p('Todas as funcionalidades, exceto cadastro e login, exigem usuário autenticado.')

    d.h1('Atores do Sistema')
    d.h2('Visitante')
    d.p('**Descrição:** pessoa que ainda não está autenticada. **Permissões:** cadastrar-se (#014), fazer login (#001) e abrir conteúdo público recebido por link.')
    d.h2('Usuário')
    d.p('**Descrição:** pessoa cadastrada que publica, participa de eventos, interage e avalia. Atua como organizador, apresentador ou participante. **Perfil técnico:** conhecimentos básicos de aplicativos.')
    d.p('**Permissões:** casos #002 a #011 e #016 a #022 — feed, posts, eventos e apresentações próprios, interações, presença, avaliações, ranking, dashboard dos próprios dados, perfil, seguir, conversar, notificações, busca, histórico, configurações e desativação da própria conta.')
    d.h2('Administrador')
    d.p('**Descrição:** responsável pela gestão e moderação. É uma **especialização do Usuário** e herda todas as permissões dele. O primeiro administrador é definido pela equipe com o comando "npm run make-admin -- e-mail".')
    d.p('**Permissões adicionais:** manter usuários (#012), analisar denúncias (#013), remover conteúdo impróprio (#023) e ver o dashboard da plataforma (#008).')
    d.h2('Agendador do Sistema')
    d.p('**Descrição:** ator não humano — rotina da API executada a cada minuto. **Responsabilidade:** conduzir o lembrete de avaliação pendente (#015).')

    d.h1('Diagrama de Casos de Uso')
    d.p('No diagrama, as cores indicam o tipo: cinza = Básico, azul = Análise e verde = Condução (automação). O Administrador é especialização do Usuário (seta de generalização).')
    d.imagem('casos-de-uso-geral.png', largura_cm=16, legenda='Figura 1 – Diagrama geral de casos de uso', altura_max_cm=21)
    d.h2('Lista de Casos de Uso')
    d.tabela(['Caso de uso', 'Tipo', 'Ator', 'Requisitos'],
             [[f"{u['id']} – {u['nome']}", u['tipo'], u['atores'], ', '.join(rfs_do_caso(u['id'])) or '—'] for u in sorted(UC, key=lambda x: x['id'])],
             [6.6, 2.0, 4.6, 3.8])

    d.h1('Especificação dos Casos de Uso')
    figura = 2
    for n, u in enumerate(sorted(UC, key=lambda x: x['id'])):
        if n:
            d.page_break()
        d.h2(f"Caso de uso {u['id']} – {u['nome']}")
        d.p(f"**Descrição:** {u['descricao']}")
        d.p(f"**Tipo:** {u['tipo']}", space_after=2)
        d.p(f"**Atores que iniciam:** {u['atores']}", space_after=2)
        rfs = rfs_do_caso(u['id'])
        if rfs:
            d.p(f"**Requisitos:** {', '.join(rfs)}  ·  **Regras de negócio:** {', '.join(rns_do_caso(u['id']))}", space_after=2)
        for rot, chave in (('Pré-condições:', 'pre'), ('Pós-condições:', 'pos'), ('Entradas:', 'entradas'), ('Saídas:', 'saidas')):
            d.rotulo(rot)
            d.bullets(u[chave])
        d.rotulo('Fluxo principal:')
        d.numerada(u['fluxo'])
        for i, (tit, passos) in enumerate(u['alternativos'], 1):
            d.rotulo(f'Fluxo alternativo {i}: {tit}')
            d.numerada(passos)
        d.rotulo('Protótipo de interface:')
        d.bullets(u['prototipo'])
        for img, leg in u.get('diagramas', []):
            d.imagem(img, largura_cm=16, legenda=f'Figura {figura} – {leg}', altura_max_cm=20)
            figura += 1
    return d


# ---------------------------------------------------------------- Modelagem
def modelagem():
    d = MeetsDoc('Modelagem do Sistema', saida('Modelagem do Sistema Meets.docx'))
    d.indice()
    d.h1('Objetivo')
    d.p('Reunir os modelos estruturais e comportamentais do Meets — MER, DER, diagramas de classe e de estado — gerados a partir do banco de dados migrado e do código. As fontes editáveis (Mermaid e Graphviz) ficam em "diagramas_LES/fontes".')
    d.h1('Modelo Entidade-Relacionamento (MER)', quebra=True)
    d.p('Modelo conceitual em notação de Chen. A Apresentação é uma especialização de Post; as avaliações são relacionamentos N:N entre Usuário e Evento e entre Usuário e Apresentação, com atributos próprios. O Perfil e a Configuração são 1:1 com o Usuário.')
    d.imagem('mer-conceitual.png', largura_cm=17, legenda='Figura 1 – MER conceitual', altura_max_cm=18.5)
    d.h1('Diagrama Entidade-Relacionamento (DER)', quebra=True)
    d.p('Modelo lógico do PostgreSQL, dividido em três partes. Todas as chaves primárias são UUID. Contas não são excluídas (situação "deactivated"), por isso as tabelas de conteúdo mantêm as chaves estrangeiras para users.')
    for i, (img, leg) in enumerate([
        ('der-1-usuarios-rede-comunicacao.png', 'DER – Usuários, rede e comunicação'),
        ('der-2-conteudo-interacoes.png', 'DER – Conteúdo e interações'),
        ('der-3-avaliacao-moderacao.png', 'DER – Avaliação e moderação'),
    ], 2):
        d.imagem(img, largura_cm=17, legenda=f'Figura {i} – {leg}', altura_max_cm=18.5)
    d.h1('Diagramas de Classe', quebra=True)
    d.p('Classes de domínio com os atributos persistidos e as operações expostas pela API/repositórios.')
    fig = 5
    for img, leg in [
        ('classe-usuarios-conteudo.png', 'Classes – Usuários e conteúdo'),
        ('classe-interacoes-avaliacoes.png', 'Classes – Interações e avaliações'),
        ('classe-avaliacao-ranking.png', 'Classes – Avaliação e ranking'),
        ('classe-dashboards-administracao.png', 'Classes – Dashboards e administração'),
    ]:
        d.imagem(img, largura_cm=17, legenda=f'Figura {fig} – {leg}', altura_max_cm=18.5)
        fig += 1
    d.h1('Diagramas de Estado', quebra=True)
    for img, leg in [
        ('estado-usuario.png', 'Estado – Conta do usuário'),
        ('estado-autenticacao.png', 'Estado – Autenticação'),
        ('estado-perfil.png', 'Estado – Perfil'),
        ('estado-post.png', 'Estado – Post'),
        ('estado-evento.png', 'Estado – Evento'),
        ('estado-avaliacao.png', 'Estado – Processo de avaliação'),
        ('estado-denuncia.png', 'Estado – Denúncia'),
    ]:
        d.imagem(img, largura_cm=15, legenda=f'Figura {fig} – {leg}', altura_max_cm=11)
        fig += 1
    d.h1('Diagramas de Sequência')
    d.p('Os diagramas de sequência acompanham as especificações dos casos de uso #005, #006, #013 e #015 no documento "Casos de Uso Meets".')
    return d


DOCUMENTOS = {'visao': visao, 'atividades': atividades, 'requisitos': requisitos, 'casos': casos_de_uso, 'modelagem': modelagem}

if __name__ == '__main__':
    alvos = sys.argv[1:] or list(DOCUMENTOS)
    for alvo in alvos:
        doc = DOCUMENTOS[alvo]()
        faltando = doc.salvar()
        print(f'{alvo}: {os.path.basename(doc.saida)}' + (f'  (sem página no índice: {faltando})' if faltando else ''))
