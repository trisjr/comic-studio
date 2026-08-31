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

⭐ PROVIDER VAN HANH tu 2026-08-31: Alibaba Cloud Model Studio, region
Singapore (endpoint `dashscope-intl`) — quyet dinh cua Founder sau khi verify
account va bang gia console. Can cu va gioi han xac minh:
`docs/050-Research/Research-Alibaba-Model-Studio-For-MVP0.md`. ⚠️ Day van la
LUA CHON VAN HANH, ⛔ khong phai chot vendor — `ADR-007` Q4 dat viec chot o
gate cuoi MVP0.

Hai vai tro di HAI DUONG API khac nhau (cang cung co viec tach adapter):
  - Sinh anh: native DashScope API (SDK `dashscope`) — dong Qwen-Image ⛔
    KHONG co duong OpenAI-compatible.
  - VLM select: endpoint OpenAI-compatible (SDK `openai`).

⚠️ Vi sao adapter anh co HAI model id: Alibaba tach text-to-image va edit
thanh hai dong san pham. Stage `refs` khong co anh input ⇒ model t2i; stage
`panels` co 1–3 reference ⇒ model edit (nhan toi da 3 anh input — khop tran
`INV-2`). Dinh tuyen TAT DINH theo hinh dang input, ⛔ KHONG phai
multi-provider fallback (`IP-C8` van giu nguyen).

⚠️ ⛔ KHONG phai abstraction da provider. `Roadmap §3.1` liet ke "viet
abstraction cho provider" la DAU HIEU SOM cua rui ro "spike bien thanh nen
mong". Moi vai tro van la MOT ham goi thang — ⛔ khong interface, ⛔ khong
factory, ⛔ khong class hierarchy. `MVP-Scope §3` A4 = "🟡 1 adapter" tai MVP0.

⚠️⚠️ MODEL ID PHAI VERIFY TRUOC KHI CHAY. Ba hang so duoi day lay ten tu tai
lieu chinh thuc Model Studio, ⛔ chua doi chieu voi console cua account that.
`IP-C3` cam alias kieu `latest` ⇒ khi console co snapshot dated (vi du
`qwen-image-max-2025-12-30`) thi pin snapshot do. Chay `--dry-run` truoc de
kiem prompt ma ⛔ khong ton tien.

Cai dat: pip install dashscope openai
Bien moi truong — nap tu `.env`, xem `.env.example` (⛔ KHONG hardcode —
`security.md` §2):
  DASHSCOPE_API_KEY            key Model Studio region Singapore
  MVP0_IMAGE_PRICE_T2I_USD     gia tham chieu 1 anh cua model t2i
  MVP0_IMAGE_PRICE_EDIT_USD    gia tham chieu 1 anh cua model edit
Gia do Founder doc tu bang gia console — `SRS §5.2` cam bia so ⇒ ⛔ khong co
gia nao hardcode trong file nay. Thieu bien gia: van chay, `cost_usd` ghi
null va `cost_status` danh dau thieu.
"""

import base64
import json
import os
import time
import urllib.request

# ⚠️ PIN TUONG MINH — `D-40`: ghi model_id vao MOI ban ghi. DashScope ⛔ khong
# tra field version rieng; voi Alibaba viec pin nam trong chinh model_id
# (snapshot dated) ⇒ `model_version` ghi null la trung thuc, ⛔ khong bia.
IMAGE_T2I_MODEL_ID = "qwen-image-max"
IMAGE_EDIT_MODEL_ID = "qwen-image-edit-plus"
VLM_MODEL_ID = "qwen3-vl-plus"

# Region Singapore — key Bac Kinh ⛔ KHONG dung duoc voi hai endpoint nay
# (hai region tach key va endpoint).
DASHSCOPE_NATIVE_BASE_URL = "https://dashscope-intl.aliyuncs.com/api/v1"
DASHSCOPE_OPENAI_BASE_URL = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

# Ma tu choi content policy cua DashScope — map thang vao ProviderRefusal de
# caller ghi `refusals.jsonl` (`D-67`). Nguon: bang error code Model Studio.
REFUSAL_ERROR_CODES = {"DataInspectionFailed", "IPInfringementSuspect"}

IMAGE_PRICE_ENV_BY_MODEL = {
    IMAGE_T2I_MODEL_ID: "MVP0_IMAGE_PRICE_T2I_USD",
    IMAGE_EDIT_MODEL_ID: "MVP0_IMAGE_PRICE_EDIT_USD",
}


class ProviderRefusal(Exception):
    """Provider tu choi vi content policy — `D-67` bat GHI LAI moi lan."""


def _api_key():
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        raise RuntimeError("Thieu bien moi truong DASHSCOPE_API_KEY")
    return api_key


def _reference_price_usd(model_id):
    """`[OFF]` `CF-3.4` — gia THAM CHIEU do Founder dien tu console vao .env.

    `cost_usd` ghi lai phai la THUC DO khi co (`D-59`). Thieu gia thi tra
    null — "chua biet" ⛔ khong phai "mien phi", ⛔ KHONG BAO GIO tra 0.
    """
    raw = os.environ.get(IMAGE_PRICE_ENV_BY_MODEL[model_id], "").strip()
    return float(raw) if raw else None


def _to_data_uri(image_bytes):
    encoded = base64.b64encode(image_bytes).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def _raise_unless_ok(response):
    """Phan loai loi native DashScope: content policy ⇒ ProviderRefusal."""
    if response.status_code == 200:
        return
    code = str(getattr(response, "code", "") or "")
    message = str(getattr(response, "message", "") or "")
    detail = f"{code}: {message} (request_id={getattr(response, 'request_id', None)})"
    if code in REFUSAL_ERROR_CODES:
        raise ProviderRefusal(detail)
    raise RuntimeError(f"DashScope tra loi khong thanh cong — {detail}")


def _first_image_url(response):
    for item in response.output.choices[0].message.content:
        if isinstance(item, dict) and item.get("image"):
            return item["image"]
    return None


def _download(url):
    """URL ket qua cua DashScope chi song 24h ⇒ tai bytes ve NGAY tai day."""
    with urllib.request.urlopen(url, timeout=120) as handle:
        return handle.read()


def _call_image_api(model_id, content):
    """Mot loi goi native DashScope, ⛔ khong retry ben trong.

    prompt_extend=False: mac dinh provider bat LLM viet lai prompt — tat de
    `G1` do prompt cua compiler TA, dung tinh than deterministic `D-34`.
    watermark=False: anh vao golden dataset phai sach watermark.
    """
    import dashscope
    from dashscope import MultiModalConversation

    dashscope.base_http_api_url = DASHSCOPE_NATIVE_BASE_URL
    return MultiModalConversation.call(
        api_key=_api_key(),
        model=model_id,
        messages=[{"role": "user", "content": content}],
        result_format="message",
        n=1,
        prompt_extend=False,
        watermark=False,
    )


def generate_candidate(text_prompt, reference_images, candidate_index):
    """Adapter ANH — sinh DUNG MOT candidate. Goi N lan de co N candidate.

    Tra ve dict: bytes anh + metadata bat buoc cua `D-40`/`D-59`.
    ⛔ Nem `ProviderRefusal` khi bi tu choi content policy — caller PHAI ghi lai.
    """
    content = [{"image": _to_data_uri(image)} for image in reference_images]
    content.append({"text": text_prompt})
    model_id = IMAGE_EDIT_MODEL_ID if reference_images else IMAGE_T2I_MODEL_ID

    started = time.time()
    response = _call_image_api(model_id, content)
    _raise_unless_ok(response)

    image_url = _first_image_url(response)
    if image_url is None:
        raise ProviderRefusal("Response ⛔ khong chua anh — nhieu kha nang output bi chan")

    image_bytes = _download(image_url)
    price_usd = _reference_price_usd(model_id)
    return {
        "candidate_index": candidate_index,
        "image_bytes": image_bytes,
        "model_id": model_id,
        "model_version": None,
        "request_id": getattr(response, "request_id", None),
        "latency_s": round(time.time() - started, 2),
        "cost_usd": price_usd,
        "cost_status": "reference_price" if price_usd is not None else "reference_price_missing",
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

    json_object cua DashScope doi message phai chua chu "JSON" — rubric da co
    san. enable_thinking=False vi structured output ⛔ khong ho tro thinking
    mode (tai lieu json-mode cua Model Studio).

    ⛔ Adapter CHI xep hang va giai thich (`D-38`). Viec chon cuoi cung —
    `approved_generation_id` — la cua NGUOI, va chinh la phep do `G1-c`.
    """
    from openai import OpenAI

    client = OpenAI(api_key=_api_key(), base_url=DASHSCOPE_OPENAI_BASE_URL)
    content = [
        {"type": "image_url", "image_url": {"url": _to_data_uri(image)}}
        for image in candidate_images
    ]
    content.append({"type": "text", "text": VLM_RUBRIC.format(
        n=len(candidate_images), spec=panel_spec_text)})

    response = client.chat.completions.create(
        model=VLM_MODEL_ID,
        messages=[{"role": "user", "content": content}],
        response_format={"type": "json_object"},
        extra_body={"enable_thinking": False},
    )

    scoring = json.loads(response.choices[0].message.content)
    scoring["model_id"] = VLM_MODEL_ID
    # Field `model` la ten model DA PHUC VU do endpoint tra ve — bang chung
    # version gan nhat co duoc khi provider khong co field version rieng.
    scoring["model_version"] = getattr(response, "model", None)
    scoring["request_id"] = getattr(response, "id", None)
    usage = getattr(response, "usage", None)
    if usage is not None:
        # "Chi phi VLM per-call" la phan CHUA TINH cua `CF-3.5` (`ADR-007`
        # Consequences) — ghi token tai day de gate cuoi MVP0 co so ma tinh.
        scoring["vlm_tokens"] = {
            "input": getattr(usage, "prompt_tokens", None),
            "output": getattr(usage, "completion_tokens", None),
        }
    return scoring
