---
id: BRD-006
type: brd
status: draft
project: comic-studio
created: 2026-08-24
---

# BRD-006 — Kinh tế & credit (module F)

> [!IMPORTANT]
> **Quy ước nhãn nguồn số liệu** (kế thừa nguyên vẹn — **số và nhãn là một cặp không tách rời**):
> `[OFF]` nguồn official/paper gốc · `[BCN]` báo cáo ngành có tên firm · `[TC]` nguồn thứ cấp · `[EM]` ước lượng hoặc phép nhân, **không phải số đo** · `[CHỐT]` quyết định của Founder tại gate.
>
> Đây là BRD **dày số liệu nhất** trong bộ tám. ⛔ **Cấm tự tra lại hoặc tự tính lại một con số đã có** (`CẤM-15`); nếu nhân/chia hai số để tạo số thứ ba thì kết quả **phải mang nhãn `[EM]`**.

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

> Đo và cưỡng chế chi phí **trước khi nó xảy ra**: `usage_event`, credit ledger có HOLD, hard quota, mô hình 3 tầng. Không có tầng này thì **một power user xoá margin của bốn user thường**.

Hai chữ *"trước khi"* là toàn bộ nội dung của module. Mọi cơ chế ở đây đều là biến thể của cùng một nguyên tắc: **đo trước, giữ chỗ trước, cưỡng chế trước** — vì mỗi lần generate là **tiền thật đã tiêu và không hoàn lại được**.

### 1.1 Mô hình đã CHỐT: cấu hình 3 tầng kiểu Novelcrafter

Nguồn: [Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints) **C2** `[CHỐT]` (CF-2.1→CF-2.4) — **đã chốt tại gate, không mở lại trong horizon này**.

| Tầng | Nội dung | Vai trò trong mô hình |
|---|---|---|
| **Tầng 1** | **$4–8/tháng, KHÔNG có image gen** — Story Bible + Comic IR + layout + versioning + export. Margin **~90%**, **không cần API key** | ⭐ **CỬA VÀO.** Người dùng vào được sản phẩm **trước khi** đối mặt với API key |
| **Tầng 2** | **Credit pack KHÔNG hết hạn**, managed inference, cho user **< ~125 ảnh/tháng** `[TC]` | Đường chính cho **user thường** |
| **Tầng 3** | **BYOK — tuỳ chọn MỞ KHOÁ** | Dành cho **power user** vượt ngưỡng |

> [!CAUTION]
> ⛔ **BYOK là tuỳ chọn MỞ KHOÁ, KHÔNG phải điều kiện để dùng sản phẩm** (CF-2.4 `[CHỐT]`).
> Viết BYOK thành **cửa vào** là đọc ngược mô hình: đúng pattern Novelcrafter, cửa vào là **tầng $4–8 không cần API key** (CF-2.2 `[CHỐT]`), để user vào được sản phẩm trước khi gặp API key. `Glossary.md` (*BYOK*) xếp **onboarding friction của BYOK là rủi ro sản phẩm số 1** — mô hình 3 tầng là **cấu trúc né** rủi ro đó, không phải cách giải nó.

### 1.2 Vì sao KHÔNG phải subscription phẳng — và cách trích con số 23% cho đúng

> [!WARNING]
> **BA CAVEAT PHẢI ĐI KÈM CON SỐ 23%. Trích 23% mà bỏ ba dòng này là TRÍCH SAI** (`CẤM-06`) — đây là **lỗi MAJOR có tiền lệ thật trong repo**.

**Con số**: **GRR 23% / NRR 32%** cho AI-native band **`<$50/tháng`** `[OFF]` — ChartMogul *"The SaaS Retention Report: The AI churn wave"*, cỡ mẫu **~3.500 software companies** (~2.700 B2B SaaS · ~600 B2C SaaS · **~200 AI-native**).

**Ba caveat bắt buộc** (CF-4.7 `[OFF]`):

1. **Cohort AI-native chỉ có ~200 công ty**, và band `<$50` là **một tập con** của 200 đó — ChartMogul **không công bố n của riêng band này**; nó **có thể chỉ vài chục công ty**.
2. **Bộ lọc `≥$250K ARR` loại bỏ toàn bộ sản phẩm quy mô indie** `[OFF]` — tức **loại đúng nhóm mà comic-studio thuộc về** (SOM năm 1 ước **$4–14K ARR** `[EM]`). **Không có bằng chứng nào cho thấy 23% áp được cho indie scale.**
3. Đây là **dữ liệu 2025**, không phải 2026.

> [!IMPORTANT]
> **Kết luận chịu lực KHÔNG phải *"AI churn"* — mà là GIÁ.**
> Cùng dataset đó, ChartMogul kết luận: *"AI-native products that sell for >$250 per month see **70% GRR** and **85% NRR**. This is essentially the same as B2B SaaS"* `[OFF]`.
> ⇒ 23% là **tín hiệu về hướng**, dùng để **thiết kế mô hình doanh thu**; ⛔ **không** dùng để **dự phóng số** cho comic-studio.

**Và luận điểm đối trọng cũng phải mang nhãn**: *"credit pack không hết hạn né được 23% GRR"* là một **LẬP LUẬN LOGIC** (doanh thu ghi nhận trước ⇒ không chịu cùng cơ chế churn hàng tháng của subscription), **KHÔNG PHẢI SỐ ĐO** — `[EM]` CF-4.9. Không tìm được **bất kỳ** dữ liệu retention nào cho mô hình credit pack ([Risk-Register §4.1](../../010-Planning/Risk-Register.md#41-năm-khoảng-trống-không-gán-score) **G-02**). `Charter` §8 A5 gọi đây là *"giả định được biện luận nhiều nhất và có bằng chứng ít nhất"*.

> ⛔ `CẤM-05`: **không gộp** con số này với payer retention **21,1%** của RevenueCat (CF-4.8 `[TC]`). GRR đo *đồng doanh thu*, payer retention đo *đầu người* — **không cộng, không lấy trung bình, không so trực tiếp**.

---

## 2. Phạm vi module

Bảng dưới là **toàn bộ sáu hàng của nhóm `F. Kinh tế & credit`** trong [MVP-Scope §3](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope). Nhãn từng mốc copy nguyên bảng gốc.

**Ký hiệu**: ✅ có đầy đủ · 🟡 có một phần / bản tối thiểu · ⛔ hoãn sang mốc sau · ❌ **cắt hẳn, không có trong Full Scope**

| # | Hạng mục | MVP0 | MVP1 | MVP2 | MVP3 | MVP4 | Full Scope | Căn cứ |
|---|---|:--:|:--:|:--:|:--:|:--:|:--:|---|
| **F1** | `usage_event` append-only + rollup `usage_daily` (regen ratio là metric first-class) | 🟡 log tay | ✅ | ✅ | ✅ | ✅ | ✅ | CF-8.6 · `findings/architect.md` B4.3 — *"đo muộn nghĩa là định giá trong bóng tối hàng tháng"* |
| **F2** | `cost_usd` + `model_id` + `model_version` + `attempt_no` trên mọi `generation` | 🟡 CSV | ✅ | ✅ | ✅ | ✅ | ✅ | Analysis §5.7 #3 — **không backfill được** |
| **F3** | Credit ledger append-only + **HOLD trước khi enqueue** + `CHECK (available >= 0)` + hold reaper | ❌ | ⛔ | ⛔ | ✅ | ✅ | ✅ | CF-6.12 — **hold reserve 3 credit/panel** (vì N=3) |
| **F4** | Hard quota **cưỡng chế trước khi enqueue** (không đếm sau) | ❌ | ⛔ | ⛔ | ✅ | ✅ | ✅ | CF-8.11b — *trước bản trả phí đầu tiên có image gen* |
| **F5** | BYOK — **tuỳ chọn MỞ KHOÁ**, không phải điều kiện dùng sản phẩm | ❌ | ❌ | ⛔ | ⛔ | ✅ | ✅ | CF-2.4 `[CHỐT]` · CF-2.5 ngưỡng **~125 ảnh/tháng** `[TC]` |
| **F6** | Tầng 1 bán được: Story Bible + Comic IR + layout + versioning + export, **KHÔNG image gen** | ❌ | ⛔ | 🟡 khả dĩ | ✅ | ✅ | ✅ | CF-2.2 `[CHỐT]` — margin ~90%, không cần API key |

> Sáu hàng của nhóm F đều **có mốc và đều thuộc phạm vi BRD-006** — **không hàng F nào bị cắt hoặc hoãn ra khỏi module này**. Vì vậy [mục 5](#5-cái-module-này-không-làm) của tài liệu này chứa **anti-feature và lệnh cấm về mô hình kinh tế**, không chứa hàng bị cắt.

### 2.1 ⚠️ Sắc thái bắt buộc của F6 — LỰA CHỌN, không phải kế hoạch đã chốt

> [!WARNING]
> Nhãn `🟡 khả dĩ` ở MVP2 của F6 **không** có nghĩa *"đã lên kế hoạch bán Tầng 1 ở MVP2"*.
>
> [Roadmap §5.2](../../010-Planning/Roadmap.md#52--hệ-quả-tích-cực-thứ-có-thể-bán-được-trong-horizon) ghi rõ nguyên văn: đây là **một LỰA CHỌN, không phải một kế hoạch đã chốt**, và mang nhãn **`[EM]` — *"suy luận của em, không có trong bảng CF"***.
>
> **Ba điều kiện + một quyết định** phải thoả **đồng thời**:
>
> | # | Điều kiện | Nguồn |
> |---|---|---|
> | 1 | Export / preview server-side hoàn thành ở MVP2 — exit criterion **M2-5** | `Roadmap` §5.2 |
> | 2 | Checklist safe harbour (X-a) xong **trước khi mở cho người ngoài** — exit criterion **M2-6** | `Roadmap` §5.2 |
> | 3 | ⭐ **[G0](../../010-Planning/MVP-Scope.md#71-g0--gate-pháp-lý) phải PASS** — đây chính là *"dòng code thương mại đầu tiên"* | `Roadmap` §5.2 |
> | 4 | **Quyết định của Founder tại G2** | `Roadmap` §5.2 callout |
>
> **Đánh đổi phải nói thẳng**: bán Tầng 1 sớm nghĩa là **có khách thật ⇒ có nghĩa vụ safe harbour thật ⇒ có support thật**, trong khi 1 dev **vẫn đang xây MVP3**. Roadmap ghi ra điều này *"để anh **thấy được lựa chọn**, không phải để mặc định chọn nó"*.

---

## 3. Yêu cầu nghiệp vụ

| ID | Phát biểu | Căn cứ (file + mục) | Mốc MVP |
|---|---|---|---|
| **BR-006-01** | Mọi lần tiêu tài nguyên phải sinh một `usage_event` **append-only**, kèm rollup `usage_daily`, trong đó **regen ratio là metric first-class**. Lý do nghiệp vụ: *"đo muộn nghĩa là **định giá trong bóng tối hàng tháng**"*. Append-only là điều kiện để bảng dùng được làm **căn cứ đối soát** | `MVP-Scope` §3 hàng **F1** · CF-8.6 · `Roadmap` §2 **M1-7** · `Glossary.md` *`usage_event`* | **MVP1** (`🟡 log tay` ở MVP0) |
| **BR-006-02** | Mọi `generation` phải mang `cost_usd` + `model_id` + `model_version` + `attempt_no`. Hai mục đích: tính **COGS thực** và phát hiện **silent model drift**. ⚠️ **Không backfill được** | `MVP-Scope` §3 **F2** · Analysis §5.7 #3 · `MVP-Scope` [§4.4](../../010-Planning/MVP-Scope.md#44--parent_generation--không-cắt-đây-là-một-sự-tự-thu-hồi) (*`seed` là **provenance metadata**, không phải replay key*) | **MVP1** (`🟡 CSV` ở MVP0) |
| **BR-006-03** ⭐ | Credit ledger **append-only** với **HOLD trước khi enqueue**, **hold reserve 3 credit/panel**, `CHECK (available >= 0)` **ở tầng DB**, và **hold reaper** cho `expires_at`. Bốn thành phần là **một bộ không tách** | `MVP-Scope` [§6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) **KC-7** · §3 **F3** · CF-6.12 · `Roadmap` §2 **M3-1, M3-2** · `Glossary.md` *credit ledger + hold*, *hold reaper* | **MVP3** — ⚠️ **NGOÀI horizon** |
| **BR-006-04** | Hard quota phải được **cưỡng chế TRƯỚC khi enqueue**, ⛔ **không đếm sau**. Phải hoàn thành **trước bản trả phí đầu tiên có image gen** | `MVP-Scope` §3 **F4** · CF-8.11b · `Roadmap` §2 **M3-3** | **MVP3** — ⚠️ **NGOÀI horizon** |
| **BR-006-05** | BYOK phải được triển khai như **tuỳ chọn MỞ KHOÁ cho power user vượt ngưỡng ~125 ảnh/tháng** `[TC]` — ⛔ **KHÔNG phải điều kiện để dùng sản phẩm**, ⛔ **KHÔNG phải cửa vào** | `MVP-Scope` §3 **F5** · CF-2.4 `[CHỐT]` · CF-2.5 `[TC]` · `Charter` §7 **C2** · `Glossary.md` *BYOK* | **MVP4** — ⚠️ **NGOÀI horizon** |
| **BR-006-06** | Kiến trúc **billing + credit ledger + onboarding** phải được thiết kế cho **CẢ BA tầng ngay từ đầu**, ⛔ **không retrofit**: Tầng 1 `$4–8/tháng` không image gen (cửa vào) → Tầng 2 credit pack **không hết hạn** → Tầng 3 BYOK mở khoá | `Charter` §7 **C2** `[CHỐT]` (CF-2.1→2.4) · `MVP-Scope` §3 **F5**, **F6** | **MVP1** (thiết kế) → **MVP3/MVP4** (triển khai từng tầng) |
| **BR-006-07** | Tầng 1 phải **bán được độc lập, KHÔNG có image gen**: Story Bible + Comic IR + layout + versioning + export. ⚠️ Việc **có bán hay không trong horizon** là một **LỰA CHỌN `[EM]`** gated on **G0 PASS + M2-5 + M2-6 + quyết định Founder tại G2** — xem [mục 2.1](#21--sắc-thái-bắt-buộc-của-f6--lựa-chọn-không-phải-kế-hoạch-đã-chốt) | `MVP-Scope` §3 **F6** · CF-2.2 `[CHỐT]` (margin ~90%) · **`Roadmap` §5.2** `[EM]` · CF-10.9 | **MVP2** `🟡 khả dĩ` → **MVP3** `✅` |
| **BR-006-08** | `usage_daily` phải cung cấp **regen ratio p50 và p90 đo thực** trên **≥1 chapter hoàn chỉnh** — đây là **điều kiện để gate G2 chạy được** (**G2-a**). ⚠️ Không có dữ liệu ⇒ G2 **KHÔNG CHẠY ĐƯỢC** ⇒ **lùi gate**, ⛔ **không PASS mặc định** | `MVP-Scope` [§7.3](../../010-Planning/MVP-Scope.md#7-gono-go-decision) tiêu chí **G2-a** · CF-10.6 · `Roadmap` §2 **M1-7** | **MVP1** |
| **BR-006-09** | Hệ thống phải **đo được tỉ lệ user vượt ~125 ảnh/tháng** `[TC]` (**G2-d**). ⚠️ Nếu kết quả đo cho thấy **phần lớn user hoạt động vượt ngưỡng**, thì *"BYOK không còn là **tuỳ chọn mở khoá** trên thực tế"* — và đó là **một phát hiện phải ghi lại, KHÔNG phải một lỗi đo** | `MVP-Scope` §7.3 tiêu chí **G2-d** · CF-3.9 `[EM]` (**1 chapter @N=3 = 180 ảnh**, kế thừa giả định CF-3.3 **60 ảnh/chapter** ⚠️ `[EM]` — *giả định, không phải số đo*) | **MVP1** (đo) · **MVP4** (hệ quả với BYOK) |
| **BR-006-10** | Mô hình giá phải giữ nguyên **ba đường lui đã thiết kế sẵn** cho trường hợp G2 FAIL, theo thứ tự: (1) đổi granularity render sang **whole-page** — **data model KHÔNG phải đổi**; (2) whole-page mặc định + per-panel là **hành động TRẢ PHÍ**; (3) đẩy BYOK lên đường chính cho nhóm vượt ngưỡng. Requirement kỹ thuật của đường (1) là hàng **A7**, thuộc [BRD-001](./BRD-001-Image-Generation-Pipeline.md) | `MVP-Scope` §7.3 *"Nếu FAIL — đường lui đã được thiết kế sẵn"* · CF-10.7 | **MVP3** (điều kiện: sau G2) |

---

## 4. Ràng buộc & điều kiện chặn

### 4.1 Danh sách cứng — `KC-x` của [MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) mà module này chạm

| KC | Nội dung | Quan hệ với BRD-006 | Không giữ thì hỏng thế nào |
|---|---|---|---|
| **KC-7** ⭐ | Credit ledger + **HOLD trước khi enqueue** + **hold reserve 3 credit/panel** + `CHECK (available >= 0)` **ở tầng DB** + **hold reaper** cho `expires_at`. Từ **MVP3 — trước bản trả phí có image gen**. Chi phí: một bảng ledger + một cron | **KC do BRD-006 sở hữu trực tiếp** (`BR-006-03`) | Ba lỗi độc lập: (a) **check-rồi-gọi là race condition** — 10 job đồng thời đều thấy đủ số dư và đều chạy ⇒ **vượt trần**; (b) reserve phải là **3 credit/panel** vì **N=3 là mặc định cho MỌI panel** (CF-3.1 `[OFF]`), **không phải retry-on-failure** (CF-3.2) — *"reserve 1 credit rồi tính sau = **hợp lệ hoá số dư âm**"*; (c) thiếu **hold reaper**: job crash sau khi hold ⇒ hold treo **vĩnh viễn** ⇒ khách *"có credit mà không generate được"* — `Glossary.md` gọi đây là **loại lỗi khó chẩn đoán nhất** |
| **KC-4** | KC-1 + KC-2 + KC-3 phải **commit CÙNG MỘT TRANSACTION** với artifact mà chúng chứng minh | `usage_event` là **một trong ba INSERT** phải commit cùng nhau: `generation` + `change_log` + `usage_event` ⇒ `BR-006-01` phụ thuộc **cứng** vào **1 PostgreSQL** của [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) (E5) | *"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."* Và về mặt kinh tế: `usage_event` không commit cùng artifact thì **số đối soát và số thực lệch nhau một cách không phát hiện được** |

> ⚠️ **Ba hiểu nhầm hay gặp về KC-7** — [MVP-Scope §6.1](../../010-Planning/MVP-Scope.md#61-ba-hiểu-nhầm-hay-gặp-về-danh-sách-này) đã ghi một: *"hold reserve 1 credit/panel rồi trừ thêm nếu cần"* là **sai**, vì **N=3 là mặc định cho mọi panel, không phải trường hợp xấu** ⇒ reserve 1 nghĩa là *"hệ thống được thiết kế để **vượt trần trong trường hợp bình thường**"*.

### 4.2 Ràng buộc cấp dự án — `C-x` của [Charter §7](../../010-Planning/Charter-Comic-Studio.md#7-ràng-buộc-constraints)

| C | Ràng buộc | Hệ quả bắt buộc với BRD-006 |
|---|---|---|
| **C2** ⭐ | **Mô hình 3 tầng kiểu Novelcrafter đã CHỐT — không mở lại trong horizon này** `[CHỐT]` CF-2.1→2.4 | *"Kiến trúc billing, credit ledger và onboarding phải được thiết kế cho **ba** tầng ngay từ đầu, **không retrofit**"* ⇒ `BR-006-06`. Và **BYOK là tuỳ chọn mở khoá**, không phải điều kiện dùng sản phẩm ⇒ `BR-006-05` |
| **C6** | **Gross margin kỳ vọng 50–60%, KHÔNG phải 80%** `[BCN]` CF-3.10 (ICONIQ 52%, Bessemer 50–60%) | *"Mọi mô hình tài chính đặt mục tiêu margin >60% là mô hình **sai kỳ vọng ngành**, không phải mô hình tham vọng."* Đây là ngưỡng của tiêu chí **G2-b** |
| **C7** | **Chi phí sàn $12,06/chapter @N=3, Gemini batch — và đây là SÀN, không phải trần** (chưa tính VLM call để score 3 candidate) `[EM tính từ OFF]` CF-3.5 | ⛔ `CẤM-04`: **cấm dùng $12,06 như chi phí thực tế trong bất kỳ tính toán margin nào mà không nêu nó là SÀN**. Hệ quả: cho tới hết MVP0, **mọi con số margin trong kho tài liệu là cận trên của margin**, tức **cận dưới của rủi ro** |
| **C8** | **N = 3 là mặc định cho MỌI panel** (best-of-N, *"performance saturates at N=3"*), và **KHÔNG phải retry-on-failure** `[OFF]` CF-3.1/3.2 | Hold reserve **phải là 3 credit/panel** (KC-7). ⛔ `CẤM-03`: **cấm lấy chất lượng của N=3 mà tính chi phí của N=2** |
| **C1** | **Đội 1 người + AI assist. Không funding** `[CHỐT]` CF-1.2 | Mọi cơ chế ở module này phải là **cưỡng chế tự động ở tầng DB**, không phải quy trình vận hành do người canh — vì **không có người thứ hai để canh** |
| **C10** | **Horizon 6 tháng CHƯA được ai xác nhận là đủ cho 1 dev** `[CHỐT]` CF-8.1 + CF-8.13 | Theo [Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027): **credit ledger + hard quota (MVP3)**, **BYOK (MVP4)** và **mọi gói trả phí CÓ image gen** đều **rơi ra ngoài** horizon. Hệ quả kép: *"cũng có nghĩa là **không có COGS inference trong horizon** — G2 chạy trên dữ liệu MVP0 + MVP1, không trên dữ liệu khách thật"* |

### 4.3 Điều kiện chặn cứng của gate G2

| Điều kiện | Nội dung | Nguồn |
|---|---|---|
| **Không mở free tier có image gen trước khi có ledger** | *"**Không có ngoại lệ.**"* | [Roadmap §5.1](../../010-Planning/Roadmap.md#51-cái-gì-rơi-ra-khỏi-092026022027) (X-b) |
| **Ngưỡng định nghĩa TRƯỚC khi đo** | ⛔ `CẤM-16`: không sửa ngưỡng sau khi nhìn thấy kết quả — *"đó là cách một gate biến thành nghi lễ"* | `MVP-Scope` §7 nguyên tắc chung |
| **Thiếu dữ liệu ≠ PASS** | G2-a không đạt ⇒ **KHÔNG CHẠY ĐƯỢC** ⇒ lùi gate. *"Thiếu dữ liệu không phải bằng chứng tốt."* | `MVP-Scope` §7.3 |
| **COGS phải là số ĐO** | G2-b/G2-c tính margin từ **tổng `generation.cost_usd` thực**, ⛔ **không** từ ước lượng | `MVP-Scope` §7.3 |

---

## 5. Cái module này KHÔNG làm

Sáu hàng `F1–F6` đều thuộc phạm vi ở [mục 2](#2-phạm-vi-module). Mục này vì thế liệt kê **anti-feature và lệnh cấm về mô hình kinh tế** — mỗi hàng có nguồn, không hàng nào là suy đoán.

| # | BRD-006 **KHÔNG** làm | Vì sao | Nguồn | Điều kiện mở lại |
|---|---|---|---|---|
| **1** | ⛔ **Subscription phẳng "unlimited"** dưới bất kỳ hình thức nào | Mâu thuẫn trực tiếp với **R-07** và margin **−262%** `[EM]` của power user (CF-3.7). *"Cấm đưa vào PRD dưới bất kỳ dạng nào"* | CF-2.7 `[OFF]` suy từ CF-3.5 · `Charter` §5.2 · `CẤM-17` | **Không.** Không có điều kiện mở lại |
| **2** | ⛔ **Free tier kiểu *"100 ảnh/ngày"*** | Cùng lý do #1: một nghĩa vụ tài chính **không giới hạn** trên một COGS **do provider đặt giá** | CF-2.7 · `CẤM-17` | **Không** |
| **3** | ⛔ **Đặt BYOK làm cửa vào / điều kiện dùng sản phẩm** | BYOK là **tuỳ chọn MỞ KHOÁ** (CF-2.4 `[CHỐT]`). Onboarding friction của BYOK là **rủi ro sản phẩm số 1** ⇒ cửa vào phải là Tầng 1 không cần API key | CF-2.4 `[CHỐT]` · `Glossary.md` *BYOK* · [R-23](../../010-Planning/Risk-Register.md#21-bảng-chính) | **Không theo dạng này.** ⚠️ Nhưng nếu **G2-d** đo được rằng phần lớn user vượt ngưỡng, thì *"BYOK không còn là tuỳ chọn mở khoá trên thực tế"* — đó là **một phát hiện phải ghi lại** (`BR-006-09`), **không** phải một lệnh đổi cửa vào |
| **4** | ⛔ **Hold reserve 1 credit/panel rồi trừ thêm nếu cần** | **N=3 là mặc định cho mọi panel**, không phải trường hợp xấu ⇒ reserve 1 = **hợp lệ hoá số dư âm** = *"hệ thống thiết kế để vượt trần trong trường hợp bình thường"* | CF-6.12 · `MVP-Scope` §6 **KC-7**, §6.1 | **Không** |
| **5** | ⛔ **Đếm quota SAU khi gọi provider** (pattern *check-rồi-gọi*) | **Là race condition**: 10 job đồng thời đều thấy đủ số dư. Cưỡng chế phải nằm **trước enqueue** và có `CHECK` ở **tầng DB** — lớp cuối **không bypass được bằng code** | CF-8.11b · CF-6.12 · [R-14](../../010-Planning/Risk-Register.md#21-bảng-chính) | **Không** |
| **6** | ⛔ **Hạ N từ 3 xuống 1–2 để cứu margin** | *"Không thể lấy chất lượng của N=3 mà tính chi phí của N=2"* (CF-3.2 `[OFF]`). Hạ N là **đổi chất lượng lấy margin** ⇒ nếu làm, **phải chạy lại G1**, không phải chỉ G2 | `MVP-Scope` §7.3 callout · `CẤM-03` | Chỉ khi **chạy lại G1** với N mới — đây là đường **bị loại tường minh** khỏi danh sách đường lui của G2 |
| **7** | ⛔ **Dựa vào cache để cứu margin** | Hit rate ước lượng chỉ **vài % tới ~10%** `[EM]` — `architect` **tự khai là ước lượng**. *"Kế hoạch tài chính nào giả định cache tiết kiệm đáng kể là kế hoạch sai"* | CF-6.13 `[EM]` · [R-17](../../010-Planning/Risk-Register.md#21-bảng-chính) | Khi có **hit rate đo được từ traffic thật** |
| **8** | ⛔ **Dùng $12,06/chapter như chi phí thực tế** trong bất kỳ tính toán margin nào mà không nêu nó là **SÀN** | Con số **chưa tính VLM call** để score 3 candidate ⇒ mọi mô hình dựng trên nó đang **lạc quan một khoản chưa biết độ lớn** | CF-3.5 `[EM tính từ OFF]` · `Charter` §7 **C7** · `CẤM-04` | Khi MVP0 đo được **cost thực/chapter đã gồm VLM call** |
| **9** | ⛔ **Dùng TAM $14,0–18,3B làm căn cứ biện minh** hoặc làm neo cho requirement kinh tế | Nó đo **tiêu thụ nội dung**; comic-studio **không lấy tiền từ độc giả**. Neo đúng là **SOM năm 1 $4K–14K ARR** ⚠️ `[EM]` | CF-4.1 `[BCN]` · `Charter` §2.1 · `CẤM-02` | **Không** |

### 5.1 Ba hạng mục kinh tế do BRD khác sở hữu

| Hạng mục | Ai sở hữu | Ranh giới |
|---|---|---|
| **Mua billing (không tự viết)** — hàng **E4** | [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) | BRD-006 định nghĩa **mô hình giá và ledger**; BRD-005 quyết định **nguồn cung cấp billing** |
| **Whole-page render granularity** — hàng **A7** (đường lui #1 của G2) | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) | BRD-006 sở hữu **quyết định kinh tế** phải đổi granularity (`BR-006-10`); BRD-001 sở hữu **cách làm** |
| **Fairness per tenant khi CLAIM job** — hàng **A6** | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) | Là *seam kinh tế* nhưng nằm trong câu SQL của queue ⇒ thuộc pipeline |

---

## 6. Rủi ro chính

Sổ rủi ro là [Risk-Register.md](../../010-Planning/Risk-Register.md). ⛔ **Tài liệu này không tự chấm điểm rủi ro mới** — chỉ trỏ tới hàng đã có.

| Rủi ro | Vì sao liên quan tới BRD-006 |
|---|---|
| [**R-07**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Kinh tế, `mitigating` ⭐ | **Power user đốt margin −262%** `[EM]`. Và **1 chapter @N=3 = 180 ảnh** `[EM]` đã **vượt ngưỡng ~125 ảnh/tháng** `[TC]` **ngay ở chapter đầu tiên** ⇒ *"phân khúc mục tiêu chính **là** power user"*. Mitigation của R-07 **chính là** `BR-006-04`, `BR-006-05`, `BR-006-06` |
| [**R-08**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Kinh tế, `mitigating` | **$12,06/chapter là SÀN, không phải trần.** Trigger: hoá đơn MVP0 vượt ~$12, hoặc dòng chi phí VLM select xuất hiện như một khoản riêng. Là lý do `BR-006-02` phải ghi `cost_usd` **thực**, không ước lượng. `Owner` của hàng này là `business-analyst` |
| [**R-09**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Kinh tế | **GRR 23% / NRR 32%** `[OFF]` — ⚠️ **kèm ba caveat bắt buộc**, xem [mục 1.2](#12-vì-sao-không-phải-subscription-phẳng--và-cách-trích-con-số-23-cho-đúng). Residual risk ghi thẳng: *"không có dữ liệu retention nào cho mô hình credit pack; nếu lập luận sai thì **không có phương án B đã được kiểm chứng**"*. `Owner`: `business-analyst` |
| [**R-14**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Kỹ thuật | **Race condition ở credit ledger.** Ba trigger đã ghi sẵn = **checklist review** của `BR-006-03`: code path gọi provider **trước khi** ghi hold · cột `available` xuống âm **dù chỉ một lần** · job treo mà hold không được reaper thu hồi. ⚠️ Residual: **reaper sai chu kỳ** có thể thu hồi hold của job đang chạy chậm ⇒ **user mất credit oan** |
| [**R-23**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Vận hành, `mitigating` | **Onboarding BYOK có ma sát — nhưng ĐỘ LỚN KHÔNG ĐO ĐƯỢC** (khoảng trống **G-08**). Mitigation là **cấu trúc né**: tầng $4–8 **không cần API key** ⇒ đây là căn cứ vận hành của `BR-006-05` và `BR-006-07` |
| [**R-11**](../../010-Planning/Risk-Register.md#21-bảng-chính) — Thị trường | **SOM năm 1 $4K–14K ARR ≈ $300–1.200 MRR** ⚠️ `[EM]`. Neo: **Anifusion** — solo founder, **$833 MRR**, có lãi, ~2 năm kể từ launch, **$0 marketing** `[TC]` ⚠️ **nguồn mâu thuẫn: nguồn khác ghi $5.000/tháng; giá $9/mo vs €20/mo — ghi cả hai, không chọn một** (`CẤM-07`). Đây là thang kỳ vọng doanh thu mà mô hình 3 tầng phải khớp |

---

## 7. Tài liệu liên quan

### 7.1 Tầng Requirements & Backlog

| Loại | Tài liệu | Quan hệ |
|---|---|---|
| PRD | [PRD-Comic-Studio.md](../PRD-Comic-Studio.md) | BRD-006 chi tiết hoá mục *Kinh tế & credit* của PRD |
| SRS | [SRS-Comic-Studio.md](../SRS-Comic-Studio.md) | Yêu cầu hệ thống tương ứng |
| Epic | [Epic-Credit-And-Unit-Economics.md](../../022-User-Stories/Epics/Epic-Credit-And-Unit-Economics.md) | Epic 1:1 với BRD-006 |
| BRD liên quan | [BRD-001](./BRD-001-Image-Generation-Pipeline.md) (A6 fairness, A7 whole-page — đường lui G2) · [BRD-004](./BRD-004-Minimum-Editor.md) (sửa thoại không phải regenerate ⇒ không đốt tiền) · [BRD-005](./BRD-005-Multi-Tenancy-And-Platform.md) (E4 mua billing, E5 một transaction boundary) · [BRD-007](./BRD-007-Legal-And-Compliance.md) (KC-4) · [BRD-008](./BRD-008-Quality-And-Operations.md) (H4 export — điều kiện doanh thu của Tầng 1) | Phụ thuộc chéo |

### 7.2 Use Case

| UC | Yêu cầu nghiệp vụ mà nó thực hiện |
|---|---|
| [UC-10 — Manage Credit & BYOK](../Use-Cases/UC-10-Manage-Credit-And-BYOK.md) | `BR-006-03`, `BR-006-04`, `BR-006-05`, `BR-006-06` — ⚠️ UC này ở **MVP3 (credit) / MVP4 (BYOK)**, tức **NGOÀI horizon** |

> Bốn requirement `BR-006-01`, `BR-006-02`, `BR-006-08`, `BR-006-09` **không có UC riêng** — chúng là **cơ chế đo xuyên hệ thống**, không phải tương tác goal-level của một actor. Chúng được kiểm chứng bằng exit criterion **M1-7** và bằng tiêu chí **G2-a / G2-d**, không bằng một màn hình.

### 7.3 Nguồn Planning & Research

- [MVP-Scope.md](../../010-Planning/MVP-Scope.md) — **§3** nhóm F (nguồn của [mục 2](#2-phạm-vi-module)) · **§6** KC-4, KC-7 · **§6.1** ba hiểu nhầm · **§7.3** gate **G2** (số nền a–g, tiêu chí G2-a→G2-d, ba đường lui, đường bị cấm) · §8.1 **K3** (kill criteria kinh tế)
- [Charter-Comic-Studio.md](../../010-Planning/Charter-Comic-Studio.md) — **§7** ràng buộc C1, C2, C6, C7, C8, C10 · §8 giả định **A1, A2, A3, A5, A10**
- [Roadmap.md](../../010-Planning/Roadmap.md) — **§5.1** (credit ledger, hard quota, BYOK, mọi gói trả phí có image gen **rơi ra ngoài horizon**) · **§5.2** (⚠️ điều kiện của Tầng 1 — **là một LỰA CHỌN `[EM]`, không phải kế hoạch đã chốt**)
- [Risk-Register.md](../../010-Planning/Risk-Register.md) — R-07, R-08, R-09, R-11, R-14, R-17, R-23 · §4.1 **G-02** · §4.2 **G-07, G-08, G-09, G-10**
- [Glossary.md](../../999-Resources/Glossary.md) — `credit ledger + hold`, `hold reaper`, `usage_event`, `BYOK`, `GRR`, `NRR`, `payer retention`, `seam kinh tế vs seam kỹ thuật`
- [Analysis-Market-Competitor-Landscape.md](../../050-Research/Analysis-Market-Competitor-Landscape.md) — **§5.1** (nguồn gốc của 23% GRR + **ba caveat bắt buộc** + kết luận *"vấn đề là GIÁ"*), §5.2 (RevenueCat — ⛔ **không gộp**)
- [Analysis-Comic-Studio-Concept.md](../../050-Research/Analysis-Comic-Studio-Concept.md) — §5.7 #3 (`cost_usd` không backfill được), §9b.3 (xung đột margin & đường lui whole-page). ⛔ **Không sửa tài liệu này** (`CẤM-18`)

> ⛔ **Không link tới `docs/030-Specs/`**: tầng technical spec chưa tồn tại và nằm ngoài scope của run này.

---

_BRD by TNMCORE-OS — role `business-analyst`._
_Author: trisjr_
