// AI Coding
/**
 * @file bootstrap-roles.ts
 * @description Tao ba DB role ung dung cua SDD §7.4 tu bien moi truong.
 *
 * Viec nay tach khoi migration vi migration la SQL tho va khong doc duoc bien
 * moi truong — nhet mat khau vao file SQL se dua secret vao git (security.md §2).
 * Lenh nay idempotent: chay lai chi cap nhat mat khau.
 *
 * ⚠️ Role thu nam `app_operator` (endpoint admin takedown TD-2/TD-3) CHUA co o
 * day: SDD §7.4 ghi no la no ky thuat dang cho Architect, va them mot role xuyen
 * tenant truoc khi mo hinh quyen duoc chot la viec khong dao nguoc duoc.
 */

import type { Pool } from 'pg';

import type { DatabaseBootstrapEnv } from '../config/env';
import type { Logger } from '../logging/logger';

type RoleSpec = { readonly name: string; readonly password: string };

const rolesFrom = (env: DatabaseBootstrapEnv): RoleSpec[] => [
  { name: 'app_api', password: env.DB_APP_API_PASSWORD },
  { name: 'app_worker', password: env.DB_APP_WORKER_PASSWORD },
  { name: 'app_public_intake', password: env.DB_APP_PUBLIC_INTAKE_PASSWORD },
];

/**
 * DDL khong nhan tham so binding, nen ten role va mat khau buoc phai di vao cau
 * lenh duoi dang van ban. `quote_ident`/`quote_literal` de chinh PostgreSQL lam
 * viec escape thay vi tu noi chuoi o phia Node.
 */
const quoteForDdl = async (
  pool: Pool,
  role: RoleSpec,
): Promise<{ ident: string; literal: string }> => {
  const result = await pool.query<{ ident: string; literal: string }>(
    'SELECT quote_ident($1) AS ident, quote_literal($2) AS literal',
    [role.name, role.password],
  );
  const quoted = result.rows[0];

  if (quoted === undefined) {
    throw new Error(`Khong lay duoc dinh danh da escape cho role "${role.name}"`);
  }

  return quoted;
};

const roleExists = async (pool: Pool, name: string): Promise<boolean> => {
  const result = await pool.query('SELECT 1 FROM pg_roles WHERE rolname = $1', [name]);
  return (result.rowCount ?? 0) > 0;
};

export const bootstrapRoles = async (
  pool: Pool,
  env: DatabaseBootstrapEnv,
  logger: Logger,
): Promise<void> => {
  for (const role of rolesFrom(env)) {
    const { ident, literal } = await quoteForDdl(pool, role);
    const exists = await roleExists(pool, role.name);
    const verb = exists ? 'ALTER' : 'CREATE';

    await pool.query(`${verb} ROLE ${ident} WITH LOGIN PASSWORD ${literal}`);
    logger.info({ role: role.name, action: verb }, 'Da dong bo DB role');
  }
};
