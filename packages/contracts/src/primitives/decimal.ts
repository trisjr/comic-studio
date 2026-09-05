// AI Coding
/**
 * @file decimal.ts
 * @description Kieu cho cac cot PostgreSQL `NUMERIC`. Driver `pg` tra `NUMERIC`
 * ve dang chuoi; ep sang `number` lam mat do chinh xac cua tien va thu tu ke
 * chuyen (ADR-001 Consequences #3).
 */

import { z } from 'zod';

declare const decimalBrand: unique symbol;

/**
 * Chuoi thap phan da duoc kiem dinh dang. Brand ngan viec mot `string` bat ky
 * bi dung nham vao cho doi `DecimalString`.
 */
export type DecimalString = string & { readonly [decimalBrand]: 'decimal' };

const DECIMAL_PATTERN = /^-?\d+(\.\d+)?$/;

export const decimalString = z
  .string()
  .regex(DECIMAL_PATTERN, 'Gia tri phai la chuoi thap phan hop le')
  .transform((value) => value as DecimalString);

export const isDecimalString = (value: string): value is DecimalString =>
  DECIMAL_PATTERN.test(value);

/**
 * Cong cu duy nhat de tao `DecimalString` tu du lieu ben ngoai. Nem loi thay vi
 * tra ve gia tri sai: mot `cost_usd` sai am tham lam hong ca mo hinh chi phi.
 */
export const toDecimalString = (value: string): DecimalString => {
  if (!isDecimalString(value)) {
    throw new TypeError(`Gia tri "${value}" khong phai chuoi thap phan hop le`);
  }
  return value;
};
