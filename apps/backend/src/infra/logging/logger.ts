// AI Coding
/**
 * @file logger.ts
 * @description Logger dung chung, ghi JSON ra stdout theo ADR-002 dieu 6.
 *
 * Quy tac che gia tri nhay cam la yeu cau cua ADR-004 dieu 3: mot signed URL
 * nam trong log la mot public bucket thu nho co thoi han.
 */

import { pino } from 'pino';
import type { Logger as PinoLogger } from 'pino';

import type { RuntimeEnv } from '../config/env';

const REDACTED_PATHS = [
  'req.headers.authorization',
  'req.headers.cookie',
  '*.signedUrl',
  '*.presignedUrl',
  '*.password',
  '*.secretAccessKey',
  '*.connectionString',
];

export type Logger = PinoLogger;

export const createLogger = (env: RuntimeEnv, entrypoint: string): Logger =>
  pino({
    level: env.LOG_LEVEL,
    base: { entrypoint },
    redact: { paths: REDACTED_PATHS, censor: '[REDACTED]' },
    formatters: {
      level: (label) => ({ level: label }),
    },
  });
