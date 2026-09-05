// AI Coding
/**
 * @file app.module.ts
 * @description Composition root dung chung cho ca hai entrypoint.
 *
 * ADR-001 CHOT #2: `api` va `worker` dung CHUNG do thi DI nay, chi khac lenh
 * khoi dong. Nho vay khong ton tai nhanh code rieng cho worker, va hai ben khong
 * bao gio lech nhau ve validation.
 */

import { Module } from '@nestjs/common';

import { HealthController } from './platform/health/health.controller';
import { ComicModule } from './modules/comic/comic.module';
import { GenerationModule } from './modules/generation/generation.module';
import { StoryModule } from './modules/story/story.module';

@Module({
  imports: [StoryModule, ComicModule, GenerationModule],
  controllers: [HealthController],
})
export class AppModule {}
