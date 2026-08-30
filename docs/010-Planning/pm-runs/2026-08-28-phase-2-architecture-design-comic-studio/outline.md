# Doc Plan: 2026-08-28-phase-2-architecture-design-comic-studio

> **Quy ước của file này**: chỉ **PM** được sửa. Writer báo xong trong `SUMMARY` + `FILES_TOUCHED`, PM đối chiếu ownership rồi mới tick cột *Xong*.
> **Tất cả** tài liệu sinh ra ở run này mang `status: draft` — tầng 020 đang `draft` toàn bộ và [Requirements-MOC §3](../../../020-Requirements/Requirements-MOC.md) ghi rõ chuyển `approved` là quyết định của Founder tại Go/No-Go, không phải của run này.
> **Liên kết**: standard markdown relative link `[Tên](./path.md)`. ⛔ **TUYỆT ĐỐI KHÔNG wiki-link `[[...]]`** — RULE-001 quy tắc #5.

## Nguồn sự thật dùng chung (mọi lô đều đọc)

| Nguồn | Vai trò |
|---|---|
| [findings/architect.md](./findings/architect.md) §1 (D-01…D-69) | **69 quyết định đã chốt ở Phase 1, mỗi hàng có file + số dòng.** Đây là nguồn sự thật số một của mọi ADR record-only và của SDD. Writer ⛔ **không được mở lại** các quyết định này. |
| [findings/architect.md](./findings/architect.md) §1.8 | 9 nhóm `TBD` mà Phase 1 **cố ý để mở** — Phase 2 được quyền quyết. |
| [findings/business-analyst.md](./findings/business-analyst.md) §3 | 7 ràng buộc pháp lý cứng `L-1…L-7` + anti-feature `SRS-NFR-15`. |
| [findings/business-analyst.md](./findings/business-analyst.md) §1.4 | Bước nghiệp vụ cần API đứng sau, theo từng UC. |

## Bốn ràng buộc xuyên suốt — viết MỘT LẦN, mọi file khác TRỎ TỚI

⛔ Đây là chống-trùng-lặp quan trọng nhất của run. Writer nào copy nội dung bốn mục này vào file của mình là tạo nguồn sự thật thứ hai.

| Ràng buộc | Nguồn duy nhất | Ai trỏ tới |
|---|---|---|
| `KC-4` — `generation` + `change_log` + `usage_event` commit **cùng một transaction** | `ADR-017` | `DB-Entity-Generation.md`, `DB-Entity-Provenance-And-Usage.md`, mọi `Endpoint-*` có ghi |
| Mọi query đi qua RLS với tenant context | `ADR-006` + SDD §6 | 14 file `Endpoint-*`, `DB-Entity-Tenancy.md` |
| Không đường nào bypass 2 human gate | SDD §6 | `Endpoint-Human-Gates.md`, `Endpoint-Generation.md` |
| Polling 2s là contract chung cho mọi tác vụ async | `ADR-015` | `Endpoint-Generation.md`, `Endpoint-Preview-Export.md` |

---

## 1. Bảng hạng mục

### 1.1 Architecture — `docs/030-Specs/Architecture/` (20 file)

| # | Tài liệu | Loại (RULE-001) | Lô | Writer | Xong |
|---|----------|-----------------|:--:|--------|:----:|
| 1 | `ADR-001-Backend-And-Frontend-Tech-Stack.md` | adr | L1 | architect | [x] |
| 2 | `ADR-002-Hosting-Platform-And-Region.md` | adr | L1 | architect | [x] |
| 3 | `ADR-003-Auth-And-Billing-Vendor-Selection.md` | adr | L1 | architect | [x] |
| 4 | `ADR-004-Object-Storage-Vendor-And-Signed-URL.md` | adr | L1 | architect | [x] |
| 5 | `ADR-005-Platform-Table-Schema-Placement.md` | adr | L2 | architect | [x] |
| 6 | `ADR-006-RLS-Tenant-Context-Injection.md` | adr | L2 | architect | [x] |
| 7 | `ADR-007-VLM-Provider-For-QA-Select.md` | adr | L2 | architect | [x] |
| 8 | `ADR-008-LLM-Provider-And-Usage-Boundaries.md` | adr | L2 | architect | [x] |
| 9 | `SDD-Comic-Studio.md` §1–7 | sdd | L3 | architect | [x] |
| 10 | `SDD-Comic-Studio.md` §8–9 | sdd | L4 | architect | [x] |
| 11 | `ADR-009-Modular-Monolith-Three-Schemas.md` | adr | L5 | architect | [x] |
| 12 | `ADR-010-Tenant-Isolation-With-RLS.md` | adr | L5 | architect | [x] |
| 13 | `ADR-011-Narrative-Time-Key-And-State-Reduction.md` | adr | L5 | architect | [x] |
| 14 | `ADR-012-Comic-IR-Spec-As-Primary-Data.md` | adr | L6 | architect | [x] |
| 15 | `ADR-013-Typeset-Layer-Separate-From-Art.md` | adr | L6 | architect | [x] |
| 16 | `ADR-014-Deterministic-Prompt-Compiler-And-Best-Of-N.md` | adr | L6 | architect | [x] |
| 17 | `ADR-015-Job-Queue-In-Postgres.md` | adr | L7 | architect | [x] |
| 18 | `ADR-016-Image-Provider-Adapter-And-Version-Pinning.md` | adr | L7 | architect | [x] |
| 19 | `ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md` | adr | L7 | architect | [x] |
| 20 | `ADR-018-Usage-Event-And-Rollup-Model.md` | adr | L7 | architect | [x] |

> `ADR-019-Credit-Ledger-Hold-And-Quota.md` **hoãn** — `[OoH]` MVP3. Schema vẫn chừa chỗ qua `DB-Entity-Credit-Ledger.md`. Quyết định này phụ thuộc câu gate #3.

### 1.2 Schema — `docs/030-Specs/Schema/` (13 file)

| # | Tài liệu | Entity trong file | Lô | Writer | Xong |
|---|----------|-------------------|:--:|--------|:----:|
| 21 | `DB-Entity-Narrative-Timeline.md` | `project`, `chapter`, `timeline`, `event` | L8 | architect | [x] |
| 22 | `DB-Entity-Story-Bible.md` | `bible_entity`, `entity_attribute_event`, `canonical_reference` | L8 | architect | [x] |
| 23 | `DB-Entity-Comic-IR.md` | `page`, `panel`, `panel_character`, `layout_template` | L8 | architect | [x] |
| 24 | `DB-Entity-Dialogue-And-Gate.md` | `dialogue_line`, `human_gate_state` | L8 | architect | [x] |
| 25 | `DB-Entity-Typeset-Layer.md` | `bubble` | L9 | architect | [x] |
| 26 | `DB-Entity-Generation.md` | `generation`, `prompt_compilation`, `vlm_evaluation` | L9 | architect | [x] |
| 27 | `DB-Entity-Prompt-Vocabulary.md` | `visual_vocabulary`, `action_pose_cache` | L9 | architect | [x] |
| 28 | `DB-Entity-Job-Queue.md` | `job` | L9 | architect | [x] |
| 29 | `DB-Entity-Tenancy.md` | `tenant`, `user`, `membership` | L10 | architect | [x] |
| 30 | `DB-Entity-Provenance-And-Usage.md` | `change_log`, `field_provenance`, `usage_event`, `usage_daily`, **`generation.vlm_scoring_call`** (bảng mới, `E20`) | L10 → **L27** | architect | [x] |
| 31 | `DB-Entity-Compliance-And-Takedown.md` | `ingest_check`, `text_clean_report`, `takedown_request`, `project_access_state` | L10 | architect | [x] |
| 32 | `DB-Entity-Quality-Assets.md` | `golden_dataset_item`, `eval_run`, `provider_refusal_log` | L11 | architect | [x] |
| 33 | `DB-Entity-Credit-Ledger.md` | `credit_ledger`, `credit_hold` — **`[OoH]`, mức "reserve chỗ"** | L11 | architect | [x] |
| 34a | `DB-Entity-Preview-And-Export.md` | `preview_render`, `export_artifact` — **bổ sung, E16**; ⭐ đóng luôn `SDD-HG-01.4` | L26 | architect | [x] |

### 1.3 API — `docs/030-Specs/API/` (21 file)

| # | Tài liệu | Endpoint | Lô | Writer | Xong |
|---|----------|:--------:|:--:|--------|:----:|
| 34 | `Endpoint-Project.md` | 4 | L12 | architect | [x] |
| 35 | `Endpoint-Chapter-Ingest.md` | 5 | L12 | architect | [x] |
| 36 | `Endpoint-Story-Bible.md` | 7 | L12 | architect | [x] |
| 37 | `Endpoint-Timeline-Event.md` | 4 | L12 | architect | [x] |
| 38 | `Endpoint-Panel-Script.md` | 7 | L13 | architect | [x] |
| 39 | `Endpoint-Page-Layout.md` | 7 | L13 | architect | [x] |
| 40 | `Endpoint-Human-Gates.md` | 6 | L13 | architect | [x] |
| 41 | `Endpoint-Generation.md` | 7 | L13 | architect | [x] |
| 42 | `Endpoint-Bubble-Typeset.md` | 5 | L14 | architect | [x] |
| 43 | `Endpoint-Preview-Export.md` | 5 | L14 | architect | [x] |
| 44 | `Endpoint-Tenancy.md` | 5 | L14 | architect | [x] |
| 45 | `Endpoint-Usage-And-Credit.md` | 4 | L14 | architect | [x] |
| 46 | `Endpoint-Takedown-Public.md` | 3 | L15 | architect | [x] |
| 47 | `Endpoint-Eval-Kit.md` | 3 | L15 | architect | [x] |
| 48 | `Spec-Integration-Image-Provider.md` | — | L16 | architect | [x] |
| 49 | `Spec-Integration-VLM-QA-Select.md` | — | L16 | architect | [x] |
| 50 | `Spec-Integration-LLM-Provider.md` | — | L16 | architect | [x] |
| 51 | `Spec-Integration-Auth-Provider.md` | — | L17 | architect | [x] |
| 52 | `Spec-Integration-Object-Storage.md` | — | L17 | architect | [x] |
| 53 | `Spec-Integration-Takedown-Intake.md` | — | L17 | architect | [x] |
| 54 | `Spec-Integration-Billing-Provider.md` | — **`[OoH]` reserve** | L17 | architect | [x] |

### 1.4 Security — `docs/030-Specs/Security/` (3 file)

| # | Tài liệu | Loại | Lô | Writer | Xong |
|---|----------|------|:--:|--------|:----:|
| 55 | `Spec-Security-Threat-Model.md` | security-spec | L18 | security-auditor | [x] |
| 56 | `Spec-Security-Tenant-Isolation.md` | security-spec | L18 | security-auditor | [x] |
| 57 | `Spec-Security-Legal-Compliance.md` | security-spec | L19 | security-auditor | [x] |

> Độ hạt 3 file là **đề xuất của PM**, không phải enumerate của lens. `security-auditor` được quyền đề nghị gộp/tách — báo `BLOCKED` kèm OPTIONS trước khi ghi, ⛔ không tự đổi rồi mới báo.

### 1.5 Ngoài `030-Specs` (phụ thuộc câu gate #2)

| # | Tài liệu | Việc | Lô | Writer | Xong |
|---|----------|------|:--:|--------|:----:|
| 58 | `docs/020-Requirements/SRS-Comic-Studio.md` | Thêm 7 hàng `b-1…b-7` vào §5.2 — **chỉ khi anh duyệt câu gate #2** | L0 | business-analyst | [x] |
| 59 | `docs/999-Resources/Glossary.md` | Delta 18 headword — **append-only**, ⛔ cấm sửa 54 term đã có. ✅ PM verify bằng `git diff`: **+19 / −1**, dòng xoá duy nhất là `updated:` | L20 | business-analyst | [x] |
| 59b | `docs/999-Resources/Glossary.md` | ⭐ **Bổ sung 3 headword hạ tầng của findings §5.3** — PM duyệt, xem `E22`. ✅ PM verify `git diff`: **+22 / −1**, dòng xoá duy nhất là `updated:` | L25c | business-analyst | [x] |
| 60 | **Chuẩn hoá trích dẫn `SRS L{n}` trong toàn bộ `docs/030-Specs/Architecture/`** — bỏ số dòng, giữ mã `SRS-FR-*`/`SRS-NFR-*` | Sửa 14 file | L23 | architect | [x] |
| 61 | **Chuẩn hoá header bảng traceability** trong `docs/030-Specs/Architecture/` — cột đã hết số dòng nhưng header còn ghi `(file + dòng)`; thống nhất thành `(file + mã requirement)` | Sửa header 19 file | L24 | architect | [x] |

---

## 2. Outline từng lô

### L0 — SRS amendment (điều kiện: gate #2 duyệt)
- **Độc giả đích**: chính Phase 2 — Security Spec cần `b-1…b-4` làm input; và mọi run sau đọc SRS như registry NFR duy nhất.
- **Cấu trúc**: thêm 7 hàng vào bảng §5.2, giữ nguyên khuôn 3 cột *"NFR chưa có chỉ tiêu — vì sao chưa có — requirement liên quan"*.
- **Nguồn sự thật**: [findings/business-analyst.md](./findings/business-analyst.md) §2.4 — 7 NFR im lặng: mã hoá/secret, BYOK key storage, retention nghiệp vụ, dữ liệu cá nhân, scalability, i18n, observability.
- **Tiêu chí xong**: 7 hàng mới có mã `b-1…b-7`; ⛔ **không gán số chỉ tiêu nào** (SRS cấm); `updated:` đã bump; 20 hàng `SRS-NFR-*` cũ **không đổi một ký tự**.

### L1–L2 — 8 ADR thực sự mở
- **Độc giả đích**: chính người sẽ code Phase 4, và mọi ADR/spec sau neo vào đây.
- **Cấu trúc mỗi ADR**: Context → Decision → Alternatives considered → Consequences → *"Đã quyết ở đâu"* (với phần đã CHỐT).
- **Nguồn sự thật**: [findings/architect.md](./findings/architect.md) §2.1 (bảng 8 ADR, mỗi hàng ghi rõ phần nào MỞ / phần nào CHỐT) + §1.8.
- **Ràng buộc riêng**:
  - `ADR-003`, `ADR-004`: ⛔ **không mở lại build-vs-buy** — D-12 đã chốt "mua". Chỉ chọn vendor + thiết kế seam đổi vendor.
  - `ADR-005`: đi hướng **(b) đặt bảng platform vào `public`** — PM đã phân xử: (a) thêm schema thứ 4 đụng quyết định CHỐT "3 schema" (`SRS` L249), (c) rải theo module phá `KC-4`.
  - `ADR-006`: phải trả lời **cả hai** đường — API có HTTP request, và **worker không có** nên phải suy tenant từ row `job`; nêu rõ khoảng giữa claim job và set context.
  - `ADR-007`: phải ghi ⛔ **chi phí VLM là phần CHƯA TÍNH của `CF-3.5`** — mọi COGS hiện tại là **sàn, không phải trần**.
- **Tiêu chí xong**: 8 file tồn tại, mỗi file có đủ 4 mục chuẩn ADR; phần đã CHỐT có backlink `D-xx` + file/dòng; ⛔ không ADR nào lật một quyết định trong §1.

### L3–L4 — SDD (một file, hai lô **tuần tự**)
- **Độc giả đích**: người code Phase 4 + Security Auditor (threat model chạy **trên** SDD).
- **Cấu trúc**: theo đúng 9 mục ở [findings/architect.md](./findings/architect.md) §6.4. **L3** viết §1–7, **L4** viết §8–9.
- **Nguồn sự thật**: §1 (D-01…D-69) · §6.1–6.3 (module M1–M10, 4 ranh giới, 6 luồng dữ liệu) · 8 ADR của L1–L2 (đã tồn tại khi L3 chạy).
- **Tiêu chí xong**:
  - ⭐ **Có sơ đồ kiến trúc Mermaid** — đây là **tiêu chí chuyển phase nguyên văn**, không phải tuỳ chọn.
  - §6 chứa **nguồn duy nhất** của "không bypass human gate"; §3 trỏ `ADR-005`; §6 trỏ `ADR-006`, `ADR-017`.
  - §8 liệt kê seam cho **17 story `[H-non⭐]` + 15 `[OoH]`**; §9 liệt kê `TBD` còn lại **kèm ai chịu trách nhiệm đóng**.
- ⚠️ **L4 dispatch writer MỚI**, không giao tiếp cho writer L3. Đây là một file — hai lô **không được** chạy song song.

### L5–L7 — 10 ADR record-only
- **Độc giả đích**: run tương lai — mục đích là **đóng băng** quyết định để không ai vô tình mở lại.
- **Cấu trúc**: như ADR chuẩn, **bắt buộc** có mục *"Đã quyết ở đâu"* trỏ đúng file + dòng.
- **Nguồn sự thật**: [findings/architect.md](./findings/architect.md) §2.2 — mỗi ADR đã ghi sẵn nó ghi lại `D-xx` nào.
- **Ràng buộc riêng**: `ADR-009` phải kèm cảnh báo ⛔ **`pgvector` cố ý để mở, không phải đã cắt** (`SRS` L489–493). `ADR-015` phải để `in_flight_per_tenant` là `TBD`. `ADR-017` là **nguồn duy nhất** của `KC-4`.
- **Tiêu chí xong**: 10 file; mỗi quyết định có backlink file + dòng; ⛔ **không phát minh quyết định mới** — đây là lô transcribe, không phải lô thiết kế.

### L8–L11 — 13 file DB Schema
- **Độc giả đích**: người viết migration đầu tiên ở Phase 4.
- **Cấu trúc mỗi file**: mục đích cụm → bảng cột (tên, kiểu, null, mặc định) → khoá & index (⚠️ `tenant_id` **là cột đầu mọi composite index**) → constraint & invariant → RLS policy → **ER diagram (Mermaid)** → liên kết tới ADR nguồn.
- **Nguồn sự thật**: [findings/architect.md](./findings/architect.md) §3.1–3.4 (38 entity, đã nhóm sẵn theo file) + ADR-005 (vị trí schema) + ADR-011/012/013/017 (invariant).
- **Tiêu chí xong**:
  - ⭐ **Mỗi file có ER diagram Mermaid** và schema **normalized** — tiêu chí chuyển phase nguyên văn.
  - `tenant_id` xuất hiện trên **mọi** bảng nghiệp vụ, và là cột đầu mọi composite index.
  - `DB-Entity-Comic-IR.md` viết được CHECK **≤3 nhân vật/panel** (trải `panel` + `panel_character`).
  - `KC-4` **được trỏ tới `ADR-017`**, ⛔ không copy nội dung.
  - `DB-Entity-Credit-Ledger.md` ở mức *"reserve chỗ"* — đủ để không phải retrofit, ⛔ không đặc tả đầy đủ MVP3.

### L12–L15 — 14 file API Endpoint
- **Độc giả đích**: người implement API + QA viết test case ở Phase sau.
- **Cấu trúc mỗi file**: resource → danh sách endpoint (method, path, auth, request, response, mã lỗi) → invariant của resource → UC nào tiêu thụ.
- **Nguồn sự thật**: [findings/architect.md](./findings/architect.md) §4.1 (17 resource, ~72 endpoint) + [findings/business-analyst.md](./findings/business-analyst.md) §1.4 (bước nghiệp vụ theo UC).
- **Ràng buộc riêng**:
  - ⛔ **4 ràng buộc xuyên-endpoint KHÔNG được lặp** trong 14 file — trỏ về SDD §6 / ADR-015 / ADR-017.
  - `Endpoint-Takedown-Public.md`: bề mặt **không auth, không tenant context, RLS không áp được** — phải nói rõ điều đó trong file.
  - `Endpoint-Generation.md`: xử lý HOLD credit theo **quyết định của câu gate #3**, PM sẽ dán nguyên văn vào `[TASK]`.
- **Tiêu chí xong**: ⭐ **10 UC trong phạm vi đều có endpoint đứng sau mọi bước nghiệp vụ** (track nghiệm thu #1 — xem §5).

### L16–L17 — 7 Spec-Integration
- **Cấu trúc**: mục đích → cái gì đã CHỐT → cái gì còn MỞ → interface/seam → retry & error taxonomy → chi phí.
- **Nguồn sự thật**: [findings/architect.md](./findings/architect.md) §5 — bảng 7 integration, mỗi hàng đã ghi phần CHỐT / phần `TBD`.
- **Ràng buộc riêng**: ⛔ `Spec-Integration-VLM-QA-Select.md` **tách khỏi** Image Provider là bắt buộc — gộp làm che mất chuyện chi phí VLM chưa vào COGS. ⛔ **Không integration nào gọi dịch vụ copyright/similarity detection** (`SRS-NFR-15`).
- **Tiêu chí xong**: 7 file; mỗi `TBD` ghi rõ **ai đóng và khi nào**, ⛔ không tự chọn vendor thay anh ở những chỗ Phase 1 để `TBD`.

### L18–L19 — 3 Security Spec (writer: `security-auditor`)
- **Độc giả đích**: chính Security Review Gate — đây là checkpoint chặn chuyển Phase 3.
- **Cấu trúc**: ⭐ **mở đầu bằng mục *"Câu hỏi chưa có câu trả lời"*** (BA#3) → tài sản & bề mặt tấn công → STRIDE trên các luồng của SDD §5 → biện pháp → nghĩa vụ pháp lý.
- **Nguồn sự thật**: `SDD-Comic-Studio.md` (phải tồn tại trước) · `ADR-006`, `ADR-010`, `ADR-017` · [findings/business-analyst.md](./findings/business-analyst.md) §3.1 (`L-1…L-7`), §3.2 (anti-feature), §3.4 (4 khoảng trống pháp lý mở) · `SRS` §5.2 `b-1…b-4` **nếu L0 chạy**.
- **Ràng buộc riêng**:
  - ⛔ **`SRS-NFR-15`: không thiết kế copyright/plagiarism/similarity detection** — nó **tự phá miễn trừ Điều 198b**. Đây là chỗ phản xạ nghề nghiệp sẽ làm ngược.
  - 4 khoảng trống pháp lý ghi dưới dạng **câu hỏi cho luật sư**, ⛔ không phải rủi ro đã đánh giá — `security-auditor` **không có thẩm quyền** đóng chúng.
  - Nếu L0 **không** chạy: phải ghi tường minh rằng `b-1…b-4` **chưa có requirement nguồn** và ⛔ **không được coi là đã quyết**.
- **Tiêu chí xong**: ⭐ **7 `KC-1…KC-7` đều được soi** (track nghiệm thu #2) + `L-1…L-7` đều có mục xử lý.

### L20 — Glossary delta (writer: `business-analyst`)
- **Nguồn sự thật**: [findings/business-analyst.md](./findings/business-analyst.md) §5.2 (18 headword) + §5.3 (3 headword hạ tầng).
- **Tiêu chí xong**: 18 headword mới, **append vào đúng nhóm sẵn có**; ⛔ **54 term cũ không đổi một ký tự** — đặc biệt các term mang cảnh báo canonical; `updated:` đã bump.

---

## 3. Link phải tạo (standard markdown, ⛔ không wiki-link)

| Từ | Tới | Quan hệ (RULE-001 §Linking Rules) |
|---|---|---|
| `SDD-Comic-Studio.md` | `../../020-Requirements/PRD-Comic-Studio.md` | `Implements:` — quy tắc #4 |
| Mọi `ADR-*.md` | `./SDD-Comic-Studio.md` | `Related to:` — quy tắc #5 |
| Mọi `DB-Entity-*.md` | ADR nguồn của invariant | `Decided in:` |
| Mọi `Endpoint-*.md` | UC nó phục vụ | `Serves:` |
| `Spec-Security-*.md` | `SDD` + `ADR-006/010/017` | `Threat model of:` |
| `Specs-MOC.md` | cả 57 tài liệu | điều hướng — **PM viết** |

## 4. MOC cần cập nhật — ⛔ PM ĐỘC QUYỀN, không cấp cho writer nào

| MOC | Mục thêm/sửa |
|---|---|
| `docs/030-Specs/Specs-MOC.md` | **Viết mới hoàn toàn** — hiện 0 byte, không có cả frontmatter. Theo pattern `Requirements-MOC.md` (`id: MOC-030`, `type: moc`, `status: live`), điều hướng 4 nhóm Architecture / Schema / API / Security. |
| `docs/000-Index.md` §030 (L94–97) | Gỡ cảnh báo *"MOC hiện là file rỗng 0 byte"* và *"(chưa có tài liệu)"*; liệt kê SDD như điểm vào của tầng. |
| `docs/000-Index.md` §Nợ kỹ thuật (L176) | Nợ #1 hiện gộp `Specs-MOC` + `Design-MOC`. **Tách ra**: `Specs-MOC` đã đóng, `Design-MOC` **vẫn còn 0 byte**. ⛔ Không xoá cả hàng. |

## 5. Ripple — tài liệu đang trích dẫn phạm vi này và sẽ lệch sau khi sửa

| File | Sẽ lệch ở đâu | Xử lý |
|---|---|---|
| `docs/020-Requirements/Requirements-MOC.md` L12 | Ghi *"tầng [030-Specs], hiện chưa khởi tạo"* — sai sau run này | PM sửa ở close-step |
| `docs/020-Requirements/Requirements-MOC.md` L77 (quy ước #4) | *"Không link tới `030-Specs/` — tầng đó rỗng"* — quy ước này **hết hiệu lực** | PM sửa ở close-step, ghi rõ lý do đổi |
| `SRS-Comic-Studio.md` L71, L549 | Tự khai *"không có link nào trỏ vào `docs/030-Specs/`"* | **Giữ nguyên** — G12: link một chiều `030` → `020`. ⛔ Không chạm SRS trừ khi gate #2 duyệt (và khi đó chỉ sửa §5.2) |

> ⚠️ **Bài học bắt buộc áp dụng ở close-step**: `Requirements-MOC.md` ghi lại rằng ở run `2026-08-24`, PM ghi đè cả file MOC và **xoá im lặng** mục *"Quy Trình Làm Việc (BA Workflow)"*; verify bắt được và phải khôi phục. ⇒ Close-step run này **sửa có phẫu thuật bằng `Edit`**, ⛔ tuyệt đối không `Write` đè cả file MOC.

## 6. Hai track nghiệm thu (BA#2 — PM nhận, đưa vào `verdict.md`)

| Track | Kiểm cái gì | Vì sao tách |
|---|---|---|
| **#1 API coverage** | 10 UC trong phạm vi đều có endpoint đứng sau mọi bước nghiệp vụ | Đây là tiêu chí chuyển phase nguyên văn |
| **#2 DB/Security coverage** | `KC-1…KC-7` đều có chỗ trong schema và được soi trong Security Spec | ⚠️ Dùng một mình ma trận UC sẽ **làm rơi entity của UC-10** khỏi DB Schema — mà `KC-1` và `KC-7` ⛔ **không backfill được** |
