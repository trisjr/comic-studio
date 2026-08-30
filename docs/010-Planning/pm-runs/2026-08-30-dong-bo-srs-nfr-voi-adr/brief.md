---
id: BRIEF-2026-08-30-DONG-BO-SRS-NFR-VOI-ADR
type: run-brief
run: 2026-08-30-dong-bo-srs-nfr-voi-adr
lane: doc
shape: B
tier: T3
status: gate-pending
created: 2026-08-30
---

# Brief — Đồng bộ lệch tầng `SRS` (020) ↔ `ADR` (030)

## Mục lục

- [1. Yêu cầu gốc](#1-yêu-cầu-gốc)
- [2. Shape và Triage](#2-shape-và-triage)
- [3. Assumptions](#3-assumptions)
- [4. Phạm vi đề xuất mang ra gate](#4-phạm-vi-đề-xuất-mang-ra-gate)
- [5. Rủi ro đã nhận diện](#5-rủi-ro-đã-nhận-diện)

## 1. Yêu cầu gốc

Nguyên văn của anh:

> ⚠️ **`SRS-NFR-09` (tầng 020) vẫn ghi framework frontend `CHƯA QUYẾT → TBD`** trong khi `ADR-001` (tầng 030) đã chốt `shadcn/ui + Tailwind`. Lệch tầng, cần run đồng bộ 020↔030
>
> Đồng bộ lại giúp anh

Nguồn của phát biểu này: [`docs/000-Index.md`](../../../000-Index.md) hàng rủi ro số **5** — chính là hạng mục nợ do run `2026-08-30-brand-guidelines-va-design-system-comic-studio` ghi nhận và cố ý để lại.

## 2. Shape và Triage

**Shape B — Normalization sweep.** ⛔ Không tạo tài liệu mới. Toàn bộ việc là **sửa hàng loạt phát biểu đã tồn tại** cho khớp nhau giữa hai tầng. Rủi ro đặc trưng của Shape B áp dụng nguyên vẹn: **sửa nửa vời ⇒ kho docs mâu thuẫn với chính nó**.

| # | Câu hỏi triage (lane doc) | Đáp | Căn cứ |
|:--:|---|:--:|---|
| **Q1** | Chạm nhiều hơn một tầng tài liệu? | ✅ **Có** | `020-Requirements` (SRS) + `030-Specs` (Architecture · Security · API · Schema) + `000-Index.md` |
| **Q2** | Sửa tài liệu `approved`, hoặc đổi taxonomy / naming / template dùng chung? | ⛔ **Không** | `SRS:4` = `status: draft`; `ADR-001…004:4` = `status: draft`. ⛔ Không đụng RULE-001, ⛔ không đổi cấu trúc Dewey |
| **Q3** | Yêu cầu mơ hồ — chưa rõ "thế nào là xong"? | ✅ **Có** | Anh nêu **một** mã (`SRS-NFR-09`), nhưng `SRS-NFR-07`/`SRS-NFR-08` **cùng một loại lệch tầng**. Ranh giới "xong" phụ thuộc quyết định phạm vi ⇒ đẩy lên gate |
| **Q4** | Vượt 5 file hoặc 1 ngày công? | ✅ **Có** — *tính điểm* | Phương án hẹp nhất đã là **1 file 020 + 4 điểm 030 + `000-Index`**; phương án rộng là **1 + 11 + 1**. Q4 tính điểm vì Q1 = Có (và Shape B luôn tính) |

**Điểm 3/4 ⇒ `T3`.** Đường đi: analysis fan-out ✅ (đã xong) → **GATE** → outline → sweep nhiều writer → verify bởi agent khác → close-step đầy đủ gồm `000-Index.md`.

> [!NOTE]
> ⭐ **Bước 2 đã hoàn tất trước khi viết brief này.** Lens `architect` (read-only, 60 tool call) đã trả về [`findings/architect.md`](./findings/architect.md) — 375 dòng, ánh xạ đủ 4 câu hỏi PM đặt. ⛔ Không cần lens thứ hai: lô này ⛔ không có thành phần nghiệp vụ, thiết kế hay dữ liệu ngoài; nó thuần **nhất quán phát biểu kiến trúc**.

## 3. Assumptions

| # | Giả định | Trạng thái |
|:--:|---|---|
| **1** | Bản `ADR-001` dùng làm nguồn là **bản chưa commit** của Founder (có `shadcn/ui + Tailwind`), đã sync vào worktree này làm input read-only. `grep -c shadcn` = **2** | ⚠️ **Chặn** — xem `Q-4` ở gate |
| **2** | `ADR-001` **là nơi đóng** `SRS-NFR-09` — ⛔ không phải suy diễn. Bằng chứng: `ADR-001:168` có heading `### ADR này quyết (phần Phase 1 cố ý để mở)`, hàng đầu bảng `:172` chính là `SRS-NFR-09` | ✅ Đã verify 2 lần (PM + lens) |
| **3** | ⛔ **Không hàng nào trong `NFR-07/08/09` trở thành `CHỐT` thuần.** Cả bốn ADR đều tự khai có **tầng MẶC ĐỊNH kèm đường lui** ⇒ theo định nghĩa `SRS:50`, chúng là **MẶC ĐỊNH** hoặc **LAI**, ⛔ không phải CHỐT | ✅ Lens verify từ `ADR-001:52`, `ADR-002:60`, `ADR-003:57`, `ADR-004:66` |
| **4** | ⭐ **PM đã sai một tiền đề, lens bác đúng.** PM viết *"đóng một hàng `TBD` làm sai **cả ba** con số ở `SRS:345`"*. ⛔ Sai: con số đầu là **`CHỐT` thuần = 55** và nó **đứng yên trong mọi phương án** (hệ quả trực tiếp của giả định 3). Chỉ **2/3** con số đổi | ✅ **Đã sửa** — ghi lại ở đây để lô sau ⛔ không lặp |
| **5** | ⛔ **`C-10` (cơ chế render an toàn) KHÔNG tự đóng theo.** Nó vẫn mở, nhưng **vì lý do khác**: `ADR-001:66` để mở *"thư viện compositor + sinh PDF"*, `:68` để mở *"`worker_threads` hay tách job"*. `ADR-001:50` chỉ chốt **cơ chế ngắt dòng**, đó là tính đúng đắn typesetting ⛔ không phải ba ràng buộc bảo mật của `C-10` | ✅ Lens kết luận, PM đồng ý — ⛔ **không đóng hộ một `TBD` bảo mật** |
| **6** | ⛔ **`ADR-001:15` và `:172` KHÔNG mâu thuẫn nội tại** — chúng mô tả **trạng thái ĐẦU VÀO** tại thời điểm viết ADR. `:15` nằm trong `## Context` (theo định nghĩa là ảnh chụp *trước* quyết định); `:172` nằm trong bảng *"cố ý để mở"* mà `escalations.md:184` của run `2026-08-28` đã ghi rõ ngữ nghĩa | ✅ ⛔ **Không sửa dòng nào của `ADR-001`** |

## 4. Phạm vi đề xuất mang ra gate

| Nhóm | Nội dung | Số điểm sửa |
|---|---|:--:|
| **A** — bắt buộc (chỉ `NFR-09`) | `SRS:15`, `:58`, `:60`, `:95`, `:149`, `:258`, `:345`, `:460`, `:461`, `:7` | **9 + frontmatter** |
| **B** — mở rộng (`NFR-07` + `NFR-08`) | `SRS:148`, `:256`, `:257`, `:263`, `:375`, `:385`, `:386`, `:455`, `:456`, `:459` | **+10** |
| **R** — ripple tầng 030 bắt buộc | `Spec-Security-Threat-Model:292`, `:521` · `Endpoint-Preview-Export:200`, `:249` | **4** |
| **R⁺** — ripple mở rộng | `SDD:457`, `:811` · `ADR-006:256`, `:258` · `ADR-015:272` · `DB-Entity-Tenancy:95`, `:312` · `Spec-Integration-Auth-Provider:189` | **+8** |
| **Close** | `000-Index.md:219` — đóng hàng nợ số 5 | **1** |

⭐ **Ripple nguy hiểm nhất, ⛔ tuyệt đối không được bỏ sót**: [`SDD-Comic-Studio.md:811`](../../../030-Specs/Architecture/SDD-Comic-Studio.md) hard-code *"**năm hàng LAI**"* kèm đủ 5 mã. Sửa `SRS:58`/`:60` mà quên dòng này là **tạo ra đúng loại lệch tầng mà lô này đang đi dọn**.

## 5. Rủi ro đã nhận diện

| # | Rủi ro | Cách chặn |
|:--:|---|---|
| **1** | ⭐ **SRS tự cấm mình link vào tầng 030.** `SRS:15` viết *"tầng đó **chưa tồn tại tại thời điểm viết**, nên SRS này **không tạo bất kỳ link nào** trỏ vào đó"*. Thêm link ADR ở `:149`/`:258` mà ⛔ không sửa `:15` ⇒ **tạo mâu thuẫn nội tại MỚI** ngay trong lô đi dọn mâu thuẫn | ⇒ Câu hỏi `Q-2` ở gate |
| **2** | **Sửa nhầm con số đang đúng.** Hai con số **đang đúng và ⛔ không được đụng**: `55` (`SRS:345`, CHỐT thuần) và `21` (`SRS:437`, số hàng ở lại `TBD` — cả 5 hàng `b-*` chỉ đổi *mệnh đề lý do*, ⛔ không đổi trạng thái) | Ghi thành ràng buộc cứng trong `[CONSTRAINTS]` của mọi writer + tiêu chí verify |
| **3** | **Đóng hộ một `TBD` có chủ đích.** Hai chỗ: **vendor billing** (`ADR-003:71-79`, chặn bởi quốc gia pháp nhân bán hàng — ⛔ không phải thiếu phân tích kỹ thuật) và **`C-10`** (bảo mật) | `SRS-NFR-08` ⛔ **không được** ghi MẶC ĐỊNH thuần; `C-10` giữ mở, chỉ viết lại lý do |
| **4** | **Lô sau "sửa" nhầm `ADR-001:172`.** Sau khi `SRS:258` mang nhãn mới, một lô `diff` hai dòng sẽ thấy lệch và tưởng `ADR-001` sai | Ghi một dòng vào `escalations.md` run này — đúng mô hình `escalations.md:184` đã dùng thành công |
| **5** | **Bốn ADR còn `status: draft`.** Repo đã dùng `draft` làm mốc chặn thật (`ADR-010:176`) ⇒ hạ nhãn tầng 020 dựa trên ADR `draft` là câu hỏi governance | ⇒ Câu hỏi `Q-3` ở gate |
| **6** | **`ADR-001` chưa commit.** Nếu `SRS` trỏ tới `ADR-001` như nơi đóng quyết định trong khi bản trong git ⛔ không có `shadcn/ui + Tailwind` ⇒ **thay một lệch tầng bằng một lệch tầng khó thấy hơn** | ⇒ Câu hỏi `Q-4` ở gate |

---

_Created by TNMCORE-OS (PM)_
_Author: trisjr_
