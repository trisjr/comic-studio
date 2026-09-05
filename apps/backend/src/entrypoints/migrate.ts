// AI Coding
/**
 * @file migrate.ts
 * @description Entrypoint `migrate` — chay migration duoi DB role owner.
 *
 * ADR-006 D7: role ung dung KHONG co quyen DDL. Day la ly do migration phai
 * chay bang mot connection rieng, khong dung chung pool voi `api` hay `worker`.
 */

import { join } from 'node:path';

import { databaseEnvSchema, loadEnv, runtimeEnvSchema } from '../infra/config/env';
import { runMigrations } from '../infra/db/migrator';
import { connectionStringFor, createPool } from '../infra/db/pool';
import { createLogger } from '../infra/logging/logger';

const MIGRATIONS_DIRECTORY = join(__dirname, '..', '..', 'db', 'migrations');

export const runMigrate = async (): Promise<void> => {
  const runtime = loadEnv(runtimeEnvSchema);
  const database = loadEnv(databaseEnvSchema);
  const logger = createLogger(runtime, 'migrate');
  const pool = createPool(connectionStringFor(database, 'owner'), 'owner');

  try {
    await runMigrations(pool, MIGRATIONS_DIRECTORY, logger);
  } finally {
    await pool.end();
  }
};
