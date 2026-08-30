---
id: UC-03
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-03 — Duyệt panel script (Comic IR)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts — **số và nhãn là một cặp không tách rời**):
> `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> ⚠️ **Bẫy đánh số (CF-10.2 · CẤM-14)**: `G1`/`G2` trong tài liệu này **luôn** là ID **gate** (kỹ thuật / kinh tế), không phải hàng compliance `GP-1`/`GP-2`.

## Mục lục

1. [Thông tin](#1-thông-tin)
2. [Mục tiêu](#2-mục-tiêu)
3. [Main flow](#3-main-flow)
4. [Alternative flow](#4-alternative-flow)
5. [Exception flow](#5-exception-flow)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Thông tin

| Hạng mục | Nội dung |
|---|---|
| **Primary actor** | **Tác giả truyện chữ** (không biết vẽ) — CF-1.5 `[CHỐT]`. ⛔ **CẤM-17**: không đặt requirement cho phân khúc hoạ sĩ |
| **Secondary actor** | **Hệ thống** (Comic Director deterministic + CHECK constraint tầng DB) · **LLM** (chỉ ở chặng đề xuất phân cảnh của Director) · **Founder-operator** (chỉ ở nhánh MVP0, khi panel script được viết tay) |
| **Mốc MVP** | **MVP0** — `Panel Specification` là **🟡 YAML viết tay** (`MVP-Scope` §3 `C1`) → **MVP2** — Director tự động sinh page/panel (`C2` ✅, `Roadmap` §2 **M2-1**) |
| **BRD module** | [BRD-003 — Comic Director And Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) (`BR-003-01`…`BR-003-09`) |
| **Điều kiện tiên quyết (precondition)** | (1) [UC-02](./UC-02-Review-And-Edit-Story-Bible.md) đã hoàn tất: Story Bible của chapter đã được tác giả duyệt, vì Director đọc state qua `resolveState()`. (2) Từ MVP2: schema **Comic IR (Comic Intermediate Representation)** đã có CHECK constraint **≤3 nhân vật/panel** và field `text_safe_zone` (`BR-003-05`, `BR-003-08`). (3) Bố cục lưu dưới dạng **toạ độ chuẩn hoá 0–1 trong `page_layout JSONB`** (`BR-003-04`). (4) ⚠️ **`TBD` (KT-1)** — actor là **phân khúc** đã chốt (CF-1.5), **không phải một persona**; hệ quả trực tiếp: *"bố cục có nhịp"* chưa có định nghĩa nghiệm thu nào ngoài CF-10.10 (*"trang này đọc có ổn không?"*, định tính). Xem `findings/business-analyst.md` §6.2 `KT-1` |

## 2. Mục tiêu

Tác giả duyệt và sửa **panel script** — tức tập `Panel Specification` của một chapter, biểu diễn dưới dạng **Comic IR (Comic Intermediate Representation)** — **trước khi tiêu bất kỳ đồng tiền API nào**. Đây là điểm rẻ nhất trong toàn pipeline để một quyết định dàn dựng được sửa: `Panel Specification` là *"**dữ liệu chính**"* của hệ thống, **ảnh là output phái sinh** (`Glossary` *Panel Specification*; `BR-003-01`). Sửa ở đây là **sửa một field**; sửa sau khi đã sinh ảnh là **re-roll cả ảnh**, và ảnh thì đã tốn tiền thật.

Giá trị thứ hai, ít lộ ra nhưng nặng hơn: cùng với Comic IR, output của Layout Director — *selection & arrangement* — là **phần được bảo hộ bản quyền** (`Glossary` *Layout Director*). Mỗi lần tác giả sửa một panel ở đây là một quyết định sáng tạo của con người, và nó được ghi lại. Tác giả kết thúc use case này với một trang truyện **đã được quyết xong trên giấy**, chưa một pixel nào được sinh.

## 3. Main flow

Main flow dưới đây là **hình dạng ở MVP2** (Director tự động). Nhánh **MVP0 viết tay** nằm ở [mục 4](#4-alternative-flow) `ALT-1`.

| # | Actor | Bước |
|---|---|---|
| 1 | **Tác giả** | Chọn chapter đã duyệt Story Bible và yêu cầu sinh panel script |
| 2 | **Hệ thống** | Đọc `Event` mức scene của chapter và gọi `resolveState()` để biết trạng thái entity tại từng thời điểm — module `comic` chỉ được gọi module `story` qua đúng hai hàm `resolveState()` và `getBible()` (`BR-002-10`) |
| 3 | **LLM** | Đề xuất phân chia **scene → page → panel** cho chapter (`BR-003-02`) |
| 4 | **Hệ thống** | Cấp diện tích cho từng panel theo **rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter** — bố cục có nhịp mà **không** cần một điểm số không kiểm chứng được (`BR-003-03`) |
| 5 | **Hệ thống** | Ghi bố cục thành **toạ độ chuẩn hoá 0–1 trong `page_layout JSONB`**; template chỉ là **preset ghi vào CÙNG schema đó** (`BR-003-04`) |
| 6 | **Hệ thống** | Khai `text_safe_zone` cho từng panel — vùng giữ trống để đặt bubble về sau (`BR-003-08`) |
| 7 | **Hệ thống** | Ghi từng panel thành một `Panel Specification` có schema: bố cục, nhân vật có mặt, camera, ràng buộc thị giác, vùng an toàn cho chữ. **CHECK constraint tầng DB từ chối mọi panel ≥4 nhân vật** (`BR-003-01`, `BR-003-05`) |
| 8 | **Tác giả** | Đọc panel script: với mỗi page, xem thứ tự đọc, kích cỡ tương đối các panel, nhân vật có mặt, và camera |
| 9 | **Tác giả** | Sửa những panel sai: đổi nhân vật có mặt, đổi camera, gộp / tách panel, đổi `beat_type` để panel quan trọng được cấp diện tích lớn hơn |
| 10 | **Hệ thống** | Với **mỗi** lần sửa ở bước 9, sinh một **`change_log`** row và cập nhật `field_provenance` (`KC-2`, `KC-3`), **commit cùng một transaction** với chính panel spec được sửa (`KC-4`) |
| 11 | **Tác giả** | Đánh dấu panel script của chapter là đã duyệt |
| 12 | **Hệ thống** | Chapter chuyển sang chặng thoại — [UC-04](./UC-04-Human-Gate-Speaker-Attribution.md) rồi [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md). ⚠️ **`dialogue condensation` phải chạy SAU layout**, vì `text_budget` phụ thuộc **diện tích panel** — đây là **ràng buộc thứ tự**, không phải tối ưu hoá (`BR-003-12`) |

> **Không có một đồng API sinh ảnh nào được tiêu trong toàn bộ flow trên.** Đó chính là giá trị của use case này, và là lý do `MVP-Scope` §3 xếp `C1` (Comic IR) là hàng **rủi ro thấp nhất bảng** trong khi vẫn giữ nó ở MVP0: spec tách khỏi ảnh nên **đổi granularity render không đổi data model** (`A7`, `MVP-Scope` §7.3 đường lui #1).

## 4. Alternative flow

| # | Nhánh | Diễn biến |
|---|---|---|
| **ALT-1** | **MVP0 — panel script viết tay** | `MVP-Scope` §3 `C1` = **🟡 YAML tay** và `C2` = ❌ **viết tay** ở MVP0. **Founder-operator** viết tay YAML panel script cho **một chapter duy nhất** (~8–30 panel theo `Roadmap` §2 deliverable của pre-cycle), rồi tự đóng vai người duyệt. **MVP0 không có database** (`MVP-Scope` §3.1) ⇒ không có `change_log` dạng bảng ở mốc này; provenance được **ghi tay** ra file (`GP-1` = 🟡 ghi tay, và đây là diễn giải `[EM]`, xem `MVP-Scope` §3.1). Dùng đúng tên **MVP0** — ⛔ **CẤM-11** cấm gọi *"phase 0"*, *"spike"*, *"PoC"* |
| **ALT-2** | **Tác giả yêu cầu Director sinh lại toàn bộ chapter** | Bước 3–7 chạy lại; panel script cũ **không bị ghi đè âm thầm** — bản cũ giữ lại và hành động thay thế sinh `change_log` (`KC-2`). Chi phí của nhánh này là chi phí LLM của Director, **không** phải chi phí sinh ảnh |
| **ALT-3** | **Tác giả sửa panel script trực tiếp mà bỏ qua bước đọc toàn chapter** | Bước 8 có thể thực hiện ở phạm vi một page. Ràng buộc duy nhất: mọi lần sửa vẫn đi qua bước 10 |
| **ALT-4** | **Chapter có cảnh đông người** | Tác giả **không** được nhồi thêm nhân vật vào một panel. Đường giải là **shot xa / silhouette / crop** (`BR-003-07`). Đây là **giới hạn sản phẩm nhìn thấy được**, phải nói rõ với người dùng — căn cứ CF-6.5 `[OFF]` (ID-Sim **42.33** ở 2 nhân vật → **27.21** ở 3 → **2.67** ở 4 → **0.52** ở 5, *"near-complete failure beyond three subjects"*) |
| **ALT-5** | **Gate `G1` cho kết quả PASS CÓ ĐIỀU KIỆN ở tiêu chí `G1-d`** | Trần nhân vật được **siết xuống ≤2 trong schema** (đổi chính hàng `C5`), **không** phải giữ ≤3 rồi khuyến nghị (`BR-003-06`). ⚠️ `G1-d` là `[EM]` — **ngưỡng do writer run trước định nghĩa tại run đó, không có nguồn ngoài** (CF-10.4). Từ thời điểm đó, bước 7 và `EXC-1` áp trần mới |

## 5. Exception flow

| # | Nhánh ngoại lệ | Diễn biến & xử lý |
|---|---|---|
| **EXC-1** | ⛔ **Tác giả sửa một panel thành 4 nhân vật trở lên** | **Tầng DB TỪ CHỐI** thao tác — **không phải cảnh báo rồi cho qua**. `Roadmap` §2 **M2-2** đo bằng: *insert panel 4 nhân vật **bị từ chối***. Hệ thống báo lý do và gợi ý đường giải hợp lệ: **shot xa / silhouette / crop** (`BR-003-07`). Căn cứ CF-6.5 `[OFF]`: attribute binding **thất bại gần hoàn toàn** từ 4 nhân vật ⇒ cho qua kèm cảnh báo là để lỗi **thất bại âm thầm** (`BRD-003` §5 mục 5: **không mở lại**; đường duy nhất là siết xuống ≤2, không phải nới lên) |
| **EXC-2** | **Director không sinh được panel script cho chapter** | Bước 3–7 thất bại. Chapter giữ nguyên trạng thái *đã có bible, chưa có panel script*. Tác giả có hai đường: **retry**, hoặc chuyển sang **ALT-1** viết tay panel script cho chapter đó. ⛔ Không sinh panel script rỗng để *"có gì đó cho tác giả xem"* — panel script rỗng đi tiếp vào chặng sinh ảnh là đường tiêu tiền vào một spec vô nghĩa |
| **EXC-3** | **`text_safe_zone` không tồn tại hoặc bằng 0 diện tích trên panel có thoại** | Panel **không được phép** đi tiếp sang chặng typeset. Thiếu `text_safe_zone` thì bubble che mặt nhân vật và **phải sinh lại toàn bộ ảnh đã làm** (`BR-003-08`). Ngưỡng nghiệm thu: **≥95%** panel typeset **không đè vùng mặt** — `Roadmap` §2 **M2-3**. ⚠️ **`[EM]` — `Roadmap` §2 ghi nguyên văn *"ngưỡng do em định nghĩa"*; cấm trích như số đo hoặc benchmark ngành** (CF-10.5) |
| **EXC-4** | **Director đọc state sai vì khoá thời gian sai** | Panel hồi tưởng mang trang phục/vết thương của **hiện tại**. Đây là lỗi **không crash, chỉ sai âm thầm** (`Risk-Register` `R-15`). Tác giả phát hiện ở bước 8; đường sửa nằm ở [UC-02](./UC-02-Review-And-Edit-Story-Bible.md) (`timeline_id` / `story_order` của event), **không** ở panel spec — sửa panel spec là chữa triệu chứng và lỗi sẽ trở lại ở panel kế tiếp |
| **EXC-5** | **Emphasis quota của chapter đã cạn mà tác giả vẫn muốn nâng một panel lên `beat_type` cao hơn** | Hệ thống buộc tác giả **hạ một panel khác xuống** để giữ quota. Lý do nghiệp vụ: nếu mọi panel đều được nhấn thì **không panel nào được nhấn** — đó là mục tiêu mà rubric rời rạc giữ lại sau khi cơ chế **Layout Score 5 số thực bị CẮT HẲN** (`C4` = ❌ ở cả cột Full Scope; CF-9.3 — **mục tiêu giữ, cơ chế bỏ**) |
| **EXC-6** | **Ghi `change_log` thất bại trong khi panel spec đã được sửa** | Toàn bộ transaction **rollback**. `KC-4`: bằng chứng phải commit **cùng một transaction** với artifact — *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*. Panel spec là artifact được bảo hộ (*selection & arrangement*), nên mất log ở đây là mất đúng phần chứng minh authorship |

> **Ba thứ use case này KHÔNG làm** — ghi ra để không ai đi tìm ở đây: (a) **sắp trang / chọn template / đổi chỗ panel qua UI** thuộc [UC-08](./UC-08-Arrange-Page-And-Preview.md) — module này sở hữu **schema** `page_layout`, không sở hữu màn hình (`BRD-003` §5 mục 4); (b) **render bubble và chữ** là typeset layer, hàng `A2` của [BRD-001](../BRD/BRD-001-Image-Generation-Pipeline.md), xem [UC-07](./UC-07-Edit-Bubble-And-Dialogue-In-Panel.md); (c) **sinh ảnh và chọn variant** thuộc [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md).

## 6. Tài liệu liên quan

### 6.1 Traceability

| Quan hệ | Tài liệu |
|---|---|
| Part of | [Epic-Comic-Director-And-Layout.md](../../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) |
| BRD nguồn | [BRD-003 — Comic Director And Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) |
| BRD lân cận được trỏ trong tài liệu này | [BRD-001 — Image Generation Pipeline](../BRD/BRD-001-Image-Generation-Pipeline.md) (typeset layer `A2`) · [BRD-002 — Story Intelligence](../BRD/BRD-002-Story-Intelligence.md) (`resolveState()`, `getBible()`) · [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) (UI sắp trang) |
| Requirement cấp sản phẩm | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) · chi tiết kỹ thuật: [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) |
| Use Case trước | [UC-02 — Review And Edit Story Bible](./UC-02-Review-And-Edit-Story-Bible.md) |
| Use Case kế tiếp (hai human gate) | [UC-04 — Human Gate Speaker Attribution](./UC-04-Human-Gate-Speaker-Attribution.md) → [UC-05 — Human Gate Dialogue Condensation](./UC-05-Human-Gate-Dialogue-Condensation.md) |

### 6.2 Nguồn đã trích (Tài liệu tham khảo)

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — §3 hàng `C1`, `C2`, `C3`, `C4`, `C5`, `C6`, `C7`, `A7` · §3.1 (MVP0 không có database; `GP-1` 🟡 ở MVP0) · §4.1, §4.2, §4.3 · §6 `KC-2`, `KC-3`, `KC-4` · §7.2 `G1-d` · §7.3 đường lui #1
- [Roadmap.md](../../010-Planning/Roadmap.md) — §2 exit criteria **M2-1**, **M2-2**, **M2-3** (**≥95%** ⚠️ `[EM]`) · §2 deliverable pre-cycle (1 chapter, ~8–30 panel)
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — `R-12` (chưa có benchmark độc lập 2–3 nhân vật/panel) · `R-15` (khoá thời gian sai)
- [Glossary.md](../../999-Resources/Glossary.md) — *Comic IR (Comic Intermediate Representation)*, *Panel Specification*, *Layout Director*, *Layout Score*, *`text_safe_zone`*, *dialogue condensation*, *attribute binding*, *MVP0*
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001
- `docs/010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md` — §3.1 (transform deterministic là **bước bên trong** UC, không phải UC), §3.2 hàng **UC-03**, §5.2 (CF-1.5, CF-6.5, CF-9.3, CF-10.2, CF-10.4, CF-10.5, CF-10.10), §5.3 (CẤM-11, CẤM-14, CẤM-16, CẤM-17), §6.2 `KT-1`, `KT-7`

---

_Created by Comic Studio — role `business-analyst`_
_Author: trisjr_
