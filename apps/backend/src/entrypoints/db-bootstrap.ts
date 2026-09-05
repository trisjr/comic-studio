// AI Coding
/**
 * @file db-bootstrap.ts
 * @description Entrypoint `db:bootstrap` — tao ba DB role ung dung tu bien moi
 * truong. Phai chay TRUOC `migrate`, vi migration 0001 cap quyen cho ba role do.
 */

import { databaseBootstrapEnvSchema, loadEnv, runtimeEnvSchema } from '../infra/config/env';
import { bootstrapRoles } from '../infra/db/bootstrap-roles';
import { createPool } from '../infra/db/pool';
import { createLogger } from '../infra/logging/logger';

export const runDbBootstrap = async (): Promise<void> => {
  const runtime = loadEnv(runtimeEnvSchema);
  const bootstrap = loadEnv(databaseBootstrapEnvSchema);
  const logger = createLogger(runtime, 'db:bootstrap');
  const pool = createPool(bootstrap.DATABASE_URL_OWNER, 'owner');

  try {
    await bootstrapRoles(pool, bootstrap, logger);
  } finally {
    await pool.end();
  }
};
