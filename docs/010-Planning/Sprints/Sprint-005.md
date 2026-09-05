---
id: SPRINT-005
type: sprint
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, sprint, ingest, text-clean, extraction, timeline]
linked-to: "../Implementation-Plans/Plan-MVP1-Story-Intelligence.md"
created: 2026-09-05
updated: 2026-09-05
---

# Sprint 005 — Story Intelligence: ingest → extraction → timeline

| | |
|---|---|
| **Thời gian** | `30/11/2026` – `11/12/2026` (2 tuần) |
| **Capacity** | 60h · **Kỹ thuật 56h** + `O4` 8h = ⚠️ **64h** |
| **Mốc** | MVP1 |
| **Exit criteria trả** | ⭐ `M1-2` |
| **OKR phục vụ** | `O2` / `KR2.1` |
| **Điều kiện vào** | `M1-4` đạt (opt-out là bước 0 của pipeline) · `M1-5` PASS · `B-01` xong ở S3 |

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

> ⭐ **Hệ thống tự đọc được một chương truyện scrape thật, thay vì mình đọc hộ nó.**

Đây là sprint mang **tên gọi của cả mốc MVP1**. Ba tầng, theo đúng nguyên tắc phân vai của [Analysis §5.5](../../050-Research/Analysis-Comic-Studio-Concept.md):

| Tầng | Việc | Ai làm |
|---|---|---|
| 1. **Text clean** | Bỏ quảng cáo, lời tác giả cuối chương, *"xin ủng hộ phiếu đề cử"* | ⭐ **Code deterministic** — ⛔ **KHÔNG** phải LLM |
| 2. **Extraction** | Rút entity: nhân vật, địa điểm, trang phục | LLM |
| 3. **Timeline state** | `state_at(N) = reduce(events)` | ⭐ **Code sở hữu state**; LLM chỉ **phát event** |

⚠️ **Sprint này vượt capacity danh nghĩa (64h / 60h)** — cùng lý do với Sprint 004.

---

## 2. Story

| Mã | Story | `E_build` | AC chính |
|---|---|--:|---|
| `NEW-02` | ⚠️ **LLM provider adapter** — ⛔ **chưa có story, phải viết trước khi làm** | 8h ⚠️ `[EM]` PM | Port + 1 adapter, ghi `cost_usd`/`model_version` cho `F-02` |
| `B-02` | [Chapter-Ingest-And-Text-Clean](../../022-User-Stories/Backlog/Story-Chapter-Ingest-And-Text-Clean.md) | 10h | ⭐ Text clean là bước **ĐẦU TIÊN** (sau opt-out) |
| `B-03` | [Story-Bible-Extraction](../../022-User-Stories/Backlog/Story-Story-Bible-Extraction.md) | 18h ⚠️ vượt trần | Trích character / location / costume tự động |
| `B-04` | [Timeline-State-Resolver](../../022-User-Stories/Backlog/Story-Timeline-State-Resolver.md) | 20h ⚠️ vượt trần | `state_at(N) = reduce(events)`, đúng ở **flashback** |
| | **Cộng kỹ thuật** | ⚠️ **56h** | |
| | `O4` — 2 post + 2 cuộc trò chuyện | 8h | `KR4.1`, `KR4.3` |

---

## 3. Thứ tự làm & vì sao

| # | Việc | Vì sao ở vị trí này |
|:-:|---|---|
| 1 | `NEW-02` LLM adapter | `B-03` ⛔ không gọi được LLM nếu ⛔ chưa có adapter. Và adapter phải ghi `cost_usd` + `model_version` ngay từ lời gọi đầu tiên — `F-02` đòi **100%** row có đủ bốn cột |
| 2 | `B-02` ingest + text clean | ⭐ Cắm **sau** bước opt-out của `G-03` (S2). Thứ tự pipeline: `opt-out → text clean → extraction`. Đảo thứ tự = phải sửa lại pipeline |
| 3 | `B-03` extraction | Cần text đã sạch. Rác vào ⇒ **entity giả** ra |
| 4 | `B-04` timeline resolver | Cần cả `B-01` (khoá thời gian, xong ở S3) lẫn `B-03` (event nguồn) |

---

## 4. Definition of Done

### ⭐ `M1-2` — pipeline nuốt được rác của đời thật

- [ ] Pipeline ingest có ⭐ **text clean là bước ĐẦU TIÊN** của phần xử lý nội dung (ngay sau bước kiểm opt-out của `G-03`)
- [ ] Chạy end-to-end trên ⭐ **≥1 chapter scrape thật**, ⛔ không phải file đã dọn tay
- [ ] Kiểm bằng mắt: quảng cáo / lời tác giả cuối chương / *"xin ủng hộ phiếu đề cử"* ⛔ **không** sinh entity giả
- [ ] Text clean là ⭐ **code deterministic** (regex/heuristic) — ⛔ **KHÔNG** gọi LLM ở bước này

### Extraction

- [ ] Trích được **character** + **location** + **costume** từ chapter đã làm sạch
- [ ] **100%** lời gọi LLM ghi `cost_usd` + `model_id` + `model_version` + `attempt_no` vào `generation` (kế thừa `F-02`)
- [ ] Mỗi lời gọi LLM đi qua **job queue** của `A-05`, ⛔ không gọi đồng bộ trong request HTTP
- [ ] ⚠️ Ngưỡng **≥80%** của `M1-3` ⛔ **chưa** đo ở sprint này — nó cần eval kit của Sprint 006. Sprint này chỉ cần extraction **chạy được**

### Timeline

- [ ] `state_at(N)` tính bằng ⭐ **reduce trên chuỗi event**, ⛔ không phải bằng một cột trạng thái ghi đè
- [ ] ⭐ Có test chứng minh **flashback** cho ra state **đúng** — đây chính là lỗi mà `B-01` tồn tại để chặn: *sai âm thầm, ⛔ không báo lỗi*
- [ ] LLM chỉ **phát event**; ⛔ **không** để LLM tự quyết state cuối cùng

### Hạ tầng

- [ ] `NEW-02` đã được viết thành story trong `Backlog/` **trước khi** code — có AC và có DoD

### ⛔ Điều sprint này KHÔNG làm

- [ ] ⛔ **Không** dùng `pgvector` / vector search — `B5` = `❌` ở mọi mốc tới MVP2. ⭐ *"**Story Bible LÀ index của mình**"* (`CF-9.2`)
- [ ] ⛔ **Không** viết Director scene → page → panel — `C2` = `⛔` ở MVP1

---

## 5. Rủi ro sprint này

| Rủi ro | Tín hiệu sớm | Xử lý |
|---|---|---|
| ⭐ Extraction kém trên truyện tiếng Việt scrape thật | Chạy thử ra entity rời rạc, sai tên riêng | ⭐ **Tăng phần human-in-the-loop, ⛔ KHÔNG kéo dài mốc** — [Roadmap §3.2](../Roadmap.md#32-mvp1--story-intelligence-102026--122026) đã chốt cách xử lý này |
| Dùng LLM cho text clean vì *"nhanh hơn viết regex"* | Thấy prompt kiểu *"hãy xoá phần quảng cáo"* | ⛔ **Sai kiến trúc.** Text clean là job của code deterministic (Analysis §5.5). LLM ở đây = ⛔ không tái lập được, và tốn tiền mỗi lần chạy |
| Để LLM sở hữu state thay vì phát event | Thấy prompt hỏi *"nhân vật đang mặc gì ở chương 5"* | Code sở hữu state. LLM phát event, code reduce. Đảo lại = ⛔ không kiểm chứng được, ⛔ không tái lập |
| `B-04` vượt 20h vì flashback phức tạp hơn dự kiến | Hết tuần 2 mà test flashback vẫn đỏ | Đây là story đã được ghi *vượt trần có lý do*. Mượn giờ từ `O4`; nếu vẫn tràn ⇒ kích van xả |
| Ba story cuối phụ thuộc chuỗi ⇒ **⛔ không song song hoá được** | — (cấu trúc) | Đã tính khi xếp thứ tự. Đây là lý do sprint này 56h chứ ⛔ không phải 60h |

---

## 6. Retro checklist

- [ ] `burn_tích_luỹ` = giờ thực tích luỹ / **301h**. Ghi số
- [ ] > **105%** ⇒ ⭐ kích van kế tiếp. ⚠️ Đường burn-down chạm **100%** tại đây
- [ ] `M1-2` đã đạt chưa? Nếu chưa, `M1-3` và `M1-6` ở S6 ⛔ **không có gì để chấm**
- [ ] `NEW-02` lệch bao nhiêu so với `[EM]` 8h? ⇒ hiệu chỉnh `NEW-03` (S6) theo cùng tỉ lệ
- [ ] `O4`: tích luỹ **10 post** + **9 cuộc trò chuyện**? ⚠️ Còn **1 sprint + 1 tuần** để đạt **20 cuộc** của `KR4.3`

---

## 7. Tài liệu tham khảo

- [Plan-MVP1-Story-Intelligence.md](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md) · [WBS-MVP1.md](../Estimates/WBS-MVP1.md)
- [ADR-008](../../030-Specs/Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) — cơ sở `NEW-02`
- [ADR-011](../../030-Specs/Architecture/ADR-011-Narrative-Time-Key-And-State-Reduction.md) — cơ sở `B-04`
- [Spec-Integration-LLM-Provider](../../030-Specs/API/Spec-Integration-LLM-Provider.md) · [Endpoint-Chapter-Ingest](../../030-Specs/API/Endpoint-Chapter-Ingest.md) · [Endpoint-Timeline-Event](../../030-Specs/API/Endpoint-Timeline-Event.md)
- [DB-Entity-Story-Bible](../../030-Specs/Schema/DB-Entity-Story-Bible.md) · [DB-Entity-Narrative-Timeline](../../030-Specs/Schema/DB-Entity-Narrative-Timeline.md)
- [UC-01-Upload-And-Ingest-Chapter](../../020-Requirements/Use-Cases/UC-01-Upload-And-Ingest-Chapter.md)
- [`mvp0/chapters/ch01.md`](../../../mvp0/chapters/ch01.md) — chapter thật dùng để chạy `M1-2`

---

_Created by product-manager_
_Author: trisjr_
