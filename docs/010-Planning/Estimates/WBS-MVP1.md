---
id: WBS-001
type: wbs
status: draft
project: comic-studio
owner: "@trisjr"
tags: [mvp1, wbs, estimate, capacity]
linked-to: "../Implementation-Plans/Plan-MVP1-Story-Intelligence.md"
created: 2026-09-05
updated: 2026-09-05
---

# WBS & ETA — MVP1 Story Intelligence

> [!IMPORTANT]
> **Quy ước nhãn**: `[EM]` ước lượng, ⛔ **không phải số đo** · `[CHỐT]` quyết định Founder.
>
> ⚠️ **Toàn bộ con số trong tài liệu này là `[EM]`.** ⛔ Không một dòng nào là số đo từ công việc đã hoàn thành. Cột *Nguồn* nói rõ mỗi con số đến từ đâu — **story** (ước lượng bottom-up đã có trong backlog) hay **PM** (em đặt, vì story ghi `TBD`).

> [!NOTE]
> ⭐ **Vì sao `.md` mà ⛔ không phải `.xlsx`.** [RULE-001](../../../knowledge-base/99-Templates/Documents-Template.md) *Document Type Mapping* ghi `WBS-{ProjectName}.xlsx`. Tài liệu này cố ý lệch khỏi đuôi file đó vì `.xlsx` là **binary ⛔ không diff được** — mọi lần chỉnh một ô sẽ vào git log như một khối nhị phân đục, ⛔ không review được và ⛔ không truy vết được. Toàn bộ kho tri thức của dự án là text, và [`ADR-001`](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md) đã đặt tiền lệ *"SQL thô là nguồn sự thật"* cho cùng một lý do. **Thư mục đích và tiền tố tên file giữ đúng mapping.**

## Mục lục

1. [Cách đọc bảng](#1-cách-đọc-bảng)
2. [Capacity](#2-capacity)
3. [WBS — phân rã theo sprint](#3-wbs--phân-rã-theo-sprint)
4. [Bảy ước lượng do PM đặt — căn cứ từng con số](#4-bảy-ước-lượng-do-pm-đặt--căn-cứ-từng-con-số)
5. [Ba khoảng trống backlog](#5-ba-khoảng-trống-backlog)
6. [Hạng mục ⛔ KHÔNG tốn giờ ở MVP1](#6-hạng-mục-⛔-không-tốn-giờ-ở-mvp1)
7. [`E_hitl` — chi phí vận hành lặp lại](#7-e_hitl--chi-phí-vận-hành-lặp-lại)
8. [ETA & burn-down dự kiến](#8-eta--burn-down-dự-kiến)
9. [Tài liệu tham khảo](#9-tài-liệu-tham-khảo)

---

## 1. Cách đọc bảng

| Cột | Nghĩa |
|---|---|
| `E_build` | Giờ-người để **xây xong một lần**. ⛔ Không bao gồm vận hành lặp lại |
| `E_hitl` | Giờ-người **lặp lại mỗi chapter** do story tạo ra. Xem [§7](#7-e_hitl--chi-phí-vận-hành-lặp-lại) |
| **Nguồn** | `story` = ước lượng bottom-up đã có trong file story · `PM` = em đặt vì story ghi `TBD` |
| **Trần 16h** | Quy ước cắt lô của dự án. Vượt trần ⇒ **phải ghi lý do thành văn**, ⛔ không tự split |

---

## 2. Capacity

| | |
|---|---|
| **Nhịp** | **30 giờ/tuần** `[CHỐT]` Founder `2026-09-05` |
| **Cửa sổ** | `05/10/2026` → `31/12/2026` |
| **Số tuần** | 12 tuần trọn + 4 ngày |
| **Capacity** | `12 × 30 + 4 × 6` = ⭐ **384 giờ-người** |
| `01–02/10/2026` | 2 ngày setup môi trường — ⛔ **không** tính vào sprint nào |

---

## 3. WBS — phân rã theo sprint

### Sprint 001 · `05/10` – `16/10` · Nền tenancy

| Mã | Hạng mục | `E_build` | Nguồn | Trần 16h |
|---|---|--:|:-:|:-:|
| `E-02` | Tenant / User / Membership là ba entity riêng | 8h | story | ✅ |
| `E-01` | `tenant_id NOT NULL` + RLS trên **100%** bảng | 24h | story | ⚠️ vượt — lý do đã ghi trong story (⛔ không split được: DoD là test nhị phân toàn cục) |
| `E-05` | Modular monolith — phần còn lại | 6h | story `14h` − `8h` đã xong PR #24 | ✅ |
| `NEW-01` | CI pipeline | 8h | **PM** `[EM]` | ✅ |
| | **Cộng kỹ thuật** | **46h** | | |
| | `O4` go-to-market | 7h | PM `[EM]` | |
| | **Tổng sprint** | **53h** | | |

### Sprint 002 · `19/10` – `30/10` · Cửa pháp lý & đường vào

| Mã | Hạng mục | `E_build` | Nguồn | Trần 16h |
|---|---|--:|:-:|:-:|
| `E-03` | Object storage `tenant/{tenant_id}/{sha256}`, ⛔ không dedup chéo | 10h | story | ✅ |
| `E-04` | **Mua** authentication provider | 12h | story | ✅ |
| `G-03` | Kiểm opt-out Điều 37b tại ingest | 12h | **PM** `[EM]` | ✅ |
| `G-04` | ToS + user warrant + `ON DELETE CASCADE` + hard-delete | 18h | **PM** `[EM]` | ⚠️ vượt — xem [§4](#4-bảy-ước-lượng-do-pm-đặt--căn-cứ-từng-con-số) |
| | **Cộng kỹ thuật** | **52h** | | |
| | `O4` go-to-market | 8h | PM `[EM]` | |
| | **Tổng sprint** | **60h** | | |

### Sprint 003 · `02/11` – `13/11` · Provenance

| Mã | Hạng mục | `E_build` | Nguồn | Trần 16h |
|---|---|--:|:-:|:-:|
| `B-01` | Sửa khoá thời gian `(chapter, scene)` | 8h | story | ✅ |
| `G-01` | `parent_generation_id` + `relation_kind` + `field_provenance` + `origin` | 14h | **PM** `[EM]` | ✅ |
| `D-02` | `change_log` ghi **mọi** hành động người dùng | 20h | story | ⚠️ vượt — lý do đã ghi trong story |
| `F-02` | `cost_usd` + `model_id` + `model_version` + `attempt_no` | 10h | story | ✅ |
| | **Cộng kỹ thuật** | **52h** | | |
| | `O4` go-to-market | 8h | PM `[EM]` | |
| | **Tổng sprint** | **60h** | | |

### Sprint 004 · `16/11` – `27/11` · Sổ cái & ranh giới transaction

| Mã | Hạng mục | `E_build` | Nguồn | Trần 16h |
|---|---|--:|:-:|:-:|
| `F-01` | `usage_event` append-only + rollup `usage_daily` | 12h | story | ✅ |
| `G-02` | **Test** chứng minh provenance commit cùng một transaction | 12h | **PM** `[EM]` | ✅ |
| `A-05` | Job queue trong Postgres (`FOR UPDATE SKIP LOCKED`) | 12h | story | ✅ |
| `H-04` | Log preference data | 10h | story | ✅ |
| `H-05` | Abuse controls tối thiểu — phần 🟡 của MVP1 | 4h | **PM** `[EM]` | ✅ |
| `G-05` | Safe harbour Điều 198b — phần 🟡 của MVP1 | 6h | **PM** `[EM]` | ✅ |
| | **Cộng kỹ thuật** | **56h** | | |
| | `O4` go-to-market | 8h | PM `[EM]` | |
| | **Tổng sprint** | ⚠️ **64h** — vượt capacity danh nghĩa `60h` | | |

### Sprint 005 · `30/11` – `11/12` · Story Intelligence

| Mã | Hạng mục | `E_build` | Nguồn | Trần 16h |
|---|---|--:|:-:|:-:|
| `NEW-02` | LLM provider adapter | 8h | **PM** `[EM]` | ✅ |
| `B-02` | Chapter ingest + text clean (deterministic) | 10h | story | ✅ |
| `B-03` | Story Bible extraction | 18h | story | ⚠️ vượt — lý do đã ghi trong story |
| `B-04` | Timeline state resolver `state_at(N) = reduce(events)` | 20h | story | ⚠️ vượt — lý do đã ghi trong story |
| | **Cộng kỹ thuật** | **56h** | | |
| | `O4` go-to-market | 8h | PM `[EM]` | |
| | **Tổng sprint** | ⚠️ **64h** — vượt capacity danh nghĩa `60h` | | |

### Sprint 006 · `14/12` – `25/12` · Editor & eval kit

| Mã | Hạng mục | `E_build` | Nguồn | Trần 16h |
|---|---|--:|:-:|:-:|
| `NEW-03` | Frontend app scaffold `apps/web` | 10h | **PM** `[EM]` | ✅ |
| `D-01` | Story Bible editor form (thành phần #5) | 14h | story | ✅ |
| `H-01` | Golden dataset regression — ⭐ **trục TEXT** | 6h | story | ✅ |
| `H-03` | HITL gate + eval kit | 24h | story | ⚠️ vượt — lý do đã ghi trong story |
| | **Cộng kỹ thuật** | **54h** | | |
| | `O4` go-to-market | 7h | PM `[EM]` | |
| | **Tổng sprint** | ⚠️ **61h** — vượt capacity danh nghĩa `60h` | | |

### Tuần gate · `28/12` – `31/12`

| Mã | Hạng mục | `E_build` | Nguồn |
|---|---|--:|:-:|
| `C-01` | Comic IR / Panel Specification | 20h | story (⚠️ vượt trần, lý do đã ghi) |
| `GATE` | Chạy `G2` + ghi verdict + retro MVP1 | 4h | **PM** `[EM]` |
| | **Tổng** | ⚠️ **24h** — capacity tuần này chỉ **24h** (4 ngày × 6h) | |

### Tổng hợp

| | Giờ |
|---|--:|
| Kỹ thuật (26 story + 3 khoảng trống + gate) | **340h** |
| `O4` go-to-market | **46h** |
| **TỔNG TẢI** | ⭐ **386h** |
| **CAPACITY** | **384h** |
| **ĐỆM** | ⚠️ **−2h** = **100,5% load** |

---

## 4. Bảy ước lượng do PM đặt — căn cứ từng con số

> [!CAUTION]
> Bảy story dưới đây ghi `E_build: TBD` trong backlog. Em đặt số để WBS có nghĩa, ⛔ **không** để giả vờ rằng chúng đã được ước lượng bottom-up. **Đây là rủi ro `P-R2`** trong [Plan §10](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#10-rủi-ro--tín-hiệu-sớm): nếu story đầu tiên trong nhóm này vượt >30%, phải ước lượng lại **cả bảy**.

| Mã | Giờ | Căn cứ em suy ra con số |
|---|--:|---|
| `G-01` | **14h** | **10 AC.** Bốn cột/quan hệ (`parent_generation_id` FK · `relation_kind` ENUM · `field_provenance` bảng phụ · `origin` ENUM) + constraint `NOT NULL` + **test race** hai request đồng thời ⛔ không ghi đè `field_provenance` của nhau. Neo so sánh: `E-02` (8h) cũng là schema thuần nhưng ⛔ không có bảng phụ và ⛔ không có test race ⇒ `+6h` |
| `G-02` | **12h** | **9 AC, ⛔ không có schema mới** — toàn bộ chi phí nằm ở **viết test khó**: rollback giữa chừng, **gây deadlock có chủ đích**, hai request song song ⛔ không trộn transaction, worker ghi `usage_event` cho generation chưa commit. Test deadlock có chủ đích là loại test đắt nhất trong nhóm |
| `G-03` | **12h** | **10 AC.** Đọc **bốn kênh** bảo lưu quyền + log timestamp + chặn pipeline + **fail-safe cho metadata hỏng** + xử lý **batch hỗn hợp**. ⚠️ `KC-6` ghi chi phí **~0** `[OFF]` — nhưng đó là chi phí **vận hành**, ⛔ không phải giờ-người **xây**. ⛔ Không được đọc nhầm hai thứ đó thành một |
| `G-04` | **18h** ⚠️ vượt trần | **12 AC** — cao nhất nhóm. Nặng nhất là AC *"tồn tại đường **xuất dữ liệu đầy đủ** cho tenant: Story Bible, Comic IR, **mọi ảnh**, và cả `change_log` + `field_provenance`"* — đó là một export toàn schema, ⛔ không phải một script `DELETE`. Cộng: `ON DELETE CASCADE` toàn bộ FK + test hard-delete ⛔ không chạm tenant khác + test gián đoạn giữa chừng + checkbox warrant chặn ở **server**. ⭐ **Lý do ⛔ không split**: [MVP-Scope §4](../MVP-Scope.md) ghi *"**đường thoát phải được xây cùng lúc với đường vào**"* — tách export ra khỏi hard-delete để lại đúng khoảng trống mà story tồn tại để chặn |
| `G-05` | **6h** | **13 AC toàn story, nhưng MVP1 chỉ `🟡`.** Trigger *"mở cho người ngoài upload"* ⛔ chưa đến ở MVP1 ⇒ phần thuộc MVP1 chỉ là: dựng **checklist 6 mục** dạng artifact + cột soft-delete + kênh `copyright@`. Phần SLA 72h, đăng ký đầu mối Bộ VHTTDL, counter-notice ⇒ **MVP2** cùng `M2-6` |
| `H-05` | **4h** | Story ghi **8h** cho bản đầy đủ; MVP1 chỉ `🟡`. Phần MVP1 = rate limit/tenant + giới hạn kích thước upload + log provider từ chối. Phần còn lại (`✅` từ MVP2) là tín hiệu abuse nâng cao |
| `GATE` | **4h** | Chạy bốn tiêu chí `G2-a`…`G2-d`, xác nhận cả bốn ⛔ không có dữ liệu, ghi verdict `KHÔNG CHẠY ĐƯỢC` + lý do + cập nhật Risk-Register. ⭐ **Rẻ chính vì ⛔ không có số để tính** — xem [Plan §9](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#9-gate-g2--verdict-đã-biết-trước) |

---

## 5. Ba khoảng trống backlog

> [!CAUTION]
> Ba hạng mục này **⛔ chưa có story nào trong `docs/022-User-Stories/Backlog/`**. Đã verify bằng `ls` và `grep` ngày `2026-09-05`. **Phải viết thành story trước khi sprint chứa nó bắt đầu**, nếu không thì chúng ⛔ không có AC và ⛔ không có DoD.

| Mã | Hạng mục | Giờ | Căn cứ ước lượng | Viết story trước |
|---|---|--:|---|---|
| `NEW-01` | **CI pipeline** | 8h | Workflow chạy `lint` + `typecheck` + `vitest` trên PostgreSQL service container (invariant test hiện tại **đã** cần Postgres thật). Cộng cache pnpm + matrix tối thiểu. ⛔ Không có deploy stage ở MVP1 | **S1** |
| `NEW-02` | **LLM provider adapter** | 8h | Port + một adapter, theo [`ADR-008`](../../030-Specs/Architecture/ADR-008-LLM-Provider-And-Usage-Boundaries.md) và [`Spec-Integration-LLM-Provider`](../../030-Specs/API/Spec-Integration-LLM-Provider.md). Neo so sánh: `A-04` image provider adapter = **6h** trong story; bản LLM cần thêm ghi `cost_usd`/`model_version` cho `F-02` ⇒ `+2h` |
| `NEW-03` | **Frontend scaffold `apps/web`** | 10h | Vite + React + TS + TanStack Query + shadcn/ui + Tailwind theo [`ADR-001`](../../030-Specs/Architecture/ADR-001-Backend-And-Frontend-Tech-Stack.md), cộng API client tiêu thụ zod schema từ `packages/contracts` + tích hợp auth provider của `E-04`. ⭐ Stack **đã chốt** ⇒ đây là công **dựng**, ⛔ không phải công **quyết** | **S6** |

---

## 6. Hạng mục ⛔ KHÔNG tốn giờ ở MVP1

⭐ Mục này tồn tại để một người đọc WBS ⛔ không tưởng rằng chúng bị bỏ sót.

| Hàng scope | Hạng mục | Trạng thái MVP1 | Vì sao **0h** |
|---|---|:-:|---|
| `A2` | Typeset layer + bubble overlay | 🟡 | `🟡` ở MVP0 **và** `🟡` ở MVP1 ⇒ **giữ nguyên trạng, ⛔ không tiến thêm**. ⚠️ `[EM]` diễn giải của em từ bảng scope |
| `A3` | Visual Prompt Compiler deterministic | 🟡 | Cùng lý do. Và ⛔ không có `A1` thì compiler ⛔ không có người gọi |
| `A1` · `A4` | Generate panel · adapter đa provider | ⛔ | Ra khỏi MVP1 `[CHỐT]` — xem [Plan §4.2](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#42-ra-khỏi-mvp1--và-vì-sao) |
| `C2`…`C7` | Director, rubric, ≤3 nhân vật, `text_safe_zone`, hai human gate | ⛔ | Toàn bộ `✅` từ MVP2 |
| `GP-4` | AI disclosure (`STORY-G-06`) | ⛔ | ⭐ **Van xả #1 đã kích** `[CHỐT]` `2026-09-05` — đẩy sang MVP2 |
| `D3`·`D4`·`D5` | Editor thành phần #1–#4 | ⛔ | MVP1 chỉ có thành phần **#5** |
| `F3`·`F4` | Credit ledger · hard quota | ⛔ | MVP3 |
| `H4` | Export PDF / CBZ / webtoon | ⛔ | MVP2 preview server-side trước |

---

## 7. `E_hitl` — chi phí vận hành lặp lại

`E_hitl` ⛔ **không** nằm trong 340h ở [§3](#3-wbs--phân-rã-theo-sprint) — đó là chi phí phát sinh **mỗi chapter** *sau khi* MVP1 chạy.

| Story | `E_hitl` | Nguồn |
|---|--:|:-:|
| `D-01` Story Bible editor form | **~0,5h / chapter** `[EM]` | story |
| `H-03` HITL gate + eval kit | `TBD` | story |
| Toàn bộ 24 story còn lại của MVP1 | **0** | story |

⭐ **Tổng `E_hitl` biết được của MVP1: ~0,5h/chapter**, cộng một ẩn số `TBD` ở `H-03`.

⚠️ `H-03` là ẩn số đáng theo dõi: nếu HITL gate đòi nhiều giờ người/chapter, nó ăn thẳng vào biên lợi nhuận mà `G2` sẽ đo ở MVP3. Con số này **phải được ghi lại ngay lần chạy đầu tiên**, ⛔ không ước lượng lùi.

---

## 8. ETA & burn-down dự kiến

| Mốc | Ngày | Tải tích luỹ | % capacity tích luỹ | Cột mốc mở khoá |
|---|---|--:|--:|---|
| Hết S1 | `16/10` | 53h | 88% | ⭐ `M1-1` — test rò rỉ chéo tenant PASS |
| Hết S2 | `30/10` | 113h | 94% | ⭐ `M1-4` — 100% upload qua opt-out |
| Hết S3 | `13/11` | 173h | 96% | 5/5 hạng mục provenance **tồn tại** |
| Hết S4 | `27/11` | 237h | 99% | ⭐ `M1-5` — test cùng transaction PASS |
| Hết S5 | `11/12` | 301h | 100% | ⭐ `M1-2` — text clean trên chapter scrape thật |
| Hết S6 | `25/12` | 362h | 101% | ⭐ `M1-3` + `M1-6` — eval kit cho ra số |
| Tuần gate | `31/12` | 386h | ⚠️ **100,5%** | `G2` verdict được ghi ⇒ `KR3.2` đạt |

> [!WARNING]
> ⭐ **Đường burn-down này chạm 100% từ S5 và ⛔ không bao giờ xuống lại.** Đó ⛔ không phải một lỗi vẽ biểu đồ — đó là hình ảnh trung thực của một kế hoạch ⛔ không có đệm. **Ngưỡng kích van xả là 105%**, nghĩa là dư địa thật chỉ còn ~5% ở mọi thời điểm.
>
> Cột *% capacity tích luỹ* là **thước đo phải kiểm ở mỗi retro**, ⛔ không phải một con số trang trí. Công thức và bảng hành động: [Plan §6.1](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md#61-ngưỡng-kích).

---

## 9. Tài liệu tham khảo

- [Plan-MVP1-Story-Intelligence.md](../Implementation-Plans/Plan-MVP1-Story-Intelligence.md) — kế hoạch master; WBS này là nguồn số của `§5` và `§7` bên đó
- [Roadmap.md](../Roadmap.md) — khung thời gian và exit criteria `M1-1`…`M1-7`
- [MVP-Scope.md](../MVP-Scope.md) — bảng scope `§3` xác định hạng mục nào `✅`/`🟡`/`⛔` ở MVP1
- [OKRs.md](../OKRs.md) — nguồn của khối `O4` **46h**
- [Sprint-001](../Sprints/Sprint-001.md) … [Sprint-006](../Sprints/Sprint-006.md) — DoD chi tiết từng sprint
- `docs/022-User-Stories/Backlog/` — nguồn của mọi `E_build` gắn nhãn *story*

---

_Created by product-manager_
_Author: trisjr_
