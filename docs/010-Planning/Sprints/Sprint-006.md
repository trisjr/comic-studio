---
id: SPRINT-006
type: sprint
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, sprint, eval-kit, story-bible-editor, frontend, gate-g2]
linked-to: "../Implementation-Plans/Plan-MVP1-Story-Intelligence.md"
created: 2026-09-05
updated: 2026-09-05
---

# Sprint 006 — Editor & eval kit: nơi moat lộ ra

| | |
|---|---|
| **Thời gian** | `14/12/2026` – `25/12/2026` (2 tuần) · **+ tuần gate** `28/12` – `31/12` |
| **Capacity** | Sprint 60h · **Kỹ thuật 54h** + `O4` 7h = ⚠️ **61h** · Tuần gate **24h** |
| **Mốc** | MVP1 — **sprint cuối** |
| **Exit criteria trả** | ⭐ `M1-3` · ⭐ `M1-6` |
| **OKR phục vụ** | `O2` / `KR2.2`, `KR2.3` · `O3` / `KR3.2` |
| **Điều kiện vào** | ⭐ `M1-2` đạt ở Sprint 005 — ⛔ không có extraction chạy được thì ⛔ không có gì để chấm |

## Mục lục

1. [Mục tiêu sprint](#1-mục-tiêu-sprint)
2. [Story](#2-story)
3. [Tuần gate `28/12` – `31/12`](#3-tuần-gate-2812--3112)
4. [Thứ tự làm & vì sao](#4-thứ-tự-làm--vì-sao)
5. [Definition of Done](#5-definition-of-done)
6. [Rủi ro sprint này](#6-rủi-ro-sprint-này)
7. [Retro MVP1](#7-retro-mvp1)
8. [Tài liệu tham khảo](#8-tài-liệu-tham-khảo)

---

## 1. Mục tiêu sprint

> ⭐ **Hai thứ: cái khách hàng nhìn thấy, và cái ngăn mọi thay đổi về sau trở thành thay đổi mù.**

| Nửa | Story | Vì sao ở sprint cuối |
|---|---|---|
| **Khách nhìn thấy** | `NEW-03` frontend + `D-01` Story Bible editor | [Roadmap §3.2](../Roadmap.md#32-mvp1--story-intelligence-102026--122026) gọi đây là ⭐ *"**nơi moat lộ ra với khách hàng**"*. Nó cần extraction chạy được (S5) mới có dữ liệu để hiển thị |
| **Ngăn thay đổi mù** | `H-01` golden dataset + `H-03` eval kit | *"⛔ Không có eval kit thì mọi thay đổi prompt/model về sau là **thay đổi mù**"* (`CF-8.7` #3) |

### 1.1 ⚠️ Eval kit ở MVP1 đo trục TEXT, ⛔ không phải trục ẢNH

> [!CAUTION]
> Golden dataset của MVP0 dừng ở **`0`** panel ảnh, và Founder đã `[CHỐT]` ⛔ **không** chèn data probe sinh ảnh vào MVP1. ⇒ Eval kit sprint này chấm **extraction**, ⛔ không chấm ảnh.

| | Ground truth | Đo cái gì | Thoả |
|---|---|---|---|
| ⭐ **MVP1 — trục TEXT** | [`mvp0/story-bible.yaml`](../../../mvp0/story-bible.yaml) **viết tay** + [`mvp0/chapters/ch01.md`](../../../mvp0/chapters/ch01.md) | Recall/precision entity (nhân vật + địa điểm) | ⭐ `M1-3` · ⭐ `M1-6` · `KR2.2` · `KR2.3` |
| **MVP3 — trục ẢNH** | 15–20 panel có bảng chấm | 5 tiêu chí `G1-a`…`G1-e` | Nợ `G1` chuyển sang MVP3 — [Plan §3.1](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#31-nợ-1--g1-chưa-từng-được-đo-chốt) |

⚠️ `[EM]` — diễn giải của em. Căn cứ: `M1-3` và `KR2.2` vốn đã định nghĩa phép đo bằng *"khớp Story Bible **viết tay** của MVP0"* — một phép đo thuần text. `M1-6` ⛔ không nói golden dataset **phải** là ảnh.

---

## 2. Story

| Mã | Story | `E_build` | AC chính |
|---|---|--:|---|
| `NEW-03` | ⚠️ **Frontend scaffold `apps/web`** — ⛔ **chưa có story, phải viết trước khi làm** | 10h ⚠️ `[EM]` PM | Vite + React + TS + TanStack Query + shadcn/ui, API client từ `packages/contracts` |
| `D-01` | [Story-Bible-Editor-Form](../../022-User-Stories/Backlog/Story-Story-Bible-Editor-Form.md) | 14h | Form: character · costume · location · state theo event |
| `H-01` | [Golden-Dataset-For-Regression](../../022-User-Stories/Backlog/Story-Golden-Dataset-For-Regression.md) — ⭐ trục TEXT | 6h | Dataset + ground truth + cách chấm, dạng file |
| `H-03` | [HITL-Gate-And-Eval-Kit](../../022-User-Stories/Backlog/Story-HITL-Gate-And-Eval-Kit.md) | 24h ⚠️ vượt trần | ⭐ Eval kit **cho ra SỐ**, sinh tự động |
| | **Cộng kỹ thuật** | ⚠️ **54h** | |
| | `O4` — 2 post + **~11 cuộc trò chuyện** hoàn tất `KR4.3` | 7h | ⚠️ xem [§6](#6-rủi-ro-sprint-này) |

---

## 3. Tuần gate `28/12` – `31/12`

Capacity **24h** (4 ngày × 6h).

| Việc | Giờ | Nội dung |
|---|--:|---|
| `C-01` [Comic-IR-Panel-Specification](../../022-User-Stories/Backlog/Story-Comic-IR-Panel-Specification.md) | 20h | Bảng spec ở schema `comic` + FK tới Story Bible + constraint trường bắt buộc |
| `GATE` Chạy `G2` + ghi verdict + retro MVP1 | 4h | Xem [§3.2](#32-gate-g2--verdict-đã-biết-trước) |

### 3.1 ⭐ `C-01` chính là van xả #2

`C-01` đặt ở tuần cuối **có chủ đích**: ⛔ **không một hạng mục nào của MVP1 tiêu thụ Comic IR** — `C-02`…`C-07` đều `⛔` ở MVP1. Nếu tràn tới đây, `C-01` thu về **schema tối thiểu** (giữ đủ cột + FK; đẩy `CHECK` constraint sang MVP2 cùng `C-04`/`C-05`) là quyết định **đã hoạch định**, ⛔ không phải một cuộc thương lượng dưới áp lực. Xem [Plan §6.2](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#62-danh-sách-van-theo-thứ-tự-kích).

### 3.2 Gate `G2` — verdict đã biết trước

> [!CAUTION]
> Cả **bốn** tiêu chí `G2-a`…`G2-d` đều đòi dữ liệu **image generation**, mà MVP1 có `A1 = ⛔`. ⇒ Verdict ⭐ **`KHÔNG CHẠY ĐƯỢC`** đã biết từ `2026-09-05`, ⛔ **không phải** một rủi ro phát sinh.

- [ ] Ghi verdict `G2` = ⭐ **`KHÔNG CHẠY ĐƯỢC`** ra văn bản, kèm bốn dòng lý do — ⇒ ⭐ **`KR3.2` ĐẠT**
- [ ] Ghi rõ `KR3.1` ⛔ **KHÔNG ĐẠT** và lý do — ⛔ không viết lại KR cho vừa kết quả
- [ ] Ghi rõ `M1-7` ⛔ **KHÔNG TRẢ ĐƯỢC** — `usage_daily` có **cấu trúc** nhưng ⛔ không có dữ liệu image gen chảy vào
- [ ] ⛔ **Không** tick `PASS`, ⛔ **không** tick `FAIL` — cùng kỷ luật mà [`g1-verdict.md`](../../../mvp0/golden-dataset/g1-verdict.md) đã áp cho `G1`: tick một dải kết luận khi ⛔ không có số đo là ⭐ **bịa ra một phép đo chưa từng xảy ra**
- [ ] Chuyển câu hỏi kinh tế sang **MVP3** + ghi hàng mới vào [Risk-Register](../Risk-Register.md)

---

## 4. Thứ tự làm & vì sao

| # | Việc | Vì sao ở vị trí này |
|:-:|---|---|
| 1 | `H-01` golden dataset | Rẻ (6h) và là **đầu vào** của `H-03`. ⛔ Không có ground truth thì eval kit ⛔ không có gì để so |
| 2 | `H-03` eval kit | Việc lớn nhất. Trả **cả hai** `M1-3` và `M1-6`. Làm sớm để còn thời gian **chạy lại** nếu extraction dưới 80% |
| 3 | `NEW-03` frontend scaffold | ⛔ Không chặn `H-03`, nên làm song song về mặt lịch nhưng sau về mặt ưu tiên |
| 4 | `D-01` Story Bible editor | Cần scaffold. Nếu tràn, đây và `NEW-03` là **van #4** — nhưng chỉ sau khi van #2, #3 đã kích |

---

## 5. Definition of Done

### ⭐ `M1-6` — eval kit cho ra SỐ

- [ ] Tồn tại một **báo cáo eval có SỐ**, ⭐ **sinh tự động** — ⛔ không chấm bằng ấn tượng
- [ ] Eval kit chạy được trên golden dataset **mức TEXT** và cho ra recall/precision entity
- [ ] Chạy lại được bằng **một lệnh**, kết quả **tái lập** trên cùng đầu vào

### ⭐ `M1-3` — extraction ≥80%

- [ ] Extraction đạt ⭐ **≥80%** entity (nhân vật + địa điểm) khớp Story Bible viết tay của MVP0
- [ ] ⚠️ Ngưỡng 80% là `[EM]` do writer Roadmap định nghĩa, ⛔ **không có nguồn ngoài** — ghi kèm nhãn khi báo cáo số
- [ ] Dưới 80% ⇒ ⭐ **tăng human-in-the-loop, ⛔ KHÔNG kéo dài mốc** (`P-R4`)

### Editor

- [ ] `apps/web` chạy được: Vite + React + TS + TanStack Query + shadcn/ui + Tailwind, theo [`ADR-001`](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md)
- [ ] Frontend là ⭐ **SPA thuần** — ⛔ không SSR, ⛔ không server action (`ADR-001` CHỐT #5)
- [ ] Form validate bằng **cùng** zod schema từ `packages/contracts` mà backend dùng — ⛔ không định nghĩa lại
- [ ] Story Bible editor sửa được: character · costume · location · state theo event
- [ ] ⭐ **Mọi** hành động sửa trong editor ghi vào `change_log` (`KC-2`, kế thừa `D-02`) — ⛔ không có đường sửa nào bỏ qua
- [ ] `NEW-03` đã được viết thành story trong `Backlog/` **trước khi** code

### ⛔ Điều sprint này KHÔNG làm

- [ ] ⛔ **Không** infinite canvas, ⛔ không zoom/pan cả chapter, ⛔ không hình học panel tự do — `D2` = `❌`. Đây là `P-R7` *cám dỗ build canvas*
- [ ] ⛔ **Không** undo/redo xuyên state phân tán — `D3` = `❌`
- [ ] ⛔ **Không** làm thành phần editor #1–#4 — MVP1 chỉ có ⭐ **thành phần #5**

---

## 6. Rủi ro sprint này

| Rủi ro | Tín hiệu sớm | Xử lý |
|---|---|---|
| ⭐ **`KR4.3` dồn toa** — cần 20 cuộc trò chuyện **trước 31/12**, mà nhịp 2/sprint chỉ cho ~11 cuộc | Hết S5 mà tích luỹ < 12 cuộc | ⚠️ **Rủi ro có thật, ⛔ không né được bằng lịch kỹ thuật.** `KR4.3` lấp khoảng trống *willingness-to-pay* nên ⛔ **không được cắt** — phải tăng nhịp từ **S3**, ⛔ không đợi tới đây |
| Extraction dưới 80% ở lần chấm đầu | Báo cáo eval đầu tiên ra số thấp | Đã có xử lý sẵn: tăng human-in-the-loop. ⛔ **Không** kéo dài mốc, ⛔ **không** hạ ngưỡng cho vừa kết quả |
| ⭐ Cám dỗ build canvas | Bắt đầu viết zoom/pan hoặc kéo thả tự do | [MVP-Scope §4.1](../MVP-Scope.md#41-canvas-editor-14--cắt-một-phần-cf-91). Đây là *"chi phí lớn nhất, giá trị tăng thêm nhỏ nhất"* |
| `H-03` vượt 24h ⇒ ăn vào tuần gate | Hết tuần 1 mà eval kit ⛔ chưa chạy được lần nào | Ưu tiên `M1-6` (**có số**) trên `M1-3` (**đạt ngưỡng**). Một báo cáo có số thấp vẫn tốt hơn ⛔ không có báo cáo |
| Editor bỏ qua `change_log` cho *"thao tác nhỏ"* | Thấy đường sửa nào ⛔ không ghi log | `KC-2` đòi **mọi** hành động. Bỏ sót = thủng hồ sơ pháp lý, và ⛔ **không backfill được** |

---

## 7. Retro MVP1

Đây là retro **cuối mốc**, ⛔ không chỉ cuối sprint.

### 7.1 Số phải chốt

- [ ] `burn_tích_luỹ` cuối cùng = giờ thực / **386h**. Ghi số thật, ⛔ không làm tròn xuống
- [ ] Bảy ước lượng `[EM]` do PM đặt lệch trung bình bao nhiêu %? ⇒ hệ số hiệu chỉnh cho WBS của MVP2
- [ ] Đã kích bao nhiêu van xả? Van nào? Vì sao?
- [ ] `E_hitl` thực đo của `D-01` và `H-03` là bao nhiêu? ⭐ **Phải ghi ngay lần chạy đầu**, ⛔ không ước lượng lùi — nó ăn thẳng vào biên lợi nhuận mà `G2` sẽ đo ở MVP3

### 7.2 Bảng nghiệm thu `M1-1`…`M1-7`

| # | Trạng thái kỳ vọng |
|:-:|---|
| `M1-1` | ✅ PASS ở S1 |
| `M1-2` | ✅ đạt ở S5 |
| `M1-3` | ✅ đạt ở S6 (⚠️ hoặc ghi số thật nếu < 80%) |
| `M1-4` | ✅ đạt ở S2 |
| `M1-5` | ✅ PASS ở S4 |
| `M1-6` | ✅ đạt ở S6 |
| `M1-7` | ⛔ **KHÔNG TRẢ ĐƯỢC** — đã biết trước `[CHỐT]` |

### 7.3 Ba việc bàn giao cho MVP2

- [ ] Nợ `G1` (5 tiêu chí ảnh) → **MVP3**, đã ghi Risk-Register
- [ ] Câu hỏi kinh tế `G2` → **MVP3**, đã ghi Risk-Register
- [ ] `STORY-G-06` AI disclosure → **MVP2** (van #1 đã kích) — ⚠️ deadline tuân thủ **~01/03/2027**, ⛔ không được quên lần hai
- [ ] Chạy `/memo` để đúc kết vào `knowledge-base/45-Role-Memory/product-manager/`

---

## 8. Tài liệu tham khảo

- [Plan-MVP1-Story-Intelligence.md](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md) · [WBS-MVP1.md](../Estimates/WBS-MVP1.md)
- [MVP-Scope §5](../MVP-Scope.md#5-editor-tối-thiểu--ranh-giới-chi-tiết) — ranh giới editor tối thiểu · [§7.3](../MVP-Scope.md#73-g2--gate-kinh-tế-sau-mvp1) — định nghĩa `G2`
- [OKRs.md](../OKRs.md) — `KR2.2`, `KR2.3`, `KR3.1`, `KR3.2`, `KR4.3`
- [ADR-001](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) · [ADR-012](../../030-Specs/Architecture/ADR-012-Comic-IR-Spec-As-Primary-Data.md)
- [Endpoint-Story-Bible](../../030-Specs/API/Endpoint-Story-Bible.md) · [Endpoint-Eval-Kit](../../030-Specs/API/Endpoint-Eval-Kit.md) · [Endpoint-Panel-Script](../../030-Specs/API/Endpoint-Panel-Script.md)
- [DB-Entity-Comic-IR](../../030-Specs/Schema/DB-Entity-Comic-IR.md) · [DB-Entity-Quality-Assets](../../030-Specs/Schema/DB-Entity-Quality-Assets.md)
- [UC-02-Review-And-Edit-Story-Bible](../../020-Requirements/Use-Cases/UC-02-Review-And-Edit-Story-Bible.md)
- [`mvp0/story-bible.yaml`](../../../mvp0/story-bible.yaml) — ground truth của eval kit
- [Design-System](../../040-Design/Design-System/Foundations.md) — nền UI cho `NEW-03`

---

_Created by product-manager_
_Author: trisjr_
