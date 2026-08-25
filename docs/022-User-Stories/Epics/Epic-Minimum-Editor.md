---
id: EPIC-D
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-D — Editor tối thiểu (module D: Editor & UI)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> ⛔⛔ **CẢNH BÁO MẪU SỐ — đọc trước khi nhìn bất kỳ con số % nào trong tài liệu này** (CẤM-01): **CF-6.7 = ~20–25%** là editor tối thiểu, **mẫu số SaaS** (đã bao gồm multi-tenancy, billing, auth, moderation). **CF-6.8 = 50–60%** là editor đầy đủ, **mẫu số công cụ cá nhân**. **CẤM TRỪ CF-6.8 CHO CF-6.7** — phép tính `50–60% − 20–25% = 25–40%` là **SAI VỀ SỐ HỌC** và tạo ra một con số không tồn tại. Điều **duy nhất** được phép kết luận, giữ nguyên định tính: *"vẫn tiết kiệm được khoảng một nửa effort của hạng mục đắt nhất"*.
>
> ⚠️ Cộng năm khoảng thành phần ở [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md) ra **20–30%**, không phải 20–25% — chênh lệch **có từ nguồn** (CF-10.3) và được ghi lại thay vì âm thầm sửa. Con số chuẩn để trích là **~20–25%** của CF-6.7; **đọc biên trên 25% như một ước lượng lạc quan**; cần con số thận trọng khi lập ngân sách thời gian ⇒ dùng **30%**.
>
> **Trục Epic**: cắt theo **module A–H**, **KHÔNG** theo mốc MVP0–MVP4. ⇒ Cột *Mốc* và cờ horizon nằm ở **tầng Story**, không ở tầng Epic.

## Mục lục

1. [Implements](#1-implements)
2. [Mục tiêu Epic](#2-mục-tiêu-epic)
3. [Story trong horizon](#3-story-trong-horizon)
4. [Story ngoài horizon — chưa có file](#4-story-ngoài-horizon--chưa-có-file)
5. [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Implements

Implements: [PRD-Comic-Studio](../../020-Requirements/PRD-Comic-Studio.md#d-editor--ui)

---

## 2. Mục tiêu Epic

Cho người dùng thực hiện — **và ghi lại** — quyết định sáng tạo của con người, ở mức tối thiểu đủ để (a) sản phẩm dùng được, (b) thoả **Điều 5a NĐ 134/2026** `[OFF]` CF-7.1/7.2/7.3. Nguyên tắc chi phối cả Epic: nghĩa vụ pháp lý *"iterative, interactive process"* đặt lên **tầng DỮ LIỆU (audit event)**, **KHÔNG** đặt lên **tầng CANVAS** (CF-9.1). Một form editor có ghi vết đầy đủ thoả nghĩa vụ đó **y hệt** một canvas editor. ⇒ **UI được tự do chọn cái rẻ; dữ liệu provenance thì không được cắt một dòng nào.** Đường nâng cấp đã được thiết kế sẵn để không mất mát: layout lưu dưới dạng **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` **ngay từ MVP**, template chỉ là preset ghi vào **cùng** schema ⇒ nếu sau này lên canvas thật thì **không phải migrate dữ liệu**, và **không viết renderer từ đầu**.

Epic-D **vắt biên horizon** `[CHỐT]` CF-8.1: một thành phần ở **MVP1** (Story Bible editor — nơi moat lộ ra với khách), ba thành phần ở **MVP2**, và **hai** Story rơi hẳn ra ngoài ở **MVP3** `[EM]` CF-10.8. Đây là **Epic to nhất** trong bốn Epic A–D: nó gánh **5 thành phần độc lập nhau về UI** ([MVP-Scope §5.2](../../010-Planning/MVP-Scope.md)) trải **3 mốc**, cộng một **ràng buộc xuyên suốt** cả năm thành phần. ⚠️ Lens phân tích đã cảnh báo Epic này **có thể vỡ** — xem [mục 5](#5-definition-of-done-cấp-epic), ô *Ghi chú cho PM về việc tách Epic*. Epic **không tự tách**.

---

## 3. Story trong horizon

> **Cột `I` / `S`**: chỉ chấm hai chữ INVEST mà việc cắt lô cần — **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ khi cắt lô ([findings §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)).
>
> **Cột *Mốc*** dùng quy ước `QC-3`: cờ gán theo **mốc đầu tiên** Story được giao. Ký hiệu `TP #n` đi kèm tên Story = **thành phần bắt buộc `#1`–`#5`** của [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md); con số `%` là effort `[EM]` của **chính thành phần đó**, ⛔ **không cộng chúng lại để suy ra một tổng mới** (CF-10.3).

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Story-Bible-Editor-Form](../Backlog/Story-Story-Bible-Editor-Form.md) — TP `#5`, **4–6%** `[EM]` | MVP1 | ✅ | ⚠️ | chưa có file |
| [Story-Change-Log-On-Every-Editor-Action](../Backlog/Story-Change-Log-On-Every-Editor-Action.md) — **ràng buộc xuyên suốt cả 5 TP** | MVP1 → áp cho **mọi** TP về sau | ⚠️ | ⚠️ | chưa có file |
| [Story-Page-Template-Layout-And-Swap-Panel](../Backlog/Story-Page-Template-Layout-And-Swap-Panel.md) — TP `#3`, **3–4%** `[EM]` | MVP2 | ✅ | ✅ | chưa có file |
| [Story-Server-Side-Page-And-Chapter-Preview](../Backlog/Story-Server-Side-Page-And-Chapter-Preview.md) — TP `#4`, **3–5%** `[EM]` | MVP2 | ✅ | ✅ | chưa có file |
| [Story-Bubble-Text-Overlay-Editor](../Backlog/Story-Bubble-Text-Overlay-Editor.md) — TP `#2`, **5–8%** `[EM]` | MVP2 (bắt đầu) → hoàn tất MVP3 (**NGOÀI**) | ✅ | ⚠️ | chưa có file |

**5/5 Story trong horizon có mặt.**

> [!CAUTION]
> **`Story-Change-Log-On-Every-Editor-Action` VẪN LÀ MỘT STORY RIÊNG — và đồng thời là một mục trong [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic). Cả hai chỗ, có chủ ý.**
>
> **Dấu vết quyết định** (giữ lại để không ai "dọn dẹp" nó về sau):
> - Lens phân tích đề xuất **chuyển hẳn** nó thành DoD, với lập luận đúng về mặt kỹ thuật: nó cross-cutting qua **cả 5 thành phần** editor ⇒ mỗi Story editor mới đều mở lại nó ([findings §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md)). [PRD `FR-D-06`](../../020-Requirements/PRD-Comic-Studio.md#d-editor--ui) cũng viết *"về bản chất là Definition of Done của module D, không phải một tính năng rời"*.
> - **PM đã BÁC đề xuất chuyển hẳn.** Hai lý do: (1) nó là **`KC-2`** trong danh sách **bảy mục KHÔNG ĐƯỢC CẮT** của [MVP-Scope §6](../../010-Planning/MVP-Scope.md) — *"danh sách duy nhất không mở ra thương lượng scope"*; (2) **một ràng buộc chỉ tồn tại trong DoD thì không có ai tick nó** — nó không có owner, không có estimate, không xuất hiện trong sprint board, và biến mất khỏi tầm nhìn đúng lúc lịch bắt đầu trượt.
> - ⇒ **Giữ ở CẢ HAI chỗ.** Story để có người làm và có người tick; DoD để không Story editor nào được `Done` mà bỏ nó.
>
> Nội dung: **MỌI** hành động trong editor sinh một `change_log` row — **kể cả** *"chọn ảnh này thay ảnh kia"*. ⚠️ Đây là điều kiện làm cho việc **cắt canvas trở nên HỢP PHÁP**: không có nó thì việc cắt canvas biến thành **cắt luôn lá chắn pháp lý**. ⛔ **KHÔNG BACKFILL ĐƯỢC** — không lưu từ generation đầu tiên thì **vĩnh viễn** không có (CF-7.1/7.2/7.3).

> [!WARNING]
> ⛔ **`D6` ≠ `KC-1` — bẫy chết người của module này (CẤM-09).**
>
> `D6` (**UI duyệt cây generation**) bị **cắt hẳn** ⇒ **không sinh Story UI**. Nhưng **cột dữ liệu lineage `KC-1` VẪN BẮT BUỘC** — đó là NFR/schema requirement, thuộc [Epic-Legal-And-Compliance](./Epic-Legal-And-Compliance.md) (`Story-Provenance-Chain-Parent-Generation`). Hai quyết định này **độc lập và trái chiều**; [MVP-Scope §6.1](../../010-Planning/MVP-Scope.md) xếp việc gộp chúng là một trong ba hiểu nhầm hay gặp nhất.
>
> **`D2` infinite canvas · `D3` undo xuyên state · `D4` realtime collab · `D5` inpainting: KHÔNG tạo Story.** [MVP-Scope §5.3](../../010-Planning/MVP-Scope.md) nêu điều kiện mở lại của từng cái; chúng được ghi tại [PRD mục 6.3](../../020-Requirements/PRD-Comic-Studio.md#63-hoãn-ngoài-mvp--kèm-điều-kiện-mở-lại).

---

## 4. Story ngoài horizon — chưa có file

| Story (link) | Mốc | I | S | Trạng thái tài liệu |
|---|---|:-:|:-:|---|
| `Story-Panel-Card-With-Variant-Picker` — TP `#1`, **5–7%** `[EM]` | MVP3 | ✅ | ⚠️ | chưa có file |
| `Story-Character-Expression-Sheet` — hàng `D7` | MVP3 (🟡) → hoàn tất Full Scope | ✅ | ✅ | chưa có file |

**2/2 Story ngoài horizon có mặt.** Tổng Epic-D = **7 Story** (5 trong / 2 ngoài).

> ⚠️ **Nghịch lý cần PM biết**: thành phần `#1` — **panel card + variant picker** — là *"hành động sáng tạo rẻ nhất mà giá trị pháp lý cao nhất"* (**chọn = authorship**), nhưng nó nằm ở **MVP3, NGOÀI horizon**. Trong horizon, bằng chứng *"iterative, interactive"* của Điều 5a **không** đến từ variant picker mà đến từ `change_log` của bốn thành phần còn lại — thêm một lý do nữa để `Story-Change-Log-On-Every-Editor-Action` **không** bị hạ xuống thành một dòng DoD không ai tick.

---

## 5. Definition of Done cấp Epic

Nguồn: exit criteria của [Roadmap §2](../../010-Planning/Roadmap.md) và danh sách cứng [MVP-Scope §6](../../010-Planning/MVP-Scope.md). Epic-D `Done` khi:

- [ ] **`KC-2` — `change_log` trên MỌI hành động editor**, kể cả *"chọn ảnh này thay ảnh kia"*, áp cho **cả năm** thành phần `#1`–`#5`. ⚠️ **Mục DoD này TỒN TẠI SONG SONG với `Story-Change-Log-On-Every-Editor-Action` ở [mục 3](#3-story-trong-horizon)** — theo quyết định của PM, xem callout ở mục đó. Không Story editor nào được `Done` khi hành động của nó không sinh `change_log` row.
- [ ] **`KC-4`**: `generation` + `change_log` + `usage_event` commit **CÙNG MỘT transaction** — *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"*. Chủ yêu cầu là [Epic-Legal-And-Compliance](./Epic-Legal-And-Compliance.md); editor là **nơi nó bị vi phạm dễ nhất** (một action UI ghi async là đủ để phá).
- [ ] **Story Bible editor (thành phần `#5`, `4–6%` `[EM]`)** chạy được ở **MVP1** — [Roadmap §2](../../010-Planning/Roadmap.md) mốc MVP1 liệt nó ở cột *Deliverable* và cột *Effort*. ⚠️ Hạng mục này **không có exit criterion `M-x` riêng**; `M1-3` (≥80% entity extraction) là criterion của [Epic-Story-Intelligence](./Epic-Story-Intelligence.md), **không** của Epic-D. Lý do nghiệp vụ để nó vẫn là điều kiện `Done` của Epic-D: ngưỡng extraction chỉ có giá trị nếu phần extraction **sai** sửa được bằng UI — đây là **suy luận của PO**, không phải phát biểu của nguồn.
- [ ] **`M2-5`** (export PDF của 1 chapter hoàn chỉnh **từ preview server-side**): điều kiện **dùng chung** với [Epic-Quality-And-Operations](./Epic-Quality-And-Operations.md) (`H4`). Epic-D sở hữu **preview**; Epic-H sở hữu **export**. Preview `Done` khi **compositor tái dùng được** cho export — không phải hai đường render.
- [ ] Layout lưu dưới dạng **toạ độ chuẩn hoá 0–1** trong `page_layout JSONB` ngay từ MVP; template chỉ là **preset ghi vào cùng schema** ⇒ đường lên canvas thật **không cần migrate dữ liệu**. ⛔ **Không viết renderer từ đầu.**
- [ ] Bubble/text overlay editor bị **giới hạn trong phạm vi MỘT panel** — *"canvas bị giới hạn trong một khung"*, **không** phải scene graph tự do. Vượt ranh giới này là đã đi vào `D2` (đã hoãn).
- [ ] ⛔ **Không có** thành phần nào của Epic-D được đánh `Done` bằng lập luận *"UI đã đủ"* khi cột dữ liệu provenance còn thiếu. **UI được chọn cái rẻ; dữ liệu thì không được cắt một dòng nào.**
- [ ] Mọi con số % trong tài liệu con của Epic này giữ **nguyên nhãn `[EM]`** và **nguyên mẫu số**. ⛔ CẤM-01.

### Ghi chú cho PM về việc tách Epic — cần PM quyết, PO không tự tách

| Hạng mục | Nội dung |
|---|---|
| **Cảnh báo đã có** | [findings §2.3](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) xếp `Epic-Minimum-Editor` là **ứng viên cần tách nếu quá to**: nó gánh **5 thành phần độc lập nhau về UI** ([MVP-Scope §5.2](../../010-Planning/MVP-Scope.md)) trải **3 mốc** (MVP1 · MVP2 · MVP3) |
| **Quan sát của PO** | Xác nhận cảnh báo là có cơ sở: đây là Epic **duy nhất** trong bốn Epic A–D có một Story **cross-cutting qua chính bốn Story còn lại của nó**, và là Epic **duy nhất** trải đủ ba mốc |
| **Khuyến nghị của PO** | ⭐ **KHÔNG tách bây giờ.** Quan hệ ba tầng đang là **1:1:1** (module PRD ↔ BRD ↔ Epic — [PRD §8.2](../../020-Requirements/PRD-Comic-Studio.md#82-tám-epic--trục-backlog-cắt-theo-module-ah-không-theo-mốc-mvp)); tách Epic-D thành nhiều Epic **phá ngay tính chất đó** và biến traceability từ **một link** thành **một ma trận** — đúng cái mà trục module A–H được chọn để tránh. Trong horizon, Epic-D chỉ có **5 Story**; đó chưa phải quy mô cần tách |
| **Nếu PM quyết tách** | Đường tách tự nhiên là **theo thành phần `#1`–`#5`** của [MVP-Scope §5.2](../../010-Planning/MVP-Scope.md), ⛔ **KHÔNG theo mốc** (theo mốc = tạo nguồn sự thật thứ hai về thời gian, đã bị bác tại gate). Khi tách, `Story-Change-Log-On-Every-Editor-Action` **phải nằm ở Epic cha hoặc được nhân bản vào DoD của mọi Epic con** — nếu không, `KC-2` mất chủ đúng lúc số Epic tăng lên |

---

## 6. Tài liệu liên quan

### 6.1 Traceability — BRD cha

| Tầng | Tài liệu |
|---|---|
| Requirements (module) | [PRD-Comic-Studio §D. Editor & UI](../../020-Requirements/PRD-Comic-Studio.md#d-editor--ui) — `FR-D-01` … `FR-D-07` |
| **BRD cha** | [BRD-004-Minimum-Editor](../../020-Requirements/BRD/BRD-004-Minimum-Editor.md) |
| Yêu cầu phi chức năng | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) |

### 6.2 Use Case liên quan

| UC | Vai trò với Epic-D |
|---|---|
| [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md) | Thành phần `#5` — MVP1, **nơi moat lộ ra với khách hàng** |
| [UC-06-Generate-Panel-And-Pick-Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | Thành phần `#1` — variant picker (**MVP3, NGOÀI horizon**); pipeline sinh ảnh thuộc [Epic-Image-Generation-Pipeline](./Epic-Image-Generation-Pipeline.md) |
| [UC-07-Edit-Bubble-And-Dialogue-In-Panel](../../020-Requirements/Use-Cases/UC-07-Edit-Bubble-And-Dialogue-In-Panel.md) | Thành phần `#2` — tiêu thụ **typeset layer** của `FR-A-02` |
| [UC-08-Arrange-Page-And-Preview](../../020-Requirements/Use-Cases/UC-08-Arrange-Page-And-Preview.md) | Thành phần `#3` **và** `#4` — template layout + preview server-side |

### 6.3 Tài liệu tham khảo

| Tài liệu | Epic-D trích mục nào |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | **§5 toàn bộ** (§5.1 cảnh báo mẫu số · §5.2 năm thành phần bắt buộc + ràng buộc xuyên suốt · §5.3 điều kiện mở lại của `D2`–`D5`) · §3 nhóm D (`D1`, `D7`; `D6` cắt hẳn) · §3.1 cặp *"rất dễ bị gộp làm một"* · §4.1 toạ độ chuẩn hoá 0–1 · §6 `KC-1`…`KC-4` · §6.1 ba hiểu nhầm hay gặp |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria `M1-3`, `M2-5` · §5.2 điều kiện doanh thu Tầng 1 |
| [Glossary.md](../../999-Resources/Glossary.md) | `typeset layer` · `Story Bible` · `Panel Specification` · `MVP0` |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | §2.3 trục Epic + cảnh báo *"ứng viên cần tách"* · §4.4 bảng Story · §4.10 bảy Story vỡ khi cắt lô · §5.2 canonical facts (CF-6.7/6.8, CF-7.1→7.3, CF-9.1, CF-10.3) · §5.3 lệnh cấm (CẤM-01, CẤM-09) |

---

_Created by product-owner_
_Author: trisjr_
