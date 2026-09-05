// AI Coding
/**
 * @file worker.ts
 * @description Entrypoint `worker` — process xu ly job, KHONG mo HTTP.
 *
 * ADR-001: dung `createApplicationContext()` chu khong `create()`, nen worker
 * dung chung toan bo do thi DI voi `api` ma khong dung mot cong nao.
 *
 * ⚠️ Vong lap claim job CHUA duoc hien thuc: no doi bang `public.job` va ham
 * `claimJobAndBindTenant()` cua Story-Job-Queue-In-Postgres. ADR-006 W-3 bat hai
 * buoc CLAIM va `SET LOCAL` nam trong dung mot ham, nen viet nua voi o day se
 * tao ra chinh khoang ho ma guardrail do ton tai de dong.
 */

import { NestFactory } from '@nestjs/core';

import { AppModule } from '../app.module';
import { loadEnv, runtimeEnvSchema } from '../infra/config/env';
import { createLogger } from '../infra/logging/logger';

export const runWorker = async (): Promise<void> => {
  const runtime = loadEnv(runtimeEnvSchema);
  const logger = createLogger(runtime, 'worker');

  const context = await NestFactory.createApplicationContext(AppModule, { logger: false });
  logger.info('Process worker da khoi dong, chua co job handler nao dang ky');

  await context.close();
};
