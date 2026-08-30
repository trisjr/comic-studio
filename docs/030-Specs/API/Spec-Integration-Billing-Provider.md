---
id: SPEC-INT-BILLING-PROVIDER
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec Integration: Billing Provider (RESERVE CHỖ — ⛔ chưa phải spec thi hành)

Serves: [UC-10](../../020-Requirements/Use-Cases/UC-10-Manage-Credit-And-BYOK.md) — `[OoH]` **MVP3**
Decided in: [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 6–8 · [SDD §8.2 `S-2`, `S-3`, `S-4`](../Architecture/SDD-Comic-Studio.md)

> [!IMPORTANT]
> ⚠️⚠️ **ĐỌC TRƯỚC — năm điều làm cho file này khác ba `Spec-Integration-*` còn lại:**
>
> 1. ⛔ **File này là RESERVE, ⛔ KHÔNG phải spec thi hành.** ⛔ Không ai được implement billing dựa trên nó. Nó tồn tại để **giữ chỗ**, ⛔ không để hướng dẫn xây.
> 2. ⛔ **`ADR-019` — ADR đặc tả credit ledger và billing — CHƯA ĐƯỢC VIẾT (đã hoãn).** Nêu bằng plain text, ⛔ **cố ý không tạo link**. Khi nào ADR đó ra đời thì **nó** là nguồn, ⛔ không phải file này.
> 3. ⭐⛔ **Founder đã chốt: ⛔ KHÔNG có HOLD credit ở MVP1–MVP2** (`T-25` **đã đóng**). Chống lạm dụng chi phí trong horizon là **rate limit per tenant đếm SỐ REQUEST**, ⛔ **không đếm tiền**. ⇒ ⛔ Đừng đọc file này thành *"billing sắp chạy"*.
> 4. ⛔ **Cố ý KHÔNG có ở đây**: danh mục sự kiện webhook, ánh xạ ba tầng giá sang SKU, vòng đời HOLD, công thức quy đổi credit, quy tắc đối soát, refund/dunning, thủ tục thuế/VAT, trang giá. Toàn bộ là việc của **MVP3**. Thêm bất kỳ thứ nào là **vượt mức reserve**.
> 5. ⛔ **File này ⛔ KHÔNG chọn vendor.**

## Mục lục

- [1. Mục đích](#1-mục-đích)
- [2. Cái gì đã CHỐT](#2-cái-gì-đã-chốt)
- [3. Cái gì còn MỞ](#3-cái-gì-còn-mở)
- [4. Interface / seam](#4-interface--seam)
- [5. Retry & error taxonomy](#5-retry--error-taxonomy)
- [6. Chi phí](#6-chi-phí)
- [Tài liệu tham khảo](#tài-liệu-tham-khảo)

---

## 1. Mục đích

Giữ **chỗ cắm** cho vendor billing ở mức **vừa đủ để ⛔ không phải retrofit** — ⛔ không hơn.

⭐ **Vì sao một hạng mục `[OoH]` MVP3 lại cần một file ngay bây giờ**: `SRS-FR-32` (`D-62`) cấm retrofit **bằng chữ** — *"kiến trúc billing + ledger + onboarding phải đỡ được **ba tầng NGAY TỪ ĐẦU**"*. Và [SDD §8.2 `S-2`](../Architecture/SDD-Comic-Studio.md) nêu chi phí cụ thể: HOLD ⛔ **không phải** một lời gọi thêm đặt trước enqueue, mà là **một câu ghi bên trong chính transaction enqueue** ⇒ chèn vào sau là **viết lại ranh giới `KC-4`**.

---

## 2. Cái gì đã CHỐT

> Mọi hàng dưới đây **đã đóng ở nơi khác**. File này chỉ **neo lại** để một lô sau ⛔ không đi ngược.

| Mã | Ràng buộc | Neo |
|:--:|---|---|
| `BI-1` | **Mua, ⛔ không tự viết luồng thanh toán**; ⛔ **không bao giờ chạm dữ liệu thẻ** | `D-12` · `SRS-FR-03` · [UC-10](../../020-Requirements/Use-Cases/UC-10-Manage-Credit-And-BYOK.md) |
| `BI-2` | ⭐ Vendor sở hữu **phương thức thanh toán, hoá đơn, nghĩa vụ thuế/VAT**. ⛔ **Vendor KHÔNG sở hữu entitlement** — `public.credit_ledger` là **nguồn sự thật duy nhất** cho số dư | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 7 · `CR-3` của [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md) |
| `BI-3` | ⛔⛔ **CẤM đọc trạng thái subscription của vendor trong ĐƯỜNG NÓNG sinh ảnh (`F5`).** `F5` đã bị `KC-4` khoá vào **một** transaction ⇒ nhét một lời gọi mạng vào giữa là **hỏng cả hai ràng buộc cùng lúc** | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 7 · [SDD §8.2 `S-3`](../Architecture/SDD-Comic-Studio.md) |
| `BI-4` | **Webhook là nguồn SỰ KIỆN, ⛔ không phải nguồn SỰ THẬT**: verify chữ ký → ghi **inbox có khoá idempotency** → xử lý bất đồng bộ → ghi **MỘT** dòng ledger | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 6 |
| `BI-5` | ⭐ **Ba tầng giá = ba hình dạng entitlement TRÊN CÙNG MỘT ledger**, ⛔ không phải ba nhánh code đọc ba nguồn khác nhau | [SDD §8.2 `S-3`](../Architecture/SDD-Comic-Studio.md) |
| `BI-6` | Chặn *"tenant này ⛔ không được sinh ảnh"* (tầng 1) nằm ở **tầng service dùng chung**, cùng khuôn với hàm kiểm của `SDD-HG-01.4` — ⛔ **không phải ẩn nút ở UI** | [SDD §8.2 `S-3`](../Architecture/SDD-Comic-Studio.md) |
| `BI-7` | ⭐ **Trong horizon MVP1–MVP2**: HOLD **bất động**, hai bảng `credit_*` tồn tại **rỗng**; chống lạm dụng là **rate limit per tenant đếm số request**. ⛔ Đường rate limit ⛔ **không được** đọc `generation.cost_usd`, ⛔ **không được** đếm `public.usage_event`, ⛔ **không được** tham chiếu bảng `credit_*` nào. **Cơ chế: `RL-a`…`RL-f` của [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md)** — ⛔ file này ⛔ không đặc tả lại | `CR-5` · `RL-b`, `RL-c` |
| `BI-8` | ⛔ `SRS-NFR-15`: bề mặt này ⛔ **không gọi** dịch vụ copyright / plagiarism / similarity detection nào. Lý do: [Spec-Security-Legal-Compliance §5](../Security/Spec-Security-Legal-Compliance.md) | `SRS-NFR-15` |
| `BI-9` | `C-9`: điều khoản dữ liệu **và khả dụng cho pháp nhân** của vendor phải verify **bằng văn bản** khi mua | [Spec-Security-Threat-Model §4.2](../Security/Spec-Security-Threat-Model.md) |

---

## 3. Cái gì còn MỞ

| # | `TBD` | Nội dung | Ai đóng | Khi nào |
|:--:|---|---|---|---|
| 1 | `SRS-NFR-08` | ⭐ **Vendor billing.** ⛔ Ở lại `TBD` **có chủ đích**: ràng buộc chặn nằm **ngoài kỹ thuật** — nó phụ thuộc **quốc gia của pháp nhân bán hàng**, mà ⛔ không tài liệu nào trong repo trả lời. **Đầu vào còn thiếu**: (a) pháp nhân bán hàng đặt ở đâu · (b) ⭐ **verify khả dụng của từng PSP cho pháp nhân Việt Nam** — đây là ràng buộc **CHẶN**, ⛔ không phải chi tiết · (c) tỷ trọng khách trong nước / quốc tế. ⚠️ **Ba lớp phương án** (PSP trực tiếp · merchant-of-record · cổng nội địa) đã được cân nhắc sẵn ở [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) — ⛔ file này ⛔ **không lặp lại và ⛔ không dán phí** | **Founder** (pháp nhân) + **dev** (verify kỹ thuật) | Trước **MVP3** — ⚠️ nhưng **seam phải có từ MVP1** |
| 2 | — | ⭐ **Bảng inbox webhook ⛔ CHƯA CÓ CHỖ trong closed list.** [ADR-005 `Q1`](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) liệt kê **12** bảng `public` và `G-2` chốt đó là **closed list** (kiểm ở CI) — ⛔ **không có** bảng inbox nào trong đó, trong khi `BI-4` bắt buộc phải có và [SDD §8.2 `S-3`](../Architecture/SDD-Comic-Studio.md) ghi nó *"phải tồn tại **trước** khi có vendor billing thật"*. ⛔ **File này ⛔ không tạo và ⛔ không đặt tên bảng** — thêm bảng ⇒ **phải sửa ADR-005 trước** | **Architect** (sửa `ADR-005`, và `ADR-019` khi viết) | Trước webhook vendor **đầu tiên** — ⚠️ **có thể đến sớm hơn MVP3** nếu vendor auth cần webhook |
| 3 | `P-6` | **Nơi lưu tầng giá của một tenant.** ⚠️ `public.tenant` hiện **cố ý ⛔ không có** cột `plan`/`tier` — thêm bây giờ là thêm một cột ⛔ không ai điền được | **Architect** (lô Schema / `ADR-019`) | MVP3 |
| 4 | `CR-2` | **Cơ chế cưỡng chế `CHECK (available >= 0)` ở tầng DB.** Yêu cầu **CHỐT**, cơ chế mở: ba đường (cột số dư materialized · bảng số dư riêng · constraint trigger) giá khác nhau | **Architect** | MVP3 |
| 5 | **`T-27`** (`b-2`) | ⚠️⚠️ **BYOK — lưu / mã hoá / THU HỒI API key của KHÁCH.** ⛔ **NGOÀI phạm vi run này**: đóng đúng nghĩa cần **một ADR mới** ⇒ ghi thành **nợ kỹ thuật**. ⛔ **Cấm** ghi bất kỳ credential nào của khách vào DB hoặc log trước khi hàng này đóng (`C-12`). ⭐ **Seam vẫn phải tồn tại về HÌNH DẠNG**, ⛔ không phải cơ chế bảo vệ key — xem `S-4` ở [§4](#4-interface--seam) | **Architect + Founder** (theo PM run-state `E22`) | Trước khi **BYOK bật** (MVP4) |
| 6 | ~~`T-25`~~ | ✅ **ĐÃ ĐÓNG — ghi lại để một lô sau ⛔ không mở lại**: Founder chọn **bước HOLD là no-op** ở MVP1–MVP2, thay bằng **rate limit cho `generate` đếm số request**, ⛔ **không đếm tiền**, ⛔ **không hard quota** | — | Đã đóng |

---

## 4. Interface / seam

> ⭐⛔ **Mức reserve nghĩa là: ghi CHỖ CẮM, ⛔ không ghi cơ chế.** Mọi hàng dưới đây đã có chủ ở nơi khác; file này chỉ ghi **nó nằm ở đâu** và **⛔ vì sao không retrofit được**.

| Seam | Chừa chỗ ở đâu | ⛔ Vì sao ⛔ không retrofit được |
|:--:|---|---|
| **`S-2`** — ledger là nguồn entitlement | Hai bảng `public.credit_ledger` + `public.credit_hold` đã reserve ([`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md)); `CHECK (available >= 0)` ở tầng DB | Bỏ hẳn ⇒ MVP3 phải **migrate dữ liệu tiền** với **hai nguồn số dư đã lệch nhau** |
| **`S-2`** — vị trí bước HOLD | ⭐ **Chỗ của HOLD trong luồng `F5` (trước enqueue, trong CÙNG transaction) ⛔ không được để trống.** Ở MVP1–MVP2 bước này ⛔ **không hiện thực** (`BI-7`) | *"Check-rồi-gọi là race condition"* ⇒ HOLD là **một câu ghi bên trong transaction enqueue**; chèn sau = **viết lại ranh giới `KC-4`** |
| **`S-3`** — adapter webhook | ⭐ **Nơi DUY NHẤT SDK vendor billing được xuất hiện** ở backend (chỗ còn lại là frontend) | Nếu vendor SDK ngấm vào đường xử lý request, đổi vendor thành sửa khắp nơi |
| **`S-3`** — ba tầng trên một ledger | `BI-5` + `BI-6` | ⭐ **Tầng 2 (credit pack KHÔNG hết hạn) ⛔ không biểu diễn được** bằng một cờ *"subscription còn hạn"*: subscription là trạng thái *đang / không đang*, credit pack là **số dư tích luỹ** |
| **`S-4`** — BYOK | ⭐ **Adapter provider nhận credential THEO TENANT ở CHỮ KÝ HÀM**, ⛔ không đọc thẳng một biến môi trường toàn cục. Và `generation.cost_usd` phải **PHÂN BIỆT ĐƯỢC** chi phí trên key của ta với chi phí trên key của khách | Hardcode credential toàn cục ⇒ bật BYOK là **sửa mọi đường gọi model**, cộng thêm ⛔ **không phân loại được** toàn bộ `usage_event`/`cost_usd` lịch sử ⇒ mất **chính con số** dùng để quyết định BYOK có đáng bật không. ⚠️ Dữ liệu lịch sử ⛔ **không backfill được** |

⛔ **Ba thứ ⛔ KHÔNG phải seam của file này**: công thức quy đổi credit · ánh xạ SKU của vendor ↔ tầng giá · trang giá. ⚠️ Và ⭐ **seam BYOK là CHỖ CẮM, ⛔ không phải cơ chế bảo vệ key** — cơ chế là `T-27`, hàng #5 của [§3](#3-cái-gì-còn-mở).

---

## 5. Retry & error taxonomy

> ⚠️ **Mục này ghi HÌNH DẠNG, ⛔ không phải đặc tả.** Nó tồn tại vì một lý do duy nhất: nhận trùng một webhook billing nghĩa là **cộng credit HAI LẦN** — và đó là loại lỗi ⛔ không sửa được bằng cách *"cẩn thận hơn"*.

| Mã | Tình huống | Hình dạng hành vi |
|:--:|---|---|
| `BILL-S1` | Webhook **chữ ký sai** | **security** — từ chối, ghi sự kiện, ⛔ không xử lý, ⛔ **không retry** |
| `BILL-S2` | Webhook **nhận trùng** | **No-op** nhờ khoá idempotency ở inbox. ⚠️ Webhook trùng lặp là **chuẩn ngành**, ⛔ không phải trường hợp hiếm |
| `BILL-S3` | **Loại sự kiện lạ** | Lưu thô vào inbox, ⛔ **không hành động**, ⛔ không đoán ngữ nghĩa |
| `BILL-S4` | Vendor **sập** / webhook ⛔ **không tới** | ⛔⛔ **Không suy entitlement từ sự vắng mặt của một sự kiện**, ⛔ không *"cho dùng tạm"*. Số dư **chỉ** đổi khi có **một dòng ledger** (`BI-2`) |
| `BILL-S5` | **Xử lý một dòng inbox thất bại** | Retry **có trần**, **giữ nguyên dòng inbox**; ⛔ không xoá. Inbox là **append-only theo tinh thần**, ⛔ không phải hàng đợi tạm |

⚠️ **Quy tắc đối soát (reconciliation) giữa vendor và ledger = `TBD` MVP3** — ⛔ file này ⛔ **không định nghĩa**.

---

## 6. Chi phí

> ⛔ **Không dán giá, phí, hay tỷ lệ chiết khấu nào.** Mọi con số tra **tại thời điểm quyết định**.

| Trục | Nội dung |
|---|---|
| ⭐ **Nghĩa vụ thuế/VAT — trục chi phí THẬT, và nó là một quyết định kiến trúc trá hình** | Nếu Founder chọn lớp **PSP trực tiếp**, phần tính và nộp VAT nhiều quốc gia **rơi về phía ta** — với `SRS` §1.3 (**1 dev**) đó là chi phí vận hành **lớn hơn toàn bộ phần code billing**. Đây là lý do lớp **merchant-of-record** được [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) nêu tường minh thay vì bỏ qua |
| **Chi phí ẩn** | Một **adapter** + một **bảng inbox** chỉ để nhận webhook — ⚠️ và bảng đó ⛔ **chưa có chỗ** trong closed list (hàng #2 của [§3](#3-cái-gì-còn-mở)) |
| ⛔ **⛔ Chưa nằm trong bất kỳ ước lượng COGS nào** | Phí PSP/MoR ⛔ **không** có trong chuỗi chi phí mỗi chapter. ⚠️ Và **mọi** ước lượng COGS hiện có **còn thiếu chi phí VLM** ⇒ ⛔ **cấm** trích một con số COGS rồi **bỏ nhãn ước lượng** |
| **Rủi ro lịch** | Seam có sẵn ⛔ **không thay được** việc chọn vendor. Nếu Founder chốt pháp nhân muộn thì **MVP3 trượt** — file này chỉ đảm bảo ⭐ **cái trượt là MỘT ADAPTER, ⛔ không phải kiến trúc** |

---

## Tài liệu tham khảo

**Tầng 020 — Requirements**
- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) — `SRS-FR-03` (`D-12`) · `SRS-FR-28` (`D-60`, `KC-7`) · `SRS-FR-29` (`D-61`) · `SRS-FR-30` (`D-58`) · `SRS-FR-32` (`D-62`) · `SRS-NFR-08` · `SRS-NFR-15` · `SRS-NFR-20` · §5.2 hàng `b-2`
- [UC-10](../../020-Requirements/Use-Cases/UC-10-Manage-Credit-And-BYOK.md) · [UC-06](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) (bước HOLD)

**Tầng 022 — User Stories**
- [Story-Minimum-Abuse-Controls](../../022-User-Stories/Backlog/Story-Minimum-Abuse-Controls.md) — cơ chế rate limit trong horizon

**Tầng 030 — Architecture** *(chỉ đọc, ⛔ không sửa)*
- [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) — điều 6, 7, 8 · `TBD` vendor billing · ba lớp phương án
- [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) — `Q1`, `G-2` closed list
- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — §8.2 `S-2`, `S-3`, `S-4` (⭐ định nghĩa mức *"chừa chỗ"*)

**Tầng 030 — Schema**
- [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md) — ⭐ cùng mức reserve; `CR-1`…`CR-7`
- [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md) — `RL-a`…`RL-f` (rate limit trong horizon)

**Tầng 030 — Security** *(⛔ không lặp lại nội dung)*
- [Spec-Security-Threat-Model](../Security/Spec-Security-Threat-Model.md) — §4.2 `C-6`, `C-9`, `C-12`
- [Spec-Security-Legal-Compliance](../Security/Spec-Security-Legal-Compliance.md) — §5 (`SRS-NFR-15`), §8 (`T-25` đã đóng, `T-27`)

**Tầng 010 — Planning**
- [PM run-state](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) — `E9` (`T-25`), `E22` (`T-27`)
- [MVP-Scope](../../010-Planning/MVP-Scope.md) — `E4 +billing` (MVP3), `F3`–`F6`

**⛔ Chưa tồn tại — nêu bằng plain text, ⛔ cố ý không tạo link**: `ADR-019` (ADR đặc tả credit ledger & billing, đã hoãn) · `Endpoint-*.md` của lô API.
