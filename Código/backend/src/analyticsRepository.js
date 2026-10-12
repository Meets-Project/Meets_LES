import { rankSpeakers, summarizeSpeakerRatings } from './services/scoring.js';

// Consultas de análise: Ranking de Apresentadores (#007) e Dashboards (#008).
export function makeAnalyticsRepository(db) {
  const many = async (sql, params = []) => (await db.query(sql, params)).rows;

  async function ranking({ since = null } = {}) {
    const rows = await many(`SELECT pr.speaker_id, pr.stars, pr.skills, pr.created_at,
        u.name, COALESCE(up.avatar,'👤') AS avatar, COALESCE(up.role,'Membro') AS role
      FROM presentation_ratings pr
      JOIN users u ON u.id = pr.speaker_id
      LEFT JOIN profiles up ON up.user_id = u.id
      WHERE u.status = 'active' AND ($1::timestamptz IS NULL OR pr.created_at >= $1)`, [since]);
    const bySpeaker = new Map();
    for (const r of rows) {
      if (!bySpeaker.has(r.speaker_id)) bySpeaker.set(r.speaker_id, { speaker: { id: r.speaker_id, name: r.name, avatar: r.avatar, role: r.role }, rows: [] });
      bySpeaker.get(r.speaker_id).rows.push(r);
    }
    const entries = [...bySpeaker.values()].map(({ speaker, rows: rs }) => {
      const s = summarizeSpeakerRatings(rs);
      return { speaker, overall: s.overall, averageStars: s.averageStars, totalRatings: s.totalRatings, averageSkills: s.averageSkills };
    });
    return rankSpeakers(entries);
  }

  return { ranking };
}
