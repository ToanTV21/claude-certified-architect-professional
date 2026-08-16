# Claude Certified Architect – Professional (CCAR-P) Study Workspace — ToanTV

Workspace học + ghi chú + làm bài tập chuẩn bị thi **CCAR-P (Claude Certified Architect –
Professional)**.

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

## Domain Progress (theo exam blueprint CCAR-P)

Mỗi domain nằm trong 1 folder riêng dưới `domains/`, gồm `notes.md` (ghi chú lý thuyết)
+ `exercises/` (code thực hành).

| # | Domain folder | Domain | Weight | Status |
|---|----------------|--------|--------|--------|
| 01 | [domains/01-solution-design-architecture](domains/01-solution-design-architecture/notes.md) | Solution Design & Architecture | 17% | ⬜ Todo |
| 02 | [domains/02-models-prompting-context-engineering](domains/02-models-prompting-context-engineering/notes.md) | Claude Models, Prompting & Context Engineering | 13% | ⬜ Todo |
| 03 | [domains/03-integration](domains/03-integration/notes.md) | Integration | 19% | ⬜ Todo |
| 04 | [domains/04-evaluation-testing-optimization](domains/04-evaluation-testing-optimization/notes.md) | Evaluation, Testing & Optimization | 16% | ⬜ Todo |
| 05 | [domains/05-governance-safety-risk-management](domains/05-governance-safety-risk-management/notes.md) | Governance, Safety & Risk Management | 14% | ⬜ Todo |
| 06 | [domains/06-stakeholder-communication-lifecycle](domains/06-stakeholder-communication-lifecycle/notes.md) | Stakeholder Communication & Lifecycle Management | 14% | ⬜ Todo |
| 07 | [domains/07-developer-productivity-operational-enablement](domains/07-developer-productivity-operational-enablement/notes.md) | Developer Productivity & Operational Enablement | 7% | ⬜ Todo |

## Layout

- `domains/` — 1 folder / exam domain: `notes.md` + `exercises/`
- `exam-prep/` — ôn thi CCAR-P — [**bản đồ ôn thi / thứ tự đọc**](exam-prep/README.md) ← bắt đầu từ đây
  ([study plan](exam-prep/study-plan.md),
  [flashcards](exam-prep/flashcards.md),
  [cheat-sheet](exam-prep/cheat-sheet.md),
  [practice questions](exam-prep/practice-questions.md),
  [mock exam log](exam-prep/mock-exam-log.md),
  [wrong answers log](exam-prep/wrong-answers.md),
  [official guide references](exam-prep/references.md))
- `docs/` — official exam guide PDF từ Anthropic
- `src/` — shared utilities (Anthropic client)
