---
id: ESCALATIONS-2026-08-30-DONG-BO-SRS-NFR-VOI-ADR
type: run-escalations
run: 2026-08-30-dong-bo-srs-nfr-voi-adr
status: in-progress
created: 2026-08-30
---

# Escalations & Quyết định — run đồng bộ `SRS` ↔ `ADR`

> [!IMPORTANT]
> ⭐ **Đọc `E1` trước khi báo bất kỳ "lỗi" nào ở `ADR-001`.** Đó là dòng phòng ngừa quan trọng nhất của run này.

## Mục lục

- [E1 — ADR-001:16 và :173 KHÔNG phải lỗi](#e1--adr-00116-và-173-không-phải-lỗi)
- [E2 — Bốn quyết định của Founder tại gate](#e2--bốn-quyết-định-của-founder-tại-gate)
- [E3 — PM sai một tiền đề, lens bác đúng](#e3--pm-sai-một-tiền-đề-lens-bác-đúng)
- [E4 — Hai con số ĐANG ĐÚNG, cấm sửa](#e4--hai-con-số-đang-đúng-cấm-sửa)
- [E5 — C-10 không tự đóng theo](#e5--c-10-không-tự-đóng-theo)
- [E6 — Phạm vi thật rộng hơn phát biểu ban đầu](#e6--phạm-vi-thật-rộng-hơn-phát-biểu-ban-đầu)
- [E7 — Ba hạng mục report-only, KHÔNG xử lý ở run này](#e7--ba-hạng-mục-report-only-không-xử-lý-ở-run-này)

## `E1` — `ADR-001:16` và `:173` KHÔNG phải lỗi

> [!WARNING]
> ⚠️ **Toạ độ dưới đây là SAU khi run này chèn `updated:` vào dòng 7** của mọi file tầng 030 ⇒ mọi dòng từ 7 trở xuống **dịch `+1`**. Nếu bạn đọc một bản `ADR-001` **trước** run `2026-08-30-dong-bo-srs-nfr-voi-adr`, ba dòng này là `:15`, `:69`, `:172`.

> [!CAUTION]
> ⛔ **Lô sau: đừng "sửa" hai dòng này.**

Sau run này, `SRS:258` mang nhãn **LAI**, trong khi `ADR-001:173` vẫn ghi `` `SRS-NFR-09` (`CHƯA QUYẾT` → `TBD`) ``. Một lô sau `diff` hai dòng sẽ thấy lệch và **tưởng `ADR-001` sai**. ⛔ Nó không sai.

| Dòng | Nằm trong | Vì sao đúng như đang có |
|---|---|---|
| `ADR-001:16` | `## Context` | `## Context` của một ADR **theo định nghĩa** là ảnh chụp thế giới **TRƯỚC** quyết định. Sửa nó sẽ: (1) **phá chuỗi biện minh** — câu *"chi phí đảo ngược thấp nhất ngay lúc này"* chỉ có nghĩa khi tiền đề *"chưa có dòng code nào"* đúng; (2) **tạo vòng lặp logic** — ADR đóng `SRS-NFR-09` lại viện dẫn `SRS-NFR-09` đã đóng; (3) **xoá dấu vết audit** |
| `ADR-001:173` | bảng `### ADR này quyết (phần Phase 1 **cố ý** để mở)` | Cột 2 là cột **`Mã`**. Ngữ nghĩa của bảng là *"requirement này **đang** mở, và ADR này là **nơi đóng** nó"*. Chú thích `(CHƯA QUYẾT → TBD)` là **trạng thái ĐẦU VÀO** mà ADR nhận việc |

⭐ Đây đúng mô hình mà [`escalations.md:184` của run `2026-08-28`](../2026-08-28-phase-2-architecture-design-comic-studio/escalations.md) đã dùng thành công để bảo vệ header khác biệt của 4 bảng `ADR-001…004`. Chi phí bằng **0**, ⛔ không chạm file tầng 030 nào.

Cùng lý do, `ADR-001:70` cũng **⛔ không được đụng** — đó là **dòng chịu lực** chứng minh `b-6`/`b-7` ⛔ không được đóng theo, và là nguồn trực tiếp cho `A3`/`A4`.

> [!CAUTION]
> ⭐ **`E1` phủ CẢ BỐN ADR, ⛔ không riêng `ADR-001`.** Chú thích **trạng thái ĐẦU VÀO** y hệt còn ở **6 chỗ** nữa, tất cả đều **đúng như đang có**:
>
> | `file:line` | Nằm trong | Diễn đạt |
> |---|---|---|
> | `ADR-002:16` | `## Context` | `` **`CHƯA QUYẾT` → `TBD`** `` |
> | `ADR-002:190` | bảng *cố ý để mở* | `` `SRS-NFR-07` (`CHƯA QUYẾT` → `TBD`) `` |
> | `ADR-003:20` | `## Context` | `` **`CHƯA QUYẾT` → `TBD`** `` |
> | `ADR-003:174` | bảng *cố ý để mở* | `` `SRS-NFR-08` (`CHƯA QUYẾT` → `TBD`) `` |
> | `ADR-004:172` | bảng *cố ý để mở* | `` `SRS-NFR-08` (`CHƯA QUYẾT` → `TBD`) `` |
> | ⚠️ `ADR-004:23` | `## Context` | *"Cái còn mở: **vendor**…"* — ⛔ **không** chứa cụm `CHƯA QUYẾT`, nên `grep "CHƯA QUYẾT"` ⛔ **không** ra dòng này. Vẫn cùng bản chất |
>
> Mỗi chỗ đều nằm trong `## Context` (ảnh chụp **trước** quyết định) hoặc trong bảng `### ADR này quyết (phần Phase 1 cố ý để mở)` (cột `Mã`, ghi **trạng thái ADR nhận việc**). ⛔ Lô sau **không được** báo chúng là lệch tầng.
> Cùng loại: `ADR-006:218` (mục `## Alternatives`) còn viện dẫn *"hosting/PaaS còn `TBD`"* làm lý do **(i)** loại phương án pooler — lý do đó nay lạc hậu, nhưng quyết định loại **vẫn đứng vững** trên lý do (ii) và (iii), và đoạn đó cũng là ảnh chụp trước quyết định.

## `E2` — Bốn quyết định của Founder tại gate

| Mã | Quyết định | Vì sao |
|---|---|---|
| `G-1` | Đồng bộ **cả ba** `NFR-07` + `NFR-08` + `NFR-09` | `NFR-07`/`NFR-08` là **cùng một loại lệch tầng**, chỉ khác mã. Sửa sau = mở lại đúng những dòng vừa động vào (`:345`, `:58`, `:60`, `:95`, `:263`) ⇒ đúng bẫy "lô thứ hai" đã làm run `2026-08-28` tốn **43,8%** ngân sách |
| `G-2` | Sửa `SRS:15`, cho phép link vào 030 | Lý do của lệnh tự cấm (*"tầng đó chưa tồn tại tại thời điểm viết"*) **đã hết hiệu lực** — tầng 030 nay có 19 file Architecture. Giữ nguyên `:15` thì SRS mang một câu **mô tả sai hiện trạng** |
| `G-3` | `ADR-001…004` → `status: accepted` | Nhãn tầng 020 và trạng thái tầng 030 khớp nhau tại **một thời điểm**. Repo đã dùng `draft` làm mốc chặn thật (`ADR-010:176`) nên để `draft` mà vẫn hạ nhãn 020 là mâu thuẫn governance |
| `G-4` | Commit `ADR-001` nguyên trạng ✅ | Nếu `SRS` trỏ tới `ADR-001` như nơi đóng quyết định mà bản trong git ⛔ không có `shadcn/ui + Tailwind` ⇒ **thay một lệch tầng bằng một lệch tầng khó thấy hơn**. Commit `f77b922`, đúng 1 file / +2 −1, ⛔ không thêm bớt một chữ |

## `E3` — PM sai một tiền đề, lens bác đúng

PM viết trong brief: *"đóng một hàng `TBD` **làm sai cả ba con số** ở `SRS:345`"*.

⛔ **Sai.** Con số thứ nhất là **`CHỐT` thuần = 55**, và nó **đứng yên trong mọi phương án** — vì ⛔ không hàng nào trong `NFR-07/08/09` trở thành **CHỐT thuần**: cả bốn ADR đều **tự khai có tầng MẶC ĐỊNH kèm đường lui** (`ADR-001:52`, `ADR-002:60`, `ADR-003:57`, `ADR-004:66`), và theo `SRS:50` thì *có đường lui ⇒ là **MẶC ĐỊNH**, ⛔ không phải **CHỐT***.

⇒ Chỉ **2/3** con số đổi. Bài học: **PM cũng phải đếm tại nguồn**, kể cả khi con số nằm trong tiền đề của chính mình.

## `E4` — Hai con số ĐANG ĐÚNG, cấm sửa

| Con số | Vị trí | Vì sao đang đúng |
|---|---|---|
| **`55`** | `SRS:345` — CHỐT thuần | Hệ quả trực tiếp của `E3` |
| **`21`** | `SRS:437` — số hàng ở lại `TBD` | Cả 5 hàng `b-1`/`b-2`/`b-5`/`b-6`/`b-7` mà run này đụng đều **VẪN ở lại `TBD`** — chỉ đổi **mệnh đề lý do**, ⛔ không đổi trạng thái |

⚠️ Đây là loại lỗi **ngược** với lệch tầng: sửa một thứ đang đúng vì tưởng nó phải đổi theo. Đã ghi thành ràng buộc `K-2` trong `[CONSTRAINTS]` của mọi writer.

## `E5` — `C-10` không tự đóng theo

⛔ **Cơ chế render an toàn của compositor (`C-10`) VẪN MỞ.** ⛔ Đừng đóng hộ một `TBD` bảo mật.

Nó vẫn mở, nhưng **vì một lý do khác** với lý do đang được ghi:

- **Lý do đang ghi (sai sau run này)**: *"vì `SRS-NFR-09` còn `TBD`"* — `ADR-001` đã đóng việc chọn ngôn ngữ/framework.
- **Lý do đúng**: `ADR-001:66` để mở *"thư viện compositor + sinh PDF"*, `:68` để mở *"compositor chạy trong `worker_threads` hay tách job"*. Ba ràng buộc bảo mật của `C-10` là thuộc tính của **engine cụ thể**, ⛔ không phải của *ngôn ngữ*.
- `ADR-001:50` (điều 8) chỉ chốt **cơ chế ngắt dòng** (`Intl.Segmenter`, NFC) — đó là **tính đúng đắn typesetting**, ⛔ không phải ràng buộc bảo mật.

⭐ **Xung đột chủ sở hữu + mốc, PM phân xử**: `Threat-Model:292`/`:521` ghi *Architect / lô API*; `Endpoint-Preview-Export:249` ghi *Architect / Phase 4*; `ADR-001:66` ghi *Dev / spike MVP0*.
**Hoà giải đã áp dụng**: tách hai việc — **Architect sở hữu TẬP RÀNG BUỘC** (đã CHỐT ở `C-10`, ⛔ không làm lại) · **Dev sở hữu việc CHỌN thư viện** thoả tập ràng buộc đó, tại **spike MVP0**, và `C-10` trở thành **tiêu chí nghiệm thu của spike**. ⇒ Mốc thật là **MVP0**, **sớm hơn** *"Phase 4"* đang ghi.

## `E6` — Phạm vi thật rộng hơn phát biểu ban đầu

Hàng nợ số 5 ở `000-Index.md:219` chỉ nêu `SRS-NFR-09`. Khảo sát cho thấy phạm vi thật:

| | Phát biểu ban đầu | Thực tế |
|---|---|---|
| Requirement lệch | 1 (`NFR-09`) | **3** (`NFR-07`, `NFR-08`, `NFR-09`) |
| File tầng 020 | — | **1** (`SRS`) — ✅ `PRD` đã grep, **sạch** |
| Điểm sửa tầng 020 | — | **19** |
| Ripple tầng 030 | — | **9 điểm / 8 file** |
| MOC + Index (PM) | — | **3 điểm** |

⚠️ **Ba dòng PM không grep ra ở lượt đầu**, lens tìm thêm — hai trong đó nghiêm trọng:
1. ⭐ `SRS:15` — chính sách toàn tài liệu **CHẶN** việc thêm link ADR ⇒ sinh ra `G-2`.
2. ⭐ `SRS:58` + `:60` — dòng **duy nhất** liệt kê danh sách hàng LAI theo tên. Bỏ sót = để lại mâu thuẫn nội tại mới.
3. `SRS:7` — `updated`.

⭐ **Và ripple nguy hiểm nhất**: `SDD-Comic-Studio.md:811` hard-code *"**năm hàng LAI**"* kèm đủ 5 mã. Sửa `SRS:58`/`:60` mà quên dòng này là **tạo ra đúng loại lệch tầng mà run này đang đi dọn**.

## `E7` — Ba hạng mục report-only, KHÔNG xử lý ở run này

Lens phát hiện, PM ghi nhận, ⛔ **cố ý không sửa** — ngoài phạm vi gate:

| # | Hạng mục | Vì sao để lại |
|:--:|---|---|
| **1** | `ADR-001` §Đường lui chỉ phủ **3/5** hàng MẶC ĐỊNH — `pnpm workspace` (`:60`) và `ESLint boundary rule` (`:61`) **thiếu đường lui ghi rõ** ⇒ ⛔ không thoả định nghĩa MẶC ĐỊNH của `SRS:50` | Là **sửa nội dung quyết định kiến trúc**, ⛔ không phải đồng bộ phát biểu. Hệ quả cho run này: writer ⛔ **không được** khẳng định *"toàn bộ tầng MẶC ĐỊNH đều có đường lui"* |
| **2** | `shadcn/ui + Tailwind` chưa có **đường lui** lẫn **alternatives** — chỉ xuất hiện ở `ADR-001:59` (tầng MẶC ĐỊNH) và `:118` (`## Consequences` tích cực); `## Alternatives considered` (`:72-109`, **sáu** phương án A–F) ⛔ không cân nhắc UI kit nào khác | Đây là bản sửa của Founder, vừa được commit nguyên trạng theo `G-4`. Bổ sung đường lui/alternatives là **quyết định kiến trúc mới** |
| **3** | ⛔ Không ADR nào đóng `SRS-FR-26` — `ADR-015:15` nói `N` của `in_flight_per_tenant` vẫn `TBD`, ⛔ không con số nào trong repo | Đúng hiện trạng, ⛔ không phải lệch tầng |

---

_Created by TNMCORE-OS (PM)_
_Author: trisjr_
