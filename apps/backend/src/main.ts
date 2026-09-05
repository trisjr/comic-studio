// AI Coding
/**
 * @file main.ts
 * @description Dispatcher cua mot image duy nhat.
 *
 * ADR-001 CHOT #2 va ADR-002 CHOT #2: `apps/backend` build ra DUNG MOT image;
 * `api` va `worker` deploy cung mot image digest, chi khac lenh. ADR-002 dieu 3
 * them mot rang buoc: job theo dong ho cung chi duoc GOI mot subcommand o day —
 * khong mot dong logic nghiep vu nao duoc song trong cau hinh cron cua platform.
 */

import 'reflect-metadata';

import { runApi } from './entrypoints/api';
import { runDbBootstrap } from './entrypoints/db-bootstrap';
import { runMigrate } from './entrypoints/migrate';
import { runWorker } from './entrypoints/worker';

type Command = 'api' | 'worker' | 'migrate' | 'db:bootstrap';

const COMMANDS: Record<Command, () => Promise<void>> = {
  api: runApi,
  worker: runWorker,
  migrate: runMigrate,
  'db:bootstrap': runDbBootstrap,
};

const isCommand = (value: string | undefined): value is Command =>
  value !== undefined && value in COMMANDS;

const main = async (): Promise<void> => {
  const requested = process.argv[2];

  if (!isCommand(requested)) {
    const available = Object.keys(COMMANDS).join(' | ');
    throw new Error(`Lenh "${requested ?? ''}" khong hop le. Lenh kha dung: ${available}`);
  }

  await COMMANDS[requested]();
};

main().catch((error: unknown) => {
  process.stderr.write(`${error instanceof Error ? error.stack : String(error)}\n`);
  process.exitCode = 1;
});
