---
id: MVPSCOPE-001
type: mvp-scope
status: draft
created: 2026-08-23
---

# MVP Scope — comic-studio

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts của run planning này — nhãn đi cùng số như một cặp không tách rời):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của founder tại gate.
>
> Mọi con số mang nhãn `[EM]` trong tài liệu này **là khoảng trống dữ liệu được thừa nhận**, không phải sự thật đã đo. Nếu anh copy một con số sang tài liệu khác, **copy cả nhãn**.

## Mục lục

1. [Mục đích & cách đọc tài liệu](#1-mục-đích--cách-đọc-tài-liệu)
2. [Nguyên tắc cắt scope](#2-nguyên-tắc-cắt-scope)
3. [Bảng MVP vs Full Scope](#3-bảng-mvp-vs-full-scope)
4. [Cắt gì và vì sao](#4-cắt-gì-và-vì-sao)
5. [Editor tối thiểu — ranh giới chi tiết](#5-editor-tối-thiểu--ranh-giới-chi-tiết)
6. [Không được cắt — danh sách cứng](#6-không-được-cắt--danh-sách-cứng)
7. [Go/No-Go Decision](#7-gono-go-decision)
8. [Điều kiện thoát (kill criteria)](#8-điều-kiện-thoát-kill-criteria)
9. [Tài liệu tham khảo](#9-tài-liệu-tham-khảo)

---

## 1. Mục đích & cách đọc tài liệu

Tài liệu này trả lời **đúng một câu hỏi**: *cái gì vào MVP, cái gì không.*

Nó **không** trả lời *"khi nào"* — đó là việc của [Roadmap.md](./Roadmap.md). Nó **không** trả lời *"vì sao dự án này đáng làm"* — đó là việc của [Charter-Comic-Studio.md](./Charter-Comic-Studio.md).

### 1.1 Ranh giới ba tài liệu

| Tài liệu | Trả lời câu hỏi | Không trả lời |
|---|---|---|
| [Charter-Comic-Studio.md](./Charter-Comic-Studio.md) | Dự án này là gì, cho ai, biện minh bằng gì, ràng buộc cấp dự án nào | Ranh giới MVP, lịch trình |
| **MVP-Scope.md** (tài liệu này) | **Cái gì vào MVP0–MVP4, cái gì bị cắt/hoãn, và điều kiện Go/No-Go** | Ngày tháng, thứ tự thời gian, phân bổ effort theo lịch |
| [Roadmap.md](./Roadmap.md) | Khi nào, theo thứ tự nào, exit criteria từng mốc | Lý do cắt một hạng mục |

### 1.2 Bối cảnh không được quên khi đọc

| Sự thật nền | Giá trị | Nhãn |
|---|---|---|
| Bản chất sản phẩm | **SaaS thương mại multi-tenant** — nền tảng cho **người khác tự upload truyện của họ** | `[CHỐT]` CF-1.1 |
| Quy mô đội | **1 người + AI assist**. Không funding, không ngân sách marketing | `[CHỐT]` CF-1.2 |
| Trạng thái code | **Chưa có dòng nào** | `[OFF]` CF-1.3 |
| Phân khúc | **Tác giả truyện chữ KHÔNG biết vẽ** — *không* nhắm hoạ sĩ | `[CHỐT]` CF-1.5 |
| Verdict khả thi | **KHẢ THI CÓ ĐIỀU KIỆN — CHÍN điều kiện phải thoả ĐỒNG THỜI** | CF-6.1 |

> Đọc mọi mục bên dưới với ràng buộc **1 dev** trong đầu. Phần lớn quyết định cắt ở đây **không đúng** với một đội 5 người — chúng đúng với đội một người.

### 1.3 Thứ tự milestone (cố định, không mở lại)

**MVP0 → MVP1 → MVP2 → MVP3 → MVP4** `[CHỐT]` CF-8.3.

| Mốc | Nội dung lõi |
|---|---|
| **MVP0** | Vertical slice — 1 chapter, Story Bible + panel script **viết tay**, code đúng một việc: generate panel với reference + N candidate + VLM select. 1–2 tuần · ~$12 (CF-8.4) |
| **MVP1** | Story Intelligence + `tenant_id` từ ngày đầu + HITL gate & eval kit + log preference data + opt-out Điều 37b (CF-8.7) |
| **MVP2** | Comic Director — rubric `beat_type`, cứng hoá ≤3 nhân vật/panel, `text_safe_zone`, hai human gate bắt buộc (CF-8.8) |
| **MVP3** | Visual Generation — **scale-up, không phải khám phá**, vì rủi ro đã được MVP0 kiểm trước (CF-8.9) |
| **MVP4** | Production — **nâng ưu tiên export lên sớm**; Continuity Checker chuyển sang N-candidate selection (CF-8.10) |

> [!WARNING]
> **Bẫy đánh số.** `findings/architect.md` §7.2 của run trước có một sơ đồ **đánh số lại** các milestone (ở đó "MVP1" nghĩa là Visual Generation Loop). Bảng trên đây theo **CF-8.3/8.7–8.10 là canon**: MVP1 = Story Intelligence, MVP3 = Visual Generation. Nếu anh đọc findings gốc, đừng để hai hệ đánh số lẫn vào nhau.

---

## 2. Nguyên tắc cắt scope

Bốn nguyên tắc dưới đây rút từ CF-9 (ba thứ nên cắt + một thứ không được cắt) và CF-8.12. Mọi tranh cãi scope về sau **giải bằng bốn nguyên tắc này**, không giải bằng cảm tính.

### NT-1 — Sinh một ảnh trong tuần đầu tiên

> *"Sinh một ảnh trong tuần đầu tiên, dù bằng tay, dù chỉ 8 panel. Không phải để có sản phẩm, mà để biết tiền đề còn đứng."* — CF-8.12

Hệ quả cắt scope: bất kỳ hạng mục nào **trì hoãn** thời điểm sinh ra tấm ảnh đầu tiên đều bị đẩy ra sau MVP0, **kể cả khi nó là nền móng kiến trúc đúng**. Đây là lý do MVP0 tồn tại và là lý do Story Bible ở MVP0 được viết tay.

### NT-2 — Nghĩa vụ pháp lý đặt lên tầng DỮ LIỆU, không đặt lên tầng UI

Đây là nguyên tắc sinh ra kết luận cắt canvas (CF-9.1). Yêu cầu *"iterative, interactive process"* của bảo hộ bản quyền là yêu cầu về **quyết định sáng tạo của con người có được ghi nhận hay không** — không phải yêu cầu về công nghệ render UI. Một form editor có ghi vết đầy đủ (`change_log`, `field_provenance`, `generation.origin`) thoả nghĩa vụ đó y hệt một canvas editor.

Hệ quả: **UI được tự do chọn cái rẻ; dữ liệu provenance thì không được cắt một dòng nào.**

### NT-3 — Cắt cái đắt-mà-không-kiểm-chứng-được; giữ cái rẻ-mà-không-backfill-được

Hai vế đối xứng:

- **Cắt**: hạng mục không có prior art, không kiểm chứng được đúng/sai, và có phương án thay thế rẻ hơn nhiều lần → Layout Score số thực (CF-9.3).
- **Giữ**: hạng mục **một cột, gần như miễn phí, nhưng thêm sau thì mất dữ liệu quá khứ vĩnh viễn** → `parent_generation_id`, `tenant_id`, `usage_event` (CF-7.3, CF-6.12).

Chi phí của một cột nullable là gần bằng 0. Chi phí của việc không có nó là **không đảo ngược được**. Bất đối xứng này quyết định.

### NT-4 — Cắt để dồn ngân sách sang khối bị bỏ trắng, không cắt để đi nhanh hơn

Phần effort tiết kiệm được từ CF-9.1 và CF-9.2 **không phải lãi** — nó là ngân sách cho khối multi-tenancy **15–25%** `[EM]` (CF-6.9) mà `Request.md` gốc không nhắc một dòng. Cắt mà không hiểu điều này sẽ dẫn tới ảo tưởng "còn dư thời gian".

---

## 3. Bảng MVP vs Full Scope

**Ký hiệu**: ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ **cắt hẳn, không có trong Full Scope**

> [!NOTE]
> Cột **Full Scope** = trạng thái đích của sản phẩm khi trưởng thành, **không** phải trạng thái trong horizon 6 tháng. Ô `❌` ở cột Full Scope nghĩa là hạng mục đó bị **loại khỏi thiết kế**, không phải bị hoãn.

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **A. Pipeline sinh ảnh** ||||||||
| A1 | Generate panel: reference + N candidate + VLM select | ✅ | ⛔ | ⛔ | ✅ | ✅ | ✅ | CF-8.4 (code MVP0 làm **đúng một việc** này) · CF-3.1 N=3 `[OFF]` |
| A2 | Typeset layer + bubble overlay (composite ra trang thật có thoại) | 🟡 thô | 🟡 | 🟡 | ✅ | ✅ | ✅ | CF-8.11c — *"nổ ngay ở panel có thoại đầu tiên, tức trong MVP0"* |
| A3 | Visual Prompt Compiler **deterministic** (lookup + policy, không LLM ở runtime) | 🟡 script | 🟡 | 🟡 | ✅ | ✅ | ✅ | Analysis §5.5 — compiler deterministic là **điều kiện cần** để bảng `Generation` có nghĩa |
| A4 | Adapter đa provider (Gemini 3 Pro Image, FLUX.2) | 🟡 1 adapter | ⛔ | ⛔ | ✅ | ✅ | ✅ | Analysis §6.2 seam #4 · CF-3.4 `[OFF]` |
| A5 | Job queue trong Postgres (`FOR UPDATE SKIP LOCKED`, transactional enqueue) | ❌ không cần | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §6.2 — MVP0 là script + file phẳng, không DB |
| A6 | Fairness per tenant trong câu CLAIM job | ⛔ | ⛔ | ⛔ | ✅ | ✅ | ✅ | Analysis §6.2 seam kinh tế — nhồi vào sau là sửa đúng câu SQL nóng nhất |
| A7 | **Whole-page render granularity** (đường lui của G2) | ⛔ | ⛔ | ⛔ | 🟡 tuỳ chọn | ✅ | ✅ | Analysis §9b.3 — spec tách khỏi ảnh nên **đổi granularity không đổi data model** |
| **B. Story Intelligence** ||||||||
| B1 | Chapter parse + **text clean** (regex/heuristic, deterministic) | ❌ viết tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 — *"text clean là bước ĐẦU TIÊN"* |
| B2 | Story Bible extraction tự động (character, location, costume) | ❌ viết tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.4 (*"không code extraction"*) · CF-8.7 |
| B3 | Timeline state resolver `state_at(N) = reduce(events)` | ❌ viết tay | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.5 — code sở hữu state, LLM chỉ phát event |
| B4 | Khoá thời gian đúng (thay `(chapter, scene)`) | — | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.1 — sai âm thầm ở flashback; **phải sửa trước dòng code đầu tiên** |
| B5 | `pgvector` / vector search | ❌ | ❌ | ❌ | ⛔ | ⛔ | 🟡 khi có bằng chứng SQL+FTS không đủ | CF-9.2 · Analysis §6.2 — *"Story Bible **là** index của mình"* |
| **C. Comic Director & Layout** ||||||||
| C1 | Comic IR / Panel Specification (spec là dữ liệu chính) | 🟡 YAML tay | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §4.2 ✅ đã giải được — rủi ro thấp nhất bảng |
| C2 | Director tự động scene → page → panel | ❌ viết tay | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 |
| C3 | Layout: **rubric `beat_type` + emphasis quota** (rời rạc, bảng tra) | ❌ | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 · CF-9.3 |
| C4 | **Layout Score 5 số thực** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ **cắt hẳn** | CF-9.3 — không prior art; *"chưa ai làm vì không đáng"* |
| C5 | Cứng hoá **≤3 nhân vật/panel** trong schema Comic IR | 🟡 kỷ luật tay | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-6.5 `[OFF]` ID-Sim 42.33 (2) → 27.21 (3) → 2.67 (4) → 0.52 (5) |
| C6 | `text_safe_zone` trong panel spec | ⛔ | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 |
| C7 | **Hai human gate bắt buộc**: speaker attribution + dialogue condensation | ❌ | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 — *không phải tuỳ chọn, không dồn sang MVP4* · CF-6.10 lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) `[EM]` |
| **D. Editor & UI** ||||||||
| D1 | Editor tối thiểu — 5 thành phần (chi tiết [mục 5](#5-editor-tối-thiểu--ranh-giới-chi-tiết)) | ❌ | 🟡 #5 Story Bible editor | 🟡 +#3 template layout, +#4 preview server-side, **bắt đầu** #2 bubble/text | ✅ đủ 5 (hoàn tất #2, thêm #1 panel card) | ✅ | ✅ | CF-6.7 **~20–25%** `[EM]`, **mẫu số SaaS** |
| D2 | Infinite canvas, zoom/pan cả chapter, hình học panel tự do | ❌ | ❌ | ❌ | ⛔ | ⛔ | 🟡 nếu có bằng chứng khách cần | CF-9.1 — chi phí lớn nhất, giá trị tăng thêm nhỏ nhất |
| D3 | Undo/redo xuyên toàn bộ state phân tán | ❌ | ❌ | ❌ | ⛔ | ⛔ | ⛔ | CF-9.1 — chỉ undo **cục bộ**; không undo qua generation (đã tiêu tiền thật) |
| D4 | Realtime collaboration | ❌ | ❌ | ❌ | ❌ | ⛔ | 🟡 khi bán gói team | CF-9.1 — 1 user = 1 tenant ở bản đầu |
| D5 | Inpainting brush / drawing tools | ❌ | ❌ | ❌ | ❌ | ⛔ | 🟡 kèm `generation.origin='ai_edited'` | CF-9.1 |
| D6 | UI duyệt **cây** generation (tree view / diff / branch-merge) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ **cắt hẳn** | Analysis §6.3–6.4 — flat list `created_at` + `approved_generation_id` đủ 95% giá trị. ⚠️ **Cắt UI, KHÔNG cắt cột dữ liệu** |
| D7 | Expression sheet đầy đủ mỗi nhân vật | ❌ | ⛔ | ⛔ | 🟡 3 góc + 3 biểu cảm | 🟡 | ✅ | Analysis §6.3 — ứng viên cắt sâu cùng loại |
| **E. Multi-tenancy & hạ tầng** ||||||||
| E1 | `tenant_id NOT NULL` mọi bảng + cột **đầu tiên** mọi composite index + Postgres RLS | ❌ không DB | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 *"`tenant_id` từ ngày đầu"* · CF-6.9 **15–25%** `[EM]` |
| E2 | `tenant` / `user` / `membership` là ba entity riêng (kể cả khi 1:1) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 quyết định #2 |
| E3 | Object storage `tenant/{tenant_id}/{sha256}`, **không dedup chéo tenant** | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 #4 — dedup chéo mâu thuẫn trực tiếp với lập luận bản quyền |
| E4 | Mua auth + billing (không tự viết) | ❌ | ✅ auth | ✅ | ✅ +billing | ✅ | ✅ | Analysis §5.7 — *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"* |
| E5 | Modular monolith: 1 process, 1 PostgreSQL, 3 schema (`story`/`comic`/`generation`) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-9.2 — lý do **MẠNH LÊN** dưới SaaS |
| E6 | **Microservices (3 service) + 2 PostgreSQL + Vector DB riêng + Job Queue riêng** | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ **cắt hẳn** | CF-9.2 — hai DB = mất transaction; RLS không bảo vệ được join phía ứng dụng |
| E7 | Worker là process triển khai riêng, **cùng codebase** (2 entrypoint) | ❌ | ⛔ | ⛔ | ✅ | ✅ | ✅ | Analysis §6.2 seam kinh tế — worker chết mà API vẫn sống ⇒ không churn |
| E8 | SSO/SAML, custom domain, white-label, multi-region | ❌ | ❌ | ❌ | ❌ | ❌ | ⛔ | Analysis §5.7 *"Hoãn được"* |
| **F. Kinh tế & credit** ||||||||
| F1 | `usage_event` append-only + rollup `usage_daily` (regen ratio là metric first-class) | 🟡 log tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.6 · `findings/architect.md` B4.3 — *"đo muộn nghĩa là định giá trong bóng tối hàng tháng"* |
| F2 | `cost_usd` + `model_id` + `model_version` + `attempt_no` trên mọi `generation` | 🟡 CSV | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 #3 — không backfill được |
| F3 | Credit ledger append-only + **HOLD trước khi enqueue** + `CHECK (available >= 0)` + hold reaper | ❌ | ⛔ | ⛔ | ✅ | ✅ | ✅ | CF-6.12 — **hold reserve 3 credit/panel** (vì N=3) |
| F4 | Hard quota **cưỡng chế trước khi enqueue** (không đếm sau) | ❌ | ⛔ | ⛔ | ✅ | ✅ | ✅ | CF-8.11b — *trước bản trả phí đầu tiên có image gen* |
| F5 | BYOK — **tuỳ chọn MỞ KHOÁ**, không phải điều kiện dùng sản phẩm | ❌ | ❌ | ⛔ | ⛔ | ✅ | ✅ | CF-2.4 `[CHỐT]` · CF-2.5 ngưỡng **~125 ảnh/tháng** `[TC]` |
| F6 | Tầng 1 bán được: Story Bible + Comic IR + layout + versioning + export, **KHÔNG image gen** | ❌ | ⛔ | 🟡 khả dĩ | ✅ | ✅ | ✅ | CF-2.2 `[CHỐT]` — margin ~90%, không cần API key |
| **G. Pháp lý & compliance** ||||||||
| GP-1 | `parent_generation_id` + `relation_kind` + `change_log` + `field_provenance` + `generation.origin` | 🟡 ghi tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-7.3 `[OFF]` — **hồ sơ pháp lý bắt buộc, không backfill được** |
| GP-2 | Kiểm **opt-out signal Điều 37b** ngay trong bước ingest | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-7.5 `[OFF]` — chi phí ~0, phải nằm ở nơi file user lần đầu vào hệ thống |
| GP-3 | Checklist safe harbour **Điều 198b**: takedown, đăng ký đầu mối Bộ VHTTDL, SLA **72 giờ** | ❌ | 🟡 | ✅ | ✅ | ✅ | ✅ | CF-7.6 `[OFF]` · CF-8.11a — **trước khi mở cho người ngoài upload** |
| GP-4 | AI disclosure (Luật TTNT 2025) | ❌ | 🟡 | 🟡 | ✅ | ✅ | ✅ | CF-7.7 `[OFF]` — deadline tuân thủ **~01/03/2027**; ⚠️ hai nguồn mô tả phạm vi **khác nhau** |
| GP-5 | ToS + user warrant + `ON DELETE CASCADE` + đường hard-delete tenant đã kiểm thử | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 #5 — takedown **sẽ** đến |
| **H. Chất lượng & vận hành** ||||||||
| H1 | HITL gate + eval kit | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 — **ngay tại MVP1, không dồn MVP4** |
| H2 | Log preference data (moat thật) | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.7 · Analysis §12 — *"một khoản đầu tư, trả hai lần"* |
| H3 | Continuity Checker dạng **N-candidate selection** (không phải flag+autofix) | 🟡 VLM select | ⛔ | ⛔ | 🟡 | ✅ | ✅ | CF-8.10 · CF-6.11 độ phủ **40–60% số panel** `[EM]` — **phải nói rõ với user** |
| H4 | Export PDF / CBZ / webtoon | ❌ | ⛔ | 🟡 preview server-side | ✅ | ✅ | ✅ | CF-8.10 — *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"* ⇒ kéo lên sớm |
| H5 | Abuse controls tối thiểu (rate limit/tenant, giới hạn upload, log provider từ chối) | ❌ | 🟡 | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 — tín hiệu abuse sớm gần như miễn phí |
| H6 | Golden dataset regression (15–20 panel có spec + ref + ảnh + đánh giá) | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | `findings/architect.md` §7.3 điểm 4 — tài sản dùng suốt vòng đời |

### 3.1 Ba ô đáng chú ý nhất trong bảng

| Ô | Vì sao đáng chú ý |
|---|---|
| **A5 = ❌ ở MVP0** | MVP0 **không có database**. Đây là chủ ý: *"code của spike KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu"* (`findings/architect.md` §7.3 điểm 5). Nếu MVP0 bắt đầu có schema, nó đã trượt khỏi định nghĩa |
| **GP-1 = 🟡 ở MVP0, ✅ ở MVP1** | CF-7.3 nói *"không lưu từ generation đầu tiên thì vĩnh viễn không có"*. Vì MVP0 là spike bị vứt, **"generation đầu tiên" có nghĩa pháp lý = generation đầu tiên của sản phẩm thật, tức MVP1**. MVP0 chỉ cần ghi tay ra CSV/file để đủ dữ liệu đo `[EM]` diễn giải của em, không có trong CF |
| **D6 = ❌ cắt hẳn, nhưng GP-1 = ✅** | Đây chính là NT-2 vận hành: **cắt UI cây generation, giữ nguyên cột `parent_generation_id`**. Hai thứ này rất dễ bị gộp làm một khi cắt scope — và gộp nhầm thì mất bảo hộ bản quyền |

---

## 4. Cắt gì và vì sao

### 4.1 Canvas editor §14 — **CẮT MỘT PHẦN** (CF-9.1)

**Quyết định**: giữ **editor tối thiểu ~20–25%** `[EM]` (mẫu số SaaS); **hoãn** infinite canvas, undo xuyên state, realtime collab, inpainting.

**Lý do**: nghĩa vụ pháp lý đặt lên **tầng DỮ LIỆU (audit event), không đặt lên tầng CANVAS** (CF-9.1). Cả ba tương tác mà §14 `Request.md` nêu ra — `Regenerate`, `Change camera → Low angle`, `Replace character costume` — đều là *"sửa một field của spec rồi generate lại"*. Không cái nào cần canvas.

**Lý do phụ, nhưng là lý do quyết định với 1 dev**: canvas editor là software engineering thuần, khó thật, và **không AI nào viết hộ được phần khó** (state machine, perf với hàng trăm ảnh, undo trên side-effect không hoàn lại, race khi user sửa spec trong lúc generation đang bay). Một dev đơn lẻ chọn build canvas editor trước là **gần như chắc chắn không bao giờ tới được phần AI**.

**Đường nâng cấp không mất mát**: giữ layout dưới dạng **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` ngay từ MVP; template chỉ là các preset ghi vào **cùng** schema đó. Khi (nếu) lên canvas thật bằng thư viện có sẵn thì **không phải migrate dữ liệu**, chỉ thay lớp tương tác. **Không viết renderer từ đầu.**

### 4.2 Microservices + Vector DB §12 — **CẮT** (CF-9.2)

**Quyết định**: modular monolith. 1 process · 1 PostgreSQL / 3 schema · queue trong Postgres · Object Storage tách khỏi DB · polling 2s thay WebSocket. Vector DB **bỏ hẳn khỏi MVP**.

**Lý do MẠNH LÊN dưới SaaS, không yếu đi** — ba lý do mới:

| # | Lý do | Vì sao nó chặn việc tách DB |
|---|---|---|
| 1 | **RLS không bảo vệ được join phía ứng dụng** | State resolution là truy vấn **xuyên** Story ↔ Comic. Hai DB ⇒ join phía ứng dụng ⇒ lớp phòng thủ thứ hai biến mất **đúng ở đường dẫn dữ liệu nóng nhất** |
| 2 | **Nghĩa vụ audit đòi một transaction boundary** | `INSERT generation` + `INSERT change_log` + `INSERT usage_event` phải commit cùng nhau. *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* |
| 3 | **Ngân sách effort đã bị multi-tenancy ăn mất 15–25%** `[EM]` | Effort đó phải lấy từ đâu đó; lấy từ hạ tầng phân tán là lựa chọn hiển nhiên đúng (NT-4) |

**Năm seam ĐÚNG chỗ vẫn giữ** (miễn phí trong monolith): async job interface `enqueue(spec) → job_id → poll` · Object Storage content-addressed · module interface `story`/`comic`/`generation` với luật `comic` gọi `story` **chỉ qua** `resolveState()` và `getBible()` (enforce bằng lint rule) · adapter per image provider · Visual Prompt Compiler là library thuần.

### 4.3 Layout Score số thực — **CẮT** (CF-9.3)

**Quyết định**: cắt **cơ chế 5 số thực**, **giữ mục tiêu** (layout theo narrative importance) → thay bằng rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter.

**Lý do**: đây là hạng mục mà lens research xếp ⚪ *không tìm được prior art*, và lens AI/ML phân định là **"chưa ai làm vì không đáng"**. Một hạng mục **không có prior art + không kiểm chứng được đúng/sai + có phương án thay thế rẻ hơn cả chục lần với chất lượng cao hơn ở MVP** — đó là định nghĩa của thứ nên cắt sớm (NT-3 vế 1).

### 4.4 ⛔ `parent_generation` — **KHÔNG CẮT.** Đây là một sự TỰ THU HỒI

> [!IMPORTANT]
> **Mục này không phải một khuyến nghị. Nó là một dấu vết quyết định.**
> PM của run trước đã **tự thu hồi công khai khuyến nghị cắt của chính mình**. Mục này được giữ nguyên hình dạng đó — nếu viết lại thành "giữ `parent_generation`" thì mất đúng phần có giá trị nhất: *lý do vì sao một kết luận có vẻ hợp lý lại sai*.

**Khuyến nghị ban đầu — và nó SAI.** Trong `findings/product-manager-pm-lens.md` mục 5 của run trước, PM viết về `Generation` lineage: *"Giữ **tối giản** — log prompt/model/seed/refs. **Bỏ cây `parent_generation` ở MVP**."* Lập luận lúc đó thuần tuý là scope: với 1 dev, cây lineage nghe như hạng mục hoãn được.

**Vì sao nó sai.** Lens có web access tra ra **Nghị định 134/2026/NĐ-CP** — ban hành **06/04/2026**, hiệu lực **09/04/2026**, sửa đổi NĐ 17/2023 `[OFF]` (CF-7.1). Theo **Điều 5a**, tác phẩm AI-assisted chỉ được bảo hộ nếu con người có *"substantial and decisive intellectual contribution"*; **tác phẩm do AI tạo hoàn toàn KHÔNG được bảo hộ**. Kèm theo là **nghĩa vụ lưu giữ prompts, inputs, intermediate drafts** (CF-7.2 `[OFF]`).

⇒ Bảng `Generation` — vốn được thiết kế cho **reproducibility/debug** — **chính là hồ sơ pháp lý bắt buộc** để chứng minh human contribution ở Việt Nam. Một feature engineering hoá ra là **compliance artifact**. Khuyến nghị cắt **bị thu hồi**.

**Bài học quy trình, đáng ghi lại hơn cả kết luận**: nghị định này hiệu lực **sau knowledge cutoff** của model. Không có một lens có web access, tài liệu planning sẽ khuyên cắt **đúng thứ mà luật bắt phải giữ**. Đây là lý do mọi run về sau phải giữ ít nhất một lens tra được nguồn ngoài.

**Và nó không chỉ "giữ nguyên" — nó MẠNH LÊN dưới SaaS**: với multi-tenant, audit trail còn là bằng chứng phục vụ **khách hàng của anh** chứng minh quyền của họ, không chỉ của anh.

**Vẫn được cắt**: **UI duyệt cây** (D6 ở bảng mục 3). Nghĩa vụ nằm ở **dữ liệu**, không ở giao diện.

**Điều chỉnh cách diễn đạt, không phải cách làm**: với closed API, mục tiêu đúng của `Generation` **không phải reproducibility mà là AUDITABILITY + LINEAGE**. Reproducibility bit-exact không đạt được (nhiều API không cho set seed; provider cập nhật weights dưới cùng một tên model — silent model drift). `seed` là **provenance metadata**, không phải replay key.

---

## 5. Editor tối thiểu — ranh giới chi tiết

### 5.1 ⚠️ Cảnh báo mẫu số — đọc trước khi nhìn bất kỳ con số % nào

> [!WARNING]
> **CF-6.7 và CF-6.8 là HAI MẪU SỐ KHÁC NHAU. CẤM TRỪ CHO NHAU.**
>
> | Con số | Giá trị | Mẫu số | Nhãn |
> |---|---|---|---|
> | **CF-6.7** — Editor tối thiểu | **~20–25%** | **SaaS** — *đã bao gồm* khối multi-tenancy, billing, auth, moderation | `[EM]` |
> | **CF-6.8** — §14 đầy đủ | **50–60%** | **Công cụ cá nhân** — *không* gồm multi-tenancy, billing, auth, moderation | `[EM]` |
>
> Phép tính `50–60% − 20–25% = 25–40% tiết kiệm` là **SAI về mặt số học**, vì hai tử số đứng trên hai mẫu số khác nhau. Bất kỳ tài liệu, ticket, hay ước lượng nào về sau thực hiện phép trừ đó đều đang tạo ra một con số không tồn tại.
>
> **Điều duy nhất được phép kết luận** — và đây là câu chốt của lens kiến trúc run trước, giữ nguyên định tính: *"vẫn tiết kiệm được khoảng một nửa effort của hạng mục đắt nhất"*. Phần tiết kiệm đó chính là ngân sách để làm khối multi-tenancy **15–25%** `[EM]` (CF-6.9), thứ vốn không có trong kế hoạch cũ (NT-4).
>
> **Cả hai con số đều mang nhãn `[EM]`** — chúng là ước lượng của lens kiến trúc, **không phải số đo**. Đừng lập kế hoạch như thể chúng là dữ liệu.

### 5.2 Năm thành phần BẮT BUỘC (~20–25% `[EM]`, mẫu số SaaS)

| # | Thành phần | Vì sao bắt buộc | % effort (mẫu số SaaS) `[EM]` | Mốc |
|---|---|---|---|---|
| 1 | **Panel card**: form spec + ảnh preview + `Regenerate` + **variant picker** | Chính là vòng lặp *iterative*. Variant picker là hành động sáng tạo **rẻ nhất mà giá trị pháp lý cao nhất** — chọn = authorship, ghi được vào `change_log` | **5–7%** | MVP3 |
| 2 | **Bubble/text overlay editor trong phạm vi MỘT panel** (kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ) | Ba lý do **độc lập**: (a) thoại do người viết là phần **được bảo hộ**; (b) bubble che mặt là lỗi không thể tự động tránh; (c) không sửa được thoại thì mọi lần sửa chữ thành một lần regenerate ảnh — **đốt tiền**. Đây là *"canvas bị giới hạn trong một khung"*, **không** phải scene graph tự do | **5–8%** | MVP2–MVP3 |
| 3 | **Page**: chọn **template layout**, đổi chỗ / swap panel giữa các ô, reorder | Sắp đặt panel là quyết định sáng tạo của con người (*selection & arrangement*). Chỉ cần **rời rạc**, không cần hình học liên tục | **3–4%** | MVP2 |
| 4 | **Preview trang + chapter render server-side** (composite PNG/PDF), read-only | Khách phải **thấy thành phẩm mới trả tiền**. Rẻ vì tái dùng compositor của export (H4) | **3–5%** | MVP2 |
| 5 | **Story Bible editor** (form: character, costume, location, state theo event) | Đây mới là nơi moat **lộ ra với khách hàng**. Vẫn là form + list | **4–6%** | MVP1 |
| — | **Tổng editor tối thiểu** | | **~20–25%** `[EM]` | |

> ⚠️ **Cộng năm dòng trên ra 20–30%, không phải 20–25% — và chênh lệch này có từ nguồn.** `Analysis-Comic-Studio-Concept` §6.1 đưa cả năm khoảng thành phần **và** con số tổng *"~20-25%"*, hai thứ không khớp nhau ở biên trên. Tài liệu này **giữ nguyên `~20–25%` của CF-6.7** làm con số chuẩn để mọi tài liệu Planning trích cùng một giá trị, và ghi lại chênh lệch thay vì âm thầm sửa một trong hai. **Đọc biên trên 25% như một ước lượng lạc quan**; nếu cần con số thận trọng khi lập ngân sách thời gian, dùng **30%**.

> **Ràng buộc thiết kế xuyên suốt cả 5 thành phần**: **mọi hành động của người dùng trong editor phải sinh một `change_log` row — kể cả hành động chỉ là "chọn ảnh này thay vì ảnh kia"**. Đây là điều kiện làm cho việc cắt canvas (mục 4.1) hợp pháp. Không có nó thì việc cắt canvas trở thành cắt luôn lá chắn pháp lý.

### 5.3 Bốn thành phần HOÃN

| # | Thành phần | Lý do hoãn | Điều kiện mở lại |
|---|---|---|---|
| 6 | Infinite canvas, zoom/pan cả chapter, hình học panel tự do, panel xoay/không chữ nhật | **Chi phí lớn nhất, giá trị tăng thêm nhỏ nhất** ở bản trả phí đầu | Có bằng chứng đo được rằng khách rời đi vì thiếu nó. Khi làm: dùng `tldraw`/`konva`/`fabric.js` sau một spike riêng — **không viết renderer từ đầu** |
| 7 | Undo/redo xuyên toàn bộ state phân tán | Chỉ undo **cục bộ** trong form + vị trí bubble. **Không undo qua generation** — một `Regenerate` tiêu tiền thật và không hoàn lại được | Không mở lại theo dạng này; đúng hơn là làm rõ UX rằng generation không undo được |
| 8 | Realtime collaboration | **1 user = 1 tenant** ở bản đầu | Khi bán gói team — mà `membership` (E2) đã chuẩn bị sẵn cho ngày đó |
| 9 | Inpainting brush / drawing tools | Cần, nhưng **không phải để bán được bản đầu** | Khi làm: bắt buộc set `generation.origin='ai_edited'` |

---

## 6. Không được cắt — danh sách cứng

> [!CAUTION]
> Đây là danh sách **duy nhất trong tài liệu này không mở ra thương lượng scope**. Mỗi mục có chung một tính chất: **rẻ khi làm từ đầu, không thể sửa về sau**. Nếu một run nào đó sau này đề xuất cắt một trong bảy mục dưới đây, câu trả lời mặc định là **không**, và người đề xuất phải bác được cột *"Không giữ thì hỏng thế nào"*.

| # | Bắt buộc giữ | Từ mốc | Chi phí giữ | **Không giữ thì hỏng thế nào** |
|---|---|---|---|---|
| **KC-1** | `parent_generation_id` (nullable FK) + `relation_kind ENUM('retry','variation','refine','continuity_fix')` | MVP1 | Hai cột | Tác phẩm của anh **và của khách hàng anh** **không được bảo hộ bản quyền ở Việt Nam** (CF-7.2 `[OFF]`). Và **không backfill được** — thêm cột sau thì mọi generation quá khứ có `parent = NULL` vĩnh viễn (CF-7.3) |
| **KC-2** | `change_log` ghi **mọi** hành động người dùng — kể cả *"chọn generation X thay vì Y"* | MVP1 | Một bảng append-only | **Prompt một mình không chứng minh được *"decisive contribution"***. Cái chứng minh được là *người đã chọn X thay vì Y, đã sửa thoại, đã đổi camera, đã kéo bubble*. Không có `change_log` ⇒ không có bằng chứng ⇒ Điều 5a không thoả |
| **KC-3** | `field_provenance` (mức field) + `generation.origin ENUM('ai','ai_edited','human')` | MVP1 | Một cột enum + một bảng phụ | Không phân biệt được phần nào do người, phần nào do AI ⇒ **không xác định được ranh giới phần được bảo hộ**. Cũng là thứ làm cho việc cắt canvas (4.1) hợp pháp |
| **KC-4** | **Cả ba mục KC-1, KC-2, KC-3 phải commit CÙNG MỘT TRANSACTION với artifact mà chúng chứng minh** | MVP1 | Kỷ luật code + monolith 1 DB | *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Audit trail commit tách rời artifact là audit trail **không đáng tin về mặt pháp lý** (CF-9.2 lý do 2) |
| **KC-5** | `tenant_id NOT NULL` trên **MỌI** bảng, là **cột ĐẦU TIÊN** của mọi composite index, cộng **Postgres RLS** | MVP1 — **ngày đầu** | Một cột + policy RLS | Retrofit `tenant_id` vào schema **đã có dữ liệu thật** là một trong những migration đắt nhất tồn tại: phải sửa mọi bảng, mọi query, mọi index, và **không có cách nào xác minh đã sửa hết**. Bỏ sót một chỗ = **rò rỉ dữ liệu chéo tenant** = **sự cố tồn vong** với một SaaS. RLS là lớp phòng thủ thứ hai — với 1 dev **không có code review**, đây là bảo hiểm rẻ nhất tồn tại |
| **KC-6** | Kiểm **opt-out signal Điều 37b** ngay trong bước **ingest** | MVP1 | **~0** (CF-7.5 `[OFF]`) | Đây là nơi **duy nhất** file của user lần đầu đi vào hệ thống. Kiểm ở chỗ khác nghĩa là đã xử lý nội dung có opt-out trước khi biết. Chi phí bằng 0 mà bỏ qua là lựa chọn không có lý do nào biện minh |
| **KC-7** | Credit ledger + **HOLD trước khi enqueue** + **hold reserve 3 credit/panel** + `CHECK (available >= 0)` ở tầng DB + **hold reaper** cho `expires_at` | MVP3 — trước bản trả phí có image gen | Một bảng ledger + một cron | **Check-rồi-gọi là race condition** (CF-6.12): 10 job đồng thời đều thấy đủ số dư và đều chạy → vượt trần. Reserve phải là **3 credit/panel** vì **N=3 là mặc định cho MỌI panel** (CF-3.1 `[OFF]`), không phải retry-on-failure (CF-3.2). Reserve 1 credit rồi tính sau = số dư âm hợp lệ hoá. Thiếu hold reaper: job crash sau khi hold ⇒ hold treo **vĩnh viễn** ⇒ khách "có credit mà không generate được" |

### 6.1 Ba hiểu nhầm hay gặp về danh sách này

| Hiểu nhầm | Thực tế |
|---|---|
| *"Provenance là feature, hoãn tới khi có khách"* | Nó là **compliance artifact** (CF-7.3), và **không backfill được**. Hoãn = mất vĩnh viễn dữ liệu của giai đoạn đầu |
| *"Cắt UI cây generation nghĩa là cắt lineage"* | **Không.** Cắt UI (D6 = ❌), giữ nguyên dữ liệu (KC-1 = bắt buộc). Đây là hai quyết định độc lập và trái chiều |
| *"Hold reserve 1 credit/panel rồi trừ thêm nếu cần"* | N=3 là **mặc định cho mọi panel**, không phải trường hợp xấu. Reserve 1 nghĩa là **hệ thống thiết kế để vượt trần trong trường hợp bình thường** |

---

## 7. Go/No-Go Decision

> Đây là mục quan trọng nhất của tài liệu. Ba gate dưới đây là **ba cửa độc lập**, đo ba loại rủi ro khác nhau, và **không thay thế được cho nhau**: một sản phẩm hợp pháp mà không consistency thì vô dụng; một sản phẩm consistency tốt mà lỗ mỗi lần dùng thì không sống được; một sản phẩm ngon và có lãi mà bất hợp pháp thì không được tồn tại.
>
> **Nguyên tắc chung**: mọi ngưỡng dưới đây được định nghĩa **TRƯỚC** khi đo. Không sửa ngưỡng sau khi nhìn thấy kết quả — đó là cách một gate biến thành nghi lễ.

### 7.0 Tổng quan ba gate

| Gate | Đo cái gì | Thời điểm | Nếu FAIL |
|---|---|---|---|
| **G0 — Pháp lý** | Rủi ro **nhị phân** | Trước dòng code **thương mại** đầu tiên | Dừng thương mại hoá |
| **G1 — Kỹ thuật** | Tiền đề sản phẩm còn đứng không | Cuối **09/2026**, sau MVP0 | Đổi cách tiếp cận — biết sau **2 tuần** thay vì 4 tháng |
| **G2 — Kinh tế** | Mô hình giá có sống được không | Cuối **Q4/2026**, sau MVP1 | Đổi granularity render sang whole-page — **data model không phải đổi** |

---

### 7.1 G0 — Gate Pháp lý

| | |
|---|---|
| **Thời điểm** | **Trước dòng code thương mại đầu tiên.** ⚠️ **KHÔNG chặn MVP0 và MVP1** — xem [Roadmap mục 6](./Roadmap.md#6-phụ-thuộc--đường-găng) |
| **Ai quyết** | Luật sư SHTT Việt Nam (bên ngoài, **chưa engage**) |
| **Chi phí** | Một buổi tư vấn — *"thấp hơn nhiều bậc so với chi phí build sai rồi phải dỡ"* (Analysis §8.5) |

**Ba câu hỏi phải mang đi** (CF-7.8 — đã được narrow xuống mức luật sư trả lời được):

| # | Câu hỏi | Bối cảnh phải đưa kèm |
|---|---|---|
| **Q1** | **Điều 37a NĐ 134/2026 có áp cho *inference-time extraction* trên nội dung do user upload, hay chỉ áp cho *huấn luyện* model?** | Cả ba điều 37a/37b/37c đóng khung quanh *"huấn luyện"*. Use case comic-studio **không phải training**: không tạo model mới, không lưu nội dung vào weights, xử lý **theo chỉ dẫn của chính người upload**. ⚠️ CF-7.4: hiểu biết hiện tại về Điều 37a **dựa trên bản tóm tắt, KHÔNG phải nguyên văn** (nguồn gốc trả 403 / paywall) — **luật sư phải đọc nguyên văn** |
| **Q2** | **Khoản 4 Điều 11 Luật TTNT 2025 — nghĩa vụ đánh dấu định dạng máy đọc áp cho *mọi* nội dung AI, hay chỉ nội dung *"mô phỏng người thật hoặc sự kiện thực tế"*? Watermark của provider (SynthID) có thoả không?** | CF-7.7 `[OFF]`: **hai nguồn mô tả phạm vi KHÁC NHAU**. Deadline tuân thủ **~01/03/2027** |
| **Q3** | **Nền tảng có được coi là "doanh nghiệp cung cấp dịch vụ trung gian" để hưởng miễn trừ Điều 198b không**, khi nó không chỉ *lưu trữ* mà còn *xử lý/biến đổi* nội dung của user? | Câu tương đương ở luật Mỹ: DMCA §512(c) có phủ *"hosting + AI processing"*? |

**Tiêu chí PASS — đo được, không phải "đánh giá chủ quan":**

Mỗi câu Q1/Q2/Q3 phải được luật sư trả về **bằng văn bản**, và mỗi câu được phân về **đúng một trong ba trạng thái**:

| Trạng thái | Định nghĩa |
|---|---|
| 🟢 **CHO PHÉP** | Luật sư kết luận mô hình user-upload thương mại không bị điều khoản đó chặn |
| 🟡 **CHO PHÉP CÓ ĐIỀU KIỆN** | Không bị chặn **nếu** thoả một danh sách điều kiện **liệt kê được** (ví dụ: bắt buộc user warrant, bắt buộc watermark, giới hạn địa lý) |
| 🔴 **CHẶN** | Luật sư kết luận mô hình như thiết kế **vi phạm** |

| Kết quả | Quyết định |
|---|---|
| **PASS** | **3/3 câu có văn bản trả lời** VÀ **0 câu 🔴** |
| **PASS CÓ ĐIỀU KIỆN** | 0 câu 🔴, nhưng có ≥1 câu 🟡 ⇒ **mọi điều kiện của câu 🟡 phải vào backlog compliance và hoàn thành TRƯỚC khi bật thanh toán**. Không được coi là "sẽ làm sau" |
| **FAIL** | ≥1 câu 🔴, **hoặc** hết thời hạn mà chưa có văn bản cho đủ 3 câu |

> Chú ý cách đo: tiêu chí là **sự tồn tại của một artifact** (văn bản tư vấn) + **phân loại nhị phân trên nội dung của nó**. Không có chỗ nào cho "cảm thấy ổn".

**Nếu FAIL**: **DỪNG THƯƠNG MẠI HOÁ.** Lý do là CF-7.9 — đây là **rủi ro nhị phân duy nhất** của cả dự án: *mọi rủi ro khác trả lời sai thì sản phẩm **kém hơn**; ba câu này trả lời sai thì sản phẩm **bất hợp pháp***.

Hai đường còn lại khi FAIL, xét theo thứ tự: (a) **cấu trúc lại mô hình** để thoát điều khoản bị chặn (ví dụ: chỉ nhận nội dung mà user chứng minh sở hữu bản quyền + giới hạn thị trường) rồi chạy lại G0; (b) nếu (a) không khả thi → xem [mục 8](#8-điều-kiện-thoát-kill-criteria) K1.

---

### 7.2 G1 — Gate Kỹ thuật (sau MVP0)

| | |
|---|---|
| **Thời điểm** | **Cuối 09/2026** |
| **Đầu vào** | MVP0: 1 chapter · Story Bible + panel script viết tay · ~$12 `[EM tính từ OFF]` (CF-3.11 — ở giá standard **$0.134**; **~$6** nếu batch, nhưng lấy **số cao làm trần an toàn** vì cần vòng lặp nhanh nên batch khó dùng) |
| **Câu hỏi gate** | *Tiền đề của cả sản phẩm còn đứng không?* |

**Năm tiêu chí, mỗi tiêu chí một ngưỡng đo được:**

| # | Chỉ số | Nguồn chỉ số | **Ngưỡng PASS** | Nguồn ngưỡng | Cách đo |
|---|---|---|---|---|---|
| **G1-a** | **Consistency nhân vật** | CF-8.5 (1) | **≥70%** panel được nhận ra là **cùng một nhân vật**, không cần retry | `findings/architect.md` §7.3 — ngưỡng đề xuất của lens kiến trúc run trước | Nhìn **8 panel liền nhau**: *có nhận ra đó là cùng một nhân vật mà không cần được nhắc không?* (CF-8.5). Đếm trên toàn bộ panel của MVP0, chấm bằng mắt, ghi ra bảng |
| **G1-b** | **N tối thiểu** để VLM-select ra panel đạt | CF-8.5 (2) | **N ≤ 3** | `findings/architect.md` §7.3 (*"số lần generate/panel dùng được ≤ 3"*) + CF-3.1 `[OFF]` *"performance saturates at N=3"* | Chạy MVP0 ở N=2 và N=3 trên cùng bộ panel, so tỉ lệ panel đạt. **Mỗi bậc N giảm được là ~33% COGS** (CF-8.5) |
| **G1-c** | ⭐ **Human-reject rate sau VLM-select** | CF-8.5 (3) — ⚠️ **chưa ai công bố con số này** | **≤30%** PASS · **30–50%** PASS CÓ ĐIỀU KIỆN · **>50%** FAIL | ⚠️ **`[EM]` — ngưỡng do em định nghĩa tại run này, không có nguồn ngoài.** Lý do chọn: CF-8.5 nói chỉ số này quyết định *"checker có cắt được công người hay chỉ thêm chi phí"*; nếu người vẫn phải loại >1/2 số panel mà VLM đã chọn, VLM-select **đang là một lớp chi phí thuần** | Người chấm pass/fail từng panel **sau khi** VLM đã chọn. `reject_rate = số panel người loại / tổng panel VLM chọn` |
| **G1-d** | ⭐ **Multi-character panel 2–3 nhân vật** — hàng load-bearing (CF-6.4) | CF-8.6 | **Panel 2 nhân vật: ≥60% đạt** (đúng identity **VÀ** đúng trang phục/vật phẩm gắn đúng người). **Panel 3 nhân vật: đo và báo cáo số, không đặt ngưỡng chặn** | ⚠️ **`[EM]` — ngưỡng do em định nghĩa.** Lý do chọn hình dạng này: CF-6.5 `[OFF]` cho thấy ID-Sim **sụp** từ 42.33 (2 người) → 27.21 (3), nên đặt cùng một ngưỡng cho cả 2 và 3 nhân vật là đặt sai. **Không benchmark độc lập nào đo frontier model ở mức này** (CF-6.4) ⇒ MVP0 **là** phép đo đầu tiên | Chấm hai trục riêng: (1) nhận ra đúng người; (2) attribute binding — trang phục/vũ khí có gắn **đúng người** không (đây là chỗ CF-6.5 nói *"near-complete failure beyond three subjects"*) |
| **G1-e** | **Đường đi của chữ tiếng Việt** | `findings/architect.md` §7.3 | **100%** panel có thoại được typeset bằng **overlay layer**; **0** panel dựa vào model render chữ trong ảnh | `findings/architect.md` §7.3 + Analysis §4.2 (*"dùng typeset layer bất kể"*) | Đếm trực tiếp trên trang composite của MVP0 |

**Đo thêm tại G1, không phải tiêu chí chặn** (CF-8.6): **regen ratio thực tế p50/p90** — biến quyết định của cả mô hình tài chính. Nó **không** chặn G1 nhưng **là đầu vào bắt buộc của G2**. Nếu MVP0 kết thúc mà không có p50/p90, G2 không chạy được.

**Kết luận gate:**

| Kết quả | Điều kiện | Hành động |
|---|---|---|
| **PASS** | 5/5 tiêu chí đạt | Đi tiếp MVP1 theo [Roadmap.md](./Roadmap.md) |
| **PASS CÓ ĐIỀU KIỆN** | G1-a, G1-b, G1-e đạt; G1-c ở dải 30–50% **hoặc** G1-d panel 2 nhân vật ở dải 50–60% | Đi tiếp, **nhưng** cứng hoá thêm ràng buộc: G1-d dưới ngưỡng ⇒ **cứng hoá ≤2 nhân vật/panel thay vì ≤3** trong schema (đổi C5 ở bảng mục 3); G1-c ở dải giữa ⇒ HITL gate ở MVP1 (H1) phải được thiết kế cho tải review cao hơn dự kiến |
| **FAIL** | Bất kỳ tiêu chí nào rơi vào vùng FAIL | **Đổi cách tiếp cận** — và biết điều đó sau **2 tuần** thay vì 4 tháng (CF-8.5). ⚠️ **FAIL ≠ huỷ dự án**: đường đầu tiên là **đổi định vị** sang storyboard generator / công cụ hỗ trợ hoạ sĩ (`findings/architect.md` §7.3). Chỉ khi đường đó cũng không đứng mới xét [mục 8](#8-điều-kiện-thoát-kill-criteria) K2 |

---

### 7.3 G2 — Gate Kinh tế (sau MVP1)

| | |
|---|---|
| **Thời điểm** | **Cuối Q4/2026** |
| **Đầu vào** | Regen ratio **p50/p90 đo được** (từ MVP0 và từ `usage_daily` của MVP1) + `generation.cost_usd` thực tế |
| **Câu hỏi gate** | *Mô hình 3 tầng (CF-2) có giữ được margin trong khoảng CF-3.10 không?* |

**Số nền — copy nguyên vẹn cả số và nhãn:**

| # | Số nền | Giá trị | Nhãn |
|---|---|---|---|
| a | Hệ số generate mặc định | **N = 3** cho **MỌI** panel — *"performance saturates at N=3"*. ⚠️ **KHÔNG phải retry-on-failure** (CF-3.2): là generate 3 candidate rồi VLM chọn 1. **Không thể lấy chất lượng của N=3 mà tính chi phí của N=2** | `[OFF]` CF-3.1/3.2 |
| b | Ảnh / chapter | **60** (15 page × 4 panel) | ⚠️ `[EM]` — **giả định, KHÔNG phải số đo** (CF-3.3) |
| c | Chi phí/chapter @N=3, Gemini batch | **$12,06** | `[EM tính từ OFF]` ⚠️ **là SÀN, không phải trần** — chưa tính VLM call để score 3 candidate (CF-3.5) |
| d | Margin trên $9.99, 1 chapter/tháng @N=3 | **−21%** | `[EM]` CF-3.6 |
| e | Margin power user 3 chapter/tháng @N=3 | **−262%** | `[EM]` CF-3.7 |
| f | **Kỳ vọng gross margin** | **50–60%** (không phải 80%) | `[BCN]` ICONIQ 52%, Bessemer 50–60% — CF-3.10 |
| g | 1 chapter @N=3 | **180 ảnh** — **vượt ngưỡng 125 ngay ở chapter đầu tiên** | `[EM]` CF-3.9 · ngưỡng CF-2.5 `[TC]` |

**Tiêu chí PASS — đo được:**

| # | Tiêu chí | Ngưỡng | Cách đo |
|---|---|---|---|
| **G2-a** | Có **dữ liệu** để tính | Regen ratio **p50 và p90** có giá trị thực đo từ `usage_daily`, trên **≥1 chapter hoàn chỉnh** | Query rollup `usage_daily` (F1). Không có dữ liệu ⇒ G2 **không chạy được**, không phải "tạm PASS" |
| **G2-b** | **Margin ở kịch bản p50** | Gross margin tính từ COGS thực đo nằm **trong dải 50–60%** `[BCN]` (CF-3.10) trên giá của **ít nhất một tầng** trong mô hình 3 tầng (CF-2) | `margin = (giá tầng − COGS thực đo/tháng của user trung vị) / giá tầng`. COGS lấy từ tổng `generation.cost_usd` thực, **không** từ ước lượng |
| **G2-c** | **Không lỗ ở kịch bản p90** | Margin ở p90 **> 0%** | Cùng công thức, thay p50 bằng p90. Đây là tiêu chí chống kịch bản power user **−262%** `[EM]` (CF-3.7) |
| **G2-d** | Ngưỡng phân tuyến còn đúng | Tỉ lệ user vượt **~125 ảnh/tháng** `[TC]` (CF-2.5) được đo, và mô hình BYOK (CF-2.4) phủ được nhóm đó | Đếm trên `usage_daily`. ⚠️ Lưu ý CF-3.9: **1 chapter = 180 ảnh** ⇒ dự kiến **phần lớn user hoạt động sẽ vượt ngưỡng**. Nếu đúng vậy, BYOK không còn là *"tuỳ chọn mở khoá"* trên thực tế — và đó là một phát hiện phải ghi lại, không phải một lỗi đo |

| Kết quả | Điều kiện |
|---|---|
| **PASS** | G2-a **và** G2-b **và** G2-c đạt |
| **FAIL** | G2-b hoặc G2-c không đạt |
| **KHÔNG CHẠY ĐƯỢC** | G2-a không đạt ⇒ **lùi gate**, không PASS mặc định. Thiếu dữ liệu không phải bằng chứng tốt |

**Nếu FAIL — đường lui đã được thiết kế sẵn, xếp theo thứ tự:**

1. ⭐ **Đổi granularity render sang whole-page.** Analysis §9b.3: per-panel @N=3 cho margin **−141%** `[EM]`; whole-page @N=3 cho **+40%** `[EM]`. *(Cả hai là kết quả reverse-engineer từ giá công bố của ComicInk, không phải margin đo được của một công ty nào — giữ nhãn khi trích.)* **`Panel Specification` không mất giá trị** — nó là *spec*, không bắt buộc mỗi panel một lần gọi model; một page compile được **nhiều panel spec thành MỘT prompt whole-page**. ⇒ **Data model KHÔNG phải đổi.** Đây là lần thứ hai quyết định *"spec là dữ liệu chính, ảnh chỉ là output"* tự trả lãi.
   > ⚠️ **Nói thẳng giới hạn của đường lui này**: whole-page @N=3 cho **+40%** `[EM]`, vẫn **dưới** dải kỳ vọng **50–60%** `[BCN]` (CF-3.10). Nó cứu được tình trạng lỗ, **không** tự động đưa margin về mức chuẩn ngành. Đừng coi nó là lời giải cuối.
   >
   > ⚠️ **Và lưu ý phép so sánh này lệch hạng nguồn**: `+40%` là `[EM]` (suy ra từ giá đối thủ), còn `50–60%` là `[BCN]` (benchmark ngành có tên firm). So một ước lượng với một benchmark thì kết luận *"vẫn dưới chuẩn"* đúng về hướng nhưng **không đủ chắc để làm ngưỡng gate**.
2. **Whole-page mặc định + per-panel là hành động TRẢ PHÍ.** Người dùng thấy giá trị đúng lúc họ *cần* sửa, và trả tiền đúng lúc đó.
3. **Đẩy BYOK (CF-2.4) từ "tuỳ chọn mở khoá" lên đường chính cho nhóm vượt ngưỡng.** Với BYOK, xung đột **biến mất hoàn toàn** vì COGS không còn là của mình (Analysis §9b.3).
4. Nếu cả ba đường trên đều không đưa margin về dương ⇒ [mục 8](#8-điều-kiện-thoát-kill-criteria) K3.

> [!WARNING]
> **Đường KHÔNG được đi khi G2 FAIL**: hạ N từ 3 xuống 1 để cứu margin. CF-3.2 `[OFF]` nói rõ **không thể lấy chất lượng của N=3 mà tính chi phí của N=2**. Hạ N là đổi chất lượng lấy margin — nếu làm, phải chạy lại **G1** chứ không phải chỉ G2.

---

## 8. Điều kiện thoát (kill criteria)

> [!IMPORTANT]
> Mục này tồn tại vì tài liệu planning thường né nó. Với một dự án **1 người, không funding** (CF-1.2), chi phí lớn nhất không phải tiền — mà là **thời gian của người duy nhất trong đội**. Định nghĩa điều kiện dừng **trước** khi đầu tư cảm xúc là cách rẻ nhất để bảo vệ chính nguồn lực đó.
>
> **Phân biệt hai loại kết cục** — trộn hai loại này là lỗi hay gặp nhất:
> - **PIVOT** = tiền đề sai, nhưng năng lực và dữ liệu đã xây vẫn dùng được cho một định vị khác.
> - **KILL** = dừng hẳn, không có định vị nào còn đứng.

### 8.1 Năm điều kiện KILL

| # | Loại | Điều kiện dừng hẳn | Vì sao là KILL chứ không phải PIVOT | Đo lúc nào |
|---|---|---|---|---|
| **K1** | **Pháp lý** | G0 có **≥1 câu 🔴 CHẶN**, **VÀ** phương án cấu trúc lại (giới hạn nội dung user sở hữu bản quyền + giới hạn thị trường) cũng bị luật sư kết luận **không thoát** | Đây là **rủi ro nhị phân duy nhất** (CF-7.9): sản phẩm **bất hợp pháp**, không phải kém hơn. Không có pivot nào cứu được một mô hình mà cơ quan quản lý cấm | G0 |
| **K2** | **Kỹ thuật** | G1-a **< 50%** `[EM]` (dưới cả ngưỡng pivot 70%), **VÀ** định vị thay thế (storyboard generator / công cụ hỗ trợ hoạ sĩ) cũng không có người dùng xác nhận trong **8 tuần** kể từ khi pivot | Consistency dưới 50% nghĩa là **không có workaround thủ công** — không ai vẽ lại 5000 panel bằng tay (`findings/architect.md` §7.1). ⚠️ Ngưỡng 50% và cửa sổ 8 tuần đều là **`[EM]` do em định nghĩa**, không có nguồn ngoài | Sau G1 + 8 tuần |
| **K3** | **Kinh tế** | Cả **ba** đường lui của G2 đều không đưa margin về dương ở p90: (1) whole-page, (2) per-panel trả phí, (3) BYOK — trong đó BYOK bị bác bởi **tỉ lệ user bật BYOK đo được < 20%** `[EM]` ở nhóm vượt ngưỡng 125 ảnh/tháng | Nếu ba đường ra đã thiết kế sẵn đều đóng, mô hình kinh doanh **không có đường thứ tư** trong thiết kế hiện tại. ⚠️ Ngưỡng 20% là **`[EM]` do em định nghĩa** | Sau G2 + 1 chu kỳ đo |
| **K4** | **Thị trường** | Sau **12 tháng** kể từ bản trả phí đầu tiên: MRR **< $300** (cận dưới CF-4.4 `[EM]`) **VÀ** không có tăng trưởng dương trong 3 tháng liên tiếp | Neo thực tế: **Anifusion** — solo founder, **$833 MRR**, có lãi, **~2 năm** kể từ launch, **$0 marketing** `[TC]` (CF-4.5, ⚠️ **nguồn mâu thuẫn**: nguồn khác ghi $5.000/tháng; giá $9/mo vs €20/mo — **ghi cả hai, không chọn một**). Dưới cận dưới của chính SOM năm 1 sau 12 tháng nghĩa là giả định phân phối sai, không phải chậm | Tháng 12 sau bản trả phí |
| **K5** | **Vận hành** | Founder không còn dành được thời gian đều đặn cho dự án trong **3 tháng liên tiếp** | **Bus factor = 1** (CF-1.2). Đây là điều kiện dừng thật nhất và ít được viết ra nhất. ⚠️ Cửa sổ 3 tháng là **`[EM]` do em định nghĩa** | Liên tục |

### 8.2 Nghĩa vụ khi KILL — "dừng có trật tự"

Nếu đã có khách trả tiền tại thời điểm kill (K3/K4/K5), việc dừng **không** phải tắt server:

1. **Thông báo trước ≥30 ngày** cho mọi tenant đang trả phí.
2. **Xuất dữ liệu đầy đủ** cho từng tenant: Story Bible, Comic IR, mọi ảnh, và **cả `change_log` + `field_provenance`** — vì đó là hồ sơ chứng minh quyền tác giả **của khách** (KC-2, KC-3). Đây là lý do E3 và GP-5 (`ON DELETE CASCADE` + đường hard-delete đã kiểm thử) phải có từ MVP1: **đường thoát phải được xây cùng lúc với đường vào**.
3. **Ngừng thu tiền** ngay tại thời điểm thông báo, không đợi hết chu kỳ.

### 8.3 Ba thứ **KHÔNG** phải điều kiện kill

Ghi ra để tránh phản ứng thái quá — mỗi mục dưới đây trông giống tin xấu nhưng không phải:

| Sự kiện | Vì sao không kill | Phản ứng đúng |
|---|---|---|
| **GlobalComix (+ INKR) ra tính năng trùng** — $13M funding, định vị *"the Figma for comics"*, đã có typesetting/text detection/image cleaning `[TC]` (CF-5.2) | Họ đánh vào **trục editor**, comic-studio đánh vào trục **Story Bible + Timeline State + Continuity** — trục *"không ai làm được rẻ"* và là trục duy nhất mà quy mô 1 dev có lợi thế (nó là thiết kế dữ liệu, không phải nhân lực UI) | Củng cố mục 4.1 (đừng đua editor). Đổi thông điệp, không đổi sản phẩm |
| **Constella (WEBTOON) ship công cụ consistency miễn phí** `[TC]` (CF-5.4 — ⚠️ **chưa xác nhận đã ship hay còn là announcement**) | Constella nhắm creator **đã biết vẽ**; comic-studio nhắm tác giả **không biết vẽ** (CF-1.5). **Hai phân khúc** — nhưng CF-5.5 nói rõ khoảng cách **có thể** hẹp lại | Theo dõi ở mỗi gate. Nếu Constella mở cho người không biết vẽ ⇒ nâng thành rủi ro cấp K |
| **Backlash cộng đồng với nội dung AI** — Naver Webtoon bị độc giả boycott; BlueLine Studio bị buộc vẽ lại `[TC]` (CF-5.6) | Đây là rủi ro **kênh**, không phải rủi ro sản phẩm. Bằng chứng đối trọng: Novelcrafter **220.000+ authors** `[OFF]` — cộng đồng **viết** chấp nhận, cộng đồng **vẽ** thì không (CF-5.7) | Giữ positioning **disclosure-first**, nhắm **writer** không nhắm **artist**. Không marketing vào cộng đồng hoạ sĩ |

---

## 9. Tài liệu tham khảo

### 9.1 Tài liệu trong repo

- [Charter-Comic-Studio.md](./Charter-Comic-Studio.md) — biện minh dự án, ràng buộc cấp dự án, RACI
- [Roadmap.md](./Roadmap.md) — lịch trình, exit criteria từng mốc, đường găng
- [OKRs.md](./OKRs.md) — mục tiêu và Key Result theo chu kỳ
- [Risk-Register.md](./Risk-Register.md) — sổ rủi ro, rà soát theo gate G0/G1/G2
- [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md) — bản thẩm định gốc (§4.2 bảng khả thi, §5.5–5.7, §6 ba thứ nên cắt, §8.5 ba câu hỏi luật sư, §9b.3 xung đột M13, §10 lộ trình, §12 kết luận)
- [findings/architect.md](./pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/findings/architect.md) — findings kiến trúc run trước (§7.1–7.3 thứ tự milestone + ngưỡng gate, §B4 credit ledger)
- [outline.md](./pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md) — bảng **Canonical Facts** CF-1 → CF-9, nguồn sự thật chung của toàn bộ tài liệu Planning

### 9.2 Nguồn ngoài được dẫn qua bảng Canonical Facts

| Nội dung | Nguồn | Nhãn |
|---|---|---|
| CANVAS — character 4.91/5, human win-rate 86,7%, props 4.19/5, N=3 saturation | [arXiv 2604.13452](https://arxiv.org/html/2604.13452v1) | `[OFF]` |
| CogCanvas ID-Sim theo số nhân vật — *"near-complete failure beyond three subjects"* | [arXiv 2606.15867](https://arxiv.org/html/2606.15867) | `[OFF]` |
| Nghị định 134/2026/NĐ-CP, Điều 5a | [Cục Bản quyền tác giả](https://cov.gov.vn/tin-tuc/gioi-thieu-nghi-dinh-so-1342026ndcp-quy-dinh-ve-quyen-tac-gia-quyen-lien-quan-168925.html) · [Baker McKenzie](https://www.bakermckenzie.com/en/insight/publications/2026/05/vietnam-redefining-copyright-for-ai) | `[OFF]` |
| Comp pricing Novelcrafter (220.000+ authors, không bao giờ bán inference) | [novelcrafter.com/pricing](https://www.novelcrafter.com/pricing) | `[OFF]` |
| Kỳ vọng gross margin 50–60% | ICONIQ 52% · Bessemer 50–60% | `[BCN]` |

> [!NOTE]
> Danh sách URL đầy đủ nằm ở mục *Tài liệu tham khảo* của [Analysis-Comic-Studio-Concept.md](../050-Research/Analysis-Comic-Studio-Concept.md). Tài liệu này **chỉ dẫn lại** những nguồn trực tiếp chống lưng cho một quyết định cắt scope hoặc một ngưỡng gate.
