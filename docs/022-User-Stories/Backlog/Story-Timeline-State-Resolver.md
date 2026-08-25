---
id: STORY-B-04
type: story
status: draft
created: 2026-08-24
---

# Story-Timeline-State-Resolver

## 1. Story

Là tác giả truyện chữ, tôi muốn **truy được trạng thái nhân vật tại một thời điểm bất kỳ** (`state_at(N) = reduce(events)`), để **panel ở chương 40 dùng đúng trang phục của chương 40**

## 2. Part of

- Epic cha: [Epic-Story-Intelligence](../Epics/Epic-Story-Intelligence.md)
- BRD: [BRD-002-Story-Intelligence](../../020-Requirements/BRD/BRD-002-Story-Intelligence.md)
- Use Case liên quan: [UC-03-Review-Panel-Script](../../020-Requirements/Use-Cases/UC-03-Review-Panel-Script.md) — Director tiêu thụ output của Story này qua `resolveState()`/`getBible()`, không đọc trực tiếp bảng của schema `story`; cũng là nền cho [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) khi hiển thị state theo event

## 3. Bối cảnh & nguồn

Đây là hàng **`B3`** của [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope): *"Timeline state resolver `state_at(N) = reduce(events)`"* — `❌ viết tay` ở MVP0, `✅` từ MVP1 trở đi, căn cứ *"Analysis §5.5 — code sở hữu state, LLM chỉ phát event"*.

> [!CAUTION]
> **Khoảng trống nguồn cần báo cáo**: không có exit criterion `M1-x` nào trong [Roadmap §2](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) đặt tên trực tiếp cho resolver này (`M1-3` đo **extraction**, không đo phép `reduce`). Exit criterion dùng làm anchor ở đây là **`P-4`** (mốc Pre-cycle 09/2026 — *"khoá thời gian thay `(chapter, scene)` được viết ra dưới dạng schema draft"*), vì resolver này là hệ quả trực tiếp của khoá đó, cộng với tiêu chí DoD cấp Epic bên dưới — chưa xác nhận được với Founder liệu có cần bổ sung một exit criterion `M1-x` riêng cho resolver hay không.

[Epic-Story-Intelligence §5](../Epics/Epic-Story-Intelligence.md#5-definition-of-done-cấp-epic) ghi trực tiếp hai điều kiện DoD mà Story này phải thoả: *"`state_at(N) = reduce(events)` trả về đúng trạng thái tại một thời điểm bất kỳ, và điều đó được chứng minh bằng **một test có flashback** — không phải bằng một chuỗi chương tuyến tính"*, và *"Ranh giới **code sở hữu state, LLM chỉ phát event** không bị vi phạm: không có đường nào để LLM ghi trực tiếp vào bảng state"*.

## 4. Acceptance Criteria

### Xác minh được

- [ ] `state_at(N)` trả về đúng trạng thái của một nhân vật (trang phục, vị trí, quan hệ) tại `story_order = N` bất kỳ — đo bằng: gọi `state_at` với N nằm giữa hai event, kết quả khớp state đã reduce đến đúng event gần nhất có `story_order ≤ N`
- [ ] Kết quả `state_at(N)` là **tất định** — đo bằng: gọi lại hai lần liên tiếp với cùng N, hai output giống hệt nhau
- [ ] Một test case có **flashback** (event đọc ở chapter sau nhưng `story_order` thuộc thời điểm trước) chứng minh `state_at` trả đúng theo `story_order`, không theo thứ tự đọc — đo bằng: test được đặt tên cụ thể cho trường hợp flashback này PASS, không chấp nhận thay bằng test trên chuỗi chương tuyến tính
- [ ] Không có đường code nào cho phép LLM ghi trực tiếp vào bảng state — chỉ `reduce(events)` mới sinh ra giá trị state — đo bằng: rà soát quyền ghi ở tầng schema/service, không có endpoint hay service nào ghi bảng state từ output LLM mà không qua `reduce`
- [ ] `resolveState()`/`getBible()` là API duy nhất để module `comic` đọc state của module `story` — đo bằng: rà soát code, không có query nào từ module `comic` trỏ trực tiếp vào bảng của schema `story` ngoài hai hàm này

### Đường không hạnh phúc (unhappy path)

- [ ] Hai event có cùng `story_order` nhưng khác `timeline_id` (nhánh song song, ví dụ giấc mơ) — `state_at` không được gộp chúng vào cùng một chuỗi reduce (đo bằng: state của mỗi `timeline_id` được tính độc lập, không lẫn dữ liệu giữa hai nhánh)
- [ ] Gọi `state_at(N)` khi N nhỏ hơn `story_order` của event đầu tiên của nhân vật (trước khi nhân vật xuất hiện trong truyện) — hệ thống trả về kết quả "chưa có state" một cách tường minh, không trả về record rỗng hoặc giá trị mặc định gây hiểu nhầm là đã có dữ liệu (đo bằng: response phân biệt rõ được với trường hợp "có state nhưng rỗng")
- [ ] Một event bị sửa hoặc xoá sau khi `state_at` liên quan đã được tính trước đó — lần gọi `state_at` tiếp theo phải phản ánh đúng thay đổi, không dùng lại giá trị đã cache từ trước (đo bằng: sau khi sửa event, gọi lại `state_at(N)` liên quan trả về giá trị mới, khác giá trị trước khi sửa)
- [ ] Chuỗi event dài (một chapter có 40+ event ảnh hưởng cùng một nhân vật) — `state_at` vẫn trả đúng kết quả, không bỏ sót event ở giữa chuỗi reduce (đo bằng: so khớp kết quả `state_at` ở cuối chuỗi với kết quả reduce thủ công trên cùng tập event)

### Ràng buộc cứng không được vi phạm

- —

### Story này KHÔNG làm

- Không extract event từ text chapter — đó là `Story-Story-Bible-Extraction`, cung cấp event làm input cho resolver này
- Không sửa khoá thời gian (`timeline_id` + `story_order`) — đó là `Story-Fix-Narrative-Time-Key`, đã phải xong trước
- Không có UI hiển thị state cho tác giả — thuộc `Story-Story-Bible-Editor-Form` (Epic-D)
- Không dùng `pgvector` để tăng tốc truy vấn state — `B5` bị `❌` tới MVP2, không dùng ở mốc này **nhưng không bị cấm vĩnh viễn** (Full Scope `🟡` khi có bằng chứng SQL+FTS không đủ)

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **20h** `[EM]` — **vượt trần 16h, lý do ghi thành văn** | Đây là nơi ranh giới *"code sở hữu state, LLM chỉ phát event"* được thực thi bắt buộc, gồm: phép `reduce` tất định qua nhiều `timeline_id` song song, xử lý biên (trước event đầu tiên, event bị sửa/xoá sau khi đã tính), và một test flashback chuyên biệt theo yêu cầu DoD cấp Epic. Đây không phải một CRUD đơn giản mà là logic lõi quyết định tính đúng đắn của toàn bộ Story Bible |
| `E_hitl` | **0** | Đây là logic backend thuần, không tạo ra một HITL gate hay nghĩa vụ lặp lại theo chapter cho con người |

## 6. INVEST

- **I (Independent)**: ⚠️ — **[không có trong bảng `findings/business-analyst.md` §4.10]**, nhưng lý do đã được chính [Epic-Story-Intelligence §3](../Epics/Epic-Story-Intelligence.md#3-story-trong-horizon) khối `[!CAUTION]` ghi rõ: *"`Story-Timeline-State-Resolver` vỡ cả `I` và `S`: nó là chỗ ranh giới 'code sở hữu state, LLM chỉ phát event' được thực thi, và nó phụ thuộc trực tiếp vào khoá thời gian [do `Story-Fix-Narrative-Time-Key` định nghĩa]"*. Đây là lý do PO ghi lại từ Epic cha, không tự suy diễn thêm.
- **S (Small)**: ⚠️ — cùng nguồn trên. Phạm vi phép `reduce` qua nhiều nhánh `timeline_id`, xử lý biên, và yêu cầu test flashback chuyên biệt của DoD cấp Epic khiến `E_build` vượt trần 16h (mục 5) — không phải một slice nhỏ, mà là logic lõi của toàn Epic.

> **Khoảng trống cần báo cáo**: `findings/business-analyst.md` §4.10 không liệt kê rõ Story này trong bảng "bảy Story vỡ" dù bảng §4.2 đã chấm `I=⚠️, S=⚠️` cho nó — lý do vỡ ở đây được lấy từ chính Epic cha (nguồn thứ cấp, không phải trực tiếp §4.10), không phải bịa ra.

---

_Created by product-owner_
_Author: trisjr_
