---
id: MOC-040
type: moc
status: live
project: comic-studio
created: 2026-08-30
updated: 2026-08-30
---

# Design MOC — bản đồ tầng thiết kế (Phase 3)

> [!NOTE]
> **6 tài liệu** sinh ra ở **SDLC Phase 3 — Product Design**, run `2026-08-30`. Toàn bộ đang ở `status: draft`.
> Hồ sơ quyết định của run nằm ở [pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio](../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/escalations.md) — mọi mã `G-{n}` và `E{n}` trong các file design đều trỏ về đó.

> [!WARNING]
> **Phase 3 CHƯA đóng.** Run này cố ý chỉ làm **bộ nền** (Brand Guidelines + Design System). **Bốn** artifact còn lại của Phase 3 — **Wireframes**, **User Flow**, **UI Specs**, **Assets** — thuộc run sau. Xem [Còn thiếu gì](#còn-thiếu-gì-để-đóng-phase-3).

## Mục lục

- [Đọc theo thứ tự nào](#đọc-theo-thứ-tự-nào)
- [1. Design System — 6 file](#1-design-system--6-file)
- [Bốn quyết định của Founder tại gate](#bốn-quyết-định-của-founder-tại-gate)
- [Ba ràng buộc xuyên suốt — đọc trước khi sửa bất kỳ file nào](#ba-ràng-buộc-xuyên-suốt--đọc-trước-khi-sửa-bất-kỳ-file-nào)
- [Còn thiếu gì để đóng Phase 3](#còn-thiếu-gì-để-đóng-phase-3)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Đọc theo thứ tự nào

| Bạn là ai | Đọc gì trước |
|---|---|
| **AI assist sắp sinh code UI** | [Foundations](./Design-System/Foundations.md) trước tất cả — nó định nghĩa hợp đồng token mà 4 file kia tuân theo → rồi file tương ứng với việc đang làm |
| Người **implement compositor / typeset layer** | ⭐ [Typography](./Design-System/Typography.md) §*HAI HỆ FONT* — bỏ qua mục này là lỗi **chỉ lộ ra sau khi đã sinh ảnh và tốn tiền** |
| Người **dựng màn hình human gate** | [Components](./Design-System/Components.md) §*Ba pattern đặc thù* `P-1` → [SDD](../030-Specs/Architecture/SDD-Comic-Studio.md) §6.3 `SDD-HG-01` |
| Người viết **microcopy / nội dung hiển thị** | [Brand-Guidelines](./Design-System/Brand-Guidelines.md) §*Điều CẤM* — có những câu **không được phép nói**, vì lý do pháp lý chứ không phải thẩm mỹ |
| Người muốn biết **vì sao lại thế** | [run-plan.md §Gate](../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/run-plan.md) — bốn quyết định `G-1`…`G-4` |

---

## 1. Design System — 6 file

`docs/040-Design/Design-System/`

| # | Tài liệu | Quyết định gì |
|---|---|---|
| `DS-001` | [Brand-Guidelines](./Design-System/Brand-Guidelines.md) | Tone, hướng màu, audience có căn cứ. ⭐ Chứa mục **CẤM tuyệt đối** — mọi biểu đạt phán đoán bản quyền bị cấm vì `SRS-NFR-15` (nó **tự phá miễn trừ Điều 198b**). ⚠️ **Tên hiển thị vẫn `TBD`**, chủ: Founder |
| `DS-002` | [Foundations](./Design-System/Foundations.md) | ⭐ **Đọc trước tiên.** Hợp đồng phát biểu token (**CSS variable là NGUỒN, Tailwind THAM CHIẾU** — một chiều), kiến trúc primitive → semantic, chuẩn a11y, và **checklist 14 mục `grep`** dùng để nghiệm thu cơ học cả 5 file kia |
| `DS-003` | [Color-Tokens](./Design-System/Color-Tokens.md) | Palette + 17 cặp semantic nền/chữ, đủ 2 cột light/dark. **27 hàng audit contrast có số — cả 27 đều ĐẠT ngưỡng**; riêng **3 màu cố ý KHÔNG đạt 3:1** nằm ở một **bảng tách biệt**, kèm phạm vi hẹp được phép dùng. ⭐ §*BA MỨC* — dải màu của *từ chối* / *cảnh báo* / *thông tin* phải phân biệt được |
| `DS-004` | [Spacing-And-Layout](./Design-System/Spacing-And-Layout.md) | Thang spacing, radius, elevation, breakpoint, z-index đặt tên. ⭐ §*Ranh giới* — hệ này **KHÔNG quản hình học panel/bubble**; đó là hệ toạ độ **0–1** do [ADR-013](../030-Specs/Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) sở hữu |
| `DS-005` | ⭐ [Typography](./Design-System/Typography.md) | **HAI hệ font, token KHÔNG chung namespace**: font UI là CSS variable ở `apps/web`; font render vào ảnh là **tham số config của `apps/backend`**, phải **đơn trị**, ⛔ không fallback stack. Giá trị font render là `TBD` do `ADR-013` sở hữu — file này chỉ ghi **ràng buộc** |
| `DS-006` | [Components](./Design-System/Components.md) | 16 component không hoãn được (`C-01`…`C-16`) + ma trận state + ánh xạ shadcn/Radix + 3 pattern đặc thù. Chứa **mục CẤM 8 hàng** — những bề mặt UI **không được phép tồn tại** |

## Bốn quyết định của Founder tại gate

Ghi ở đây vì mọi file trên đều viện dẫn chúng. Nguồn: [run-plan.md §Gate](../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/run-plan.md).

| Mã | Quyết định | Vì sao |
|---|---|---|
| `G-1` | Brand **trung tính, accent lạnh** | Sản phẩm **luôn hiển thị artwork comic nhiều màu** trong editor/preview ⇒ UI màu mạnh **cạnh tranh với chính nội dung người dùng đang đánh giá** |
| `G-2` | **Light default**, token khai đủ cặp dark ngay | Preview trang comic có **nền trắng giấy**; chrome tối làm lệch cảm nhận. Khai sẵn cặp dark ⇒ ⛔ không retrofit |
| `G-3` | **WCAG 2.2 AA**, desktop-first | ⭐ Kéo theo **SC 2.5.7** — kéo bubble bắt buộc có **đường thao tác thay thế không-kéo** (`Components.md` `P-3`) |
| `G-4` | Brand-Guidelines map vào hàng `Design System` của RULE-001 | ⛔ Không sửa RULE-001. Brand là **tầng trên của cùng một token graph**, ⛔ không phải brand book độc lập |

## Ba ràng buộc xuyên suốt — đọc trước khi sửa bất kỳ file nào

1. ⭐ **Hai hệ font ⛔ KHÔNG được gộp.** Ngắt dòng tính theo font A + glyph vẽ bằng font B ⇒ dấu tiếng Việt bị mép bubble cắt. Nó **hỏng im lặng và vẫn chạy được**, chỉ lộ ra **sau khi ảnh đã sinh** — tức sau khi đã gọi image provider và tốn tiền; `D-29` cấm nướng chữ vào pixel nên ⛔ không có đường vá nhanh.
2. ⭐ **⛔ Không có component bulk approve.** `API-HG-6`: đường ghi `PASS` là **duy nhất**, ⛔ không batch. `SDD-HG-01.1` cấm mọi control **pre-selected**. Một nút *"Duyệt cả trang"* trông như tiện ích UX nhưng **phá một invariant kiến trúc**.
3. ⭐ **Có bề mặt bị CẤM và có bề mặt BẮT BUỘC.** Cấm mọi badge/messaging phán đoán bản quyền (`SRS-NFR-15`). Bắt buộc **AI-disclosure indicator** (`SRS-FR-40`, mức **CHỐT**) — bằng chứng tuân thủ là *một bề mặt UI*, ⛔ không để lại hàng dữ liệu nào, nên ⛔ không có Design System thì nghĩa vụ đó **không có nhà**.

## Còn thiếu gì để đóng Phase 3

`docs/040-Design/` còn ba thư mục **chưa có tài liệu**. Đây là phạm vi được cắt **tường minh** ở gate, ⛔ không phải sót.

| Thư mục | Artifact Phase 3 | Trạng thái |
|---|---|---|
| `Wireframes/` | `WF-{Screen}-{Device}.png` | ⏳ run sau |
| `Specs/` | User Flow `UF-{Feature}.md` · UI Spec `Proto-{Screen}.md` | ⏳ run sau |
| `Assets/` | Images, Icons, Illustrations | ⏳ run sau |

**Tiêu chí chuyển Phase**: đạt **1/4** — *"Design System có đủ Colors, Typography, Spacing"* ✅. Ba tiêu chí còn lại (Wireframe màn hình chính · User Flow phủ Main Flow · UI Specs đủ trạng thái) phụ thuộc run sau.

## Tài liệu tham khảo

- [Documentation Master Index](../000-Index.md)
- [RULE-001 — Quy tắc Cấu trúc Tài liệu](../../knowledge-base/99-Templates/Documents-Template.md)
- [Specs-MOC — tầng 030](../030-Specs/Specs-MOC.md) · [Requirements-MOC — tầng 020](../020-Requirements/Requirements-MOC.md)
- [Glossary](../999-Resources/Glossary.md)
- [Run-state của run này](../010-Planning/pm-runs/2026-08-30-brand-guidelines-va-design-system-comic-studio/brief.md)
