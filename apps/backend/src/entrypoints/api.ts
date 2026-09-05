// AI Coding
/**
 * @file api.ts
 * @description Entrypoint `api` — process phuc vu HTTP.
 *
 * SDD §7.3 dieu 1: process nay KHONG duoc chua vong lap worker va KHONG duoc co
 * scheduler chay trong process. Do la dieu kien de "worker chet ma API van song"
 * la mot hanh vi kiem duoc, khong phai mot khau hieu.
 */

import { NestFactory } from '@nestjs/core';
import { FastifyAdapter, type NestFastifyApplication } from '@nestjs/platform-fastify';

import { AppModule } from '../app.module';
import { httpEnvSchema, loadEnv, runtimeEnvSchema } from '../infra/config/env';
import { createLogger } from '../infra/logging/logger';

export const runApi = async (): Promise<void> => {
  const runtime = loadEnv(runtimeEnvSchema);
  const http = loadEnv(httpEnvSchema);
  const logger = createLogger(runtime, 'api');

  const app = await NestFactory.create<NestFastifyApplication>(AppModule, new FastifyAdapter(), {
    logger: false,
  });

  await app.listen(http.APP_PORT, http.APP_HOST);
  logger.info({ port: http.APP_PORT, host: http.APP_HOST }, 'Process api dang lang nghe');
};
