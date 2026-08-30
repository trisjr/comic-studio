---
id: HANDOFF-P2
type: reference
status: live
created: 2026-08-29
---

# Handoff — run `2026-08-28-phase-2-architecture-design-comic-studio`

> ✅ **RUN ĐÃ HOÀN TẤT.** File này giữ lại như hồ sơ; kết quả và bài học ở [`cost.md`](./cost.md).
> Đọc theo thứ tự: [`brief.md`](./brief.md) → [`run-plan.md`](./run-plan.md) → [`outline.md`](./outline.md) → [`cost.md`](./cost.md) → [`escalations.md`](./escalations.md).

## 1. Trạng thái — ✅ XONG

**63/63 hạng mục.** Nguồn sự thật là cột *Xong* của [`outline.md`](./outline.md).

**58 tài liệu mới** ở `docs/030-Specs/` (19 Architecture · 14 Schema · 21 API · 3 Security · 1 MOC), cộng 3 file được sửa (`SRS`, `Glossary`, `000-Index`).

> ⚠️ **Hai việc còn hở, đã ghi rõ chủ, ⛔ không phải lỗi ẩn** — quyết định mở/đóng gate là của **Founder**:
> 1. **Tiêu chí thoát #3 chưa trọn**: `UC-02` bước 1/`EXC-1` (kích hoạt/retry extraction) và `UC-07` bước 3 (auto-placement bubble) ⛔ chưa có endpoint. Cả hai **tự khai trong file**, có mã `TBD` và có chủ.
> 2. **`TD-2`/`TD-3` đang BỊ CHẶN** cho tới khi role thứ năm `app_operator` được thêm vào `SDD` §7.4 + `ADR-006` — **nợ kỹ thuật số 2** ở [`000-Index.md`](../../../000-Index.md).

### Phần dưới đây là trạng thái GIỮA CHỪNG, giữ làm hồ sơ — ⛔ đã lạc hậu

| Tầng | Trạng thái |
|---|---|
| `docs/030-Specs/Architecture/` | ✅ **ĐÓNG BĂNG** — 1 SDD + 18 ADR. 0 trích dẫn `SRS L{n}`, header traceability thống nhất |
| `docs/020-Requirements/SRS-Comic-Studio.md` | ✅ Đã thêm 7 hàng `b-1…b-7` vào §5.2, `updated: 2026-08-29` |
| `docs/030-Specs/Schema/` | 🟡 **13/14 file viết xong, 12 ĐẠT** — `DB-Entity-Provenance-And-Usage.md` chưa đạt, xem **E19 (CRITICAL)** — xong `Narrative-Timeline`, `Story-Bible`, `Comic-IR`, `Dialogue-And-Gate`, `Typeset-Layer`, `Generation`, `Prompt-Vocabulary`, `Job-Queue`, `Quality-Assets`, `Credit-Ledger` |
| `docs/030-Specs/API/` | ⛔ chưa bắt đầu (21 file) |
| `docs/030-Specs/Security/` | ⛔ chưa bắt đầu (3 file) |
| `docs/999-Resources/Glossary.md` | ⛔ chưa bắt đầu (delta 18 headword) |
| MOC + `000-Index` + ripple | ⛔ chưa bắt đầu (close-step, PM giữ) |

**Lô đang chạy lúc dừng**: **L10** — `DB-Entity-Tenancy.md`, `DB-Entity-Provenance-And-Usage.md`, `DB-Entity-Compliance-And-Takedown.md`.
⚠️ Nó **có thể đã ghi xong file** dù PM chưa nhận Worker Contract. **Việc đầu tiên khi resume**: `ls docs/030-Specs/Schema/` và kiểm 3 file đó, rồi mới tick `outline.md`.
⚠️ Bằng chứng gián tiếp cho thấy L10 đã đóng `TBD-USAGE-VLM` và hợp đồng `CO-1.1…CO-1.3` (lô L9 đọc được giữa chừng) — nhưng ⛔ **phải tự verify**, không tin gián tiếp.

> ✅ **E19 ĐÃ ĐÓNG** bằng [E20](./escalations.md) — PM chọn **hướng (ii) biến thể**: chi phí VLM-select tách sang **bảng riêng ở schema `generation`**, `public.usage_event` trở lại đồng nhất *"một dòng = một candidate"* ⇒ `COUNT(*)` trần = 3.
> ⭐ Lời giải này đúng dưới **cả hai** cách đọc AC ⇒ ⛔ không cần Product Owner phân xử, ⛔ không chạm `SDD`/`ADR` đã đóng băng, ⛔ không chạm closed-list `G-2` của `ADR-005`.
> **Lô thi hành**: **L27**.

## 2. Thứ tự các lô còn lại

| Wave | Lô | Nội dung | Trạng thái |
|:--:|---|---|---|
| **A** | **L27** | Thi hành [E20](./escalations.md): bảng chi phí VLM riêng ở schema `generation` · bỏ `event_kind` khỏi `usage_event` · câu đo AC bỏ mệnh đề lọc · `usage_daily` đổi bảng nguồn · dọn nốt enum của `E15` | 🟡 đang chạy |
| **A** | **L26** | `DB-Entity-Preview-And-Export.md` — file thứ 14, 2 entity bị sót ([E16](./escalations.md)); **sở hữu và phải đóng `SDD-HG-01.4`** | 🟡 đang chạy |
| **A** | **L18** | `Spec-Security-Threat-Model.md` + `Spec-Security-Tenant-Isolation.md` | 🟡 đang chạy |
| **A** | **L19** | `Spec-Security-Legal-Compliance.md` | 🟡 đang chạy |
| **B** | **L25** | Chuẩn hoá tầng Schema: `enum` → `text`+`CHECK` · `id:` frontmatter → `DB-{TÊN-CỤM}` · áp `CO-1` phương án (a) với `generation_kind` dạng `text`+`CHECK` | ⛔ **chạy MỘT MÌNH**, sau wave A |
| **C** | L12–L15 | 14 file `Endpoint-*` | sau L25 |
| **C** | L16–L17 | 7 file `Spec-Integration-*` | sau L25 |
| **C** | L20 | Glossary delta 18 headword, **append-only** | độc lập, chạy kèm được |
| **D** | L21–L22 | Verify: `context-auditor` ∥ `quality-assurance` | sau tất cả |
| **E** | close-step | `Specs-MOC.md` (viết mới) · `000-Index.md` §030 + Nợ kỹ thuật · `Requirements-MOC.md` ripple · `cost.md` | PM giữ |

> ⚠️ **Vì sao wave A an toàn**: 4 lô ghi vào **4 tập file rời nhau**. Hai lô Security bị cấm tường minh trích `DB-Entity-Provenance-And-Usage.md` (L27 đang sửa) — neo về `ADR-017`/`ADR-018` theo mã. Đây là cách tránh lặp lại [bài học #1](#4-ba-bài-học-của-pm-phải-đưa-vào-pm-coremd).

## 3. Ràng buộc PHẢI mang vào mọi dispatch còn lại

1. ⛔ **KHÔNG copy số dòng `SRS L{n}` từ `findings/`** — neo bằng mã `SRS-FR-*`/`SRS-NFR-*`. Tầng Architecture đã mất **7 lô** để dọn đúng lỗi này.
2. ⚠️ **`findings` mâu thuẫn `SDD`/`ADR` ⇒ theo `SDD`/`ADR`.** findings là enumerate *trước khi quyết*.
3. ⛔ **KHÔNG wiki-link `[[...]]`** — RULE-001 quy tắc #5 (override phần văn bản của `pm-doc.md`).
4. ⛔ **CHỈ dùng `Edit`/`Write`. KHÔNG `sed`/`python3`/`node`/`awk`/heredoc sửa file.**
5. ⚠️ **`KC-4` trỏ `ADR-017` theo mã `Q4.x`, ⛔ không copy nội dung.**
6. ⚠️ Bảng `job` là **`public.job`**. Bảng platform ở schema **`public`** (`ADR-005`).
7. ⚠️ Tầng Schema dùng **`text` + `CHECK`**, ⛔ không Postgres enum type.
8. ⚠️ Ràng buộc xuyên-endpoint (không bypass 2 human gate) là **`SDD-HG-01`** ở `SDD` §6.3 — 14 file API **trỏ theo mã điều khoản**, ⛔ không lặp lại.
9. ⚠️ `UC-06` bước 4 dùng **rate limit per tenant cho generate** (đếm request, ⛔ không đếm tiền) — xem [E9](./escalations.md) 6 điều diễn giải. ⛔ Không HOLD credit ở MVP1–MVP2.
10. ⚠️ ⛔ **`SRS-NFR-15`**: không thiết kế copyright/similarity detection — nó **tự phá miễn trừ Điều 198b**.
11. Mọi deliverable `status: draft`. Ngân sách **60 tool call**/lô.
12. ⚠️ **Hai dạng header traceability ở tầng Architecture là CÓ CHỦ Ý** ([E13](./escalations.md)) — ⛔ lô verify không được báo là lỗi.
13. ⚠️ `visual_vocabulary` **không có `tenant_id`** là ngoại lệ có lập luận ([E18](./escalations.md)) — CI phải **whitelist đúng bảng đó kèm comment**, ⛔ không nới test.

## 4. Ba bài học của PM, phải đưa vào `pm-core.md`

1. ⛔ **Không dispatch lô SỬA nguồn-sự-thật song song với lô ĐỌC nguồn đó.** Ở run này L0 (sửa `SRS`) chạy cùng L1/L2 (đọc `SRS`) ⇒ **ba hệ toạ độ số dòng**, tốn **7 lô** dọn dẹp.
2. ⛔ **PM chỉ được viết một khẳng định về nội dung file vào run-state SAU khi đã `grep`/`Read` chính file đó.** Mô tả của worker là đầu vào cần kiểm chứng, không phải nguồn. Vi phạm 3 lần: [E9](./escalations.md), [E12](./escalations.md), [E15](./escalations.md).
3. ⛔ **Khi nhận bảng "N mục → M nhóm" từ lens, PM phải chạy một phép diff cơ học trước khi đưa vào `outline.md`.** Fan-out **không tự bắt được mục bị bỏ sót** — mỗi worker chỉ thấy phần của mình, entity không thuộc lô nào thì không ai báo thiếu. Xem [E16](./escalations.md): 2 entity `[24⭐]` suýt mất schema.

## 5. Việc ngoài lane doc, cần anh quyết

- **`.claude/commands/pm-core.md` đã bị xoá** ở commit `90a990f`, trong khi `pm-code.md`, `pm-doc.md` và `pm-runs/README.md` đều còn tham chiếu nó như dependency bắt buộc. Run này nạp lại bằng `git show 90a990f^:.claude/commands/pm-core.md`. Đề xuất khôi phục như một việc riêng.
- **`docs/030-Specs/**` đang untracked trong git.** Việc commit nằm ngoài phạm vi lane doc.
