// AI Coding
/**
 * @file index.ts
 * @description Be mat CONG KHAI duy nhat cua module `story`.
 *
 * ⚠️ ADR-009 D3 va SDD §4.1 B-1: module `comic` chi duoc cham `story` qua dung
 * hai ham `resolveState()` va `getBible()` — va chung phai duoc export tu day.
 * Moi import sau vao noi bo `story` bi lint rule chan o CI.
 *
 * Hai ham do chua ton tai: ngu nghia cua chung thuoc ADR-011 va duoc hien thuc
 * o Story-Timeline-State-Resolver. File nay giu ranh gioi san de khi chung ra
 * doi, chung ra doi DUNG CHO.
 */

export { StoryModule } from './story.module';
