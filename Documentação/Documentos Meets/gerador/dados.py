"""Requisitos e regras do Meets, conferidos com o código (Código/backend e Código/snack).

Cada RF indica as regras de negócio (RN) que o restringem e o caso de uso que o realiza.
Ao mudar o código, ajuste aqui e rode gerar.py para manter documentação e programação iguais.
"""

# (id, grupo, nome, prioridade, especificação, [RNs], caso de uso)
RF = [
    # Conta e acesso
    ('RF01', 'Conta e acesso', 'Cadastrar usuário', 'Alta',
     'O sistema deve permitir que um visitante crie uma conta informando nome, e-mail e senha. O cadastro cria o perfil e as configurações do usuário e envia um código de verificação para o e-mail.',
     ['RN02', 'RN03', 'RN04', 'RN08', 'RN26'], '#014'),
    ('RF02', 'Conta e acesso', 'Verificar e-mail', 'Alta',
     'O sistema deve validar o código de verificação enviado por e-mail, permitir o reenvio de um novo código e liberar o uso do aplicativo somente após a verificação.',
     ['RN04'], '#014'),
    ('RF03', 'Conta e acesso', 'Autenticar usuário', 'Alta',
     'O sistema deve autenticar o usuário por e-mail e senha e emitir um token JWT de sessão.',
     ['RN01', 'RN03', 'RN05'], '#001'),
    ('RF04', 'Conta e acesso', 'Encerrar sessão', 'Média',
     'O usuário deve poder sair do aplicativo; o token salvo no dispositivo é apagado.',
     ['RN01'], '#001'),
    ('RF05', 'Conta e acesso', 'Alterar senha', 'Média',
     'O usuário autenticado deve poder trocar a senha informando a senha atual e a nova senha.',
     ['RN03'], '#022'),
    ('RF06', 'Conta e acesso', 'Desativar a própria conta', 'Média',
     'O usuário deve poder desativar a própria conta confirmando a senha. A conta não é excluída: login e sessões são bloqueados e o conteúdo fica oculto até um administrador reativá-la.',
     ['RN05', 'RN06', 'RN07'], '#010'),
    # Perfil e rede
    ('RF07', 'Perfil e rede', 'Manter perfil', 'Alta',
     'O usuário deve poder consultar e editar o seu perfil: nome, cargo, cidade/UF, número, foto e biografia.',
     ['RN08', 'RN26'], '#010'),
    ('RF08', 'Perfil e rede', 'Visualizar e compartilhar perfil', 'Média',
     'O usuário deve poder abrir o perfil público de outro usuário, com publicações visíveis e o desempenho como apresentador, e compartilhar perfis por link.',
     ['RN05', 'RN09'], '#010'),
    ('RF09', 'Perfil e rede', 'Seguir usuários', 'Média',
     'O usuário deve poder seguir e deixar de seguir outro usuário e consultar quem segue e quem o segue.',
     ['RN05', 'RN11'], '#017'),
    ('RF10', 'Perfil e rede', 'Conversar', 'Baixa',
     'O usuário deve poder abrir uma conversa direta com outro usuário, enviar mensagens e marcá-las como lidas.',
     ['RN26', 'RN27'], '#018'),
    # Conteúdo
    ('RF11', 'Conteúdo', 'Visualizar feed', 'Alta',
     'O sistema deve listar, do mais recente para o mais antigo, os posts, apresentações e eventos que o usuário tem permissão de ver, com autor, contadores de curtidas, comentários e compartilhamentos.',
     ['RN01', 'RN05', 'RN09'], '#002'),
    ('RF12', 'Conteúdo', 'Publicar post', 'Alta',
     'O usuário deve poder publicar um post com texto, título e imagem opcionais e escolher a visibilidade.',
     ['RN09', 'RN26'], '#009'),
    ('RF13', 'Conteúdo', 'Editar e excluir post', 'Alta',
     'O autor deve poder editar o texto, a imagem e a visibilidade do seu post e excluí-lo.',
     ['RN10'], '#009'),
    ('RF14', 'Conteúdo', 'Criar apresentação', 'Alta',
     'O usuário deve poder publicar uma apresentação (post do tipo apresentação) com data, horário de início e fim, local, evento vinculado e apresentadores vinculados.',
     ['RN09', 'RN12', 'RN13', 'RN16'], '#011'),
    ('RF15', 'Conteúdo', 'Definir visibilidade', 'Alta',
     'Posts, apresentações e eventos devem ter visibilidade pública, somente seguidores, pessoas selecionadas ou somente quem tiver o link.',
     ['RN09'], '#009'),
    ('RF16', 'Conteúdo', 'Curtir', 'Média',
     'O usuário deve poder curtir e descurtir posts e eventos.',
     ['RN09', 'RN11'], '#003'),
    ('RF17', 'Conteúdo', 'Comentar', 'Média',
     'O usuário deve poder comentar posts e eventos e excluir os próprios comentários.',
     ['RN09', 'RN10', 'RN26'], '#003'),
    ('RF18', 'Conteúdo', 'Compartilhar', 'Média',
     'O usuário deve poder compartilhar posts, apresentações, eventos e perfis por link; o sistema registra cada compartilhamento e exibe o total.',
     ['RN09'], '#003'),
    ('RF19', 'Conteúdo', 'Salvar e favoritar', 'Média',
     'O usuário deve poder salvar posts e eventos para ver depois e favoritar posts, consultando cada lista separadamente.',
     ['RN11'], '#003'),
    # Eventos
    ('RF20', 'Eventos', 'Criar evento', 'Alta',
     'O usuário deve poder criar um evento com título, descrição, imagem, data, horário de início e de fim, local (CEP, UF e número) e visibilidade. O organizador fica registrado como participante anfitrião.',
     ['RN09', 'RN12', 'RN13', 'RN26'], '#011'),
    ('RF21', 'Eventos', 'Editar e excluir evento', 'Alta',
     'O organizador deve poder editar e excluir os seus eventos.',
     ['RN10', 'RN12'], '#011'),
    ('RF22', 'Eventos', 'Marcar presença', 'Alta',
     'O usuário deve poder confirmar e cancelar a presença em um evento e consultar os participantes; o organizador é avisado de novas confirmações.',
     ['RN09', 'RN11', 'RN20'], '#004'),
    ('RF23', 'Eventos', 'Consultar calendário', 'Média',
     'O usuário deve poder consultar em um calendário os eventos que organiza ou dos quais participa.',
     ['RN14', 'RN25'], '#011'),
    # Avaliação e análise
    ('RF24', 'Avaliação e análise', 'Avaliar evento', 'Alta',
     'O participante deve poder avaliar um evento encerrado com 1 a 5 estrelas e comentário opcional, de forma pública ou anônima.',
     ['RN14', 'RN15', 'RN17'], '#005'),
    ('RF25', 'Avaliação e análise', 'Avaliar apresentador', 'Alta',
     'O participante deve poder avaliar o apresentador de uma apresentação encerrada com 1 a 5 estrelas e notas de 0 a 99 em seis atributos, com comentário opcional e opção de anonimato.',
     ['RN14', 'RN16', 'RN17', 'RN18'], '#006'),
    ('RF26', 'Avaliação e análise', 'Lembrar avaliação pendente', 'Média',
     'O sistema deve, automaticamente, avisar cada participante quando um evento ou apresentação de que participou terminar, convidando-o a avaliar.',
     ['RN14', 'RN19', 'RN20', 'RN25'], '#015'),
    ('RF27', 'Avaliação e análise', 'Visualizar ranking de apresentadores', 'Alta',
     'O sistema deve exibir o ranking dos apresentadores pela pontuação geral, com filtro de período (desde o início, 90 ou 30 dias), e abrir o perfil do apresentador.',
     ['RN18', 'RN05'], '#007'),
    ('RF28', 'Avaliação e análise', 'Visualizar dashboards', 'Alta',
     'O sistema deve exibir indicadores de posts, eventos, avaliações e apresentadores, com filtro de período. O usuário vê os dados do próprio conteúdo; o administrador também vê a visão geral da plataforma.',
     ['RN24'], '#008'),
    # Comunicação e utilidades
    ('RF29', 'Comunicação e utilidades', 'Visualizar notificações', 'Média',
     'O sistema deve listar as notificações do usuário, abrir o conteúdo relacionado e permitir marcá-las como lidas.',
     ['RN20'], '#019'),
    ('RF30', 'Comunicação e utilidades', 'Pesquisar', 'Média',
     'O sistema deve pesquisar usuários (nome ou cargo) e posts (conteúdo) respeitando a visibilidade.',
     ['RN05', 'RN09'], '#020'),
    ('RF31', 'Comunicação e utilidades', 'Consultar histórico', 'Baixa',
     'O sistema deve registrar e exibir as atividades do usuário (criações, exclusões, presenças, denúncias).',
     ['RN01'], '#021'),
    ('RF32', 'Comunicação e utilidades', 'Gerenciar configurações', 'Média',
     'O usuário deve poder ligar ou desligar notificações e o modo escuro.',
     ['RN20'], '#022'),
    # Administração e moderação
    ('RF33', 'Administração e moderação', 'Manter usuários', 'Alta',
     'O administrador deve poder listar e filtrar usuários, criar, editar, promover ou rebaixar administradores, desativar e reativar contas e consultar o histórico de ações sobre cada conta.',
     ['RN02', 'RN05', 'RN06', 'RN07', 'RN23'], '#012'),
    ('RF34', 'Administração e moderação', 'Denunciar', 'Alta',
     'O usuário deve poder denunciar um post, apresentação, evento ou usuário, escolhendo o motivo e descrevendo o problema; os administradores são notificados.',
     ['RN21'], '#016'),
    ('RF35', 'Administração e moderação', 'Analisar denúncias', 'Alta',
     'O administrador deve poder consultar a fila de denúncias, iniciar a análise e decidir: improcedente ou procedente com uma ação (remover o conteúdo, advertir o autor ou desativar a conta do autor).',
     ['RN05', 'RN21', 'RN22', 'RN23'], '#013'),
    ('RF36', 'Administração e moderação', 'Remover conteúdo impróprio', 'Alta',
     'O administrador deve poder excluir qualquer post ou evento, informando o motivo; o autor é avisado.',
     ['RN10', 'RN20', 'RN23'], '#023'),
]

# (id, grupo, prioridade, descrição)
RNF = [
    ('RNF01', 'Segurança', 'Alta', 'Senhas armazenadas com hash bcrypt (custo 12); rotas protegidas exigem token JWT válido; a chave JWT_SECRET vem de variável de ambiente.'),
    ('RNF02', 'Segurança HTTP', 'Média', 'A API usa Helmet e CORS com origens configuráveis; textos enviados por e-mail são escapados.'),
    ('RNF03', 'Persistência', 'Alta', 'Os dados de negócio ficam no PostgreSQL; o dispositivo guarda apenas o token de sessão (AsyncStorage).'),
    ('RNF04', 'Validação', 'Alta', 'Toda entrada da API é validada com esquemas Zod; dados inválidos retornam 400 com os detalhes, e falta de permissão retorna 401/403.'),
    ('RNF05', 'Desempenho', 'Média', 'Listas de feed, busca, notificações e histórico são limitadas em quantidade e apoiadas por índices.'),
    ('RNF06', 'Usabilidade', 'Alta', 'As telas exibem estados de carregamento, erro e lista vazia, e ações destrutivas pedem confirmação.'),
    ('RNF07', 'Portabilidade', 'Média', 'O aplicativo usa React Native/Expo e funciona em Android, iOS e web.'),
    ('RNF08', 'Manutenibilidade', 'Alta', 'O backend é organizado em camadas: rotas (app.js e routes/), serviços (services/) e repositórios SQL; o aplicativo separa telas, componentes e serviços.'),
    ('RNF09', 'Testabilidade', 'Média', 'A API possui testes automatizados de integração (Vitest + Supertest) que rodam com banco em memória (pg-mem), sem depender de um PostgreSQL externo.'),
    ('RNF10', 'Fuso horário', 'Alta', 'Datas e horários de eventos são interpretados no fuso do Meets (APP_TIMEZONE, padrão America/Sao_Paulo), independente do fuso do servidor.'),
    ('RNF11', 'Auditoria', 'Alta', 'Ações administrativas ficam registradas de forma permanente, com autor, alvo, data e observação.'),
    ('RNF12', 'Reversibilidade', 'Média', 'Cada alteração de banco é uma migração versionada com script de desfazer (npm run rollback -- <migração>).'),
]

# (id, regra)
RN = [
    ('RN01', 'Todas as funções exigem usuário autenticado, exceto cadastro, login e abertura de conteúdo público por link.'),
    ('RN02', 'O e-mail é único no sistema (sem diferenciar maiúsculas e minúsculas) e é o único identificador de login.'),
    ('RN03', 'A senha deve ter entre 6 e 128 caracteres.'),
    ('RN04', 'O cadastro envia um código de verificação com validade limitada; o aplicativo só libera o uso após o e-mail ser verificado.'),
    ('RN05', 'Conta desativada não faz login, tem as sessões recusadas e o seu conteúdo deixa de aparecer em feed, busca, comentários, conexões e ranking. Os dados são mantidos: não existe exclusão definitiva de conta.'),
    ('RN06', 'Somente um administrador pode reativar uma conta desativada.'),
    ('RN07', 'Sempre deve existir ao menos um administrador ativo: o único administrador ativo não pode ser desativado nem rebaixado. Um administrador desativa a própria conta somente pelas Configurações.'),
    ('RN08', 'Cada usuário possui exatamente um perfil, criado junto com a conta.'),
    ('RN09', 'Visibilidade: "público" – qualquer usuário; "seguidores" – quem segue o autor; "selecionados" – as pessoas escolhidas; "link" – quem tiver o link. O autor sempre vê o próprio conteúdo.'),
    ('RN10', 'Somente o autor edita ou exclui o próprio post, evento ou comentário. Um administrador pode excluir qualquer post ou evento por moderação, e o autor é avisado.'),
    ('RN11', 'Curtir, salvar, favoritar, seguir e marcar presença são alternâncias: repetir a ação desfaz; não há registros duplicados.'),
    ('RN12', 'Evento e apresentação exigem data, horário de início, horário de fim e local; a data não pode ser anterior a hoje e o fim deve ser depois do início.'),
    ('RN13', 'Quando a UF do local é informada, ela deve ser a mesma UF do perfil do organizador.'),
    ('RN14', 'Um evento ou apresentação é considerado realizado quando a data e o horário de fim já passaram; essa situação é calculada, não registrada.'),
    ('RN15', 'Só avalia um evento quem confirmou presença nele e depois que ele terminou. Cada pessoa tem uma avaliação por evento; um novo envio atualiza a anterior.'),
    ('RN16', 'Só avalia uma apresentação quem participou do evento vinculado e depois que ela terminou. O apresentador avaliado deve estar vinculado à apresentação e ninguém avalia a si mesmo.'),
    ('RN17', 'Escala: 1 a 5 estrelas; atributos do apresentador de 0 a 99 (clareza, domínio do conteúdo, engajamento, storytelling, gestão de tempo e recursos visuais). Na avaliação anônima o nome do avaliador não é exibido.'),
    ('RN18', 'Pontuação geral do apresentador (0 a 99) = média das médias dos seis atributos; sem atributos, usa média de estrelas × 20. O ranking ordena por pontuação geral, depois média de estrelas, quantidade de avaliações e nome.'),
    ('RN19', 'Uma rotina automática, a cada minuto, cria um único lembrete por evento ou apresentação encerrado para cada participante que ainda não o recebeu.'),
    ('RN20', 'Com as notificações desligadas, avisos comuns não são gerados; avisos de moderação (remoção, advertência, desativação) sempre são.'),
    ('RN21', 'Podem ser denunciados posts, apresentações, eventos e usuários, por um motivo da lista (spam, ofensivo, assédio, falso, impróprio, outro). Ninguém denuncia o próprio conteúdo, e cada pessoa tem no máximo uma denúncia aberta por alvo.'),
    ('RN22', 'Ciclo da denúncia: Pendente → Em análise → Procedente ou Improcedente; após decidida não muda. Procedente exige uma ação; "remover conteúdo" não vale para denúncia de usuário nem para conteúdo já removido. Quando a ação é remover o conteúdo ou desativar a conta, as demais denúncias abertas sobre o mesmo alvo são encerradas junto.'),
    ('RN23', 'Toda ação administrativa (criar, editar, promover, desativar, reativar, remover, advertir, decidir denúncia) é registrada com administrador, alvo, data e observação.'),
    ('RN24', 'No dashboard, o usuário vê somente dados do próprio conteúdo; a visão da plataforma é exclusiva de administradores. O período do dashboard pode ser tudo, 7, 30 ou 90 dias (no ranking: desde o início, 90 ou 30 dias).'),
    ('RN25', 'Os horários do Meets seguem o fuso America/Sao_Paulo (configurável por APP_TIMEZONE).'),
    ('RN26', 'Limites: nome 2–120 caracteres; título 160; post e mensagem 5.000; comentário 2.000; biografia e comentário de avaliação 1.000; imagem até cerca de 15 MB.'),
    ('RN27', 'A conversa é direta entre duas pessoas diferentes; somente os participantes leem e enviam mensagens.'),
]

RF_POR_ID = {r[0]: r for r in RF}
RN_POR_ID = {r[0]: r for r in RN}


def rfs_do_caso(uc):
    return [r[0] for r in RF if r[6] == uc]


def rns_do_caso(uc):
    ids = []
    for r in RF:
        if r[6] == uc:
            for rn in r[5]:
                if rn not in ids:
                    ids.append(rn)
    return sorted(ids)


# Detalhes da implementação de cada RF (modelo da professora: "Detalhes da implementação prevista").
# Conferidos com Código/backend/src (rotas e repositórios), migrations/ e Código/snack/screens.
IMPL = {
    'RF01': 'Tela SignupScreen (nome, e-mail, senha e confirmação). API POST /auth/signup valida com Zod, grava a senha com bcrypt na tabela users e cria o registro em profiles e settings; em seguida POST /auth/send-verification gera o código.',
    'RF02': 'Tela EmailVerificationScreen (campo do código e botão de reenviar). API POST /auth/verify-email confere o hash do código e a validade (colunas email_verification_token_hash e email_verification_expires_at em users) e marca email_verified.',
    'RF03': 'Tela LoginScreen (e-mail e senha). API POST /auth/login compara a senha com bcrypt e devolve o token JWT, guardado pelo aplicativo no AsyncStorage.',
    'RF04': 'Opção "Sair" no menu do aplicativo; apaga o token do AsyncStorage e volta para a tela de login. Não há chamada à API.',
    'RF05': 'Tela SettingsScreen (senha atual, nova senha e confirmação). API PUT /users/me/password confere a senha atual e grava o novo hash.',
    'RF06': 'Tela de perfil, opção "Desativar conta" com confirmação da senha. API POST /users/me/deactivate muda o status em users para desativado; nada é apagado.',
    'RF07': 'Telas ProfileScreen e EditProfileScreen (nome, cargo, cidade/UF, número, foto e biografia; a foto passa pelo ImageEditorScreen). API GET e PUT /users/me sobre users e profiles.',
    'RF08': 'Telas SpeakerProfileScreen e ShareProfileScreen. API GET /users/:id/public devolve perfil, publicações visíveis e médias como apresentador; o link aberto por quem não está logado usa GET /public/content/:type/:id.',
    'RF09': 'Botão "Seguir" no perfil público. API POST /users/:id/connect (alternância), GET /users/:id/connection-status, GET /users/connections e GET /users/followers sobre a tabela user_connections.',
    'RF10': 'Tela ChatScreen. API GET e POST /chats, GET e POST /chats/:id/messages e POST /chats/:id/read sobre chats, chat_members e chat_messages.',
    'RF11': 'Tela HomeScreen. API GET /feed reúne posts, apresentações e eventos visíveis ao usuário (tabelas posts, events e content_audience), em ordem de criação, com os contadores de curtidas, comentários e compartilhamentos.',
    'RF12': 'Tela CreateScreen, aba post (título, texto, imagem e visibilidade). API POST /posts grava em posts e, para "selecionados", em content_audience; registra a ação em history.',
    'RF13': 'Menu ⋮ do post (Editar / Excluir com confirmação). API PUT /posts/:id e DELETE /posts/:id, permitidos somente ao autor; a exclusão remove curtidas e comentários em cascata.',
    'RF14': 'Tela CreateScreen, aba apresentação (data, início, fim, local, evento vinculado e apresentadores). API POST /content grava em posts (tipo apresentação) e em presentation_speakers.',
    'RF15': 'Seletor de visibilidade nas telas de criação e edição (público, seguidores, selecionados, link). Coluna visibility em posts e events; pessoas escolhidas em content_audience; link com share_token.',
    'RF16': 'Ícone de coração no feed e no detalhe. API POST /posts/:id/like e POST /events/:id/like (alternância) sobre post_likes e event_likes.',
    'RF17': 'Telas PostDetailScreen e EventDetailScreen. API GET e POST /posts/:id/comments, GET e POST /events/:id/comments e DELETE /comments/:id sobre post_comments.',
    'RF18': 'Botão "Compartilhar" (folha de compartilhamento do aparelho). API POST /shares grava em content_shares; o link abre SharedContentScreen.',
    'RF19': 'Ícones salvar e favoritar; telas SavesScreen e FavoritesScreen. API POST /posts/:id/save, POST /events/:id/save, POST /posts/:id/favorite, GET /saves e GET /favorites sobre saved_posts, saved_events e favorites.',
    'RF20': 'Tela CreateScreen, aba evento (título, descrição, imagem, data, início, fim, CEP, UF, número e visibilidade). API POST /content grava em events e inclui o organizador em event_participants como anfitrião.',
    'RF21': 'Tela EventDetailScreen, menu do organizador (Editar / Excluir com confirmação). API PUT /events/:id e DELETE /events/:id, permitidos somente ao organizador.',
    'RF22': 'Botão "Confirmar presença" em EventDetailScreen. API POST /events/:id/participate (alternância) e GET /events/:id/participants sobre event_participants; gera notificação para o organizador.',
    'RF23': 'Tela CalendarScreen (datas da agenda e, ao tocar em uma data, os eventos do dia). API GET /calendar devolve os eventos organizados ou confirmados pelo usuário.',
    'RF24': 'Tela EventRatingScreen (estrelas, comentário, público ou anônimo). API POST /ratings/events grava em event_ratings (uma por pessoa e evento) e GET /ratings/events/:eventId devolve a média.',
    'RF25': 'Tela PresentationRatingScreen (apresentador, estrelas, seis atributos de 0 a 99, comentário e anonimato). API GET /ratings/available e POST /ratings/presentations gravam em presentation_ratings (atributos em skills, jsonb).',
    'RF26': 'Rotina notifyFinished em server.js, executada na inicialização e a cada 60 segundos (setInterval), com um INSERT ... SELECT na tabela notifications; ensureRatingNotifications em repository.js repete a verificação quando o usuário abre as notificações.',
    'RF27': 'Tela RankingScreen (pódio e filtro de período). API GET /ranking?days= calcula a pontuação em services/scoring.js a partir de presentation_ratings; o toque abre SpeakerProfileScreen (GET /ratings/speakers/:speakerId).',
    'RF28': 'Tela DashboardScreen (escopo "Meu conteúdo" ou "Plataforma" e período). API GET /dashboard?scope=&days= em analyticsRepository.js; scope=platform só para administrador.',
    'RF29': 'Gaveta NotificationsDrawer. API GET /notifications (50 mais recentes) e POST /notifications/:id/read sobre notifications; o toque abre a tela do alvo (target_type e target_id).',
    'RF30': 'Tela SearchScreen (campo de busca com abas pessoas e posts). API GET /search?q= respeitando visibilidade e contas ativas.',
    'RF31': 'Tela HistoryScreen. API GET /history lista os registros da tabela history do usuário.',
    'RF32': 'Tela SettingsScreen (chaves de notificações e modo escuro). API GET e PUT /settings sobre a tabela settings.',
    'RF33': 'Telas AdminUsersScreen e AdminUserFormScreen. API GET e POST /admin/users, GET e PUT /admin/users/:id, POST /admin/users/:id/deactivate e /reactivate e GET /admin/actions (adminRoutes.js); cada ação gera registro em admin_actions.',
    'RF34': 'Opção "Denunciar" no menu do conteúdo ou do perfil (motivo e descrição). API POST /reports grava em reports com status pendente e notifica os administradores.',
    'RF35': 'Telas AdminReportsScreen e AdminReportDetailScreen. API GET /admin/reports, GET /admin/reports/:id, POST /admin/reports/:id/start e POST /admin/reports/:id/decide (reportRoutes.js), com as ações em services/moderation.js.',
    'RF36': 'Menu do administrador no post ou evento ("Remover", com motivo). API DELETE /posts/:id ou /events/:id, que para o administrador chama moderation.removeContent, registra em admin_actions e notifica o autor.',
}
