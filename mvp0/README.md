# MVP0 — dữ liệu viết tay

> Thư mục này chứa **dữ liệu đầu vào viết tay** của MVP0, ⛔ không phải tài liệu dự án.
>
> **Vì sao nằm ngoài `docs/`**: [`RULE-001`](../knowledge-base/99-Templates/Documents-Template.md) quản lý **tài liệu**; đây là **nguyên liệu chạy**. Tách riêng còn làm rõ một ranh giới mà kỷ luật MVP0 bắt buộc phải rõ — xem ngay dưới.

## Kỷ luật MVP0 — cái gì vứt, cái gì giữ

> *"Code của MVP0 KHÔNG phải nền của sản phẩm — viết để trả lời câu hỏi rồi **bỏ**; giữ lại **kết luận và dữ liệu**."* — [MVP-Scope §3.1](../docs/010-Planning/MVP-Scope.md) · [Roadmap §3.1](../docs/010-Planning/Roadmap.md)

| Thành phần | Số phận |
|---|---|
| Script sinh ảnh, adapter, compiler | ⛔ **Vứt** sau khi có số |
| `story-bible.yaml` · `panel-script.yaml` | ✅ **Giữ** — là nguyên liệu tái dựng golden dataset |
| Golden dataset (ảnh + bảng chấm) | ✅ **Giữ vĩnh viễn** — `H6` là `✅` ở **mọi** mốc MVP0–MVP4, và là đầu vào eval kit `M1-6` |

⛔ **Không** tạo migration, config loader, hay abstraction provider trong thư mục này — đó là **dấu hiệu sớm** của rủi ro *"spike biến thành nền móng"* ([Roadmap §3.1](../docs/010-Planning/Roadmap.md)).

## Nội dung

| File | Nội dung | Neo |
|---|---|---|
| [`story-bible.yaml`](./story-bible.yaml) | **3 nhân vật** viết tay + canonical reference + trạng thái theo thời điểm | `Roadmap §3.1` việc 2 |
| [`panel-script-ch1.yaml`](./panel-script-ch1.yaml) | **22 panel / trang 1–6** — nghĩa địa → tỉnh dậy → bia đá → flashback → ký hiệu con mắt | `Roadmap §2` · [DB-Entity-Comic-IR](../docs/030-Specs/Schema/DB-Entity-Comic-IR.md) |
| [`panel-script-ch2.yaml`](./panel-script-ch2.yaml) | **20 panel / trang 7–12** — cánh cửa TÀ → giao kèo → hắc khí → Vọng Tử → khuôn mặt sau mây | như trên |
| [`typeset-corpus.json`](./typeset-corpus.json) | **5 mục** ở **cả NFC và NFD**, sinh bằng [`scripts/gen-typeset-corpus.py`](../scripts/gen-typeset-corpus.py) | `ADR-001` `## Consequences` **#5** |
| [`threshold-signoff.md`](./threshold-signoff.md) | Phiếu ký nhận ngưỡng `[EM]` — **ký TRƯỚC khi đo** | `MVP-Scope §7` · `Q-2` |
| ⭐ [`golden-dataset/`](./golden-dataset) | **Bảng chấm** (`scoring-sheet.csv`, append-only) + phiếu verdict `G1` + ảnh đã duyệt — **dữ liệu giữ vĩnh viễn**, ⛔ không nằm trong `run-*/` | `MVP-Scope §3` `H6` · `Roadmap P-6` |

**Nguồn**: *Tà Nguyệt Vô Tận* — Chương chữ 1 *(Người chết trở về)*, tách thành **hai chương comic**.

**Ràng buộc đã kiểm cơ học** (cả hai file): tổng **42 panel / 12 trang** · `character_count` max = **3** (trần `INV-2`) · emphasis quota **mỗi chương comic** = 1 full_page + 3 large (đúng `ADR-012 D-23`) · mọi toạ độ **0–1** (`INV-5`) · `panel_index` liên tục 1–42.

> [!WARNING]
> ⚠️ **Ngân sách phải tính lại theo giá Alibaba đã verify — ⛔ repo chưa có số chốt.** Công thức không đổi: phủ trọn chương chữ = **42 panel × N=3 = 126 ảnh** × giá/ảnh. Hai mốc để so:
>
> - Theo giá **Gemini cũ** (`$0.134`): ≈ **$16,88** — vượt trần `~$12` (`CF-3.11`) khoảng **41%**, dưới trần thực tế `~$50` (`Analysis §10`).
> - Theo **dải giá Alibaba từ nguồn thứ ba** (`$0.02–$0.075`/ảnh — ⚠️ **chưa verify từ trang chính thức**, xem [Research-Alibaba-Model-Studio-For-MVP0 §4](../docs/050-Research/Research-Alibaba-Model-Studio-For-MVP0.md)): ≈ **$2,52–$9,45** — lần đầu nằm **trong** trần `~$12`. Free quota 90 ngày còn kéo số thật xuống nữa.
>
> ⇒ **Founder điền giá đã đọc từ console vào `.env`** (`MVP0_IMAGE_PRICE_T2I_USD` / `MVP0_IMAGE_PRICE_EDIT_USD`) **trước khi chạy thật**, rồi thay khối này bằng số đã verify — `SRS §5.2` cấm bịa số. **Đường lui nếu số thật vẫn vượt trần**: chạy **chỉ chương comic #1** (22 panel); đổi lại thì mất phần đo `G1-e` giàu nhất — 7 trong 9 panel có thoại nằm ở chương comic #2.

> [!NOTE]
> ⭐ **Điểm dữ liệu đầu tiên cho `G-07`**: chương chữ này ra **42 panel**, so với giả định **60 ảnh/chapter** `[EM]` `CF-3.3` — **thấp hơn 30%**.
>
> ⛔ **Chưa kết luận được gì**: `n = 1`, và đây là số panel do **người phân cảnh**, ⛔ không phải số đo từ hệ thống. Nhưng nó là điểm dữ liệu thật đầu tiên chạm vào thứ mà `Charter §8 A1` gọi là *"thừa số gốc của toàn bộ mô hình chi phí"*. Ghi lại để đối chiếu khi có chương thứ hai.

## ⚠️ Giới hạn đo lường đã biết — đọc trước khi chấm `G1`

Chương này chấm theo phiếu [`C-1…C-8`](../docs/050-Research/Analysis-MVP0-Requirements.md):

| # | Kết quả | Ghi chú |
|:-:|:-:|---|
| `C-1` ≥2 nhân vật cùng cảnh | ⛔ **TRƯỢT** | Xem cảnh báo dưới |
| `C-2` ≥1 cảnh 3 nhân vật | 🟡 Mỏng | Đúng **một** panel (16) |
| `C-3` 8 panel liền cùng nhân vật | ✅ | `lam_uyen` có mặt ở **24/42** panel |
| `C-4` có thoại | ✅ | **9 panel** có thoại, gồm **2 ca typeset khó** — xem dưới |
| `C-5` dấu chồng hai tầng | ✅ | `ế`×25 · `ữ`×8 · `ợ`×8 · 30 loại / 283 lần |
| `C-6` trọn trong ≤30 panel | ✅ | **22 và 20 panel** — mỗi chương comic đều dưới trần |
| `C-7` content policy | ⚠️ Rủi ro | Panel **18** (kiếm xuyên ngực + máu) là chỗ rủi ro cao nhất |
| `C-8` bằng chứng đồng ý | — | Founder xác nhận đã có |

> [!WARNING]
> ⭐ **`G1-d` sẽ ra một con số, nhưng con số đó có mẫu quá nhỏ để mang nghĩa.**
>
> - Panel **2 nhân vật**: `n = 3` (panel 14, 15, 18)
> - Panel **3 nhân vật**: `n = 1` (panel 16)
>
> `G1-d` đòi *"panel 2 nhân vật **≥60%** đạt"*, với dải `50–60%` là PASS CÓ ĐIỀU KIỆN. Với `n=3`, các giá trị quan sát được **chỉ có thể là** `0% · 33% · 67% · 100%` — ⛔ **dải `50–60%` không tồn tại trên thang đo này**, và một panel hỏng làm verdict tụt **33 điểm phần trăm**.
>
> ⇒ Khi ghi verdict `G1-d`, **bắt buộc ghi kèm cỡ mẫu**. Báo cáo `67%` mà không nói `n=3` là biến một phép đo trên ba tấm ảnh thành một tuyên bố về năng lực model — đúng thứ [MVP-Scope §7](../docs/010-Planning/MVP-Scope.md) gọi là *"gate biến thành nghi lễ"*.
>
> **Đường xử lý**: bổ sung một chương có hội thoại nhiều người để nâng cỡ mẫu, hoặc chấp nhận và ghi `G1-d` là **đo-và-báo-cáo**, ⛔ không dùng làm điều kiện chặn.

## Provider dùng cho MVP0

> [!IMPORTANT]
> ⚠️ **Đây là LỰA CHỌN VẬN HÀNH để chạy MVP0, ⛔ KHÔNG phải chốt vendor.**
>
> [ADR-007](../docs/030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q4` đã định sẵn: *"**Ai đóng**: PM + Architect. **Khi nào**: tại gate cuối **MVP0**, khi ba phép đo bắt buộc của MVP0 có kết quả."* Lý do là biến quyết định — chi phí per-call, `N` tối thiểu, human-reject rate — **chính là output của MVP0**. ⇒ Chốt trước là *"chọn mù"* (chữ của ADR).

⭐ **Đổi provider vận hành `2026-08-31`** — Founder quyết định chạy MVP0 trên **Alibaba Cloud Model Studio** (region Singapore) thay cho Gemini, sau khi tự verify account + bảng giá console. Căn cứ, nguồn và giới hạn xác minh: [Research-Alibaba-Model-Studio-For-MVP0](../docs/050-Research/Research-Alibaba-Model-Studio-For-MVP0.md). ⚠️ Mọi con số chi phí trong tài liệu Phase 1–2 (`$0.134`, `$12,06`, `CF-3.5`) vẫn tính theo Gemini — chúng là **mốc lịch sử**, ⛔ không sửa hồi tố; mô hình chi phí cho `G2` dựng lại từ số **thực đo** của run này.

| Vai trò | Dùng cho MVP0 | Căn cứ |
|---|---|---|
| **Sinh ảnh — stage `refs`** (0 ảnh input) | `qwen-image-max` — text-to-image, sync | Alibaba tách t2i và edit thành hai dòng sản phẩm; stage `refs` không có ảnh input. Định tuyến theo hình dạng input là **tất định**, ⛔ không phải multi-provider fallback (`IP-C8` giữ nguyên) |
| **Sinh ảnh — stage `panels`** (1–3 reference) | `qwen-image-edit-plus` — nhận **1–3 ảnh input** + text, sync, PNG qua Base64 | Khớp chính xác trần ≤3 nhân vật (`INV-2`). Đi đường native DashScope — sinh ảnh ⛔ **không có** đường OpenAI-compatible |
| **VLM-select** | `qwen3-vl-plus` qua endpoint **OpenAI-compatible**, adapter **RIÊNG** | Đạt tiêu chí **loại** `ADR-007` `Q5` #1 (nhiều ảnh trong MỘT call) và #2 (`response_format: json_object`) |

**Vì sao đổi mà vẫn giữ nguyên kỷ luật cũ:**

1. Vẫn **một vendor, một bộ credential** (`DASHSCOPE_API_KEY`) — ⛔ không thêm điểm phụ thuộc ngoài nào so với trước. Hai adapter vẫn **TÁCH** đúng [ADR-007](../docs/030-Specs/Architecture/ADR-007-VLM-Provider-For-QA-Select.md) `Q1` — ở Alibaba hai vai trò còn buộc phải đi **hai đường API khác nhau**, nên ranh giới adapter càng rõ.
2. Lý do kinh tế: dải giá tham khảo rẻ hơn Gemini ~2–4× đưa full chương từ **vượt trần 41%** về **trong trần `~$12`** (số chốt chờ Founder verify — xem khối WARNING ở đầu file), cộng free quota 90 ngày (100 ảnh `qwen-image-max`/`qwen-image-edit-max`, ~1M token/model VL) đủ chạy stage `refs` + batch thăm dò gần như miễn phí.

⚠️ **Hai rủi ro mở — phải xử lý TRƯỚC khi ký ngưỡng:**

- **Content moderation**: Alibaba kiểm duyệt **cả input lẫn output**, ⛔ **không có safety settings chỉnh được** như Gemini, ngưỡng với fantasy violence không công bố. Panel **18** (kiếm xuyên ngực + máu) là ca thử của `C-7`. ⇒ Chạy **batch thăm dò trong free quota** trước khi cam kết; mã từ chối `DataInspectionFailed` / `IPInfringementSuspect` được adapter map thẳng vào `refusals.jsonl` (`D-67`).
- **`G1` sẽ đo năng lực model Alibaba**, ⛔ không phải Gemini — verdict và đầu vào `G2` nói về provider này. FAIL trên Alibaba ⛔ không suy ra FAIL trên Gemini (và ngược lại). Quay lại Gemini trước khi sinh ảnh thật = chưa mất gì.

**Việc chốt vendor thật** vẫn dùng **5 tiêu chí `Q5`** của `ADR-007`, theo thứ tự — tiêu chí #1 (*nhận nhiều ảnh trong MỘT call*) là tiêu chí **loại**, ⛔ không phải cộng điểm.

## Art style dùng cho MVP0

> [!IMPORTANT]
> ⭐ **Founder chốt `2026-09-01`: manga Nhật ĐEN TRẮNG + "đỏ tà dị"** — đen trắng thuần (nét mực đậm, screentone, cross-hatching), **duy nhất màu đỏ máu** được phép xuất hiện ở **yếu tố siêu nhiên**: chớp đỏ · sợi dây đỏ số mệnh · mắt phải đỏ của `lam_uyen`.
>
> **Chốt qua BA vòng A/B trong free quota** (mỗi vòng Founder nhìn ảnh thật rồi quyết): ① đen-trắng cũ thua vì mâu thuẫn dữ liệu màu → chọn hướng manhua màu; ② manhua màu B vs manga Nhật C (theo ảnh tham khảo Founder) → chọn C; ③ C tuyệt đối vs C + đỏ tà dị → chốt **C + đỏ tà dị** (bằng chứng: panel 1 chớp đỏ trên nền B/W).
>
> **Hệ quả đã cài vào code và data:**
> - Chuỗi style nằm ở **một nơi duy nhất**: `BASE_STYLE` trong [`compile_prompt.py`](../scripts/mvp0/compile_prompt.py); cờ `BASE_STYLE_IS_MONOCHROME` làm compiler **bỏ `palette:` màu** khỏi prompt (data palette giữ nguyên — tri thức cho preset màu sau này).
> - Mô-tả-màu **bám nhân vật** trong Story Bible / panel script đổi thành **tông + chất liệu + hình** (*nâu sẫm→tông sẫm đậm, chỉ vàng→hoa văn thêu nổi, nhẫn ngọc→nhẫn mặt đá lớn, rỉ xanh→rỉ sét*); màu gốc giữ trong comment YAML — bằng chứng thực nghiệm: chữ màu (kể cả "ngọc") trong prompt **thắng** cả style block lẫn chỉ dẫn ép xám.
> - Ba yếu tố "đỏ tà dị" **giữ nguyên chữ đỏ** trong data — đó là ý đồ nghệ thuật, không phải rò rỉ.
>
> ⚠️ Hệ quả đo lường: ảnh sinh **trước** mốc này (38 ảnh style cũ/thăm dò) là dữ liệu quan sát, ⛔ không trộn vào golden dataset. Canonical refs sinh lại toàn bộ với style chốt (xem [`refs/selection-log.md`](./refs/selection-log.md)). Việc bổ sung **catalog thể loại style** (nhiều preset có tên) là năng lực sau MVP0 — `G1` chạy đúng MỘT style này.

## Chạy MVP0

⚠️ **Cài trước**: `pip install dashscope openai pyyaml` · biến môi trường nạp từ `.env`: `cp .env.example .env`, điền `DASHSCOPE_API_KEY` + hai giá tham chiếu, rồi `set -a && source .env && set +a` (⛔ **không** hardcode — [`security.md`](../.claude/rules/security.md) §2).

### Hai stage — `refs` là bắt buộc trước `panels`

```bash
# Stage 1 — sinh character sheet cho 3 nhân vật
python3 scripts/mvp0/run_mvp0.py refs --dry-run   # kiểm prompt, ⛔ không tốn tiền
python3 scripts/mvp0/run_mvp0.py refs
# ⭐ Bước NGƯỜI làm: chọn 1 ảnh/nhân vật, lưu thành mvp0/refs/<char_id>.png

# Stage 2 — sinh panel với reference đã chọn
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1 --dry-run
python3 scripts/mvp0/run_mvp0.py panels --chapter ch1
```

> [!IMPORTANT]
> ⭐ **Vì sao stage `refs` phải tồn tại** — đây là bước ⛔ **không có trong tài liệu planning nào**:
>
> Story Bible mô tả nhân vật bằng **chữ**, nhưng pipeline `A1` cần **ảnh reference**. ⇒ Phải có một bước biến mô tả chữ thành ảnh, và **người phải chọn tay** ảnh nào là canonical. ⛔ Không có bước này thì *"generate panel **với reference**"* ⛔ không chạy được.
>
> Đây cũng là **quyết định sáng tạo đầu tiên của con người** trong toàn pipeline — thứ mà Điều 5a đòi hỏi. Ở MVP1 nó phải sinh `change_log` (`KC-2`); ở MVP0 thì ghi tay.

### Ba file script

| File | Vai trò | Ràng buộc cứng |
|---|---|---|
| [`compile_prompt.py`](../scripts/mvp0/compile_prompt.py) | Visual Prompt Compiler tối giản | ⛔ **Deterministic** — `D-34`/`SRS-FR-17` cấm LLM ở compiler runtime |
| [`providers.py`](../scripts/mvp0/providers.py) | **Hai** adapter tách riêng | `ADR-007` `Q1` — cùng vendor nhưng **hai** adapter |
| [`run_mvp0.py`](../scripts/mvp0/run_mvp0.py) | Orchestrator, ghi file phẳng | ⛔ Không UI, ⛔ không DB |

**Bất biến đã cài vào code**, mỗi cái có neo:

- **Precedence ladder** — identity reference + `state_ref` + `attribute_binding` ⛔ **không bao giờ** bị drop khi vượt constraint budget. ⭐ Cắt chúng là cắt đúng thứ `G1-a`/`G1-d` tồn tại để đo
- **Constraint budget = 8**, phần bị drop ghi ra `dropped_constraints.jsonl` — ⛔ không drop im lặng
- **N=3 cho MỌI panel**, ⛔ không phải retry-on-failure (`CF-3.1`, `Charter §7 C8`)
- **`unclear` là giá trị hạng nhất** — rubric VLM nói thẳng ⛔ đừng ép thành pass/fail (`D-38`)
- **Adapter chỉ xếp hạng**, ⛔ không tự chọn thay người (`D-38`) — lựa chọn cuối là của người, và đó **chính là phép đo `G1-c`**
- **`usage` ghi ngay sau khi sinh**, ⛔ không đợi VLM — tài nguyên đã tiêu thì phải ghi
- **VLM lỗi sau khi ảnh đã sinh** = trạng thái hợp lệ, ảnh vẫn giữ (`ADR-007` `Q6`)
- **Mọi lần provider từ chối** ghi vào `refusals.jsonl` (`D-67`) — đây là dữ liệu cho `C-7`

⚠️ **`IMAGE_T2I_MODEL_ID`, `IMAGE_EDIT_MODEL_ID` và `VLM_MODEL_ID` phải verify trước khi chạy thật.** Ba hằng số trong `providers.py` lấy **tên model** từ tài liệu chính thức Model Studio, ⛔ chưa đối chiếu với console của account thật. `IP-C3` cấm alias kiểu `latest` ⇒ pin **snapshot có ngày** (ví dụ `qwen-image-max-2025-12-30`) khi console cho phép. Chạy `--dry-run` trước.

### Output mỗi lần chạy

`mvp0/run-<stage>-<timestamp>/` — `prompts/` · `candidates/` · `results.jsonl` · `usage.jsonl` · `refusals.jsonl` · `dropped_constraints.jsonl`. Thư mục này **nằm trong `.gitignore`**; ⚠️ **ngoại lệ**: `mvp0/refs/*.png` là reference **đã chọn** — đó là **dữ liệu giữ lại**, ⛔ không phải output tạm.

## ⭐ Hai ca typeset khó — nơi `G1-e` thật sự bị thử

`G1-e` đòi **100%** panel có thoại dùng overlay và **0** panel nhờ model render chữ. Chín panel có thoại chứa **hai loại bubble mà một chương đối thoại thường ⛔ không có**:

| Loại | Panel | Vì sao khó |
|---|---|---|
| `voice_no_speaker` | 27, 42 | Tà Thần và thiên đạo ⛔ **không có thân thể** — bubble ⛔ không có đuôi trỏ về người nói. Chạm thẳng vào **human gate speaker attribution** (MVP2) ngay từ MVP0 |
| `system_panel` | 37, 39, 40 | Bảng trạng thái là **giao diện**, ⛔ không phải lời thoại. ⭐ Đây là chỗ dễ hỏng nhất: model rất hay **tự vẽ "bảng chữ" thành một phần của tranh** — mà đó chính là định nghĩa của việc **trượt `G1-e`** |

## Việc còn thiếu

- [ ] Chốt **vendor VLM** — `Q-3`. ⚠️ ⛔ **KHÔNG chặn MVP0**: `ADR-007` `Q4` đặt việc này ở **gate cuối MVP0**, vì đầu vào của nó là chính số đo MVP0
- [ ] Ký nhận [`threshold-signoff.md`](./threshold-signoff.md) — `Q-2`, phải xong **trước** khi sinh ảnh đầu tiên
- [ ] **Dữ liệu** golden dataset (`P-6`) — 15–20 panel có spec + ref + ảnh + đánh giá. ⭐ **Bảng chấm đã có** ([`golden-dataset/`](./golden-dataset)); còn thiếu là **ảnh và điểm**, tức phải chạy thật
- [ ] Nâng cỡ mẫu `G1-d`, hoặc chấp nhận ghi nó là **đo-và-báo-cáo** thay vì điều kiện chặn
- [ ] Điền **giá đã verify từ console** vào `.env` (`MVP0_IMAGE_PRICE_T2I_USD`, `MVP0_IMAGE_PRICE_EDIT_USD`) và thay khối ngân sách đầu file bằng số chốt — trước khi chạy thật
- [ ] **Batch thăm dò content policy** trong free quota (stage `refs` + vài panel rủi ro, gồm 18) — dữ liệu cho `C-7`, làm **trước** khi ký ngưỡng

**Đã xong**: ✅ Story Bible · ✅ panel script cả hai chương comic · ✅ corpus NFC/NFD · ✅ provider vận hành cho MVP0 · ✅ bảng chấm + phiếu verdict `G1` ([`golden-dataset/`](./golden-dataset)) · ✅ script tính regen ratio `p50`/`p90` ([`regen_ratio.py`](../scripts/mvp0/regen_ratio.py))
