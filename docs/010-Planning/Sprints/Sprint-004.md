---
id: SPRINT-004
type: sprint
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, sprint, usage-event, transaction, job-queue, preference-data]
linked-to: "../Implementation-Plans/Plan-MVP1-Story-Intelligence.md"
created: 2026-09-05
updated: 2026-09-05
---

# Sprint 004 — Sổ cái sử dụng & ranh giới transaction

| | |
|---|---|
| **Thời gian** | `16/11/2026` – `27/11/2026` (2 tuần) |
| **Capacity** | 60h · **Kỹ thuật 56h** + `O4` 8h = ⚠️ **64h** |
| **Mốc** | MVP1 |
| **Exit criteria trả** | ⭐ `M1-5` (trọn vẹn) |
| **OKR phục vụ** | `O1` / `KR1.2` · `O3` / `KR3.3` |
| **Điều kiện vào** | 5 hạng mục provenance **tồn tại** sau Sprint 003 |

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

> ⭐ **Bằng chứng pháp lý ⛔ không thể thiếu ngẫu nhiên** — vì nó commit **cùng một transaction** với chính artifact mà nó chứng minh.

`KC-4` nói bằng một câu: *"**Bằng chứng có thể thiếu ngẫu nhiên thì ⛔ không phải bằng chứng.**"* Sprint 003 đã dựng **cấu trúc** provenance; sprint này chứng minh **tính toàn vẹn** của nó bằng test — và `M1-5` nghiệm thu bằng ⭐ **test**, ⛔ không phải bằng *"đã thấy đủ cột trong DB"*.

⚠️ **Sprint này vượt capacity danh nghĩa (64h / 60h).** Đó là hệ quả trực tiếp của load 100,5% ở [Plan §5.3](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#53--kết-luận-trung-thực), ⛔ không phải lỗi phân bổ. Nếu `burn_tích_luỹ` chạm 105% ở retro S3, van xả đã phải được kích **trước khi** sprint này bắt đầu.

---

## 2. Story

| Mã | Story | `E_build` | AC chính |
|---|---|--:|---|
| `F-01` | [Usage-Event-And-Daily-Rollup](../../022-User-Stories/Backlog/Story-Usage-Event-And-Daily-Rollup.md) | 12h | `usage_event` append-only + rollup `usage_daily` |
| `G-02` | [Provenance-Committed-In-Same-Transaction](../../022-User-Stories/Backlog/Story-Provenance-Committed-In-Same-Transaction.md) | 12h ⚠️ `[EM]` PM | ⭐ Test rollback: **⛔ không** row nào sống sót |
| `A-05` | [Job-Queue-In-Postgres](../../022-User-Stories/Backlog/Story-Job-Queue-In-Postgres.md) | 12h | `FOR UPDATE SKIP LOCKED` + transactional enqueue |
| `H-04` | [Log-Preference-Data](../../022-User-Stories/Backlog/Story-Log-Preference-Data.md) | 10h | ⭐ Moat thật — *một khoản đầu tư, trả hai lần* |
| `H-05` | [Minimum-Abuse-Controls](../../022-User-Stories/Backlog/Story-Minimum-Abuse-Controls.md) — phần 🟡 | 4h ⚠️ `[EM]` PM | Rate limit/tenant + giới hạn upload + log provider từ chối |
| `G-05` | [Safe-Harbour-Checklist-Article-198b](../../022-User-Stories/Backlog/Story-Safe-Harbour-Checklist-Article-198b.md) — phần 🟡 | 6h ⚠️ `[EM]` PM | Checklist **6 mục** tồn tại + cột soft-delete + kênh `copyright@` |
| | **Cộng kỹ thuật** | ⚠️ **56h** | |
| | `O4` — 2 post + 2 cuộc trò chuyện | 8h | `KR4.1`, `KR4.3` |

---

## 3. Thứ tự làm & vì sao

| # | Việc | Vì sao ở vị trí này |
|:-:|---|---|
| 1 | `F-01` usage_event | ⭐ `G-02` cần **cả ba** bảng (`generation` · `change_log` · `usage_event`) mới test được cùng-transaction. `usage_event` là bảng cuối còn thiếu |
| 2 | `G-02` test cùng transaction | Ngay sau `F-01`. Đây là DoD của `M1-5` |
| 3 | `A-05` job queue | Cần trước `B-03` extraction ở S5 (LLM call chạy async). Enqueue phải **transactional** — cùng kỷ luật với `G-02` |
| 4 | `H-04` preference data | ⭐ *"Dùng **chung đúng cơ chế** mà luật VN buộc phải có"* — cắm vào `change_log` đã có từ S3, nên rẻ |
| 5 | `H-05` + `G-05` phần 🟡 | Hai hạng mục nhỏ, ⛔ không chặn gì. Đặt cuối để chúng là **phần đầu tiên bị hoãn** nếu sprint tràn |

---

## 4. Definition of Done

### ⭐ `M1-5` — test, ⛔ không phải quan sát

> [!CAUTION]
> Nghiệm thu **chỉ** bằng test. [Epic cha](../../022-User-Stories/Epics/Epic-Legal-And-Compliance.md) ghi rõ: *"có **TEST** chứng minh"*, ⛔ **không** phải *"đã thấy đủ cột trong DB"*.

- [ ] Tồn tại **một test tự động**: khi tạo generation, dòng `generation` + `change_log` + `usage_event` (nếu có phát sinh usage) được ghi trong ⭐ **cùng một database transaction**
- [ ] Test rollback: raise exception **sau** khi ghi `generation` nhưng **trước** khi ghi `change_log` ⇒ ⭐ **cả ba bảng rollback về `0` dòng mới**
- [ ] Test đó **PASS trong CI** ở trạng thái hiện tại của schema — tên test cụ thể được ghi lại
- [ ] Toàn bộ pipeline ghi provenance nằm trong **một** connection pool tới **một** PostgreSQL instance — ⛔ không gọi service/DB khác để ghi `change_log` hay `usage_event`
- [ ] Transaction abort giữa chừng (deadlock / timeout) ⇒ ⛔ **không** dòng nào trong ba bảng được giữ lại **một phần**
- [ ] Hai generation tạo gần như đồng thời cho **hai panel khác nhau** có transaction boundary **riêng** — rollback của A ⛔ không ảnh hưởng commit của B
- [ ] Worker ghi `usage_event` cho generation ⛔ **chưa** commit ⇒ bị **từ chối hoặc chờ đúng transaction**, ⛔ không tạo `usage_event` mồ côi

### Sổ cái & hàng đợi

- [ ] `usage_event` là bảng **append-only**; `usage_daily` là rollup sinh từ nó
- [ ] Job queue dùng `FOR UPDATE SKIP LOCKED`; **enqueue là transactional** — job ⛔ không tồn tại nếu transaction nghiệp vụ rollback
- [ ] Preference data được ghi qua **đúng cơ chế `change_log`** đã có, ⛔ không dựng đường ghi song song

### Phần 🟡

- [ ] Rate limit theo tenant + giới hạn kích thước upload + log mọi lần provider từ chối
- [ ] Checklist safe harbour **6 mục** tồn tại dưới dạng artifact tick được + cột soft-delete + kênh tiếp nhận `copyright@` hoạt động
- [ ] ⛔ **Không** bật *"mở cho người ngoài upload"* — trigger đó chưa đến; phần SLA 72h, đăng ký đầu mối Bộ VHTTDL, counter-notice thuộc **MVP2** (`M2-6`)

### ⛔ Điều sprint này KHÔNG làm

- [ ] ⛔ **Không** xây bộ phát hiện bản quyền chủ động dưới **bất kỳ** tên nào — anti-feature, [Risk-Register R-04](../Risk-Register.md)
- [ ] ⛔ **Không** tự khẳng định nền tảng được hưởng miễn trừ Điều 198b — đó là câu **Q3 của `G0`**, thuộc luật sư

---

## 5. Rủi ro sprint này

| Rủi ro | Tín hiệu sớm | Xử lý |
|---|---|---|
| ⭐ **Sprint đã vượt capacity từ khi lập kế hoạch** (64h/60h) | — (đã hiện thực hoá) | Kiểm `burn_tích_luỹ` ở retro S3. Nếu >105% thì van xả **phải** đã kích trước khi sprint này mở |
| Provenance bị commit **tách rời** artifact | Thấy code ghi `change_log` ở một service call riêng, hoặc sau `await` của lời gọi khác | `M1-5` đòi **test** chứng minh — ⛔ không phải review bằng mắt. Đây là `P-R5`, *cao về hậu quả* |
| Test deadlock có chủ đích khó viết ⇒ bị bỏ | AC deadlock ⛔ không có test tương ứng | Đây là phần đắt nhất của `[EM]` 12h cho `G-02`. Nếu bỏ, ước lượng đúng nhưng **DoD sai** |
| `H-05` + `G-05` bị nuốt vì sprint tràn | Hết tuần 2 mà mới xong 4 story đầu | ⭐ **Đã tính trước**: hai story này đặt cuối chính vì chúng là phần hoãn được. Hoãn sang tuần gate, ⛔ **không** hoãn `G-02` |

---

## 6. Retro checklist

- [ ] `burn_tích_luỹ` = giờ thực tích luỹ / **237h**. Ghi số
- [ ] > **105%** ⇒ ⭐ kích van kế tiếp. ⚠️ Đây là retro **rủi ro nhất** — đường burn-down chạm 99% ở đây
- [ ] `M1-5` đã PASS chưa? Nếu chưa, ⛔ **không mở Sprint 005** — mọi generation sau đó thiếu bằng chứng, và bằng chứng ⛔ **không backfill được**
- [ ] `G-02` lệch bao nhiêu % so với `[EM]` 12h?
- [ ] `O4`: tích luỹ **8 post** + **7 cuộc trò chuyện**?

---

## 7. Tài liệu tham khảo

- [Plan-MVP1-Story-Intelligence.md](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md) · [WBS-MVP1.md](../Estimates/WBS-MVP1.md)
- [MVP-Scope §6](../MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) — `KC-4`
- [ADR-015](../../030-Specs/Architecture/ADR-015-Job-Queue-In-Postgres.md) · [ADR-017](../../030-Specs/Architecture/ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) · [ADR-018](../../030-Specs/Architecture/ADR-018-Usage-Event-And-Rollup-Model.md)
- [DB-Entity-Job-Queue](../../030-Specs/Schema/DB-Entity-Job-Queue.md) · [DB-Entity-Provenance-And-Usage](../../030-Specs/Schema/DB-Entity-Provenance-And-Usage.md) · [DB-Entity-Compliance-And-Takedown](../../030-Specs/Schema/DB-Entity-Compliance-And-Takedown.md)
- [Endpoint-Usage-And-Credit](../../030-Specs/API/Endpoint-Usage-And-Credit.md) · [Endpoint-Takedown-Public](../../030-Specs/API/Endpoint-Takedown-Public.md)

---

_Created by product-manager_
_Author: trisjr_
