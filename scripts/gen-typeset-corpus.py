# AI Coding
"""
gen-typeset-corpus.py
Sinh corpus tieng Viet cho nghiem thu typeset bat buoc cua MVP0.

Nguon rang buoc — ADR-001 `## Consequences` #5 (nguyen van):
  "corpus tieng Viet gom CA NFC VA NFD, co dau chong (e-hat-sac, u-moc-nga,
   o-moc-nang), render o 300 DPI, kiem tra (a) khong ky tu nao bi tach khoi
   dau cua no khi xuong dong, (b) khong dau nao bi cat cut boi mep bubble,
   (c) chuoi NFD va chuoi NFC tuong duong cho ra CUNG ket qua ngat dong."

Vi sao can script nay: van ban nguon la NFC THUAN (kiem co hoc: t == NFC).
Bien the NFD ⛔ KHONG tu co — phai sinh ra. Go tay hai dang canh nhau la
khong kiem chung duoc, vi chung hien thi GIONG HET nhau.

Cach dung:
    python3 scripts/gen-typeset-corpus.py            # ghi mvp0/typeset-corpus.json
    python3 scripts/gen-typeset-corpus.py --stdout   # in ra man hinh
"""

import io
import sys
import json
import pathlib
import unicodedata

OUTPUT_PATH = pathlib.Path("mvp0/typeset-corpus.json")

# Thoai that, lay tu panel-script.yaml — ⛔ khong bia chuoi test nhan tao.
DIALOGUE_SAMPLES = [
    {"id": "p10-lam-uyen", "panel": 10, "speaker": "lam_uyen", "text": "Ta… Ta đang ở đâu?"},
    {"id": "p17-bach-y-nu", "panel": 17, "speaker": "bach_y_nu", "text": "Phế vật thì không có tư cách sống."},
]

# Ca bien cho tieu chi (a) va (b) — dau chong hai tang, ⛔ khong phai thoai.
EDGE_CASES = [
    {"id": "edge-stacked", "text": "Chiếc thuyền ấy đã cũ, những mảnh ván mục rữa vẫn còn nguyên vẹn."},
    {"id": "edge-triple", "text": "Người ấy khước từ, rồi lặng lẽ rời khỏi chỗ ngồi trước cửa."},
    {"id": "edge-adr-001", "text": "ế ữ ợ — ba ký tự ADR-001 nêu đích danh."},
]


def count_stacked(text):
    """Dem ky tu co >= 2 combining mark (dau chong hai tang)."""
    total = 0
    for char in text:
        decomposed = unicodedata.normalize("NFD", char)
        if sum(1 for c in decomposed if unicodedata.combining(c)) >= 2:
            total += 1
    return total


def build_entry(sample):
    text = sample["text"]
    nfc = unicodedata.normalize("NFC", text)
    nfd = unicodedata.normalize("NFD", text)
    return {
        **sample,
        "nfc": nfc,
        "nfd": nfd,
        "nfc_codepoints": len(nfc),
        "nfd_codepoints": len(nfd),
        "stacked_diacritics": count_stacked(nfc),
        "canonically_equivalent": unicodedata.normalize("NFC", nfd) == nfc,
    }


def main():
    entries = [build_entry(s) for s in DIALOGUE_SAMPLES + EDGE_CASES]

    assert all(e["canonically_equivalent"] for e in entries), "NFD khong tuong duong NFC"
    assert all(e["nfd_codepoints"] > e["nfc_codepoints"] for e in entries), \
        "NFD phai dai hon NFC ve codepoint — neu bang nhau thi chuoi khong co dau"

    corpus = {
        "nguon_rang_buoc": "ADR-001 ## Consequences #5",
        "tieu_chi_nghiem_thu": {
            "a": "Khong ky tu nao bi tach khoi dau cua no khi xuong dong",
            "b": "Khong dau nao bi cat cut boi mep bubble",
            "c": "Chuoi NFD va chuoi NFC tuong duong cho ra CUNG ket qua ngat dong",
        },
        "render_dpi": 300,
        "entries": entries,
    }

    payload = json.dumps(corpus, ensure_ascii=False, indent=2) + "\n"
    if "--stdout" in sys.argv:
        sys.stdout.write(payload)
    else:
        OUTPUT_PATH.write_text(payload, encoding="utf-8")
        print(f"Da ghi {OUTPUT_PATH} — {len(entries)} muc")
        for e in entries:
            print(f"  {e['id']:16s} NFC={e['nfc_codepoints']:3d}  NFD={e['nfd_codepoints']:3d}  "
                  f"dau_chong={e['stacked_diacritics']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
