---
id: EPIC-F
type: epic
status: draft
project: comic-studio
created: 2026-08-24
---

# Epic-F — Kinh tế & credit

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Epic này **chỉ trích lại** số liệu từ tầng Planning và Requirements. Không tự tra lại, không tự tính lại (`CẤM-15`).
>
> **Trục Epic của backlog này cắt theo MODULE A–H, 1:1 với 8 BRD — KHÔNG cắt theo mốc MVP.** Lý do: [MVP-Scope §1.1](../../010-Planning/MVP-Scope.md#11-ranh-giới-ba-tài-liệu) phân định *"khi nào"* thuộc [Roadmap.md](../../010-Planning/Roadmap.md); Epic theo mốc tạo **nguồn sự thật thứ hai** về thời gian.

## Mục lục

1. [Implements](#1-implements)
2. [Mục tiêu Epic](#2-mục-tiêu-epic)
3. [Story trong horizon](#3-story-trong-horizon)
4. [Story ngoài horizon — chưa có file](#4-story-ngoài-horizon--chưa-có-file)
5. [Definition of Done cấp Epic](#5-definition-of-done-cấp-epic)
6. [Tài liệu liên quan](#6-tài-liệu-liên-quan)

---

## 1. Implements

Implements: [PRD-Comic-Studio §4 — F. Kinh tế & credit](../../020-Requirements/PRD-Comic-Studio.md#f-kinh-tế--credit)

> Anchor trên trỏ tới **H3 `F. Kinh tế & credit`** trong [PRD mục 4](../../020-Requirements/PRD-Comic-Studio.md#4-yêu-cầu-chức-năng-theo-8-module) — nơi chứa `FR-F-01`…`FR-F-06`. PRD §4.0 quy ước 4 ghi rõ **cấu trúc tám H3 là contract cứng**: đổi tên hoặc đổi thứ tự H3 ⇒ link này chết.

---

## 2. Mục tiêu Epic

> **Đo và cưỡng chế chi phí TRƯỚC KHI nó xảy ra**: `usage_event`, credit ledger có HOLD, hard quota, mô hình 3 tầng. Không có tầng này thì **một power user xoá margin của bốn user thường**.

| # | Điều làm Epic này khác các Epic khác | Hệ quả lên backlog |
|---|---|---|
| 1 | Phần lớn giá trị của module nằm ở **chỗ chặn**, không ở chỗ hiển thị | Story của Epic này hầu hết được chứng minh bằng **test và constraint tầng DB**, không bằng một màn hình |
| 2 | Hai Story `MVP1` (`F1`, `F2`) là **dữ liệu KHÔNG BACKFILL ĐƯỢC** | Thiếu `cost_usd` / `model_id` / `model_version` / `attempt_no` từ đầu ⇒ COGS phải **ước lượng lại vĩnh viễn** |
| 3 | Bốn hàng còn lại (`F3`, `F4`, `F5`, `F6`) đều gắn vào **MVP3/MVP4 hoặc một quyết định của Founder** | Epic **vắt biên** horizon: **3 Story trong** (1 **có điều kiện**) / **3 Story ngoài** |
| 4 | Đây là Epic sở hữu **đầu vào bắt buộc của gate G2** | `M1-7` (p50/p90 regen ratio) là điều kiện để [G2](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) **chạy được**; ⚠️ **G2 thiếu dữ liệu ⇒ KHÔNG CHẠY ĐƯỢC, không PASS mặc định** (CF-10.6) |

### 2.1 Mô hình ba tầng — `[CHỐT]`, không mở lại trong horizon này

CF-2.1–2.4 `[CHỐT]` · [Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints) **C2**:

| Tầng | Nội dung | Ghi chú bắt buộc đi kèm |
|---|---|---|
| **Tầng 1** | **$4–8/tháng, KHÔNG có image gen**, margin **~90%**, **không cần API key** | Là thứ **duy nhất** bán được mà không phụ thuộc COGS của provider |
| **Tầng 2** | **Credit pack không hết hạn**, managed inference, cho user **dưới** ngưỡng **~125 ảnh/tháng** `[TC]` CF-2.5 | ⚠️ Nguồn CF-2.5 là **bên bán managed** nhưng khuyến nghị **ngược chiều lợi ích của họ** ⇒ chấp nhận được, **không nâng lên `[OFF]`** |
| **Tầng 3** | **BYOK là tuỳ chọn MỞ KHOÁ** | ⛔ **BYOK KHÔNG phải điều kiện để dùng sản phẩm** (CF-2.4 `[CHỐT]`). Kiến trúc billing/ledger/onboarding phải thiết kế cho **ba** tầng ngay từ đầu, **không retrofit** |

> ⚠️ **Một phát hiện phải mang theo, không được làm mượt**: 1 chapter @N=3 = **180 ảnh** `[EM]` (CF-3.9, phép nhân 60 × 3) ⇒ **vượt ngưỡng 125 ngay ở chapter đầu tiên**. Hệ quả: **BYOK có thể không còn là "tuỳ chọn mở khoá" trên thực tế** — `MVP-Scope` **G2-d** gọi đây là *"một phát hiện phải ghi lại, không phải một lỗi đo"*. ⚠️ Con số này kế thừa sai số của **CF-3.3 = 60 ảnh/chapter**, vốn là ⚠️ `[EM]` — *"giả định của run trước, KHÔNG phải số đo"*.

### 2.2 Hai khái niệm CẤM nhầm — nguồn của sai số chi phí +50%

> [!CAUTION]
> ⛔ **`best-of-N` (N=3) KHÁC `retry-on-failure`.** Best-of-N chạy trên **MỌI** panel **như mặc định**, không chỉ khi panel lỗi — *"performance saturates at N=3"* `[OFF]` CF-3.1/3.2. Nhầm hai khái niệm này là nguồn của **sai số chi phí +50%**.
>
> Hệ quả trực tiếp lên Epic này: **hold reserve phải là 3 credit/panel** (`M3-2`). *Reserve 1 credit rồi tính sau = **hợp lệ hoá số dư âm***.
>
> ⛔ `CẤM-03`: **cấm lấy chất lượng của N=3 mà tính chi phí của N=2**. Hạ N là đổi chất lượng lấy margin ⇒ **phải chạy lại G1, không phải chỉ G2**.

---

## 3. Story trong horizon

**3 Story** — trong đó **1 có điều kiện**. Horizon **09/2026 → 02/2027** `[CHỐT]` CF-8.1.

> **Cách đọc cột `I` / `S`**: chỉ chấm hai chữ của INVEST mà việc cắt lô cần — **I** (Independent) và **S** (Small). `⚠️` = sẽ vỡ · `⚠️⚠️` = vỡ ở mức nặng nhất của cả backlog.
>
> ⚠️ **File Story chưa tồn tại** — chúng được tạo ở lô sau với **đúng** những tên dưới đây.

| Story (link) | Mốc | I | S | Trạng thái |
|---|---|:-:|:-:|---|
| [Story-Usage-Event-And-Daily-Rollup](../Backlog/Story-Usage-Event-And-Daily-Rollup.md) | MVP1 | ✅ | ✅ | `[TRONG HORIZON]` · `usage_event` **append-only** + rollup `usage_daily`; **regen ratio là metric first-class**, không phải chỉ số phụ. *"Đo muộn nghĩa là định giá trong bóng tối hàng tháng"* (CF-8.6) |
| [Story-Generation-Cost-And-Model-Metadata](../Backlog/Story-Generation-Cost-And-Model-Metadata.md) | MVP1 | ✅ | ✅ | `[TRONG HORIZON]` · `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **mọi** `generation`. ⚠️ **KHÔNG BACKFILL ĐƯỢC**; `model_version` có mặt vì **silent model drift** là sự cố chỉ **phát hiện được**, không kiểm soát được |
| [Story-Tier-1-Sellable-Without-Image-Gen](../Backlog/Story-Tier-1-Sellable-Without-Image-Gen.md) ⚠️ | MVP2–MVP3 | ⚠️ | ⚠️ | ⭐ **`[TRONG HORIZON — CÓ ĐIỀU KIỆN]`** · ⚠️ **LÀ MỘT LỰA CHỌN `[EM]`, KHÔNG PHẢI KẾ HOẠCH ĐÃ CHỐT** ([Roadmap §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) · CF-10.9). Gated on **4 điều kiện ĐỒNG THỜI**: **G0 PASS** + **M2-5** (export PDF 1 chapter) + **M2-6** (checklist safe harbour) + **quyết định của Founder tại G2**. ⛔ Không được làm phẳng thành *"trong horizon"* |

> [!WARNING]
> **Vì sao sắc thái của `Story-Tier-1-Sellable-Without-Image-Gen` là load-bearing.** [Roadmap §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) ghi nguyên văn: *"Đây là một **lựa chọn**, không phải một kế hoạch đã chốt... Ghi ra đây để anh **thấy được lựa chọn**, không phải để mặc định chọn nó."*
>
> Đánh đổi đã biết: bán Tầng 1 sớm nghĩa là **có khách thật, có nghĩa vụ safe harbour thật, có support thật** — trong khi 1 dev vẫn đang xây MVP3. Neo kỳ vọng: **SOM năm 1 $4K–14K ARR ≈ $300–1.200 MRR, 30–80 paying user** ⚠️ `[EM]` CF-4.4 — thang **trăm đô/tháng**, không phải nghìn.

---

## 4. Story ngoài horizon — chưa có file

**3 Story** — `F3`/`F4` ở **MVP3**, `F5` ở **MVP4**; cả ba **NGOÀI horizon** `[EM]` CF-10.8.

| Story (link) | Mốc | I | S | Vì sao ngoài horizon + ràng buộc phải giữ nguyên | Trạng thái tài liệu |
|---|---|:-:|:-:|---|---|
| `Story-Credit-Ledger-With-Hold-Before-Enqueue` | MVP3 | ⚠️⚠️ | ⚠️⚠️ | Gói trả phí **CÓ image gen** rơi ra ngoài horizon ⇒ `X-b` chưa đến trigger. ⚠️⚠️ **`KC-7` là một BỘ BA KHÔNG TÁCH**: hold trước enqueue + `CHECK (available >= 0)` **ở tầng DB** + **hold reaper**. **Ship 2/3 tệ hơn không ship**: thiếu reaper ⇒ job crash sau khi hold ⇒ hold treo **vĩnh viễn** ⇒ khách *"có credit mà không generate được"* — `Glossary.md` gọi đây là **loại lỗi khó chẩn đoán nhất** | **chưa có file** |
| `Story-Hard-Quota-Enforced-Before-Enqueue` | MVP3 | ⚠️ | ✅ | Cùng trigger `X-b`. Quota phải cưỡng chế **TRƯỚC** khi enqueue, **không đếm sau** — *"đếm sau nghĩa là đã tiêu tiền rồi mới biết"*. Là **BLOCKER-03** của [Charter §9.3](../../010-Planning/Charter-Comic-Studio.md#9-tiêu-chí-thành-công--gono-go): chặn **bản trả phí đầu tiên** | **chưa có file** |
| `Story-BYOK-As-Unlock-Option` | MVP4 | ✅ | ⚠️ | Tầng 3 rơi ra ngoài horizon ([Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027)). ⛔ **BYOK là tuỳ chọn MỞ KHOÁ, KHÔNG phải điều kiện dùng sản phẩm** (CF-2.4 `[CHỐT]`); ngưỡng phân tuyến **~125 ảnh/tháng** `[TC]` CF-2.5. ⚠️ Đánh đổi đã biết: **friction cao với người dùng non-technical** ⇒ onboarding flow là **rủi ro sản phẩm số 1** của tầng này | **chưa có file** |

> ⚠️ **`X-b` neo vào TRIGGER, không neo vào ngày** ([Roadmap §4](../../010-Planning/Roadmap.md#4-ba-việc-xen-ngang)): *trước bản trả phí ĐẦU TIÊN CÓ image gen*. Lưu ý phạm vi ghi trong chính hàng đó: nếu trong horizon chỉ bán **Tầng 1 không có image gen**, `X-b` **chưa cần** — nhưng **abuse control cho upload thì cần ngay ở MVP1** (thuộc [Epic-H](./Epic-Quality-And-Operations.md), hàng `H5`).
>
> ⛔ **Không mở free tier có image gen trước khi có ledger. Không có ngoại lệ** ([Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027)).

---

## 5. Definition of Done cấp Epic

### 5.1 Điều kiện ra trong horizon — nguồn là `Roadmap` §2

| # | Tiêu chí | Nguồn |
|---|---|---|
| 1 | ⭐ **`usage_daily` có p50/p90 regen ratio ⇒ [G2](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) chạy được** | **M1-7** |
| 2 | `usage_event` là **append-only** — có thể dùng làm căn cứ đối soát | `FR-F-01` · CF-8.6 |
| 3 | **100%** `generation` mang đủ `cost_usd` + `model_id` + `model_version` + `attempt_no` | `FR-F-02` |
| 4 | Mô hình dữ liệu billing/ledger/onboarding **chứa được cả ba tầng** mà không cần retrofit | CF-2.1–2.4 `[CHỐT]` |
| 5 | Tầng 1: **chỉ** được coi là *bán được* khi **G0 PASS** + **M2-5** + **M2-6** đều đạt **và** Founder quyết tại **G2** | **M2-5**, **M2-6** · [Roadmap §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) · CF-10.9 |

> ⚠️ **Tiêu chí #1 là điều kiện của một GATE, không phải một tính năng.** `p50/p90 regen ratio` không có thì G2 **không chạy được** — và *"G2 thiếu dữ liệu ⇒ KHÔNG CHẠY ĐƯỢC, không PASS mặc định"* (CF-10.6). Đây là lý do `Story-Usage-Event-And-Daily-Rollup` không được dời sau MVP1.

### 5.2 Điều kiện ra ngoài horizon — ghi ra để không mất dấu

| # | Tiêu chí | Nguồn |
|---|---|---|
| 6 | Credit ledger có **hold trước enqueue**, `CHECK (available >= 0)`, **hold reaper** — đo bằng test: **10 job đồng thời trên số dư đủ cho 5 job ⇒ đúng 5 job chạy** | **M3-1** — MVP3, **NGOÀI horizon** |
| 7 | **Hold reserve = 3 credit/panel** (vì **N=3 là mặc định cho MỌI panel**) | **M3-2** · CF-6.12 · `[OFF]` CF-3.1 |
| 8 | Hard quota cưỡng chế **trước** khi enqueue, **không đếm sau** | **M3-3** |

> [!IMPORTANT]
> **Bộ ba `KC-7` chỉ có hai trạng thái: đủ ba, hoặc chưa xong.** Tiêu chí #6 **không được** tách thành ba lô nghiệm thu riêng. Lý do đã ghi ở [mục 4](#4-story-ngoài-horizon--chưa-có-file): thiếu **reaper** sinh ra lỗi *"có credit mà không generate được"* — **tệ hơn không ship**, vì nó là loại lỗi khó chẩn đoán nhất và nó xảy ra với **khách đã trả tiền**.
>
> ⚠️ **Check-rồi-gọi là race condition** (CF-6.12): 10 job đồng thời đều thấy đủ số dư và đều chạy → vượt trần. Đây là lý do `hold` phải xảy ra **trước** `enqueue`, không phải *"kiểm tra trước khi gọi API"*.

### 5.3 Ba điều KHÔNG thuộc DoD của Epic này

1. ⛔ **Không** có tiêu chí *"cập nhật MOC"* — **PM giữ MOC** ở close-step của run.
2. ⛔ **Không** có tiêu chí về `tenant_id` / RLS / billing provider — thuộc [Epic-E](./Epic-Multi-Tenancy-And-Platform.md) (`KC-5`, `FR-E-04`).
3. ⛔ **Không** có tiêu chí về export — export là **điều kiện doanh thu** của Tầng 1 nhưng thuộc [Epic-H](./Epic-Quality-And-Operations.md) (`H4` / `FR-H-04`). Epic-F **phụ thuộc** nó, không **sở hữu** nó.

---

## 6. Tài liệu liên quan

### 6.1 BRD cha & tầng Requirements

| Quan hệ | Tài liệu | Ghi chú |
|---|---|---|
| **BRD cha** | [BRD-006-Credit-And-Unit-Economics](../../020-Requirements/BRD/BRD-006-Credit-And-Unit-Economics.md) | **1:1 với Epic này** |
| PRD | [PRD-Comic-Studio — F. Kinh tế & credit](../../020-Requirements/PRD-Comic-Studio.md#f-kinh-tế--credit) | `FR-F-01`…`FR-F-06` |
| NFR chi tiết | [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) | *Cost observability* là một trục NFR của SRS |
| Epic phụ thuộc chéo | [Epic-Multi-Tenancy-And-Platform](./Epic-Multi-Tenancy-And-Platform.md) · [Epic-Quality-And-Operations](./Epic-Quality-And-Operations.md) · [Epic-Legal-And-Compliance](./Epic-Legal-And-Compliance.md) | billing provider, `tenant_id` · export (điều kiện doanh thu Tầng 1) · `KC-4` (`usage_event` commit cùng transaction) |

### 6.2 Use Case liên quan

| Use Case | Vì sao liên quan |
|---|---|
| [UC-10 — Manage Credit And BYOK](../../020-Requirements/Use-Cases/UC-10-Manage-Credit-And-BYOK.md) | UC duy nhất thuộc Epic này. ⚠️ Ở **MVP3 (credit) / MVP4 (BYOK)**, tức **NGOÀI horizon** — nó là UC của `F3`, `F4`, `F5` |
| [UC-09 — Export Chapter](../../020-Requirements/Use-Cases/UC-09-Export-Chapter.md) | **Điều kiện doanh thu** của Tầng 1 (`M2-5`): không có export ở MVP2 thì Tầng 1 không bán được. UC thuộc `BRD-008` nhưng là **tiền đề** của `Story-Tier-1-Sellable-Without-Image-Gen` |
| [UC-06 — Generate Panel And Pick Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) | Nơi **N=3 best-of-N** thật sự tiêu tài nguyên ⇒ nơi `usage_event` được phát và nơi hold **3 credit/panel** được đặt |

### 6.3 Tài liệu tham khảo

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — **§3** nhóm F (nguồn của [mục 3](#3-story-trong-horizon) và [mục 4](#4-story-ngoài-horizon--chưa-có-file)) · **§6 KC-7** · **§7** ba gate, đặc biệt [G2](../../010-Planning/MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) và **G2-d** · §1.1
- [Roadmap.md](../../010-Planning/Roadmap.md) — **§2** exit criteria **M1-7**, **M2-5**, **M2-6**, **M3-1**, **M3-2**, **M3-3** (nguồn của [mục 5](#5-definition-of-done-cấp-epic)) · **§4** việc xen ngang **X-b** · **§5.1** · **§5.2**
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — **§7** ràng buộc **C2**, C7 · **§8** giả định A5 · **§9.3 BLOCKER-03**
- [Glossary.md](../../999-Resources/Glossary.md) — `credit ledger + hold` · `hold reaper` · `BYOK` · `usage_event`
- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md) — **§2.3** · **§4.6** (bảng 6 Story của Epic này) · **§4.10** (`Story-Credit-Ledger-With-Hold-Before-Enqueue` vỡ `I` và `S`) · **§5.2** canonical facts (CF-2.x, CF-3.x, CF-6.12, CF-10.6, CF-10.9) · **§5.3** lệnh cấm `CẤM-03`, `CẤM-15`, `CẤM-17`
- [Documents-Template.md](../../../knowledge-base/99-Templates/Documents-Template.md) — **RULE-001**: thư mục, naming `Epic-{Title}.md`, frontmatter, **standard markdown link** (⛔ cấm wiki-link `[[...]]`)

> ⛔ **Không link tới `docs/030-Specs/`** — tầng technical spec chưa tồn tại và nằm ngoài scope của run này.
