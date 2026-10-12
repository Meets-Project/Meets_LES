import { describe, expect, it, beforeEach } from 'vitest';
import request from 'supertest';
import { summarizeSpeakerRatings } from '../src/services/scoring.js';
import { auth, createTestApp, signup } from './helpers.js';

const skills = (v) => ({ clarity: v, content: v, engagement: v, storytelling: v, timing: v, visuals: v });

describe('Pontuação do apresentador', () => {
  it('usa a média dos atributos e, sem atributos, as estrelas x 20', () => {
    expect(summarizeSpeakerRatings([{ stars: 5, skills: skills(90) }, { stars: 3, skills: skills(70) }]).overall).toBe(80);
    expect(summarizeSpeakerRatings([{ stars: 4, skills: {} }]).overall).toBe(80);
    expect(summarizeSpeakerRatings([]).overall).toBe(0);
  });
});

describe('Ranking de apresentadores (#007)', () => {
  let app, db, users;
  beforeEach(async () => {
    ({ app, db } = await createTestApp());
    users = {};
    for (const n of ['ana', 'bia', 'caio', 'rater']) users[n] = await signup(app, { name: n.toUpperCase(), email: `${n}@example.com` });
  });

  async function rate(speaker, stars, value, presentation) {
    await db.query(`INSERT INTO presentation_ratings(presentation_id,rater_id,speaker_id,stars,skills) VALUES($1,$2,$3,$4,$5)`,
      [presentation, users.rater.user.id, speaker.user.id, stars, JSON.stringify(skills(value))]);
  }

  it('lista vazia quando ninguém foi avaliado', async () => {
    const res = await request(app).get('/ranking').set(auth(users.rater.token));
    expect(res.status).toBe(200);
    expect(res.body.data).toHaveLength(0);
  });

  it('ordena pela pontuação geral e numera as posições', async () => {
    await rate(users.ana, 4, 70, 'p1');
    await rate(users.bia, 5, 95, 'p2');
    await rate(users.caio, 3, 85, 'p3');
    const res = await request(app).get('/ranking').set(auth(users.rater.token));
    expect(res.body.data.map((r) => r.speaker.name)).toEqual(['BIA', 'CAIO', 'ANA']);
    expect(res.body.data[0]).toMatchObject({ position: 1, overall: 95, totalRatings: 1 });
  });

  it('o perfil do apresentador mostra a mesma pontuação do ranking', async () => {
    await rate(users.ana, 4, 70, 'p1');
    await rate(users.ana, 5, 90, 'p2');
    const ranking = await request(app).get('/ranking').set(auth(users.rater.token));
    const summary = await request(app).get(`/ratings/speakers/${users.ana.user.id}`).set(auth(users.rater.token));
    expect(summary.body.data.overall).toBe(ranking.body.data[0].overall);
    expect(summary.body.data.overall).toBe(80);
  });

  it('apresentador com conta desativada sai do ranking', async () => {
    await rate(users.ana, 4, 70, 'p1');
    await rate(users.bia, 5, 95, 'p2');
    await db.query(`UPDATE users SET status='deactivated' WHERE id=$1`, [users.bia.user.id]);
    const res = await request(app).get('/ranking').set(auth(users.rater.token));
    expect(res.body.data.map((r) => r.speaker.name)).toEqual(['ANA']);
  });
});
