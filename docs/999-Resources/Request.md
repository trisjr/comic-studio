## 1. Core concept

```text
Novel / Truyện chữ
       │
       ▼
┌─────────────────────┐
│  Story Understanding │
│  Phân tích nội dung  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Story Bible / World  │
│ Nhân vật, bối cảnh,  │
│ trang phục, timeline │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Comic Script Engine  │
│ Chuyển chapter →     │
│ comic script         │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Layout / Panel       │
│ Page → Panel → Shot  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Visual Generation    │
│ Character + Scene +  │
│ Style + Composition  │
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Consistency Check    │
│ Continuity / Style   │
└──────────┬──────────┘
           ▼
        Comic Pages
```

Điểm em muốn nhấn mạnh: **đừng để AI đọc chapter rồi generate ảnh ngay**. Phải có các intermediate representation ở giữa.

---

# 2. Story Bible — trái tim của hệ thống

Mỗi project comic nên có một **Story Bible**.

Ví dụ:

```text
Project
 ├── Story
 ├── Characters
 ├── Locations
 ├── Items
 ├── Costumes
 ├── Relationships
 ├── Timeline
 ├── Visual Style
 └── Comic Chapters
```

### Character

Không chỉ lưu:

```json
{
  "name": "Lâm Phong",
  "age": 24,
  "hair": "black",
  "personality": ["cold", "calm"]
}
```

Mà phải có **version theo timeline**.

Ví dụ:

```text
Lâm Phong

Timeline
─────────────────────────────────
Chapter 01
  Age: 24
  Hair: long black
  Costume: blue robe
  Weapon: none

Chapter 05
  Hair: long black
  Costume: damaged blue robe
  Weapon: sword

Chapter 12
  Hair: tied black hair
  Costume: black battle armor
  Weapon: Crimson Sword
  Injury: scar on left eye
```

Như vậy khi AI xử lý Chapter 12, nó không lấy “character hiện tại” một cách mù quáng mà query:

> Character state tại Chapter 12 / Scene 4

Đây sẽ là một feature **cực kỳ quan trọng**.

---

# 3. Timeline nên là first-class entity

Em thậm chí sẽ không gắn state trực tiếp vào chapter mà tạo một hệ thống:

```text
Timeline
   │
   ├── Event
   │    ├── Character state
   │    ├── Costume state
   │    ├── Location state
   │    └── Relationship state
   │
   └── Chapter
```

Ví dụ:

```text
Event #102

Chapter: 17
Scene: 4
Time: Night
Location: Imperial Palace

Character:
  Lâm Phong
    emotion = angry
    costume = black robe
    injury = left shoulder

Relationship:
  Lâm Phong → Princess
    trust = low
```

Sau này AI có thể hỏi:

> “Ở thời điểm này Lâm Phong đang mặc gì?”

và lấy đúng state.

---

# 4. Novel → Comic Script

Đây nên là một pipeline riêng.

Ví dụ input:

```text
Chapter 18

Lâm Phong bước vào căn phòng.
Hắn nhìn thấy công chúa đang đứng bên cửa sổ...
```

AI không generate ảnh ngay.

Nó convert thành:

```text
Chapter 18
│
├── Scene 01
│   Location: Palace Room
│   Time: Night
│
│   ├── Panel 01
│   │   Shot: Establishing
│   │   Characters: Lâm Phong
│   │   Action: enters room
│   │
│   ├── Panel 02
│   │   Shot: Medium
│   │   Characters: Princess
│   │   Action: standing near window
│   │
│   └── Panel 03
│       Shot: Close-up
│       Characters: Lâm Phong
│       Emotion: surprised
```

Tức là tạo một **Comic Intermediate Representation**.

Đây chính là thứ giúp hệ thống dễ debug và chỉnh sửa.

---

# 5. AI Layout Director

Phần này khá thú vị.

AI không chỉ quyết định:

> “Trang này có 4 panels.”

Nó phải quyết định dựa trên **narrative importance**.

Ví dụ:

### Normal dialogue

```text
┌────────────┬────────────┐
│            │            │
│  Panel 1   │  Panel 2   │
│            │            │
├────────────┼────────────┤
│                         │
│        Panel 3          │
│                         │
└─────────────────────────┘
```

### Action scene

```text
┌─────────────────────────┐
│                         │
│       Panel 1           │
│                         │
├───────────┬─────────────┤
│ Panel 2   │   Panel 3   │
├───────────┴─────────────┤
│                         │
│       BIG ACTION        │
│                         │
└─────────────────────────┘
```

### Emotional climax

Có thể:

```text
┌─────────────────────────┐
│                         │
│                         │
│       FULL PAGE         │
│                         │
│      Character          │
│                         │
│                         │
└─────────────────────────┘
```

AI nên có một **Layout Score**:

```text
Narrative importance      0.95
Emotional intensity       0.88
Action intensity          0.76
Dialogue density          0.20
Visual spectacle          0.91

=> FULL PAGE
```

Từ đó layout engine mới render page.

---

# 6. Panel specification

Mỗi panel nên có schema tương đối chi tiết.

Ví dụ:

```text
Panel
├── Narrative purpose
├── Characters
├── Location
├── Camera
├── Composition
├── Action
├── Emotion
├── Dialogue
├── SFX
├── Lighting
├── Costume state
└── Visual references
```

Ví dụ:

```json
{
  "panel_id": "ch18-sc04-p03",
  "shot": "close_up",
  "camera_angle": "low_angle",
  "characters": ["lam_phong"],
  "emotion": "rage",
  "action": "draws sword",
  "lighting": "moonlight",
  "dialogue": "Ngươi đã phản bội ta.",
  "importance": 0.91
}
```

---

# 7. Style Consistency — đây mới là boss cuối

Nếu chỉ prompt:

> “Generate Lâm Phong in anime style”

thì Chapter 1 và Chapter 30 gần như chắc chắn sẽ có khác biệt.

Em sẽ thiết kế một **Visual Identity System**.

```text
Visual Style
│
├── Global Style
│   ├── Art style
│   ├── Line art
│   ├── Color palette
│   ├── Lighting
│   ├── Rendering
│   └── Camera language
│
├── Character Identity
│   ├── Face embedding/reference
│   ├── Body proportions
│   ├── Hair
│   └── Costume
│
├── Location Identity
│
└── Object Identity
```

---

# 8. Character Reference Sheet

Mỗi nhân vật nên có một **canonical visual representation**.

Ví dụ:

```text
Lâm Phong

[Canonical Portrait]

Face ID
Body ID
Hair ID
Costume ID
Color Palette

Reference Images:
  front
  3/4
  side
  full body
  expression sheet
```

Khi generate panel:

```text
Panel Prompt
     +
Character Reference
     +
Costume Reference
     +
Style Reference
     +
Location Reference
     +
Previous Panel Context
          │
          ▼
      Image Model
```

Chứ không chỉ đưa text prompt.

---

# 9. Có thể chia “identity” và “appearance”

Đây là một abstraction rất đáng làm.

### Identity

Không đổi:

```text
Character ID
Face
Body
Age baseline
Personality
```

### Appearance

Thay đổi theo timeline:

```text
Hair style
Costume
Weapon
Injury
Expression
Accessories
```

Ví dụ:

```text
Character:
    lam_phong

Identity:
    face_v1
    body_v1

Appearance @ Chapter 12:
    hair_v2
    costume_v4
    weapon_v2
    scar_left_eye
```

Nhờ vậy AI có thể hiểu:

> “Đây vẫn là cùng một người, nhưng appearance đã thay đổi.”

---

# 10. Location cũng cần consistency

Không chỉ character.

Ví dụ:

```text
Imperial Palace

Canonical:
  Architecture: Chinese fantasy
  Main colors: red / gold
  Floor: marble
  Windows: circular
  Lighting: warm

Reference:
  exterior
  throne room
  bedroom
  corridor
```

Nếu chapter 1 có cung điện kiểu A, chapter 30 không được tự nhiên biến thành kiểu B.

---

# 11. Generation nên có 3 tầng

Em sẽ không để một model làm tất cả.

### Layer 1 — Semantic AI

Hiểu truyện:

```text
Novel
 ↓
Scenes
 ↓
Events
 ↓
Characters
 ↓
Relationships
```

### Layer 2 — Comic Director

Quyết định:

```text
Scene
 ↓
Page
 ↓
Panel
 ↓
Camera
 ↓
Composition
 ↓
Dialogue
```

### Layer 3 — Image Generator

Chỉ tập trung:

```text
Character
+
Pose
+
Environment
+
Camera
+
Style
+
Lighting
```

Điều này giúp hệ thống dễ thay model.

---

# 12. Một kiến trúc backend khá hợp

Em hình dung:

```text
                    ┌───────────────┐
                    │   Web Editor  │
                    └───────┬───────┘
                            │
                     API / WebSocket
                            │
                ┌───────────▼──────────┐
                │    Comic Studio API  │
                └───────────┬──────────┘
                            │
       ┌────────────────────┼───────────────────┐
       ▼                    ▼                   ▼
 Story Service        Comic Service       Generation Service
       │                    │                   │
       ▼                    ▼                   ▼
 PostgreSQL            PostgreSQL          Job Queue
       │                                        │
       ▼                                        ▼
 Vector DB                              Image Generation
```

Có thể thêm:

```text
Object Storage
     │
     ├── original novels
     ├── generated images
     ├── references
     ├── character sheets
     └── page assets
```

---

# 13. Database model

Một version đơn giản:

```text
Project
 ├── Chapter
 ├── Character
 │    └── CharacterState
 ├── Location
 │    └── LocationState
 ├── Item
 │    └── ItemState
 ├── Event
 ├── Timeline
 ├── ComicPage
 │    └── ComicPanel
 ├── Style
 ├── ReferenceImage
 └── Generation
```

Quan trọng nhất là `Generation`.

Ví dụ:

```text
Generation
├── prompt
├── model
├── model_version
├── seed
├── character_refs
├── style_refs
├── location_refs
├── input_panel
├── output_image
├── parent_generation
└── status
```

Cái này giúp **reproducibility**.

---

# 14. UI em nghĩ sẽ rất hay

Không nên làm UI kiểu “upload truyện → generate”.

Nó nên giống **Figma + comic editor + AI director**.

Layout:

```text
┌──────────────────────────────────────────────────────┐
│ Comic Studio                           Chapter 18    │
├────────────┬─────────────────────────────┬───────────┤
│ Story      │                             │ AI        │
│            │                             │ Director  │
│ Characters │       COMIC CANVAS          │           │
│ Locations  │                             │ Scene     │
│ Timeline   │   ┌──────────┬──────────┐   │ Analysis  │
│ Style      │   │ Panel 1  │ Panel 2  │   │           │
│            │   ├──────────┴──────────┤   │ Layout    │
│            │   │      Panel 3        │   │           │
│            │   └─────────────────────┘   │           │
│            │                             │ Generate  │
└────────────┴─────────────────────────────┴───────────┘
```

User có thể click vào Panel 3:

> Regenerate

hoặc:

> Change camera → Low angle

hoặc:

> Replace character costume

và **không ảnh hưởng các panel khác**.

---

# 15. Một feature rất đáng tiền: Continuity Checker

Sau khi generate, AI kiểm tra:

```text
Panel 7
  Lâm Phong
    ✓ face
    ✓ hair
    ✓ costume
    ✗ sword missing

Panel 8
  Princess
    ✓ face
    ✗ costume mismatch
```

Hoặc:

```text
⚠ Continuity issue

Chapter 18 / Page 12 / Panel 3

Character: Lâm Phong

Expected:
  Costume = Black Robe v2
  Weapon = Crimson Sword

Generated:
  Costume = Blue Robe
  Weapon = Crimson Sword

[Fix automatically]
```

Đây sẽ là một feature rất mạnh khi project bắt đầu scale.

---

# 16. Đừng chỉ dùng prompt — tạo “Visual Prompt Compiler”

Đây là một ý tưởng kiến trúc em khá thích.

Thay vì:

```text
prompt = """
Draw Lâm Phong...
"""
```

hãy có:

```text
Comic Scene
      │
      ▼
Visual Prompt Compiler
      │
      ├── Character Identity
      ├── Character State
      ├── Costume
      ├── Location
      ├── Camera
      ├── Composition
      ├── Lighting
      ├── Style
      └── Continuity constraints
      │
      ▼
Model-specific prompt
```

Tức là hệ thống của mình có một **ngôn ngữ trung gian cho hình ảnh**.

Sau này đổi model image generation cũng dễ hơn rất nhiều.

---

# 17. Pipeline hoàn chỉnh

Nếu gom tất cả lại:

```text
                    NOVEL
                      │
                      ▼
             ┌─────────────────┐
             │ Story Analyzer  │
             └────────┬────────┘
                      │
             ┌────────▼────────┐
             │   Story Bible   │
             │                 │
             │ Characters      │
             │ Locations       │
             │ Items           │
             │ Timeline        │
             └────────┬────────┘
                      │
                      ▼
               Chapter Analyzer
                      │
                      ▼
                 Scene Graph
                      │
                      ▼
               Comic Director
                      │
             ┌────────┴────────┐
             ▼                 ▼
          Page Plan        Panel Script
             │                 │
             └────────┬────────┘
                      ▼
               Visual Compiler
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Character    Location     Style
      Reference    Reference   Reference
          │           │           │
          └───────────┼───────────┘
                      ▼
                Image Generator
                      │
                      ▼
               Continuity Check
                      │
                ┌─────┴─────┐
                │           │
               PASS        FAIL
                │           │
                ▼           ▼
             Final       Regenerate
```

## 18. Nếu làm MVP, em sẽ **không** làm hết ngay

Em sẽ chia thành 4 milestone:

### MVP 1 — Story Intelligence

Làm được:

- Upload/import novel
- Chapter parser
- Character extraction
- Location extraction
- Timeline
- Character state
- Story Bible

**Chưa cần generate ảnh.**

### MVP 2 — Comic Director

```text
Chapter
 ↓
Scene
 ↓
Page
 ↓
Panel
 ↓
Comic Script
```

Có UI cho user chỉnh layout.

### MVP 3 — Visual Generation

```text
Panel
+
Character references
+
Style
+
Location
 ↓
Image
```

Bắt đầu giải bài toán consistency.

### MVP 4 — Production System

Thêm:

- Continuity checker
- Regeneration
- Versioning
- Character sheet
- Style lock
- Seed/model tracking
- Batch generation
- Human approval workflow
- Export PDF/CBZ/Webtoon

---

## Một quyết định kiến trúc em nghĩ nên chốt ngay

**Đừng xem “AI-generated image” là dữ liệu chính.**

Dữ liệu chính phải là:

> **Story → Timeline → Scene → Panel Specification → Visual Specification**

Ảnh chỉ là **output/cache** của specification đó.

Như vậy sau này anh có thể:

```text
                    Panel Specification
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
         Image Model A  Image Model B  Video Model
```

hoặc thay style/model mà **không phải phân tích lại truyện từ đầu**.

Và quan trọng nhất: nếu sau này anh muốn comic-studio chạy hàng trăm chapter, cái giúp nó không “loạn nhân vật” chính là **Story Bible + Timeline State + Canonical References + Visual Prompt Compiler + Continuity Checker**. Đây mới là moat của sản phẩm, chứ không phải bản thân việc gọi image model.
