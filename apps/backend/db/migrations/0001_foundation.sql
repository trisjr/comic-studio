-- AI Coding
-- 0001_foundation.sql
-- Nen cua database: ba schema module, guardrail cua schema `public`, va ham
-- helper doc tenant context cho RLS.
--
-- ⛔ Migration nay CO Y khong tao mot bang nghiep vu nao. Policy RLS cho
-- `tenant`/`user`/`membership` con dang mo (ADR-005 Q4 giao cho Architect o lo
-- DB Schema), va viet DDL cho chung bay gio la bia ra mot quyet dinh chua ai
-- dong. Bang dau tien thuoc Story-Tenant-Id-And-RLS-Everywhere.

-- ---------------------------------------------------------------------------
-- 1. Ba schema module (ADR-009 D1 · SRS-NFR-02)
--    Dieu kien xac minh cua Story-Modular-Monolith-Three-Schemas: truy van
--    `information_schema.schemata` phai tra ve du ba ten trong MOT database.
-- ---------------------------------------------------------------------------

CREATE SCHEMA IF NOT EXISTS story;
CREATE SCHEMA IF NOT EXISTS comic;
CREATE SCHEMA IF NOT EXISTS generation;

COMMENT ON SCHEMA story IS 'M1 Ingest & Compliance Gate, M2 Story Intelligence';
COMMENT ON SCHEMA comic IS 'M3 Comic Director & Layout, M4 Dialogue & Human Gates, M6 Typeset';
COMMENT ON SCHEMA generation IS 'M5 Generation Pipeline';

-- ---------------------------------------------------------------------------
-- 2. Guardrail G-1 cua ADR-005
--    `public` la schema mac dinh cua PostgreSQL. Khong chan thi no troi thanh
--    noi chua moi thu, va closed list o G-2 mat y nghia.
-- ---------------------------------------------------------------------------

REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA story, comic, generation FROM PUBLIC;

-- ---------------------------------------------------------------------------
-- 3. Ham doc tenant context (ADR-006 D2)
--    AC "fail-closed 0 row" doi: bien CHUA SET hoac set gia tri KHONG HOP LE
--    deu phai cho 0 row, ⛔ khong duoc nem exception.
--
--    `current_setting(..., true)` tra NULL khi chua set — thoa nua dau. Nhung ep
--    mot chuoi khong hop le sang uuid VAN nem, nen phai co khoi EXCEPTION o day.
--    Policy luon viet dang `USING (tenant_id = public.current_tenant_id())`:
--    NULL cho ra NULL, row bi loc, va so sanh giu nguyen kieu uuid nen index
--    tren `tenant_id` van dung duoc.
-- ---------------------------------------------------------------------------

CREATE OR REPLACE FUNCTION public.current_tenant_id()
RETURNS uuid
LANGUAGE plpgsql
STABLE
SET search_path = pg_catalog
AS $$
BEGIN
  RETURN current_setting('app.current_tenant', true)::uuid;
EXCEPTION
  WHEN others THEN
    RETURN NULL;
END;
$$;

COMMENT ON FUNCTION public.current_tenant_id() IS
  'ADR-006 D2: doc GUC app.current_tenant, tra NULL thay vi nem khi thieu hoac sai dinh dang';

-- ---------------------------------------------------------------------------
-- 4. Quyen toi thieu cho ba role ung dung (SDD §7.4)
--    ⚠️ CO Y khong dung ALTER DEFAULT PRIVILEGES: cap SELECT mac dinh cho moi
--    bang tuong lai se lang le cap quyen cho `app_public_intake` tren bang
--    nghiep vu — dung dieu ADR-006 D6 cam. Moi migration tao bang phai tu grant.
-- ---------------------------------------------------------------------------

GRANT USAGE ON SCHEMA public, story, comic, generation TO app_api;
GRANT USAGE ON SCHEMA public, story, comic, generation TO app_worker;
GRANT USAGE ON SCHEMA public TO app_public_intake;

GRANT EXECUTE ON FUNCTION public.current_tenant_id() TO app_api, app_worker;
