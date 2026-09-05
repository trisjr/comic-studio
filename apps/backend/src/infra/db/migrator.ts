// AI Coding
/**
 * @file migrator.ts
 * @description Chay migration SQL tho theo thu tu, mot lan duy nhat moi file.
 *
 * ADR-001 CHOT #3: file SQL la NGUON SU THAT cua schema. Khong cong cu nao duoc
 * sinh migration roi tu apply — RLS policy, CHECK constraint va trigger khong
 * bieu dien duoc trong DSL cua ORM.
 *
 * ⚠️ So migration nam o schema `ops`, KHONG o `public`: ADR-005 G-2 dinh nghia
 * `public` la closed list gom dung 12 bang nghiep vu. Them mot bang ha tang vao
 * do se lam test closed-list do, hoac buoc noi long chinh test day.
 */

import { createHash } from 'node:crypto';
import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';

import type { Pool } from 'pg';

import type { Logger } from '../logging/logger';

const MIGRATION_LOCK_KEY = 8_531_207;

const ENSURE_LEDGER_SQL = `
  CREATE SCHEMA IF NOT EXISTS ops;
  CREATE TABLE IF NOT EXISTS ops.schema_migration (
    filename    text        PRIMARY KEY,
    checksum    text        NOT NULL,
    applied_at  timestamptz NOT NULL DEFAULT now()
  );
`;

const checksumOf = (content: string): string =>
  createHash('sha256').update(content, 'utf8').digest('hex');

const readMigrationFiles = async (directory: string): Promise<string[]> => {
  const entries = await readdir(directory);
  return entries.filter((name) => name.endsWith('.sql')).sort();
};

/**
 * File da chay ma doi noi dung la mot su co im lang: DB dang o mot trang thai
 * khong con tai lap duoc tu repo. Dung lai va bao, khong tu sua.
 */
const assertUnchanged = (filename: string, expected: string, actual: string): void => {
  if (expected !== actual) {
    throw new Error(
      `Migration "${filename}" da chay nhung noi dung file da doi. ` +
        'Migration la append-only: tao file moi thay vi sua file cu.',
    );
  }
};

export const runMigrations = async (
  pool: Pool,
  directory: string,
  logger: Logger,
): Promise<void> => {
  const client = await pool.connect();

  try {
    await client.query(ENSURE_LEDGER_SQL);
    await client.query('SELECT pg_advisory_lock($1)', [MIGRATION_LOCK_KEY]);

    const applied = await client.query<{ filename: string; checksum: string }>(
      'SELECT filename, checksum FROM ops.schema_migration',
    );
    const appliedByName = new Map(applied.rows.map((row) => [row.filename, row.checksum]));

    for (const filename of await readMigrationFiles(directory)) {
      const content = await readFile(join(directory, filename), 'utf8');
      const checksum = checksumOf(content);
      const previous = appliedByName.get(filename);

      if (previous !== undefined) {
        assertUnchanged(filename, previous, checksum);
        continue;
      }

      logger.info({ filename }, 'Dang chay migration');
      await client.query('BEGIN');
      try {
        await client.query(content);
        await client.query(
          'INSERT INTO ops.schema_migration (filename, checksum) VALUES ($1, $2)',
          [filename, checksum],
        );
        await client.query('COMMIT');
      } catch (error) {
        await client.query('ROLLBACK');
        throw error;
      }
    }

    logger.info('Migration hoan tat');
  } finally {
    await client.query('SELECT pg_advisory_unlock($1)', [MIGRATION_LOCK_KEY]);
    client.release();
  }
};
