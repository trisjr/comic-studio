---
id: BRD-003
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# BRD-003 — Comic Director & Layout

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn từ bảng Canonical Facts — **số và nhãn là một cặp không tách rời**):
> `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> **Ký hiệu mốc** (giữ nguyên từ [MVP-Scope.md](../../010-Planning/MVP-Scope.md) §3): ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ **cắt hẳn, không có trong Full Scope**.

## Mục lục

1. [Business goal](#1-business-goal)
2. [Phạm vi module](#2-phạm-vi-module)
3. [Yêu cầu nghiệp vụ](#3-yêu-cầu-nghiệp-vụ)
4. [Ràng buộc & điều kiện chặn](#4-ràng-buộc--điều-kiện-chặn)
5. [Cái module này KHÔNG làm](#5-cái-module-này-không-làm)
6. [Rủi ro chính](#6-rủi-ro-chính)
7. [Tài liệu liên quan](#7-tài-liệu-liên-quan)

---

## 1. Business goal

Tự động chuyển **scene → page → panel** dưới dạng **Comic IR (Comic Intermediate Representation)**, và **khoá cứng các ràng buộc kỹ thuật vào schema thay vì vào prompt** — cụ thể là trần **≤3 nhân vật/panel** và **`text_safe_zone`**.

Đây là module quyết định *"trang truyện trông như thế nào"* **trước khi** một đồng tiền API nào được tiêu: `Panel Specification` là dữ liệu chính, ảnh chỉ là output phái sinh. Nhờ vậy, sửa một quyết định dàn dựng là **sửa một field**, không phải re-roll cả ảnh. Cùng với Comic IR, output của Layout Director (*selection & arrangement*) là **phần được bảo hộ bản quyền**.

## 2. Phạm vi module

Bảng dưới đây là **nhóm C của [MVP-Scope.md](../../010-Planning/MVP-Scope.md) §3, trích nguyên nhãn từng mốc** — không đổi nhãn, không diễn giải lại nhãn. Sáu hàng `C1`, `C2`, `C3`, `C5`, `C6`, `C7` thuộc phạm vi module; hàng `C4` nằm ở [mục 5](#5-cái-module-này-không-làm).

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ (theo `MVP-Scope` §3) |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **C1** | Comic IR / Panel Specification (spec là dữ liệu chính) | 🟡 YAML tay | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §4.2 ✅ đã giải được — rủi ro thấp nhất bảng |
| **C2** | Director tự động scene → page → panel | ❌ viết tay | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 |
| **C3** | Layout: **rubric `beat_type` + emphasis quota** (rời rạc, bảng tra) | ❌ | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 · CF-9.3 |
| **C5** | Cứng hoá **≤3 nhân vật/panel** trong schema Comic IR | 🟡 kỷ luật tay | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-6.5 `[OFF]` ID-Sim 42.33 (2) → 27.21 (3) → 2.67 (4) → 0.52 (5) |
| **C6** | `text_safe_zone` trong panel spec | ⛔ | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 |
| **C7** | **Hai human gate bắt buộc**: speaker attribution + dialogue condensation | ❌ | ⛔ | ✅ | ✅ | ✅ | ✅ | CF-8.8 — *không phải tuỳ chọn, không dồn sang MVP4* · CF-6.10 lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) `[EM]` |

> Cờ horizon (quy ước **QC-3**): cả sáu hàng **TRONG** horizon 09/2026–02/2027 — `C1` bắt đầu ở MVP0, năm hàng còn lại đạt ✅ ở **MVP2** (01–02/2027 theo `Roadmap` §1.2, ⚠️ `[EM]`).

## 3. Yêu cầu nghiệp vụ

| ID | Phát biểu yêu cầu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-003-01** | Panel được lưu dưới dạng **`Panel Specification` có schema** (bố cục, nhân vật, camera, ràng buộc thị giác, vùng an toàn cho chữ), **không** dưới dạng ảnh. Ảnh là **output phái sinh**; spec là thứ được lưu và sửa. | `MVP-Scope` §3 C1 (dẫn Analysis §4.2) · `Glossary` *Comic IR (Comic Intermediate Representation)*, *Panel Specification* | MVP0 🟡 YAML tay → MVP1 ✅ |
| **BR-003-02** | Hệ thống **tự chia scene thành page và panel**, để người dùng không phải viết tay panel script cho từng chương. | `MVP-Scope` §3 C2 · CF-8.8 · `Roadmap` §2 exit criterion **M2-1** | MVP2 ✅ (MVP0 = ❌ viết tay) |
| **BR-003-03** | Panel quan trọng được cấp diện tích lớn hơn theo **rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota theo chapter** — bố cục **có nhịp** mà không cần một điểm số không kiểm chứng được. | `MVP-Scope` §3 C3 · `MVP-Scope` §4.3 · CF-9.3 · `Glossary` *Layout Score* (mục tiêu giữ, cơ chế bỏ) | MVP2 ✅ |
| **BR-003-04** | Bố cục trang được lưu dưới dạng **toạ độ chuẩn hoá 0–1 trong `page_layout JSONB`** ngay từ MVP; **template chỉ là các preset ghi vào CÙNG schema đó**. Đây là đường nâng cấp **không mất mát** — nếu về sau lên canvas thật thì **không phải migrate dữ liệu**, chỉ thay lớp tương tác. | `MVP-Scope` §4.1 (*"Đường nâng cấp không mất mát"*) · CF-9.1 | MVP2 (cùng `C3`) |
| **BR-003-05** | Panel có **4 nhân vật trở lên bị TỪ CHỐI ở tầng DB** (CHECK constraint), **không phải bị cảnh báo**. Trần **≤3 nhân vật/panel** là ràng buộc **sản phẩm**, không phải tuỳ chọn kỹ thuật. | `MVP-Scope` §3 C5 · CF-6.5 `[OFF]` arXiv 2606.15867 — ID-Sim **42.33** (2) → **27.21** (3) → **2.67** (4) → **0.52** (5), *"near-complete failure beyond three subjects"* · `Charter` §7 **C3** · `Roadmap` §2 **M2-2** | MVP2 ✅ (MVP0 = 🟡 kỷ luật tay) |
| **BR-003-06** | Nếu gate **G1-d** không đạt ngưỡng, trần được **siết xuống ≤2 nhân vật/panel trong schema** (đổi chính hàng `C5`) — không phải giữ ≤3 rồi khuyến nghị. | `MVP-Scope` §7.2 bảng *Kết luận gate*, dòng **PASS CÓ ĐIỀU KIỆN** · CF-6.5 caveat *"ngưỡng có thể siết xuống ≤2"* | Quyết tại **G1** (cuối 09/2026) |
| **BR-003-07** | Cảnh đông người được giải bằng **shot xa / silhouette / crop**, không bằng cách nhồi thêm nhân vật vào một panel. Đây là **giới hạn sản phẩm nhìn thấy được**, phải nói rõ với người dùng. | `Charter` §7 **C3** · CF-6.5 `[OFF]` · [Risk-Register](../../010-Planning/Risk-Register.md#21-bảng-chính) R-12 cột *Residual Risk* | MVP2 |
| **BR-003-08** | `Panel Specification` **khai báo sẵn `text_safe_zone`** — vùng được giữ trống để đặt bubble. Thiếu nó thì bubble che mặt nhân vật và **phải sinh lại toàn bộ ảnh đã làm**. | `MVP-Scope` §3 C6 · CF-8.8 · `Glossary` *`text_safe_zone`* | MVP2 ✅ |
| **BR-003-09** | Ngưỡng nghiệm thu của `text_safe_zone`: **≥95%** panel typeset **không đè vùng mặt**. ⚠️ **`[EM]` — `Roadmap` §2 ghi nguyên văn *"ngưỡng do em định nghĩa"*; cấm trích như số đo hoặc benchmark ngành.** | CF-10.5 (`findings/business-analyst.md` §5.2) · `Roadmap` §2 **M2-3** | MVP2 |
| **BR-003-10** | **Human gate #1 — speaker attribution**: mỗi dòng thoại phải được người xác nhận gán **đúng người nói** trước khi trang được xuất bản. Đây là gate **bắt buộc, không phải tuỳ chọn, không dồn sang MVP4**. | `MVP-Scope` §3 C7 · CF-8.8 · CF-6.10 lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) ⚠️ `[EM]` **ước lượng, KHÔNG phải số đo** · `Glossary` *speaker attribution* (chi phí lỗi **bất đối xứng**) | MVP2 ✅ |
| **BR-003-11** | **Human gate #2 — dialogue condensation**: thoại đã nén phải được người xác nhận trước khi trang được xuất bản, vì nén là **hành vi biên tập CÓ MẤT** (30–80 từ → ~8–20 từ, hệ số **2–5×**). | `MVP-Scope` §3 C7 · CF-8.8 · `Glossary` *dialogue condensation* | MVP2 ✅ |
| **BR-003-12** | **`dialogue condensation` phải chạy SAU layout**, vì `text_budget` phụ thuộc **diện tích panel**. Thứ tự này là ràng buộc, không phải tối ưu hoá. | `Glossary` *dialogue condensation* (*"phải chạy SAU layout"*) · `findings/business-analyst.md` §4.10 (ràng buộc thứ tự giữa hai gate) | MVP2 |
| **BR-003-13** | Tiêu chí đo của hai gate là **sự VẮNG MẶT của một đường code bypass** — không phải sự tồn tại của một màn hình xác nhận. Hai gate chỉ *"xong"* **cùng nhau**, vì đó là thuộc tính của **pipeline xuất bản**. | `Roadmap` §2 exit criterion **M2-4** · `findings/business-analyst.md` §3.1 (*"không tồn tại đường code bypass"*), §4.10 | MVP2 |
| **BR-003-14** | Mỗi lần người dùng xác nhận / sửa ở hai gate phải sinh một **`change_log`** row — xác nhận của con người là **bằng chứng đóng góp trí tuệ**, không chỉ là một bước UI. | `MVP-Scope` §6 **KC-2** · `MVP-Scope` §5.2 (ràng buộc xuyên suốt: *"mọi hành động của người dùng phải sinh một `change_log` row"*) · CF-7.2 `[OFF]` | MVP2 (dữ liệu có từ MVP1) |

> **`TBD` — khoảng trống không nguồn nào trong repo trả lời được** (không được viết thành số):
>
> | # | Khoảng trống | Trạng thái |
> |---|---|---|
> | **KT-7** | Benchmark độc lập đo frontier model ở **2–3 nhân vật/panel** — **KHÔNG TỒN TẠI** trong dữ liệu công khai ⇒ **MVP0 là phép đo đầu tiên**, và nó là đầu vào của BR-003-06 | `TBD` |
> | **G-04** | **Tỉ lệ lỗi thật của speaker attribution.** Con số đang lưu hành (30–50% / 40–60%) ⚠️ là `[EM]`, **không phải số đo** — không có benchmark nào đo speaker attribution trên văn bản truyện chữ tiếng Việt ở cấu hình này | `TBD` — cho tới lúc đó, MVP2 **thiết kế như thể tỉ lệ lỗi ở cận trên** |
> | **KT-1** | ⭐ **KHÔNG CÓ persona / JTBD / định nghĩa "đủ tốt" trong toàn repo** ⇒ *"bố cục có nhịp"* chưa có định nghĩa nghiệm thu nào ngoài CF-10.10 (*"trang này đọc có ổn không?"*, định tính) | `TBD` |
>
> Nguồn xác nhận khoảng trống: `findings/business-analyst.md` §6.2 · [Risk-Register](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống-không-gán-score) §4.1.

## 4. Ràng buộc & điều kiện chặn

### 4.1 Danh sách cứng `KC-x` mà module này chạm (`MVP-Scope` §6)

| # | Ràng buộc | Module C chạm ở đâu |
|---|---|---|
| **KC-2** | `change_log` ghi **mọi** hành động người dùng — kể cả *"chọn generation X thay vì Y"* | Hai human gate của `C7` và mọi lần sửa `Panel Specification` (căn cứ của BR-003-14). *"Prompt một mình không chứng minh được decisive contribution"* |
| **KC-3** | `field_provenance` (mức field) + `generation.origin ENUM('ai','ai_edited','human')` | Panel spec có field do Director sinh và field do người sửa ⇒ phải phân biệt được ranh giới phần được bảo hộ |
| **KC-4** | KC-1 + KC-2 + KC-3 **commit CÙNG MỘT TRANSACTION** với artifact chúng chứng minh | Xác nhận gate + thay đổi panel spec phải commit cùng nhau: *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* |
| **KC-5** | `tenant_id NOT NULL` mọi bảng + **cột đầu tiên** mọi composite index + **RLS** — từ MVP1, ngày đầu | Mọi bảng Comic IR (`page`, `panel`, `page_layout`, dialogue) đều là bảng nghiệp vụ. Cơ chế thuộc [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) |

### 4.2 Ràng buộc cấp dự án `C-x` (`Charter` §7)

| # | Ràng buộc | Hệ quả cho module C |
|---|---|---|
| **C1** | Đội **1 người + AI assist**, không funding `[CHỐT]` CF-1.2 | Layout phải **rời rạc** (bảng tra + template preset), không phải hình học liên tục |
| **C3** | **Trần cứng ≤3 nhân vật/panel**, cứng hoá trong Comic IR `[OFF]` CF-6.5 | Ràng buộc **lõi** của module: BR-003-05, BR-003-06, BR-003-07 |
| **C5** | **Positioning disclosure-first, nhắm writer KHÔNG nhắm artist** | ⛔ **CẤM-17**: cấm đặt requirement cho phân khúc hoạ sĩ. Primary actor là **tác giả truyện chữ không biết vẽ** (CF-1.5 `[CHỐT]`) |
| **C9** | Thứ tự milestone cố định — **MVP2 = Comic Director** CF-8.3 | Không đảo thứ tự để *"làm phần dễ trước"*; ⚠️ bẫy đánh số CF-10.2 |
| **C10** | Horizon 6 tháng **chưa được ai xác nhận là đủ cho 1 dev** `[CHỐT]` CF-8.1 + CF-8.13 | ⛔ **CẤM-08**: cấm nén lịch cho vừa khung. MVP2 là **mốc cuối** còn nằm trong horizon `[EM]` (CF-10.8) |

### 4.3 Điều kiện chặn khác

| Điều kiện | Nội dung |
|---|---|
| **Exit criteria MVP2** (`Roadmap` §2) | **M2-1** Director tự động · **M2-2** CHECK constraint ≤3 nhân vật ở **tầng DB** · **M2-3** **≥95%** panel typeset không đè vùng mặt ⚠️ `[EM]` · **M2-4** **không tồn tại đường code bypass** hai human gate |
| **G1 — Kỹ thuật** (cuối 09/2026) | **G1-d** quyết định trần nhân vật là ≤3 hay ≤2 (BR-003-06). ⚠️ **G1-d là `[EM]` — ngưỡng do writer run trước định nghĩa tại run đó, không có nguồn ngoài** (CF-10.4) |
| **Nguyên tắc chung của mọi gate** | ⛔ **CẤM-16**: **cấm sửa ngưỡng sau khi nhìn thấy kết quả** — *"đó là cách một gate biến thành nghi lễ"* (`MVP-Scope` §7) |
| **G0 — Pháp lý** | ⚠️ **KHÔNG chặn MVP0 và MVP1**; G0 chặn **thương mại hoá** (⛔ **CẤM-10**) |

## 5. Cái module này KHÔNG làm

| # | Không làm | Lý do + căn cứ | Điều kiện mở lại |
|---|---|---|---|
| 1 | ⛔ **`C4` — Layout Score 5 số thực. CẮT HẲN.** Trích nguyên nhãn từng mốc của `MVP-Scope` §3 hàng `C4`: MVP0 **❌** · MVP1 **❌** · MVP2 **❌** · MVP3 **❌** · MVP4 **❌** · **Full Scope ❌ cắt hẳn**. <br><br>**Cặp "giữ mục tiêu, bỏ cơ chế"**: **mục tiêu ĐƯỢC GIỮ** — layout theo narrative importance, tức *bố cục có nhịp*; **cơ chế BỊ BỎ** — 5 số thực. Cơ chế thay thế là **rubric `beat_type` rời rạc + bảng tra deterministic + emphasis quota** — hàng đó đã nằm trong [mục 2](#2-phạm-vi-module) và được phát biểu ở BR-003-03. | CF-9.3 · `MVP-Scope` §4.3: lens research xếp ⚪ *không tìm được prior art*, lens AI/ML phân định **"chưa ai làm vì không đáng"** — *"không có prior art + không kiểm chứng được đúng/sai + có phương án thay thế rẻ hơn cả chục lần"* là **định nghĩa của thứ nên cắt sớm** (NT-3 vế 1) · `Glossary` *Layout Score*: số thực *"không đo được, không calibrate được, tạo cảm giác chính xác giả"* | **KHÔNG có điều kiện mở lại** — `MVP-Scope` §3 ghi ❌ **ở cả cột Full Scope**, tức hạng mục bị **loại khỏi thiết kế**, không phải bị hoãn. (Khác hẳn hàng `B5` của [BRD-002](./BRD-002-Story-Intelligence.md), là **hoãn có điều kiện mở lại**) |
| 2 | **Không làm hình học panel tự do, panel xoay / không chữ nhật, infinite canvas, zoom/pan cả chapter** | Hàng **D2**, thuộc [BRD-004](./BRD-004-Minimum-Editor.md); CF-9.1 — *"chi phí lớn nhất, giá trị tăng thêm nhỏ nhất"*. Layout của module này là **rời rạc**, không cần hình học liên tục (`MVP-Scope` §5.2 thành phần #3) | Theo `MVP-Scope` §5.3 hàng #6 — điều kiện thuộc module D, không thuộc module này |
| 3 | **Không render bubble và chữ** | `Panel Specification` chỉ **khai báo** `text_safe_zone`; việc render bubble + chữ là **typeset layer**, hàng `A2` của [BRD-001](./BRD-001-Image-Generation-Pipeline.md) | — (không bị cắt, chỉ khác chủ) |
| 4 | **Không làm UI sắp trang** (chọn template, đổi chỗ panel, preview) | Đó là **thành phần #3 và #4** của editor tối thiểu (`MVP-Scope` §5.2), thuộc [BRD-004](./BRD-004-Minimum-Editor.md). Module này sở hữu **schema** `page_layout` (BR-003-04), không sở hữu màn hình | — |
| 5 | ⛔ **Không có chế độ "cảnh báo rồi cho qua" cho panel 4+ nhân vật** | `Roadmap` §2 **M2-2** yêu cầu **CHECK constraint ở tầng DB**; CF-6.5 `[OFF]`: attribute binding **thất bại gần hoàn toàn** từ 4 nhân vật ⇒ cảnh báo là để lỗi **thất bại âm thầm** | Không mở lại. Đường duy nhất là **siết xuống ≤2** (BR-003-06), không phải nới lên |
| 6 | ⛔ **Không có đường code nào bỏ qua hai human gate**, kể cả cờ cấu hình, kể cả chế độ "auto-approve" | CF-8.8: hai gate *"không phải tuỳ chọn, không dồn sang MVP4"* · `Roadmap` §2 **M2-4** đo bằng **sự vắng mặt** của đường bypass | Không mở lại trong Full Scope |
| 7 | **Không chạy `dialogue condensation` trước layout** | `text_budget` phụ thuộc diện tích panel (`Glossary` *dialogue condensation*) ⇒ nén trước layout là nén theo một trần không tồn tại | Không mở lại — đây là ràng buộc thứ tự |
| 8 | **Không làm `Continuity Checker`, không autofix layout theo state** | Hàng **H3** thuộc [BRD-008](./BRD-008-Quality-And-Operations.md). ⛔ **CẤM-12**: nghĩa canon là **QA-based selection giữa N candidate** (*"trong N cái này, cái nào consistent hơn"*), **KHÔNG** phải gắn nhãn ✓/✗ từng attribute rồi autofix (`Glossary` *Continuity Checker*; CF-8.10). ⚠️ [R-15](../../010-Planning/Risk-Register.md#21-bảng-chính) nêu hệ quả nếu làm sai: checker *"sửa"* theo state sai ⇒ **tự động làm hỏng đúng những panel đang đúng** | Chỉ nếu Full Scope đổi checker trở lại dạng flag+autofix — điều mà CF-8.10 đã bác |
| 9 | **Không đua tính năng typesetting với đối thủ có funding** | `MVP-Scope` §8.3 · CF-5.2/5.3 `[TC]`: GlobalComix ($13M, mua lại INKR) đánh trục **editor**; comic-studio đánh trục **Story Bible + Timeline State + Continuity**. Phản ứng đúng là *"đổi thông điệp, không đổi sản phẩm"* | Không mở lại như một mục tiêu cạnh tranh |
| 10 | **Không sở hữu `resolveState()` và `getBible()`** | Hai hàm đó thuộc module `story` ([BRD-002](./BRD-002-Story-Intelligence.md)). Module `comic` **chỉ** được gọi `story` qua đúng hai hàm này, enforce bằng **lint rule** (`MVP-Scope` §4.2) | — |

## 6. Rủi ro chính

> [!IMPORTANT]
> Tài liệu này **không tự chấm điểm rủi ro mới** và **không lập thang Probability × Impact riêng**. Thang, Score, Trigger, Mitigation và Owner do [Risk-Register.md](../../010-Planning/Risk-Register.md) sở hữu — bảng dưới đây **chỉ trỏ tới hàng tương ứng**.

| ID | Vì sao nó là rủi ro của module C | Rà tại |
|---|---|---|
| [R-12](../../010-Planning/Risk-Register.md#21-bảng-chính) | ⭐ Multi-character panel 2–3 nhân vật **chưa có benchmark độc lập** — hàng **load-bearing** của cả verdict khả thi, và là đầu vào quyết định trần `≤3` hay `≤2` trong schema | G1 |
| [R-15](../../010-Planning/Risk-Register.md#21-bảng-chính) | Khoá thời gian sai ⇒ panel hồi tưởng render state của hiện tại; và checker sẽ *"sửa"* theo state sai. Module C là **người tiêu dùng** của `resolveState()` | Tại PR/migration đầu tiên chạm schema · G1 |
| [R-18](../../010-Planning/Risk-Register.md#21-bảng-chính) | Đối thủ có funding sở hữu **typesetting / text detection / image cleaning** — đúng phần layout & chữ mà module này chạm | Hàng tháng |
| [R-13](../../010-Planning/Risk-Register.md#21-bảng-chính) | Props là metric **thấp nhất** trong bốn metric của CANVAS; prop mang ý nghĩa cốt truyện phải được khai báo trong spec như một entity riêng | G1 |
| [R-01](../../010-Planning/Risk-Register.md#21-bảng-chính) | Xác nhận ở hai human gate là **bằng chứng pháp lý**; không ghi `change_log` thì **không backfill được** | Tại PR/migration đầu tiên chạm schema |
| [G-04](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống-không-gán-score) · [G-05](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống-không-gán-score) | Hai **khoảng trống không gán Score**: tỉ lệ lỗi thật của speaker attribution; độ phủ thật của Continuity Checker — cả hai là `[EM]`, **không phải số đo** | G1 |

## 7. Tài liệu liên quan

### 7.1 Traceability

| Quan hệ | Tài liệu |
|---|---|
| Implements | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) |
| Chi tiết kỹ thuật | [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) |
| Epic tương ứng (1:1) | [Epic-Comic-Director-And-Layout.md](../../022-User-Stories/Epics/Epic-Comic-Director-And-Layout.md) |
| Use Case liên quan | [UC-03-Review-Panel-Script.md](../Use-Cases/UC-03-Review-Panel-Script.md) · [UC-04-Human-Gate-Speaker-Attribution.md](../Use-Cases/UC-04-Human-Gate-Speaker-Attribution.md) · [UC-05-Human-Gate-Dialogue-Condensation.md](../Use-Cases/UC-05-Human-Gate-Dialogue-Condensation.md) · [UC-08-Arrange-Page-And-Preview.md](../Use-Cases/UC-08-Arrange-Page-And-Preview.md) |
| BRD lân cận được trỏ trong tài liệu này | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) (người tiêu dùng của `Panel Specification`) · [BRD-002](./BRD-002-Story-Intelligence.md) · [BRD-004](./BRD-004-Minimum-Editor.md) · [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) · [BRD-008](./BRD-008-Quality-And-Operations.md) |

### 7.2 Nguồn đã trích

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — §3 nhóm C (nguồn của mục 2 và mục 5 hàng `C4`), §4.1, §4.3, §5.2, §6 KC-2…KC-5, §7.2 G1-d, §8.3
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — §7 ràng buộc C1, C3, C5, C9, C10
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — §2.1 bảng chính (R-01, R-12, R-13, R-15, R-18), §4.1 G-04/G-05, §5 lịch rà soát
- [Roadmap.md](../../010-Planning/Roadmap.md) — §2 M2-1…M2-4
- [Glossary.md](../../999-Resources/Glossary.md) — *Comic IR*, *Panel Specification*, *Layout Director*, *Layout Score*, *`text_safe_zone`*, *dialogue condensation*, *speaker attribution*, *attribute binding*, *Continuity Checker*
- [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) — §4.2, §5.3, §5.6 (**dẫn qua** cột *Căn cứ* của `MVP-Scope` §3 và bảng Canonical Facts; tài liệu này **không sửa** Analysis — CẤM-18)
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — RULE-001

---

_Created by TNMCORE-OS — role `business-analyst`_
_Author: trisjr_
