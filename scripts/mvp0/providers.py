# AI Coding
"""
providers.py
HAI adapter TACH RIENG cho MVP0 — ⛔ khong gop lam mot.

Nguon `ADR-007` Q1: "VLM QA-select la integration THU HAI, RIENG BIET, ⛔ khong
phai mot ham cua adapter anh." Ba ly do van dung du CUNG mot vendor:
  - hai vong doi model version khac nhau ⇒ PIN RIENG (`D-40`, `D-44`/`D-66`);
  - hai duong loi khac nhau — "anh sinh xong nhung cham hong la mot TRANG THAI
    HOP LE", ⛔ khong phai mot that bai chung;
  - hai bang gia khac nhau.

⚠️ ⛔ KHONG phai abstraction da provider. `Roadmap §3.1` liet ke "viet
abstraction cho provider" la DAU HIEU SOM cua rui ro "spike bien thanh nen
mong". Day la MOT ham goi thang cho MOI vai tro — ⛔ khong interface, ⛔ khong
factory, ⛔ khong class hierarchy. `MVP-Scope §3` A4 = "🟡 1 adapter" tai MVP0.

⚠️⚠️ MODEL ID PHAI VERIFY TRUOC KHI CHAY. Hai hang so duoi day lay ten tu
`Analysis-Comic-Studio-Concept §.. bang gia` va `ADR-016`; chung la TEN SAN
PHAM trong tai lieu, ⛔ chua duoc doi chieu voi model id that cua API.
Chay `--dry-run` truoc de kiem prompt ma ⛔ khong ton tien.

Cai dat: pip install google-genai
Bien moi truong: GEMINI_API_KEY  (⛔ KHONG hardcode — `security.md` §2)
"""

import os
import time

# ⚠️ PIN TUONG MINH — `D-40`: ghi model_id + model_version vao MOI ban ghi.
IMAGE_MODEL_ID = "gemini-3-pro-image-preview"
VLM_MODEL_ID = "gemini-3-pro-preview"

# `[OFF]` `CF-3.4` — gia THAM CHIEU. `cost_usd` ghi lai phai la THUC DO khi co,
# ⛔ khong phai so nay (`D-59`).
IMAGE_PRICE_STANDARD_USD = 0.134


class ProviderRefusal(Exception):
    """Provider tu choi vi content policy — `D-67` bat GHI LAI moi lan."""


def _client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Thieu bien moi truong GEMINI_API_KEY")
    from google import genai
    return genai.Client(api_key=api_key)


def generate_candidate(text_prompt, reference_images, candidate_index):
    """Adapter ANH — sinh DUNG MOT candidate. Goi N lan de co N candidate.

    Tra ve dict: bytes anh + metadata bat buoc cua `D-40`/`D-59`.
    ⛔ Nem `ProviderRefusal` khi bi tu choi content policy — caller PHAI ghi lai.
    """
    from google.genai import types

    parts = [types.Part.from_bytes(data=img, mime_type="image/png") for img in reference_images]
    parts.append(types.Part.from_text(text=text_prompt))

    started = time.time()
    try:
        response = _client().models.generate_content(
            model=IMAGE_MODEL_ID,
            contents=parts,
            config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
        )
    except Exception as exc:
        if "safety" in str(exc).lower() or "blocked" in str(exc).lower():
            raise ProviderRefusal(str(exc)) from exc
        raise

    image_bytes = None
    for part in response.candidates[0].content.parts:
        if getattr(part, "inline_data", None):
            image_bytes = part.inline_data.data
            break

    if image_bytes is None:
        raise ProviderRefusal("Response ⛔ khong chua anh — nhieu kha nang bi chan")

    return {
        "candidate_index": candidate_index,
        "image_bytes": image_bytes,
        "model_id": IMAGE_MODEL_ID,
        "model_version": getattr(response, "model_version", None),
        "latency_s": round(time.time() - started, 2),
        "cost_usd": IMAGE_PRICE_STANDARD_USD,
        "cost_status": "reference_price",  # ⚠️ ⛔ chua phai thuc do
    }


VLM_RUBRIC = """Bạn đang chấm {n} ứng viên ảnh cho CÙNG một panel truyện tranh.

Đặc tả panel:
{spec}

Với MỖI ứng viên, chấm hai trục ĐỘC LẬP:
1. identity — có đúng (các) nhân vật theo mô tả không?
2. attribute_binding — trang phục và vật phẩm có gắn ĐÚNG người không?

Trả về JSON: {{"ranking": [chỉ số ứng viên, tốt nhất trước],
"verdicts": [{{"candidate_index": int, "verdict": "pass"|"fail"|"unclear",
"identity_ok": bool, "attribute_binding_ok": bool, "reason": "một câu",
"confidence": 0.0-1.0}}]}}

QUAN TRỌNG: "unclear" là giá trị HẠNG NHẤT. Khi không chắc, hãy trả "unclear" —
TUYỆT ĐỐI KHÔNG ép nó thành "pass" hay "fail"."""


def score_candidates(candidate_images, panel_spec_text):
    """Adapter VLM — nhan TAT CA candidate trong MOT call.

    Day la tieu chi #1 cua `ADR-007` Q5 va la tieu chi LOAI: neu provider chi
    nhan 1 anh/call thi ban chat bai toan doi tu "so sanh N" thanh "cham diem
    tung cai roi so so", va chi phi nhan N.

    ⛔ Adapter CHI xep hang va giai thich (`D-38`). Viec chon cuoi cung —
    `approved_generation_id` — la cua NGUOI, va chinh la phep do `G1-c`.
    """
    from google.genai import types

    parts = [types.Part.from_bytes(data=img, mime_type="image/png") for img in candidate_images]
    parts.append(types.Part.from_text(
        text=VLM_RUBRIC.format(n=len(candidate_images), spec=panel_spec_text)))

    response = _client().models.generate_content(
        model=VLM_MODEL_ID,
        contents=parts,
        config=types.GenerateContentConfig(response_mime_type="application/json"),
    )

    import json
    scoring = json.loads(response.text)
    scoring["model_id"] = VLM_MODEL_ID
    scoring["model_version"] = getattr(response, "model_version", None)
    return scoring
