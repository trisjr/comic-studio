# Findings — Lens KIẾN TRÚC & DATA MODEL (`Request.md`)

## Table of Contents

1. [Phạm vi & giả định của lens](#phạm-vi--giả-định-của-lens)
2. [Kết luận của worker](#kết-luận-của-worker)
   - [1. Quyết định kiến trúc cốt lõi — đúng hay sai?](#1-quyết-định-kiến-trúc-cốt-lõi--đúng-hay-sai)
   - [2. Temporal state modeling — điểm khó nhất về data](#2-temporal-state-modeling--điểm-khó-nhất-về-data)
   - [3. `Generation` entity và reproducibility](#3-generation-entity-và-reproducibility)
   - [4. Backend architecture §12 — microservices có đúng không?](#4-backend-architecture-12--microservices-có-đúng-không)
   - [5. §14 UI — Web Editor kiểu "Figma + comic editor + AI director"](#5-14-ui--web-editor-kiểu-figma--comic-editor--ai-director)
   - [6. Visual Prompt Compiler §16 dưới góc compiler design](#6-visual-prompt-compiler-16-dưới-góc-compiler-design)
   - [7. Thứ tự 4 MVP milestone §18](#7-thứ-tự-4-mvp-milestone-18)
   - [8. Cái gì THIẾU hẳn trong tài liệu](#8-cái-gì-thiếu-hẳn-trong-tài-liệu)
   - [9. Kết luận kiến trúc](#9-kết-luận-kiến-trúc)
3. [Tài liệu tham khảo](#tài-liệu-tham-khảo)

## Phạm vi & giả định của lens

Lens này chỉ thẩm định **kiến trúc hệ thống và data model**. Không đánh giá thị trường/đối thủ, không đánh giá năng lực của model image generation cụ thể — hai lens kia làm.

Giả định vận hành (từ `brief.md` §Assumptions, A1/A2): **1 dev duy nhất, dự án cá nhân, greenfield tuyệt đối, ngân sách tự bỏ**. Mọi khuyến nghị về scope và infrastructure dưới đây đều **treo vào giả định này**; nếu A1 sai (có team + funding) thì phần §4 và §9 phải đọc lại.

**Giả định công nghệ cần lens AI/ML xác nhận chéo (đánh dấu rõ để PM đối chiếu):**

- **GĐ-1**: Character consistency đạt được chủ yếu bằng **reference-image conditioning** (đưa ảnh nhân vật vào input), không phải bằng fine-tune per-character. Nếu thực tế bắt buộc fine-tune/LoRA từng nhân vật thì §3 và §6 đổi bản chất (mỗi character trở thành một model artifact có version, chi phí và pipeline train khác hoàn toàn).
- **GĐ-2**: Image model dùng qua **closed API**, không tự host. Kéo theo: không set được seed một cách đảm bảo, model có thể đổi âm thầm phía provider. Cả §1 và §3 phụ thuộc điểm này.
- **GĐ-3**: Image model **không** render được text tiếng Việt có dấu ở chất lượng xuất bản. Kéo theo §8 (speech bubble phải composite ngoài model). Nếu GĐ-3 sai thì mục đó nhẹ đi, nhưng em đánh giá xác suất sai là thấp.

---

## Kết luận của worker

### 1. Quyết định kiến trúc cốt lõi — đúng hay sai?

**Đúng, và đây là điểm mạnh nhất của toàn bộ tài liệu.** Nếu chỉ giữ được một quyết định trong `Request.md` thì giữ cái này.

**Tương đương pattern nào:**

| Góc nhìn | Pattern tương đương |
|---|---|
| Build system | **Source vs. build artifact.** Spec = source code, ảnh = compiled binary. Story Bible + Panel Spec là thứ đi vào version control; ảnh là `dist/`. |
| CQRS / Read model | Spec = **write model** (source of truth), ảnh = **materialized view / projection** có thể rebuild. |
| Data engineering | **Declarative desired-state + reconciliation** (kiểu Terraform/Kubernetes): spec khai báo "panel này phải trông thế nào", generator là reconciler đưa thực tế về gần desired state, Continuity Checker (§15) chính là **drift detection**. |
| Rendering | Ảnh là **cache có key** = hash(panel spec + resolved refs + style + model config). Cache invalidation khi spec đổi. |

**Vì sao đúng:** nó tách được thứ **đắt để tạo ra và không thể tái tạo** (hiểu truyện: quan hệ nhân vật, timeline, ý nghĩa cảnh) khỏi thứ **rẻ và thay thế được** (một lần gọi image model). Đổi model, đổi style, xuất sang video — chỉ phải re-render, không phải re-analyze. Với truyện hàng trăm chapter thì đây là khác biệt giữa "làm được" và "không làm được".

**Cái giá phải trả — chỗ sẽ đau:**

1. **Chi phí authoring spec.** Panel spec §6 có 12 trường. Một chapter ~ 30-60 panel. Nếu LLM extract sai, user phải sửa spec (nhiều field) chứ không phải sửa ảnh (một hành động). Spec càng giàu, cost sửa càng cao. → Phải có **default/inherit**: panel kế thừa scene (location, time, lighting), scene kế thừa chapter. Chỉ lưu **delta**, không lưu full 12 field mỗi panel.
2. **Write amplification khi spec đổi ở tầng cao.** Sửa `Costume v4` của Lâm Phong ở Chapter 12 → invalidate toàn bộ panel từ Ch12 trở đi có nhân vật đó. Với 100 chapter đây là hàng nghìn panel bị đánh dấu stale. → Cần **stale flag, không auto-regenerate**: đánh dấu `is_stale = true` + hiển thị "N panel lệch spec", để user quyết định regenerate lô nào. Auto-regenerate = đốt tiền không kiểm soát.
3. **Spec drift không quan sát được.** Nói "ảnh là output của spec" chỉ đúng nếu có cách **đo** ảnh có khớp spec hay không. Đó là lý do §15 Continuity Checker **không phải feature phụ mà là điều kiện để §1 đứng được**. Nếu Continuity Checker không đủ chính xác, "ảnh = f(spec)" trở thành một niềm tin chứ không phải một invariant.

**Trường hợp nó phản tác dụng (quan trọng, tài liệu không nói):**

- **Ảnh KHÔNG phải cache khi dùng closed API (GĐ-2).** Cache có định nghĩa: mất rồi tái tạo lại được y hệt. Với API không lộ seed và model đổi âm thầm, một ảnh đã generate là **artifact độc bản** — xóa là mất vĩnh viễn. → Sửa mô hình tư duy: ảnh là **immutable artifact có provenance**, không phải cache. Hệ quả kỹ thuật: **không bao giờ xóa ảnh đã approved** để "tiết kiệm storage vì regenerate được"; ảnh approved phải pin cứng vào panel (`approved_generation_id`), và lifecycle policy chỉ được xóa ảnh **rejected/orphan**.
- **Khi user retouch tay.** Người dùng inpaint sửa bàn tay, sửa màu mắt, vẽ thêm chi tiết. Ảnh đó **không còn là hàm của spec** — nó là source mới. Nếu kiến trúc không dự tính, lần regenerate kế tiếp sẽ xóa mất công sức thủ công. → Cần `generation.origin ENUM('ai','ai_edited','human')` và luật: `origin != 'ai'` thì **cấm auto-regenerate**, chỉ regenerate khi user xác nhận rõ ràng.
- **Khi kết quả đẹp ngoài ý spec.** Model trả về một panel hay hơn spec mô tả. Luồng đúng phải là **spec learns back from output** (cập nhật spec theo ảnh đã chọn) — nếu không, spec và ảnh phân kỳ và Continuity Checker sẽ báo false positive triền miên. Đây là edge case tài liệu bỏ qua hoàn toàn.

---

### 2. Temporal state modeling — điểm khó nhất về data

#### 2.1 Nó là pattern gì?

**Không phải event sourcing.** Event sourcing yêu cầu state = fold(events) và không lưu state, mọi truy vấn phải replay. Ở đây `Event` là **thực thể miêu tả của truyện** (một cảnh xảy ra), không phải một command đã commit. Đừng đi hướng fold-replay: nó bắt phải replay từ chapter 1 cho mọi truy vấn, và `Event` do LLM extract nên không đáng tin đủ để làm log bất khả xâm phạm.

**Không phải bitemporal.** Bitemporal cần hai trục: valid time + transaction time. Hệ này có **hai trục nhưng khác**: thời gian *trong truyện* (narrative) và thứ tự *đọc* (reading order). Đó là bài toán **narrative time**, không phải audit time. (Transaction time có thể cần cho versioning Story Bible — xem §8 — nhưng đó là chuyện khác.)

**Gần nhất: SCD Type 2 trên trục narrative time** — mỗi state row có khoảng hiệu lực `[valid_from, valid_to)` trên trục thứ tự truyện, cộng thêm một nét **temporal snapshot table** (as-of query). Đây là pattern đã được giải triệt để trong data warehousing; không cần phát minh gì mới.

**Đây là hạt nhân kỹ thuật của cả sản phẩm.** §2, §3, §9, §13 đều đang mô tả cùng một thứ bằng bốn từ vựng khác nhau (`Character.timeline`, `Event.character_state`, `Appearance @ Chapter`, `CharacterState`) — **đó là một mùi thiết kế**: chưa chốt được một mô hình duy nhất. Việc phải làm trước khi code: **hợp nhất bốn cái này thành một**.

#### 2.2 Schema cụ thể cho truy vấn "state của X tại Chapter 17 / Scene 4"

Nguyên tắc: **anchor state vào `Event` (mức scene), không vào chapter**; đưa một khóa sắp xếp số học duy nhất (`story_order`) xuống thẳng bảng state để index dùng được.

```sql
-- Trục thời gian truyện. Một project có thể có nhiều timeline (tuyến song song).
CREATE TABLE timeline (
    id            UUID PRIMARY KEY,
    project_id    UUID NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    name          TEXT NOT NULL,              -- 'main', 'flashback-15-nam-truoc', 'tuyen-cong-chua'
    kind          TEXT NOT NULL,              -- 'main' | 'flashback' | 'parallel' | 'dream'
    parent_id     UUID REFERENCES timeline(id),
    -- story_order trên timeline cha mà nhánh này gắn vào (để merge khi cần view toàn cục)
    anchor_order  NUMERIC(20,6),
    UNIQUE (project_id, name)
);

-- Event = một scene trong truyện. Đơn vị neo state.
CREATE TABLE event (
    id            UUID PRIMARY KEY,
    project_id    UUID NOT NULL REFERENCES project(id) ON DELETE CASCADE,
    timeline_id   UUID NOT NULL REFERENCES timeline(id),
    chapter_no    INT  NOT NULL,              -- vị trí VĂN BẢN
    scene_no      INT  NOT NULL,
    beat_no       INT  NOT NULL DEFAULT 0,    -- chia nhỏ trong scene (xem 2.4)
    -- reading_order: thứ tự người đọc gặp. Suy ra được, denormalize để sort nhanh.
    reading_order NUMERIC(20,6) NOT NULL,
    -- story_order: thứ tự SỰ VIỆC XẢY RA trong thế giới truyện. Trục thật của state.
    -- NUMERIC + sparse (bước nhảy 1000) để chèn giữa không phải renumber.
    story_order   NUMERIC(20,6) NOT NULL,
    story_time    TEXT,                       -- 'Night', 'Day 3 sau đại chiến' — mô tả, không dùng để sort
    location_id   UUID REFERENCES location(id),
    summary       TEXT,
    UNIQUE (project_id, timeline_id, chapter_no, scene_no, beat_no)
);
CREATE INDEX idx_event_story   ON event (project_id, timeline_id, story_order);
CREATE INDEX idx_event_reading ON event (project_id, reading_order);

-- State của nhân vật. SCD-2 rút gọn: chỉ lưu khi CÓ THAY ĐỔI (sparse), không lưu mỗi event.
CREATE TABLE character_state (
    id            UUID PRIMARY KEY,
    character_id  UUID NOT NULL REFERENCES character(id) ON DELETE CASCADE,
    event_id      UUID NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    timeline_id   UUID NOT NULL REFERENCES timeline(id),   -- denormalize từ event
    story_order   NUMERIC(20,6) NOT NULL,                  -- denormalize từ event: BẮT BUỘC
    -- delta hay full? -> lưu FULL snapshot của các field đã biết tại mốc này.
    -- Lý do: as-of query thành 1 row lookup, không phải merge N delta.
    costume_id    UUID REFERENCES costume(id),
    hair_variant  TEXT,
    weapon_id     UUID REFERENCES item(id),
    emotion       TEXT,
    injuries      JSONB NOT NULL DEFAULT '[]',   -- ['scar_left_eye','wound_shoulder']
    accessories   JSONB NOT NULL DEFAULT '[]',
    extra         JSONB NOT NULL DEFAULT '{}',   -- field chưa dự tính, tránh migration liên tục
    source        TEXT NOT NULL DEFAULT 'ai',    -- 'ai' | 'human' | 'ai_confirmed'
    confidence    REAL,
    schema_version INT NOT NULL DEFAULT 1,
    UNIQUE (character_id, event_id)
);
-- INDEX QUYẾT ĐỊNH: trả lời as-of query bằng 1 index scan lùi + LIMIT 1
CREATE INDEX idx_charstate_asof
    ON character_state (character_id, timeline_id, story_order DESC);
```

**Truy vấn cốt lõi** — "Lâm Phong mặc gì tại Chapter 17 / Scene 4":

```sql
WITH target AS (
    SELECT timeline_id, story_order
    FROM   event
    WHERE  project_id = :project AND chapter_no = 17 AND scene_no = 4
    ORDER  BY beat_no LIMIT 1
)
SELECT cs.*
FROM   character_state cs, target t
WHERE  cs.character_id = :lam_phong
  AND  cs.timeline_id  = t.timeline_id
  AND  cs.story_order <= t.story_order
ORDER  BY cs.story_order DESC
LIMIT  1;
```

Đây là **backward index scan + LIMIT 1**, độ phức tạp O(log n) bất kể truyện dài bao nhiêu. Không replay, không aggregate. `LocationState` và `ItemState` dùng đúng khuôn này (`(location_id, timeline_id, story_order DESC)`).

**Relationship state** cần bảng riêng vì khóa là một **cặp**:

```sql
CREATE TABLE relationship_state (
    id           UUID PRIMARY KEY,
    from_char_id UUID NOT NULL REFERENCES character(id) ON DELETE CASCADE,
    to_char_id   UUID NOT NULL REFERENCES character(id) ON DELETE CASCADE,
    event_id     UUID NOT NULL REFERENCES event(id) ON DELETE CASCADE,
    timeline_id  UUID NOT NULL REFERENCES timeline(id),
    story_order  NUMERIC(20,6) NOT NULL,
    kind         TEXT,        -- 'ally' | 'enemy' | 'lover' | 'master-disciple'
    trust        REAL,        -- -1.0 .. 1.0
    known_facts  JSONB NOT NULL DEFAULT '[]',  -- 'biet-Lam-Phong-la-hoang-tu'
    UNIQUE (from_char_id, to_char_id, event_id)
);
CREATE INDEX idx_relstate_asof
    ON relationship_state (from_char_id, to_char_id, timeline_id, story_order DESC);
```

`known_facts` là thứ tài liệu chưa có nhưng cực quan trọng cho comic: **ai biết gì tại thời điểm nào** quyết định biểu cảm và cách vẽ (nhân vật chưa biết sự thật thì không được vẽ mặt phản ứng như đã biết).

**Hợp nhất §9 (Identity/Appearance) vào schema trên:** `character` = Identity (bất biến: `face_ref_id`, `body_proportions`, `age_baseline`, `personality`); `character_state` = Appearance (biến thiên). §9 **đúng về mặt phân tách** nhưng phải hiểu Identity là "bất biến trong phạm vi một timeline" — truyện có time-skip 10 năm hoặc nhân vật lúc nhỏ/lúc lớn thì face cũng đổi. → Bổ sung `character_identity_variant(character_id, variant_name, valid_from_story_order, face_ref_id, body_ref_id)`, ví dụ `lam_phong@child`, `lam_phong@adult`. Không có cái này, truyện dài nào có hồi ức tuổi thơ là vỡ.

#### 2.3 Vấn đề thứ tự: `(chapter, scene)` KHÔNG đủ — đây là lỗ hổng thiết kế thật

Tài liệu dùng `(chapter, scene)` làm khóa thời gian (§3: `Event #102 / Chapter: 17 / Scene: 4`). Đó là **thứ tự đọc** (syuzhet), không phải **thứ tự sự việc** (fabula). Với truyện tuyến tính hai cái trùng nhau nên lỗi bị che. Với flashback thì sai:

Chapter 20 kể hồi ức 15 năm trước. Với khóa `(chapter, scene)`, Event ở Ch20 có thứ tự **lớn hơn** Ch19 → query "state tại Ch20" trả về costume của hiện tại, trong khi cảnh đó phải là Lâm Phong lúc 9 tuổi. Ngược lại, sau khi xử lý Ch20, mọi query "state gần nhất" cho Ch21 sẽ vô tình lấy state của **quá khứ** vì nó là row mới nhất theo `(chapter, scene)`. **Cả hai chiều đều sai** — đây là bug loại corrupt dữ liệu âm thầm, không phải crash, nên sẽ phát hiện muộn và rất đắt.

Flashback/hồi tưởng/song tuyến là **cực kỳ phổ biến** trong truyện dài — coi đây là trường hợp thường, không phải edge case.

**Cách vá (đã nằm trong schema §2.2):**

1. **Hai trục tách bạch**: `reading_order` (dùng để render page theo thứ tự đọc) và `story_order` (dùng cho **mọi** as-of state query). Trộn hai cái là nguồn của toàn bộ lớp bug này.
2. **`timeline_id`**: mỗi tuyến song song / mỗi flashback lớn là một `timeline` row có `kind` và `anchor_order`. State query luôn scope theo `timeline_id`. Nhánh flashback kế thừa state từ timeline cha tại `anchor_order` — resolver fallback hai bước: tìm trong timeline hiện tại trước, không có thì tìm trong timeline cha với `story_order <= anchor_order`.
3. **`story_order` là `NUMERIC` sparse, không phải `INT` tuần tự.** Cấp phát bước nhảy 1000. LLM extract sai thứ tự là chắc chắn xảy ra; user sẽ phải chèn/kéo lại — với NUMERIC thì chèn giữa là một UPDATE một row (`(a+b)/2`), với INT là renumber cả bảng. Kèm một job renormalize offline khi khoảng cách quá nhỏ.
4. **`story_order` phải là editable, có UI.** Không có công cụ nào tự suy ra thứ tự fabula đáng tin. Chấp nhận: LLM đề xuất, người xác nhận. Tối thiểu là một danh sách kéo-thả ở mức scene.
5. **Guard bắt buộc**: mọi query state phải đi qua **một** hàm/repository duy nhất `resolveState(entity, at_event)`. Nếu để mỗi chỗ tự viết SQL, sẽ có chỗ dùng `chapter_no` và bug quay lại. Đây là guardrail nên viết thành test: "không được có `ORDER BY chapter_no` trong bất kỳ đường dẫn resolve state nào".

**Nếu không vá**: hệ thống vẽ sai trang phục/vết thương/vũ khí ở mọi cảnh hồi tưởng, và Continuity Checker sẽ "sửa" theo state sai — tức là tự động làm hỏng đúng những panel đang đúng. Đây là rủi ro nghiêm trọng nhất về data model trong cả tài liệu.

#### 2.4 Granularity: `Appearance @ Chapter 12` (§9) là SAI mức

Chapter là quá thô. Ví dụ thường gặp: nhân vật vào chapter mặc thường phục → bị tấn công → đổi sang áo giáp → cuối chapter áo giáp hỏng. Ba state trong một chapter. Neo theo chapter thì mất hai.

**Granularity đúng: neo vào `Event` (mức scene), và cho phép chia nhỏ hơn scene bằng `beat_no`** khi state đổi giữa scene (đúng lúc rút kiếm, đúng lúc bị thương). Panel trỏ tới `event_id`, nên state resolve tới đúng panel mà không cần bảng state riêng cho panel.

Ba luật kèm theo:

- **Sparse, không dense**: chỉ insert `character_state` khi có thay đổi. Truyện 100 chapter × 50 scene × 30 nhân vật = 150k row nếu dense; sparse thì thực tế chỉ vài nghìn. Trade-off: query cần `story_order <= X ... LIMIT 1` thay vì equality — đã tính trong index.
- **Full snapshot của field đã biết, không lưu delta**: as-of thành 1 row lookup. Nếu lưu delta phải merge N row → chậm và logic phức tạp. Đổi lấy chút dư thừa dữ liệu, xứng đáng.
- **Panel là nơi override cuối**: `comic_panel.state_override JSONB` cho trường hợp director muốn lệch spec cố ý (ví dụ close-up chỉ thấy mặt, costume không liên quan). Không có override thì user sẽ đi sửa `character_state` để hack một panel → làm bẩn Story Bible.

---

### 3. `Generation` entity và reproducibility

#### 3.1 Bộ field §13 chưa đủ để reproduce

Thiếu, theo thứ tự quan trọng:

| Nhóm | Field thiếu | Vì sao chặn reproducibility |
|---|---|---|
| Sampling | `sampler` / `scheduler`, `steps`, `cfg_scale`, `denoise_strength` (nếu img2img) | Cùng prompt + seed nhưng khác sampler/steps là ra ảnh khác. Không có thì `seed` vô nghĩa. |
| Hình học | `width`, `height`, `aspect_ratio` | Aspect ảnh hưởng composition rất mạnh; panel comic đủ loại tỉ lệ. Không lưu thì không tái tạo được layout. |
| Prompt | `negative_prompt`, `prompt_template_version` | Negative prompt là nửa còn lại của prompt. `prompt_template_version` để biết Visual Prompt Compiler bản nào sinh ra chuỗi này — thiếu nó thì không phân biệt được "model đổi" với "compiler của mình đổi". |
| Reference | **`content_hash` của TỪNG ref image** (SHA-256) + **thứ tự ref (`ordinal`)** + `weight/strength` mỗi ref | `character_refs: [id]` chỉ trỏ tới ID; file phía sau ID có thể bị thay. Thứ tự ref có ý nghĩa với nhiều API (ref đầu ảnh hưởng mạnh hơn). Không có hash + ordinal thì "cùng input" là không kiểm chứng được. |
| Toàn vẹn | `request_payload JSONB` (payload thô gửi provider) + `response_metadata JSONB` | Đây là **cứu cánh**: mọi field chưa dự tính đều nằm trong payload thô. Đơn giản, rẻ, và là thứ duy nhất chắc chắn đủ. Nếu chỉ thêm được một field, thêm cái này. |
| Nguồn gốc | `provider`, `provider_request_id`, `api_version`, `created_at`, `origin ENUM('ai','ai_edited','human')` | `provider_request_id` để đối chiếu/khiếu nại với provider. `origin` chặn auto-regenerate lên ảnh user đã sửa tay (xem §1). |
| Chi phí | `cost_usd`, `latency_ms`, `token/credit_used` | Không lưu thì không có cách nào xây budget cap (§8). Phải lưu **từ generation đầu tiên**, thêm sau là mất dữ liệu lịch sử. |
| Kết quả | `status` + `failure_reason`, `output_image_hash`, `qc_score` | `status` đã có nhưng thiếu lý do fail → không phân loại được lỗi transient vs. permanent để retry đúng (xem §8). |

Bổ sung cấu trúc: tách `generation_reference(generation_id, ref_kind, reference_image_id, content_hash, ordinal, weight)` thành bảng riêng thay vì nhồi vào ba mảng `character_refs / style_refs / location_refs`. Lý do: cần query ngược "ảnh reference này đã được dùng ở những generation nào" khi thay reference sheet — không có bảng này thì phải scan JSONB.

#### 3.2 `parent_generation` — cây đó để làm gì?

Đọc kỹ thì `parent_generation` đang gánh **ba** ngữ nghĩa khác nhau bị gộp làm một:

1. **Retry/variation**: cùng spec, generate lại (seed khác) → sibling.
2. **Refinement**: img2img/inpaint từ output của generation trước → thật sự là parent-child.
3. **Continuity fix**: regenerate sau khi Continuity Checker báo lỗi, có thêm constraint.

Gộp ba loại vào một FK sẽ làm mọi câu hỏi sau này khó trả lời. → Thêm `relation_kind ENUM('retry','variation','refine','continuity_fix')` bên cạnh FK. Một cột enum, gần như miễn phí.

**Ai đọc cây:** (a) user, để so sánh các phương án và quay lại bản trước — nhưng cái này thực tế chỉ cần **một danh sách phẳng các generation của panel, sort theo thời gian**, không cần cây; (b) chính em/dev, để debug "tại sao panel này sai" — cần lineage; (c) cost analysis "panel nào đốt nhiều lượt nhất".

**Over-engineering ở MVP?** — **Cột `parent_generation_id` (nullable FK): giữ, không phải over-engineering** (một cột, thêm sau thì mất dữ liệu quá khứ). **UI duyệt cây: bỏ**. Ở MVP, hiển thị flat list theo `created_at` + `approved_generation_id` trên panel là đủ 95% giá trị. Đừng build tree view, diff view, branch/merge — đó là nơi effort bốc hơi.

#### 3.3 Closed API vs. self-host — và `seed` còn nghĩa gì?

Nói thẳng: **với closed API (GĐ-2), reproducibility đúng nghĩa là không đạt được.** Lý do cộng dồn: (a) nhiều API không cho set seed; (b) cho set seed vẫn không đảm bảo bit-exact vì batching/hardware/precision phía server; (c) provider cập nhật weights dưới cùng một tên model (**silent model drift**) — cùng payload, khác thời điểm, khác ảnh; (d) model có thể **bị khai tử**, lúc đó không còn gì để reproduce.

Self-host: reproducibility đạt gần tuyệt đối nếu pin weights hash + sampler + library version + hardware. Nhưng đổi lấy chi phí GPU và effort vận hành mà 1 dev khó gánh (khuyến nghị về self-host thuộc lens AI/ML — em chỉ nêu hệ quả kiến trúc).

**Vậy `seed` để làm gì?** Reframe — đây là điểm em không đồng ý với cách tài liệu diễn đạt ("Cái này giúp reproducibility"):

- `seed` là **provenance metadata**, không phải replay key. Giá trị thật của nó: (i) trong một session ngắn, cùng model, seed **thường** cho kết quả gần giống → dùng để **giữ nhất quán giữa các panel cùng scene** và để "thay đổi một tham số, giữ nguyên phần còn lại"; (ii) làm bằng chứng khi debug/khiếu nại.
- Do đó **mục tiêu đúng của `Generation` không phải reproducibility mà là AUDITABILITY + LINEAGE**: trả lời được "ảnh này sinh ra từ spec nào, ref nào (hash gì), tham số gì, tốn bao nhiêu, ai approve". Cái đó **đạt được 100%** và đủ để chạy sản phẩm.
- Hệ quả kiến trúc bắt buộc, tài liệu chưa nói: **ảnh đã approved là bất biến và không được xóa** (§1). Đừng thiết kế dựa trên giả định "cần thì regenerate lại".
- Nên thêm `is_reproducible BOOLEAN` (suy ra từ provider capability) để hệ thống **tự biết** ảnh nào tái tạo được, ảnh nào không — trước khi đề nghị user regenerate một panel không thể lấy lại.

---

### 4. Backend architecture §12 — microservices có đúng không?

#### 4.1 Verdict: over-engineering, rõ ràng

Với **1 dev, greenfield, ngân sách tự bỏ** (A1/A2): 3 service + 2 PostgreSQL riêng + Vector DB riêng + Job Queue riêng là **over-engineering nghiêm trọng**. Nói thẳng các chi phí nó tạo ra mà không đổi lấy gì:

- **Hai database = mất transaction.** Story ở DB1, Comic ở DB2, nhưng panel phải tham chiếu `character_id` và `event_id` — cross-DB thì **không có foreign key, không có join, không có ACID**. Hệ quả: phải tự viết eventual consistency, saga, reconciliation. Đây chính là **thứ dữ liệu ràng buộc chặt nhất của hệ** (panel spec resolve state từ Story Bible ở mọi lần render) bị cắt làm hai. Sai chỗ chí tử.
- **3 service = 3 lần deploy, 3 lần log, 3 lần config, N lần debug distributed.** Với 1 dev, mỗi feature nhỏ thành một cuộc di chuyển qua nhiều repo/process.
- **Không có lý do vận hành nào biện minh.** Microservices trả cho hai thứ: (a) scale độc lập, (b) team độc lập. (b) không tồn tại (1 dev). (a) thì workload thật là **1 user, nhiều job dài** — bottleneck là quota/GPU phía provider, không phải CPU service của mình. Tách service không giải quyết bottleneck đó.

Ước lượng của em: đi theo §12 nguyên bản làm chậm thời gian tới sản phẩm chạy được khoảng **2-3 lần** so với monolith, phần lớn effort tan vào plumbing.

#### 4.2 Kiến trúc thay thế cho MVP

**Modular monolith, một process, một database.**

```text
┌──────────────────────────────────────────────┐
│  comic-studio (một app, một deploy)          │
│                                              │
│  modules/                                    │
│    story/       -- import, parse, Bible,     │
│                    timeline, state resolver  │
│    comic/       -- scene→page→panel, layout  │
│    visual/      -- Visual Prompt Compiler    │
│                    (library, KHÔNG service)  │
│    generation/  -- job enqueue + adapter     │
│                    per provider              │
│    continuity/  -- checker (report-only)     │
│    export/      -- composite + PDF/CBZ       │
│                                              │
│  Giao tiếp giữa module: gọi hàm qua           │
│  interface tường minh. KHÔNG HTTP nội bộ.    │
└────────────┬─────────────────────────────────┘
             │
   ┌─────────▼─────────┐      ┌──────────────────┐
   │ PostgreSQL (1)    │      │ Object Storage   │
   │ + pgvector        │      │ (S3/R2)          │
   │ + job queue table │      │ ảnh, refs, novel │
   │ schema: story,    │      └──────────────────┘
   │  comic, gen       │
   └───────────────────┘
```

| Hạng mục | §12 đề xuất | Khuyến nghị MVP | Vì sao |
|---|---|---|---|
| Service | 3 service tách rời | **1 process, module boundary bằng package + interface** | Giữ được ranh giới logic mà không trả giá distributed. Tách sau chỉ cần đổi lớp gọi hàm thành RPC. |
| Database | 2 PostgreSQL | **1 PostgreSQL, 3 schema** (`story`, `comic`, `generation`) | Giữ FK/join/transaction. Schema tách sẵn để sau này split ra DB riêng bằng dump-restore. |
| Vector DB | Vector DB riêng | **`pgvector` trong cùng Postgres. Hoặc HOÃN HẲN.** | Xem 4.3. |
| Job Queue | queue riêng (Redis/SQS/...) | **Queue nằm trong Postgres** (lớp `pg-boss` / Graphile Worker / hoặc bảng `job` + `SELECT ... FOR UPDATE SKIP LOCKED`) | Không thêm một hệ tồn trạng thái nữa. Được **transactional enqueue**: `INSERT generation` + `INSERT job` trong **một** transaction → không bao giờ có job mồ côi hay generation không có job. Đây là lợi thế kỹ thuật thật, không chỉ là tiết kiệm. |
| Object Storage | có | **Giữ nguyên, làm từ ngày đầu** | Xem 4.4. |
| WebSocket | có | **Hoãn. Dùng polling** (`GET /jobs?ids=...` mỗi 2s) | Generation mất hàng chục giây; polling 2s là quá đủ UX. WebSocket + reconnect + state sync là hạng mục lớn, đổi lấy gần như không có gì ở giai đoạn này. |

#### 4.3 Vector DB dùng để làm gì trong hệ này, và thay bằng gì?

Tài liệu vẽ Vector DB dưới Story Service nhưng **không nói nó làm gì**. Các mục đích hợp lý em thấy được:

1. **Semantic retrieval trên văn bản truyện**: khi phân tích Chapter 40, cần bối cảnh liên quan từ 39 chapter trước mà không nhồi hết vào context — retrieve các đoạn liên quan tới nhân vật/địa điểm đang xét (RAG). **Đây là use case chính đáng nhất.**
2. **Entity resolution / dedup**: "Phong", "Lâm Phong", "hắn", "vị công tử áo xanh" là một người → so khớp bằng embedding.
3. **Visual similarity search** trên ảnh đã generate (tìm panel giống, phát hiện lệch style). Đây là **image embedding**, khác hoàn toàn text embedding — đừng gộp.

Thay bằng gì rẻ hơn:

- **Với (1) và (2): `pgvector` là đủ tuyệt đối** ở quy mô này. Ước lượng: 100 chapter × ~3000 từ → cỡ 20-50k chunk. Đó là quy mô nhỏ với pgvector + HNSW index. Không cần hệ riêng.
- **Còn rẻ hơn nữa cho MVP: chưa cần vector gì cả.** Story Bible **là** index của mình — nhân vật, địa điểm, event đều có ID và quan hệ tường minh trong SQL. Truy vấn "mọi event có Lâm Phong ở Imperial Palace trước Ch17" là một câu SQL, **chính xác hơn** vector search. Cộng thêm PostgreSQL full-text search (`tsvector`) cho tra cứu văn bản. → **Khuyến nghị: bỏ Vector DB khỏi MVP hoàn toàn**, thêm `pgvector` khi có bằng chứng cụ thể là SQL + FTS không đủ.
- **Với (3)**: hoãn tới sau khi có Continuity Checker chạy thật; và khi cần thì cũng vẫn là pgvector.

#### 4.4 Seam nào ĐÚNG chỗ (giữ) — cái gì bỏ ngay

**Giữ, vì là ranh giới thật:**

1. **`Generation` sau một async job interface.** Đây là seam **đúng nhất** trong §12. Generate ảnh vốn: chậm (chục giây tới phút), fail được, tốn tiền, cần retry, cần rate-limit. Nó **phải** khác biệt về mặt vận hành với phần request-response còn lại. Giữ ranh giới `enqueue(spec) → job_id → poll/callback` ngay từ đầu, dù worker chạy cùng process. Đây là chỗ duy nhất sau này thật sự cần tách ra thành service riêng (để scale worker, để đặt rate limit riêng, để deploy độc lập khi đổi provider).
2. **Object Storage tách khỏi DB, từ ngày đầu.** Không bao giờ lưu ảnh dạng blob trong Postgres. Ảnh: content-addressed (`sha256`) trên S3/R2, DB chỉ giữ key + hash + metadata. Sửa sau rất đau (phải migrate dữ liệu binary), nên làm đúng ngay. Rẻ, không thêm phức tạp.
3. **Module interface giữa `story` / `comic` / `generation`.** Đúng ranh giới domain: `story` không được biết gì về panel; `comic` gọi `story` qua **duy nhất** `resolveState()` và `getBible()`; `generation` chỉ nhận **compiled visual spec**, không được đọc DB của story. Kỷ luật này là thứ khiến sau này tách service được — và nó **miễn phí** trong monolith. Enforce bằng lint rule cấm import chéo, hoặc test kiểm tra dependency direction.
4. **Adapter per image provider** (dưới `generation`). Đổi model là chắc chắn xảy ra. Interface: `generate(CompiledPrompt, ModelConfig) → GenerationResult`. Đây là seam có ROI cao nhất trên mỗi dòng code.
5. **Visual Prompt Compiler là một hàm/library thuần** (xem §6) — nhưng phải là một **module riêng biệt, không lẫn vào adapter**. Ranh giới đúng, chi phí bằng không.

**Bỏ ngay:**

1. **Tách 3 service** → module.
2. **Tách 2 database** → một DB nhiều schema. (Đây là điểm rủi ro cao nhất của §12.)
3. **Vector DB riêng** → bỏ hẳn ở MVP (4.3).
4. **WebSocket** → polling.
5. **API Gateway riêng ("Comic Studio API" như một tầng trước 3 service)** → không cần khi chỉ có một app.

---

### 5. §14 UI — Web Editor kiểu "Figma + comic editor + AI director"

#### 5.1 Ước lượng độ phức tạp: đây là hạng mục đắt nhất của cả sản phẩm

**Ước lượng của em (nêu rõ là ước lượng, không phải benchmark): một canvas editor đúng như §14 mô tả chiếm khoảng 50-60% tổng effort của toàn sản phẩm.** Phân bổ ước lượng:

| Hạng mục | % tổng effort (ước lượng) | Ghi chú |
|---|---|---|
| Canvas editor đầy đủ như §14 | **50-60%** | Bao gồm layout engine, selection/transform, undo-redo, sync state, perf |
| Story pipeline (import, parse, Bible, timeline, state resolver) | 15-20% | Chủ yếu là prompt engineering + schema; logic không rối |
| Comic Director (scene→page→panel, layout score) | 10% | Phần lớn là LLM call + rule đơn giản |
| Visual Compiler + generation + adapter + job queue | 10-15% | Nhiều I/O, ít logic phức tạp |
| Export/composite/typesetting | 5-10% | Bị đánh giá thấp — xem §8 |

Điểm cần nói với anh: **toàn bộ phần "AI" của sản phẩm này về mặt code là orchestration** — gọi LLM, gọi image API, lưu kết quả. Nó **không khó viết**, cái khó là chất lượng prompt và consistency (thuộc lens AI/ML). Ngược lại, canvas editor là **software engineering thuần, khó thật, không AI nào viết hộ được phần khó** (state machine, perf, edge case tương tác). Một dev đơn lẻ chọn build canvas editor trước là gần như chắc chắn không bao giờ tới được phần AI.

Đối chiếu để hiệu chỉnh: Figma là sản phẩm nhiều năm của hàng chục engineer với renderer WebGL viết riêng. §14 nhẹ hơn nhiều (không cần multiplayer, không cần vector editing), nhưng "nhẹ hơn nhiều" so với Figma vẫn là hạng mục nhiều tháng người.

#### 5.2 Vấn đề kỹ thuật tài liệu chưa nhắc tới

1. **Undo/redo trên state phân tán + tác dụng phụ không hoàn lại.** Undo trên canvas là bài toán đã khó; ở đây khó hơn vì một hành động (`Regenerate`) **tiêu tiền thật và mất 30s**. Undo một regenerate nghĩa là gì — quay lại ảnh cũ (được, nếu chưa xóa) hay huỷ job đang chạy (đã trả tiền rồi)? → Cần tách **hai loại action**: *spec edit* (undo được, local, dùng command pattern) và *side-effectful action* (không undo, chỉ có "quay lại generation trước"). Trộn hai loại vào một undo stack là nguồn bug và nguồn mất tiền.
2. **Optimistic update khi async 30s+.** UI không thể block. Panel cần state machine tường minh: `idle → queued → running → succeeded/failed → stale`, kèm placeholder/skeleton và progress. Đây là cái phải thiết kế từ đầu, không bolt-on được: nó lan ra mọi component.
3. **Race: user sửa spec trong khi generation đang bay.** Job trả về ảnh dựa trên spec **cũ**. Nếu ghi thẳng vào panel thì user thấy ảnh không khớp thứ mình vừa sửa → mất niềm tin vào hệ thống. → Bắt buộc: `generation.spec_version` (hoặc `spec_hash`); khi job hoàn thành mà `panel.spec_version != generation.spec_version` thì **không auto-apply**, đánh dấu `stale` và hỏi user. Cộng thêm khả năng **cancel job**. Đây là lỗ hổng cụ thể nhất tài liệu bỏ sót ở tầng UI.
4. **Panel layout engine — thứ bị đánh giá thấp nhất.** §5 vẽ layout đẹp nhưng để **thật sự** đi từ "Layout Score" tới hình học trang cần: grid/BSP-based partition, gutter, bleed, panel không chữ nhật (đường chéo — rất phổ biến trong manga), panel tràn lề, panel overlap, và **aspect ratio của ảnh phải khớp ô panel** (không thì crop mất nội dung quan trọng). → Vá tối thiểu: **thư viện template layout cố định** (10-15 layout dựng tay, mỗi cái có sẵn aspect từng ô), AI chỉ **chọn** template chứ không **sinh** hình học. Rẻ hơn cả chục lần và chất lượng cao hơn ở MVP.
5. **State sync và source of truth.** Canvas cần state cây phức tạp (page → panel → spec → generation). Nếu để client là source of truth rồi sync ngược sẽ có conflict; nếu server là source thì mỗi tương tác nhỏ thành một round-trip. → MVP: **server là source of truth, autosave theo debounce, một session một tab**. Chấp nhận hạn chế "không mở hai tab", ghi rõ, đừng build conflict resolution.
6. **Perf canvas với hàng trăm ảnh.** Một chapter 20 trang × 5 panel = 100 ảnh full-res; zoom out cả chapter là hàng trăm ảnh cùng lúc → tụt frame và ngốn RAM ngay. → Bắt buộc **multi-resolution pyramid** (thumb 256 / preview 1024 / full), virtualized rendering theo viewport, `IntersectionObserver`. Kéo theo yêu cầu backend: mỗi ảnh phải sinh **nhiều biến thể lúc upload**. Đây là ràng buộc UI đẩy ngược vào kiến trúc storage — cần biết **trước** khi thiết kế storage, không phải sau.
7. **Chưa nhắc: text/bubble là đối tượng có thể chọn/di chuyển trên canvas.** Nếu bubble là layer riêng (đúng — xem §8) thì canvas phải editable cho text: font, kern, wrap, tail của bubble trỏ đúng nhân vật. Đây gần như là **một editor thứ hai** nằm bên trong editor thứ nhất. Chi phí này hoàn toàn vắng mặt trong tài liệu.

#### 5.3 Con đường MVP đạt 80% giá trị mà không build canvas editor

**Thay canvas bằng form + list editor.** Cụ thể:

- **Trang = danh sách dọc các "panel card"**. Mỗi card: ảnh preview bên trái, form spec bên phải (shot, camera, characters, emotion, action, lighting, dialogue), nút `Regenerate`, dropdown chọn giữa các generation đã có, badge trạng thái/continuity. Đây là UI **CRUD + form + list** — thứ một dev làm nhanh và ít bug.
- **Layout chọn bằng template**: một hàng thumbnail 10-15 layout, click để gán cho trang. Không kéo thả hình học.
- **Sắp xếp panel bằng drag-to-reorder trong list** (một chiều), không phải kéo thả tự do 2D. Rẻ hơn cả chục lần.
- **Preview trang render server-side**: composite ảnh + bubble ra một PNG/PDF, hiển thị read-only. User xem thành phẩm, sửa thì quay lại form. Vòng lặp chậm hơn canvas nhưng **đúng và làm được**.

Điểm mấu chốt biện minh cho hướng này: **cả ba tương tác §14 nêu ra — `Regenerate`, `Change camera → Low angle`, `Replace character costume` — đều là "sửa một field của spec rồi generate lại". Không cái nào cần canvas.** Canvas chỉ thật sự cần thiết cho *bố trí hình học tự do* — mà đó chính là thứ nên thay bằng template ở MVP. Đây là bằng chứng trực tiếp từ chính tài liệu rằng canvas chưa cần thiết.

Yêu cầu "không ảnh hưởng các panel khác" cũng **không phải yêu cầu UI mà là yêu cầu data model**: panel là entity độc lập, generation gắn per-panel. Schema ở §2/§3 đã đảm bảo điều đó rồi, không cần canvas để đạt.

**Đường thoát về sau:** khi (và chỉ khi) đã có vòng lặp story→panel→ảnh chạy được và bằng chứng là bố cục tự do mới là bottleneck, thì thêm canvas trên **thư viện có sẵn** (`tldraw`, `konva`, `fabric.js` — lớp canvas/scene-graph phổ biến; em không khẳng định cái nào phù hợp nhất, cần spike riêng). **Không viết renderer từ đầu.** Điều kiện để làm được việc đó: giữ layout dưới dạng dữ liệu tường minh (`page_layout JSONB` với toạ độ chuẩn hoá 0-1 của từng ô) ngay từ MVP — template ghi vào chính schema đó, nên khi lên canvas không phải migrate. Đây là **seam đúng chỗ** ở tầng UI: hình học là dữ liệu, không phải hard-code trong component.

---

### 6. Visual Prompt Compiler §16 dưới góc compiler design

#### 6.1 Ánh xạ sang thuật ngữ compiler

| Tầng compiler | Trong comic-studio | Ghi chú |
|---|---|---|
| Source | Panel Specification (§6) + Story Bible | Thứ người/LLM viết ra và sửa |
| Semantic analysis / name resolution | **Resolver**: `character_id` → identity + `resolveState(at_event)`; `costume_id` → canonical costume + ref images; `location_id` → location identity | Đây là pha có giá trị nhất, và là chỗ Story Bible được "link" vào |
| **IR (AST đã resolve)** | **`CompiledVisualSpec`** — mô tả panel **độc lập model**: subject(s) với appearance đã resolve, danh sách reference asset (đã có hash), camera, composition, lighting, style token, continuity constraint | Đây là artifact nên **persist** và hash |
| Optimization pass | ưu tiên/lược bớt thuộc tính khi vượt hạn mức, dedup, resolve xung đột (spec nói costume A, state nói costume B) | Chỗ đặt policy tường minh |
| Backend / codegen | **Adapter per model**: `CompiledVisualSpec → payload thật của provider` (chuỗi prompt, negative prompt, danh sách ảnh ref, tham số) | Một backend một model family |
| Linker/assembler | Compositor: ảnh panel + bubble + layout → trang | Thuộc §8 |

Nhận xét: **§16 là ý tưởng đúng về mặt kiến trúc**, và nó ăn khớp trực tiếp với §1 (spec là source thì phải có compiler từ spec sang thứ model hiểu). Nó cũng là chỗ duy nhất thực thi được các invariant về consistency một cách tập trung.

**Điều chỉnh quan trọng:** phải **persist IR**, không chỉ persist chuỗi prompt cuối. `generation.compiled_spec JSONB` + `compiled_spec_hash`. Lý do: (a) khi đổi model, so sánh được "cùng IR, khác backend" để biết lỗi do model hay do resolver; (b) `compiled_spec_hash` là **cache key đúng** cho ảnh (§1) — hash prompt chuỗi thì không phát hiện được ref image đã đổi nội dung; (c) Continuity Checker cần biết **kỳ vọng** là gì, và kỳ vọng nằm ở IR chứ không ở prompt.

#### 6.2 Leaky abstraction — có rò rỉ, và rò rỉ ở đâu

**Có, chắc chắn rò rỉ.** IR chung **không** che được khác biệt capability. Các chỗ rò rỉ cụ thể:

1. **Multi-image reference vs. text-only.** IR chứa `references: [face_ref, costume_ref, location_ref]`. Backend A nhận cả ba ảnh. Backend B chỉ nhận text → phải **degrade lossily**: dịch ảnh thành mô tả chữ. Kết quả **không tương đương** — đó không phải khác biệt về cú pháp mà về **năng lực**. Cùng một IR sinh ra hai chất lượng khác hẳn nhau, và consistency (mục tiêu số 1 của cả sản phẩm) có thể tụt xuống mức không dùng được.
2. **Số lượng ref tối đa.** IR có 5 ref, backend chấp nhận 2 → phải **chọn bỏ**. Bỏ cái nào là **quyết định thẩm mỹ**, không phải quyết định kỹ thuật, nên không thể ẩn trong adapter một cách vô hại.
3. **Kiểm soát không gian** (pose/depth/region, kiểu ControlNet, hoặc regional prompt): có backend có, có backend không. `composition` trong IR mà backend không thực thi được thì trở thành gợi ý mờ.
4. **Ngữ pháp weighting/negative prompt** khác nhau; có model không có negative prompt.
5. **Giới hạn độ dài prompt** khác nhau → phải cắt, và cắt cái gì lại là quyết định thẩm mỹ.

#### 6.3 Vậy abstraction này còn đáng làm không? — Đáng, với ba điều kiện

**Đáng làm**, vì phần **resolution** (Story Bible + state → appearance cụ thể) là 70-80% giá trị của compiler (ước lượng) và nó **hoàn toàn model-agnostic**. Phần rò rỉ nằm ở 20-30% cuối (codegen). Bỏ compiler để mỗi chỗ tự nối chuỗi prompt thì logic resolve state sẽ bị nhân bản khắp code — đó là lỗi tệ hơn nhiều.

Ba điều kiện để không tự lừa mình:

1. **Capability manifest tường minh.** Mỗi backend khai báo: `max_reference_images`, `supports_image_reference`, `supports_negative_prompt`, `supports_pose_control`, `max_prompt_tokens`, `supports_seed`, `supported_aspect_ratios`. Compiler đọc manifest và **lập kế hoạch degrade**, thay vì adapter im lặng bỏ bớt. Đây là cách xử lý leaky abstraction đúng: **không che, mà phơi ra một cách có cấu trúc**.
2. **Degradation phải được báo cáo, không im lặng.** Output của compiler là `(payload, degradations[])`. Lưu `generation.degradations JSONB`. Khi Continuity Checker báo lỗi ở một panel mà panel đó có `degradations = ['dropped costume_ref: max 2 refs']`, ta biết ngay lỗi là do abstraction, không phải do model dở. Không có cái này thì mọi lỗi consistency đều mờ về nguyên nhân — và đó chính là kịch bản dự án chết vì không debug được.
3. **Là library/hàm thuần, KHÔNG phải service.** `compile(panel_spec, bible, model_capability) → (CompiledVisualSpec, payload, degradations)`. Không I/O trong hàm compile (resolve xong truyền vào), để test được bằng golden test: cùng input → cùng output. Đây là **module dễ test nhất của cả hệ** và nên tận dụng: một bộ golden file cho ~20 panel mẫu sẽ bắt được hầu hết regression khi sửa prompt.

Cảnh báo YAGNI: **đừng thiết kế IR như một ngôn ngữ có parser/grammar riêng.** Nó chỉ cần là một **struct/JSON schema có version** (`ir_version`). Viết DSL với cú pháp riêng cho việc này là over-engineering cổ điển — không có người dùng thứ hai nào cần đọc DSL đó.

---

### 7. Thứ tự 4 MVP milestone §18

#### 7.1 §18 vi phạm nguyên tắc de-risk-first

**Có, vi phạm rõ.** Xếp hạng rủi ro **chưa được kiểm chứng** trong 4 milestone:

| Milestone | Rủi ro kỹ thuật | Mức | Đã kiểm chứng chưa |
|---|---|---|---|
| MVP1 Story Intelligence | LLM extract nhân vật/timeline/state từ truyện dài | **Trung bình** | Về cơ bản là bài toán đã có nhiều tiền lệ; sai thì user sửa tay được. Không giết được dự án. |
| MVP2 Comic Director | LLM chia scene→page→panel, chọn layout | **Thấp-Trung bình** | Chất lượng thẩm mỹ có thể kém, nhưng **luôn ra được kết quả** và luôn sửa tay được. |
| **MVP3 Visual Generation** | **Character/location/style consistency xuyên hàng trăm panel** | **CAO NHẤT — và có tính nhị phân** | **Chưa kiểm chứng.** Nếu không đạt, **toàn bộ sản phẩm vô nghĩa**. Không có workaround thủ công (không ai vẽ lại 5000 panel bằng tay). |
| MVP4 Production | Continuity checker, export, batch | Trung bình | Chủ yếu là engineering, ít ẩn số. |

Nói cách khác: §18 đặt **rủi ro tồn vong ở vị trí thứ ba**. Kịch bản xấu rất cụ thể: hoàn thành MVP1 + MVP2 (theo phân bổ effort ở §5.1, cỡ 25-30% tổng effort, và với 1 dev là nhiều tháng), rồi tới MVP3 phát hiện consistency không đạt mức xuất bản → mọi thứ trước đó **không có giá trị độc lập** (một Story Bible đẹp mà không ra được comic thì để làm gì). Đây đúng là định nghĩa của "để rủi ro lớn nhất tới cuối".

Có một lập luận bảo vệ §18: MVP3 **cần** ref sheet và panel spec làm input, nên có phụ thuộc kỹ thuật. Nhưng phụ thuộc đó **không cần bản tự động hoá** — chỉ cần dữ liệu, và dữ liệu đó viết tay được trong vài giờ. Ràng buộc thứ tự này là giả.

Điểm phụ nhưng đáng nói: MVP1 nói "chưa cần generate ảnh" — **hoàn toàn hợp lý** như một *ranh giới scope*. Sai lầm không phải ở việc MVP1 không có ảnh, mà ở việc **hoàn thiện MVP1 trước khi thử ảnh lần nào**.

#### 7.2 Thứ tự thay thế đề xuất

```text
MVP0  Vertical Slice / Spike  (mục tiêu: một câu trả lời GO / NO-GO)
      -> Story Bible viết TAY bằng YAML cho MỘT chapter (3-5 nhân vật, 2-3 địa điểm)
      -> Panel spec viết TAY hoặc LLM một lần, ~15-20 panel
      -> Ref sheet dựng tay cho từng nhân vật
      -> Generate 15-20 panel bằng ref-based conditioning
      -> Composite ra một trang thật, CÓ speech bubble
      -> Đo: consistency (mắt người + tự đánh giá), chi phí/panel, số lần retry/panel
      Không UI. Không database. Script + file phẳng.

MVP1  Visual Generation Loop  (cũ là MVP3)
      -> schema Story Bible + timeline + state resolver (§2) ở mức tối thiểu
      -> Visual Prompt Compiler + một adapter
      -> job queue trong Postgres, generation lineage
      -> UI form/list (§5.3), KHÔNG canvas

MVP2  Story Intelligence  (cũ là MVP1)
      -> tự động extract Bible/timeline/state, có provenance ai_generated/human_edited
      -> thay thế dần phần viết tay ở MVP0/MVP1

MVP3  Comic Director  (cũ là MVP2)
      -> tự động scene→page→panel, chọn template layout

MVP4  Production  (giữ nguyên vị trí)
      -> Continuity checker (report-only), export PDF/CBZ/webtoon, batch, budget cap
```

Lý do đảo MVP1 ↔ MVP3: **rủi ro cao nhất đi trước**, và phần tự động hoá story luôn có thể **thay thế input viết tay** — tức là MVP2 mới là phần tăng năng suất, còn MVP1 mới là phần chứng minh sản phẩm tồn tại được. Xây phần tăng năng suất trước khi biết sản phẩm có tồn tại được là đầu tư sai thứ tự.

#### 7.3 Có nên làm vertical slice trước? — CÓ, đây là khuyến nghị mạnh nhất của em về roadmap

**Nên, và nên coi là bắt buộc.** Lập luận:

1. **Giá của việc biết sớm.** Ước lượng vertical slice: **cỡ 1-2 tuần người** (viết tay Bible + script gọi API + composite thô). So với nhiều tháng để đi hết MVP1+MVP2 rồi mới biết. Tỉ lệ đòn bẩy rất cao.
2. **Nó trả lời được đúng những câu quyết định go/no-go**, mà không câu nào trả lời được trên giấy: consistency có đạt không? chi phí một panel bao nhiêu (× ~5000 panel cho 100 chapter → tổng ngân sách; với A1 "ngân sách tự bỏ" đây có thể là **ràng buộc chặn**)? cần bao nhiêu lần retry mỗi panel? text tiếng Việt lên ảnh bằng cách nào (§8)? aspect ratio panel có kiểm soát được không?
3. **Nó buộc phải chạm vào mọi layer** → phát hiện sớm những **mismatch giữa các tầng** mà thiết kế trên giấy luôn bỏ sót. Ví dụ điển hình: layout template cần panel tỉ lệ 21:9, nhưng model chỉ hỗ trợ vài aspect cố định → **layout engine phải thiết kế quanh ràng buộc của model, không ngược lại**. Đây là loại phát hiện chỉ đến từ vertical slice, và nếu đến muộn thì phải làm lại layout engine.
4. **Nó sinh ra golden dataset.** 15-20 panel với spec + ref + ảnh + đánh giá bằng mắt trở thành bộ test regression cho toàn bộ phần sau (đặc biệt cho Visual Prompt Compiler ở §6.3 điều kiện 3). Tài sản này dùng suốt vòng đời dự án.
5. **Kỷ luật quan trọng: code của spike KHÔNG phải nền của sản phẩm.** Viết để trả lời câu hỏi rồi **bỏ**, giữ lại **kết luận và dữ liệu**. Nếu không nói rõ điều này trước, spike sẽ biến thành nền móng tạm bợ — đây là bẫy phổ biến nhất khi làm spike.

**Cổng quyết định sau MVP0** — định nghĩa trước, đừng để tự phán khi đã đầu tư cảm xúc:

| Tiêu chí | Ngưỡng đề xuất (điều chỉnh cùng lens AI/ML) |
|---|---|
| Consistency nhân vật | ≥ 70% panel nhận ra là cùng một người, không cần retry, ở mức người đọc chấp nhận |
| Số lần generate / panel dùng được | ≤ 3 |
| Chi phí | tổng chi phí ước tính cho một chapter nằm trong ngân sách anh chấp nhận |
| Text | có đường đi rõ ràng để đưa thoại tiếng Việt lên trang ở chất lượng đọc được |

Không đạt → **không phải hủy dự án**, mà là đổi định vị (ví dụ: công cụ hỗ trợ họa sĩ / storyboard generator thay vì comic hoàn chỉnh) — nhưng phải quyết định đó **sớm**, không phải sau nhiều tháng.

**Phụ thuộc chéo cần lens AI/ML xác nhận:** toàn bộ §7 dựa trên GĐ-1 (consistency bằng reference-image conditioning là con đường chính). Nếu lens kia kết luận consistency chỉ đạt được qua fine-tune/LoRA per-character, thì MVP0 phải bao gồm cả một vòng train, effort tăng đáng kể, và ranh giới `generation` phải mở rộng để quản lý model artifact per-character (thêm entity `character_model` có version + training data lineage).

---

### 8. Cái gì THIẾU hẳn trong tài liệu

Xếp theo mức nguy hiểm giảm dần.

#### 8.1 Speech bubble & typesetting — lỗ hổng lớn nhất

Comic là **tranh + chữ**. Tài liệu có `dialogue` như một field của panel (§6) và có `Dialogue` trong Comic Director (§11) nhưng **không một dòng nào** nói chữ đó lên ảnh bằng cách nào. Với truyện chữ Trung/Việt, thoại là phần lớn nội dung — đây không phải chi tiết nhỏ.

**Nổ khi nào:** ngay panel có thoại đầu tiên, tức là **trong MVP0**. Không thể hoãn.

**Vá tối thiểu (và đây là kiến trúc đúng, không phải workaround):**

- **Generate art KHÔNG có chữ** (đưa "text, letters, watermark, speech bubble" vào negative prompt), rồi **overlay bubble bằng code**. Lý do (GĐ-3): image model render text tiếng Việt có dấu ở chất lượng xuất bản là không đáng tin, và chữ trong ảnh raster thì **không sửa được, không dịch được, không đổi font được**.
- Bubble là **layer dữ liệu riêng**, không nướng vào ảnh:

```sql
CREATE TABLE speech_bubble (
    id          UUID PRIMARY KEY,
    panel_id    UUID NOT NULL REFERENCES comic_panel(id) ON DELETE CASCADE,
    speaker_id  UUID REFERENCES character(id),      -- NULL = narration
    kind        TEXT NOT NULL,   -- 'speech'|'thought'|'shout'|'whisper'|'narration'|'sfx'
    text        TEXT NOT NULL,
    -- toạ độ CHUẨN HOÁ 0-1 theo khung panel => độc lập resolution
    x REAL, y REAL, w REAL, h REAL,
    tail_x REAL, tail_y REAL,                        -- đuôi bubble trỏ tới miệng speaker
    font_family TEXT, font_size_pt REAL,
    z_index     INT NOT NULL DEFAULT 0,
    reading_index INT NOT NULL,                      -- thứ tự đọc trong panel
    UNIQUE (panel_id, reading_index)
);
```

- Ràng buộc **đẩy ngược lên panel spec**: panel có 3 câu thoại dài thì bố cục phải **để chỗ trống** cho bubble. Nếu không truyền yêu cầu này xuống prompt (kiểu "để không gian trống phía trên bên phải"), bubble sẽ che mặt nhân vật. → Panel spec cần `text_budget` (số ký tự thoại) và `negative_space_hint`. **Đây là ràng buộc kiến trúc từ typesetting ngược vào Visual Prompt Compiler mà tài liệu hoàn toàn không có.**
- Auto-placement bubble ở MVP: heuristic đơn giản (đặt gần vị trí speaker, tránh vùng có mặt nếu detect được, thứ tự đọc trên-xuống/phải-sang-trái tuỳ định dạng) + **cho phép user kéo tay**. Không cần thuật toán tối ưu.

#### 8.2 Page composition — từ N ảnh panel thành một trang thật

Tài liệu vẽ layout dạng ASCII (§5) nhưng không có bước **composite thật**: đặt N ảnh vào N ô, crop/fit theo aspect, vẽ khung, gutter, bleed, overlay bubble, xuất trang ở đúng DPI.

**Nổ khi nào:** ngay khi muốn xem "một trang" chứ không phải "các ảnh rời" — trong MVP0.

**Vá tối thiểu:** một module `export/compositor` chạy server-side với thư viện xử lý ảnh (lớp `sharp`/Pillow/ImageMagick), lấy input là `page_layout JSONB` (toạ độ chuẩn hoá 0-1 mỗi ô) + `approved_generation_id` mỗi panel + bảng `speech_bubble`, xuất PNG. Toạ độ chuẩn hoá là điểm then chốt: cùng một dữ liệu render được cả thumbnail preview và bản in 300 DPI. Đồng thời phải chốt sớm **canonical page size + DPI** (ví dụ A5 @ 300 DPI) vì nó quyết định resolution cần generate cho mỗi panel — và resolution quyết định **chi phí**. Chốt muộn thì phải generate lại toàn bộ.

#### 8.3 Xuất bản (PDF / CBZ / Webtoon strip)

§18 xếp export vào MVP4 — **hợp lý về thứ tự ưu tiên**, nhưng thiếu ràng buộc ngược: ba định dạng này có **hình dạng trang khác nhau về bản chất**. Webtoon là dải dọc liên tục, không có "trang", không có gutter ngang, tỉ lệ ~1:15+. PDF/CBZ là trang rời cố định tỉ lệ. **Không thể lấy layout thiết kế cho trang A5 rồi tự động ra webtoon.**

**Nổ khi nào:** lúc muốn xuất webtoon sau khi đã làm hàng trăm trang theo layout sách → phải làm lại layout.

**Vá tối thiểu:** chốt **một** target format cho MVP (em đề xuất **PDF/CBZ trang rời** vì đơn giản hơn và test bằng mắt dễ hơn), nhưng đưa `target_format` vào `project` **ngay từ schema đầu tiên** và cho `page_layout` mang `format_variant`, để sau này một page có thể có hai layout cho hai format thay vì phải migrate. Chi phí bây giờ: một cột. Chi phí sau: làm lại layout engine.

#### 8.4 Chi phí và quota inference — vắng mặt hoàn toàn

`Request.md` **không có một chữ nào** về tiền, quota, hay rate limit. Nhưng với A1 ("ngân sách tự bỏ") thì đây có thể là **ràng buộc chặn mạnh hơn mọi ràng buộc kỹ thuật**.

**Nổ khi nào:** lần đầu chạy batch cả chapter (~50 panel × N retry), hoặc lần đầu regenerate hàng loạt sau khi sửa một costume ở Story Bible. Rủi ro cụ thể: một hành động một click ở UI làm phát sinh hàng nghìn generation.

**Vá tối thiểu (làm ngay từ MVP1, không hoãn):**

- Lưu `cost_usd` trên mỗi `generation` (đã nêu §3.1).
- Bảng `budget(project_id, period, limit_usd, spent_usd)` + **kiểm tra hạn mức trước khi enqueue**, không phải sau khi tiêu.
- **Trần cứng cho mỗi batch**: mọi thao tác sinh ra > N job phải hiển thị chi phí dự kiến và yêu cầu xác nhận. N nhỏ, ví dụ 10.
- `max_attempts` mỗi panel, để một panel "khó" không đốt vô hạn.
- Rate limiter phía worker theo provider (concurrency giới hạn) — nếu không sẽ bị 429 hàng loạt và mất job.

#### 8.5 Idempotency của job queue

Không nhắc tới. Mọi queue đều là at-least-once trên thực tế (worker chết sau khi gọi API nhưng trước khi ghi DB → job chạy lại → **tốn tiền hai lần và tạo generation trùng**).

**Nổ khi nào:** lần đầu worker bị kill/deploy giữa lúc chạy — chắc chắn xảy ra trong tuần đầu vận hành.

**Vá tối thiểu:** `job(idempotency_key UNIQUE)` với key = `hash(panel_id, compiled_spec_hash, attempt_no)`; transactional enqueue (§4.2) để không có job mồ côi; và **tạo row `generation` với `status='pending'` TRƯỚC khi gọi API**, lưu `provider_request_id` ngay khi có. Khi retry, kiểm tra `provider_request_id` đã tồn tại thì đi lấy kết quả thay vì gọi lại. Không có bước này thì mọi retry đều là tiền mất thật.

#### 8.6 Lỗi giữa batch, retry, resume

Không nhắc tới. Batch 50 panel, panel 23 fail — hiện tại tài liệu không định nghĩa chuyện gì xảy ra.

**Nổ khi nào:** batch đầu tiên.

**Vá tối thiểu:** **không có "batch" như một đơn vị nguyên tử.** Mỗi panel một job độc lập, có `status` riêng; batch chỉ là một `batch_id` để nhóm và hiển thị tiến độ `43/50 done, 2 failed, 5 running`. Phân loại lỗi tường minh: `transient` (429, 5xx, timeout → retry với exponential backoff, `max_attempts=3`) vs. `permanent` (content policy refusal, invalid input → **không retry**, báo user, vì retry chỉ đốt tiền). Nút "resume batch" chỉ chạy lại panel `failed`. Với ngân sách cá nhân, phân biệt transient/permanent là khác biệt giữa tốn 3 lần và tốn 1 lần.

#### 8.7 Migration schema khi Story Bible đổi hình dạng

Không nhắc tới, nhưng chắc chắn xảy ra: hình dạng Story Bible sẽ đổi hàng chục lần trong lúc phát triển (đây là bản chất của việc chưa biết trước cần field gì).

**Nổ khi nào:** khoảng lần đổi thứ ba, khi đã có dữ liệu thật của một truyện dài và không muốn nhập lại.

**Vá tối thiểu:**

- **Chiến lược lai, tường minh về ranh giới**: cột SQL cho thứ **cần query/join/index** (`character_id`, `story_order`, `costume_id`, `emotion`); `JSONB` cho thứ **mô tả và còn biến động** (`extra`, `visual_attributes`, `personality`). Vẽ đúng đường này là quyết định schema quan trọng thứ hai sau §2.
- `schema_version INT` trên mỗi row JSONB (đã có trong DDL §2.2) + **upcaster đọc lười**: khi đọc row version cũ thì nâng cấp trong bộ nhớ, ghi lại version mới khi có dịp. Tránh migration lớn khoá cả bảng và tránh phải viết migration cho mọi thay đổi nhỏ.
- Giữ **artifact gốc** (văn bản chương đã import) trong object storage vĩnh viễn. Đây là bảo hiểm cuối: schema hỏng thì extract lại được. Rẻ, và nhiều dự án bỏ qua rồi hối.

#### 8.8 Versioning Story Bible khi user sửa tay — thiếu và sẽ rất đau

Tài liệu có "Versioning" trong MVP4 nhưng không nói versioning **cái gì**. Vấn đề thật, rất cụ thể: user sửa tay costume của Lâm Phong (LLM extract sai). Sau đó chạy lại extraction cho chapter mới → **LLM ghi đè lên sửa tay của user**. User mất công sức, và mất niềm tin — thường là đủ để bỏ công cụ.

**Nổ khi nào:** lần thứ hai chạy extraction trên một project đã được sửa tay. Rất sớm.

**Vá tối thiểu (rẻ và hiệu quả cao):**

- **Provenance ở mức field, không mức row**: `character_state.field_provenance JSONB` kiểu `{"costume_id":"human","emotion":"ai","injuries":"ai"}`.
- **Luật ghi bất di bất dịch**: re-extraction **không bao giờ** ghi đè field có provenance `human`. Nếu LLM ra kết quả khác thì tạo một `suggestion` để user xem, không apply.
- **Audit log tối thiểu** thay vì full versioning: `change_log(entity_type, entity_id, field, old_value, new_value, actor, at)`. Append-only, một bảng, rẻ. Đủ để trả lời "ai đổi cái này, khi nào" và để undo thủ công. **Không** cần Git-like branching/merge cho Story Bible ở MVP — đó là hố effort không đáy.
- Nếu muốn một mức nữa: `bible_snapshot` (dump JSONB toàn bộ Bible) tạo tại các mốc quan trọng. Một bảng, dùng để rollback thảm hoạ.

#### 8.9 Ba thứ khác chưa nhắc, đáng ghi lại

- **Story Bible không có nguồn dẫn (citation) về văn bản gốc.** Khi Bible nói "Lâm Phong có vết sẹo mắt trái", cần biết câu nào ở chapter nào nói vậy để verify. → `evidence JSONB` trên state row: `[{chapter, char_offset_start, char_offset_end}]`. Không có thì mọi lỗi extraction đều không kiểm chứng được và user phải tin mù. Rẻ nếu làm từ đầu (lưu offset lúc parse), gần như không thể thêm sau (offset thay đổi khi re-parse).
- **Nhân vật/địa điểm chưa có tên hoặc trùng tên.** Truyện dài đầy "người đàn ông áo đen" (sau này mới lộ danh tính) và tên trùng. Cần `character_alias(character_id, alias, first_seen_event_id)` và một quy trình **merge hai character đã tạo nhầm thành một** (merge phải cập nhật mọi state/panel/generation reference). Nổ khi extract tới chapter mà danh tính được tiết lộ. Không có merge thì Bible thành rác.
- **Chapter dài hơn context window của LLM.** Tài liệu giả định "chapter" là đơn vị xử lý được. Với chapter dài hoặc khi cần bối cảnh 39 chapter trước, phải chunk + carry-over state giữa các chunk. Đây là chỗ duy nhất **thật sự** cần retrieval (§4.3). Vá tối thiểu: chunk theo scene boundary, truyền `resolveState()` của cuối chunk trước vào đầu chunk sau (running state), không nhồi cả lịch sử.

---

### 9. Kết luận kiến trúc

#### 9.1 Verdict

**PHÙ HỢP CÓ ĐIỀU KIỆN.** Tầm nhìn kiến trúc (spec-as-source, tách 3 layer, intermediate representation) là **đúng và ở mức trên trung bình rõ rệt** so với cách tiếp cận thông thường — tác giả đã nhìn ra đúng chỗ khó (consistency và state theo timeline) chứ không bị hút vào phần dễ (gọi image model). Nhưng scope và infrastructure **không phù hợp với ràng buộc 1 dev / ngân sách cá nhân (A1)**, và data model có một lỗ hổng cụ thể (thứ tự thời gian) sẽ gây sai dữ liệu âm thầm nếu không vá trước.

Ba điều kiện để "phù hợp":

1. **Thu §12 về modular monolith + một PostgreSQL + queue trong Postgres, bỏ Vector DB** (§4.2). Giữ 5 seam ở §4.4.
2. **Đảo thứ tự §18 để đâm vào rủi ro consistency trước, và chạy vertical slice MVP0 (1-2 tuần) với cổng go/no-go định trước** (§7.2, §7.3).
3. **Bỏ canvas editor §14 khỏi MVP, thay bằng form/list editor** (§5.3), nhưng lưu layout dạng toạ độ chuẩn hoá để sau này lên canvas không phải migrate.

Không đạt ba điều kiện này thì dự đoán của em (ước lượng, không phải sự thật): dự án dừng ở trạng thái hạ tầng chạy tốt nhưng chưa bao giờ ra được một trang comic hoàn chỉnh.

#### 9.2 Top 3 điểm mạnh — giữ nguyên không đổi

1. **"Ảnh là output của specification, không phải dữ liệu chính"** (§Quyết định kiến trúc). Đây là quyết định đúng nhất trong tài liệu và là thứ duy nhất khiến hệ thống chịu nổi 100 chapter. Chỉ cần điều chỉnh cách diễn đạt: ảnh là *immutable artifact có provenance*, không phải cache tái tạo được (§1).
2. **Tách 3 layer Semantic AI / Comic Director / Image Generator (§11) + Visual Prompt Compiler (§16)**. Ranh giới đúng chỗ, cho phép đổi model mà không đụng phần hiểu truyện — chỗ đắt nhất và không tái tạo được. Điều kiện: compiler là library thuần với capability manifest và báo cáo degradation (§6.3).
3. **Timeline + state theo thời điểm là first-class (§2, §3, §9)**. Nhìn ra đây là hạt nhân của consistency là insight then chốt — đúng, và hiếm. Cần siết lại thành **một** mô hình duy nhất với `story_order` (§2.2) thay vì bốn cách diễn đạt song song.

#### 9.3 Top 3 sai lầm/rủi ro cần sửa TRƯỚC dòng code đầu tiên

1. **`(chapter, scene)` làm khóa thời gian — lỗi data model, mức nghiêm trọng.** Trộn reading order với story order → sai state ở mọi cảnh flashback, sai **âm thầm** (không crash), và Continuity Checker sẽ "sửa" panel đúng thành sai. → Sửa: hai trục `reading_order` / `story_order` (NUMERIC sparse) + `timeline_id`, mọi state query đi qua **một** `resolveState()`, index `(entity_id, timeline_id, story_order DESC)` (§2.2, §2.3). Sửa trước khi code vì đây là schema **và là giả định lan khắp mọi module**; sửa sau đồng nghĩa migrate dữ liệu và rà lại toàn bộ query.
2. **Hai database tách rời (§12)** cắt đúng chỗ dữ liệu ràng buộc chặt nhất (panel ⇄ Story Bible), mất FK/join/transaction, buộc tự viết eventual consistency mà không được lợi gì. → Sửa: một PostgreSQL, ba schema (§4.2). Sửa trước vì đây là quyết định gần như không thể đảo chiều rẻ.
3. **Speech bubble & typesetting hoàn toàn vắng mặt (§8.1).** Comic không có chữ thì không phải comic; và ràng buộc "để chỗ trống cho bubble" phải đi **ngược** vào panel spec và Visual Prompt Compiler. Phát hiện muộn → phải generate lại toàn bộ ảnh đã làm vì bubble che mặt nhân vật. → Sửa: chốt ngay "generate art không chữ + overlay bubble bằng code", thêm `speech_bubble` table và `text_budget`/`negative_space_hint` vào panel spec, và **thử nghiệm trong MVP0**.

#### 9.4 Top 3 thứ nên CẮT khỏi MVP (dù nghe hay)

1. **Canvas editor kiểu Figma (§14).** Ước lượng 50-60% tổng effort, và **cả ba tương tác tài liệu nêu ra đều không cần canvas** (§5.2, §5.3). Thay bằng form/list + template layout + preview render server-side. Đây là khoản cắt lớn nhất và ít mất mát nhất.
2. **"Fix automatically" của Continuity Checker (§15).** Auto-fix có nghĩa: tự regenerate dựa trên state mà chính hệ thống có thể đang hiểu sai (§9.3 điểm 1), tự tiêu tiền, và tự ghi đè ảnh user đã chọn. Rủi ro tệ nhất: nó **phá** những panel đang đúng. → MVP: Continuity Checker **report-only** ("panel 7: costume lệch — kỳ vọng Black Robe v2, phát hiện Blue Robe"), user bấm regenerate. Giữ được 80% giá trị với 20% rủi ro. Bản thân **detection** đã là phần khó và đủ giá trị.
3. **Toàn bộ hạ tầng phân tán: 3 service + 2 DB + Vector DB riêng + WebSocket (§12).** Không phục vụ user nào ở MVP, tiêu effort vào plumbing. → Monolith + 1 Postgres (có queue) + object storage + polling (§4.2).

**Ứng viên cắt bổ sung (nếu cần cắt sâu hơn):** UI duyệt cây generation (§3.2 — flat list là đủ); "Layout Score" 5 chiều của §5 (bắt đầu bằng heuristic 2 chiều: mật độ thoại + độ quan trọng, chọn trong 10-15 template — 5 chiều số thực không kiểm chứng được là đúng hay sai, nên không đáng làm sớm); expression sheet đầy đủ mỗi nhân vật (§8 — bắt đầu 3 góc + 3 biểu cảm).

---

## Tài liệu tham khảo

- `docs/999-Resources/Request.md` — đối tượng phân tích (894 dòng, 18 mục). Các mục được viện dẫn trực tiếp: §2 (Story Bible/Character timeline), §3 (Timeline first-class), §5 (AI Layout Director), §6 (Panel specification), §9 (Identity vs Appearance), §11 (3 tầng generation), §12 (backend architecture), §13 (database model + `Generation`), §14 (UI Web Editor), §15 (Continuity Checker), §16 (Visual Prompt Compiler), §18 (4 MVP milestone), §Một quyết định kiến trúc em nghĩ nên chốt ngay.
- `docs/010-Planning/pm-runs/2026-08-23-danh-gia-y-tuong-comic-studio/brief.md` — Assumptions A1-A5, Open questions OQ1-OQ3, Nợ kỹ thuật.
- `knowledge-base/45-Role-Memory/architect/000-Core-Memory.md` — nguyên tắc KISS/chống over-engineering (§3), ưu tiên giải thích "The Why".
- `knowledge-base/45-Role-Memory/architect/2026-03-31-standalone-skill-creator-pattern.md` — bài học về module tự chứa và tránh phụ thuộc ngầm vào ngữ cảnh bên ngoài.
- `.claude/rules/clean-code.md`, `.claude/rules/mindset.md` — Simplicity First, YAGNI, Systems Thinking (ripple effects).

---

## PM đọc được gì

1. **Lỗ hổng `(chapter, scene)` là phát hiện có giá trị cao nhất của lens này**, và PM không lường trước. Nó là lỗi *âm thầm* — không crash, không sai rõ ràng, chỉ resolve sai state ở flashback. Với truyện dài (use case chính), flashback gần như chắc chắn xuất hiện. Hệ quả dây chuyền mà `architect` nêu đáng đưa lên đầu deliverable: **Continuity Checker sẽ "sửa" đúng những panel đang đúng** — tức là một lỗi data model biến feature đắt nhất thành công cụ phá hoại.
2. **Ước lượng §14 = 50-60% tổng effort** xác nhận và định lượng điều lens PM chỉ nêu định tính. Kèm lập luận mạnh hơn PM đã có: cả 3 tương tác mà §14 nêu ra (Regenerate / Change camera / Replace costume) **không cần canvas** — chúng là 3 form action trên một danh sách. Đây là loại lập luận cắt scope mà anh có thể hành động ngay.
3. **Kết luận "ràng buộc thật là thời gian dev, không phải hạ tầng"** hội tụ độc lập với `researcher` (chi phí inference $400–1.600/100 chapter) và với `senior-ai-engineer` (nút thắt là phút-người ở HITL gate). **Ba lens, ba đường lập luận khác nhau, cùng một kết luận** — đây là mức tin cậy cao nhất mà run này đạt được về bất kỳ điểm nào.
4. **`architect` chủ động đánh dấu 3 giả định công nghệ (GĐ-1/2/3) thay vì đoán** — đúng thiết kế fan-out. Phân xử ở mục *Mâu thuẫn* bên dưới.

## Mâu thuẫn với lens khác

| # | Nội dung | PM phân xử |
|---|---|---|
| **GĐ-1** | Consistency đạt bằng reference-image conditioning, không phải fine-tune per-character. | ✅ **`researcher` XÁC NHẬN.** Native multi-image reference model (Nano Banana Pro 14 ảnh / FLUX.2 pro 10 ảnh) là hướng khuyến nghị; LoRA chỉ là lớp tăng cường tùy chọn ($2–5/LoRA). → GĐ-1 đúng, **không** cần thêm entity `character_model` có version ở MVP. |
| **GĐ-2** | Closed API ⇒ reproducibility đúng nghĩa không đạt được; `seed` chỉ còn giá trị provenance; mục tiêu thật của `Generation` là auditability/lineage. | ✅ **`researcher` XÁC NHẬN VÀ NÂNG CẤP.** `architect` suy ra đúng bản chất bằng lập luận kỹ thuật thuần. `researcher` bổ sung lý do mạnh hơn: auditability đó là **nghĩa vụ pháp lý** ở Việt Nam theo Nghị định 134/2026/NĐ-CP (hiệu lực 09/04/2026) — phải lưu prompts, inputs, intermediate drafts để chứng minh "substantial and decisive intellectual contribution". → `parent_generation` **không được cắt** khỏi MVP, và phải bổ sung lưu **các bước human edit/chọn-loại**. |
| **GĐ-3** | Model không render được text tiếng Việt có dấu ở chất lượng xuất bản. | 🟡 **Tiền đề SAI một phần, kết luận ĐÚNG.** `researcher`: press VN xác nhận Nano Banana Pro render tiếng Việt có dấu tốt (không có benchmark định lượng). **Nhưng** `researcher` vẫn khuyến nghị typeset layer riêng *bất kể* chất lượng render, vì 3 lý do độc lập: editability (sửa thoại không phải regenerate ảnh), bubble không được che mặt (cần field `text_safe_zone` trong panel spec — trùng khớp đề xuất của `architect`), và ranh giới bản quyền theo Zarya (text do người viết là phần **được bảo hộ**). → Khuyến nghị của `architect` giữ nguyên, nhưng deliverable phải nêu **đúng lý do**, không nêu lý do sai. |
| **M-thứ-tự-MVP** | `architect` đề xuất đảo thứ tự §18 + vertical slice MVP0. | **Hội tụ với cả hai lens kia**, chỉ khác tên gọi: `researcher` gọi là "spike nhỏ của MVP3 đẩy lên trước" (~$12), `senior-ai-engineer` gọi là "Story Bible spike, và spike image consistency nên chạy song song", PM gọi là MVP0. **Deliverable dùng một tên: MVP0**, và ghi rõ ba lens độc lập cùng đề xuất. Điều chỉnh theo dữ liệu `researcher`: **không cắt MVP1** (nó rủi ro thấp, có CANVAS làm bằng chứng) — chỉ chèn MVP0 trước nó. |

---

## Bổ sung sau GATE — kiến trúc dưới mô hình SaaS thương mại multi-tenant

> **Giả định đã đổi.** Phân tích ở các mục trên chạy dưới `A1 = công cụ cá nhân, 1 dev, ngân sách tự bỏ`. Đáp án thật tại GATE: **vẫn 1 dev + AI assist**, nhưng là **SaaS thương mại multi-tenant, khách hàng tự upload truyện của họ**. Section này chỉ xử lý phần **thay đổi**; mọi kết luận cũ không được nhắc lại ở đây thì vẫn giữ nguyên hiệu lực.
>
> **Lưu ý về mẫu số của các con số % bên dưới:** ước lượng cũ (§5.1: canvas = 50-60%) tính trên mẫu số **công cụ cá nhân** (không có multi-tenancy, billing, auth, moderation). Các ước lượng mới trong section này tính trên mẫu số **SaaS** — đã bao gồm khối multi-tenancy. Hai bộ số **không so sánh trực tiếp được**; em ghi rõ mẫu số ở mỗi chỗ.

### B1. ⭐ Khuyến nghị cắt canvas editor §14 — xét lại

**Kết luận: (c) CẮT MỘT PHẦN.** Không cắt sạch như khuyến nghị cũ, nhưng cũng dứt khoát không build §14 đầy đủ. Lý do phải điều chỉnh: dưới mô hình SaaS, phản biện của PM có một phần đúng — nhưng đúng ở chỗ khác với chỗ PM nghĩ.

**Phản biện bản quyền: đúng về nghĩa vụ, sai về phương tiện.** Đây là điểm em muốn nói rõ nhất.

Yêu cầu "*iterative, interactive process rather than solely relying on prompts*" là yêu cầu về **quyết định sáng tạo của con người có được ghi nhận hay không** — không phải yêu cầu về công nghệ render UI. Một canvas editor **không** tự sinh ra tính được bảo hộ; nó chỉ là một cách nhập liệu. Ngược lại, một form editor có ghi vết đầy đủ **cũng thoả mãn**, miễn là nó emit đủ audit event: *người dùng đã chọn generation X thay vì Y*, *đã tự viết/sửa thoại*, *đã đổi camera từ medium sang low-angle*, *đã kéo bubble sang phải*, *đã sửa costume trong Story Bible*.

Điều này khớp thẳng với phần PM vừa nâng cấp ở GĐ-2: Nghị định 134/2026/NĐ-CP (theo `researcher` relay: phải lưu prompts, inputs, intermediate drafts để chứng minh đóng góp trí tuệ của con người) khiến **audit trail trở thành nghĩa vụ pháp lý, không còn là tuỳ chọn**. Và toàn bộ cơ chế đó **em đã đề xuất từ trước** dưới dạng dữ liệu, không phải UI: `generation.origin`, `parent_generation` + `relation_kind`, `field_provenance`, `change_log` (§3.2, §8.8). Tức là:

> **Nghĩa vụ pháp lý đặt lên tầng DỮ LIỆU (audit event), không đặt lên tầng CANVAS.** Việc phải làm là bảo đảm mọi hành động của người dùng trong editor đều sinh một `change_log` row — kể cả hành động chỉ là "chọn ảnh này thay vì ảnh kia". Đây là ràng buộc thiết kế mới, và nó **không** đòi canvas.

Vậy nên phản biện bản quyền của PM, khi truy tới cùng, **củng cố** đáp án (c) chứ không bác bỏ nó: thứ phải build là **provenance đầy đủ**, còn hình dạng UI vẫn được tự do chọn cái rẻ.

**Phản biện "editor CHÍNH LÀ sản phẩm": đúng một phần, và đây là chỗ em phải nhượng bộ.** Với SaaS, khách trả tiền cho một trải nghiệm, không cho một CLI. Nhưng đừng suy ra "phải là canvas". Hai lập luận ngược:

1. **Trục cạnh tranh sai.** Dữ liệu PM cấp: đối thủ đang thu $9-10/tháng và đã tồn tại. Một dev đơn lẻ đua độ mượt editor với các team có funding là chọn **trục yếu nhất**. Còn moat mà chính tài liệu §Quyết định kiến trúc xác định — Story Bible + Timeline State + Canonical Reference + Continuity — là trục **không ai làm được rẻ** và là trục duy nhất mà quy mô 1 dev có lợi thế (nó là thiết kế dữ liệu, không phải nhân lực UI).
2. **Cả 3 tương tác §14 nêu ra vẫn không cần canvas.** Lập luận cũ vẫn đứng nguyên và không có gì trong đáp án GATE làm nó yếu đi. `Regenerate` / `Change camera` / `Replace costume` là 3 form action, dù người dùng là anh hay là khách trả tiền.

**Editor tối thiểu cho một SaaS BÁN ĐƯỢC** — đây là phần em nhượng bộ so với khuyến nghị cũ (khuyến nghị cũ chỉ có form/list thuần):

| # | Thành phần | Bắt buộc? | Vì sao | Ước lượng % effort (mẫu số SaaS) |
|---|---|---|---|---|
| 1 | Panel card: form spec + ảnh preview + `Regenerate` + **variant picker** (chọn giữa các generation) | **CÓ** | Chính là vòng lặp iterative. Variant picker là hành động sáng tạo **rẻ nhất mà giá trị pháp lý cao nhất** (chọn = authorship, ghi được vào `change_log`). | 5-7% |
| 2 | **Bubble/text overlay editor trong phạm vi MỘT panel** (kéo bubble, sửa thoại, chọn kiểu bubble, kéo đuôi trỏ) | **CÓ** | Ba lý do độc lập: thoại do người viết là phần **được bảo hộ** (Zarya, theo `researcher`); bubble che mặt là lỗi không thể tự động tránh; và không sửa được thoại thì mọi lần sửa chữ thành một lần regenerate ảnh — đốt tiền. Đây là "canvas bị giới hạn" trong một khung, **không** phải scene graph tự do. | 5-8% |
| 3 | Page: chọn **template layout**, đổi chỗ / swap panel giữa các ô, reorder | **CÓ** | Sắp đặt panel là quyết định sáng tạo của con người (selection & arrangement). Nhưng chỉ cần **rời rạc** (chọn template, swap ô), không cần hình học liên tục. | 3-4% |
| 4 | Preview trang + chapter render **server-side** (composite PNG/PDF), read-only | **CÓ** | Khách phải thấy thành phẩm mới trả tiền. Rẻ vì tái dùng compositor của export (§8.2). | 3-5% |
| 5 | Story Bible editor (form: character, costume, location, state theo event) | **CÓ** | Đây mới là nơi moat lộ ra với khách hàng. Vẫn là form + list. | 4-6% |
| — | **Tổng editor tối thiểu** | | | **~20-25%** |
| 6 | Infinite canvas, zoom/pan cả chapter, hình học panel tự do, panel xoay/không chữ nhật | **HOÃN** | Chi phí lớn nhất, giá trị tăng thêm nhỏ nhất ở bản trả phí đầu. | — |
| 7 | Undo/redo xuyên toàn bộ state phân tán | **HOÃN** | Chỉ làm undo **cục bộ trong form + vị trí bubble** (command pattern, per-page). Không undo qua generation (§5.2 điểm 1). | — |
| 8 | Realtime collaboration / multi-user cùng lúc | **HOÃN** | 1 user = 1 tenant ở bản đầu (xem B2). | — |
| 9 | Inpainting brush / drawing tools | **HOÃN** | Cần nhưng không phải để bán được bản đầu. Lưu ý: khi làm thì phải set `generation.origin='ai_edited'` (§1). | — |

**Ý nghĩa con số:** §14 đầy đủ ≈ 50-60% (mẫu số công cụ cá nhân). Editor tối thiểu ≈ **20-25% mẫu số SaaS**. Dù hai mẫu số khác nhau, kết luận hành động không đổi: **vẫn tiết kiệm được khoảng một nửa effort của hạng mục đắt nhất** — và phần tiết kiệm đó chính là ngân sách để làm khối multi-tenancy ở B2, thứ vốn không có trong kế hoạch cũ.

**Đường nâng cấp không mất mát:** giữ nguyên yêu cầu cũ — layout lưu dưới dạng **toạ độ chuẩn hoá 0-1** trong `page_layout JSONB`, bubble cũng vậy (§8.1). Template chỉ là các preset ghi vào **cùng** schema đó. Nên khi (nếu) lên canvas thật bằng thư viện có sẵn, **không phải migrate dữ liệu** — chỉ thay lớp tương tác. Đây là điều kiện để đáp án (c) không khoá đường tới (b).

### B2. Multi-tenancy — hạng mục `Request.md` không hề nhắc tới

**Ước lượng effort khối multi-tenancy: 15-25% tổng effort SaaS nếu tự viết; 8-12% nếu MUA phần mua được** (ước lượng của em, không phải số ngành). So sánh: pipeline lõi (story → panel → generate → composite) là 35-45%. Tức là multi-tenancy **không nhỏ hơn** phần AI của sản phẩm — đó là điều `Request.md` bỏ sót hoàn toàn.

Nguyên tắc phân bổ cho 1 dev: **mua auth và billing, đừng viết.** Đây là hai hạng mục có sản phẩm chín, rủi ro bảo mật cao, và giá trị khác biệt bằng không. Tự viết auth là cách nhanh nhất để một dev đơn lẻ đốt hai tháng và vẫn có lỗ hổng.

**Phải có ngay ở phiên bản trả phí đầu tiên:**

| Hạng mục | Mức tối thiểu | Ghi chú |
|---|---|---|
| Auth | Mua (managed auth provider). Email + OAuth. | Không tự viết password reset, session, MFA. |
| `tenant_id` mọi bảng + enforcement ở tầng truy cập dữ liệu | **Bắt buộc tuyệt đối** | Xem "không đảo được rẻ" bên dưới. |
| Postgres **RLS** làm lớp phòng thủ thứ hai | Bắt buộc | App-layer filter sẽ có lúc bị lọt (một query quên `WHERE tenant_id`). RLS biến lỗi lập trình thành no-op thay vì rò rỉ dữ liệu chéo tenant. Với 1 dev không có code review, đây là bảo hiểm rẻ nhất tồn tại. |
| Billing + entitlement | Mua (merchant of record càng tốt, để không tự xử thuế). `tier → limits` là **dữ liệu**, không hard-code. | |
| **Hard quota cưỡng chế trước khi enqueue** | Bắt buộc | Xem B4 — đây là nơi mất tiền thật. |
| Per-tenant cost attribution | Bắt buộc | `generation.cost_usd` + `tenant_id`. Không có thì không định giá được. |
| Object storage: prefix `tenant/{tenant_id}/...` + **signed URL có hạn** | Bắt buộc | Không bao giờ public bucket. Ảnh của khách là tài sản của khách. |
| ToS + khách cam kết có quyền với truyện upload + đường DMCA/takedown | Bắt buộc | Đây là cách **chuyển rủi ro** OQ1/A3 sang người upload. Kiến trúc phải đỡ được: lưu provenance của upload (ai, khi nào, IP), bảng `content_report`, và **khả năng hard-delete toàn bộ dữ liệu một tenant**. |
| Abuse controls tối thiểu | Bắt buộc | Giới hạn dung lượng/số upload, rate limit per tenant, và **ghi lại mọi lần provider từ chối vì content policy** (`generation.failure_reason='policy'`) — đó là tín hiệu abuse sớm và gần như miễn phí. |
| Moderation nội dung | Dựa vào safety filter của provider + xử lý báo cáo thủ công | Tự build ML moderation là hố không đáy. Nhưng phải có **quy trình người** và nút suspend tenant. |

**Hoãn được:** SSO/SAML, team/org nhiều thành viên có role, custom domain / white-label, multi-region, fine-tune riêng cho từng tenant, self-serve refund tự động.

**Quyết định ở MVP1 mà sai thì sau không sửa được rẻ** (câu quan trọng thứ hai — trả lời trực tiếp):

1. **`tenant_id NOT NULL` trên MỌI bảng, từ ngày đầu — CÓ, không có ngoại lệ.** Retrofit `tenant_id` vào schema đã có dữ liệu thật là một trong những migration đắt nhất tồn tại: phải sửa mọi bảng, mọi query, mọi index, và **không có cách nào xác minh đã sửa hết** — bỏ sót một chỗ nghĩa là rò rỉ dữ liệu chéo tenant, tức là sự cố tồn vong với một SaaS. Cụ thể về index: `tenant_id` phải là **cột đầu tiên** của mọi composite index, ví dụ index as-of ở §2.2 đổi thành `(tenant_id, character_id, timeline_id, story_order DESC)`. Chọn mô hình **shared database + shared schema + tenant_id + RLS** (không phải schema-per-tenant hay db-per-tenant: hai cái sau nhân chi phí migration lên N lần — thảm hoạ với 1 dev).
2. **`tenant` và `user` là HAI entity riêng ngay từ đầu**, kể cả khi bản đầu là 1:1. `tenant(id, plan, status)`, `user(id, email)`, `membership(tenant_id, user_id, role)`. Mọi dữ liệu nghiệp vụ trỏ `tenant_id`, **không** trỏ `user_id`. Nếu ban đầu gắn dữ liệu vào `user_id`, ngày muốn bán gói team là viết lại toàn bộ authz + migrate quyền sở hữu dữ liệu.
3. **`cost_usd` + `model_id` + `model_version` + `attempt_no` trên `generation` từ generation ĐẦU TIÊN.** Dữ liệu lịch sử không backfill được. Không có nó thì không trả lời được "khách nào lỗ" và không định giá được — đúng vào lúc B4 cho thấy định giá là bài toán sống còn.
4. **Layout key của object storage + phạm vi content-addressing.** Chốt `tenant/{tenant_id}/{sha256}` ngay. Và một điểm tinh tế: **content-address trong phạm vi tenant, KHÔNG dedup chéo tenant.** Dedup chéo tenant nghe như tiết kiệm nhưng tạo hai vấn đề không sửa được: (a) suy ra được tenant khác có cùng asset (rò rỉ thông tin), (b) hai khách cùng "sở hữu" một ảnh, mà quyền tác giả của ảnh đó lại thuộc về đóng góp sáng tạo của **một** người — mâu thuẫn trực tiếp với chính lập luận bản quyền ở B1. Di chuyển hàng triệu object về sau là chậm và dễ sai.
5. **Kỷ luật `ON DELETE CASCADE` + một đường hard-delete tenant đã kiểm thử.** Takedown và yêu cầu xoá dữ liệu sẽ đến. Nếu FK lỏng, xoá một tenant biến thành khảo cổ học thủ công, và sót dữ liệu là rủi ro pháp lý.
6. **`usage_event` append-only từ ngày đầu** (xem B4) — vì mô hình giá **sẽ** đổi, và đổi giá mà không có event thô để tính lại là bế tắc.

### B3. Kiến trúc §12 — monolith còn đúng không?

**MẠNH LÊN, không yếu đi.** Khuyến nghị giữ nguyên và giờ có thêm ba lập luận mới, trong đó một cái ở mức pháp lý:

1. **Multi-tenancy làm việc tách 2 database TỆ HƠN, không trung tính.** Tenant isolation phải cưỡng chế ở **mọi** database — hai DB là hai lần cấu hình RLS, hai lần cơ hội sai. Nghiêm trọng hơn: state resolution (§2.2) là truy vấn **xuyên** Story và Comic. Với hai DB thì nó thành join phía ứng dụng, mà **join phía ứng dụng thì RLS không bảo vệ được** — lớp phòng thủ thứ hai biến mất đúng ở đường dẫn dữ liệu nóng nhất. Đây là lập luận đủ mạnh để một mình nó loại bỏ việc tách DB.
2. **Nghĩa vụ audit (GĐ-2, Nghị định 134/2026) đòi một transaction boundary.** Bản ghi audit và artifact nó chứng minh **phải commit cùng nhau**. Một DB: `INSERT generation` + `INSERT change_log` + `INSERT usage_event` trong một transaction, bất khả phân. Hai DB: audit có thể mất độc lập với thứ nó audit — tức là **audit trail không đáng tin về mặt pháp lý**. Bằng chứng mà có thể thiếu ngẫu nhiên thì không phải bằng chứng.
3. **Ngân sách effort đã bị khối multi-tenancy (B2: 15-25%) ăn mất một phần.** Effort đó phải lấy từ đâu đó. Lấy từ hạ tầng phân tán là lựa chọn hiển nhiên đúng.

Vector DB: **giữ nguyên khuyến nghị bỏ khỏi MVP.** Không có gì trong mô hình SaaS làm nó cần thiết sớm hơn.

**Seam cần chuẩn bị cho lúc phải tách vì lý do KINH TẾ** (khác với lý do kỹ thuật — đây là phần bổ sung mới):

| Seam | Chuẩn bị gì ngay | Vì sao là kinh tế, không phải kỹ thuật |
|---|---|---|
| **Generation worker là process TRIỂN KHAI RIÊNG, cùng codebase** | Hai entrypoint (`api` và `worker`) trên cùng một repo/image, khác command. Chi phí gần bằng 0. | Tải generation biến thiên theo hành vi khách, không theo traffic API. Cần scale số worker replica độc lập theo tiền/quota, và cần worker chết mà **API vẫn sống** (khách vẫn sửa được spec, vẫn xem được trang → vẫn thấy sản phẩm hoạt động → không churn). Đây là seam duy nhất do kinh tế bắt buộc. |
| **Fairness per tenant trong lúc CLAIM job** | Ngay trong câu claim (`FOR UPDATE SKIP LOCKED`) phải có điều kiện giới hạn số job đang chạy của mỗi tenant (`in_flight_per_tenant < N`). | Noisy neighbour: một khách batch cả bộ truyện làm mọi khách khác chờ → churn của người vô can. Nhồi fairness vào queue **sau** khi đã chạy là sửa lại đúng câu SQL nóng nhất, rất dễ sinh deadlock. Làm ngay thì gần như miễn phí. |
| **Adapter mang thêm dữ liệu kinh tế** | Capability manifest (§6.3) bổ sung `cost_per_image`, `tier_allowed`, `is_reproducible`. | Đổi model theo tier khách hàng thành **thay đổi config**, không phải deploy code. Xem B4. |
| **Phục vụ asset qua CDN, không qua app** | Signed URL trỏ CDN ngay từ đầu. | Egress ảnh sẽ là khoản hạ tầng lớn nhất sau inference. Đi qua app thì trả cả compute lẫn egress. |
| **`usage_event` append-only thay vì tăng counter tại chỗ** | Bảng event thô, billing là hàm tổng hợp trên nó. | Mô hình giá **chắc chắn** phải đổi (B4). Có event thô thì đổi giá là viết lại query; chỉ có counter thì là mất dữ liệu vĩnh viễn. |

Không đổi: **không** tách Story/Comic thành service. Ranh giới module + lint rule cấm import chéo vẫn là cách đúng.

### B4. Cơ chế để sống với ràng buộc chi phí

Dữ liệu PM cấp (official, em dùng nguyên): Gemini 3 Pro Image batch **$0.067/ảnh** → 60 ảnh/chapter = **$4,02 @1x / $8,04 @2x**. FLUX.2 pro **$0.03/ảnh** → **$1,80 @1x**. Trần giá đối thủ **$9-10/tháng**.

#### B4.1 Phát hiện trái trực giác: "draft rẻ rồi final đắt" gần như KHÔNG tiết kiệm

Cơ chế ai cũng nghĩ tới đầu tiên là two-pass: draft toàn chapter bằng model rẻ, người duyệt, rồi final chỉ những panel đã duyệt bằng model đắt. Em tính bằng chính số PM cấp:

| Phương án | Phép tính | Tổng /chapter |
|---|---|---|
| Một pass, model đắt, regen 2x | 120 × $0.067 | **$8,04** |
| Two-pass, draft 2x rẻ + final 1x đắt | 120 × $0.030 + 60 × $0.067 = $3,60 + $4,02 | **$7,62** (tiết kiệm chỉ **5%**) |
| Two-pass, draft 2x rẻ + final **1,2x** đắt | $3,60 + 72 × $0.067 = $3,60 + $4,82 | **$8,42** — **ĐẮT HƠN** |
| Điểm hoà vốn | $3,60 overhead ÷ $0.067 ⇒ final regen ≤ 66 ảnh | **≈ 1,1x** |

**Kết luận: two-pass chỉ thắng nếu bước draft kéo tỉ lệ regen ở bước final xuống ≈1,1x hoặc thấp hơn.** Chỉ cần final regen ở mức 1,2x là two-pass **lỗ**. Nguyên nhân: tỉ lệ giá giữa hai model chỉ là 2,2x — quá hẹp để một pass phụ tự trả tiền cho chính nó.

*Giả định của phép tính, nêu rõ:* (a) draft tính đúng giá FLUX.2 pro $0.03, không có bậc giá thấp hơn; (b) **em không biết** hai provider này có tính giá theo resolution hay không — nếu draft ở resolution thấp mà rẻ hơn $0.03 thì cán cân đổi, và điểm hoà vốn dịch có lợi cho two-pass. Cần lens nghiên cứu xác nhận điểm (b) trước khi chốt.

**Hệ quả kiến trúc:** đừng kỳ vọng giải bài toán chi phí bằng **pipeline**. Giải bằng **đo đếm và định giá** — tức là bằng ledger. Two-pass vẫn nên làm, nhưng vì lý do **UX** (thấy layout trước khi trả tiền cho ảnh đẹp) chứ **không phải** vì tiết kiệm; và phải đo mới biết nó tiết kiệm hay không.

#### B4.2 Cơ chế lõi: credit ledger + hold trước khi gọi model

Yêu cầu "cưỡng chế trước khi gọi model, không phải đếm sau" chỉ đạt được bằng **pre-authorization (hold/reserve)**, giống hệt cơ chế authorize/capture của thẻ. Kiểm tra số dư rồi mới gọi (không hold) là một **race**: 10 job đồng thời đều thấy đủ số dư và đều chạy → vượt trần.

```sql
-- Ledger append-only. KHÔNG dùng counter tăng tại chỗ.
CREATE TABLE credit_ledger (
    id          BIGSERIAL PRIMARY KEY,
    tenant_id   UUID NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
    delta       NUMERIC(14,4) NOT NULL,   -- + nạp/grant, - tiêu
    kind        TEXT NOT NULL,            -- 'grant'|'purchase'|'hold'|'settle'|'release'|'refund'|'expire'
    ref_type    TEXT,                     -- 'generation'|'invoice'|'promo'
    ref_id      UUID,
    hold_id     BIGINT REFERENCES credit_ledger(id),  -- settle/release trỏ về hold gốc
    expires_at  TIMESTAMPTZ,              -- CHỈ với kind='hold'
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_ledger_tenant ON credit_ledger (tenant_id, created_at DESC);
CREATE INDEX idx_ledger_hold_open ON credit_ledger (expires_at)
    WHERE kind = 'hold' AND expires_at IS NOT NULL;

-- Số dư vật chất hoá, để lock được và để check constraint chặn âm.
CREATE TABLE tenant_balance (
    tenant_id UUID PRIMARY KEY REFERENCES tenant(id) ON DELETE CASCADE,
    available NUMERIC(14,4) NOT NULL DEFAULT 0,
    held      NUMERIC(14,4) NOT NULL DEFAULT 0,
    CONSTRAINT no_negative CHECK (available >= 0)
);
```

Luồng bắt buộc, **tất cả trong một transaction**:

1. **Enqueue**: `SELECT ... FROM tenant_balance WHERE tenant_id=$1 FOR UPDATE` → nếu `available < estimated_cost` thì **từ chối, không bao giờ gọi model**. Ngược lại: `available -= est`, `held += est`, insert `kind='hold'` + insert `generation(status='pending')` + insert `job` — **một transaction duy nhất**. Đây là chỗ hợp nhất ba việc: transactional enqueue (§4.2), idempotency (§8.5), và hard quota. `CHECK (available >= 0)` là chốt cuối cùng ở tầng DB — dù logic app sai thì DB vẫn không cho vượt trần.
2. **Hoàn tất**: `held -= est`, insert `kind='settle'` với **chi phí thật** (`generation.cost_usd` từ response), chênh lệch trả về `available`.
3. **Fail transient (5xx/429/timeout)**: `release` toàn bộ hold — khách không trả tiền cho lỗi hạ tầng của mình.
4. **Fail permanent (content policy)**: chính sách phải **biểu diễn được** trong ledger (charge hay không là quyết định kinh doanh, nhưng schema phải cho phép cả hai).
5. **Hold reaper — bắt buộc, đừng bỏ:** job crash sau khi hold mà chưa settle thì hold treo **vĩnh viễn** → khách "có credit mà không generate được". Một cron: hold nào `expires_at < now()` thì release + đánh dấu job `failed`. Không có bước này thì thiết kế có một chỗ rỉ chậm, biểu hiện thành ticket support khó hiểu.
6. **Free tier là nghĩa vụ tài chính không giới hạn nếu không chặn ở đúng đây.** Cùng ledger, grant ban đầu, và **không bao giờ cho số dư âm**. Không có cửa nào khác.

`estimated_cost` phải lấy từ **capability manifest của adapter** (`cost_per_image` × số ảnh × hệ số resolution), không hard-code — để đổi provider/giá là đổi config.

#### B4.3 Tỉ lệ regenerate là metric first-class từ MVP0

PM nói đúng: đây là biến quyết định và không có dữ liệu ngành. Kiến trúc phải làm nó **đo được từ ngày đầu**, vì đo muộn nghĩa là định giá trong bóng tối hàng tháng.

Tin tốt: nó **suy ra được** từ những gì em đã đề xuất, không cần cơ chế mới — `panel.approved_generation_id` + `generation.attempt_no` + `relation_kind` + `usage_event`. Cần thêm đúng một rollup:

```sql
CREATE TABLE usage_daily (
    tenant_id        UUID NOT NULL REFERENCES tenant(id) ON DELETE CASCADE,
    day              DATE NOT NULL,
    panels_approved  INT     NOT NULL DEFAULT 0,
    generations_total INT    NOT NULL DEFAULT 0,
    generations_wasted INT   NOT NULL DEFAULT 0,  -- không bao giờ được approve
    cost_usd         NUMERIC(12,4) NOT NULL DEFAULT 0,
    PRIMARY KEY (tenant_id, day)
);
```

Hai yêu cầu về cách đọc chỉ số này:

- **Đo theo PHÂN PHỐI, không đo trung bình.** Báo cáo p50/p90/p99 của `generations_per_approved_panel`. Trung bình sẽ che mất sự thật là vài khách regen 10x — và **giá phải sống được với khách p90**, không phải khách trung bình. Đây là loại sai sót định giá phổ biến nhất.
- **Đo ngay ở MVP0**, khi còn là script chạy tay: chỉ cần ghi mỗi lần generate ra một dòng JSONL kèm `panel_id`, `attempt_no`, `approved`. Không cần database. Đây là **output quan trọng nhất của MVP0 sau câu hỏi consistency** — nó là input trực tiếp cho quyết định định giá.

#### B4.4 Cache/dedup — nói thật về mức tiết kiệm

`compiled_spec_hash` (§6.1) **chính là** cache key đúng (nó bao gồm hash nội dung của từng reference image, nên phát hiện được ref đã đổi — điều mà hash chuỗi prompt không làm được).

```sql
CREATE TABLE generation_cache (
    tenant_id          UUID NOT NULL,
    compiled_spec_hash BYTEA NOT NULL,
    model_id           TEXT  NOT NULL,
    model_version      TEXT  NOT NULL,
    generation_id      UUID  NOT NULL REFERENCES generation(id),
    PRIMARY KEY (tenant_id, compiled_spec_hash, model_id, model_version)
);
```

Đánh giá trung thực về hiệu quả (ước lượng của em, **không có dữ liệu**): **hit rate thấp, cỡ vài % tới ~10%**. Lý do: mỗi panel có spec khác nhau nên hit chủ yếu đến từ chạy lại sau crash, người dùng bấm trùng, và panel establishing lặp lại. **Đừng dựa vào cache để cứu unit economics.**

**Phạm vi cache: theo tenant, KHÔNG chéo tenant** — cùng lý do đã nêu ở B2 điểm 4 (rò rỉ thông tin + mâu thuẫn quyền tác giả).

Hai chỗ dedup **thật sự** ra tiền, và đều đã có trong kiến trúc:

1. **Reference sheet amortization** — ref sheet mỗi nhân vật generate **một lần**, dùng cho hàng trăm panel. Đây là khoản tiết kiệm lớn nhất của cả hệ, và nó là hệ quả trực tiếp của §8 (Character Reference Sheet). Đáng nêu rõ như một cơ chế chi phí, không chỉ như một cơ chế consistency.
2. **Idempotency key** (§8.5) — chặn trả tiền hai lần cho cùng một lần gọi khi worker retry. Không phải tiết kiệm, mà là **chống thất thoát**.

#### B4.5 Phân tầng model theo tier — §16 có đủ không?

**Đủ về mặt cơ chế, và đây là lập luận kinh tế mạnh nhất cho việc xây §16** — mạnh hơn lý do gốc "sau này đổi model dễ hơn". Vì IR là model-agnostic, cùng một panel spec render được bằng model $0.03 (tier rẻ / draft) hoặc $0.067 (tier cao / final) mà **không đụng tới logic hiểu truyện**. Không có §16 thì phân tầng model là fork code, không phải config.

Còn hai khoảng trống phải bít:

1. **`model_policy` là dữ liệu, không phải code:** `model_policy(tier, purpose, model_id, max_refs, resolution)` với `purpose ∈ {draft, final}`. Đổi giá hoặc đổi provider = một UPDATE.
2. **Degradation report phải hướng ra KHÁCH HÀNG, không chỉ hướng dev.** Đây là điểm mới so với §6.3. Model rẻ nhận ít reference hơn → compiler phải drop ref → consistency kém hơn. Nếu không nói rõ, khách tier rẻ sẽ đổ lỗi cho sản phẩm về đúng cái chất lượng họ đã chọn. Hiển thị "*bản này dùng model tiết kiệm, 2/5 reference bị lược — nâng tier để dùng đủ*" biến một khiếu nại thành một **cơ hội upsell**. `generation.degradations JSONB` đã có sẵn; chỉ cần cho nó lộ ra UI.

#### B4.6 Chốt: cái gì phải có trong schema từ NGÀY ĐẦU

Chỉ 9 thứ, tất cả đều rẻ khi làm sớm và rất đắt khi làm muộn:

1. `tenant_id NOT NULL` mọi bảng + là cột **đầu tiên** mọi composite index + RLS.
2. `tenant` / `user` / `membership` tách rời.
3. `credit_ledger` + `tenant_balance` (+ `CHECK available >= 0`) + hold có `expires_at`.
4. `generation`: `cost_usd`, `model_id`, `model_version`, `attempt_no`, `relation_kind`, `origin`, `compiled_spec_hash`, `degradations`.
5. `panel.approved_generation_id`.
6. `usage_event` append-only (billing/metric là hàm tổng hợp trên nó, không phải counter).
7. `job.idempotency_key UNIQUE` + fairness per tenant trong câu claim.
8. Object storage key `tenant/{tenant_id}/{sha256}`, content-address **trong** phạm vi tenant.
9. `change_log` ghi **mọi** hành động người dùng, kể cả "chọn generation X" — đây là nghĩa vụ audit theo GĐ-2, và là bằng chứng authorship theo B1.

Mọi thứ khác (moderation ML, team/role, custom domain, canvas thật, tree view generation) đều thêm sau được mà không phải migrate dữ liệu.
