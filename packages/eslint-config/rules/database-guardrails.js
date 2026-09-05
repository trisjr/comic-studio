// AI Coding
/**
 * @file database-guardrails.js
 * @description Cam doan tang DB ma ADR-001 va ADR-006 yeu cau cuong che bang
 * cong cu, khong bang ky luat ca nhan (repo nay khong co code review).
 */

const BACKEND_TS = 'apps/backend/src/**/*.ts';

const SQL_STRING_NODES = ['Literal[value=/{PATTERN}/]', 'TemplateElement[value.raw=/{PATTERN}/]'];

const forbidSqlPattern = (pattern, message) =>
  SQL_STRING_NODES.map((node) => ({
    selector: node.replace('{PATTERN}', pattern),
    message,
  }));

/**
 * ADR-006 D5: mot lan quen `LOCAL` la mot lan ro tenant sang request ke tiep
 * dung lai connection do. Hai dang viet duoi day deu la pham vi session.
 */
const sessionScopedTenantContext = [
  ...forbidSqlPattern(
    'SET\\s+app\\.current_tenant',
    'ADR-006 D5: phai dung `SET LOCAL app.current_tenant`. `SET` muc session di theo connection ve pool va lam ro tenant.',
  ),
  ...forbidSqlPattern(
    'set_config\\s*\\([^)]*false',
    'ADR-006 D5: `set_config(..., false)` la pham vi session — tuong duong `SET`, mang dung rui ro ro tenant.',
  ),
];

/**
 * SDD §4.1 B-2 va ADR-006 W-3: giua cau CLAIM va `SET LOCAL` khong duoc chen
 * statement nao. Cach duy nhat bao dam dieu do la gom hai buoc vao mot ham.
 */
const jobTableAccess = forbidSqlPattern(
  'public\\.job\\b',
  'B-2/W-3: chi `platform/jobs/claim.ts` duoc cham `public.job`, qua dung ham claimJobAndBindTenant().',
);

/**
 * ADR-001 Consequences #3: driver `pg` tra `NUMERIC` ve dang chuoi. Ep kieu no
 * sang `number` lam mat do chinh xac cua `cost_usd`, `story_order`, credit.
 */
const numericCoercion = [
  {
    selector: 'CallExpression[callee.name="parseFloat"]',
    message:
      'ADR-001: cot NUMERIC (cost_usd, story_order, credit) phai giu dang chuoi/decimal. Dung helper trong @comic-studio/contracts thay cho parseFloat.',
  },
];

export const databaseGuardrails = [
  {
    files: [BACKEND_TS],
    rules: {
      'no-restricted-syntax': [
        'error',
        ...sessionScopedTenantContext,
        ...jobTableAccess,
        ...numericCoercion,
      ],
    },
  },
  {
    files: ['apps/backend/src/platform/jobs/claim.ts'],
    rules: {
      'no-restricted-syntax': ['error', ...sessionScopedTenantContext, ...numericCoercion],
    },
  },
];
