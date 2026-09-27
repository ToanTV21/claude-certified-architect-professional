"""
Build quiz HTML từ PDF gốc của Matthew Purcell (CCAR-P practice set).

Mục đích:
  - Đọc PDF gốc TRÊN MÁY (không commit PDF vào repo), lấy nguyên văn câu hỏi + options tiếng Anh.
  - Ghép với giải thích tiếng Anh tự viết trong explanations_en.json.
  - Đối chiếu đáp án trong JSON với answer key trong PDF (fail nếu lệch).
  - Sinh file HTML self-contained vào thư mục dist/ (đã gitignore, chỉ dùng nội bộ).

Cách chạy:
  python practice-sets/matthew-purcell/quiz/build_quiz.py --pdf "C:/Users/<you>/Downloads/claude-architecture-professional.pdf"

Yêu cầu: có lệnh `pdftotext` (poppler) trong PATH — Git Bash trên Windows thường có sẵn.
"""
import argparse          # parse tham số dòng lệnh (--pdf, --out)
import datetime          # lấy ngày hôm nay để đặt tên file output
import json              # đọc explanations_en.json và nhúng data vào HTML
import re                # regex để parse cấu trúc text của PDF
import shutil            # shutil.which: kiểm tra pdftotext có trong PATH không
import subprocess        # gọi pdftotext để trích text
import sys               # sys.exit khi gặp lỗi validate
from pathlib import Path # thao tác đường dẫn đa nền tảng

# Thư mục chứa script này — mọi file phụ trợ (template, JSON) nằm cùng chỗ
HERE = Path(__file__).resolve().parent

# Tên 7 domain theo exam guide, key là số domain (chữ số đầu của question id)
DOMAINS = {
    "1": "D1 · Solution Design & Architecture",
    "2": "D2 · Models, Prompting & Context",
    "3": "D3 · Integration",
    "4": "D4 · Evaluation, Testing & Optimization",
    "5": "D5 · Governance, Safety & Risk",
    "6": "D6 · Stakeholder & Lifecycle",
    "7": "D7 · Developer Productivity",
}

# Regex nhận diện dòng header câu hỏi, ví dụ "Question 1.9 · Multiple response · select TWO"
RE_QHEAD = re.compile(r"^Question (\d\.\d+) · (.+)$")
# Dòng footer mỗi trang PDF — cần bỏ
RE_FOOTER = re.compile(r"^CCAR-P Practice Questions")
# Dòng header domain ("Domain 2: ...") và dòng tiếp nối "(13%)" — cần bỏ
RE_DOMAIN = re.compile(r"^Domain \d: ")
RE_PCT = re.compile(r"^\(\d+%\)$")
# Dòng bắt đầu một option MC/MR: "A. ...", "B. ..."
RE_OPT = re.compile(r"^([A-E])\. (.*)$")
# Dòng bắt đầu một scenario item: "1. ...", "2. ..."
RE_ITEM = re.compile(r"^(\d)\. (.*)$")
# Dòng bắt đầu một entry trong answer key: "1.9 — Correct: B, D" hoặc "1.11 — 1 → ..." (PDF dùng em dash)
RE_KEY = re.compile(r"^(\d\.\d+) (?:--|—) (.*)$")
# Số lượng đáp án cần chọn trong câu multiple response
WORD2NUM = {"ONE": 1, "TWO": 2, "THREE": 3}


def pdf_to_lines(pdf_path: Path) -> list[str]:
    """Gọi pdftotext (UTF-8, giữ layout) rồi trả về list dòng đã strip + gộp khoảng trắng."""
    if not shutil.which("pdftotext"):
        sys.exit("ERROR: không tìm thấy pdftotext trong PATH (chạy từ Git Bash hoặc cài poppler).")
    # "-" ở cuối = ghi output ra stdout thay vì file
    raw = subprocess.run(
        ["pdftotext", "-enc", "UTF-8", "-layout", str(pdf_path), "-"],
        check=True, capture_output=True,
    ).stdout.decode("utf-8")
    lines = []
    for ln in raw.splitlines():
        # PDF chèn zero-width space sau "A." → xoá để regex option match được
        ln = re.sub(r"[​‌‍﻿]", "", ln)
        # -layout chèn nhiều space để căn cột → gộp về 1 space cho text liền mạch
        ln = re.sub(r"\s+", " ", ln).strip()
        # Bỏ ký tự form-feed / dòng footer / header domain
        if not ln or RE_FOOTER.match(ln) or RE_DOMAIN.match(ln) or RE_PCT.match(ln):
            lines.append("")  # giữ dòng trống làm ranh giới đoạn
            continue
        lines.append(ln)
    return lines


def join_text(parts: list[str]) -> str:
    """Nối các mảnh dòng thành 1 đoạn, bỏ khoảng trắng thừa."""
    return re.sub(r"\s+", " ", " ".join(p for p in parts if p)).strip()


def parse_questions(lines: list[str]) -> list[dict]:
    """Tách phần đề (trước 'Answer Key') thành list question dict nguyên văn."""
    end = next(i for i, l in enumerate(lines) if l.startswith("Answer Key & Rationales"))
    body = lines[:end]

    # Gom các dòng theo từng câu hỏi: blocks = [(qid, header_rest, [lines...])]
    blocks, cur = [], None
    for ln in body:
        m = RE_QHEAD.match(ln)
        if m:
            cur = (m.group(1), m.group(2), [])
            blocks.append(cur)
        elif cur is not None:
            cur[2].append(ln)

    questions = []
    for qid, head, blines in blocks:
        q = {"id": qid, "domain": DOMAINS[qid[0]]}
        if "Scenario matching" in head:
            q.update(parse_matching(blines))
            q["type"] = "matching"
            q["format"] = "Scenario matching"
        else:
            q.update(parse_choice(blines))
            # head dạng "Multiple choice · select ONE"
            fmt, _, sel = head.partition(" · ")
            q["format"] = fmt
            q["select"] = WORD2NUM[sel.split()[-1]]
            q["type"] = "single" if q["select"] == 1 else "multiple"
        questions.append(q)
    return questions


def parse_choice(blines: list[str]) -> dict:
    """Parse câu multiple choice / multiple response: stem + options A..E."""
    stem, options, cur = [], [], None
    for ln in blines:
        m = RE_OPT.match(ln)
        if m:
            cur = [m.group(1), [m.group(2)]]
            options.append(cur)
        elif cur is None:
            stem.append(ln)           # chưa tới option → vẫn là stem
        elif ln:
            cur[1].append(ln)         # dòng tiếp nối của option hiện tại
    return {
        "stem": join_text(stem),
        "options": [{"key": k, "text": join_text(t)} for k, t in options],
    }


def parse_matching(blines: list[str]) -> dict:
    """Parse câu scenario matching: stem + các item 1..N + dòng 'Options: a · b · c'."""
    stem, items, cur, opt_parts = [], [], None, None
    for ln in blines:
        if ln.startswith("Options:"):
            opt_parts = [ln[len("Options:"):]]
            continue
        if opt_parts is not None:
            if ln:
                opt_parts.append(ln)  # dòng Options bị ngắt sang dòng sau
            continue
        m = RE_ITEM.match(ln)
        if m:
            cur = [m.group(2)]
            items.append(cur)
        elif cur is None:
            stem.append(ln)
        elif ln:
            cur.append(ln)
    # Bỏ chuỗi "→ ______" (chỗ điền đáp án trong PDF)
    items = [join_text(p).replace("______", "").strip().rstrip("→").strip() for p in items]
    choices = [c.strip() for c in join_text(opt_parts).split("·")]
    return {"stem": join_text(stem), "items": items, "choices": choices}


def parse_answer_key(lines: list[str]) -> dict:
    """Parse phần 'Answer Key & Rationales' → {qid: {"raw": dòng đáp án, "rationale": ..., "why_not": ...}}."""
    start = next(i for i, l in enumerate(lines) if l.startswith("Answer Key & Rationales"))
    key, cur = {}, None
    for ln in lines[start + 1:]:
        if ln.startswith("How did you go?"):
            break  # hết phần answer key
        m = RE_KEY.match(ln)
        if m:
            cur = {"head": [m.group(2)], "body": []}
            key[m.group(1)] = cur
        elif cur is not None:
            # Đáp án matching ("1 → x; 2 → y ...") hay bị ngắt sang dòng sau; dòng tiếp nối
            # bắt đầu bằng chữ thường (hoặc dòng trước kết thúc bằng "→", vd "4 →" + "MCP server"),
            # còn đoạn rationale bắt đầu bằng số/chữ hoa
            if not cur.get("closed") and "→" in cur["head"][0] and ln and (
                    re.match(r"^[a-z]", ln) or cur["head"][-1].rstrip().endswith("→")):
                cur["head"].append(ln)
            else:
                cur["closed"] = True
                cur["body"].append(ln)
    out = {}
    for qid, c in key.items():
        body = join_text(c["body"])
        rationale, _, why_not = body.partition("Why not the others:")
        out[qid] = {
            "raw": join_text(c["head"]),
            "rationale": rationale.strip(),
            "why_not": why_not.strip(),
        }
    return out


def validate_and_merge(questions: list[dict], key: dict, expl: dict) -> None:
    """Ghép giải thích + đối chiếu đáp án JSON với answer key trong PDF. Lệch → dừng."""
    errors = []
    for q in questions:
        qid = q["id"]
        e = expl.get(qid)
        k = key.get(qid)
        if not e or not k:
            errors.append(f"{qid}: thiếu explanation hoặc answer key")
            continue
        if q["type"] == "matching":
            # Mọi đáp án phải nằm trong bộ choices, số lượng = số item
            if len(e["answer"]) != len(q["items"]):
                errors.append(f"{qid}: số đáp án ({len(e['answer'])}) != số item ({len(q['items'])})")
            for a in e["answer"]:
                if a not in q["choices"]:
                    errors.append(f"{qid}: đáp án '{a}' không có trong choices {q['choices']}")
            # Answer key PDF dạng "1 → x; 2 → y" → kiểm tra mỗi đáp án xuất hiện đúng thứ tự
            pdf_ans = [re.sub(r"^\d+\s*→\s*", "", p.strip()).strip() for p in k["raw"].split(";")]
            if [a.lower() for a in pdf_ans] != [a.lower() for a in e["answer"]]:
                errors.append(f"{qid}: lệch answer key PDF {pdf_ans} vs JSON {e['answer']}")
        else:
            m = re.search(r"Correct: ([A-E](?:, [A-E])*)", k["raw"])
            pdf_ans = m.group(1).split(", ") if m else []
            if sorted(pdf_ans) != sorted(e["answer"]):
                errors.append(f"{qid}: lệch answer key PDF {pdf_ans} vs JSON {e['answer']}")
            if len(e["answer"]) != q["select"]:
                errors.append(f"{qid}: đề yêu cầu chọn {q['select']} nhưng JSON có {len(e['answer'])}")
            if len(q["options"]) < 4:
                errors.append(f"{qid}: parse được quá ít option ({len(q['options'])})")
        # Gắn dữ liệu vào question để nhúng HTML
        q["answer"] = e["answer"]
        q["explanation"] = e["explanation"]
        q["why_not"] = e.get("why_not", {})
        q["tip"] = e.get("tip", "")
        q["author_rationale"] = k["rationale"]
        q["author_why_not"] = k["why_not"]
    if errors:
        sys.exit("VALIDATION FAILED:\n  " + "\n  ".join(errors))


def main():
    # Console Windows mặc định cp1252 → ép stdout/stderr UTF-8 để in được tiếng Việt
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Build CCAR-P practice quiz HTML từ PDF gốc")
    ap.add_argument("--pdf", required=True, type=Path, help="đường dẫn PDF gốc của Matthew Purcell")
    ap.add_argument("--out", type=Path, default=None, help="file HTML output (mặc định dist/quiz-...html)")
    args = ap.parse_args()

    lines = pdf_to_lines(args.pdf)
    questions = parse_questions(lines)
    key = parse_answer_key(lines)
    expl = json.loads((HERE / "explanations_en.json").read_text(encoding="utf-8"))

    if len(questions) != 63:
        sys.exit(f"ERROR: parse được {len(questions)} câu, kỳ vọng 63")
    validate_and_merge(questions, key, expl)

    # Nhúng data vào template; escape "</" để chuỗi JSON không đóng nhầm thẻ <script>
    data = json.dumps(questions, ensure_ascii=False).replace("</", "<\\/")
    html = (HERE / "template.html").read_text(encoding="utf-8").replace("/*__QUIZ_DATA__*/[]", data)

    today = datetime.date.today().strftime("%Y%m%d")
    out = args.out or HERE / "dist" / f"quiz-ccarp-matthew-purcell-{today}.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html, encoding="utf-8")
    print(f"OK: {len(questions)} questions → {out}")


if __name__ == "__main__":
    main()
