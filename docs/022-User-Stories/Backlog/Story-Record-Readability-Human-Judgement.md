---
id: STORY-H-02
type: story
status: draft
created: 2026-08-24
---

# Story-Record-Readability-Human-Judgement

## 1. Story

Là Founder (operator), tôi muốn **cạnh mọi metric kỹ thuật có đúng một câu người trả lời — *"trang này đọc có ổn không?"* — và câu trả lời được GHI LẠI từ MVP0**, để **hệ thống không pass mọi check trong khi không ai muốn đọc**.

## 2. Part of

- Epic cha: [Epic-Quality-And-Operations](../Epics/Epic-Quality-And-Operations.md)
- BRD cha: [BRD-008-Quality-And-Operations](../../020-Requirements/BRD/BRD-008-Quality-And-Operations.md)
- UC liên quan: [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — nơi panel/trang được sinh ra và là điểm đầu tiên câu hỏi readability áp dụng được ở MVP0. Không có UC riêng cho câu hỏi này — nó là một phép đo xuyên suốt, không phải một luồng người dùng độc lập.

## 3. Bối cảnh & nguồn

> ⚠️ **Ghi chú anchor**: `findings/business-analyst.md` §4.8 chỉ trích **Analysis §3.2** cho Story này, không trích một hàng `MVP-Scope §3` hay một exit criterion `Roadmap` có mã. Hai anchor dưới đây là kết nối do `quality-assurance` bổ sung để thoả yêu cầu cấu trúc (mục 3 bắt buộc có cả hai loại anchor) — **`[QA suy luận]`**, không phải trích dẫn nguyên văn có sẵn.

- **[QA suy luận] Anchor `MVP-Scope §3`**: không có hạng mục riêng cho "readability judgement". Hạng mục gần nhất là **H6** (Golden dataset regression) — vì cột *"bảng chấm"* của H6 chính là nơi câu hỏi *"trang này đọc có ổn không?"* lần đầu được ghi lại, và cả hai Story (`Story-Golden-Dataset-For-Regression` và Story này) cùng được Epic cha xếp chung một mục DoD (§5.2: *"DoD của hai Story MVP0 — đo bằng gate G1"*).
- **[QA suy luận] Anchor `Roadmap` exit criterion**: không có mã `P-x`/`M1-x` riêng cho tiêu chí này — đúng như `Epic-Quality-And-Operations.md` §5.1 mục #7 đã tự ghi (dẫn `CF-10.10`/Analysis §3.2, không dẫn mã Roadmap). Theo nguyên tắc *"không có mã riêng ⇒ ghi rõ nằm ở cột Deliverable"*: neo vào cột **Deliverable** của mốc **Pre-cycle 09/2026** (`Roadmap.md` §2) — *"...trang composite có speech bubble"* là artifact đầu tiên nơi câu hỏi readability áp dụng được; dataset đi kèm nó chính là **P-6**.
- `Analysis-Comic-Studio-Concept.md` §3.2 đoạn *"→ Sửa cái gì"* (nguồn gốc của yêu cầu, **không sửa tài liệu này** — `CẤM-18`): câu hỏi *"trang này đọc có ổn không?"* **vừa là metric chất lượng thật, vừa là dữ liệu preference cho moat**.
- CF-10.10 (`findings/business-analyst.md` §5.2): lỗi *"pass mọi check mà không ai muốn đọc"* là **vô hình đối với chính hệ thống** — Continuity Checker không bắt được, không metric nào trong `Request.md` bắt được.
- `MVP-Scope.md` §3.1 kỷ luật MVP0: giữ lại **kết luận và dữ liệu** — câu trả lời readability là một phần của dữ liệu phải giữ lại đó, từ MVP0.

## 4. Acceptance Criteria

### Xác minh được

- [ ] Với mỗi panel/trang composite được sinh ra ở MVP0, tồn tại đúng một câu trả lời nhị phân "đọc ổn / không ổn" do Founder ghi lại — đo bằng: đếm số panel có bản ghi readability, phải bằng **100%** tổng số panel MVP0 sinh ra.
- [ ] Bản ghi readability có timestamp và được lưu ở một trường/cột **tách biệt** khỏi 5 tiêu chí `G1-a…G1-e` — đo bằng: kiểm tra schema/bảng ghi có cột riêng `readability_verdict`, độc lập với các cột G1.
- [ ] Giá trị readability thuộc một tập giá trị cố định đã định nghĩa trước (ví dụ: `ổn` / `không ổn` / `chưa chấm`), không phải văn bản tự do không phân loại được — đo bằng: kiểm tra giá trị ghi nhận thuộc enum cố định.
- [ ] Từ MVP1 trở đi, mỗi lần sinh panel/trang mới đều có bản ghi readability tương ứng, không có khoảng trống liên tục nào chưa được chấm — đo bằng: đối chiếu số lượng generation với số lượng bản ghi readability trong cùng kỳ, phải bằng nhau.

### Đường không hạnh phúc (unhappy path)

- [ ] Nếu Founder bỏ qua không chấm một panel (do chạy dồn dập), panel đó phải hiển thị trạng thái `chưa chấm` tường minh — **không** được mặc định là "ổn" — đo bằng: giá trị mặc định của trường readability khi chưa ghi là `chưa chấm`/`NULL`, không phải giá trị PASS ngầm định.
- [ ] Nếu điểm readability và điểm kỹ thuật (`G1-a…G1-e` / eval kit) mâu thuẫn nhau (panel PASS kỹ thuật nhưng readability = "không ổn"), hệ thống phải giữ lại **cả hai** giá trị độc lập, không cho phép điểm kỹ thuật ghi đè hoặc ẩn điểm readability — đo bằng: hai trường tồn tại độc lập, không có logic tự động suy readability từ điểm kỹ thuật.
- [ ] Với 1 Founder duy nhất chấm (bus factor = 1, không có second rater — `Glossary.md` *bus factor*), nếu Founder đổi câu trả lời cho cùng một panel ở hai thời điểm khác nhau, bản ghi phải giữ **lịch sử cả hai lần chấm**, không ghi đè giá trị cũ — đo bằng: bảng ghi có ≥2 dòng lịch sử cho panel đó khi có sửa.

### Ràng buộc cứng không được vi phạm

- — Không tìm thấy `KC-x`/`C-x`/`AG-x` áp trực tiếp trong các nguồn đã đọc (`MVP-Scope.md` §6, `Charter-Comic-Studio.md` §7). Không tự gắn mã để lấp chỗ trống.

### Story này KHÔNG làm

- [ ] KHÔNG dùng câu trả lời readability để tự động pass/fail gate `G1`/`G2` — nó là dữ liệu bổ sung song song, không thay thế 5 tiêu chí `G1` (`MVP-Scope.md` §7.2).
- [ ] KHÔNG để VLM tự trả lời câu hỏi này thay người — CF-10.10 nêu rõ đây là **đúng một câu người trả lời**.
- [ ] KHÔNG xây eval kit tự động từ dữ liệu readability — đó là phạm vi của `Story-HITL-Gate-And-Eval-Kit`.
- [ ] KHÔNG giới hạn việc ghi nhận chỉ ở MVP0 — nghĩa vụ là **liên tục** từ MVP0 trở đi, không dừng lại sau khi MVP0 kết thúc.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | **~4 giờ-người** `[EM]` | Thiết kế 1 trường ghi nhận + quy trình ghi mỗi lần sinh panel/trang. Trong trần 16h. |
| `E_hitl` | `TBD` | Đây là nghĩa vụ **lặp lại liên tục** (mỗi panel/trang, mỗi chapter) — đúng loại đại lượng mà Epic này dễ vượt trần nhất. **Không có nguồn nào trong repo đo thời gian trung bình để trả lời "đọc ổn không" cho một panel** — tự tính bằng cách nhân số panel/chapter (CF-3.3 `[EM]` 60 ảnh/chapter) với một giả định thời gian/panel sẽ vi phạm `CẤM-15` (cấm tự tính số mới không có nguồn). **Điều kiện escalate**: nếu sau khi vận hành thực tế ở MVP1, tổng thời gian chấm readability đo được vượt **2 giờ-người/chapter**, escalate cho Founder xem xét đổi granularity chấm (ví dụ chấm theo trang thay vì theo panel) — không tự split Story. |

## 6. INVEST

`INVEST không áp — Story thuộc [MVP0]`. Lý do (`findings/business-analyst.md` §4.9, `MVP-Scope.md` §3.1, `Roadmap.md` §3.1): code của MVP0 không phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu. Story này không cần `Independent` (nó là một lát cắt xuyên tầng đo lường, sống trong mọi luồng sinh panel/trang từ MVP0 trở đi); tiêu chí `Valuable` của nó là **thông tin đo được** (câu trả lời readability), không phải một tính năng giao cho khách. Ghi chú: BA table cho Story này chấm `I=✅`/`S=✅` (không vỡ), nhưng Epic cha (§5.2) xếp Story này **chung nhóm MVP0 với `Story-Golden-Dataset-For-Regression`** — hai Story duy nhất của Epic-H có nhãn `[MVP0]` — nên áp dụng đúng quy tắc ràng buộc riêng #1 của lô này bất kể cột `I`/`S` gốc.

**Definition of Done — 5 tiêu chí gate G1** (`MVP-Scope.md` §7.2), thay cho Acceptance Criteria kiểu Gherkin thông thường:

- [ ] `G1-a` Consistency nhân vật ≥70% panel — câu trả lời readability là dữ liệu **bổ sung**, chạy song song với tiêu chí này, không thay thế nó.
- [ ] `G1-b` N tối thiểu ≤3 để VLM-select ra panel đạt.
- [ ] `G1-c` `reject_rate` sau VLM-select có số và verdict phân loại đúng dải `⚠️ [EM]`.
- [ ] `G1-d` Panel 2 nhân vật ≥60% đúng identity + attribute binding; panel 3 nhân vật đo và báo cáo `⚠️ [EM]`.
- [ ] `G1-e` 100% panel có thoại dùng overlay, 0 panel nhờ model render chữ.
- [ ] **Bổ sung riêng của Story này** (ngoài 5 tiêu chí G1, vì đây là dữ liệu song song không thuộc G1): 100% panel MVP0 có bản ghi readability — đây là điều kiện Done thực tế của Story, không phải một tiêu chí G1.

⛔ Dùng đúng tên **MVP0** — `Glossary.md` cấm *"phase 0"*, *"spike"*, *"PoC"* (`CẤM-11`).

---

_Created by quality-assurance_
_Author: trisjr_
