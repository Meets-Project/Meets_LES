import { describe, expect, it, beforeEach } from 'vitest';
import request from 'supertest';
import { createTestApp, signup } from './helpers.js';

describe('API: cadastro, login e perfil', () => {
  let app, db;
  beforeEach(async () => {
    ({ app, db } = await createTestApp());
  });

  it('cadastra, entra e lê o próprio perfil', async () => {
    const { res, token } = await signup(app);
    expect(res.status).toBe(201);
    expect(token).toBeTruthy();

    const login = await request(app).post('/auth/login').send({ email: 'pessoa@example.com', password: 'senha123' });
    expect(login.status).toBe(200);

    const me = await request(app).get('/users/me').set('Authorization', `Bearer ${login.body.data.token}`);
    expect(me.status).toBe(200);
    expect(me.body.data.email).toBe('pessoa@example.com');
  });

  it('recusa rota protegida sem token', async () => {
    const res = await request(app).get('/users/me');
    expect(res.status).toBe(401);
  });
});
