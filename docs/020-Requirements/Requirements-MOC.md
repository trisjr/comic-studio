---
id: MOC-020
type: moc
status: live
created: 2026-02-04
updated: 2026-08-24
author: TNMCORE-OS (BA Role)
---

# 📂 020-Requirements Map of Content

Trung tâm quản lý Yêu cầu của dự án `comic-studio`. Tầng này trả lời **"sản phẩm phải làm gì"** (What) và **"tại sao"** (Why). Nó **không** trả lời *"làm thế nào"* — đó là tầng [030-Specs](../030-Specs/Specs-MOC.md), hiện chưa khởi tạo.

> **Trục phân rã của cả tầng: 8 module `A–H`**, lấy nguyên từ [MVP-Scope §3](../010-Planning/MVP-Scope.md). Quan hệ **1 module ↔ 1 BRD ↔ 1 Epic** là 1:1:1 — đây là lý do trục module được chọn thay vì trục mốc MVP: nó giữ traceability ở dạng **một link**, không phải một ma trận.

## 📍 Định Hướng (Navigation)

### 📦 020.20 — Product Requirements (PRD)

_Yêu cầu sản phẩm toàn cảnh, tổng hợp cả 8 module._

| Tài liệu | Nội dung |
|---|---|
| [PRD-Comic-Studio](./PRD-Comic-Studio.md) | **Điểm vào của cả tầng.** Yêu cầu chức năng theo 8 module A–H, ranh giới scope, success metrics. ⚠️ Mục *Người dùng & vấn đề* mở bằng `TBD` có cấu trúc — repo **không có persona/JTBD**, cần user interview. |

> ⚠️ **Link chết đã gỡ**: MOC này từng trỏ tới `PRD-TNMCORE-OS.md` — một file **chưa bao giờ tồn tại**, kế thừa từ repo template. Nó được thay bằng PRD thật ở trên, không phải xoá suông.

### 🏢 020.10 — Business Requirements (BRD)

_Một BRD cho mỗi module. Trả lời: "module này có đáng làm ở mốc này không"._

| # | Tài liệu | Module `MVP-Scope §3` |
|---|---|---|
| 001 | [BRD-001-Image-Generation-Pipeline](./BRD/BRD-001-Image-Generation-Pipeline.md) | A · Pipeline sinh ảnh |
| 002 | [BRD-002-Story-Intelligence](./BRD/BRD-002-Story-Intelligence.md) | B · Story Intelligence |
| 003 | [BRD-003-Comic-Director-And-Layout](./BRD/BRD-003-Comic-Director-And-Layout.md) | C · Comic Director & Layout |
| 004 | [BRD-004-Minimum-Editor](./BRD/BRD-004-Minimum-Editor.md) | D · Editor & UI |
| 005 | [BRD-005-Multi-Tenancy-And-Platform](./BRD/BRD-005-Multi-Tenancy-And-Platform.md) | E · Multi-tenancy & hạ tầng |
| 006 | [BRD-006-Credit-And-Unit-Economics](./BRD/BRD-006-Credit-And-Unit-Economics.md) | F · Kinh tế & credit |
| 007 | [BRD-007-Legal-And-Compliance](./BRD/BRD-007-Legal-And-Compliance.md) | G · Pháp lý & compliance |
| 008 | [BRD-008-Quality-And-Operations](./BRD/BRD-008-Quality-And-Operations.md) | H · Chất lượng & vận hành |

> ⚠️ **Nhóm `H` gần như bị đánh rơi khỏi tầng này.** PM chấm triage khi chỉ đọc phần đầu bảng `MVP-Scope §3` và kết luận có 7 module. Nhóm `H` chứa bốn hàng chịu lực — **H1** HITL gate + eval kit (chính là điều kiện khả thi **R9** của Charter §4), **H2** log preference data (*"moat thật"*), **H4** export (*"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"*), **H6** golden dataset (`✅` ở **mọi** mốc). Chi tiết: `pm-runs/2026-08-24-.../brief.md` assumption #3.

### 🔧 020.20 — Software Requirements (SRS)

| Tài liệu | Nội dung |
|---|---|
| [SRS-Comic-Studio](./SRS-Comic-Studio.md) | Yêu cầu kỹ thuật, tổ chức theo 8 module. Mỗi hàng requirement mang **nhãn độ cứng** `CHỐT` / `MẶC ĐỊNH` / `CHƯA QUYẾT` / `LAI`. Có mục **negative requirements** — những gì đã bị **cắt hẳn**, viết ra tường minh vì *"im lặng sẽ bị đọc là chưa quyết"*. |

### 👤 020.30 — Use Cases

_11 kịch bản sử dụng: Actor, Main flow, Alternative flow, Exception flow._

| Tài liệu | | Tài liệu |
|---|---|---|
| [UC-01-Upload-And-Ingest-Chapter](./Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) | | [UC-07-Edit-Bubble-And-Dialogue-In-Panel](./Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) |
| [UC-02-Review-And-Edit-Story-Bible](./Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | | [UC-08-Arrange-Page-And-Preview](./Use-Cases/UC-08-Arrange-Page-And-Preview.md) |
| [UC-03-Review-Panel-Script](./Use-Cases/UC-03-Review-Panel-Script.md) | | [UC-09-Export-Chapter](./Use-Cases/UC-09-Export-Chapter.md) |
| [UC-04-Human-Gate-Speaker-Attribution](./Use-Cases/UC-04-Human-Gate-Speaker-Attribution.md) | | [UC-10-Manage-Credit-And-BYOK](./Use-Cases/UC-10-Manage-Credit-And-BYOK.md) |
| [UC-05-Human-Gate-Dialogue-Condensation](./Use-Cases/UC-05-Human-Gate-Dialogue-Condensation.md) | | [UC-11-Handle-Takedown-Request](./Use-Cases/UC-11-Handle-Takedown-Request.md) |
| [UC-06-Generate-Panel-And-Pick-Variant](./Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | | |

> **Không Use Case nào có Exception flow rỗng** — 11/11. *"Rỗng là không đạt"* là tiêu chí cứng, vì một luồng chỉ có happy path thì không dùng được để viết test case.

### 🛡️ 020.40 — Non-Functional Requirements

Không có file riêng — NFR nằm trong [SRS](./SRS-Comic-Studio.md) mục *Other Non-functional Requirements*, gồm **17 NFR có số** (mỗi số kèm nhãn nguồn) và **14 NFR `TBD`** đặt riêng, **không** hàng nào bị gán số bịa.

---

## 📝 Quy ước bắt buộc của tầng này

1. **Mọi requirement phải truy được về một mục cụ thể** trong `MVP-Scope §3` / `Charter §4–5` / `Analysis-Comic-Studio-Concept` / `Roadmap §3`. Không có căn cứ ⇒ ghi `TBD` tường minh, **không suy diễn mới**.
2. **Số và nhãn nguồn là một cặp không tách rời**: `[OFF]` official · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/ngưỡng tự định nghĩa (**không phải số đo**) · `[CHỐT]` quyết định Founder tại gate. Con số nào có caveat thì **mang nguyên caveat**.
3. **Toàn bộ tầng đang `status: draft`** — không phải sơ suất. [Charter §9](../010-Planning/Charter-Comic-Studio.md) còn **ba điều kiện chặn cấp dự án chưa gỡ**, trong đó có tư vấn luật sư SHTT trước khi thương mại hoá. Chuyển `approved` là quyết định của Founder tại Go/No-Go.
4. **Không link tới `030-Specs/`** — tầng đó rỗng. Cần trỏ sang design thì viết văn bản thuần *"sẽ được đặc tả tại tầng 030-Specs"*.
5. Liên kết dùng **standard markdown relative link** — **KHÔNG** wiki-link `[[...]]` (RULE-001 quy tắc #5).

## 📝 Quy Trình Làm Việc (BA Workflow)

> ♻️ **Mục này được GIỮ LẠI từ bản MOC trước run `2026-08-24`.** Khi PM ghi lại toàn bộ file này ở close-step, mục đã bị **xoá im lặng** — verify L24 phát hiện và `grep` chứng minh nội dung không còn ở bất kỳ đâu trong repo. Đã khôi phục. Đây là vi phạm guardrail *"không xoá im lặng"* của chính PM, ghi lại vì **lý do tài liệu cũ sai cũng là dữ liệu** — và ở đây tài liệu cũ **không** sai.

Mọi tài liệu trong thư mục này tuân thủ quy trình kiểm soát chất lượng của BA:

1. **Elicitation** — thu thập yêu cầu thô, lưu vào `Meeting-Notes/` hoặc draft.
2. **Analysis** — phân tích và cấu trúc hoá → tạo PRD/BRD.
3. **Validation** — review với stakeholder → chuyển `status: approved`.
4. **Specification** — chuyển thành User Story tại [`022-User-Stories`](../022-User-Stories/Stories-MOC.md).

> **Luôn đảm bảo tính Nhất quán (Consistency) và Khả thi (Feasibility) với đội ngũ Technical.**

⚠️ **Quy trình này áp vào thực tế `comic-studio` với hai điều chỉnh, không phải nguyên khuôn:**
- **Bước 3 chưa từng chạy.** Đội là **1 người + AI assist** — không có stakeholder committee. `Validation` ở đây nghĩa là Founder ra quyết định tại một trong ba **gate Go/No-Go** của [MVP-Scope §7](../010-Planning/MVP-Scope.md). Đó cũng là lý do **cả 21 tài liệu của tầng này đang `status: draft`**, không phải sơ suất.
- **Bước 1 đã hoàn tất trước tầng này.** Yêu cầu thô không nằm trong `Meeting-Notes/` (thư mục rỗng) mà ở [Request.md](../999-Resources/Request.md) → [Analysis-Comic-Studio-Concept](../050-Research/Analysis-Comic-Studio-Concept.md) → tầng [010-Planning](../010-Planning/Planning-MOC.md). Tầng 020 bắt đầu từ **bước 2**.

## 📚 Tài liệu liên quan

- [User Stories MOC](../022-User-Stories/Stories-MOC.md) — 8 Epic + 41 Story + Backlog đã xếp ưu tiên, dẫn xuất từ tầng này
- [Planning MOC](../010-Planning/Planning-MOC.md) — nguồn sự thật của mọi requirement ở đây
- [Glossary](../999-Resources/Glossary.md) — Ubiquitous Language, 69 thuật ngữ
- [Documentation Master Index](../000-Index.md) · [RULE-001](../../knowledge-base/99-Templates/Documents-Template.md)
