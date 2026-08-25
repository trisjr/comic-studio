---
id: UC-09
type: use-case
status: draft
project: comic-studio
created: 2026-08-24
---

# UC-09 — Export chapter (lấy thành phẩm ra khỏi hệ thống)

> [!IMPORTANT]
> **Đây là luồng ở BIÊN RA của sản phẩm.** CF-8.10: export là *"thứ **duy nhất** trong MVP4 người dùng thật sự nhận được"* ⇒ ưu tiên **được nâng lên sớm**. Với `Roadmap` §5.2, export không còn là hạng mục MVP4 mà là **điều kiện doanh thu** của Tầng 1.
>
> ⚠️ **Export là bước COMPOSITE, không phải bước "lấy ảnh gốc ra".** Thoại nằm ở **`typeset layer` tách khỏi ảnh** (`Glossary.md` *typeset layer*: ảnh được sinh **không có chữ**; bubble và thoại render bằng code lên trên). Vì vậy thành phẩm chỉ tồn tại **sau khi** composite — trước đó nó không phải một file, mà là hai tầng dữ liệu.
>
> ⛔ **KHÔNG viết renderer/compositor mới.** Export **tái dùng compositor của preview** ([BRD-008](../BRD/BRD-008-Quality-And-Operations.md) mục 5 hàng 10 · CF-9.1 *"không viết renderer từ đầu"*).

**Quy ước nhãn nguồn** (kế thừa nguyên vẹn — *số và nhãn là một cặp không tách rời*): `[OFF]` official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` thứ cấp · `[EM]` ước lượng/phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.

## Mục lục

1. [Thông tin](#1-thông-tin)
2. [Mục tiêu](#2-mục-tiêu)
3. [Main flow](#3-main-flow)
4. [Alternative flow](#4-alternative-flow)
5. [Exception flow](#5-exception-flow)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Thông tin

| Trường | Giá trị |
|---|---|
| **Primary actor** | **Tác giả truyện chữ** (không biết vẽ) — CF-1.5 `[CHỐT]`. ⛔ Không phải hoạ sĩ (`CẤM-17`) |
| **Secondary actor** | **Founder với vai operator** — chỉ xuất hiện ở [AF-2](#4-alternative-flow) (export hồ sơ tenant khi KILL, `BR-007-09`). Không tham gia luồng chính |
| **Mốc MVP** | **MVP2 — chỉ PDF** (`H4` = `🟡 preview server-side`; exit criterion **`M2-5`**) → **MVP3 — đủ định dạng PDF / CBZ / webtoon** (`H4` = `✅`). ⚠️ MVP3 **NGOÀI horizon** 09/2026–02/2027 (`Roadmap` §5.1) |
| **BRD module** | [BRD-008 — Quality And Operations](../BRD/BRD-008-Quality-And-Operations.md) — hàng `H4`, requirement `BR-008-11`, `BR-008-12`, `BR-008-13`. Phụ thuộc chéo: [BRD-004](../BRD/BRD-004-Minimum-Editor.md) (compositor của preview, thành phần `#4`) · [BRD-003](../BRD/BRD-003-Comic-Director-And-Layout.md) (`C7` hai human gate) · [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) (`BR-007-06` dấu máy đọc ở export path, `BR-007-09` export hồ sơ khi KILL) |
| **Điều kiện tiên quyết** | (1) Chapter đã có **page layout** và **panel có ảnh đã được chọn** (`approved_generation_id` — [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) mục 5.3, thay thế cho tree view của `D6`); (2) **Mọi page của chapter đã qua CẢ HAI human gate** — speaker attribution + dialogue condensation (`MVP-Scope` §3 `C7` · `Roadmap` §2 **`M2-4`**); (3) **preview server-side đã chạy được** — vì compositor của export **là** compositor của preview; (4) ⚠️ **Persona / định nghĩa *"đủ tốt"* của người dùng: `TBD`** — findings §6.2 `KT-1` ghi *"KHÔNG CÓ persona / JTBD / định nghĩa 'đủ tốt' trong toàn repo"* |

### 1.1 ⚠️ Sắc thái bắt buộc — `F6` Tầng 1 là một LỰA CHỌN, không phải kế hoạch đã chốt

> [!WARNING]
> UC này **chạm tới** điều kiện doanh thu của Tầng 1 (`F6` · `BR-008-13`). Sắc thái phải viết đúng:
>
> **Tầng 1 bán được (`$4–8/tháng`, KHÔNG image gen, margin ~90%) là một LỰA CHỌN `[EM]` của [`Roadmap` §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) — KHÔNG phải một kế hoạch đã chốt.** Nguyên văn nhãn của Roadmap: *"`[EM]` — suy luận của em, không có trong bảng CF"*.
>
> Nó gated on **bốn** thứ phải thoả **đồng thời**: (1) **`M2-5`** export/preview server-side hoàn thành ở MVP2 · (2) **`M2-6`** checklist safe harbour `X-a` xong trước khi mở cho người ngoài · (3) ⭐ **`G0` PASS** — *"dòng code thương mại đầu tiên"* · (4) **quyết định của Founder tại gate `G2`**.
>
> Roadmap ghi ra lựa chọn này *"để anh **thấy được lựa chọn**, không phải để mặc định chọn nó"*. ⛔ UC này **không** viết như thể việc bán Tầng 1 đã được quyết.

---

## 2. Mục tiêu

**Tác giả truyện chữ lấy được thành phẩm của mình ra khỏi hệ thống dưới dạng một file đọc được ở nơi khác** — MVP2: **PDF của 1 chapter hoàn chỉnh**; MVP3: thêm **CBZ** và **webtoon**.

Ba điều làm UC này khác mọi UC khác của tác giả:

| # | Điểm khác biệt | Căn cứ |
|---|---|---|
| **1** | **Đây là điểm duy nhất giá trị rời khỏi hệ thống.** Mọi UC trước (`UC-01` → `UC-08`) tích luỹ dữ liệu **bên trong** sản phẩm; UC-09 là nơi người dùng **nhận được một thứ** | CF-8.10 · findings §1.2 hàng `H4` |
| **2** | **Nó là bước COMPOSITE, không phải bước tải file.** Thành phẩm không tồn tại sẵn ở đâu: ảnh panel không có chữ, thoại nằm ở `typeset layer` riêng. Export là nơi hai tầng gặp nhau lần đầu dưới dạng một artifact | `Glossary.md` *typeset layer* · `MVP-Scope` §3 `A2` · CF-8.11c |
| **3** | **Nó là cửa cuối cùng cưỡng chế hai human gate.** `M2-4` được đo bằng **sự VẮNG MẶT của đường code bypass**. Nếu export không kiểm hai gate thì **export CHÍNH LÀ đường bypass** | `Roadmap` §2 **`M2-4`** · `MVP-Scope` §3 `C7` · CF-8.8 |

⛔ **Ngoài mục tiêu**: UC này **không** đo chất lượng trang, **không** chấm layout, **không** chạy Continuity Checker. Câu hỏi *"trang này đọc có ổn không?"* (CF-10.10) thuộc HITL gate của [BRD-008](../BRD/BRD-008-Quality-And-Operations.md) `H1`, không thuộc luồng export.

---

## 3. Main flow

**Bối cảnh mốc: MVP2 — định dạng khả dụng chỉ có PDF** (`H4` = `🟡 preview server-side`).

| # | Actor thực hiện | Hành động | Căn cứ |
|---|---|---|---|
| **1** | **Tác giả truyện chữ** | Mở chapter đã hoàn thành trong workspace của tenant mình và chọn hành động *Export* | `MVP-Scope` §3 `H4` · `E1`/`KC-5` (mọi truy cập bị chặn theo `tenant_id` + RLS) |
| **2** | **Hệ thống** | **Kiểm tra điều kiện xuất bản trước mọi việc khác**: mọi page của chapter đã qua **cả hai** human gate (speaker attribution + dialogue condensation). ⛔ **Không có tham số, cờ hay đường code nào bỏ qua bước này** | `Roadmap` §2 **`M2-4`** (*"không tồn tại đường code nào xuất bản page mà chưa qua cả hai"*) · `MVP-Scope` §3 `C7` · CF-8.8 (*không phải tuỳ chọn*) |
| **3** | **Hệ thống** | Kiểm tra project không ở trạng thái **disable-access** do takedown | [`BR-007-04`](../BRD/BRD-007-Legal-And-Compliance.md) (soft-delete + disable-access **cấp project**) · [UC-11](./UC-11-Handle-Takedown-Request.md) |
| **4** | **Hệ thống** | Hiển thị **các định dạng khả dụng theo mốc hiện tại**: MVP2 = **PDF**; CBZ và webtoon hiển thị là **chưa có** (không phải lỗi) | `MVP-Scope` §3 `H4` (MVP2 `🟡` → MVP3 `✅`) · `BR-008-11`, `BR-008-12` |
| **5** | **Tác giả truyện chữ** | Chọn **PDF** và xác nhận export | `BR-008-11` |
| **6** | **Hệ thống** | Chạy **composite server-side** — **tái dùng compositor của preview**, không phải một renderer thứ hai | `M2-5` (*"từ preview server-side"*) · [BRD-008](../BRD/BRD-008-Quality-And-Operations.md) mục 5 hàng 10 · CF-9.1 |
| **7** | **Hệ thống** | Với **mỗi page**: lấy ảnh panel đã được chọn (`approved_generation_id`), đặt vào toạ độ **chuẩn hoá 0–1** của `page_layout`, rồi **render `typeset layer` (bubble + thoại + đuôi trỏ) bằng code lên trên** — ⛔ **không** nhờ image model render chữ | `MVP-Scope` §4.1 (toạ độ 0–1 trong `page_layout JSONB`) · `Glossary.md` *typeset layer* · exit criterion `G1-e` (**0** panel nhờ model render chữ) |
| **8** | **Hệ thống** | Ghép các page composite theo thứ tự thành **một file PDF của 1 chapter hoàn chỉnh** | `Roadmap` §2 **`M2-5`** |
| **9** | **Hệ thống** | Ghi **`change_log`** cho hành động export của người dùng (`KC-2` yêu cầu ghi **mọi** hành động người dùng), commit **cùng transaction** với artifact theo `KC-4` | `MVP-Scope` §6 `KC-2`, `KC-4` · [`BR-007-01`](../BRD/BRD-007-Legal-And-Compliance.md), `BR-007-02` |
| **10** | **Hệ thống** | Trả file PDF cho tác giả tải về | `BR-008-11` |
| **11** | **Tác giả truyện chữ** | Nhận file và dùng nó ở ngoài hệ thống (đọc, gửi, đăng ở nơi khác) | CF-8.10 (*"thứ duy nhất người dùng thật sự nhận được"*) |

> [!NOTE]
> **Bước 2 và bước 3 phải nằm TRƯỚC bước 6.** Lý do không phải hiệu năng mà là bản chất: composite là nơi tiêu tài nguyên; kiểm sau khi composite nghĩa là hệ thống **đã tạo ra thành phẩm của một page chưa được duyệt** — và `M2-4` đo *"không tồn tại đường code nào **xuất bản** page mà chưa qua cả hai"*.

---

## 4. Alternative flow

| ID | Nhánh | Ai làm gì | Căn cứ |
|---|---|---|---|
| **AF-1** | **Export đủ định dạng (MVP3)** | **Tác giả** chọn **CBZ** hoặc **webtoon** thay vì PDF ở bước 5. **Hệ thống** dùng **cùng một compositor**, chỉ khác bước đóng gói cuối. ⚠️ **MVP3 — NGOÀI horizon** | `MVP-Scope` §3 `H4` (MVP3 `✅`) · `BR-008-12` · `Roadmap` §5.1 |
| **AF-2** | **Export hồ sơ tenant khi KILL** — actor đổi sang **Founder (operator)** | **Founder** kích hoạt export dữ liệu đầy đủ cho **từng tenant**, **gồm cả `change_log` + `field_provenance`** — vì đó là **hồ sơ chứng minh quyền tác giả của khách**. Kèm: thông báo trước **≥30 ngày** cho mọi tenant đang trả phí và **ngừng thu tiền ngay tại thời điểm thông báo**. Dùng **chung cơ chế** với `H4` | [`BR-007-09`](../BRD/BRD-007-Legal-And-Compliance.md) · `MVP-Scope` §8.2 · §6 `KC-2`, `KC-3` |
| **AF-3** | **Nhúng dấu máy đọc vào export path (từ MVP3)** | **Hệ thống** nhúng **machine-readable marking** cho nội dung do AI tạo tại bước 8, theo **diễn giải RỘNG** đã chốt ở `Charter` §7 `C4`. ⚠️ **Phạm vi thật: `TBD`** — hai nguồn trong repo mô tả phạm vi khoản 4 Điều 11 **khác nhau**; và **SynthID của provider có thoả nghĩa vụ hay không: `TBD`, phải verify, không giả định**. Là **câu `Q2` của gate `G0`** | [`BR-007-06`](../BRD/BRD-007-Legal-And-Compliance.md) · `GP-4` (MVP1 `🟡` → MVP3 `✅`, deadline tuân thủ **~01/03/2027**) · CF-7.7 `[OFF]` · findings §6.1 `MT-6` |
| **AF-4** | **Chapter chỉ có một phần page đạt điều kiện** | **Tác giả** chọn export **chỉ các page đã qua hai gate**. ⚠️ **`TBD` — repo KHÔNG trả lời**: `M2-5` chỉ định nghĩa *"PDF của **1 chapter hoàn chỉnh**"*, không có nguồn nào nói export từng phần có được phép hay không. **Không tự phân xử** — câu hỏi mang tới Founder | `Roadmap` §2 **`M2-5`** · findings §6.2 (nguyên tắc *"không phân xử ngầm"*) |

---

## 5. Exception flow

**Năm nhánh. Nhánh `EF-1` là nhánh load-bearing của cả UC.**

| ID | Điều kiện phát sinh | Ai làm gì | Kết cục | Căn cứ |
|---|---|---|---|---|
| **EF-1** ⭐ | **Có ≥1 page của chapter CHƯA qua đủ hai human gate** | **Hệ thống** **TỪ CHỐI** export tại bước 2, liệt kê các page còn thiếu gate nào, và điều hướng tác giả về [UC-04](./UC-04-Human-Gate-Speaker-Attribution.md) / [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) | **Không có file nào được sinh ra.** ⛔ Không có cờ *"export nháp"*, *"bỏ qua kiểm tra"* hay quyền admin nào vượt qua được — nếu có, **export chính là đường bypass mà `M2-4` cấm** | `Roadmap` §2 **`M2-4`** (đo bằng **sự vắng mặt** của đường code bypass) · `MVP-Scope` §3 `C7` · CF-8.8 |
| **EF-2** | **Tác giả yêu cầu CBZ / webtoon ở MVP2** | **Hệ thống** báo định dạng **chưa có ở mốc hiện tại**, chỉ chào **PDF** | Export PDF vẫn chạy được. ⛔ **Không** dựng một đường đóng gói tạm cho CBZ/webtoon — `H4` = `✅` từ **MVP3** | `MVP-Scope` §3 `H4` · `BR-008-12` |
| **EF-3** | **Project đang bị `disable-access` do takedown** (`BR-007-04`) | **Hệ thống** từ chối export ở bước 3 và ghi lại lần từ chối | Export bị chặn, **nhưng dữ liệu VẪN ĐƯỢC GIỮ** — takedown là **soft-delete + disable-access cấp project**, **KHÔNG hard delete**, vì dữ liệu còn phải giữ cho **counter-notice**. Đường hard-delete tenant là đường **tách biệt** (`BR-007-08`) | [`BR-007-04`](../BRD/BRD-007-Legal-And-Compliance.md) · [UC-11](./UC-11-Handle-Takedown-Request.md) |
| **EF-4** | **≥1 panel của page chưa có ảnh được chọn** (`approved_generation_id` rỗng) | **Hệ thống** dừng composite cho page đó và báo rõ page/panel nào thiếu | Không trả file **một phần** cho một page. Tác giả quay về [UC-06](./UC-06-Generate-Panel-And-Pick-Variant.md) để chọn variant | [BRD-007](../BRD/BRD-007-Legal-And-Compliance.md) mục 5.3 (`approved_generation_id`) · `MVP-Scope` §3 `A1` |
| **EF-5** | **Composite / đóng gói thất bại giữa đường** (lỗi hệ thống) | **Hệ thống** báo lỗi, **không trả file dở**, giữ nguyên dữ liệu nguồn để chạy lại | ⚠️ **`SLA` / `uptime` của export: `TBD`** — [BRD-008](../BRD/BRD-008-Quality-And-Operations.md) `TBD-4` ghi nguyên văn *"Không nguồn nào trong repo đặt con số này. Không tự gán"*. ⛔ UC này **không** phát minh một ngưỡng thời gian | [BRD-008](../BRD/BRD-008-Quality-And-Operations.md) `TBD-4` |

> [!CAUTION]
> **`EF-1` là lý do UC-09 không phải một luồng tầm thường.** Ba UC khác cũng chạm hai human gate, nhưng chỉ ở UC-09 cái giá của việc quên kiểm là **một artifact đã ra khỏi hệ thống**. Artifact đã export thì **không thu hồi được** — cùng một tính chất *"không rút lại được"* mà `X-a` nói về nghĩa vụ takedown.

---

## 6. Tài liệu liên quan

### 6.1 Traceability lên tầng trên

| Quan hệ | Tài liệu |
|---|---|
| **Part of (Epic)** | [Epic-Quality-And-Operations](../../022-User-Stories/Epics/Epic-Quality-And-Operations.md) |
| **Requirement cha** | [BRD-008 — Quality And Operations](../BRD/BRD-008-Quality-And-Operations.md) — hàng `H4`, `BR-008-11` (PDF @MVP2), `BR-008-12` (đủ định dạng @MVP3), `BR-008-13` (export là **điều kiện doanh thu**) |
| **Sản phẩm** | [PRD-Comic-Studio](../PRD-Comic-Studio.md) — mục *Chất lượng & vận hành* |
| **Hệ thống** | [SRS-Comic-Studio](../SRS-Comic-Studio.md) |

### 6.2 BRD phụ thuộc chéo

| BRD | Vì sao liên quan |
|---|---|
| [BRD-004 — Minimum Editor](../BRD/BRD-004-Minimum-Editor.md) | Export **tái dùng compositor của preview** — thành phần `#4` của editor tối thiểu. *"Không viết renderer từ đầu"* (CF-9.1) |
| [BRD-003 — Comic Director And Layout](../BRD/BRD-003-Comic-Director-And-Layout.md) | `C7` hai human gate (điều kiện của `EF-1`) · `page_layout` toạ độ chuẩn hoá 0–1 |
| [BRD-007 — Legal And Compliance](../BRD/BRD-007-Legal-And-Compliance.md) | `BR-007-04` disable-access cấp project (`EF-3`) · `BR-007-06` dấu máy đọc ở export path (`AF-3`) · `BR-007-09` export hồ sơ tenant khi KILL (`AF-2`) · `KC-2`/`KC-4` (bước 9) |
| [BRD-006 — Credit And Unit Economics](../BRD/BRD-006-Credit-And-Unit-Economics.md) | `F6` / `BR-006-07` — export là điều kiện để **Tầng 1 bán được**, và đó là **LỰA CHỌN `[EM]`** gated on `G0` PASS + `M2-5` + `M2-6` + quyết định Founder tại `G2` (xem [mục 1.1](#11--sắc-thái-bắt-buộc--f6-tầng-1-là-một-lựa-chọn-không-phải-kế-hoạch-đã-chốt)) |

### 6.3 Use Case liền kề

| UC | Quan hệ |
|---|---|
| [UC-08 — Arrange Page And Preview](./UC-08-Arrange-Page-And-Preview.md) | **Đầu vào trực tiếp**: preview server-side chính là compositor mà export dùng lại |
| [UC-04](./UC-04-Human-Gate-Speaker-Attribution.md) · [UC-05](./UC-05-Human-Gate-Dialogue-Condensation.md) | Hai gate mà `EF-1` cưỡng chế |
| [UC-06 — Generate Panel And Pick Variant](./UC-06-Generate-Panel-And-Pick-Variant.md) | Nguồn của `approved_generation_id` (`EF-4`) |
| [UC-11 — Handle Takedown Request](./UC-11-Handle-Takedown-Request.md) | Nguồn của trạng thái `disable-access` ở `EF-3` |

### 6.4 Tài liệu tham khảo

| Tài liệu | Phần được dùng ở đây |
|---|---|
| [MVP-Scope.md](../../010-Planning/MVP-Scope.md) | §3 hàng `H4` (bảng mốc export) · §3 `C7` (hai human gate) · §3 `A1`, `A2` · §4.1 (toạ độ chuẩn hoá 0–1) · §6 `KC-2`, `KC-4`, `KC-5` · §7.3 gate `G2` · §8.2 (nghĩa vụ khi KILL) |
| [Roadmap.md](../../010-Planning/Roadmap.md) | §2 exit criteria **`M2-4`**, **`M2-5`**, **`M2-6`**, `G1-e` · §4 việc `X-a`, `X-c` · **§5.1** (MVP3/MVP4 rơi ra ngoài horizon) · **§5.2** (⚠️ Tầng 1 là một **LỰA CHỌN `[EM]`**) |
| [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) | §7 `C4` (thiết kế theo diễn giải RỘNG cho AI disclosure) · `C9` (thứ tự milestone) |
| [Glossary.md](../../999-Resources/Glossary.md) | *typeset layer* · *`text_safe_zone`* · *dialogue condensation* · *speaker attribution* |
| [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) | **§3.2** hàng `UC-09` (actor · mục tiêu · BRD · mốc · anchor) · §1.2 hàng `H4` · §5.2 CF-8.10, CF-8.11c, CF-9.1, CF-10.9 · §5.3 `CẤM-17` (không đặt requirement cho phân khúc hoạ sĩ) · §6.2 `KT-1` |
| [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) | `RULE-001` — thư mục `docs/020-Requirements/Use-Cases/`, naming `UC-{NN}-{Title}.md`, frontmatter, **standard markdown link** (quy tắc #5) |

> ⛔ **Không link tới `docs/030-Specs/`** — tầng technical spec chưa tồn tại và nằm ngoài scope của run này.

---

_Use Case by TNMCORE-OS — role `business-analyst`._
_Author: trisjr_
</content>
</invoke>
