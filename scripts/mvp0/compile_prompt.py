# AI Coding
"""
compile_prompt.py
Visual Prompt Compiler ban toi gian cho MVP0.

⛔ PHAI la code DETERMINISTIC — ⛔ TUYET DOI khong goi LLM/VLM o day.
Nguon: `D-34` / `SRS-FR-17` — cam LLM tai compiler runtime. Ban chat cua
compiler la TRA BANG `field value -> cum tu`, sap thu tu, dedup, xu ly xung
dot theo precedence ladder, va ghi log rang buoc bi drop.

Hai bat bien mang tu `ADR-014` / `SRS-FR-18`:
  1. PRECEDENCE LADDER — identity reference ⛔ KHONG BAO GIO bi drop.
  2. CONSTRAINT BUDGET — 5-8 rang buoc thi giac duoc ton trong dong thoi
     (`Analysis §5.5`). Vuot budget thi DROP tu duoi len, va GHI LAI cai bi drop.

⭐ Compiler tra ve HAI thu, ⛔ khong phai mot chuoi text:
   `text_prompt` VA `conditioning_set` (anh reference).
   Nguon `D-35` / `SRS-FR-18`: identity reference ⛔ khong duoc canh tranh voi
   mo ta canh trong CUNG mot chuoi text.
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


# Bang tra `field value -> cum tu`. ⛔ Khong sinh dong, ⛔ khong LLM.
CAMERA_SHOT = {
    "extreme_wide": "extreme wide establishing shot",
    "wide": "wide shot",
    "medium_wide": "medium wide shot",
    "medium": "medium shot",
    "full_body": "full body shot",
    "close_up": "close-up",
    "extreme_close_up": "extreme close-up",
}

CAMERA_ANGLE = {
    "low": "low angle, looking up",
    "high": "high angle, looking down",
    "eye": "eye level",
    "dutch": "dutch angle, tilted frame",
}

BEAT_TREATMENT = {
    "establishing": "wide readable composition, environment legible",
    "climax": "dramatic lighting, high contrast, strong silhouette",
    "reaction": "facial expression is the subject, shallow depth",
    "transition": "neutral framing, motion implied",
}

# ⭐ Art style van hanh cho MVP0 — Founder chot 2026-09-01 sau BA vong A/B
# (1: den-trang cu vs manhua mau · 2: manhua mau B vs manga Nhat C theo anh
# tham khao Founder gui · 3: C tuyet doi vs C + "DO TA DI"): chot C + do ta
# di — shonen manga den trang, DUY NHAT mau do mau danh cho yeu to sieu
# nhien (chop do, soi day do so menh, mat phai do). Mo ta DAC TRUNG thi
# giac, ⛔ khong neu ten tac pham/tac gia (tranh `IPInfringementSuspect`).
BASE_STYLE = ("traditional Japanese shonen manga art, black and white ink drawing, "
              "bold confident linework, heavy solid black shadows, screentone halftone shading, "
              "detailed cross-hatching, dynamic speed lines, high contrast monochrome, "
              "a single blood-red spot color reserved strictly for supernatural elements")

# Style den trang ⇒ `palette:` (mau) cua panel bi loai khoi prompt. Bai hoc
# thuc nghiem vong A/B 1: menh de mau trong prompt DE bep tuyen bo den-trang
# va keo anh sang mau lai tap. Mo ta mau trong Story Bible (nau sam, ngoc
# luc...) van giu — model B/W-hoa chung thanh gia tri xam (da verify bang
# anh test lam_phu truoc khi sinh lai refs).
BASE_STYLE_IS_MONOCHROME = True


def _state_description(entity, state_ref):
    """Tra `state_ref` cua panel vao moc trang thai cua nhan vat trong Story Bible."""
    for state in entity.get("trang_thai_theo_thoi_diem", []):
        if state["moc"] == state_ref:
            return state["mo_ta"].replace("\n", " ").strip()
    return None


def _identity_clauses(panel, bible_by_id):
    """Precedence 1 — ⛔ KHONG BAO GIO bi drop khi vuot budget.

    Bac nay chua BA thu, ⛔ khong phai mot:
      1. Canonical reference — nhan dang co dinh cua nhan vat.
      2. Trang thai tai thoi diem panel (`state_ref`) — cung mot nguoi co the
         mac hai bo do khac nhau; bo sai la truot `G1-a`.
      3. `attribute_binding` — gan dung trang phuc/vat pham cho dung nguoi;
         day la TRUC THU HAI cua `G1-d`, va la cho `CF-6.5` bao that bai
         "gan sai ao cho sai nguoi".
    ⛔ Ca ba deu MIEN TRU khoi constraint budget. Cat chung di la cat dung
    thu ma phep do ton tai de do.
    """
    constraints = panel["visual_constraints"]
    state_ref = constraints.get("state_ref")
    clauses = []

    for char_id in panel.get("characters", []):
        entity = bible_by_id.get(char_id)
        if entity is None:
            continue
        ref = entity["canonical_reference"]
        parts = [f"{entity['ten']}: {strip_meta(ref['khuon_mat'])} {strip_meta(ref['toc'])}"]

        state = _state_description(entity, state_ref) if state_ref else None
        parts.append(strip_meta(state if state else ref["trang_phuc"]))

        if "vat_pham" in ref:
            parts.append(strip_meta(ref["vat_pham"]))
        if "dac_diem_khong_doi" in ref:
            parts.append(strip_meta(ref["dac_diem_khong_doi"]))

        clauses.append(" ".join(p for p in parts if p).replace("\n", " ").strip())

    binding = strip_meta(constraints.get("attribute_binding"))
    if binding:
        clauses.append(f"attribute binding — {binding}".replace("\n", " ").strip())

    return clauses


def _scene_clauses(panel):
    """Precedence 2 — mo ta canh. Bi drop TRUOC identity khi vuot budget."""
    camera = panel["camera"]
    clauses = [
        strip_meta(panel["action"]),
        CAMERA_SHOT.get(camera.get("shot"), camera.get("shot", "")),
        CAMERA_ANGLE.get(camera.get("angle"), camera.get("angle", "")),
        BEAT_TREATMENT.get(panel["beat_type"], ""),
    ]
    return [c for c in clauses if c]


def _constraint_clauses(panel):
    """Precedence 3 — rang buoc thi giac. Bi drop DAU TIEN."""
    constraints = panel["visual_constraints"]
    # ⛔ `state_ref` va `attribute_binding` KHONG o day — chung thuoc precedence 1.
    ordered_keys = ["palette", "light_source", "mood", "detail", "scale",
                    "composition", "density", "motion", "pov", "flashback_treatment",
                    "figurant", "content_note"]
    if BASE_STYLE_IS_MONOCHROME:
        ordered_keys = [key for key in ordered_keys if key != "palette"]
    cleaned = [(key, strip_meta(constraints[key])) for key in ordered_keys
               if key in constraints]
    return [f"{key}: {value}".replace("\n", " ").strip()
            for key, value in cleaned if value]


def compile_panel(panel, bible_by_id):
    """Tra ve (text_prompt, conditioning_set, dropped) — ⛔ khong goi model nao."""
    identity = _identity_clauses(panel, bible_by_id)
    scene = _scene_clauses(panel)
    constraints = _constraint_clauses(panel)

    # Constraint budget: identity mien tru, phan con lai bi cat tu duoi len.
    budget_left = max(CONSTRAINT_BUDGET - len(identity), 0)
    kept_tail, dropped = (scene + constraints)[:budget_left], (scene + constraints)[budget_left:]

    seen, ordered = set(), []
    for clause in [BASE_STYLE] + identity + kept_tail:
        if clause not in seen:
            seen.add(clause)
            ordered.append(clause)

    # conditioning_set tach RIENG khoi text_prompt (`D-35`).
    conditioning_set = [
        {"character_id": cid, "role": "identity_reference"}
        for cid in panel.get("characters", [])
        if cid in bible_by_id
    ]

    negative_space = strip_meta(panel.get("negative_space_hint"))
    if negative_space:
        ordered.append(f"leave negative space: {negative_space}")

    return ". ".join(ordered), conditioning_set, dropped
