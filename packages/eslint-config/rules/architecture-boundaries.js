// AI Coding
/**
 * @file architecture-boundaries.js
 * @description Cuong che duong ranh gioi B-1 cua SDD §4.1 va chieu phu thuoc ba
 * lop `modules` -> `platform` -> `infra` cua backend.
 *
 * ⚠️ Pattern o day khop tren CHUOI import specifier, khong phai duong dan da
 * phan giai. Vi vay moi ranh gioi phai liet ke ca dang tuong doi (`../story/x`)
 * lan dang di qua nhieu cap (`**\/modules/story/x`) — bo mot dang la de ho mot
 * duong vong ma lint van bao xanh.
 */

const BACKEND = 'apps/backend/src';

/** Sinh cac dang specifier co the tro toi ben trong mot thu muc dich. */
const deepImportsInto = (segment) => [
  `../${segment}/*`,
  `../${segment}/*/**`,
  `../../${segment}/*`,
  `../../${segment}/*/**`,
  `**/${segment}/*`,
  `**/${segment}/*/**`,
];

/** Sinh cac dang specifier tro toi bat ky dau trong mot tang. */
const anyImportInto = (segment) => [
  `../${segment}/**`,
  `../../${segment}/**`,
  `../../../${segment}/**`,
  `**/${segment}/**`,
];

const boundary = (from, patterns) => ({
  files: [`${BACKEND}/${from}/**/*.ts`],
  rules: {
    'no-restricted-imports': ['error', { patterns }],
  },
});

/**
 * B-1 (SDD §4.1 · ADR-009 D3): module `comic` chi duoc cham `story` qua dung hai
 * ham `resolveState()` va `getBible()`, tuc chi qua barrel. Quy uoc import la
 * `from '../story'` — dang `'../story/index'` cung bi chan de chi con MOT cach
 * viet dung.
 */
export const comicToStoryBoundary = boundary('modules/comic', [
  {
    group: [...deepImportsInto('story'), ...deepImportsInto('modules/story')],
    message:
      "B-1: module `comic` chi duoc goi `story` qua resolveState()/getBible(). Viet `from '../story'` thay vi import sau vao noi bo module (ADR-009 D3).",
  },
]);

/**
 * Tang `platform` la ha tang nghiep vu dung chung: no khong duoc biet module nao
 * ton tai. Job handler di nguoc lai bang registry, tuc dao chieu, khong phai
 * import nguoc.
 */
export const platformIndependence = boundary('platform', [
  {
    group: anyImportInto('modules'),
    message:
      'Tang `platform` khong duoc import module nghiep vu. Dao chieu bang registry hoac port thay vi import nguoc.',
  },
]);

/** `infra` la tang thap nhat: khong biet platform, khong biet module. */
export const infraIndependence = boundary('infra', [
  {
    group: [...anyImportInto('platform'), ...anyImportInto('modules')],
    message:
      'Tang `infra` chi chua adapter ha tang. Import len `platform`/`modules` la dao nguoc chieu phu thuoc.',
  },
]);

export const architectureBoundaries = [
  comicToStoryBoundary,
  platformIndependence,
  infraIndependence,
];
