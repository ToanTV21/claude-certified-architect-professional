# Claude Certified Architect – Professional (CCAR-P) Study Workspace — ToanTV

Workspace học + ghi chú + làm bài tập chuẩn bị thi **CCAR-P (Claude Certified Architect –
Professional)**, bám theo
[prep course chính thức trên Skilljar](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional).

- **Owner:** ToanTV — Senior Android Automotive Engineer, FPT Software Japan
- **Target:** Pass CCAR-P (720/1000)
- **Stack:** Python 3.10+, `anthropic` SDK, `python-dotenv`, `mcp`

Chi tiết layout, conventions, và AI behavior khi làm việc trong project này:
xem [CLAUDE.md](CLAUDE.md).

## Quick Start

```bash
git clone https://github.com/ToanTV21/claude-certified-architect-professional.git
cd claude-certified-architect-professional
pip install -r requirements.txt
cp .env.example .env   # rồi điền ANTHROPIC_API_KEY của bạn
python src/client.py   # health check — in ra response mẫu từ Claude
```

## Hai góc nhìn, một nội dung

| | `courses/` | `domains/` |
|---|---|---|
| Chia theo | 5 course module của prep course | 7 domain của exam blueprint |
| Dùng khi | **đang học** — ghi note theo lesson | **đang ôn** — revise theo weight |
| Nội dung | note chi tiết, trade-off table, code | index link sang lesson + phần tổng hợp |

Hai cách chia này cross-cut, không map 1:1 → bảng nối:
[**exam-prep/course-map.md**](exam-prep/course-map.md).

## Course Progress (prep course — 5 module, 733 phút)

Path bị khoá tuần tự: phải hoàn thành course trước mới mở được course sau.

| # | Course | Thời lượng | Domain phủ | Status |
|---|--------|-----------:|------------|--------|
| 1 | [Claude Platform & Solution Design](courses/01-claude-platform-solution-design/README.md) | 238 min | D1, D2 | ⬜ Todo |
| 2 | [Enterprise Integration & Production](courses/02-enterprise-integration-production/README.md) | 158 min | D4, D3 | ⬜ Todo |
| 3 | [Responsible AI, Safety & Risk for Architects](courses/03-responsible-ai-safety-risk/README.md) | 114 min | D5 | ⬜ Todo |
| 4 | [Stakeholder Engagement, Lifecycle & GTM](courses/04-stakeholder-engagement-lifecycle-gtm/README.md) | 178 min | D6, D3 | ⬜ Todo |
| 5 | [Team Enablement & Operational Productivity](courses/05-team-enablement-operational-productivity/README.md) | 45 min | D7 | ⬜ Todo |

> **Prerequisites** Anthropic khuyến nghị học trước: Claude 101 · Claude Code in Action ·
> AI Fluency Foundations.

## Domain Progress (exam blueprint — dùng khi ôn)

| # | Domain | Weight | Status |
|---|--------|-------:|--------|
| 03 | [Integration](domains/03-integration/notes.md) | 19% | ⬜ Todo |
| 01 | [Solution Design & Architecture](domains/01-solution-design-architecture/notes.md) | 17% | ⬜ Todo |
| 04 | [Evaluation, Testing & Optimization](domains/04-evaluation-testing-optimization/notes.md) | 16% | ⬜ Todo |
| 05 | [Governance, Safety & Risk Management](domains/05-governance-safety-risk-management/notes.md) | 14% | ⬜ Todo |
| 06 | [Stakeholder Communication & Lifecycle Management](domains/06-stakeholder-communication-lifecycle/notes.md) | 14% | ⬜ Todo |
| 02 | [Claude Models, Prompting & Context Engineering](domains/02-models-prompting-context-engineering/notes.md) | 13% | ⬜ Todo |
| 07 | [Developer Productivity & Operational Enablement](domains/07-developer-productivity-operational-enablement/notes.md) | 7% | ⬜ Todo |

## Layout

- `courses/` — **nơi ghi note khi học**: 1 folder / course module, gồm `README.md` +
  `notes/<lesson>.md` + `exercises/`
- `domains/` — exam view: 1 `notes.md` / domain, index sang lesson + phần consolidation
- `exam-prep/` — ôn thi — [**bản đồ ôn thi / thứ tự đọc**](exam-prep/README.md) ← bắt đầu từ đây
  ([study plan](exam-prep/study-plan.md),
  [course ↔ domain map](exam-prep/course-map.md),
  [flashcards](exam-prep/flashcards.md),
  [cheat-sheet](exam-prep/cheat-sheet.md),
  [practice questions](exam-prep/practice-questions.md),
  [mock exam log](exam-prep/mock-exam-log.md),
  [wrong answers log](exam-prep/wrong-answers.md),
  [official guide references](exam-prep/references.md))
- `docs/` — official exam guide PDF từ Anthropic
- `src/` — shared utilities (Anthropic client)
