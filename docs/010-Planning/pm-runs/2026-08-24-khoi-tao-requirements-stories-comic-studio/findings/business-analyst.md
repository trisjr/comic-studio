---
type: findings
role: business-analyst
run: 2026-08-24-khoi-tao-requirements-stories-comic-studio
status: draft
created: 2026-08-24
---

# Findings — `business-analyst` · lens phân rã requirement

> [!IMPORTANT]
> **File run-state cho PM đọc và trích vào `outline.md`. Không phải deliverable.**
>
> **Quy ước nhãn nguồn** (kế thừa nguyên vẹn, **số và nhãn là một cặp không tách rời**):
> `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/phép nhân — **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> **Quy ước anchor**: mỗi hạng mục đề xuất có cột *Anchor nguồn* trỏ tới **mục/hàng cụ thể** của một tài liệu có thật trong repo. Chỗ nào không truy được, ghi nguyên văn `KHÔNG CÓ CĂN CỨ TRONG REPO`.

## Mục lục

1. [Bảng phân rã BRD](#1-bảng-phân-rã-brd)
2. [Trục Epic](#2-trục-epic)
3. [Danh sách Use Case](#3-danh-sách-use-case)
4. [Danh sách User Story](#4-danh-sách-user-story)
5. [Bảng canonical facts nháp](#5-bảng-canonical-facts-nháp)
6. [Mâu thuẫn / khoảng trống](#6-mâu-thuẫn--khoảng-trống)
7. [Nguồn đã đọc](#7-nguồn-đã-đọc)

---

## 0. Ba quyết định quy ước phải chốt TRƯỚC khi PM dựng outline

Ba thứ này chi phối mọi bảng bên dưới. Nếu PM chọn khác, các bảng phải sửa theo.

| # | Quyết định | Đề xuất của em | Lý do |
|---|---|---|---|
| **QC-1** | **Số module là 7 hay 8?** | **8** | Brief của run này ghi *"7 nhóm A–G"*. **`MVP-Scope.md` §3 thực tế có TÁM nhóm**: A, B, C, D, E, F, **G (Pháp lý & compliance)** và **H (Chất lượng & vận hành, H1–H6)**. Chi tiết ở [mục 1.2](#12-delta-so-với-brief--nhóm-h-bị-bỏ-khỏi-bảng-7-module) |
| **QC-2** | **Ngôn ngữ trong tên file** | **ASCII/English cho `{Title}`, tiêu đề H1 tiếng Việt** | `RULE-001` không quy định ngôn ngữ của `{Title}`. Mọi file đang tồn tại trong `docs/` đều dùng tên ASCII (`Charter-Comic-Studio.md`, `MVP-Scope.md`, `Analysis-Market-Competitor-Landscape.md`). Dấu tiếng Việt trong tên file gây rủi ro với anchor link và path. **Đây là đề xuất, không phải rule đã có** |
| **QC-3** | **Cờ horizon của một hạng mục vắt qua biên 02/2027** | Cờ gán theo **mốc đầu tiên hạng mục được giao**, kèm ghi chú *"hoàn tất ở mốc X (NGOÀI)"* | `MVP-Scope.md` §3 dùng `🟡` cho *"có một phần"*. Rất nhiều hàng là `🟡` trong horizon và `✅` ngoài horizon (A2, A3, A4, D1#2, GP-4, H4). Cờ nhị phân thuần sẽ **hoặc** phóng đại **hoặc** xoá mất phần trong horizon |

---

## 1. Bảng phân rã BRD

### 1.1 Tám BRD đề xuất

| BRD | Tên file đề xuất | Business goal (1–2 dòng) | Bao hàng `MVP-Scope §3` | Anchor nguồn |
|---|---|---|---|---|
| **BRD-001** | `BRD-001-Image-Generation-Pipeline.md` | Sinh được panel có nhân vật nhất quán từ một `Panel Specification`, ở chi phí và chất lượng cho phép bán được. Là hàng duy nhất tạo ra artifact khách hàng nhìn thấy. | **A1–A7** | `MVP-Scope.md` §3 nhóm A (7 hàng) · căn cứ từng hàng: CF-8.4, CF-8.11c, CF-3.1/3.4, Analysis §5.5, §6.2, §9b.3 |
| **BRD-002** | `BRD-002-Story-Intelligence.md` | Biến văn bản truyện thô thành **Story Bible** truy vấn được theo thời điểm — đây là tài sản tích luỹ của người dùng và là ứng viên moat thật. | **B1–B5** | `MVP-Scope.md` §3 nhóm B (5 hàng) · CF-8.7 · Analysis §5.1, §5.5 · `Glossary.md` *Story Bible*, *syuzhet vs fabula* |
| **BRD-003** | `BRD-003-Comic-Director-And-Layout.md` | Tự động chuyển scene → page → panel dưới dạng **Comic IR (Comic Intermediate Representation)**, và khoá cứng các ràng buộc kỹ thuật (≤3 nhân vật/panel, `text_safe_zone`) vào schema thay vì vào prompt. | **C1–C7** (C4 = ❌ cắt hẳn) | `MVP-Scope.md` §3 nhóm C · CF-8.8 · CF-6.5 `[OFF]` · CF-9.3 · Analysis §4.2, §5.3, §5.6 |
| **BRD-004** | `BRD-004-Minimum-Editor.md` | Cho người dùng thực hiện — và **ghi lại** — quyết định sáng tạo của con người ở mức tối thiểu đủ để (a) sản phẩm dùng được, (b) thoả Điều 5a NĐ 134/2026. | **D1 (5 thành phần), D7**; D2–D6 hoãn/cắt | `MVP-Scope.md` §3 nhóm D + **§5 toàn bộ** (bảng 5 thành phần bắt buộc + 4 thành phần hoãn) · CF-6.7 `[EM]` · CF-9.1 |
| **BRD-005** | `BRD-005-Multi-Tenancy-And-Platform.md` | Nền multi-tenant an toàn từ commit đầu tiên: `tenant_id` + RLS + storage tách tenant, trên kiến trúc modular monolith. Khối này chiếm **15–25%** effort `[EM]` mà `Request.md` gốc không nhắc một dòng. | **E1–E8** (E6 = ❌ cắt hẳn) | `MVP-Scope.md` §3 nhóm E · §6 KC-5 · CF-6.9 `[EM]` · CF-8.7 · CF-9.2 · Analysis §5.7 |
| **BRD-006** | `BRD-006-Credit-And-Unit-Economics.md` | Đo và cưỡng chế chi phí trước khi nó xảy ra: `usage_event`, credit ledger có HOLD, hard quota, mô hình 3 tầng. Không có tầng này thì một power user xoá margin của bốn user thường. | **F1–F6** | `MVP-Scope.md` §3 nhóm F · §6 KC-7 · CF-2.1→2.7 `[CHỐT]` · CF-3.6/3.7 `[EM]` · CF-6.12 |
| **BRD-007** | `BRD-007-Legal-And-Compliance.md` | Giữ được bảo hộ bản quyền cho tác phẩm **của Founder và của khách hàng**, và giữ được miễn trừ trung gian. Đây là nhóm chứa **rủi ro nhị phân duy nhất** của dự án. | **GP-1 – GP-5** | `MVP-Scope.md` §3 nhóm G (ID nguồn là `GP-1`…`GP-5`, **không phải G1…G5** — xem [CF-10.2](#52-bảng-canonical-facts)) · §6 KC-1…KC-4, KC-6 · CF-7.1→7.9 `[OFF]` |
| **BRD-008** ⚠️ | `BRD-008-Quality-And-Operations.md` | Làm cho mọi thay đổi về sau **đo được**: HITL gate, eval kit, golden dataset, preference data, export, abuse control. Không có nhóm này thì mọi thay đổi prompt/model là thay đổi mù. | **H1–H6** | `MVP-Scope.md` §3 nhóm **H** (6 hàng) · CF-8.7, CF-8.10 · CF-6.11 `[EM]` · `findings/architect.md` §7.3 điểm 4 (dẫn qua cột *Căn cứ* của H6) |

### 1.2 Delta so với brief — nhóm H bị bỏ khỏi bảng "7 module"

> [!CAUTION]
> **Đây là đề xuất ĐỔI so với cách brief mô tả `MVP-Scope §3`, không phải đổi so với `MVP-Scope` — tài liệu nguồn vốn đã có 8 nhóm.**

Brief của run liệt kê 7 nhóm A–G. `MVP-Scope.md` §3 có thêm nhóm **`H. Chất lượng & vận hành`** với 6 hàng. Ba hàng trong đó là load-bearing:

| Hàng H | Nội dung | Vì sao không được để rơi |
|---|---|---|
| **H1** | HITL gate + eval kit | CF-8.7 nói **"ngay tại MVP1, không dồn MVP4"**. Đây là điều kiện khả thi **R9** của `Charter` §4 |
| **H2** | Log preference data | Analysis §12 gọi đây là **moat thật** — *"một khoản đầu tư, trả hai lần"*. Gần như miễn phí, nhưng không ghi từ đầu thì mất dữ liệu giai đoạn đầu |
| **H4** | Export PDF / CBZ / webtoon | CF-8.10: *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"* ⇒ đã được **kéo lên sớm**. `Roadmap` §5.2 còn dùng nó làm **điều kiện doanh thu** của Tầng 1 |

**Vì sao em không gộp H vào các nhóm khác**: `Roadmap.md` §2 dùng H1/H2/H6 làm exit criteria của **hai mốc khác nhau** (M1-6 eval kit ở MVP1, P-6 golden dataset ở pre-cycle). Rải H vào A–G làm mất mất khả năng truy một exit criterion về đúng một BRD.

**Nếu PM vẫn muốn giữ đúng 7 BRD**, đây là bảng redistribute — không hàng H nào rơi:

| Hàng H | BRD nhận | Điểm mất khi gộp |
|---|---|---|
| H1 HITL gate + eval kit | BRD-003 (gate nằm ở Director output) | Eval kit vốn đo **cả** output của A và C ⇒ bị gán sai chủ |
| H2 preference data | BRD-007 (dùng chung cơ chế `change_log`) | Mất tính chất "moat", chỉ còn đọc như compliance |
| H3 Continuity Checker | BRD-001 (là N-candidate selection) | Hợp lý nhất trong 6 hàng |
| H4 Export | BRD-004 (tái dùng compositor của preview) | Export là **điều kiện doanh thu** (`Roadmap` §5.2), không phải tính năng editor |
| H5 Abuse controls | BRD-005 | Hợp lý |
| H6 Golden dataset | BRD-001 | Dataset là tài sản xuyên vòng đời, không thuộc pipeline |

### 1.3 Ba hàng KHÔNG sinh requirement — ghi ra để không ai đi tìm

| Hàng | Trạng thái Full Scope | Xử lý |
|---|---|---|
| **C4** Layout Score 5 số thực | ❌ **cắt hẳn** | Không viết requirement. BRD-003 phải có mục *"đã cắt và vì sao"* — CF-9.3, và ghi rõ **mục tiêu được giữ**, cơ chế bị bỏ (`Glossary.md` *Layout Score*) |
| **D6** UI duyệt cây generation | ❌ **cắt hẳn** | Không viết requirement UI. ⚠️ **BRD-004 phải nói tường minh: cắt UI, KHÔNG cắt cột dữ liệu** — `MVP-Scope` §3.1 gọi đây là cặp *"rất dễ bị gộp làm một"* |
| **E6** Microservices + Vector DB riêng | ❌ **cắt hẳn** | Không viết requirement. Thuộc mục *Scope Out* của `Charter` §5.2 |

---

## 2. Trục Epic

### 2.1 Trả lời tường minh: cắt theo **module A–H**, không theo mốc MVP0–MVP4

**Bốn lý do, xếp theo sức nặng:**

| # | Lý do | Anchor |
|---|---|---|
| **1** | **Cắt theo mốc là nhân bản một source of truth đã có chủ.** `MVP-Scope.md` §1.1 phân định rành mạch: *"khi nào"* là việc của `Roadmap.md`, `MVP-Scope` **không** trả lời nó. Epic đặt tên theo MVP1/MVP2 đưa lịch trình vào backlog ⇒ có **hai** nơi nói về thời gian, và chúng lệch nhau ngay lần đầu lịch trượt | `MVP-Scope.md` §1.1 bảng ranh giới ba tài liệu |
| **2** | **Lịch được chính tài liệu nguồn khai là chưa ổn định.** `Roadmap.md` §1.3 xếp *"MVP1 có thể tràn khỏi Q4/2026"* là **rủi ro lịch số 1**, và §2 ghi rõ cột thời gian là **PHÂN BỔ, không phải ƯỚC LƯỢNG**. Epic theo mốc thì trượt lịch = phải đổi tên và cấu trúc lại backlog | `Roadmap.md` §1.3, §2 (note đầu bảng) |
| **3** | **BRD ↔ Epic thành 1:1**, nên traceability là một link, không phải một ma trận | Role memory `MEM-BA-000` §2.B *Traceability Matrix* |
| **4** | **Cùng một module có ràng buộc kỹ thuật dùng chung**. Ví dụ ≤3 nhân vật/panel (C5) và `text_safe_zone` (C6) đều là ràng buộc của schema Comic IR (C1). Cắt theo mốc thì ba thứ này rơi vào ba Epic khác nhau | `MVP-Scope.md` §3 nhóm C |

### 2.2 Đánh đổi của trục KHÔNG chọn — nói thẳng

| Cái mất khi chọn trục module | Mức độ | Giảm nhẹ bằng |
|---|---|---|
| **Epic không map 1:1 với mốc** ⇒ không dùng Epic làm đơn vị lập kế hoạch sprint được. Ví dụ Epic-A có hàng ở MVP0 (A1), MVP1 (A5) và MVP3 (A6, A7) | **Cao** — đây là cái mất thật | Cột *Mốc MVP* và cờ horizon đặt ở **tầng Story**, không ở tầng Epic. Story là đơn vị lập lô |
| **Không có một Epic nào tương ứng "MVP0"** ⇒ mốc quan trọng nhất của horizon không có một cái tên trong backlog | Trung bình | 5 Story mang cờ `[MVP0]` (xem [mục 4.9](#49-năm-story-mvp0--invest-không-áp)). PM có thể dùng **milestone label**, không dùng Epic |
| **Báo cáo tiến độ theo mốc phải aggregate chéo Epic** | Thấp | Query theo cột *Mốc MVP* của Story |
| Trục mốc **thắng** ở một điểm: nó khiến câu *"MVP1 gồm những gì"* trả lời được bằng một link | — | Chấp nhận mất. `Roadmap.md` §2 đã trả lời câu đó bằng cột *Deliverable* + exit criteria M1-1…M1-7 |

### 2.3 Tám Epic đề xuất

> **Cột *Implements PRD*: `PRD-Comic-Studio.md` CHƯA TỒN TẠI** (`docs/020-Requirements/` rỗng). Không link nào ở cột này phân giải được lúc này. **Đề xuất cho PM: cho các mục H2 của PRD phản chiếu đúng 8 module A–H**, khi đó cột này resolve được không cần sửa Epic. Nếu PM chọn cấu trúc PRD khác ⇒ cột này là `TBD`.

| Epic | Tên file đề xuất | Implements PRD (đề xuất) | BRD cha | Mốc MVP (các hàng của nó) | Horizon 09/2026–02/2027 |
|---|---|---|---|---|---|
| **E-A** | `Epic-Image-Generation-Pipeline.md` | PRD §*Pipeline sinh ảnh* | BRD-001 | MVP0 (A1, A2, A3, A4 một phần) · MVP1 (A5) · MVP3 (A6, A7) | **VẮT BIÊN** — 5/7 Story trong, 2/7 ngoài |
| **E-B** | `Epic-Story-Intelligence.md` | PRD §*Story Intelligence* | BRD-002 | pre-cycle (B4) · MVP1 (B1, B2, B3) | **TRONG** — 4/4 Story trong |
| **E-C** | `Epic-Comic-Director-And-Layout.md` | PRD §*Comic Director & Layout* | BRD-003 | MVP0 (C1 YAML tay) · MVP2 (C2, C3, C5, C6, C7) | **TRONG** — 7/7 Story trong |
| **E-D** | `Epic-Minimum-Editor.md` | PRD §*Editor tối thiểu* | BRD-004 | MVP1 (#5) · MVP2 (#3, #4, bắt đầu #2) · MVP3 (#1, D7) | **VẮT BIÊN** — 5/7 trong, 2/7 ngoài |
| **E-E** | `Epic-Multi-Tenancy-And-Platform.md` | PRD §*Multi-tenancy & hạ tầng* | BRD-005 | MVP1 (E1–E5) · MVP3 (E4 billing, E7) | **VẮT BIÊN** — 5/7 trong, 2/7 ngoài |
| **E-F** | `Epic-Credit-And-Unit-Economics.md` | PRD §*Kinh tế & credit* | BRD-006 | MVP1 (F1, F2) · MVP2–MVP3 (F6) · MVP3 (F3, F4) · MVP4 (F5) | **VẮT BIÊN** — 3/6 trong (1 **có điều kiện**), 3/6 ngoài |
| **E-G** | `Epic-Legal-And-Compliance.md` | PRD §*Pháp lý & compliance* | BRD-007 | MVP1 (GP-1, GP-2, GP-5, KC-4) · MVP2 (GP-3) · MVP1🟡→MVP3✅ (GP-4) | **TRONG** — 6/6 Story bắt đầu trong horizon; GP-4 hoàn tất MVP3 |
| **E-H** | `Epic-Quality-And-Operations.md` | PRD §*Chất lượng & vận hành* | BRD-008 | MVP0 (H6, readability) · MVP1 (H1, H2, H5) · MVP2🟡→MVP3 (H4) · MVP4 (H3) | **VẮT BIÊN** — 6/7 trong, 1/7 ngoài |

**Ứng viên cần tách nếu quá to**: `Epic-Minimum-Editor` gánh 5 thành phần độc lập nhau về UI (`MVP-Scope` §5.2) trải 3 mốc. Nếu PM thấy Epic này vỡ, đường tách tự nhiên là **theo thành phần #1–#5**, không theo mốc. Ghi ra để PM quyết, em **không** tự tách.

---

## 3. Danh sách Use Case

### 3.1 Nguyên tắc cắt UC và vì sao con số là **11**

| Nguyên tắc | Hệ quả |
|---|---|
| **Một UC = một tương tác goal-level của một actor** — actor kết thúc UC là đã đạt được một thứ mình muốn | Loại bỏ UC bọc quanh bảng DB. Không có `UC-Manage-Tenant-Table`, không có `UC-Insert-Generation` |
| **Transform deterministic là BƯỚC bên trong UC, không phải UC** | `text clean` (B1), `Story Bible extraction` (B2), `timeline state resolver` (B3), `Visual Prompt Compiler` (A3) đều nằm **trong** UC-01/UC-03/UC-06. Anchor: Analysis §5.5 — code sở hữu state, LLM chỉ phát event |
| **Mỗi human gate bắt buộc phải là một UC riêng** — vì nó là điểm mà `MVP-Scope` yêu cầu *"không tồn tại đường code bypass"* | Sinh ra UC-04 và UC-05. Anchor: `Roadmap.md` §2 exit criterion **M2-4** |
| **Nghĩa vụ pháp lý có actor NGOÀI hệ thống thì phải có UC riêng** | Sinh ra UC-11 (chủ sở hữu quyền gửi takedown). Anchor: GP-3, CF-7.6 `[OFF]` SLA **72 giờ** |

**Vì sao 11, không nhiều hơn**: `Roadmap.md` §5.1 loại **Tầng 2/Tầng 3 có image gen** ra khỏi horizon, và `MVP-Scope` §3 cắt hẳn 4 hàng (C4, D6, E6, và `Layout Score`). Số điểm mà **một con người thật ra một quyết định** trong toàn pipeline `upload → Story Bible → panel script → sinh panel → HITL → typeset → export` là **9**; cộng 2 UC nghĩa vụ ngoài luồng (credit/BYOK, takedown) = **11**. Thêm UC thứ 12 chỉ có hai đường: (a) bọc quanh một bảng DB — bị nguyên tắc 1 loại; (b) tách một UC theo mốc MVP — bị [mục 2.1](#21-trả-lời-tường-minh-cắt-theo-module-ah-không-theo-mốc-mvp0mvp4) loại.

### 3.2 Bảng 11 Use Case

| UC | Tên file đề xuất | Primary actor | Mục tiêu (1 dòng) | BRD module | Mốc MVP | Anchor nguồn |
|---|---|---|---|---|---|---|
| **UC-01** | `UC-01-Upload-And-Ingest-Chapter.md` | **Tác giả truyện chữ** (không biết vẽ) | Đưa một chapter vào hệ thống và biết nó đã sạch, hợp pháp để xử lý | BRD-002 + BRD-007 | MVP1 | `MVP-Scope` §3 B1 (*"text clean là bước ĐẦU TIÊN"*, CF-8.7) + GP-2 · `Roadmap` §2 **M1-2, M1-4** · CF-7.5 `[OFF]` |
| **UC-02** | `UC-02-Review-And-Edit-Story-Bible.md` | Tác giả truyện chữ | Xác nhận / sửa nhân vật, trang phục, địa điểm, state theo event — nơi moat lộ ra với khách | BRD-002 + BRD-004 | MVP1 | `MVP-Scope` §5.2 thành phần **#5** · §3 B2, B3, D1 · `Roadmap` §2 **M1-3** (≥80% `[EM]`) |
| **UC-03** | `UC-03-Review-Panel-Script.md` | Tác giả truyện chữ | Duyệt / sửa panel script (Comic IR) do Director sinh, trước khi tiêu bất kỳ đồng tiền API nào | BRD-003 | MVP0 (viết tay) → MVP2 (tự động) | `MVP-Scope` §3 C1, C2 · `Roadmap` §2 **M2-1** · Analysis §4.2 (Comic IR là hàng rủi ro thấp nhất) |
| **UC-04** | `UC-04-Human-Gate-Speaker-Attribution.md` | Tác giả truyện chữ | Xác nhận mỗi dòng thoại được gán đúng người nói — **gate bắt buộc, không bypass được** | BRD-003 | MVP2 | `MVP-Scope` §3 **C7** · CF-8.8 · CF-6.10 `[EM]` lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) · `Roadmap` §2 **M2-4** |
| **UC-05** | `UC-05-Human-Gate-Dialogue-Condensation.md` | Tác giả truyện chữ | Xác nhận thoại đã nén vừa bubble mà không mất nghĩa — **gate bắt buộc thứ hai** | BRD-003 | MVP2 | `MVP-Scope` §3 **C7** · CF-8.8 · `Glossary.md` *dialogue condensation* (30–80 từ → ~8–20 từ, hệ số **2–5×**, *"phải chạy SAU layout"*) |
| **UC-06** | `UC-06-Generate-Panel-And-Pick-Variant.md` | Tác giả truyện chữ | Sinh panel (best-of-N, N=3) và **chọn** ứng viên — hành động sáng tạo rẻ nhất mà giá trị pháp lý cao nhất | BRD-001 + BRD-004 | MVP0 (script) → MVP3 (có variant picker UI) | `MVP-Scope` §3 A1, A3, A4 · §5.2 thành phần **#1** · CF-3.1/3.2 `[OFF]` · KC-2 |
| **UC-07** | `UC-07-Edit-Bubble-And-Dialogue-In-Panel.md` | Tác giả truyện chữ | Kéo bubble, sửa thoại, chọn kiểu, kéo đuôi trỏ — **trong phạm vi MỘT panel** | BRD-001 + BRD-004 | MVP0 (thô) → MVP2 bắt đầu → MVP3 hoàn tất | `MVP-Scope` §3 A2 · §5.2 thành phần **#2** (ba lý do độc lập a/b/c) · CF-8.11c · `Glossary.md` *typeset layer* |
| **UC-08** | `UC-08-Arrange-Page-And-Preview.md` | Tác giả truyện chữ | Chọn template layout, đổi chỗ panel, xem trang thành phẩm — *selection & arrangement* là phần được bảo hộ | BRD-003 + BRD-004 | MVP2 | `MVP-Scope` §5.2 thành phần **#3** và **#4** · §3 C3, D1 · §4.1 (toạ độ chuẩn hoá 0–1 trong `page_layout JSONB`) |
| **UC-09** | `UC-09-Export-Chapter.md` | Tác giả truyện chữ | Lấy thành phẩm ra khỏi hệ thống (PDF / CBZ / webtoon) | BRD-008 | MVP2 (PDF) → MVP3 (đủ định dạng) | `MVP-Scope` §3 **H4** · CF-8.10 (*"thứ duy nhất người dùng thật sự nhận được"*) · `Roadmap` §2 **M2-5** · `Roadmap` §5.2 (điều kiện doanh thu Tầng 1) |
| **UC-10** | `UC-10-Manage-Credit-And-BYOK.md` | Tác giả truyện chữ (power user) | Nạp / theo dõi credit, hoặc bật BYOK để tự chịu COGS | BRD-006 | MVP3 (credit) · MVP4 (BYOK) — **NGOÀI HORIZON** | `MVP-Scope` §3 F3, F4, F5 · §6 **KC-7** · CF-2.4 `[CHỐT]` · CF-2.5 `[TC]` **~125 ảnh/tháng** · `Roadmap` §5.1 |
| **UC-11** | `UC-11-Handle-Takedown-Request.md` | **Chủ sở hữu quyền (bên ngoài)** — secondary actor: Founder với vai operator | Gửi và được xử lý yêu cầu hạ nội dung trong **SLA 72 giờ**, để nền tảng giữ được miễn trừ Điều 198b | BRD-007 | MVP2 (hoặc sớm hơn nếu trigger đến sớm) | `MVP-Scope` §3 **GP-3** · CF-7.6 `[OFF]` · `Roadmap` §4 **X-a** (neo vào **trigger**, không neo vào ngày) · `Charter` §9.3 **BLOCKER-02** |

### 3.3 Ba UC em **cố ý không** đề xuất — kèm lý do

| UC bị loại | Lý do loại | Nếu PM muốn có thì phải chốt gì |
|---|---|---|
| `UC-Signup-And-Create-Tenant` | E4 = **mua auth, không tự viết** (Analysis §5.7: *"tự viết auth là cách nhanh nhất để một dev đốt hai tháng và vẫn có lỗ hổng"*). Viết UC cho một luồng do vendor sở hữu là viết spec cho thứ mình không điều khiển | Chốt vendor auth trước. UC lúc đó là UC **cấu hình**, không phải UC luồng người dùng |
| `UC-Review-Generation-Tree` | **D6 = ❌ cắt hẳn.** ⚠️ Nhưng dữ liệu lineage KC-1 **vẫn bắt buộc** — nó là NFR/schema requirement, không phải UC | Không mở lại. `MVP-Scope` §6.1 xếp việc gộp hai thứ này là một trong ba hiểu nhầm hay gặp |
| `UC-Run-Continuity-Check` | H3 ở MVP4 và nó **không phải một tương tác của người dùng** — Continuity Checker là **N-candidate selection** bên trong UC-06, không phải một luồng riêng (`Glossary.md` *Continuity Checker*, định nghĩa đã được sửa lại) | Chỉ tách UC nếu Full Scope đổi checker trở lại dạng flag+autofix — điều mà CF-8.10 đã bác |

---

## 4. Danh sách User Story

### 4.0 Cách đọc bảng

- **Cờ horizon** gán theo quy ước **QC-3**: mốc **đầu tiên** Story được giao. Cột *Hoàn tất* nêu mốc mà hàng `MVP-Scope §3` đạt `✅`.
- **INVEST**: chỉ chấm hai chữ mà PM cần cho việc cắt lô — **I** (Independent) và **S** (Small). `⚠️` = em thấy sẽ vỡ.
- **Tổng**: **51 Story** — **41 TRONG HORIZON** (trong đó **1 có điều kiện**) · **10 NGOÀI HORIZON**.

### 4.1 `Epic-Image-Generation-Pipeline` (BRD-001) — 5 trong / 2 ngoài

| Story (tên file) | Câu chuẩn | Mốc | Cờ | Hoàn tất | I | S | Anchor |
|---|---|---|---|---|:-:|:-:|---|
| `Story-Generate-Panel-With-Reference-And-VLM-Select.md` | Là **tác giả truyện chữ**, tôi muốn **sinh 3 ứng viên cho một panel từ ảnh reference rồi để VLM chọn 1**, để **có panel dùng được mà không phải tự chấm từng ảnh** | MVP0 | `[TRONG HORIZON]` | MVP3 | ✅ | ✅ | `MVP-Scope` §3 A1 · CF-8.4 (*"code MVP0 làm đúng một việc này"*) · CF-3.1 `[OFF]` |
| `Story-Typeset-Layer-And-Bubble-Overlay.md` | Là tác giả truyện chữ, tôi muốn **thoại được render bằng overlay layer tách khỏi ảnh**, để **sửa một câu thoại không phải sinh lại ảnh** | MVP0 (thô) | `[TRONG HORIZON]` | MVP3 | ✅ | ⚠️ | `MVP-Scope` §3 A2 · CF-8.11c · exit criterion **G1-e** (100% panel có thoại dùng overlay, **0** panel nhờ model render chữ) |
| `Story-Deterministic-Visual-Prompt-Compiler.md` | Là tác giả truyện chữ, tôi muốn **cùng một `Panel Specification` luôn cho ra cùng một prompt**, để **panel sai là do spec sai, không do hệ thống ngẫu nhiên** | MVP0 (script) | `[TRONG HORIZON]` | MVP3 | ✅ | ⚠️ | `MVP-Scope` §3 A3 · Analysis §5.5 · `Glossary.md` *Visual Prompt Compiler*, *precedence ladder*, *constraint budget* |
| `Story-Image-Provider-Adapter.md` | Là **Founder (operator)**, tôi muốn **đổi image provider bằng cách thay adapter**, để **giá đầu vào của provider không khoá cứng sản phẩm** | MVP0 (1 adapter) | `[TRONG HORIZON]` | MVP3 | ✅ | ✅ | `MVP-Scope` §3 A4 · Analysis §6.2 seam #4 · CF-3.4 `[OFF]` |
| `Story-Job-Queue-In-Postgres.md` | Là Founder (operator), tôi muốn **enqueue job trong cùng transaction với dữ liệu nghiệp vụ**, để **không có job mồ côi và không cần thêm một hạ tầng queue** | MVP1 | `[TRONG HORIZON]` | MVP1 | ✅ | ✅ | `MVP-Scope` §3 A5 (`FOR UPDATE SKIP LOCKED`) · CF-9.2 |
| `Story-Fairness-Per-Tenant-Job-Claim.md` | Là Founder (operator), tôi muốn **một tenant không chiếm hết worker**, để **tenant khác không thấy sản phẩm treo** | MVP3 | `[NGOÀI HORIZON]` | MVP3 | ⚠️ | ✅ | `MVP-Scope` §3 A6 (*"nhồi vào sau là sửa đúng câu SQL nóng nhất"*) · `Glossary.md` *seam kinh tế* |
| `Story-Whole-Page-Render-Granularity.md` | Là Founder (operator), tôi muốn **compile nhiều panel spec thành MỘT prompt whole-page**, để **có đường lui khi gate G2 FAIL mà không đổi data model** | MVP3 | `[NGOÀI HORIZON]` | MVP4 | ✅ | ⚠️ | `MVP-Scope` §3 A7 · §7.3 đường lui #1 · Analysis §9b.3 |

### 4.2 `Epic-Story-Intelligence` (BRD-002) — 4 trong / 0 ngoài

| Story | Câu chuẩn | Mốc | Cờ | I | S | Anchor |
|---|---|---|---|:-:|:-:|---|
| `Story-Fix-Narrative-Time-Key.md` | Là **Founder (architect)**, tôi muốn **khoá thời gian dùng `timeline_id` + `story_order` thay cho `(chapter, scene)`**, để **flashback không làm sai state một cách âm thầm** | **pre-cycle 09/2026** | `[TRONG HORIZON]` | ⚠️ | ✅ | `MVP-Scope` §3 B4 (*"phải sửa TRƯỚC dòng code đầu tiên"*) · Analysis §5.1 · `Roadmap` §3.1 việc 3 + §6.2 (phụ thuộc **cứng**) · `Glossary.md` *syuzhet vs fabula*, *`timeline_id`* |
| `Story-Chapter-Ingest-And-Text-Clean.md` | Là tác giả truyện chữ, tôi muốn **rác scrape bị loại trước khi extraction chạy**, để **Story Bible không sinh entity giả** | MVP1 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 B1 · CF-8.7 · `Roadmap` §2 **M1-2** · `Roadmap` §3.2 bổ sung #1 |
| `Story-Story-Bible-Extraction.md` | Là tác giả truyện chữ, tôi muốn **nhân vật, địa điểm, trang phục được rút ra tự động từ chapter**, để **không phải khai tay toàn bộ Story Bible** | MVP1 | `[TRONG HORIZON]` | ✅ | ⚠️ | `MVP-Scope` §3 B2 · `Roadmap` §2 **M1-3** ngưỡng **≥80%** `[EM]` |
| `Story-Timeline-State-Resolver.md` | Là tác giả truyện chữ, tôi muốn **truy được trạng thái nhân vật tại một thời điểm bất kỳ** (`state_at(N) = reduce(events)`), để **panel ở chương 40 dùng đúng trang phục của chương 40** | MVP1 | `[TRONG HORIZON]` | ⚠️ | ⚠️ | `MVP-Scope` §3 B3 · Analysis §5.5 (code sở hữu state, LLM chỉ phát event) · Analysis §3.3 (4) SCD Type 2 |

> **B5 `pgvector` / vector search: KHÔNG tạo Story.** `MVP-Scope` §3 B5 = `❌` tới MVP2, `⛔` MVP3–MVP4, Full Scope `🟡` *"khi có bằng chứng SQL+FTS không đủ"*. CF-9.2: *"Story Bible **là** index của mình"*.

### 4.3 `Epic-Comic-Director-And-Layout` (BRD-003) — 7 trong / 0 ngoài

| Story | Câu chuẩn | Mốc | Cờ | I | S | Anchor |
|---|---|---|---|:-:|:-:|---|
| `Story-Comic-IR-Panel-Specification.md` | Là tác giả truyện chữ, tôi muốn **panel được lưu dưới dạng spec có schema, không phải dưới dạng ảnh**, để **sửa một field thay vì re-roll cả ảnh** | MVP0 (YAML tay) | `[TRONG HORIZON]` | ⚠️ | ⚠️ | `MVP-Scope` §3 C1 · Analysis §4.2, §3.3 (3) · `Glossary.md` *Comic IR*, *Panel Specification* |
| `Story-Auto-Director-Scene-To-Page-Panel.md` | Là tác giả truyện chữ, tôi muốn **hệ thống tự chia scene thành page và panel**, để **không phải viết tay panel script cho từng chương** | MVP2 | `[TRONG HORIZON]` | ✅ | ⚠️ | `MVP-Scope` §3 C2 · CF-8.8 · `Roadmap` §2 **M2-1** |
| `Story-Layout-Rubric-Beat-Type-And-Emphasis-Quota.md` | Là tác giả truyện chữ, tôi muốn **panel quan trọng được cấp diện tích lớn hơn theo một bảng tra rời rạc**, để **bố cục có nhịp mà không cần một điểm số không kiểm chứng được** | MVP2 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 C3 · §4.3 · CF-9.3 · `Glossary.md` *Layout Score* (cơ chế số thực **đã bị cắt**) |
| `Story-Enforce-Max-Three-Characters-Per-Panel.md` | Là Founder (architect), tôi muốn **panel có 4 nhân vật bị DB TỪ CHỐI, không phải bị cảnh báo**, để **attribute binding không thất bại âm thầm** | MVP2 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 C5 · `Roadmap` §2 **M2-2** (CHECK constraint tầng DB) · CF-6.5 `[OFF]` · `Charter` §7 **C3** |
| `Story-Text-Safe-Zone-In-Panel-Spec.md` | Là tác giả truyện chữ, tôi muốn **panel spec chừa sẵn vùng đặt bubble**, để **bubble không che mặt nhân vật và tôi không phải sinh lại ảnh** | MVP2 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 C6 · CF-8.8 · `Roadmap` §2 **M2-3** ngưỡng **≥95%** `[EM]` · `Glossary.md` *`text_safe_zone`* |
| `Story-Human-Gate-Speaker-Attribution.md` | Là tác giả truyện chữ, tôi muốn **bắt buộc phải xác nhận ai nói câu nào trước khi trang được xuất bản**, để **một dòng gán sai không làm hỏng cả trang** | MVP2 | `[TRONG HORIZON]` | ⚠️ | ⚠️ | `MVP-Scope` §3 C7 · CF-8.8 (*không phải tuỳ chọn*) · CF-6.10 `[EM]` · `Roadmap` §2 **M2-4** |
| `Story-Human-Gate-Dialogue-Condensation.md` | Là tác giả truyện chữ, tôi muốn **bắt buộc phải xác nhận thoại đã nén trước khi trang được xuất bản**, để **việc nén có mất không âm thầm đổi nghĩa lời nhân vật** | MVP2 | `[TRONG HORIZON]` | ⚠️ | ⚠️ | `MVP-Scope` §3 C7 · CF-8.8 · `Roadmap` §2 **M2-4** · `Glossary.md` *dialogue condensation* |

### 4.4 `Epic-Minimum-Editor` (BRD-004) — 5 trong / 2 ngoài

| Story | Câu chuẩn | Mốc | Cờ | Hoàn tất | I | S | Anchor |
|---|---|---|---|---|:-:|:-:|---|
| `Story-Story-Bible-Editor-Form.md` | Là tác giả truyện chữ, tôi muốn **sửa nhân vật / trang phục / địa điểm / state bằng form**, để **kiểm soát được tài sản tích luỹ của mình** | MVP1 | `[TRONG HORIZON]` | MVP1 | ✅ | ⚠️ | `MVP-Scope` §5.2 **#5** (**4–6%** `[EM]`) · §3 D1 |
| `Story-Change-Log-On-Every-Editor-Action.md` | Là Founder (operator), tôi muốn **MỌI hành động trong editor sinh một `change_log` row — kể cả "chọn ảnh này thay ảnh kia"**, để **việc cắt canvas không đồng thời cắt luôn lá chắn pháp lý** | MVP1 | `[TRONG HORIZON]` | MVP1 | ⚠️ | ⚠️ | `MVP-Scope` §5.2 (ràng buộc thiết kế xuyên suốt cả 5 thành phần) · §6 **KC-2** · CF-7.2 `[OFF]` |
| `Story-Page-Template-Layout-And-Swap-Panel.md` | Là tác giả truyện chữ, tôi muốn **chọn template trang và đổi chỗ panel giữa các ô**, để **quyết định sắp đặt là của tôi** (*selection & arrangement*) | MVP2 | `[TRONG HORIZON]` | MVP2 | ✅ | ✅ | `MVP-Scope` §5.2 **#3** (**3–4%** `[EM]`) · §4.1 (toạ độ chuẩn hoá 0–1, **không viết renderer từ đầu**) |
| `Story-Server-Side-Page-And-Chapter-Preview.md` | Là tác giả truyện chữ, tôi muốn **xem trang / chương thành phẩm dưới dạng ảnh composite**, để **thấy thành phẩm trước khi trả tiền** | MVP2 | `[TRONG HORIZON]` | MVP2 | ✅ | ✅ | `MVP-Scope` §5.2 **#4** (**3–5%** `[EM]`, tái dùng compositor của H4) |
| `Story-Bubble-Text-Overlay-Editor.md` | Là tác giả truyện chữ, tôi muốn **kéo bubble và sửa thoại trong phạm vi một panel**, để **sửa chữ không thành một lần đốt tiền API** | MVP2 (bắt đầu) | `[TRONG HORIZON]` | MVP3 | ✅ | ⚠️ | `MVP-Scope` §5.2 **#2** (**5–8%** `[EM]`, *"canvas bị giới hạn trong một khung"*, ba lý do độc lập a/b/c) |
| `Story-Panel-Card-With-Variant-Picker.md` | Là tác giả truyện chữ, tôi muốn **thấy spec + ảnh preview + `Regenerate` + chọn giữa các variant trên một card**, để **vòng lặp iterative của tôi được ghi nhận là hành động sáng tạo** | MVP3 | `[NGOÀI HORIZON]` | MVP3 | ✅ | ⚠️ | `MVP-Scope` §5.2 **#1** (**5–7%** `[EM]`, *"chọn = authorship"*) |
| `Story-Character-Expression-Sheet.md` | Là tác giả truyện chữ, tôi muốn **mỗi nhân vật có sẵn 3 góc + 3 biểu cảm tham chiếu**, để **panel cần biểu cảm khác không phải sinh lại identity** | MVP3 (🟡) | `[NGOÀI HORIZON]` | Full Scope | ✅ | ✅ | `MVP-Scope` §3 **D7** · Analysis §6.3 (*"ứng viên cắt sâu cùng loại"*) |

> **D2 infinite canvas · D3 undo xuyên state · D4 realtime collab · D5 inpainting · D6 UI cây generation: KHÔNG tạo Story.** `MVP-Scope` §5.3 nêu điều kiện mở lại của từng cái. ⚠️ D6 bị **cắt hẳn** nhưng cột dữ liệu KC-1 vẫn bắt buộc — xem `Story-Provenance-Chain-Parent-Generation` ở [mục 4.7](#47-epic-legal-and-compliance-brd-007--6-trong--0-ngoài).

### 4.5 `Epic-Multi-Tenancy-And-Platform` (BRD-005) — 5 trong / 2 ngoài

| Story | Câu chuẩn | Mốc | Cờ | I | S | Anchor |
|---|---|---|---|:-:|:-:|---|
| `Story-Tenant-Id-And-RLS-Everywhere.md` | Là **khách hàng SaaS**, tôi muốn **dữ liệu của tôi không bao giờ lọt sang tenant khác**, để **tôi dám đưa bản thảo chưa công bố của mình vào hệ thống** | MVP1 (**ngày đầu**) | `[TRONG HORIZON]` | ⚠️⚠️ | ⚠️⚠️ | `MVP-Scope` §6 **KC-5** · §3 E1 · CF-8.7 · `Roadmap` §2 **M1-1** (100% bảng + test rò rỉ chéo PASS) · `Glossary.md` *`tenant_id`*, *RLS* |
| `Story-Tenant-User-Membership-As-Three-Entities.md` | Là Founder (architect), tôi muốn **`tenant` / `user` / `membership` là ba entity riêng kể cả khi quan hệ đang là 1:1**, để **ngày bán gói team không phải migrate mô hình định danh** | MVP1 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 E2 · Analysis §5.7 quyết định #2 · §5.3 thành phần 8 (*"`membership` đã chuẩn bị sẵn cho ngày đó"*) |
| `Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md` | Là khách hàng SaaS, tôi muốn **file của tôi nằm ở `tenant/{tenant_id}/{sha256}` và KHÔNG bị dedup chéo tenant**, để **không có ai chia sẻ artifact của tôi một cách vô hình** | MVP1 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 E3 · Analysis §5.7 #4 (*"dedup chéo mâu thuẫn trực tiếp với lập luận bản quyền"*) |
| `Story-Buy-Authentication-Provider.md` | Là Founder (operator), tôi muốn **mua auth thay vì tự viết**, để **không đốt hai tháng và vẫn có lỗ hổng** | MVP1 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 E4 · Analysis §5.7 |
| `Story-Modular-Monolith-Three-Schemas.md` | Là Founder (architect), tôi muốn **1 process, 1 PostgreSQL, 3 schema (`story`/`comic`/`generation`) với luật `comic` gọi `story` CHỈ qua `resolveState()` và `getBible()`**, để **giữ được một transaction boundary cho nghĩa vụ audit** | MVP1 | `[TRONG HORIZON]` | ⚠️ | ⚠️ | `MVP-Scope` §3 E5 · §4.2 (ba lý do mới, đặc biệt lý do 2) · CF-9.2 |
| `Story-Buy-Billing-Provider.md` | Là Founder (operator), tôi muốn **mua billing thay vì tự viết**, để **không tự xây một hệ thống tiền tệ** | MVP3 | `[NGOÀI HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 E4 (`✅ +billing` ở MVP3) · Analysis §5.7 |
| `Story-Worker-As-Separate-Process-Same-Codebase.md` | Là khách hàng SaaS, tôi muốn **worker chết mà API vẫn phục vụ được**, để **một sự cố sinh ảnh không làm tôi mất truy cập vào dữ liệu của mình** | MVP3 | `[NGOÀI HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 E7 (2 entrypoint, **cùng codebase**) · `Roadmap` §2 **M3-4** |

> **E6 microservices + Vector DB riêng: `❌` cắt hẳn.** **E8 SSO/SAML, custom domain, white-label, multi-region: `⛔` Full Scope, không có mốc.** Không tạo Story.

### 4.6 `Epic-Credit-And-Unit-Economics` (BRD-006) — 3 trong (1 có điều kiện) / 3 ngoài

| Story | Câu chuẩn | Mốc | Cờ | I | S | Anchor |
|---|---|---|---|:-:|:-:|---|
| `Story-Usage-Event-And-Daily-Rollup.md` | Là Founder (operator), tôi muốn **mọi lần tiêu tài nguyên được ghi append-only và rollup theo ngày, với regen ratio là metric first-class**, để **không định giá trong bóng tối hàng tháng** | MVP1 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 F1 · CF-8.6 · `Roadmap` §2 **M1-7** (p50/p90 ⇒ G2 chạy được) · `Glossary.md` *`usage_event`* |
| `Story-Generation-Cost-And-Model-Metadata.md` | Là Founder (operator), tôi muốn **mọi `generation` mang `cost_usd` + `model_id` + `model_version` + `attempt_no`**, để **tính được COGS thực và phát hiện được silent model drift** | MVP1 | `[TRONG HORIZON]` | ✅ | ✅ | `MVP-Scope` §3 F2 (*"không backfill được"*) · Analysis §5.7 #3 · `MVP-Scope` §4.4 (seed là **provenance metadata**, không phải replay key) |
| `Story-Tier-1-Sellable-Without-Image-Gen.md` ⚠️ | Là tác giả truyện chữ, tôi muốn **mua gói Story Bible + Comic IR + layout + versioning + export mà KHÔNG có image gen**, để **dùng phần giá trị lõi mà không cần API key** | MVP2–MVP3 | `[TRONG HORIZON — CÓ ĐIỀU KIỆN]` | ⚠️ | ⚠️ | `MVP-Scope` §3 F6 · CF-2.2 `[CHỐT]` (margin ~90%) · ⚠️ `Roadmap` §5.2 — **là một LỰA CHỌN `[EM]`, không phải kế hoạch đã chốt**; gated on **G0 PASS** + M2-5 + M2-6 + quyết định của Founder tại G2 |
| `Story-Credit-Ledger-With-Hold-Before-Enqueue.md` | Là khách hàng SaaS, tôi muốn **credit bị HOLD trước khi job vào queue, với reserve 3 credit/panel**, để **10 job đồng thời không cùng vượt trần số dư của tôi** | MVP3 | `[NGOÀI HORIZON]` | ⚠️⚠️ | ⚠️⚠️ | `MVP-Scope` §6 **KC-7** · §3 F3 · CF-6.12 · `Roadmap` §2 **M3-1, M3-2** · §4 **X-b** · `Glossary.md` *credit ledger + hold*, *hold reaper* |
| `Story-Hard-Quota-Enforced-Before-Enqueue.md` | Là Founder (operator), tôi muốn **quota bị cưỡng chế TRƯỚC khi enqueue, không đếm sau**, để **free tier không là một nghĩa vụ tài chính không giới hạn** | MVP3 | `[NGOÀI HORIZON]` | ⚠️ | ✅ | `MVP-Scope` §3 F4 · CF-8.11b · `Roadmap` §2 **M3-3** · `Charter` §9.3 **BLOCKER-03** |
| `Story-BYOK-As-Unlock-Option.md` | Là **tác giả truyện chữ vượt ~125 ảnh/tháng**, tôi muốn **dùng API key của chính tôi**, để **chi phí sinh ảnh của tôi không bị nhân thêm margin của nền tảng** | MVP4 | `[NGOÀI HORIZON]` | ✅ | ⚠️ | `MVP-Scope` §3 F5 · CF-2.4 `[CHỐT]` (**tuỳ chọn MỞ KHOÁ**, không phải điều kiện dùng sản phẩm) · CF-2.5 `[TC]` · `Glossary.md` *BYOK* (⚠️ onboarding friction = rủi ro sản phẩm số 1) |

### 4.7 `Epic-Legal-And-Compliance` (BRD-007) — 6 trong / 0 ngoài

| Story | Câu chuẩn | Mốc | Cờ | Hoàn tất | I | S | Anchor |
|---|---|---|---|---|:-:|:-:|---|
| `Story-Provenance-Chain-Parent-Generation.md` | Là **khách hàng SaaS**, tôi muốn **mọi generation lưu `parent_generation_id` + `relation_kind` + `field_provenance` + `generation.origin`**, để **tôi chứng minh được quyền tác giả của mình theo Điều 5a** | MVP1 | `[TRONG HORIZON]` | MVP1 | ⚠️⚠️ | ⚠️ | `MVP-Scope` §6 **KC-1, KC-3** · §3 GP-1 · CF-7.2/7.3 `[OFF]` · `Roadmap` §2 **M1-5** · `Charter` §9.3 **BLOCKER-04** |
| `Story-Provenance-Committed-In-Same-Transaction.md` | Là khách hàng SaaS, tôi muốn **`generation` + `change_log` + `usage_event` commit CÙNG MỘT transaction**, để **bằng chứng của tôi không thể thiếu ngẫu nhiên** | MVP1 | `[TRONG HORIZON]` | MVP1 | ⚠️⚠️ | ⚠️⚠️ | `MVP-Scope` §6 **KC-4** · §4.2 lý do 2 · `Roadmap` §2 **M1-5** (*"có test chứng minh"*) |
| `Story-Opt-Out-Check-At-Ingest.md` | Là Founder (operator), tôi muốn **kiểm opt-out signal Điều 37b ngay tại bước ingest**, để **hệ thống không xử lý nội dung có opt-out trước khi biết** | MVP1 | `[TRONG HORIZON]` | MVP1 | ✅ | ✅ | `MVP-Scope` §6 **KC-6** · §3 GP-2 · CF-7.5 `[OFF]` (chi phí ~0) · `Roadmap` §2 **M1-4** (100% file upload) |
| `Story-ToS-User-Warrant-And-Tenant-Hard-Delete.md` | Là khách hàng SaaS, tôi muốn **có đường xoá cứng toàn bộ dữ liệu tenant của tôi đã được kiểm thử**, để **quyền rút khỏi hệ thống là quyền thực thi được, không phải lời hứa** | MVP1 | `[TRONG HORIZON]` | MVP1 | ✅ | ⚠️ | `MVP-Scope` §3 GP-5 (`ON DELETE CASCADE`) · Analysis §5.7 #5 (*"takedown SẼ đến"*) · `MVP-Scope` §8.2 (nghĩa vụ khi KILL) |
| `Story-Safe-Harbour-Checklist-Article-198b.md` | Là **chủ sở hữu quyền (bên ngoài)**, tôi muốn **có công cụ takedown và một đầu mối đã đăng ký với Bộ VHTTDL, xử lý trong SLA 72 giờ**, để **yêu cầu của tôi được xử lý theo luật** | MVP2 | `[TRONG HORIZON]` | MVP2 | ✅ | ⚠️ | `MVP-Scope` §3 GP-3 · CF-7.6 `[OFF]` · CF-8.11a · `Roadmap` §4 **X-a** (neo vào **trigger**: *trước lần đầu mở cho NGƯỜI NGOÀI upload*) · `Roadmap` §2 **M2-6** |
| `Story-AI-Disclosure-Article-11.md` | Là **độc giả / cơ quan quản lý**, tôi muốn **nội dung do AI tạo được đánh dấu**, để **nền tảng tuân thủ Luật TTNT 2025 trước deadline ~01/03/2027** | MVP1 (🟡) | `[TRONG HORIZON]` | MVP3 | ✅ | ⚠️ | `MVP-Scope` §3 GP-4 · CF-7.7 `[OFF]` ⚠️ **hai nguồn mô tả phạm vi KHÁC NHAU** · `Charter` §7 **C4** (thiết kế theo diễn giải **rộng** cho tới khi luật sư chốt) |

> **Không có Story cho G0 (ba câu hỏi luật sư).** Đó là **hoạt động**, không phải increment sản phẩm — `Roadmap` §3.1 việc 1 và §2 exit criterion **P-1** đã sở hữu nó. Đưa nó vào backlog là biến một blocker thành một ticket có thể "dời sprint sau".

### 4.8 `Epic-Quality-And-Operations` (BRD-008) — 6 trong / 1 ngoài

| Story | Câu chuẩn | Mốc | Cờ | Hoàn tất | I | S | Anchor |
|---|---|---|---|---|:-:|:-:|---|
| `Story-Golden-Dataset-For-Regression.md` | Là Founder (operator), tôi muốn **một golden dataset 15–20 panel có spec + ref + ảnh + bảng chấm**, để **mọi thay đổi prompt/model về sau đo được thay vì đoán** | MVP0 | `[TRONG HORIZON]` | MVP0 | ✅ | ✅ | `MVP-Scope` §3 **H6** (✅ ở **mọi** mốc) · `Roadmap` §2 **P-6** · §6.2 (chặn **mềm** eval kit M1-6) |
| `Story-Record-Readability-Human-Judgement.md` | Là Founder (operator), tôi muốn **cạnh mọi metric kỹ thuật có đúng một câu người trả lời — *"trang này đọc có ổn không?"* — và câu trả lời được GHI LẠI từ MVP0**, để **hệ thống không pass mọi check trong khi không ai muốn đọc** | MVP0 | `[TRONG HORIZON]` | liên tục | ✅ | ✅ | **Analysis §3.2** (đoạn *"→ Sửa cái gì"*) — *"vừa là metric chất lượng thật, vừa là dữ liệu preference cho moat"* |
| `Story-HITL-Gate-And-Eval-Kit.md` | Là Founder (operator), tôi muốn **HITL gate và eval kit có ngay ở MVP1**, để **mọi thay đổi prompt/model về sau không phải thay đổi mù** | MVP1 | `[TRONG HORIZON]` | MVP1 | ✅ | ⚠️ | `MVP-Scope` §3 **H1** · CF-8.7 (*"ngay tại MVP1, không dồn MVP4"*) · `Charter` §4 **R9** · `Roadmap` §2 **M1-6** · `Glossary.md` *HITL gate*, *eval kit* |
| `Story-Log-Preference-Data.md` | Là Founder (operator), tôi muốn **mọi lần người dùng chấp nhận/từ chối một gợi ý được ghi làm preference data**, để **moat thật được tích luỹ từ ngày đầu bằng đúng cơ chế mà luật đã buộc phải có** | MVP1 | `[TRONG HORIZON]` | MVP1 | ⚠️ | ✅ | `MVP-Scope` §3 **H2** · CF-8.7 · Analysis §12 (*"một khoản đầu tư, trả hai lần"*) · `Glossary.md` *preference data* |
| `Story-Minimum-Abuse-Controls.md` | Là Founder (operator), tôi muốn **rate limit/tenant, giới hạn upload, log provider từ chối**, để **tín hiệu abuse xuất hiện sớm khi nó gần như miễn phí** | MVP1 (🟡) | `[TRONG HORIZON]` | MVP2 | ✅ | ✅ | `MVP-Scope` §3 **H5** · Analysis §5.7 · ⚠️ `Roadmap` §4 X-b lưu ý phạm vi: *"abuse control cho upload thì cần ngay ở MVP1"* |
| `Story-Export-Chapter-To-PDF-CBZ-Webtoon.md` | Là tác giả truyện chữ, tôi muốn **xuất chương ra PDF / CBZ / webtoon**, để **tôi thật sự nhận được một thứ ra khỏi hệ thống** | MVP2 (PDF) | `[TRONG HORIZON]` | MVP3 | ✅ | ⚠️ | `MVP-Scope` §3 **H4** · CF-8.10 · `Roadmap` §2 **M2-5** (PDF của 1 chapter hoàn chỉnh) · `Roadmap` §5.2 |
| `Story-Continuity-Checker-As-N-Candidate-Selection.md` | Là tác giả truyện chữ, tôi muốn **checker trả lời *"trong N cái này cái nào consistent hơn"*, không phải *"panel này đúng hay sai"***, để **tôi không bị flood bởi false positive** | MVP4 | `[NGOÀI HORIZON]` | MVP4 | ⚠️ | ⚠️ | `MVP-Scope` §3 **H3** · CF-8.10 · CF-6.11 `[EM]` **40–60% số panel** · `Roadmap` §2 **M4-1, M4-2** · `Glossary.md` *Continuity Checker* (định nghĩa **đã được sửa lại**) |

### 4.9 Năm Story MVP0 — INVEST không áp

> [!WARNING]
> `MVP-Scope` §3.1 và `Roadmap` §3.1 đều ghi kỷ luật bắt buộc: **code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi bỏ, giữ lại kết luận và dữ liệu.**
>
> Với 5 Story sau, chấm INVEST là **chấm sai đối tượng**: chúng không cần `Independent` (chúng là một lát cắt xuyên tầng), và tiêu chí `Valuable` của chúng là **thông tin đo được**, không phải tính năng giao cho khách.
>
> `Story-Generate-Panel-With-Reference-And-VLM-Select` · `Story-Typeset-Layer-And-Bubble-Overlay` (bản thô) · `Story-Comic-IR-Panel-Specification` (bản YAML tay) · `Story-Golden-Dataset-For-Regression` · `Story-Record-Readability-Human-Judgement`
>
> **Đề xuất cho PM**: gộp 5 mục này dưới một nhãn `[MVP0]` và **định nghĩa Definition of Done của chúng bằng 5 tiêu chí gate G1** (`MVP-Scope` §7.2) thay vì bằng Acceptance Criteria kiểu Gherkin thông thường. Dùng đúng tên **MVP0** — `Glossary.md` ghi rõ *"một tên duy nhất cho khái niệm này — không dùng 'phase 0', 'spike', 'PoC'"*.

### 4.10 Bảy Story sẽ VỠ khi cắt lô — PM cần biết trước

| Story | Vỡ ở chữ nào | Vì sao và không cắt được theo đường nào |
|---|---|---|
| `Story-Tenant-Id-And-RLS-Everywhere` | **I** và **S** | Chạm **100% bảng nghiệp vụ** + 100% composite index + 100% query. Không có sub-slice nào "xong" mà có nghĩa: `tenant_id` trên 8/10 bảng = **vẫn rò rỉ**. `MVP-Scope` KC-5: *"không có cách nào xác minh đã sửa hết"* ⇒ **DoD phải là test rò rỉ chéo tenant PASS (M1-1), không phải số bảng đã sửa** |
| `Story-Provenance-Chain-Parent-Generation` | **I** | KC-1 + KC-3 gắn với nhau về giá trị pháp lý: có `parent_generation_id` mà thiếu `field_provenance` ⇒ **không xác định được ranh giới phần được bảo hộ**. Cắt thành hai lô cho ra hai lô đều không đủ chứng minh Điều 5a |
| `Story-Provenance-Committed-In-Same-Transaction` | **I** và **S** | **KC-4 là một thuộc tính của ba Story khác**, không phải một feature. Nó phụ thuộc `Story-Modular-Monolith-Three-Schemas` (một DB) và bị chứng minh bằng một **test**, không bằng một màn hình |
| `Story-Credit-Ledger-With-Hold-Before-Enqueue` | **I** và **S** | KC-7 là một **bộ ba không tách**: hold trước enqueue + `CHECK (available >= 0)` ở tầng DB + **hold reaper**. Ship 2/3 sinh ra lỗi tệ hơn không ship: thiếu reaper ⇒ *"có credit mà không generate được"* — `Glossary.md` gọi đây là **loại lỗi khó chẩn đoán nhất** |
| `Story-Human-Gate-Speaker-Attribution` + `Story-Human-Gate-Dialogue-Condensation` | **I** | Cả hai được đo bằng **M2-4: sự VẮNG MẶT của đường code bypass**. Đó là thuộc tính của **pipeline xuất bản**, không của một màn hình ⇒ hai Story này chỉ "xong" cùng nhau. Thêm ràng buộc thứ tự từ `Glossary.md`: dialogue condensation **phải chạy sau layout** |
| `Story-Change-Log-On-Every-Editor-Action` | **I** và **S** | Cross-cutting qua **cả 5 thành phần editor** (`MVP-Scope` §5.2 ràng buộc xuyên suốt) ⇒ mỗi Story editor mới đều mở lại Story này. **Đề xuất: đưa nó thành Definition of Done của Epic-D, không phải một Story** |
| `Story-Fix-Narrative-Time-Key` | **I** | Nó nằm **trong khoá** của mọi bảng timeline (`Roadmap` §6.2: phụ thuộc **cứng**). Làm sau MVP1 = migration toàn bộ. Nó là **điều kiện tiên quyết**, không phải một lô song song |

---

## 5. Bảng canonical facts nháp

### 5.1 Hai nguyên tắc trước khi đọc bảng

1. **Em KHÔNG lập một hệ đánh số mới.** `outline.md` của run 2026-08-23 đã có bảng **CF-1 → CF-9**, và cả 4 tài liệu Planning đang trích theo id đó. Bảng dưới đây **giữ nguyên id gốc** cho các fact đã có, và chỉ đề xuất id mới `CF-10.x` cho fact **có trong `MVP-Scope`/`Roadmap` nhưng chưa có trong bảng CF** — cột đó ghi `[MỚI]`, **PM sở hữu quyết định đánh số**.
2. **Bảng này chỉ chứa fact dùng ở >1 tài liệu sắp viết** (PRD, SRS, NFR, 8 BRD, 11 UC, 8 Epic, 51 Story). Fact chỉ dùng ở một chỗ đã nằm ở cột *Anchor nguồn* của mục 1–4.

### 5.2 Bảng Canonical Facts

| CF-id | Phát biểu | Giá trị | Nhãn | Tài liệu nguồn + mục | **Cảnh báo BẮT BUỘC đi kèm** |
|---|---|---|---|---|---|
| **CF-1.1** | Bản chất sản phẩm | SaaS thương mại multi-tenant — nền tảng cho **người khác tự upload truyện của họ** | `[CHỐT]` | `outline.md` CF-1.1 · `Charter` §1 | — |
| **CF-1.2** | Quy mô đội | **1 người + AI assist**, không funding, không ngân sách marketing | `[CHỐT]` | `outline.md` CF-1.2 · `Charter` §7 C1 | Mọi scope phải chia được cho một người. Kênh phân phối phải là kênh **$0 spend** |
| **CF-1.5** | Phân khúc | **Tác giả truyện chữ (writer) KHÔNG biết vẽ** — *không* nhắm hoạ sĩ | `[CHỐT]` | `outline.md` CF-1.5 · `Charter` §5.2 | Primary actor của **mọi** UC người dùng là actor này. **Cấm** viết UC cho actor "hoạ sĩ" |
| **CF-2.1–2.4** | Mô hình 3 tầng | T1 **$4–8/tháng KHÔNG image gen** (margin ~90%) · T2 **credit pack không hết hạn** (<125 ảnh/tháng) · T3 **BYOK là tuỳ chọn MỞ KHOÁ** | `[CHỐT]` | `outline.md` CF-2.1→2.4 · `Charter` §7 C2 | **BYOK KHÔNG phải điều kiện để dùng sản phẩm.** Kiến trúc billing/ledger/onboarding phải thiết kế cho **ba** tầng ngay từ đầu, không retrofit |
| **CF-2.5** | Ngưỡng phân tuyến | **~125 ảnh/tháng** | `[TC]` | `outline.md` CF-2.5 (vendor blog kompozy.io) | Nguồn là **bên bán managed** nhưng khuyến nghị **ngược chiều lợi ích của họ** ⇒ chấp nhận được. **Không nâng lên `[OFF]`** |
| **CF-2.7** | Tuyệt đối tránh | Subscription phẳng unlimited; free tier kiểu *"100 ảnh/ngày"* | `[OFF]` suy từ CF-3.5 | `outline.md` CF-2.7 · `Charter` §5.2 | ⛔ Mâu thuẫn trực tiếp với R5 và CF-3.7. **Cấm** đưa vào PRD dưới bất kỳ dạng nào |
| **CF-3.1 + CF-3.2** | Hệ số generate | **N = 3**, best-of-N, **mặc định cho MỌI panel** — *"performance saturates at N=3"* | `[OFF]` arXiv 2604.13452 | `outline.md` CF-3.1/3.2 · `MVP-Scope` §7.3 a · `Charter` §7 C8 | ⚠️ **KHÔNG phải retry-on-failure.** **CẤM lấy chất lượng của N=3 mà tính chi phí của N=2.** Hold reserve phải là **3 credit/panel**. Hạ N là đổi chất lượng lấy margin ⇒ **phải chạy lại G1, không phải chỉ G2** |
| **CF-3.3** | Ảnh / chapter | **60** (15 page × 4 panel) | ⚠️ `[EM]` | `outline.md` CF-3.3 · `Charter` §8 A1 | **Giả định của `researcher` run trước, KHÔNG phải số đo.** Là **thừa số gốc** của toàn bộ mô hình chi phí — sai 2 lần thì chi phí/chapter, ngưỡng 125, margin, giá tầng 2 sai theo cùng bội số |
| **CF-3.4** | Giá ảnh | Gemini 3 Pro Image **$0.134** standard / **$0.067** batch · FLUX.2 pro **$0.03** | `[OFF]` | `outline.md` CF-3.4 · `Charter` §6 hàng 5 | Giá đầu vào **do provider đặt, không đàm phán được**. Đổi giá = đổi toàn bộ mô hình |
| **CF-3.5** | Chi phí/chapter @N=3, Gemini batch | **$12,06** | `[EM tính từ OFF]` | `outline.md` CF-3.5 · `Charter` §7 C7 | ⚠️ **Là SÀN, KHÔNG phải trần** — chưa tính VLM call để score 3 candidate. **Cấm dùng $12,06 như chi phí thực tế trong bất kỳ tính toán margin nào mà không nêu nó là sàn** |
| **CF-3.6 / 3.7** | Margin | **−21%** (1 chapter/tháng trên $9.99) · **−262%** (power user 3 chapter/tháng) | `[EM]` | `outline.md` CF-3.6/3.7 | Cả hai kế thừa sai số của CF-3.3 |
| **CF-3.9** | 1 chapter @N=3 | **180 ảnh** — vượt ngưỡng 125 **ngay ở chapter đầu tiên** | `[EM]` 60 × 3 | `outline.md` CF-3.9 · `MVP-Scope` §7.3 g | Kế thừa sai số CF-3.3. ⚠️ Hệ quả phải ghi vào PRD: **BYOK có thể không còn là "tuỳ chọn mở khoá" trên thực tế** — `MVP-Scope` G2-d gọi đây là *"một phát hiện phải ghi lại, không phải một lỗi đo"* |
| **CF-3.10** | Kỳ vọng gross margin | **50–60%**, không phải 80% | `[BCN]` ICONIQ 52%, Bessemer 50–60% | `outline.md` CF-3.10 · `Charter` §7 C6 | Mọi mô hình đặt mục tiêu >60% là **sai kỳ vọng ngành**, không phải tham vọng |
| **CF-3.11** | Chi phí MVP0 | **~$12** @ $0.134 standard · **~$6** nếu batch — **lấy số cao làm trần an toàn** | `[EM tính từ OFF]` | `outline.md` CF-3.11 · `Roadmap` §1.4 A3 | Trần thực tế lên tới **~$50** nếu lặp nhiều vòng (Analysis §10). Lập ngân sách theo số thấp = hết tiền giữa vòng lặp |
| **CF-4.1** | TAM webtoon | $14,0–18,3B (2026), CAGR 26,3–33,1% | `[BCN]` 7 firm phân kỳ | `outline.md` CF-4.1 · `Charter` §2.1 | ⛔ **CẤM dùng làm căn cứ biện minh dự án hoặc làm neo cho bất kỳ requirement nào.** Nó đo **tiêu thụ nội dung**; comic-studio không lấy tiền từ độc giả. `Charter` §2.1 gọi việc trích nó là **vi phạm ràng buộc Charter, không phải một lựa chọn diễn đạt** |
| **CF-4.4** | SOM năm 1 | **$4K–14K ARR ≈ $300–1.200 MRR**, 30–80 paying user | ⚠️ `[EM]` | `outline.md` CF-4.4 · `Charter` §2.2, §3 MT-5 | Thang **trăm đô/tháng**, không phải nghìn |
| **CF-4.5** | Neo thực tế | **Anifusion**: solo founder, **$833 MRR**, có lãi, **~2 năm** kể từ launch, **$0 marketing** | `[TC]` | `outline.md` CF-4.5 · `Charter` §2.2 | ⚠️ **NGUỒN MÂU THUẪN — GHI CẢ HAI, KHÔNG CHỌN MỘT**: nguồn khác ghi **$5.000/tháng**; giá **$9/mo** (run trước) vs **€20/mo** (vòng delta). `Charter` §2.2: chọn một số rồi trình bày như sự thật *"là chính xác cách một `[EM]` bị rửa thành một `[OFF]`"* |
| **CF-4.6** | Retention band | **GRR 23% / NRR 32%** cho AI-native `<$50/tháng` | `[OFF]` ChartMogul, ~3.500 công ty | `outline.md` CF-4.6 · `Glossary.md` *GRR* | ⚠️ **BA CAVEAT BẮT BUỘC (CF-4.7) — trích con số mà bỏ ba dòng này là TRÍCH SAI.** Đây là **lỗi MAJOR có tiền lệ trong repo** |
| **CF-4.7** | Ba caveat của 23% | (a) cohort AI-native chỉ **~200 công ty**, **n của riêng band không được công bố**; (b) bộ lọc **≥$250K ARR** ⇒ **loại đúng nhóm indie mà comic-studio thuộc về**; (c) dữ liệu **2025**, không phải 2026 | `[OFF]` | `outline.md` CF-4.7 · `Glossary.md` *GRR* callout | Kết luận **chịu lực không phải "AI churn" mà là GIÁ**: cùng dataset, sản phẩm AI trên $250/tháng đạt GRR **70%** |
| **CF-4.8** | Xác nhận độc lập cùng chiều | RevenueCat 10/03/2026: AI app retention 12 tháng **21,1%** vs non-AI **30,7%**, ~115.000 app | `[TC]` | `outline.md` CF-4.8 · `Glossary.md` *payer retention* | ⚠️ **CẤM GỘP với CF-4.6.** GRR đo *đồng doanh thu*, payer retention đo *đầu người* — **không cộng, không lấy trung bình, không so trực tiếp** |
| **CF-4.9** | Luận điểm chưa có bằng chứng | *"Credit pack không hết hạn né được 23% GRR"* | `[EM]` | `outline.md` CF-4.9 · `Charter` §8 A5 | **Là lập luận logic (doanh thu ghi trước), KHÔNG phải số đo.** Không tìm được dữ liệu retention nào cho mô hình credit pack. `Charter`: *"giả định được biện luận nhiều nhất và có bằng chứng ít nhất"* |
| **CF-5.2 / 5.3** | Đối thủ chiến lược | **GlobalComix** $13M (25/03/2026), mua lại **INKR** ⇒ có typesetting / text detection / image cleaning; định vị *"the Figma for comics"* | `[TC]` Publishers Weekly | `outline.md` CF-5.2/5.3 · `MVP-Scope` §8.3 | Họ đánh trục **editor**; comic-studio đánh trục **Story Bible + Timeline State + Continuity**. Hệ quả requirement: **không đua editor** (củng cố CF-9.1) |
| **CF-5.4 / 5.5** | Rủi ro nền tảng | **Constella (WEBTOON)** — convert 3D model → 2D theo nét vẽ của chính creator, miễn phí cho creator của platform | `[TC]` | `outline.md` CF-5.4 · `Charter` §8 A13 | ⚠️ **fetch nguồn FAIL — chưa xác nhận đã ship hay còn là announcement.** Constella nhắm creator **đã biết vẽ**; comic-studio nhắm người **không biết vẽ** — hai phân khúc, nhưng khoảng cách **có thể** hẹp lại |
| **CF-5.6 / 5.7** | Cộng đồng là kênh **có rủi ro ngược** | Naver Webtoon bị **độc giả boycott subscription**; **BlueLine Studio bị buộc vẽ lại** episode | `[TC]` | `outline.md` CF-5.6 · `Charter` §7 C5 | Hệ quả requirement bắt buộc: **positioning disclosure-first, nhắm writer KHÔNG nhắm artist**. Bằng chứng đối trọng: Novelcrafter **220.000+ authors** `[OFF]` |
| **CF-6.1** | Verdict khả thi | **KHẢ THI CÓ ĐIỀU KIỆN — CHÍN điều kiện phải thoả ĐỒNG THỜI** | run trước §4.1 | `outline.md` CF-6.1 · `Charter` §4 (R1–R9) | ⚠️ Analysis §4.1 đặt tiêu đề *"BẢY điều kiện"* — đó là số của **một lens**. **Số phải thoả là CHÍN.** `Charter` §4: *"đếm bảy khi lập kế hoạch là bỏ sót hai điều kiện"* |
| **CF-6.5** | Trần nhân vật | CogCanvas ID-Sim: **42.33** (2) → **27.21** (3) → **2.67** (4) → **0.52** (5); *"near-complete failure beyond three subjects"* | `[OFF]` arXiv 2606.15867 | `outline.md` CF-6.5 · `Charter` §7 C3 · `MVP-Scope` §3 C5 | Sinh ra ràng buộc **sản phẩm** ≤3 nhân vật/panel, **không phải tuỳ chọn kỹ thuật**. Cảnh đông người giải bằng shot xa / silhouette / crop. ⚠️ Ngưỡng có thể siết xuống **≤2** nếu G1-d dưới ngưỡng |
| **CF-6.7 + CF-6.8** | Effort editor | **~20–25%** (editor tối thiểu, **mẫu số SaaS**) · **50–60%** (§14 đầy đủ, **mẫu số công cụ cá nhân**) | `[EM]` cả hai | `outline.md` CF-6.7/6.8 · **`MVP-Scope` §5.1** · `Charter` §8 A6 | ⛔⛔ **HAI MẪU SỐ KHÁC NHAU — CẤM TRỪ 6.8 CHO 6.7.** Phép tính `50–60% − 20–25% = 25–40%` là **SAI VỀ SỐ HỌC** và tạo ra một con số không tồn tại. Điều duy nhất được phép kết luận, giữ nguyên định tính: *"vẫn tiết kiệm được khoảng một nửa effort của hạng mục đắt nhất"* |
| **CF-6.9** | Effort multi-tenancy | **15–25%** | `[EM]` | `outline.md` CF-6.9 · `Charter` §8 A7 | `Request.md` **không nhắc một dòng**. Ước thiếu thì *"nó không lấy chỗ của tính năng — nó lấy chỗ của thời gian không tồn tại"* |
| **CF-6.10** | Speaker attribution | Lỗi **30–50%** (3+ người) / **40–60%** (câu ngắn) | ⚠️ `[EM]` | `outline.md` CF-6.10 · `Charter` §8 A8 | **Ước lượng, KHÔNG phải số đo.** Chi phí lỗi **bất đối xứng** — một dòng gán sai làm hỏng cả trang |
| **CF-6.11** | Độ phủ Continuity Checker | **40–60% số panel** | ⚠️ `[EM]` | `outline.md` CF-6.11 · `Charter` §8 A9 · `Roadmap` §2 M4-2 | **PHẢI nói rõ với user** — *"đừng để họ hiểu là được bảo vệ toàn diện"*. Giấu = lời hứa sản phẩm không giữ được |
| **CF-6.12** | Ràng buộc kiến trúc bắt buộc | Credit ledger + **HOLD trước enqueue** + **reserve 3 credit/panel** + `CHECK (available >= 0)` ở tầng DB + **hold reaper** | `architect` + `researcher` | `outline.md` CF-6.12 · `MVP-Scope` §6 KC-7 | **Check-rồi-gọi là race condition.** Reserve 1 credit rồi tính sau = **hợp lệ hoá số dư âm**. Thiếu reaper ⇒ hold treo **vĩnh viễn** |
| **CF-6.13** | Cache hit rate | **vài % tới ~10%** | ⚠️ `[EM]` `architect` tự khai | `outline.md` CF-6.13 · `Charter` §8 A10 | **Đừng dựa vào cache để cứu margin.** Kế hoạch tài chính nào giả định cache tiết kiệm đáng kể là kế hoạch sai |
| **CF-7.1 / 7.2 / 7.3** | Nền tảng pháp lý | NĐ **134/2026/NĐ-CP** hiệu lực **09/04/2026**, **Điều 5a**: AI-assisted chỉ được bảo hộ nếu con người có *"substantial and decisive intellectual contribution"*; **AI tạo hoàn toàn KHÔNG được bảo hộ**. Kèm nghĩa vụ lưu **prompts, inputs, intermediate drafts** | `[OFF]` | `outline.md` CF-7.1→7.3 · `MVP-Scope` §4.4, §6 KC-1→KC-4 | **KHÔNG BACKFILL ĐƯỢC** — không lưu từ generation đầu tiên thì **vĩnh viễn** không có. `Charter` §9.3 **BLOCKER-04 chặn MỌI THỨ** |
| **CF-7.4** | Điều 37a | Giới hạn TDM ở *"non-commercial purposes at the point of use"* | ⚠️ `[OFF]` **tóm tắt** | `outline.md` CF-7.4 · `MVP-Scope` §7.1 Q1 | ⚠️ **DỰA TRÊN BẢN TÓM TẮT, KHÔNG PHẢI NGUYÊN VĂN** — thuvienphapluat/nhansu trả **403**, IAPP **paywall**. **Luật sư phải đọc nguyên văn.** Cấm viết requirement như thể phạm vi đã rõ |
| **CF-7.5** | Điều 37b | Kiểm **opt-out signal** ngay trong bước **ingest** — chi phí **~0** | `[OFF]` tóm tắt | `outline.md` CF-7.5 · `MVP-Scope` §6 KC-6 | Đây là nơi **DUY NHẤT** file của user lần đầu vào hệ thống. Kiểm ở chỗ khác = đã xử lý nội dung có opt-out **trước khi biết** |
| **CF-7.6** | Điều 198b safe harbour | Công cụ takedown · đăng ký đầu mối với **Bộ VHTTDL** · **SLA 72 giờ** | `[OFF]` tóm tắt | `outline.md` CF-7.6 · `Roadmap` §4 X-a · `Charter` §9.3 BLOCKER-02 | Neo vào **TRIGGER** (*trước lần đầu mở cho người ngoài upload*), **không neo vào ngày**. Một lần upload của người ngoài mà chưa có đường takedown là nghĩa vụ **không rút lại được** |
| **CF-7.7** | Luật TTNT 2025 — AI disclosure | Nghĩa vụ **nội địa Việt Nam**, deadline tuân thủ **~01/03/2027** | `[OFF]` | `outline.md` CF-7.7 · `Charter` §7 C4 · `MVP-Scope` §7.1 Q2 | ⚠️ **HAI NGUỒN MÔ TẢ PHẠM VI KHÁC NHAU** (chỉ *"mô phỏng người thật"* vs **mọi** nội dung AI). Deadline nằm **ngay sau** horizon ⇒ **thiết kế theo diễn giải RỘNG** cho tới khi luật sư chốt |
| **CF-7.8 / 7.9** | Rủi ro nhị phân | Ba câu hỏi Q1/Q2/Q3 phải mang tới luật sư SHTT VN **trước khi thương mại hoá** | run trước §12 | `outline.md` CF-7.8/7.9 · `MVP-Scope` §7.1 · `Charter` §9.1 BLOCKER-01 | **Rủi ro nhị phân DUY NHẤT**: mọi rủi ro khác trả lời sai thì sản phẩm **kém hơn**; ba câu này trả lời sai thì sản phẩm **bất hợp pháp**. ⚠️ **Chặn THƯƠNG MẠI HOÁ, KHÔNG chặn MVP0–MVP1** — `Charter` §9.2 gọi việc đọc sai điều này là *"cách hiểu nhầm đắt nhất"* |
| **CF-8.1** | Horizon | **09/2026 → 02/2027** (6 tháng) | `[CHỐT]` | `outline.md` CF-8.1 · `Roadmap` §1.1 | — |
| **CF-8.3** | Thứ tự milestone | **MVP0 → MVP1 → MVP2 → MVP3 → MVP4**, cố định | `[CHỐT]` | `outline.md` CF-8.3 · `Charter` §7 C9 | **MVP1 = Story Intelligence · MVP3 = Visual Generation.** Không đảo thứ tự để *"làm phần dễ trước"* |
| **CF-8.4 / 8.5 / 8.6** | MVP0 | **1–2 tuần** · **1 chapter duy nhất** · Story Bible + panel script **viết tay** · code đúng một việc. Đo 3 chỉ số + 2 chỉ số bổ sung | run trước §10 | `outline.md` CF-8.4→8.6 · `Roadmap` §3.1 việc 2 | ⭐ **Human-reject rate sau VLM-select: CHƯA AI CÔNG BỐ CON SỐ NÀY.** Kỷ luật bắt buộc: **code của MVP0 KHÔNG phải nền của sản phẩm** — viết để trả lời câu hỏi rồi **bỏ**. MVP0 **không có database** |
| **CF-8.12** | Nguyên tắc bao trùm | **Sinh một ảnh trong tuần đầu tiên**, dù bằng tay, dù chỉ 8 panel | run trước §10 | `outline.md` CF-8.12 · `MVP-Scope` §2 NT-1 | Bất kỳ hạng mục nào **trì hoãn** thời điểm sinh ra tấm ảnh đầu tiên đều bị đẩy ra sau MVP0, **kể cả khi nó là nền móng kiến trúc đúng** |
| **CF-8.13** | Ràng buộc kiểm chứng lịch | **Chưa ai xác nhận 6 tháng đủ cho 1 dev** | ràng buộc PM | `outline.md` CF-8.13 · `Roadmap` §1.2 | ⛔ **CẤM NÉN LỊCH CHO VỪA KHUNG.** Câu trả lời đã có: **KHÔNG** — MVP3, MVP4 và mọi gói trả phí có image gen **rơi ra ngoài** horizon `[EM]` |
| **CF-9.1** | Canvas editor | **CẮT MỘT PHẦN** — giữ editor tối thiểu 5 thành phần; **HOÃN** infinite canvas, undo xuyên state, realtime collab, inpainting | run trước §6.1 | `outline.md` CF-9.1 · `MVP-Scope` §4.1, §5 | Nghĩa vụ pháp lý đặt lên **tầng DỮ LIỆU**, không đặt lên tầng CANVAS. Đường nâng cấp: layout là **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` từ MVP ⇒ lên canvas không phải migrate. **Không viết renderer từ đầu** |
| **CF-9.2** | Kiến trúc | **CẮT** microservices + Vector DB → **modular monolith** 1 process / 1 PostgreSQL / 3 schema | run trước §6.2 | `outline.md` CF-9.2 · `MVP-Scope` §4.2 | Lý do **MẠNH LÊN dưới SaaS**: (1) RLS không bảo vệ join phía ứng dụng; (2) nghĩa vụ audit đòi **một** transaction boundary — *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*; (3) multi-tenancy đã ăn **15–25%** `[EM]` |
| **CF-9.3** | Layout Score | **CẮT** cơ chế 5 số thực, **GIỮ** mục tiêu → rubric `beat_type` rời rạc + emphasis quota | run trước §6.3 | `outline.md` CF-9.3 · `MVP-Scope` §4.3 | Không có prior art; *"chưa ai làm vì không đáng"*. **Mục tiêu giữ, cơ chế bỏ** — đừng viết requirement như thể cả mục tiêu bị cắt |
| **CF-9.4** | `parent_generation` | **KHÔNG CẮT** — PM run trước **tự thu hồi** khuyến nghị cắt của chính mình | run trước §6.4 | `outline.md` CF-9.4 · `MVP-Scope` §4.4 | ⚠️ **Là một DẤU VẾT QUYẾT ĐỊNH, không phải một khuyến nghị.** `MVP-Scope` §4.4: viết lại thành *"giữ `parent_generation`"* làm **mất đúng phần có giá trị nhất — lý do vì sao một kết luận có vẻ hợp lý lại sai** |
| **CF-10.1** `[MỚI]` | **Bảy mục KHÔNG ĐƯỢC CẮT** | **KC-1** lineage · **KC-2** `change_log` mọi hành động · **KC-3** `field_provenance` + `generation.origin` · **KC-4** cả ba commit **cùng transaction** · **KC-5** `tenant_id` + RLS · **KC-6** opt-out 37b tại ingest · **KC-7** credit ledger + hold + reaper | tổng hợp `[OFF]`+`[CHỐT]` | **`MVP-Scope` §6** · `Roadmap` §2 P-5, §6.2 | **Danh sách duy nhất không mở ra thương lượng scope.** Đề xuất cắt một trong bảy ⇒ câu trả lời mặc định là **không**, và người đề xuất phải bác được cột *"Không giữ thì hỏng thế nào"*. Chung một tính chất: **rẻ khi làm từ đầu, không thể sửa về sau** |
| **CF-10.2** `[MỚI]` | **Bẫy đánh số — hai loại** | (a) `findings/architect.md` §7.2 run trước **đánh số lại** milestone (ở đó *"MVP1"* = Visual Generation Loop) — **CF-8.3 là canon**. (b) Nhóm pháp lý ở `MVP-Scope` §3 có ID **`GP-1`…`GP-5`**, dễ lẫn với **gate `G0`/`G1`/`G2`** | — | **`MVP-Scope` §1.2 callout WARNING** · §3 nhóm G · §7 | **Cấm để hai hệ đánh số lẫn vào nhau.** Trong BRD-007 và mọi UC/Story, viết `GP-n` cho hàng compliance và `G0/G1/G2` cho gate — **không viết tắt `G1` cho `GP-1`** |
| **CF-10.3** `[MỚI]` | Chênh lệch có nguồn của % editor | Cộng 5 thành phần `MVP-Scope` §5.2 ra **20–30%**, không phải **20–25%** | `[EM]` | **`MVP-Scope` §5.2 callout** | Chênh lệch **có từ nguồn** (Analysis §6.1 đưa cả 5 khoảng **và** tổng ~20–25%, không khớp ở biên trên). Con số chuẩn để trích là **~20–25%** của CF-6.7; **đọc biên trên 25% như ước lượng lạc quan**; cần con số thận trọng khi lập ngân sách thời gian ⇒ dùng **30%** |
| **CF-10.4** `[MỚI]` | **Ngưỡng gate G1 do run trước tự định nghĩa** | **G1-a ≥70%** consistency · **G1-b N ≤3** · **G1-c ≤30%** PASS / 30–50% có điều kiện / **>50% FAIL** · **G1-d panel 2 nhân vật ≥60%**; panel 3 nhân vật **đo và báo cáo, không đặt ngưỡng chặn** · **G1-e 100%** panel có thoại dùng overlay, **0** panel nhờ model render chữ | ⚠️ `[EM]` phần lớn | **`MVP-Scope` §7.2** bảng 5 tiêu chí | ⚠️ **G1-c và G1-d là ngưỡng do writer run trước ĐỊNH NGHĨA TẠI RUN ĐÓ, KHÔNG CÓ NGUỒN NGOÀI.** Trích mà bỏ nhãn này ⇒ chúng **mạo danh benchmark ngành**. Nguyên tắc chung: **ngưỡng được định nghĩa TRƯỚC khi đo; không sửa ngưỡng sau khi nhìn kết quả** |
| **CF-10.5** `[MỚI]` | **Ngưỡng exit criteria do Roadmap tự định nghĩa** | **M1-3 ≥80%** entity extraction khớp bible viết tay · **M2-3 ≥95%** panel typeset không đè vùng mặt | ⚠️ `[EM]` | **`Roadmap` §2** bảng lộ trình tổng | Cả hai ghi nguyên văn *"ngưỡng do em định nghĩa"*. **Cấm trích như số đo hoặc benchmark** |
| **CF-10.6** `[MỚI]` | **Ba gate độc lập, không thay thế nhau** | **G0** pháp lý (trước dòng code thương mại đầu tiên) · **G1** kỹ thuật (cuối 09/2026) · **G2** kinh tế (cuối Q4/2026) | `[CHỐT]` khung | **`MVP-Scope` §7.0** · `Roadmap` §6 | *"Một sản phẩm hợp pháp mà không consistency thì vô dụng; consistency tốt mà lỗ mỗi lần dùng thì không sống được; ngon và có lãi mà bất hợp pháp thì không được tồn tại."* **G2 thiếu dữ liệu ⇒ KHÔNG CHẠY ĐƯỢC, không PASS mặc định** |
| **CF-10.7** `[MỚI]` | Đường lui khi G2 FAIL | Whole-page @N=3 → **+40%** margin vs per-panel @N=3 → **−141%** | `[EM]` | **`MVP-Scope` §7.3** đường lui #1 · Analysis §9b.3 | ⚠️ **Hai caveat.** (a) **+40% vẫn DƯỚI dải kỳ vọng 50–60%** — nó cứu tình trạng lỗ, **không** đưa margin về mức chuẩn ngành; *"đừng coi nó là lời giải cuối"*. (b) **Phép so sánh LỆCH HẠNG NGUỒN**: `+40%` là `[EM]` reverse-engineer từ giá công bố của ComicInk, `50–60%` là `[BCN]` ⇒ kết luận *"vẫn dưới chuẩn"* đúng về hướng nhưng **không đủ chắc để làm ngưỡng gate**. ⛔ Đường **KHÔNG được đi**: hạ N từ 3 xuống 1 |
| **CF-10.8** `[MỚI]` | Kết luận horizon | Chứa được: **MVP0** (09/2026) · **MVP1** (10–12/2026) · **MVP2** (01–02/2027). Rơi ra: **MVP3**, **MVP4**, **mọi gói trả phí CÓ image gen** | ⚠️ `[EM]` | **`Roadmap` §1.2, §5.1** | *"Ước lượng của em tại run này. Không có nguồn nào trong bảng CF xác nhận nó."* Trong CF chỉ có **ĐÚNG MỘT thời lượng tuyệt đối** (MVP0 = 1–2 tuần); mọi % effort là **tỉ lệ không có mẫu số person-month** ⇒ câu *"6 tháng có đủ không"* **không thể trả lời bằng phép tính**. Ước lượng bottom-up = **`TBD`** |
| **CF-10.9** `[MỚI]` | Bán được gì trong horizon | **Tầng 1 nằm gọn trong horizon** (≈ MVP1 + MVP2 + export) | ⚠️ `[EM]` | **`Roadmap` §5.2** | ⚠️ **LÀ MỘT LỰA CHỌN, KHÔNG PHẢI KẾ HOẠCH ĐÃ CHỐT.** Cần Founder quyết tại G2. Ba điều kiện: M2-5 export + M2-6 safe harbour + **G0 PASS**. Đánh đổi: có khách thật ⇒ có nghĩa vụ safe harbour thật + support thật, trong khi 1 dev vẫn đang xây MVP3 |
| **CF-10.10** `[MỚI]` | Tiêu chí "đủ tốt" của sản phẩm | Cạnh mọi metric kỹ thuật phải có **đúng một câu người trả lời**: *"trang này đọc có ổn không?"* — và câu trả lời **được ghi lại từ MVP0** | Analysis §3.2 | **Analysis §3.2** đoạn *"→ Sửa cái gì"* | Lỗi *"pass mọi check mà không ai muốn đọc"* là **vô hình đối với chính hệ thống** — Continuity Checker không bắt được, không metric nào trong `Request.md` bắt được. Nó **vừa** là metric chất lượng thật **vừa** là preference data cho moat |

### 5.3 Lệnh cấm tường minh — trích nguyên để writer dán vào tài liệu

| # | Lệnh cấm | Nguồn |
|---|---|---|
| **CẤM-01** | **CẤM TRỪ CF-6.8 CHO CF-6.7.** Hai mẫu số khác nhau (công cụ cá nhân vs SaaS). `50–60% − 20–25%` là sai số học | `MVP-Scope` §5.1 |
| **CẤM-02** | **CẤM dùng TAM $14–18,3B (CF-4.1) làm căn cứ biện minh dự án hoặc neo cho requirement** | `Charter` §2.1 callout WARNING |
| **CẤM-03** | **CẤM lấy chất lượng của N=3 mà tính chi phí của N=2.** Hạ N ⇒ phải chạy lại **G1** | CF-3.2 `[OFF]` · `MVP-Scope` §7.3 callout |
| **CẤM-04** | **CẤM dùng $12,06 (CF-3.5) như chi phí thực tế mà không nêu nó là SÀN** | `Charter` §7 C7 |
| **CẤM-05** | **CẤM gộp CF-4.8 (payer retention 21,1%) với CF-4.6 (GRR 23%)** — hai metric khác nhau, không cộng, không lấy trung bình | `outline.md` CF-4.8 · `Glossary.md` *payer retention* |
| **CẤM-06** | **CẤM trích 23% GRR mà bỏ ba caveat CF-4.7.** Đây là **lỗi MAJOR có tiền lệ** trong repo | `Glossary.md` *GRR* callout |
| **CẤM-07** | **CẤM chọn một số Anifusion rồi trình bày như sự thật** — ghi cả `$833 MRR` và `$5.000/tháng`, cả `$9/mo` và `€20/mo` | `Charter` §2.2 callout CAUTION |
| **CẤM-08** | **CẤM nén lịch cho vừa khung 6 tháng** | CF-8.13 · `Roadmap` §1.2 |
| **CẤM-09** | **CẤM gộp "cắt UI cây generation (D6)" với "cắt lineage (KC-1)".** Hai quyết định độc lập và **trái chiều** | `MVP-Scope` §3.1, §6.1 |
| **CẤM-10** | **CẤM đọc BLOCKER-01 / G0 thành *"phải chờ luật sư mới được viết dòng code đầu tiên"*.** G0 chặn **thương mại hoá**, không chặn MVP0–MVP1 | `Charter` §9.2 · `Roadmap` §6.1 |
| **CẤM-11** | **CẤM dùng tên khác cho MVP0** — không *"phase 0"*, không *"spike"*, không *"PoC"* | `Glossary.md` *MVP0* |
| **CẤM-12** | **CẤM viết Continuity Checker theo nghĩa cũ** (flag ✓/✗ từng attribute + autofix). Nghĩa canon là **N-candidate selection** | `Glossary.md` *Continuity Checker* · CF-8.10 |
| **CẤM-13** | **CẤM viết requirement như thể phạm vi Điều 37a đã rõ** — hiểu biết hiện tại dựa trên **bản tóm tắt, không phải nguyên văn** | CF-7.4 |
| **CẤM-14** | **CẤM lẫn hệ ID `GP-n` (compliance) với `G0/G1/G2` (gate)** | `MVP-Scope` §3 nhóm G vs §7 |
| **CẤM-15** | **CẤM tự tra lại hoặc tự tính lại một con số đã có trong bảng CF.** Nhân/chia hai số CF để tạo số thứ ba **phải gắn nhãn `[EM]`** cho kết quả | `outline.md` quy tắc cứng #1–#3 |
| **CẤM-16** | **CẤM sửa ngưỡng gate sau khi nhìn thấy kết quả** — *"đó là cách một gate biến thành nghi lễ"* | `MVP-Scope` §7 nguyên tắc chung |
| **CẤM-17** | **CẤM đặt requirement cho phân khúc hoạ sĩ** (CF-1.5 + CF-5.6) hoặc cho subscription phẳng unlimited / free tier *"100 ảnh/ngày"* (CF-2.7) | `Charter` §5.2 |
| **CẤM-18** | **CẤM sửa `Analysis-Comic-Studio-Concept.md`** — nó là **dấu vết quyết định tại thời điểm viết**. Tài liệu mới **link sang**, không sửa | `Charter` §10 · `outline.md` bảng Ripple |

---

## 6. Mâu thuẫn / khoảng trống

### 6.1 Hai nguồn trong repo nói khác nhau

| # | Chỗ mâu thuẫn | Hai phía | Xử lý đề xuất |
|---|---|---|---|
| **MT-1** | **Số nhóm trong `MVP-Scope §3`** | Brief run này ghi **7 nhóm A–G**; tài liệu nguồn có **8 nhóm A–H** | PM chốt **QC-1**. Đề xuất: **8 BRD**. Không được để nhóm H rơi ⇒ xem [mục 1.2](#12-delta-so-với-brief--nhóm-h-bị-bỏ-khỏi-bảng-7-module) |
| **MT-2** | **Số điều kiện khả thi** | Analysis §4.1 tiêu đề *"BẢY điều kiện"*; `Charter` §4 + CF-6.1 nói **CHÍN** | Dùng **CHÍN** (R1–R9). `Charter` §4 đã ghi lại lý do khác biệt — **không phân xử lại, chỉ trích** |
| **MT-3** | **Đánh số milestone** | `findings/architect.md` §7.2 run trước: *"MVP1"* = Visual Generation Loop; CF-8.3: **MVP1 = Story Intelligence** | **CF-8.3 là canon.** Xem CF-10.2 |
| **MT-4** | **% effort editor tối thiểu** | Analysis §6.1 cộng 5 thành phần ra **20–30%**; CF-6.7 ghi tổng **~20–25%** | Trích **~20–25%** làm số chuẩn, **ghi lại chênh lệch** (CF-10.3). ⚠️ `MVP-Scope` §5.2 đã cố ý **không âm thầm sửa một trong hai** — giữ nguyên hình dạng đó |
| **MT-5** | **Anifusion** | `$833 MRR` vs `$5.000/tháng`; `$9/mo` vs `€20/mo` | **Ghi cả hai** (CẤM-07) |
| **MT-6** | **Phạm vi khoản 4 Điều 11 Luật TTNT 2025** | Nguồn A: chỉ nội dung *"mô phỏng người thật hoặc sự kiện thực tế"*; nguồn B: **mọi** nội dung AI | Thiết kế theo diễn giải **RỘNG** (`Charter` §7 C4) và ghi `TBD` cho phạm vi thật. Là **câu Q2 của G0** |
| **MT-7** | **Thời điểm bắt đầu nghĩa vụ provenance** | CF-7.3: *"không lưu từ generation đầu tiên thì vĩnh viễn không có"* ⇒ đọc thô là **MVP0**; `MVP-Scope` §3.1 diễn giải *"generation đầu tiên của sản phẩm thật, tức MVP1"* | Dùng diễn giải **MVP1**, nhưng ⚠️ `MVP-Scope` §3.1 **tự khai đây là `[EM]` diễn giải của writer run trước, KHÔNG có trong CF**. Viết requirement phải giữ nhãn đó |

### 6.2 Requirement bắt buộc phải có mà KHÔNG nguồn nào trả lời được ⇒ `TBD`

> PM đưa vào tài liệu dưới dạng `TBD` kèm lý do. **Em không phân xử ngầm.**

| # | Khoảng trống | Chặn tài liệu nào | Nguồn xác nhận khoảng trống |
|---|---|---|---|
| **KT-1** | ⭐ **KHÔNG CÓ persona / JTBD / định nghĩa "đủ tốt" trong toàn repo.** Analysis §3.2 gọi thẳng: `Request.md` *"có data model 13 entity và không có một dòng nào về ai là người dùng, vấn đề gì đang được giải, và 'đủ tốt' nghĩa là gì"*. Repo có **phân khúc** (CF-1.5) nhưng không có persona | **PRD** mục *Người dùng & vấn đề* · mọi UC mục *Preconditions* | Analysis §3.2 (bảng *Có / Không có*) · Analysis §11 OQ3 |
| **KT-2** | **Không có Design partner, không có user interview nào.** `Charter` §6 ghi *"chưa có ai"*; `docs/050-Research/User-Interviews/` rỗng | PRD (validation), NFR (tiêu chí usability) | `Charter` §6 ba lỗ hổng · CF-4.x |
| **KT-3** | **Không có ước lượng bottom-up (WBS/ETA) cho MVP1/MVP2/MVP3** | Sizing của mọi Story · thứ tự backlog | `Roadmap` §1.3 (`TBD` tường minh) · §2 (cột thời lượng là **phân bổ**, không phải ước lượng) |
| **KT-4** | **Hệ số AI assist rút ngắn được bao nhiêu % thời gian của 1 dev cho loại việc này** | Sizing Story | `Roadmap` §1.3: *"Không được dùng 'có AI nên nhanh hơn' làm lý do rút ngắn lịch"* |
| **KT-5** | **Nguyên văn Điều 37a/37b/37c NĐ 134/2026** — cov.gov.vn chỉ có bản giới thiệu; thuvienphapluat + nhansu **403**; IAPP **paywall** | BRD-007, NFR compliance | CF-7.4 · Analysis §11 điểm 6 |
| **KT-6** | **Điều 198b có áp cho SaaS *xử lý/biến đổi* nội dung** (không phải hosting thuần) không — NĐ 17 chỉ nói *"lưu trữ nội dung số theo yêu cầu"* | BRD-007, UC-11 | Analysis §11 điểm 9 · CF-7.8 câu Q3 |
| **KT-7** | **Benchmark độc lập đo frontier model ở 2–3 nhân vật/panel: KHÔNG TỒN TẠI** trong dữ liệu công khai ⇒ **MVP0 là phép đo đầu tiên** | BRD-001, BRD-003, ngưỡng G1-d | CF-6.4 `[OFF]` · Analysis §11 điểm 1 |
| **KT-8** | **Human-reject rate sau VLM-select: CHƯA AI CÔNG BỐ.** CANVAS không báo | BRD-001, BRD-008, ngưỡng G1-c | CF-8.5 (3) · Analysis §11 điểm 2 |
| **KT-9** | **Benchmark định lượng render tiếng Việt có dấu** của bất kỳ image model — chỉ có press coverage. Đặc biệt thiếu số cho chữ chồng hai dấu (*"ế"*, *"ữ"*, *"ượ"*) | NFR (chất lượng typeset), BRD-001 A2 | Analysis §11 điểm 3 |
| **KT-10** | **Tỉ lệ regenerate thực tế trong sản xuất** (khác N=3 của CANVAS) — không có số liệu ngành ⇒ **G2-a không chạy được nếu MVP0+MVP1 không đo** | BRD-006, NFR (quota) | Analysis §11 điểm 5 · CF-8.6 · `Roadmap` §6.2 |
| **KT-11** | **Willingness-to-pay study** cho tác giả web novel với tool adapt truyện — không tìm được. *"Khoảng trống nằm dưới nền của câu 'bán được không'"* | PRD (pricing), BRD-006 | Analysis §11 điểm 12 |
| **KT-12** | **`PRD-Comic-Studio.md` và `SRS-Comic-Studio.md` chưa tồn tại** ⇒ mọi link `Epic → Implements PRD` và `Story → BRD` chưa phân giải được lúc viết | Toàn bộ traceability của run này | `docs/020-Requirements/` rỗng (chỉ MOC + `.gitkeep`) · `RULE-001` §Linking Rules #1, #2 |
| **KT-13** | **KHÔNG CÓ KHUÔN cho BRD / Use Case / Epic / User Story trong repo.** `docs/999-Resources/Templates/` chỉ có `Template-PRD.md` và `Template-SRS.md` | 8 BRD + 11 UC + 8 Epic + 51 Story | Brief run này ghi rõ *"**không có** khuôn cho BRD/UC/Epic/Story"*. `RULE-001` chỉ định naming + frontmatter, **không** định cấu trúc nội dung ⇒ PM phải chốt cấu trúc trong `outline.md`, nếu không 4 loại tài liệu sẽ có 4 hình dạng |
| **KT-14** | **Không có định nghĩa "một Story point là gì" hay trần size** cho dự án này. Role memory `MEM-BA-000` nói *"tốn hơn 5 story points thì phải tách"* — nhưng thang điểm chưa được định nghĩa ở đâu trong repo | Sizing, [mục 4.10](#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước) | `MEM-BA-000` §3 · **KHÔNG CÓ CĂN CỨ TRONG REPO** cho thang điểm |

---

## 7. Nguồn đã đọc

| Tài liệu | Phần đã đọc |
|---|---|
| `docs/010-Planning/MVP-Scope.md` | **toàn bộ 505 dòng** |
| `docs/010-Planning/Charter-Comic-Studio.md` | **toàn bộ 304 dòng** |
| `docs/010-Planning/Roadmap.md` | **toàn bộ 370 dòng** |
| `docs/010-Planning/pm-runs/2026-08-23-khoi-tao-tai-lieu-planning-comic-studio/outline.md` | **toàn bộ 370 dòng** — bảng Canonical Facts CF-1→CF-9 |
| `docs/999-Resources/Glossary.md` | **toàn bộ 128 dòng** |
| `knowledge-base/99-Templates/Documents-Template.md` | **toàn bộ** (RULE-001) — naming convention, frontmatter, linking rules |
| `docs/050-Research/Analysis-Comic-Studio-Concept.md` | mục lục đầy đủ (Grep) · **§3.2, §3.3** (159–208) · **§11, §12** (994–1055). Các mục còn lại **truy qua bảng CF và cột *Căn cứ* của `MVP-Scope` §3** thay vì đọc lại — đúng lý do bảng CF tồn tại (`outline.md` quy tắc cứng #1) |
| `docs/050-Research/Analysis-Market-Competitor-Landscape.md` | ⚠️ **KHÔNG đọc trực tiếp.** Mọi số thị trường/kinh doanh trong mục 5 lấy từ **CF-2, CF-3, CF-4, CF-5** của `outline.md` — là nguồn canon và đã được `Charter` §2 trích. Nếu PM cần fact ngoài phạm vi CF-2→CF-5, phải dispatch đọc file đó |
| `knowledge-base/45-Role-Memory/business-analyst/000-Core-Memory.md` | toàn bộ (Gherkin AC, Traceability Matrix, trần INVEST) |

> ⚠️ **`.agent/roles/business-analyst.md` KHÔNG TỒN TẠI** — `Glob` trên `.agent/**/*.md` trả về 0 file. Persona được lấy từ system prompt của run + role memory `MEM-BA-000`.

---

_Findings by TNMCORE-OS — role `business-analyst`._
_Author: trisjr_
