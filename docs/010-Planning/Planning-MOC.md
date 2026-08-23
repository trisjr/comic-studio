---
id: MOC-PLANNING
type: moc
status: draft
created: 2026-02-04
updated: 2026-08-23
---

# Planning Map of Content (MOC)

Tầng **010-Planning** chứa chiến lược, lịch trình và quản trị rủi ro của dự án `comic-studio`.

## Tài liệu nền tảng

Đọc theo thứ tự này — mỗi tài liệu giả định anh đã đọc tài liệu trước nó.

| # | Tài liệu | Nội dung | Trạng thái |
|---|---|---|---|
| 1 | [Charter-Comic-Studio](./Charter-Comic-Studio.md) | Mục tiêu, Business Case, phạm vi, **Stakeholder Matrix (RACI)**, ràng buộc, giả định. Tài liệu neo quyết định cấp dự án | `draft` |
| 2 | [MVP-Scope](./MVP-Scope.md) | Ranh giới **MVP vs Full Scope**, cái gì cắt và vì sao, danh sách **không được cắt**, ba gate **G0/G1/G2** Go/No-Go, và kill criteria | `draft` |
| 3 | [Roadmap](./Roadmap.md) | Lộ trình **09/2026 → 02/2027**. ⚠️ Kết luận: khung 6 tháng **không** chứa hết MVP0–MVP3 — MVP3 rơi ra ngoài | `draft` |
| 4 | [OKRs](./OKRs.md) | Q4/2026 (chu kỳ chính) + preview Q1/2027. ⚠️ Q4/2026 **cố ý không có KR doanh thu** — lý do nêu tại mục 3.0 | `draft` |
| 5 | [Risk-Register](./Risk-Register.md) | 23 rủi ro có Score + 10 khoảng trống không gán Score + rủi ro nền tảng + **rủi ro nhị phân** (ba câu hỏi luật sư SHTT) | `draft` |

> **Vì sao cả năm đều là `draft`, không phải `approved`.** Thẩm định ở [Analysis-Comic-Studio-Concept](../050-Research/Analysis-Comic-Studio-Concept.md) kết luận **ba việc phải làm trước dòng code đầu tiên**, trong đó có việc mang ba câu hỏi pháp lý tới luật sư SHTT Việt Nam. Một Charter `approved` khi các điều kiện chặn chưa được gỡ là tự tuyên bố sai. Chúng chuyển `approved` khi anh ra quyết định Go/No-Go, không phải khi chúng được viết xong.

## Thư mục con

| Thư mục | Nội dung | Trạng thái |
|---|---|---|
| [Sprints/](./Sprints/) | `Sprint-{NNN}.md`, `Retro-Sprint-{NNN}.md` | *(chưa có tài liệu)* |
| [Estimates/](./Estimates/) | WBS, ETA, Budget | *(chưa có tài liệu)* |
| [Implementation-Plans/](./Implementation-Plans/) | `Plan-{Feature}.md` | *(chưa có tài liệu)* |

## Run-state của PM

[pm-runs/](./pm-runs/README.md) — sổ tay điều phối của các slash command `/pm-code` và `/pm-doc`.

> ⚠️ **Không phải deliverable, và không được chuẩn hoá.** Đây là dấu vết quyết định tại thời điểm chạy; sửa nó là xoá mất lý do một quyết định đã được đưa ra.

| Run | Sinh ra gì |
|---|---|
| `2026-08-23-danh-gia-y-tuong-comic-studio` | [Analysis-Comic-Studio-Concept](../050-Research/Analysis-Comic-Studio-Concept.md) — thẩm định ý tưởng |
| `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio` | Toàn bộ 5 tài liệu ở bảng trên + [000-Index](../000-Index.md) + cấu trúc Dewey + [Analysis-Market-Competitor-Landscape](../050-Research/Analysis-Market-Competitor-Landscape.md) |

## Tài liệu tham khảo

- [Documentation Master Index](../000-Index.md)
- [Analysis-Comic-Studio-Concept](../050-Research/Analysis-Comic-Studio-Concept.md) — căn cứ thẩm định của toàn bộ tầng này
- [Analysis-Market-Competitor-Landscape](../050-Research/Analysis-Market-Competitor-Landscape.md) — thị trường, đối thủ, pricing
- [Documentation Structure Rule (RULE-001)](../../knowledge-base/99-Templates/Documents-Template.md)
