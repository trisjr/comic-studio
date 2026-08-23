# Findings — Lens AI/ML Pipeline

- **Role**: Senior AI Engineer
- **Đối tượng**: `docs/999-Resources/Request.md` (894 dòng, 18 mục) — đã đọc toàn văn
- **Phạm vi lens**: mọi chỗ trong pipeline có một model đưa ra phán đoán. **Ngoài phạm vi**: đánh giá thị trường, đối thủ, và năng lực cụ thể của từng image generation model theo tên (lens khác lo).
- **Ngày**: 2026-08-23
- **Ràng buộc nhận thức**: em **không có WebSearch**. Mọi con số trong tài liệu này là **ước lượng engineering** kèm giả định, **không** phải benchmark đã verify. Chỗ nào kết luận phụ thuộc năng lực image model, em nêu thành **giả định có mã IM-Ax** ở §9 để PM đối chiếu chéo.

---

## Mục lục

1. [Nguyên tắc "đừng generate ảnh ngay" (§1) — đúng hay sai?](#1-nguyên-tắc-đừng-để-ai-đọc-chapter-rồi-generate-ảnh-ngay-1--đúng-hay-sai)
2. [Layer 1 — Semantic AI: novel → Story Bible](#2-layer-1--semantic-ai-novel--story-bible-11-layer-1-18-mvp1)
3. [Layer 2 — Comic Director: Comic Intermediate Representation](#3-layer-2--comic-director-comic-intermediate-representation-4-5-6)
4. [Continuity Checker (§15) — thẩm định nghiêm khắc](#4-continuity-checker-15--thẩm-định-nghiêm-khắc)
5. [Visual Prompt Compiler (§16) — dưới góc prompt engineering](#5-visual-prompt-compiler-16--dưới-góc-prompt-engineering)
6. [Evaluation & testing — mục tài liệu hoàn toàn thiếu](#6-evaluation--testing--mục-tài-liệu-hoàn-toàn-thiếu)
7. [Chi phí và độ trễ của cả pipeline (phần LLM)](#7-chi-phí-và-độ-trễ-của-cả-pipeline-phần-llm-không-phải-image)
8. [Human-in-the-loop — thiết kế đúng nằm ở đâu?](#8-human-in-the-loop--thiết-kế-đúng-nằm-ở-đâu)
9. [Kết luận AI/ML](#9-kết-luận-aiml)

---

## Kết luận của worker

### 1. Nguyên tắc "đừng để AI đọc chapter rồi generate ảnh ngay" (§1) — đúng hay sai?

**Nguyên tắc: ĐÚNG. Cách hiện thực hoá được ngụ ý trong tài liệu: SAI ở một điểm cốt tử.**

Cần tách hai thứ mà tài liệu đang trộn làm một:

| | Cái gì | Đánh giá |
|---|---|---|
| **A** | IR như một **data model bền vững, người sửa được**, là source of truth | Đúng, rất đúng. Đây là quyết định kiến trúc tốt nhất của cả tài liệu. |
| **B** | IR như một **chuỗi 5-6 bước LLM nối tiếp**, mỗi bước là một transform tự động | Đây là chỗ rủi ro, và tài liệu không phân biệt nó với (A). |

**IR mua được gì (thật, không phải lý thuyết)**

- **Editability** — đây mới là lợi ích số một, không phải debuggability. Một panel spec sai thì con người sửa được **một field**; một ảnh sai thì chỉ có nút re-roll. Không có IR thì sản phẩm không có cơ chế sửa nào ngoài "tạo lại và cầu may".
- **Cache + tái sử dụng**: đổi style hoặc đổi image model không phải phân tích lại truyện. Đúng như §18 nói.
- **Model swap ở Layer 3**: có giá trị thật.
- **Reproducibility + lineage**: bảng `Generation` (§13) chỉ có nghĩa khi input của nó là một spec có ID ổn định. Không có IR thì không có reproducibility.
- **Attribution khi debug**: biết lỗi ở tầng nào.

**IR mất gì (tài liệu không nhắc một chữ)**

- **Error cascade nhân tính, không cộng**. Minh hoạ (số **giả định để minh hoạ**, không phải đo được): 5 tầng, mỗi tầng đúng 90% → end-to-end ≈ 0.9⁵ ≈ **59%**. Mỗi tầng 95% → ≈ **77%**. Muốn end-to-end 90% thì mỗi tầng phải ≈ 98%. Không tầng LLM nào trong pipeline này đạt 98% ở trạng thái zero-shot.
- **Information loss đơn hướng**: prose → scene → panel → prompt. Mỗi lần chuyển là một lần **nén có mất**, và subtext là thứ chết đầu tiên (xem §3). Tầng dưới **không thể** phục hồi thông tin tầng trên đã bỏ, vì nó không còn thấy văn bản gốc. Đây là lý do panel spec **bắt buộc** phải giữ `source_span` trỏ về đoạn văn gốc — tài liệu không có field này.
- **Error laundering** — nguy hiểm nhất và không hiển nhiên: một lỗi ở tầng trên, sau khi đi qua tầng dưới, **trông như một quyết định hợp lệ**. Nếu extraction gán sai "Lâm Phong mặc áo xanh", panel spec sẽ ghi "blue robe" một cách tự tin, prompt compiler sẽ nhét "blue robe" vào prompt, và Continuity Checker sẽ báo **PASS**. Toàn hệ thống đồng thuận với một sai lầm. Ảnh sai mà không một tầng nào báo động. Chuỗi nhiều tầng **làm lỗi khó thấy hơn**, không dễ hơn — trái với trực giác "dễ debug" của tài liệu.
- **Chi phí + latency nhân theo số tầng** — thực ra không đáng lo, xem §7. Đây là mối lo nhỏ nhất.

**Vấn đề đặc thù của chuỗi 5-6 tầng LLM nối tiếp**

1. **Không có tầng nào tự biết mình sai.** LLM không hiệu chỉnh: output sai vẫn được phát ngôn với cùng độ tự tin như output đúng. Chuỗi nối tiếp = chuỗi không có phanh.
2. **Không có đường phản hồi ngược.** Tầng 4 phát hiện panel vô nghĩa thì không có cơ chế nào bảo tầng 2 rằng scene graph sai. Tài liệu vẽ pipeline một chiều (§17) — mũi tên duy nhất đi ngược là `FAIL → Regenerate` ở cuối, và nó regenerate **ảnh**, tức là chữa ở tầng sai nhất.
3. **Non-determinism cộng dồn**: chạy lại cùng một chapter ra một cây scene khác → mọi ID panel đổi → không diff được, không regression test được (xem §6).
4. **Khoảng cách semantic giữa các tầng bị bỏ trống**: giữa "panel spec" và "prompt" có một bước dịch mà không ai định nghĩa (§5 của em).

**Kết luận mục 1**: giữ nguyên tắc IR, nhưng bổ sung ba điều kiện, thiếu bất kỳ điều nào thì IR chỉ đang **giặt sạch lỗi** thay vì chặn lỗi:
1. Mỗi tầng phải **người sửa được và edit của người phải sống sót qua lần re-run sau** (cần provenance field từ ngày đầu — xem §8).
2. Mỗi artifact phải giữ **con trỏ về văn bản gốc** (`source_span`) để tầng dưới và con người truy nguyên được.
3. **Tối thiểu hoá số tầng LLM**, không phải số tầng IR. IR nhiều tầng nhưng nửa số transform là **deterministic code** thì mới là thiết kế đúng. Cụ thể: chapter parse, Story Bible reduce, layout mapping, prompt compile — cả bốn nên là code, không phải LLM. Tài liệu mặc định cả bốn là "AI".

---

### 2. Layer 1 — Semantic AI: novel → Story Bible (§11 Layer 1, §18 MVP1)

**Khả thi bằng LLM hiện nay không, ở mức reliability nào**

Đây là tầng **khả thi nhất** trong toàn pipeline, vì nó là information extraction có ground truth — tức là đo được, sửa được, và lỗi của nó không mang tính thẩm mỹ. Ước lượng reliability (**ước lượng engineering, không phải benchmark**, giả định: LLM tier khá + prompt có schema + few-shot, truyện web-novel dịch từ tiếng Trung, đánh giá trên main cast ~10 nhân vật):

| Task | Reliability ước lượng | Ghi chú |
|---|---|---|
| Chapter boundary parse | ~99% | **Nên là code, không phải LLM.** Regex/heuristic trên `Chương N` / `Chapter N`. |
| Character mention detection trong 1 chapter | 90-96% | Cao. |
| Location extraction trong 1 chapter | 85-93% | Địa danh mơ hồ ("căn phòng", "bên ngoài") là nguồn lỗi. |
| Event/state-change extraction trong 1 chapter | 75-88% | Bắt được sự kiện lớn, hay bỏ chi tiết ngoại hình lướt qua. |
| **Cross-chapter entity resolution** | **60-80% nếu làm zero-shot per-chapter** | Điểm yếu thật. Xem dưới. |
| **State query đúng tại chapter N (N lớn)** | **50-75% nếu không có reducer deterministic** | Điểm yếu thật. Xem dưới. |

Đọc bảng này theo chiều dọc thì thấy điều tài liệu không thấy: **MVP1 không phải milestone dễ.** §18 trình bày MVP1 như phần "chưa cần generate ảnh nên nhẹ", nhưng nó chứa đúng hai bài toán khó nhất của phần non-visual: entity resolution xuyên chapter và state inference bền vững. Cái dễ (parse, extract trong một chapter) thì lại là cái tài liệu liệt kê ra; cái khó thì không được đặt tên.

**Cross-chapter entity resolution — đề xuất cụ thể**

Nguyên tắc chủ đạo, em sẽ dùng lại nó nhiều lần trong tài liệu này: **LLM đề xuất, code quyết định** (LLM proposes, deterministic code decides). Registry alias là dữ liệu, không phải phán đoán — nó không được sống trong context window của model.

Thiết kế 4 lớp, chạy theo thứ tự, lớp trên chặn được thì không gọi lớp dưới:

1. **Lớp deterministic (miễn phí, chính xác cao, xử lý phần lớn khối lượng)**
   - Normalize: fold diacritics, lowercase, chuẩn hoá khoảng trắng → `lâm phong` = `Lam Phong` = `LÂM PHONG`.
   - **Strip honorific/appellation**: bảng affix cứng cho thể loại tiên hiệp/cổ trang — `công tử, tiểu thư, thiếu gia, lão, tiền bối, đạo hữu, sư phụ, sư huynh, phu nhân, đại nhân, thí chủ, chân nhân, tổ`. `Lâm công tử` → head token `Lâm` → khớp họ của `Lâm Phong`.
   - **Bảng Hán-Việt ↔ pinyin ↔ tên gốc**: truyện MTL thường chuyển tự không nhất quán trong cùng một bộ (`Lâm Phong` / `Lin Feng` / `Lam Phong`). Đây là lỗi **có quy luật**, xử lý bằng mapping table + fuzzy match (edit distance trên chuỗi đã normalize) chứ tuyệt đối không nên đốt LLM call.
   - Kết quả: theo ước lượng của em, lớp này một mình giải quyết ~60-75% ca alias trong web-novel dịch, với precision rất cao.

2. **Lớp LLM đề xuất merge (chỉ cho ca còn lại)**
   - Với mỗi mention chưa khớp, gọi LLM với: mention + câu chứa nó + **danh sách candidate rút từ registry** (không phải cả Story Bible).
   - Output bắt buộc có cấu trúc: `{candidate_id, confidence, evidence_span}`. Có `evidence_span` thì con người review được trong 3 giây; không có thì không review được.
   - **Constrained decoding**: model chỉ được chọn trong tập candidate hoặc trả `NEW_ENTITY` / `UNKNOWN`. Cho phép **abstain** là biện pháp giảm lỗi rẻ nhất ở đây.

3. **Lớp registry deterministic (code sở hữu sự thật)**
   - `confidence ≥ ngưỡng cao` → auto-merge, ghi log.
   - `ngưỡng thấp ≤ confidence < cao` → vào **human review queue** trong UI (§14 đã có chỗ cho nó).
   - `< thấp` → tạo entity mới **tạm** (provisional), không được nhập vào canonical bible cho tới khi tích luỹ đủ mention. Chống rác từ nhân vật xuất hiện một lần.

4. **Đại từ thì KHÔNG bao giờ được lên bible**
   - `hắn / nàng / y / gã / thị / lão / ả` là coreference **cục bộ trong scene**, giải trong cửa sổ 1 chapter và kết quả **chỉ sống ở scope chapter**. Nếu promote "hắn" thành fact của bible thì một lần giải sai sẽ nhiễm độc bible vĩnh viễn.
   - Đây là một quy tắc kiến trúc, không phải tối ưu: **fact vào bible phải neo vào một mention có danh từ riêng.**

**Tỉ lệ lỗi kỳ vọng** (tất cả là **ước lượng**, giả định như bảng trên):

| Cách làm | Lỗi trên main cast (~10 nv) | Lỗi trên nhân vật phụ / xuất hiện 1 lần |
|---|---|---|
| LLM zero-shot per-chapter, không registry | 20-40% | 40-70% |
| Deterministic + LLM propose + registry (không human) | 5-12% | 20-40% |
| Trên + human review queue cho vùng confidence thấp | **2-5%** | 15-30% |

Chấp nhận được rằng nhân vật phụ sai nhiều — họ ít khi cần visual consistency. Nhưng **main cast phải xuống dưới 5%**, vì một alias sai trên nhân vật chính sẽ tạo ra một "nhân vật ma" có state riêng, và mọi panel gọi tên đó sẽ vẽ sai suốt hàng chục chapter.

**Vấn đề context window — đề xuất chiến lược**

Không có phương án nào trong ba phương án tài liệu ngụ ý là đúng nếu dùng đơn lẻ. Đề xuất: **incremental state-in/state-out + retrieval có trần cứng**.

- Mỗi chapter là một transform `f(chapter_text, bible_slice) → (events, mentions)`.
- `bible_slice` **không phải cả Story Bible**. Nó là: (a) canonical list của các entity **được nhắc trong chapter này** (lấy sau một lần scan mention nhanh, hoặc từ chapter trước), (b) state hiện tại của các entity đó, (c) 5-10 alias gần nhất. **Cap cứng, ví dụ 3k token.** Cap này là **yêu cầu kiến trúc, không phải tối ưu** — nó là thứ giữ chi phí linear thay vì superlinear (xem §7).
- Map-reduce thuần (extract độc lập rồi merge cuối) **không dùng được** cho state, vì state có thứ tự thời gian: "mất kiếm ở ch10" và "có kiếm ở ch05" chỉ có nghĩa khi biết cái nào trước. Nhưng map-reduce **dùng được** cho mention detection (không phụ thuộc thứ tự) → có thể chạy song song để tăng tốc.
- Rolling summary văn xuôi (kiểu "tóm tắt những gì đã xảy ra") là **anti-pattern** ở đây: nó nén có mất, không truy vấn được, và trôi dạt theo thời gian. Story Bible phải là **structured state**, không phải summary.

**Ước lượng chi phí token cho extraction (chi tiết đầy đủ cả pipeline ở §7)**

Giả định: chapter 3000 từ; tiếng Việt/truyện dịch tốn khoảng **1.5-2× token so với English cùng số từ** (ước lượng do dấu thanh + tách subword kém hiệu quả với tiếng Việt trong các BPE phổ biến) → ~7k token/chapter văn bản thuần.

| Quy mô | Chỉ riêng tầng extraction + bible | Ghi chú |
|---|---|---|
| 100 chapter | ~1.1M input + ~0.25M output, ~130-230 call | Linear, vì `bible_slice` bị cap |
| 500 chapter | ~5.5M input + ~1.25M output, ~650-1150 call | **Vẫn linear** nhờ cap |
| 500 chapter **nếu nhồi cả bible mỗi call** | Ước lượng bible ở ch500 đạt 150k-400k token → input mỗi call phình 20-50× → **hàng trăm triệu token**, và sẽ vỡ context limit trước khi vỡ ví | Đây là kịch bản mà thiết kế hiện tại của tài liệu **không loại trừ** |

Điểm cần báo cho anh: khác biệt giữa hai dòng cuối là **hai bậc độ lớn**, và nó phụ thuộc đúng một quyết định kiến trúc (retrieval có cap vs nhồi cả bible). Tài liệu không nói gì về nó.

**Vấn đề state inference — đây là bài toán gì**

Đây **không phải** bài toán ghi nhớ dài hạn của LLM. Đóng khung nó như "model phải nhớ vĩnh viễn" là sai hướng và sẽ dẫn tới thiết kế sai. Đây là bài toán **event sourcing**:

- **LLM làm**: đọc chapter 11, phát ra event có cấu trúc — `{type: StateChange, entity: lam_phong, attribute: injury, value: "scar_left_eye", permanence: PERMANENT, chapter: 11, evidence_span: "...", confidence: 0.9}`. LLM chỉ chịu trách nhiệm cho **một chapter**, trong một context window, và không cần nhớ gì cả.
- **Deterministic reducer (code) làm**: fold chuỗi event theo thứ tự chapter → state tại bất kỳ chapter N. `state_at(N) = reduce(events where chapter <= N)`. Query "Lâm Phong ở chapter 12 mặc gì" là một **truy vấn database**, không phải một lần suy luận của model. Sổ vết sẹo tồn tại tới chapter 400 vì **code không quên**, không phải vì model nhớ.

Ranh giới này quan trọng đến mức nếu đảo lại thì cả MVP1 sụp. Và nó cho một hệ quả đẹp: reducer là hàm thuần, unit-test được, chi phí bằng 0, tái chạy được, và edit của con người là một event ưu tiên cao trong cùng chuỗi.

**Lỗ hổng cụ thể của tài liệu ở đây**: §2 và §3 mô tả state theo chapter nhưng **không có khái niệm phân loại độ bền của attribute**. Không có nó thì reducer không thể biết `scar` sống 400 chapter còn `angry` chỉ sống 1 scene. Đề xuất bổ sung một trường bắt buộc `permanence` với 4 lớp:

| Lớp | Ví dụ | Semantic của reducer |
|---|---|---|
| `PERMANENT` | vết sẹo, mất một tay, tuổi, chiều cao | Ghi một lần, không bao giờ hết hạn |
| `SEMI_PERSISTENT` | kiểu tóc, vũ khí đang sở hữu, cảnh giới tu luyện | Sống tới khi có event ghi đè |
| `SCENE_SCOPED` | trang phục đang mặc, vết máu, đang ướt | Hết hiệu lực khi hết scene/chapter, cần default fallback |
| `TRANSIENT` | cảm xúc, tư thế | Chỉ sống trong panel, **không nên vào bible** |

Không có bảng này, tài liệu sẽ tự nhiên tạo ra bug kinh điển: nhân vật khóc ở chapter 12 rồi khóc suốt 300 chapter còn lại, hoặc mất vết sẹo sau một lần đổi áo.

**Truyện tiếng Việt và truyện dịch từ tiếng Trung — khó thêm gì**

Có, và không phải khó lặt vặt:

1. **Bùng nổ appellation** — nghiêm trọng nhất. Cùng một người được gọi khác nhau tuỳ **ai đang nói**: sư phụ / Lâm công tử / tiểu tử / nghiệt súc / Lâm đại nhân. Đây không phải noise, nó là **thông tin quan hệ** (§2 có `Relationships` — nên khai thác: appellation là tín hiệu để suy ra quan hệ, không chỉ là rác cần lọc).
2. **Đại từ dày và mơ hồ**: `hắn/y/gã` đều là "he" nhưng khác sắc thái; đoạn hội thoại tay đôi dài toàn đại từ. Xử lý theo mục "đại từ không lên bible" ở trên.
3. **Chuyển tự không nhất quán trong bản MTL** — lỗi có quy luật, dùng fuzzy + mapping table.
4. **Nhiễu của văn bản scrape**: quảng cáo, lời tác giả cuối chương, "xin ủng hộ phiếu đề cử", watermark của trang nguồn. Tài liệu **không có bước làm sạch text** trong MVP1 — nhưng đây là bước **đầu tiên** phải làm và là job của code, không của LLM.
5. **Attribute riêng của thể loại tu tiên: cảnh giới/tu vi.** Nó là state, nó thay đổi, và nó **có hệ quả thị giác** (hào quang, trang phục, khí chất). Story Bible của tài liệu không có chỗ cho nó. Cần một attribute mở rộng theo genre.
6. **Độ dài chapter biến thiên lớn** (800 → 6000 từ), và một scene thường bị cắt qua hai chapter → cây `Chapter → Scene` của §4 giả định scene nằm gọn trong chapter, giả định này sẽ vỡ.
7. **Tokenizer tốn hơn** — đã tính vào ước lượng ở trên (1.5-2×, ước lượng).

---

### 3. Layer 2 — Comic Director: Comic Intermediate Representation (§4, §5, §6)

#### 3.1. §4 — chapter văn xuôi → cây Scene → Panel

**Khả thi: có. Chất lượng kỳ vọng: "dùng tạm được, cần người sửa" — không phải "tốt".**

Điểm mấu chốt mà tài liệu bỏ qua: §4 và §2 là **hai loại việc khác nhau về bản chất**. Extraction có đáp án đúng; directing thì không. Không có ground truth nghĩa là: không đo tự động được, không regression test bằng exact match được, và không cải thiện bằng cách "sửa prompt cho đúng hơn" được. Nó chỉ cải thiện bằng rubric + người đánh giá (§6 của em).

LLM sẽ ra được panel breakdown hợp lệ về cú pháp gần như 100% (nếu có schema constraint). Nhưng chất lượng directing, ước lượng của em: khoảng **50-65% panel là hợp lý, 25-35% tầm thường nhưng vô hại, 10-15% sai rõ** (chia panel ở chỗ vô nghĩa, vẽ cái đáng nói bằng lời, bỏ mất cái đáng vẽ).

**Xu hướng lỗi cụ thể — nói thẳng từng loại:**

1. **Pacing đều đều (tệ nhất).** LLM có thiên hướng chia đều: mỗi scene ~3 panel, panel nào cũng cỡ trung bình. Comic sống bằng **tương phản nhịp** — 6 panel nhỏ dồn dập rồi một full page. Sản phẩm sẽ ra thứ "đúng mà chết", đọc phẳng như slideshow. Đây là lỗi khó nhận ra khi xem một trang, chỉ lộ ra khi đọc 20 trang liền.
2. **Panel count máy móc**: bị neo vào con số trong prompt/example. Đưa ví dụ 3 panel thì sẽ ra 3 panel mãi.
3. **Bỏ mất subtext.** Cái hay của truyện chữ thường ở chỗ **không nói ra**. LLM directing có xu hướng **minh hoạ theo nghĩa mặt chữ**: câu "hắn im lặng rất lâu" → panel "character standing silently". Mất hết. Một comic artist sẽ vẽ bàn tay siết chặt, hoặc một panel trống chỉ có bối cảnh — LLM gần như không tự làm điều đó.
4. **Không phân biệt "cái gì đáng vẽ" và "cái gì chỉ nên nói".** Nội tâm, hồi tưởng giải thích thế giới quan, mô tả cảnh giới tu luyện — những thứ này thuộc narration box hoặc bỏ hẳn, không phải panel. Đây là **phán đoán biên tập**, và ước lượng của em là LLM sai ở đây thường xuyên nhất. Hệ quả kinh tế trực tiếp: mỗi panel không cần thiết là một lần gọi image model tốn tiền.
5. **Nghịch lý dàn nhân vật**: LLM có xu hướng nhồi tất cả nhân vật có mặt vào cùng một panel — mà panel nhiều nhân vật lại là panel khó giữ consistency nhất (giả định IM-A4). Directing nên **thiên vị panel một nhân vật** vì lý do kỹ thuật, và LLM không biết điều đó nếu không được nói.
6. **Bỏ qua ngữ pháp comic**: eyeline match, quy tắc 180 độ, hướng đọc trái→phải (hay phải→trái với manga), shot-reverse-shot. Cần panel spec có con trỏ tới panel trước (thiếu — xem 3.3).
7. **Scene vắt qua ranh giới chapter** — đã nêu ở §2.

**Khuyến nghị**: coi Layer 2 là **"AI đề xuất bản nháp, người biên tập"**, không phải "AI quyết định". Và nếu buộc phải chọn, hãy để LLM giỏi ở phần **decomposition** (chuỗi beat nào xảy ra) và để **con người/template** quyết định phần **emphasis** (beat nào to, beat nào nhỏ) — vì decomposition có tín hiệu trong văn bản, còn emphasis là thẩm mỹ.

#### 3.2. §5 Layout Score — phản biện mạnh

Tài liệu đề xuất:

```
Narrative importance 0.95 / Emotional intensity 0.88 / Action intensity 0.76
Dialogue density 0.20 / Visual spectacle 0.91  =>  FULL PAGE
```

**Kết luận thẳng: cơ chế này, đúng như đang viết, là trang trí (decorative), không phải khoa học.** Nó tạo cảm giác định lượng mà không có phép đo nào phía sau. Bốn lý do, theo thứ tự sức nặng:

1. **Không calibrated — và không thể calibrate.** `0.95` là gì? Thang này neo vào đâu? Không có định nghĩa toán tử, không có anchor example, không có đơn vị. LLM đang sinh ra một **token trông giống số**, không phải kết quả của một phép đo. Khác biệt `0.95` vs `0.91` **không mang thông tin** — nó không phản ánh một khác biệt nào có thể quan sát được. Đây là pseudo-precision: hai chữ số thập phân ngụ ý độ phân giải mà quá trình sinh ra nó không có.
2. **Không ổn định giữa hai lần gọi.** Gọi lại cùng chapter sẽ ra `0.88` hoặc `0.79` thay vì `0.95`. Với temperature > 0 thì chắc chắn; kể cả temperature = 0 thì serving stack vẫn không đảm bảo bit-exact. Hệ quả nghiêm trọng: nếu quyết định layout nằm ở ngưỡng (`> 0.90 → FULL PAGE`), thì **cùng một chapter chạy hai lần ra hai layout khác nhau**. Đây là phi-determinism ở đúng chỗ người dùng nhìn thấy.
3. **Không so sánh được giữa chapter.** Điểm này quyết định. LLM chấm điểm **tương đối với context nó đang thấy**. Panel "quan trọng nhất" của một chapter filler cũng được ~0.9, y như climax của cả bộ truyện. Không có thang toàn cục → **ngưỡng cố định là vô nghĩa**. Kết quả thực tế: cứ vài trang lại có một full page, "full page" mất hết sức nặng, và chính cái nó định làm (nhấn mạnh) bị phá.
4. **Hàm tổng hợp không tồn tại.** 5 số → 1 quyết định `FULL PAGE`, nhưng tài liệu **không định nghĩa cách gộp**. Nếu để LLM gộp luôn, thì các con số là **lời biện minh hậu nghiệm** cho một quyết định đã được đưa ra bởi cùng một quá trình tiềm ẩn — chúng không tham gia vào quyết định. Đây là định nghĩa của trang trí.

**Một điểm nữa, cụ thể và không thể bào chữa**: `dialogue density 0.20`. Đại lượng này **tính được chính xác bằng code** — đếm ký tự thoại / tổng ký tự trong đoạn. Tài liệu đang trả tiền cho LLM để **đoán** một con số mà một dòng Python cho ra chính xác. Chi tiết này cho thấy vấn đề không phải "LLM tệ", mà là **ranh giới LLM/code chưa được vẽ**.

**Phương án thay thế — ba tầng, có thể làm cả ba, xếp theo mức em đề xuất:**

**(A) Rubric phân loại rời rạc + bảng mapping deterministic — ĐỀ XUẤT CHÍNH của em**

Không cho LLM sinh số. Cho nó **phân loại** vào một enum có anchor example rõ ràng:

```
beat_type ∈ { establishing, dialogue_exchange, reaction, reveal,
              action_burst, climax, transition, aftermath }
```

Rồi một **bảng tra deterministic** `beat_type × dialogue_density(code tính) × character_count(code đếm) → layout_template`. Ưu điểm: LLM làm việc nó giỏi (phân loại có nhãn), quyết định layout thành hàm thuần — reproducible, unit-testable, giải thích được cho user ("panel này là climax nên full page"), và **sửa được bằng cách sửa bảng** thay vì sửa prompt.

**(B) Emphasis budget trong phạm vi chapter — chống lạm phát full page**

Buộc quyết định thành **tương đối** thay vì tuyệt đối: mỗi chapter được cấp quota, ví dụ **tối đa 1 full page + 2-3 large panel**. LLM chỉ phải **xếp hạng** các beat trong chapter (ranking ổn định hơn scoring rất nhiều, vì nó là so sánh nội bộ, không cần thang tuyệt đối). Code phân bổ theo quota. Việc này một mình giải quyết cả vấn đề (3) và vấn đề "pacing đều đều" ở 3.1 — vì quota **buộc** phải có tương phản.

**(C) So sánh cặp — chỉ dùng khi làm eval, không dùng ở runtime**

Pairwise "panel A hay panel B quan trọng hơn" đáng tin hơn scoring, nhưng tốn O(n log n) call. Dùng nó để **hiệu chỉnh** rubric (A) offline, không dùng trong đường sinh.

**(D) User chọn — luôn phải có, không phải phương án thay thế**

Nút đổi page template trong UI (§14 đã có chỗ). AI đề xuất, người đổi bằng một click. Đây là lối thoát khi (A)+(B) chấm sai.

Nếu chỉ được làm một việc: **bỏ số thực, dùng (A) + (B)**. Nếu muốn giữ số vì lý do UI, thì chỉ hiển thị nhãn định tính (`cao / trung bình / thấp`) và **không bao giờ đưa số vào một biểu thức ngưỡng**.

#### 3.3. §6 Panel schema — đủ chưa, thiếu gì, field nào là ảo tưởng

Trước tiên, một quan sát: **cây field ở đầu §6 và JSON example ở cuối §6 không khớp nhau.** Cây có `Narrative purpose`, `Location`, `Composition`, `SFX`, `Costume state`, `Visual references`; JSON example **mất cả sáu**. Đặc biệt JSON example **không có location** — mà panel không có location thì prompt compiler không compile được. Đây là dấu hiệu schema chưa được nghĩ đến mức thực thi.

**Thiếu (theo mức độ chặn đường, cao xuống thấp):**

| Field thiếu | Vì sao chặn |
|---|---|
| `page_id`, `panel_index`, `reading_order` | Không có thì không dựng được trang. Cây Scene→Panel của §4 không có tầng Page, nhưng §11 lại có. Bất nhất. |
| `dialogue[]` có cấu trúc, thay vì một string | Xem 3.4. Một string không đủ chỗ cho speaker, thứ tự, loại bubble (speech/thought/narration/off-panel/SFX). |
| `dialogue_rendered` vs `dialogue_source` | Hai field, không phải một. Xem 3.4. |
| `source_span` (trỏ về đoạn văn gốc) | Không có thì tầng dưới và con người mất đường truy nguyên; error laundering ở §1 không chặn được. |
| `permanence`-aware costume/state ref (`costume_state_id`) | JSON hiện hard-code state vào panel → khi bible sửa, panel không đồng bộ. Phải là **reference tới state**, không phải copy giá trị. |
| `character_staging` (ai bên trái / bên phải, ai trước / sau) | Cần cho eyeline và hướng đọc. Không có thì không có ngữ pháp comic. |
| `prev_panel_ref` | Cần cho shot-reverse-shot, quy tắc 180°, và cho continuity check kiểu so sánh cặp (§4 của em). |
| `negative_constraints` | "không có vũ khí trong tay", "không có nhân vật khác trong frame". Prompt compiler cần nó và không suy ra được. |
| `text_budget_chars` | Suy ra từ diện tích panel. Không có thì không biết rút gọn thoại tới đâu. |
| `panel_aspect_ratio` / `size_class` | Layout engine cần; và image model cần đúng aspect từ đầu (crop sau sẽ cắt mất mặt nhân vật). |
| `confidence` / `needs_review` | Đường vào human review queue. |

**Field ảo tưởng — LLM điền được nhưng downstream không dùng nổi:**

1. **`importance: 0.91`** — đã mổ ở 3.2. Ảo tưởng rõ nhất.
2. **`camera_angle: "low_angle"`** — LLM điền dễ, nhưng khả năng image model tuân thủ chính xác góc camera là **giả định IM-A3**, và ước lượng của em là **yếu**. Giữ field (nó có nghĩa về mặt IR, và người vẽ/tool khác dùng được) nhưng **đừng coi nó là ràng buộc đã được đảm bảo**, và hạ nó xuống bậc thấp trong precedence ladder (§5 của em).
3. **`action: "draws sword"`** — mid-action pose là chỗ image model yếu (giả định IM-A3). Sẽ hay ra "đứng cầm kiếm" thay vì "đang rút kiếm".
4. **`lighting: "moonlight"`** — coarse thì được, và đây là chỗ xung đột với global style (xử lý ở §5 của em).
5. **`emotion: "rage"`** — dùng được, nhưng chỉ ở mức thô. Sắc thái ("cố nén giận") thì không.

Nhận xét gộp: schema đang trộn hai loại field mà **không phân tầng** — field **mô tả ý định** (dùng cho IR, cho người, cho tool khác) và field **ràng buộc model** (thực sự đi vào prompt và được tuân thủ). Đề xuất: đánh dấu tường minh mỗi field thuộc loại nào. Không làm việc này thì compiler sẽ đối xử với `camera_angle` như `character_id`, và §5 sẽ hỏng.

#### 3.4. `dialogue` — nguyên văn hay rút gọn, và ai làm việc rút gọn?

Tài liệu **không trả lời**, và đây là một **bước pipeline bị bỏ trống hoàn toàn** — không phải một chi tiết nhỏ.

Số liệu định tính (**ước lượng**): một speech bubble đọc thoải mái chứa khoảng **8-20 từ**; câu thoại trong web-novel dịch thường **30-80 từ**, kèm cả cụm tự sự chen vào. Tức là hệ số nén cần thiết thường **2-5×**. Không có bước rút gọn thì hoặc bubble che hết panel, hoặc thoại bị cắt máy móc giữa câu.

Ba điều phải nói rõ:

1. **Rút gọn là hành vi biên tập có mất, không phải formatting.** Nó phải giữ giọng nhân vật, giữ hàm ý, và biết cái gì chuyển sang narration box, cái gì bỏ, cái gì chuyển thành hình. Đây là việc **cần LLM** (một trong ít chỗ trong pipeline mà em thấy LLM là đúng công cụ) **và cần người review**.
2. **Phải là hai field, không phải một.** `dialogue_source` (nguyên văn + `source_span`, bất biến, để truy nguyên và để re-render khi đổi layout) và `dialogue_rendered` (bản đã nén, có `text_budget_chars` làm ràng buộc, người sửa được, và edit của người **phải khoá lại** khỏi bị re-run ghi đè). Tài liệu chỉ có một string → mất nguyên bản ngay lần compile đầu.
3. **Ràng buộc phải chảy ngược từ layout.** `text_budget_chars` phụ thuộc diện tích panel, mà diện tích lại do layout quyết định. Tức là **layout phải chốt trước khi nén thoại**. Thứ tự trong §17 (`Page Plan` và `Panel Script` song song rồi mới tới compiler) làm sai chỗ này: nén thoại phải nằm **sau** layout. Đây là một lỗi thứ tự pipeline cụ thể, đáng sửa.

#### 3.5. Dialogue attribution

Đúng như đề bài nhận định: đây là bài toán riêng, và nó hay sai. Ví dụ ngay trong tài liệu — `"dialogue": "Ngươi đã phản bội ta."` — không có gì trong văn bản gốc chỉ ra ai nói.

**Vì sao khó trong đúng thể loại này:** truyện dịch dùng dấu gạch đầu dòng `—` không kèm speaker tag; quy ước "luân phiên" chỉ đúng khi đúng hai người và không bị chen; đoạn hội thoại 3+ người kèm nội tâm và tự sự chen giữa thì quy ước sụp; thán từ và câu ngắn ("Hừ.") không mang tín hiệu nào.

**Đề xuất — lại là "LLM đề xuất, code quyết định", cộng ba tầng:**

1. **Anchor deterministic trước.** Regex bắt các dòng **có tag rõ ràng**: `X nói:`, `— ... — X lạnh giọng`, `X cười`, `giọng X`. Precision rất cao. Ước lượng phủ được 30-60% dòng thoại trong web-novel dịch.
2. **LLM chỉ gán các dòng còn lại**, và bắt buộc kèm ba thứ: (a) **danh sách nhân vật có mặt trong scene** lấy từ bible (constrained decoding — speaker phải nằm trong tập này; chỉ riêng ràng buộc này đã diệt một lớp lỗi lớn, vì phần lớn lỗi attribution là gán cho nhân vật **không có mặt**), (b) các dòng đã anchor ở bước 1 làm mốc, (c) cho phép trả `UNKNOWN`.
3. **Kiểm tra chéo bằng prior luân phiên** + kiểm tra nhất quán đại từ/appellation (nếu dòng gọi "sư phụ" thì speaker phải là đệ tử của người nghe — bible có `Relationships`, dùng được).
4. **Dòng confidence thấp thì hiện cờ trong UI**, không âm thầm đoán. Sai speaker là loại lỗi **người đọc thấy ngay**, nên bắt buộc có review gate.

**Tỉ lệ lỗi ước lượng** (ước lượng, giả định như trên):

| Tình huống | Lỗi ước lượng (không có anchor + constraint) | Lỗi ước lượng (có đủ 4 tầng) |
|---|---|---|
| 2 người, hội thoại luân phiên sạch | 10-20% | 3-8% |
| 3+ người, có tự sự chen | 30-50% | 15-25% |
| Câu ngắn / thán từ đơn lẻ | 40-60% | 25-40% |

Kết luận: đây là một trong hai chỗ **bắt buộc** có human gate ở MVP2 (chỗ còn lại là dialogue condensation) — không phải vì không cải thiện được, mà vì chi phí lỗi bất đối xứng: một dòng gán sai làm hỏng cả trang trong mắt người đọc.

---

### 4. Continuity Checker (§15) — thẩm định nghiêm khắc

Tài liệu gọi đây là "feature rất đáng tiền" và ở phần chốt kiến trúc, gọi nó là một phần của **moat**. Em phản biện: **thành phần được tuyên bố là moat lại chính là thành phần ít được kiểm chứng nhất trong toàn thiết kế.** Ở dạng đang mô tả, ước lượng của em là nó tạo ra **giá trị âm**.

#### 4.1. Các cơ chế khả dĩ, và giới hạn từng cái

| Cơ chế | Cách làm | Khả thi | Độ chính xác kỳ vọng (**ước lượng**) |
|---|---|---|---|
| **VLM đọc ảnh + so với spec, output có cấu trúc** | 1 call/panel, hỏi từng attribute thô | Khả thi nhất, dễ dựng | Chỉ dùng được cho attribute **thô + diện tích lớn**: màu trang phục, màu tóc, có/không vật lớn trên tay |
| **Face embedding vs canonical portrait** | Cosine similarity với reference sheet (§8) | Về mặt code: dễ. Về mặt hiệu quả: **em đánh giá là không dùng được làm pass/fail** | Các face recognition model phổ biến được huấn luyện trên ảnh thật; trên art cách điệu/anime, ước lượng của em là khoảng cách embedding **bị nén** — phương sai trong-cùng-nhân-vật xấp xỉ phương sai giữa-các-nhân-vật, nên không có ngưỡng tách được. **Đây là nhận định engineering của em, không phải benchmark.** Tối đa dùng để **xếp hạng** panel đáng xem lại. |
| **Object detection cho vũ khí** | Detector tìm "sword" | Detector off-the-shelf huấn luyện trên ảnh thật; kiếm fantasy cách điệu ngoài phân phối | Ước lượng: kém hơn một câu hỏi yes/no cho VLM. **Không đáng làm** khi đã có VLM |
| **Color histogram / palette trên vùng nhân vật** | Segment người → so palette với costume canonical | Rẻ, deterministic, ổn định | Khá tốt **nếu** segment được. Không segment thì background lấn hết. Đây là check **đáng tin nhất** trong nhóm, nhưng phụ thuộc một bước segmentation mà tài liệu không có |
| **CLIP-style image-text similarity** | Điểm tương đồng với câu mô tả spec | Dễ | **Rơi lại đúng cái bẫy pseudo-precision của §5**: một scalar không có ngưỡng hiệu chỉnh. Không dùng làm gate |

#### 4.2. Điểm quan trọng nhất: false positive làm checker có giá trị âm

Logic kinh tế: giả sử 35 panel/chapter, checker báo lỗi trên 30% panel, và **một nửa số báo là sai**. Người dùng phải mở ~10 panel, phát hiện 5 cái vô cớ. Sau hai chapter, họ học được rằng checker không đáng tin → **bỏ qua toàn bộ cảnh báo**, kể cả cảnh báo đúng. Checker khi đó tệ hơn không có, vì nó đã tiêu **niềm tin**, thứ đắt hơn thời gian.

Ước lượng FP/FN (tất cả là **ước lượng engineering**, giả định: VLM tier khá, art cách điệu, single-character panel, mỗi attribute một câu hỏi có cấu trúc):

| Loại kiểm tra | FP ước lượng | FN ước lượng | Đáng làm? |
|---|---|---|---|
| Màu trang phục chủ đạo (đen vs xanh) | 10-20% | 15-25% | **Có** — diện tích lớn, phân biệt thô |
| Màu tóc (đen vs bạc) | 10-20% | 15-25% | **Có** |
| Có/không vật lớn trên tay (kiếm) | 15-25% | 20-35% | **Biên** — nhiễu từ che khuất, ngoài frame, kiếm trong vỏ. Làm, nhưng phải cho phép `unclear` |
| Kiểu tóc (buộc vs xoã) | 30-50% | 30-50% | **Không** |
| Danh tính khuôn mặt ("có cùng người không") | **40-60%** | 30-50% | **Không** — đây là check tài liệu nhấn mạnh nhất (`✓ face`) và là check **kém khả thi nhất** |
| Chi tiết nhỏ (vết sẹo mắt **trái**) | **50%+** | 40-60% | **Không** — và có lý do riêng: image model rất hay lật gương, nên mọi khẳng định trái/phải gần như vô vọng (giả định IM-A3) |
| Số ngón tay / giải phẫu | 40-70% | 30-60% | **Không** — và đây là nghịch lý: con người phát hiện lỗi này trong 0.2 giây, nên tự động hoá nó là tự động hoá đúng phần **con người đang làm tốt** |
| Trang phục đúng loại (giáp vs áo choàng) | 20-35% | 25-40% | **Biên** |
| **Drift giữa hai panel liền kề** (so ảnh với ảnh, không so ảnh với spec) | 20-35% | 25-40% | **Có, và bị bỏ sót** — so sánh cặp bền hơn phán đoán tuyệt đối, và đúng cái người đọc thực sự cảm nhận |

**Một dependency mà §15 không nhận ra, và nó chặn đường:** để kiểm tra "Lâm Phong trong panel này có mặc áo đen không", trước tiên phải biết **nhân vật nào trong panel là Lâm Phong**. Trong panel 2+ nhân vật, đó chính là bài toán **re-identification** — bài toán mà chính checker được lập ra để giải. Vòng lặp logic. Ví dụ của §15 (`Panel 8 / Princess / ✗ costume mismatch`) giả định đã re-identify được, mà không nói bằng cách nào.

Hệ quả cụ thể, và nó thu hẹp scope rất mạnh: **panel nhiều nhân vật về cơ bản không kiểm tra được** bằng cơ chế này. MVP chỉ nên kiểm panel một nhân vật. Điều này cũng có nghĩa checker phủ được ước lượng **40-60%** số panel, không phải 100% — cần nói rõ với user, đừng để họ hiểu là đã được bảo vệ toàn diện.

#### 4.3. `[Fix automatically]` — về mặt kỹ thuật nghĩa là gì?

Hai khả năng, cả hai đều không phải "fix":

1. **Regenerate cả panel** với prompt được nhấn mạnh hơn. Đây **không phải sửa, đây là re-roll**: mất mọi thứ đang đúng, có thể sửa được áo mà làm hỏng mặt, kết quả không xác định, tốn thêm một lần gọi image model. Và nếu nguyên nhân gốc là **spec sai** (error laundering ở §1) thì re-roll sẽ tái tạo đúng lỗi cũ.
2. **Inpaint vùng sai.** Cần một **mask**. Nhưng checker chỉ biết "costume mismatch", **không biết ở đâu** — nó không có localization. Muốn có mask thì cần thêm một bước segmentation nhân vật + phân vùng trang phục, mà tài liệu không có. Kể cả có mask, đổi màu áo qua nếp gấp + ánh sáng + che khuất thì thường lộ đường ghép.

**Kết luận: `[Fix automatically]` là một nút hứa hẹn quá mức.** Nó ngụ ý hệ thống hiểu lỗi ở mức đủ để sửa có mục tiêu, trong khi thực tế nó chỉ có một tín hiệu nhị phân thô. Đây là loại nút phá niềm tin nhanh nhất: bấm 3 lần không được kết quả tốt hơn là user kết luận cả feature là giả.

Phiên bản trung thực: **`[Tạo lại với ràng buộc được nhấn mạnh]`**, giữ cả hai version (data model §13 đã có `parent_generation` — dùng đúng chỗ này), hiển thị side-by-side, **người chọn**. Không bao giờ tự áp dụng.

#### 4.4. Phiên bản thu hẹp mà thực sự hoạt động, cho MVP

1. **Phạm vi**: chỉ panel **một nhân vật**, chỉ **top 5 nhân vật chính**. Nói rõ với user rằng checker phủ một phần.
2. **Chỉ 3 check**: màu trang phục chủ đạo (nhóm màu, không phải mã màu), màu tóc (nhóm màu), có/không vật lớn trên tay. Cộng thêm **1 check so sánh cặp**: drift so với panel liền trước của cùng nhân vật.
3. **Cơ chế**: một VLM call/panel, structured output, mỗi attribute có `confidence` và **`unclear` là câu trả lời hợp lệ hạng nhất**. Cho phép abstain là cách hạ FP rẻ nhất và hiệu quả nhất.
4. **Hình thức output**: **hàng đợi review được xếp hạng** ("những panel đáng xem lại nhất"), **không** phải huy hiệu ✓/✗ trên từng panel. Khác biệt này không phải chuyện UI — dấu ✗ là một **phán quyết** (sai thì mất niềm tin), còn thứ hạng là một **gợi ý** (sai thì chỉ tốn 3 giây). Cùng một mô hình, hai giá trị sản phẩm hoàn toàn khác.
5. **Cổng chất lượng trước khi ship**: dán nhãn tay **≥100 panel**, đo precision/recall/abstain cho từng attribute. **Chỉ bật check nào đạt precision ≥ ~0.7** (đây là ngưỡng **em đặt ra**, không phải benchmark). Check nào dưới ngưỡng thì ẩn đi — kể cả `face`.
6. **Không autofix.**
7. **Chạy khi nào**: theo yêu cầu / lúc chốt trang, **không** chạy trên mọi bản nháp. Đây là cost hot spot #2 (§7).

Và một điểm định vị lại: giá trị lớn nhất của checker **không phải** ở chỗ bắt lỗi. Nó là ở chỗ **tạo ra dữ liệu có nhãn** — mỗi lần người dùng chấp nhận/từ chối một cảnh báo là một nhãn. Đó là nguồn duy nhất cho eval của Layer 3 (§6). Nên coi nó là **công cụ đo lường có mặc áo feature**, và điều đó lại càng là lý do làm nó nhỏ và trung thực thay vì to và ồn ào.

---

### 5. Visual Prompt Compiler (§16) — dưới góc prompt engineering

#### 5.1. Instruction/attention dilution và tác động lên thiết kế này

Hiện tượng là **thật** (đây là đánh giá engineering của em, không dẫn benchmark): khi số ràng buộc trong một prompt tăng, tỉ lệ tuân thủ **từng** ràng buộc giảm; và các model có position bias — thông tin ở đầu/cuối prompt được tôn trọng hơn phần giữa. Với text-conditioned image model, ước lượng của em: **trần thực tế khoảng 5-8 ràng buộc thị giác được tôn trọng đồng thời** (**ước lượng, giả định IM-A2, cần lens khác verify với model 2026 cụ thể**).

§16 liệt kê **9 nhóm** ràng buộc, và mỗi nhóm khi bung ra thành câu chữ sẽ thành nhiều ràng buộc con (Character Identity một mình đã là tóc + mắt + tuổi + tỉ lệ cơ thể + nét mặt). Tổng thực tế dễ đạt **20-40 ràng buộc**. Hệ quả: prompt sẽ luôn có **một tập con bị bỏ âm thầm**, và tập con đó **thay đổi giữa các lần gọi** — nên lỗi không tái lập được, không debug được.

Ba hệ quả thiết kế, đi từ hệ quả nặng nhất:

1. **Compiler phải là compiler theo nghĩa thật — nó phải BIẾT LOẠI BỎ, không phải nối chuỗi.** Cần một **constraint budget** cứng và một **precedence ladder**; ràng buộc vượt ngân sách bị **drop tường minh** và **ghi log những gì đã drop** (auditability). Sơ đồ §16 hiện là một phép hợp nhất 9 nhánh — tức là nối chuỗi. Đó không phải compile, đó là concatenate.
2. **Identity KHÔNG được đi qua kênh text.** Đây là điểm kiến trúc nặng nhất của mục này. Nếu prompt phải cạnh tranh giữa "khuôn mặt nhân vật" và "ánh trăng gay gắt", thì identity — thứ **không được phép** sai — đang bị đặt cùng hạng với thứ có sai cũng chẳng chết. Identity phải đi qua **kênh không phải text** (reference image conditioning / character-consistency feature / fine-tune per character — tên cụ thể thuộc lens khác, giả định IM-A1), và prompt text chỉ mô tả **cái gì thay đổi**.

   Đáng chú ý: **§8 của tài liệu đã có trực giác đúng** ("Chứ không chỉ đưa text prompt", có sơ đồ cộng các reference). Nhưng **§16 lại làm phẳng tất cả thành một output duy nhất "Model-specific prompt"**. Hai mục **mâu thuẫn nhau**, và §16 là mục đang định nghĩa kiến trúc. Cần sửa: compiler có **hai output** — `text_prompt` **và** `conditioning_set` (danh sách reference asset + trọng số) — cộng `negative_prompt` và `model_params`.
3. **Panel nhiều nhân vật ăn ngân sách gấp đôi** (mỗi nhân vật một bộ identity constraint). Cộng với kết luận ở §4 (panel nhiều nhân vật không kiểm tra được), có một khuyến nghị **xuyên tầng** đáng đưa vào Layer 2: **directing nên thiên vị panel một nhân vật vì lý do kỹ thuật.**

#### 5.2. Khi ràng buộc xung đột — tài liệu không nói. Đề xuất precedence rule.

Ví dụ đề bài: style nói `soft lighting`, panel spec nói `harsh moonlight`. Nếu compiler nối cả hai, model sẽ nhận một prompt tự mâu thuẫn và ra kết quả nhoè nhoẹt trung bình của hai bên — kết quả tệ nhất trong ba khả năng.

**Ba quy tắc, phải có cả ba:**

**Quy tắc 1 — Precedence ladder (bậc cao thắng; bậc thấp bị DROP, không trộn):**

| Bậc | Nhóm ràng buộc | Ghi chú |
|---|---|---|
| 1 | Character identity refs (face/body) | Không thương lượng. Không bao giờ bị drop |
| 2 | Hard continuity từ timeline state, `permanence = PERMANENT` (vết sẹo, mất tay, màu tóc canonical) | Sai là lộ ngay và phá liên tục |
| 3 | Semantic cốt lõi của panel: shot size, ai có mặt, hành động chính, cảm xúc | Bỏ là panel vô nghĩa |
| 4 | Location identity (thô: nơi nào, palette chính) | |
| 5 | Lighting/mood cục bộ của panel | |
| 6 | Global style descriptor (art style tokens) | Nên chuyển phần lớn sang style reference/fine-tune thay vì chữ |
| 7 | Camera angle, composition language, props phụ | Bị drop đầu tiên khi hết ngân sách |

**Quy tắc 2 — Xung đột giải theo TỪNG CHIỀU, ở scope cụ thể nhất.** Không phải "panel thắng style" một cách toàn cục. Panel thắng style **chỉ trên chiều lighting**; các chiều khác của style (line art, rendering, palette) **không bị ảnh hưởng**. Nếu không tách theo chiều, một xung đột lighting sẽ vô tình xoá cả art style — lỗi này khó thấy và rất tốn tiền.

**Quy tắc 3 — Cờ `style_lock` do người dùng chốt, ở cấp project:**
- `style_lock = strict` → global style thắng, panel lighting bị hạ xuống mô tả yếu ("dim light" thay vì "harsh moonlight").
- `style_lock = loose` → panel thắng (mặc định).
- Và trong **cả hai** trường hợp: compiler **phải phát warning ra UI** khi nó override — "panel này bỏ qua style lock về lighting". Người dùng thấy được quyết định thì mới sửa được. Override âm thầm là cách nhanh nhất để tạo ra lỗi không ai truy được.

#### 5.3. Deterministic template code vs LLM — vẽ ranh giới

**Nên là deterministic code (mục tiêu: ~90-95% compiler):**

- Tra bảng `field value → cụm từ` (`shot: close_up` → `"close-up shot"`; `emotion: rage` → cụm từ đã chọn sẵn). Đây là **lookup table**, không phải suy luận.
- Sắp thứ tự, dedup, xử lý xung đột theo Quy tắc 1-3, thực thi constraint budget + **ghi log ràng buộc bị drop**.
- Chọn reference asset theo ID từ bible/state (`costume_state_id` → file reference).
- Assemble negative prompt.
- Adapter theo cú pháp từng model (weighting syntax, param name) — đây chính là chỗ "dễ thay model" của §11 được hiện thực, và nó là **code**.
- Ghi `compiler_version` + hash input vào bảng `Generation`.

**Cần LLM (hẹp, và nên cache vĩnh viễn):**

- **(a) Soạn từ vựng, offline, một lần**: sinh cụm từ tốt cho mỗi giá trị attribute, **người review**, rồi **lưu vào bảng**. Đây là dữ liệu, không phải runtime.
- **(b) Dịch action tự do → cụm pose ngắn**, chỉ khi từ vựng chưa có entry. **Cache theo hash của action text** → trả tiền một lần cho toàn bộ bộ truyện. Trong web-novel, action lặp lại rất nhiều ("rút kiếm", "chắp tay", "phi thân") nên hit rate cache ước lượng rất cao sau vài chapter.
- **Ngoài hai việc trên: không có LLM trong compiler.**

**Cảnh báo mạnh, và nó là một mâu thuẫn nội tại của tài liệu:** §13 dựng bảng `Generation` với `prompt / model / model_version / seed / parent_generation` với mục đích tuyên bố là **reproducibility**. Nhưng nếu có LLM trong đường compile ở runtime, thì **cùng một panel spec sẽ sinh ra prompt khác nhau vào ngày mai** — và reproducibility mà §13 tồn tại để bảo đảm **bị phá ngay tại chỗ**. Hai mục này không thể cùng đúng. Compiler deterministic là **điều kiện cần** để §13 có nghĩa.

Cộng thêm: compiler deterministic thì unit-test được bằng golden snapshot (§6), chi phí bằng 0, và là **cách rẻ nhất để tăng độ tin cậy toàn pipeline** — vì nó chuyển một tầng từ 90% sang 100% trong phép nhân cascade ở §1. Ngược lại, đặt LLM ở đây là chỗ **dễ đốt token nhất mà thu về ít nhất**: theo ước lượng ở §7, LLM-in-compiler một mình có thể chiếm >50% tổng token của pipeline text.

---

### 6. Evaluation & testing — mục tài liệu HOÀN TOÀN thiếu

Xác nhận: em đã đọc toàn văn 894 dòng, **không có một dòng nào** về đo lường chất lượng, golden set, metric, hay regression. Với một hệ thống mà mọi tầng đều là phán đoán của model, đây không phải "thiếu một mục" — đây là **thiếu vòng phản hồi**. Không có nó thì mọi lần sửa prompt là một lần thay đổi mù, và sau ba tháng sẽ không ai trả lời được câu "hôm nay tốt hơn tháng trước không".

#### 6.1. Bộ eval cho từng layer

| Layer | Golden set | Metric | Judge | Tự động? |
|---|---|---|---|---|
| **L1 Extraction** | 5-10 chapter thật, dán nhãn tay: entity, alias cluster, state-change event (kèm `permanence`) | Entity P/R/F1; **alias cluster purity**; state-event F1; **bible corruption rate** (% fact sai tại chapter N) | Script so nhãn | **Có, hoàn toàn** |
| **L1 Chapter parse / text clean** | 20 file thật từ nhiều nguồn | % chapter boundary đúng; % dòng rác còn lại | Script | **Có** |
| **L2 Dialogue attribution** | Cùng golden set, dán nhãn speaker từng dòng | Accuracy; accuracy trên tập không có tag; abstain rate | Script | **Có** — đây là sub-metric duy nhất của L2 có ground truth, phải khai thác |
| **L2 Dialogue condensation** | 100 cặp (nguyên văn, bản nén) | Có vừa `text_budget`? Có giữ nghĩa? (entailment check trên mẫu) + rubric người | Người + LLM-judge hỗ trợ | **Một phần** |
| **L2 Directing (scene/panel breakdown)** | 10 chapter | Rubric người 1-5 trên: pacing, panel count hợp lý, chọn đúng beat, có bắt được subtext | **Người**. LLM-judge chỉ dùng **pairwise A/B**, và chỉ sau khi hiệu chỉnh với ~30 nhãn người; **không bao giờ dùng làm điểm tuyệt đối** | **Không** |
| **L2 Layout** | 10 chapter | Sau khi đổi sang rubric (§3.2): agreement với nhãn `beat_type` của người; **phân bố** full-page/chapter (phát hiện lạm phát) | Script + người | **Một phần** |
| **L3 Compiler** | Bộ panel spec cố định | **Golden prompt snapshot, so exact-match**; test constraint-drop; test precedence với case xung đột dựng sẵn | Unit test | **Có, gần như miễn phí** |
| **L3 Image gen** | Tập panel cố định | Consistency do người chấm; ngoài scope lens em về việc chọn model | **Người** | **Không** |
| **Continuity Checker** | ≥100 panel dán nhãn tay | Precision/recall/abstain **theo từng attribute** | Script | **Có, sau khi có nhãn** |

#### 6.2. Cái gì đo tự động được, cái gì buộc phải có người — nói thẳng

- **Tự động được (và phải tự động ngay)**: extraction, alias resolution, state-at-chapter-N, dialogue attribution, compiler output, schema/property validity, cost/token. Đây đều là những thứ **có đáp án đúng**.
- **Buộc phải có người**: chất lượng directing, "panel này có đáng vẽ không", giọng nhân vật trong bản nén thoại, chất lượng thị giác cuối cùng. Đây là những thứ **không có đáp án đúng**, và mọi cố gắng tự động hoá chúng bằng LLM-judge chỉ chuyển bài toán "AI có tốt không" thành "AI khác nghĩ AI này có tốt không" — không giải quyết gì, chỉ che đi.
- Cách đọc bảng này cho đúng: **ranh giới automatable/human trùng khớp với ranh giới extraction/creative ở §3.1.** Tầng nào tài liệu gọi là "AI quyết định" mà không có ground truth thì tầng đó cần người — và đó cũng chính là các HITL gate ở §8.

#### 6.3. Non-determinism — regression test kiểu gì

Exact-match là vô dụng cho L1/L2. Bốn kỹ thuật, dùng đồng thời:

1. **Property-based assertion thay vì so sánh output** (rẻ nhất, giá trị cao nhất, chạy được trên **mọi** chapter chứ không chỉ golden set):
   - Output hợp schema.
   - Mọi `character_id` trong panel **resolve được** trong bible.
   - Không panel nào chứa nhân vật **không có mặt** trong scene.
   - **Không có mâu thuẫn state**: nhân vật cầm vũ khí X ở ch12 trong khi bible ghi đã mất X ở ch10. Đây là assertion mạnh nhất — nó bắt được error laundering ở §1.
   - Panel count / 1000 từ nằm trong dải hợp lý.
   - `dialogue_rendered` có overlap từ vựng tối thiểu với `dialogue_source` (chống hallucination thoại).
   - Fact có `permanence = PERMANENT` **không bao giờ biến mất** ở chapter sau.
2. **Metric phân bố, không phải điểm đơn**: chạy golden set **n=3 lần**, báo mean ± spread, và **gate theo mean** với ngưỡng sụt cho phép. Một lần chạy tốt không phải bằng chứng.
3. **Ghim seed + temperature = 0** ở đâu có, để giảm nhiễu — nhưng **không tin nó**, và ghim cả `model_version` (§13 đã có field, tốt).
4. **Snapshot diff cho người xem nhanh**: giữ output cũ của 10 chapter cố định, hiện diff. 10 phút của người mỗi lần đổi prompt là mức đầu tư đúng.

#### 6.4. Bộ eval TỐI THIỂU phải có ngay ở MVP1

Đây là danh sách em cho là không thể cắt. Ước lượng khối lượng: **1-2 ngày công** để dựng, và nó là ranh giới giữa engineering và cảm tính.

1. **Golden set 5 chapter** từ đúng bộ truyện mục tiêu, dán nhãn tay (main cast + alias + state event + speaker từng dòng thoại). ~4-6 giờ người.
2. **Script tính metric**: entity F1, alias purity, state-event F1, dialogue attribution accuracy. Một file, chạy một lệnh.
3. **Property assertion** (mục 6.3.1) chạy trên 20 chapter — không cần nhãn, nên rất rẻ và phủ rộng.
4. **Bộ đếm token + chi phí mỗi lần chạy**, ghi log. Không có nó thì §7 chỉ là ước lượng mãi mãi.
5. **Prompt version log**: prompt nào ra số nào. Không có thì mọi phép so sánh vô nghĩa.

Và một lời nhắc về thứ tự: **eval kit này phải ra đời TRƯỚC hoặc CÙNG LÚC với MVP1**, không phải sau. Vì nó chính là công cụ để biết MVP1 đã xong hay chưa. Hiện tại §18 định nghĩa "xong MVP1" bằng danh sách feature ("có Story Bible") thay vì bằng ngưỡng chất lượng ("Story Bible đạt entity F1 ≥ 0.9") — và với một hệ thống LLM, định nghĩa xong bằng feature là định nghĩa không kiểm chứng được.

---

### 7. Chi phí và độ trễ của cả pipeline (phần LLM, không phải image)

**Giả định (nêu rõ để PM đối chiếu):**
- Chapter 3000 từ → **~7k token** (hệ số 1.5-2× so với English, do tiếng Việt/truyện dịch — **ước lượng**).
- ~5 scene/chapter, **~35 panel/chapter**.
- `bible_slice` bị **cap 3k token** (nếu không cap thì xem dòng cảnh báo cuối bảng).
- Giá blended **giả định**: ~$2.5/1M input, ~$12/1M output. **Đây là giả định về mặt bằng giá, không phải giá đã verify** — giá 2026 biến động, PM cần đối chiếu.

**Một chapter:**

| Tầng | Số call | Input | Output | Ghi chú |
|---|---|---|---|---|
| Chapter parse + text clean | **0** | 0 | 0 | Deterministic |
| Extraction (entity/event/state) | 1-2 | ~11k | ~2k | chapter 7k + bible_slice 3k + schema 1k |
| Alias merge proposal | ~0.3 | ~2k | ~0.5k | Chỉ khi có candidate mới; giảm dần theo chapter |
| Story Bible reduce | **0** | 0 | 0 | **Deterministic reducer** |
| Scene graph | 1 | ~9k | ~2k | |
| Panel script (5 scene) | 5 | ~25k | ~10k | |
| Dialogue attribution + condensation | 5 | ~15k | ~5k | Có thể gộp vào panel script |
| Layout (rubric + bảng tra) | ~0 | ~0 | ~0 | **Deterministic** sau khi bỏ Layout Score |
| Prompt compile | **0** | 0 | 0 | **Deterministic** (§5) |
| **Tổng "lean"** | **~13** | **~62k** | **~19.5k** | |
| Continuity check (VLM, 1/panel) | +35 | +~70k | +~10k | Tuỳ chọn, on-demand |
| **(phản ví dụ) LLM-in-compiler** | +35 | +~70k | +~10k | Thiết kế **không nên** làm |

**100 chapter (ước lượng):**

| Kịch bản | Số call | Input | Output | Chi phí ước lượng |
|---|---|---|---|---|
| Lean (compiler deterministic, không VLM check) | ~1,300 | ~6.2M | ~2.0M | **~$40** |
| Lean + VLM check mọi panel | ~4,800 | ~13.2M | ~3.0M | **~$70-150** (token ảnh có thể tính giá khác) |
| Có LLM trong compiler nữa | ~8,300 | ~20M | ~4.0M | **~$100+** |
| Nhân hệ số thử-sai lúc dev (5-10× re-run) | — | — | — | **~$200-1,000** cho toàn bộ đời dự án 100 chapter |

**Kết luận quan trọng và hơi phản trực giác: chi phí LLM KHÔNG phải nút thắt.** Vài chục tới vài trăm đô cho 100 chapter là chấp nhận được kể cả với giả định A1 (1 dev, ngân sách tự bỏ). Nút thắt thật, theo thứ tự:

1. **Image generation**: 35 panel × 100 chapter = **3,500 ảnh**, và với re-roll 3-5× thì là 10,000-17,500 lần gọi. Ngay cả ở đơn giá thấp, đây là bậc độ lớn lớn hơn phần LLM. (Đơn giá cụ thể: ngoài scope lens em.)
2. **Thời gian của con người**: HITL gate (§8) dù chỉ 5 phút/chapter cũng là **~8 giờ cho 100 chapter**. Với A1 (một người), **đây là ràng buộc gắt nhất của cả dự án** — gắt hơn tiền. Mọi quyết định thiết kế nên tối ưu **phút-người/chapter**, không phải đô-la/chapter.
3. **VLM continuity check**: hot spot #2 về token, và là lý do phải chạy on-demand thay vì mọi bản nháp.

**Cắt ở đâu:**
- **Deterministic hoá** (compiler, reducer, layout mapping, parse): cắt được ~50% token trong kịch bản xấu, và **tăng** độ tin cậy — hiếm khi có đánh đổi một chiều như vậy, nên làm ngay.
- **Model nhỏ cho tầng dễ**: chapter parse (0 call), alias normalize (0 call), extraction có thể dùng tier rẻ hơn; giữ tier khá cho directing và condensation (việc sáng tạo).
- **Cache**: pose lexicon theo hash action (hit rate cao trong web-novel), `bible_slice` theo chapter, và **không tính lại chapter đã xử lý** (cần content hash).
- **Batch panel theo scene**: 1 call cho cả scene thay vì 1 call/panel — hệ số tiết kiệm ~3-7× ở tầng panel script.
- **VLM check chọn lọc**: chỉ panel single-character, chỉ khi chốt trang.

**Latency**: chuỗi lean có ~4-6 bước phụ thuộc tuần tự (các call cấp scene song song được) → ước lượng **1-4 phút/chapter** cho toàn bộ phần text. Không đáng lo, và nó **xác nhận** lựa chọn Job Queue của §12 là đúng: pipeline này là **batch/async**, không phải interactive. Điểm cần chú ý: **UI ở §14 lại là interactive**. Cần thiết kế rõ chỗ nào là "bấm rồi chờ vài phút, có progress" và chỗ nào là "phản hồi tức thì" — nếu không, trải nghiệm sẽ là một cái spinner dài không giải thích.

**Cảnh báo phi tuyến (nhắc lại vì nó là rủi ro chi phí duy nhất đáng lo):** nếu bỏ cap `bible_slice`, ở chapter 500 bible có thể đạt 150k-400k token, input mỗi call phình 20-50×, và tổng chi phí nhảy **hai bậc độ lớn** — kèm nguy cơ vỡ context limit. **Cap retrieval là yêu cầu kiến trúc, không phải tối ưu về sau.**

---

### 8. Human-in-the-loop — thiết kế đúng nằm ở đâu?

Trước hết, một **mâu thuẫn nội tại của tài liệu** cần chỉ ra: §14 mô tả UI kiểu "Figma + comic editor + AI director", cho phép click panel để regenerate, đổi camera, đổi costume — **đó chính là một human-in-the-loop editor**, và nó là phần hay nhất của concept. Nhưng §18 lại đặt "Human approval workflow" ở **MVP4**, tức là cuối cùng. Hai mục này không nhất quán: §14 giả định HITL là bản chất sản phẩm, §18 coi nó là feature phụ.

**Gate bắt buộc (không phải "nice to have"):**

| Gate | Ở đâu | Người làm gì | Vì sao BẮT BUỘC |
|---|---|---|---|
| **A — Story Bible** | Sau khi extract N chapter đầu (5-10), rồi định kỳ | Duyệt/gộp alias cluster, sửa attribute nhân vật, xác nhận `permanence`, xoá entity rác | Đây là **điểm sửa lỗi rẻ nhất trong toàn hệ thống**. Một fact sai ở bible sẽ nhiễm độc **mọi** panel của **mọi** chapter sau. 15 phút của người ở đây tiết kiệm hàng trăm ảnh sai. Nó cũng là gate duy nhất chặn được error laundering (§1) |
| **B — Panel script, TRƯỚC image gen** | Sau Layer 2 | Sửa panel breakdown, sửa dialogue attribution, sửa bản nén thoại, chọn lại layout | Chặn ngay trước tầng **đắt và không hoàn lại** (image gen). Cũng là chỗ duy nhất sửa được "AI không biết cái gì đáng vẽ" (§3.1) |
| **C — Accept/reject ảnh** | Sau Layer 3 | Chọn giữ / re-roll / sửa | Trên thực tế không tránh được; nó là vòng lặp chính của UI §14 |

Gate tuỳ chọn: chọn layout template (mặc định do rubric, người override).

**Nếu để tới MVP4 mới làm thì hỏng ở đâu — cụ thể, không chung chung:**

1. **Hỏng ở data model, và đây là hỏng nặng nhất.** HITL không phải một cái UI, nó là một **yêu cầu về schema**. Cần từ ngày đầu, trên **mọi** bible fact / panel field / dòng thoại:
   - `source: ai | human`
   - `locked: bool` — **edit của người phải sống sót qua lần re-run sau**
   - `edited_at`, `edited_by`
   - `superseded_by` / lineage
   Nếu MVP1-3 xây không có các field này, thì việc thêm vào ở MVP4 **không phải thêm feature** — nó là viết lại schema + viết lại logic merge của cả ba tầng. Đây là loại nợ kỹ thuật đắt nhất: nó không đau lúc vay và không thể trả từng phần.
2. **Hỏng ở chỗ mất luôn eval.** UI review của con người **chính là công cụ dán nhãn**. Hoãn HITL = hoãn nhãn = hoãn eval (§6) = xây ba tầng LLM trong bóng tối suốt ba milestone. Đến MVP4 mới đo thì sẽ phát hiện Layer 1 sai 20% **sau khi** đã xây Layer 2 và 3 trên nền đó.
3. **Hỏng ở kinh tế của MVP3.** Không có Gate B, MVP3 sẽ generate ảnh từ panel script chưa ai xem. Với ước lượng 10-15% panel sai rõ (§3.1), đó là 10-15% chi phí image gen đốt vào ảnh chắc chắn bỏ — cộng thời gian người ngồi lọc ở cuối, nơi lỗi đắt nhất để sửa.
4. **Hỏng ở việc không biết pipeline sai ở tầng nào.** Không có gate trung gian, khi ảnh sai thì không phân biệt được lỗi extraction / directing / compile / model. Toàn bộ lợi ích debuggability mà §1 hứa hẹn **chỉ hiện thực hoá được qua các gate** — IR mà không có ai xem thì không debug được gì.

**Khuyến nghị**: chuyển Gate A vào **MVP1** (nó vốn là UI chính của MVP1 — Story Bible editor), Gate B vào **MVP2**, Gate C vào **MVP3**. MVP4 chỉ còn lại phần **quy trình** (approval status, batch, export) chứ không phải phần **năng lực**. Và ba trường provenance ở trên phải có trong migration đầu tiên.

---

### 9. Kết luận AI/ML

#### 9.1. Verdict một câu

**Khả thi có điều kiện** — phần AI **hiểu truyện và sinh IR** (Layer 1 + 2) là khả thi ở mức "bản nháp cần người biên tập", với điều kiện: (1) mọi transform có đáp án đúng phải là **deterministic code, không phải LLM** (reducer, compiler, layout mapping, parse); (2) **HITL gate ở MVP1**, không phải MVP4; (3) **eval kit tối thiểu ra đời cùng MVP1**; (4) **bỏ Layout Score dạng số thực** và **thu hẹp Continuity Checker** về warning-only, bỏ autofix; và (5) — điều kiện nằm ngoài lens em — **consistency của image model phải được kiểm chứng riêng**, vì đó là giả định chịu lực của cả sản phẩm.

#### 9.2. Xếp hạng rủi ro (chưa được kiểm chứng — cao nhất trước)

| # | Thành phần | Mức | Đánh giá |
|---|---|---|---|
| 1 | **Character visual identity consistency qua hàng trăm panel** (Layer 3) | **Cầu may** | Giả định chịu lực của toàn sản phẩm. **Ngoài lens em** — phụ thuộc giả định IM-A1/A4. Nếu cái này không đạt, mọi thứ khác vô nghĩa |
| 2 | **Continuity Checker** | **Cầu may** | Tài liệu tự gọi là moat; là phần **ít được kiểm chứng nhất**. FP profile xấu + vòng lặp re-identification (§4) |
| 3 | **`[Fix automatically]`** | **Cầu may** | Nên cắt hoặc đổi tên. Không có localization |
| 4 | **Layout Score dạng số thực** | Cao, nhưng **đã biết cách sửa** | Cơ chế không hoạt động như tác giả nghĩ; có phương án thay thế rõ ràng (§3.2) |
| 5 | **Chất lượng directing** (panel-worthiness, pacing, subtext) | Trung bình-cao | Sẽ ra "dùng tạm được". Cần người. Không có ground truth → không tự cải thiện được |
| 6 | **Dialogue attribution + condensation** | Trung bình | Giải được bằng constrained decoding + gate. Nhưng hiện **không ai sở hữu bước này** trong tài liệu |
| 7 | **Cross-chapter entity resolution ở quy mô 500 chapter** | Trung bình-thấp | Bài toán có hình dạng đã biết, có pattern giải đã biết. Cần kỷ luật, không cần đột phá |
| 8 | **State inference qua event sourcing** | Thấp | Sau khi tách LLM/reducer thì gần như là software thường. **Nhưng cần thêm phân loại `permanence`, hiện đang thiếu** |
| 9 | **Extraction entity/location/event trong một chapter** | **Chắc chắn làm được** | |
| 10 | **Deterministic compiler, Generation lineage, versioning, DB model** | **Chắc chắn làm được** | Software thuần. Phần vững nhất của tài liệu |
| 11 | **Chi phí LLM** | **Rủi ro thấp** | Vài chục-vài trăm đô/100 chapter (§7). Không phải nút thắt |

Câu chốt của bảng này: **thứ tài liệu tự tuyên bố là moat (Continuity Checker + bộ máy consistency) lại chính là thứ ít được kiểm chứng nhất; thứ tài liệu coi là hiển nhiên (Story Bible + event sourcing + compiler) mới là thứ chắc chắn làm được và thực sự tạo giá trị.** Moat thật nằm ở **IR + provenance + editability**, không nằm ở checker.

#### 9.3. Top 3 chỗ tài liệu lạc quan quá mức

1. **Layout Score (§5) — `0.95 / 0.88 / 0.76 => FULL PAGE`.** Trình bày như một cơ chế định lượng, thực chất là số không hiệu chỉnh, không ổn định giữa hai lần gọi, không so sánh được giữa chapter, và **không có hàm tổng hợp nào được định nghĩa**. Bằng chứng tự tố: `dialogue density 0.20` là đại lượng **code tính chính xác được** mà tài liệu lại giao cho LLM đoán. Đây là trang trí đội lốt khoa học, và cái giá thật là nó sẽ sinh ra một bảng cấu hình ngưỡng chẳng điều khiển gì.
2. **Continuity Checker là "feature rất đáng tiền" + `[Fix automatically]` (§15).** Ba vấn đề chồng nhau: check quan trọng nhất (`✓ face`) là check **kém khả thi nhất** trên art cách điệu (FP ước lượng 40-60%); mọi panel nhiều nhân vật **không kiểm được** vì cần re-identification — chính bài toán checker định giải; và `[Fix automatically]` không có localization nên chỉ có thể là re-roll (mất cái đang đúng) hoặc inpaint (không có mask). Ở dạng hiện tại, đây là **máy sinh nhiễu**, và một checker nhiễu **tệ hơn không có checker** vì nó tiêu niềm tin, thứ không mua lại được.
3. **MVP1 được đóng khung là milestone dễ (§18) — "chưa cần generate ảnh".** Thực tế MVP1 chứa **hai bài toán khó nhất của phần non-visual**: cross-chapter entity resolution và state inference bền vững qua hàng trăm chapter. Cả hai **không được đặt tên** trong tài liệu. Đồng thời MVP1 thiếu: bước làm sạch text, phân loại `permanence` của attribute, provenance field cho HITL, và toàn bộ eval. Và định nghĩa "xong" của nó là **danh sách feature** thay vì **ngưỡng chất lượng** — với hệ thống LLM, đó là định nghĩa không kiểm chứng được.

*(Đề cử thứ tư): "dễ thay model" (§11, §18).* IR giúp thật, nhưng đổi image model sẽ **vô hiệu hoá** toàn bộ reference asset, fine-tune per-character, prompt lexicon đã hiệu chỉnh, và mọi trang đã sinh (style lệch giữa chapter cũ và mới). "Không phải phân tích lại truyện" **≠** "đổi model là rẻ".

#### 9.4. Top 3 thay đổi thiết kế đáng giá nhất, nên làm ngay

1. **Event-sourced Story Bible + provenance từ ngày đầu.** LLM chỉ phát **event** (`entity, attribute, value, permanence, evidence_span, confidence`); **deterministic reducer** sở hữu state; `state_at(N)` là truy vấn DB. Bắt buộc thêm **phân loại `permanence`** (PERMANENT / SEMI_PERSISTENT / SCENE_SCOPED / TRANSIENT) — không có nó thì reducer không thể vừa giữ vết sẹo 400 chapter vừa quên cơn giận sau một scene. Kèm `source / locked / edited_at / superseded_by` trên mọi fact. Một thay đổi này giải quyết đồng thời: state inference, khả năng retrofit HITL, reproducibility, và cắt chi phí.
2. **Vẽ lại ranh giới LLM/code — deterministic hoá 4 chỗ.** Prompt compiler (bỏ hẳn LLM ở runtime; nếu không thì bảng `Generation` của §13 vô nghĩa), Story Bible reduce, layout mapping (bỏ số thực → rubric `beat_type` + bảng tra + **emphasis quota theo chapter** để chống lạm phát full page và chống pacing phẳng), và chapter parse/text clean. Kèm **precedence ladder + constraint budget + drop log** trong compiler, và tách compiler thành **hai output** (`text_prompt` + `conditioning_set`) để identity không phải cạnh tranh với ánh trăng trong cùng một chuỗi text.
3. **Dịch HITL và eval lên MVP1.** Gate A (Story Bible review) vào MVP1, Gate B (panel script review, trước image gen) vào MVP2. Kèm eval kit tối thiểu (golden set 5 chapter + script F1 + property assertion + token counter + prompt version log) — ước lượng 1-2 ngày công. Đồng thời **thu hẹp Continuity Checker** về: single-character panel, 3 attribute thô + 1 check drift theo cặp, có `unclear`, output là **hàng đợi xếp hạng chứ không phải phán quyết ✓/✗**, cổng precision ≥ ~0.7 trên 100 panel dán nhãn trước khi bật, **và bỏ `[Fix automatically]`**.

#### 9.5. Đề xuất spike đầu tiên (1 tuần, một thí nghiệm duy nhất)

Trong phạm vi lens của em, thí nghiệm có giá trị quyết định cao nhất là **Story Bible Spike: entity resolution + state persistence trên truyện thật, đo ở khoảng cách xa**. Lý do chọn: nó kiểm chứng đúng cái mà cả sản phẩm dựa vào ("không loạn nhân vật qua hàng trăm chapter"), nó **đo được bằng số**, và nó vừa một tuần.

**Input**
- **Một** bộ web-novel dịch từ tiếng Trung có **≥60 chapter** (đúng thể loại target). Lấy văn bản thật, kể cả rác scrape — không làm sạch bằng tay.
- Chọn hai cửa sổ: **chapter 1-10** (liên tục, để dựng bible) và **chapter 38-42** (cửa sổ xa, để đo carry-over).
- **Ground truth dán nhãn tay** cho 15 chapter đó, **chỉ main cast** (~8-10 nhân vật): danh sách canonical, danh sách alias/appellation cho từng người, các state-change event kèm `permanence`, và 20 "state probe" (câu hỏi dạng "ở chapter 40, X đang mặc gì / có vũ khí gì / có thương tích gì"). **Ước lượng 4-6 giờ người.**

**Làm gì**
- Pipeline tối thiểu, không UI, JSON trên đĩa:
  1. Extraction từng chapter với `bible_slice` **cap 3k token**.
  2. Alias registry: normalize + strip honorific + fuzzy/Hán-Việt match (deterministic) → LLM đề xuất merge cho phần còn lại, có `evidence_span` → registry do code sở hữu.
  3. Deterministic reducer fold event → `state_at(N)`.
- **Không** làm: directing, layout, compiler, image, UI. Nếu tuần đó chạm vào ảnh thì spike đã thất bại về mặt phạm vi.

**Đo gì (và đây là phần quyết định)**

| Chỉ số | Cách đo | **Ngưỡng pass (ngưỡng do em đặt, KHÔNG phải benchmark)** |
|---|---|---|
| Entity P/R/F1 trên main cast | So nhãn | **F1 ≥ 0.90** |
| **Alias resolution ở cửa sổ xa** | "Lâm công tử" ở ch40 có resolve về cùng canonical ID với "Lâm Phong" ở ch3? | **≥ 0.85** mention main-cast ở ch38-42 đúng |
| **State-at-chapter-40** | 20 probe dán nhãn tay | **≥ 0.80** đúng |
| **Persistence của attribute PERMANENT** | Cắm 3 event permanent ở ch5/ch8/ch11 (vết sẹo, mất vũ khí, đổi màu tóc), truy vấn ở ch40 | **100%** — phải tuyệt đối. Reducer là deterministic, nên nếu thiếu thì **lỗi nằm ở extraction event**, và điều đó chỉ đúng một nửa pipeline. Chỉ số này chẩn đoán mạnh nhất vì nó **tự chỉ ra chỗ hỏng** |
| Chi phí + token/chapter, ngoại suy 500 chapter | Bộ đếm | Có số thật thay cho ước lượng §7; và xác nhận cap giữ được tuyến tính |
| Độ ổn định | Chạy **3 lần** | Phương sai entity F1 **≤ 0.05** |

**Đọc kết quả**
- **Pass**: Story Bible đứng được ở khoảng cách xa → phần khó nhất của MVP1 đã được kiểm chứng → xây tiếp Layer 2 với gate + eval.
- **Fail ở entity/alias**: "không loạn nhân vật qua hàng trăm chapter" **không đứng được ở quy mô đó** → phải rescope: hoặc giới hạn tác phẩm ngắn (≤30 chapter), hoặc yêu cầu người **soạn bible thủ công** trước. Điều đó **đổi bản chất sản phẩm** từ "AI chuyển truyện của anh thành comic" sang "comic editor có AI hỗ trợ" — vẫn là sản phẩm tốt, nhưng là sản phẩm khác. Biết điều này sau một tuần thay vì sau ba tháng là toàn bộ giá trị của spike.
- **Fail chỉ ở persistence**: chẩn đoán hẹp, sửa được bằng prompt event extraction + schema `permanence`. Không phải tin xấu về kiến trúc.

**Nói thẳng về giới hạn của spike này**: nó **không** kiểm chứng rủi ro #1 (visual identity consistency), vốn là rủi ro có khả năng giết ý tưởng cao nhất và nằm **ngoài lens của em**. Nếu chỉ được chạy **một** thí nghiệm cho **cả dự án**, thì câu trả lời trung thực là **thí nghiệm về image consistency đáng chạy trước** — nó rẻ hơn và nó là điều kiện tiên quyết. Em khuyến nghị chạy **song song** hai spike (một tuần, hai nhánh: bible spike do em mô tả + image consistency spike do lens công nghệ mô tả), và **không** cam kết xây MVP1 trước khi cả hai có số.

#### 9.6. Các giả định về năng lực image model — gom lại để PM đối chiếu chéo với lens khác

Kết luận của em **có phụ thuộc** vào các giả định sau. Em **không** verify được (không có WebSearch, và ngoài phạm vi lens). Nếu giả định nào sai, phần kết luận tương ứng phải xét lại:

| Mã | Giả định | Nếu sai thì đổi kết luận nào |
|---|---|---|
| **IM-A1** | Prompt **chỉ bằng text** không thể tải được character identity một cách đáng tin; identity cần reference-image conditioning hoặc fine-tune per-character | Nền tảng của §7/§8/§16 và của toàn bộ §5 mục compiler hai-output. Nếu **sai** (text đủ) thì compiler đơn giản hơn nhiều và rủi ro #1 giảm mạnh |
| **IM-A2** | Số ràng buộc thị giác được tôn trọng đồng thời trong một prompt là hữu hạn và nhỏ (**ước lượng 5-8**) | Nền tảng của constraint budget + precedence ladder (§5). Nếu trần cao hơn nhiều thì có thể nới, nhưng ladder vẫn cần cho xung đột |
| **IM-A3** | Điều khiển tinh (camera angle cụ thể, mid-action pose, chi tiết nhỏ như vết sẹo, và đặc biệt khẳng định **trái/phải** do hiện tượng lật gương) là **yếu tới không đáng tin** | Nền tảng của phần "field ảo tưởng" (§3.3) và của bảng FP (§4.2, dòng vết sẹo) |
| **IM-A4** | Panel **nhiều nhân vật** giữ đúng 2+ identity trong cùng một ảnh **khó hơn đáng kể** panel một nhân vật | Nền tảng của khuyến nghị "directing thiên vị panel một nhân vật" (§3.1, §5.1) và của scope thu hẹp của checker (§4.4) |
| **IM-A5** | Reproducibility theo seed **chỉ đúng khi ghim model version**; API hosted có thể đổi model âm thầm | Điều kiện hoá tuyên bố reproducibility của §13 |
| **IM-A6** | Consistency của **bối cảnh/địa điểm** khó hơn của nhân vật (ít công cụ identity cho địa điểm hơn) | §10 của tài liệu (Location consistency) có thể khó hơn tác giả nghĩ |
| **IM-A7** | VLM đọc được attribute **thô** (nhóm màu, có/không vật lớn) trên art cách điệu ở mức dùng được, nhưng face-identity trên art cách điệu thì **không** | Nền tảng của toàn bộ §4 (bảng FP/FN và MVP thu hẹp) |

Ngoài ra, hai con số em dùng nhưng **không** verify được và **không** thuộc lens em: **đơn giá image generation** và **đơn giá token 2026** (em giả định ~$2.5/1M in, ~$12/1M out ở §7). Kết luận "chi phí LLM không phải nút thắt" khá vững vì nó cách ngưỡng đau khá xa, nhưng PM nên đối chiếu.

---

## Tài liệu tham khảo

- `docs/999-Resources/Request.md` — nguồn sơ cấp duy nhất, đã đọc toàn văn 894 dòng.
- `docs/010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/brief.md` — mục *Assumptions* (A1: 1 dev, cá nhân, ngân sách tự bỏ).
- `knowledge-base/45-Role-Memory/senior-ai-engineer/000-Core-Memory.md`.

> [!NOTE]
> **Không có nguồn ngoài nào được trích dẫn.** Lens này chạy **không có WebSearch**: mọi nhận định định lượng là **ước lượng engineering nội bộ** kèm giả định nêu tường minh, **không** phải benchmark, paper, hay số liệu thị trường đã verify. Các giả định về năng lực image model được gom ở mục 9.6 (mã `IM-A1`…`IM-A7`) để PM đối chiếu chéo với lens nghiên cứu công nghệ.

---

*Lens: AI/ML Pipeline — Senior AI Engineer. Mọi con số trong tài liệu này là **ước lượng engineering** kèm giả định, không phải benchmark đã verify.*

---

## PM đọc được gì

1. **"Nghịch lý moat" là phát hiện sắc nhất của lens này.** Tài liệu tự tuyên bố Continuity Checker là moat, nhưng đó lại là thành phần **ít được kiểm chứng nhất**. Lập luận vòng tròn mà lens này chỉ ra rất mạnh: check quan trọng nhất (`✓ face`) là check kém khả thi nhất trên art cách điệu, và panel nhiều nhân vật cần **re-identification** — chính bài toán mà checker được lập ra để giải. → Ghép với `researcher` (moat đã public trên arXiv) và lens PM (barrier ≠ moat): **ba lens độc lập cùng bác bỏ luận điểm moat của tài liệu, mỗi lens một lý do khác nhau.** Đây là kết luận trung tâm của deliverable.
2. **Layout Score: bằng chứng tự tố nằm trong chính ví dụ của tài liệu.** `dialogue density 0.20` là đại lượng **code đếm chính xác được** (số ký tự thoại / diện tích panel) mà lại giao cho LLM đoán. Cộng với việc không có hàm tổng hợp nào được định nghĩa cho 5 con số → nếu để LLM gộp luôn thì 5 số chỉ là **biện minh hậu nghiệm** cho quyết định LLM đã đưa ra. Ghép với `researcher` (⚪ không tìm được prior art nào cho Layout Score) → **M7 ở `researcher.md` được phân định: đây là phần "chưa ai làm vì không đáng", không phải phần "thật sự mới".**
3. **Mâu thuẫn nội tại §13 vs §16 mà không lens nào khác thấy**: §13 dựng bảng `Generation` để bảo đảm reproducibility, nhưng nếu có LLM trong đường compile runtime thì cùng một panel spec sẽ ra prompt khác vào ngày mai. **Hai mục không thể cùng đúng.** Đây là loại mâu thuẫn chỉ phát hiện được khi đọc cả hai mục cạnh nhau — giá trị của việc có lens chuyên biệt.
4. **Ranh buộc "phút-người, không phải đô-la"**: 5 phút/chapter × 100 chapter ≈ 8 giờ chỉ riêng HITL gate. Hội tụ lần thứ ba với `architect` và `researcher`. → Deliverable phải nêu: **đơn vị đo chi phí đúng của dự án này là giờ-người, không phải đô-la.**
5. **Lens này trung thực về giới hạn của chính nó** — nó nói thẳng rằng spike nó đề xuất *không* kiểm chứng rủi ro số một (visual consistency nằm ngoài lens), và khuyến nghị chạy song song hai nhánh. Đây là hành vi đúng của một lens trong fan-out, và PM ghi nhận.

## Mâu thuẫn với lens khác

| # | Mâu thuẫn | PM phân xử |
|---|---|---|
| **M8** ⭐ | **Mâu thuẫn thật duy nhất của cả run.** `senior-ai-engineer`: Continuity Checker ở dạng hiện tại tạo **giá trị âm** do false positive cao, và `[Fix automatically]` là nút hứa hẹn quá mức. `researcher`: continuity check bằng VLM là ✅ **"Đã giải được"** — ContinuityEval dùng trong CANVAS, MIE đạt **0.922 pairwise accuracy** vs human preference. | **Cả hai đều đúng, vì hai bên đang nói về HAI TASK KHÁC NHAU.** MIE/ContinuityEval được validate ở task **pairwise ranking** — "trong hai ứng viên này, cái nào consistent hơn". `senior-ai-engineer` phản biện task **absolute per-panel detection** — "panel này sai hay đúng, có/không". Một VLM có thể rất tốt ở so sánh tương đối mà vẫn tệ ở ngưỡng tuyệt đối; đó là khác biệt đã biết, không phải nghịch lý. <br><br>**Bằng chứng phân xử nằm trong chính CANVAS**: nó dùng VLM để **select giữa N candidate** (`QA-based selection`), **không** dùng làm checker gắn nhãn lỗi rồi autofix. Tức là paper mà `researcher` dẫn ra để nói "đã giải được" thật ra đang dùng cơ chế mà `senior-ai-engineer` mới là người mô tả đúng. <br><br>**→ Phân xử: bỏ Continuity Checker dạng "flag lỗi + [Fix automatically]" (theo `senior-ai-engineer`). Thay bằng "generate N candidate → VLM chọn cái consistent nhất" (theo CANVAS/`researcher`).** Cùng công nghệ, cùng chi phí, khác hoàn toàn về tính khả thi — vì nó không bao giờ phải trả lời "đúng hay sai", chỉ phải trả lời "cái nào hơn". Đây là **kết luận tổng hợp có giá trị nhất của run**, và không lens nào tự đến được nó. |
| **M9** | `senior-ai-engineer` xếp props/vũ khí là điểm yếu suy luận từ nguyên lý. | ✅ **`researcher` xác nhận bằng số**: CANVAS Props chỉ **4.19/5**, thấp nhất trong 4 metric, cải thiện so baseline chỉ **+2,5%** (so với character +11,8%). → Ví dụ `✗ sword missing` ở §15 không phải lo hão mà là **lỗi hệ thống đã đo được**. |
| **M10** | `senior-ai-engineer` lo multi-character panel về mặt re-identification. | ✅ **`researcher` xác nhận bằng số và làm gắt hơn**: CogCanvas ID-Sim 42.33 (2 người) → 27.21 (3) → **2.67 (4) → 0.52 (5)**; attribute binding *"near-complete failure beyond three subjects"*. → Sinh ra ràng buộc thiết kế cứng: **≤3 nhân vật/panel trong Comic IR**. |
| **M11** | `IM-A1`…`IM-A7` — 7 giả định về năng lực image model. | Phần lớn được `researcher` trả lời: multi-ref native là hướng đúng, 1 nhân vật/panel đạt 4.91/5 (đủ xuất bản), 2–3 nhân vật cần verify từng panel, 4+ chưa giải được, props yếu nhất, location tốt bất ngờ (4.88/5 cả consecutive và non-consecutive). Deliverable sẽ đối chiếu chi tiết ở mục *Bảng khả thi*. Khoảng trống `researcher` không lấp được: **không có benchmark độc lập nào đo frontier model ở 2–3 nhân vật** — đây chính là thứ MVP0 phải tự đo. |
| **M12** | `senior-ai-engineer`: nếu chỉ chạy được một thí nghiệm, **image consistency spike nên chạy trước** Story Bible spike. | ✅ Hội tụ với `architect` và lens PM. Lần thứ ba trong run. → **MVP0 = image consistency spike**; Story Bible spike chạy song song nếu có sức, nhưng không phải điều kiện tiên quyết. |
