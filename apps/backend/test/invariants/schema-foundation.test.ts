// AI Coding
/**
 * @file schema-foundation.test.ts
 * @description Kiem cac invariant ma migration 0001 dung len.
 *
 * ⚠️ Test nay chay tren PostgreSQL THAT tu `pnpm db:up`. RLS, hanh vi
 * fail-closed va `information_schema` khong kiem duoc bang mot DB gia — mot mock
 * se luon tra ve dieu ta mong doi, ke ca khi database that dang sai.
 */

import { Pool } from 'pg';
import { afterAll, beforeAll, describe, expect, it } from 'vitest';

const OWNER_URL = process.env['DATABASE_URL_OWNER'];
const MODULE_SCHEMAS = ['story', 'comic', 'generation'];

describe.skipIf(OWNER_URL === undefined)('nen database sau migration 0001', () => {
  let pool: Pool;

  beforeAll(() => {
    pool = new Pool({ connectionString: OWNER_URL, options: '-c search_path=' });
  });

  afterAll(async () => {
    await pool.end();
  });

  it('co du ba schema module trong cung mot database', async () => {
    const result = await pool.query<{ schema_name: string }>(
      'SELECT schema_name FROM information_schema.schemata WHERE schema_name = ANY($1)',
      [MODULE_SCHEMAS],
    );

    expect(result.rows.map((row) => row.schema_name).sort()).toEqual([...MODULE_SCHEMAS].sort());
  });

  it('khong cho PUBLIC tao object trong schema public', async () => {
    const result = await pool.query<{ has_create: boolean }>(
      "SELECT has_schema_privilege('public', 'public', 'CREATE') AS has_create",
    );

    expect(result.rows[0]?.has_create).toBe(false);
  });

  /**
   * AC "fail-closed 0 row" cua Story-Tenant-Id-And-RLS-Everywhere: bien chua set
   * phai cho NULL, ⛔ khong duoc nem. Nem exception se lam policy do vo thay vi
   * loc row, va do la mot che do hong khac han.
   */
  it('tra NULL khi tenant context chua duoc set', async () => {
    const result = await pool.query<{ tenant: string | null }>(
      'SELECT public.current_tenant_id() AS tenant',
    );

    expect(result.rows[0]?.tenant).toBeNull();
  });

  it('tra NULL thay vi nem khi tenant context sai dinh dang', async () => {
    const client = await pool.connect();

    try {
      await client.query('BEGIN');
      await client.query("SELECT set_config('app.current_tenant', 'khong-phai-uuid', true)");
      const result = await client.query<{ tenant: string | null }>(
        'SELECT public.current_tenant_id() AS tenant',
      );

      expect(result.rows[0]?.tenant).toBeNull();
      await client.query('ROLLBACK');
    } finally {
      client.release();
    }
  });

  it('xoa tenant context khi transaction ket thuc', async () => {
    const client = await pool.connect();
    const tenant = '00000000-0000-4000-8000-000000000001';

    try {
      await client.query('BEGIN');
      await client.query("SELECT set_config('app.current_tenant', $1, true)", [tenant]);
      const inside = await client.query<{ tenant: string | null }>(
        'SELECT public.current_tenant_id() AS tenant',
      );
      expect(inside.rows[0]?.tenant).toBe(tenant);

      await client.query('COMMIT');

      const outside = await client.query<{ tenant: string | null }>(
        'SELECT public.current_tenant_id() AS tenant',
      );
      expect(outside.rows[0]?.tenant).toBeNull();
    } finally {
      client.release();
    }
  });
});
