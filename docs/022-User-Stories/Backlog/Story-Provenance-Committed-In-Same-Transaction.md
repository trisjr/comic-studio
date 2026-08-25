---
id: STORY-G-02
type: story
status: draft
created: 2026-08-24
---

# Story-Provenance-Committed-In-Same-Transaction

## 1. Story

> Là khách hàng SaaS, tôi muốn **`generation` + `change_log` + `usage_event` commit CÙNG MỘT transaction**, để **bằng chứng của tôi không thể thiếu ngẫu nhiên**.

## 2. Part of

| Quan hệ | Tài liệu |
|---|---|
| **Epic cha** | [Epic-Legal-And-Compliance](../Epics/Epic-Legal-And-Compliance.md) — hàng 2/6 mục 3 |
| **BRD cha** | [BRD-007-Legal-And-Compliance](../../020-Requirements/BRD/BRD-007-Legal-And-Compliance.md) — `BR-007-02`, `KC-4` §4.1 |
| **Use Case liên quan** | [UC-06 — Generate Panel And Pick Variant](../../020-Requirements/Use-Cases/UC-06-Generate-Panel-And-Pick-Variant.md) — nơi artifact (generation) và các bản ghi audit đi kèm được tạo cùng lúc |
| **Phụ thuộc chéo** | [Story-Modular-Monolith-Three-Schemas](./Story-Modular-Monolith-Three-Schemas.md) — chưa có file tại thời điểm Story này được tạo; `KC-4` cần **một** transaction boundary, tức **một** DB (modular monolith), theo đúng cách Epic cha đã ghi ở mục 3 |

## 3. Bối cảnh & nguồn

- **Hạng mục MVP-Scope**: [MVP-Scope §3 GP-1](../../010-Planning/MVP-Scope.md#3-bảng-mvp-vs-full-scope) (bảng cha của `KC-4`) · [MVP-Scope §6 KC-4](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng) — *"Cả ba mục KC-1, KC-2, KC-3 phải commit CÙNG MỘT TRANSACTION với artifact mà chúng chứng minh"*.
- **Exit criterion Roadmap**: [Roadmap §2 — M1-5](../../010-Planning/Roadmap.md#2-bảng-lộ-trình-tổng) — *"...và có test chứng minh chúng commit CÙNG MỘT transaction với artifact"*. Đây là **tiêu chí #2** của M1-5, tách biệt với tiêu chí #1 (5 cột tồn tại, thuộc `Story-Provenance-Chain-Parent-Generation`).
- **Lý do kiến trúc**: [MVP-Scope §4.2](../../010-Planning/MVP-Scope.md#42-microservices--vector-db-12--cắt-cf-92) — nghĩa vụ audit đòi **một** transaction boundary vì *"RLS không bảo vệ join phía ứng dụng"* và *"bằng chứng có thể thiếu ngẫu nhiên thì không phải bằng chứng"* (CF-9.2 lý do 2).
- **`Valuable-I`**: audit trail commit tách rời artifact là audit trail **không đáng tin về mặt pháp lý** — nếu `generation` commit thành công nhưng `change_log`/`usage_event` thất bại do lỗi transaction (crash, timeout), hồ sơ chứng minh *"decisive contribution"* có thể thiếu mà không ai biết, và **không backfill được** cho các generation đã xảy ra.
- **Epic DoD liên quan** ([Epic-Legal-And-Compliance §5.1 tiêu chí #2](../Epics/Epic-Legal-And-Compliance.md#5-definition-of-done-cấp-epic)): *"Tiêu chí #2 là một TEST, không phải một màn hình. `KC-4` là thuộc tính của ba Story khác — nó không có UI để demo."*

## 4. Acceptance Criteria

### Xác minh được

- [ ] Tồn tại **một test tự động** khẳng định: khi một generation được tạo, dòng `generation` + dòng `change_log` tương ứng + dòng `usage_event` tương ứng (nếu nghiệp vụ có phát sinh usage) được ghi trong **cùng một database transaction** — đo bằng: test giả lập lỗi (raise exception) ngay sau khi ghi `generation` nhưng trước khi ghi `change_log`, kỳ vọng **toàn bộ ba bảng rollback về 0 dòng mới**.
- [ ] Test trên PASS trong CI ở trạng thái hiện tại của schema — đo bằng: tên test cụ thể + kết quả PASS được ghi lại (theo `Epic DoD #2`: *"có TEST chứng minh"*, không phải "đã thấy đủ cột trong DB").
- [ ] Toàn bộ pipeline ghi provenance nằm trong **một** connection pool tới **một** PostgreSQL instance (modular monolith, CF-9.2) — đo bằng: kiểm tra cấu hình kết nối DB của service tạo generation, xác nhận không gọi tới service/DB khác để ghi `change_log` hoặc `usage_event`.

### Đường không hạnh phúc (unhappy path)

- [ ] Nếu transaction bị abort giữa chừng (deadlock, timeout, out-of-memory), **không** dòng nào trong ba bảng (`generation`, `change_log`, `usage_event`) được giữ lại một phần — đo bằng test gây deadlock có chủ đích và kiểm tra trạng thái sau rollback.
- [ ] Hai generation được tạo gần như đồng thời cho hai panel khác nhau không được phép chia sẻ hoặc trộn transaction với nhau (mỗi request có transaction boundary riêng) — đo bằng test 2 request song song, xác nhận rollback của request A không ảnh hưởng tới commit của request B.
- [ ] Nếu một service khác (ví dụ worker sinh ảnh) cố gắng ghi `usage_event` cho một generation mà `generation` đó chưa commit, thao tác đó phải bị từ chối hoặc chờ đúng transaction, không được tạo `usage_event` mồ côi.

### Ràng buộc cứng không được vi phạm

- `KC-4` — `generation` + `change_log` + `usage_event` phải commit CÙNG MỘT transaction với artifact mà chúng chứng minh.

### Story này KHÔNG làm

- [ ] **KHÔNG** định nghĩa lại schema của `parent_generation_id` / `relation_kind` / `field_provenance` / `origin` — đó là phạm vi của `Story-Provenance-Chain-Parent-Generation` (`KC-1`, `KC-3`).
- [ ] **KHÔNG** thiết kế modular monolith / 3 schema từ đầu — Story này **tiêu thụ** kiến trúc một-DB đã được `Story-Modular-Monolith-Three-Schemas` cung cấp, không tự dựng lại.
- [ ] **KHÔNG** có màn hình hay báo cáo hiển thị cho người dùng — nghiệm thu **chỉ** bằng test, theo đúng ghi chú DoD của Epic cha.

## 5. Ước lượng

| Đại lượng | Giá trị | Ghi chú |
|---|---|---|
| `E_build` | `TBD` | Không có ước lượng bottom-up trong repo (`Roadmap §1.3`: *"Tổng tuần-người: TBD"*). `MVP-Scope §6 KC-4` mô tả chi phí giữ là *"kỷ luật code + monolith 1 DB"* — định tính. **Điều kiện escalate**: Story này **không split được** theo mục 6 (`I` và `S` đều `⚠️⚠️`) ⇒ nếu ước lượng thực tế vượt **16 giờ-người**, phải ghi lý do vượt trần thành văn thay vì tách lô. |
| `E_hitl` | `0` giờ-người/chapter | Story kiểm chứng bằng test tự động, không tạo bước xác nhận thủ công lặp lại theo chapter. |

## 6. INVEST

| Tiêu chuẩn | Đánh giá |
|---|---|
| Independent | ⚠️⚠️ **VỠ.** [`findings/business-analyst.md` §4.10](../../010-Planning/pm-runs/2026-08-24-khoi-tao-requirements-stories-comic-studio/findings/business-analyst.md#410-bảy-story-sẽ-vỡ-khi-cắt-lô--pm-cần-biết-trước): *"`KC-4` là một thuộc tính của ba Story khác, không phải một feature. Nó phụ thuộc `Story-Modular-Monolith-Three-Schemas` (một DB) và bị chứng minh bằng một TEST, không bằng một màn hình."* |
| Negotiable | ⚠️ **Bị giới hạn** — `KC-4` nằm trong bảy mục không mở ra thương lượng scope ([MVP-Scope §6](../../010-Planning/MVP-Scope.md#6-không-được-cắt--danh-sách-cứng)). |
| Valuable | `Valuable-I` — xem mục 3: mất tính đáng tin cậy pháp lý của audit trail nếu commit thiếu ngẫu nhiên, không phải một tính năng người dùng thấy. |
| Estimable | Estimable bằng giờ-người, hiện `TBD` — xem mục 5. |
| Small | ⚠️⚠️ **VỠ** (cùng dòng §4.10 với `I`, table gốc không tách hai lý do): *"`KC-4` là một thuộc tính của ba Story khác... bị chứng minh bằng một TEST, không bằng một màn hình"* — kích thước thực tế của Story neo vào việc ba Story kia (provenance chain, modular monolith, usage event) đã tồn tại đủ để test có gì mà xác nhận, không tự nhỏ được. |
| Testable | Testable bằng một test tự động cụ thể — xem mục 4 AC-1. |

> **Kết luận mục 6**: `I` và `S` đều `⚠️⚠️` theo đúng nguyên văn `findings/business-analyst.md` §4.10 — lý do được trích chung cho cả hai cột trong bảng gốc, không phải suy luận riêng của lô này.
