// SQLite verilənlər bazası (Node 22.22+ daxili node:sqlite modulu, əlavə paket lazım deyil).
import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const file = process.env.DB_FILE ?? resolve(root, 'server', 'data', 'career-arena.db');
if (file !== ':memory:') mkdirSync(dirname(file), { recursive: true });

export const db = new DatabaseSync(file);
db.exec('PRAGMA journal_mode = WAL; PRAGMA foreign_keys = ON;');

db.exec(`
  CREATE TABLE IF NOT EXISTS users (
    id              TEXT PRIMARY KEY,
    full_name       TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    email_verified  INTEGER NOT NULL DEFAULT 0,
    avatar_url      TEXT,
    plan            TEXT NOT NULL DEFAULT 'free',
    created_at      TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS sessions (
    token_hash  TEXT PRIMARY KEY,
    user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TEXT NOT NULL,
    expires_at  TEXT NOT NULL
  );

  CREATE TABLE IF NOT EXISTS verification_codes (
    user_id     TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    code_hash   TEXT NOT NULL,
    expires_at  TEXT NOT NULL,
    attempts    INTEGER NOT NULL DEFAULT 0
  );

  CREATE TABLE IF NOT EXISTS results (
    id            TEXT PRIMARY KEY,
    user_id       TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    grade         INTEGER NOT NULL,
    subject_id    TEXT NOT NULL,
    section_id    TEXT,
    total         INTEGER NOT NULL,
    correct       INTEGER NOT NULL,
    wrong         INTEGER NOT NULL,
    blank         INTEGER NOT NULL,
    percent       INTEGER NOT NULL,
    used_sec      INTEGER NOT NULL,
    end_reason    TEXT NOT NULL,
    violations    INTEGER NOT NULL DEFAULT 0,
    created_at    TEXT NOT NULL
  );
  CREATE INDEX IF NOT EXISTS idx_results_user ON results(user_id, created_at);
`);
