// AI Coding
/**
 * @file pool.ts
 * @description Tao connection pool theo tung DB role cua SDD §7.4. Bon role la
 * bon danh tinh tach bach, nen chung la bon pool tach bach — dung chung mot pool
 * roi doi quyen luc chay se pha chinh mo hinh phan quyen do.
 */

import { Pool } from 'pg';

import type { DatabaseEnv } from '../config/env';

export type DatabaseRole = 'owner' | 'api' | 'worker' | 'public_intake';

const CONNECTION_STRING_BY_ROLE: Record<DatabaseRole, keyof DatabaseEnv> = {
  owner: 'DATABASE_URL_OWNER',
  api: 'DATABASE_URL_API',
  worker: 'DATABASE_URL_WORKER',
  public_intake: 'DATABASE_URL_PUBLIC_INTAKE',
};

/**
 * ADR-005 G-3: `search_path` de rong co chu dich — moi cau SQL phai dung ten du
 * dieu kien (`public.job`, `story.chapter`). Mot bang trung ten o schema khac se
 * doi nghia cau lenh ma khong bao loi, nen day la loi phai chan bang cau hinh.
 *
 * Dat qua tham so khoi dong ket noi thay vi mot cau `SET` sau khi ket noi: cach
 * thu hai co khoang thoi gian trong do query dau tien chay voi search_path mac
 * dinh, va khoang do khong quan sat duoc.
 */
const EMPTY_SEARCH_PATH_OPTION = '-c search_path=';

export const connectionStringFor = (env: DatabaseEnv, role: DatabaseRole): string =>
  env[CONNECTION_STRING_BY_ROLE[role]];

export const createPool = (connectionString: string, role: DatabaseRole): Pool =>
  new Pool({
    connectionString,
    application_name: `comic-studio-${role}`,
    options: EMPTY_SEARCH_PATH_OPTION,
  });
