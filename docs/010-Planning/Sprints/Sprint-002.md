---
id: SPRINT-002
type: sprint
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, sprint, legal, opt-out, auth, hard-delete]
linked-to: "../Implementation-Plans/Plan-MVP1-Story-Intelligence.md"
created: 2026-09-05
updated: 2026-09-05
---

# Sprint 002 — Cửa pháp lý & đường vào của dữ liệu

| | |
|---|---|
| **Thời gian** | `19/10/2026` – `30/10/2026` (2 tuần) |
| **Capacity** | 60h · **Kỹ thuật 52h** + `O4` 8h = **60h** |
| **Mốc** | MVP1 |
| **Exit criteria trả** | ⭐ `M1-4` |
| **OKR phục vụ** | `O1` / `KR1.3` |
| **Điều kiện vào** | ⭐ `M1-1` PASS ở Sprint 001 |

## Mục lục

1. [Mục tiêu sprint](#1-mục-tiêu-sprint)
2. [Story](#2-story)
3. [Thứ tự làm & vì sao](#3-thứ-tự-làm--vì-sao)
4. [Definition of Done](#4-definition-of-done)
5. [Rủi ro sprint này](#5-rủi-ro-sprint-này)
6. [Retro checklist](#6-retro-checklist)
7. [Tài liệu tham khảo](#7-tài-liệu-tham-khảo)

---

## 1. Mục tiêu sprint

> ⭐ **Trước khi một byte nội dung của người dùng đi vào hệ thống, cả cửa vào lẫn cửa ra đều đã tồn tại và đã được kiểm thử.**

Hai nửa của cùng một nguyên tắc:

| Nửa | Story | Nguyên tắc |
|---|---|---|
| **Cửa vào** | `G-03` opt-out Điều 37b | Đây là nơi **duy nhất** file của user lần đầu vào hệ thống. Kiểm ở chỗ khác nghĩa là **đã xử lý nội dung có opt-out trước khi biết** (`KC-6`) |
| **Cửa ra** | `G-04` hard-delete + export | *"**Đường thoát phải được xây cùng lúc với đường vào**"* — [MVP-Scope §4](../MVP-Scope.md). Takedown **sẽ** đến, ⛔ không phải *có thể* đến |

---

## 2. Story

| Mã | Story | `E_build` | AC chính |
|---|---|--:|---|
| `E-03` | [Per-Tenant-Object-Storage-No-Cross-Dedup](../../022-User-Stories/Backlog/Story-Per-Tenant-Object-Storage-No-Cross-Dedup.md) | 10h | Key `tenant/{tenant_id}/{sha256}`, ⛔ **không** dedup chéo tenant |
| `E-04` | [Buy-Authentication-Provider](../../022-User-Stories/Backlog/Story-Buy-Authentication-Provider.md) | 12h | ⭐ **Mua**, ⛔ không tự viết |
| `G-03` | [Opt-Out-Check-At-Ingest](../../022-User-Stories/Backlog/Story-Opt-Out-Check-At-Ingest.md) | 12h ⚠️ `[EM]` PM | ⭐ **100%** file upload có bản ghi log kiểm opt-out |
| `G-04` | [ToS-User-Warrant-And-Tenant-Hard-Delete](../../022-User-Stories/Backlog/Story-ToS-User-Warrant-And-Tenant-Hard-Delete.md) | 18h ⚠️ `[EM]` PM, vượt trần | Hard-delete đã **kiểm thử tự động** + đường export đầy đủ |
| | **Cộng kỹ thuật** | **52h** | |
| | `O4` — 2 post + 2 cuộc trò chuyện | 8h | `KR4.1`, `KR4.3` |

---

## 3. Thứ tự làm & vì sao

| # | Việc | Vì sao ở vị trí này |
|:-:|---|---|
| 1 | `E-04` **mua** auth | ⭐ *"Tự viết auth là cách nhanh nhất để một dev đơn lẻ **đốt hai tháng và vẫn có lỗ hổng**"* (Analysis §5.7). Đây là rủi ro lịch số 1 của roadmap — xử lý sớm để biết sớm nếu tích hợp khó hơn dự kiến |
| 2 | `E-03` object storage | `G-04` cần biết ảnh nằm ở đâu để export và để xoá. Làm trước `G-04` |
| 3 | `G-03` opt-out | ⭐ Phải xong **trước** `B-02` ingest ở Sprint 005 — AC đòi *"chạy **trước** mọi bước xử lý nội dung khác"*. Dựng khung pipeline ingest với opt-out là **bước 0** ngay từ đây |
| 4 | `G-04` hard-delete + export | Việc lớn nhất sprint. Cần cả `E-03` (biết ảnh ở đâu) lẫn `M1-1` (biết ranh giới tenant ở đâu) |

---

## 4. Definition of Done

### ⭐ `M1-4` — cửa vào

- [ ] ⭐ **100%** file upload có một bản ghi log kết quả kiểm opt-out — đo bằng: `số dòng log kiểm / tổng số file upload = 1,00`
- [ ] Mỗi bản ghi có đủ **timestamp** + **kết quả** (`có signal` / `không có signal`)
- [ ] File có ≥1 trong **bốn kênh** bảo lưu quyền bị **chặn xử lý tiếp** — pipeline dừng **trước** bước extraction; ⛔ **không** tạo `generation` hay `usage_event` nào từ file đó
- [ ] Bước kiểm opt-out chạy **trước** mọi bước xử lý nội dung khác — đo bằng đọc thứ tự bước trong code pipeline hoặc trace log

### Đường ⛔ không hạnh phúc — cửa vào

- [ ] Metadata **hỏng / ⛔ không đọc được** ⇒ log `không đọc được` và **chặn**, ⛔ **KHÔNG** mặc định coi là `không có signal` rồi cho qua
- [ ] Nhiều kênh **mâu thuẫn** nhau ⇒ **fail-safe theo hướng bảo thủ hơn** (chặn), ⛔ không ưu tiên kênh cho phép xử lý
- [ ] Batch hỗn hợp: chỉ file có signal bị chặn; các file khác trong cùng batch vẫn được xử lý

### Cửa ra

- [ ] **100%** FK trỏ về `tenant` dùng `ON DELETE CASCADE` — đo bằng đọc schema migration
- [ ] Tồn tại thao tác vận hành xoá cứng toàn bộ dữ liệu của một `tenant_id`
- [ ] ⭐ Đường hard-delete đã được **kiểm thử tự động** — ⛔ không phải chạy tay một lần
- [ ] Tồn tại đường **xuất dữ liệu đầy đủ**: Story Bible + Comic IR + mọi ảnh + ⭐ **cả `change_log` và `field_provenance`** — đó là hồ sơ chứng minh quyền tác giả **của khách**
- [ ] Hard-delete tenant A ⇒ **100%** dữ liệu tenant B còn nguyên
- [ ] Hard-delete bị gián đoạn giữa chừng ⇒ tenant ở **một trong hai** trạng thái xác định được (⛔ chưa xoá / đã xoá hoàn toàn), ⛔ không có trạng thái nửa vời
- [ ] Checkbox **user warrant + indemnify** gắn ở **bước upload**, ⛔ không chỉ nằm trong trang ToS
- [ ] Request bỏ qua checkbox (gọi thẳng API) bị **server chặn** — ⛔ không tin validation phía client

### Hạ tầng

- [ ] Object key theo đúng dạng `tenant/{tenant_id}/{sha256}`; ⛔ **không** dedup nội dung giữa hai tenant
- [ ] Auth là **dịch vụ mua**, ⛔ không phải code tự viết — theo [`ADR-003`](../../030-Specs/Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md)

---

## 5. Rủi ro sprint này

| Rủi ro | Tín hiệu sớm | Xử lý |
|---|---|---|
| ⭐ Tự viết auth vì *"tích hợp vendor phiền quá"* | Bắt đầu viết bảng `password_hash` hoặc logic session | ⛔ **Dừng ngay.** `E-04` là **mua** `[CHỐT]`. Đây là rủi ro lịch số 1 của cả roadmap |
| `G-04` vượt 18h vì đường export nặng hơn dự kiến | Hết tuần 2 mà export mới có Story Bible | Export là AC **⛔ không cắt được** — nó là hồ sơ pháp lý của khách. Mượn giờ từ `O4`, hoàn ở S3 |
| Dedup chéo tenant lọt vào vì *"tiết kiệm storage"* | Thấy logic tra `sha256` toàn cục | Dedup chéo **mâu thuẫn trực tiếp** với lập luận bản quyền (Analysis §5.7 #4) |
| Xây **anti-feature**: bộ phát hiện bản quyền chủ động | Xuất hiện từ `similarity`, `plagiarism`, `flag nội dung khả nghi` | ⛔ **CẤM.** Nó có thể **phá chính miễn trừ Điều 198b** — [Risk-Register R-04](../Risk-Register.md). `G-03` chỉ đọc tín hiệu **do chủ quyền gắn vào file** |
| Diễn giải phạm vi Điều 37a | Bắt đầu viết kết luận pháp lý vào code comment hoặc doc | Đó là câu **Q1 của gate `G0`**, thuộc luật sư. `CẤM-13` |

---

## 6. Retro checklist

- [ ] `burn_tích_luỹ` = giờ thực tích luỹ / **113h**. Ghi số
- [ ] > **105%** ⇒ ⭐ kích van kế tiếp ngay tại retro
- [ ] `G-03` và `G-04` là **hai ước lượng `[EM]` đầu tiên** được kiểm chứng. Lệch bao nhiêu %? ⇒ hiệu chỉnh `G-01`, `G-02`, `G-05` theo cùng tỉ lệ
- [ ] `M1-4` đã đạt chưa? Nếu chưa, ⛔ **không được** bắt đầu `B-02` ingest ở S5 — pipeline sẽ có thứ tự sai
- [ ] `O4`: đã có **2 post** và **2 cuộc trò chuyện có ghi chép** chưa? (`KR4.3` cần 20 cuộc **trước 31/12**, tức ~2/sprint)

---

## 7. Tài liệu tham khảo

- [Plan-MVP1-Story-Intelligence.md](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md) · [WBS-MVP1.md](../Estimates/WBS-MVP1.md)
- [MVP-Scope §6](../MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) — `KC-6`
- [Risk-Register.md](../Risk-Register.md) — `R-02`, `R-04`
- [ADR-003](../../030-Specs/Architecture/ADR-003-Auth-And-Billing-Vendor-Selection.md) · [ADR-004](../../030-Specs/Architecture/ADR-004-Object-Storage-Vendor-And-Signed-URL.md)
- [Spec-Security-Legal-Compliance](../../030-Specs/Security/Spec-Security-Legal-Compliance.md)
- [Endpoint-Chapter-Ingest](../../030-Specs/API/Endpoint-Chapter-Ingest.md) · [Spec-Integration-Object-Storage](../../030-Specs/API/Spec-Integration-Object-Storage.md)
- [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md) · [UC-11-Handle-Takedown-Request](../../020-Requirements/Use-Cases/UC-11-Handle-Takedown-Request.md)

---

_Created by product-manager_
_Author: trisjr_
