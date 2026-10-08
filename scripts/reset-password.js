'use strict';
// Сброс пароля владельцем сайта: node scripts/reset-password.js <логин>
// Запускать там же, где лежит файл базы (на Render — во вкладке Shell сервиса).
// Печатает новый временный пароль и завершает все сессии этого человека.
const crypto = require('crypto');
const db = require('../db');

const login = String(process.argv[2] || '').trim().toLowerCase();
if (!login) { console.error('Укажи логин: node scripts/reset-password.js <логин>'); process.exit(1); }
const user = db.get('SELECT id FROM users WHERE login = ?', login);
if (!user) { console.error('Такого логина нет.'); process.exit(1); }
const password = crypto.randomBytes(9).toString('base64url');
const salt = crypto.randomBytes(16);
const key = crypto.scryptSync(password, salt, 64, { N: 16384, r: 8, p: 1 });
db.run('UPDATE users SET pass_hash = ? WHERE id = ?', ['scrypt', 16384, 8, 1, salt.toString('base64'), key.toString('base64')].join('$'), user.id);
db.run('DELETE FROM sessions WHERE user_id = ?', user.id);
db.close();
console.log(`Новый пароль для ${login}: ${password}`);
console.log('Передай его лично; после входа пароль меняется в панели аккаунта.');
