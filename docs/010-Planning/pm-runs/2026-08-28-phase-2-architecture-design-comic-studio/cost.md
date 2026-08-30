---
id: COST-P2
type: reference
status: final
project: comic-studio
created: 2026-08-30
---

# Chi phí & bài học — run Phase 2 Architecture Design

## 1. Sản lượng

| Tầng | File | Ghi chú |
|---|:--:|---|
| `docs/030-Specs/Architecture/` | **19** | 1 SDD (5 sơ đồ Mermaid) + 18 ADR |
| `docs/030-Specs/Schema/` | **14** | 14 ER diagram Mermaid; 0 Postgres enum type |
| `docs/030-Specs/API/` | **21** | 14 `Endpoint-*` + 7 `Spec-Integration-*` |
| `docs/030-Specs/Security/` | **3** | Đã qua **review độc lập** |
| `docs/030-Specs/Specs-MOC.md` | **1** | Viết mới, index 57/57, 0 link gãy |
| Sửa đổi | **3** | `SRS` (+7 hàng §5.2) · `Glossary` (+21 headword) · `000-Index` |

**Tổng: 58 tài liệu mới**, ~16.700 dòng. **~35 lô**, **25 escalation** ghi sổ.

## 2. Năm bài học đắt nhất — đưa vào `pm-core.md`

### `L-1` ⛔ Không dispatch lô SỬA nguồn-sự-thật song song với lô ĐỌC nguồn đó
`L0` (sửa `SRS`) chạy cùng `L1`/`L2` (đọc `SRS`) ⇒ **ba hệ toạ độ số dòng**.

⚠️ **Đính chính (đo lại 2026-08-30): tốn 8 lô, ⛔ không phải 7 — vì phải dọn HAI đợt.**
- **Đợt 1 — 7 lô** (`L23a`…`L23f` + `L24`): xác định phạm vi bằng một `grep` **chỉ bắt `SRS`**.
- **Đợt 2 — 1 lô**: sau khi một lô audit đếm ra **217 chỗ còn sót trên 10 file** (trích dẫn tới `MVP-Scope` và file khác), `L36` phải quét lại — **202 turn, 160 tool call, $24: lô đắt nhất toàn run**.

> ⚠️ Lô audit phát hiện ra 217 chỗ ⛔ **không** được tính vào con số 8 lô này: ⛔ không tách được nó khỏi các lô verify bằng bằng chứng (`grep "217"` trúng gần như mọi transcript nên vô dụng), và nếu nó là `L21` thì đã nằm ở nhóm **verify** của §6.3.

⇒ Tổng **≈ $90 = 20,9% chi phí subagent**, cho một lỗi lập lịch mất 10 giây để tránh. ⭐ Và đợt dọn đầu tiên **tự nó phạm `L-2`**: phạm vi lấy từ một grep hẹp, ⛔ không đo lại sau khi sửa.

### `L-2` ⛔ PM chỉ được khẳng định về nội dung file SAU khi đã tự đọc file đó
Vi phạm **4 lần**: `E9` (suýt quyết gate trên tiền đề sai) · `E12` (truyền bảng mapping chưa verify cho 3 lô) · `E15` · và `E23` (grep **phân biệt hoa/thường** ⇒ đếm sót 4/5 vị trí, ra lệnh sai cho worker).
⭐ **Hệ quả cụ thể**: mọi `grep` dùng làm **căn cứ quyết định** phải chạy `-i`, và phải **kiểm mẫu tìm kiếm có bắt hết biến thể không** — enum type ở dự án này đặt tên **không** có hậu tố `_enum`, nên grep hẹp bỏ sót 9/9.

### `L-3` ⛔ Fan-out KHÔNG tự bắt được mục bị bỏ sót
Mỗi worker chỉ thấy phần của mình ⇒ thứ **không thuộc lô nào** thì **không ai báo thiếu**.
- `E16`: 2 entity `[24⭐]` rơi khỏi bảng gom cụm ⇒ suýt mất schema.
- `E24`: seam `S-4` (phân biệt chi phí BYOK) — `SDD` **bắt buộc** ở §8.2, nhưng mọi lô Schema chỉ được trỏ tới §3.x ⇒ **không lô nào có §8.2 trong nguồn**.
⇒ ⭐ **PM phải chạy một phép diff cơ học** giữa danh sách nguồn và bảng phân lô, **và** phải kiểm nguồn đã cấp có phủ hết mục nguồn bắt buộc không.

### `L-4` ⛔ Ghi việc vào sổ escalation KHÔNG đảm bảo việc đó vào prompt
`E21` giao `CO-EX-2` cho L25a; prompt PM gửi L25a liệt 5 hạng mục và **bỏ sót đúng hàng đó**. Nó nằm im tới khi L14 độc lập gặp lại.
⇒ **Đối chiếu sổ ↔ prompt trước mỗi dispatch.**

### `L-5` ⭐ Khi tiêu chí gate nói *"X được **review** bởi vai trò R"* mà lô sản xuất cũng là R ⇒ PHẢI chạy lô R thứ hai
PM đã tick *"Security Spec đã được Security Auditor review"* trong khi chính `security-auditor` **viết** ba file đó. `L22` gọi tên. Lô `L31` (context mới) tìm ra **hai thứ tác giả về nguyên tắc không thể thấy**:
- Bề mặt operator xuyên tenant — **sinh ra ở tầng API SAU khi threat model được viết**.
- `C-3` là **lời hứa**: nó giao cho *"lô API"* đóng danh sách *"mọi đường đọc"*; lô API chạy xong mà 4 file ⛔ không nhắc `access_state` ⇒ **nội dung đã takedown vẫn đọc được theo đặc tả**.
⭐ ⛔ Cùng một agent role ⛔ **không tự review được đầu ra của chính nó** — ⛔ không phải vì cẩu thả, mà vì **giả định của nó là điểm mù của nó**.

## 3. ⭐ Năm lần worker ĐÚNG hơn PM — mẫu hành vi cần giữ

| Lô | Nó làm gì |
|---|---|
| `L10` | Giải bài toán **và tự đánh dấu** rằng cách đọc phép đo cần PM xác nhận ⇒ PM verify AC nguyên văn và **lật kết luận**. Nếu nó im lặng, `E19` đã lọt |
| `L25a` | PM bảo *"L9 kết luận chỉ `G-6` bị chạm"* ⇒ nó **tự kiểm** và tìm ra chạm **cả `G-5`**: dòng `request` bị ép mang `cost_status='unknown_provider_error'`, một **khẳng định sai** làm hệ thống tự báo cáo sai tỉ lệ lỗi provider |
| `L28a` | PM ra lệnh *"sửa một dòng"* dựa trên một grep sai ⇒ nó tìm ra **5 vị trí**, sửa đủ và **báo lại**, thay vì im lặng làm theo lệnh sai |
| `L34` | PM bảo *"gỡ khoá 6 field"* ⇒ nó gỡ 4, **giữ 2** vì chúng ⛔ không nằm trong tập mỏ neo của `edit_panel_field` — áp nguyên tắc *"⛔ không tái dụng thầm lặng"* **ngược lại lệnh của PM** |
| `L36` | PM chỉ định sai **độ hạt** (cột duyệt bible đặt lên `bible_entity` project-scoped, trong khi `SB-7` là chapter-scoped) ⇒ nó **dừng lại hỏi**, đưa 3 phương án và **tự đánh dấu cái nó không khuyến nghị** chính là cái làm theo lệnh PM |

⇒ ⭐ **Điểm chung**: prompt luôn nói rõ *"⛔ nếu tìm được nguồn nói ngược thì BÁO CÁO, ⛔ đừng tự áp"* và *"⛔ đừng tin bảng này, tự verify"*. **Cho worker quyền bác PM là thứ đã cứu run này nhiều lần nhất.**

## 4. Hai chỗ PM cố ý KHÔNG hành động

| Việc | Vì sao ⛔ không làm |
|---|---|
| Nâng `INV-14` thành `CHECK` liên cột | Worker có **lập luận cụ thể** và tự khai *"vắng mặt constraint là chủ ý"*. PM chỉ có **phân tích nhanh**, ⛔ không phải bằng chứng ngược. ⭐ Lật một quyết định có lập luận bằng trực giác PM **chính là hình dạng của `E9`** |
| Thêm role `app_operator` vào `SDD` §7.4 | Đó là **thay đổi mô hình quyền**, ⛔ không phải ripple tài liệu. Ghi thành nợ kỹ thuật số 2, và ghi rõ **`TD-2`/`TD-3` vẫn bị chặn** |

## 5. Trạng thái 5 tiêu chí thoát Phase 2

| # | Tiêu chí | |
|:--:|---|---|
| 1 | SDD có sơ đồ kiến trúc | ✅ 5 khối Mermaid |
| 2 | ≥1 ADR cho tech stack | ✅ `ADR-001` |
| 3 | API Specs cover Use Case chính | ⚠️ **Còn 2 bước hở**: `UC-02` b1/`EXC-1` (kích hoạt/retry extraction) và `UC-07` b3 (auto-placement bubble) — cả hai **tự khai trong file**, có mã `TBD` và chủ |
| 4 | DB Schema normalized + ER Diagram | ✅ 14/14 |
| 5 | Security Spec được Security Auditor review | ✅ **review độc lập** (`L31`), 4 điều kiện thoát đã đóng |

⚠️ **Tiêu chí #3 chưa trọn.** Hai bước hở ⛔ không phải lỗi ẩn — chúng có mã, có chủ, và nằm ở chỗ findings §4.1 ⛔ không liệt kê resource nào phục vụ. Quyết định mở/đóng gate là của **Founder**, ⛔ không phải của PM.

## 6. Post-mortem token — đo lại 2026-08-30

> ⚠️ Mục này ⛔ không có lúc đóng run. Nó phải dựng lại từ transcript ở một session sau, vì close-step *"đo chi phí thật (BẮT BUỘC)"* của `pm-core.md` đã **bị bỏ qua** — file đó bị xoá nhầm ở commit `90a990f`. Đã khôi phục và bổ sung công cụ đo.

### 6.1 Tiền thật ≈ $710 — con số hiển thị chỉ phủ 39%

| Tầng | Nguồn | Chi phí |
|---|---|---:|
| PM main loop | `cost-state` — **đo được** | $193,95 |
| `advisor` (93 lần, `fable-5`) | `cost-state` — **đo được** | $84,91 |
| **46 subagent** | ⛔ **không có trong `cost-state`** — ước lượng | **≈ $431** |
| | | **≈ $710** |

`cost-state` ghi `totalCostUSD: 278,85`, và $193,95 + $84,91 khớp **chính xác** con số đó ⇒ nó chỉ phủ main loop + `advisor`. ⭐ **61% chi phí thật nằm ở subagent và ⛔ không được kế toán.**

Đơn giá hiệu chuẩn ngược từ chính `cost-state`: `$5/$25/$0,5/$6,25` per MTok (in/out/cache-read/cache-write), sai số dư **2,3%**. Thời gian: 15 giờ wall-clock, 8,76 giờ API.

### 6.2 Vì sao tốn — `turns × context mỗi turn`

| | turns | context `p50` | context `p90` | cache-read | **$ / turn** |
|---|--:|--:|--:|--:|--:|
| PM main loop | 613 | **272k** | 428k | 164,8M | **0,316** |
| 46 worker | 3.705 | 106k | 199k | 415,3M | 0,115 |
| | | | | **580M** | |

580 triệu token đọc lại, để giữ 58 file / 16.441 dòng. **PM đắt gấp 2,75 lần worker mỗi turn**, và tự làm **210 tool call tay chân** (129 `Bash` · 53 `Edit` · 28 `Read`) so với chỉ 46 `Agent` ⇒ ước **$67** chỉ để tự `grep`/`Edit`.

### 6.3 415M token của worker đi đâu

| Nhóm | cache-read | output | **chi phí** | Đánh giá |
|---|--:|--:|--:|---|
| Sản xuất nội dung | 202,0M (48,7%) | 1,64M | **$214** | Bắt buộc |
| **Dọn trích dẫn số dòng** | 88,4M (21,3%) | 0,52M | **$90** | ⛔ **Lãng phí thuần** — xem `L-1` |
| Rework sau escalation | 96,1M (23,1%) | 0,42M | **$99** | Một phần tránh được |
| Verify độc lập | 28,7M (6,9%) | 0,11M | **$28** | ⭐ **ROI cao nhất run** |

> ⛔ **KHÔNG đọc "51% ⛔ không sinh nội dung mới" thành "cắt đi".** $28 verify là khoản **sinh lời nhất**: `L31` tìm ra lỗ `C-3` (nội dung đã takedown vẫn đọc được theo đặc tả) và bề mặt operator xuyên tenant. Cắt verify là cách rẻ nhất để phá hỏng run sau.

### 6.4 ⭐ Run này PHỦ ĐỊNH luật `turns^1.74` của `pm-core.md`

Hồi quy log-log trên 46 subagent: **`k = 0,94`, `R² = 0,50`** (bỏ outlier: `k = 0,92`). Chi phí mỗi turn gần **hằng số**: 0,119 / 0,122 / 0,110 / 0,110 qua bốn nhóm kích thước.

⇒ Chi phí là **hai chế độ**, ⛔ không phải một luật: **lô ⛔ không cắt ⇒ `turns^1.74`** (lane code, agent 621 turn) · **lô cắt ngắn ⇒ gần tuyến tính** (lane doc, context worker `p50` 106k / `p90` 199k). `pm-core.md` đã được sửa thành hai chế độ.

⭐ **Cơ chế là việc CẮT LÔ, ⛔ không phải việc thi hành trần.** Bằng chứng quyết định: cả **3 lô của nhóm ≥130 turn đều VƯỢT trần** (77 · 77 · 160 tool call) mà `$/turn` vẫn **thấp nhất bảng** (0,110) ⇒ tuyến tính giữ được **ngay cả trong lô phá trần**. Trần là **tín hiệu dừng**; cắt lô mới là thứ bẻ đường cong.

⚠️ Và **cấp trần ≠ thi hành trần**: ngân sách có mặt trong **46/46 dispatch prompt** (đã grep), vậy mà **8/46 lô vượt trần**, tiêu **$102 = 24% chi phí subagent**, ⛔ không lô nào bị chặn hay báo `PARTIAL`.

### 6.5 Năm đòn bẩy — ước tiết kiệm ~$220 (31%)

| # | Đòn bẩy | Tiết kiệm |
|---|---|--:|
| 1 | PM ⛔ không tự làm việc cơ học — mọi `grep`/sweep → worker context sạch | ~$60 |
| 2 | Freeze nguồn trước fan-out (`L-1`) | ~$90 |
| 3 | Lô quét cắt theo **số chỗ sửa** (≲50), ⛔ không theo số file; đo lại sau khi sửa | Tránh đợt dọn thứ 2 |
| 4 | `advisor` theo chính sách: lô quyết định có, lô cơ học ⛔ không | ~$40 |
| 5 | PM `/compact` sớm hơn — `p90` = 428k là quá muộn | ~$30 |

⛔ **KHÔNG khuyến nghị**: giảm số lô hay gộp worker. 46 worker × 106k rẻ hơn nhiều so với một PM 272k ôm hết — kiến trúc fan-out **đúng**; cái sai là PM ôm việc tay chân và lịch dispatch.

## 7. Tài liệu tham khảo

- [escalations.md](./escalations.md) — 25 mục `E1`…`E25`
- [outline.md](./outline.md) — bảng tick 63 hạng mục
- [Specs-MOC](../../../030-Specs/Specs-MOC.md) — bản đồ 57 tài liệu
