// AI Coding
/**
 * @file health.controller.ts
 * @description Diem kiem tra suc khoe cua process `api`.
 *
 * SDD §7.3 dieu 5: liveness cua `api` va cua `worker` phai danh gia DOC LAP.
 * Endpoint nay chi noi ve process `api` — no khong duoc bao cao trang thai cua
 * worker, vi "worker chet ma API van song" la hanh vi dung, khong phai su co.
 */

import { Controller, Get } from '@nestjs/common';

@Controller('health')
export class HealthController {
  @Get()
  check(): { status: 'ok'; entrypoint: 'api' } {
    return { status: 'ok', entrypoint: 'api' };
  }
}
