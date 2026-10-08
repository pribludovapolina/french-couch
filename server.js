'use strict';
// Cahier de français: статический сайт + API (регистрация, вход, личный прогресс в базе Turso).
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const crypto = require('crypto');
const { promisify } = require('util');
const express = require('express');
const db = require('./db');

const PORT = Number(process.env.PORT) || 3000;
const PROD = process.env.NODE_ENV === 'production';
const INVITE = (process.env.INVITE_CODE || '').trim();
const MAX_USERS = Number(process.env.MAX_USERS) || 200;
const MAX_ITEMS = 5000;            // карточек и записей на одного человека
const MAX_ITEM_BYTES = 256 * 1024; // одна запись
const MAX_PROGRESS_BYTES = 1024 * 1024;
const SESSION_DAYS = 60;
const COOKIE = 'cahier_sid';
const COLLS = new Set(['cards', 'texts', 'pasted', 'gloss']);

/* ---------------- пароли: scrypt из стандартной библиотеки ---------------- */
const scrypt = promisify(crypto.scrypt);
const SCRYPT = { N: 16384, r: 8, p: 1 };
async function hashPassword(password) {
  const salt = crypto.randomBytes(16);
  const key = await scrypt(password.normalize('NFKC'), salt, 64, SCRYPT);
  return ['scrypt', SCRYPT.N, SCRYPT.r, SCRYPT.p, salt.toString('base64'), key.toString('base64')].join('$');
}
async function verifyPassword(password, stored) {
  const [alg, N, r, p, salt, hash] = String(stored).split('$');
  if (alg !== 'scrypt' || !salt || !hash) return false;
  const want = Buffer.from(hash, 'base64');
  const got = await scrypt(password.normalize('NFKC'), Buffer.from(salt, 'base64'), want.length, { N: Number(N), r: Number(r), p: Number(p) });
  return crypto.timingSafeEqual(want, got);
}
// Хэш несуществующего пароля: чтобы вход с неизвестным логином занимал столько же времени, сколько с известным.
const DUMMY_HASH = hashPassword(crypto.randomBytes(18).toString('base64'));

const sha256 = s => crypto.createHash('sha256').update(s).digest('hex');
const safeEqual = (a, b) => { const x = Buffer.from(sha256(a)), y = Buffer.from(sha256(b)); return crypto.timingSafeEqual(x, y); };

/* ---------------- ограничение частоты (в памяти процесса) ---------------- */
const hits = new Map();
function tooMany(key, max) {
  const now = Date.now(); const h = hits.get(key);
  return !!h && h.reset > now && h.n >= max;
}
function hit(key, windowMs) {
  const now = Date.now(); const h = hits.get(key);
  if (!h || h.reset <= now) hits.set(key, { n: 1, reset: now + windowMs }); else h.n++;
}
setInterval(() => { const now = Date.now(); for (const [k, h] of hits) if (h.reset <= now) hits.delete(k); }, 10 * 60 * 1000).unref();
const MIN15 = 15 * 60 * 1000, HOUR = 60 * 60 * 1000;

/* ---------------- статика: файлы из public/ в памяти, со сжатием ---------------- */
const TYPES = { '.html': 'text/html; charset=utf-8', '.json': 'application/json; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon', '.webmanifest': 'application/manifest+json', '.txt': 'text/plain; charset=utf-8' };
const FILES = new Map();
(function loadStatic(dir, prefix) {
  for (const f of fs.readdirSync(dir, { withFileTypes: true })) {
    if (f.name.startsWith('.')) continue;
    const full = path.join(dir, f.name);
    if (f.isDirectory()) { loadStatic(full, prefix + f.name + '/'); continue; }
    const buf = fs.readFileSync(full); const ext = path.extname(f.name).toLowerCase();
    const text = /^(text\/|application\/(json|manifest)|image\/svg)/.test(TYPES[ext] || '');
    FILES.set(prefix + f.name, { buf, gz: text ? zlib.gzipSync(buf, { level: 9 }) : null, type: TYPES[ext] || 'application/octet-stream', etag: '"' + sha256(buf).slice(0, 20) + '"' });
  }
})(path.join(__dirname, 'public'), '/');
async function serveStatic(req, res, next) {
  if (req.method !== 'GET' && req.method !== 'HEAD') return next();
  const f = FILES.get(req.path === '/' ? '/index.html' : req.path);
  if (!f) return next();
  const closed = req.path.startsWith('/data/'); // уроки отдаём только вошедшим
  if (closed) {
    if (!db.isReady()) return res.status(503).json({ error: 'db_unavailable' });
    if (!(await currentUser(req, res))) return res.status(401).json({ error: 'unauthorized' });
  }
  res.set({ 'Content-Type': f.type, ETag: f.etag, 'Cache-Control': closed ? 'private, no-cache' : 'no-cache', Vary: 'Accept-Encoding' });
  if (req.headers['if-none-match'] === f.etag) return res.status(304).end();
  const gz = f.gz && /\bgzip\b/.test(req.headers['accept-encoding'] || '');
  if (gz) res.set('Content-Encoding', 'gzip');
  res.end(req.method === 'HEAD' ? undefined : gz ? f.gz : f.buf);
}

/* ---------------- приложение ---------------- */
const app = express();
app.disable('x-powered-by');
app.set('trust proxy', 1); // Render отдаёт сайт через свой прокси

app.use((req, res, next) => {
  res.set({
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; media-src 'self' blob:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self'",
  });
  if (PROD) res.set('Strict-Transport-Security', 'max-age=15552000');
  next();
});

app.get('/healthz', (req, res) => res.json({ ok: true, db: db.isReady() }));
app.use(serveStatic);

const api = express.Router();
app.use('/api', api);
api.use((req, res, next) => {
  res.set('Cache-Control', 'no-store');
  if (!db.isReady()) return res.status(503).json({ error: 'db_unavailable' });
  // Изменяющие запросы принимаем только от своей страницы: чужой сайт не сможет поставить этот заголовок.
  if (req.method !== 'GET' && req.method !== 'HEAD') {
    if (req.headers['x-cahier'] !== '1') return res.status(403).json({ error: 'forbidden' });
    const origin = req.headers.origin;
    if (origin) { let host = ''; try { host = new URL(origin).host; } catch (e) {} if (host !== req.headers.host) return res.status(403).json({ error: 'forbidden' }); }
  }
  next();
});
api.use(express.json({ limit: '3mb' }));

/* ---------------- сессии ---------------- */
function readCookie(req, name) {
  for (const part of String(req.headers.cookie || '').split(';')) {
    const i = part.indexOf('='); if (i < 0) continue;
    if (part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return '';
}
function setCookie(req, res, token, maxAgeSec) {
  const secure = PROD || req.secure;
  res.append('Set-Cookie', `${COOKIE}=${token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=${maxAgeSec}${secure ? '; Secure' : ''}`);
}
const DAY = 86400000;
async function startSession(req, res, userId) {
  const token = crypto.randomBytes(32).toString('base64url'), now = Date.now();
  await db.run('INSERT INTO sessions (token_hash, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)', sha256(token), userId, now, now + SESSION_DAYS * DAY);
  setCookie(req, res, token, SESSION_DAYS * 86400);
  db.run('DELETE FROM sessions WHERE expires_at < ?', now).catch(() => {});
}
async function currentUser(req, res) {
  const token = readCookie(req, COOKIE);
  if (!/^[A-Za-z0-9_-]{40,64}$/.test(token)) return null;
  const th = sha256(token), now = Date.now();
  const row = await db.get('SELECT u.id, u.login, s.expires_at FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ? AND s.expires_at > ?', th, now);
  if (!row) return null;
  if (row.expires_at - now < SESSION_DAYS * DAY / 2) { // продлеваем, пока человек пользуется сайтом
    await db.run('UPDATE sessions SET expires_at = ? WHERE token_hash = ?', now + SESSION_DAYS * DAY, th);
    setCookie(req, res, token, SESSION_DAYS * 86400);
  }
  return { id: row.id, login: row.login, tokenHash: th };
}
async function auth(req, res, next) {
  const u = await currentUser(req, res);
  if (!u) return res.status(401).json({ error: 'unauthorized' });
  req.user = u; next();
}

/* ---------------- регистрация и вход ---------------- */
const LOGIN_RE = /^[a-z0-9][a-z0-9_.-]{2,31}$/;
const normLogin = s => String(s == null ? '' : s).trim().toLowerCase();
const validPassword = p => typeof p === 'string' && p.length >= 8 && p.length <= 200;

api.get('/me', async (req, res) => {
  const u = await currentUser(req, res);
  res.json({ user: u ? { login: u.login } : null, invite: !!INVITE });
});

api.post('/register', async (req, res) => {
  const ipKey = 'reg:' + req.ip;
  if (tooMany(ipKey, 8)) return res.status(429).json({ error: 'rate_limited' });
  hit(ipKey, HOUR);
  const login = normLogin(req.body && req.body.login), password = req.body && req.body.password;
  if (!LOGIN_RE.test(login)) return res.status(400).json({ error: 'bad_login' });
  if (!validPassword(password)) return res.status(400).json({ error: 'bad_password' });
  if (INVITE && !safeEqual(String((req.body && req.body.invite) || '').trim(), INVITE)) return res.status(403).json({ error: 'bad_invite' });
  if ((await db.get('SELECT COUNT(*) AS n FROM users')).n >= MAX_USERS) return res.status(403).json({ error: 'registration_closed' });
  if (await db.get('SELECT 1 AS x FROM users WHERE login = ?', login)) return res.status(409).json({ error: 'login_taken' });
  const hash = await hashPassword(password);
  let id;
  try { id = (await db.run('INSERT INTO users (login, pass_hash, created_at) VALUES (?, ?, ?)', login, hash, Date.now())).lastInsertRowid; }
  catch (e) { if (db.isUnique(e)) return res.status(409).json({ error: 'login_taken' }); throw e; }
  await startSession(req, res, id);
  res.json({ user: { login } });
});

api.post('/login', async (req, res) => {
  const login = normLogin(req.body && req.body.login), password = req.body && req.body.password;
  const ipKey = 'login-ip:' + req.ip, userKey = 'login-user:' + login;
  if (tooMany(ipKey, 30) || tooMany(userKey, 10)) return res.status(429).json({ error: 'rate_limited' });
  let user = null;
  if (LOGIN_RE.test(login) && typeof password === 'string' && password.length <= 200) {
    const row = await db.get('SELECT id, login, pass_hash FROM users WHERE login = ?', login);
    const ok = await verifyPassword(password, row ? row.pass_hash : await DUMMY_HASH);
    if (ok && row) user = row;
  }
  if (!user) { hit(ipKey, MIN15); hit(userKey, MIN15); return res.status(401).json({ error: 'bad_credentials' }); }
  await startSession(req, res, user.id);
  res.json({ user: { login: user.login } });
});

api.post('/logout', async (req, res) => {
  const token = readCookie(req, COOKIE);
  if (token) await db.run('DELETE FROM sessions WHERE token_hash = ?', sha256(token));
  setCookie(req, res, '', 0);
  res.json({ ok: true });
});

api.post('/password', auth, async (req, res) => {
  const key = 'pw:' + req.user.id;
  if (tooMany(key, 10)) return res.status(429).json({ error: 'rate_limited' });
  const { old, password } = req.body || {};
  if (!validPassword(password)) return res.status(400).json({ error: 'bad_password' });
  const row = await db.get('SELECT pass_hash FROM users WHERE id = ?', req.user.id);
  if (typeof old !== 'string' || old.length > 200 || !(await verifyPassword(old, row.pass_hash))) { hit(key, MIN15); return res.status(401).json({ error: 'bad_credentials' }); }
  const hash = await hashPassword(password);
  await db.run('UPDATE users SET pass_hash = ? WHERE id = ?', hash, req.user.id);
  await db.run('DELETE FROM sessions WHERE user_id = ? AND token_hash <> ?', req.user.id, req.user.tokenHash); // выходим на остальных устройствах
  res.json({ ok: true });
});

/* ---------------- личные данные ---------------- */
const parse = s => { try { return JSON.parse(s); } catch (e) { return null; } };

api.get('/state', auth, async (req, res) => {
  const p = await db.get('SELECT v, data FROM progress WHERE user_id = ?', req.user.id);
  const out = { user: { login: req.user.login }, progress: (p && parse(p.data)) || { days: {} }, v: p ? p.v : 0, cards: {}, texts: {}, pasted: {}, gloss: {} };
  const rows = await db.all('SELECT coll, item_id, data FROM items WHERE user_id = ?', req.user.id);
  for (const r of rows) { const d = parse(r.data); if (d != null && out[r.coll]) out[r.coll][r.item_id] = d; }
  res.json(out);
});

// Прогресс сохраняется целиком. base — версия, которую видел браузер: если с другого устройства уже
// сохранили более новую, отвечаем 409 и отдаём её, а страница сливает изменения и повторяет запрос.
api.put('/progress', auth, async (req, res) => {
  const { data, base } = req.body || {};
  if (!data || typeof data !== 'object' || Array.isArray(data) || !Number.isInteger(base) || base < 0) return res.status(400).json({ error: 'bad_request' });
  const json = JSON.stringify(data);
  if (Buffer.byteLength(json) > MAX_PROGRESS_BYTES) return res.status(413).json({ error: 'too_large' });
  const now = Date.now();
  const r = base === 0
    ? await db.run('INSERT INTO progress (user_id, v, data, updated_at) VALUES (?, 1, ?, ?) ON CONFLICT (user_id) DO NOTHING', req.user.id, json, now)
    : await db.run('UPDATE progress SET data = ?, v = v + 1, updated_at = ? WHERE user_id = ? AND v = ?', json, now, req.user.id, base);
  if (r.changes === 1) return res.json({ v: base + 1 });
  const cur = await db.get('SELECT v, data FROM progress WHERE user_id = ?', req.user.id);
  res.status(409).json({ error: 'conflict', v: cur ? cur.v : 0, data: (cur && parse(cur.data)) || { days: {} } });
});

// Карточки и остальные записи: put — создать или заменить, del — удалить. Одним запросом можно прислать пачку.
const validId = id => typeof id === 'string' && id.length >= 1 && id.length <= 128 && !/[\u0000-\u001f]/.test(id);
api.post('/items', auth, async (req, res) => {
  const put = Array.isArray(req.body && req.body.put) ? req.body.put : [], del = Array.isArray(req.body && req.body.del) ? req.body.del : [];
  if (put.length + del.length === 0 || put.length + del.length > 1000) return res.status(400).json({ error: 'bad_request' });
  const rows = [];
  for (const it of put) {
    if (!it || !COLLS.has(it.c) || !validId(it.id) || it.d == null || typeof it.d !== 'object') return res.status(400).json({ error: 'bad_request' });
    const json = JSON.stringify(it.d);
    if (Buffer.byteLength(json) > MAX_ITEM_BYTES) return res.status(413).json({ error: 'too_large' });
    rows.push([it.c, it.id, json]);
  }
  for (const it of del) if (!it || !COLLS.has(it.c) || !validId(it.id)) return res.status(400).json({ error: 'bad_request' });
  const uid = req.user.id, now = Date.now();
  const stmts = [
    ...del.map(it => ({ sql: 'DELETE FROM items WHERE user_id = ? AND coll = ? AND item_id = ?', args: [uid, it.c, it.id] })),
    ...rows.map(([c, id, json]) => ({ sql: 'INSERT INTO items (user_id, coll, item_id, data, updated_at) VALUES (?, ?, ?, ?, ?) ON CONFLICT (user_id, coll, item_id) DO UPDATE SET data = excluded.data, updated_at = excluded.updated_at', args: [uid, c, id, json, now] })),
  ];
  try {
    await db.tx(async t => {
      await t.batch(stmts);
      if (rows.length && (await t.get('SELECT COUNT(*) AS n FROM items WHERE user_id = ?', uid)).n > MAX_ITEMS) throw { quota: true };
    });
  } catch (e) { if (e && e.quota) return res.status(413).json({ error: 'quota' }); throw e; }
  res.json({ ok: true });
});

api.use((req, res) => res.status(404).json({ error: 'not_found' }));
app.use((req, res) => res.status(404).type('text/plain; charset=utf-8').send('Страница не найдена'));
app.use((err, req, res, next) => { // eslint-disable-line no-unused-vars
  if (err && (err.type === 'entity.parse.failed' || err.type === 'entity.too.large')) return res.status(err.status || 400).json({ error: 'bad_request' });
  console.error('[error]', req.method, req.path, err && (err.code || ''), err && err.message);
  res.status(500).json({ error: 'server_error' });
});

const server = app.listen(PORT, '0.0.0.0', () => console.log(`[web] слушаю порт ${PORT}, база: ${db.where}${INVITE ? ', регистрация по коду приглашения' : ', регистрация открыта'}`));
db.init();
for (const sig of ['SIGTERM', 'SIGINT']) process.on(sig, () => { server.close(() => { try { db.close(); } catch (e) {} process.exit(0); }); setTimeout(() => process.exit(0), 8000).unref(); });
