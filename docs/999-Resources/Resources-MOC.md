---
id: MOC-999
type: moc
status: live
project: TNMCORE-OS
created: 2026-02-26
---

# 📂 999-Resources Map of Content (MOC)

Chào mừng tới danh mục Tài Nguyên của dự án. Đây là nơi chứa các mẫu, bảng thuật ngữ và ghi chép cuộc họp.

## 📋 Mục lục (Table of Contents)
1. [Templates (Bản mẫu)](#templates-bản-mẫu)
2. [Glossary (Thuật ngữ)](#glossary-thuật-ngữ)
3. [Meeting Notes (Ghi chép cuộc họp)](#meeting-notes-ghi-chép-cuộc-họp)

---

## 📂 Templates (Bản mẫu)

*Các mẫu chuẩn nhằm đảm bảo tính nhất quán cho tài liệu dự án.* **13 mẫu hiện có:**

| Mẫu | Dùng cho | Tình trạng |
|---|---|---|
| [Template-Analysis](./Templates/Template-Analysis.md) | Tài liệu phân tích | ⚠️ **stub** — chỉ có frontmatter, chưa dùng được làm khuôn |
| [Template-Component](./Templates/Template-Component.md) | Design System component | |
| [Template-Incident-Report](./Templates/Template-Incident-Report.md) | Sự cố vận hành | |
| [Template-PRD](./Templates/Template-PRD.md) | Product Requirements Document | |
| [Template-Project-Charter](./Templates/Template-Project-Charter.md) | Project Charter | ⚠️ **không có bảng RACI** — xem [Charter-Comic-Studio](../010-Planning/Charter-Comic-Studio.md) để lấy bảng RACI đã được định nghĩa |
| [Template-Release-Notes](./Templates/Template-Release-Notes.md) | Release notes | |
| [Template-Risk-Register](./Templates/Template-Risk-Register.md) | Risk Register | ⚠️ mục *Risk Matrix Overview* để trống, **không định nghĩa công thức `Score`** — công thức `Score = P × I` (thang 1–3) được thiết lập tại [Risk-Register](../010-Planning/Risk-Register.md) §1 |
| [Template-SDD](./Templates/Template-SDD.md) | System Design Document | |
| [Template-Spec](./Templates/Template-Spec.md) | Technical Spec | |
| [Template-SRS](./Templates/Template-SRS.md) | Software Requirements Spec | |
| [Template-Status-Report](./Templates/Template-Status-Report.md) | Báo cáo tiến độ | |
| [Template-Test-Plan](./Templates/Template-Test-Plan.md) | Master Test Plan | |
| [Template-WBS-ETA](./Templates/Template-WBS-ETA.md) | WBS / ETA | |

> ⚠️ **`Template-Daily-Report.md` KHÔNG tồn tại** dù MOC này từng trỏ tới nó. Ghi nhận thay vì xoá — theo guardrail *"không xoá tài liệu, lý do tài liệu cũ sai cũng là dữ liệu"*. Tạo mẫu đó hoặc gỡ tham chiếu là việc của một run dọn dẹp riêng.

## 📂 Glossary (Thuật ngữ)
- [Glossary](./Glossary.md) — 40 thuật ngữ, 7 nhóm: xác thực & bảo mật · kiến trúc pipeline · mô hình dữ liệu & thời gian · sinh ảnh & kiểm tra nhất quán · chữ & trình bày · quy trình & vận hành · SaaS & multi-tenancy.

## 📂 Request (Concept gốc)
- [Request.md](./Request.md) — concept gốc 894 dòng của `comic-studio`, kiến trúc 18 mục. Là **input** của [Analysis-Comic-Studio-Concept](../050-Research/Analysis-Comic-Studio-Concept.md), không phải kết luận.
  > ⚠️ File này **thiếu hoàn toàn YAML frontmatter**, vi phạm RULE-001 quy tắc #3. Đã ghi nhận là nợ kỹ thuật.

## 📂 Meeting Notes (Ghi chép cuộc họp)
[Mục Meeting Notes](./Meeting-Notes/) — *(chưa có tài liệu)*

---
## 📚 Tài liệu tham khảo
- [Documentation Master Index](../000-Index.md)
- [Documentation Structure Rule](../../knowledge-base/99-Templates/Documents-Template.md)
