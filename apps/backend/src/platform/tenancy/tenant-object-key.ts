// AI Coding
/**
 * @file tenant-object-key.ts
 * @description Dung key cho object storage theo so do da CHOT o ADR-004.
 *
 * ⚠️ KHONG dedup cheo tenant (ADR-004 dieu 9): hai tenant upload cung mot file
 * cho ra hai object, hai key, hai lan tra tien luu tru. Day la chi phi CO CHU
 * DICH — dedup cheo tenant mau thuan truc tiep voi lap luan ban quyen cua du an.
 */

import type { TenantId } from '@comic-studio/contracts';

const SHA256_HEX_PATTERN = /^[0-9a-f]{64}$/;

/**
 * Prefix tam cua pha 1 upload. ⛔ Khong object nao trong day duoc coi la du lieu
 * hop le, va khong duong doc nao cua san pham duoc tro vao prefix nay
 * (ADR-004 dieu 7).
 */
export const incomingObjectKey = (tenantId: TenantId, uploadId: string): string =>
  `tenant/${tenantId}/incoming/${uploadId}`;

/**
 * Key canonical cua pha 2. `sha256` do SERVER tinh sau khi da kiem opt-out —
 * client khong duoc tu quyet key cuoi vi khong ai tin duoc bam do client gui.
 */
export const canonicalObjectKey = (tenantId: TenantId, sha256: string): string => {
  if (!SHA256_HEX_PATTERN.test(sha256)) {
    throw new TypeError(`"${sha256}" khong phai bam sha256 dang hex 64 ky tu`);
  }

  return `tenant/${tenantId}/${sha256}`;
};

export const isIncomingObjectKey = (key: string): boolean => key.includes('/incoming/');
