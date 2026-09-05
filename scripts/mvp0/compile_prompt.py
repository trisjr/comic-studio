# AI Coding
"""
compile_prompt.py
Page Prompt Compiler cho MVP0 — unit sinh anh la CA MOT TRANG (D-1).

⛔ PHAI la code DETERMINISTIC — ⛔ TUYET DOI khong goi LLM/VLM o day.
Nguon: `D-34` / `SRS-FR-17` — cam LLM tai compiler runtime. Ban chat cua
compiler la TRA BANG `field value -> cum tu`, sap thu tu, dedup, xu ly xung
dot theo precedence ladder, va ghi log rang buoc bi drop.

Hai bat bien mang tu `ADR-014` / `SRS-FR-18`:
  1. PRECEDENCE LADDER — identity reference ⛔ KHONG BAO GIO bi drop. Voi page
     prompt, dieu nay nghia la `canonical_reference` cua tung nhan vat luon
     nam trong `conditioning_set` (anh), ⛔ khong bao gio bi cat theo budget.
  2. CONSTRAINT BUDGET — 5-8 rang buoc thi giac duoc ton trong dong thoi
     (`Analysis §5.5`). Vuot budget thi DROP tu duoi len, va GHI LAI cai bi drop.

⭐ Compiler tra ve HAI thu, ⛔ khong phai mot chuoi text:
   `text_prompt` VA `conditioning_set` (anh reference).
   Nguon `D-35` / `SRS-FR-18`: identity reference ⛔ khong duoc canh tranh voi
   mo ta canh trong CUNG mot chuoi text.

D-1: unit sinh anh chuyen sang PAGE-LEVEL (mvp0/prompt-template.txt,
mvp0/prompt-example.yaml). `compile_page(page_doc)` doc CA MOT page YAML
(`page`, `characters`, `panels`, `style`, `text_policy`,
`negative_constraints`) va serialize deterministic thanh MOT prompt tieng
Anh. Compiler nay ⛔ khong biet gi ve story-bible.yaml — page YAML da tu chua
day du du lieu nhan vat can cho MOT trang (D-4).
"""

import re

CONSTRAINT_BUDGET = 8

# ---------------------------------------------------------------------------
# Loc chu thich meta khoi text truoc khi vao prompt.
#
# Vi sao ton tai — bang chung thuc nghiem `run-refs-20260831-223131`: cau chu
# thich "⛔ khong gan cho nguoi phu nu ao trang" trong Story Bible bi dua
# nguyen van vao prompt, va model ve LUON nguoi phu nu ao trang vao ca 3/3
# character sheet cua lam_phu — chu thich chong nham lan gay ra dung loi no
# dinh chong (T2I model khong hieu cau phu dinh).
#
# Story Bible van la NGUON SU THAT va giu nguyen chu thich (chung phuc vu
# nguoi doc va human gate); compiler chiu trach nhiem loc chung khoi prompt.
# Bo pattern duoi day phu 100% cac chuoi ⭐/⛔ da kiem ke co hoc trong
# story-bible + panel-script-ch1/ch2 (dataset DONG cua MVP0, 2026-08-31).
# ---------------------------------------------------------------------------
META_SENTENCE_MARKERS = [
    "⛔",
    "dấu phân biệt", "dau phan biet",
    "phải gắn", "phai gan",
    "đây là mốc", "day la moc",
    "quan trọng nhất", "quan trong nhat",
]
META_CODE_REGEX = re.compile(r"\bG1|\bG-\d|\bMVP\d")


def _is_meta_sentence(sentence):
    lowered = sentence.lower()
    if any(marker in lowered for marker in META_SENTENCE_MARKERS):
        return True
    return bool(META_CODE_REGEX.search(sentence))


def strip_meta(text):
    """Bo cau chu thich meta; giu mo ta thi giac that.

    Cau meta dang `nhan meta: DATA = mapping` giu lai phan data sau dau `:`
    (dau hieu `=`) — vi attribute binding la precedence 1, ⛔ khong duoc mat.
    Ky tu ⭐ tu than vo nghia voi model ⇒ luon bi xoa khoi cau duoc giu.
    """
    pieces = re.split(r"[.;]\s*", (text or "").replace("\n", " "))
    kept = []
    for piece in pieces:
        piece = piece.strip()
        if not piece:
            continue
        if _is_meta_sentence(piece):
            _, colon, tail = piece.partition(":")
            tail = tail.strip()
            if colon and "=" in tail and not _is_meta_sentence(tail):
                kept.append(tail)
            continue
        kept.append(piece)
    cleaned = ". ".join(re.sub(r"⭐+\s*", "", p).strip() for p in kept)
    return f"{cleaned}." if cleaned else ""


# ⭐ Art style CHUẨN: Pure 2D Anime / Manhwa Webtoon (Dark Xianxia Comic Art)
# Van giu lai cho stage `refs` (character sheet) trong run_mvp0.py — page YAML
# tu mang phan `style` rieng nen `compile_page` ⛔ khong dung hang so nay.
BASE_STYLE_CORE = ("2D manhwa webcomic art style, dark xianxia fantasy comic art, graphic novel panel, "
                   "clean sharp black ink lineart, flat cel shading with crisp shadow edges, "
                   "dramatic high contrast, professional digital webtoon illustration, "
                   "no 3D CGI, no 3D render, no 3D Donghua, no volumetric lighting, "
                   "no realistic photography, no 3D game engine")

BASE_STYLE_CHARACTER = (f"{BASE_STYLE_CORE}. Dynamic 2D anime/manhwa character drawing, "
                        "stylized expressive anime face and eyes, natural comic character action pose, "
                        "integrated full background environment. Single narrative comic book panel frame, "
                        "storytelling scene, NOT a character model sheet, NOT multiple angle views, "
                        "NOT standing on blank white background")

BASE_STYLE_SCENERY = (f"{BASE_STYLE_CORE}. Atmospheric establishing scenery and environment comic panel, "
                      "rich environmental depth, detailed landscape architecture and props. "
                      "Pure scenery background comic panel frame, NO humans, NO people, NO characters, "
                      "NO faces in frame")
BASE_STYLE = BASE_STYLE_CHARACTER
BASE_STYLE_IS_MONOCHROME = False


def _clean(value):
    """Chuan hoa MOT field bat ky (str / list / dict / scalar) thanh 1 chuoi.

    Deterministic 100%: chi flatten + strip_meta + sap xep theo thu tu key da
    co san trong dict (Python 3.7+ giu insertion order cua YAML). ⛔ Khong co
    logic sinh ngon ngu, ⛔ khong LLM.
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return strip_meta(value)
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        parts = [_clean(item) for item in value]
        return "; ".join(p for p in parts if p)
    if isinstance(value, dict):
        parts = []
        for key, item in value.items():
            cleaned = _clean(item)
            if cleaned:
                parts.append(f"{key}: {cleaned}")
        return "; ".join(parts)
    return strip_meta(str(value))


def _field(label, value):
    cleaned = _clean(value)
    return f"{label}: {cleaned}" if cleaned else ""


def _join_lines(lines):
    return "\n".join(line for line in lines if line)


def _style_section(style):
    if not style:
        return ""
    lines = [_field(key, value) for key, value in style.items()]
    return _join_lines(["STYLE:", *lines])


def _page_section(page):
    lines = [
        _field("aspect_ratio", page.get("aspect_ratio")),
        _field("target_resolution", page.get("target_resolution")),
        _field("reading_direction", page.get("reading_direction")),
        _field("purpose", page.get("purpose")),
        _field("overall_mood", page.get("overall_mood")),
    ]
    layout = page.get("layout") or {}
    rows = layout.get("rows", [])

    # ⭐ Dem TUONG MINH thay vi de model dem lay danh sach ten panel. Probe
    # `ch01_page001` tren `qwen-image-2.0-pro` ra 8 panel thay vi 5: dung 4
    # row nhung row 2 ve 3 panel (dac ta 2) va row 4 ve 3 panel (dac ta 1).
    # Danh sach `panel_02, panel_03` la thu model phai DEM; mot con so thi
    # ⛔ khong phai. Chi tiet: `mvp0/pages-stage-probe.md`.
    total_panels = sum(len(row.get("panels", [])) for row in rows)
    if total_panels:
        lines.append(f"panel_count: exactly {total_panels} panels on this page, "
                     f"laid out in exactly {len(rows)} horizontal rows.")
    if layout.get("dominant_panel"):
        lines.append(_field("dominant_panel", layout["dominant_panel"]))
    for row in rows:
        panels = row.get("panels", [])
        panel_list = ", ".join(panels)
        lines.append(f"row {row.get('row')}: y {row.get('y')} to "
                     f"{round(row.get('y', 0) + row.get('h', 0), 3)}, "
                     f"exactly {len(panels)} panel(s): {panel_list}")
    return _join_lines(["PAGE:", *lines])


def _continuity_section(continuity):
    if not continuity:
        return ""
    lines = [_field(key, value) for key, value in continuity.items()]
    return _join_lines(["CONTINUITY:", *lines])


def _character_label(char_id, characters_by_id):
    entity = characters_by_id.get(char_id)
    if entity is None:
        return char_id
    name = entity.get("name") or char_id
    return f"{char_id} ({name})"


def _characters_section(characters):
    if not characters:
        return ""
    lines = []
    for character in characters:
        label = _character_label(character.get("id"), {character.get("id"): character})
        parts = [
            _field("silhouette_cue", character.get("silhouette_cue")),
            _field("identity", character.get("identity")),
            _field("appearance", character.get("appearance")),
            _field("outfit", character.get("outfit")),
            _field("personality", character.get("personality")),
            _field("reference_instruction", character.get("reference_instruction")),
        ]
        body = "; ".join(p for p in parts if p)
        lines.append(f"{label} — {body}" if body else label)
    return _join_lines(["CHARACTERS:", *lines])


def _panel_characters_clause(panel_characters, characters_by_id):
    clauses = []
    for entry in panel_characters or []:
        label = _character_label(entry.get("character_id"), characters_by_id)
        fields = {key: value for key, value in entry.items() if key != "character_id"}
        detail = _clean(fields)
        clauses.append(f"{label} — {detail}" if detail else label)
    return "; ".join(clauses)


def _panel_section(panel, characters_by_id):
    lines = [f"panel {panel.get('id')}:"]
    geometry = (f"row {panel.get('row')}, column {panel.get('column')}, "
                f"width {panel.get('relative_width')}, height {panel.get('relative_height')}, "
                f"{panel.get('shape', '')}").strip()
    lines.append(f"  position/size: {geometry}")
    scene_delta = _field("scene_delta", panel.get("scene_delta"))
    if scene_delta:
        lines.append(f"  {scene_delta}")
    chars_clause = _panel_characters_clause(panel.get("characters"), characters_by_id)
    if chars_clause:
        lines.append(f"  characters: {chars_clause}")
    for key in ("camera", "lighting", "effects"):
        clause = _field(key, panel.get(key))
        if clause:
            lines.append(f"  {clause}")
    purpose = _field("panel_purpose", panel.get("panel_purpose"))
    if purpose:
        lines.append(f"  {purpose}")
    return _join_lines(lines)


def _panels_section(panels, characters_by_id):
    if not panels:
        return ""
    blocks = [_panel_section(panel, characters_by_id) for panel in panels]
    return _join_lines(["PANELS:", *blocks])


def _text_policy_section(text_policy):
    if not text_policy:
        return ""
    render = text_policy.get("render_text_in_image", False)
    rule = _clean(text_policy.get("rule"))
    sentence = ("Do not render any text into the image; typeset is a separate overlay stage."
                if not render else "Render text directly into the image.")
    if rule:
        sentence = f"{sentence} {rule}"
    return _join_lines(["TEXT_POLICY:", sentence])


def _negative_section(negative_constraints):
    kept = negative_constraints[:CONSTRAINT_BUDGET]
    dropped = negative_constraints[CONSTRAINT_BUDGET:]
    if not kept:
        return "", dropped
    lines = [_clean(item) for item in kept]
    return _join_lines(["NEGATIVE_CONSTRAINTS:", *lines]), dropped


def compile_page(page_doc):
    """Serialize MOT page YAML (structure = mvp0/prompt-example.yaml) thanh
    (text_prompt, conditioning_set, dropped). ⛔ Khong LLM, ⛔ khong ngau nhien.
    """
    page = page_doc.get("page", {})
    characters = page_doc.get("characters", [])
    panels = page_doc.get("panels", [])
    style = page_doc.get("style", {})
    text_policy = page_doc.get("text_policy", {})
    negative_constraints = page_doc.get("negative_constraints", [])

    characters_by_id = {c["id"]: c for c in characters if c.get("id")}

    negative_section, dropped = _negative_section(negative_constraints)
    sections = [
        _style_section(style),
        _page_section(page),
        _continuity_section(page.get("continuity", {})),
        _characters_section(characters),
        _panels_section(panels, characters_by_id),
        _text_policy_section(text_policy),
        negative_section,
    ]
    text_prompt = "\n\n".join(s for s in sections if s)

    # conditioning_set — thu tu THEO characters, identity reference ⛔ KHONG
    # BAO GIO bi drop theo budget (`ADR-014`/`SRS-FR-18`).
    conditioning_set = [c["canonical_reference"] for c in characters if c.get("canonical_reference")]

    return text_prompt, conditioning_set, dropped
