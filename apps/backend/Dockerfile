# AI Coding
# Dockerfile — build DUNG MOT image cho ca hai process type.
#
# ADR-001 CHOT #2 va ADR-002 CHOT #2: `api` va `worker` deploy cung mot image
# digest, chi khac command. Vi vay image nay ⛔ khong co ENTRYPOINT co dinh cho
# mot vai tro nao — vai tro do lenh khoi dong quyet dinh.

# ⚠️ Pin theo digest-friendly tag. ADR-013 R-4 canh bao mot lan `docker build`
# keo ve patch version moi cua FONT co the doi cach ngat dong ma khong bao loi;
# cung logic do ap cho base image.
FROM node:22.22.0-bookworm-slim AS base
ENV PNPM_HOME=/usr/local/bin
RUN corepack enable && corepack prepare pnpm@10.33.0 --activate
WORKDIR /app

FROM base AS deps
COPY package.json pnpm-lock.yaml pnpm-workspace.yaml .npmrc ./
COPY packages/tsconfig/package.json ./packages/tsconfig/
COPY packages/eslint-config/package.json ./packages/eslint-config/
COPY packages/contracts/package.json ./packages/contracts/
COPY apps/backend/package.json ./apps/backend/
RUN pnpm install --frozen-lockfile

FROM deps AS build
COPY packages ./packages
COPY apps/backend ./apps/backend
RUN pnpm --filter @comic-studio/contracts build \
  && pnpm --filter @comic-studio/backend build \
  && pnpm deploy --filter @comic-studio/backend --prod /runtime

FROM base AS runtime
ENV NODE_ENV=production
COPY --from=build /runtime/node_modules ./node_modules
COPY --from=build /app/apps/backend/dist ./dist
# File migration di theo image: ADR-002 dieu 3 bat lenh migrate la mot subcommand
# cua chinh image nay, nen no phai mang theo du lieu no can.
COPY --from=build /app/apps/backend/db ./db
COPY --from=build /app/apps/backend/package.json ./package.json

USER node
CMD ["node", "dist/main.js", "api"]
