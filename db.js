'use strict';
// База данных: SQLite в одном файле (встроенный в Node модуль node:sqlite, без сторонних библиотек).
// Путь к файлу задаёт переменная DB_FILE. Таблицы создаются сами при первом запуске.
const fs = require('fs');
const path = require('path');
const { DatabaseSync } = require('node:sqlite');

const FILE = process.env.DB_FILE || path.join(__dirname, 'data', 'cahier.db');
if (FILE !== ':memory:') fs.mkdirSync(path.dirname(FILE), { recursive: true });

const db = new DatabaseSync(FILE);
db.exec(`
  PRAGMA journal_mode = WAL;
  PRAGMA synchronous = NORMAL;
  PRAGMA foreign_keys = ON;
  PRAGMA busy_timeout = 5000;

  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    pass_hash TEXT NOT NULL,
    created_at INTEGER NOT NULL
  );
  CREATE TABLE IF NOT EXISTS sessions (
    token_hash TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    created_at INTEGER NOT NULL,
    expires_at INTEGER NOT NULL
  );
  CREATE INDEX IF NOT EXISTS ix_sessions_user ON sessions (user_id);
  -- Прогресс по дням: один JSON-документ на человека; v — номер версии, защищает от затирания с другого устройства.
  CREATE TABLE IF NOT EXISTS progress (
    user_id INTEGER PRIMARY KEY REFERENCES users (id) ON DELETE CASCADE,
    v INTEGER NOT NULL DEFAULT 1,
    data TEXT NOT NULL,
    updated_at INTEGER NOT NULL
  );
  -- Карточки, тексты домашек, вставленные тексты и сохранённые переводы: coll — раздел, item_id — ключ внутри раздела.
  CREATE TABLE IF NOT EXISTS items (
    user_id INTEGER NOT NULL REFERENCES users (id) ON DELETE CASCADE,
    coll TEXT NOT NULL,
    item_id TEXT NOT NULL,
    data TEXT NOT NULL,
    updated_at INTEGER NOT NULL,
    PRIMARY KEY (user_id, coll, item_id)
  ) WITHOUT ROWID;
`);

const cache = new Map();
const stmt = sql => { let s = cache.get(sql); if (!s) { s = db.prepare(sql); cache.set(sql, s); } return s; };
const isUnique = e => !!e && (e.errcode === 2067 || e.errcode === 1555 || /UNIQUE constraint failed/.test(e.message || ''));

module.exports = {
  file: FILE,
  isUnique,
  get: (sql, ...p) => stmt(sql).get(...p),
  all: (sql, ...p) => stmt(sql).all(...p),
  run: (sql, ...p) => stmt(sql).run(...p),
  // Несколько записей одним неделимым действием: либо применится всё, либо ничего.
  tx(fn) {
    db.exec('BEGIN IMMEDIATE');
    try { const r = fn(); db.exec('COMMIT'); return r; }
    catch (e) { try { db.exec('ROLLBACK'); } catch (_) {} throw e; }
  },
  close() { try { db.exec('PRAGMA wal_checkpoint(TRUNCATE)'); } catch (_) {} db.close(); },
};
