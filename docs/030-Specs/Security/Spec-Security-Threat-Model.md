---
id: SPEC-SEC-THREAT-MODEL
type: security-spec
status: draft
project: comic-studio
created: 2026-08-29
updated: 2026-08-30
---

# Spec Security: Threat Model — Comic Studio

Threat model of: [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)

> [!IMPORTANT]
> **Tài liệu này là bản đồ mối đe doạ, ⛔ không phải nơi ra quyết định kiến trúc.**
> Mọi cơ chế phòng thủ đã được quyết ở `SDD` hoặc ở một `ADR`. File này **trỏ** tới chúng bằng mã điều khoản và **soi xem chúng có bị vòng qua được không**. ⛔ Không đặc tả lại cơ chế; ⛔ không mở lại quyết định đã CHỐT.
> **Phần cô lập tenant** — mọi đường vòng qua RLS, connection pool, job queue, signed URL — nằm ở [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md), ⛔ không lặp ở đây.
> **Phần soạn thảo nghĩa vụ pháp lý** — checklist Điều 198b, nội dung ToS, AI disclosure — thuộc [Spec-Security-Legal-Compliance](./Spec-Security-Legal-Compliance.md) (lô L19, ✅ **đã viết xong**). File này chỉ soi **góc an ninh** của các nghĩa vụ đó.

## Mục lục

1. [Câu hỏi chưa có câu trả lời](#1-câu-hỏi-chưa-có-câu-trả-lời)
2. [Tài sản & bề mặt tấn công](#2-tài-sản--bề-mặt-tấn-công)
3. [STRIDE trên bảy luồng `F1`–`F7`](#3-stride-trên-bảy-luồng-f1f7)
4. [Biện pháp](#4-biện-pháp)
5. [⛔ Anti-feature `SRS-NFR-15` — vì sao file này KHÔNG đề xuất phát hiện tương đồng](#5--anti-feature-srs-nfr-15--vì-sao-file-này-không-đề-xuất-phát-hiện-tương-đồng)
6. [Nghĩa vụ pháp lý — phần thuộc file này](#6-nghĩa-vụ-pháp-lý--phần-thuộc-file-này)
7. [Ma trận `KC-1`…`KC-7`](#7-ma-trận-kc-1kc-7)
8. [Bảng `TBD` của file này](#8-bảng-tbd-của-file-này)
9. [Tài liệu tham khảo](#9-tài-liệu-tham-khảo)

### Quy ước trích dẫn

| Ký hiệu | Nghĩa |
|---|---|
| `A-n` | Tài sản cần bảo vệ, định nghĩa ở [§2.1](#21-tài-sản) |
| `AS-n` | Bề mặt tấn công, định nghĩa ở [§2.2](#22-bề-mặt-tấn-công) |
| `TM-Fx-n` | Mối đe doạ số `n` trên luồng `Fx` của [`SDD` §5](../Architecture/SDD-Comic-Studio.md) |
| `C-n` | Biện pháp, định nghĩa ở [§4](#4-biện-pháp) |
| `T-n`, `P-n` | Mã `TBD` của [`SDD` §9](../Architecture/SDD-Comic-Studio.md) — ⛔ file này không đánh mã `TBD` mới khi `SDD` đã có mã |
| `L-n` | Ràng buộc bắt buộc pháp lý, [§6](#6-nghĩa-vụ-pháp-lý--phần-thuộc-file-này) |
| `KC-n` | Bảy hàng chốt không thương lượng, [§7](#7-ma-trận-kc-1kc-7) |

⛔ Mọi requirement được neo bằng **mã** (`SRS-FR-*` / `SRS-NFR-*`), ⛔ không bằng số dòng.

---

## 1. Câu hỏi chưa có câu trả lời

> [!CAUTION]
> ⭐ **Mục này đứng đầu tài liệu là có chủ ý.** Một threat model mở đầu bằng danh sách biện pháp sẽ được đọc là *"đã an toàn"*. Sự thật là: **bốn nhóm câu hỏi dưới đây chưa có câu trả lời**, và phần lớn ⛔ **không thuộc thẩm quyền của Security Auditor**.
>
> ⛔ **Ba cách đọc sai bị cấm tường minh**:
> 1. ⛔ Đọc một hàng ở đây thành *"rủi ro đã đánh giá, mức thấp"*. Chúng là **câu hỏi**, ⛔ không phải kết luận.
> 2. ⛔ Đọc một hàng `TBD` thành **giấy phép tự chọn số** — cấm bởi `R-5` ([`SDD` §1.1](../Architecture/SDD-Comic-Studio.md)) và [`SRS` §5.2](../../020-Requirements/SRS-Comic-Studio.md): *"bịa một con số performance là lỗi nghiêm trọng hơn để trống nó"*.
> 3. ⛔ Đọc *"cơ chế CHỐT + tham số `TBD`"* thành *"cả cơ chế cũng chưa quyết"*. `SRS-NFR-20` (abuse controls) là hàng **LAI**: cơ chế **đã CHỐT**, chỉ ngưỡng số mở.

### 1.1 Nhóm CHỜ LUẬT SƯ — ⛔ Security Auditor KHÔNG có thẩm quyền đóng

| # | Câu hỏi | Nó chặn cái gì trong threat model này | Ai đóng | Khi nào |
|---|---|---|---|---|
| `T-18` | **Điều 37a có áp cho inference-time extraction không?** (`SRS-NFR-17` Q1) | Quyết định liệu bước extraction ở `F2` có phải một hành vi chịu điều chỉnh hay không ⇒ ảnh hưởng phạm vi log bắt buộc | **PM + luật sư SHTT** | ⭐ TRƯỚC thương mại hoá — điều kiện chặn cấp dự án |
| `T-19` | **Phạm vi khoản 4 Điều 11** (`SRS-NFR-17` Q2) | Phạm vi nghĩa vụ đánh dấu nội dung AI ở `F6` (`L-5`). ⚠️ **Quy tắc tạm thời ĐÃ QUYẾT**: thiết kế theo **diễn giải RỘNG** (`SRS-FR-39`) cho tới khi có câu trả lời | **PM + luật sư SHTT** | như trên |
| `T-20` | **Nền tảng *hosting + processing* có được coi là trung gian theo Điều 198b không?** (`SRS-NFR-17` Q3) | ⭐ Câu hỏi mà **`SRS-NFR-15` phụ thuộc trực tiếp** — xem [§5](#5--anti-feature-srs-nfr-15--vì-sao-file-này-không-đề-xuất-phát-hiện-tương-đồng) | **PM + luật sư SHTT** | như trên |
| `T-21` | **SynthID của provider có thoả nghĩa vụ đánh dấu máy đọc không?** (`SRS-NFR-16`) | Quyết định stage watermark ở `F6` là *"đã có sẵn"* hay *"phải tự nhúng"* — chi phí đường lui **chưa ước lượng** | **PM + luật sư SHTT**, dev verify kỹ thuật | *"Phải verify, ⛔ không giả định"* |
| `T-22` | **Có nghĩa vụ lưu trữ dữ liệu trong lãnh thổ Việt Nam không?** | ⚠️ **Reopen trigger đã ghi trước**: nếu *"phải"* thì [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) và [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) mở lại **cùng lúc** | **PM + luật sư SHTT/tuân thủ** | Trước khi có khách trả tiền |
| `T-23` | **`b-3` — giữ dữ liệu bao lâu?** ([`SRS` §5.2](../../020-Requirements/SRS-Comic-Studio.md) hàng `b-3`) | `change_log` và `usage_event` là append-only ⇒ **tăng vô hạn** nếu không có retention. ⚠️ ⛔ Đây ⛔ **không** phải hàng RPO/RTO/backup (`T-9`) — hai thứ khác nhau | **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| `T-24` | **`b-4` — nghĩa vụ nào áp cho dữ liệu cá nhân?** ([`SRS` §5.2](../../020-Requirements/SRS-Comic-Studio.md) hàng `b-4`) | ⭐ `SRS-FR-38` **bắt buộc thu email + số điện thoại** của người gửi takedown — người **NGOÀI hệ thống, không có tài khoản**. Đây là dữ liệu cá nhân duy nhất mà hệ thống thu **không** qua onboarding. ⛔ Không nêu tên văn bản pháp luật cụ thể ở đây | **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| `CẤM-13` | **Ràng buộc lên CÁCH VIẾT của chính file này** | ⛔ **CẤM viết requirement như thể phạm vi Điều 37a đã rõ** — hiểu biết hiện tại dựa trên bản **tóm tắt**, ⛔ không phải nguyên văn | — (ràng buộc thường trực) | ⛔ Không đóng được, phải tuân |

**Ba điều kiện chặn kế thừa** — ghi lại vì chúng đổi ngữ cảnh rủi ro của toàn bộ mục 3, ⛔ file này không đóng hàng nào:

| # | Điều kiện | Chặn cái gì |
|---|---|---|
| `BLOCKER-01` | Ba câu hỏi luật sư chưa có trả lời **bằng văn bản** | ⭐ Chặn **THƯƠNG MẠI HOÁ**. ⛔ **KHÔNG** chặn MVP0–MVP1 — đọc sai điều này là *"cách hiểu nhầm đắt nhất"* |
| `BLOCKER-02` | Checklist safe harbour Điều 198b chưa hoàn tất | Chặn **mở cho người ngoài upload**, ⛔ không chặn dùng nội bộ |
| `BLOCKER-04` | Provenance chain chưa ghi từ generation **đầu tiên** | ⭐ Chặn **MỌI THỨ** — vì ⛔ **không backfill được** (`KC-1`, xem [§7](#7-ma-trận-kc-1kc-7)) |

### 1.2 Nhóm input an ninh mà Phase 1 IM LẶNG (`SRS` §5.2 hàng `b-1`…`b-7`)

> ⚠️ Bảy hàng `b-1`…`b-7` **đã tồn tại trong `SRS` §5.2** (lô L0 đã chạy). Chúng là **hàng `TBD` có mã**, ⛔ không phải khoảng trống vô danh — nhưng ⛔ **vẫn chưa có requirement nguồn nào phát biểu nghĩa vụ**, nên file này ⛔ **không được coi chúng là đã quyết**.

| Hàng | Vì sao nó là input BẮT BUỘC của threat model | Ai đóng | Khi nào |
|---|---|---|---|
| **`b-1`** — mã hoá at-rest / in-transit + quản lý secret | ⭐ Không có nó thì mọi phát biểu về `A-1`…`A-4` ở [§2.1](#21-tài-sản) chỉ dựa vào **mặc định của vendor**. Phần đã quyết **chỉ gồm**: signed URL có hạn, ⛔ không bao giờ public bucket (`SRS-FR-02`), và cấu hình **chỉ** qua biến môi trường ([ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) điều 6) | **Dev** (`T-16`) | Sau khi platform được mua và MVP0 có số đo |
| **`b-2`** — lưu / mã hoá / **thu hồi** API key của khách (BYOK) | ⭐ **Hạng mục rủi ro cao nhất của cả hệ thống**: lưu credential của bên thứ ba. `SRS-FR-32` cấm retrofit ba tầng giá ⇒ **seam phải có sớm**, dù BYOK là `[OoH]` MVP4 | ⭐ **owner: Architect + Founder** (`T-27`) — PM gán ở [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md); chọn cơ chế KMS **kéo theo** [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) | Trước khi seam BYOK bật. ⚠️ Phụ thuộc `b-1` và `SRS-NFR-08`. ⛔ **Đóng đúng nghĩa cần một ADR mới ⇒ ngoài phạm vi run Phase 2** ⇒ **nợ kỹ thuật số 1** |
| **`b-3`** — retention nghiệp vụ | Xem `T-23` ở [§1.1](#11-nhóm-chờ-luật-sư---security-auditor-không-có-thẩm-quyền-đóng) | **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| **`b-4`** — dữ liệu cá nhân | Xem `T-24` ở [§1.1](#11-nhóm-chờ-luật-sư---security-auditor-không-có-thẩm-quyền-đóng) | **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| **`b-5`** — mục tiêu scalability / capacity | Không có trần tài nguyên thì ⛔ **không tính được** ngưỡng nào là *"tấn công"* và ngưỡng nào là *"dùng nhiều"* ⇒ chặn việc chốt ngưỡng của `C-6` | **Founder + dev** (`T-17`) | Sau khi chọn hosting và MVP0 có số đo |
| **`b-6`** — i18n / l10n | Ảnh hưởng gián tiếp: xử lý Unicode ở typeset và ở compositor là bề mặt xử lý dữ liệu không tin cậy (`TM-F6-3`) | ⛔ **owner: chưa xác định** (`T-28`) | Khi có người phát biểu nó thành requirement |
| **`b-7`** — observability / logging / alerting **như một hạng mục** | ⭐ Đây là hàng làm **hỏng khả năng PHÁT HIỆN** của toàn bộ threat model: ⛔ **không có** ngưỡng alert queue depth, ⛔ **không có** uptime SLA. ⚠️ Hệ quả nặng nhất: failure mode *"fail-closed 0 row"* của [ADR-006 `D4.3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) **không để lại dấu vết** nếu không có alerting | **Dev** (`T-16`) — cả [ADR-001](../Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) lẫn [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) đều **tuyên bố không đóng** | Sau khi platform được mua |

### 1.3 Nhóm tham số chờ SỐ ĐO — ⛔ file này KHÔNG gán số

| Tham số | Cơ chế đã CHỐT ở đâu | Ràng buộc lên con số tương lai *(quyết được ngay)* | Ai đóng | Khi nào |
|---|---|---|---|---|
| `T-10` **Ngưỡng rate limit per tenant** · giới hạn dung lượng/số file upload | `SRS-NFR-20` — hàng **LAI**, **cơ chế CHỐT** | ⭐ Rate limit của `generate` **đếm SỐ REQUEST**, ⛔ **không đếm tiền**; ⛔ **không HOLD credit ở MVP1–MVP2** (`KC-7` là `[OoH]` MVP3). Ngưỡng phải áp **per tenant**, ⛔ không per user | **PM + Architect** | Sau khi đo tải |
| `T-7` **TTL của signed URL** | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 4–5 | Đã chốt sẵn ở ADR-004: ngắn hơn TTL phiên đăng nhập · ⛔ không vô hạn · ⛔ không tính bằng ngày · một hằng số duy nhất | **Dev đề xuất, Founder duyệt** | MVP1 |
| `T-6` **`N` của `in_flight_per_tenant < N`** | `SRS-FR-26` — cơ chế nằm **trong chính câu CLAIM** | ⚠️ Đây là biện pháp chống **DoS chéo tenant** (`TM-F5-4`), ⛔ không chỉ là fairness | **PM + Architect** | Sau MVP0 đo tải thật |
| `T-9` Uptime SLA · RPO/RTO/backup retention · **queue depth alert threshold** | ⛔ Không tài liệu nào đặt | ⚠️ Thiếu chúng ⇒ ⛔ **không có tiêu chí phát hiện** cho `TM-F5-4` và `TM-F7-2` | **Founder + dev** | Sau MVP0 |

### 1.4 Nhóm CHƯA CÓ CHỦ — ⛔ không gán bừa

| # | Hàng | Vì sao nó chạm an ninh | Ghi chú chủ sở hữu |
|---|---|---|---|
| `T-27` | `b-2` BYOK key storage | Xem [§1.2](#12-nhóm-input-an-ninh-mà-phase-1-im-lặng-srs-52-hàng-b-1b-7) | ⭐ **Architect + Founder** (PM gán, `E22`) — ⛔ cần **ADR mới**, ngoài phạm vi run Phase 2 ⇒ **nợ kỹ thuật số 1** |
| `T-29` | **Nội dung / hình thức / thời hạn thông báo cho tenant bị takedown** | ⭐ Bước đó là **điều kiện tối thiểu để counter-notice tồn tại**. ⚠️ Nó cũng là **bề mặt lộ thông tin**: thông báo mang nội dung đơn takedown sẽ **chuyển dữ liệu cá nhân của người khiếu nại** (`b-4`) sang tenant. ⛔ File này ⛔ **không quyết** — nó tương tác trực tiếp với điều kiện miễn trừ Điều 198b | ⭐ **owner: Founder + luật sư**, PM điều phối (PM gán, [`E22`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md)). [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) có nêu `security-auditor` là ứng viên — ⛔ file này **từ chối đóng** vì nó là quyết định pháp lý, ⛔ không phải quyết định kỹ thuật; ✅ **PM chấp nhận lời từ chối** |
| ~~`T-25`~~ | ~~Hành vi của bước HOLD credit ở MVP1–MVP2 khi **chưa có ledger**~~ | Chọn **biện pháp chống lạm dụng chi phí** có hiệu lực ở MVP1–MVP2: chỉ rate limit, hay hard quota tạm | ✅ **ĐÃ ĐÓNG — Founder đã chọn: CHỈ rate limit cho `generate`, đếm **số request**, ⛔ không đếm tiền.** ⛔ **Không** hard quota, ⛔ **không** HOLD credit ở MVP1–MVP2. Xem [PM run-state `E9`](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) (6 điều diễn giải) |

---

## 2. Tài sản & bề mặt tấn công

### 2.1 Tài sản

> Xếp theo **hậu quả khi mất**, ⛔ không theo kích thước dữ liệu.

| # | Tài sản | Mất/lộ nó nghĩa là gì | Neo |
|---|---|---|---|
| **`A-1`** | ⭐ **Bản thảo chưa công bố của khách** (chapter đã upload, Story Bible dẫn xuất) | Rò rỉ chéo tenant ở đây ⛔ **không phải một bug — nó là mất sản phẩm**. Đây là lý do tồn tại của toàn bộ [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) | `SRS-NFR-01` · `KC-5` |
| **`A-2`** | ⭐ **Chuỗi provenance** (`generation` lineage, `change_log`, `field_provenance`, `usage_event`) | ⭐ **Kho bằng chứng pháp lý**, ⛔ không phải log vận hành. Mất/sửa được nó = **mất bảo hộ bản quyền** cho khách. ⛔ **Không backfill được** | `KC-1`…`KC-4` · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`A-3`** | **Artifact ảnh trong object storage** | ⚠️ **Không sinh lại được**: bit-exact reproducibility ⛔ không đạt được (`seed` là provenance metadata, ⛔ không phải replay key). ⇒ đối xử như **kho bằng chứng**, ⛔ không như thư mục cache | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) mục *"Một chỗ dễ đọc sai"* |
| **`A-4`** | **Comic IR / panel spec / typeset layer** — dữ liệu chính của sản phẩm | *"Spec là dữ liệu chính, ảnh chỉ là output"* ⇒ đây là nơi giá trị thiết kế nằm | `SRS-FR-07` |
| **`A-5`** | **Credential của hệ thống**: bốn connection string DB, khoá ký object storage, API key của image/VLM/LLM provider, secret webhook vendor | Lộ một trong bốn connection string = lộ mô hình role; lộ khoá ký = **public bucket không giới hạn thời gian** | [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) điều 6 · `b-1` |
| **`A-6`** | ⭐ **API key của KHÁCH trong BYOK** — `[OoH]` MVP4, seam bắt buộc có sớm | ⭐ Lưu credential của bên thứ ba là **hạng mục rủi ro cao nhất**. ⛔ Chưa có bất kỳ requirement nào nói lưu thế nào (`b-2`, `T-27`) | `SRS-FR-32` |
| **`A-7`** | **Định danh & membership** (`tenant` / `user` / `membership`) | Là **nguồn duy nhất** của `tenant_id` cho RLS. ⛔ Vendor auth ⛔ không sở hữu nó | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 1–2, 4 |
| **`A-8`** | **Trạng thái hai human gate** (`comic.human_gate_state`) | Ghi được `PASS` bằng máy = **phá điều kiện xuất bản** của cả sản phẩm | [`SDD-HG-01`](../Architecture/SDD-Comic-Studio.md) |
| **`A-9`** | **Dữ liệu cá nhân của người gửi takedown** (email + số điện thoại) | ⭐ Người **NGOÀI hệ thống**, ⛔ không có tài khoản, ⛔ không có tenant. Nghĩa vụ áp dụng ⛔ **chưa xác định** (`b-4`, `T-24`) | `SRS-FR-38` |
| **`A-10`** | **Ngân sách gọi provider** (tiền thật, tiêu theo request) | Lạm dụng ở đây ⛔ không lộ dữ liệu — nó **đốt tiền**. Ở MVP1–MVP2 ⛔ **không có** ledger/HOLD để chặn ⇒ ⭐ **rate limit đếm số request là biện pháp DUY NHẤT** (`E9` đã đóng `T-25`) | `SRS-NFR-20` · `SRS-FR-28` (`[OoH]`) |

### 2.2 Bề mặt tấn công

| # | Bề mặt | Ai chạm được | Ràng buộc đã có | Neo |
|---|---|---|---|---|
| **`AS-1`** | **API đã đăng nhập** (SPA → `api`) | Tenant đã xác thực | JWT verify qua **JWKS chuẩn OIDC**; ⛔ không SDK vendor trong đường xử lý request; `tenant_id` tra từ `membership` **mỗi request** | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 3–4 |
| **`AS-2`** | ⭐ **Endpoint takedown CÔNG KHAI** — ⛔ không tài khoản, ⛔ không tenant context | **Bất kỳ ai trên Internet** | Role riêng `app_public_intake`: **chỉ** `INSERT` vào `public.takedown_request`; ⛔ ⛔ không `SELECT` bảng nghiệp vụ nào | [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md) |
| **`AS-3`** | **Presigned `PUT` pha 1** vào `tenant/{tenant_id}/incoming/{upload_id}` | Tenant đã xác thực (và bất kỳ ai giữ URL đó trong TTL) | ⛔ Client **không được** tự quyết key cuối; ⛔ ⛔ không object nào trong `incoming/` được coi là dữ liệu hợp lệ | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 7 |
| **`AS-4`** | **Signed URL đọc** (editor + tải export) | Bất kỳ ai giữ URL trong TTL | ⭐ URL ⛔ **KHÔNG BAO GIỜ** được lưu bền: ⛔ không DB · ⛔ không log · ⛔ không nhúng file export · ⛔ không email/webhook | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3 |
| **`AS-5`** | **Webhook của vendor auth / billing** | Bất kỳ ai biết URL | Verify chữ ký → ghi **bảng inbox** có khoá idempotency → xử lý bất đồng bộ. ⭐ Webhook là **nguồn SỰ KIỆN, ⛔ không phải nguồn SỰ THẬT** | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 6 |
| **`AS-6`** | **Nội dung do người dùng nạp** (file chapter, text dán, thoại đã sửa, tên nhân vật) | Tenant | Đi vào LLM prompt (`F2`, `F3`, `F4`), vào compositor (`F6`), vào tên file export | `SRS-FR-06` |
| **`AS-7`** | **Egress tới provider ngoài** (image, VLM, LLM, storage) | Hệ thống gọi ra | Chỉ qua **adapter**, model version **pinned**; ⛔ không tính năng riêng của vendor | [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 1 |
| **`AS-8`** | **Ingress từ provider**: bytes ảnh, JSON điểm số VLM, text LLM | Provider (và bất kỳ ai chiếm được kênh) | ⛔ Chưa có ràng buộc nào về **parse dữ liệu trả về** — xem `C-8` | — |
| **`AS-9`** | **`public.job`** — kênh giao tiếp **duy nhất** giữa `api` và `worker` | Hai process nội bộ | ⛔ Không HTTP nội bộ, ⛔ không broker; mọi truy vấn qua **đúng một** hàm `claimJobAndBindTenant()` | ranh giới `B-2` ([`SDD` §4.1](../Architecture/SDD-Comic-Studio.md)) |
| **`AS-10`** | **Scheduled job** (rollup `usage_daily`, golden dataset regression) | Cron của platform | Chỉ được **gọi một subcommand** của chính image; ⛔ không một dòng logic nghiệp vụ nào sống trong cấu hình cron | [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) điều 3 |
| **`AS-11`** | **Migration / role owner** | Người vận hành | Role owner **tách khỏi** `app_api` / `app_worker` / `app_public_intake`; ⛔ role ứng dụng ⛔ không có DDL | [ADR-006 `D7`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| **`AS-12`** | **`stdout`/`stderr`** — kênh log duy nhất | Bất kỳ ai đọc được log platform | ⛔ Không ghi log ra file, ⛔ không state trên đĩa cục bộ. ⚠️ Quy tắc **che** nội dung log: xem `C-4` | [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) điều 6 · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3 |
| **`AS-13`** | ⭐⭐ **Bề mặt OPERATOR xuyên tenant** — `GET /v1/admin/takedown-requests` và `PATCH /v1/admin/takedown-requests/{id}` ([Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md), `TD-2`/`TD-3`) | Người vận hành (founder ở vai operator) — ⛔ **không** phải một tenant | ⛔⛔ **CHƯA CÓ.** `public.takedown_request` ⛔ không có `tenant_id` ⇒ hai endpoint này **đọc và ghi dữ liệu của MỌI tenant**: `requester_email`, `requester_phone` (`A-9`), `project_id`, và `access_state` của `public.project_access_state`. **DB role ⛔ CHƯA PIN**; **cơ chế uỷ quyền operator ở tầng ứng dụng ⛔ CHƯA TỒN TẠI** (`membership` ⛔ không có mô hình role/permission). ⇒ Xem `C-13` và câu trả lời `TD-Q1` ở [§4.5](#45--trả-lời-td-q1--db-role-và-uỷ-quyền-cho-bề-mặt-operator) | `SRS-FR-38` · `TD-Q1` của [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md) |
| **`AS-14`** | ⚠️ **Lần GHI ĐẦU TIÊN dòng `public."user"`** — xảy ra khi ⛔ **chưa có** tenant context | Đường đăng nhập lần đầu (webhook vendor auth **hoặc** JIT provisioning) | ⛔⛔ **CHƯA CÓ.** Policy của `public."user"` dựa trên `EXISTS(membership)` ⇒ ghi khi chưa có membership ⛔ không qua được. Carve-out `D6` của [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) ⛔ **không phủ** (nó chỉ cho `INSERT` `public.takedown_request`); hàm `SECURITY DEFINER` của `D3` chỉ **ĐỌC** `user → tenant`, ⛔ không ghi | `API-TN-5` của [Endpoint-Tenancy](../API/Endpoint-Tenancy.md) · [ADR-006 `D3`, `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |

### 2.3 Ba loại session DB — ranh giới tin cậy

⭐ Cơ chế bơm context ⛔ **không được giả định mọi session DB đều có tenant**. Ba loại session tồn tại **hợp lệ**, và mỗi loại là một ranh giới tin cậy riêng:

| Loại session | Role | Trạng thái tenant | Ghi chú an ninh |
|---|---|---|---|
| **Có tenant** | `app_api`, `app_worker` (sau bước `SET LOCAL`) | `app.current_tenant` đã set trong transaction | Trạng thái *bình thường* |
| **Không tenant + carve-out hẹp** | `app_worker` (lúc claim job), `app_public_intake`, ⚠️ **bề mặt operator `AS-13`** (role ⛔ chưa pin), ⚠️ **lần ghi đầu `public."user"` `AS-14`** (cơ chế ⛔ chưa pin) | ⛔ Chưa/không có tenant | ⭐ **Bề mặt đặc quyền đếm được** — chi tiết ở [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) |
| **Owner / migration** | role owner | ⛔ Không áp dụng | ⛔ Không dùng cho đường nghiệp vụ, ⛔ bao giờ |

⇒ **Bề mặt đặc quyền của toàn hệ thống rút về NĂM điểm** — ⚠️ **ba điểm đầu có cơ chế đã CHỐT, hai điểm sau ⛔ CHƯA PIN nhưng vẫn phải nằm trong danh sách**:

| # | Bề mặt đặc quyền | Trạng thái cơ chế |
|---|---|---|
| 1 | Hàm `SECURITY DEFINER` phân giải `user → tenant` | ✅ CHỐT — [ADR-006 `D3`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| 2 | Cặp policy carve-out trên `public.job` | ✅ CHỐT — [ADR-006 `D4.1`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| 3 | Role `app_public_intake` chỉ-`INSERT` | ✅ CHỐT — [ADR-006 `D6`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) |
| 4 | ⭐ **Đường operator xuyên tenant** trên `public.takedown_request` + `public.project_access_state` (`AS-13`) | ⛔ **CHƯA PIN** — phương án chốt ở [§4.5](#45--trả-lời-td-q1--db-role-và-uỷ-quyền-cho-bề-mặt-operator), cần PM lands ripple `SDD` §7.4 |
| 5 | ⚠️ **Lần ghi đầu tiên dòng `public."user"`** khi chưa có tenant context (`AS-14`) | ⛔ **CHƯA PIN** — **Architect**, [Endpoint-Tenancy](../API/Endpoint-Tenancy.md) `TBD` |

⭐ **Năm điểm này phải nằm trong danh sách review bảo mật cố định** (`C-11`). ⚠️ ⛔ **Một điểm chưa pin ⛔ không được rơi khỏi danh sách chỉ vì nó chưa có cơ chế** — danh sách đếm **bề mặt**, ⛔ không đếm **cơ chế đã hiện thực**.

---

## 3. STRIDE trên bảy luồng `F1`–`F7`

> [!NOTE]
> **Cách đọc bảng**: cột *"Biện pháp"* trỏ tới cơ chế **đã được quyết ở nơi khác** — ⛔ file này không đặc tả lại. Cột *"Còn hở"* là phần **file này khẳng định là chưa được đóng**, và mọi hàng ở đó phải xuất hiện lại ở [§8](#8-bảng-tbd-của-file-này) kèm chủ sở hữu.
> Chữ viết tắt STRIDE: **S**poofing · **T**ampering · **R**epudiation · **I**nformation disclosure · **D**enial of service · **E**levation of privilege.

### 3.1 `F1` — Upload → cam kết quyền → `tenant_id` → opt-out check → `text clean` → tách `Event`

| # | STRIDE | Mối đe doạ | Biện pháp đã có | Còn hở |
|---|:--:|---|---|---|
| `TM-F1-1` | **T**, **E** | ⭐ **Vòng qua kiểm opt-out Điều 37b** bằng một kênh nạp khác (dán text, import lại, re-ingest) ⇒ **phá `KC-6`** | Ingest là **choke point DUY NHẤT**; opt-out check đứng **trước** `text clean`; ⛔ ⛔ **không tồn tại tham số bỏ qua**; đo bằng **100%** file upload, ⛔ không ngoại lệ theo kênh nạp (`SRS-FR-37`) | ⛔ Không — nhưng phải kiểm **mọi** đường nạp mới trong tương lai đều đi qua stage này. `C-1` |
| `TM-F1-2` | **T** | **Client tự đặt key cuối** (chứa `sha256`) ⇒ ghi đè object của chính tenant, hoặc đưa dữ liệu **chưa kiểm** vào vị trí hợp lệ | Upload **hai pha**; `sha256` **chỉ server mới tin được**; ⛔ không đường đọc nào trỏ vào `incoming/` | ⛔ Không |
| `TM-F1-3` | **D** | **File độc hại / quá lớn / nén bung** (zip bomb, chapter khổng lồ) làm cạn CPU–RAM của process `api` | Giới hạn dung lượng/số file là **cơ chế CHỐT** (`SRS-NFR-20`) | ⭐ **Ngưỡng số = `T-10`**. ⛔ File này ⛔ không gán số. `C-6` |
| `TM-F1-4` | **R** | Chối bỏ *"tôi không cam kết quyền"* / *"hệ thống không kiểm opt-out"* | Checkbox cam kết quyền gắn vào **bước upload** (thiếu tick ⇒ upload **bị từ chối**); log opt-out **kèm timestamp kể cả khi *"không có signal"*** | ⛔ Không |
| `TM-F1-5` | **I** | Tên file / metadata của người dùng lọt vào log hoặc vào thông báo lỗi trả về | Kênh log là `stdout`/`stderr` | ⚠️ **Hở** — chưa có quy tắc che nội dung log. `C-4` |
| `TM-F1-6` | **S** | Rác mồ côi trong `incoming/` bị dùng làm điểm đặt dữ liệu chờ | Job dọn dẹp `incoming/` là hạng mục công việc **đã ghi nhận** | ⚠️ Chu kỳ dọn ⛔ chưa có số — cùng nhóm `T-10` |

### 3.2 `F2` — `Event` → LLM phát attribute event → `reduce()` → `state_at(N)`

| # | STRIDE | Mối đe doạ | Biện pháp đã có | Còn hở |
|---|:--:|---|---|---|
| `TM-F2-1` | **T**, **E** | ⭐ **Prompt injection từ bản thảo**: văn bản của người dùng chứa chỉ thị khiến LLM sinh attribute event sai lệch, hoặc cố khiến LLM ghi thẳng vào state | ⭐ ⛔ **Không đường nào cho LLM ghi thẳng vào bảng state**; **đúng một** hàm `resolveState()` (`SRS-FR-05`, `SRS-NFR-10`) | ⚠️ Injection vẫn **làm bẩn dữ liệu** dù không ghi thẳng ⇒ mọi output LLM phải đi qua validate. `C-7` |
| `TM-F2-2` | **I** | Bản thảo `A-1` được **gửi ra provider LLM** — dữ liệu chưa công bố rời khỏi hệ thống | Ranh giới sử dụng LLM ở [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) | ⚠️ Điều khoản *"không dùng dữ liệu để train"* của vendor là **hạng mục phải verify khi mua**, ⛔ file này không xác nhận thay. `C-9` |
| `TM-F2-3` | **R** | Không truy được *"vì sao state ra như vậy"* | `field_provenance` mức **field** + `generation.origin`; `change_log` ghi **mọi** hành động người dùng (`KC-2`, `KC-3`) | ⛔ Không |
| `TM-F2-4` | **D** | Chapter cực dài ⇒ chi phí LLM tăng đột biến | `SRS-NFR-20` cơ chế CHỐT | Ngưỡng = `T-10` |

### 3.3 `F3` — Bible đã duyệt → Director → `page_layout` → panel spec

| # | STRIDE | Mối đe doạ | Biện pháp đã có | Còn hở |
|---|:--:|---|---|---|
| `TM-F3-1` | **T** | Ghi panel **≥4 nhân vật** hoặc panel thiếu `text_safe_zone` để lách ràng buộc hạ nguồn | ⭐ **CHECK constraint ở tầng DB TỪ CHỐI** panel ≥4 nhân vật — ⛔ không phải cảnh báo rồi cho qua (`SRS-FR-08`) | ⛔ Không |
| `TM-F3-2` | **T** | `page_layout JSONB` mang **toạ độ ngoài `0–1`** hoặc **ID trỏ sang tài nguyên của tenant khác** | Toạ độ chuẩn hoá `0–1`; RLS lọc khi đọc | ⭐ **Hở thật** — ID nhúng trong `JSONB` ⛔ **không được FK kiểm**. Chi tiết ở [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) |
| `TM-F3-3` | **E** | LLM tự phân bổ diện tích thay vì chỉ xếp hạng ⇒ ràng buộc quota mất hiệu lực | ⭐ LLM **chỉ xếp hạng** beat, **code phân bổ** theo quota (`SRS-FR-09`) | ⛔ Không |

### 3.4 `F4` — Panel spec → gate 1 speaker → `text_budget` → gate 2 condensation

| # | STRIDE | Mối đe doạ | Biện pháp đã có | Còn hở |
|---|:--:|---|---|---|
| `TM-F4-1` | **E** | ⭐ **Ghi `PASS` bằng máy**: job / LLM / cron / cờ cấu hình / biến môi trường / tham số API | ⭐ `SDD-HG-01.2` — **chỉ hành động CON NGƯỜI** mới chuyển `OPEN → PASS`; `SDD-HG-01.1` — ⛔ không migration/seed nào được ghi `PASS` | ⛔ Không — nhưng phải test, xem `C-2` |
| `TM-F4-2` | **T** | **Reset im lặng**: đổi layout/thoại làm gate rơi về `OPEN` mà người dùng không biết ⇒ họ tin trang vẫn xuất bản được | `SDD-HG-01.5` + hệ quả API #4: endpoint phải **trả về danh sách gate bị reset** | ⛔ Không |
| `TM-F4-3` | **T** | **Ghi đè bản người đã sửa** bằng một lần re-run | `SDD-HG-01.7` — `dialogue_source` **bất biến**; edit của người **khoá lại** khỏi re-run | ⛔ Không |
| `TM-F4-4` | **R** | Chối bỏ *"tôi không duyệt dòng này"* | `SDD-HG-01.6` — mỗi lần `OPEN → PASS` sinh **một** `change_log` row **cùng transaction**; endpoint ghi `PASS` yêu cầu **định danh người dùng thật** | ⛔ Không |
| `TM-F4-5` | **S** | Batch-approve trá hình *"duyệt cả trang"* | ⛔ Cấm batch-approve (`UC-04`); gate ở mức `dialogue_line` | ⛔ Không — điều kiện xuất bản đã có **thêm** một lớp ở tầng DB, xem `TM-F6-1` |

### 3.5 `F5` — Compiler → HOLD credit → enqueue → worker → adapter → N candidate → VLM preselect → người chọn

> ⭐ Luồng dày ràng buộc nhất, và là nơi **tiền thật** bị tiêu.

| # | STRIDE | Mối đe doạ | Biện pháp đã có | Còn hở |
|---|:--:|---|---|---|
| `TM-F5-1` | **E** | ⭐ **Worker claim job của tenant khác** hoặc chạy công việc **ngoài tenant context** | Carve-out **đúng một cặp policy** trên `public.job`; `SET LOCAL` là statement **kế tiếp ngay lập tức**; ⛔ ⛔ **TUYỆT ĐỐI KHÔNG `BYPASSRLS`** | Chi tiết + đường vòng: [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) |
| `TM-F5-2` | **T** | **`usage_event` / `change_log` bị sửa hoặc xoá** để che dấu vết chi phí | ⛔ **REVOKE `UPDATE`, `DELETE`** khỏi **mọi** DB role ứng dụng (`GR-3` của [ADR-017 `Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md)) | ⭐ ⛔ File này ⛔ **không** cấp quyền `UPDATE`/`DELETE` cho role ứng dụng trên hai bảng append-only — đó là hợp đồng trích dẫn của [ADR-017 `Q4.7`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| `TM-F5-3` | **R** | **Artifact tồn tại mà bằng chứng thiếu** ⇒ *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* | ⚠️ **Phát biểu đúng**: tầng DB cưỡng chế **các CỘT** và **tính APPEND-ONLY** (`GR-1`…`GR-5`); **tính NGUYÊN TỬ** được cưỡng chế bằng **kiến trúc 1-DB (`L1`) + middleware (`L2`) + test CI (`L3`)**. ⛔ **Đừng viết *"tầng DB cưỡng chế `KC-4`"*** | Thứ tự gắn `usage_event` / `cost_usd` trong vòng đời job = `P-7`, **Architect lô DB Schema** |
| `TM-F5-4` | **D** | ⭐ **Một tenant chiếm hết worker** ⇒ DoS chéo tenant | Điều kiện `in_flight_per_tenant < N` **nằm trong chính câu CLAIM** — ⛔ nhồi vào sau là sửa đúng câu SQL nóng nhất | ⭐ **`N` = `T-6`**. ⚠️ Và ⚠️ subquery đếm **cũng đi qua RLS** ⇒ nếu policy hẹp quá thì phép đếm luôn `0` và điều kiện **không bao giờ ràng buộc** — hỏng **im lặng** |
| `TM-F5-5` | **D**, **T** | ⭐ **Đốt ngân sách provider** (`A-10`) bằng cách spam `generate`/`regenerate` | Rate limit per tenant — **cơ chế CHỐT** (`SRS-NFR-20`) | ⭐ Ngưỡng = `T-10`; và ở **MVP1–MVP2 ⛔ không có HOLD credit** để chặn ⇒ **rate limit là biện pháp DUY NHẤT còn hiệu lực**. ✅ `T-25` **đã đóng**: Founder chọn **chỉ rate limit**, ⛔ không hard quota (`E9`) |
| `TM-F5-6` | **T** | **Đếm trùng chi phí** khi job chạy lại (queue là **at-least-once**) | Mỗi `usage_event` mang **idempotency key** ⇒ `usage_daily` chỉ tính **một** lần | Hình dạng key = `P-7`, lô DB Schema |
| `TM-F5-7` | **S** | **Provider tự fallback sang model khác** mà hệ thống vẫn ghi model dự kiến ⇒ hồ sơ audit sai | `model_id` là model **THỰC SỰ được gọi**; `model_version` ghi **riêng biệt**, ⛔ không ghi đè — dữ liệu để truy **silent model drift** | ⛔ Không |
| `TM-F5-8` | **T**, **E** | **Bytes ảnh / JSON từ provider là dữ liệu KHÔNG TIN CẬY** (`AS-8`): ảnh dị dạng làm nổ thư viện xử lý, JSON điểm số VLM làm lệch preselect | ⭐ VLM **chỉ preselect**, `[Fix automatically]` bị **cắt hẳn**, **người chọn** (`SRS-FR-21`) ⇒ một điểm số bị thao túng ⛔ không tự động thành kết quả | ⚠️ **Hở**: chưa có ràng buộc nào về **parse an toàn** dữ liệu trả về. `C-8` |
| `TM-F5-9` | **I** | Prompt đã compile + reference sheet đi ra provider ⇒ `A-1`, `A-4` rời hệ thống | `AS-7` chỉ qua adapter | Cùng nhóm `TM-F2-2` — `C-9` |
| `TM-F5-10` | **E** | **SSRF qua adapter**: một trường do người dùng kiểm soát trở thành URL/endpoint mà hệ thống gọi ra | Adapter chỉ nói chuyện với **tập con S3 API** / endpoint provider **cấu hình cố định** | ⚠️ **Hở về nguyên tắc** — phải phát biểu thành guardrail. `C-8` |

### 3.6 `F6` — Ảnh đã chọn + typeset layer → compositor → preview → export PDF + watermark

| # | STRIDE | Mối đe doạ | Biện pháp đã có | Còn hở |
|---|:--:|---|---|---|
| `TM-F6-1` | **E** | ⭐ **Export CHÍNH LÀ đường bypass** nếu nó không kiểm hai gate | ⭐ `SDD-HG-01.4` — kiểm **ở tầng server**, qua **đúng một** hàm dùng chung; ⛔ không `force`, ⛔ không `skip_gates`, ⛔ không `admin_override`; ⛔ không dựa vào việc UI ẩn nút. ⭐ **Hàng `P-2` ĐÃ ĐÓNG**: có **thêm** một lớp ở tầng DB — trigger trên `comic.export_artifact` gọi **đúng một** vị từ SQL dùng chung với tầng service ⇒ ⛔ không sinh nguồn sự thật thứ hai ([DB-Entity-Preview-And-Export](../Schema/DB-Entity-Preview-And-Export.md)) | ⛔ Không |
| `TM-F6-2` | **E** | **Export/preview một project đang bị disable-access do takedown** | `SDD-HG-01.4` gộp **cả hai** điều kiện: gate PASS **VÀ** project không disable-access | ⚠️ **Preview ⛔ KHÔNG bị chặn bởi gate** (đúng thiết kế) — nhưng **phải** bị chặn bởi disable-access. Ranh giới này ⛔ không được đọc lẫn |
| `TM-F6-3` | **E**, **D** | ⭐ **Compositor xử lý dữ liệu không tin cậy**: thoại/tên nhân vật/tên file do người dùng nhập được render thành PDF. Nếu compositor dựa trên HTML/SVG ⇒ **injection**, đọc file cục bộ, hoặc treo tài nguyên | ⛔ Chưa có ràng buộc nào — [ADR-013](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) chốt *tách layer*, ⛔ không chốt an toàn render | ⭐ **Hở thật, mức cao.** `C-10` |
| `TM-F6-4` | **I** | ⭐ **Signed URL bị nhúng vào file export** ⇒ file phát tán mang theo quyền đọc | ⭐ [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3 — ⛔ không nhúng vào file export | ⛔ Không — nhưng cần test CI, `C-4` |
| `TM-F6-5` | **T** | **Bỏ qua stage nhúng watermark máy đọc** (`L-5`) | Watermark là **stage bắt buộc trong export pipeline**; thiết kế theo **diễn giải RỘNG** cho tới khi luật sư chốt | ⚠️ SynthID có thoả nghĩa vụ không = `T-21`; đường lui *"tự nhúng"* **chi phí chưa ước lượng** |
| `TM-F6-6` | **T** | Ảnh sinh ra **có chữ trong pixel** ⇒ typeset không tách được, sửa thoại phải sinh lại ảnh | Art sinh ra ⛔ **không có chữ** (`SRS-FR-11`); typeset render **bằng code**, ⛔ không tiêu credit sinh ảnh | ⛔ Không |

### 3.7 `F7` — Takedown công khai → timestamp tiếp nhận → soft-delete + disable-access trong 72h

| # | STRIDE | Mối đe doạ | Biện pháp đã có | Còn hở |
|---|:--:|---|---|---|
| `TM-F7-1` | **S**, **T** | ⭐ **Takedown giả mạo làm vũ khí DoS**: bất kỳ ai cũng nộp được đơn nhắm vào project của một tenant | ⭐ Bước 4 là **người đánh giá** (founder ở vai operator), ⛔ không phải tự động hạ nội dung | ⭐ **Hở về vận hành**: ⛔ không có yêu cầu xác minh danh tính người nộp; và ⛔ **chưa có** quy trình thông báo cho tenant bị nhắm (`T-29`) ⇒ ⛔ counter-notice ⛔ chưa có đường tồn tại |
| `TM-F7-2` | **D** | **Spam / flood endpoint công khai** (`AS-2`) làm ngập bảng `takedown_request` và che đơn thật | `SRS-NFR-20` cơ chế CHỐT | ⭐ Ngưỡng = `T-10`; ⚠️ ⛔ **không được** dùng rate limit chặt tới mức làm **mất một đơn hợp lệ** — mất đơn là mất chính điều kiện miễn trừ. Cân bằng này ⛔ chưa ai quyết |
| `TM-F7-3` | **E** | Bề mặt công khai được nới quyền *"cho tiện tra cứu"* | ⛔ Role `app_public_intake` **chỉ** `INSERT`; ⛔ ⛔ không `SELECT` bảng nghiệp vụ nào; ⛔ không giải bằng bypass RLS | ⛔ Không |
| `TM-F7-4` | **R** | Tranh chấp *"các anh nhận đơn lúc nào"* ⇒ ⛔ không chứng minh được **SLA 72 giờ** | ⭐ **Timestamp tiếp nhận do HỆ THỐNG ghi**, đứng **TRƯỚC** bước hạ nội dung | ⛔ Không |
| `TM-F7-5` | **T** | ⭐ **Dùng hard-delete để làm takedown** ⇒ **phá mất bằng chứng counter-notice** | ⭐ Takedown = **soft-delete + disable-access cấp project**, ⛔ **KHÔNG hard delete**; hai đường xoá **TÁCH BIỆT** (`D7` của [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md)) | ⚠️ Giữ bao lâu = `T-23` (`b-3`) |
| `TM-F7-6` | **I** | ⭐ **Dữ liệu cá nhân của người nộp đơn** (`A-9`) bị lộ qua thông báo cho tenant, qua log, hoặc qua màn hình vận hành | ⚠️ **Đóng ĐÚNG MỘT trong ba chân**: chân **log** ⇒ `C-4` nay kê tường minh `requester_email`, `requester_phone` vào danh sách trường phải che. ⛔ Hai chân còn lại — **thông báo cho tenant** và **màn hình vận hành** — ⛔ **chưa có ràng buộc nào** | ⭐ **Vẫn hở ở hai chân**: thông báo cho tenant = `T-29`; nghĩa vụ áp cho `A-9` = `b-4` (`T-24`). ⚠️ Màn hình vận hành nay có hình dạng bề mặt (`AS-13`) nhưng ⛔ chưa có cơ chế uỷ quyền — `C-13`. ⛔ Security Auditor ⛔ **không đóng** hai chân đó — quyết định pháp lý |
| `TM-F7-7` | **T** | Cờ disable-access **không được kiểm ở một đường đọc nào đó** ⇒ nội dung đã hạ vẫn tải được | Cờ trạng thái cấp project phải được kiểm ở **MỌI** đường đọc và export; gộp vào `SDD-HG-01.4`; khuôn triển khai = `API-PRJ-4` của [Endpoint-Project](../API/Endpoint-Project.md) | ✅ **Danh sách *"mọi đường đọc"* nay ĐÃ ĐÓNG** ở [§4.4](#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access). ✅ **Và việc ÁP nay cũng XONG** (lô `L37`): 4 file Nhóm B + `Endpoint-Generation.md` đã mang `403 PROJECT_ACCESS_DISABLED`, kèm invariant `API-BT-8` · `API-PL-13` · `API-PS-12` · `API-HG-13` · `API-GEN-19/20`. ⚠️ **Còn lại là việc HIỆN THỰC**: test bảng route toàn cục khuôn `M1-1` (`C3-K4`) — ⛔ chưa tồn tại, thuộc Phase 4 |
| `TM-F7-8` | ⭐ **E**, **I** | ⭐⭐ **Bề mặt operator `AS-13` là đường ĐỌC + GHI XUYÊN TENANT duy nhất của tầng HTTP.** `TD-2` `SELECT` toàn bảng `public.takedown_request` (⛔ không `tenant_id` ⇒ ⛔ không RLS nào lọc); `TD-3` `UPDATE` `access_state` của project **bất kỳ tenant nào**. Ai chiếm được một phiên operator ⇒ **đọc `A-9` của mọi đơn** và **hạ nội dung của mọi tenant** | ⛔⛔ **CHƯA CÓ.** [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md) ghi thẳng: DB role **CHƯA PIN**, uỷ quyền operator **CHƯA CÓ CƠ CHẾ**. ⚠️ `C-11` ở dạng cũ ⛔ **không bắt được** bề mặt này vì nó cưỡng chế bằng đối chiếu `pg_policies` — mà đặc quyền này sống **một nửa ở tầng ứng dụng** | ⭐ **Hở, mức CAO.** Phương án chốt: [§4.5](#45--trả-lời-td-q1--db-role-và-uỷ-quyền-cho-bề-mặt-operator) + `C-13`. ⛔ `TD-2`/`TD-3` ⛔ **không được triển khai** trước khi PM lands ripple `SDD` §7.4 |
| `TM-F7-9` | **E** | ⚠️ **Đường lui "cho tiện"**: chạy `TD-2`/`TD-3` dưới **role owner/migration** vì nó "đã có sẵn quyền" | ⛔ Chưa có ràng buộc nào ở tầng cưỡng chế — [§4.5](#45--trả-lời-td-q1--db-role-và-uỷ-quyền-cho-bề-mặt-operator) **LOẠI** phương án này bằng lập luận, ⛔ chưa bằng test | ⭐ **Hở cho tới khi có test CI**: *"⛔ không connection string nào của process `api` trỏ tới role owner"* — xem [§4.3](#43-ma-trận-cưỡng-chế--biến-biện-pháp-thành-thứ-ci-kiểm-được) |

---

## 4. Biện pháp

### 4.1 Biện pháp đã có chủ — file này chỉ TRỎ, ⛔ không đặc tả lại

| Biện pháp | Nguồn duy nhất | Mối đe doạ nó đóng |
|---|---|---|
| `tenant_id` + RLS + `SET LOCAL app.current_tenant` | [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md), [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | `TM-F5-1`, và toàn bộ [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) |
| Hai human gate không bypass được | [`SDD-HG-01`](../Architecture/SDD-Comic-Studio.md) — ⭐ **nguồn duy nhất** | `TM-F4-1`…`TM-F4-5`, `TM-F6-1`, `TM-F6-2` |
| Một-transaction-boundary + append-only | [ADR-017 `Q4`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md), [ADR-018 `Q1`, `Q3`](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md) | `TM-F5-2`, `TM-F5-3`, `TM-F5-6` |
| Signed URL: không public bucket · không lưu bền · TTL một hằng số · client coi hết hạn là **bình thường** | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 2–5 | `TM-F6-4`, `AS-4` |
| Upload hai pha + `incoming/` | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 7 | `TM-F1-2` |
| ⛔ Cấm `DeleteObject` cho `api`/`worker` trên prefix canonical + bucket versioning | [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 8 | Bảo vệ `A-2`, `A-3` khỏi lỗi lập trình |
| JWT qua JWKS · claim ⛔ **không bao giờ** là nguồn sự thật của `tenant_id`/role · webhook có inbox + idempotency | [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 3, 4, 6 | `AS-1`, `AS-5` |
| Bốn DB role tách bạch, ⛔ role ứng dụng không có DDL | [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md), [ADR-006 `D7`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | `AS-11` |
| Cấu hình **chỉ** qua biến môi trường; log ra `stdout`/`stderr` | [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) điều 6 | `A-5` (một phần — `b-1` vẫn mở) |

### 4.2 Biện pháp file này CHỐT — phần chưa ai viết

> ⚠️ Mỗi biện pháp dưới đây được phát biểu ở mức **cơ chế + ràng buộc lên tham số tương lai**, ⛔ **không kèm con số** — đúng khuôn `TTL` của [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md).

| # | Biện pháp | Nội dung chuẩn tắc | Đóng mối đe doạ |
|---|---|---|---|
| **`C-1`** | **Opt-out check là stage, ⛔ không phải hàm tiện ích** | Mọi đường đưa nội dung mới của người dùng vào hệ thống — hiện tại và **tương lai** — phải đi qua **cùng một** stage kiểm opt-out. Thêm một kênh nạp mà không đi qua stage đó là **phá `KC-6`**, ⛔ không phải một thiếu sót nhỏ | `TM-F1-1` |
| **`C-2`** | **Guardrail phải là thứ MÁY cưỡng chế được** (`R-1`) | Mọi biện pháp trong file này phải quy về **một trong ba**: ràng buộc/quyền ở tầng DB · lint rule ở CI · test tự động. ⛔ Một biện pháp chỉ tồn tại dưới dạng *"quy ước"* thì trong repo này coi như **không tồn tại** — vì đội **1 người, ⛔ không có code review** | Toàn bộ §3 |
| **`C-3`** | **Kiểm disable-access ở MỌI đường đọc — qua đúng một hàm** | Cùng khuôn với `SDD-HG-01.4`: **đúng một** hàm dùng chung; lint rule chặn mọi đường khác. ✅ **Danh sách *"mọi đường đọc"* ĐÃ ĐÓNG** — [§4.4](#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access) — ✅ **và đã ÁP xong vào tầng API** (lô `L37`). ⚠️ `C-3` nay ⛔ **không còn là lời hứa** ở tầng đặc tả; phần còn lại là **hiện thực test `M1-1`** ở Phase 4 | `TM-F7-7`, `TM-F6-2` |
| **`C-4`** | ⭐ **Quy tắc che trong logger** | ⛔ **Cấm** để lọt vào `stdout`/`stderr`: signed URL (đầy đủ hoặc phần chữ ký) · connection string · API key provider · token của vendor auth · **nội dung bản thảo** và thoại của người dùng · ⭐ **`A-9` — `requester_email` và `requester_phone` của người nộp takedown** (`SRS-FR-38`). ⚠️ **`A-9` là hàng dễ rơi nhất**: nó ⛔ **không** phải nội dung của tenant nào, nên một quy tắc che viết theo khuôn *"che dữ liệu tenant"* sẽ **bỏ sót nó**. [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md) **đang viện dẫn `C-4`** để cấm hai trường này lọt vào log ⇒ chúng **phải có tên trong danh sách này**. Cưỡng chế: **test CI** grep output log của bộ test tích hợp. ⚠️ [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) điều 3 **đã yêu cầu** *"phải có quy tắc che trong logger"* — mục này là chỗ nó được phát biểu | `TM-F1-5`, `TM-F6-4`, `TM-F7-6` *(⭐ chỉ chân **log**; hai chân còn lại vẫn hở — xem [§3.7](#37-f7--takedown-công-khai--timestamp-tiếp-nhận--soft-delete--disable-access-trong-72h))* |
| **`C-5`** | **Thông báo lỗi ⛔ không được phân biệt *"không tồn tại"* với *"không thuộc về bạn"*** | RLS làm mọi truy vấn sai tenant trả **0 row**. Tầng API ⛔ **không được** biến sự khác biệt đó thành hai mã lỗi khác nhau — đó là một **oracle** cho phép dò sự tồn tại của tài nguyên tenant khác | Bổ trợ `TM-F5-1` |
| **`C-6`** | **Abuse controls tối thiểu** — cơ chế CHỐT, ⛔ ngưỡng số mở | Ba thành phần bắt buộc (`SRS-NFR-20`): (a) **rate limit per tenant** · (b) **giới hạn dung lượng/số file upload** · (c) ⭐ **ghi lại MỌI lần provider từ chối vì content policy**. ⛔ Ràng buộc lên con số tương lai: rate limit của `generate` **đếm SỐ REQUEST**, ⛔ **không đếm tiền**; áp **per tenant**, ⛔ không per user; ⛔ **không** HOLD credit ở MVP1–MVP2. ⚠️ Với `AS-2` (takedown), ngưỡng ⛔ **không được** chặt tới mức làm **mất một đơn hợp lệ**. ⭐⭐ **HAI ĐIỀU KIỆN TIÊN QUYẾT — xem khối cảnh báo ngay dưới bảng này** | `TM-F1-3`, `TM-F2-4`, `TM-F5-5`, `TM-F7-2` |
| **`C-7`** | **Output của LLM là dữ liệu ĐỀ XUẤT, ⛔ không phải lệnh** | Đã có ở tầng kiến trúc: LLM ⛔ không ghi thẳng state (`F2`), LLM **chỉ xếp hạng** (`F3`), LLM bị **constrained** vào tập nhân vật có mặt trong scene (gate 1). ⇒ Quy tắc chung: mọi output LLM/VLM phải được **validate theo schema** trước khi chạm DB; giá trị ngoài miền ⇒ **từ chối**, ⛔ không *"chuẩn hoá cho gần đúng"*. `unclear` là câu trả lời **hợp lệ hạng nhất** | `TM-F2-1`, `TM-F5-8` |
| **`C-8`** | **Ranh giới egress/ingress của adapter** | (a) Endpoint provider và endpoint storage đến **chỉ** từ **cấu hình** (biến môi trường), ⛔ **không bao giờ** từ dữ liệu người dùng hoặc từ response của provider ⇒ ⛔ không có đường SSRF. (b) Bytes ảnh và JSON trả về là **dữ liệu không tin cậy**: giới hạn kích thước, kiểm định dạng trước khi decode, ⛔ không dùng kết quả parse để quyết định đường code đặc quyền | `TM-F5-8`, `TM-F5-10` |
| **`C-9`** | **Điều khoản dữ liệu của provider là hạng mục PHẢI VERIFY khi mua** | Với mỗi vendor (auth, storage, image, VLM, LLM, billing): xác nhận **bằng văn bản** điều khoản về *"không dùng dữ liệu khách để train"* và về vị trí lưu trữ. ⛔ File này ⛔ **không xác nhận thay**, và ⛔ **không dán tên/giá vendor**. ⚠️ Liên đới `T-22` | `TM-F2-2`, `TM-F5-9` |
| **`C-10`** | ⭐ **Compositor render dữ liệu không tin cậy — phải chọn cơ chế AN TOÀN, ⛔ không chọn cơ chế TIỆN** | Compositor dùng chung cho preview và export nhận **văn bản do người dùng nhập**. Ràng buộc lên lựa chọn kỹ thuật tương lai: ⛔ **không** render qua một engine cho phép nạp tài nguyên ngoài (remote URL, file cục bộ, entity ngoài); ⛔ **không** để chuỗi người dùng đi vào ngữ cảnh có thể thực thi; có **trần tài nguyên** (kích thước trang, số panel, thời gian render). ⚠️ ⛔ Chưa chọn được cơ chế cụ thể — ⛔ **không phải** vì `SRS-NFR-09`: [ADR-001](../Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) **đã đóng việc chọn ngôn ngữ/framework**. Cái còn mở là `ADR-001` §`TBD`: **thư viện compositor + sinh PDF** và **compositor chạy trong `worker_threads` hay tách hẳn thành job** — ba ràng buộc trên là thuộc tính của **engine cụ thể**, ⛔ không phải của *ngôn ngữ*. ⇒ **Tập ràng buộc: Architect — đã CHỐT ngay tại hàng này, ⛔ không cần làm lại** · **Chọn thư viện: Dev, tại spike MVP0**, nghiệm thu bằng chính ba ràng buộc trên, trước khi compositor đầu tiên chạy | `TM-F6-3` |
| **`C-11`** | **NĂM bề mặt đặc quyền là danh sách REVIEW CỐ ĐỊNH** | Hàm `SECURITY DEFINER` phân giải `user → tenant` · cặp policy carve-out trên `public.job` · role `app_public_intake` · ⭐ **đường operator xuyên tenant `AS-13`** · ⚠️ **lần ghi đầu `public."user"` `AS-14`**. Mọi thay đổi chạm năm điểm này phải được review như **code bảo mật**, và danh sách policy phải được **đối chiếu với hằng số trong repo ở CI**. ⭐⭐ **Ràng buộc mới, ⛔ không được bỏ**: phép đối chiếu `pg_policies` **chỉ nhìn thấy đặc quyền sống ở tầng DB** ⇒ nó **MÙ** với hai điểm 4–5, vì đặc quyền của chúng nằm **một nửa (hoặc toàn bộ) ở tầng ứng dụng**. ⇒ Danh sách phải được cưỡng chế bằng **HAI** phép kiểm chạy song song: (i) `pg_policies` + `pg_roles` vs hằng số repo *(tầng DB)*; (ii) `C-13` — **registry đặc quyền tầng ứng dụng** vs hằng số repo. ⛔ Chỉ có (i) là **tự tuyên bố an toàn dựa trên một phép đo mù** | `AS-2`, `AS-9`, `AS-13`, `AS-14`, `TM-F5-1`, `TM-F7-8` |
| **`C-12`** | **Seam BYOK: ⛔ không có key nào được lưu cho tới khi `b-2` đóng** | `A-6` là hạng mục rủi ro cao nhất; `T-27` nay có chủ (**Architect + Founder**, `E22`) nhưng ⛔ **chưa đóng** — cần một ADR mới. ⇒ Ràng buộc tạm thời **vẫn nguyên hiệu lực**: ⛔ **cấm** ghi bất kỳ credential nào của khách vào DB hoặc log trước khi có requirement nguồn. Seam vẫn phải tồn tại về **hình dạng** (`SRS-FR-32` cấm retrofit), nhưng ⛔ **không hiện thực** | `A-6` |
| **`C-13`** | ⭐⭐ **Đặc quyền ở TẦNG ỨNG DỤNG phải là một REGISTRY đếm được, ⛔ không phải một điều kiện `if` rải rác** | Sinh ra vì `C-11` (đối chiếu `pg_policies`) **mù** với đặc quyền tầng ứng dụng — mà `AS-13` chính là loại đó. Bốn ràng buộc chuẩn tắc: **(a)** ⭐ Mọi route mang đặc quyền **vượt ra ngoài một tenant** phải đi qua **ĐÚNG MỘT** hàm uỷ quyền dùng chung — cùng khuôn `API-PRJ-4` và `SDD-HG-01.4`. **(b)** ⭐ Danh sách các route đó là **HẰNG SỐ trong repo**; **lint rule**: mọi route dưới tiền tố quản trị mà ⛔ không gọi hàm đó ⇒ **CI đỏ**; mọi route **có** gọi hàm đó mà ⛔ không có tên trong hằng số ⇒ **CI đỏ**. ⭐ Hai chiều, ⛔ không một chiều — một chiều chỉ bắt được lỗi quên, ⛔ không bắt được lỗi **thêm lén**. **(c)** ⛔ **Danh tính operator ⛔ KHÔNG BAO GIỜ đến từ claim của vendor auth** — cùng lập luận `BP-10`/`IC-9` của [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md): quyền neo vào **trạng thái hiện tại**, ⛔ không vào một bản sao đã ký. **(d)** ⛔ **Operator ⛔ không phải một cấp của `membership`** — trộn hai thứ biến một tenant admin thành người xem được đơn của tenant khác | `AS-13`, `TM-F7-8`, `TM-F7-9`, `TM-F7-6` *(chân màn hình vận hành)* |

> [!CAUTION]
> ### ⭐⭐ Hai điều kiện tiên quyết của `C-6` — ⛔ chưa được ghi ở bất kỳ đâu trước mục này
>
> `C-6` tự gọi mình là *"biện pháp DUY NHẤT còn hiệu lực"* chống lạm dụng chi phí ở MVP1–MVP2 (`A-10`, `KC-7` là `[OoH]` MVP3). ⭐ **Một biện pháp duy nhất thì mọi điều kiện nó đứng trên đều là điều kiện của cả hệ thống** — nên chúng phải có tên.
>
> **`C-6-PRE-1`** — ⭐ **Rate limit hiện có hiệu lực CHỈ VÌ hệ thống chạy đúng MỘT tiến trình.**
> `RL-1` ([DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md)) chốt state của rate limit là **bộ đếm trong tiến trình**, ⛔ **không** lưu bền ở DB. Nó là bộ đếm **toàn cục** đúng chừng nào `D-01` (modular monolith, `SRS-NFR-02`) còn giữ **1 process**.
> ⚠️ ⛔ **Với N tiến trình, mỗi tiến trình chỉ thấy ~1/N lưu lượng ⇒ ngưỡng thực tế PHỒNG LÊN N LẦN mà ⛔ KHÔNG một lỗi nào được báo.** Đây là **hỏng im lặng**, cùng lớp với `TM-F5-4` và với `BP-2` của [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md).
> ⇒ ⭐ **Ràng buộc thường trực**: bất kỳ thay đổi nào làm hệ thống chạy **>1 tiến trình `api`** — scale-out ngang, thêm replica, thêm region — **PHẢI mở lại `RL-1` bằng một ADR mới TRƯỚC khi bật**, ⛔ không phải sau. ⛔ Đây ⛔ **không** phải một hạng mục hiệu năng; đối với `A-10` nó là **mất luôn biện pháp phòng thủ duy nhất**.
> ⇒ ⭐ **Cưỡng chế đề xuất** (⛔ không phải một con số): một phép kiểm khởi động **khẳng định số tiến trình `api` = 1**, và ⛔ **fail-closed** — ⛔ không log cảnh báo rồi chạy tiếp. Ai đóng: **Dev**, cùng `T-16`/`b-7`.
>
> **`C-6-PRE-2`** — ⭐ **`TD-1` (bề mặt CÔNG KHAI duy nhất) ⛔ CHƯA CÓ HÌNH DẠNG KHOÁ để rate limit theo.**
> Khoá đếm của `RL-1` là **`(tenant_id, action)`**. Nhưng `AS-2`/`TD-1` ⛔ **không có `tenant_id`** — đó là ngoại lệ **đã được duyệt** của mô hình (`BP-14`).
> ⇒ ⚠️ ⛔ **Đây là thiếu CƠ CHẾ, ⛔ KHÔNG phải thiếu NGƯỠNG.** ⛔ **Đừng** ghi nó vào `T-10` rồi coi như đã có chủ: `T-10` là *"chọn con số"*, và ⛔ **không có con số nào gán được cho một khoá chưa tồn tại**. Ghi nhầm nó thành `T-10` là cách hàng này biến mất.
> ⇒ ⭐ **Ràng buộc lên cơ chế tương lai** *(⛔ không chọn thay Architect)*: khoá phải là thứ **hệ thống tự quan sát được**, ⛔ **không** lấy từ trường do người gửi tự khai (`requester_email`, `requester_phone` — chính là `A-9`; lấy chúng làm khoá vừa **vô dụng** vì bịa được, vừa **biến `A-9` thành khoá index sống lâu**, đẩy ngược vào `T-24`). Và ⚠️ **ràng buộc ngược của `TM-F7-2` vẫn nguyên hiệu lực**: ⛔ **không được** chặt tới mức làm **mất một đơn hợp lệ** — mất đơn là mất chính điều kiện miễn trừ.
> ⇒ Ai đóng: **Architect + PM**, cùng `TD-Q5` của [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md). ⭐ **Trước** khi công cụ takedown chạy thật.

### 4.3 Ma trận cưỡng chế — biến biện pháp thành thứ CI kiểm được

| Biện pháp | Cưỡng chế bằng | Trạng thái |
|---|---|---|
| `C-1` | Test: mọi đường nạp nội dung mới ⇒ có row `story.ingest_check` kèm timestamp, **kể cả khi không có signal** | Cần viết ở lô API |
| `C-3` | Lint rule: mọi đường sinh `export_artifact`/đường đọc đi qua đúng một hàm. ⭐ **Cộng thêm — test bảng route toàn cục**: seed một project `disabled_by_takedown`, duyệt **toàn bộ route table**, mọi route ⛔ **không** có tên trong allowlist miễn kiểm ⇒ phải trả `403 PROJECT_ACCESS_DISABLED`. ⛔ **Đừng viết test per-endpoint** — khuôn `M1-1`: route mới quên kiểm cờ thì CI **phải đỏ mà ⛔ không ai phải nhớ thêm test** | ✅ **Danh sách đã đóng** ([§4.4](#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access)); ⛔ **việc ÁP** cần một lô do PM giao |
| `C-4` | Test CI: grep output log của bộ test tích hợp cho mẫu signed URL / khoá / token | ⭐ **Chưa có** — file này chốt yêu cầu |
| `C-5` | Test: request tài nguyên của tenant khác và tài nguyên không tồn tại ⇒ **cùng một** phản hồi | ⭐ **Chưa có** |
| `C-6` | Test: vượt ngưỡng ⇒ bị từ chối (chạy được **sau khi** `T-10` đóng); test: mọi lần provider từ chối ⇒ có row `generation.provider_refusal_log` | Một phần chạy được ngay (thành phần (c)) |
| `C-7` | Test: output LLM sai schema ⇒ **từ chối**, ⛔ không ghi DB | Cần viết ở lô API |
| `C-8` | Test cấu hình: endpoint provider đọc từ env; lint: ⛔ không có lời gọi HTTP nào lấy URL từ dữ liệu | Cần viết ở lô API |
| `C-4` *(chân `A-9`)* | Test CI: grep output log tìm mẫu email và mẫu số điện thoại sinh ra từ fixture của `TD-1`/`TD-2` | ⭐ **Chưa có** — mục này chốt yêu cầu |
| `C-11` *(tầng DB — điểm 1–3)* | Test CI: đối chiếu `pg_policies` với hằng số trong repo (`W-2` của [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md)) | Đã có chủ ở ADR-006. ⚠️ **MÙ với điểm 4–5** |
| `C-11` *(tầng ứng dụng — điểm 4–5)* | ⭐ Test CI: registry đặc quyền tầng ứng dụng khớp **hằng số trong repo**, **hai chiều** (`C-13b`) | ⭐ **Chưa có** — mục này chốt yêu cầu |
| `C-13` | Lint CI: mọi route quản trị đi qua **đúng một** hàm uỷ quyền operator; test: request có định danh tenant hợp lệ nhưng ⛔ không phải operator ⇒ `403`; test: ⛔ ⛔ **không** connection string nào của process `api` trỏ tới **role owner** (chặn `TM-F7-9`) | ⭐ **Chưa có** — ⛔ chạy được **sau khi** PM lands ripple `SDD` §7.4 |

---

### 4.4 ⭐ `C-3` DANH SÁCH ĐÓNG các đường đọc phải kiểm cờ disable-access

> [!CAUTION]
> ⭐⭐ **`C-3` cho tới mục này vẫn là một LỜI HỨA, và lời hứa đó đang hở thật.**
> `TM-F7-7` ghi *"danh sách 'mọi đường đọc' phải đóng ở **lô API**"*. **Lô API đã chạy xong**, và **bốn** file `Endpoint-*` ⛔ **KHÔNG hề nhắc** `access_state` / `PROJECT_ACCESS_DISABLED`: `Endpoint-Page-Layout.md` · `Endpoint-Bubble-Typeset.md` · `Endpoint-Panel-Script.md` · `Endpoint-Human-Gates.md`.
> ⇒ ⚠️ **Theo đặc tả hiện tại, nội dung đã bị takedown VẪN ĐỌC ĐƯỢC** qua các endpoint đó — đúng nguyên văn mối đe doạ `TM-F7-7`, và nó chạm thẳng điều kiện miễn trừ Điều 198b (`L-4`).
> ⇒ **Mục này ĐÓNG danh sách.** ⛔ File này ⛔ **không sửa một dòng nào** của `docs/030-Specs/API/**` — việc **áp** thuộc một lô do PM giao.

**Khuôn đã có, ⛔ không phát minh lại**: `API-PRJ-4` của [Endpoint-Project](../API/Endpoint-Project.md) đã phát biểu quy tắc — *"mọi endpoint đọc/ghi NỘI DUNG trong phạm vi project kiểm `access_state`; `disabled_by_takedown` ⇒ `403 PROJECT_ACCESS_DISABLED`, qua **đúng một** hàm dùng chung ở tầng service"*. Danh sách dưới đây là **phần liệt kê** mà quy tắc đó đang thiếu.

#### Nhóm A — ĐÃ tuyên bố kiểm ⇒ chỉ cần **giữ**, ⛔ không phải việc mới

| File | Đường phải kiểm |
|---|---|
| `Endpoint-Project.md` | `GET /v1/projects` · `PATCH /v1/projects/{project_id}` |
| `Endpoint-Story-Bible.md` | `SB-1` … `SB-8` — **cả tám** |
| `Endpoint-Chapter-Ingest.md` | `CH-1` … `CH-5` — **cả năm** |
| `Endpoint-Timeline-Event.md` | `TE-1` … `TE-4` — **cả bốn** |
| `Endpoint-Preview-Export.md` | `E-PE-1` … `E-PE-5` — **cả năm**, gồm cả **preview** (⭐ preview miễn *gate*, ⛔ **không** miễn disable-access) |

#### Nhóm B — ⛔ CHƯA hề nhắc `access_state` ⇒ ⭐ **LỖ HỔNG ĐANG MỞ, phải áp**

| File | Đường phải kiểm — ⭐ **thêm `403 PROJECT_ACCESS_DISABLED`** |
|---|---|
| ⭐ `Endpoint-Page-Layout.md` | `GET /v1/pages/{page_id}/layout` · `POST /v1/pages/{page_id}/layout:apply-template` · `POST /v1/pages/{page_id}/panels:swap` · `POST /v1/pages/{page_id}/panels:reorder` · `GET /v1/pages/{page_id}/emphasis-suggestion` |
| ⭐ `Endpoint-Panel-Script.md` | `POST /v1/chapters/{chapter_id}/panel-script:generate` · `GET /v1/chapters/{chapter_id}/pages` · `GET /v1/panels/{panel_id}` · `PATCH /v1/panels/{panel_id}` · `POST /v1/panels/{panel_id}:split` · `POST /v1/pages/{page_id}/panels:merge` · `POST /v1/chapters/{chapter_id}/panel-script:approve` |
| ⭐ `Endpoint-Bubble-Typeset.md` | `E-BT-1` … `E-BT-5` — **cả năm** |
| ⭐ `Endpoint-Human-Gates.md` | `GET /v1/panels/{panel_id}/dialogue-lines` · `PATCH /v1/dialogue-lines/{id}/speaker` · `POST /v1/panels/{panel_id}/dialogue:condense` · `PATCH /v1/dialogue-lines/{id}/rendered` · `POST /v1/dialogue-lines/{id}/gates/{gate_kind}:pass` · `GET /v1/pages/{page_id}/gate-status` |
| ⚠️ `Endpoint-Generation.md` — **phủ MỘT PHẦN** | ✅ đã có: `GET /v1/generations/{generation_id}/image-url`. ⛔ **thiếu**: `POST /v1/panels/{panel_id}/generations` · `GET /v1/panels/{panel_id}/generations` · `GET /v1/generations/{generation_id}` · `PUT /v1/panels/{panel_id}/approved-generation` · `GET /v1/jobs/{job_id}` · `GET /v1/panels/{panel_id}/jobs` |

⚠️ **Phủ một phần nguy hiểm hơn ⛔ không phủ**: nó tạo cảm giác *"file này đã lo rồi"*. `GET /v1/generations/{generation_id}` trả `GenerationDetail` — tức **prompt đã compile + đánh giá VLM của nội dung đã bị hạ**.

#### Nhóm C — ⛔ KHÔNG kiểm, **có lý do** ⇒ đây là **allowlist miễn kiểm, và nó là HẰNG SỐ**

| Đường | Vì sao ⛔ không kiểm |
|---|---|
| ⭐ `GET /v1/projects/{project_id}` (`PRJ-3`) | ⭐ **Ngoại lệ đúng một, đã có lập luận**: `API-PRJ-4` — *"nếu cả metadata cũng bị chặn thì tác giả ⛔ không còn đường nào biết vì sao nội dung của mình biến mất"*. Response **luôn mang `access_state`** |
| `GET /v1/layout-templates` (`Endpoint-Page-Layout.md`) | Registry là **hằng số trong code**, ⛔ không thuộc phạm vi project nào |
| `EK-1` … `EK-3` (`Endpoint-Eval-Kit.md`) | `INV-API-EK-9` — *"tài sản đo lường ⛔ KHÔNG bị takedown chạm tới"*. ⚠️ **Điều kiện giữ mệnh đề đúng**: `provider_refusal_log` ⛔ không lưu nội dung người dùng thô |
| `E-TN-1` … `E-TN-5` (`Endpoint-Tenancy.md`) | Định danh/membership, ⛔ không phạm vi project |
| `TD-1`, `TD-2`, `TD-3` (`Endpoint-Takedown-Public.md`) | ⭐ **Chính là đường tạo ra cờ.** `INV-API-TD-9`: ⛔ không endpoint nào ngoài `TD-3` đổi được `access_state` |
| ⚠️ `E-UC-1` … `E-UC-4` (`Endpoint-Usage-And-Credit.md`) | Dữ liệu **đối soát chi phí**, ⛔ không phải nội dung; chặn nó làm hỏng đối soát của chính tenant. ⭐ **Điều kiện có hạn**: mệnh đề này đúng **chỉ khi** response ⛔ **không** mang trường dẫn xuất từ nội dung (prompt, tiêu đề, thoại). ⚠️ Ngày nào một trường như vậy xuất hiện, hàng này **chuyển sang Nhóm B** |

#### Tiêu chí đóng — ⭐ để lô áp ⛔ không phải đoán

| # | Tiêu chí |
|---|---|
| **`C3-K1`** | ⭐ **Định nghĩa *"đường đọc"***: mọi endpoint mà response chứa — hoặc mọi ghi chạm — dữ liệu **dẫn xuất từ nội dung của một project**, ⭐ **kể cả khi path ⛔ không chứa `project_id`**. ⚠️ Đây đúng là chỗ cả bốn file Nhóm B rơi: chúng định danh bằng `page_id` / `panel_id` / `dialogue_line_id` / `bubble_id` / `chapter_id` ⇒ phải **resolve ngược lên project** rồi mới kiểm |
| **`C3-K2`** | ⛔ **Fail-closed**: ⛔ **không thấy** dòng `public.project_access_state` ⇒ **TỪ CHỐI**. ⛔ Tuyệt đối ⛔ không đọc *"thiếu dòng"* thành `'active'`. *(Khuôn này `Endpoint-Preview-Export.md` đã viết đúng — nhân bản nó, ⛔ đừng viết lại)* |
| **`C3-K3`** | **Đúng MỘT hàm dùng chung** ở tầng service (`API-PRJ-4`), ⛔ không mỗi handler một bản sao. ⛔ Không `force`, ⛔ không `skip_gates`, ⛔ không `admin_override` — cùng khuôn `SDD-HG-01.4` |
| **`C3-K4`** | ⭐ **Cưỡng chế bằng test TOÀN CỤC, ⛔ không per-endpoint**: seed project `disabled_by_takedown`, duyệt **toàn bộ route table**; route ⛔ không nằm trong **allowlist Nhóm C** mà ⛔ không trả `403 PROJECT_ACCESS_DISABLED` ⇒ **CI đỏ**. ⇒ Route **mới** sinh sau này **tự động** rơi vào danh sách. ⭐ Đây là khuôn `M1-1` áp cho disable-access: **thuộc tính toàn cục**, ⛔ không phải đếm *"đã sửa N/M endpoint"* |
| **`C3-K5`** | **Nhóm C là HẰNG SỐ trong repo**, ⛔ không phải một cờ trong test. ⭐ **Thêm phần tử phải qua review bảo mật**, ⛔ không qua PR sửa test — cùng kỷ luật `IC-10`/`BP-11` của [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) |
| **`C3-K6`** | ⚠️ ⭐ **Ranh giới thành thật của `C-3`**: một **signed URL đã phát TRƯỚC** khi takedown có hiệu lực **vẫn đọc được** cho tới khi hết TTL — ⛔ **không thu hồi được** (`API-PE-7`). ⇒ `C-3` chặn **việc CẤP quyền đọc**, ⛔ **không** chặn quyền đọc **đã rời khỏi hệ thống**. ⭐ Cận trên của cửa sổ đó **chính là `T-7`** ⇒ ⛔ **không được** tuyên bố *"nội dung đã bị hạ hoàn toàn"* trong khi `T-7` còn mở |
| **`C3-K7`** | ⛔ **`deleted_at` ⛔ KHÔNG BAO GIỜ được đọc thành trạng thái takedown** — hai cột độc lập (`INV-API-TD-10`, `API-PRJ-2`). Một hàm dùng chung đọc nhầm `deleted_at` là **phá nguồn sự thật**, ⛔ không phải một tối ưu |

### 4.5 ⭐ Trả lời `TD-Q1` — DB role và uỷ quyền cho bề mặt operator

> `TD-Q1` của [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md) ghi chủ là **`Spec-Security-*`** và nó **đang CHẶN triển khai** `TD-2`/`TD-3`. Mục này **trả lời**.

**Câu hỏi có HAI nửa, ⛔ đừng gộp**: (i) **DB role** nào chạy `TD-2`/`TD-3`; (ii) **cơ chế uỷ quyền operator ở tầng ứng dụng**.

#### Nửa (i) — ⭐ CHỐT: role thứ **NĂM** `app_operator`. ⛔ Đường owner bị LOẠI.

| Phương án | Kết luận |
|---|---|
| ⛔ **Đi đường owner / vận hành đã có** | ⛔⛔ **LOẠI — ⛔ không phải "kém hơn", mà là KHÔNG KHẢ THI.** Ba căn cứ độc lập: **(a)** Chủ sở hữu bảng trong PostgreSQL ⛔ **không chịu RLS theo mặc định** ⇒ một đường **HTTP chạm tới được** chạy dưới owner chính là `BP-12b` **dựng lên như thiết kế**, và nó xoá RLS trên **mọi** bảng chứ ⛔ không riêng `takedown_request`. **(b)** [ADR-006 `D7`](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) + [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md) chốt owner là role **DDL**; role ứng dụng ⛔ không có DDL và ⛔ không là owner của bảng nào (`IC-11`) — dùng owner cho đường nghiệp vụ **đảo ngược** chính ràng buộc đó. **(c)** Biến thể *"founder chạy tay bằng `psql`"* cũng ⛔ **không được**: `TD-3` bắt buộc `UPDATE takedown_request` + `UPDATE project_access_state` + `INSERT change_log` trong **MỘT** transaction (`KC-2`, `KC-4`), với `resolved_at` do **hệ thống** ghi làm bằng chứng SLA. Một phiên `psql` thủ công là biện pháp dạng *"quy ước"* — mà `C-2` phát biểu: ⛔ **trong repo này coi như không tồn tại** |
| ✅ ⭐ **Role thứ năm `app_operator`** | ✅ **CHỌN.** Đây là phương án **duy nhất** giữ được đặc quyền cực tiểu: bề mặt xuyên tenant được **đếm được, đặt tên được, và đối chiếu được với hằng số repo** |

⭐ **Hình dạng grant của `app_operator` — ⛔ không rộng hơn một dòng nào**:

| Cho phép | Cấm |
|---|---|
| `SELECT`, `UPDATE` trên `public.takedown_request` | ⛔ **Không `DELETE`** — ⛔ không hard-delete, dữ liệu giữ cho counter-notice (`TM-F7-5`) |
| `SELECT`, `UPDATE` trên `public.project_access_state` | ⛔ **Không `INSERT`** — `INV-PAS-5` bảo đảm dòng đã tồn tại từ transaction tạo project |
| `INSERT` trên `public.change_log` | ⛔ **Không `UPDATE`/`DELETE`** — append-only (`GR-3`) |
| — | ⛔⛔ **KHÔNG `BYPASSRLS`** · ⛔ **không DDL** · ⛔ **không là owner** của bảng nào · ⛔ **không `SELECT`** một bảng nghiệp vụ nào của `story`/`comic`/`generation` |

⚠️ ⭐ **Vì sao `app_operator` ⛔ KHÔNG được đọc bảng nghiệp vụ**: operator cần biết *"project này có tồn tại không"*, ⛔ **không** cần đọc nội dung của nó. Cấp `SELECT` trên `story.project` *"cho tiện hiển thị tiêu đề"* biến `TD-2` thành **đường liệt kê tác phẩm của mọi tenant** — đúng `BP-14` dịch sang một role mới.

#### ⚠️ Nửa (i) BUỘC SỬA `SDD` §7.4 — và `SDD` **đã ĐÓNG BĂNG**

⛔ **File này ⛔ KHÔNG sửa `SDD`.** Ghi ra để PM xử ở close-step:

| Ripple bắt buộc | Nội dung |
|---|---|
| [`SDD` §7.4](../Architecture/SDD-Comic-Studio.md) | *"Bốn DB role"* ⇒ **NĂM**; thêm hàng `app_operator`; *"bốn connection string"* ⇒ **năm** |
| [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) | Thêm một điều khoản cạnh `D6` cho carve-out của `app_operator`; `W-2` phải mở rộng để đối chiếu role mới |
| Hằng số `pg_policies`/`pg_roles` trong repo | Cập nhật theo, ⛔ không nới test để cho qua (`BP-4` cảnh báo đúng cái bẫy này) |

> [!CAUTION]
> ⭐ **Chốt phương án ⛔ KHÔNG tự nó gỡ chặn.** `TD-2`/`TD-3` **vẫn ⛔ không được triển khai** cho tới khi PM lands ba ripple trên. `TD-Q1` chuyển từ *"⛔ chưa có câu trả lời"* sang *"⭐ đã có câu trả lời, ⛔ chờ tầng Architecture mở băng"*.

#### Nửa (ii) — cơ chế uỷ quyền operator ở tầng ứng dụng

⚠️ `membership` ⛔ **chưa có** mô hình role/permission, và Story tenancy **loại tường minh** việc xây luồng đổi role ở horizon này ⇒ ⛔ **danh tính operator ⛔ KHÔNG được lấy từ `membership`** (`C-13d`).

⭐ **Ràng buộc CHỐT lên cơ chế** — cơ chế, ⛔ không phải con số:

1. ⭐ Danh sách operator là **cấu hình, nạp CHỈ qua biến môi trường** ([ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) điều 6) — ⛔ không bảng mới *(bảng mới ⇒ `ADR-005` `G-2` closed list ⇒ tầng đã đóng băng)*, ⛔ không cột mới trên `membership`.
2. ⭐ Đối chiếu theo **`public."user".id` của ta**, ⛔ **không** theo `external_auth_id`, ⛔ **không** theo email — cả hai đều do vendor sở hữu và đổi được ngoài tầm kiểm soát.
3. ⛔⛔ **Claim của vendor auth ⛔ KHÔNG BAO GIỜ là nguồn sự thật** của tư cách operator — `BP-10`/`IC-9`. Một *"role: admin"* trong JWT là đúng lỗi mà [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 4 đã loại.
4. ⭐ Kiểm ở **đúng một** hàm uỷ quyền dùng chung + **lint rule hai chiều** (`C-13a`, `C-13b`).
5. ⭐ Phiên operator ⛔ **không mang tenant context** ⇒ ⛔ **không** dùng lại middleware bơm tenant. ⚠️ Trộn hai đường là cách một request operator vô tình chạy dưới `app_api` **có** tenant, hoặc ngược lại.
6. ⛔ **Mọi hành động operator sinh `change_log`** cùng transaction (`KC-2`) — `TD-3` đã yêu cầu; ⚠️ và `TD-2` là **đường ĐỌC xuyên tenant** ⇒ ⭐ nó **cũng cần dấu vết**. ⚠️ ⛔ Giá trị `action_type` cho *"operator đọc danh sách đơn"* ⛔ **chưa có** trong danh mục đóng của `public.change_log` ⇒ ⛔ **file này ⛔ không bịa một giá trị** — ghi thành hàng `TBD` cho **Architect**.

---

## 5. ⛔ Anti-feature `SRS-NFR-15` — vì sao file này KHÔNG đề xuất phát hiện tương đồng

> [!CAUTION]
> ⭐ **Đây là chỗ phản xạ nghề nghiệp của một security auditor sẽ làm NGƯỢC.** Nguyên văn cảnh báo trong repo: *"một dev sẽ làm ngược điều này theo bản năng, vì 'chủ động kiểm tra' nghe như hành vi có trách nhiệm"*.

**Quy tắc CHỐT** (`SRS-NFR-15`, và [`SDD` §1.2](../Architecture/SDD-Comic-Studio.md) liệt kê nó trong nhóm *"kiến trúc này KHÔNG được phép làm gì"*):

> Hệ thống **KHÔNG được** có bộ phát hiện *"truyện này có thể có bản quyền của người khác"* — copyright detection, plagiarism check, similarity scan — **trước khi có xác nhận của luật sư**.

**Lý do — pháp lý, ⛔ không phải kỹ thuật**: điều kiện (a) của miễn trừ Điều 198b là **"không biết"**. Xây một bộ phát hiện **tạo ra đúng tri thức mà luật đang miễn trừ cho việc không có** ⇒ **tự phá miễn trừ của chính mình**. Một feature "an toàn" ở đây làm **tăng** rủi ro pháp lý, ⛔ không giảm.

⚠️ **Phụ thuộc**: câu hỏi `T-20` (*nền tảng có được coi là trung gian theo Điều 198b không?*) chưa có trả lời ⇒ ⛔ **không ai** — kể cả file này — được phép nới quy tắc trên.

### Tam giác phân biệt — ⛔ ba thứ này KHÔNG được lẫn

| | Việc | Trạng thái | Vì sao |
|---|---|---|---|
| **1** | **Đọc opt-out signal do CHÍNH CHỦ QUYỀN gắn vào file** (`L-3`, `KC-6`) | ✅ **BẮT BUỘC** | Đây là **dữ kiện khách quan**, ⛔ không phải suy đoán — *"đọc nhãn không tạo ra tri thức suy đoán"* |
| **2** | **Ghi lại mọi lần PROVIDER từ chối vì content policy** (`SRS-NFR-20`) | ✅ **BẮT BUỘC** | Đây là **sự kiện do bên thứ ba tạo ra và thông báo cho ta**, ⛔ không phải kết luận của ta về nội dung của khách |
| **3** | **Tự dò tương đồng / phát hiện bản quyền / chấm điểm nghi vấn** | ⛔ **CẤM** | Tạo ra tri thức mà miễn trừ Điều 198b đang dựa trên việc **không có** |

### Hai quy tắc bắt buộc cho mọi review sau

1. ⛔ **Trong file này và trong [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md), *"thiếu content scanning"* ⛔ KHÔNG xuất hiện ở bất kỳ cột lỗ hổng nào.** Nó ⛔ không phải một gap, ⛔ không phải một finding, ⛔ không phải nợ kỹ thuật.
2. ⛔ **Nếu một run sau sinh ra đề xuất *"quét nội dung upload để phát hiện vi phạm"*, đó là VI PHẠM một requirement CHỐT, ⛔ không phải một cải tiến** — phải bị chặn ở review, kể cả khi nó được trình bày dưới nhãn *"security hardening"*.

⚠️ **Ranh giới ⛔ không được đọc quá**: `SRS-NFR-15` cấm **phát hiện tương đồng nội dung**. Nó ⛔ **không** cấm các biện pháp an ninh thông thường — rate limit, kiểm kích thước file, kiểm định dạng, log truy cập, ghi nhận provider refusal. Đọc `SRS-NFR-15` thành *"cấm mọi kiểm tra trên dữ liệu upload"* là **sai theo chiều ngược lại**, và nó sẽ làm rơi `C-6`.

---

## 6. Nghĩa vụ pháp lý — phần thuộc file này

> ⭐ Cột *"Góc an ninh của file này"* là phần file này sở hữu. Cột *"Phần thuộc file khác"* trỏ đi, ⛔ không đặc tả lại — đặc biệt là [Spec-Security-Legal-Compliance](./Spec-Security-Legal-Compliance.md) (lô L19, ✅ đã viết xong).

| # | Nghĩa vụ | Góc an ninh của file này | Phần thuộc file khác |
|---|---|---|---|
| **`L-1`** | **Năm hạng mục provenance trên MỌI generation** | `A-2` là **kho bằng chứng** ⇒ mối đe doạ chính là **tampering + repudiation**: `TM-F5-2` (sửa/xoá append-only), `TM-F5-3` (bằng chứng thiếu), `TM-F2-3`. ⚠️ ⛔ **Không backfill được** ⇒ `BLOCKER-04` chặn **mọi thứ** | Hình dạng cột, DDL: **lô DB Schema**. Cơ chế: [ADR-017 `Q1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`L-2`** | **`generation` + `change_log` + `usage_event` commit CÙNG MỘT transaction** | ⭐ Phát biểu đúng: tầng DB cưỡng chế **cột + append-only** (`GR-1`…`GR-5`); **nguyên tử** cưỡng chế bằng **1-DB + middleware + test CI**. ⇒ Mối đe doạ an ninh thật là **kiến trúc trôi**: bất kỳ đề xuất nào tách DB thứ hai/service nội bộ **phá `KC-4` trước khi phá bất cứ thứ gì khác** | Chuẩn tắc đầy đủ: [ADR-017 `Q4.1`–`Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md). Thứ tự vòng đời: `P-7`, lô DB Schema |
| **`L-3`** | **Kiểm opt-out Điều 37b tại ingest, 4 kênh, log kèm timestamp, chặn nếu có signal** | `TM-F1-1` — **đường vòng qua choke point** là mối đe doạ duy nhất đáng kể; `C-1` phát biểu nó thành ràng buộc thường trực. ⭐ Đây cũng là **cạnh 1 của tam giác** ở [§5](#5--anti-feature-srs-nfr-15--vì-sao-file-này-không-đề-xuất-phát-hiện-tương-đồng) — được phép và bắt buộc | Nội dung bốn kênh, hình thức log: `Spec-Security-Legal-Compliance.md` + `Spec-Integration-*` |
| **`L-4`** | **Checklist safe harbour Điều 198b**: công cụ tiếp nhận · đăng ký đầu mối · SLA 72h bằng soft-delete + disable-access | ⭐ **BỐN** hệ quả an ninh: (i) `AS-2` là bề mặt **CÔNG KHAI** duy nhất, ngoài mọi tenant context ⇒ `TM-F7-1`…`TM-F7-3`; (ii) cờ disable-access phải kiểm ở **mọi** đường đọc ⇒ `C-3`, `TM-F7-7`, danh sách đóng ở [§4.4](#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access); (iii) ⛔ **không hard delete** ⇒ `TM-F7-5`; (iv) ⭐ **cùng nghĩa vụ này sinh ra bề mặt OPERATOR `AS-13`** — nửa **vận hành** của `L-4` (đánh giá đơn + thi hành trong 72h) ⛔ **không tồn tại được nếu không có** một đường xuyên tenant ⇒ `TM-F7-8`, `C-13`, [§4.5](#45--trả-lời-td-q1--db-role-và-uỷ-quyền-cho-bề-mặt-operator). ⚠️ `T-29` (thông báo cho tenant) chủ = **Founder + luật sư** | Nội dung checklist, đăng ký đầu mối với cơ quan quản lý, mẫu phản hồi 72h: [Spec-Security-Legal-Compliance](./Spec-Security-Legal-Compliance.md) |
| **`L-5`** | **Đánh dấu nội dung AI bằng định dạng máy đọc** (metadata cấp page/panel + watermark ở export path) | `TM-F6-5` — **bỏ qua stage** là mối đe doạ; stage phải nằm **trong** đường export dùng chung, ⛔ không phải một bước tuỳ chọn. ⚠️ Thiết kế theo **diễn giải RỘNG** cho tới khi `T-19` đóng | Phạm vi nghĩa vụ + `T-21` (SynthID): `Spec-Security-Legal-Compliance.md` + luật sư |
| **`L-6`** | **Cơ chế để user nhận biết đang tương tác với hệ thống AI** | Nhỏ về kỹ thuật; góc an ninh **duy nhất**: nó ⛔ **không được** là một cờ cấu hình **tắt được** — cùng khuôn `SDD-HG-01.2` (⛔ không cờ cấu hình nào mở được đường vòng). ⚠️ Có deadline ⇒ ⛔ không được rơi | Nội dung và vị trí hiển thị: `Spec-Security-Legal-Compliance.md` + lô API/UI |
| **`L-7`** | **Đường hard-delete toàn bộ dữ liệu tenant phải TỒN TẠI VÀ ĐÃ KIỂM THỬ** (`ON DELETE CASCADE` trên mọi FK) | ⭐ Đây là **năng lực đặc quyền cao nhất trong hệ thống** ⇒ nó là một bề mặt: đường xoá phải là **một đường riêng có đặc quyền**, ⛔ **tách biệt tuyệt đối** khỏi soft-delete của `L-4` (gộp = **phá bằng chứng counter-notice**). ⚠️ `api`/`worker` ⛔ **không** có quyền `DeleteObject` trên prefix canonical. Chi tiết CASCADE + prefix storage: [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) | Retention/purge (`T-23`): **PM + luật sư SHTT** |

---

## 7. Ma trận `KC-1`…`KC-7`

> ⭐ Bảy hàng `KC` là *"danh sách **duy nhất** không mở ra thương lượng scope"*. ⚠️ **Bộ lọc Story giới hạn phạm vi BUILD, ⛔ không giới hạn phạm vi SCHEMA/SECURITY** ⇒ `KC-7` vẫn phải được soi dù `UC-10` ngoài phạm vi build.

| `KC` | Neo | Soi ở đâu trong file này | Thuộc file nào (nếu không phải file này) |
|---|---|---|---|
| **`KC-1`** — chuỗi lineage (`parent_generation_id` + `relation_kind` + `origin`) | `SRS-FR-34` | `A-2`, `L-1`, `TM-F5-3`, `TM-F5-7`; `BLOCKER-04` chặn **mọi thứ** vì ⛔ không backfill được. ⚠️ **Cắt UI cây ≠ cắt cột dữ liệu** — một tài liệu viết *"đã cắt UI cây nên không cần lưu quan hệ cha-con"* là **vi phạm `KC-1`** | DDL: lô DB Schema. Cơ chế: [ADR-017 `Q1`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`KC-2`** — `change_log` ghi **mọi** hành động người dùng | `SRS-FR-35` | `A-2`; `TM-F4-4` (chống repudiation ở gate), `TM-F5-2` (append-only), `TM-F6-1` (export **cũng là** hành động phải ghi) | Điểm cưỡng chế middleware: [ADR-017 `Q2`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`KC-3`** — `field_provenance` mức field + `generation.origin` | `SRS-FR-36` | `TM-F2-3`; guardrail `GR-1` (`INSERT` thiếu `origin` **FAIL ở tầng DB**) | [ADR-017 `Q3`, `Q5`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`KC-4`** — một-transaction-boundary | `SRS-NFR-13` | `L-2`, `TM-F5-3`. ⛔ File này ⛔ **không** viết *"tầng DB cưỡng chế `KC-4`"* — ba lớp `L1`/`L2`/`L3` | [ADR-017 `Q4.1`–`Q4.6`](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) |
| **`KC-5`** — `tenant_id` + RLS ở **mọi** bảng nghiệp vụ | `SRS-NFR-01` | Chỉ nêu ở mức tài sản (`A-1`) và ranh giới session ([§2.3](#23-ba-loại-session-db--ranh-giới-tin-cậy)) | ⭐ **Toàn bộ nằm ở [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md)** — đó là file sở hữu `KC-5` |
| **`KC-6`** — opt-out check Điều 37b tại ingest | `SRS-FR-37` | ⭐ **File này sở hữu**: `TM-F1-1`, `C-1`, `L-3`, và cạnh 1 của tam giác ở [§5](#5--anti-feature-srs-nfr-15--vì-sao-file-này-không-đề-xuất-phát-hiện-tương-đồng) | Prefix `incoming/` ở góc cô lập: [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md). Nội dung bốn kênh: `Spec-Security-Legal-Compliance.md` |
| **`KC-7`** — credit ledger + HOLD trước enqueue + reaper | `SRS-FR-28` | ⭐ **Soi ở `A-10` + `TM-F5-5`**: `KC-7` là `[OoH]` MVP3 — ⛔ **không HOLD ở MVP1–MVP2** ⇒ **rate limit đếm SỐ REQUEST** là biện pháp chống lạm dụng chi phí **duy nhất** còn hiệu lực ở horizon này (`C-6`). ✅ `T-25` **đã đóng** — Founder chọn **chỉ rate limit**, ⛔ không hard quota, ⛔ không HOLD (`E9`) | Ledger/`CHECK (available >= 0)`/reaper: **lô DB Schema** (reserve chỗ) + [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md). Seam billing: [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) điều 7 |

---

## 8. Bảng `TBD` của file này

> ⛔ **Mục này ⛔ KHÔNG đóng hàng nào.** Nó chỉ trả lời **ai đóng** và **khi nào**. Hàng nào đã có mã ở [`SDD` §9](../Architecture/SDD-Comic-Studio.md) thì **giữ nguyên mã**, ⛔ không đánh mã mới.

| # | Việc còn mở | Ai đóng | Khi nào |
|---|---|---|---|
| `T-6` | `N` của `in_flight_per_tenant` — biện pháp chống DoS chéo tenant | **PM + Architect** | Sau MVP0 đo tải thật |
| `T-7` | TTL signed URL | **Dev đề xuất, Founder duyệt** | MVP1 |
| `T-9` | Uptime SLA · RPO/RTO/backup retention · **queue depth alert threshold** | **Founder + dev** | Sau MVP0 |
| `T-10` | Ngưỡng rate limit + giới hạn upload (`C-6`) | **PM + Architect** | Sau khi đo tải |
| `T-16` | `b-1` mã hoá + secret · `b-7` observability/alerting | **Dev** | Sau khi platform được mua và MVP0 có số đo |
| `T-17` | `b-5` scalability/capacity — ⛔ không có nó thì ⛔ không định nghĩa được *"bất thường"* | **Founder + dev** | Sau khi chọn hosting |
| `T-18`…`T-22` | Bốn câu hỏi pháp lý + nghĩa vụ lưu trữ trong nước | ⭐ **PM + luật sư SHTT** | Trước thương mại hoá |
| `T-23` | `b-3` retention nghiệp vụ (gồm purge cho hai bảng append-only) | ⭐ **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| `T-24` | `b-4` dữ liệu cá nhân — gồm `A-9` (email + SĐT người nộp takedown) | ⭐ **PM + luật sư SHTT** | Cùng gói `SRS-NFR-17` |
| ~~`T-25`~~ | ~~Hành vi thay HOLD credit ở MVP1–MVP2~~ | ✅ **ĐÃ ĐÓNG** — Founder chọn **chỉ rate limit cho `generate`, đếm số request** (`E9`) | — |
| `T-27` | `b-2` lưu/mã hoá/thu hồi API key BYOK (`A-6`, `C-12`) | ⭐ **Architect + Founder** — PM đã gán chủ (`E22`); chọn cơ chế KMS **kéo theo** [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) | Trước khi seam BYOK bật. ⚠️ Đóng đúng nghĩa cần **một ADR mới** ⇒ ⛔ **ngoài phạm vi run Phase 2 này**, ghi thành **nợ kỹ thuật số 1** |
| `T-29` | Thông báo cho tenant bị takedown (`TM-F7-1`, `TM-F7-6`) | ⭐ **Founder + luật sư**, PM điều phối (PM gán, `E22`). ⛔ Security Auditor **từ chối đóng** vì đây là **quyết định pháp lý** — PM **chấp nhận** lời từ chối | Trước khi `Spec-Integration-Takedown-Intake.md` được coi là đầy đủ |
| ~~`P-2`~~ | ~~`SDD-HG-01.4` có cưỡng chế thêm ở tầng DB không~~ | ✅ **ĐÃ ĐÓNG** bởi [DB-Entity-Preview-And-Export](../Schema/DB-Entity-Preview-And-Export.md) — **CÓ**, trigger + vị từ SQL dùng chung | — |
| `P-7` | Thứ tự gắn `usage_event`/`cost_usd` trong vòng đời job; hình dạng idempotency key (`TM-F5-3`, `TM-F5-6`) | **Architect, lô DB Schema** | Trước khi lô DB Schema được duyệt |
| **mới** | ⭐ **Cơ chế render an toàn của compositor** (`C-10`, `TM-F6-3`) — ⛔ chưa chọn được vì **[ADR-001](../Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) §`TBD` chưa chọn *thư viện compositor + sinh PDF*** (và chưa chốt `worker_threads` hay tách job), ⛔ **không phải** vì `SRS-NFR-09` | ⭐ Tách đôi: **tập ràng buộc — Architect**, đã CHỐT tại `C-10`, ⛔ không làm lại · **chọn thư viện — Dev** | **Spike MVP0** — `C-10` là **tiêu chí nghiệm thu của spike** |
| **mới** | **Chu kỳ dọn rác `incoming/`** (`TM-F1-6`) | **Architect + dev**, cùng nhóm `T-10` | Trước deploy MVP1 |
| ~~`TD-Q1`~~ *(nửa i)* | ~~DB role cho bề mặt operator `TD-2`/`TD-3`~~ | ✅ ⭐ **ĐÃ TRẢ LỜI** ở [§4.5](#45--trả-lời-td-q1--db-role-và-uỷ-quyền-cho-bề-mặt-operator) — role thứ năm **`app_operator`**; đường owner **bị loại**. ⚠️ ⛔ **Chưa gỡ chặn**: cần **PM** lands ripple `SDD` §7.4 + `ADR-006` + hằng số repo | ⭐ **Trước** khi `TD-2`/`TD-3` được triển khai |
| **mới** | ⭐ **Ba ripple mở băng tầng Architecture** cho `app_operator` (`SDD` §7.4 bốn ⇒ năm role · `ADR-006` carve-out cạnh `D6` · `W-2` mở rộng) | ⭐ **PM** điều phối, **Architect** thực hiện | Close-step của lô này |
| **mới** | **Giá trị `action_type` của `change_log` cho hành động operator** — gồm cả **đường ĐỌC xuyên tenant** `TD-2` (`C-13.6`). ⛔ File này ⛔ không bịa giá trị | **Architect**, cùng danh mục đóng `public.change_log` | Cùng lúc với `app_operator` |
| **mới** | ⭐ **Cơ chế rate limit cho `TD-1`** — `RL-1` khoá theo `(tenant_id, action)` mà `TD-1` ⛔ **không có `tenant_id`** ⇒ ⛔ **thiếu CƠ CHẾ, ⛔ KHÔNG phải thiếu ngưỡng**. ⛔ **Đừng gộp vào `T-10`** | **Architect + PM**, cùng `TD-Q5` | ⭐ Trước khi công cụ takedown chạy thật |
| **mới** | ⚠️ **Điều kiện tiên quyết `C-6-PRE-1`**: `RL-1` là bộ đếm **trong tiến trình**, chỉ đúng vì `D-01` chốt **1 process**. Cần phép kiểm khởi động fail-closed; và **ADR mới bắt buộc** trước khi chạy >1 tiến trình `api` | **Dev** (phép kiểm) · **Architect** (ADR khi scale-out) | Cùng `T-16`/`b-7`; ⭐ **trước** mọi thay đổi scale-out |
| **mới** | ⛔ **Cơ chế đặc quyền cho lần GHI đầu tiên dòng `public."user"`** (`AS-14`) — `D6` ⛔ không phủ, `D3` chỉ ĐỌC. ⛔ File này ⛔ **không chọn** nhánh webhook hay JIT | ⭐ **Architect**, [Endpoint-Tenancy](../API/Endpoint-Tenancy.md) | **Trước** request đã xác thực đầu tiên |
| **mới** | ⭐ **Lô ÁP `C-3`** — thêm `403 PROJECT_ACCESS_DISABLED` vào 4 file Nhóm B + phần thiếu của `Endpoint-Generation.md` ([§4.4](#44--c-3-danh-sách-đóng-các-đường-đọc-phải-kiểm-cờ-disable-access)) | ⭐ **PM giao lô**; Architect/Engineer thực hiện | ⚠️ Trước khi công cụ takedown chạy thật — ⛔ hiện là **lỗ hổng tuân thủ đang mở** |

---

## 9. Tài liệu tham khảo

**Kiến trúc** — [SDD-Comic-Studio](../Architecture/SDD-Comic-Studio.md) (§4 ranh giới · §5 luồng `F1`–`F7` · §6.1 tenant context · §6.3 `SDD-HG-01` · §6.4 observability & audit · §7.4 bốn DB role · §9 bảng `TBD`) · [ADR-002](../Architecture/ADR-002-Hosting-Platform-And-Region.md) · [ADR-003](../Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) · [ADR-004](../Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md) · [ADR-006](../Architecture/ADR-006-RLS-Tenant-Context-Injection.md) · [ADR-008](../Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) · [ADR-010](../Architecture/ADR-010-Tenant-Isolation-With-RLS.md) · [ADR-013](../Architecture/ADR-013-Typeset-Layer-Separate-From-Art.md) · [ADR-016](../Architecture/ADR-016-Image-Provider-Adapter-And-Version-Pinning.md) · [ADR-017](../Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-018](../Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)

**Requirements** — [SRS-Comic-Studio](../../020-Requirements/SRS-Comic-Studio.md) (§3 các hàng `SRS-FR-*`/`SRS-NFR-*` · §5.2 gồm bảy hàng `b-1`…`b-7`)

**Security** — [Spec-Security-Tenant-Isolation](./Spec-Security-Tenant-Isolation.md) · [Spec-Security-Legal-Compliance](./Spec-Security-Legal-Compliance.md) *(lô L19 — ✅ đã viết xong)*

**API** *(⛔ chỉ đọc — file này ⛔ không sửa một dòng nào của tầng API)* — [Endpoint-Takedown-Public](../API/Endpoint-Takedown-Public.md) (`TD-1`…`TD-3`, `TD-Q1`, `TD-Q5`, `INV-API-TD-*`) · [Endpoint-Project](../API/Endpoint-Project.md) (`API-PRJ-4` — khuôn kiểm `access_state`) · [Endpoint-Tenancy](../API/Endpoint-Tenancy.md) (`API-TN-5`) · [Endpoint-Preview-Export](../API/Endpoint-Preview-Export.md) · [Endpoint-Generation](../API/Endpoint-Generation.md) · [Endpoint-Page-Layout](../API/Endpoint-Page-Layout.md) · [Endpoint-Panel-Script](../API/Endpoint-Panel-Script.md) · [Endpoint-Bubble-Typeset](../API/Endpoint-Bubble-Typeset.md) · [Endpoint-Human-Gates](../API/Endpoint-Human-Gates.md) · [Endpoint-Eval-Kit](../API/Endpoint-Eval-Kit.md) (`INV-API-EK-9`) · [Endpoint-Usage-And-Credit](../API/Endpoint-Usage-And-Credit.md)

**Schema** — [DB-Entity-Tenancy](../Schema/DB-Entity-Tenancy.md) (`RL-1` — bộ đếm rate limit trong tiến trình) · [DB-Entity-Compliance-And-Takedown](../Schema/DB-Entity-Compliance-And-Takedown.md) · [DB-Entity-Preview-And-Export](../Schema/DB-Entity-Preview-And-Export.md)

---

_Created by security-auditor_
_Author: trisjr_
