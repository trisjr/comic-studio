// AI Coding
/**
 * @file env.ts
 * @description Doc va kiem cau hinh tu bien moi truong. ADR-002 dieu 6 cam moi
 * nguon cau hinh khac (khong SDK secret manager, khong file config), nen day la
 * cua duy nhat cau hinh di vao he thong.
 *
 * Schema duoc tach theo nhom vi moi entrypoint can mot tap khac nhau: `migrate`
 * khong can storage, `worker` khong can cong HTTP. Bat buoc du moi bien cho moi
 * lenh se lam lenh migration khong chay duoc truoc khi storage ton tai.
 */

import { z } from 'zod';

const nonEmpty = z.string().min(1);

export const runtimeEnvSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace']).default('info'),
});

export const httpEnvSchema = z.object({
  APP_PORT: z.coerce.number().int().positive().default(3000),
  APP_HOST: z.string().default('0.0.0.0'),
});

/**
 * Bon danh tinh ket noi tach bach cua SDD §7.4. Chung la bon connection string
 * rieng, khong phai mot chuoi dung chung voi quyen khac nhau.
 */
export const databaseEnvSchema = z.object({
  DATABASE_URL_OWNER: nonEmpty,
  DATABASE_URL_API: nonEmpty,
  DATABASE_URL_WORKER: nonEmpty,
  DATABASE_URL_PUBLIC_INTAKE: nonEmpty,
});

/**
 * Mat khau role ung dung chi duoc `db:bootstrap` dung. Migration SQL tho khong
 * doc duoc bien moi truong, nen viec tao role song o subcommand rieng.
 */
export const databaseBootstrapEnvSchema = z.object({
  DATABASE_URL_OWNER: nonEmpty,
  DB_APP_API_PASSWORD: nonEmpty,
  DB_APP_WORKER_PASSWORD: nonEmpty,
  DB_APP_PUBLIC_INTAKE_PASSWORD: nonEmpty,
});

export const storageEnvSchema = z.object({
  STORAGE_ENDPOINT: z.url(),
  STORAGE_REGION: nonEmpty,
  STORAGE_BUCKET: nonEmpty,
  STORAGE_ACCESS_KEY_ID: nonEmpty,
  STORAGE_SECRET_ACCESS_KEY: nonEmpty,
  STORAGE_FORCE_PATH_STYLE: z
    .enum(['true', 'false'])
    .default('true')
    .transform((value) => value === 'true'),
  STORAGE_SIGNED_URL_TTL_SECONDS: z.coerce.number().int().positive().default(300),
});

export type RuntimeEnv = z.infer<typeof runtimeEnvSchema>;
export type HttpEnv = z.infer<typeof httpEnvSchema>;
export type DatabaseEnv = z.infer<typeof databaseEnvSchema>;
export type DatabaseBootstrapEnv = z.infer<typeof databaseBootstrapEnvSchema>;
export type StorageEnv = z.infer<typeof storageEnvSchema>;

/**
 * Nem ngay khi thieu cau hinh, thay vi de process khoi dong roi hong o request
 * dau tien. Thong bao liet ke du moi bien sai de mot lan sua la du.
 */
export const loadEnv = <TSchema extends z.ZodType>(
  schema: TSchema,
  source: NodeJS.ProcessEnv = process.env,
): z.infer<TSchema> => {
  const result = schema.safeParse(source);

  if (!result.success) {
    const details = result.error.issues
      .map((issue) => `  - ${issue.path.join('.')}: ${issue.message}`)
      .join('\n');
    throw new Error(`Cau hinh bien moi truong khong hop le:\n${details}`);
  }

  return result.data;
};
