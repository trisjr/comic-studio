// AI Coding
/**
 * @file transaction.ts
 * @description Duong duy nhat mo transaction va bom tenant context cho RLS.
 *
 * ADR-006 D5: moi truy van cham du lieu tenant phai nam trong mot transaction
 * tuong minh. Query o che do autocommit khong co context nen tra 0 row — fail
 * closed, dung theo thiet ke.
 */

import type { Pool, PoolClient } from 'pg';

import type { TenantId } from '@comic-studio/contracts';

export type TransactionWork<TResult> = (client: PoolClient) => Promise<TResult>;

/**
 * ADR-006 D1 yeu cau context o pham vi transaction. Bai viet `SET LOCAL` khong
 * nhan tham so nen se phai noi suy chuoi vao SQL; `set_config(..., true)` la
 * dang tham so hoa duoc cua cung mot pham vi, nen no la dang duy nhat duoc dung
 * o day. Tham so thu ba `true` = local — `false` bi cam tuyet doi (ADR-006 D5).
 */
const BIND_TENANT_SQL = "SELECT set_config('app.current_tenant', $1, true)";

export const withTransaction = async <TResult>(
  pool: Pool,
  work: TransactionWork<TResult>,
): Promise<TResult> => {
  const client = await pool.connect();

  try {
    await client.query('BEGIN');
    const result = await work(client);
    await client.query('COMMIT');
    return result;
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
};

/**
 * Bom tenant context ngay sau `BEGIN`, truoc bat ky statement nghiep vu nao.
 * `COMMIT`/`ROLLBACK` tu xoa context, nen connection quay ve pool o trang thai
 * khong tenant — trang thai an toan mac dinh.
 */
export const withTenantTransaction = async <TResult>(
  pool: Pool,
  tenantId: TenantId,
  work: TransactionWork<TResult>,
): Promise<TResult> =>
  withTransaction(pool, async (client) => {
    await client.query(BIND_TENANT_SQL, [tenantId]);
    return work(client);
  });
