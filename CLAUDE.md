# CLAUDE.md — Claude Certified Architect, Professional Study Project

## Project Purpose
Workspace học + ghi chú + làm bài tập để chuẩn bị thi **CCAR-P (Claude Certified Architect –
Professional)**.

**Owner:** ToanTV — Senior Android Automotive Engineer, FPT Software Japan
**Target:** Pass CCAR-P (720/1000)
**Stack:** Python 3.10+, `anthropic` SDK, `python-dotenv`, `mcp`
**Official course path:** https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional
**Official exam guide:** [docs/exam-guide.pdf](docs/exam-guide.pdf)

---

## Directory Layout
```
claudeCertArchitecture_professional/
├── CLAUDE.md                   ← You are here (project context)
├── AGENTS.md                   ← pointer to CLAUDE.md cho agent khác
├── README.md                   ← course progress + domain progress + quick start
├── .env / .env.example
├── .gitignore
├── requirements.txt
├── docs/
│   └── exam-guide.pdf          ← official CCAR-P exam guide (Anthropic)
│
├── courses/                    ← NƠI GHI NOTE CHÍNH khi học (bám 5 module prep course)
│   ├── README.md               ← course path + quy ước ghi note
│   ├── _lesson-template.md
│   ├── 01-claude-platform-solution-design/      (238 min · D1, D2)
│   │   ├── README.md           ← lesson table + status
│   │   ├── notes/              ← 1 file / learning objective (C1.1 … C1.6)
│   │   └── exercises/          ← code thực hành của course này
│   ├── 02-enterprise-integration-production/    (158 min · D4, D3)
│   ├── 03-responsible-ai-safety-risk/           (114 min · D5)
│   ├── 04-stakeholder-engagement-lifecycle-gtm/ (178 min · D6, D3)
│   └── 05-team-enablement-operational-productivity/ (45 min · D7)
│
├── domains/                    ← EXAM VIEW: ôn theo weight (7 domain blueprint)
│   ├── _domain-template.md     ← chỉ index + consolidation, KHÔNG ghi note chi tiết ở đây
│   ├── 01-solution-design-architecture/notes.md
│   ├── 02-models-prompting-context-engineering/notes.md
│   ├── 03-integration/notes.md
│   ├── 04-evaluation-testing-optimization/notes.md
│   ├── 05-governance-safety-risk-management/notes.md
│   ├── 06-stakeholder-communication-lifecycle/notes.md
│   └── 07-developer-productivity-operational-enablement/notes.md
│
├── exam-prep/                  ← Ôn thi CCAR-P
│   ├── README.md               ← bản đồ ôn thi, bắt đầu từ đây
│   ├── study-plan.md           ← 4 phase: course → vá gap → domain → luyện đề
│   ├── course-map.md           ← ánh xạ course ↔ domain (cross-cut, không 1:1)
│   ├── flashcards.md
│   ├── cheat-sheet.md
│   ├── practice-questions.md
│   ├── mock-exam-log.md
│   ├── wrong-answers.md
│   └── references.md
│
└── src/                        ← Shared utilities
    ├── __init__.py
    └── client.py                ← Khởi tạo Anthropic client dùng chung
```

> **Hai góc nhìn, một nội dung:** `courses/` = đang học (note chi tiết theo lesson);
> `domains/` = đang ôn (index + tổng hợp theo weight). Prep course chia 5 module, đề thi chia
> 7 domain — **cross-cut, không map 1:1**. Không duplicate nội dung: viết ở `courses/`, link từ
> `domains/`.

## CCAR-P Exam Overview
- **Exam code:** CCAR-P
- **Format:** 63 câu (multiple-choice / multiple-response), 120 phút, passing score 720/1000
- **Lệ phí:** $175 USD, hiệu lực 12 tháng
- **Domains (theo weight, xem chi tiết ở [exam-prep/cheat-sheet.md](exam-prep/cheat-sheet.md)):**

| Domain | Weight |
|--------|--------|
| Solution Design & Architecture | 17% |
| Claude Models, Prompting & Context Engineering | 13% |
| Integration | 19% |
| Evaluation, Testing & Optimization | 16% |
| Governance, Safety & Risk Management | 14% |
| Stakeholder Communication & Lifecycle Management | 14% |
| Developer Productivity & Operational Enablement | 7% |

- **Đối tượng thi:** solution architect, AI/ML engineer, technical lead, senior software engineer — thiết kế/xây dựng/vận hành production-grade Claude solutions, thường xuyên trao đổi với stakeholder về kiến trúc, bảo mật, compliance.
### Prep Course (Skilljar — 5 module, 733 phút, khoá tuần tự)
| # | Course | Thời lượng | Domain phủ |
|---|--------|-----------:|------------|
| 1 | Claude Platform & Solution Design | 238 min | D1, D2 |
| 2 | Enterprise Integration & Production | 158 min | D4, D3 |
| 3 | Responsible AI, Safety & Risk for Architects | 114 min | D5 |
| 4 | Stakeholder Engagement, Lifecycle & GTM | 178 min | D6, D3 |
| 5 | Team Enablement & Operational Productivity | 45 min | D7 |

Prerequisites Anthropic khuyến nghị: Claude 101 · Claude Code in Action · AI Fluency Foundations.
Chi tiết lesson ↔ domain: [exam-prep/course-map.md](exam-prep/course-map.md).

- **Khác biệt với CCDV-F:** nặng về architecture/design trade-off, governance, và stakeholder communication hơn là chi tiết code — câu hỏi thiên về scenario "chọn giải pháp tốt nhất cho tình huống".

---

## Coding Conventions
### Python Setup
```python
# Mọi script đều dùng pattern này
from dotenv import load_dotenv
import anthropic
import os
load_dotenv()
client = anthropic.Anthropic()  # tự đọc ANTHROPIC_API_KEY từ .env
# Dev: dùng haiku để tiết kiệm cost
# Prod/test: dùng sonnet
MODEL_DEV  = "claude-haiku-4-5"
MODEL_MAIN = "claude-sonnet-4-6"
```

### Key Gotchas (luôn nhớ)
| Gotcha | Đúng | Sai |
|--------|------|-----|
| Least privilege | Gỡ bỏ hẳn capability không cần thiết | Chỉ thêm logging/confirmation |
| Cost + latency cùng lúc | Static content trước + prompt caching | Truncate content cần thiết / downsize model mù quáng |
| RAG trả lời sai sau data refresh | Kiểm tra retrieval/indexing trước | Nghi ngờ model weights/temperature |
| Integration mechanism | MCP cho reusable/maintainable tool access | Hard-code logic vào system prompt |
| Kiến trúc | Chọn pattern theo bài toán: workflow vs. agent | Luôn mặc định dùng agent cho mọi task |

---

## Common Commands
```bash
# Setup
pip install -r requirements.txt
# Run an exercise
python courses/02-enterprise-integration-production/exercises/01_example.py
# Start Claude Code interactive session
claude
# Continue last session
claude --continue
```

---

## AI Behavior in This Project
Khi làm việc trong project này, Claude Code nên:
1. **Ưu tiên dùng `claude-haiku-4-5`** cho các bài tập dev/test để tiết kiệm cost
2. **Luôn dùng `python-dotenv`** để load API key, không bao giờ hardcode
3. **Viết code có comments giải thích** vì đây là môi trường học — mỗi đoạn code, mỗi hàm, và mỗi parameter bên trong đều phải có comment giải thích rõ nó làm gì / dùng để làm gì
4. **Khi ghi note bài học mới** tạo file trong `courses/NN-ten-course/notes/` từ template
   `courses/_lesson-template.md` — **không ghi note chi tiết vào `domains/`**. `domains/NN/notes.md`
   chỉ chứa index (blueprint task → lesson) + phần Consolidation khi ôn; template là
   `domains/_domain-template.md`
5. **Khi tạo bài tập mới** đặt trong đúng `courses/NN-ten-course/exercises/`
6. **Sau khi ghi xong note / làm xong bài tập** cập nhật status ở 3 chỗ: lesson table trong
   `courses/NN/README.md`, course progress table trong `README.md`, và
   `exam-prep/study-plan.md`
6b. **Sau mỗi lần write/edit file** phải `git add` + `git commit` (message ngắn gọn) rồi `git push` lên remote GitHub ngay, không gộp nhiều thay đổi rồi mới commit 1 lần
7. **Ngôn ngữ:**
   - **Khi chat trực tiếp với user:** luôn dùng **tiếng Anh**.
   - **Khi ghi note vào file** (notes.md, comment trong code...): luôn viết phần giải thích bằng **tiếng Việt**. Keyword/thuật ngữ kỹ thuật giữ nguyên **tiếng Anh**, không dịch.
8. **Khi user yêu cầu "giải thích chi tiết code"**, áp dụng đúng format sau:
   - Explain theo **từng đoạn code ngắn** (1 block nhỏ mỗi lần), không giải thích dồn cả file trong 1 đoạn văn dài
   - Với mỗi đoạn: trích lại code block đó trước, rồi giải thích ý nghĩa từng phần/cú pháp bên dưới
   - **User là Senior Android Automotive Engineer, code chính là Java** — khi giải thích cú pháp Python lạ, nếu có khái niệm tương đương trong Java/Android thì đối chiếu ngắn gọn để dễ liên tưởng
   - Kết thúc bằng phần **"Tóm tắt luồng chạy"** ngắn gọn, liệt kê các bước theo thứ tự
   - Nếu file đích là bài tập trong `exercises/`, lưu giải thích vào file `.md` riêng cùng cấp, đặt tên `<tên_file_exercise>_notes.md`, rồi git add/commit/push theo rule 6b
9. **Đặc thù architect-level:** với lesson thuộc domain 1, 3, 5, 6 (design, integration, governance,
   stakeholder), **bắt buộc** điền bảng **Trade-off analysis** (option / khi nào chọn / cost / risk /
   reversal) thay vì chỉ liệt kê fact — exam thi dạng scenario "chọn giải pháp tốt nhất".
   Công thức course dạy khi trình bày trade-off: mỗi option đi kèm **cost + risk + reversal cost**.
10. **Giữ nguyên văn learning objective tiếng Anh** trong mỗi lesson note (mục "Learning objective"),
   không dịch — phần giải thích bên dưới mới viết tiếng Việt. Đây là wording chính thức của course.
11. **Khi note một lesson phủ nhiều domain**, ghi ở `courses/` một lần rồi link từ bảng trong
   `domains/NN/notes.md` — không copy nội dung sang cả hai nơi.

---

## Note-Taking Template
Mỗi lesson note trong `courses/NN-ten-course/notes/` theo cấu trúc
(nguồn: [courses/_lesson-template.md](courses/_lesson-template.md)):
```markdown
# C<N>.<M> — [Tên lesson]
> **Course:** N — [Tên course] · **Exam domain:** D<x> (<weight>%) · **Status:** ⬜ Chưa học
## Learning objective (nguyên văn từ course)
> [paste nguyên văn tiếng Anh, không dịch]
## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- ...
## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
## Gotchas / bẫy hay gặp
- [ ] ...
## Exam tips
- ...
## Code / config snippets
\`\`\`python
# snippet
\`\`\`
## Câu hỏi chưa rõ
- ?
```

Còn `domains/NN-ten-domain/notes.md` chỉ là exam view — xem
[domains/_domain-template.md](domains/_domain-template.md).

## Exercise Template
Mỗi file trong `courses/NN-ten-course/exercises/` theo cấu trúc:
```python
"""
Exercise XX-YY: [Tên bài tập]
Course: [Tên course] · Lesson: C<N>.<M>
Objective: [Mục tiêu]
"""
from dotenv import load_dotenv
import anthropic
load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-4-5"  # dùng haiku cho dev
def main():
    # TODO: implement
    pass
if __name__ == "__main__":
    main()
```
