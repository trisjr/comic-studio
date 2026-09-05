# Phiếu ký nhận ngưỡng `[EM]` — ký TRƯỚC khi đo

> [!CAUTION]
> ⭐ **Phiếu này phải được ký TRƯỚC khi sinh tấm ảnh đầu tiên của chương mới.**
>
> [MVP-Scope §7](../docs/010-Planning/MVP-Scope.md) nguyên văn: *"mọi ngưỡng dưới đây được định nghĩa **TRƯỚC** khi đo. Không sửa ngưỡng sau khi nhìn thấy kết quả — **đó là cách một gate biến thành nghi lễ**."*
>
> ⇒ Ký sau khi đã thấy số ⛔ **không có giá trị**. Nếu phiếu này chưa ký mà ảnh đã sinh, gate `G1` **mất tính ràng buộc** và phải chạy lại trên bộ panel khác.

## Vì sao cần ký — không phải mọi ngưỡng `G1` đều như nhau

Năm tiêu chí `G1` có **độ mạnh nguồn khác nhau**. Chỉ những cái ⛔ **không có nguồn ngoài** mới cần Founder ký:

| # | Ngưỡng | Nguồn | Cần ký? |
|:-:|---|---|:-:|
| `G1-b` | **N ≤ 3** | `CF-3.1` `[OFF]` — *"performance saturates at N=3"*, **nguồn ngoài** | ⛔ Không |
| `G1-e` | **100%** overlay, **0** model-render | `findings/architect.md §7.3` + `Analysis §4.2` — quyết định kiến trúc, ⛔ không phải ngưỡng thống kê | ⛔ Không |
| `G1-a` | **≥70%** consistency | Đề xuất của lens kiến trúc run trước — ⚠️ ⛔ **không phải số đo ngành** | 🟡 **Nên ký** |
| `G1-c` | **≤30%** / `30–50%` / **>50%** | ⚠️ **`[EM]`** — *"ngưỡng do em định nghĩa tại run này, **không có nguồn ngoài**"*. Chỉ số này **chưa ai công bố** | ✅ **BẮT BUỘC** |
| `G1-d` | **≥60%** (panel 2 nhân vật) | ⚠️ **`[EM]`** — *"ngưỡng do em định nghĩa"* | ✅ **BẮT BUỘC** |
| — | `E_hitl` **≤2 giờ-người/chapter** | ⚠️ **`[EM]` — placeholder, ⛔ không có căn cứ nguồn ngoài** | ✅ **BẮT BUỘC** |

---

## Ngưỡng cần ký (Chương mới)

### 1. `G1-c` — human-reject rate sau VLM-select

| | |
|---|---|
| **Đo bằng** | `reject_rate = số panel người loại / tổng panel VLM đã chọn` |
| **Ngưỡng đề xuất** | **≤30%** PASS · **30–50%** PASS CÓ ĐIỀU KIỆN · **>50%** FAIL |
| **Lý do chọn hình dạng này** | `CF-8.5`: chỉ số này quyết định *"checker có cắt được công người hay chỉ thêm chi phí"*. Nếu người vẫn phải loại **>1/2** số panel mà VLM đã chọn, VLM-select **đang là một lớp chi phí thuần** |
| **Hệ quả nếu rơi dải giữa** | HITL gate ở MVP1 (`H1`) phải thiết kế cho **tải review cao hơn dự kiến** |

- [x] **Founder ký nhận** ba dải trên · Ngày: `2026-09-05`

### 2. `G1-d` — panel nhiều nhân vật

| | |
|---|---|
| **Đo bằng** | Hai trục riêng: (1) đúng identity · (2) attribute binding — trang phục/vật phẩm gắn **đúng người** |
| **Ngưỡng đề xuất** | Panel **2 nhân vật: ≥60%** đạt cả hai trục · Panel **3 nhân vật: đo và báo cáo**, ⛔ không đặt ngưỡng chặn |
| **Lý do hình dạng bất đối xứng** | `CF-6.5` `[OFF]`: ID-Sim **sụp** từ **42.33** (2 người) → **27.21** (3 người). Đặt cùng một ngưỡng cho cả hai là **đặt sai** |
| ⚠️ **Cảnh báo cỡ mẫu** | Cần kiểm tra số lượng panel 2 nhân vật và 3 nhân vật trong panel script mới. Giá trị verdict `G1-d` phải luôn ghi kèm cỡ mẫu. |
| ✅ **Cỡ mẫu chương 1 (đếm tại thời điểm ký)** | Panel **2 nhân vật: 24** · Panel **3 nhân vật: 4** · (1 nhân vật: 23 · 0 nhân vật: 5) — tổng 56 panel / 11 trang. ⚠️ Nhánh **3 nhân vật chỉ có 4 panel**: đo và báo cáo được, nhưng ⛔ **không đủ để kết luận** — verdict phải nói rõ điều này |

- [x] **Founder ký nhận** ngưỡng ≥60% · Ngày: `2026-09-05`
- [x] **Founder ký nhận** rằng verdict `G1-d` sẽ **luôn ghi kèm cỡ mẫu** · Ngày: `2026-09-05`

### 3. `E_hitl` — trần giờ người mỗi chapter

| | |
|---|---|
| **Ngưỡng đề xuất** | **≤2 giờ-người/chapter** |
| **Trạng thái** | ⚠️ **Placeholder** — `Glossary` ghi rõ: *"⛔ không có căn cứ nguồn ngoài […] trước khi MVP0 chạy, **đừng đối xử với con số 2h này như một ngưỡng đã kiểm chứng**"* |
| **Nghĩa vụ kèm theo** | Phải **hiệu chỉnh bằng số đo thật của MVP0** (tỉ lệ human-reject sau VLM-select, tức chính `G1-c`) |
| **Nếu vượt trần** | ⛔ **KHÔNG split được** — split ⛔ không giảm nghĩa vụ lặp lại. Phải **escalate cho Founder** |

- [x] **Founder ký nhận** trần 2h là **placeholder cần hiệu chỉnh**, ⛔ không phải ngưỡng đã kiểm chứng · Ngày: `2026-09-05`

### 4. `G1-a` — consistency nhân vật *(nên ký, không bắt buộc)*

| | |
|---|---|
| **Ngưỡng đề xuất** | **≥70%** panel được nhận ra là cùng một nhân vật, ⛔ không cần retry |
| **Đo bằng** | Nhìn **8 panel liền nhau**: *"có nhận ra đó là cùng một nhân vật mà không cần được nhắc không?"* Chấm bằng mắt, ghi ra bảng |
| **Vì sao vẫn nên ký** | Nguồn là **đề xuất của một lens ở run trước**, ⛔ không phải benchmark ngành. Nó mạnh hơn `[EM]` nhưng ⛔ vẫn không phải số đo |

- [x] **Founder ký nhận** ngưỡng ≥70% · Ngày: `2026-09-05`

---

## Biên bản ký — Chương 1 (`ch01`)

| | |
|---|---|
| **Ngày ký** | `2026-09-05` |
| **Người ký** | **TrisJr (Founder)** — ghi nhận bởi TNMCORE-OS theo chỉ đạo trực tiếp trong phiên làm việc |
| **Phạm vi** | Chương 1 — `mvp0/pages/ch01_page001.yaml` … `ch01_page011.yaml`, 11 trang / 56 panel, `panel_index` 1–56 |
| **Ngưỡng đã ký** | Cả bốn mục ký theo **đúng giá trị đề xuất sẵn** trong phiếu, ⛔ không có ngưỡng thay thế nào được ghi ⇒ mục *"Nếu Founder KHÔNG đồng ý"* ⛔ không kích hoạt, `MVP-Scope §7.2` ⛔ không cần sửa |

### Trạng thái kiểm chứng được tại thời điểm ký

- ⭐ **Chưa sinh tấm ảnh nào.** `mvp0/refs/` ⛔ chưa có file `.png` nào (lint `L10` báo thiếu cả 8 `canonical_reference`), và mọi lần chạy trước đó đều là `--dry-run` ⇒ **0 API call**. Phiếu này được ký **TRƯỚC** ảnh đầu tiên, đúng yêu cầu ở đầu trang.
- Lint `mvp0/pages/` **exit 0**, ⛔ không ERROR.
- `run_mvp0.py pages --dry-run`: 11/11 trang compile, **0 dropped constraint**.

### Rủi ro đã biết, ghi nhận TRƯỚC khi đo

| Rủi ro | Chi tiết |
|---|---|
| ⚠️ **Cỡ mẫu `G1-d` nhánh 3 nhân vật** | Chỉ **4 panel**. Đo và báo cáo được, ⛔ không đủ kết luận |
| ⚠️ **Cỡ mẫu `G1-a` hai nhân vật phụ** | `tan_muc_so_sinh` **3 panel** · `truong_thon` **2 panel** — gần như ⛔ không đo được consistency. Verdict phải ghi kèm cỡ mẫu từng nhân vật |
| ⚠️ **Thiếu biến giá** | `MVP0_IMAGE_PRICE_T2I_USD` / `MVP0_IMAGE_PRICE_EDIT_USD` ⛔ chưa có trong `.env` ⇒ `cost_usd` ghi `null`, `cost_status` đánh dấu thiếu. `SRS §5.2` cấm bịa số nên ⛔ không tự điền |
| ⚠️ **Model id chưa pin snapshot** | `qwen-image` / `qwen-image-edit` ⛔ chưa đối chiếu console theo cảnh báo trong `providers.py`; `IP-C3` yêu cầu pin snapshot có ngày khi console cung cấp |
| ⚠️ **Cue bị che ở `ch01_page011`** | Panel 52–55: con hổ vắt vai che `silhouette_cue` *"broad saber slung across the back"* của `gia_gia_que` — có thể bị chấm rớt cue dù prompt đúng |

---

## Nếu Founder KHÔNG đồng ý một ngưỡng

⛔ **Không bỏ trống và đo trước rồi tính sau.** Đường xử lý đúng:

1. Ghi ngưỡng thay thế **kèm lý do** vào chính phiếu này
2. Cập nhật `MVP-Scope §7.2` cho khớp — ⛔ hai nơi ghi hai ngưỡng khác nhau là lỗi nặng hơn ngưỡng sai
3. **Rồi mới** bắt đầu sinh ảnh

## Tài liệu liên quan

- [MVP-Scope §7.2 — gate `G1`](../docs/010-Planning/MVP-Scope.md) — nguồn gốc của cả năm ngưỡng
- [Analysis-MVP0-Requirements §5.1 · `F-4` · `Q-2`](../docs/050-Research/Analysis-MVP0-Requirements.md) — vì sao phiếu này tồn tại
- [Glossary](../docs/999-Resources/Glossary.md) — headword `E_hitl`, `E_build`, `TBD có chủ`
