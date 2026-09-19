# Course ↔ Domain Map — CCAR-P

Prep course chia theo **5 module**, đề thi chia theo **7 domain** — hai cách chia này
**cross-cut**, không map 1:1. Bảng dưới là cầu nối: học theo course, ôn theo domain.

- Course view (nơi ghi note khi học): [`../courses/`](../courses/)
- Domain view (nơi ôn theo weight): [`../domains/`](../domains/)

---

## 1. Course → Domain

| Lesson | Nội dung | Domain |
|--------|----------|--------|
| **C1.1** | Scope: Claude / existing systems / humans; four properties of generative AI | D1 |
| **C1.2** | Augmented call vs. workflow vs. agent (naming the cost of each) | D1 |
| **C1.3** | Reference architecture patterns; retrieval vs. live-state | D1, D3 |
| **C1.4** | Model / context-window / context-strategy; eval là gate trước khi swap model | D2, D4 |
| **C1.5** | Platform entry points (Claude.ai, API, SDK, Claude Code, MCP) + customization layer | D3, D7 |
| **C1.6** | Entry point vs. build-time interface vs. delivery route; governance constraints | D3, D5 |
| **C2.1** | Success criteria + eval suite; model-based vs. code-based eval; eval as gate | D4 |
| **C2.2** | POC-to-production checklist; cost/latency budget; retries, fallbacks, circuit breakers | D1, D4 |
| **C2.3** | Call volume / token / cost estimate; feasibility; boundary conditions | D1 |
| **C2.4** | Compliance, identity (SSO/OAuth), authorization, data handling, observability | D3, D5 |
| **C2.5** | A/B test: hypothesis, metrics, sample size, đọc kết quả không overclaim | D4 |
| **C3.1** | Training reduces X vs. application layer must enforce Y | D5 |
| **C3.2** | Input screening / output screening / tool-call authorization; fail closed | D5 |
| **C3.3** | Unequal outcomes; explanation cho user, regulator, debug team | D5 |
| **C3.4** | Review routing theo confidence, reversibility, cost of wrong answer | D5, D1 |
| **C3.5** | Compliance obligation → control → owner → evidence artifact | D5 |
| **C4.1** | Structured discovery → architectural requirements + documented assumptions | D6, D1 |
| **C4.2** | Trade-off presentation: cost + risk + what a reversal takes | D6 |
| **C4.3** | Lifecycle feedback loop; SLA breach; iterate vs. re-architect; governance checkpoint | D6, D5 |
| **C4.4** | Partner GTM: demo, objection handling, joint scoping với Applied AI team | D6 |
| **C4.5** | Direct API vs. Bedrock vs. Vertex vs. third-party; outcome document | D3, D6 |
| **C5.1** | Shared config, rollout pattern, Skills distribution, spend controls | D7 |
| **C5.2** | AI-assisted dev workflow + review discipline | D7 |
| **C5.3** | Symptom → architecture cause; team self-sufficiency | D7, D4 |

---

## 2. Domain → Course (dùng khi ôn theo weight)

| Domain | Weight | Lessons phủ domain này |
|--------|-------:|------------------------|
| **D1** Solution Design & Architecture | 17% | C1.1, C1.2, C1.3, C2.2, C2.3, C3.4, C4.1 |
| **D2** Claude Models, Prompting & Context Engineering | 13% | C1.4 |
| **D3** Integration | 19% | C1.3, C1.5, C1.6, C2.4, C4.5 |
| **D4** Evaluation, Testing & Optimization | 16% | C1.4, C2.1, C2.2, C2.5, C5.3 |
| **D5** Governance, Safety & Risk Management | 14% | C1.6, C2.4, C3.1, C3.2, C3.3, C3.4, C3.5, C4.3 |
| **D6** Stakeholder Communication & Lifecycle | 14% | C4.1, C4.2, C4.3, C4.4, C4.5 |
| **D7** Developer Productivity & Operational Enablement | 7% | C1.5, C5.1, C5.2, C5.3 |

---

## 3. Khoảng trống cần tự bù

Course không phủ đều 7 domain — những chỗ cần đọc thêm docs ngoài course:

| Domain | Gap | Nguồn bù |
|--------|-----|----------|
| **D2** (13%) | Chỉ có 1 lesson (C1.4). Prompt engineering chi tiết, prompt caching, extended thinking, tool use format | docs.anthropic.com + kiến thức CCA-F/CCDV-F |
| **D4** (16%) | Course thiên về *khi nào* dùng eval; cách viết eval cụ thể phải tự thực hành | `courses/02-.../exercises/` |
| **D7** (7%) | Course 5 chỉ 45 phút; Claude Code features chi tiết tự bù | Claude Code docs |

> Prerequisites Anthropic khuyến nghị (Claude 101, Claude Code in Action, AI Fluency Foundations)
> chính là phần lấp gap D2 — "four properties of generative AI" ở C1.1/C2.3 đến từ
> AI Fluency Foundations, course không dạy lại.
