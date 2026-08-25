---
id: STORY-G-01
type: story
status: draft
created: 2026-08-24
---

# Story-Provenance-Chain-Parent-Generation

## 1. Story

> Là **khách hàng SaaS**, tôi muốn **mọi generation lưu `parent_generation_id` + `relation_kind` + `field_provenance` + `generation.origin`**, để **tôi chứng minh được quyền tác giả của mình theo Điều 5a**.

## 2. Part of

| Quan hệ | Tài liệu |
|---|---|
| **Epic cha** | [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md) — hàng 1/6 mục 3 |
| **BRD cha** | [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) — `BR-007-01`, `KC-1`/`KC-3` §4.1 |
| **Use Case liên quan** | [UC-06 — Generate Panel And Pick Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — nơi *"đã chọn X thay vì Y"* xảy ra và nơi `parent_generation_id` + `relation_kind` được ghi lần đầu |
| **Điều kiện chặn liên quan** | `BLOCKER-04` ([Charter §9.3](../../010-Planning/Charter-Comic-Studio.md#93-ba-điều-kiện-chặn-phụ)) — chặn **MỌI THỨ**, vì không backfill được |

## 3. Bối cảnh & nguồn

- **Hạng mục MVP-Scope**: [MVP-Scope §3 GP-1](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) — `🟡` ghi tay ở MVP0 → `✅` ở MVP1. [MVP-Scope §6 KC-1, KC-3](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) — hai trong bảy mục không mở ra thương lượng scope.
- **Exit criterion Roadmap**: [Roadmap §2 — M1-5](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — *"5 hạng mục provenance (`parent_generation_id`, `relation_kind`, `change_log`, `field_provenance`, `generation.origin`) tồn tại, và có test chứng minh chúng commit CÙNG MỘT transaction với artifact"* (tiêu chí #2 của test được sở hữu đầy đủ bởi `Story-Provenance-Committed-In-Same-Transaction`, Story này sở hữu tiêu chí #1 — 5 cột tồn tại).
- **Căn cứ pháp lý**: **NĐ 134/2026/NĐ-CP, Điều 5a** `[OFF]` (CF-7.2 / CF-7.3, `findings/business-analyst.md` §5.2) — tác phẩm AI-assisted **chỉ** được bảo hộ nếu con người có *"substantial and decisive intellectual contribution to the creative process"*; tác phẩm do AI tạo hoàn toàn **không** được bảo hộ. Kèm nghĩa vụ lưu **prompts, inputs, intermediate drafts**.
- **`Valuable-I` (giá trị không đảo ngược)**: không lưu từ generation đầu tiên ⇒ **vĩnh viễn** không có hồ sơ Điều 5a cho những generation đó (CF-7.3 `[OFF]`); mọi generation quá khứ giữ `parent = NULL` mãi mãi.
- **Ghi chú diễn giải `[EM]`**: [MVP-Scope §3.1](../../010-Planning/MVP-Scope.md#31-ba-ô-đáng-chú-ý-nhất-trong-bảng) diễn giải *"generation đầu tiên"* theo nghĩa pháp lý = generation đầu tiên của **sản phẩm thật** (MVP1), vì code MVP0 bị vứt sau khi trả lời câu hỏi và **không có database** (Glossary term *MVP0*). Nhãn `[EM]` giữ nguyên khi trích.
- ⛔ **CẤM-09** ([BRD-007 §4.5](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md#45-ràng-buộc-về-chất-lượng-nguồn--bắt-buộc-mang-theo)): cắt UI cây generation (`D6` = `❌`) **không** đồng nghĩa cắt cột dữ liệu `parent_generation_id` (`KC-1` = bắt buộc). Hai quyết định độc lập và trái chiều.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Bảng `generation` có đủ 4 cột/quan hệ: `parent_generation_id` (nullable FK tới `generation.id`) + `relation_kind ENUM('retry','variation','refine','continuity_fix')` + `field_provenance` (mức field) + `generation.origin ENUM('ai','ai_edited','human')` — kiểm bằng đọc schema migration đã merge.
- [ ] `INSERT` vào bảng `generation` **thiếu** giá trị `origin` bị **DB từ chối** (constraint `NOT NULL`), không phải chỉ bị cảnh báo ở tầng ứng dụng — đo bằng: chạy insert test thiếu cột này, kỳ vọng lỗi ở tầng DB.
- [ ] Một generation tạo ra bằng thao tác *"retry"* có `relation_kind = 'retry'` và `parent_generation_id` trỏ đúng generation gốc — đo bằng truy vấn generation vừa tạo sau khi thực hiện retry trên UI/luồng nghiệp vụ.
- [ ] Một field bị người dùng sửa tay (ví dụ đổi thoại) có dòng `field_provenance` ghi `origin = 'human'` hoặc `'ai_edited'` cho đúng field đó, **không** phải cho toàn bộ generation — đo bằng đối chiếu field đã sửa với bảng `field_provenance`.

### Đường không hạnh phúc (unhappy path)

- [ ] Generation đầu tiên của một chuỗi (không có generation cha) vẫn phải có `origin` xác định (`'ai'` hoặc `'human'`) và `parent_generation_id = NULL` hợp lệ — không được coi `NULL` là lỗi dữ liệu.
- [ ] Hai request tạo generation đồng thời cho cùng một panel không được ghi đè `field_provenance` của nhau — đo bằng test race: gửi 2 generation request song song, kiểm tra cả hai dòng `field_provenance` đều tồn tại và không dòng nào bị mất.
- [ ] Một generation có `relation_kind = 'continuity_fix'` nhưng không trỏ được về generation gốc (dữ liệu hỏng) phải bị chặn tại tầng ứng dụng trước khi tạo record, không được lưu record mồ côi về mặt nghiệp vụ.

### Ràng buộc cứng không được vi phạm

- `KC-1` — `parent_generation_id` (nullable FK) + `relation_kind ENUM(...)`, bắt buộc từ MVP1, không backfill được.
- `KC-3` — `field_provenance` (mức field) + `generation.origin ENUM(...)`, bắt buộc từ MVP1.

### Story này KHÔNG làm

- [ ] **KHÔNG** xây UI duyệt cây generation (tree view / diff / branch-merge) — `D6` bị cắt hẳn ở mọi mốc kể cả Full Scope. Thay thế là flat list theo `created_at` + `approved_generation_id`, thuộc Story khác (nếu có), không thuộc Story này.
- [ ] **KHÔNG** đảm bảo commit cùng transaction với `change_log`/`usage_event` — đó là phạm vi của `Story-Provenance-Committed-In-Same-Transaction` (`KC-4`).
- [ ] **KHÔNG** tự diễn giải hay khẳng định thêm phạm vi Điều 5a ngoài những gì CF-7.2/CF-7.3 đã ghi.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | `TBD` | Không có ước lượng bottom-up nào trong repo cho Story này (`Roadmap §1.3`: *"Tổng tuần-người: TBD"*). Chi phí giữ theo `MVP-Scope §6 KC-1/KC-3` là *"hai cột"* / *"một cột enum + một bảng phụ"* — định tính, không phải giờ-người. **Điều kiện escalate**: nếu ước lượng thực tế lúc nhặt Story lên vượt **16 giờ-người**, Story này **không được split** (xem mục 6 — vỡ `Independent`) ⇒ phải ghi lý do vượt trần thành văn, không tách lô. |
| `E_hitl` | `0` giờ-người/chapter | Story thuần schema + ràng buộc DB, không tạo ra bước xác nhận thủ công lặp lại theo chapter. Nếu vận hành thực tế phát sinh nhu cầu review thủ công `field_provenance`, đó là tín hiệu escalate, không phải chi phí đã biết trước. |

## 6. INVEST

| Tiêu chuẩn | Đánh giá |
|---|---|
| Independent | ⚠️⚠️ **VỠ.** [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước): *"`KC-1` + `KC-3` gắn với nhau về giá trị pháp lý: có `parent_generation_id` mà thiếu `field_provenance` ⇒ không xác định được ranh giới phần được bảo hộ. Cắt thành hai lô cho ra hai lô đều không đủ chứng minh Điều 5a."* |
| Negotiable | ⚠️ **Bị giới hạn** — Story chạm `KC-1`, `KC-3`, cả hai đều là *"danh sách duy nhất không mở ra thương lượng scope"* ([MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng)). |
| Valuable | `Valuable-I` — xem mục 3: hậu quả không đảo ngược là mất bảo hộ bản quyền vĩnh viễn cho generation không có provenance. |
| Estimable | Estimable bằng giờ-người, hiện `TBD` — xem mục 5. |
| Small | ⚠️ [Security suy luận] — §4.7 chấm cột `S = ⚠️` nhưng §4.10 chỉ ghi lý do cho `I`, không có dòng riêng cho `S`. Suy luận: `KC-1` và `KC-3` bị ràng buộc chung (xem cột `I`) khiến kích thước thực tế của Story phụ thuộc vào việc thiết kế đủ cả bốn hạng mục cùng lúc — không có sub-slice nào nhỏ hơn mà vẫn đủ điều kiện chứng minh Điều 5a, nên Story khó giữ nhỏ độc lập với quyết định thiết kế `field_provenance`. |
| Testable | Testable bằng checklist assertion nhị phân — xem mục 4 AC-1/AC-2. |

> **Kết luận mục 6**: `I` và `S` đều mang `⚠️`/`⚠️⚠️`. Lý do `I` là nguyên văn từ `findings/business-analyst.md` §4.10. Lý do `S` là suy luận của lô này (`[Security suy luận]`), không phải trích dẫn có sẵn trong `findings`.
