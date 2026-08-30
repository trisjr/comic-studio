---
id: ADR-001
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-001: Tech stack backend, frontend và tầng truy cập dữ liệu

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

## Context

`SRS-NFR-09` (*"Ngôn ngữ / framework backend & frontend"*) là **`CHƯA QUYẾT` → `TBD`** — [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) §3.E ghi rõ *"Không anchor được"*, và `CF-1.3` `[OFF]`: *"chưa có dòng nào"*. Em đã verify lại tại thời điểm viết: `src/` và `test/` ở repo root **rỗng hoàn toàn**. Đây là quyết định có **chi phí đảo ngược thấp nhất của toàn dự án ngay lúc này**, và sẽ không bao giờ rẻ như vậy nữa sau commit đầu tiên.

ADR này là **nền của mọi ADR sau**: ADR-005 (vị trí schema bảng platform) và ADR-006 (cơ chế bơm tenant context cho RLS) đều phụ thuộc vào lựa chọn driver/ORM ở đây.

### Ba ràng buộc bao trùm — phải thoả **đồng thời**

| # | Ràng buộc | Nguồn |
|---|---|---|
| **R1** | Đội **1 người + AI assist**, không funding. *"Mọi requirement phải chia được cho một người"* | `SRS` §1.3 (`CF-1.2` `[CHỐT]`) |
| **R2** | **Hai entrypoint (`api`, `worker`) trên cùng một image**, cùng codebase, khác command. Yêu cầu vận hành: *"worker chết mà API vẫn sống"* | `D-02` · `SRS` `SRS-NFR-03` |
| **R3** | Wrap thoại tiếng Việt **phải dùng thư viện hiểu Unicode combining marks** | `D-30` · `SRS` `SRS-FR-16` |

`R1` là ràng buộc **nặng nhất**: mọi lựa chọn dưới đây phải biện minh được dưới nó. `R3` **không phải chi tiết nhỏ** — bubble là sản phẩm cuối mà người đọc nhìn thấy; wrap sai dấu tiếng Việt là hỏng sản phẩm, không phải lỗi cosmetic.

### Ràng buộc kế thừa mà stack phải đỡ được (⛔ không mở lại)

- **Tầng DB là tầng cưỡng chế, không phải tầng lưu trữ.** RLS làm lớp phòng thủ thứ hai (`D-09`), ⛔ cấm tenant isolation kiểu app-layer filter (`D-10`), CHECK `≤3` nhân vật ở tầng DB (`D-21`), `INSERT generation` thiếu `origin` phải **FAIL ở tầng DB** (`D-51`), `CHECK (available >= 0)` (`D-60`). ⇒ **ORM không được sở hữu schema.**
- **Câu CLAIM job là SQL thô**: `SELECT … FOR UPDATE SKIP LOCKED` + fairness `in_flight_per_tenant < N` nằm **trong chính câu đó** (`D-03`, `D-42`). ⇒ stack phải cho viết SQL thô mà không phải "thoát ra khỏi" framework.
- **`KC-4` — một transaction bất khả phân**: `INSERT generation` + `INSERT change_log` + `INSERT usage_event` (`D-50`). ⇒ cần interactive transaction thật, kiểm soát được connection.
- **Compositor server-side dùng chung cho preview và export 300 DPI** (`D-22`, `D-32`), art **không có chữ**, bubble là **layer dữ liệu** toạ độ 0–1 (`D-29`). ⇒ runtime phải render được text với shaping đúng cho tiếng Việt.
- **Không mua GPU** (`D-07`) và **⛔ không có LLM ở runtime của Visual Prompt Compiler** (`D-34`). ⇒ main path **không cần** ML runtime; đây là lý do lợi thế hệ sinh thái ML **không** phải tiêu chí chọn ngôn ngữ chính.
- **`reading_order` / `story_order` là `NUMERIC` sparse** (`D-15`); `cost_usd` trên mọi generation (`D-59`); credit ledger (`D-60`). ⇒ stack phải xử lý số thập phân chính xác, ⛔ không float.
- **Polling 2 giây**, ⛔ không WebSocket (`D-45`). ⇒ frontend cần một tầng data-fetching có cache + polling, không cần realtime transport.

## Decision

### Tầng CHỐT — bất biến kiến trúc, ⛔ không đổi mà không viết ADR mới

1. **Một ngôn ngữ duy nhất cho API, worker và frontend: TypeScript trên Node.js LTS.**
2. **`apps/api` build ra ĐÚNG MỘT image**, hai command: `node dist/main.js api` và `node dist/main.js worker`. Image được **build một lần, push lên registry, và cả hai process deploy cùng một image digest** — đây là cách thoả `R2` mà không phụ thuộc platform nào.
3. **Migration là file SQL thô, đánh số, append-only — và nó là NGUỒN SỰ THẬT của schema.** Không công cụ nào được sinh migration rồi apply mà không có người đọc. Lý do: RLS policy, CHECK constraint, partial index, trigger guardrail (`D-10`, `D-21`, `D-51`, `D-60`) **không biểu diễn được** trong DSL của ORM.
4. **⛔ KHÔNG dùng ORM sở hữu schema (schema-first / active-record).** Tầng truy cập DB là **typed query builder** trên driver `pg`, luôn để lộ connection và transaction ra ngoài.
5. **Frontend là SPA thuần, ⛔ không SSR, ⛔ không server action.** API là **hợp đồng duy nhất** giữa web và dữ liệu — vì tenant context (ADR-006) chỉ được bơm ở **một** chỗ.
6. **Một `packages/contracts` là nguồn sự thật của hợp đồng API** (zod schema → sinh OpenAPI cho backend, sinh kiểu cho web). ⛔ Không khai báo kiểu request/response hai lần.
7. **Ranh giới module `story` / `comic` / `generation` được cưỡng chế bằng lint ở CI** (`D-04`), không bằng kỷ luật cá nhân.
8. **Wrap tiếng Việt (`R3`) nằm CÙNG runtime với compositor.** Chuẩn hoá **NFC** ngay tại biên ingest; ngắt dòng theo **grapheme cluster + word boundary** bằng `Intl.Segmenter` (ECMA-402, ICU-backed, có sẵn trong Node LTS); ⛔ **không** được wrap ở frontend rồi gửi kết quả xuống, ⛔ **không** được wrap bằng font khác font sẽ render.

### Tầng MẶC ĐỊNH — đã chọn, đường lui ghi rõ ở `## Consequences`

| Vị trí | Lựa chọn | Lý do neo vào ràng buộc |
|---|---|---|
| Backend framework | **NestJS** | Module system ánh xạ **1-1** vào ba module của `D-01`; `createApplicationContext()` là entrypoint worker **không mở HTTP** ⇒ `R2` là một file ngắn, không phải một composition root tự viết. Với `R1` (1 dev, ⛔ không code review), cấu trúc do framework cưỡng chế đáng giá hơn cấu trúc do kỷ luật |
| Tầng DB | **Drizzle ORM** dùng như **query builder**, trên `node-postgres` | Giữ nguyên quyền viết SQL thô cho câu CLAIM; không che connection — điều kiện cần của ADR-006 |
| Frontend & UI | **Vite + React + TypeScript**, **TanStack Query**, **shadcn/ui + Tailwind CSS** | Editor là ứng dụng trạng thái nặng (kéo bubble, so sánh side-by-side, layout 0–1); TanStack Query cho polling 2 s (`D-45`) là cấu hình, không phải code hạ tầng. `shadcn/ui` (Radix Primitives) + Tailwind CSS quản lý toàn bộ UI Shell, Form (tích hợp Zod contracts), Modal, Review Gates; component code nằm trực tiếp trong repo, không vendor lock-in và tối ưu cho AI assist (`R1`) |
| Repo | **pnpm workspace**: `apps/api` · `apps/web` · `packages/contracts` | Một Dockerfile cho `apps/api`; `apps/web` là bundle tĩnh |
| Guardrail import | **ESLint boundary rule** (hoặc `dependency-cruiser`), fail build ở CI | Hiện thực trực tiếp của `D-04` |

### `TBD` — chưa có căn cứ, ⛔ không tự gán

| Chưa quyết | Vì sao chưa | Ai đóng | Khi nào |
|---|---|---|---|
| Thư viện compositor + sinh PDF (shaping tiếng Việt, 300 DPI) | Không tài liệu nào trong repo đánh giá; ⛔ không dán tên kèm con số khi chưa đo | Dev | **Spike MVP0**, nghiệm thu bằng test ở `## Consequences` |
| Phiên bản Node LTS pin cụ thể | Phụ thuộc thời điểm khởi tạo repo | Dev | Commit đầu tiên |
| Compositor chạy trong `worker_threads` hay tách hẳn thành job | Phụ thuộc số đo chưa có | Dev | Sau spike MVP0 |
| **Nghĩa vụ i18n/l10n** (font, collation, cấu hình full-text search) và **stack observability** | `SRS` §5.2 hàng `b-6`, `b-7` ghi rõ hai hạng mục này **phụ thuộc `SRS-NFR-09`** — tức phụ thuộc chính ADR này. ⚠️ **ADR này đóng việc CHỌN ngôn ngữ/framework, ⛔ KHÔNG đóng hai hàng đó.** `D-30` là một FR về **typesetting**, ⛔ không phải NFR ngôn ngữ | Dev đề xuất, Founder duyệt (`b-6`) · Dev (`b-7`) | Sau khi stack được dựng, trước MVP1 |

## Alternatives considered

### A. Python + FastAPI + SQLAlchemy Core + Alembic (frontend vẫn React/TS)

- **Ưu điểm thật**: Alembic là migration tool trưởng thành nhất trong nhóm; SQLAlchemy Core không ép sở hữu schema và viết SQL thô rất tốt; hệ sinh thái xử lý ảnh và Unicode (`regex` với `\X`, `PyICU`) mạnh.
- **Loại vì**: vi phạm `R1` theo cách khó thấy — frontend **bắt buộc** vẫn là TypeScript, nên phương án này là **hai ngôn ngữ cho một người**, mọi hợp đồng phải sinh chéo và mọi lần đổi model là hai lần sửa.
- **Và**: lợi thế lớn nhất của Python là ML/inference, mà `D-07` (⛔ không mua GPU) + `D-34` (⛔ không LLM ở runtime compiler) đẩy **toàn bộ** phần đó ra khỏi main path. Chọn ngôn ngữ vì một lợi thế nằm ngoài main path là chọn sai tiêu chí.

### B. Go + `chi`/`echo` + `sqlc` (frontend React/TS)

- **Ưu điểm thật**: một binary với hai subcommand là hiện thực **tự nhiên nhất** của `R2`; `sqlc` khớp gần như hoàn hảo với điều 3–4 của `## Decision` (SQL thô là nguồn sự thật, sinh kiểu từ SQL); tiêu thụ RAM thấp nhất.
- **Loại vì**: tầng typeset là phần nặng nhất và rủi ro nhất của sản phẩm (`D-29`, `D-30`, `D-32`) — text shaping tiếng Việt, đo bề rộng theo font, compose ảnh, sinh PDF 300 DPI. Trong Go, phần lớn việc này phải tự ghép từ thư viện mức thấp hoặc bind sang C. Với `R1` đó là rủi ro không trả nổi.
- **Và**: vẫn là hai ngôn ngữ.

### C. Full-stack monolith có view server-side (Rails / Laravel)

- **Ưu điểm thật**: tốc độ dựng CRUD cho một người là cao nhất trong tất cả phương án; migration, background job, admin có sẵn trong framework.
- **Loại vì**: editor **không phải CRUD** — kéo bubble, so sánh hai generation side-by-side, layout toạ độ 0–1, gate reset khi `text_budget` đổi (`D-33`) là ứng dụng client trạng thái nặng. Ta vẫn phải viết SPA ⇒ lợi thế biến mất, chi phí (hai ngôn ngữ) ở lại.
- **Và**: active-record có xu hướng sở hữu schema — đánh nhau trực diện với `D-10`, `D-21`, `D-51`, nơi tầng DB **phải** là tầng cưỡng chế.

### D. Prisma thay Drizzle (cùng hệ TypeScript)

- **Ưu điểm thật**: DX tốt nhất trong hệ, tài liệu dày, AI assist quen thuộc nhất.
- **Loại vì**: Prisma coi file schema của nó là nguồn sự thật và sinh migration từ đó. RLS policy, CHECK `≤3` nhân vật, trigger `origin` phải nhét vào migration bằng tay ⇒ **hai nguồn sự thật cho cùng một schema**, và cái do người viết là cái dễ bị công cụ ghi đè.
- **Và**: ADR-006 sẽ phải ghim tenant context vào **đúng connection** của transaction. Thêm một lớp trừu tượng trên connection ở **đúng chỗ không được phép sai** là rủi ro không cần thiết. (Đây là đánh giá rủi ro thiết kế, không phải khẳng định Prisma không làm được.)

### E. Next.js full-stack (route handler + server action) thay SPA + API riêng

- **Ưu điểm thật**: một deploy, một repo, ít code hạ tầng nhất; tốt cho `R1`.
- **Loại vì ba lý do độc lập**:
  1. Server action gọi thẳng DB từ component **làm mờ ranh giới** *"API là hợp đồng duy nhất"* — mà tenant context (ADR-006) phải bơm ở **một** chỗ duy nhất. Với 1 dev không code review, mỗi đường vào DB thêm là một chỗ quên `SET LOCAL`.
  2. Worker **vẫn** phải là process riêng (`R2`) — Next.js không giúp gì cho nửa nặng nhất của hệ thống.
  3. SEO không phải yêu cầu: toàn bộ sản phẩm nằm sau đăng nhập.

### F. Đưa job runtime ra ngoài (BullMQ + Redis, hoặc broker khác)

⛔ **Đây không phải một phương án và không được đọc thành một phương án.** `D-03` + `D-05` đã **CHỐT**: job queue **trong PostgreSQL**, ⛔ không broker ngoài. Mục này tồn tại **chỉ để** một run sau không tưởng rằng nó bị bỏ sót khi cân nhắc.

## Consequences

### Tích cực

- Một type system chạy suốt từ zod contract → handler → dòng DB → component React. Với `R1`, đây là khoản tiết kiệm lớn nhất mà không đánh đổi gì.
- Entrypoint thứ hai (`R2`) là một file ngắn dùng lại toàn bộ DI graph — ⛔ không có nhánh code riêng cho worker, nên không có chuyện worker và API lệch nhau về validation.
- SQL thô là nguồn sự thật ⇒ mọi guardrail tầng DB (`D-10`, `D-21`, `D-51`, `D-60`) viết được **nguyên văn**, review được bằng mắt, và test được bằng cách cố tình vi phạm.
- TypeScript + NestJS + React là vùng có mật độ dữ liệu huấn luyện cao nhất ⇒ phần *"AI assist"* của `R1` cho sản lượng cao nhất.
- `shadcn/ui + Tailwind CSS` tích hợp trực tiếp với Zod schema từ `packages/contracts` qua React Hook Form, giúp validate form ở frontend dùng chung 100% type với backend mà không cần định nghĩa lại.

### Tiêu cực — cái gì trở nên KHÓ HƠN sau quyết định này

1. **Node là single-thread — compositing 300 DPI là CPU-bound.** ⛔ **Cấm** chạy compositor trong request handler của API. Preview server-side (`D-32`) **phải** đi qua worker hoặc `worker_threads`. Vi phạm điều này thì một lần preview treo cả API — và `D-02` yêu cầu ngược lại đúng điều đó (*"worker chết mà API vẫn sống"*).
2. **Ngôn ngữ thứ hai không tránh được ở rìa.** `D-07` cho phép self-host LoRA train / upscale / inpainting — phần đó gần như chắc chắn là Python. **Guardrail**: chỉ được gọi qua adapter (giống seam của `D-40`), ⛔ không import chéo, ⛔ không nằm trên main path, ⛔ không dùng chung DB connection.
3. **`NUMERIC` không phải `number`.** Driver `pg` trả `NUMERIC` về dạng chuỗi. ⛔ **Cấm** `parseFloat`/`Number()` trên `reading_order`, `story_order` (`D-15`), `cost_usd` (`D-59`) và mọi cột credit (`D-60`). Kiểu trong `packages/contracts` cho các cột này là chuỗi/decimal, và cần một lint rule chặn ép kiểu. Đây là lỗi *sẽ* xảy ra nếu không chặn.
4. **Mất "auto-migrate".** Đổi lại việc SQL thô là nguồn sự thật, ta phải tự viết migration runner và tự viết đường lùi. Chi phí trả trước, có chủ ý — vì thứ được bảo vệ là tầng cưỡng chế của toàn hệ thống.
5. **`Intl.Segmenter` giải quyết ngắt, KHÔNG giải quyết đo.** Nó cho ranh giới grapheme/word đúng chuẩn Unicode, nhưng **không** biết chữ rộng bao nhiêu pixel. Wrap đúng = *segmentation* **+** *đo bằng chính font sẽ render*. Đây là lý do điều 8 của `## Decision` bắt wrap ở cùng runtime với compositor.
   **Nghiệm thu bắt buộc ở spike MVP0** (⛔ không được bỏ qua): corpus tiếng Việt gồm **cả NFC và NFD**, có dấu chồng (`ế`, `ữ`, `ợ`), render ở 300 DPI, kiểm tra (a) không ký tự nào bị tách khỏi dấu của nó khi xuống dòng, (b) không dấu nào bị cắt cụt bởi mép bubble, (c) chuỗi NFD và chuỗi NFC tương đương cho ra **cùng** kết quả ngắt dòng.
6. **SPA không SSR ⇒ hai hệ quả chuyển xuống ADR khác**: (a) landing/marketing page phải là tài sản tĩnh riêng, không dùng lại app; (b) **vendor auth bắt buộc phải hỗ trợ SPA + PKCE** — ràng buộc này chuyển xuống **ADR-003**.
7. **ADR-001 và ADR-006 khớp nhau ở một điểm.** Request-scoped provider của NestJS là nơi ADR-006 dự kiến móc tenant context. Nếu ADR-006 chọn cơ chế khác (ví dụ DB role per tenant), mục "Tầng MẶC ĐỊNH" của ADR này **phải được đọc lại**, không được coi là đã đóng.

### Đường lui đã ghi rõ (cho tầng MẶC ĐỊNH)

| Nếu | Thì lùi về | Chi phí đảo ngược |
|---|---|---|
| NestJS quá nặng / DI cản trở kiểm soát connection | **Fastify** + composition root tự viết + giữ nguyên cấu trúc thư mục module | Trung bình — hợp đồng và SQL không đổi |
| Drizzle không đủ trưởng thành cho một truy vấn nào đó | **Kysely** hoặc `pg` thuần cho riêng truy vấn đó | Thấp — đã là query builder, SQL thô vẫn viết được song song |
| Vite/React không đủ cho editor | Chỉ đổi **frontend**; API và hợp đồng không đổi | Thấp — nhờ điều 5 và 6 của `## Decision` |

⛔ Ba dòng **CHỐT** (một ngôn ngữ TypeScript · SQL thô là nguồn sự thật schema · API là hợp đồng duy nhất) **không có đường lui** — đổi chúng là viết ADR mới thay thế ADR này.

## Đã quyết ở đâu

### Kế thừa từ Phase 1 — ⛔ ADR này KHÔNG mở lại

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|---|---|
| Đội **1 người + AI assist**, không funding (`CF-1.2`) | — (ràng buộc bao trùm) | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) §1.3 |
| Modular monolith: 1 process · 1 PostgreSQL · 3 schema `story`/`comic`/`generation`, ⛔ không HTTP nội bộ | `D-01` | `SRS` `SRS-NFR-02` |
| Hai entrypoint (`api`, `worker`) trên cùng image, cùng codebase, khác command | `D-02` | `SRS` `SRS-NFR-03` |
| Job queue **trong PostgreSQL**, `FOR UPDATE SKIP LOCKED`, transactional enqueue | `D-03` | `SRS` `SRS-FR-25` |
| Lint rule cấm import chéo module, cưỡng chế ở CI | `D-04` | `SRS` `SRS-NFR-04` |
| ⛔ Không microservices, ⛔ không 2 PostgreSQL, ⛔ không broker ngoài | `D-05` | `SRS` `SRS-NFR-21` · §6.1 |
| ⛔ Không mua GPU — API cho main path | `D-07` | `SRS` `SRS-NFR-11` |
| RLS là lớp phòng thủ thứ hai; `tenant_id` là cột đầu mọi composite index | `D-09` | `SRS` `SRS-NFR-01` |
| ⛔ Cấm tenant isolation kiểu *"filter `tenant_id` ở tầng ứng dụng"* | `D-10` | `SRS` §3.E (khối `[!WARNING]`) |
| Khoá thời gian `reading_order`/`story_order` là `NUMERIC` sparse | `D-15` | `SRS` `SRS-FR-04` · §3.B |
| CHECK `≤3` nhân vật/panel **ở tầng DB**, ⛔ không phải guideline trong prompt | `D-21` | `SRS` `SRS-FR-08` · §5.1 |
| Layout là toạ độ chuẩn hoá 0–1 trong `page_layout JSONB` | `D-22` | `SRS` §3.D (khối `[!IMPORTANT]`) |
| Art sinh **không có chữ**; bubble là layer dữ liệu riêng | `D-29` | `SRS` `SRS-FR-11` |
| Wrap tiếng Việt **phải dùng thư viện hiểu Unicode combining marks** | `D-30` | `SRS` `SRS-FR-16` |
| Preview server-side **tái dùng compositor của export** | `D-32` | `MVP-Scope` §5.2 hàng **4** (*"Preview trang + chapter render server-side"*) · `UC-08` bước 11 |
| Visual Prompt Compiler là code deterministic, ⛔ không LLM ở runtime | `D-34` | `SRS` `SRS-FR-17` · §5.1 |
| Polling 2 giây, ⛔ không WebSocket | `D-45` | `SRS` `SRS-NFR-06` · §4.4 · §5.1 |
| `KC-4`: `generation` + `change_log` + `usage_event` trong **một** transaction | `D-50` | `SRS` `SRS-NFR-13` |
| `INSERT generation` thiếu `origin` phải **FAIL ở tầng DB** | `D-51` | `SRS` `SRS-NFR-14` |
| `cost_usd`/`model_id`/`model_version`/`attempt_no` trên **mọi** generation | `D-59` | `SRS` `SRS-FR-31` |
| Credit ledger append-only + `CHECK (available >= 0)` ở tầng DB | `D-60` | `SRS` `SRS-FR-28` · §3.F (khối `[!CAUTION]`) |

### ADR này quyết (phần Phase 1 **cố ý** để mở)

| Quyết định | Mã | Nguồn (file + mã requirement) |
|---|---|---|
| Ngôn ngữ / framework backend & frontend, ORM & migration tool | `SRS-NFR-09` (`CHƯA QUYẾT` → `TBD`) | `SRS` §3.E · [findings/architect](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) §1.8, §2.1 |
