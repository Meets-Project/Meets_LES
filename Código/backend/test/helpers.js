import crypto from 'node:crypto';
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { newDb } from 'pg-mem';

export const migrationDir = path.join(path.dirname(fileURLToPath(import.meta.url)), '..', 'migrations');

// Ajustes para o pg-mem: extensões e funções que ele não traz prontas.
export function registerPgMemFunctions(mem) {
  mem.public.registerFunction({
    name: 'gen_random_uuid',
    impure: true,
    implementation: () => crypto.randomUUID(),
  });
  mem.public.registerFunction({
    name: 'nullif',
    implementation: (value, other) => value === other ? null : value,
  });
  mem.public.registerFunction({
    name: 'left',
    implementation: (value, length) => String(value || '').slice(0, Number(length || 0)),
  });
}

// Aplica as mesmas migrations do servidor, para o teste usar o esquema real do banco.
export async function applyMigrations(mem) {
  const files = (await fs.readdir(migrationDir)).filter((file) => file.endsWith('.sql')).sort();
  for (const file of files) {
    const sql = (await fs.readFile(path.join(migrationDir, file), 'utf8'))
      .replace(/^﻿/, '')
      .replace(/CREATE EXTENSION IF NOT EXISTS pgcrypto;?/gi, '')
      .replace(/UPDATE posts SET title[\s\S]*?WHERE title = '';?/i, '');
    await mem.public.none(sql);
  }
}

export async function createTestDb() {
  const mem = newDb();
  registerPgMemFunctions(mem);
  await applyMigrations(mem);
  const { Pool } = mem.adapters.createPg();
  return { mem, db: new Pool() };
}
