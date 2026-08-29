---
id: SPEC-SEC-LEGAL-COMPLIANCE
type: security-spec
status: draft
project: comic-studio
created: 2026-08-29
---

# Spec Security — Nghĩa vụ pháp lý & bằng chứng

Threat model of: [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) · [ADR-006 — RLS Tenant Context Injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010 — Tenant Isolation With RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) · [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)

> [!IMPORTANT]
> **Câu hỏi chủ đạo của file này**: mỗi nghĩa vụ pháp lý của hệ thống được **chứng minh bằng hàng dữ liệu nào**, và chỗ nào **chưa chứng minh được**.
>
> ⛔ **File này KHÔNG làm STRIDE** và ⛔ **không đặc tả tenant isolation** — hai việc đó thuộc [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) và [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) (lô `L18`, ✅ **đã viết xong**). Mọi mục dưới đây chỉ chạm hai chủ đề đó ở đúng phần **liên quan tới bằng chứng pháp lý**.
>
> ⛔ **File này KHÔNG đặc tả lại `KC-4`.** Nguồn duy nhất là [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` — ở đây chỉ trỏ theo mã điều khoản `Q4.1`…`Q4.7`.

---

## Mục lục

- [1. Câu hỏi chưa có câu trả lời](#1-câu-hỏi-chưa-có-câu-trả-lời)
- [2. Ánh xạ nghĩa vụ: `L-1`…`L-7` ↔ `KC-1`…`KC-7`](#2-ánh-xạ-nghĩa-vụ-l-1l-7--kc-1kc-7)
- [3. Bảy nghĩa vụ `KC` — nghĩa vụ · bằng chứng · chỗ hổng](#3-bảy-nghĩa-vụ-kc--nghĩa-vụ--bằng-chứng--chỗ-hổng)
- [4. ⭐ `KC-4` soi sâu — vì sao RANH GIỚI TRANSACTION chính là bằng chứng](#4--kc-4-soi-sâu--vì-sao-ranh-giới-transaction-chính-là-bằng-chứng)
- [5. ⛔ `SRS-NFR-15` — vì sao hệ thống KHÔNG được có copyright / similarity detection](#5--srs-nfr-15--vì-sao-hệ-thống-không-được-có-copyright--similarity-detection)
- [6. Bề mặt takedown — không auth, không tenant context](#6-bề-mặt-takedown--không-auth-không-tenant-context)
- [7. Thứ tự triển khai — `KC-1` và `KC-7` KHÔNG backfill được](#7-thứ-tự-triển-khai--kc-1-và-kc-7-không-backfill-được)
- [8. Bảng `TBD` — ai đóng và khi nào](#8-bảng-tbd--ai-đóng-và-khi-nào)
- [9. `RIPPLE`](#9-ripple)
- [10. Tài liệu tham khảo](#10-tài-liệu-tham-khảo)

---

## 1. Câu hỏi chưa có câu trả lời

⭐ **Mục này đứng đầu file có chủ đích.** Toàn bộ phần còn lại được viết **bên trong** vùng bất định mà mục này khoanh ra. Đọc các mục sau như thể những câu hỏi này đã có đáp án là **cách đọc sai duy nhất bị cấm tường minh** ở đây.

### 1.1 ⭐ Bốn khoảng trống pháp lý — viết dưới dạng CÂU HỎI CHO LUẬT SƯ

> [!CAUTION]
> ⛔ **Bốn hàng dưới đây ⛔ KHÔNG phải rủi ro đã đánh giá.** Chúng là **câu hỏi chưa có câu trả lời**.
> ⛔ **Security Auditor ⛔ KHÔNG có thẩm quyền đóng bất kỳ hàng nào** — [SDD §9.1](../Architecture/SDD-Comic-Studio.md) nhóm C ghi thẳng: *"Architect, Engineer và Security Auditor **đều không có thẩm quyền** đóng"*.
> ⛔ **Cố ý KHÔNG chấm điểm CVSS, ⛔ không gán likelihood/impact, ⛔ không xếp hạng.** Chấm điểm một câu hỏi pháp lý chưa có đáp án là biến **cái chưa biết** thành **cái đã đo** — đúng thứ `CẤM-13` cấm.

| # | ⭐ Câu hỏi cho luật sư SHTT Việt Nam | Nếu đáp án là *"có"* thì cái gì trong hệ thống phải đổi | Neo | Ai đóng · khi nào |
|:--:|---|---|---|---|
| **`GAP-1`** | **Điều 37a (NĐ 134/2026) có áp cho *inference-time extraction* không?** — tức việc hệ thống rút entity / state / thoại từ văn bản tác giả upload **tại thời điểm chạy** có bị coi là hành vi thuộc phạm vi điều chỉnh của Điều 37a không? | Chạm **toàn bộ `M2`/`M3`** — Story Intelligence và Comic Director đều là inference-time extraction. Có thể phải bổ sung nghĩa vụ ở bước ingest ngoài `KC-6` | `SRS-NFR-17` Q1 · [SDD §9.1](../Architecture/SDD-Comic-Studio.md) `T-18` · findings §3.4 | **PM + luật sư SHTT** · **TRƯỚC thương mại hoá** — điều kiện chặn cấp dự án, ⛔ không phải hạng mục backlog |
| **`GAP-2`** | **Phạm vi nghĩa vụ đánh dấu nội dung AI theo khoản 4 Điều 11 (Luật 134/2025/QH15) rộng tới đâu?** — mọi nội dung có AI tham gia, hay chỉ nội dung AI-only? | Quyết định `SRS-FR-39` phải nhúng dấu ở **mọi** export hay chỉ một tập con. ⚠️ **Quy tắc tạm thời ĐÃ QUYẾT**: thiết kế theo **diễn giải RỘNG** cho tới khi luật sư chốt ⇒ ⛔ **hạ `SRS-FR-39` xuống `TBD` là MẤT một requirement** | `SRS-NFR-17` Q2 · `SRS-FR-39` · [SDD §9.1](../Architecture/SDD-Comic-Studio.md) `T-19` | **PM + luật sư SHTT** · như `GAP-1` |
| **`GAP-3`** | ⭐ **Nền tảng vừa *hosting* vừa *processing* có được coi là TRUNG GIAN theo Điều 198b Luật SHTT không?** | ⭐ Đây là chân đỡ của **cả mục [5](#5--srs-nfr-15--vì-sao-hệ-thống-không-được-có-copyright--similarity-detection)**. Nếu đáp án là *"không"* thì miễn trừ Điều 198b **không áp dụng**, và toàn bộ lập luận *"đừng tạo ra tri thức"* phải được luật sư đọc lại từ đầu. ⛔ **Không tự suy ra hệ quả** | `SRS-NFR-17` Q3 · [SDD §9.1](../Architecture/SDD-Comic-Studio.md) `T-20` · `SRS-NFR-15` phụ thuộc **trực tiếp** câu này | **PM + luật sư SHTT** · như `GAP-1` |
| **`GAP-4`** | **Watermark sẵn có của model provider (SynthID) có THOẢ nghĩa vụ đánh dấu máy đọc không?** | Nếu **không thoả**: phải tự nhúng watermark ở export path — **chi phí chưa ước lượng**, và đó là một stage mới trong `M6` | `SRS-NFR-16` · [SDD §9.1](../Architecture/SDD-Comic-Studio.md) `T-21` | **PM + luật sư SHTT**, phần kỹ thuật **dev verify** · *"phải verify, ⛔ không giả định"* |

⚠️ **Ba câu `GAP-1`…`GAP-3` là `SRS-NFR-17`** — `SRS` gọi đây là **rủi ro NHỊ PHÂN duy nhất của dự án**: trả lời sai ⛔ không làm sản phẩm *kém hơn* mà làm nó **bất hợp pháp**. `GAP-4` (`SRS-NFR-16`) **cùng lớp rủi ro nhị phân** nhưng ⛔ **không mang chữ *"duy nhất"*** — ⛔ không nới nguyên văn của nguồn.

### 1.2 Ba điều kiện chặn — ⛔ KHÔNG phải câu hỏi, và ⛔ KHÔNG chặn cùng một thứ

⚠️ Ba hàng này khác loại với `GAP-1`…`GAP-4`: chúng là **điều kiện chặn đã xác định**, không phải câu hỏi mở. Chúng ở đây vì Security Review Gate phải phân biệt được hai loại.

| Mã | Nội dung | ⭐ Chặn **chính xác** cái gì |
|:--:|---|---|
| **`BLOCKER-01`** | Ba câu hỏi luật sư SHTT (`GAP-1`…`GAP-3`) chưa có câu trả lời **bằng văn bản** | ⭐ Chặn **THƯƠNG MẠI HOÁ** — ⛔ không thu tiền, ⛔ không mở cho người ngoài upload. ⛔⛔ **KHÔNG chặn MVP0–MVP1.** ⚠️ Nguồn gọi việc đọc ngược điều này là ***"cách hiểu nhầm đắt nhất"*** |
| **`BLOCKER-02`** | Checklist safe harbour Điều 198b (`SRS-FR-38`) chưa hoàn tất | Chặn **mở cho người ngoài upload**. ⛔ Không chặn dùng nội bộ |
| **`BLOCKER-04`** | Chuỗi provenance chưa ghi từ generation đầu tiên | ⭐ Chặn **MỌI THỨ** — vì ⛔ **không backfill được**. Xem [mục 7](#7-thứ-tự-triển-khai--kc-1-và-kc-7-không-backfill-được) |

### 1.3 `CẤM-13` — quy tắc viết mà chính file này phải tuân

⛔ **CẤM viết requirement như thể phạm vi Điều 37a đã rõ.** Hiểu biết hiện tại trong repo dựa trên **bản TÓM TẮT, ⛔ không phải nguyên văn điều luật** (nguồn gốc trả `403` / paywall). Luật sư phải đọc nguyên văn.

⇒ Ba hệ quả áp lên **cách viết** của file này, và lên mọi file Security sau nó:

1. Mọi phát biểu về Điều 37a / Điều 37b / khoản 4 Điều 11 / Điều 198b trong file này đều mang ngầm định *"theo bản tóm tắt hiện có trong repo"*. ⛔ Không dùng chúng làm căn cứ để **đóng** bất cứ thứ gì.
2. ⛔ **Không tự suy ra kết luận pháp lý** từ một chuỗi lập luận kỹ thuật. Ranh giới: file này được phép nói *"bằng chứng X tồn tại/không tồn tại trong hệ thống"*; ⛔ **không** được nói *"do đó hệ thống hợp pháp/không hợp pháp"*.
3. Một `TBD` ⛔ **không phải giấy phép tự chọn**. Bịa một đáp án ở đây **nặng hơn** để trống nó, vì tầng design và tầng QA sẽ dùng nó làm chuẩn nghiệm thu.

---

## 2. Ánh xạ nghĩa vụ: `L-1`…`L-7` ↔ `KC-1`…`KC-7`

⚠️ **Hai bộ mã này KHÔNG trùng nhau, và đó là lý do phải có bảng này.** `L-1`…`L-7` (findings §3.1) phân loại theo **văn bản pháp luật**; `KC-1`…`KC-7` (`MVP-Scope §6`) là **danh sách cứng không mở ra thương lượng scope**. Có nghĩa vụ `L` không sinh ra `KC` nào, và có `KC` không nằm trong nhóm `L`.

| `L` | Nghĩa vụ (rút gọn) | Văn bản pháp luật | `KC` tương ứng | Mã requirement | Mục xử lý |
|:--:|---|---|:--:|---|---|
| **`L-1`** | Năm hạng mục provenance trên **MỌI** generation | NĐ 134/2026 **Điều 5a** | `KC-1` + `KC-2` + `KC-3` | `SRS-FR-34`, `SRS-FR-35`, `SRS-FR-36`, `SRS-NFR-14` · `BR-007-01` | [3.1](#31-kc-1--chuỗi-lineage), [3.2](#32-kc-2--change_log-ghi-mọi-hành-động-người-dùng), [3.3](#33-kc-3--field_provenance--origin) |
| **`L-2`** | Bằng chứng và artifact commit **CÙNG MỘT** transaction | dẫn xuất Điều 5a | **`KC-4`** | `SRS-NFR-13` · `BR-007-02` | [3.4](#34-kc-4--một-transaction-boundary) + ⭐ [mục 4](#4--kc-4-soi-sâu--vì-sao-ranh-giới-transaction-chính-là-bằng-chứng) |
| **`L-3`** | Kiểm opt-out signal **ngay tại ingest**, log kèm timestamp, chặn nếu có signal | NĐ 134/2026 **Điều 37b** | `KC-6` | `SRS-FR-37` · `BR-007-03` | [3.6](#36-kc-6--kiểm-opt-out-signal-tại-ingest) |
| **`L-4`** | Checklist safe harbour: (a) công cụ tiếp nhận takedown · (b) **đăng ký đầu mối với Bộ VHTTDL** · (c) **SLA 72h** bằng soft-delete + disable-access cấp project | **Điều 198b** Luật SHTT | — (⛔ không có `KC`) | `SRS-FR-38` · `BR-007-04` | [mục 6](#6-bề-mặt-takedown--không-auth-không-tenant-context) |
| **`L-5`** | Đánh dấu nội dung AI bằng **định dạng máy đọc** ở cấp page/panel + export path nhúng được watermark | Luật 134/2025 **khoản 4 Điều 11** | — | `SRS-FR-39` · `SRS-NFR-16` · `BR-007-06` | [2.1](#21-ba-nghĩa-vụ-l-không-có-kc--vẫn-phải-có-mục-xử-lý) |
| **`L-6`** | Cơ chế để user **nhận biết đang tương tác với hệ thống AI** | Luật 134/2025 **Điều 11** — minh bạch | — | `SRS-FR-40` · `BR-007-05` | [2.1](#21-ba-nghĩa-vụ-l-không-có-kc--vẫn-phải-có-mục-xử-lý) |
| **`L-7`** | Đường **xoá cứng toàn bộ dữ liệu tenant** phải TỒN TẠI và ĐÃ KIỂM THỬ — `ON DELETE CASCADE` trên **mọi** FK | dẫn xuất nghĩa vụ *"yêu cầu xoá dữ liệu SẼ đến"* | — | `SRS-NFR-05` · `BR-007-08` | [2.1](#21-ba-nghĩa-vụ-l-không-có-kc--vẫn-phải-có-mục-xử-lý) |
| — | Cô lập tenant (`tenant_id` + RLS) | ⛔ không neo vào văn bản pháp luật | `KC-5` | `SRS-NFR-01` | [3.5](#35-kc-5--cô-lập-tenant-phần-liên-quan-tới-bằng-chứng) |
| — | Credit ledger + HOLD trước enqueue | ⛔ không neo vào văn bản pháp luật | `KC-7` | `SRS-FR-28` · `SRS-FR-32` | [3.7](#37-kc-7--credit-ledger--hold-trước-enqueue) |

### 2.1 Ba nghĩa vụ `L` không có `KC` — vẫn phải có mục xử lý

| `L` | Nghĩa vụ được chứng minh bằng gì | ⚠️ Chỗ hổng |
|:--:|---|---|
| **`L-5`** | Một **field metadata AI provenance ở cấp page/panel** + một **stage bắt buộc trong export pipeline** (`M6`) nhúng dấu máy đọc. Vết kiểm chứng: mỗi `export_artifact` phải truy được về stage đã chạy | ⭐ **Phạm vi nghĩa vụ là `GAP-2`/`T-19` — chưa có đáp án.** Quy tắc tạm thời **đã quyết**: thiết kế theo **diễn giải RỘNG**. ⚠️ Việc SynthID có thoả hay không là `GAP-4`/`T-21` ⇒ **đường lui** (tự nhúng watermark) **chi phí chưa ước lượng**. ⛔ ⛔ Không hạ `SRS-FR-39` xuống `TBD` |
| **`L-6`** | Một **bề mặt UI** + có thể một trường cấu hình cấp hệ thống. ⚠️ **Nhỏ về kỹ thuật, ⛔ không được rơi** vì có deadline tuân thủ (`SRS-FR-40`) | ⚠️ Nghĩa vụ này **⛔ không để lại hàng dữ liệu nào** ⇒ Security Review Gate ⛔ **không kiểm được nó từ database**. Bằng chứng phải là **ảnh chụp UI + hàng checklist ở tầng release**, ⛔ không phải một query. Ghi ra đây để ⛔ không ai tưởng nó đã được `KC-2` phủ |
| **`L-7`** | Đường hard-delete tenant **tồn tại VÀ đã được kiểm thử**: kỷ luật `ON DELETE CASCADE` trên **mọi** FK + object storage xoá theo **cùng đường** (prefix key theo tenant làm việc này khả thi) | ⛔⛔ **TÁCH BIỆT TUYỆT ĐỐI với `L-4`** — [ADR-010 `D7`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) chốt **HAI đường xoá, ⛔ không gộp**. Dùng hard-delete để làm takedown là **phá mất chính bằng chứng** counter-notice cần. ⚠️ Story Bible là nhóm bảng nhiều nhất ⇒ **chỗ dễ sót nhất**. ⚠️ **`SRS-NFR-05` ⛔ không có SLA** — thời hạn thuộc `b-3`/`T-23` |

---

## 3. Bảy nghĩa vụ `KC` — nghĩa vụ · bằng chứng · chỗ hổng

> Khuôn của mọi mục con: **nghĩa vụ là gì** → ⭐ **bằng chứng nào trong hệ thống chứng minh được nó** → **chỗ nào còn hổng**.

### 3.1 `KC-1` — chuỗi lineage

| | |
|---|---|
| **Nghĩa vụ** | Chuỗi quan hệ giữa các generation phải tồn tại từ **migration số 1**: `parent_generation_id` (**nullable FK**) + `relation_kind ENUM('retry','variation','refine','continuity_fix')`. Nó là phần *"lưu intermediate drafts"* của nghĩa vụ Điều 5a — hình dạng chốt ở [ADR-017 `Q1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) (`D-47`) |
| ⭐ **Bằng chứng** | Các **hàng `generation`** mang `parent_generation_id` khác `NULL` cùng `relation_kind` — đọc được thành câu *"artifact này là bản `refine` của artifact kia"*. Cưỡng chế nền: **`GR-4`** ([ADR-017 `Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)) — FK self-reference, nullable ⇒ chuỗi ⛔ không trỏ vào hư vô, `NULL` vẫn hợp lệ |
| ⚠️ **Chỗ hổng** | (a) ⭐ **Lineage một mình ⛔ KHÔNG chứng minh được *"decisive contribution"***. Nó chứng minh *"có nhiều bản"*, ⛔ không chứng minh *"con người đã chọn"* — cái đó là `KC-2`. ⇒ ⛔ Đừng viết ở bất kỳ đâu rằng `KC-1` đủ. (b) ⚠️ **Bẫy cắt lẫn**: `SRS-NFR-23` cắt **UI cây generation** (`D-56`); ⛔ **cắt UI, KHÔNG cắt cột dữ liệu**. Gộp hai quyết định này là **MẤT BẢO HỘ BẢN QUYỀN** — nguồn xếp nó vào *ba hiểu nhầm hay gặp*. (c) ⛔ **Không backfill được** — xem [mục 7](#7-thứ-tự-triển-khai--kc-1-và-kc-7-không-backfill-được) |

### 3.2 `KC-2` — `change_log` ghi MỌI hành động người dùng

| | |
|---|---|
| **Nghĩa vụ** | `public.change_log` **append-only** ghi **MỌI** hành động người dùng — kể cả *"chọn generation X thay vì Y"*, sửa thoại, đổi camera, kéo bubble, **export** (`D-48`, [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)). ⭐ ***"Prompt một mình không chứng minh được decisive contribution"*** |
| ⭐ **Bằng chứng** | Chuỗi **hàng `change_log`** dựng lại được **trình tự lựa chọn của con người** dẫn tới artifact. Cưỡng chế nền: **`GR-3`** — ⛔ **REVOKE `UPDATE`, `DELETE`** khỏi **mọi** DB role ứng dụng ⇒ một dòng đã ghi ⛔ không sửa, ⛔ không xoá được từ đường ứng dụng. Tính duy nhất của bảng (⛔ không rải theo module — [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) Alternatives `(c)`) chính là **điều kiện kiểm chứng**: có **một** chỗ duy nhất để hỏi *"bằng chứng của artifact này có đủ không"* |
| ⚠️ **Chỗ hổng** | (a) ⭐ **Chữ *"MỌI"* là một khẳng định về ĐỘ ĐẦY ĐỦ, và ⛔ không ràng buộc PostgreSQL nào chứng minh được nó.** DB chỉ cưỡng chế được *"dòng đã ghi thì bất biến"*, ⛔ không cưỡng chế được *"hành động đã xảy ra thì có dòng"*. Chỗ này chỉ có **`L2` middleware + `L3` test CI** đỡ ([ADR-017 `Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)) ⇒ Security Review Gate phải đòi **test *"endpoint bỏ qua middleware ⇒ FAIL"***, ⛔ không chấp nhận lời hứa. (b) ⚠️ ⛔ **Repo chưa có danh mục đóng của *"hành động người dùng"*** — không có nguồn nào liệt kê đủ tập đó ⇒ ⛔ không có cách đo *"đã phủ hết"*. (c) ⚠️ **Retention**: append-only **tăng vô hạn**; một policy purge sai chỗ sẽ **xoá chính bằng chứng** ⇒ `b-3`/`T-23`, chờ **PM + luật sư** |

### 3.3 `KC-3` — `field_provenance` + `origin`

| | |
|---|---|
| **Nghĩa vụ** | Provenance ở **mức FIELD** (⛔ không phải mức row) + `generation.origin ENUM('ai','ai_edited','human')` (`D-49`, [ADR-017 `Q3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)). Đây là thứ **xác định RANH GIỚI phần được bảo hộ** — thiếu nó thì ⛔ không nói được phần nào do người, phần nào do AI |
| ⭐ **Bằng chứng** | Hàng **`public.field_provenance`** cho **từng field** bị ghi/sửa, cộng giá trị `origin` trên chính artifact. Cưỡng chế nền: **`GR-1`** — `generation.origin` **`NOT NULL`**, `INSERT` thiếu ⇒ **FAIL ở tầng DB**, ⛔ không phải cảnh báo ở tầng ứng dụng (`D-51`, `SRS-NFR-14`). ⭐ Lý do đặt ở tầng DB đã có sẵn trong nguồn: đội **1 người**, `bus factor = 1`, ⛔ **không có code review** ⇒ guardrail ở code chỉ mạnh bằng người review nó |
| ⚠️ **Chỗ hổng** | (a) ⚠️ **`GR-1` cưỡng chế *sự tồn tại* của `origin`, ⛔ không cưỡng chế *tính đúng* của nó.** ⛔ Không ràng buộc nào bắt được việc ghi `origin='human'` cho một field do LLM sinh. Đây là **chỗ hổng thật**, ⛔ không vá được ở tầng DB — chỉ vá được bằng `L2` (một đường ghi duy nhất) + `L3`. (b) ⚠️ [ADR-017 `Q3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) đã **cảnh báo race** ở mức field ⇒ ⛔ không giả định đã giải. (c) ⚠️ Cùng vấn đề *"độ đầy đủ"* với `KC-2`: ⛔ không có cách đo *"mọi field bị sửa đều có dòng"* ngoài test |

### 3.4 `KC-4` — MỘT transaction boundary

| | |
|---|---|
| **Nghĩa vụ** | `KC-1` + `KC-2` + `KC-3` phải commit **CÙNG MỘT TRANSACTION** với artifact mà chúng chứng minh (`D-50`, `SRS-NFR-13`). Phát biểu chuẩn tắc: [ADR-017 `Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — ⛔ file này **không đặc tả lại** |
| ⭐ **Bằng chứng** | ⭐ **Bằng chứng KHÔNG phải một hàng dữ liệu — nó là một TÍNH CHẤT của tập hàng**: với mọi artifact, tập bằng chứng của nó hoặc **đủ**, hoặc **không tồn tại**; ⛔ không có trạng thái trung gian. Phép đo là **năm thuộc tính `P-1`…`P-5`** ở [ADR-017 `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md), và nghiệm thu là **một TEST, ⛔ không phải một màn hình** (exit criterion `M1-5`) |
| ⚠️ **Chỗ hổng** | Xem đầy đủ ở ⭐ [mục 4](#4--kc-4-soi-sâu--vì-sao-ranh-giới-transaction-chính-là-bằng-chứng) |

### 3.5 `KC-5` — cô lập tenant (phần liên quan tới bằng chứng)

> ⚠️ **Mục này CỐ Ý mỏng.** Chiều sâu thuộc [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) (lô `L18`, ✅ đã viết xong). Ở đây chỉ giữ phần **liên quan tới nghĩa vụ pháp lý**.

| | |
|---|---|
| **Nghĩa vụ** | `tenant_id NOT NULL` trên **MỌI** bảng nghiệp vụ · cột **ĐẦU TIÊN** của mọi composite index · **RLS** làm lớp phòng thủ thứ hai (`SRS-NFR-01`, [ADR-010 `D1`–`D4`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)). ⭐ **Liên đới pháp lý**: `change_log` và `field_provenance` là ***"hồ sơ chứng minh quyền tác giả CỦA KHÁCH"*** — rò rỉ chéo tenant ⛔ không chỉ là lộ dữ liệu, nó **làm ô nhiễm hồ sơ bằng chứng của một bên thứ ba** |
| ⭐ **Bằng chứng** | ⭐ **Một test nhị phân toàn cục**: seed 2 tenant A/B, **mọi** query dưới session của A trả **0 row** thuộc B — `M1-1`, [ADR-010 `D8`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md). ⛔ **KHÔNG** phải *"đã thêm `tenant_id` cho N/M bảng"*. Cộng **`GR-5`**: RLS + `tenant_id` trên `change_log`, `field_provenance`, `usage_event` |
| ⚠️ **Chỗ hổng** | (a) ⚠️ **RLS ⛔ không bảo vệ join thực hiện phía application** ([ADR-010 `D10`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)) — đây là **giới hạn đã biết được ghi tường minh**, ⛔ không phải khiếm khuyết cần vá ở đây. (b) ⚠️ **Bề mặt takedown ⛔ KHÔNG có tenant context** ⇒ ⛔ không áp được RLS theo tenant — xem [mục 6](#6-bề-mặt-takedown--không-auth-không-tenant-context). (c) ✅ ~~*Policy RLS cụ thể cho `public.takedown_request` còn mở*~~ — ⭐ **`P-3` ĐÃ ĐÓNG**: [DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md) đóng phần ba bảng định danh, [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md) đóng phần `takedown_request`. *(Lô Schema đóng `P-3` **trước** khi file này được viết ⇒ đây là **staleness của file này**, ⛔ không phải một hàng còn mở.)* (d) ⭐ ⚠️ **Chỗ hổng THẬT còn lại của trục này**: bề mặt **OPERATOR** `TD-2`/`TD-3` đọc/ghi **xuyên tenant** trên chính bảng đó, mà **DB role ⛔ chưa pin** và **uỷ quyền tầng ứng dụng ⛔ chưa có cơ chế** ⇒ `BP-16` của [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md); phương án chốt ở [Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md) |

### 3.6 `KC-6` — kiểm opt-out signal tại ingest

| | |
|---|---|
| **Nghĩa vụ** | Đọc tín hiệu bảo lưu quyền theo **Điều 37b** ngay tại bước **ingest**, qua **bốn kênh** (metadata · biện pháp bảo vệ công nghệ · thông tin quản lý quyền dạng máy đọc · thông báo công khai từ tổ chức quản lý tập thể); **log kết quả kèm timestamp**; **CHẶN** nếu có signal (`SRS-FR-37`, `BR-007-03`). ⭐ **Ingest là choke point DUY NHẤT** — nơi file của user **lần đầu** vào hệ thống |
| ⭐ **Bằng chứng** | ⭐ Hàng **`story.ingest_check`** có **timestamp**, ghi **KỂ CẢ KHI KHÔNG CÓ SIGNAL** ([SDD §6.4](../Architecture/SDD-Comic-Studio.md) dòng *Audit pháp lý*). ⚠️ **Chính bản ghi ÂM TÍNH mới là bằng chứng**: nó chứng minh *"đã kiểm tại thời điểm T và không thấy"*. Nếu chỉ ghi khi có signal thì ⛔ không phân biệt được *"đã kiểm, sạch"* với *"chưa từng kiểm"*. Phép đo: `M1-4` — **100%** file đi qua bước kiểm, ⛔ **không ngoại lệ theo kênh nạp** (kể cả dán text), và ⛔ **không tồn tại đường cấu hình bỏ qua** |
| ⚠️ **Chỗ hổng** | (a) ⚠️ **Kênh thứ tư** (*thông báo công khai từ tổ chức quản lý tập thể*) ⛔ **không phải tín hiệu gắn trên file** — ⛔ **không nguồn nào trong repo pin việc hệ thống quan sát kênh này bằng cách nào**, cũng ⛔ không nói tần suất. Đây là chỗ hổng thật của `L-3`, ⛔ ⛔ **và ⛔ KHÔNG được vá bằng cách quét nội dung** (xem [mục 5](#5--srs-nfr-15--vì-sao-hệ-thống-không-được-có-copyright--similarity-detection)). (b) ⚠️ **Phạm vi Điều 37a/37b dựa trên bản TÓM TẮT** (`CẤM-13`) ⇒ ⛔ không khẳng định bốn kênh là đủ. (c) ⚠️ Liên đới `GAP-1`/`T-18`: nếu Điều 37a áp cho inference-time extraction thì nghĩa vụ tại ingest có thể **rộng hơn** `KC-6` hiện tại |

### 3.7 `KC-7` — credit ledger + HOLD trước enqueue

| | |
|---|---|
| **Nghĩa vụ** | **Credit ledger append-only** + **HOLD trước khi enqueue** (*check-rồi-gọi là race condition*) + **`CHECK (available >= 0)` ở tầng DB** (chốt cuối, ⛔ không bypass được bằng code) + **hold reaper** cho `expires_at`. **Hold reserve = 3 credit/panel** (= `N` của best-of-N), **⛔ không phải 1** (`SRS-FR-28`) |
| ⭐ **Bằng chứng** | Chuỗi **hàng ledger append-only** — số dư là **hàm tổng hợp trên event thô**, ⛔ không phải counter tăng tại chỗ (cùng nguyên lý với [ADR-018 `Q1`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)). Đây là **bằng chứng về tiền**: dựng lại được *"tại thời điểm T tenant có bao nhiêu, đã giữ bao nhiêu, đã tiêu bao nhiêu"*. `CHECK (available >= 0)` là ràng buộc **duy nhất** không bypass được từ tầng ứng dụng |
| ⚠️ **Chỗ hổng** | (a) ⚠️ **Cụm này là `[OoH]` MVP3**; `ADR-019` — nơi lẽ ra đặc tả nó — ⛔ **chưa tồn tại** ⇒ ⛔ không trỏ tới. Phần đã ghi nằm ở [DB-Entity-Credit-Ledger](../Schema/DB-Entity-Credit-Ledger.md). (b) ⭐ **`SRS-FR-32` cấm retrofit BẰNG CHỮ**, và [SDD §8.2 `S-2`](../Architecture/SDD-Comic-Studio.md) nêu chi phí cụ thể: HOLD ⛔ **không phải một lời gọi thêm đặt trước enqueue** mà là **một câu ghi BÊN TRONG chính transaction enqueue** ⇒ chèn nó vào sau là **viết lại ranh giới `KC-4`**. (c) ✅ **`T-25` ĐÃ ĐÓNG** ([SDD §9.1](../Architecture/SDD-Comic-Studio.md) để mở ba lựa chọn: no-op · hard quota tạm · ⛔ không mở generation) — **Founder chọn: bước HOLD là *no-op*, thay bằng rate limit cho `generate` đếm số request** ([`E9`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)). (d) ⛔ **Rate limit của `SRS-NFR-20` ⛔ KHÔNG phải `KC-7`** — biến rate limit thành hard quota cưỡng chế chi phí là **vượt ranh giới** |

---

## 4. ⭐ `KC-4` soi sâu — vì sao RANH GIỚI TRANSACTION chính là bằng chứng

> ⛔ **Nguồn duy nhất của `KC-4` là [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4`.** Mục này ⛔ **không đặc tả lại** — nó chỉ trả lời câu hỏi mà một Security Spec phải trả lời: *vì sao đây là hạng mục bảo mật, và cái gì hỏng khi nó bị nới*.

### 4.1 Chuỗi lập luận — bốn mệnh đề, ⛔ không rút gọn được

1. Nghĩa vụ pháp lý (NĐ 134/2026 Điều 5a, `[OFF]`) đòi **con người có đóng góp trí tuệ quyết định**; tác phẩm do AI tạo hoàn toàn **không được bảo hộ**.
2. **Prompt một mình ⛔ KHÔNG chứng minh được điều đó** (`SRS-FR-35`). Cái chứng minh được là **chuỗi lựa chọn của con người** — chọn X thay vì Y, sửa thoại, đổi camera, kéo bubble, export.
3. ⇒ Bằng chứng nằm ở **`KC-1` + `KC-2` + `KC-3` — cả ba, ⛔ không phải một**.
4. ⇒ ⭐ **Nếu ba thứ đó có thể thiếu NGẪU NHIÊN so với artifact chúng chứng minh, thì chúng KHÔNG PHẢI bằng chứng.** Nguyên văn `SRS-NFR-13`: ***"Bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng."***

⭐ **Đó là toàn bộ lý do ranh giới transaction là một hạng mục pháp lý, ⛔ không phải một tối ưu kỹ thuật.** Nhất quán dữ liệu ở đây là **hệ quả phụ**, ⛔ không phải mục đích.

⚠️ **Phát biểu lại theo ngôn ngữ security**: ranh giới transaction là **cơ chế toàn vẹn (integrity control) của hồ sơ bằng chứng**. Nới nó ra ⛔ không tạo ra *"log thiếu vài dòng"* — nó tạo ra **một artifact có thể bán được mà chủ nhân không chứng minh được quyền tác giả**.

### 4.2 Phạm vi chính xác — trỏ theo mã, ⛔ không copy

| Câu hỏi | Trả lời ở đâu | Ghi chú cho người đọc Security |
|---|---|---|
| Phát biểu chuẩn tắc của `KC-4` | [ADR-017 `Q4.1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | *Tất cả cùng commit, hoặc không dòng nào tồn tại* — ⛔ không trạng thái trung gian nào hợp lệ |
| Chính xác **những bảng nào** vào transaction | [ADR-017 `Q4.2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | ⚠️ Cột *"bắt buộc?"* ở đó ⛔ **KHÔNG phải cửa thoát** — nó nói *"khi nghiệp vụ sinh ra dòng đó thì dòng đó ở cùng transaction"*, ⛔ không nói *"được phép hoãn"* |
| *"Cùng transaction"* nghĩa là gì | [ADR-017 `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `P-1`…`P-5` | ⭐ Đây là **checklist nghiệm thu của Security Review Gate**. Mỗi thuộc tính có một phép đo bằng **test**, ⛔ không bằng màn hình |
| Span nhiều schema có phải vấn đề không | [ADR-017 `Q4.4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | **Không** — transaction PostgreSQL có phạm vi **database**, ⛔ không phải schema |
| ⚠️ `KC-4` ⛔ **không** phải *"một transaction cho cả vòng đời job"* | [ADR-017 `Q4.5`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | ⛔ Đọc quá tay theo hướng này sẽ đẻ ra yêu cầu **giữ transaction mở trong lúc chờ mạng** — bất khả thi và **tự tạo lỗ DoS** |
| Cái gì DB cưỡng chế được, cái gì **không** | [ADR-017 `Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — `GR-1`…`GR-5`, `L1`/`L2`/`L3` | ⭐ Xem [4.4](#44-câu-phải-viết-đúng--và-câu--tuyệt-đối-không-được-viết) |
| Hợp đồng trích dẫn cho **chính file này** | [ADR-017 `Q4.7`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) hàng `Spec-Security-*` | Trỏ `Q4.6` `GR-3` + [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md); ⛔ **không tự đặt quyền `UPDATE`/`DELETE`** cho role ứng dụng trên hai bảng append-only |

### 4.3 ⛔ Cái gì HỎNG nếu ranh giới bị nới — bốn kịch bản, cả bốn đã bị LOẠI

⚠️ **Mối đe doạ lớn nhất ở đây ⛔ không phải attacker bên ngoài.** Nó là **một refactor có thiện chí** — *"ghi `change_log` bất đồng bộ cho nhanh"*. Vì vậy bốn kịch bản dưới đây phải nằm trong Security Spec, ⛔ không chỉ trong ADR.

| # | Đề xuất nghe hợp lý | ⛔ Cái hỏng — nói thẳng | Đã bị loại ở |
|:--:|---|---|---|
| **`SC-1`** | Ghi provenance **bất đồng bộ** sau khi commit artifact (outbox / event bus / background writer) | ⭐ Tạo ra đúng thứ `SRS-NFR-13` cấm: **cửa sổ thời gian mà artifact tồn tại còn bằng chứng thì chưa**. Một crash trong cửa sổ đó ⇒ artifact **vĩnh viễn** không có bằng chứng. ⛔ Không có cách nào phát hiện sau đó | [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) Alternatives `(a)` |
| **`SC-2`** | **Reconcile job** chạy đêm để **vá** những dòng bằng chứng bị thiếu | ⭐⭐ **Tệ hơn `SC-1`.** Một dòng `change_log` do **máy vá lại sau sự việc** ⛔ không phải bằng chứng về một **quyết định của con người** — và nó ⛔ **không phân biệt được với giả mạo**. Nó biến một lỗ hổng **nhìn thấy được** thành một hồ sơ **trông có vẻ đầy đủ** | [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) Alternatives `(f)` |
| **`SC-3`** | Tách dữ liệu ra **database thứ hai**, hoặc đặt một service HTTP nội bộ giữa artifact và bằng chứng | ⭐ Làm **`P-1` không thể đạt được VỀ NGUYÊN LÝ** — ⛔ không phải *"khó"*, mà là ⛔ **không tồn tại transaction nào bao được cả hai** (`P-5`). Đây là lý do `SRS-NFR-21` cắt microservices và 2 DB, và lý do được nêu đúng là **2 DB = mất transaction boundary `KC-4`** | `D-05` · [ADR-017 `Q4.3`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) `P-5` |
| **`SC-4`** | Rải `change_log` theo **module chủ sở hữu** cho gọn | Phá **TÍNH DUY NHẤT** của bảng ⇒ phá **chính điều kiện kiểm chứng** của `KC-4`: ⛔ không còn **một** bảng nào để hỏi *"bằng chứng của artifact này có đủ không"* | [ADR-005](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) Alternatives `(c)` |

⭐ **Guardrail vận hành cho Security Review Gate**: bất kỳ đề xuất nào chạm bốn kịch bản trên — kể cả khi được gói dưới tên *"tối ưu latency"*, *"giảm contention"*, *"tách bounded context"* — **phải trả lời được `P-1`…`P-5` bằng test TRƯỚC khi được xét**. ⛔ Không xét bằng lập luận.

### 4.4 Câu PHẢI viết đúng — và câu ⛔ TUYỆT ĐỐI không được viết

> [!CAUTION]
> ⛔⛔ **⛔ ĐỪNG viết ở bất kỳ file nào rằng *"tầng DB cưỡng chế `KC-4`"*.**
>
> **Câu đúng, nguyên trạng theo [ADR-017 `Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)**: tầng DB cưỡng chế các **CỘT** và tính **APPEND-ONLY** (`GR-1`…`GR-5`); tính **NGUYÊN TỬ** được cưỡng chế bằng **kiến trúc 1-DB (`L1`) + middleware (`L2`) + test CI (`L3`)**.
>
> ⛔ Không `CHECK`, ⛔ không trigger, ⛔ không constraint nào bắt được *"nếu anh `INSERT` cái này thì anh **phải** `INSERT` cái kia trong cùng transaction"* — vì lúc ràng buộc chạy, transaction chưa kết thúc và DB ⛔ không biết cái gì **sẽ** được ghi tiếp.

⇒ **Hệ quả cho Security Review Gate**: `KC-4` ⛔ **không kiểm được bằng cách đọc schema**. Nó chỉ kiểm được bằng **ba bằng chứng cùng lúc**:

| Lớp | Bằng chứng phải xuất trình |
|:--:|---|
| **`L1`** | Cấu hình kết nối: **một** connection pool tới **một** PostgreSQL instance (`P-5`) |
| **`L2`** | **Một** middleware `change_log` dùng chung ([ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)); mọi đường ghi đi qua nó trong **cùng** unit-of-work với ghi nghiệp vụ |
| **`L3`** | Test CI `P-1`…`P-5` **xanh**, cộng test *"endpoint bỏ qua middleware ⇒ FAIL"* |

### 4.5 Yêu cầu quyền DB mà file này SỞ HỮU

Theo hợp đồng trích dẫn [ADR-017 `Q4.7`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) (hàng `Spec-Security-*`):

| Mã | Yêu cầu | Neo |
|:--:|---|---|
| **`SEC-LC-1`** | ⛔ **KHÔNG role ứng dụng nào** (`app_api`, `app_worker`, `app_public_intake`) được cấp `UPDATE` hoặc `DELETE` trên `public.change_log` và `public.usage_event` | `GR-3` · [ADR-018 `Q1`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) |
| **`SEC-LC-2`** | ⛔ **KHÔNG cấp `BYPASSRLS`** cho role ứng dụng hay role worker — đã bị [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) bác, ghi lại ở đây vì nó là **đường phá `GR-5`** | [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) `(h)` |
| **`SEC-LC-3`** | Quyền DDL **chỉ** thuộc role owner/migration, tách khỏi mọi role ứng dụng — nếu không, `GR-3` **tự vô hiệu** (ai `ALTER` được bảng thì `REVOKE` không còn nghĩa) | [ADR-006 `D7`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| **`SEC-LC-4`** | Chống đếm trùng khi retry dựa trên **idempotency key** ⇒ ⛔ **không được giải bằng `UPDATE`/`DELETE`** trên bảng append-only | [ADR-018 `Q3`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) |

⚠️ **Phần còn mở của `KC-4`**: *thứ tự chính xác trong vòng đời job* — dòng `usage_event` gắn vào lần `INSERT generation` nào, và `cost_usd` thực đo đi vào bằng `INSERT` hay `UPDATE`. [ADR-017 `Q4.5`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) **route đi chứ không giải**. *Ai đóng*: **Architect, lô DB Schema**. *Khi nào*: **trước khi hai file schema tương ứng được duyệt**. ⚠️ Ràng buộc mang theo: lời giải phải giữ **cả** `P-1`…`P-5` **và** tính append-only.

---

## 5. ⛔ `SRS-NFR-15` — vì sao hệ thống KHÔNG được có copyright / similarity detection

> [!CAUTION]
> ⛔⛔ **`SRS-NFR-15` — mức độ rắn CHỐT.** Hệ thống **KHÔNG được** có bộ phát hiện *"truyện này có thể có bản quyền của người khác"* — ⛔ copyright detection, ⛔ plagiarism check, ⛔ similarity scan, ⛔ chấm điểm/gắn cờ *"nghi vấn bản quyền"* — **trước khi có xác nhận của luật sư**.

### 5.1 ⭐ Lý do — và vì sao mục này là một trong những mục có giá trị nhất của file

Điều kiện **(a)** của miễn trừ trách nhiệm theo **Điều 198b** là ***"không biết"***.

⇒ Xây một bộ phát hiện **tạo ra đúng cái tri thức mà luật đang miễn trừ cho việc KHÔNG CÓ** ⇒ ⭐ **tự phá miễn trừ của chính mình**.

⚠️ **Đây là chỗ phản xạ nghề nghiệp làm ngược.** Nguồn nói thẳng: *"Một dev sẽ làm ngược điều này theo bản năng, vì **'chủ động kiểm tra' nghe như hành vi có trách nhiệm**"*. Với một Security Auditor thì phản xạ còn mạnh hơn — *"quét input"* là mặc định nghề nghiệp. Ở hệ thống này, **cái quét chính là cái gây thiệt hại**.

### 5.2 ⛔ Hệ quả bắt buộc cho mọi tài liệu Security và mọi lô sau

| # | Quy tắc | Ghi chú |
|:--:|---|---|
| **1** | ⛔ ***"Thiếu content scanning" ⛔ KHÔNG được xếp vào cột lỗ hổng*** ở bất kỳ file Security nào — kể cả `Spec-Security-Threat-Model.md` | Đây là mục *"tính năng an toàn lại là rủi ro"* |
| **2** | Nếu một lô Phase 2/Phase 3 sinh ra đề xuất *"quét nội dung upload để phát hiện vi phạm"*, đó là **VI PHẠM một requirement CHỐT**, ⛔ **không phải một cải tiến** | Xử lý: **từ chối tại review**, ⛔ không thương lượng phạm vi |
| **3** | ⛔ **Không integration nào được gọi dịch vụ copyright / similarity detection bên ngoài** | Gọi vendor bên ngoài cũng **tạo ra tri thức** — cùng hậu quả |
| **4** | ⛔ **Không quét / flag / chấm điểm nghi vấn bản quyền** ở luồng takedown (`F7`) | [SDD §5.4](../Architecture/SDD-Comic-Studio.md) ghi đây là **cấm tuyệt đối** của `F7` |
| **5** | ⛔ **Không dùng lý do này để bỏ các phép kiểm khác.** Nó **chỉ** áp cho phán đoán *"nội dung này có thể vi phạm bản quyền"* — ⛔ không áp cho abuse control, ⛔ không áp cho rate limit, ⛔ không áp cho validate định dạng file, ⛔ không áp cho `provider_refusal_log` | ⚠️ Đọc nới ra là **mất các control hợp lệ** |

### 5.3 ⭐ Ranh giới ĐƯỢC PHÉP — phân biệt bắt buộc

| Việc | Cho phép? | Vì sao |
|---|:--:|---|
| Đọc **opt-out signal do chính chủ quyền gắn vào file** (`KC-6`/`L-3`) | ✅ **ĐƯỢC** | ⭐ ***"Đọc nhãn không tạo ra tri thức suy đoán."*** Đây là **dữ kiện khách quan** do bên thứ ba công bố, ⛔ không phải phán đoán của hệ thống |
| Tự **suy đoán** một nội dung *"có thể"* thuộc về ai đó | ⛔ **KHÔNG** | Là **tri thức do hệ thống tạo ra** — đúng thứ phá điều kiện (a) |
| Tiếp nhận và xử lý **thông báo từ chủ quyền** (takedown) | ✅ **ĐƯỢC** | Tri thức đến **từ bên ngoài**, và **xử lý trong 72h** chính là điều kiện (c) của miễn trừ |

### 5.4 ⚠️ Điều kiện làm lập luận này sụp đổ — ghi ra, ⛔ không tự giải

⭐ Toàn bộ mục 5 đứng trên tiền đề: **nền tảng này được coi là trung gian theo Điều 198b**. Đó chính là câu hỏi **`GAP-3`/`T-20` — CHƯA CÓ ĐÁP ÁN**.

⇒ Nếu luật sư trả lời *"không phải trung gian"*, miễn trừ ⛔ không áp dụng và **toàn bộ phép tính này phải được luật sư đọc lại từ đầu**. ⛔ **Security Auditor ⛔ không có thẩm quyền dự đoán đáp án đó**, và ⛔ **không được viết thiết kế dự phòng cho một đáp án chưa có**. *Ai đóng*: **PM + luật sư SHTT** · *khi nào*: **trước thương mại hoá**.

---

## 6. Bề mặt takedown — không auth, không tenant context

### 6.1 ⚠️ Ngoại lệ của mô hình RLS — HAI bề mặt

`public.takedown_request` là bề mặt **CÔNG KHAI, ⛔ không cần tài khoản** (`SRS-FR-38`) ⇒ ⭐ **⛔ KHÔNG có tenant để bơm** ⇒ ⛔ **không áp được RLS theo tenant**.

Cách xử lý đã chốt ở [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — ⛔ file này không quyết lại:

- Đường này chạy dưới **role riêng `app_public_intake`**, quyền **CHỈ `INSERT`** vào `public.takedown_request`.
- ⛔ **Không** giải bằng cách cho đường này **bypass RLS**; ⛔ **không** cho nó `SELECT` **bất kỳ bảng nghiệp vụ nào**.
- ⇒ Quy tắc chung: cơ chế bơm context ⛔ **không được giả định mọi session DB đều có tenant**.

⭐⭐ **Bề mặt thứ HAI — ⛔ ĐỪNG gộp với bề mặt trên.** Cùng nghĩa vụ `L-4` còn đẻ ra **nửa VẬN HÀNH**: `GET /v1/admin/takedown-requests` và `PATCH /v1/admin/takedown-requests/{id}` ([Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md), `TD-2`/`TD-3`).

| | Bề mặt CÔNG KHAI (`TD-1`) | ⭐ Bề mặt OPERATOR (`TD-2`/`TD-3`) |
|---|---|---|
| Ai chạm | Bất kỳ ai trên Internet | Người vận hành (founder ở vai operator) |
| Hành vi | ⭐ **Ghi mù MỘT dòng** | ⭐⭐ **ĐỌC và GHI dữ liệu của MỌI tenant** |
| Tenant context | ⛔ Không có | ⛔ Không có |
| Cơ chế | ✅ **CHỐT** — `app_public_intake`, chỉ `INSERT` ([ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)) | ⛔⛔ **CHƯA CÓ** — DB role **chưa pin**, uỷ quyền tầng ứng dụng **chưa tồn tại** |

⚠️ **Hệ quả pháp lý mà mục này SỞ HỮU**: nửa **XỬ LÝ** của `L-4` — *đánh giá đơn rồi thi hành trong 72 giờ* — ⛔ **không tồn tại được nếu không có** bề mặt operator. ⇒ ⭐ **`L-4(c)` (SLA 72h) ⛔ chưa chạy được trên thực tế**, dù mọi bằng chứng ở [6.2](#62--bằng-chứng-của-l-4--và-chỗ-nó-hổng) đã có hình dạng. Và bề mặt đó **đọc `requester_email` + `requester_phone`** ⇒ nó là **nơi `A-9` bị phơi ra**, kéo thẳng vào `T-24`.

⚠️ **Liệt kê threat chi tiết của cả hai bề mặt (abuse / spam / DoS / enumeration / đặc quyền operator) thuộc [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md)** — `AS-13`, `TM-F7-8`, `C-13`, và câu trả lời `TD-Q1` ở §4.5; đường vòng cô lập ở [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) `BP-16`. Ở đây chỉ giữ **yêu cầu về bằng chứng**. ⛔ **Hai file kia là nguồn sự thật, ⛔ mục này không đặc tả lại cơ chế.**

### 6.2 ⭐ Bằng chứng của `L-4` — và chỗ nó hổng

| Nghĩa vụ (`L-4`) | ⭐ Bằng chứng trong hệ thống | ⚠️ Chỗ hổng |
|---|---|---|
| **(a)** Công cụ tiếp nhận takedown (form + `copyright@`) | Hàng `public.takedown_request`; đường `INSERT` tồn tại và chạy được **không cần tài khoản** | ✅ ~~*Policy RLS còn mở*~~ — **`P-3` ĐÃ ĐÓNG** ([DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md)). ⭐ **Chỗ hổng THẬT nay là bề mặt vận hành**: `TD-2`/`TD-3` — nửa **operator** của chính nghĩa vụ này — ⛔ **chưa triển khai được** vì `TD-Q1` (DB role + uỷ quyền) chưa lands ripple. ⇒ ⚠️ **Nghĩa vụ (a) mới xong nửa TIẾP NHẬN, ⛔ chưa xong nửa XỬ LÝ** — xem hàng (c) |
| **(b)** **Đăng ký đầu mối (email + SĐT) với Bộ VHTTDL** | ⛔⛔ **KHÔNG CÓ ARTIFACT NÀO TRONG HỆ THỐNG.** Bằng chứng là **giấy tờ đăng ký ngoài hệ thống** | ⭐ **Security Review Gate ⛔ KHÔNG kiểm được hàng này từ codebase.** Phải kiểm bằng checklist vận hành. *Ai đóng*: **Founder/PM** · *khi nào*: **trước khi mở cho người ngoài upload** (`BLOCKER-02`) |
| **(c)** **SLA 72 giờ**, xử lý bằng **soft-delete + disable-access cấp project** | ⭐ **Timestamp tiếp nhận DO HỆ THỐNG GHI** là mốc đếm SLA ([SDD §5.4](../Architecture/SDD-Comic-Studio.md), §6.4) + hàng `public.project_access_state` + `change_log` row của hành động (`KC-2`, commit cùng transaction theo `KC-4`) | ⚠️ Timestamp là **bằng chứng SLA** ⇒ ⛔ **không được để client cung cấp**, ⛔ không được sửa. ⚠️ `SRS-NFR-20` chốt **cơ chế** rate limit nhưng **ngưỡng số là `T-10`** ⇒ chưa có số để chống spam làm nhiễu chính mốc SLA |

### 6.3 Ba ràng buộc cứng của luồng takedown

1. ⛔ **KHÔNG hard delete.** Dữ liệu **PHẢI GIỮ** cho counter-notice. Dùng hard-delete để làm takedown là **phá mất chính bằng chứng** ⇒ [ADR-010 `D7`](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md): **hai đường xoá TÁCH BIỆT, ⛔ không gộp** (`L-4` ≠ `L-7`).
2. ⭐ **Cờ trạng thái cấp project phải được kiểm ở MỌI đường đọc và export.** Điểm cưỡng chế đã có sẵn: [`SDD-HG-01.4`](../Architecture/SDD-Comic-Studio.md) buộc `export_artifact` chỉ sinh khi project **không** ở trạng thái disable-access, kiểm **ở tầng server** qua **đúng một** hàm dùng chung — ⛔ không `force`, ⛔ không `skip_gates`, ⛔ không `admin_override`.
3. ⛔ **Không quét / flag / chấm điểm nghi vấn bản quyền** ở luồng này — [mục 5](#5--srs-nfr-15--vì-sao-hệ-thống-không-được-có-copyright--similarity-detection).

### 6.4 Các `TBD` chặn tính đầy đủ của luồng này

| `TBD` | Nội dung | Ai đóng · khi nào |
|:--:|---|---|
| **`T-24`** (`b-4`) | **Bảo vệ dữ liệu cá nhân / quyền riêng tư**. ⚠️ `SRS-FR-38` **bắt buộc thu email + số điện thoại** của người gửi takedown — người **NGOÀI hệ thống, ⛔ không có tài khoản**, ⛔ không có tenant, ⛔ không nằm trong mô hình `KC-5`. ⛔ **Không nêu tên văn bản pháp luật cụ thể ở đây** (`CẤM-13`) | **Luật sư** · cùng gói `SRS-NFR-17` |
| **`T-29`** | Nội dung / hình thức / thời hạn **thông báo cho tenant bị takedown**. ⚠️ Chính bước đó là **điều kiện tối thiểu để counter-notice tồn tại** | ⭐ **owner: Founder + luật sư**, PM điều phối — PM gán ở [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) sau khi **chấp nhận lời từ chối** của Security Auditor |
| ⭐ **`TD-Q1`** | ⭐⭐ **Bề mặt OPERATOR chưa triển khai được** — DB role + cơ chế uỷ quyền. ⚠️ Đây là hàng chặn **nửa XỬ LÝ** của `L-4`: ⛔ không có nó thì bước *đánh giá đơn rồi thi hành trong 72 giờ* ⛔ **không chạy được**, dù nửa TIẾP NHẬN đã đủ. ⛔ **Hàng này ⛔ không thay thế** `T-24`/`T-29` — ba hàng chặn **ba thứ khác nhau** | ✅ **Đã có câu trả lời** ([Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md)) · ⛔ **chưa gỡ chặn**: **PM** lands ripple [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md) — xem `RIP-4` ở [mục 9](#9-ripple) và hàng `TD-Q1` ở **mục 8.3** |

---

## 7. Thứ tự triển khai — `KC-1` và `KC-7` KHÔNG backfill được

### 7.1 ⭐ *"Không backfill được"* nghĩa là gì — chính xác

⚠️ Cụm này ⛔ **không phải** *"làm sau sẽ tốn công hơn"*. Nó nghĩa là: **dữ liệu quá khứ ⛔ KHÔNG có nguồn nào tái tạo lại được.**

| `KC` | Cái mất **vĩnh viễn** nếu làm sau | Vì sao ⛔ không tái tạo được |
|:--:|---|---|
| **`KC-1`** | Mọi generation quá khứ giữ `parent_generation_id = NULL` **mãi mãi** | Quan hệ *"bản này là `refine` của bản kia"* là **ý định tại thời điểm tạo**. Sau đó ⛔ không dữ liệu nào suy ra được — kể cả timestamp |
| **`KC-2`** *(cùng lớp)* | Một hành động người dùng đã xảy ra mà ⛔ không có dòng `change_log` | ⛔ **Không nguồn nào tái tạo lại nó.** Và vá lại sau = **`SC-2`** ở [4.3](#43--cái-gì-hỏng-nếu-ranh-giới-bị-nới--bốn-kịch-bản-cả-bốn-đã-bị-loại) — bằng chứng do máy vá ⛔ không phân biệt được với giả mạo |
| **`KC-7`** | Lịch sử **số dư / HOLD / tiêu dùng** của tenant trong giai đoạn chưa có ledger | ⭐ Số dư là **hàm tổng hợp trên event thô**; ⛔ không có event thì ⛔ không có hàm. Nguồn ghi rõ hậu quả: bỏ hẳn hai bảng ⇒ MVP3 phải **migrate dữ liệu tiền với hai nguồn số dư ĐÃ LỆCH NHAU** |

### 7.2 ⭐ Hệ quả với thứ tự triển khai

| # | Ràng buộc thứ tự | Neo |
|:--:|---|---|
| **1** | ⭐ **`KC-1`…`KC-4` phải có từ MIGRATION SỐ 1** — ⛔ không phải backlog. `BLOCKER-04` chặn **MỌI THỨ** | `SRS-FR-34` · `BLOCKER-04` |
| **2** | ⚠️ **Diễn giải *"generation đầu tiên"*** = generation đầu tiên của **SẢN PHẨM THẬT, tức MVP1** — MVP0 là spike bị vứt và ⛔ **không có database** (ghi tay ra file để đủ dữ liệu đo). ⛔ Đọc thành *"phải có ở MVP0"* là đọc sai | [SDD/SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.G khối `[!IMPORTANT]` |
| **3** | ⭐ **`KC-7`: cưỡng chế là MVP3, nhưng SEAM phải có từ MVP1.** `SRS-FR-32` cấm retrofit **bằng chữ**; HOLD là **một câu ghi bên trong transaction enqueue** ⇒ chèn sau = **viết lại ranh giới `KC-4`** | `SRS-FR-32` · [SDD §8.2 `S-2`](../Architecture/SDD-Comic-Studio.md) |
| **4** | ⚠️ ⛔ **Không được đảo thứ tự để *"làm feature trước, provenance sau"*.** Với `KC-1`/`KC-2`/`KC-7`, mỗi ngày chạy thiếu là **một khối dữ liệu vĩnh viễn không có bằng chứng** — chi phí ⛔ không phẳng theo thời gian mà **tích luỹ** | `BLOCKER-04` · `Valuable-I` |
| **5** | ⚠️ **`BLOCKER-01`/`BLOCKER-02` ⛔ KHÔNG chặn MVP0–MVP1.** Chúng chặn **thương mại hoá** và **mở cho người ngoài upload**. ⛔ Đọc chúng thành *"chặn phát triển"* là ***cách hiểu nhầm đắt nhất*** | [1.2](#12-ba-điều-kiện-chặn---không-phải-câu-hỏi-và--không-chặn-cùng-một-thứ) |

⇒ ⭐ **Hai loại điều kiện chặn, ⛔ không được trộn**: `BLOCKER-04` chặn theo **thứ tự kỹ thuật** (phải có trước khi có dữ liệu thật); `BLOCKER-01`/`BLOCKER-02` chặn theo **cột mốc thương mại**.

---

## 8. Bảng `TBD` — ai đóng và khi nào

> ⛔ **Mục này ⛔ KHÔNG đóng hàng nào.** Nó chỉ trả lời *ai đóng* và *điều kiện gì mở khoá* — mã `T-nn` lấy nguyên từ [SDD §9.1](../Architecture/SDD-Comic-Studio.md), ⛔ không đánh số lại.

### 8.1 Bảy hàng `b-1`…`b-7` của `SRS` §5.2 — ánh xạ sang chủ

⚠️ Bảy hàng này **đã được bổ sung vào `SRS` §5.2 giữa run** (lô `L0` đã chạy) ⇒ chúng **có requirement nguồn**, nhưng **chưa có chỉ tiêu**.

| Hàng | Nội dung | `T-nn` | Ai đóng · khi nào |
|:--:|---|:--:|---|
| **`b-1`** | Mã hoá at-rest / in-transit + **quản lý secret** | `T-16` | **Dev** · sau khi **platform được mua** và MVP0 có số đo. ⚠️ Phần đã quyết **chỉ** gồm: signed URL **có hạn**, ⛔ **không bao giờ** public bucket ([ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)); **TTL là `T-7`** |
| **`b-2`** | Cách **lưu / mã hoá / THU HỒI** API key của khách trong BYOK | `T-27` | ⭐ **owner: Architect + Founder** — PM gán ở [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md). Phải đóng **trước khi BYOK bật**. ⛔ **Cần một ADR mới ⇒ ngoài phạm vi run Phase 2** ⇒ **nợ kỹ thuật số 1** |
| **`b-3`** | Chính sách **lưu giữ / xoá dữ liệu nghiệp vụ** (retention), gồm purge cho bảng append-only | `T-23` | **PM + Luật sư** (cùng nhóm `SRS-NFR-17`). ⚠️ ⛔ **Khác** RPO/RTO (`T-9`, backup). Hệ quả nếu để mở: bảng append-only **tăng vô hạn**; nhưng purge sai chỗ = **xoá bằng chứng `KC-2`** |
| **`b-4`** | **Bảo vệ dữ liệu cá nhân / quyền riêng tư** | `T-24` | **Luật sư**. Xem [6.4](#64-các-tbd-chặn-tính-đầy-đủ-của-luồng-này) |
| **`b-5`** | Mục tiêu **scalability / capacity** | `T-17` | **Founder + dev** · sau khi chọn hosting và MVP0 có số đo |
| **`b-6`** | **i18n / l10n** | `T-28` | ⛔ **owner: CHƯA XÁC ĐỊNH.** Hiện là **giả định vận hành**, ⛔ chưa được phát biểu thành requirement |
| **`b-7`** | **Observability / logging / alerting như một hạng mục** | `T-16` | **Dev** · sau khi platform được mua. ⚠️ Cả [ADR-001](../Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) lẫn [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) **tuyên bố không đóng** hàng này |

### 8.2 `TBD` pháp lý và vận hành mà file này chạm

| `T-nn` | Nội dung | Ai đóng | Khi nào / điều kiện mở khoá |
|:--:|---|---|---|
| **`T-18`** | `GAP-1` — Điều 37a có áp cho inference-time extraction? | **PM + luật sư SHTT** | **TRƯỚC thương mại hoá** — điều kiện chặn cấp dự án |
| **`T-19`** | `GAP-2` — phạm vi khoản 4 Điều 11 | **PM + luật sư SHTT** | như trên. ⚠️ Quy tắc tạm thời **đã quyết**: diễn giải RỘNG |
| **`T-20`** | `GAP-3` — nền tảng có là **trung gian** theo Điều 198b? | **PM + luật sư SHTT** | như trên. ⭐ `SRS-NFR-15` phụ thuộc **trực tiếp** |
| **`T-21`** | `GAP-4` — SynthID có thoả nghĩa vụ đánh dấu máy đọc? | **PM + luật sư**, dev verify | *"phải verify, ⛔ không giả định"* |
| **`T-22`** | Nghĩa vụ **lưu trữ dữ liệu trong lãnh thổ Việt Nam** | **Luật sư SHTT / tuân thủ** | Trước khi có **khách trả tiền**. ⚠️ **Reopen trigger đã ghi trước**: nếu đáp án là *"phải"* thì **cả [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) và [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) mở lại** |
| ~~**`T-25`**~~ | ~~Hành vi bước **HOLD credit** ở MVP1–MVP2 khi chưa có ledger~~ | ✅ **ĐÃ ĐÓNG — Founder chọn: bước HOLD là *no-op*, thay bằng rate limit cho `generate` đếm **số request**, ⛔ không đếm tiền.** ⛔ Không hard quota. Xem [PM run-state `E9`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) | — |
| **`T-29`** | Thông báo cho tenant bị takedown | ⭐ **Founder + luật sư**, PM điều phối (PM gán, [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)) | ⚠️ Chặn tính đầy đủ của luồng counter-notice |
| **`T-10`** | Ngưỡng **rate limit** per tenant · giới hạn dung lượng/số file upload | **PM + Architect** | Sau khi đo tải. ⚠️ Hàng **LAI**: **cơ chế CHỐT**, chỉ ngưỡng số mở |
| **`T-7`** | **TTL của signed URL** | **Dev đề xuất, Founder duyệt** | **MVP1**. ⚠️ Ràng buộc đã chốt sẵn: ngắn hơn TTL phiên đăng nhập · ⛔ không vô hạn, ⛔ không tính bằng ngày |

### 8.3 `TBD` trong Phase 2 mà mục [4](#4--kc-4-soi-sâu--vì-sao-ranh-giới-transaction-chính-là-bằng-chứng) và [6](#6-bề-mặt-takedown--không-auth-không-tenant-context) trỏ tới

| Mã | Nội dung | Ai đóng | Khi nào |
|:--:|---|---|---|
| ~~**`P-3`**~~ | ~~Policy RLS cụ thể cho `public.takedown_request` (và ba bảng định danh)~~ | ✅ **ĐÃ ĐÓNG** — [DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md) (ba bảng định danh) + [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md) (`takedown_request`). ⚠️ Lô Schema đóng hàng này **trước** khi file này được viết | — |
| ⭐ **`TD-Q1`** | ⭐ **DB role + cơ chế uỷ quyền cho bề mặt OPERATOR** `TD-2`/`TD-3` — nửa **XỬ LÝ** của nghĩa vụ `L-4(a)`, và là thứ đang **chặn** SLA 72h chạy thật | ✅ **Đã có câu trả lời** ([Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md): role thứ năm `app_operator`, đường owner **bị loại**). ⚠️ ⛔ **Chưa gỡ chặn** — cần **PM** lands ripple [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md) + [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | ⭐ **Trước** khi công cụ takedown chạy thật (`BLOCKER-02`) |
| ⭐ **`C-3` áp** | ⭐⭐ **Danh sách các đường đọc phải kiểm cờ disable-access ĐÃ ĐÓNG** ([Spec-Security-Threat-Model §4.4](./Spec-Security-Threat-Model.md)), nhưng **4 file `Endpoint-*` ⛔ chưa áp** ⇒ ⚠️ **theo đặc tả hiện tại, nội dung đã bị takedown vẫn đọc được** — chạm thẳng `L-4` | ⭐ **PM giao lô áp**; Architect/Engineer thực hiện | ⚠️ Trước khi công cụ takedown chạy thật |
| **`P-7`** | Thứ tự gắn `usage_event` / `cost_usd` trong vòng đời job — phần còn mở của [ADR-017 `Q4.5`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) | **Architect, lô DB Schema** | Trước khi file schema provenance được duyệt |
| **`P-2`** | Điều kiện `SDD-HG-01.4` có cưỡng chế **thêm** ở tầng DB hay chỉ tầng service | **Architect, lô DB Schema** | Trước khi file schema dialogue/gate được duyệt |

---

## 9. `RIPPLE`

⛔ **File này ⛔ không sửa file nào khác.** `docs/030-Specs/Architecture/**` đã **đóng băng**. Ba mục dưới đây là **đề nghị gửi PM**, ⛔ **không tự thực hiện**.

| # | File | Nội dung đề nghị | Mức |
|:--:|---|---|:--:|
| **`RIP-1`** | `docs/030-Specs/Specs-MOC.md` | Bổ sung file này vào nhóm **Security** khi PM viết MOC (MOC là **độc quyền PM**) | thường lệ |
| **`RIP-2`** | [Spec-Security-Threat-Model](./Spec-Security-Threat-Model.md) (lô `L18`) | ⚠️ **Phải mang theo [mục 5](#5--srs-nfr-15--vì-sao-hệ-thống-không-được-có-copyright--similarity-detection)**: ⛔ *"thiếu content scanning"* ⛔ không được xếp vào cột lỗ hổng. ✅ **Đã verify ở L33 — file đó viết ĐÚNG chiều** (§5 của nó cấm tường minh) ⇒ ⛔ **không còn là xung đột** | ✅ **đã giải** |
| **`RIP-3`** | [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) (lô `L18`) | Mục [6.1](#61-️-ngoại-lệ-của-mô-hình-rls--hai-bề-mặt) chỉ nêu **hệ quả bằng chứng** của hai bề mặt takedown. Chiều sâu (`app_public_intake`, `BP-16` operator, abuse surface) thuộc file đó ⇒ ⛔ tránh viết hai nguồn sự thật | thường lệ |
| ⭐ **`RIP-4`** | ⭐⭐ [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md) + [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — ⛔ **ĐÃ ĐÓNG BĂNG** | ⭐ Câu trả lời `TD-Q1` chốt **role thứ NĂM `app_operator`** ([Spec-Security-Threat-Model §4.5](./Spec-Security-Threat-Model.md)) ⇒ `SDD` §7.4 *"bốn DB role"* / *"bốn connection string"* phải thành **năm**, và `ADR-006` cần một carve-out cạnh `D6`, `W-2` mở rộng. ⛔ **L33 ⛔ KHÔNG tự sửa** — đề nghị gửi PM xử ở **close-step**. ⚠️ Cho tới lúc đó `TD-2`/`TD-3` **vẫn bị chặn** ⇒ nửa **XỬ LÝ** của `L-4` chưa chạy được | ⭐ **chặn `BLOCKER-02`** |
| ⭐ **`RIP-5`** | `docs/030-Specs/API/**` — 4 file: `Endpoint-Page-Layout.md`, `Endpoint-Bubble-Typeset.md`, `Endpoint-Panel-Script.md`, `Endpoint-Human-Gates.md` *(+ phần thiếu của `Endpoint-Generation.md`)* | ⭐⭐ **Danh sách các đường đọc phải kiểm cờ disable-access nay ĐÃ ĐÓNG** ([Spec-Security-Threat-Model §4.4](./Spec-Security-Threat-Model.md)), nhưng 4 file trên ⛔ **không hề nhắc** `access_state` ⇒ ⚠️ **theo đặc tả hiện tại, nội dung đã bị takedown VẪN ĐỌC ĐƯỢC** — chạm thẳng nghĩa vụ `L-4`. ⛔ **L33 ⛔ KHÔNG sửa file API** — PM giao một lô áp | ⚠️ **chặn gate** |

---

## 10. Tài liệu tham khảo

### 10.1 Tầng 020 — Requirements

- [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) — §3.G (`SRS-FR-34`…`SRS-FR-41`, `SRS-NFR-13`…`SRS-NFR-17`) · `SRS-NFR-01`, `SRS-NFR-05`, `SRS-NFR-20`, `SRS-NFR-23` · §5.1 (SLA 72h, deadline ~01/03/2027) · **§5.2 hàng `b-1`…`b-7`** · §6.2 (hai bẫy cắt lẫn)

### 10.2 Tầng 030 — Architecture (chỉ đọc, ⛔ không sửa)

- [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) — §5.4 (`F1`/`F7` chạm nghĩa vụ pháp lý) · §6.2 (`KC-4` áp ở đâu) · **§6.3 `SDD-HG-01`** · §6.4 (bốn dòng audit) · **§9.1** (`T-1`…`T-29`), §9.2 (`P-1`…`P-11`)
- [ADR-017 — Provenance Chain And One Transaction Boundary](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — ⭐ **nguồn duy nhất của `KC-4`**: `Q1`, `Q2`, `Q3`, `Q4.1`…`Q4.7`, Alternatives `(a)`/`(f)`
- [ADR-006 — RLS Tenant Context Injection](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) — `D6` (bề mặt không tenant), `D7` (role migration)
- [ADR-010 — Tenant Isolation With RLS](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) — `D7` (hai đường xoá), `D8` (test nhị phân), `D10` (giới hạn RLS)
- [ADR-018 — Usage Event And Rollup Model](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) — `Q1` (append-only ở tầng DB), `Q3` (idempotency key)
- [ADR-005 — Platform Table Schema Placement](../Architecture/ADR-005-Platform-Table-Schema-Placement.md) · [ADR-002 — Hosting Platform And Region](../Architecture/ADR-002-Hosting-Platform-And-Region.md) · [ADR-004 — Object Storage Vendor And Signed URL](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) · [ADR-015 — Job Queue In Postgres](../Architecture/ADR-015-Job-Queue-In-Postgres.md)

### 10.3 Tầng 030 — Schema

- [DB-Entity-Credit-Ledger](../Schema/DB-Entity-Credit-Ledger.md) — `KC-7`, lý do ⛔ không bỏ hẳn dù cụm là `[OoH]` MVP3

### 10.4 Tầng 010 — Planning

- [findings/business-analyst.md](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/business-analyst.md) — §3.1 (`L-1`…`L-7`) · §3.2 (⛔ anti-feature) · §3.3 (`P-1`…`P-8` lựa chọn sản phẩm) · **§3.4 (bốn khoảng trống pháp lý + `BLOCKER-01`/`02`/`04` + `CẤM-13`)**

---

> [!WARNING]
> ⛔ **Nhắc cuối — dành cho người đọc file này ở Security Review Gate.**
> Hai câu dễ viết sai nhất, cả hai đều đã bị cấm tường minh ở trên:
> 1. ⛔ *"Tầng DB cưỡng chế `KC-4`"* → câu đúng ở [4.4](#44-câu-phải-viết-đúng--và-câu--tuyệt-đối-không-được-viết).
> 2. ⛔ *"Hệ thống thiếu content scanning ⇒ đây là một lỗ hổng"* → câu đúng ở [mục 5](#5--srs-nfr-15--vì-sao-hệ-thống-không-được-có-copyright--similarity-detection).
