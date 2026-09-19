# Study Plan — CCAR-P

Học **theo course** (path bị khoá tuần tự, phải đi 1 → 5), ôn **theo domain weight**.

## Phase 1 — Đi hết prep course (733 phút video)

| Course | Thời lượng | Domain phủ | Status |
|--------|-----------:|------------|--------|
| 1. [Claude Platform & Solution Design](../courses/01-claude-platform-solution-design/README.md) | 238 min | D1, D2 | ⬜ Todo |
| 2. [Enterprise Integration & Production](../courses/02-enterprise-integration-production/README.md) | 158 min | D4, D3 | ⬜ Todo |
| 3. [Responsible AI, Safety & Risk](../courses/03-responsible-ai-safety-risk/README.md) | 114 min | D5 | ⬜ Todo |
| 4. [Stakeholder Engagement, Lifecycle & GTM](../courses/04-stakeholder-engagement-lifecycle-gtm/README.md) | 178 min | D6, D3 | ⬜ Todo |
| 5. [Team Enablement & Operational Productivity](../courses/05-team-enablement-operational-productivity/README.md) | 45 min | D7 | ⬜ Todo |

**Quy trình mỗi lesson:**
1. Xem lesson → ghi vào `courses/NN-.../notes/<lesson>.md` (tiếng Việt, keyword giữ tiếng Anh)
2. Điền bảng **Trade-off analysis** — bắt buộc với lesson thuộc D1/D3/D5/D6
3. Đổi Status ⬜ → ✅ trong README của course
4. Có gotcha mới → chép lên [cheat-sheet.md](cheat-sheet.md)

> Prerequisites Anthropic khuyến nghị: **Claude 101**, **Claude Code in Action**,
> **AI Fluency Foundations**. Riêng "four properties of generative AI" (dùng ở C1.1 và C2.3)
> đến từ AI Fluency Foundations — course CCAR-P không dạy lại.

## Phase 2 — Vá gap ngoài course

Course không phủ đều 7 domain. Xem cột "Gap" trong [course-map.md](course-map.md) và phần
`## Gap` ở cuối mỗi `domains/NN/notes.md`. Ưu tiên:

| Gap | Weight bị ảnh hưởng | Hành động |
|-----|--------------------:|-----------|
| Prompt engineering chi tiết, prompt caching | D2 — 13% | Đọc docs.anthropic.com |
| Viết eval thực tế (không chỉ biết khi nào dùng) | D4 — 16% | Code trong `courses/02-.../exercises/` |
| Claude Code features chi tiết | D7 — 7% | Đọc Claude Code docs |

## Phase 3 — Ôn theo domain weight (nặng → nhẹ)

Dùng `domains/NN/notes.md` — điền phần **Consolidation** cho từng domain theo thứ tự này:

| # | Domain | Weight | Status |
|---|--------|-------:|--------|
| 3 | [Integration](../domains/03-integration/notes.md) | 19% | ⬜ Todo |
| 1 | [Solution Design & Architecture](../domains/01-solution-design-architecture/notes.md) | 17% | ⬜ Todo |
| 4 | [Evaluation, Testing & Optimization](../domains/04-evaluation-testing-optimization/notes.md) | 16% | ⬜ Todo |
| 5 | [Governance, Safety & Risk Management](../domains/05-governance-safety-risk-management/notes.md) | 14% | ⬜ Todo |
| 6 | [Stakeholder Communication & Lifecycle](../domains/06-stakeholder-communication-lifecycle/notes.md) | 14% | ⬜ Todo |
| 2 | [Claude Models, Prompting & Context Engineering](../domains/02-models-prompting-context-engineering/notes.md) | 13% | ⬜ Todo |
| 7 | [Developer Productivity & Operational Enablement](../domains/07-developer-productivity-operational-enablement/notes.md) | 7% | ⬜ Todo |

## Phase 4 — Luyện đề
[practice-questions.md](practice-questions.md) → [mock-exam-log.md](mock-exam-log.md) →
[wrong-answers.md](wrong-answers.md). Mỗi câu sai phải truy được về đúng 1 lesson trong `courses/`.

## Target
- Pass CCAR-P (720/1000) — deadline: _điền ngày_

## Ghi chú
- D3 (19%) + D1 (17%) = 36% đề — nhưng D3 bị rải across course 1, 2, 4, dễ học sót.
  Dùng bảng "Domain → Course" trong [course-map.md](course-map.md) để tick đủ.
- So với CCA-F/CCDV-F, CCAR-P thiên về trade-off analysis và stakeholder communication hơn code —
  câu hỏi dạng scenario "chọn giải pháp tốt nhất".
