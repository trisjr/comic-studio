# Findings — Lens ARCHITECT: ranh giới SRS ↔ 030-Specs

> **Phạm vi lens**: chỉ trả lời **một** câu hỏi — *SRS được phép khẳng định gì, và phải để lại gì cho tầng 030?* Không viết SRS, không đề xuất outline SRS, không chạm tầng 020/030.
>
> **Quy ước nhãn kép — đọc trước bảng Mục 2.** Hai hệ nhãn trong file này **trực giao**, không thay thế nhau:
> - **Nhãn nguồn** kế thừa từ bảng Canonical Facts: `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng, **không phải số đo** · `[CHỐT]` quyết định của founder tại gate. Nhãn này đo **chất lượng bằng chứng**.
> - **Mức độ rắn** (cột cuối Mục 2): **CHỐT** đã quyết, không mở lại · **MẶC ĐỊNH** đã chọn nhưng có đường lui được ghi rõ · **CHƯA QUYẾT** phải ghi `TBD` trong SRS. Nhãn này đo **độ cứng của quyết định**.
>
> Một hàng có thể là **CHỐT** về quyết định mà bằng chứng vẫn mang `[EM]` — ví dụ trần ≤3 nhân vật/panel. Khi copy số sang SRS, **copy cả nhãn nguồn** (MVP-Scope §quy ước nhãn).
>
> ⚠️ Tầng `docs/030-Specs/` hiện **rỗng** và không thuộc scope run này ⇒ file này **không tạo link nào** trỏ vào đó. Mọi chỗ cần trỏ sang design được viết dạng văn bản *"sẽ được đặc tả tại tầng 030-Specs"*.

## Table of Contents

1. [Ranh giới SRS vs 030-Specs](#1-ranh-giới-srs-vs-030-specs)
2. [Requirement kỹ thuật ĐÃ ĐƯỢC QUYẾT trong repo](#2-requirement-kỹ-thuật-đã-được-quyết-trong-repo)
3. [NFR có số đo được](#3-nfr-có-số-đo-được)
4. [Cảnh báo cho writer SRS](#4-cảnh-báo-cho-writer-srs)

---

## 1. Ranh giới SRS vs 030-Specs

> **Nguyên tắc phân định (áp cho mọi trường hợp không liệt kê dưới đây):**
> **SRS khẳng định đúng những gì đã được quyết ở tầng Planning/Analysis và KHÔNG đảo được rẻ — phát biểu dưới dạng requirement hoặc design constraint *kiểm chứng được*, kèm anchor nguồn + nhãn, kể cả khi buộc phải nêu tên cơ chế; mọi chi tiết hiện thực còn lại (DDL đầy đủ, API contract, thuật toán, tham số hoá, lựa chọn vendor) thuộc tầng 030-Specs.**

Nguyên tắc này **không** phải phép chia "WHAT vs HOW". Phép chia đó sai ở đây: `FOR UPDATE SKIP LOCKED` và key `tenant/{tenant_id}/{sha256}` đều là "how" nhưng **phải** nằm trong SRS, vì cả hai đã được quyết và cả hai retrofit sau là migration xuyên hệ thống. Tiêu chí thật là **đã-quyết + không-đảo-được-rẻ**, không phải mức độ trừu tượng.

| Chủ đề kỹ thuật | SRS khẳng định gì (mức requirement) | Để lại cho 030 gì (mức design) |
|---|---|---|
| **Multi-tenancy & RLS** | `tenant_id NOT NULL` trên **mọi** bảng nghiệp vụ; là **cột đầu tiên** của mọi composite index; Postgres **RLS** là lớp phòng thủ thứ hai; mô hình shared database + shared schema (**không** schema-per-tenant, **không** db-per-tenant); `tenant`/`user`/`membership` là ba entity riêng kể cả khi 1:1; dữ liệu nghiệp vụ trỏ `tenant_id` **không** trỏ `user_id` | Câu lệnh `CREATE POLICY` cụ thể, cách set `app.current_tenant` per session/connection pool, danh sách policy per bảng, chiến lược test rò rỉ cross-tenant, migration order |
| **Mô hình dữ liệu & khoá thời gian** | Hai trục **tách bạch** `reading_order` / `story_order`; `story_order` là `NUMERIC` **sparse** và **editable qua UI**; `timeline_id` có `kind` + `anchor_order`; state neo vào `Event` **mức scene** (không mức chapter); **một** hàm `resolveState(entity, at_event)` duy nhất; `state_at(N) = reduce(events where story_order <= N)` là hàm thuần | DDL đầy đủ từng bảng, tên/kiểu từng cột, độ chính xác `NUMERIC(p,s)`, index nào partial/covering, resolver fallback hai bước cho flashback, chiến lược renumber, ERD |
| **Job queue** | Queue nằm **trong** PostgreSQL; claim bằng `SELECT ... FOR UPDATE SKIP LOCKED`; **transactional enqueue** (`INSERT generation` + `INSERT job` trong một transaction); câu CLAIM phải chứa điều kiện fairness `in_flight_per_tenant < N`; **không** message broker riêng | Câu SQL claim đầy đủ, giá trị N, retry/backoff policy, visibility timeout, dead-letter, chỉ số queue-depth, cơ chế lease renewal |
| **Storage** | Object storage **tách khỏi DB** (không lưu ảnh blob trong Postgres); key `tenant/{tenant_id}/{sha256}`; content-address **trong phạm vi tenant**, **không dedup chéo tenant**; signed URL có hạn, **không** public bucket | Vendor cụ thể, bucket/prefix layout chi tiết, lifecycle & tiering policy, thời hạn signed URL, CDN, cấu hình CORS, cơ chế multipart upload |
| **Adapter model provider** | Adapter **per provider** là một seam bắt buộc (một interface, nhiều provider); model version **pin tường minh** trong config; compiler xuất **hai** output `text_prompt` + `conditioning_set` để adapter tiêu thụ | Interface signature, mapping tham số từng provider, error taxonomy & retry per provider, cơ chế đo/so sánh chất lượng khi đổi provider, rate-limit handling |
| **Credit/quota** | Credit ledger **append-only**; **HOLD trước khi enqueue** (check-rồi-gọi là race condition); hold reserve = **N credit/panel**; `CHECK (available >= 0)` ở **tầng DB**; **hold reaper** cho `expires_at`; hard quota **cưỡng chế trước khi enqueue**; `usage_event` append-only, billing là hàm tổng hợp trên event thô | Schema ledger/hold/usage_event, chu kỳ reaper, công thức quy đổi credit↔ảnh, kiến trúc rollup, idempotency key, tích hợp payment provider |
| **Provenance pháp lý** | `parent_generation_id` (nullable FK) + `relation_kind`; `change_log` ghi **mọi** hành động người dùng; `field_provenance` mức field + `generation.origin`; cả ba **commit cùng một transaction** với artifact chúng chứng minh; `cost_usd`/`model_id`/`model_version`/`attempt_no` trên mọi `generation` từ generation đầu tiên; provenance field ở **cấp page/panel** + export path nhúng được machine-readable marker | Schema `change_log` (event type enum, payload shape), cấu trúc `field_provenance`, định dạng marker/watermark cụ thể, export pipeline, chính sách retention & xuất hồ sơ khi cơ quan yêu cầu |
| **Deployment topology** | Modular monolith: **1 process**, **1 PostgreSQL**, **3 schema** (`story`/`comic`/`generation`), module boundary bằng package + interface (**không** HTTP nội bộ); worker là process triển khai **riêng, cùng codebase** — hai entrypoint (`api`, `worker`) trên cùng image; **không mua GPU** (API cho main path); multi-region **hoãn** | Hosting/PaaS/container platform, region, CI/CD, IaC, scaling policy, secret management, observability stack, backup/restore runbook, blue-green vs rolling |

**Ba trường hợp biên đáng nêu, vì nguyên tắc trên cho ra kết quả phản trực giác:**

| Trường hợp | Kết quả áp nguyên tắc |
|---|---|
| Cắt hẳn microservices / 2 DB / Vector DB riêng / Layout Score số thực | **Vào SRS**, dưới dạng **negative requirement** — vì đây là quyết định đã chốt "không mở lại" (CF-9), và một SRS im lặng về nó sẽ được đọc là "chưa quyết" |
| Chọn vendor auth/billing/storage cụ thể | **Không vào SRS.** Quyết định đã chốt chỉ là *"mua, không tự viết"*. Tên vendor là design ⇒ tầng 030 |
| Anti-feature "phát hiện nội dung có bản quyền" | **Vào SRS** như một cấm chỉ tường minh — vì đây là chỗ dev sẽ làm ngược theo bản năng, và làm ngược thì phá miễn trừ Điều 198b |

---

## 2. Requirement kỹ thuật ĐÃ ĐƯỢC QUYẾT trong repo

> **Cách đánh id**: bám đúng phân rã module **A–G/H** của `MVP-Scope.md` §3 — **không** tạo taxonomy thứ hai (`brief.md` Assumption 3). Hàng nhóm in đậm là module, không phải requirement.
>
> **Quy ước anchor**: `MVP-Scope §3 E1` = hàng `E1` của bảng MVP vs Full Scope · `MVP-Scope §6 KC-5` = hàng `KC-5` của danh sách cứng · `Analysis §5.7 #1` = mục con của Analysis · `CF-x.y` = hàng bảng Canonical Facts tại `pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md` · `R-nn` = hàng Risk Log · `Charter §7 C3` = hàng ràng buộc Charter.

### 2.1 Nhóm E — Multi-tenancy & hạ tầng

| id đề xuất | Phát biểu requirement | Đã quyết ở đâu | Mức độ rắn |
|---|---|---|---|
| **SRS-NFR-01** | `tenant_id NOT NULL` trên **MỌI** bảng nghiệp vụ, là **cột ĐẦU TIÊN** của mọi composite index, cộng **Postgres RLS** làm lớp phòng thủ thứ hai. Mô hình shared DB + shared schema — **không** schema-per-tenant, **không** db-per-tenant | `MVP-Scope §6 KC-5` (*"không mở ra thương lượng scope"*) · `MVP-Scope §3 E1` · `Analysis §5.7 #1` · `Charter §4` ba yêu cầu hạ tầng (CF-8.7) · `R-16` | **CHỐT** |
| **SRS-FR-01** | `tenant` / `user` / `membership` là **ba entity riêng** ngay từ đầu, kể cả khi quan hệ là 1:1. Mọi dữ liệu nghiệp vụ trỏ `tenant_id`, **không** trỏ `user_id` | `MVP-Scope §3 E2` · `Analysis §5.7 #2` | **CHỐT** |
| **SRS-NFR-02** | Modular monolith: **1 process**, **1 PostgreSQL**, **3 schema** (`story` / `comic` / `generation`), module boundary bằng package + interface — **không HTTP nội bộ** | `MVP-Scope §3 E5` · `MVP-Scope §4.2` (CF-9.2) · `Analysis §6.2` | **CHỐT** |
| **SRS-NFR-03** | Worker là **process triển khai riêng, CÙNG codebase** — hai entrypoint (`api`, `worker`) trên cùng repo/image, khác command. Yêu cầu vận hành: worker chết mà **API vẫn sống** | `MVP-Scope §3 E7` · `Analysis §6.2` bảng seam kinh tế | **CHỐT** |
| **SRS-NFR-04** | Lint rule **cấm import chéo module**: `comic` gọi `story` qua **DUY NHẤT** `resolveState()` và `getBible()` | `Analysis §6.2` seam #3 | **CHỐT** |
| **SRS-FR-02** | Object storage **tách khỏi DB từ ngày đầu** (không bao giờ lưu ảnh blob trong Postgres); key **`tenant/{tenant_id}/{sha256}`**, content-address **TRONG phạm vi tenant**, **KHÔNG dedup chéo tenant**; signed URL có hạn, **không bao giờ** public bucket | `MVP-Scope §3 E3` · `Analysis §5.7 #4` | **CHỐT** |
| **SRS-FR-03** | **Mua** auth và billing, **không tự viết** | `MVP-Scope §3 E4` · `Analysis §5.7` (*"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"*) | **CHỐT** |
| **SRS-NFR-05** | Kỷ luật `ON DELETE CASCADE` + **một đường hard-delete tenant đã kiểm thử**, tách biệt khỏi soft-delete của takedown | `MVP-Scope §3 GP-5` · `Analysis §5.7 #5` | **CHỐT** |
| **SRS-NFR-06** | Cập nhật trạng thái job cho client bằng **polling 2 giây**, không WebSocket | `Analysis §6.2` | **MẶC ĐỊNH** — đường lui ghi rõ trong chính lý do: *"generation mất hàng chục giây, polling là quá đủ"* ⇒ tiền đề đảo (generation nhanh hơn nhiều) thì mở lại được |
| **SRS-NFR-07** | Hosting / PaaS / container platform / region đặt máy | **Không anchor được** — grep toàn `docs/010-Planning/`, `Analysis`, `Glossary` không có quyết định nào. Phần đã quyết chỉ gồm: 2 entrypoint 1 image (E7), worker riêng, **không mua GPU** (`Analysis §9`), multi-region hoãn (E8) | **CHƯA QUYẾT** → `TBD` |
| **SRS-NFR-08** | Vendor cụ thể của auth / billing / object storage | `MVP-Scope §3 E4` chỉ quyết *"mua"*; `E3` chỉ quyết **key schema**. Tên vendor không xuất hiện ở bất kỳ tài liệu nào | **CHƯA QUYẾT** → `TBD` |
| **SRS-NFR-09** | Ngôn ngữ / framework backend & frontend | Không anchor được. `CF-1.3` `[OFF]`: *"chưa có dòng nào"* — `src/`, `test/`, `openspec/changes/` đều rỗng | **CHƯA QUYẾT** → `TBD` |

### 2.2 Nhóm B + C — Story Intelligence, Comic IR, khoá thời gian

| id đề xuất | Phát biểu requirement | Đã quyết ở đâu | Mức độ rắn |
|---|---|---|---|
| **SRS-FR-04** | **Thay hẳn `(chapter, scene)`** làm khoá thời gian bằng: hai trục tách bạch `reading_order` / `story_order` (`NUMERIC` **sparse**, bước nhảy 1000, **editable qua UI**); `timeline_id` có `kind` (`main`/`flashback`/`parallel`/`dream`) + `anchor_order`; state neo vào `Event` **mức scene** (cho phép chia nhỏ bằng `beat_no`), **không** mức chapter | `MVP-Scope §3 B4` (*"phải sửa trước dòng code đầu tiên"*) · `Analysis §5.1` · `R-15` | **CHỐT** |
| **SRS-NFR-10** | **Một** hàm `resolveState(entity, at_event)` duy nhất cho mọi query state, cộng test guardrail: **không được có `ORDER BY chapter_no`** trong bất kỳ đường dẫn resolve state nào | `Analysis §5.1` điểm 6 · `R-15` cột trigger (*"hoặc có nhiều hơn một hàm truy vấn state trong codebase"*) | **CHỐT** |
| **SRS-FR-05** | Story Bible state là **hàm thuần** trên event: `state_at(N) = reduce(events where story_order <= N)`. LLM chỉ phát **event** (`entity, attribute, value, permanence, evidence_span, confidence`) cho **một** chapter; **code sở hữu state** | `MVP-Scope §3 B3` · `Analysis §5.5` | **CHỐT** |
| **SRS-FR-06** | **Chapter parse + text clean là bước ĐẦU TIÊN** của pipeline, và là **code deterministic** (regex/heuristic), không LLM | `MVP-Scope §3 B1` · `CF-8.7` · `Analysis §5.5` | **CHỐT** |
| **SRS-FR-07** | Comic IR / Panel Specification: **spec là dữ liệu chính, ảnh chỉ là output/cache**. Panel spec **tách khỏi granularity render** — một page compile được nhiều panel spec thành một prompt | `MVP-Scope §3 C1` · `Analysis §9b.3` | **CHỐT** |
| **SRS-FR-08** | **Cứng hoá trần ≤3 nhân vật/panel trong schema Comic IR** (constraint + validation), **không** phải guideline trong prompt. Cảnh đông người giải bằng shot xa / silhouette / crop | `Charter §7 C3` `[OFF]` CF-6.5 · `Charter §4 R1` · `MVP-Scope §3 C5` · `R-12` | **CHỐT** *(bằng chứng mang caveat `CF-6.4`: không benchmark độc lập nào đo frontier model ở 2–3 nhân vật ⇒ MVP0 phải tự đo — caveat này **không** làm lỏng quyết định)* |
| **SRS-FR-09** | Layout quyết định bằng **rubric `beat_type` rời rạc** (enum có anchor example) + `dialogue_density` **do code đếm** + `character_count` **do code đếm** → **bảng tra deterministic**; cộng **emphasis budget theo phạm vi chapter**. LLM chỉ **xếp hạng** beat trong chapter, code phân bổ theo quota | `MVP-Scope §3 C3` · `CF-9.3` · `Analysis §5.3` (A)+(B) | **CHỐT** về cơ chế |
| **SRS-FR-10** | User đổi layout template bằng **một click** — lối thoát khi rubric chấm sai | `Analysis §5.3` (D) (*"luôn phải có"*) | **CHỐT** |
| **SRS-FR-11** | **Chữ đi qua typeset layer riêng**: art sinh **KHÔNG có chữ** (`text, letters, watermark, speech bubble` vào negative prompt), bubble là **layer dữ liệu riêng** với toạ độ **chuẩn hoá 0–1** (cùng dữ liệu render được thumbnail và bản in 300 DPI), **không nướng vào ảnh** | `Charter §4 R2` · `MVP-Scope §3 A2` (CF-8.11c) · `Analysis §5.4` | **CHỐT** |
| **SRS-FR-12** | **Hai** field cho thoại, không phải một: `dialogue_source` (nguyên văn + `source_span`, **bất biến**) và `dialogue_rendered` (bản đã nén, người sửa được, và **edit của người phải khoá lại** khỏi bị re-run ghi đè) | `Analysis §5.4` | **CHỐT** |
| **SRS-FR-13** | `text_safe_zone` + `text_budget` + `negative_space_hint` là **field của panel spec**, và Visual Prompt Compiler **phải truyền yêu cầu chỗ trống xuống prompt** — ràng buộc đi **ngược** từ typesetting vào compiler | `MVP-Scope §3 C6` (CF-8.8) · `Analysis §5.4` lý do 2 | **CHỐT** |
| **SRS-FR-14** | **Hai human gate bắt buộc**: (1) speaker attribution, (2) dialogue condensation. Không phải tuỳ chọn, không dồn sang MVP4. Kèm: anchor deterministic bằng regex **trước** LLM; LLM bị **constrained** vào tập nhân vật có mặt trong scene; `UNKNOWN` là giá trị **hợp lệ**; lưu `speaker_confidence` và **hiện cờ trong UI khi thấp** | `MVP-Scope §3 C7` · `CF-8.8` · `Analysis §5.4b` | **CHỐT** |
| **SRS-FR-15** | Thứ tự pipeline: **dialogue condensation nằm SAU layout**, vì `text_budget` phụ thuộc diện tích panel | `Analysis §5.4` (*"Thứ tự trong §17 làm sai chỗ này"*) | **CHỐT** |
| **SRS-FR-16** | Auto-placement bubble **phải tự build**; ở MVP là heuristic (gần speaker, tránh vùng có mặt, thứ tự đọc) + **cho user kéo tay**. Wrap tiếng Việt phải dùng thư viện hiểu Unicode combining marks | `Analysis §5.4` · `R-18` (không cạnh tranh ở typesetting) | **CHỐT** |

### 2.3 Nhóm A — Pipeline sinh ảnh, compiler, queue

| id đề xuất | Phát biểu requirement | Đã quyết ở đâu | Mức độ rắn |
|---|---|---|---|
| **SRS-FR-17** | **Visual Prompt Compiler là code deterministic — KHÔNG có LLM ở runtime.** Bản chất: tra bảng `field value → cụm từ`, sắp thứ tự, dedup, xử lý xung đột theo **precedence ladder**, thực thi **constraint budget**, ghi **drop log** (`generation.degradations JSONB`) | `MVP-Scope §3 A3` · `Glossary` mục *Visual Prompt Compiler* · `Analysis §5.5` · `Charter §4 R8` | **CHỐT** — và là **điều kiện cần** để bảng `Generation` có nghĩa |
| **SRS-FR-18** | Compiler xuất **HAI** output: `text_prompt` **và** `conditioning_set`. Identity reference **không được** cạnh tranh với mô tả cảnh trong cùng một chuỗi text | `Analysis §5.5` (phân xử mâu thuẫn §8 vs §16 của `Request.md`) | **CHỐT** |
| **SRS-FR-19** | LLM chỉ được xuất hiện trong compiler ở **hai chỗ hẹp**, và **phải cache**: (a) soạn từ vựng **offline** một lần → người review → **lưu vào bảng** (là dữ liệu, không phải runtime); (b) dịch action tự do → cụm pose khi từ vựng chưa có entry, **cache theo hash của action text**. Ngoài hai việc đó: không có LLM trong compiler | `Analysis §5.5` | **CHỐT** |
| **SRS-FR-20** | **best-of-N**: generate **N candidate cho MỌI panel** rồi VLM QA-select 1. **KHÔNG phải retry-on-failure.** N mặc định = **3** | `Charter §7 C8` `[OFF]` CF-3.1, CF-3.2 · `MVP-Scope §3 A1` · `Glossary` mục *best-of-N (N=3)* | Cơ chế **CHỐT** · giá trị **N = 3** là **MẶC ĐỊNH** — đường lui ghi rõ: `CF-8.5` đặt *"N tối thiểu"* là **một trong ba chỉ số bắt buộc MVP0 phải đo**, mỗi bậc N giảm được là **~33% COGS**. ⚠️ **Budget** thì vẫn phải ở N=3 (`Charter §4 R7`) |
| **SRS-FR-21** | **Continuity Checker = QA-based selection giữa N candidate**, output là **hàng đợi review được xếp hạng**. Cắt hẳn `[Fix automatically]`; phiên bản hợp lệ là **"Tạo lại với ràng buộc được nhấn mạnh"** — giữ cả hai version, hiển thị side-by-side, **người chọn**, không bao giờ tự áp dụng. `unclear` là câu trả lời hợp lệ **hạng nhất** | `Glossary` mục *Continuity Checker* (*"Mọi tài liệu mới phải dùng nghĩa sau"*) · `MVP-Scope §3 H3` · `CF-8.10` · `Analysis §5.2` | **CHỐT** |
| **SRS-FR-22** | Hệ thống **phải hiện tường minh độ phủ của checker** cho user: *"đã kiểm N/M panel, M−N panel không kiểm được vì có nhiều nhân vật"* | `Charter §8 A9` `[EM]` CF-6.11 · `Analysis §5.2` (*"đây không phải chi tiết kỹ thuật mà là yêu cầu giao tiếp sản phẩm"*) | **CHỐT** — đây là **FR minh bạch**, không phải chỉ tiêu chất lượng |
| **SRS-FR-23** | **Adapter per image provider** là seam bắt buộc (một interface, nhiều provider: Gemini 3 Pro Image, FLUX.2); **pin model version tường minh** trong config | `MVP-Scope §3 A4` · `Analysis §6.2` seam #4 · `R-22` | Seam **CHỐT** · provider chính là **MẶC ĐỊNH**: Gemini batch mặc định, **đường lui đã ghi rõ** là FLUX.2 pro `$0.03` `[OFF]` (`R-10`, `R-22`) |
| **SRS-FR-24** | Dùng **batch API**, không realtime API — comic generation vốn là async job queue nên batch là fit tự nhiên | `Analysis §9` (*"khoản tiết kiệm lớn nhất mà không đánh đổi gì"*) | **MẶC ĐỊNH** — đường lui ghi rõ: `CF-3.11` lấy **giá standard** làm trần an toàn cho MVP0 *"vì cần vòng lặp nhanh nên batch khó dùng"* |
| **SRS-NFR-11** | **Không mua GPU.** API cho main path; self-host chỉ cho LoRA train, upscale, inpainting | `Analysis §9` | **CHỐT** |
| **SRS-FR-25** | **Job queue nằm TRONG PostgreSQL**, claim bằng `SELECT ... FOR UPDATE SKIP LOCKED`; **transactional enqueue**: `INSERT generation` + `INSERT job` trong **một** transaction ⇒ **không bao giờ có job mồ côi** | `MVP-Scope §3 A5` · `Analysis §6.2` | **CHỐT** |
| **SRS-FR-26** | Câu **CLAIM job phải chứa** điều kiện fairness per tenant: `in_flight_per_tenant < N` — nhồi vào sau là sửa lại đúng câu SQL nóng nhất | `MVP-Scope §3 A6` · `Analysis §6.2` bảng seam kinh tế | Cơ chế **CHỐT** · giá trị **N**: **CHƯA QUYẾT** → `TBD` (không con số nào trong repo) |
| **SRS-FR-27** | Prop quan trọng đưa vào **reference image như một entity riêng**, không mô tả bằng chữ trong prompt | `R-13` (mitigation, status `accepted`) · `CF-6.3` `[OFF]` Props **4.19/5** là metric thấp nhất | **CHỐT** |

### 2.4 Nhóm F — Kinh tế & credit

| id đề xuất | Phát biểu requirement | Đã quyết ở đâu | Mức độ rắn |
|---|---|---|---|
| **SRS-FR-28** | **Credit ledger append-only + HOLD trước khi enqueue** (check-rồi-gọi là **race condition**) + `CHECK (available >= 0)` **ở tầng DB** (chốt cuối, không bypass được bằng code) + **hold reaper** cho `expires_at`. **Hold reserve = N credit/panel** (N mặc định 3, kế thừa SRS-FR-20), **không phải 1** | `MVP-Scope §6 KC-7` · `CF-6.12` · `Charter §4` ba yêu cầu hạ tầng · `R-14` | **CHỐT** |
| **SRS-FR-29** | **Hard quota cưỡng chế TRƯỚC khi enqueue**, không đếm sau, không cảnh báo sau | `MVP-Scope §3 F4` · `CF-8.11b` · `R-07` | **CHỐT** |
| **SRS-FR-30** | `usage_event` **append-only** + rollup `usage_daily`; billing/metric là **hàm tổng hợp trên event thô**, **không** counter tăng tại chỗ. **Regen ratio là metric first-class**, đo theo p50/p90 từ MVP0 | `MVP-Scope §3 F1` · `Analysis §5.7 #6` · `Analysis §6.2` bảng seam kinh tế | **CHỐT** |
| **SRS-FR-31** | `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **MỌI** `generation`, từ **generation ĐẦU TIÊN** — dữ liệu lịch sử **không backfill được** | `MVP-Scope §3 F2` · `Analysis §5.7 #3` | **CHỐT** |
| **SRS-FR-32** | Kiến trúc billing + credit ledger + onboarding phải đỡ được **BA tầng ngay từ đầu, không retrofit**: tầng 1 **không có image gen** (không cần API key) · tầng 2 **credit pack không hết hạn** (managed inference) · tầng 3 **BYOK là tùy chọn MỞ KHOÁ**, không phải điều kiện dùng sản phẩm | `Charter §7 C2` `[CHỐT]` · `CF-2.1`–`CF-2.4` · `MVP-Scope §3 F5, F6` | **CHỐT** |
| **SRS-FR-33** | Render granularity: **per-panel** là mặc định (spec là đơn vị); **whole-page** là **đường lui đã thiết kế sẵn** và đổi được **không đổi data model** | `MVP-Scope §3 A7` (*"đường lui của G2"*) · `Analysis §9b.3` | **MẶC ĐỊNH** — đường lui tường minh, gắn vào gate G2 |
| **SRS-NFR-12** | **Đừng dựa vào cache để cứu margin.** Hai chỗ ra tiền thật là **reference-sheet amortization** và **idempotency** | `CF-6.13` `[EM]` (hit rate **vài % → ~10%**, `architect` **tự khai là ước lượng**) · `R-17` status `accepted` | **CHỐT** |

### 2.5 Nhóm G — Provenance & pháp lý

| id đề xuất | Phát biểu requirement | Đã quyết ở đâu | Mức độ rắn |
|---|---|---|---|
| **SRS-FR-34** | `parent_generation_id` (**nullable FK**) + `relation_kind ENUM('retry','variation','refine','continuity_fix')` — từ **migration số 1**, không phải backlog | `MVP-Scope §6 KC-1` · `CF-7.3` `[OFF]` · `CF-9.4` (PM run trước **tự thu hồi** khuyến nghị cắt) · `R-01` | **CHỐT** |
| **SRS-FR-35** | `change_log` append-only ghi **MỌI** hành động người dùng — kể cả *"chọn generation X thay vì Y"*, sửa thoại, đổi camera, kéo bubble. **Prompt một mình không chứng minh được *"decisive contribution"*** | `MVP-Scope §6 KC-2` · `CF-7.2` `[OFF]` NĐ 134/2026 Điều 5a | **CHỐT** |
| **SRS-FR-36** | `field_provenance` (mức **field**) + `generation.origin ENUM('ai','ai_edited','human')` | `MVP-Scope §6 KC-3` · `Glossary` mục *`field_provenance` / `change_log`* | **CHỐT** |
| **SRS-NFR-13** | **KC-1 + KC-2 + KC-3 phải commit CÙNG MỘT TRANSACTION** với artifact mà chúng chứng minh (`INSERT generation` + `INSERT change_log` + `INSERT usage_event` bất khả phân). *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* | `MVP-Scope §6 KC-4` · `Analysis §6.2` lý do 2 (CF-9.2) | **CHỐT** |
| **SRS-NFR-14** | Guardrail tầng DB: mọi `INSERT` vào `generation` **thiếu `origin` phải fail ở tầng DB** | `R-01` cột mitigation | **CHỐT** |
| **SRS-FR-37** | **Kiểm opt-out signal Điều 37b ngay trong bước ingest**: đọc metadata / rights-management-info của file user upload, **log kết quả kèm timestamp**, **chặn nếu có signal bảo lưu**. Ingest là nơi **duy nhất** file của user lần đầu vào hệ thống | `MVP-Scope §6 KC-6` · `MVP-Scope §3 GP-2` · `CF-7.5` `[OFF]` tóm tắt · `R-06` · `Analysis §8.3` item 6 | **CHỐT** |
| **SRS-FR-38** | **Checklist safe harbour Điều 198b**: công cụ tiếp nhận takedown (form + `copyright@`), **đăng ký đầu mối (email + số điện thoại) với Bộ VHTTDL**, và xử lý bằng **soft-delete + disable-access ở cấp project** — **KHÔNG hard delete**, còn phải giữ dữ liệu cho counter-notice | `MVP-Scope §3 GP-3` · `CF-7.6` `[OFF]` tóm tắt · `R-02` · `Analysis §8.3` | **CHỐT** |
| **SRS-NFR-15** | ⛔ **Anti-feature**: hệ thống **KHÔNG được** có bộ phát hiện *"truyện này có thể có bản quyền của người khác"* (copyright detection / plagiarism check / similarity scan) **trước khi có xác nhận của luật sư** — vì nó tạo ra đúng tri thức mà điều kiện (a) *"không biết"* của miễn trừ Điều 198b đang miễn trừ cho việc **không có**. Phân biệt rõ: **đọc opt-out signal do chính chủ quyền gắn vào file là dữ kiện khách quan, được phép** (SRS-FR-37) | `R-04` · `Analysis §8.3` khối *Nghịch lý safe harbour* | **CHỐT** |
| **SRS-FR-39** | **AI provenance metadata field ở cấp page/panel**, và **export path phải nhúng được machine-readable watermark**. Vì phạm vi khoản 4 Điều 11 chưa rõ, **thiết kế theo diễn giải RỘNG (mọi nội dung AI)** cho tới khi luật sư chốt | `Charter §7 C4` (*"phải thiết kế theo diễn giải rộng"*) · `MVP-Scope §3 GP-4` · `CF-7.7` `[OFF]` · `R-03` · `Analysis §8.4` | **CHỐT** — quy tắc tạm thời *"diễn giải rộng"* **là một quyết định**, không phải một `TBD` |
| **SRS-FR-40** | Cơ chế để **user nhận biết đang tương tác với hệ thống AI** (Điều 11 Luật TTNT 2025) | `Analysis §8.4` bảng Điều 11 · `R-03` cột trigger | **CHỐT** |
| **SRS-NFR-16** | Watermark của model provider (**SynthID** đã nhúng trong Nano Banana Pro) có thoả nghĩa vụ đánh dấu máy đọc hay không | `Analysis §8.4` (*"Phải verify, không giả định"*) · `R-03` · `RB-01` câu 2 | **CHƯA QUYẾT** → `TBD`. Đường lui đã ghi: nếu không được chấp nhận thì tự nhúng watermark ở export path — **chi phí chưa ước lượng** |
| **SRS-FR-41** | ToS: **user warrant + indemnify**; **assign toàn bộ quyền output cho user** kèm disclaimer bất định pháp lý theo jurisdiction; checkbox cam kết quyền gắn vào **BƯỚC UPLOAD**, không chỉ ở trang ToS. DMCA designated agent nếu nhắm thị trường Mỹ | `MVP-Scope §3 GP-5` · `R-05` · `Analysis §8.3` | **CHỐT** |
| **SRS-NFR-17** | **Ba câu hỏi pháp lý phải mang tới luật sư SHTT Việt Nam TRƯỚC khi thương mại hoá** (Điều 37a có áp cho inference-time extraction? · phạm vi khoản 4 Điều 11? · nền tảng *hosting + processing* có được coi là trung gian theo Điều 198b?) | `Charter §4 R6` · `Charter §9.1` điều kiện chặn cấp dự án · `CF-7.8`, `CF-7.9` · `RB-01` · `Analysis §8.5` | **CHỐT** là điều kiện chặn · nội dung câu trả lời: **CHƯA QUYẾT** → `TBD` (rủi ro **nhị phân** duy nhất) |

### 2.6 Nhóm H — Chất lượng & vận hành

| id đề xuất | Phát biểu requirement | Đã quyết ở đâu | Mức độ rắn |
|---|---|---|---|
| **SRS-NFR-18** | **HITL gate + eval kit ngay tại MVP1**, không dồn MVP4; **log preference data từ MVP1** | `MVP-Scope §3 H1, H2` · `CF-8.7` · `Charter §4 R9` | **CHỐT** |
| **SRS-NFR-19** | **Golden dataset regression** (spec + ref + ảnh + đánh giá), chạy **định kỳ**, lưu kết quả để so sánh theo thời gian — phòng **silent model drift** | `MVP-Scope §3 H6` · `R-22` | **CHỐT** |
| **SRS-NFR-20** | **Abuse controls tối thiểu**: rate limit per tenant, giới hạn dung lượng/số upload, **ghi lại mọi lần provider từ chối vì content policy** (tín hiệu abuse sớm gần như miễn phí) | `MVP-Scope §3 H5` · `Analysis §5.7` | Cơ chế **CHỐT** · **ngưỡng số: CHƯA QUYẾT** → `TBD` |
| **SRS-FR-42** | Export **PDF / CBZ / webtoon** — *"thứ duy nhất trong MVP4 người dùng thật sự nhận được"* ⇒ được **nâng ưu tiên lên sớm** | `MVP-Scope §3 H4` · `CF-8.10` | **CHỐT** |

### 2.7 Negative requirements — những gì bị CẮT HẲN

> Ba lý do phải viết vào SRS thay vì im lặng: (a) `CF-9` ghi rõ *"đã có kết luận, **không mở lại**"*; (b) một SRS im lặng về chúng sẽ bị đọc là *"chưa quyết"*; (c) hai trong số này rất dễ bị **cắt lẫn sang thứ phải giữ**.

| id đề xuất | Phát biểu requirement (dạng phủ định) | Đã quyết ở đâu | Mức độ rắn |
|---|---|---|---|
| **SRS-NFR-21** | Hệ thống **KHÔNG** dùng microservices (3 service), **KHÔNG** 2 PostgreSQL, **KHÔNG** Vector DB riêng, **KHÔNG** job queue ngoài Postgres. ⚠️ **`pgvector` KHÔNG bị cấm** — `B5` để mở ở Full Scope *"khi có bằng chứng SQL+FTS không đủ"*. Thay thế ở MVP: **Story Bible là index của mình** (SQL) + PostgreSQL full-text search | `MVP-Scope §3 E6` (`❌ cắt hẳn`) vs `B5` · `CF-9.2` · `Analysis §6.2` | **CHỐT** |
| **SRS-NFR-22** | Hệ thống **KHÔNG** dùng **Layout Score 5 số thực**. **Cắt cơ chế, GIỮ mục tiêu** (layout theo narrative importance) — thay bằng SRS-FR-09 | `MVP-Scope §3 C4` (`❌ cắt hẳn`) · `CF-9.3` · `Analysis §6.3` | **CHỐT** |
| **SRS-NFR-23** | **KHÔNG** UI duyệt **cây** generation (tree view / diff view / branch-merge) — flat list theo `created_at` + `approved_generation_id` là đủ. ⚠️ **Cắt UI, KHÔNG cắt cột dữ liệu** — `parent_generation_id` vẫn bắt buộc (SRS-FR-34) | `MVP-Scope §3 D6` (`❌ cắt hẳn`) vs `MVP-Scope §6 KC-1` · `MVP-Scope §3.1`, `§6.1` · `Analysis §6.3`–`§6.4` | **CHỐT** |
| **SRS-NFR-24** | **KHÔNG** subscription phẳng unlimited; **KHÔNG** free tier kiểu *"100 ảnh/ngày"* | `CF-2.7` · `Charter §4 R5` · `R-07` | **CHỐT** |
| **SRS-NFR-25** | Hoãn khỏi horizon: infinite canvas / zoom-pan cả chapter / hình học panel tự do, undo-redo xuyên state phân tán, realtime collaboration, inpainting brush, expression sheet đầy đủ | `MVP-Scope §3 D2`–`D5`, `D7` · `CF-9.1` | **MẶC ĐỊNH** — đường lui ghi rõ ở cột Full Scope: `D2` = *"🟡 nếu có bằng chứng khách cần"*, `D5` = *"🟡 kèm `generation.origin='ai_edited'`"* |
| **SRS-NFR-26** | Hoãn khỏi horizon: SSO/SAML, team nhiều thành viên có role, custom domain / white-label, multi-region, fine-tune riêng từng tenant, self-serve refund tự động | `MVP-Scope §3 E8` · `Analysis §5.7` mục *"Hoãn được"* | **CHỐT** (về việc hoãn) |

### 2.8 Tổng kết đếm

**Tổng: 68 hàng requirement** (SRS-FR-01…42 · SRS-NFR-01…26).

| Mức độ rắn | Số hàng | Ghi chú |
|---|---:|---|
| **CHỐT** (thuần) | **55** | Trong đó **7** hàng phủ trọn `MVP-Scope §6` danh sách cứng — *"không mở ra thương lượng scope"*: KC-1→SRS-FR-34 · KC-2→SRS-FR-35 · KC-3→SRS-FR-36 · KC-4→SRS-NFR-13 · KC-5→SRS-NFR-01 · KC-6→SRS-FR-37 · KC-7→SRS-FR-28 |
| **MẶC ĐỊNH** | **6** | Thuần **4**: SRS-NFR-06 (polling 2s) · SRS-FR-24 (batch API) · SRS-FR-33 (per-panel granularity) · SRS-NFR-25 (canvas/collab/inpainting hoãn). **Lai** với CHỐT **2**: SRS-FR-20 (cơ chế best-of-N CHỐT, **giá trị N** MẶC ĐỊNH) · SRS-FR-23 (seam adapter CHỐT, **provider chính** MẶC ĐỊNH) |
| **CHƯA QUYẾT** → `TBD` | **7** | Thuần **4**: SRS-NFR-07 (hosting/region) · SRS-NFR-08 (vendor auth/billing/storage) · SRS-NFR-09 (ngôn ngữ/framework) · SRS-NFR-16 (SynthID có thoả nghĩa vụ?). **Lai** với CHỐT **3**: SRS-FR-26 (cơ chế fairness CHỐT, **giá trị N** TBD) · SRS-NFR-20 (abuse control CHỐT, **ngưỡng số** TBD) · SRS-NFR-17 (điều kiện chặn CHỐT, **nội dung câu trả lời của luật sư** TBD) |

> Năm hàng **lai** (SRS-FR-20, FR-23, FR-26, NFR-17, NFR-20) là chỗ writer dễ trượt nhất: **cơ chế đã CHỐT nhưng một tham số bên trong nó chưa quyết**. Cách viết đúng là khẳng định cơ chế rồi để `TBD` riêng cho tham số — **không** hạ cả hàng xuống `TBD`, cũng **không** tự chọn tham số.

---

## 3. NFR có số đo được

> **Điều kiện vào bảng này**: chỉ tiêu **truy được về một con số cụ thể trong repo**. Con số nào không truy được ⇒ xuống mục 3.2 dưới nhãn `TBD`, **không tự gán số**.
>
> ⚠️ **Copy số thì copy cả nhãn** — nhãn `[EM]` nghĩa là *khoảng trống dữ liệu được thừa nhận*, không phải sự thật đã đo.

### 3.1 Có chỉ tiêu

| NFR | Chỉ tiêu | Nguồn | Nhãn |
|---|---|---|---|
| **Takedown SLA** | **72 giờ** (quy trình kép *"72 giờ và 10 ngày làm việc"*; mốc **24 giờ** chỉ áp cho livestream ⇒ không áp cho comic-studio) | `CF-7.6` · `MVP-Scope §3 GP-3` · `R-02` · `Analysis §8.3` | `[OFF]` **tóm tắt, không phải nguyên văn điều luật** |
| **Deadline compliance AI disclosure** | **~01/03/2027** (12 tháng chuyển tiếp từ 01/03/2026, lĩnh vực ngoài y tế/giáo dục/tài chính) | `Charter §7 C4` · `CF-7.7` · `Analysis §8.4` | `[OFF]` ⚠️ **hai nguồn mô tả phạm vi KHÁC NHAU** |
| **best-of-N** | **N = 3** candidate/panel, mặc định **mọi** panel (*"Performance saturates at N=3"*) | `CF-3.1` · `Charter §7 C8` · `MVP-Scope §3 A1` | `[OFF]` arXiv 2604.13452 |
| **Trần nhân vật/panel** | **≤ 3** | `CF-6.5` · `Charter §7 C3` · `MVP-Scope §3 C5` | `[OFF]` arXiv 2606.15867 — ID-Sim **42.33** (2) → **27.21** (3) → **2.67** (4) → **0.52** (5). ⚠️ caveat `CF-6.4`: **không benchmark độc lập nào** đo frontier model ở 2–3 nhân vật |
| **Hold reserve credit** | **3 credit/panel** (= N của best-of-N), **không phải 1** | `MVP-Scope §6 KC-7` · `CF-6.12` · `R-14` | dẫn xuất từ `[OFF]` `CF-3.1` |
| **Ngưỡng phân tuyến tầng 2 / tầng 3** | **~125 ảnh/tháng** (dưới ngưỡng credit thắng, trên ngưỡng BYOK thắng) | `CF-2.5` · `Charter §7 C2` · `R-07` | `[TC]` ⚠️ **vendor blog của bên bán managed inference** — chấp nhận được vì khuyến nghị ngược chiều lợi ích của họ |
| **Constraint budget của compiler** | **5–8** ràng buộc thị giác được tôn trọng đồng thời (trong khi §16 gốc của `Request.md` bung ra dễ đạt **20–40**) | `Analysis §5.5` | `[EM]` — Analysis ghi rõ *"trần thực tế **ước lượng** 5-8"* |
| **Emphasis budget/chapter** | tối đa **1 full page + 2–3 large panel** | `Analysis §5.3` (B) | `[EM]` — đề xuất của lens, không có hàng CF tương ứng |
| **Cổng chất lượng check report-only** | **precision ≥ ~0.7** trên **≥ 100 panel dán nhãn tay**, **trước khi bật một check nào** — kể cả `face` | `Analysis §5.2` | `[EM]` — ngưỡng do lens đặt ra |
| **Độ phủ Continuity Checker** | **40–60% số panel** (phần còn lại là panel nhiều nhân vật ⇒ không kiểm được vì vòng lặp re-identification) | `CF-6.11` · `Charter §8 A9` · `Analysis §5.2` | `[EM]` ⚠️ **đây là chỉ tiêu PHẢI CÔNG BỐ cho user (SRS-FR-22), KHÔNG phải mục tiêu chất lượng để đạt** |
| **Golden dataset regression** | **15–20 panel** (spec + ref + ảnh + đánh giá) | `MVP-Scope §3 H6` | quyết định run planning 2026-08-23 |
| **Expression sheet (MVP3)** | **3 góc + 3 biểu cảm** mỗi nhân vật (không phải sheet đầy đủ) | `MVP-Scope §3 D7` · `Analysis §6.3` | quyết định run planning 2026-08-23 |
| **`story_order` sparse step** | bước nhảy **1000**, kiểu `NUMERIC` (không `INT` tuần tự) | `Analysis §5.1` điểm 4 | quyết định kỹ thuật của lens `architect` |
| **Polling interval trạng thái job** | **2 giây** | `Analysis §6.2` | quyết định kỹ thuật của lens `architect` |
| **COGS sàn/chapter** | **$12,06** @N=3, Gemini batch — ⛔ **là SÀN, không phải trần** (chưa tính VLM call để score 3 candidate) | `CF-3.5` · `Charter §7 C7` · `R-08` | `[EM tính từ OFF]` ⛔ `Charter §7 C7` **cấm** dùng con số này như chi phí thực tế mà không nêu nó là sàn |
| **Trần chi phí MVP0** | **~$12** (giá standard `$0.134`); **~$6** nếu batch. **Lấy số cao làm trần an toàn** | `CF-3.11` · `R-08` cột trigger | `[EM tính từ OFF]` |
| **Gross margin kỳ vọng** | **50–60%**, **không phải 80%** | `CF-3.10` · `Charter §7 C6` | `[BCN]` ICONIQ 52%, Bessemer 50–60% |

### 3.2 `TBD` — chưa có chỉ tiêu

> **Không tự gán số cho bất kỳ hàng nào dưới đây.** Bịa một con số performance là lỗi nghiêm trọng hơn để trống nó — vì con số bịa sẽ được tầng 030 và tầng QA dùng làm chuẩn nghiệm thu.

| NFR chưa có chỉ tiêu | Vì sao chưa có |
|---|---|
| Latency / response time của API | Không tài liệu nào đặt mục tiêu |
| Thời gian sinh một panel end-to-end (p50/p95) | Chỉ có mốc tham chiếu self-host bị **loại** (`12–30s/ảnh`, `Analysis §9`) — không phải chỉ tiêu của kiến trúc đã chọn |
| Uptime / availability SLA | Không tài liệu nào đặt. Ràng buộc gần nhất là **định tính**: *"worker chết mà API vẫn sống"* (SRS-NFR-03) |
| Rate limit cụ thể per tenant | `MVP-Scope §3 H5` quyết **cơ chế**, không quyết con số |
| Giới hạn dung lượng / số file upload | Như trên |
| Thời hạn signed URL | `Analysis §5.7 #4` chỉ nói *"có hạn"* |
| RPO / RTO / backup retention | Không xuất hiện ở bất kỳ tài liệu nào |
| N của `in_flight_per_tenant < N` | `Analysis §6.2` viết đúng chữ `N`, không cho giá trị |
| Throughput job/giờ, queue depth alert threshold | Không có |
| **Human-reject rate sau VLM-select** | `CF-8.5` ghi rõ: ⭐ ***"chưa ai công bố con số này"*** — MVP0 phải đo. Đây là chỉ số quyết định checker có cắt được công người hay chỉ thêm chi phí |
| Regen ratio p50/p90 thực tế | `CF-8.6` — biến quyết định của cả mô hình tài chính, MVP0 phải đo |
| Cache hit rate | `CF-6.13` chỉ có `[EM]` **vài % → ~10%**, `architect` **tự khai là ước lượng** ⇒ không dùng làm chỉ tiêu (`R-17`) |
| Chi phí VLM call để score N candidate | `CF-3.5` ghi rõ đây là phần **chưa tính** ⇒ không có số |
| Tổng effort person-month | `Roadmap.md` §2 nói thẳng: trong toàn bảng CF **chỉ có ĐÚNG MỘT thời lượng tuyệt đối** (MVP0 = 1–2 tuần, `CF-8.4`); ước lượng bottom-up hiện là `TBD` |

⚠️ **Hai con số `[EM]` KHÔNG được nâng thành NFR chỉ tiêu:**

| Con số | Vì sao không phải NFR |
|---|---|
| Speaker attribution lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) — `CF-6.10` `[EM]` | Đây là **căn cứ biện minh cho FR human gate** (SRS-FR-14), không phải chỉ tiêu chất lượng phải đạt. Viết nó vào mục NFR biến một ước lượng thành một hợp đồng nghiệm thu |
| Effort **~20–25%** (editor tối thiểu, `CF-6.7`) và **50–60%** (§14 đầy đủ, `CF-6.8`) | Hai **mẫu số khác nhau** — `CF-6.8` ⛔ ghi rõ **CẤM TRỪ 6.8 CHO 6.7**. Đây là ước lượng effort, không phải NFR |

---

## 4. Cảnh báo cho writer SRS

| # | Chỗ writer sẽ trượt | Vì sao trượt | Câu **ĐÚNG** để dùng thay |
|---|---|---|---|
| **W-01** | Viết Continuity Checker là *"gắn nhãn ✓/✗ từng attribute rồi autofix"* — vì đó là mô tả trong `Request.md` §15 và là hình dung trực giác | Định nghĩa **đã bị sửa lại**. Cơ chế cũ chưa được validate và có FP profile xấu; `Glossary` ghi *"Mọi tài liệu mới phải dùng nghĩa sau"* | *"**Continuity Checker** là **QA-based selection giữa N candidate** — trả lời câu *"trong N cái này, cái nào consistent hơn"* thay vì *"panel này đúng hay sai"*."* Kèm: **cắt hẳn `[Fix automatically]`**; phiên bản hợp lệ là **"Tạo lại với ràng buộc được nhấn mạnh"**, giữ cả hai version, **người chọn** |
| **W-02** | Viết N=3 như *"generate, nếu lỗi thì generate lại"* (retry-on-failure) | Nhầm hai khái niệm này là nguồn của **sai số chi phí +50%**, và kéo theo hold reserve sai (1 thay vì 3 credit/panel) | *"**best-of-N (N=3)**: sinh **N phương án** cho mỗi panel rồi chọn cái tốt nhất. **Phân biệt tuyệt đối với retry-on-failure**: best-of-N chạy trên **mọi** panel như mặc định, không phải chỉ khi panel lỗi."* (`Glossary`) |
| **W-03** | Trích **$12,06/chapter** như chi phí thực tế trong bảng margin | `Charter §7 C7` **cấm tường minh**: *"Cấm dùng $12,06 như chi phí thực tế trong bất kỳ tính toán margin nào mà không nêu nó là sàn"* | *"**$12,06/chapter** @N=3, Gemini batch — `[EM tính từ OFF]` `CF-3.5`, **là SÀN, không phải trần**: chưa tính VLM call để score 3 candidate."* |
| **W-04** | Trích **60 ảnh/chapter** như một thông số hệ thống | Đây là **thừa số gốc của toàn bộ mô hình chi phí** và là `[EM]` — *"giả định của `researcher` run trước, **KHÔNG phải số đo**"*. Sai 2 lần thì chi phí/chapter, ngưỡng 125 ảnh, margin và giá tầng 2 sai theo **cùng bội số** | *"**60 ảnh/chapter** (15 page × 4 panel) — `[EM]` `CF-3.3`, giả định chưa được đo. Mọi con số dẫn xuất từ nó thừa hưởng nguyên vẹn sai số này."* |
| **W-05** | Trừ **50–60%** cho **20–25%** để suy ra "phần canvas bị cắt tiết kiệm 30%" | `CF-6.8` ⛔ **HAI MẪU SỐ KHÁC NHAU**: 20–25% tính trên mẫu số **SaaS** (đã gồm multi-tenancy), 50–60% tính trên mẫu số **công cụ cá nhân** (không gồm multi-tenancy/billing/auth) | *"`CF-6.7` **~20–25%** `[EM]` (mẫu số **SaaS**) và `CF-6.8` **50–60%** `[EM]` (mẫu số **công cụ cá nhân**) — ⛔ **CẤM TRỪ 6.8 CHO 6.7**. Tổng effort hợp nhất hiện là `TBD`."* |
| **W-06** | Gộp *"cắt UI cây generation"* thành *"cắt lineage"* — hai thứ ở sát nhau trong tài liệu và nghe như một | Gộp nhầm thì **mất bảo hộ bản quyền**. `MVP-Scope §6.1` liệt kê đây là một trong **ba hiểu nhầm hay gặp** | *"Cắt **UI** duyệt cây generation (`D6` = ❌ cắt hẳn), **giữ nguyên cột dữ liệu** `parent_generation_id` (`KC-1` = bắt buộc). Đây là **hai quyết định độc lập và trái chiều**."* |
| **W-07** | Viết *"BẢY điều kiện khả thi"* — vì đó là tiêu đề của `Analysis §4.1` | `Charter §4` sửa lại tường minh: bảy là số của **một lens**. *"Đếm bảy khi lập kế hoạch là bỏ sót hai điều kiện"* | *"**CHÍN** điều kiện phải thoả **ĐỒNG THỜI** (`CF-6.1`): bảy của `researcher` cộng hai từ `architect` (R8) và `senior-ai-engineer` (R9), **cùng mức bắt buộc**."* |
| **W-08** | Viết bảng `Generation` là để **reproducibility** — vì đó là mục đích tác giả `Request.md` tuyên bố | Reproducibility bit-exact **không đạt được**: nhiều API không cho set seed, và provider cập nhật weights dưới cùng một tên model (silent model drift) | *"Mục tiêu của bảng `Generation` là **AUDITABILITY + LINEAGE**, không phải reproducibility: trả lời được *"ảnh này sinh ra từ spec nào, ref nào (hash gì), tham số gì, tốn bao nhiêu, ai approve"*. **`seed` là provenance metadata, không phải replay key.**"* (`Analysis §6.4`) |
| **W-09** | Viết *"provenance phải có từ generation đầu tiên"* rồi gán nó vào **MVP0** | MVP0 **không có database** (`A5` = ❌, chủ ý: *"code của spike KHÔNG phải nền của sản phẩm"*). Nếu MVP0 bắt đầu có schema, nó đã trượt khỏi định nghĩa | *"Vì MVP0 là spike bị vứt, **"generation đầu tiên" theo nghĩa pháp lý = generation đầu tiên của sản phẩm thật, tức MVP1**. MVP0 chỉ ghi tay ra CSV/file để đủ dữ liệu đo."* (`MVP-Scope §3.1`) |
| **W-10** | Viết *"cấm dùng vector search"* — vì `E6` cắt hẳn Vector DB | Hai thứ khác nhau: **Vector DB riêng như một service** bị cắt hẳn; **`pgvector` trong cùng PostgreSQL** thì để mở | *"**Vector DB riêng** (`E6`) bị **cắt hẳn** khỏi thiết kế. **`pgvector`** (`B5`) là ❌ trong toàn horizon MVP0–MVP4, và ở Full Scope là **🟡 khi có bằng chứng cụ thể là SQL + FTS không đủ**. Ở MVP: **Story Bible *là* index của mình** + PostgreSQL full-text search."* |
| **W-11** | Ghi `TBD` cho nghĩa vụ đánh dấu máy đọc, vì phạm vi khoản 4 Điều 11 chưa rõ | Phạm vi là `TBD`, **nhưng quy tắc tạm thời thì đã được quyết** — bỏ nó thành `TBD` là mất một requirement | *"Vì phạm vi khoản 4 Điều 11 chưa rõ (⚠️ **hai nguồn mô tả khác nhau**), **phải thiết kế theo diễn giải RỘNG (mọi nội dung AI) cho tới khi luật sư chốt** (`Charter §7 C4`). Riêng câu *"SynthID có thoả nghĩa vụ không"* là `TBD` — **phải verify, không giả định**."* |
| **W-12** | Viết một requirement kiểu *"hệ thống cảnh báo khi truyện upload có thể có bản quyền của người khác"* — vì *"chủ động kiểm tra"* nghe như hành vi có trách nhiệm | `R-04`: bộ phát hiện đó **PHÁ chính miễn trừ Điều 198b**, vì điều kiện (a) của miễn trừ là **"không biết"**. `Analysis §8.3` nói thẳng *"một dev sẽ làm ngược điều này theo bản năng"* | *"⛔ **Anti-feature**: không xây bộ phát hiện nội dung có thể vi phạm bản quyền trước khi có xác nhận của luật sư. Việc **được phép** là **đọc opt-out signal do chính chủ quyền gắn vào file** (Điều 37b) — đó là **dữ kiện khách quan**, không phải tri thức suy đoán."* |
| **W-13** | Trích **~125 ảnh/tháng** như một ngưỡng đã được đo | `CF-2.5` là `[TC]` từ **vendor blog của bên bán managed inference** | *"**~125 ảnh/tháng** — `[TC]` `CF-2.5`, vendor blog bên bán managed inference (chấp nhận được vì khuyến nghị **ngược chiều lợi ích** của họ). `R-07` ghi rõ ngưỡng này **cần đo lại bằng dữ liệu thật**."* |
| **W-14** | Viết *"cắt Layout Score"* mà không nói cắt cái gì ⇒ đọc thành "bỏ luôn việc layout theo narrative importance" | `CF-9.3` cắt **cơ chế**, **GIỮ mục tiêu** | *"**Cắt cơ chế 5 số thực, GIỮ mục tiêu** (layout theo narrative importance) — thay bằng **rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter**."* |
| **W-15** | Viết requirement như design: sao chép **DDL đầy đủ** của `event` / `speech_bubble` / `generation` vào SRS vì `Analysis §5.1`, `§5.4`, `§6.4` có sẵn danh sách cột | SRS trở thành **SDD giả**, và khi 030 viết schema thật thì có **hai** nguồn sự thật cho cùng một bảng | Phát biểu **ràng buộc kiểm chứng được** rồi dừng: *"Bảng `event` phải có hai trục thời gian tách bạch, trong đó trục dùng cho **mọi** as-of state query là `story_order` kiểu `NUMERIC` sparse và editable. **DDL đầy đủ sẽ được đặc tả tại tầng 030-Specs.**"* |
| **W-16** | Viết *"tenant isolation bằng cách filter theo `tenant_id` ở tầng ứng dụng"* — nghe đủ và tiết kiệm | `Analysis §5.7 #1`: app-layer filter **sẽ có lúc bị lọt** (một query quên `WHERE tenant_id`). Với **1 dev không có code review**, RLS là *"bảo hiểm rẻ nhất tồn tại"* | *"`tenant_id NOT NULL` + là cột **đầu tiên** của mọi composite index + **Postgres RLS làm lớp phòng thủ thứ hai** — RLS biến lỗi lập trình thành **no-op** thay vì rò rỉ dữ liệu chéo tenant."* |
| **W-17** | Đặt *"độ phủ checker 40–60%"* vào mục NFR như một chỉ tiêu chất lượng phải đạt | Đây là **giới hạn phải công bố**, không phải mục tiêu. Đặt nó làm chỉ tiêu tạo ra động lực **tăng con số** thay vì **nói thật con số** | *"Hệ thống **phải hiện tường minh**: *"đã kiểm N/M panel, M−N panel không kiểm được vì có nhiều nhân vật"*. Độ phủ ước lượng **40–60%** `[EM]` `CF-6.11` là **thông tin phải công bố cho user**, không phải chỉ tiêu nghiệm thu."* |
| **W-18** | Chọn giúp vendor (auth/billing/storage), hosting, hoặc framework — vì SRS "trống một chỗ" trông như thiếu sót | Không tài liệu nào quyết. Chọn giúp ở SRS làm tầng 030 mất quyền quyết định thật và tạo một *"quyết định"* không có ai chịu trách nhiệm | *"`TBD` — quyết định đã chốt chỉ gồm **"mua auth + billing, không tự viết"** (`E4`) và **key schema object storage** (`E3`). Lựa chọn vendor/hosting/framework **sẽ được đặc tả tại tầng 030-Specs**."* |

---

## Tài liệu tham khảo

| Nguồn | Vai trò trong findings này |
|---|---|
| [Analysis-Comic-Studio-Concept.md](../../../../050-Research/Analysis-Comic-Studio-Concept.md) | Nguồn chính — §5 (bảy vấn đề phải sửa), §6 (cắt/không cắt, seam), §8.3–8.5 (pháp lý), §9–9b (kinh tế) |
| [MVP-Scope.md](../../../MVP-Scope.md) | §3 bảng MVP vs Full Scope (taxonomy module A–H, id hàng dùng làm anchor), §3.1, §4, §6 danh sách cứng KC-1…KC-7, §6.1 |
| [Charter-Comic-Studio.md](../../../Charter-Comic-Studio.md) | §4 chín yêu cầu cấp cao R1–R9, §7 ràng buộc C1–C10, §8 giả định A1–A13, §9.1 điều kiện chặn cấp dự án |
| [Risk-Register.md](../../../Risk-Register.md) | §2.1 Risk Log R-01…R-23 (đặc biệt R-01, R-02, R-04, R-06, R-13, R-14, R-15, R-16, R-17, R-22), §3 RB-01 |
| [Glossary.md](../../../../999-Resources/Glossary.md) | Định nghĩa canonical của `Story Bible`, `Comic IR`, `Visual Prompt Compiler`, `Continuity Checker`, `best-of-N (N=3)`, `field_provenance`/`change_log`, `tenant_id`, `credit ledger + hold`, `hold reaper`, `seam kinh tế vs seam kỹ thuật`, `MVP0` |
| [outline.md — run planning 2026-08-23](../../2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md) | Bảng **Canonical Facts** CF-1 → CF-9 — nguồn của mọi nhãn `[OFF]`/`[TC]`/`[EM]`/`[BCN]`/`[CHỐT]` trong file này |
| [Template-SRS.md](../../../../999-Resources/Templates/Template-SRS.md) | Khuôn có sẵn — mọi requirement ở Mục 2 đều map được vào §3 (System Features) hoặc §5 (Other Non-functional Requirements) của khuôn này. ⚠️ **Lệch so với brief**: brief run này ghi *"khuôn SRS có sẵn (**7 mục**)"*, nhưng file thực tế chỉ có **5 mục** đánh số: `1. Introduction` · `2. Overall Description` · `3. System Features` · `4. External Interface Requirements` · `5. Other Non-functional Requirements`. Không tự thêm 2 mục — **PM cần xác nhận** khuôn đích là 5 mục của file, hay một khuôn 7 mục khác mà em không tra được |
| `knowledge-base/99-Templates/Documents-Template.md` (RULE-001) | Quy tắc #3 frontmatter · #5 **markdown link, không wiki-link** · #7 tra Document Type Mapping trước khi tạo tài liệu |

> ⚠️ **Không có link nào trong file này trỏ vào `docs/030-Specs/`** — tầng đó rỗng, `Specs-MOC.md` là 0 byte, và không thuộc scope run này. Mọi chỗ cần trỏ sang design được viết dạng văn bản *"sẽ được đặc tả tại tầng 030-Specs"*.
