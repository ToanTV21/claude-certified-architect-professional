# Domain 3: Integration (19% — domain nặng nhất)

> **Exam view** — dùng khi ôn theo weight. Note chi tiết viết khi học nằm trong
> [`courses/`](../../courses/README.md); file này chỉ index + phần tổng hợp để revise.
> Bảng map đầy đủ: [exam-prep/course-map.md](../../exam-prep/course-map.md)

## Blueprint task → lesson phủ nó
| Task (exam blueprint) | Lesson phủ |
|-----------------------|------------|
| Evaluate tool/agent configuration for capability bloat | [C1.5](../../courses/01-claude-platform-solution-design/notes/05-platform-entry-points.md), [C3.2](../../courses/03-responsible-ai-safety-risk/notes/02-safety-stack-placement.md) |
| Analyze authentication and authorization requirements to identify security gaps | [C2.4](../../courses/02-enterprise-integration-production/notes/04-enterprise-integration-architecture.md), [C3.2](../../courses/03-responsible-ai-safety-risk/notes/02-safety-stack-placement.md) |
| Evaluate accuracy-latency trade-offs and justify configuration decisions | [C1.4](../../courses/01-claude-platform-solution-design/notes/04-model-context-strategy.md), [C2.2](../../courses/02-enterprise-integration-production/notes/02-poc-to-production-checklist.md) |
| Analyze observability challenges and select monitoring strategies at scale | [C2.4](../../courses/02-enterprise-integration-production/notes/04-enterprise-integration-architecture.md), [C5.3](../../courses/05-team-enablement-operational-productivity/notes/03-debugging-operational-support.md) |
| Design a RAG pipeline with appropriate chunking and indexing strategies | [C1.3](../../courses/01-claude-platform-solution-design/notes/03-reference-architecture-patterns.md) |
| Apply retrieval strategies matched to data shape and query pattern | [C1.3](../../courses/01-claude-platform-solution-design/notes/03-reference-architecture-patterns.md) |
| Evaluate connection protocols and select the appropriate integration mechanism (MCP, API/CLI, agent-to-agent) | [C1.5](../../courses/01-claude-platform-solution-design/notes/05-platform-entry-points.md), [C1.6](../../courses/01-claude-platform-solution-design/notes/06-delivery-routes-governance-constraints.md), [C2.4](../../courses/02-enterprise-integration-production/notes/04-enterprise-integration-architecture.md) |
| Evaluate progressive discovery vs. monolithic context strategy | [C1.4](../../courses/01-claude-platform-solution-design/notes/04-model-context-strategy.md) |

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
- Domain nặng nhất (19%) nhưng bị chia nhỏ across course 1, 2, 4 — dễ học sót. Dùng bảng trên để tick đủ.
- Bẫy kinh điển: RAG trả lời sai sau data refresh → soi retrieval/indexing trước, đừng đổ cho model.
- Bẫy kinh điển: retrieval đang làm việc mà **live-state** nên làm (C1.3) — dữ liệu thay đổi liên tục
  thì query hệ thống nguồn, không index rồi retrieve.

## Gap — phần course không phủ, phải tự đọc thêm
- Chi tiết MCP protocol (transport, resource vs. tool vs. prompt): đọc spec MCP.

## Questions / Unclear Points
- ?
