'use strict';
// Сброс пароля владельцем сайта. Нужен файл .env с адресом и токеном базы:
//   node --env-file=.env scripts/reset-password.js <логин>
// Печатает новый временный пароль и завершает все сессии этого человека.
const crypto = require('crypto');
const db = require('../db');

(async () => {
  const login = String(process.argv[2] || '').trim().toLowerCase();
  if (!login) { console.error('Укажи логин: node --env-file=.env scripts/reset-password.js <логин>'); process.exit(1); }
  const user = await db.get('SELECT id FROM users WHERE login = ?', login);
  if (!user) { console.error(`Логина «${login}» нет в базе: ${db.where}.`); process.exit(1); }
  const password = crypto.randomBytes(9).toString('base64url');
  const salt = crypto.randomBytes(16);
  const key = crypto.scryptSync(password, salt, 64, { N: 16384, r: 8, p: 1 });
  await db.run('UPDATE users SET pass_hash = ? WHERE id = ?', ['scrypt', 16384, 8, 1, salt.toString('base64'), key.toString('base64')].join('$'), user.id);
  await db.run('DELETE FROM sessions WHERE user_id = ?', user.id);
  console.log(`Новый пароль для ${login}: ${password}`);
  console.log('Передай его лично; после входа пароль меняется в панели аккаунта.');
  db.close();
})().catch(e => { console.error(e.message); process.exit(1); });
