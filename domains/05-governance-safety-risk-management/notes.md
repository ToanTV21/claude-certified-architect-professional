# Domain 5: Governance, Safety & Risk Management (14%)

> **Exam view** — dùng khi ôn theo weight. Note chi tiết viết khi học nằm trong
> [`courses/`](../../courses/README.md); file này chỉ index + phần tổng hợp để revise.
> Bảng map đầy đủ: [exam-prep/course-map.md](../../exam-prep/course-map.md)

## Blueprint task → lesson phủ nó
| Task (exam blueprint) | Lesson phủ |
|-----------------------|------------|
| Implement guardrails and safety controls | [C3.1](../../courses/03-responsible-ai-safety-risk/notes/01-training-vs-application-layer.md), [C3.2](../../courses/03-responsible-ai-safety-risk/notes/02-safety-stack-placement.md) |
| Identify risks, limitations, and failure modes of LLM systems | [C3.1](../../courses/03-responsible-ai-safety-risk/notes/01-training-vs-application-layer.md), [C2.2](../../courses/02-enterprise-integration-production/notes/02-poc-to-production-checklist.md) |
| Apply human-in-the-loop validation strategies | [C3.4](../../courses/03-responsible-ai-safety-risk/notes/04-human-review-routing.md) |
| Ensure compliance with regulations (e.g., GDPR, HIPAA, FedRAMP) | [C3.5](../../courses/03-responsible-ai-safety-risk/notes/05-compliance-control-mapping.md), [C1.6](../../courses/01-claude-platform-solution-design/notes/06-delivery-routes-governance-constraints.md), [C2.4](../../courses/02-enterprise-integration-production/notes/04-enterprise-integration-architecture.md) |
| Address ethical AI considerations (bias, fairness, transparency) | [C3.3](../../courses/03-responsible-ai-safety-risk/notes/03-fairness-transparency-explanations.md) |

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
- Bẫy lớn nhất của cả course 3: **assume Claude enforce 1 rule mà nó chưa bao giờ được cho**.
  Control phải nằm ở application layer.
- Least privilege: gỡ hẳn capability không cần — thêm logging/confirmation chỉ là detective control.
- Hệ thống phải **fail closed**, không fail open (C3.2).
- Compliance = obligation → control → owner → evidence artifact. Thiếu evidence artifact thì không audit được.

## Gap — phần course không phủ, phải tự đọc thêm
- Chi tiết từng regulation (GDPR article, HIPAA safeguard, FedRAMP baseline) course không dạy —
  chỉ cần nhớ *nghĩa vụ nào ép ra control nào*, không cần học thuộc luật.

## Questions / Unclear Points
- ?
