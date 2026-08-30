---
id: ADR-016
type: adr
status: draft
project: comic-studio
created: 2026-08-29
---

# ADR-016: Adapter image provider và pin model version

Related to: [SDD-Comic-Studio](./SDD-Comic-Studio.md)

> [!IMPORTANT]
> **ADR LAI**: **seam CHỐT** (adapter một interface nhiều provider — ⛔ không mở lại) · **provider MẶC ĐỊNH** (đã chọn, có đường lui ghi rõ) · **retry policy + error taxonomy per provider MỞ** (tầng design).
> ⚠️ **VLM QA-select là integration RIÊNG, ⛔ không phải một hàm của adapter này** — xem [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md).

---

## Context

### Quyết định đã CHỐT / MẶC ĐỊNH — ⛔ ADR này ghi lại, không mở lại

| Nội dung | Mã | Nguồn (mã requirement) | Độ rắn |
|---|:--:|---|:--:|
| **Adapter per image provider** là **seam bắt buộc** — một interface, nhiều provider (Gemini 3 Pro Image, FLUX.2); **pin model version tường minh trong config** | `D-40` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-23`** · §4.3 · `MVP-Scope §3 A4` | **LAI** — seam **CHỐT**, provider **MẶC ĐỊNH** |
| Dùng **batch API**, ⛔ không realtime API — *"comic generation vốn là async job queue nên batch là fit tự nhiên"* | `D-41` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-24`** · §4.3 | **MẶC ĐỊNH** — đường lui: `CF-3.11` lấy giá **standard** làm trần an toàn cho MVP0 |
| Render granularity: **per-panel** là mặc định (spec là đơn vị); **whole-page** là **đường lui đã thiết kế sẵn**, đổi được **⛔ KHÔNG đổi data model** | `D-46` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-33`** · §2.1 · `MVP-Scope §3 A7` | **MẶC ĐỊNH** — gắn vào gate `G2` |
| ⛔ **Không mua GPU.** API cho main path; self-host **chỉ** cho LoRA train / upscale / inpainting | `D-07` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-11`** | **CHỐT** |
| Mục tiêu bảng `generation` là **auditability + lineage**, ⛔ **không phải reproducibility** — bit-exact ⛔ không đạt được (API ⛔ không cho set seed; **silent model drift**); `seed` là **provenance metadata**, ⛔ không phải replay key | `D-44` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.A | **CHỐT** |

### ⭐ Provider mặc định và đường lui — ⛔ dùng đúng, ⛔ không tự đổi

Nguồn: [findings/architect §5 hàng #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md), nguyên văn:

| Hạng mục | Giá trị | Nhãn |
|---|---|---|
| **Provider MẶC ĐỊNH** | **Gemini 3 Pro Image**, gọi qua **batch API** | `MẶC ĐỊNH` |
| **Đường lui đã ghi rõ** | **FLUX.2 pro** — `$0.03` | `[OFF]` |
| Giá tham chiếu Gemini 3 Pro Image | `$0.134` standard / `$0.067` batch (`CF-3.4`) | `[OFF]`, dẫn qua [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 3 |
| Trần chi phí MVP0 | **~$12** (giá standard) · **~$6** nếu batch — ⭐ **lấy số cao làm trần an toàn** (`CF-3.11`) | `[EM tính từ OFF]`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 |
| Phạm vi MVP0 | **Đúng MỘT adapter cố định** (`A4` = `🟡 1 adapter`) — số đo cho exit criterion `P-2` chỉ đo được qua một adapter cố định | [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 3 |

> [!CAUTION]
> ⛔ **MỌI con số chi phí trong ADR này mang nhãn G7 và phải mang theo khi trích:**
> [SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 và §5.2: **chi phí VLM call để score N candidate là phần CHƯA TÍNH** của `CF-3.5`.
> ⇒ **`$12,06`/chapter là SÀN, ⛔ KHÔNG phải trần** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1, `CẤM-04`). Bỏ nhãn này khi nhân một ước lượng là lỗi mà [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2 gọi là **"rửa sạch khoảng trống"**.

### Những gì ADR khác ĐÃ chốt — ⛔ không quyết lại

| Đã chốt ở đâu | Nội dung |
|---|---|
| [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) | **VLM QA-select là integration thứ hai, riêng biệt**, có adapter riêng; provider VLM = `TBD`. ⛔ ADR này **không hấp thụ** nó — xem [Q6](#q6-ranh-giới--adr-này-không-quyết-cái-gì) |
| [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q5` | **Lớp lỗi ở mức JOB** và quyết định retry/backoff. Adapter **phân loại** lỗi provider; job queue **quyết định làm gì** với lớp đó |
| [ADR-017](./ADR-017-Provenance-Chain-And-One-Transaction-Boundary.md) mục `Q4` | `KC-4` — ⛔ không đặc tả lại |
| [ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md) | `usage_event` append-only, `cost_usd`/`model_id`/`model_version`/`attempt_no` |

---

## Decision

### Q1. Seam: một interface, nhiều provider — ⛔ ⛔ không rò rỉ SDK

⛔ **⛔ Không một dòng code nghiệp vụ nào được gọi thẳng SDK của provider.** Mọi lời gọi nằm trong module adapter ([Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 4, AC-1).

**Phép đo của seam** (AC-2, đã ký): đổi provider (Gemini → FLUX.2) **chỉ cần thay implementation của adapter**, ⛔ không sửa code gọi compiler / queue / business logic — nghiệm thu bằng cách viết một adapter thứ hai (test/dummy) và xác nhận phần còn lại của hệ thống ⛔ không đổi.

⭐ **Lý do tồn tại của seam — nguyên văn từ Story**: *"để **giá đầu vào của provider không khoá cứng sản phẩm**"*. ⇒ Đây là seam **kinh tế** trước khi là seam kỹ thuật: nó là đường lui thật khi gate `G2` (gate kinh tế sau MVP1) không PASS.

**Hình dạng hợp đồng của adapter** (⚠️ chữ ký chi tiết thuộc `Spec-Integration-Image-Provider.md`):

| Thành phần | Nội dung | Neo |
|---|---|---|
| **Input** | ⭐ **HAI** output của compiler: `text_prompt` **VÀ** `conditioning_set` | `D-35` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-18`**) — identity reference ⛔ **không được** cạnh tranh với mô tả cảnh trong cùng một chuỗi text |
| **Input** | Reference image, trong đó **prop quan trọng là ENTITY RIÊNG** | `D-43` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-27`) — ⛔ không mô tả prop bằng chữ trong prompt |
| **Output** | Artifact ảnh + **`model_id`, `model_version`** cho **mỗi** lần gọi | `D-40` + `D-59`; [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) AC-3 |
| **Output** | **`cost_usd` thực đo** tại thời điểm hoàn tất, ⛔ không phải ước lượng trước khi gọi | `D-59` · [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4 |
| **Output (lỗi)** | **Lớp lỗi đã phân loại** — ⛔ không để lỗi rơi tự do làm crash caller | [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) (unhappy path) ⇒ ánh xạ sang [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q5` |

⚠️ **`generation.model_id` phải là model THỰC SỰ ĐƯỢC GỌI, ⛔ không phải model dự kiến.** Nếu provider tự fallback sang model khác giữa lúc request đang chạy, adapter ghi model thật ([Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md), unhappy path).

### Q2. Pin model version tường minh trong config

**Version của model là CẤU HÌNH TƯỜNG MINH, ⛔ không phải mặc định của SDK.** ⛔ Không được để chuỗi rỗng, ⛔ không `latest`, ⛔ không dựa vào alias của provider.

⭐ **Lý do — và nó ⛔ không phải reproducibility**: `D-44` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.A) đã chốt bit-exact **không đạt được**, và `seed` là provenance chứ ⛔ không phải replay key. Vậy pin version để làm gì?

> Để **phát hiện được silent model drift**. [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) (unhappy path) nói thẳng: provider đổi weights dưới **cùng một tên model** ⇒ Story ⛔ không tự phát hiện được, *"nhưng adapter phải ghi `model_version` để về sau **có thể truy vết** khi có nghi ngờ drift"*.

Hai điều kiện đi kèm, ⛔ không được bỏ:

1. ⚠️ **`model_version` khác nhau giữa hai lần gọi cùng `model_id` phải được ghi RIÊNG BIỆT, ⛔ không ghi đè** — [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4 đo bằng: 2 lần gọi cùng `model_id` nhưng provider trả `model_version` khác nhau ⇒ query phải trả **đúng 2 giá trị phân biệt** trên 2 dòng `generation`.
2. **Đối chứng bằng golden dataset** — `D-66` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-19`): golden dataset regression **15–20 panel**, chạy định kỳ, **lưu bền** để so sánh theo thời gian, **phòng silent model drift**. ⛔ **Không dùng VLM tự chấm thay người.**

⛔ **ADR này KHÔNG xây hệ thống alert drift** — [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) và [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) đều đặt nó ngoài phạm vi. Cái được đảm bảo là **dữ liệu đủ để phát hiện bằng query**, ⛔ không phải cảnh báo tự động.

### Q3. Batch API là chế độ gọi mặc định

**Mặc định: batch API.** ⛔ Không realtime. Lý do trong nguồn: comic generation vốn là **async job queue** ([ADR-015](./ADR-015-Job-Queue-In-Postgres.md)) ⇒ batch là **fit tự nhiên**, và [SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-24` gọi nó là *"khoản tiết kiệm lớn nhất mà ⛔ không đánh đổi gì"*.

⚠️ **Đường lui đã ghi rõ, và nó là đường lui về NGÂN SÁCH chứ ⛔ không phải về kiến trúc**: `CF-3.11` lấy **giá standard** làm trần an toàn cho MVP0, *"vì cần vòng lặp nhanh nên batch khó dùng"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-24`, §5.1).

⇒ **Quy tắc mang theo**: chế độ gọi (`batch` / `standard`) là **thuộc tính của adapter, cấu hình được**, ⛔ không hardcode. Đổi chế độ ⛔ **không** được kéo theo thay đổi data model — hệ quả duy nhất là `cost_usd` thực đo khác đi, và `D-59` đã lo phần đó.

### Q4. Đổi granularity ⛔ KHÔNG đổi data model

**Per-panel là mặc định** (spec là đơn vị). **Whole-page là đường lui ĐÃ THIẾT KẾ SẴN**, đổi được mà ⛔ **không đổi data model**.

⭐ **Vì sao đổi được mà không đổi data model** — nguyên tắc kiến trúc chi phối: **spec là dữ liệu chính, ảnh chỉ là output/cache** (`D-20` / `SRS-FR-07`). [SRS](../../020-Requirements/SRS-Comic-Studio.md) §2.1 nói thẳng: *"Nó là lý do đổi render granularity per-panel ↔ whole-page **không đổi data model** (`SRS-FR-33`)"*, và `SRS-FR-07` (§3.C): panel spec **tách khỏi granularity render** — một page compile được **nhiều panel spec thành một prompt**.

⇒ **Hệ quả hợp đồng cho adapter**: adapter nhận **một đơn vị render** (một hoặc nhiều panel spec đã compile), ⛔ **không** giả định đơn vị đó luôn là *"đúng một panel"*. Một adapter viết cứng theo giả định per-panel là **đóng đường lui của `G2`** — vi phạm `D-46`.

> [!CAUTION]
> ⛔⛔ **`D-46` TUYỆT ĐỐI KHÔNG được đọc thành "hạ N để cứu margin".**
> [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.F (khối `[!CAUTION]`) ghi nguyên văn: *"Đường lui khi `G2` FAIL là **đổi granularity**, ⛔ **không phải hạ N**: `CF-10.7` ghi rõ đường **KHÔNG được đi** là hạ N từ 3 xuống 1, và **`CẤM-03` buộc mọi thay đổi N phải chạy lại `G1`**."*
> ⇒ Hai đường lui khác nhau, ⛔ **không thay thế cho nhau**:
> - **Đổi granularity** (`D-46`) ⇒ ⛔ không đổi data model, ⛔ không chạy lại gate nào.
> - **Đổi N** (`D-37`) ⇒ ⭐ **bắt buộc chạy lại `G1`** (`CẤM-03`), vì N là biến chất lượng, ⛔ không phải biến chi phí.
> ⚠️ Và ⛔ **budget vẫn phải tính ở N=3** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-20`, `Charter §4 R7`).

### Q5. Thang đường lui Gemini ↔ FLUX.2 — điều kiện, không phải tuỳ hứng

| Bậc | Cấu hình | Khi nào dùng | Nhãn |
|:--:|---|---|---|
| **0** | **Gemini 3 Pro Image · batch API · per-panel · N=3** | **Mặc định khởi động** | `MẶC ĐỊNH` (`D-40` + `D-41` + `D-46` + `D-37`) |
| **1** | Gemini 3 Pro Image · **standard** thay batch | Khi cần vòng lặp nhanh (MVP0) — ⚠️ dùng làm **trần chi phí an toàn**, ⛔ không phải tối ưu | `CF-3.11`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 |
| **2** | **Đổi granularity → whole-page** | Khi `G2` (gate kinh tế) không PASS | `D-46` — ⭐ đường lui **chính thức** của `G2` |
| **3** | **Đổi provider → FLUX.2 pro (`$0.03` `[OFF]`)** | Khi kinh tế của provider mặc định ⛔ không đỡ được | `D-40` — đường lui **đã ghi rõ trong nguồn** |
| ⛔ **KHÔNG** | Hạ **N** từ 3 xuống 1 | ⛔ **CẤM** — `CF-10.7`, `CẤM-03` | Xem cảnh báo ở [Q4](#q4-đổi-granularity--không-đổi-data-model) |

⚠️ **Ba bậc trên là ĐỘC LẬP, ⛔ không phải một thang bắt buộc đi tuần tự.** Chúng được xếp cạnh nhau vì cùng phục vụ một câu hỏi (*"kinh tế không đỡ được thì rút ở đâu"*), ⛔ không vì nguồn nào quy định thứ tự. ⚠️ **Nhãn**: việc xếp chúng thành một bảng là **cách trình bày của ADR này**; ⛔ **không nguồn Phase 1 nào phát biểu một "thang" như vậy** — nội dung từng bậc thì có nguồn, thứ tự thì không.

⚠️ **MVP0 chỉ có đúng MỘT adapter cố định** ([Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 4): ⛔ **không** multi-provider fallback tự động trong cùng một lần chạy, ⛔ **không** tự chọn provider theo giá thấp nhất. Đổi provider là **quyết định vận hành có người bấm nút**, ⛔ không phải logic runtime.

### Q6. Ranh giới — ADR này KHÔNG quyết cái gì

| ⛔ Không quyết | Ai quyết |
|---|---|
| ⭐ **VLM QA-select** — provider, hợp đồng adapter, chế độ report-only | [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md). ⚠️ [findings §5 lưu ý #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md): tách #2 khỏi #1 là **bắt buộc, ⛔ không phải sở thích** — gộp chúng **làm che mất** chuyện chi phí VLM chưa được tính vào bất kỳ con số COGS nào |
| Retry / backoff và **quyết định** làm gì khi lỗi | [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) mục `Q4`, `Q5` |
| Ánh xạ **chi tiết** lỗi từng provider → lớp lỗi job | `Spec-Integration-Image-Provider.md` — ⛔ `TBD`, [SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.3 xếp vào tầng design |
| DDL của `generation` (`cost_usd`, `model_id`, `model_version`, `attempt_no`, `seed`, `degradations`) | Lô **DB Schema** + [ADR-018](./ADR-018-Usage-Event-And-Rollup-Model.md) |
| Compiler deterministic, best-of-N, `conditioning_set` | `ADR-014` — ⛔ ADR này chỉ **tiêu thụ** output của compiler |
| Object storage key / signed URL cho artifact ảnh | [ADR-004](./ADR-004-Object-Storage-Vendor-And-Signed-URL.md) |
| ⛔ **ANTI-FEATURE**: ⛔ không integration nào được gọi dịch vụ copyright / plagiarism / similarity detection | `D-53` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-15`) — ⛔ **CẤM TUYỆT ĐỐI**, áp cho toàn bộ mục External Integration |

---

## Alternatives considered

### (a) Gọi thẳng SDK provider từ code nghiệp vụ, ⛔ không adapter — ⛔ LOẠI (Phase 1 đã loại)

**Điểm mạnh phải ghi nhận**: ít một lớp trừu tượng, ít code, dùng được ngay tính năng riêng của provider mà ⛔ không phải nghĩ cách tổng quát hoá — đúng tinh thần YAGNI khi mới có **một** provider.

**⛔ Vì sao LOẠI**: `D-40` là seam **CHỐT** ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23`) và [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) đặt AC nhị phân đúng chỗ này. Lý do sâu hơn là **kinh tế, không phải thẩm mỹ**: giá provider là biến số lớn nhất của COGS, và `G2` cần một đường lui **thật**. Adapter mà nhồi vào sau khi code nghiệp vụ đã bám SDK là **viết lại**, ⛔ không phải refactor — đúng lớp chi phí mà đội **1 người** ⛔ không trả nổi.

### (b) Multi-provider fallback tự động trong cùng một lần chạy — ⛔ LOẠI

**Điểm mạnh**: chịu lỗi tốt hơn; provider chính lỗi thì tự chuyển, ⛔ không mất job.

**⛔ Vì sao LOẠI**: [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 4 (*"Story này KHÔNG làm"*) loại tường minh — MVP0 chỉ có **1 adapter cố định**. Lý do kỹ thuật thêm: fallback tự động làm bẩn chính dữ liệu mà `D-59` tồn tại để giữ sạch — trong một *"logical generation request"* sẽ có nhiều `model_id` khác nhau, và cả số đo `P-2` của MVP0 (**exit criterion**) lẫn phép so sánh golden dataset đều mất mẫu số chung. ⇒ Đo trước, tự động hoá sau.

### (c) Tự chọn provider theo **giá thấp nhất** ở runtime — ⛔ LOẠI

**Điểm mạnh**: nghe như tối ưu COGS trực tiếp.

**⛔ Vì sao LOẠI**: [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 4 gọi đúng tên nó: *"đó là **quyết định vận hành**, ⛔ không phải yêu cầu kỹ thuật của Story này"*. Và nó **sai về chất**: provider rẻ hơn ⛔ không phải là provider tương đương — đổi provider là đổi **chất lượng ảnh**, thứ mà gate `G1` (chất lượng) chứ không phải `G2` (kinh tế) mới có thẩm quyền phán. Một bộ chọn theo giá ở runtime là **đi vòng qua `G1`**.

### (d) ⛔ Không pin version, dùng alias `latest` của provider — ⛔ LOẠI

**Điểm mạnh**: tự động hưởng model mới tốt hơn, ⛔ không phải bảo trì config.

**⛔ Vì sao LOẠI**: `D-40` chốt *"pin model version **tường minh** trong config"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-FR-23`). `latest` biến **silent model drift** từ *"rủi ro phát hiện được"* thành *"rủi ro không quan sát được"* — và drift là đúng thứ `D-66` bắt phải phòng bằng golden dataset ([SRS](../../020-Requirements/SRS-Comic-Studio.md) `SRS-NFR-19`). ⚠️ Thêm nữa, `D-44` đã nêu drift là **một trong hai lý do** bit-exact không đạt được; bỏ pin version là **tự nguyện mất luôn khả năng truy vết**.

### (e) Tự host model ảnh (mua/thuê GPU) thay vì gọi API — ⛔ LOẠI (Phase 1 đã loại)

**Điểm mạnh**: chi phí biên tiến gần 0 khi đủ tải; toàn quyền pin weights ⇒ ⛔ không có drift; ⛔ không phụ thuộc chính sách nội dung của bên thứ ba.

**⛔ Vì sao LOẠI**: `D-07` ([SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-11`**) chốt **⛔ không mua GPU**; API cho main path, self-host **chỉ** cho LoRA train / upscale / inpainting.

### (f) Gộp VLM QA-select vào chính adapter này — ⛔ LOẠI

⛔ **Đã LOẠI ở [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) Alternatives `(a)`**; ADR này ⛔ **không lập luận lại**, chỉ ghi nhận lý do quyết định: gộp lại **che mất** chuyện chi phí VLM chưa được tính vào bất kỳ con số COGS nào ([findings §5 lưu ý #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md)) — và đó chính là khoản làm `$12,06` là **SÀN** chứ ⛔ không phải trần.

---

## Consequences

### ⛔ Hệ quả BẮT BUỘC ĐỌC — chi phí

⚠️ **Mọi con số chi phí trong ADR này là SÀN.** `$12,06`/chapter @N=3 ⛔ **chưa tính** chi phí VLM call để score N candidate ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.1 + `CẤM-04`; §4.3, §5.2). File nào trích số từ đây **phải mang theo nhãn này**; bỏ nhãn là *"rửa sạch khoảng trống"* ([SRS](../../020-Requirements/SRS-Comic-Studio.md) §1.2).

### Tích cực

- **Giá provider ⛔ không khoá cứng sản phẩm** — đây là mục tiêu nguyên văn của Story, và là điều kiện để `G2` có đường lui **thật**.
- **Ba đường lui độc lập** (chế độ gọi · granularity · provider) ⇒ ⛔ **không phải chạm N**, tức là ⛔ không phải chạy lại `G1`.
- **Dữ liệu đủ để truy vết drift** từ generation đầu tiên: `model_id` + `model_version` trên **mọi** lần gọi, đối chứng bằng golden dataset.
- **Đường lui granularity ⛔ không tốn migration** — vì spec là dữ liệu chính, ảnh chỉ là output/cache.

### Tiêu cực — chi phí thật

- **Một lớp trừu tượng nữa phải bảo trì**, và nó có xu hướng **rò rỉ**: mỗi provider có tính năng riêng, và mỗi lần chiều một tính năng riêng là một lần seam mỏng đi. ⇒ ⛔ Cần kỷ luật liên tục, không phải một lần thiết kế.
- **Interface chung có nguy cơ hạ xuống mẫu số chung nhỏ nhất** — mất tính năng riêng đáng giá của provider mặc định. ⚠️ Chấp nhận có ý thức: `D-40` ưu tiên **thay được** hơn **tối đa hoá một provider**.
- **Adapter phải hỗ trợ đơn vị render tổng quát** (một hoặc nhiều panel spec), kể cả khi MVP chỉ chạy per-panel ⇒ tốn công cho một đường lui **chưa chắc đi**. ⚠️ Nhưng đây chính là điều `D-46` mua: nếu ⛔ không làm sẵn thì đường lui của `G2` ⛔ không tồn tại.
- **⛔ Không có alert drift.** Drift chỉ phát hiện được **bị động**, qua golden dataset chạy định kỳ + query thủ công. ⇒ Có một cửa sổ thời gian mà chất lượng đã tụt nhưng chưa ai biết. Đây là lỗ **đã biết và chấp nhận**, ⛔ không phải sơ suất.

### Việc còn để `TBD` — ⛔ không được bịa

| `TBD` | Ai đóng | Khi nào |
|---|---|---|
| **Retry policy + error taxonomy PER PROVIDER**; ánh xạ lỗi provider → lớp lỗi job của [ADR-015](./ADR-015-Job-Queue-In-Postgres.md) `Q5` | Architect + Engineer | Trong `Spec-Integration-Image-Provider.md`, trước khi adapter đầu tiên chạy |
| Chữ ký chi tiết của interface adapter (tên method, hình dạng `conditioning_set`) | Architect | Trong `Spec-Integration-Image-Provider.md` |
| **Chi phí VLM per-call** và tổng khoản thiếu của `CF-3.5` — ⛔ **không có số trong repo** | PM + Architect | Sau đo MVP0 — [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) sở hữu hàng này |
| **N tối thiểu** (`CF-8.5`) — ⚠️ **budget vẫn phải tính ở N=3**; ⛔ đổi N ⇒ chạy lại `G1` (`CẤM-03`) | PM | Sau đo MVP0 |
| Ngưỡng/điều kiện định lượng để kích hoạt từng bậc đường lui ở [Q5](#q5-thang-đường-lui-gemini--flux2--điều-kiện-không-phải-tuỳ-hứng) | PM (tại gate `G2`) | Tại gate `G2` sau MVP1 |
| Thời hạn signed URL cho artifact ảnh (`SRS-FR-02`) | Architect | [ADR-004](./ADR-004-Object-Storage-Vendor-And-Signed-URL.md) / lô API |

---

## Đã quyết ở đâu

| Quyết định | Mã `D-xx` | Nguồn (file + mã requirement) |
|---|:--:|---|
| **Adapter per image provider** là seam bắt buộc (một interface, nhiều provider: Gemini 3 Pro Image, FLUX.2); **pin model version tường minh trong config** | `D-40` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-23`** · §4.3 · `MVP-Scope §3 A4` · [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 4 |
| Dùng **batch API**, ⛔ không realtime; đường lui: `CF-3.11` lấy giá **standard** làm trần an toàn MVP0 | `D-41` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-24`** · §4.3 · §5.1 |
| **Provider MẶC ĐỊNH = Gemini 3 Pro Image (batch)**; **đường lui = FLUX.2 pro `$0.03` `[OFF]`** | `D-40` | [findings/architect §5 hàng #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) · `CF-3.4` `[OFF]` qua [Story-Image-Provider-Adapter](../../022-User-Stories/Backlog/Story-Image-Provider-Adapter.md) mục 3 |
| Render granularity **per-panel** mặc định; **whole-page** là đường lui đã thiết kế sẵn, ⛔ **không đổi data model** | `D-46` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-33`** · §2.1 · `SRS-FR-07` (§3.C) · `MVP-Scope §3 A7` |
| ⛔⛔ `D-46` **KHÔNG** được đọc thành *"hạ N để cứu margin"*; đường lui `G2` là **đổi granularity**; `CF-10.7` cấm hạ N 3→1; **`CẤM-03`** buộc mọi thay đổi N **chạy lại `G1`** | `D-46` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **§3.F** (khối `[!CAUTION]`) |
| Compiler xuất **HAI** output `text_prompt` + `conditioning_set`; identity reference ⛔ không cạnh tranh với mô tả cảnh | `D-35` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-18`** · §4.3 |
| Prop quan trọng vào **reference image như một ENTITY RIÊNG**, ⛔ không mô tả bằng chữ | `D-43` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-27`** |
| Mục tiêu bảng `generation` là **auditability + lineage**, ⛔ không phải reproducibility; `seed` là provenance, ⛔ không phải replay key; **silent model drift** là một trong hai lý do | `D-44` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §3.A |
| `cost_usd` + `model_id` + `model_version` + `attempt_no` trên **MỌI** generation; **`cost_usd` thực đo**; `model_version` khác nhau ⛔ không ghi đè | `D-59` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-FR-31`** · [Story-Generation-Cost-And-Model-Metadata](../../022-User-Stories/Backlog/Story-Generation-Cost-And-Model-Metadata.md) mục 4 |
| **Golden dataset regression 15–20 panel**, chạy định kỳ, lưu bền — phòng **silent model drift**; ⛔ không dùng VLM tự chấm thay người | `D-66` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-19`** · §5.1 |
| ⛔ **Không mua GPU**; API cho main path; self-host chỉ cho LoRA train / upscale / inpainting | `D-07` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-11`** |
| Ghi lại **MỌI** lần provider từ chối vì **content policy** | `D-67` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-20`** |
| ⛔ **ANTI-FEATURE**: ⛔ không gọi dịch vụ copyright / plagiarism / similarity detection trước khi luật sư xác nhận | `D-53` | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **`SRS-NFR-15`** · [findings §5 lưu ý #3](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
| ⭐ **VLM là integration RIÊNG**, ⛔ không gộp — vì gộp **che mất** chi phí VLM chưa tính | — | [ADR-007](./ADR-007-VLM-Provider-For-QA-Select.md) · [findings §5 lưu ý #1](../../010-Planning/pm-runs/2026-08-28-phase-2-architecture-design-comic-studio/findings/architect.md) |
| ⛔ Chi phí VLM là phần **CHƯA TÍNH** của `CF-3.5`; **`$12,06`/chapter là SÀN, ⛔ không phải trần** (`CẤM-04`) | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §4.3 · §5.2 · §5.1 |
| **Error taxonomy + retry policy per provider thuộc TẦNG DESIGN**, đặc tả tại `030-Specs` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) **§1.3** |
| ⛔ Không tự gán số cho hàng `TBD` | — | [SRS](../../020-Requirements/SRS-Comic-Studio.md) §5.2 |

---

_Created by system-architect_
_Author: trisjr_
