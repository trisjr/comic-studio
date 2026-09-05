// AI Coding
/**
 * @file tenant-object-key.test.ts
 * @description Kiem so do key object storage cua ADR-004, gom ca rang buoc
 * "khong dedup cheo tenant" — thu de mat neu ai do toi uu chi phi luu tru.
 */

import { describe, expect, it } from 'vitest';

import type { TenantId } from '@comic-studio/contracts';

import {
  canonicalObjectKey,
  incomingObjectKey,
  isIncomingObjectKey,
} from '../../src/platform/tenancy/tenant-object-key';

const TENANT_A = '11111111-1111-4111-8111-111111111111' as TenantId;
const TENANT_B = '22222222-2222-4222-8222-222222222222' as TenantId;
const SHA256 = 'a'.repeat(64);

describe('key object storage theo tenant', () => {
  it('dat tenant o tien to cua key canonical', () => {
    expect(canonicalObjectKey(TENANT_A, SHA256)).toBe(`tenant/${TENANT_A}/${SHA256}`);
  });

  /**
   * ADR-004 dieu 9: dedup cheo tenant mau thuan truc tiep voi lap luan ban quyen
   * cua du an. Hai tenant cung noi dung PHAI cho hai key khac nhau.
   */
  it('cho hai key khac nhau khi hai tenant co cung noi dung', () => {
    expect(canonicalObjectKey(TENANT_A, SHA256)).not.toBe(canonicalObjectKey(TENANT_B, SHA256));
  });

  it('tu choi bam khong phai sha256 hex 64 ky tu', () => {
    expect(() => canonicalObjectKey(TENANT_A, 'qua-ngan')).toThrow(TypeError);
  });

  it('phan biet duoc key tam cua pha 1 upload', () => {
    expect(isIncomingObjectKey(incomingObjectKey(TENANT_A, 'upload-1'))).toBe(true);
    expect(isIncomingObjectKey(canonicalObjectKey(TENANT_A, SHA256))).toBe(false);
  });
});
