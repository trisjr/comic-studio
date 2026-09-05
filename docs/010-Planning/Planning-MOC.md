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

## Kế hoạch thực thi MVP1

Ba tài liệu dưới đây biến cột *Effort ước tính: `TBD`* của [Roadmap](./Roadmap.md) mốc MVP1 thành một lịch có giờ, có thứ tự và có DoD.

| # | Tài liệu | Nội dung | Trạng thái |
|---|---|---|---|
| 1 | [Plan-MVP1-Story-Intelligence](./Implementation-Plans/Plan-MVP1-Story-Intelligence.md) | Kế hoạch master `10/2026 – 12/2026`: phạm vi 26 story, ba nợ thừa kế, đường găng, van xả xếp sẵn, ánh xạ `M1-1`…`M1-7`. ⚠️ Kết luận: tải **386h / 384h capacity** — **⛔ không có đệm** | `draft` |
| 2 | [WBS-MVP1](./Estimates/WBS-MVP1.md) | Phân rã giờ theo sprint, căn cứ của **7 ước lượng do PM đặt**, ba khoảng trống backlog, burn-down dự kiến | `draft` |
| 3 | [Sprint-001](./Sprints/Sprint-001.md) … [Sprint-006](./Sprints/Sprint-006.md) | Mục tiêu, story, thứ tự, DoD và retro checklist từng sprint | `draft` |

> ⚠️ **Hai điều phải biết trước khi đọc ba tài liệu trên.**
>
> 1. **`G1` chưa từng được đo.** MVP0 khép theo quyết định Founder `2026-09-05` với **0/5** tiêu chí có số ([`g1-verdict.md`](../../mvp0/golden-dataset/g1-verdict.md)) ⇒ MVP1 chạy trên một tiền đề **chưa kiểm chứng**, và nợ đó chuyển sang MVP3.
> 2. **`G2` cuối Q4/2026 sẽ ra verdict `KHÔNG CHẠY ĐƯỢC`** — biết trước, ⛔ không phải rủi ro. Cả bốn tiêu chí `G2-a`…`G2-d` đòi dữ liệu image generation, mà MVP1 có `A1 = ⛔`.

### Sprint MVP1

| Sprint | Ngày | Chủ đề | Exit criteria trả |
|---|---|---|---|
| [001](./Sprints/Sprint-001.md) | `05/10` – `16/10` | Nền tenancy ⛔ không retrofit được | ⭐ `M1-1` |
| [002](./Sprints/Sprint-002.md) | `19/10` – `30/10` | Cửa pháp lý & đường vào của dữ liệu | ⭐ `M1-4` |
| [003](./Sprints/Sprint-003.md) | `02/11` – `13/11` | Provenance — bằng chứng ⛔ không thiếu ngẫu nhiên | `M1-5` (phần tồn tại) |
| [004](./Sprints/Sprint-004.md) | `16/11` – `27/11` | Sổ cái sử dụng & ranh giới transaction | ⭐ `M1-5` (trọn vẹn) |
| [005](./Sprints/Sprint-005.md) | `30/11` – `11/12` | Story Intelligence — ingest → extraction → timeline | ⭐ `M1-2` |
| [006](./Sprints/Sprint-006.md) | `14/12` – `31/12` | Editor & eval kit + tuần gate `G2` | ⭐ `M1-3` · ⭐ `M1-6` |

## Thư mục con

| Thư mục | Nội dung | Trạng thái |
|---|---|---|
| [Sprints/](./Sprints/) | `Sprint-{NNN}.md`, `Retro-Sprint-{NNN}.md` | 6 sprint MVP1 · *(chưa có retro)* |
| [Estimates/](./Estimates/) | WBS, ETA, Budget | [WBS-MVP1](./Estimates/WBS-MVP1.md) · *(chưa có Budget)* |
| [Implementation-Plans/](./Implementation-Plans/) | `Plan-{Feature}.md` | [Plan-MVP1-Story-Intelligence](./Implementation-Plans/Plan-MVP1-Story-Intelligence.md) |

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
