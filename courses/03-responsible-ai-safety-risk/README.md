# Course 3 — Responsible AI, Safety & Risk for Architects (114 min)

> Course 3 / 5 · [Skilljar](https://anthropic-partners.skilljar.com/path/claude-certified-architect-professional/responsible-ai-safety-risk-for-architects)

**About:** What controls stop Claude from refusing a valid request, producing an unfair outcome, or
taking an unapproved action. Safety is a set of controls spanning the request path, each with a
blind spot the next must catch.

**Trọng tâm ôn (VN):** phủ trọn domain 5 (14%). Bẫy lớn nhất: *assuming Claude enforces a rule it
was never given* — control phải nằm ở application layer, không phải "tin model tự biết".

## Lessons

| # | Lesson | Exam domain | Status |
|---|--------|-------------|--------|
| C3.1 | [Model training giảm gì vs. application layer phải enforce gì](notes/01-training-vs-application-layer.md) | D5 | ⬜ |
| C3.2 | [Safety stack: input screening, output screening, tool-call authorization](notes/02-safety-stack-placement.md) | D5 | ⬜ |
| C3.3 | [Fairness & transparency: giải thích cho user / regulator / debug team](notes/03-fairness-transparency-explanations.md) | D5 | ⬜ |
| C3.4 | [Routing decision tới reviewer theo confidence / reversibility / cost](notes/04-human-review-routing.md) | D5 + D1 | ⬜ |
| C3.5 | [Compliance obligation → control → owner → evidence artifact](notes/05-compliance-control-mapping.md) | D5 | ⬜ |

## Exercises
Code thực hành cho course này nằm trong [`exercises/`](exercises/).
