'use strict';
// База данных: Turso (libSQL, совместима с SQLite). Адрес и токен берутся из TURSO_DATABASE_URL и TURSO_AUTH_TOKEN.
// Без этих переменных используется локальный файл data/cahier.db: удобно для запуска на своём компьютере.
// Таблицы создаются сами при первом запуске.
const fs = require('fs');
const path = require('path');
const { createClient } = require('@libsql/client');

const LOCAL = path.join(__dirname, 'data', 'cahier.db');
const DB_URL = process.env.TURSO_DATABASE_URL || 'file:' + LOCAL;
const remote = !DB_URL.startsWith('file:');
if (!remote && DB_URL === 'file:' + LOCAL) fs.mkdirSync(path.dirname(LOCAL), { recursive: true });

const client = createClient({ url: DB_URL, authToken: process.env.TURSO_AUTH_TOKEN || undefined });

const SCHEMA = [
  `CREATE TABLE IF NOT EXISTS users (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     login TEXT NOT NULL UNIQUE,
     pass_hash TEXT NOT NULL,
     created_at INTEGER NOT NULL
   )`,
  `CREATE TABLE IF NOT EXISTS sessions (
     token_hash TEXT PRIMARY KEY,
     user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
     created_at INTEGER NOT NULL,
     expires_at INTEGER NOT NULL
   )`,
  `CREATE INDEX IF NOT EXISTS ix_sessions_user ON sessions (user_id)`,
  // Прогресс по дням: один JSON-документ на человека; v — номер версии, защищает от затирания с другого устройства.
  `CREATE TABLE IF NOT EXISTS progress (
     user_id INTEGER PRIMARY KEY REFERENCES users (id) ON DELETE CASCADE,
     v INTEGER NOT NULL DEFAULT 1,
     data TEXT NOT NULL,
     updated_at INTEGER NOT NULL
   )`,
  // Карточки, тексты домашек, вставленные тексты и сохранённые переводы: coll — раздел, item_id — ключ внутри раздела.
  `CREATE TABLE IF NOT EXISTS items (
     user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
     coll TEXT NOT NULL,
     item_id TEXT NOT NULL,
     data TEXT NOT NULL,
     updated_at INTEGER NOT NULL,
     PRIMARY KEY (user_id, coll, item_id)
   )`,
];

let ready = false;
// Сервер поднимается сразу, а к базе переподключается сам, пока она не ответит.
async function init() {
  for (let n = 1; ; n++) {
    try {
      await client.batch(SCHEMA, 'write');
      ready = true;
      console.log(`[db] готово: ${remote ? DB_URL : "локальный файл " + DB_URL.slice(5)}`);
      return;
    } catch (e) {
      const hint = /\b401\b/.test(e.message || '') ? ' — проверь TURSO_AUTH_TOKEN: токен не задан или не подходит к этой базе' : '';
      console.error(`[db] база не отвечает (попытка ${n}): ${e.code || ''} ${e.message}${hint}`);
      await new Promise(r => setTimeout(r, Math.min(30000, 2000 * n)));
    }
  }
}

const result = rs => ({ changes: rs.rowsAffected, lastInsertRowid: rs.lastInsertRowid == null ? null : Number(rs.lastInsertRowid) });
const isUnique = e => !!e && (String(e.code || '').startsWith('SQLITE_CONSTRAINT') || /UNIQUE constraint failed/.test(e.message || ''));

module.exports = {
  init,
  isReady: () => ready,
  where: remote ? DB_URL : 'локальный файл',
  isUnique,
  get: async (sql, ...args) => (await client.execute({ sql, args })).rows[0],
  all: async (sql, ...args) => (await client.execute({ sql, args })).rows,
  run: async (sql, ...args) => result(await client.execute({ sql, args })),
  // Несколько записей одним неделимым действием: либо применится всё, либо ничего.
  // fn получает t.batch([{ sql, args }, …]) и t.get(sql, …args).
  async tx(fn) {
    const t = await client.transaction('write');
    try {
      const r = await fn({
        batch: stmts => t.batch(stmts),
        get: async (sql, ...args) => (await t.execute({ sql, args })).rows[0],
      });
      await t.commit();
      return r;
    } catch (e) { try { await t.rollback(); } catch (_) {} throw e; }
    finally { t.close(); }
  },
  close: () => client.close(),
};
