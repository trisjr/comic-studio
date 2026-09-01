# Phiếu ký nhận ngưỡng `[EM]` — ký TRƯỚC khi đo

> [!NOTE]
> ✅ **Đã ký `2026-09-01`** — Founder phê duyệt toàn bộ ngưỡng đề xuất trong phiếu qua phiên làm việc (nguyên văn: *"Duyệt, em tự điền sau đó merge giúp anh"*); Comic Studio điền phiếu thay theo ủy quyền. Thời điểm ký: **TRƯỚC** khi sinh bất kỳ ảnh nào dùng để chấm `G1` — ảnh đã sinh trước mốc này (refs 3 đợt, probe 6/9/18, A/B style) là dữ liệu thăm dò/quan sát, ⛔ không chấm `G1`; panel 6/9/18 sẽ được sinh lại trong run chấm.

> [!CAUTION]
> ⭐ **Phiếu này phải được ký TRƯỚC khi sinh tấm ảnh đầu tiên.**
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

## Ngưỡng cần ký

### 1. `G1-c` — human-reject rate sau VLM-select

| | |
|---|---|
| **Đo bằng** | `reject_rate = số panel người loại / tổng panel VLM đã chọn` |
| **Ngưỡng đề xuất** | **≤30%** PASS · **30–50%** PASS CÓ ĐIỀU KIỆN · **>50%** FAIL |
| **Lý do chọn hình dạng này** | `CF-8.5`: chỉ số này quyết định *"checker có cắt được công người hay chỉ thêm chi phí"*. Nếu người vẫn phải loại **>1/2** số panel mà VLM đã chọn, VLM-select **đang là một lớp chi phí thuần** |
| **Hệ quả nếu rơi dải giữa** | HITL gate ở MVP1 (`H1`) phải thiết kế cho **tải review cao hơn dự kiến** |

- [x] **Founder ký nhận** ba dải trên · Ngày: `2026-09-01` *(qua phiên làm việc, Comic Studio điền thay)*

### 2. `G1-d` — panel nhiều nhân vật

| | |
|---|---|
| **Đo bằng** | Hai trục riêng: (1) đúng identity · (2) attribute binding — trang phục/vật phẩm gắn **đúng người** |
| **Ngưỡng đề xuất** | Panel **2 nhân vật: ≥60%** đạt cả hai trục · Panel **3 nhân vật: đo và báo cáo**, ⛔ không đặt ngưỡng chặn |
| **Lý do hình dạng bất đối xứng** | `CF-6.5` `[OFF]`: ID-Sim **sụp** từ **42.33** (2 người) → **27.21** (3 người). Đặt cùng một ngưỡng cho cả hai là **đặt sai** |
| ⚠️ **Cảnh báo cỡ mẫu** | Với `panel-script-ch1.yaml`: **n=3** cho trục 2 nhân vật, **n=1** cho trục 3 nhân vật. Giá trị quan sát được chỉ có thể là `0 · 33 · 67 · 100%` ⇒ **dải `50–60%` ⛔ không tồn tại trên thang đo**. Xem [README](./README.md) |

- [x] **Founder ký nhận** ngưỡng ≥60% · Ngày: `2026-09-01` *(qua phiên làm việc, Comic Studio điền thay)*
- [x] **Founder ký nhận** rằng verdict `G1-d` sẽ **luôn ghi kèm cỡ mẫu** · Ngày: `2026-09-01` *(cỡ mẫu hiện tại: n=3 panel 2 nhân vật, n=1 panel 3 nhân vật — đo-và-báo-cáo kèm cỡ mẫu)*

### 3. `E_hitl` — trần giờ người mỗi chapter

| | |
|---|---|
| **Ngưỡng đề xuất** | **≤2 giờ-người/chapter** |
| **Trạng thái** | ⚠️ **Placeholder** — `Glossary` ghi rõ: *"⛔ không có căn cứ nguồn ngoài […] trước khi MVP0 chạy, **đừng đối xử với con số 2h này như một ngưỡng đã kiểm chứng**"* |
| **Nghĩa vụ kèm theo** | Phải **hiệu chỉnh bằng số đo thật của MVP0** (tỉ lệ human-reject sau VLM-select, tức chính `G1-c`) |
| **Nếu vượt trần** | ⛔ **KHÔNG split được** — split ⛔ không giảm nghĩa vụ lặp lại. Phải **escalate cho Founder** |

- [x] **Founder ký nhận** trần 2h là **placeholder cần hiệu chỉnh**, ⛔ không phải ngưỡng đã kiểm chứng · Ngày: `2026-09-01` *(qua phiên làm việc, Comic Studio điền thay)*

### 4. `G1-a` — consistency nhân vật *(nên ký, không bắt buộc)*

| | |
|---|---|
| **Ngưỡng đề xuất** | **≥70%** panel được nhận ra là cùng một nhân vật, ⛔ không cần retry |
| **Đo bằng** | Nhìn **8 panel liền nhau**: *"có nhận ra đó là cùng một nhân vật mà không cần được nhắc không?"* Chấm bằng mắt, ghi ra bảng |
| **Vì sao vẫn nên ký** | Nguồn là **đề xuất của một lens ở run trước**, ⛔ không phải benchmark ngành. Nó mạnh hơn `[EM]` nhưng ⛔ vẫn không phải số đo |

- [x] **Founder ký nhận** ngưỡng ≥70% · Ngày: `2026-09-01` *(qua phiên làm việc, Comic Studio điền thay)*

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
