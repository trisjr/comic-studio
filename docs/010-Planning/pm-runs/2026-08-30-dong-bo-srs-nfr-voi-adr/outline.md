---
id: OUTLINE-2026-08-30-DONG-BO-SRS-NFR-VOI-ADR
type: doc-plan
run: 2026-08-30-dong-bo-srs-nfr-voi-adr
status: in-progress
created: 2026-08-30
---

# Doc Plan — Đồng bộ `SRS` (020) ↔ `ADR` (030)

> [!IMPORTANT]
> ⛔ **File này do PM độc quyền chỉnh sửa.** Writer báo xong trong `SUMMARY`, PM tick.

## Mục lục

- [Quyết định tại gate](#quyết-định-tại-gate)
- [Bảng hạng mục](#bảng-hạng-mục)
- [Ràng buộc CỨNG — áp cho mọi writer](#ràng-buộc-cứng--áp-cho-mọi-writer)
- [Lô 1 — SRS](#lô-1--srs-comic-studiomd)
- [Lô 2a — Security · API · Schema · Integration](#lô-2a--security--api--schema--integration)
- [Lô 2b — Architecture](#lô-2b--architecture)
- [Lô 3 — Close-step (PM)](#lô-3--close-step-pm)
- [Ripple](#ripple)

## Quyết định tại gate

| Mã | Quyết định của Founder |
|---|---|
| `G-1` | **Đồng bộ cả ba** `SRS-NFR-07` + `SRS-NFR-08` + `SRS-NFR-09` — theo **Phương án 3** của [findings §2.1](./findings/architect.md), quy tắc *"xếp theo thành phần yếu nhất"* |
| `G-2` | **Sửa `SRS:15`** — bỏ lệnh tự cấm, cho phép SRS link vào 030 ở những hàng đã đóng |
| `G-3` | **Chuyển `ADR-001…004` sang `status: accepted`** cùng lô |
| `G-4` | **Commit `ADR-001`** nguyên trạng bản Founder sửa ✅ **ĐÃ XONG** — commit `f77b922`, 1 file / +2 −1 |

## Bảng hạng mục

| # | Tài liệu | Loại | Điểm sửa | Writer | Xong |
|:--:|---|---|:--:|---|:--:|
| 1 | `docs/020-Requirements/SRS-Comic-Studio.md` | srs | **19** + frontmatter | `business-analyst` | ✅ **21** (+`:39`, `:72`) |
| 2a | `Spec-Security-Threat-Model.md` · `Endpoint-Preview-Export.md` · `DB-Entity-Tenancy.md` · `Spec-Integration-Auth-Provider.md` | spec | **7** | `security-auditor` | ✅ **7/7** |
| 2b | `SDD-Comic-Studio.md` · `ADR-001`…`ADR-004` · `ADR-006` · `ADR-010` · `ADR-015` | sdd/adr | **9** + 4 frontmatter | `architect` | ✅ **9/9** |
| 3 | `Specs-MOC.md` · `000-Index.md` · `escalations.md` + ⚠️ `ADR-002:85` · `ADR-006:270` | moc/index | **8** | ⭐ **PM** | ✅ |
| 4 | Verify toàn lô — **2 pass** | — | — | `context-auditor` ×2 | ✅ **0 CRITICAL** |

**Lịch chạy**: Lô 1 **chạy một mình trước** → Lô 2a ‖ 2b song song → Lô 3 (PM) → Lô 4 (verify).

> [!WARNING]
> ⭐ **Vì sao Lô 1 KHÔNG chạy song song với Lô 2**: `SDD-Comic-Studio.md:457` **trích nguyên văn** hàng `b-7` của `SRS §5.2`. Câu chữ cuối của nó phụ thuộc bản `SRS` đã land. Chạy song song ⇒ hai hệ toạ độ ⇒ đúng lỗi đã làm run `2026-08-28` tốn **43,8%** ngân sách cho dọn dẹp + rework.

## Ràng buộc CỨNG — áp cho mọi writer

| # | Ràng buộc |
|:--:|---|
| **K-1** | ⛔ **ĐẾM LẠI TẠI NGUỒN.** Mọi con số phải được suy ra bằng `grep` trên **bảng thật**, ⛔ **không** copy số từ `findings/architect.md`. Findings là **bản đồ, ⛔ không phải nguồn**. Dự án này đã mắc lỗi trích lại số từ nguồn thứ cấp **hai lần** (`E9`, `E10` run trước) |
| **K-2** | ⛔ **KHÔNG sửa hai con số đang ĐÚNG**: `55` (`SRS:345`, CHỐT thuần — ⛔ không hàng nào thành CHỐT thuần) và `21` (`SRS:437` — cả 5 hàng `b-*` chỉ đổi *mệnh đề lý do*, ⛔ **không** đổi trạng thái `TBD`) |
| **K-3** | ⛔ **KHÔNG đóng hộ `TBD` có chủ đích**: (a) **vendor billing** (`ADR-003:71-79` — chặn bởi quốc gia pháp nhân bán hàng) ⇒ `SRS-NFR-08` ⛔ **không được** ghi MẶC ĐỊNH thuần; (b) **`C-10` cơ chế render an toàn** — **vẫn MỞ**, chỉ viết lại **lý do** |
| **K-4** | ⛔ **KHÔNG chạm `ADR-001:15`, `:69`, `:172`** *(toạ độ lúc lập plan; sau khi run chèn `updated:` vào dòng 7 thì là `:16`, `:70`, `:173` — xem `E1`)*. `## Context` là ảnh chụp **trước** quyết định; bảng *"cố ý để mở"* ghi **trạng thái ĐẦU VÀO**; dòng thứ ba là **dòng chịu lực** chứng minh `b-6`/`b-7` ⛔ không được đóng theo |
| **K-5** | **Bump `updated: 2026-08-30`** ở frontmatter **MỌI** file chạm vào — kể cả file tầng 030 chỉ sửa một dòng |
| **K-6** | RULE-001: link markdown chuẩn `[Text](./path.md)`. ⛔ **CẤM wiki-link `[[...]]`** |
| **K-7** | ⛔ **KHÔNG chạm** `*-MOC.md` và `000-Index.md` — PM giữ |
| **K-8** | ⛔ **Không bịa.** Mọi phát biểu phải truy được về `file:line` trong repo. Không nguồn ⇒ ghi `TBD` + báo `PARTIAL` |

## Lô 1 — `SRS-Comic-Studio.md`

- **Độc giả đích**: người đọc SRS để biết **cái gì đã quyết, cái gì chưa** — và với mỗi cái đã quyết thì **cứng tới mức nào**.
- **Nguồn sự thật**: [`findings/architect.md` §2](./findings/architect.md) (bảng A1–A9, B1–B10, và §2.1 phép tính) · `ADR-001`…`ADR-004` trong repo.
- **Tiêu chí xong** (đo được):
  - `grep -c 'CHƯA QUYẾT.*TBD' ` ở `:256`, `:257`, `:258` → cả ba hàng mang nhãn mới, ⛔ không còn `CHƯA QUYẾT` thuần
  - `SRS:345` khớp **tổng 68** và giữ nguyên `55`
  - `SRS:58` + `:60` khớp nhau về **số** và **danh sách mã**
  - `grep -c '\[.*\](\.\./030-Specs' SRS…` > 0 (hệ quả của `G-2`)
  - `updated: 2026-08-30`

| Mã | Điểm | Việc |
|:--:|---|---|
| `A8` | `:15` | ⭐ **Làm TRƯỚC** — bỏ lệnh tự cấm link (`G-2`). ⛔ Không làm bước này thì A1/A2 tạo mâu thuẫn nội tại mới |
| `A1` | `:149` | Bảng §2.3 — điền stack đã quyết + link `ADR-001` |
| `A2` | `:258` | ⭐ Hàng chi tiết `SRS-NFR-09` → nhãn **LAI**, ghi đủ 3 tầng CHỐT/MẶC ĐỊNH/`TBD` |
| `A3` | `:460` (`b-6`) | Giữ `TBD`, **đổi lý do** — `ADR-001:69` tuyên bố ⛔ không đóng hàng này |
| `A4` | `:461` (`b-7`) | Giữ `TBD`, **đổi lý do** — `ADR-001:69` + `ADR-002:84` |
| `A5` | `:345` | ⭐ Câu đếm → Phương án 3. **`55` giữ nguyên** (`K-2`) |
| `A6` | `:58`, `:60` | *"Năm hàng LAI"* → *"**Tám** hàng LAI"*, thêm `NFR-07/08/09` |
| `A7` | `:95` | Đổi thì tương lai *"sẽ được đặc tả"* → *"đã được đặc tả"* |
| `A9` | `:7` | `updated: 2026-08-30` |
| `B1` `B2` | `:148`, `:256` | `SRS-NFR-07` → **LAI nghiêng MẶC ĐỊNH** + ⚠️ reopen trigger data-residency |
| `B3` | `:257` | ⭐ `SRS-NFR-08` → **LAI**, ⛔ **vendor billing VẪN `TBD`** (`K-3`) |
| `B4` | `:263` | *"Ba hàng `TBD`"* → đã đóng ở 030, phần còn `TBD` thật là billing |
| `B5` `B6` `B7` | `:375`, `:385`, `:386` | §4.2 · §4.3 — Render/Singapore · Clerk (chưa mua) · R2 (chưa mua) |
| `B8` `B9` `B10` | `:455`, `:456`, `:459` | Ba hàng `b-1`/`b-2`/`b-5` — giữ `TBD`, **đổi lý do** |

## Lô 2a — Security · API · Schema · Integration

- **Nguồn sự thật**: [`findings/architect.md` §3.1, §3.2 (R1–R4), §3.3 (R13–R15)](./findings/architect.md) · bản `SRS` đã land ở Lô 1.
- **Tiêu chí xong**: `grep -rn 'SRS-NFR-09.*TBD'` trên 4 file → **0 kết quả**; `C-10` vẫn hiện diện như hạng mục **MỞ**.

| Mã | `file:line` | Việc |
|:--:|---|---|
| `R1` | `Spec-Security-Threat-Model.md:292` | ⭐ Đổi lý do `C-10`: ⛔ **không phải** vì `SRS-NFR-09`, mà vì `ADR-001:66` để mở *thư viện compositor + sinh PDF* và `:68` để mở *`worker_threads` hay tách job* |
| `R2` | `Spec-Security-Threat-Model.md:521` | Như `R1`. **Chủ sở hữu + mốc**: tách đôi — **Architect sở hữu TẬP RÀNG BUỘC** (đã CHỐT) · **Dev sở hữu việc CHỌN thư viện** tại **spike MVP0**, `C-10` thành **tiêu chí nghiệm thu của spike** |
| `R3` | `Endpoint-Preview-Export.md:200` | Như `R1` |
| `R4` | `Endpoint-Preview-Export.md:249` | Như `R2`. Mốc **Phase 4** → **MVP0 (spike)** |
| `R13` | `DB-Entity-Tenancy.md:95` | Vendor auth → **MẶC ĐỊNH (Clerk), chưa mua**. ⭐ Kết luận ⛔ **không đổi** — vẫn ⛔ không thêm cột `email` |
| `R14` | `DB-Entity-Tenancy.md:312` | *"Khi chốt vendor"* → *"Khi spike Clerk đạt/trượt 3 tiêu chí — kickoff MVP1"* (`ADR-003:69`) |
| `R15` | `Spec-Integration-Auth-Provider.md:189` | `SRS-NFR-08` (vendor auth = MẶC ĐỊNH, billing `TBD`) |

## Lô 2b — Architecture

- **Nguồn sự thật**: [`findings/architect.md` §3.2 (R5–R6), §3.3 (R10–R12), §3.4](./findings/architect.md) · bản `SRS` đã land.
- **Tiêu chí xong**: 4 ADR `status: accepted`; `SDD:811` khớp `SRS:58`/`:60` về số và danh sách mã.

| Mã | `file:line` | Việc |
|:--:|---|---|
| `G-3` | `ADR-001:4` `ADR-002:4` `ADR-003:4` `ADR-004:4` | `status: draft` → `status: accepted` + bump `updated` |
| `R17` | `ADR-010:176` | ⭐ **Ripple của `G-3`** — *"Khi `ADR-003` chuyển khỏi `draft` — trước MVP1"*: mốc **đã đến**. Viết lại cho đúng hiện trạng |
| `R6` | `SDD-Comic-Studio.md:457` | Trích dẫn `SRS §5.2` hàng `b-7` — **đồng bộ theo bản `SRS` đã land** (`A4`). ⛔ Nửa sau (*"cả `ADR-001` lẫn `ADR-002` đều tuyên bố không đóng"*) **đang ĐÚNG**, giữ nguyên |
| `R⭐` | `SDD-Comic-Studio.md:811` | ⭐⭐ **RIPPLE NGUY HIỂM NHẤT** — hard-code *"**năm hàng LAI**"* + đủ 5 mã. Phải khớp `SRS:58`/`:60`. **Đếm lại tại nguồn** (`K-1`) |
| `R10` | `ADR-006:256` | Vendor auth = MẶC ĐỊNH (Clerk) theo `ADR-003`; ⛔ billing vẫn `TBD` |
| `R11` | `ADR-006:258` | Hosting → `ADR-002` chọn Render (MẶC ĐỊNH). ⭐ Kết luận *"không bị chặn"* **giữ nguyên** |
| `R12` | `ADR-015:272` | Trần chịu tải → *"sau khi có số đo thật trên platform đã chọn"*. ⭐ Kết luận ⛔ **không đổi** — trần tải vẫn chưa đo |
| `R5` | `SDD-Comic-Studio.md:62` | ⛔ **KHÔNG SỬA** — chỉ neo `R-6`, ⛔ không khẳng định `TBD`. Sau đồng bộ nó **đúng hơn trước** |

## Lô 3 — Close-step (PM)

| # | File | Việc | Nguồn |
|:--:|---|---|---|
| 1 | `Specs-MOC.md:13` | ⭐ *"57 tài liệu… **toàn bộ** `status: draft`"* → sai sau `G-3`. Đếm lại tại nguồn ⇒ **53 `draft` + 4 `accepted`** | plan |
| 2 | `Specs-MOC.md` frontmatter | Thêm `updated: 2026-08-30` (file trước đó ⛔ không có trường này) | `K-5` |
| 3 | `000-Index.md:96` | Cùng lỗi như hàng 1 | plan |
| 4 | `000-Index.md:220` | ⭐ **Đóng hàng nợ số 5** — chính là hạng mục lô này đi dọn | plan |
| 5 | `000-Index.md:178` | Hàng run-state mới | plan |
| 6 | `escalations.md` | ⭐ Ghi rào chắn `E1`: *"`ADR-001:16`/`:173`/`:70` mô tả **trạng thái ĐẦU VÀO** — lô sau ⛔ không được báo là lỗi"* (đúng mô hình `escalations.md:184` run `2026-08-28`); mở rộng phủ 6 chỗ ở `ADR-002/003/004` | plan + `S-2` |
| 7 | ⚠️ `ADR-002:85` | Lệch **do chính lô này tạo ra**: sau khi `A4` viết lại `b-7`, hàng đó ⛔ không còn neo `SRS-NFR-07`, nhưng `ADR-002:85` vẫn khẳng định cả ba `b-1`/`b-5`/`b-7` phụ thuộc nó | Lô 2b `RECOMMEND` #1 |
| 8 | ⚠️ `ADR-006:270` | Sót `TBD` cũ, tự mâu thuẫn với `:257` **cách 13 dòng** — ⛔ không nằm trong bảng Ripple nên ⛔ không ai kiểm | verify pass 1 `W-3` |

> [!WARNING]
> ⭐ **Hàng 7 và 8 ⛔ KHÔNG có trong plan ban đầu.** Cả hai là **lệch do chính run này sinh ra** — bằng chứng rằng một lô đồng bộ có thể tự đẻ lệch mới, và rằng bảng *Ripple* lập tại gate ⛔ **không đủ** để phủ hết.

## Ripple

| Tài liệu đang trích phạm vi này | Xử lý |
|---|---|
| `SDD-Comic-Studio.md:457`, `:811` | Lô 2b — ⛔ **không** để rời khỏi lô SRS |
| `ADR-010:176` | Lô 2b — ripple của `G-3` |
| `Specs-MOC.md:12` · `000-Index.md:96` | Lô 3 — PM (ripple của `G-3`) |
| `Spec-Security-Threat-Model.md:85` · `DB-Entity-Generation.md:486` · `SDD:724`, `:777` · `Spec-Integration-Billing-Provider.md:65` · `Spec-Integration-Object-Storage.md:128` · `Spec-Integration-Auth-Provider.md:92` | ⛔ **KHÔNG sửa** — đã kiểm, **đang đúng** |

---

_Created by TNMCORE-OS (PM)_
_Author: trisjr_
