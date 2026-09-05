---
id: SPRINT-003
type: sprint
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, sprint, provenance, change-log, narrative-time-key]
linked-to: "../Implementation-Plans/Plan-MVP1-Story-Intelligence.md"
created: 2026-09-05
updated: 2026-09-05
---

# Sprint 003 — Provenance: bằng chứng ⛔ không thiếu ngẫu nhiên

| | |
|---|---|
| **Thời gian** | `02/11/2026` – `13/11/2026` (2 tuần) |
| **Capacity** | 60h · **Kỹ thuật 52h** + `O4` 8h = **60h** |
| **Mốc** | MVP1 |
| **Exit criteria trả** | `M1-5` (phần **tồn tại**; phần **test cùng transaction** ở Sprint 004) |
| **OKR phục vụ** | `O1` / `KR1.2` |
| **Điều kiện vào** | `M1-1` PASS · `M1-4` đạt |

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

> ⭐ **Năm hạng mục provenance tồn tại trong schema trước khi generation đầu tiên của sản phẩm thật ra đời.**

`CF-7.3` `[OFF]`: *"⛔ không lưu từ generation đầu tiên thì **vĩnh viễn ⛔ không có**"*. Và [MVP-Scope §3.1](../MVP-Scope.md#31-ba-ô-đáng-chú-ý-nhất-trong-bảng) làm rõ: vì MVP0 là spike bị vứt, **"generation đầu tiên" có nghĩa pháp lý = generation đầu tiên của sản phẩm thật, tức MVP1**.

⚠️ **Bối cảnh pháp lý gắt hơn người ta tưởng**: tác phẩm của anh **và của khách hàng anh** ⛔ **không được bảo hộ bản quyền ở Việt Nam** (`CF-7.2` `[OFF]`) nếu ⛔ không chứng minh được *"decisive contribution"*. ⭐ **Prompt một mình ⛔ không chứng minh được điều đó.** Cái chứng minh được là: *người đã **chọn X thay vì Y**, đã sửa thoại, đã đổi camera, đã kéo bubble.* Đó chính là `change_log`.

Sprint này cũng gánh `B-01` — **sửa khoá thời gian**. Nó ⛔ không thuộc provenance, nhưng nó **chặn `B-04`** ở Sprint 005 và nằm trong khoá của mọi bảng timeline, nên sửa sau = migration toàn bộ.

---

## 2. Story

| Mã | Story | `E_build` | AC chính |
|---|---|--:|---|
| `B-01` | [Fix-Narrative-Time-Key](../../022-User-Stories/Backlog/Story-Fix-Narrative-Time-Key.md) | 8h | Khoá thời gian ⛔ không sai âm thầm ở flashback |
| `G-01` | [Provenance-Chain-Parent-Generation](../../022-User-Stories/Backlog/Story-Provenance-Chain-Parent-Generation.md) | 14h ⚠️ `[EM]` PM | 4 cột/quan hệ + test race `field_provenance` |
| `D-02` | [Change-Log-On-Every-Editor-Action](../../022-User-Stories/Backlog/Story-Change-Log-On-Every-Editor-Action.md) | 20h ⚠️ vượt trần | ⭐ Ghi **mọi** hành động — kể cả *"chọn generation X thay vì Y"* |
| `F-02` | [Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) | 10h | `cost_usd` + `model_id` + `model_version` + `attempt_no` |
| | **Cộng kỹ thuật** | **52h** | |
| | `O4` — 2 post + 2 cuộc trò chuyện | 8h | `KR4.1`, `KR4.3` |

---

## 3. Thứ tự làm & vì sao

| # | Việc | Vì sao ở vị trí này |
|:-:|---|---|
| 1 | `B-01` khoá thời gian | ⭐ Phụ thuộc **CỨNG** ([Roadmap §6.2](../Roadmap.md#62-bảng-phụ-thuộc)): *"sai âm thầm ở flashback; **nằm trong khoá** nên sửa sau = migration toàn bộ"*. Làm đầu tiên, khi bảng timeline ⛔ chưa tồn tại |
| 2 | `G-01` provenance chain | Cung cấp bảng `generation` + `field_provenance` mà `D-02` và `F-02` cắm vào |
| 3 | `F-02` cost metadata | Bốn cột trên chính bảng `generation` của `G-01`. Làm liền mạch, ⛔ tránh hai lần migration cùng một bảng |
| 4 | `D-02` change_log | Việc lớn nhất sprint. Cần biết `generation.id` để tham chiếu |

---

## 4. Definition of Done

### ⭐ Năm hạng mục provenance **tồn tại**

- [ ] Bảng `generation` có đủ **4** cột/quan hệ: `parent_generation_id` (nullable FK) · `relation_kind ENUM('retry','variation','refine','continuity_fix')` · `field_provenance` (mức field) · `origin ENUM('ai','ai_edited','human')`
- [ ] `change_log` là bảng **append-only**, ghi **mọi** hành động người dùng — ⭐ **kể cả** *"chọn generation X thay vì Y"* (`KC-2`)
- [ ] `INSERT` vào `generation` thiếu `origin` bị **DB từ chối** (`NOT NULL`), ⛔ không phải chỉ cảnh báo ở tầng ứng dụng
- [ ] Generation tạo bằng *retry* có `relation_kind = 'retry'` và `parent_generation_id` trỏ **đúng** generation gốc
- [ ] Field bị người dùng sửa tay có dòng `field_provenance` ghi `origin = 'human'` / `'ai_edited'` **cho đúng field đó**, ⛔ không phải cho toàn bộ generation
- [ ] Generation đầu chuỗi: `parent_generation_id = NULL` là **hợp lệ**, ⛔ không bị coi là lỗi dữ liệu — nhưng `origin` vẫn phải xác định

### Đường ⛔ không hạnh phúc

- [ ] Hai request tạo generation **đồng thời** cho cùng một panel ⛔ không ghi đè `field_provenance` của nhau — cả hai dòng tồn tại, ⛔ không dòng nào mất
- [ ] Generation `relation_kind = 'continuity_fix'` mà ⛔ không trỏ được về generation gốc bị **chặn ở tầng ứng dụng trước khi tạo record**

### Khoá thời gian & chi phí

- [ ] Khoá thời gian mới thay `(chapter, scene)` đã vào schema, và có test chứng minh **flashback ⛔ không cho ra kết quả sai âm thầm**
- [ ] **100%** row `generation` có đủ `cost_usd` + `model_id` + `model_version` + `attempt_no` — đo bằng: đếm `NULL` trên bốn cột = ⭐ **`0`** (`KR3.3`)

### ⛔ Điều sprint này KHÔNG làm

- [ ] ⛔ **Không** xây UI duyệt **cây** generation (tree view / diff / branch-merge) — `D6` **cắt hẳn** ở mọi mốc, kể cả Full Scope. ⭐ **Cắt UI, ⛔ KHÔNG cắt cột dữ liệu** — hai thứ này rất dễ bị gộp nhầm khi cắt scope, và gộp nhầm thì **mất bảo hộ bản quyền**
- [ ] ⛔ **Không** đảm bảo commit cùng transaction — đó là `G-02` ở **Sprint 004**

---

## 5. Rủi ro sprint này

| Rủi ro | Tín hiệu sớm | Xử lý |
|---|---|---|
| ⭐ Gộp nhầm *"cắt UI cây generation"* thành *"cắt cột `parent_generation_id`"* | Thấy đề xuất bỏ cột vì *"⛔ không có UI dùng"* | [MVP-Scope §3.1](../MVP-Scope.md#31-ba-ô-đáng-chú-ý-nhất-trong-bảng) ghi thẳng bẫy này. Cột **⛔ không backfill được**; UI thì luôn xây lại được |
| `D-02` vượt 20h vì *"mọi hành động"* rộng hơn dự kiến | Hết tuần 2 mà mới ghi được hành động CRUD cơ bản | Ưu tiên đúng thứ `KC-2` gọi tên: **chọn generation**, **sửa thoại**, **đổi camera**, **kéo bubble**. Các hành động khác bổ sung dần |
| Test race `field_provenance` bị bỏ vì khó viết | AC race ⛔ không có test tương ứng | Đây là AC bắt buộc. Bug loại này ⛔ không tái hiện đều ⇒ ⛔ không phát hiện được bằng dùng tay |
| `B-01` bị hoãn vì *"⛔ chưa có bảng timeline nào"* | Lập luận *"để S5 làm luôn thể"* | ⛔ **Sai.** Chính vì ⛔ chưa có bảng nên bây giờ mới **rẻ**. Để S5 thì `B-04` phải chờ, hoặc phải migrate |

---

## 6. Retro checklist

- [ ] `burn_tích_luỹ` = giờ thực tích luỹ / **173h**. Ghi số
- [ ] > **105%** ⇒ ⭐ kích van kế tiếp
- [ ] `G-01` lệch bao nhiêu % so với `[EM]` 14h? ⇒ hiệu chỉnh `G-02` (S4) **trước khi** S4 bắt đầu
- [ ] Đã đếm `NULL` trên bốn cột cost chưa? `KR3.3` đo **hàng tuần**, ⛔ không phải cuối sprint
- [ ] `O4`: tích luỹ đã **6 post** + **5 cuộc trò chuyện** chưa?

---

## 7. Tài liệu tham khảo

- [Plan-MVP1-Story-Intelligence.md](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md) · [WBS-MVP1.md](../Estimates/WBS-MVP1.md)
- [MVP-Scope §6](../MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) — `KC-1`, `KC-2`, `KC-3`
- [ADR-011](../../030-Specs/Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) — cơ sở `B-01`
- [ADR-017](../../030-Specs/Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) — cơ sở `G-01`
- [DB-Entity-Provenance-And-Usage](../../030-Specs/Schema/DB-Entity-Provenance-And-Usage.md) · [DB-Entity-Generation](../../030-Specs/Schema/DB-Entity-Generation.md) · [DB-Entity-Narrative-Timeline](../../030-Specs/Schema/DB-Entity-Narrative-Timeline.md)

---

_Created by product-manager_
_Author: trisjr_
