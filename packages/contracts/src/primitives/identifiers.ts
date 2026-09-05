// AI Coding
/**
 * @file identifiers.ts
 * @description Kieu dinh danh dung chung. `TenantId` duoc tach rieng vi no la
 * gia tri bom vao GUC `app.current_tenant` cho RLS (ADR-006 D1) — nham no voi
 * mot uuid khac la loi khong bao loi.
 */

import { z } from 'zod';

declare const tenantIdBrand: unique symbol;

export type TenantId = string & { readonly [tenantIdBrand]: 'tenant' };

export const tenantId = z.uuid().transform((value) => value as TenantId);

export const entityId = z.uuid();

export type EntityId = z.infer<typeof entityId>;
