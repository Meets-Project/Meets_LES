"""Trechos curtos do código (até ~72 colunas) para o 3º slide de cada caso de uso
(sequência + código + tela). Os comentários "passo N" seguem a numeração dos diagramas
de sequência em ../fontes-elk."""

CURTO = {
    '#015': {
        'arquivos': ['server.js', 'repository.js', 'NotificationsDrawer.js'],
        'codigo': """// server.js — passo 1: agendador a cada 60 s
await notifyFinished();
setInterval(() => notifyFinished().catch(...), 60_000);

async function notifyFinished() {
  await pool.query(`INSERT INTO notifications
      (user_id, title, body, target_type, target_id)
    SELECT ... FROM (/* participantes */) target
    -- fim já passou no fuso APP_TIMEZONE
    WHERE NOT EXISTS (/* notificações desligadas */)
      AND NOT EXISTS (/* lembrete já enviado */)
    ON CONFLICT (...) DO NOTHING`, [APP_TIMEZONE]);
}

// repository.js — passos 4-9: garante e lista
async listNotifications(userId) {
  await this.ensureRatingNotifications(userId);
  return many(`SELECT ... FROM notifications
    WHERE user_id=$1 ORDER BY created_at DESC
    LIMIT 50`, [userId]);
}
async ensureRatingNotifications(userId) {
  for (const e of events.filter((r) =>
      hasEnded(r.event_date, r.event_end_time))) {   // passo 7
    if (!exists) await this.createNotification(userId, {
      title: 'Avalie o evento que você participou',
      targetType: 'event-rating', targetId: e.id }); // passo 8
  }
}

// NotificationsDrawer.js — passos 14-16
const handleNotificationPress = (id) => {
  if (item.unread) markNotificationRead(item.id);
  if (item.target_type === 'event-rating')
    navigation.navigate('EventRating',
      { eventId: item.target_id });
};""",
    },
    '#005': {
        'arquivos': ['EventRatingScreen.js', 'app.js', 'repository.js'],
        'codigo': """// EventRatingScreen.js — passos 2-3
const handleSubmit = async () => {
  if (rating < 1 || rating > 5)                 // FA1
    return Alert.alert('Avaliação inválida', ...);
  await createEventRating(
    { eventId, stars: rating, comment, visibility });
  setSummary(await getEventRatingSummary(eventId));
};

// app.js — passos 4-6: Zod (estrelas 1 a 5)
app.post('/ratings/events', requireAuth, async (req, res, next) => {
  const data = z.object({
    eventId: z.string().uuid(),
    stars: z.coerce.number().min(1).max(5),
    comment: z.string().max(1000).optional(),
  }).parse(req.body);                       // FE1 → 400
  res.status(201).json(
    { data: await repo.createEventRating(req.auth.sub, data) });
});

// repository.js — passos 7-13
async createEventRating(userId, { eventId, stars, ... }) {
  const event = await one(`SELECT ... FROM events ...`);
  const participant = await one(`SELECT 1
    FROM event_participants WHERE ...`);
  if (!event || !participant ||
      !hasEnded(event.event_date, event.event_end_time))
    throw FORBIDDEN;                         // FE2 → 403
  return one(`INSERT INTO event_ratings (...)
    VALUES($1,$2,$3,$4,$5)
    ON CONFLICT(event_id, rater_id)          -- FA2
    DO UPDATE SET stars=EXCLUDED.stars, ...`);
}

// passos 19-21: média exibida
async getEventRatingSummary(eventId) {
  const averageStars = soma(stars) / totalRatings;
  return { totalRatings, averageStars, recentRatings };
}""",
    },
    '#006': {
        'arquivos': ['PresentationRatingScreen.js', 'app.js', 'repository.js'],
        'codigo': """// PresentationRatingScreen.js — passos 7-8
async function handleSubmit() {
  if (stars < 1 || stars > 5 || !selectedSpeaker)
    return setFeedback(...);                    // FA1
  await savePresentationRating({ presentationId,
    stars, speakerId, skills: selectedSkills, ... });
  setFeedback('Avaliação salva com sucesso!');
  navigation.goBack();
}

// app.js — passos 9-11: estrelas 1-5, 6 atributos 0-99
const data = z.object({
  stars: z.coerce.number().min(1).max(5),
  skills: z.object({ clarity, content, engagement,
    storytelling, timing, visuals }), // cada um 0..99
}).parse(req.body);
res.status(201).json(
  { data: await repo.createRating(req.auth.sub, data) });

// repository.js — passos 12-17: regras (FE1)
async createRating(raterId, payload) {
  if (!hasEnded(post.event_date, post.event_end_time))
    throw forbidden('A apresentação ainda não terminou.');
  if (!participant)
    throw forbidden('Só quem participou do evento ...');
  if (speaker.id === raterId) throw 'SELF_RATING';
  if (!linked) throw 'SPEAKER_NOT_LINKED';

  // passo 18: grava estrelas e skills (jsonb)
  return one(`INSERT INTO presentation_ratings
    (presentation_id, rater_id, speaker_id,
     stars, skills, comment, visibility)
    VALUES(...)
    ON CONFLICT(presentation_id, rater_id, speaker_id)
    DO UPDATE SET ...`);                         // FA2
}""",
    },
    '#007': {
        'arquivos': ['RankingScreen.js', 'app.js', 'analyticsRepository.js', 'scoring.js'],
        'codigo': """// RankingScreen.js — passos 1-2
const load = useCallback(async () => {
  try { setItems(await getRanking(Number(period))); }
  catch (e) { setError(e.message); }            // FE1
}, [period]);

// app.js — passos 2-4: período vira "since"
app.get('/ranking', requireAuth, async (req, res) => {
  const days = Number(req.query.days || 0);
  const since = days > 0
    ? new Date(Date.now() - days * 86400000) : null;
  res.json({ data: await analyticsRepo.ranking({ since }) });
});

// analyticsRepository.js — passos 5-10
async function ranking({ since }) {
  const rows = await many(`SELECT pr.speaker_id,
      pr.stars, pr.skills, u.name ...
    FROM presentation_ratings pr
    JOIN users u ON u.id = pr.speaker_id
    WHERE u.status = 'active'
      AND ($1 IS NULL OR pr.created_at >= $1)`);
  // agrupa por speaker_id (passo 7)
  const entries = grupos.map(({ speaker, rows }) => ({
    speaker, ...summarizeSpeakerRatings(rows) }));
  return rankSpeakers(entries);
}

// scoring.js — passos 8-11 (RN18)
overall = Math.round(média das médias dos 6 atributos);
// sem atributos: overall = averageStars * 20
.sort((a, b) => (b.overall - a.overall)
  || (b.averageStars - a.averageStars)
  || (b.totalRatings - a.totalRatings)
  || a.speaker.name.localeCompare(b.speaker.name))
.map((e, i) => ({ position: i + 1, ...e }));""",
    },
    '#008': {
        'arquivos': ['DashboardScreen.js', 'app.js', 'analyticsRepository.js'],
        'codigo': """// DashboardScreen.js — passos 1-2
const load = useCallback(async () => {
  try { setData(await getDashboard(
          { scope, days: Number(period) })); }
  catch (e) { setError(e.message); }           // passo 4
}, [scope, period]);

// app.js — passos 2-5
app.get('/dashboard', requireAuth, async (req, res) => {
  const scope = req.query.scope === 'platform'
    ? 'platform' : 'me';
  if (scope === 'platform' && !req.auth.isAdmin)
    return res.status(403).json(                // FE1
      { code: 'ADMIN_ONLY', message: ... });
  const since = days > 0 ? ... : null; // tudo, 7, 30, 90
  res.json({ data: await analyticsRepo.dashboard(
    { scope, ownerId: req.auth.sub, since }) });
});

// analyticsRepository.js — passos 6-13
async function dashboard({ scope, ownerId, since }) {
  const owner = scope === 'platform' ? null : ownerId;
  const [posts, events, ratings, presenters] =
    await Promise.all([
      postsBlock(params), eventsBlock(params),
      ratingsBlock(params),
      presentersBlock({ since, ownerId: owner }) ]);
  const result = { scope, posts, events,
                   ratings, presenters };
  if (scope === 'platform')                     // FA1
    result.community = { activeUsers,
      deactivatedUsers, newUsers, openReports };
  return result;
}""",
    },
    '#013': {
        'arquivos': ['AdminReportDetailScreen.js', 'routes/reportRoutes.js'],
        'codigo': """// AdminReportDetailScreen.js — passos 6-10
async function start() { await adminStartReport(reportId); }
async function decide(decision) {
  await adminDecideReport(reportId, { decision,
    action: decision === 'upheld' ? action : undefined });
}

// reportRoutes.js — POST /admin/reports/:id/decide
const data = decideSchema.parse(req.body);   // passo 11
if (!['pending', 'in_review'].includes(report.status))
  return res.status(409).json(               // FE1
    { message: 'Esta denúncia já foi analisada.' });
const action = data.decision === 'upheld'
  ? data.action : null;          // FA1: improcedente

// passos 13-16: ação de moderação (+ logAction)
if (action === 'remove_content')
  await moderation.removeContent(adminId, { ... });
else if (action === 'warn_author')
  await moderation.warnUser(adminId, { ... });
else if (action === 'deactivate_user')
  await moderation.deactivateUser(adminId, { ... });

// passos 17-18: decisão e auditoria (RN23)
await reportsRepo.decide(report.id, { status, action });
await adminRepo.logAction(adminId,
  { action: 'report_upheld' | 'report_dismissed' });

// passo 19 (FA2): fecha as outras do mesmo alvo
if (action === 'remove_content'
    || action === 'deactivate_user')
  closedTogether = await reportsRepo
    .closeOthersOnTarget(type, targetId, id, ...);

// passo 20: avisa cada denunciante
for (const id of new Set(reporters))
  await repo.createNotification(id,
    { title: 'Sua denúncia foi analisada' });""",
    },
}
