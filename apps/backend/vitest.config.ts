// AI Coding
/**
 * @file vitest.config.ts
 * @description Cau hinh test cua backend. Test invariant chay tren PostgreSQL
 * that tu Docker Compose — RLS, transaction boundary va `information_schema`
 * khong kiem duoc bang DB gia.
 */

import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'node',
    include: ['test/**/*.test.ts'],
    hookTimeout: 30_000,
    testTimeout: 30_000,
  },
});
