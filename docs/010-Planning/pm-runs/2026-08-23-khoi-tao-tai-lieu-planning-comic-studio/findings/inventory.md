# Findings — `context-auditor`: Inventory kho `docs/`

**Run**: `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio` · **Bước 2 (Analysis fan-out)** · **Lens**: hiện trạng kho tài liệu
**Contract đối chiếu**: `knowledge-base/99-Templates/Documents-Template.md` (RULE-001, `status: approved`, `updated: 2026-03-03`)
**Phương pháp**: mọi dòng dưới đây được xác minh bằng `find` / `head` / `grep` / `Read` trên đĩa. Không suy đoán.
**Ghi chú phạm vi**: `docs/010-Planning/pm-runs/**` bị loại khỏi Mục 2 (run-state, cấm sửa) nhưng vẫn được đọc để đối chiếu ở Mục 4.

---

## Mục 1 — Thư mục RULE-001 bắt buộc nhưng CHƯA tồn tại

Nguồn: RULE-001 §*Cấu trúc thư mục bắt buộc (Required Folder Structure)* (dòng 127–192).
Hiện trạng đĩa: `docs/` chỉ có **14 thư mục** — 12 thư mục Dewey cấp 1 (thiếu `090-Archive/`), cộng `999-Resources/Templates/` và `010-Planning/pm-runs/**`.

### 1A. Danh sách `mkdir` — **32 thư mục** thiếu

> Đây là danh sách đầy đủ và duy nhất PM cần cho hạng mục #6. **Đúng 32 dòng.** Không mục nào trong đây tồn tại trên đĩa.

| # | Đường dẫn | Đã tồn tại? | RULE-001 bắt buộc? |
|---:|---|:---:|:---:|
| 1 | `docs/010-Planning/Sprints/` | ❌ Không | ✅ Có |
| 2 | `docs/010-Planning/Estimates/` | ❌ Không | ✅ Có |
| 3 | `docs/010-Planning/Implementation-Plans/` | ❌ Không | ✅ Có |
| 4 | `docs/020-Requirements/BRD/` | ❌ Không | ✅ Có |
| 5 | `docs/020-Requirements/Use-Cases/` | ❌ Không | ✅ Có |
| 6 | `docs/022-User-Stories/Epics/` | ❌ Không | ✅ Có |
| 7 | `docs/022-User-Stories/Active-Sprint/` | ❌ Không | ✅ Có |
| 8 | `docs/022-User-Stories/Backlog/` | ❌ Không | ✅ Có |
| 9 | `docs/030-Specs/Architecture/` | ❌ Không | ✅ Có |
| 10 | `docs/030-Specs/API/` | ❌ Không | ✅ Có |
| 11 | `docs/030-Specs/Schema/` | ❌ Không | ✅ Có |
| 12 | `docs/030-Specs/Security/` | ❌ Không | ✅ Có |
| 13 | `docs/035-QA/Test-Plans/` | ❌ Không | ✅ Có |
| 14 | `docs/035-QA/Test-Cases/` | ❌ Không | ✅ Có |
| 15 | `docs/035-QA/Automation/` | ❌ Không | ✅ Có ¹ |
| 16 | `docs/035-QA/Reports/` | ❌ Không | ✅ Có |
| 17 | `docs/035-QA/Performance/` | ❌ Không | ✅ Có |
| 18 | `docs/040-Design/Wireframes/` | ❌ Không | ✅ Có |
| 19 | `docs/040-Design/Design-System/` | ❌ Không | ✅ Có |
| 20 | `docs/040-Design/Specs/` | ❌ Không | ✅ Có |
| 21 | `docs/040-Design/Assets/` | ❌ Không | ✅ Có ¹ |
| 22 | `docs/050-Research/Competitor-Analysis/` | ❌ Không | ✅ Có |
| 23 | `docs/050-Research/User-Interviews/` | ❌ Không | ✅ Có |
| 24 | `docs/050-Research/Surveys/` | ❌ Không | ✅ Có |
| 25 | `docs/060-Manuals/User-Guide/` | ❌ Không | ✅ Có |
| 26 | `docs/060-Manuals/Admin-Guide/` | ❌ Không | ✅ Có |
| 27 | `docs/070-Deployment/Releases/` | ❌ Không | ✅ Có |
| 28 | `docs/070-Deployment/Runbooks/` | ❌ Không | ✅ Có |
| 29 | `docs/080-Operations/Incidents/` | ❌ Không | ✅ Có |
| 30 | `docs/080-Operations/SLAs/` | ❌ Không | ✅ Có |
| 31 | `docs/090-Archive/` | ❌ Không | ✅ Có (**cấp 1 duy nhất còn thiếu**) |
| 32 | `docs/999-Resources/Meeting-Notes/` | ❌ Không | ✅ Có |

¹ `035-QA/Automation/` và `040-Design/Assets/` **có** trong khối *Required Folder Structure* nhưng **không** xuất hiện ở bất kỳ hàng nào của bảng *Document Type Mapping*. Chúng vẫn bắt buộc (khối cấu trúc là nguồn), nhưng RULE-001 không quy định naming convention cho file bên trong. Ghi nhận, không tự vá.

### 1B. Thư mục RULE-001 bắt buộc và **đã** tồn tại (không cần `mkdir`)

| Đường dẫn | Đã tồn tại? | RULE-001 bắt buộc? |
|---|:---:|:---:|
| `docs/010-Planning/` | ✅ Có | ✅ Có |
| `docs/020-Requirements/` | ✅ Có | ✅ Có |
| `docs/022-User-Stories/` | ✅ Có | ✅ Có |
| `docs/030-Specs/` | ✅ Có | ✅ Có |
| `docs/035-QA/` | ✅ Có | ✅ Có |
| `docs/040-Design/` | ✅ Có | ✅ Có |
| `docs/050-Research/` | ✅ Có | ✅ Có |
| `docs/060-Manuals/` | ✅ Có | ✅ Có |
| `docs/070-Deployment/` | ✅ Có | ✅ Có |
| `docs/080-Operations/` | ✅ Có | ✅ Có |
| `docs/999-Resources/` | ✅ Có | ✅ Có |
| `docs/999-Resources/Templates/` | ✅ Có | ✅ Có |

### 1C. Thư mục tồn tại nhưng **ngoài** RULE-001

| Đường dẫn | Đã tồn tại? | RULE-001 bắt buộc? | Ghi chú |
|---|:---:|:---:|---|
| `docs/010-Planning/pm-runs/` (+ 2 run dir + 2 `findings/`) | ✅ Có | ❌ Không có trong RULE-001 | **Run-state, cấm chuẩn hoá.** Chỉ báo cáo. Đã được `Planning-MOC.md` trỏ tới hợp lệ. |

### 1D. File bắt buộc (không phải thư mục)

| Đường dẫn | Đã tồn tại? | RULE-001 bắt buộc? |
|---|:---:|:---:|
| `docs/000-Index.md` | ❌ Không | ✅ Có — RULE-001 ghi nguyên văn `# "Trang chủ" - BẮT BUỘC phải có` |

> ⚠️ **Không tính `000-Index.md` vào con số 32.** Nó là file, PM tạo bằng `Write`, không phải `mkdir`. Chi tiết ở Mục 4.

---

## Mục 2 — Kiểm kê file trong `docs/` (loại trừ `pm-runs/**`)

**Tổng: 29 file.** (Toàn kho `docs/` có 42 file; 13 file thuộc `pm-runs/**` đã bị loại theo yêu cầu.)
Định nghĩa **stub** = chỉ có frontmatter + một dòng nội dung kiểu `*(Content to be added)*`.

| # | Đường dẫn | `id` | `type` | `status` | `created` | `updated` | Dòng | Stub? |
|---:|---|---|---|---|---|---|---:|:---:|
| 1 | `docs/010-Planning/OKRs.md` | `OKRS-001` | `okrs` | `draft` | 2026-02-04 | — | 10 | ✅ **Stub** |
| 2 | `docs/010-Planning/Roadmap.md` | `ROADMAP-001` | `roadmap` | `draft` | 2026-02-04 | — | 10 | ✅ **Stub** |
| 3 | `docs/010-Planning/Planning-MOC.md` | `MOC-PLANNING` | `moc` | `draft` | 2026-02-04 | — | 14 | ❌ (5 bullet link thật) |
| 4 | `docs/020-Requirements/Requirements-MOC.md` | `MOC-020` | `moc` | `live` | 2026-02-04 | 2026-02-04 | 56 | ❌ |
| 5 | `docs/022-User-Stories/Stories-MOC.md` | `MOC-STORIES` | `moc` | `draft` | 2026-02-04 | — | 14 | ❌ |
| 6 | `docs/030-Specs/Specs-MOC.md` | — | — | — | — | — | **0** | ❌ — **file rỗng hoàn toàn, không có frontmatter** |
| 7 | `docs/035-QA/QA-MOC.md` | `MOC-QA` | `moc` | `draft` | 2026-02-04 | — | 12 | ❌ |
| 8 | `docs/040-Design/Design-MOC.md` | — | — | — | — | — | **0** | ❌ — **file rỗng hoàn toàn, không có frontmatter** |
| 9 | `docs/050-Research/Analysis-Comic-Studio-Concept.md` | `RESEARCH-001` | `research` | `draft` | 2026-08-23 | 2026-08-23 | 1148 | ❌ |
| 10 | `docs/050-Research/Research-MOC.md` | `MOC-RESEARCH` | `moc` | `draft` | 2026-02-04 | 2026-08-23 | 20 | ❌ |
| 11 | `docs/060-Manuals/Manuals-MOC.md` | `MOC-MANUALS` | `moc` | `draft` | 2026-02-04 | — | 13 | ❌ |
| 12 | `docs/070-Deployment/Deployment-MOC.md` | `MOC-070` | `moc` | `draft` | 2026-03-03 | 2026-03-03 | 23 | ❌ |
| 13 | `docs/080-Operations/Operations-MOC.md` | `MOC-080` | `moc` | `draft` | 2026-03-03 | 2026-03-03 | 22 | ❌ |
| 14 | `docs/999-Resources/Glossary.md` | `GLOSSARY-001` | `glossary` | `live` | 2026-02-04 | 2026-08-23 | 103 | ❌ |
| 15 | `docs/999-Resources/Request.md` | — | — | — | — | — | 894 | ❌ — **KHÔNG có frontmatter**; file bắt đầu ngay ở `## 1. Core concept`. Vi phạm RULE-001 quy tắc #3. |
| 16 | `docs/999-Resources/Resources-MOC.md` | `MOC-999` | `moc` | `live` | 2026-02-26 | — | 33 | ❌ (thêm field `project: TNMCORE-OS`) |
| 17 | `docs/999-Resources/Templates/Template-Analysis.md` | `ANALYSIS-TEMPLATE` | `research` | `draft` | 2026-02-04 | — | 10 | ✅ **Stub** |
| 18 | `docs/999-Resources/Templates/Template-Component.md` | `COMPONENT-TEMPLATE` | `design-system` | `draft` | 2026-02-04 | — | 10 | ✅ **Stub** |
| 19 | `docs/999-Resources/Templates/Template-Spec.md` | `SPEC-TEMPLATE` | `technical-spec` | `draft` | 2026-02-04 | — | 10 | ✅ **Stub** |
| 20 | `docs/999-Resources/Templates/Template-Incident-Report.md` | `TEMP-INCIDENT` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 32 | ❌ |
| 21 | `docs/999-Resources/Templates/Template-PRD.md` | `TEMP-PRD` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 39 | ❌ |
| 22 | `docs/999-Resources/Templates/Template-Project-Charter.md` | `TEMP-CHARTER` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 32 | ❌ |
| 23 | `docs/999-Resources/Templates/Template-Release-Notes.md` | `TEMP-RELEASE` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 30 | ❌ |
| 24 | `docs/999-Resources/Templates/Template-Risk-Register.md` | `TEMP-RISK` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 20 | ❌ |
| 25 | `docs/999-Resources/Templates/Template-SDD.md` | `TEMP-SDD` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 33 | ❌ |
| 26 | `docs/999-Resources/Templates/Template-SRS.md` | `TEMP-SRS` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 36 | ❌ |
| 27 | `docs/999-Resources/Templates/Template-Status-Report.md` | `TEMP-STATUS` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 27 | ❌ |
| 28 | `docs/999-Resources/Templates/Template-Test-Plan.md` | `TEMP-TESTPLAN` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 31 | ❌ |
| 29 | `docs/999-Resources/Templates/Template-WBS-ETA.md` | `TEMP-WBS-ETA` | `template` | `draft` | 2026-03-03 | 2026-03-03 | 23 | ❌ |

### Quan sát cho PM

- **5 stub thật**: `OKRs.md`, `Roadmap.md`, `Template-Analysis.md`, `Template-Component.md`, `Template-Spec.md`. Hai cái đầu chính là hạng mục #2 và #3 của run này — điền nội dung là *authoring*, khớp Shape A của `brief.md`.
- **2 file 0 byte**: `Specs-MOC.md`, `Design-MOC.md`. Chúng **không** phải stub theo định nghĩa — không có cả frontmatter. Đây là vi phạm RULE-001 nặng hơn stub (MOC bắt buộc của 030 và 040 rỗng tuyệt đối). Thuộc Shape B ngoài scope.
- **Hai hệ id không nhất quán trong cùng thư mục `Templates/`**: nhóm 2026-02-04 dùng `{NAME}-TEMPLATE` + `type` là loại tài liệu đích (`research`, `design-system`, `technical-spec`); nhóm 2026-03-03 dùng `TEMP-{NAME}` + `type: template`. Ghi nhận cho một run chuẩn hoá sau, **không** đụng trong run này (brief §*Ngoài scope* mục 3).
- **`Request.md` thiếu frontmatter hoàn toàn** — chưa từng được ghi nhận trong `brief.md`. Đây là phát hiện mới.

---

## Mục 3 — MOC hiện có và tình trạng link

Tất cả 11 MOC được liệt kê. Mỗi đích link đã được kiểm tra sự tồn tại trên đĩa.
**Tổng: 25 link chết / 31 link nội bộ.**

| MOC | Trỏ tới | Phân giải được ✅ | **Link chết** ❌ (đường dẫn đích) |
|---|---|---|---|
| `docs/010-Planning/Planning-MOC.md` | 5 link | `./Roadmap.md`, `./OKRs.md`, `./pm-runs/README.md` | `docs/010-Planning/Sprints/`<br>`docs/010-Planning/Implementation-Plans/` |
| `docs/020-Requirements/Requirements-MOC.md` | 3 link | *(không có)* | `docs/020-Requirements/BRD/`<br>`docs/020-Requirements/PRD-TNMCORE-OS.md`<br>`docs/020-Requirements/Use-Cases/` |
| `docs/022-User-Stories/Stories-MOC.md` | 5 link | *(không có)* | `docs/022-User-Stories/Epics/`<br>`docs/022-User-Stories/Active-Sprint/`<br>`docs/022-User-Stories/Backlog/`<br>`docs/022-User-Stories/Backlog/Story-Request-OTP.md`<br>`docs/022-User-Stories/Backlog/Story-Verify-OTP.md` |
| `docs/030-Specs/Specs-MOC.md` | **0 link — file 0 byte** | — | — (không có link để chết; bản thân MOC rỗng là lỗi) |
| `docs/035-QA/QA-MOC.md` | 3 link | *(không có)* | `docs/035-QA/Test-Plans/`<br>`docs/035-QA/Test-Cases/`<br>`docs/035-QA/Automation/` |
| `docs/040-Design/Design-MOC.md` | **0 link — file 0 byte** | — | — (như trên) |
| `docs/050-Research/Research-MOC.md` | 1 link | `./Analysis-Comic-Studio-Concept.md` | **0 link chết** ✅ |
| `docs/060-Manuals/Manuals-MOC.md` | 4 link | *(không có)* | `docs/060-Manuals/User-Guide/`<br>`docs/060-Manuals/Admin-Guide/`<br>`docs/060-Manuals/User-Guide/Cursor-CLI-Workflow-Mapping.md`<br>`docs/060-Manuals/User-Guide/Cursor-CLI-Snippets.md` |
| `docs/070-Deployment/Deployment-MOC.md` | 3 link | *(không có)* | `docs/070-Deployment/Releases/`<br>`docs/070-Deployment/CHANGELOG.md`<br>`docs/070-Deployment/Runbooks/` |
| `docs/080-Operations/Operations-MOC.md` | 2 link | *(không có)* | `docs/080-Operations/Incidents/`<br>`docs/080-Operations/SLAs/` |
| `docs/999-Resources/Resources-MOC.md` | 5 link nội dung (+3 anchor nội bộ) | `./Glossary.md`<br>`../../knowledge-base/99-Templates/Documents-Template.md` | `docs/999-Resources/Templates/Template-Daily-Report.md`<br>`docs/999-Resources/Meeting-Notes/`<br>`docs/000-Index.md` (viết là `../000-Index.md`, dòng 32) |

### Ghi chú quan trọng cho PM

1. **`Research-MOC.md` là MOC duy nhất sạch 0 link chết.** Hai mục `Competitor-Analysis/` và `User-Interviews/` trong đó được viết bằng **backtick, KHÔNG phải markdown link** — có chú thích `*(chưa tồn tại)*` ngay tại chỗ. Đó là placeholder có chủ đích, **không tính là link chết**. Đây là mẫu xử lý tốt nhất trong kho, PM có thể nhân bản cho các MOC khác.
2. **Delta với `brief.md`**: brief §*Ngoài scope* mục 1 ghi *"2 link chết trong `Resources-MOC.md`"*. Kiểm tra thực tế cho **3**: `Template-Daily-Report.md`, `../000-Index.md`, **và `./Meeting-Notes/`** (thư mục này cũng chưa tồn tại — nó nằm trong danh sách 32 ở Mục 1, dòng #32). Brief bỏ sót cái thứ ba.
3. **Phân tách 25 link chết theo cách chữa** — quan trọng để PM scope đúng:

   **(a) 17 link trỏ tới THƯ MỤC → tự lành** sau khi thực thi trọn vẹn danh sách 32 `mkdir` ở Mục 1:
   Planning 2 (`Sprints/`, `Implementation-Plans/`) · Requirements 2 (`BRD/`, `Use-Cases/`) · Stories 3 (`Epics/`, `Active-Sprint/`, `Backlog/`) · QA 3 · Manuals 2 (`User-Guide/`, `Admin-Guide/`) · Deployment 2 (`Releases/`, `Runbooks/`) · Operations 2 · Resources 1 (`Meeting-Notes/`).

   **(b) 8 link trỏ tới FILE → `mkdir` KHÔNG cứu được:**
   - `docs/000-Index.md` — **run này sẽ tạo** ⇒ lành trong run này
   - `docs/020-Requirements/PRD-TNMCORE-OS.md`
   - `docs/022-User-Stories/Backlog/Story-Request-OTP.md`
   - `docs/022-User-Stories/Backlog/Story-Verify-OTP.md`
   - `docs/060-Manuals/User-Guide/Cursor-CLI-Workflow-Mapping.md`
   - `docs/060-Manuals/User-Guide/Cursor-CLI-Snippets.md`
   - `docs/070-Deployment/CHANGELOG.md`
   - `docs/999-Resources/Templates/Template-Daily-Report.md`

   ⇒ **Sau run này còn đúng 7 link chết**, tất cả thuộc run Shape B tương lai. Năm trong bảy (`PRD-TNMCORE-OS`, 2 × `Story-*-OTP`, 2 × `Cursor-CLI-*`) là **tàn dư của dự án TNMCORE-OS**, không thuộc `comic-studio`. Chỉ báo cáo, không xoá.
4. **Không MOC nào dùng wiki-link `[[...]]`** — toàn kho tuân thủ RULE-001 quy tắc #5. Xác minh bằng **đọc toàn văn 11 MOC** (mọi MOC ≤ 56 dòng nên đọc trọn được), không phải bằng grep.

---

## Mục 4 — `docs/000-Index.md`

### 4.1. Xác nhận hiện trạng

`docs/000-Index.md` **KHÔNG tồn tại** (xác minh bằng `find docs -type f`). RULE-001 dòng 129 ghi nguyên văn:
`├── 000-Index.md                        # "Trang chủ" - BẮT BUỘC phải có`

### 4.2. File đang trỏ tới nó → **đúng 2 link chết**

| File nguồn | Dòng | Cú pháp | Đích | Trạng thái |
|---|---:|---|---|---|
| `docs/999-Resources/Resources-MOC.md` | 32 | `[Documentation Master Index](../000-Index.md)` | `docs/000-Index.md` | ❌ **Chết** |
| `knowledge-base/00-Index.md` | 66 | `[Project Documentation Index](../docs/000-Index.md)` | `docs/000-Index.md` | ❌ **Chết** |

> **Cảnh báo chống-đuổi-hình-bắt-bóng**: `000-Index.md` còn xuất hiện ở 8 chỗ khác — trong `pm-runs/**` (README, verdict, run-plan, 2 brief) và trong chính RULE-001 (dòng 59, 129, 245). **Tất cả đều là prose/inline-code, KHÔNG phải markdown link.** Chúng không chết và không cần sửa. Chỉ có **2** link thật ở bảng trên.
>
> Lưu ý thêm: sửa `knowledge-base/00-Index.md` nằm **ngoài `docs/`** — PM cân nhắc riêng, không thuộc scaffolding hạng mục #6.

### 4.3. Đề xuất cấu trúc nội dung

Nguyên tắc: **chỉ trỏ tới thứ tồn tại thật trên đĩa sau khi run này kết thúc.** Không liệt kê tài liệu tưởng tượng.

```
---
id: INDEX-000
type: index
status: live
project: comic-studio
created: 2026-08-23
updated: 2026-08-23
---

# 📚 Documentation Master Index — comic-studio
```

| Mục đề xuất | Nội dung trỏ tới (**tồn tại thật**) | Ghi chú |
|---|---|---|
| **Bắt đầu từ đâu** | `./050-Research/Analysis-Comic-Studio-Concept.md` (1.148 dòng — thẩm định ý tưởng, 4 verdict) · `./999-Resources/Request.md` (894 dòng — concept gốc) | Hai tài liệu nội dung **duy nhất** đang có thực trong kho |
| **010 · Planning** | `./010-Planning/Planning-MOC.md` · `Roadmap.md` · `OKRs.md` | ⚠️ Roadmap/OKRs hiện là stub → run này điền. **Thêm Charter, Risk-Register, MVP-Scope vào đây sau khi writer tạo xong** |
| **020 · Requirements** | `./020-Requirements/Requirements-MOC.md` | MOC có nội dung nhưng 3/3 link chết — ghi rõ "chưa có tài liệu" |
| **022 · User Stories** | `./022-User-Stories/Stories-MOC.md` | MOC 5/5 link chết |
| **030 · Specs** | `./030-Specs/Specs-MOC.md` | ⚠️ **MOC rỗng 0 byte** — phải chú thích, không được giả vờ nó dùng được |
| **035 · QA** | `./035-QA/QA-MOC.md` | 3/3 link chết |
| **040 · Design** | `./040-Design/Design-MOC.md` | ⚠️ **MOC rỗng 0 byte** — chú thích như trên |
| **050 · Research** | `./050-Research/Research-MOC.md` + `Analysis-Comic-Studio-Concept.md` | MOC sạch nhất kho. **Thêm `Analysis-Market-Competitor-Landscape.md` (A6) sau khi tạo** |
| **060 · Manuals** | `./060-Manuals/Manuals-MOC.md` | 4/4 link chết, 2 cái là tàn dư TNMCORE-OS |
| **070 · Deployment** | `./070-Deployment/Deployment-MOC.md` | 3/3 link chết |
| **080 · Operations** | `./080-Operations/Operations-MOC.md` | 2/2 link chết |
| **090 · Archive** | *(thư mục rỗng sau `mkdir`)* | Chỉ nêu tên + mục đích, không link file |
| **999 · Resources** | `./999-Resources/Resources-MOC.md` · `Glossary.md` (40 term, 7 nhóm) · `Request.md` · `Templates/` (13 file) | Nên **liệt kê tên 13 template** ngay tại đây — hiện không MOC nào liệt kê chúng (brief đã ghi nhận) |
| **Run-state (`/pm-doc`)** | `./010-Planning/pm-runs/README.md` · 2 thư mục run | Chỉ trỏ tới README + tên run. **Không index từng file run-state.** |
| **Contract & quy ước** | `../knowledge-base/99-Templates/Documents-Template.md` (RULE-001) · `../knowledge-base/00-Index.md` | Đóng vòng link chết #2 ở bảng 4.2 |
| **Nợ kỹ thuật đã biết** | Bảng ngắn: 2 MOC rỗng 0 byte, 5 link chết loại-file, `Request.md` thiếu frontmatter | Giữ minh bạch thay vì che giấu; trỏ tới run Shape B tương lai |

**Hai điều cần tránh khi PM viết file này:**
1. Đừng copy nội dung MOC vào Index — Index chỉ là **lớp điều hướng một cấp** (trỏ tới MOC, MOC trỏ tới tài liệu). Copy sẽ tạo duplicate content phải đồng bộ hai nơi.
2. Đừng liệt kê 32 thư mục vừa `mkdir` như thể chúng có nội dung. Thư mục rỗng nên xuất hiện dưới dạng backtick + `*(chưa có tài liệu)*` — đúng mẫu `Research-MOC.md` đang dùng.

---

## Mục 5 — Cấu trúc 2 template PM sắp dùng làm khuôn

### 5.1. `docs/999-Resources/Templates/Template-Project-Charter.md`

**Verdict: KHUÔN DÙNG ĐƯỢC — nhưng nông.** 32 dòng, không phải stub. Có đủ 6 H2 với gợi ý một dòng mỗi mục. **Không có bảng nào.**

Frontmatter: `id: TEMP-CHARTER` · `type: template` · `status: draft` · `created/updated: 2026-03-03`

| Cấp | Heading (đúng thứ tự) | Nội dung có sẵn |
|:---:|---|---|
| H1 | `# 📜 Template: Project Charter` | — |
| H2 | `## 1. Project Information` | 3 bullet rỗng: `**Project Name:**`, `**Sponsor:**`, `**Manager:**` |
| H2 | `## 2. Business Case` | 1 dòng gợi ý: "Lý do tại sao dự án này được thực hiện." |
| H2 | `## 3. Project Objectives` | "Các mục tiêu đo lường được." |
| H2 | `## 4. High-Level Requirements` | "Các yêu cầu cốt lõi." |
| H2 | `## 5. Stakeholders` | "Danh sách các bên liên quan." |
| H2 | `## 6. Assumptions & Constraints` | "Các giả định và ràng buộc." |
| — | Footer: `*Generated by TNMCORE-OS PM Role.*` | — |

**Không có H3 nào.** Không có bảng.

> **Khoảng trống PM phải tự lấp**: yêu cầu gốc của hạng mục #1 đòi **Stakeholder Matrix (RACI)** — template chỉ cho `## 5. Stakeholders` dưới dạng văn xuôi, **không có bảng RACI**. `outline.md` phải tự định nghĩa cột. Gợi ý bám bối cảnh "1 dev": ma trận RACI với 1 người thật + các vai trò AI agent + bên ngoài (luật sư SHTT, model provider) — nếu không nó suy biến thành một dòng.
>
> Ngoài ra template **thiếu**: `Scope In / Scope Out`, `Success Criteria`, `Milestones`, `Budget`, `Sign-off`. Charter cho `comic-studio` nhiều khả năng cần ít nhất *Scope In/Out* (vì có `MVP-Scope.md` riêng — cần định rõ ranh giới giữa hai tài liệu để không duplicate).

### 5.2. `docs/999-Resources/Templates/Template-Risk-Register.md`

**Verdict: KHUÔN DÙNG ĐƯỢC — tối giản nhưng đủ xương sống.** 20 dòng, không phải stub. **Có 1 bảng.**

Frontmatter: `id: TEMP-RISK` · `type: template` · `status: draft` · `created/updated: 2026-03-03`

| Cấp | Heading (đúng thứ tự) | Nội dung có sẵn |
|:---:|---|---|
| H1 | `# ⚠️ Template: Risk Register` | — |
| H2 | `## 1. Risk Matrix Overview` | 1 dòng gợi ý: "(Mô tả cách đánh giá Impact vs Probability)" — **chưa có ma trận thật** |
| H2 | `## 2. Risk Log` | **Bảng 7 cột** + 1 hàng ví dụ |
| — | Footer: `*Generated by TNMCORE-OS PM Role.*` | — |

**Không có H3 nào.**

**Bảng `## 2. Risk Log` — mô tả cột:**

| # | Cột | Kiểu dữ liệu quan sát từ hàng ví dụ | Ghi chú |
|---:|---|---|---|
| 1 | `ID` | `R-01` | Định danh tuần tự, prefix `R-` |
| 2 | `Risk Description` | `API Rate Limit` | Text ngắn |
| 3 | `Probability` | `High` | Thang chữ (High/Med/Low) — **template không định nghĩa thang chính thức** |
| 4 | `Impact` | `Med` | Thang chữ |
| 5 | `Score` | `6` | Số. **Công thức không được nêu ở đâu** — `High×Med = 6` gợi ý thang 1–3 nhân nhau (3×2=6), nhưng đây là **suy luận, không xác nhận được** từ template |
| 6 | `Mitigation Plan` | `Caching, Retry logic` | Text |
| 7 | `Owner` | `Architect` | Tên vai trò |

Căn lề bảng: `| :--- |` (left-align) cho cả 7 cột.

> **Khoảng trống PM phải lấp**:
> - `## 1. Risk Matrix Overview` là **placeholder rỗng** — PM phải viết thang Probability/Impact và công thức `Score` thật, nếu không `Score` sẽ là con số vô nghĩa.
> - Thiếu các cột mà một Risk Register thực chiến thường cần: `Category` (pháp lý / kỹ thuật / thị trường / vận hành), `Status` (open/mitigating/closed/accepted), `Trigger` (dấu hiệu rủi ro đang xảy ra), `Residual Risk`. Với `comic-studio` thì **`Category`** đặc biệt đáng thêm — run trước đã tách rõ rủi ro **pháp lý** (safe harbour, TDM thương mại, NĐ 134/2026/NĐ-CP) khỏi rủi ro **kỹ thuật** (error cascade, attribute binding) và **kinh tế** (GRR 23%, COGS).
> - Cột `Owner` với đội 1 người sẽ luôn là cùng một giá trị → cân nhắc giữ nhưng ghi rõ, hoặc đổi nghĩa thành "vai trò chịu trách nhiệm" theo hệ role của TNMCORE-OS.

### 5.3. Toàn bộ file trong `docs/999-Resources/Templates/` — **13 file**

| # | Tên file | Dòng | Tình trạng |
|---:|---|---:|---|
| 1 | `Template-Analysis.md` | 10 | ⚠️ **Stub** — không dùng được làm khuôn (brief §*Ngoài scope* mục 2 đã ghi nhận) |
| 2 | `Template-Component.md` | 10 | ⚠️ **Stub** |
| 3 | `Template-Incident-Report.md` | 32 | ✅ Khuôn dùng được |
| 4 | `Template-PRD.md` | 39 | ✅ Khuôn dùng được (dài nhất) |
| 5 | `Template-Project-Charter.md` | 32 | ✅ Khuôn dùng được — **run này dùng** |
| 6 | `Template-Release-Notes.md` | 30 | ✅ Khuôn dùng được |
| 7 | `Template-Risk-Register.md` | 20 | ✅ Khuôn dùng được — **run này dùng** |
| 8 | `Template-SDD.md` | 33 | ✅ Khuôn dùng được |
| 9 | `Template-Spec.md` | 10 | ⚠️ **Stub** |
| 10 | `Template-SRS.md` | 36 | ✅ Khuôn dùng được |
| 11 | `Template-Status-Report.md` | 27 | ✅ Khuôn dùng được |
| 12 | `Template-Test-Plan.md` | 31 | ✅ Khuôn dùng được |
| 13 | `Template-WBS-ETA.md` | 23 | ✅ Khuôn dùng được (có bảng WBS) |

> **KHÔNG có template nào cho Roadmap, OKRs, hay MVP-Scope.** Ba tài liệu này (hạng mục #2, #3, #5) không có khuôn sẵn — `outline.md` của run phải là contract cấu trúc duy nhất cho chúng.
> **KHÔNG có `Template-Daily-Report.md`** dù `Resources-MOC.md` dòng 22 đang link tới nó (xem Mục 3).
> Cả 13 file **không được liệt kê trong bất kỳ MOC nào** — `Resources-MOC.md` chỉ liệt kê đúng 1 template, và cái đó lại không tồn tại.

---

## Mục 6 — Thuật ngữ: `docs/999-Resources/Glossary.md`

Frontmatter: `id: GLOSSARY-001` · `type: glossary` · `status: live` · `created: 2026-02-04` · `updated: 2026-08-23` · 103 dòng.
Đếm bằng cách quét bullet `- **Term**` trong từng khối H2.

| # | Nhóm (H2) | Dòng | Số term |
|---:|---|---:|---:|
| 1 | `## Xác thực & bảo mật` | 24 | **3** |
| 2 | `## Kiến trúc pipeline comic-studio` | 32 | **7** |
| 3 | `## Mô hình dữ liệu & thời gian` | 44 | **7** |
| 4 | `## Sinh ảnh & kiểm tra nhất quán` | 56 | **6** |
| 5 | `## Chữ & trình bày` | 67 | **4** |
| 6 | `## Quy trình & vận hành` | 76 | **5** |
| 7 | `## SaaS & multi-tenancy` | 86 | **8** |
| | **TỔNG** | | **40** |

**Hai H2 KHÔNG phải nhóm term** (không đếm vào 40):
- `## Mục lục` (dòng 11) — 8 anchor link nội bộ, tất cả phân giải đúng
- `## Tài liệu tham khảo` (dòng 99) — 3 link ngoài, **cả 3 đều sống**: `../050-Research/Analysis-Comic-Studio-Concept.md`, `./Request.md`, `../../knowledge-base/99-Templates/Documents-Template.md`

### Ghi chú cho PM

- Con số **40** khớp chính xác với "~40 term domain thêm ở run trước". Nhóm 1 (`Xác thực & bảo mật`, 3 term: OTP, OTP Expiry, Rate Limit) là **tàn dư TNMCORE-OS**, không liên quan `comic-studio` — 37 term còn lại mới là domain của dự án này.
- `Mục lục` liệt kê đủ 7 nhóm + `Tài liệu tham khảo` → **nếu run này thêm nhóm term mới, PM phải cập nhật cả `Mục lục`**, nếu không sẽ lệch.
- Glossary là file `status: live` duy nhất trong `docs/` cùng với `Requirements-MOC.md` và `Resources-MOC.md`.
- Một số term đã có **cảnh báo định nghĩa đã bị sửa** (`Continuity Checker`, `Layout Score` — đánh dấu ⚠️ ngay trong định nghĩa). Writer của run này **phải dùng nghĩa mới**, không được lấy nghĩa cũ từ `Request.md`.

---

## Tổng kết cho PM — 6 con số cần nhớ

| Chỉ số | Giá trị |
|---|---|
| Thư mục phải `mkdir` (Mục 1) | **32** |
| File trong `docs/` ngoài `pm-runs/` (Mục 2) | **29** (5 stub, 2 file 0 byte, 1 thiếu frontmatter) |
| Link chết trong các MOC (Mục 3) | **25** / 31 link nội bộ — **17** trỏ tới thư mục (tự lành sau `mkdir`), **8** trỏ tới file (không lành). Trong 8 cái đó, `000-Index.md` lành trong run này ⇒ **còn 7 link chết sau run** |
| File link chết tới `000-Index.md` (Mục 4) | **2** (1 trong `docs/`, 1 trong `knowledge-base/`) |
| Template trong `Templates/` (Mục 5) | **13** (10 dùng được, 3 stub) — **0 khuôn cho Roadmap / OKRs / MVP-Scope** |
| Term trong Glossary (Mục 6) | **40** trong **7 nhóm** |

### Ba phát hiện mới, chưa có trong `brief.md`

1. **`docs/999-Resources/Request.md` (894 dòng) hoàn toàn không có YAML frontmatter** — vi phạm RULE-001 quy tắc #3. Là một trong hai tài liệu nội dung thật của kho.
2. **`Resources-MOC.md` có 3 link chết, không phải 2** — brief bỏ sót `./Meeting-Notes/`.
3. **`Specs-MOC.md` và `Design-MOC.md` là file 0 byte**, không phải "MOC rỗng nội dung" như brief mô tả — chúng không có cả frontmatter, nặng hơn một bậc.

---

_`context-auditor` · run `2026-08-23-khoi-tao-tai-lieu-planning-comic-studio` · Bước 2 fan-out_
_Read-only ngoài chính file này. Không thư mục nào được tạo, không MOC nào bị sửa, không gì bị xoá._
