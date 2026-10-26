"""Trechos de código mostrados nos slides "Sequência ↔ código" (copiados do repositório,
com quebras de linha para caber no slide) e a legenda dos passos dos diagramas de sequência."""

CODIGO = {
    '#015': {
        'arquivos': ['backend/src/server.js', 'backend/src/repository.js'],
        'codigo': '''// Passo 1: o agendador roda na inicialização e a cada 60 s
await notifyFinished();
setInterval(() => { notifyFinished().catch(...); }, 60_000);

async function notifyFinished() {
  await pool.query(`INSERT INTO notifications (user_id, title, body, target_type, target_id, target_token)
    SELECT ... FROM ( /* participantes de eventos e apresentações */ ) target
    -- terminou no fuso do Meets:
    --   event_date < (NOW() AT TIME ZONE $1)::date
    --   OR (event_date = hoje AND event_end_time <= (NOW() AT TIME ZONE $1)::time)
    WHERE NOT EXISTS (SELECT 1 FROM settings st
            WHERE st.user_id = target.user_id AND st.notifications_enabled = FALSE)
      AND NOT EXISTS (SELECT 1 FROM notifications n          -- sem lembrete repetido
            WHERE n.user_id = target.user_id AND n.target_type = target.target_type
              AND n.target_id = target.target_id)
    ON CONFLICT (user_id, target_type, target_id) ... DO NOTHING`, [APP_TIMEZONE]);
}

// Passos 4-9: GET /notifications garante os lembretes e lista
async listNotifications(userId) {
  await this.ensureRatingNotifications(userId);
  return many(`SELECT id,title,body,target_type,target_id,target_token,read_at,created_at
    FROM notifications WHERE user_id=$1 ORDER BY created_at DESC LIMIT 50`, [userId]);
},

async ensureRatingNotifications(userId) {
  const events = await many(`SELECT e.id,e.title,e.share_token,e.event_date,e.event_end_time
    FROM events e JOIN event_participants ep ON ep.event_id=e.id WHERE ep.user_id=$1 ...`, [userId]);
  for (const e of events.filter((row) => hasEnded(row.event_date, row.event_end_time))) {
    const exists = await one(`SELECT 1 FROM notifications
      WHERE user_id=$1 AND target_type='event-rating' AND target_id=$2 ...`, [userId, e.id]);
    if (!exists) await this.createNotification(userId, {
      title: 'Avalie o evento que você participou',
      targetType: 'event-rating', targetId: e.id, targetToken: e.share_token,
    });
  }
  // ... o mesmo para as apresentações ('presentation-rating')
},''',
        'passos': [
            ('1', 'notifyFinished(): um INSERT ... SELECT cria os lembretes de quem participou, no fuso do Meets'),
            ('3-5', 'getNotifications() → listNotifications() → ensureRatingNotifications()'),
            ('7-8', 'hasEnded() confere o término e createNotification() cria o lembrete que faltar'),
            ('14-16', 'target_type "event-rating" leva o app ao formulário de avaliação'),
        ],
    },
    '#005': {
        'arquivos': ['backend/src/app.js', 'backend/src/repository.js'],
        'codigo': '''// Passos 4-5: POST /ratings/events e validação Zod (nota de 1 a 5)
app.post('/ratings/events', requireAuth, async (req, res, next) => {
  try {
    const data = z.object({
      eventId: z.string().uuid(),
      visibility: z.enum(['public', 'anonymous']).default('public'),
      stars: z.coerce.number().min(1).max(5),
      comment: z.string().max(1000).optional(),
    }).parse(req.body);                                   // inválido → 400 (passo 6)
    res.status(201).json({ data: await repo.createEventRating(req.auth.sub, data) });  // passos 7 e 16
  } catch (e) { next(e); }
});

// Passos 8-12: participou? terminou? senão, FORBIDDEN → 403
async createEventRating(userId, { eventId, stars, comment, visibility = 'public' }) {
  const event = await one(`SELECT id,title,author_id,event_date,event_end_time
    FROM events WHERE id=$1`, [eventId]);
  const participant = await one(`SELECT 1 FROM event_participants
    WHERE event_id=$1 AND user_id=$2`, [eventId, userId]);
  if (!event || !participant || !hasEnded(event.event_date, event.event_end_time)) {
    const error = new Error('Você só pode avaliar um evento do qual participou e que já terminou.');
    error.code = 'FORBIDDEN';
    throw error;
  }
  // Passo 13: uma avaliação por pessoa; um novo envio atualiza a anterior
  return one(`INSERT INTO event_ratings(event_id,rater_id,stars,comment,visibility)
    VALUES($1,$2,$3,$4,$5)
    ON CONFLICT(event_id,rater_id) DO UPDATE SET stars=EXCLUDED.stars,
      comment=EXCLUDED.comment, visibility=EXCLUDED.visibility, updated_at=NOW()
    RETURNING id,event_id,rater_id,stars,comment,visibility,created_at,updated_at`, [...]);
},

// Passos 17-22: média exibida no app (GET /ratings/events/:eventId)
async getEventRatingSummary(eventId) {
  const allRatings = await many(`SELECT er.stars, er.comment, er.visibility, ... FROM event_ratings er
    JOIN users u ON u.id=er.rater_id WHERE er.event_id=$1 ORDER BY er.created_at DESC`, [eventId]);
  const totalRatings = allRatings.length;
  const averageStars = totalRatings ? Number((allRatings.reduce((s, r) => s + Number(r.stars || 0), 0)
    / totalRatings).toFixed(1)) : 0;
  return { totalRatings, averageStars, recentRatings: allRatings.slice(0, 10) /* anônimo → "Anônimo" */ };
},''',
        'passos': [
            ('4-5', 'POST /ratings/events e validação Zod (estrelas de 1 a 5)'),
            ('8-12', 'createEventRating(): participação e término (hasEnded); senão 403'),
            ('13', 'INSERT ... ON CONFLICT: uma avaliação por pessoa por evento'),
            ('17-22', 'getEventRatingSummary() devolve a média exibida'),
        ],
    },
    '#006': {
        'arquivos': ['backend/src/app.js', 'backend/src/repository.js'],
        'codigo': '''// Passos 9-11: POST /ratings/presentations — estrelas 1..5 e 6 atributos de 0 a 99
const data = z.object({
  postId: z.string().uuid().optional()..., presentationId: z.string()...,
  stars: z.coerce.number().min(1).max(5),
  visibility: z.enum(['public', 'anonymous']).default('public'),
  speakerId: z.string().uuid().optional()...,
  skills: z.object({
    clarity: z.coerce.number().min(0).max(99), content: z.coerce.number().min(0).max(99),
    engagement: z.coerce.number().min(0).max(99), storytelling: z.coerce.number().min(0).max(99),
    timing: z.coerce.number().min(0).max(99), visuals: z.coerce.number().min(0).max(99),
  }),
  comment: z.string().max(1000).optional(),
}).refine(v => v.postId || v.presentationId, ...).parse(req.body);
const rating = await repo.createRating(req.auth.sub, data);
res.status(201).json({ data: rating });                                   // passo 21

// Passos 12-17: regras de quem pode avaliar
async createRating(raterId, payload) {
  let post = await one(`SELECT ${POST_COLS} FROM posts WHERE id=$1`, [payload.postId]);
  if (!post.event_date || !post.event_end_time || !hasEnded(post.event_date, post.event_end_time))
    throw forbidden('A apresentação ainda não terminou. A avaliação será liberada após o horário de fim.');
  const isSpeaker = await one(`SELECT 1 FROM presentation_speakers
    WHERE presentation_id=$1 AND speaker_id=$2`, [presentationId, raterId]);
  if (post.mentioned_event_id && !isSpeaker && post.author_id !== raterId) {
    const participant = await one(`SELECT 1 FROM event_participants
      WHERE event_id=$1 AND user_id=$2`, [post.mentioned_event_id, raterId]);
    if (!participant) throw forbidden('Só quem participou do evento pode avaliar esta apresentação.');
  }
  if (speaker?.id === raterId) { /* code = 'SELF_RATING' */ throw error; }
  const linked = await one(`SELECT 1 FROM presentation_speakers
    WHERE presentation_id=$1 AND speaker_id=$2`, [presentationId, speaker.id]);
  if (!linked) { /* code = 'SPEAKER_NOT_LINKED' */ throw err; }

  // Passo 18: grava estrelas e atributos (jsonb); repetir atualiza
  const row = await one(`INSERT INTO presentation_ratings
    (presentation_id,post_id,rater_id,speaker_id,stars,skills,comment,visibility)
    VALUES($1,$2,$3,$4,$5,$6::jsonb,$7,$8)
    ON CONFLICT(presentation_id,rater_id,speaker_id) DO UPDATE SET stars=EXCLUDED.stars, ...`, [...]);
  return row;
},''',
        'passos': [
            ('9-11', 'POST /ratings/presentations: Zod valida estrelas (1–5) e os 6 atributos (0–99)'),
            ('12-15', 'createRating(): término (hasEnded), participação e vínculo do apresentador'),
            ('16-17', 'FORBIDDEN, SELF_RATING ou SPEAKER_NOT_LINKED viram 403/400'),
            ('18', 'INSERT ... ON CONFLICT grava estrelas e skills (jsonb)'),
        ],
    },
    '#007': {
        'arquivos': ['backend/src/app.js', 'backend/src/analyticsRepository.js', 'backend/src/services/scoring.js'],
        'codigo': '''// Passos 2-4: GET /ranking?days=N (tudo, 90 ou 30 dias) vira data inicial do período
app.get('/ranking', requireAuth, async (req, res, next) => {
  try {
    const days = Number(req.query.days || 0);
    const since = Number.isFinite(days) && days > 0 ? new Date(Date.now() - days * 86400000) : null;
    res.json({ data: await analyticsRepo.ranking({ since }) });            // passos 12-13
  } catch (e) { next(e); }
});

// Passos 5-7: avaliações do período, só de contas ativas, agrupadas por apresentador
async function ranking({ since = null } = {}) {
  const rows = await many(`SELECT pr.speaker_id, pr.stars, pr.skills, pr.created_at, u.name, ...
    FROM presentation_ratings pr JOIN users u ON u.id = pr.speaker_id
    LEFT JOIN profiles up ON up.user_id = u.id
    WHERE u.status = 'active' AND ($1::timestamptz IS NULL OR pr.created_at >= $1)`, [since]);
  const bySpeaker = new Map();
  for (const r of rows) { /* bySpeaker.get(r.speaker_id).rows.push(r) */ }
  const entries = [...bySpeaker.values()].map(({ speaker, rows: rs }) => {
    const s = summarizeSpeakerRatings(rs);                                  // passos 8-9
    return { speaker, overall: s.overall, averageStars: s.averageStars,
             totalRatings: s.totalRatings, averageSkills: s.averageSkills };
  });
  return rankSpeakers(entries);                                             // passos 10-11
}

// scoring.js — pontuação geral (0 a 99) = média das médias dos 6 atributos
const averageSkills = Object.fromEntries(SKILL_KEYS.map((k) =>
  [k, skillsCount ? Math.round(sums[k] / skillsCount) : 0]));
if (skillsCount) overall = Math.round(SKILL_KEYS.reduce((a, k) => a + averageSkills[k], 0) / SKILL_KEYS.length);
else if (totalRatings) overall = Math.round(averageStars * 20);

// Desempate: pontuação, média de estrelas, total de avaliações, nome
export function rankSpeakers(entries) {
  return [...entries]
    .sort((a, b) => (b.overall - a.overall) || (b.averageStars - a.averageStars)
      || (b.totalRatings - a.totalRatings) || String(a.speaker.name).localeCompare(String(b.speaker.name)))
    .map((e, i) => ({ position: i + 1, ...e }));
}''',
        'passos': [
            ('2-4', 'GET /ranking: o período (dias) vira a data inicial "since"'),
            ('5-7', 'SELECT só de contas ativas, agrupado por speaker_id'),
            ('8-9', 'summarizeSpeakerRatings(): médias e pontuação geral (0 a 99)'),
            ('10-11', 'rankSpeakers(): ordena e numera as posições (RN18)'),
        ],
    },
    '#008': {
        'arquivos': ['backend/src/app.js', 'backend/src/analyticsRepository.js'],
        'codigo': '''// Passos 2-4: GET /dashboard?scope=me|platform&days=N — "platform" só para administradores
app.get('/dashboard', requireAuth, async (req, res, next) => {
  try {
    const scope = req.query.scope === 'platform' ? 'platform' : 'me';
    if (scope === 'platform' && !req.auth.isAdmin) {
      return res.status(403).json({ message: 'O dashboard da plataforma é exclusivo dos administradores.',
                                    code: 'ADMIN_ONLY' });
    }
    const days = Number(req.query.days || 0);                    // tudo, 7, 30 ou 90 dias
    const since = Number.isFinite(days) && days > 0 ? new Date(Date.now() - days * 86400000) : null;
    res.json({ data: await analyticsRepo.dashboard({ scope, ownerId: req.auth.sub, since }) });  // passo 5
  } catch (e) { next(e); }
});

// Passos 6-10: os quatro painéis em paralelo; owner = null na visão da plataforma
async function dashboard({ scope = 'me', ownerId = null, since = null } = {}) {
  const owner = scope === 'platform' ? null : ownerId;
  const params = [since, owner];
  const [posts, events, ratings, presenters] = await Promise.all([
    postsBlock(params), eventsBlock(params), ratingsBlock(params),
    presentersBlock({ since, ownerId: owner }),
  ]);
  const result = { scope, since, generatedAt: new Date().toISOString(), posts, events, ratings, presenters };

  // Passos 11-12: indicadores da comunidade (só plataforma)
  if (scope === 'platform') {
    const [activeUsers, deactivatedUsers, newUsers, openReports] = await Promise.all([
      count(`SELECT count(*)::int AS total FROM users WHERE status = 'active'`, []),
      count(`SELECT count(*)::int AS total FROM users WHERE status = 'deactivated'`, []),
      count(`SELECT count(*)::int AS total FROM users WHERE ${PERIOD('created_at')}`, [since]),
      count(`SELECT count(*)::int AS total FROM reports WHERE status IN ('pending','in_review')`, []),
    ]);
    result.community = { activeUsers, deactivatedUsers, newUsers, openReports };
  }
  return result;                                                    // passos 13-14
}''',
        'passos': [
            ('2-4', 'escopo "platform" sem ser administrador → 403 ADMIN_ONLY'),
            ('5', 'dashboard({ scope, ownerId, since }); owner nulo = plataforma inteira'),
            ('6-10', 'Promise.all: postsBlock, eventsBlock, ratingsBlock e presentersBlock'),
            ('11-12', 'community: ativos, desativados, novos e denúncias abertas'),
        ],
    },
    '#013': {
        'arquivos': ['backend/src/routes/reportRoutes.js'],
        'codigo': '''// Passos 10-11: POST /admin/reports/:id/decide (somente administradores)
app.post('/admin/reports/:id/decide', ...guard, async (req, res, next) => {
  try {
    const data = decideSchema.parse(req.body);           // procedente exige a ação
    const report = await reportsRepo.get(req.params.id);
    // Passo 12: já decidida → 409; ação inválida para o alvo → 400
    if (!['pending', 'in_review'].includes(report.status)) {
      return res.status(409).json({ message: 'Esta denúncia já foi analisada.', data: report });
    }
    const action = data.decision === 'upheld' ? data.action : null;
    if (action === 'remove_content' && report.target_type === 'user') {
      return res.status(400).json({ message: 'Para denúncia de usuário, escolha advertir ou desativar a conta.' });
    }
    // Passos 13-16: a ação de moderação (cada uma grava o próprio logAction)
    const note = data.note || '';                    // reason = note || REASON_LABELS[report.reason]
    if (action === 'remove_content') {
      await moderation.removeContent(req.auth.sub, { type: report.target_type, id: report.target_id, reason: ... });
    } else if (action === 'warn_author') {
      await moderation.warnUser(req.auth.sub, { userId: report.target_owner_id, reason: ... });
    } else if (action === 'deactivate_user') {
      await moderation.deactivateUser(req.auth.sub, { userId: report.target_owner_id, reason: ... });
    }
    // Passos 17-18: registra a decisão e a auditoria
    await reportsRepo.decide(report.id, { adminId: req.auth.sub, status: data.decision, action, note });
    await adminRepo.logAction(req.auth.sub, {
      action: data.decision === 'upheld' ? 'report_upheld' : 'report_dismissed',
      targetType: 'report', targetId: report.id, note: [action, note].filter(Boolean).join(' · '),
    });
    // Passo 19: remoção ou desativação resolvem as outras denúncias abertas do mesmo alvo
    let closedTogether = [];
    if (action === 'remove_content' || action === 'deactivate_user') {
      closedTogether = await reportsRepo.closeOthersOnTarget(report.target_type, report.target_id,
        report.id, { adminId: req.auth.sub, status: 'upheld', action, note: ... });
    }
    // Passo 20: avisa cada denunciante uma vez
    const reporters = [report.reporter_id, ...closedTogether.map((r) => r.reporter_id)].filter(Boolean);
    for (const reporterId of [...new Set(reporters)]) {
      await repo.createNotification(reporterId, { title: 'Sua denúncia foi analisada', body: ... });
    }
    res.json({ data: { ...(await reportsRepo.get(report.id)), closed_together: closedTogether.length } });
  } catch (e) { next(e); }
});''',
        'passos': [
            ('10-12', 'decide: valida o corpo; já decidida → 409, ação inválida → 400'),
            ('13-16', 'removeContent, warnUser ou deactivateUser (moderation.js) + logAction'),
            ('17-18', 'reportsRepo.decide() e adminRepo.logAction() (auditoria, RN23)'),
            ('19-20', 'closeOthersOnTarget() e notificação de cada denunciante'),
        ],
    },
}
