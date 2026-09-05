<!-- AI Coding -->

# Nhật ký chọn canonical reference — MVP0

> [!IMPORTANT]
> ⚠️ **Trạng thái: ĐÃ ĐỀ XUẤT ĐỦ 8/8 — chương 1 (`ch01`) · CHỜ FOUNDER XÁC NHẬN** · Ngày `2026-09-05`
>
> | | |
> |---|---|
> | **Tiêu chí chọn** | Founder chốt — **Hướng A** (xem [§2](#2-tiêu-chí-chọn-đã-dùng)) |
> | **Áp tiêu chí & đề xuất** | TNMCORE-OS |
> | **Founder đã xem ảnh?** | ⛔ **Chưa** — phải xác nhận **trước khi** chạy `run_mvp0.py pages` |
>
> [Chay-MVP0 Bước 2](../../docs/060-Manuals/User-Guide/Chay-MVP0.md): Chọn canonical reference là *"việc của con người — ⛔ không giao cho máy"*. ⇒ Máy chỉ được **đề xuất**; ⛔ dòng nào chưa có mắt người nhìn qua thì ⛔ không được ghi là đã duyệt.
> Sau khi chạy `python3 scripts/mvp0/run_mvp0.py refs`, người vận hành/Founder duyệt ảnh candidate trong `mvp0/run-refs-<timestamp>/candidates/`, lưu thành `mvp0/refs/<char_id>.png` và ghi log vào bảng dưới đây.

## Mục lục

- [1. Bảng ghi nhận Canonical References — `ch01`](#1-bảng-ghi-nhận-canonical-references--ch01)
- [2. Tiêu chí chọn đã dùng](#2-tiêu-chí-chọn-đã-dùng)
- [3. Ứng viên bị loại — lý do](#3-ứng-viên-bị-loại--lý-do)
- [4. Ngân sách API đã tiêu](#4-ngân-sách-api-đã-tiêu)
- [5. Tài liệu tham khảo](#5-tài-liệu-tham-khảo)

---

## 1. Bảng ghi nhận Canonical References — `ch01`

| char_id | File nguồn (provenance) | Lý do đề xuất / phê chuẩn | Trạng thái |
|---|---|---|---|
| `tu_ba_ba` | `run-refs-20260905-152001/candidates/tu_ba_ba-c2.png` | Nhất quán nhất giữa 4 góc nhìn; đúng mặt, áo chàm, tạp dề xám, túi kim, khăn bịt đầu | ⭐ Đề xuất · ⚠️ thiếu lưng gù (xem [`g1-verdict.md` §4](../golden-dataset/g1-verdict.md)) |
| `ma_lao` | `run-refs-20260905-154113/candidates/ma_lao-c0.png` (run sửa) | Giữ đúng phong cách 2D manhwa; ⛔ hết mảnh xương rời của bản gốc | ⭐ Đề xuất · ⚠️ vẫn đủ hai tay |
| `gia_gia_que` | `run-refs-20260905-154256/candidates/gia_gia_que-c2.png` (run sửa) | Góc lưng đọc rõ **cả** đao bản rộng đeo chéo **lẫn** gậy gỗ — đúng `silhouette_cue` cần cho `ch01_page011` | ⭐ Đề xuất · ⚠️ vẫn đủ hai chân |
| `truong_thon` | `run-refs-20260905-153930/candidates/truong_thon-c2.png` (run sửa) | Bố cục sạch, đúng tư thế nằm trên cáng tre, áo trắng và tóc/râu bạc dài; ⛔ hết mảnh xương rời | ⭐ Đề xuất · ⚠️ vẫn đủ tay chân |
| `tan_muc_so_sinh` | `run-refs-20260905-152001/candidates/tan_muc_so_sinh-c0.png` | Đúng trẻ sơ sinh quấn tã, ngọc bội phát sáng xanh nhạt | ⭐ Đề xuất |
| `tan_muc_thieu_nien` | `run-refs-20260905-172723/candidates/tan_muc_thieu_nien-c2.png` (run sửa tuổi) | ⛔ Không còn là thanh niên 18–20 như bản gốc; ⛔ không có chữ cháy vào ảnh; nhất quán 4 góc nhìn | ⭐ Đề xuất · ⚠️ lệch tuổi (~7–9 thay vì 11) là **loại 2**, ⛔ không sửa được bằng chữ ở tầng `refs` |
| `yeu_phu_nguoi` | `run-refs-20260905-152001/candidates/yeu_phu_nguoi-c1.png` | Tóc rối che nửa mặt ✓ · vệt liền da đỏ quanh đùi rõ ✓ · áo lụa rách ẩm bết ✓ | ⭐ Đề xuất |
| `yeu_phu_bo` | `run-refs-20260905-154439/candidates/yeu_phu_bo-c0.png` (run sửa) | Đúng con bò bốn chân nhìn nghiêng, da trần, dây thừng mũi bện; ánh mắt mang nét người | ⭐ Đề xuất |

> [!WARNING]
> ⚠️ **Mọi dòng có `⚠️` ⛔ KHÔNG được chấm vào `G1-a`.** Đó là hạn chế đã có sẵn trong ảnh reference lúc chọn, ⛔ không phải lỗi nhất quán của model ở tầng page. Phân loại đầy đủ nằm ở [`g1-verdict.md` §4](../golden-dataset/g1-verdict.md).

## 2. Tiêu chí chọn đã dùng

Founder chốt **Hướng A**: chọn theo **mặt / tóc / trang phục**, chấp nhận tầng `refs` ⛔ không tả được chi thể bị cụt, để tầng `pages` (có khối `NEGATIVE_CONSTRAINTS`) quyết.

Thứ tự ưu tiên khi hai ứng viên ngang nhau:

1. ⛔ **Không có chữ cháy vào ảnh** — ảnh reference có chữ hoặc bong bóng thoại là mầm rủi ro cho `G1-e` (*100% overlay · 0 model-render*).
2. **Giữ đúng phong cách 2D manhwa** của `BASE_STYLE_CORE` — ứng viên trôi sang nét hoạt hình phương Tây bị loại.
3. **Đọc được `silhouette_cue`** ở góc nhìn mà chương thật sự cần.
4. **Nhất quán giữa 4 góc nhìn** trong cùng một model sheet.

## 3. Ứng viên bị loại — lý do

| Ứng viên | Lý do loại |
|---|---|
| `yeu_phu_nguoi-c2` | Có **bong bóng thoại + chữ Hán cháy vào ảnh** — vi phạm tiêu chí 1 |
| `tan_muc_thieu_nien-c1` (run sửa) | Có chữ `Qin Mu:` và chữ Hán cháy vào ảnh — vi phạm tiêu chí 1 |
| `ma_lao-c1`, `ma_lao-c2` (run sửa) | Trôi sang nét hoạt hình phương Tây, lệch `BASE_STYLE_CORE` — vi phạm tiêu chí 2 |
| `truong_thon-c1` (run sửa) | Có thêm góc nhìn nửa người để trần ⛔ không cần, bố cục nhiễu hơn `c2` |
| `tan_muc_thieu_nien-c0` (run sửa) | Mặt đọc ra trẻ hơn `c2`, càng xa mốc 11 tuổi |
| Toàn bộ `tan_muc_thieu_nien` run gốc (`152001`) | Cả 3/3 ra **thanh niên 18–20** — sai loại 1, đã sửa bằng cách đưa tuổi vào `canonical_reference_en.khuon_mat` |
| Toàn bộ `tan_muc_thieu_nien` run neo chiều cao (`183740`) | Tỉ lệ đầu/thân ⛔ **không đổi** so với `172723`, mà 3/3 lại sinh thêm **băng vải quấn tay** ⛔ không có trong bible ⇒ nhiều sai lệch hơn. Chi tiết ở [`g1-verdict.md` §4.2b](../golden-dataset/g1-verdict.md) |

## 4. Ngân sách API đã tiêu

| Run | Nhân vật | Số call | Ghi chú |
|---|---|:-:|---|
| `run-refs-20260905-152001` | cả 8 | 24 | Run gốc |
| `run-refs-20260905-153930` | `truong_thon` | 3 | Sửa lối viết phủ định → khẳng định |
| `run-refs-20260905-154113` | `ma_lao` | 3 | Sửa lối viết phủ định → khẳng định |
| `run-refs-20260905-154256` | `gia_gia_que` | 3 | Sửa lối viết phủ định → khẳng định |
| `run-refs-20260905-154439` | `yeu_phu_bo` | 3 | Bổ sung hình dạng bốn chân vào `dac_diem_rieng` |
| `run-refs-20260905-172723` | `tan_muc_thieu_nien` | 3 | Bổ sung tuổi vào `khuon_mat` / `dac_diem_rieng` — ✅ hết người lớn 18–20 |
| `run-refs-20260905-183740` | `tan_muc_thieu_nien` | 3 | Thử neo chiều cao *"shoulder-high to an adult"* — ⛔ **thất bại**, ⛔ không chọn ảnh nào |
| **Tổng** | | **42** | 0 refusal |

## 5. Tài liệu tham khảo

| Tài liệu | Dùng khi |
|---|---|
| [Chay-MVP0 Bước 2](../../docs/060-Manuals/User-Guide/Chay-MVP0.md) | Quy trình chọn canonical reference |
| [`g1-verdict.md` §4](../golden-dataset/g1-verdict.md) | Phân loại đầy đủ hai loại lỗi và sai lệch tồn đọng |
| [`story-bible.yaml`](../story-bible.yaml) | Nguồn sự thật cho mọi mô tả nhân vật |
| [`threshold-signoff.md`](../threshold-signoff.md) | Ngưỡng `G1` đã ký trước khi sinh ảnh thật |

---

_Created by TNMCORE-OS_
_Author: trisjr_
