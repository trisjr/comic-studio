# Doc Plan: 2026-08-24-khoi-tao-requirements-stories-comic-studio

> **File này do PM độc quyền chỉnh sửa.** Writer báo xong trong `SUMMARY` + `FILES_TOUCHED`, PM tick. Đây là chốt chặn chống ghi đè.

## 0. Ba quy ước đã chốt (áp cho mọi writer)

| # | Quy ước | Chốt | Lý do |
|---|---|---|---|
| **QC-1** | Số module | **8 (A–H)**, không phải 7 | `MVP-Scope.md` §3 thực tế có **tám** nhóm. Nhóm **H. Chất lượng & vận hành** (H1–H6) bị bỏ khỏi bảng "7 module" trong yêu cầu gốc, nhưng nó chứa H1 (HITL gate + eval kit = điều kiện khả thi **R9** của Charter §4), H2 (preference data = moat thật) và H4 (export = *"thứ duy nhất trong MVP4 người dùng thật sự nhận được"*). Bỏ nhóm H là bỏ ba hàng load-bearing. |
| **QC-2** | Ngôn ngữ tên file | **`{Title}` dùng ASCII/English · tiêu đề H1 và toàn bộ nội dung tiếng Việt** | RULE-001 không quy định ngôn ngữ `{Title}`. 100% file đang tồn tại trong `docs/` dùng tên ASCII (`Charter-Comic-Studio.md`, `MVP-Scope.md`, `Analysis-Market-Competitor-Landscape.md`). Dấu tiếng Việt trong tên file gây rủi ro anchor link + path. |
| **QC-3** | Cờ horizon của hạng mục vắt biên 02/2027 | Gán theo **mốc ĐẦU TIÊN** hạng mục được giao, kèm ghi chú *"hoàn tất ở mốc X (NGOÀI HORIZON)"* | `MVP-Scope.md` §3 dùng `🟡` cho *"có một phần"*. Nhiều hàng là `🟡` trong horizon và `✅` ngoài horizon (A2, A3, A4, D1#2, GP-4, H4). Cờ nhị phân thuần **hoặc** phóng đại **hoặc** xoá mất phần trong horizon. |

## 1. Hạng mục

**Tổng: 72 file** — 21 file tầng `020-Requirements` · 49 file tầng `022-User-Stories` · 1 Glossary · (+ MOC/Index/RULE-001 do PM giữ, không tính là hạng mục writer).

### 1.1 Tầng 020-Requirements — 21 file

| # | Tài liệu | Loại (RULE-001) | Đích | Writer | Lô | Xong |
|---|----------|-----------------|------|--------|----|------|
| 1 | `PRD-Comic-Studio.md` | **PRD** | `docs/020-Requirements/` | `business-analyst` | L1 | [x] 627 dòng ⚠️ |
| 2 | `SRS-Comic-Studio.md` | **SRS** | `docs/020-Requirements/` | `architect` | L2 | [x] 549 dòng ⚠️ |
| 3 | `BRD-001-Image-Generation-Pipeline.md` | **BRD** | `docs/020-Requirements/BRD/` | `business-analyst` #2 | L3 | [x] 169 dòng |
| 4 | `BRD-002-Story-Intelligence.md` | BRD | `docs/020-Requirements/BRD/` | `business-analyst` #2 | L3 | [x] 156 dòng |
| 5 | `BRD-003-Comic-Director-And-Layout.md` | BRD | `docs/020-Requirements/BRD/` | `business-analyst` #2 | L3 | [x] 163 dòng |
| 6 | `BRD-004-Minimum-Editor.md` | BRD | `docs/020-Requirements/BRD/` | `business-analyst` #3 | L4 | [x] 216 dòng ⚠️ |
| 7 | `BRD-005-Multi-Tenancy-And-Platform.md` | BRD | `docs/020-Requirements/BRD/` | `business-analyst` #3 | L4 | [x] 213 dòng ⚠️ |
| 8 | `BRD-006-Credit-And-Unit-Economics.md` | BRD | `docs/020-Requirements/BRD/` | `business-analyst` #3 | L4 | [x] 235 dòng ⚠️ |
| 9 | `BRD-007-Legal-And-Compliance.md` | BRD | `docs/020-Requirements/BRD/` | `security-auditor` | L5a | [x] 360 dòng |
| 10 | `BRD-008-Quality-And-Operations.md` | BRD | `docs/020-Requirements/BRD/` | `quality-assurance` | L5b | [x] 288 dòng ⚠️ |

> ⚠️ **Sáu file mang dấu ⚠️ được tick bằng CHECK CƠ HỌC CỦA PM, không bằng Worker Contract.** Bốn lô L1, L2, L4, L5b bị **terminate giữa chừng do session limit** (`resets 2:50am`) — cả bốn đã ghi xong file rồi mới chết ở bước tự-verify, nên **không lô nào trả về khối `STATUS`/`FILES_TOUCHED`**. Guardrail `pm-core.md` cấm tick thay worker khi chưa đọc `FILES_TOUCHED`, nên PM **thay thế bằng năm check cơ học** trước khi tick: (1) `git status` — đúng 10 file mới, **0 vi phạm ownership**, 0 file bị modify; (2) `tail` từng file — cả 10 kết thúc bằng block signature đầy đủ, **0 file bị cắt giữa**; (3) `grep "\[\["` — **0 wiki-link**; (4) `grep "030-Specs"` trong link — **0 link chết**; (5) frontmatter — cả 10 đủ `id`/`type`/`status: draft`/`created: 2026-08-24`, id đúng dãy `PRD-001`, `SRS-001`, `BRD-001…008`.
> **Hệ quả còn lại**: PM **không có** `SUMMARY` tự báo của 4 lô đó, nên **không biết chúng có tự phát hiện `PARTIAL` nào không**. Cụ thể: L1 (PRD) được ràng buộc phải báo `PARTIAL` vì khoảng trống persona — PM đã xác minh §3.3 *có* mục `TBD` đúng yêu cầu, nhưng nợ `PARTIAL` này phải được **verify khẳng định lại ở L21**, không coi là đã đóng.
| 11 | `UC-01-Upload-And-Ingest-Chapter.md` | **Use Case** | `docs/020-Requirements/Use-Cases/` | `business-analyst` #4 | L6 | [ ] |
| 12 | `UC-02-Review-And-Edit-Story-Bible.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `business-analyst` #4 | L6 | [ ] |
| 13 | `UC-03-Review-Panel-Script.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `business-analyst` #4 | L6 | [ ] |
| 14 | `UC-04-Human-Gate-Speaker-Attribution.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `business-analyst` #4 | L6 | [ ] |
| 15 | `UC-05-Human-Gate-Dialogue-Condensation.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `product-designer` | L7 | [ ] |
| 16 | `UC-06-Generate-Panel-And-Pick-Variant.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `product-designer` | L7 | [ ] |
| 17 | `UC-07-Edit-Bubble-And-Dialogue-In-Panel.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `product-designer` | L7 | [ ] |
| 18 | `UC-08-Arrange-Page-And-Preview.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `product-designer` | L7 | [ ] |
| 19 | `UC-09-Export-Chapter.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `business-analyst` #5 | L8 | [ ] |
| 20 | `UC-10-Manage-Credit-And-BYOK.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `business-analyst` #5 | L8 | [ ] |
| 21 | `UC-11-Handle-Takedown-Request.md` | Use Case | `docs/020-Requirements/Use-Cases/` | `business-analyst` #5 | L8 | [ ] |

### 1.2 Tầng 022-User-Stories — 8 Epic + 41 Story

**Epic** (`docs/022-User-Stories/Epics/`) — 8 file, writer `product-owner`:

| # | Tài liệu | BRD cha | Lô | Xong |
|---|----------|---------|----|------|
| 22 | `Epic-Image-Generation-Pipeline.md` | BRD-001 | L9 | [ ] |
| 23 | `Epic-Story-Intelligence.md` | BRD-002 | L9 | [ ] |
| 24 | `Epic-Comic-Director-And-Layout.md` | BRD-003 | L9 | [ ] |
| 25 | `Epic-Minimum-Editor.md` | BRD-004 | L9 | [ ] |
| 26 | `Epic-Multi-Tenancy-And-Platform.md` | BRD-005 | L10 | [ ] |
| 27 | `Epic-Credit-And-Unit-Economics.md` | BRD-006 | L10 | [ ] |
| 28 | `Epic-Legal-And-Compliance.md` | BRD-007 | L10 | [ ] |
| 29 | `Epic-Quality-And-Operations.md` | BRD-008 | L10 | [ ] |

**Story** (`docs/022-User-Stories/Backlog/`) — 41 file **trong horizon**, cắt lô theo Epic:

| Lô | Epic | Số Story | Writer | Xong |
|----|------|---------:|--------|------|
| L11 | Epic-Image-Generation-Pipeline | 5 | `product-owner` #2 | [ ] |
| L12 | Epic-Story-Intelligence | 4 | `product-owner` #3 | [ ] |
| L13 | Epic-Comic-Director-And-Layout | 7 | `product-owner` #4 | [ ] |
| L14 | Epic-Minimum-Editor | 5 | `product-owner` #5 | [ ] |
| L15 | Epic-Multi-Tenancy-And-Platform | 5 | `architect` #2 | [ ] |
| L16 | Epic-Credit-And-Unit-Economics | 3 | `product-owner` #6 | [ ] |
| L17 | Epic-Legal-And-Compliance | 6 | `security-auditor` #2 | [ ] |
| L18 | Epic-Quality-And-Operations | 6 | `quality-assurance` #2 | [ ] |

> **Danh sách tên file chính xác của 41 Story nằm ở `findings/business-analyst.md` §4.1–§4.8**, cột đầu mỗi bảng. Writer **đọc bảng của đúng Epic mình được giao** và tạo đúng những tên file đó — **cấm tự đặt tên mới, cấm bỏ sót, cấm thêm Story không có trong bảng**.

**10 Story `[NGOÀI HORIZON]` — KHÔNG tạo file trong run này.** Chúng được ghi thành **hàng trong Epic cha** (mục *Story ngoài horizon*) và **hàng trong `Backlog-Priority.md`** với cột `Trạng thái tài liệu = chưa có file`. Lý do: một Story file cho việc cách đây 6+ tháng sẽ bị viết lại trước khi có ai nhặt nó, còn `Roadmap` §5.1 đã sở hữu câu trả lời *"cái gì rơi ra khỏi horizon"*. Traceability vẫn nguyên vẹn qua Epic + backlog row, mà không sinh 10 file nợ bảo trì. Danh sách 10 Story đó: `findings/business-analyst.md` §4.1–§4.8, các hàng có cờ `[NGOÀI HORIZON]`.

### 1.3 Hai file còn lại

| # | Tài liệu | Loại | Đích | Writer | Lô | Xong |
|---|----------|------|------|--------|----|------|
| 30 | `Backlog-Priority.md` | **Prioritized Backlog** ⚠️ chưa có trong Mapping | `docs/022-User-Stories/` | `product-owner` #7 | L19 — **tuần tự sau L11–L18** | [ ] |
| 31 | `Glossary.md` (**sửa**) | Glossary | `docs/999-Resources/` | `business-analyst` #6 | L20 | [ ] |

## 2. Outline theo LOẠI tài liệu

> Per-file anchor nguồn đã có trong findings — writer đọc theo path. Mục này là **contract cấu trúc**, thứ duy nhất tồn tại vì repo **không có template** cho BRD / Use Case / Epic / Story / Prioritized Backlog (`Template-PRD.md` và `Template-SRS.md` là hai khuôn duy nhất có sẵn).

### 2.1 PRD — `PRD-Comic-Studio.md`

- **Độc giả đích**: Founder (người duy nhất build), và bất kỳ agent/người mới vào dự án cần biết *"sản phẩm phải làm gì"* mà không phải đọc lại 1.148 dòng Analysis.
- **Cấu trúc** (bám `Template-PRD.md`, mở rộng đúng chỗ cần):
  `## 1. Executive Summary` · `## 2. Bối cảnh & mục tiêu` (Problem / Goals / Non-Goals) · `## 3. Người dùng & vấn đề` · `## 4. Yêu cầu chức năng theo 8 module` — **tám H2 con đúng tên 8 module A–H**, mỗi module một bảng `FR-{Module}-{nn}` · `## 5. Yêu cầu phi chức năng` (trỏ sang SRS, **không lặp lại nội dung**) · `## 6. Ranh giới scope` (In / Out / cắt hẳn) · `## 7. Success metrics` (mượn OKRs, không tự đặt KR mới) · `## 8. Tài liệu liên quan` (8 BRD + 8 Epic + SRS).
- **Nguồn sự thật**: `Charter-Comic-Studio.md` §4 (yêu cầu cấp cao) và §5 (Scope In/Out) · `MVP-Scope.md` §3 (toàn bộ bảng A–H), §5, §6 · `OKRs.md` §3–§5 cho mục 7 · `findings/business-analyst.md` §1.1 (mapping module → hàng), §5.2 (canonical facts), §5.3 (lệnh cấm).
- ⚠️ **Mục 3 phải mở bằng `TBD` có cấu trúc.** `findings/business-analyst.md` KT-1: **toàn repo không có persona / JTBD / định nghĩa "đủ tốt"** — Analysis §3.2 đã gọi thẳng khoảng trống này. Repo có *phân khúc* (`[CHỐT]` tác giả truyện chữ không biết vẽ) nhưng **không có persona**. Writer ghi phân khúc đã chốt + một mục `TBD — chưa có persona/JTBD, cần user interview` và **báo `PARTIAL`**. Bịa một persona ở đây là bịa vào tầng cao nhất của cây requirement.
- **Cấu trúc mục 4 là ràng buộc cứng**: 8 H2 con đúng tên 8 module, vì cột *Implements PRD* của cả 8 Epic trỏ vào đúng các anchor đó. Đổi cấu trúc mục 4 ⇒ 8 link Epic chết.
- **Tiêu chí xong**: đủ 8 H2 con ở mục 4, mỗi module ≥1 hàng FR có anchor; mục 3 có `TBD` tường minh; 0 con số không có nhãn nguồn; link tới 8 BRD + 8 Epic + SRS đều là relative path phân giải được.

### 2.2 SRS — `SRS-Comic-Studio.md`

- **Độc giả đích**: chính Founder ở vai architect, tại thời điểm viết dòng code đầu tiên.
- **Cấu trúc** (bám `Template-SRS.md` — ⚠️ file thực tế có **5 mục** đánh số, không phải 7): `## 1. Introduction` · `## 2. Overall Description` · `## 3. System Features` — **tổ chức theo 8 module A–H** · `## 4. External Interface Requirements` · `## 5. Other Non-functional Requirements` · thêm `## 6. Negative requirements — những gì đã bị CẮT HẲN`.
- **Nguồn sự thật**: **`findings/architect.md` là nguồn chính** — §1 (nguyên tắc phân định SRS ↔ 030), §2.1–§2.8 (68 hàng `SRS-FR-01…42` / `SRS-NFR-01…26` đã gắn nhãn CHỐT / MẶC ĐỊNH / CHƯA QUYẾT kèm anchor), §3.1 (17 NFR có số), §3.2 (14 NFR `TBD`), §4 (18 cảnh báo). Writer **dùng đúng id và đúng nhãn** trong đó.
- **Ba ràng buộc riêng của SRS**:
  1. **Cấm mọi link tới `docs/030-Specs/`** — tầng đó rỗng, `Specs-MOC.md` là 0 byte, không thuộc scope run này. Cần trỏ sang design thì viết văn bản thuần *"sẽ được đặc tả tại tầng 030-Specs"*.
  2. **Năm hàng "lai"** (cơ chế CHỐT nhưng một tham số bên trong chưa quyết — `best-of-N`, fairness `in_flight_per_tenant`, abuse threshold, adapter provider, ba câu hỏi luật sư): khẳng định **cơ chế**, `TBD` **riêng cho tham số**. Không hạ cả hàng xuống `TBD`, cũng không tự chọn giúp.
  3. **Negative requirement phải viết ra, không được im lặng** (mục 6). `CF-9` ghi *"không mở lại"*; một SRS im lặng sẽ bị đọc là *"chưa quyết"*. Hai bẫy cắt-lẫn phải nói rõ: **`pgvector` KHÔNG bị cấm** (B5 để mở ở Full Scope — khác hẳn E6 cắt Vector DB riêng), và **cắt UI cây generation ≠ cắt cột `parent_generation_id`** (D6 `❌` vs KC-1 bắt buộc — gộp nhầm thì mất bảo hộ bản quyền).
- **Tiêu chí xong**: 68 hàng requirement đều có mặt với đúng nhãn độ cứng; 17 NFR có số kèm nhãn nguồn nguyên trạng; 14 NFR `TBD` nằm riêng và **không hàng nào bị gán số**; mục 6 có đủ 5 negative requirement + 2 bẫy cắt-lẫn; 0 link tới `030-Specs/`.

### 2.3 BRD — 8 file `BRD-{NNN}-{Title}.md`

- **Độc giả đích**: Founder khi quyết định *"module này có đáng làm ở mốc này không"*.
- **Cấu trúc** (7 H2, giống nhau ở cả 8 file): `## 1. Business goal` · `## 2. Phạm vi module` (bảng hàng `MVP-Scope §3` mà nó bao, kèm nhãn từng mốc `✅🟡⛔❌`) · `## 3. Yêu cầu nghiệp vụ` (bảng `BR-{NNN}-{nn}` — phát biểu · căn cứ · mốc) · `## 4. Ràng buộc & điều kiện chặn` · `## 5. Cái module này KHÔNG làm` (gồm hàng bị cắt hẳn, kèm điều kiện mở lại nếu `MVP-Scope` có ghi) · `## 6. Rủi ro chính` (trỏ `Risk-Register.md`, không tự chấm điểm rủi ro mới) · `## 7. Tài liệu liên quan` (PRD, Epic tương ứng, UC liên quan).
- **Nguồn sự thật**: `findings/business-analyst.md` §1.1 hàng của đúng BRD đó (business goal + cột *Bao hàng* + cột *Anchor nguồn*) · `MVP-Scope.md` §3 nhóm tương ứng · `MVP-Scope.md` §6 (KC-1…KC-7) · `MVP-Scope.md` §5 riêng cho BRD-004 · §5.2 canonical facts.
- **Tiêu chí xong**: mọi hàng `MVP-Scope §3` của nhóm đó xuất hiện đúng một lần trong mục 2 hoặc mục 5 (**không hàng nào rơi**); mục 5 không rỗng; mọi `BR-` có anchor; link tới PRD + Epic + UC phân giải được.

### 2.4 Use Case — 11 file `UC-{NN}-{Title}.md`

- **Độc giả đích**: Founder khi implement luồng đó, và người viết test case về sau.
- **Cấu trúc** (6 H2): `## 1. Thông tin` (bảng: Primary actor · Secondary actor · Mốc MVP · BRD module · Điều kiện tiên quyết) · `## 2. Mục tiêu` · `## 3. Main flow` (bảng đánh số bước, mỗi bước ghi rõ **actor nào làm**) · `## 4. Alternative flow` · `## 5. Exception flow` (≥1 nhánh — rỗng là không đạt) · `## 6. Tài liệu liên quan`.
- **Nguồn sự thật**: `findings/business-analyst.md` §3.2 hàng của đúng UC đó (actor · mục tiêu · BRD · mốc · anchor) · các mục `MVP-Scope`/`Roadmap`/`Glossary` mà cột *Anchor nguồn* trỏ tới.
- **Hai ràng buộc**: (a) UC-04 và UC-05 là **hai human gate BẮT BUỘC, không bypass được** — main flow phải nêu rõ *không có đường đi nào vòng qua bước này*, vì `Roadmap` M2-4 đo bằng **sự vắng mặt của đường code bypass**; (b) UC-11 có primary actor là **người ngoài** (chủ sở hữu quyền), không phải người dùng sản phẩm — Founder chỉ là secondary actor với vai operator.
- **Tiêu chí xong**: mục 5 có ≥1 nhánh exception; mọi bước main flow ghi rõ actor; 0 bước bịa ra tính năng không có trong `MVP-Scope §3`.

### 2.5 Epic — 8 file `Epic-{Title}.md`

- **Độc giả đích**: Founder khi lập kế hoạch một mốc.
- **Cấu trúc** (6 H2): `## 1. Implements` — **một dòng link tới PRD kèm anchor mục 4 của module đó**, đúng khuôn RULE-001 §Linking Rules quy tắc #2 · `## 2. Mục tiêu Epic` · `## 3. Story trong horizon` (bảng: tên Story + link + mốc + `I`/`S` + trạng thái) · `## 4. Story ngoài horizon — chưa có file` (bảng, cột *Trạng thái tài liệu* = `chưa có file`) · `## 5. Definition of Done cấp Epic` · `## 6. Tài liệu liên quan` (BRD cha + UC liên quan).
- **Nguồn sự thật**: `findings/business-analyst.md` §2.3 hàng của đúng Epic đó · §4.1–§4.8 bảng Story của Epic đó · `MVP-Scope §3` nhóm tương ứng.
- **Ba ràng buộc**:
  1. **`Epic-Minimum-Editor` (E-D): `Story-Change-Log-On-Every-Editor-Action` VẪN là một Story riêng** *và đồng thời* là một mục trong DoD cấp Epic. Lens đề xuất chuyển hẳn nó thành DoD; PM **bác** — nó là `KC-2`, nằm trong danh sách *"không được cắt"*, và một ràng buộc chỉ tồn tại trong DoD thì không có ai tick nó.
  2. **`Epic-Legal-And-Compliance` (E-G) KHÔNG có Story cho G0** (ba câu hỏi luật sư). Đó là **hoạt động**, không phải increment sản phẩm; `Roadmap` §3.1 việc 1 + exit criterion **P-1** đã sở hữu nó. Đưa vào backlog là biến một blocker thành ticket có thể "dời sprint sau".
  3. Mục 3 phải liệt kê **đúng và đủ** số Story trong horizon của Epic đó (5/4/7/5/5/3/6/6) — thiếu một dòng là mất traceability.
- **Tiêu chí xong**: mục 1 link tới đúng anchor PRD; mục 3 đủ số Story và mọi link phân giải được; mục 4 có đủ Story ngoài horizon của Epic đó (nếu có).

### 2.6 User Story — 41 file `Story-{Title}.md`

- **Độc giả đích**: chính Founder tại thời điểm nhặt Story lên làm.
- **Cấu trúc** (bắt buộc, đúng thứ tự): `## 1. Story` (một câu `Là <actor>, tôi muốn <hành động>, để <giá trị>` — **copy nguyên văn** từ bảng findings) · `## 2. Part of` (link Epic cha + BRD + UC liên quan) · `## 3. Bối cảnh & nguồn` (anchor: ≥1 hạng mục `MVP-Scope §3` **và** ≥1 exit criterion `Roadmap`) · `## 4. Acceptance Criteria` — **đúng 4 khối dưới đây** · `## 5. Ước lượng` (bảng `E_build` giờ-người / `E_hitl` giờ-người-mỗi-chapter) · `## 6. INVEST` (chấm `I` và `S`, ghi thẳng `⚠️` nếu vỡ, kèm lý do).
- **Khuôn Acceptance Criteria — CHECKLIST, KHÔNG Gherkin** (chốt tại `findings/product-owner.md` §4.4):

  | Khối | Heading | Nội dung | Rỗng được? |
  |---|---|---|---|
  | AC-1 | `### Xác minh được` | mỗi dòng `- [ ]` = **một** assertion **nhị phân**, **cách đo ghi ngay trong dòng đó** | ❌ ≥1 dòng |
  | AC-2 | `### Đường không hạnh phúc (unhappy path)` | ≥1 dòng cho failure mode / edge case / race condition | ❌ ≥1 dòng — rỗng ⇒ **không Ready** |
  | AC-3 | `### Ràng buộc cứng không được vi phạm` | trích id `KC-x` / `C-x` / `AG-x`; không có thì ghi `—` | 🟡 ghi `—` được |
  | AC-4 | `### Story này KHÔNG làm` | chống scope creep | ❌ ≥1 dòng |

  **Luật viết dòng AC-1: mỗi dòng phải THẤT BẠI ĐƯỢC.** *"insert panel 4 nhân vật bị từ chối"* là hợp lệ; *"schema hỗ trợ giới hạn nhân vật"* là **không hợp lệ** (không có cách nào chứng minh sai).
- **Nguồn sự thật**: `findings/business-analyst.md` §4.x bảng của đúng Epic đó (câu chuẩn · mốc · cờ · `I`/`S` · anchor) · `findings/product-owner.md` §4.1–§4.6 (INVEST diễn giải lại, `Small` neo vào **giờ-người**, DoR/DoD) · các mục `MVP-Scope`/`Roadmap`/`Glossary` mà cột *Anchor* trỏ tới.
- **Bốn ràng buộc**:
  1. **5 Story MVP0 — INVEST KHÔNG áp** (`Story-Generate-Panel-With-Reference-And-VLM-Select`, `Story-Typeset-Layer-And-Bubble-Overlay`, `Story-Comic-IR-Panel-Specification`, `Story-Golden-Dataset-For-Regression`, `Story-Record-Readability-Human-Judgement`). Mục 6 của chúng ghi `INVEST không áp — Story thuộc [MVP0]` kèm lý do, và **DoD lấy từ 5 tiêu chí gate G1** (`MVP-Scope` §7.2). Dùng đúng tên **MVP0** — `Glossary.md` cấm *"phase 0"*, *"spike"*, *"PoC"*.
  2. **7 Story vỡ `Independent`/`Small`** (`findings/business-analyst.md` §4.10): mục 6 phải ghi `⚠️` **kèm nguyên lý do "không cắt được theo đường nào"** trong bảng đó. Đặc biệt `Story-Tenant-Id-And-RLS-Everywhere`: DoD **phải là test rò rỉ chéo tenant PASS (M1-1)**, không phải số bảng đã sửa.
  3. **`Small` neo vào giờ-người**, không story point, không ngày công: `E_build ≤ 16` giờ-người, `E_hitl ≤ 2` giờ-người/chapter. Vượt trần `E_build` ⇒ ghi lý do thành văn; vượt trần `E_hitl` ⇒ **không split được**, phải ghi `escalate`.
  4. ⛔ **Writer KHÔNG cập nhật `Stories-MOC.md`** — DoD mục **D5** của `findings/product-owner.md` yêu cầu writer làm việc đó, nhưng MOC là **điểm hội tụ do PM giữ**. PM ghi MOC ở close-step. Writer chạm MOC = vi phạm ownership.
- **Tiêu chí xong**: đúng số file của lô; mọi file có 6 H2; AC đủ 4 khối với AC-1/AC-2/AC-4 không rỗng; mục 3 có ≥1 anchor `MVP-Scope` **và** ≥1 exit criterion `Roadmap`; câu Story ở mục 1 khớp **nguyên văn** bảng findings.

### 2.7 Prioritized Backlog — `Backlog-Priority.md`

- **Độc giả đích**: Founder khi chọn *"làm gì tiếp"* trong phạm vi một mốc đã được `Roadmap` ấn định.
- **Ranh giới — copy nguyên từ `findings/product-owner.md` §2**:

  | Tài liệu | Trả lời câu hỏi | KHÔNG trả lời |
  |---|---|---|
  | `Roadmap.md` | Khi nào, theo thứ tự nào, exit criteria từng mốc | Thứ tự trong nội bộ một mốc |
  | `MVP-Scope.md` | Cái gì vào MVP0–MVP4, cái gì bị cắt, Go/No-Go | Ngày tháng, thứ tự thời gian |
  | `OKRs.md` | Đo thành công bằng gì | Việc nào làm trước |
  | **`Backlog-Priority.md`** | **Trong một mốc đã cho, Story nào làm trước Story nào** | **Mốc nào đến khi nào — và bất kỳ ngày tháng nào** |

  **Xung đột: `Roadmap` thắng tuyệt đối.** Lệch nhau ⇒ **sửa/xoá hàng backlog**, không sửa `Roadmap` (mượn nguyên luật `OKRs` §1.1: *"KR đó sai, không phải Roadmap sai"*). `Backlog-Priority` là **view xếp hạng dẫn xuất**, không phải nguồn độc lập.
  ⛔ **Guardrail cơ học: CẤM mọi ngày tháng.** `grep` thấy `/2026`, `/2027`, `Q4`, `Q1`, hoặc `tuần` trong file này là **đã drift** — chỉ được chứa **tên mốc** (`MVP0`…`MVP4`, `pre-cycle`).
- **Framework**: `UNLOCK-ORDER` — chi tiết `findings/product-owner.md` §1.4. Cột kế thừa (`Mốc`, `Scope-Label`) **chấm một lần ở nguồn, copy ở đây, cấm chấm lại**; `Rank` lexicographic 3 khoá trong **phạm vi một mốc**; tie-break T1→T4 khi thang bão hoà.
  ⚠️ **Đây là điểm lệch khỏi chữ "(RICE/MoSCoW)" trong yêu cầu gốc** — xem câu gate #2. Writer chỉ chạy sau khi anh chốt.
- **Cấu trúc**: 7 H2 + bảng 15 cột — schema chính xác ở `findings/product-owner.md` §3.2 và §3.3. Đánh dấu MVP Story bằng `⭐` theo quy tắc **suy ra được từ cột** (§3.4), không phán đoán tay.
- **Nguồn sự thật**: 41 Story đã tạo (L11–L18) + 10 Story ngoài horizon · `MVP-Scope §3` cho cột `Scope-Label` · `Roadmap §2` cho cột `Mốc` · `findings/product-owner.md` §1.4, §3.
- **Tiêu chí xong**: đủ 51 hàng (41 có file + 10 `chưa có file`); mọi link Story/Epic phân giải được; `grep` không tìm thấy ngày tháng nào; cột kế thừa khớp 100% với `MVP-Scope §3` và `Roadmap §2`.

### 2.8 Glossary — `docs/999-Resources/Glossary.md` (**sửa, không tạo**)

- **Đây là SỬA file đã tồn tại**: `id: GLOSSARY-001`, `type: glossary`, `status: live`, `created: 2026-02-04`, hiện **54 term**. **Giữ nguyên `id` / `type` / `status` / `created`. Bump `updated: 2026-08-24`.**
- **Việc phải làm**: bổ sung term **mới phát sinh từ tầng Requirements/Stories** mà 54 term hiện có chưa phủ — ví dụ `BRD`, `Use Case`, `Epic`, `INVEST`, `Definition of Ready/Done`, `E_build` / `E_hitl` (giờ-người), `UNLOCK-ORDER`, `Scope-Label`, `human gate` (phân biệt với `HITL gate` đã có), `negative requirement`, `attribute binding` (đã có — kiểm trùng). Term nào đã có thì **không viết lại**.
- ⛔ **Ba lệnh cấm**: (a) **không sửa, không rút gọn, không diễn giải lại 54 term đang có** — chỉ được thêm; (b) con số nào có caveat thì **mang nguyên caveat** — repo đã có tiền lệ lỗi MAJOR: `23% GRR` bị trích mà rơi ba caveat; (c) **không xoá mục *Xác thực & bảo mật*** (OTP/rate limit) dù nó là boilerplate kế thừa — guardrail lane doc cấm xoá, và đó là quyết định của một run khác.
- **Nguồn sự thật**: `findings/business-analyst.md` §5.2 (canonical facts) · `findings/product-owner.md` §4.3, §4.4 (định nghĩa `E_build`/`E_hitl`, khuôn AC) · `findings/architect.md` §2.7 (negative requirement).
- **Tiêu chí xong**: term mới nằm đúng nhóm H2 phù hợp (hoặc một nhóm mới có tên rõ ràng); 54 term cũ **không thay đổi một ký tự**; `updated` đã bump; mục *Mục lục* ở đầu file đồng bộ với các H2 thực tế.

## 3. Bảng canonical facts — KHÔNG copy vào file này

**57 canonical facts + 18 lệnh cấm tường minh nằm nguyên tại `findings/business-analyst.md` §5.2 và §5.3.** Mọi writer **đọc trực tiếp theo path** và **copy nguyên cặp *số + nhãn nguồn*** vào tài liệu của mình.

> **Vì sao không copy vào `outline.md` như run trước.** Run `2026-08-23` đặt bảng CF trong `outline.md` và nó hoạt động (0 lệch giá trị, 0 mất nhãn trên 4 writer song song) — nhưng `cost.md` §3.2 đã đo được cái giá: bảng CF *"ở lại trong context PM tới hết run"* và là **nguồn phình thứ hai** trong ba nguồn. Run này có **72 deliverable và ~20 lô writer** thay vì 6 — nhân cái giá đó lên là không chịu được. Đóng băng bảng CF ở một file read-only rồi cấp path đạt **cùng một bảo đảm** (mọi writer copy từ **một** nguồn) mà không đi qua context PM. `pm-core.md` cho phép tường minh: *"[CONTEXT] Đọc tham chiếu: <đường dẫn artifact lớn — chỉ phần này mới dùng path>"*.

**Ba lệnh cấm phải xuất hiện nguyên văn trong mọi prompt dispatch** (trích từ §5.3, đây là các lỗi đã thật sự xảy ra trong repo):
1. ⛔ **CẤM TRỪ `CF-6.8` cho `CF-6.7`** — hai mẫu số khác nhau, phép trừ tạo ra một con số vô nghĩa.
2. ⛔ **Trích `23% GRR` phải mang đủ BA caveat** (cohort ~200 công ty và n của band không công bố · bộ lọc ≥$250K ARR loại đúng nhóm indie · dữ liệu 2025). Bỏ ba dòng này là **trích sai** — và đây chính là lỗi MAJOR `M-1` của run trước.
3. ⛔ **`Continuity Checker` chỉ có một nghĩa**: QA-based selection giữa N candidate. **KHÔNG** phải "gắn nhãn ✓/✗ từng attribute rồi autofix". Và **`best-of-N` KHÁC `retry-on-failure`** — nhầm hai khái niệm này là nguồn của sai số chi phí **+50%**.

## 4. Link phải tạo (RULE-001 §Linking Rules)

⛔ **Standard markdown link relative path. CẤM wiki-link `[[...]]`** — RULE-001 quy tắc #5. (`pm-doc.md` Bước 5 mục 4 nói ngược lại; RULE-001 là contract của lane, và run `2026-08-23` đã có tiền lệ được duyệt cho đúng điểm này.)

| Từ | Tới | Quan hệ |
|---|---|---|
| `PRD-Comic-Studio.md` | 8 × `BRD/BRD-{NNN}-*.md` | `## Related BRDs` |
| `PRD-Comic-Studio.md` | 8 × `../022-User-Stories/Epics/Epic-*.md` | `## Related Epics` (RULE-001 #1) |
| `PRD-Comic-Studio.md` | `SRS-Comic-Studio.md` | NFR chi tiết |
| `SRS-Comic-Studio.md` | `PRD-Comic-Studio.md` | `Implements:` |
| `BRD-{NNN}-*.md` | `../PRD-Comic-Studio.md` + Epic tương ứng + UC liên quan | `Part of:` / `Related:` |
| `UC-{NN}-*.md` | `../../022-User-Stories/Epics/Epic-*.md` | `Part of:` (RULE-001 #3) |
| `Epic-*.md` | `../../020-Requirements/PRD-Comic-Studio.md#<anchor module>` | `Implements:` (RULE-001 #2) |
| `Epic-*.md` | các `../Backlog/Story-*.md` của nó | bảng mục 3 |
| `Story-*.md` | `../Epics/Epic-*.md` | `Part of:` |
| `Story-*.md` | `../../020-Requirements/BRD/BRD-{NNN}-*.md` | `Related:` |
| `Backlog-Priority.md` | 41 × `./Backlog/Story-*.md` + 8 × `./Epics/Epic-*.md` | bảng backlog |
| **⛔ KHÔNG** | bất kỳ file nào trong `docs/030-Specs/` | tầng rỗng, `Specs-MOC.md` 0 byte, ngoài scope |

## 5. MOC cần cập nhật (PM giữ — close-step)

| File | Mục thêm/sửa |
|---|---|
| `docs/020-Requirements/Requirements-MOC.md` | Đăng ký PRD + SRS + 8 BRD + 11 UC. **Xoá link chết `PRD-TNMCORE-OS.md`** (boilerplate kế thừa, file không tồn tại). Mục *020.40 NFR* ghi rõ NFR nằm trong SRS. Bump `updated`. |
| `docs/022-User-Stories/Stories-MOC.md` | Đăng ký 8 Epic + 41 Story + `Backlog-Priority.md`. **Xoá 2 link chết `Story-Request-OTP.md`, `Story-Verify-OTP.md`** (boilerplate kế thừa). Bump `updated`, `status: draft → live`. |
| `docs/999-Resources/Resources-MOC.md` | Kiểm mục Glossary còn đúng sau khi bump. |
| `docs/000-Index.md` | Mục *020 · Requirements* và *022 · User Stories* hiện ghi *"(chưa có tài liệu)"* → thay bằng bảng thật. Thêm PRD + SRS vào mục *Bắt đầu từ đâu*. Bump `updated`. |
| `knowledge-base/99-Templates/Documents-Template.md` (**RULE-001**) | **Thêm đúng một hàng additive** vào Document Type Mapping: `022-User-Stories` → `Prioritized Backlog` → `docs/022-User-Stories/` → `Backlog-Priority.md`. Bump `updated`, ghi nhật ký thay đổi đúng khuôn comment đã có. **Chỉ sau khi anh duyệt tại gate.** |

## 6. Ripple — tài liệu đang trích phạm vi này và sẽ lệch sau khi sửa

| Tài liệu | Lệch ở đâu | Xử lý |
|---|---|---|
| `docs/000-Index.md` | Hai mục *(chưa có tài liệu)* thành sai; mục *Nợ kỹ thuật* có thể đã ghi khoảng trống 020/022 | PM sửa ở close-step |
| `docs/010-Planning/Planning-MOC.md` | Không lệch — 010 không bị chạm | Không làm gì |
| `docs/999-Resources/Glossary.md` | Là deliverable của run (L20), **nằm trong phạm vi verify** — không để PM sửa ở close-step. Đây chính là cách lỗi `M-1` của run trước phát sinh | Có writer + verify |
| `docs/030-Specs/Specs-MOC.md` (0 byte) | **Không** thuộc scope run này. SRS bị cấm link tới 030 nên không sinh link chết mới | Ghi vào *Nợ lại* của báo cáo |
| `openspec/` | Không bị chạm | Không làm gì |
