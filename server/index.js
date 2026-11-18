// Career Arena API serveri — xarici paket istifadə etmir (node:http + node:sqlite + node:crypto).
// İşə salmaq: `npm run server` (yalnız API) və ya `npm run dev` (API + Vite).
import { createServer } from 'node:http';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { extname, join, normalize, resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash, randomBytes, randomInt, randomUUID, scrypt, timingSafeEqual } from 'node:crypto';
import { promisify } from 'node:util';
import { db } from './db.js';

const PORT = Number(process.env.PORT ?? 4000);
const IS_PROD = process.env.NODE_ENV === 'production' || process.argv.includes('--prod');
const SESSION_DAYS = 30;
const CODE_MINUTES = 15;
const MAX_CODE_ATTEMPTS = 5;
const DIST = resolve(dirname(fileURLToPath(import.meta.url)), '..', 'dist');
const scryptAsync = promisify(scrypt);

class HttpError extends Error {
  constructor(status, message) {
    super(message);
    this.status = status;
  }
}

// ---------- köməkçilər ----------

const now = () => new Date().toISOString();
const inMinutes = (m) => new Date(Date.now() + m * 60_000).toISOString();
const sha256 = (s) => createHash('sha256').update(s).digest('hex');
const normalizeEmail = (e) => String(e ?? '').trim().toLowerCase();
const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

async function hashPassword(password) {
  const salt = randomBytes(16).toString('hex');
  const key = await scryptAsync(password, salt, 64);
  return `${salt}:${key.toString('hex')}`;
}

async function verifyPassword(password, stored) {
  const [salt, hex] = stored.split(':');
  const key = await scryptAsync(password, salt, 64);
  const expected = Buffer.from(hex, 'hex');
  return expected.length === key.length && timingSafeEqual(expected, key);
}

function toUser(row) {
  return {
    id: row.id,
    fullName: row.full_name,
    email: row.email,
    createdAt: row.created_at,
    emailVerified: !!row.email_verified,
    ...(row.avatar_url ? { avatarUrl: row.avatar_url } : {}),
    plan: row.plan,
  };
}

function createSession(userId) {
  const token = randomBytes(32).toString('hex');
  db.prepare('INSERT INTO sessions (token_hash, user_id, created_at, expires_at) VALUES (?, ?, ?, ?)').run(
    sha256(token),
    userId,
    now(),
    inMinutes(SESSION_DAYS * 24 * 60),
  );
  return token;
}

/** Yeni təsdiq kodu yaradır. Real e-poçt göndərilmir: kod server konsoluna yazılır, dev rejimində cavabda da qaytarılır. */
function issueCode(user) {
  const code = String(randomInt(0, 1_000_000)).padStart(6, '0');
  db.prepare(
    `INSERT INTO verification_codes (user_id, code_hash, expires_at, attempts) VALUES (?, ?, ?, 0)
     ON CONFLICT(user_id) DO UPDATE SET code_hash = excluded.code_hash, expires_at = excluded.expires_at, attempts = 0`,
  ).run(user.id, sha256(code), inMinutes(CODE_MINUTES));
  console.log(`[e-poçt] ${user.email} üçün təsdiq kodu: ${code}`);
  return IS_PROD ? {} : { devCode: code };
}

function currentUser(req) {
  const header = req.headers.authorization ?? '';
  const token = header.startsWith('Bearer ') ? header.slice(7) : '';
  if (!token) throw new HttpError(401, 'Sessiya bitib. Yenidən daxil olun.');
  const row = db
    .prepare(
      `SELECT u.* FROM sessions s JOIN users u ON u.id = s.user_id
       WHERE s.token_hash = ? AND s.expires_at > ?`,
    )
    .get(sha256(token), now());
  if (!row) throw new HttpError(401, 'Sessiya bitib. Yenidən daxil olun.');
  return { row, tokenHash: sha256(token) };
}

async function readBody(req) {
  const chunks = [];
  let size = 0;
  for await (const chunk of req) {
    size += chunk.length;
    if (size > 3_000_000) throw new HttpError(413, 'Sorğu çox böyükdür.');
    chunks.push(chunk);
  }
  if (!chunks.length) return {};
  try {
    return JSON.parse(Buffer.concat(chunks).toString('utf8'));
  } catch {
    throw new HttpError(400, 'Yanlış JSON.');
  }
}

function send(res, status, body) {
  res.writeHead(status, { 'Content-Type': 'application/json; charset=utf-8' });
  res.end(JSON.stringify(body));
}

// ---------- marşrutlar ----------

const routes = {
  'POST /api/auth/register': async (req) => {
    const { fullName, email, password } = await readBody(req);
    const name = String(fullName ?? '').trim();
    const mail = normalizeEmail(email);
    if (name.length < 2) throw new HttpError(400, 'Ad və soyadı daxil edin.');
    if (!EMAIL_RE.test(mail)) throw new HttpError(400, 'E-poçt ünvanı düzgün deyil.');
    if (String(password ?? '').length < 8) throw new HttpError(400, 'Şifrə ən azı 8 simvol olmalıdır.');
    if (db.prepare('SELECT 1 FROM users WHERE email = ?').get(mail)) {
      throw new HttpError(409, 'Bu e-poçt artıq qeydiyyatdan keçib. Daxil olmağa cəhd edin.');
    }
    const id = randomUUID();
    db.prepare(
      'INSERT INTO users (id, full_name, email, password_hash, created_at) VALUES (?, ?, ?, ?, ?)',
    ).run(id, name, mail, await hashPassword(String(password)), now());
    const row = db.prepare('SELECT * FROM users WHERE id = ?').get(id);
    return [201, { user: toUser(row), token: createSession(id), ...issueCode(row) }];
  },

  'POST /api/auth/login': async (req) => {
    const { email, password } = await readBody(req);
    const row = db.prepare('SELECT * FROM users WHERE email = ?').get(normalizeEmail(email));
    if (!row || !(await verifyPassword(String(password ?? ''), row.password_hash))) {
      throw new HttpError(401, 'E-poçt və ya şifrə yanlışdır.');
    }
    return [200, { user: toUser(row), token: createSession(row.id) }];
  },

  'POST /api/auth/logout': async (req) => {
    const { tokenHash } = currentUser(req);
    db.prepare('DELETE FROM sessions WHERE token_hash = ?').run(tokenHash);
    return [200, { ok: true }];
  },

  'POST /api/auth/verify-email': async (req) => {
    const { row } = currentUser(req);
    const { code } = await readBody(req);
    const vc = db.prepare('SELECT * FROM verification_codes WHERE user_id = ?').get(row.id);
    if (!vc || vc.expires_at < now()) throw new HttpError(400, 'Kodun vaxtı bitib. Yeni kod göndərin.');
    if (vc.attempts >= MAX_CODE_ATTEMPTS) throw new HttpError(429, 'Cəhdlər bitdi. Yeni kod göndərin.');
    if (sha256(String(code ?? '')) !== vc.code_hash) {
      db.prepare('UPDATE verification_codes SET attempts = attempts + 1 WHERE user_id = ?').run(row.id);
      throw new HttpError(400, 'Kod yanlışdır. Yenidən yoxlayın.');
    }
    db.prepare('UPDATE users SET email_verified = 1 WHERE id = ?').run(row.id);
    db.prepare('DELETE FROM verification_codes WHERE user_id = ?').run(row.id);
    return [200, { user: toUser(db.prepare('SELECT * FROM users WHERE id = ?').get(row.id)) }];
  },

  'POST /api/auth/resend-code': async (req) => {
    const { row } = currentUser(req);
    return [200, { ok: true, ...issueCode(row) }];
  },

  'GET /api/me': async (req) => [200, { user: toUser(currentUser(req).row) }],

  'PATCH /api/me': async (req) => {
    const { row } = currentUser(req);
    const body = await readBody(req);
    if (body.fullName !== undefined) {
      const name = String(body.fullName).trim();
      if (name.length < 2) throw new HttpError(400, 'Ad ən azı 2 simvol olmalıdır.');
      db.prepare('UPDATE users SET full_name = ? WHERE id = ?').run(name, row.id);
    }
    if (body.avatarUrl !== undefined) {
      const url = body.avatarUrl === null ? null : String(body.avatarUrl);
      if (url && !url.startsWith('data:image/')) throw new HttpError(400, 'Şəkil formatı dəstəklənmir.');
      db.prepare('UPDATE users SET avatar_url = ? WHERE id = ?').run(url, row.id);
    }
    return [200, { user: toUser(db.prepare('SELECT * FROM users WHERE id = ?').get(row.id)) }];
  },

  'POST /api/me/password': async (req) => {
    const { row } = currentUser(req);
    const { currentPassword, newPassword } = await readBody(req);
    if (!(await verifyPassword(String(currentPassword ?? ''), row.password_hash))) {
      throw new HttpError(400, 'Cari şifrə yanlışdır.');
    }
    if (String(newPassword ?? '').length < 8) throw new HttpError(400, 'Yeni şifrə ən azı 8 simvol olmalıdır.');
    db.prepare('UPDATE users SET password_hash = ? WHERE id = ?').run(await hashPassword(String(newPassword)), row.id);
    return [200, { ok: true }];
  },

  'POST /api/results': async (req) => {
    const { row } = currentUser(req);
    const b = await readBody(req);
    const int = (v, min = 0, max = 10_000) => Math.min(max, Math.max(min, Math.round(Number(v) || 0)));
    const grade = int(b.grade, 9, 11);
    const total = int(b.total, 1, 200);
    const correct = int(b.correct, 0, total);
    const wrong = int(b.wrong, 0, total - correct);
    const result = {
      // Eyni sessiya ikinci dəfə yazılmasın; fərqli istifadəçilərin id-ləri toqquşmasın
      id: sha256(`${row.id}:${String(b.sessionId ?? randomUUID())}`).slice(0, 32),
      grade,
      subjectId: ['math', 'aze', 'eng'].includes(b.subjectId) ? b.subjectId : 'math',
      sectionId: b.sectionId ? String(b.sectionId).slice(0, 80) : null,
      total,
      correct,
      wrong,
      blank: total - correct - wrong,
      percent: Math.round((correct / total) * 100),
      usedSec: int(b.usedSec, 0, 24 * 3600),
      endReason: ['manual', 'time', 'tab-switch'].includes(b.endReason) ? b.endReason : 'manual',
      violations: int(b.violations, 0, 100),
    };
    db.prepare(
      `INSERT OR IGNORE INTO results (id, user_id, grade, subject_id, section_id, total, correct, wrong, blank,
        percent, used_sec, end_reason, violations, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    ).run(
      result.id, row.id, result.grade, result.subjectId, result.sectionId, result.total, result.correct,
      result.wrong, result.blank, result.percent, result.usedSec, result.endReason, result.violations, now(),
    );
    return [201, { result }];
  },

  'GET /api/results': async (req) => {
    const { row } = currentUser(req);
    const rows = db
      .prepare('SELECT * FROM results WHERE user_id = ? ORDER BY created_at DESC LIMIT 100')
      .all(row.id);
    return [200, { results: rows.map(mapResult) }];
  },

  'GET /api/ranking': async (req) => {
    const url = new URL(req.url, 'http://x');
    const subject = url.searchParams.get('subject');
    const grade = Number(url.searchParams.get('grade')) || null;
    const where = [];
    const params = [];
    if (subject && ['math', 'aze', 'eng'].includes(subject)) {
      where.push('r.subject_id = ?');
      params.push(subject);
    }
    if (grade) {
      where.push('r.grade = ?');
      params.push(grade);
    }
    const rows = db
      .prepare(
        `SELECT u.id, u.full_name, u.avatar_url, COUNT(r.id) AS exams, SUM(r.correct) AS correct,
                ROUND(AVG(r.percent)) AS avg_percent
         FROM results r JOIN users u ON u.id = r.user_id
         ${where.length ? `WHERE ${where.join(' AND ')}` : ''}
         GROUP BY u.id ORDER BY correct DESC, avg_percent DESC LIMIT 50`,
      )
      .all(...params);
    return [
      200,
      {
        ranking: rows.map((r, i) => ({
          rank: i + 1,
          userId: r.id,
          fullName: r.full_name,
          avatarUrl: r.avatar_url ?? undefined,
          exams: r.exams,
          correct: r.correct,
          avgPercent: r.avg_percent,
        })),
      },
    ];
  },

  'GET /api/health': async () => [200, { ok: true }],
};

function mapResult(r) {
  return {
    id: r.id,
    grade: r.grade,
    subjectId: r.subject_id,
    sectionId: r.section_id,
    total: r.total,
    correct: r.correct,
    wrong: r.wrong,
    blank: r.blank,
    percent: r.percent,
    usedSec: r.used_sec,
    endReason: r.end_reason,
    violations: r.violations,
    createdAt: r.created_at,
  };
}

// ---------- statik fayllar (production: npm start) ----------

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.json': 'application/json',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
};

function serveStatic(req, res) {
  if (!existsSync(DIST)) return false;
  const pathname = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  let file = normalize(join(DIST, pathname));
  if (!file.startsWith(DIST)) return false;
  if (!existsSync(file) || statSync(file).isDirectory()) file = join(DIST, 'index.html'); // SPA
  res.writeHead(200, { 'Content-Type': MIME[extname(file)] ?? 'application/octet-stream' });
  createReadStream(file).pipe(res);
  return true;
}

// ---------- server ----------

const server = createServer(async (req, res) => {
  const path = new URL(req.url, 'http://x').pathname;
  const handler = routes[`${req.method} ${path}`];
  try {
    if (handler) {
      const [status, body] = await handler(req);
      return send(res, status, body);
    }
    if (path.startsWith('/api/')) throw new HttpError(404, 'Belə endpoint yoxdur.');
    if (req.method === 'GET' && serveStatic(req, res)) return;
    throw new HttpError(404, 'Tapılmadı.');
  } catch (err) {
    if (err instanceof HttpError) return send(res, err.status, { error: err.message });
    console.error(err);
    return send(res, 500, { error: 'Serverdə xəta baş verdi.' });
  }
});

// Vaxtı keçmiş sessiyaları təmizlə
db.prepare('DELETE FROM sessions WHERE expires_at < ?').run(now());

server.listen(PORT, () => {
  console.log(`Career Arena API: http://localhost:${PORT}/api`);
  if (existsSync(DIST) && IS_PROD) console.log(`Sayt: http://localhost:${PORT}`);
});
