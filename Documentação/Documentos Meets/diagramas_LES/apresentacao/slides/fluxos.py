"""Fluxo principal (FP), alternativos (FA) e exceções (FE) de cada caso, para o 1º slide.
FP vem da especificação (gerador/casos_de_uso.py); FA = desvio que volta ao fluxo ou termina bem;
FE = erro que encerra o caso. A numeração FA/FE é a mesma usada nos diagramas de sequência."""

FLUXOS = {
    '#015': {
        'fa': [('FA1', 'Lembrete já enviado ou notificações desligadas: o participante é ignorado (sem duplicidade).'),
               ('FA2', 'Garantia ao consultar: ao abrir as notificações, o sistema repete a verificação e cria o lembrete que faltar.')],
        'fe': [('FE1', 'Falha na rotina (erro de banco): o erro vai para o log e a rotina tenta de novo no minuto seguinte.')],
    },
    '#005': {
        'fa': [('FA1', 'Nota inválida (fora de 1 a 5): o app recusa e pede a correção; volta ao passo 4.'),
               ('FA2', 'Já avaliou: o novo envio substitui a avaliação anterior (uma por pessoa).')],
        'fe': [('FE1', 'Dados inválidos na API: recusa com 400 e o caso termina.'),
               ('FE2', 'Não participou ou o evento não terminou: recusa com 403 e o caso termina.')],
    },
    '#006': {
        'fa': [('FA1', 'Estrelas fora de 1 a 5 ou sem apresentador escolhido: o app pede a correção; volta ao passo 5.'),
               ('FA2', 'Já avaliou este apresentador: o novo envio substitui a avaliação anterior.')],
        'fe': [('FE1', 'Sem permissão (não participou, apresentação não terminou, apresentador não vinculado) ou autoavaliação: recusa com 403/400 e o caso termina.')],
    },
    '#007': {
        'fa': [('FA1', 'Sem avaliações no período: o app informa que o ranking ainda não tem dados suficientes.'),
               ('FA2', 'Trocar período (desde o início, 90 ou 30 dias): o fluxo volta ao passo 2.')],
        'fe': [('FE1', 'Falha ao consultar a API: o app mostra a mensagem de erro.')],
    },
    '#008': {
        'fa': [('FA1', 'Administrador escolhe a visão da plataforma: entram também os indicadores da comunidade.'),
               ('FA2', 'Sem dados no período: os painéis mostram zero e a mensagem de vazio.')],
        'fe': [('FE1', 'Visão da plataforma pedida por quem não é administrador: recusa com 403 (ADMIN_ONLY).')],
    },
    '#013': {
        'fa': [('FA1', 'Improcedente: nenhuma ação de moderação; o conteúdo continua e os denunciantes são avisados.'),
               ('FA2', 'Remover conteúdo ou desativar a conta: as outras denúncias abertas do mesmo alvo são fechadas juntas.')],
        'fe': [('FE1', 'Denúncia já decidida (409), procedente sem ação ou ação inválida para o alvo (400): o sistema recusa.')],
    },
}
