/**
 * AUTH SERVİSİ — backend API (server/index.js) ilə işləyir.
 *
 * Endpoint-lər (Vite dev rejimində /api → http://localhost:4000 proxy olunur):
 *   POST  /api/auth/register        { fullName, email, password }  → { user, token, devCode? }
 *   POST  /api/auth/login           { email, password }            → { user, token }
 *   POST  /api/auth/logout
 *   POST  /api/auth/verify-email    { code }                       → { user }
 *   POST  /api/auth/resend-code                                    → { ok, devCode? }
 *   GET   /api/me                                                  → { user }
 *   PATCH /api/me                   { fullName?, avatarUrl? }      → { user }
 *   POST  /api/me/password          { currentPassword, newPassword }
 *
 * Token və istifadəçi brauzerdə saxlanır («Məni xatırla» → localStorage, əks halda sessionStorage).
 * Real e-poçt hələ göndərilmir: təsdiq kodu server konsoluna yazılır, dev rejimində ekranda da göstərilir.
 */
import type { AuthUser } from '../types';

const SESSION_KEY = 'ca-session';
const TOKEN_KEY = 'ca-token';
const DEV_CODE_KEY = 'ca-dev-code';

export const VERIFICATION_CODE_LENGTH = 6;

export class AuthError extends Error {}

export interface RegisterInput {
  fullName: string;
  email: string;
  password: string;
}

function readJson<T>(storage: Storage, key: string): T | null {
  try {
    const raw = storage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : null;
  } catch {
    return null;
  }
}

function writeJson(storage: Storage, key: string, value: unknown) {
  try {
    storage.setItem(key, JSON.stringify(value));
  } catch {
    /* storage əlçatmazdırsa (məs. məxfi rejim) səssiz keç */
  }
}

function remove(key: string) {
  try {
    localStorage.removeItem(key);
    sessionStorage.removeItem(key);
  } catch {
    /* ignore */
  }
}

/** Sessiyanın saxlandığı yaddaş (localStorage — «məni xatırla») */
function activeStorage(): Storage {
  return readJson<string>(localStorage, TOKEN_KEY) ? localStorage : sessionStorage;
}

export function getToken(): string | null {
  return readJson<string>(localStorage, TOKEN_KEY) ?? readJson<string>(sessionStorage, TOKEN_KEY);
}

export function getSession(): AuthUser | null {
  return (
    readJson<AuthUser>(localStorage, SESSION_KEY) ?? readJson<AuthUser>(sessionStorage, SESSION_KEY)
  );
}

function saveSession(user: AuthUser, token: string, remember: boolean) {
  remove(SESSION_KEY);
  remove(TOKEN_KEY);
  const storage = remember ? localStorage : sessionStorage;
  writeJson(storage, TOKEN_KEY, token);
  writeJson(storage, SESSION_KEY, user);
}

function updateCachedUser(user: AuthUser) {
  writeJson(activeStorage(), SESSION_KEY, user);
}

/** Dev rejimində serverin qaytardığı son təsdiq kodu (real e-poçt olmadığı üçün) */
export function getDevVerificationCode(): string | null {
  return import.meta.env.DEV ? readJson<string>(sessionStorage, DEV_CODE_KEY) : null;
}

function rememberDevCode(code?: string) {
  if (code) writeJson(sessionStorage, DEV_CODE_KEY, code);
}

/** API sorğusu: xəta olduqda serverin mesajı ilə AuthError atır */
export async function api<T>(
  path: string,
  options: { method?: string; body?: unknown } = {},
): Promise<T> {
  const headers: Record<string, string> = { 'Content-Type': 'application/json' };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  let res: Response;
  try {
    res = await fetch(`/api${path}`, {
      method: options.method ?? 'GET',
      headers,
      body: options.body === undefined ? undefined : JSON.stringify(options.body),
    });
  } catch {
    throw new AuthError('Serverə qoşulmaq olmadı. «npm run dev» ilə serverin işlədiyini yoxlayın.');
  }

  const data = (await res.json().catch(() => ({}))) as T & { error?: string };
  if (!res.ok) {
    if (res.status === 401 && path !== '/auth/login') {
      remove(SESSION_KEY);
      remove(TOKEN_KEY);
    }
    throw new AuthError(data.error ?? 'Xəta baş verdi. Bir az sonra yenidən cəhd edin.');
  }
  return data;
}

export async function register(input: RegisterInput): Promise<AuthUser> {
  const data = await api<{ user: AuthUser; token: string; devCode?: string }>('/auth/register', {
    method: 'POST',
    body: input,
  });
  saveSession(data.user, data.token, true);
  rememberDevCode(data.devCode);
  return data.user;
}

export async function login(email: string, password: string, remember: boolean): Promise<AuthUser> {
  const data = await api<{ user: AuthUser; token: string }>('/auth/login', {
    method: 'POST',
    body: { email, password },
  });
  saveSession(data.user, data.token, remember);
  return data.user;
}

export function logout() {
  if (getToken()) void api('/auth/logout', { method: 'POST' }).catch(() => undefined);
  remove(SESSION_KEY);
  remove(TOKEN_KEY);
  remove(DEV_CODE_KEY);
}

export async function verifyEmail(code: string): Promise<AuthUser> {
  const data = await api<{ user: AuthUser }>('/auth/verify-email', {
    method: 'POST',
    body: { code },
  });
  updateCachedUser(data.user);
  remove(DEV_CODE_KEY);
  return data.user;
}

export async function resendVerificationCode(): Promise<void> {
  const data = await api<{ devCode?: string }>('/auth/resend-code', { method: 'POST' });
  rememberDevCode(data.devCode);
}

export async function updateProfile(patch: {
  fullName?: string;
  /** null = şəkli sil */
  avatarUrl?: string | null;
}): Promise<AuthUser> {
  const data = await api<{ user: AuthUser }>('/me', { method: 'PATCH', body: patch });
  updateCachedUser(data.user);
  return data.user;
}

export async function changePassword(currentPassword: string, newPassword: string): Promise<void> {
  await api('/me/password', { method: 'POST', body: { currentPassword, newPassword } });
}
