---
id: SPEC-API-USAGE-AND-CREDIT
type: spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Endpoint: Usage & Credit

Bề mặt **ĐỌC** của tầng đo lường: `public.usage_event` (event thô) và `public.usage_daily` (rollup). Hai route credit nằm cùng file ở mức **`[OoH]` reserve** — giữ riêng để lô này chỉ viết phần MVP mà ⛔ không phải sửa file khác ở MVP3.

**Serves:** [UC-06 — Generate Panel And Pick Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) bước 10 (mặt đọc của `usage_event`) · [UC-10 — Manage Credit And BYOK](../../020-Requirements/Use-Cases/UC-10-Manage-Credit-And-BYOK.md) — ⚠️ **`[OoH]`**, xem [UC nào tiêu thụ](#uc-nào-tiêu-thụ)

**Nguồn ràng buộc** (⛔ file này **không** đặc tả lại, chỉ trỏ theo mã):

| Ràng buộc | Nguồn duy nhất |
|---|---|
| Billing/metric là **hàm tổng hợp trên event thô**, idempotency key, ba `usage_event` cho một panel | [ADR-018 `Q1`…`Q5`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) |
| Hình dạng bảng, `cost_state`, `rollup_state`, ba cột `vlm_*` | ⭐ [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) |
| Vị trí `public` của bảng platform | [ADR-005 `Q1`, `Q2`](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) |
| `KC-4` — một transaction boundary | [ADR-017 `Q4.1`, `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| Tenant context + RLS | [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| Cụm credit ở mức **reserve** | [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md) |

---

## ⭐ Ba điều phải đọc trước danh sách endpoint

> [!IMPORTANT]
> **(1) ⛔ KHÔNG có HOLD credit ở MVP1–MVP2.** Chống lạm dụng chi phí được thực hiện bằng **rate limit per tenant cho `generate`**, **đếm SỐ REQUEST**, ⛔ **không đếm tiền**. ⇒ ⭐ **File này ⛔ KHÔNG đặc tả bất kỳ API hold / quota cưỡng chế nào.** Cụm `credit_ledger` / `credit_hold` ở mức *"reserve chỗ"*, `[OoH]` MVP3.
> ⚠️ **`429` khi vượt ngưỡng `generate` phát ở chính endpoint `generate`** (`Endpoint-Generation.md`), ⛔ **không** ở file này. ⛔ Đường rate limit ⛔ **không được** đọc `generation.cost_usd`, ⛔ **không được** đếm dòng `public.usage_event`, ⛔ **không được** chạm bảng `credit_*` (`RL-b`, `RL-c`, `INV-T-8`).

> [!IMPORTANT]
> **(2) ⭐ `usage_event` là bảng ĐỒNG NHẤT: một dòng = MỘT image candidate.** Một lần best-of-N (`N = 3`) tạo **đúng 3** dòng ⇒ `COUNT(*)` cho một request có **trần bằng 3**. ⛔ **Không** có dòng nào không ứng với một candidate, ⛔ không cột phân loại.
> ⭐ **Chi phí VLM-select nằm ở bảng RIÊNG `generation.vlm_scoring_call`**, ⛔ **KHÔNG** trong `usage_event` — vì **đơn vị đo khác nhau**: một lời gọi VLM chấm **cả N** candidate. ⇒ Trộn hai thứ vào một bảng làm gãy chính phép đo `COUNT(*) = 3`.

> [!IMPORTANT]
> **(3) ⭐ Ba cột `vlm_*` của `usage_daily` là FIRST-CLASS và ⛔ KHÔNG đổi.** Chỉ **bảng nguồn** của chúng đổi (từ `usage_event` sang `vlm_scoring_call`); **mặt báo cáo giữ nguyên**. ⇒ Response của `E-UC-1` **bắt buộc** mang `vlm_call_count`, `vlm_cost_usd`, `vlm_cost_unknown_count`. ⛔ Bỏ một cột vì *"API gọn hơn"* là làm khoản chi phí VLM **biến mất bằng cách bị quên**.

---

## Danh sách endpoint

> **Auth**: mọi endpoint yêu cầu **session người dùng thật** trong **một transaction tường minh** có tenant context ([ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)). ID ngoài tenant ⇒ **`404`** (RLS `0 row`, fail-closed), ⛔ không `403`.

| # | Method · Path | Trạng thái | Mục đích |
|--:|---|---|---|
| `E-UC-1` | `GET /v1/usage/daily` | ✅ MVP | Đọc rollup theo ngày UTC |
| `E-UC-2` | `GET /v1/usage/events` | ✅ MVP | Liệt kê event thô — một dòng = một image candidate |
| `E-UC-3` | `GET /v1/credit/balance` | ⚠️ **`[OoH]` MVP3 — seam CHƯA MỞ** | Đọc số dư credit |
| `E-UC-4` | `POST /v1/credit/packs` | ⚠️ **`[OoH]` MVP3 — seam CHƯA MỞ** | Mua credit pack |

---

### `E-UC-1` · `GET /v1/usage/daily`

| | |
|---|---|
| **Auth** | Session + tenant context |
| **Request** | Query: `from` (DATE, bắt buộc), `to` (DATE, bắt buộc) — ⭐ **ngày UTC** |
| **Response `200`** | `{ from, to, days: [ { usage_date, rollup_state, image_candidate_count, regen_ratio_p50, regen_ratio_p90, vlm_call_count, vlm_cost_usd, vlm_cost_unknown_count, rollup_ran_at, rollup_error } ] }` |

⭐ **Bốn quy tắc bắt buộc của response — đây là nội dung chịu lực của endpoint này:**

| # | Quy tắc |
|:--:|---|
| ⭐ `R-1` | **`rollup_state` là trường BẮT BUỘC của mọi mục** — `'complete'` / `'partial'` / `'failed'` / `'missing'`. ⛔ **Không** được lược đi khi *"trạng thái bình thường"* |
| ⭐ `R-2` | ⛔ **TUYỆT ĐỐI không render ngày lỗi/thiếu thành `0`.** Ngày ⛔ không `complete` ⇒ các số trả về `null` **kèm `rollup_state` nói ra lý do**. ⚠️ Một số `0` ngầm định trông **giống hệt** một ngày ⛔ không tiêu gì — và đó là cách một khoản chi phí thật biến mất khỏi báo cáo |
| ⭐ `R-3` | ⛔ **`vlm_cost_unknown_count` ⛔ KHÔNG BAO GIỜ được gộp vào `vlm_cost_usd` như số `0`.** *"Chưa biết"* ⛔ không phải *"miễn phí"*. Client hiển thị hai con số **tách bạch** |
| `R-4` | Ngày ⛔ không có dòng nào trong khoảng `from`–`to` trả `rollup_state = 'missing'` với các số `null` — ⛔ **không** bỏ ngày đó khỏi mảng (bỏ đi làm lỗ hổng trông như liên tục) |

- ⭐ **`image_candidate_count` = số dòng `usage_event` trong ngày, ⛔ không cần mệnh đề lọc nào** — bảng đã đồng nhất.
- ⭐ **`vlm_call_count` / `vlm_cost_usd` / `vlm_cost_unknown_count` đọc từ `generation.vlm_scoring_call`**, ⛔ không từ `usage_event`. ⚠️ Một ngày `rollup_state = 'complete'` mà `vlm_call_count` là `null` là **vi phạm invariant**, ⛔ không phải một response hợp lệ.
- ⛔ **Endpoint này ⛔ không chạy rollup.** Job rollup là **subcommand của chính image**, ⛔ **không** đi qua `public.job` và ⛔ không kích hoạt bằng API.
- ⚠️ **`regen_ratio_p50` / `p90`**: định nghĩa số học (tử số / mẫu số / đơn vị quan sát) còn `TBD` ⇒ hai trường có mặt trong contract nhưng **ý nghĩa chưa cố định**. ⛔ File này ⛔ không gán công thức.

| Mã lỗi | Khi nào |
|---|---|
| `400` | Thiếu `from`/`to`; `from > to`; định dạng ⛔ không phải `DATE` |
| `422` | Khoảng ngày vượt trần cho phép (trần = `TBD`, xem cuối file) |

---

### `E-UC-2` · `GET /v1/usage/events`

| | |
|---|---|
| **Auth** | Session + tenant context |
| **Request** | Query: `from`, `to` (bắt buộc); `generation_id?`; `limit`, `cursor` (phân trang) |
| **Response `200`** | `{ events: [ { id, generation_id, idempotency_key, cost_usd, cost_state, occurred_at, usage_date } ], next_cursor }` |

- ⭐ **Một dòng = MỘT image candidate đã sinh** — ⛔ **không** phải *"kết quả có dùng được không"*. Tiền đã tiêu là tiền đã tiêu. ⇒ Hai candidate ⛔ **không** được chọn vẫn **có mặt** ở đây, ⛔ không bị lọc.
- ⭐ **`cost_usd` luôn `null` và `cost_state` luôn `'carried_by_generation'`** ở bảng này. ⚠️ `null` ⛔ **không** nghĩa là *"bằng 0"* — nghĩa được `cost_state` nói ra. **Chi phí thực của một candidate đọc ở resource `generation`** (`Endpoint-Generation.md`), ⛔ không ở đây.
- ⭐ **Phép đo kiểm chứng được**: một request best-of-N với `N = 3` ⇒ lọc theo `generation_id` cấp request cho ra **đúng 3** dòng. ⛔ Nhiều hơn 3 ⇒ đã đếm trùng (thiếu idempotency key) hoặc đã có loại event lạ trôi vào bảng.
- ⛔ **⛔ Endpoint này ⛔ KHÔNG trả chi phí VLM.** Lời gọi VLM sống ở `generation.vlm_scoring_call` với **đơn vị đo khác** (một lời gọi / N candidate). Trộn vào đây là **đếm đôi** và làm gãy phép đo trên.
- ⛔ **Read-only tuyệt đối.** ⛔ Không `POST`/`PATCH`/`DELETE`: `usage_event` là **append-only**, được cưỡng chế bằng `REVOKE UPDATE, DELETE` khỏi mọi role ứng dụng. ⚠️ Số liệu sai ⛔ **không** sửa bằng cách ghi đè — append-only là **điều kiện** để nó dùng được làm căn cứ đối soát.
- ⚠️ Dòng `usage_event` được ghi bởi **đường generation**, **cùng transaction** với artifact và `change_log` ([ADR-017 `Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)) — ⛔ **không** phải bởi endpoint nào của file này.

| Mã lỗi | Khi nào |
|---|---|
| `400` | Thiếu `from`/`to`; `cursor` ⛔ không hợp lệ |
| `404` | `generation_id` ⛔ không thấy dưới RLS |
| `422` | `limit` vượt trần |

---

### `E-UC-3` · `GET /v1/credit/balance` — ⚠️ `[OoH]` MVP3

> [!WARNING]
> ⛔ **SEAM CHƯA MỞ — file này ⛔ KHÔNG đặc tả request/response cho route này.**
> Lý do ⛔ không phải bỏ sót: khách hàng đã chốt **⛔ KHÔNG có HOLD credit ở MVP1–MVP2**; hai bảng `public.credit_ledger` / `public.credit_hold` tồn tại **RỖNG** ở mức reserve, và ⛔ **không đường code nào trong horizon được ghi/đọc chúng**.
> ⇒ Ở horizon MVP0–MVP2, route này ⛔ **không được implement**. Nếu bị gọi ⇒ **`404`** như mọi route ⛔ không tồn tại — ⛔ **không** trả một số dư giả, ⛔ **không** trả `0`.

**Ràng buộc phải mang theo khi seam mở ở MVP3** (ghi ở đây để MVP3 ⛔ không thiết kế sai, ⛔ **không** phải đặc tả):

- ⭐ ⛔ **`available` ⛔ TUYỆT ĐỐI không được gộp với credit đang HOLD.** Ba số **tách bạch**: `available` / đang HOLD / mức tiêu theo `usage_daily`.
- ⭐ **Số dư có đúng MỘT nguồn: ledger của ta.** ⛔ Vendor billing **không sở hữu** entitlement ⇒ ⛔ không đọc số dư từ trạng thái subscription của vendor.
- ⚠️ Lượng credit giữ trước cho một panel là **N credit** với `N` mặc định **3** (kế thừa best-of-N), ⛔ **không phải 1**.
- ⛔ Cơ chế cưỡng chế `CHECK (available >= 0)` còn `TBD` ⇒ ⛔ ⛔ không dựng một counter số dư ở chỗ khác *"cho nhanh"*.

**Nguồn**: [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md) (mức reserve). ⚠️ ADR đặc tả credit ledger — `ADR-019` — **chưa được viết (đã hoãn)**; nêu bằng plain text, ⛔ cố ý không tạo link. Khi nó ra đời thì **nó** là nguồn, ⛔ không phải file này.

---

### `E-UC-4` · `POST /v1/credit/packs` — ⚠️ `[OoH]` MVP3

> [!WARNING]
> ⛔ **SEAM CHƯA MỞ — cùng lý do và cùng cách xử lý như `E-UC-3`.** Route ⛔ không được implement ở horizon này; bị gọi ⇒ **`404`**.

**Ràng buộc phải mang theo khi seam mở**:

- Callback từ vendor billing cần **bảng inbox webhook idempotent** — hạng mục MVP3, ⛔ chưa đặc tả ở đâu.
- Ledger là **append-only** ⇒ mua credit là **một bút toán cộng thêm**, ⛔ không phải một lần `UPDATE` số dư.
- **Ba tầng giá** phải được thiết kế **ngay từ đầu, ⛔ không retrofit** — nhưng chỗ chừa cho nó ⛔ **không** thuộc file này.

---

## Invariant của resource

| # | Invariant | Neo |
|:--:|---|---|
| ⭐ `API-UC-1` | **`usage_event` đồng nhất: một dòng = một image candidate; best-of-N với `N=3` ⇒ đúng 3 dòng, `COUNT(*)` trần = 3** | [ADR-018 `Q5`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) |
| ⭐ `API-UC-2` | ⛔ **Chi phí VLM ⛔ KHÔNG ở `usage_event`** — nó ở `generation.vlm_scoring_call`, đơn vị **một lời gọi**, và chỉ lộ ra API qua ba cột `vlm_*` của `E-UC-1` | `E20` · [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) |
| ⭐ `API-UC-3` | ⛔ **Ngày rollup lỗi/thiếu ⛔ KHÔNG BAO GIỜ hiển thị ngầm là `0`** | `R-2`, `R-3` |
| ⭐ `API-UC-4` | ⛔ **⛔ Không API hold / quota cưỡng chế chi phí ở horizon này.** Chống lạm dụng = **rate limit đếm số REQUEST**, phát `429` ở endpoint `generate` | `RL-b`, `RL-c`, `CR-5` |
| `API-UC-5` | ⛔ **Mọi endpoint của file này là READ-ONLY** (trừ `E-UC-4` đã đóng). ⛔ Không đường ghi `usage_event`/`usage_daily` qua API — event được ghi bởi đường generation trong `KC-4` | [ADR-017 `Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| `API-UC-6` | ⛔ **Không counter tăng tại chỗ.** Mọi con số là **hàm tổng hợp trên event thô**; rollup tính lại được và **chạy lại phải cho cùng kết quả** | [ADR-018 `Q2`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) |
| `API-UC-7` | ⛔ **Không endpoint nào của file này là async** — rollup chạy bằng subcommand, ⛔ không qua `public.job`, ⛔ không polling | [SDD §7.5](../Architecture/SDD-Comic-Studio.md) · [`DB-Entity-Job-Queue.md`](../Schema/DB-Entity-Job-Queue.md) |
| `API-UC-8` | ⛔ **Không endpoint trạng thái rate limit / quota.** Bộ đếm ⛔ **không** là entity trong data model; ⛔ không nguồn nào yêu cầu phơi nó ra | `RL-1` |

---

## UC nào tiêu thụ

| UC · bước | Endpoint |
|---|---|
| [UC-06](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) bước 10 (ghi `usage_event`) | ⚠️ **Mặt GHI thuộc `Endpoint-Generation.md`**; `E-UC-2` là **mặt ĐỌC** của cùng dữ liệu |
| [UC-06](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) bước 3 (🔒 HOLD 3 credit trước enqueue) | ⛔ **⛔ KHÔNG có endpoint nào phục vụ bước này ở horizon MVP1–MVP2** — thay bằng **rate limit** ở `Endpoint-Generation.md`. ⚠️ Đây là một **quyết định sản phẩm đã ghi nhận**, ⛔ không phải một lỗ hổng của lô này |
| Gate vận hành `G2` (COGS + regen ratio p50/p90) | `E-UC-1` — ⭐ đây là **mặt báo cáo** mà phép tính COGS đọc |
| Bề mặt Founder-operator (theo dõi chi phí VLM chưa vào COGS) | `E-UC-1` (ba cột `vlm_*`) |
| [UC-10](../../020-Requirements/Use-Cases/UC-10-Manage-Credit-And-BYOK.md) bước 2 (đọc ba số tách bạch) · bước 12 | ⚠️ **`[OoH]`** — `E-UC-3`, `E-UC-4` ở mức seam. ⛔ **Lô này ⛔ KHÔNG tuyên bố phủ `UC-10`**: UC đó ⛔ **không có Story nào trong 24** và nằm **ngoài phạm vi build** |

> [!NOTE]
> ⭐ **Story đứng sau phần MVP của file này**: [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) — **trong 24**, đứng sau `UC-06`. ⇒ `E-UC-1` và `E-UC-2` là **phần trong phạm vi build**; `E-UC-3`/`E-UC-4` thì ⛔ không.
> ⚠️ **⛔ Đừng đọc file này thành *"UC-10 đã có API"*.** `KC-7` (credit ledger + hold + reaper) vẫn là hàng CHỐT **ở tầng DB Schema và Security**, ⛔ **không** ở tầng API của horizon này.

---

## `TBD` còn lại

| Khoảng trống | Ai đóng | Khi nào |
|---|---|---|
| **Định nghĩa số học của `regen_ratio`** (tử số / mẫu số / đơn vị quan sát) ⇒ hai trường `regen_ratio_*` của `E-UC-1` có mặt nhưng ⛔ chưa cố định nghĩa | **PM** + Engineer đo MVP0 | Trước phép đo `M1-7` |
| **Trần khoảng ngày + trần `limit`** của `E-UC-1`/`E-UC-2` (⇒ điều kiện phát `422`) | **Dev**, sau số đo tải đầu tiên | Trước khi mở cho người dùng ngoài |
| **Chi phí VLM per-call** và tổng khoản thiếu của COGS — ⛔ không có số trong repo | **PM + Architect** | Sau đo MVP0 |
| **Vòng lặp theo tenant của job rollup dưới RLS**, cho **cả hai** nhánh đọc (`usage_event` và `vlm_scoring_call`) | **Lô API / vận hành** | Trước khi rollup chạy lần đầu |
| Chính sách **purge / retention** cho `change_log` + `usage_event` + `vlm_scoring_call` (cả ba append-only) | **PM + luật sư SHTT** | Trước khi bảng đủ lớn để thành vấn đề vận hành |
| ⚠️ **Toàn bộ contract của `E-UC-3`, `E-UC-4`** — mở cùng ADR đặc tả credit ledger (`ADR-019`, chưa viết) | **Architect**, MVP3 | Khi `KC-7` vào scope |

---

## Tài liệu tham khảo

- [ADR-018 — Usage Event And Rollup Model](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)
- [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)
- [ADR-005 — Platform Table Schema Placement](../Architecture/ADR-005-Platform-Table-Schema-Placement.md)
- [ADR-006 — RLS Tenant Context Injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)
- [ADR-007 — VLM Provider For QA Select](../Architecture/ADR-007-VLM-Provider-For-QA-Select.md)
- [SDD — Comic Studio](../Architecture/SDD-Comic-Studio.md) §6.4, §7.5, §8.2
- [`DB-Entity-Provenance-And-Usage.md`](../Schema/DB-Entity-Provenance-And-Usage.md) · [`DB-Entity-Credit-Ledger.md`](../Schema/DB-Entity-Credit-Ledger.md) · [`DB-Entity-Tenancy.md`](../Schema/DB-Entity-Tenancy.md)
- [Story-Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) · [Story-Minimum-Abuse-Controls](../../022-User-Stories/Backlog/Story-Minimum-Abuse-Controls.md)
