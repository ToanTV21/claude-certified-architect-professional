# Domain 4: Evaluation, Testing & Optimization (16%)

> **Exam view** — dùng khi ôn theo weight. Note chi tiết viết khi học nằm trong
> [`courses/`](../../courses/README.md); file này chỉ index + phần tổng hợp để revise.
> Bảng map đầy đủ: [exam-prep/course-map.md](../../exam-prep/course-map.md)

## Blueprint task → lesson phủ nó
| Task (exam blueprint) | Lesson phủ |
|-----------------------|------------|
| Define evaluation metrics (accuracy, latency, cost, safety, security) | [C2.1](../../courses/02-enterprise-integration-production/notes/01-success-criteria-eval-suite.md) |
| Design evaluation datasets and test frameworks using mixed methodologies | [C2.1](../../courses/02-enterprise-integration-production/notes/01-success-criteria-eval-suite.md) |
| Conduct A/B testing and iterative improvements | [C2.5](../../courses/02-enterprise-integration-production/notes/05-ab-testing-experiments.md) |
| Diagnose system issues (prompt failure, hallucinations, model mismatch) | [C5.3](../../courses/05-team-enablement-operational-productivity/notes/03-debugging-operational-support.md) |
| Optimize token usage, latency, and cost-performance trade-offs | [C2.2](../../courses/02-enterprise-integration-production/notes/02-poc-to-production-checklist.md), [C2.3](../../courses/02-enterprise-integration-production/notes/03-use-case-sizing-feasibility.md) |
| Monitor system performance using logging and observability tools | [C2.4](../../courses/02-enterprise-integration-production/notes/04-enterprise-integration-architecture.md), [C5.3](../../courses/05-team-enablement-operational-productivity/notes/03-debugging-operational-support.md) |

## Consolidation — điền sau khi học xong các lesson ở trên

### Key concepts phải thuộc
- ...

### Trade-off phải thuộc (dạng câu hỏi scenario)
| Tình huống | Chọn | Vì | Loại trừ option nào & vì sao |
|------------|------|----|------------------------------|
|            |      |    |                              |

### Gotchas
- [ ] ...

### Exam tips
- Câu thần chú của course: **eval được xây trước khi viết dòng code production đầu tiên**, và là
  gate cho mọi thay đổi (model swap, prompt change, architecture change).
- Phân biệt model-based eval vs. code-based eval — biết khi nào dùng cái nào (C2.1).
- Đọc kết quả A/B test **không overclaim**: sample size không đủ thì kết luận là "chưa biết".

## Gap — phần course không phủ, phải tự đọc thêm
- Cách *viết* eval cụ thể course không dạy sâu — tự thực hành trong
  [`courses/02-enterprise-integration-production/exercises/`](../../courses/02-enterprise-integration-production/exercises/).

## Questions / Unclear Points
- ?
