# Practice Set — Matthew Purcell (63 câu, CCAR-P)

> **Nguồn:** "Claude Certified Architect – Professional: Full Practice Question Set" của **Matthew Purcell**
> (linkedin.com/in/purcellmatthew), viết theo Exam Guide v1.0 (July 2026). Tác giả đã thi đỗ và tự soạn 63 câu
> **nguyên bản** (không phải đề thật), phân bổ theo đúng weight của blueprint.
>
> **Lưu ý bản quyền:** các file ở đây **diễn giải lại đề bằng tiếng Việt** + giải thích của mình, **không chép
> nguyên văn** bộ đề. Muốn làm với wording tiếng Anh gốc (sát format thi thật) thì dùng file PDF gốc lưu ở máy,
> **không commit PDF vào repo**.

## Cách dùng
1. Làm "cold" từng domain (mở file domain, **không** mở `Đáp án & giải thích`), hoặc làm cả 63 câu trong **120 phút** bằng PDF gốc.
2. Tự chấm bằng [bảng đáp án nhanh](#bảng-đáp-án-nhanh) bên dưới.
3. Câu sai → đọc phần giải thích trong file domain → ghi vào [wrong-answers.md](../../exam-prep/wrong-answers.md).
4. Ghi điểm vào [mock-exam-log.md](../../exam-prep/mock-exam-log.md). Mục tiêu: **≥ 75% mỗi domain**.
5. Ôn [decision-patterns.md](decision-patterns.md) — tổng hợp cách tư duy lặp lại xuyên đề.

## Nội dung

| Domain | Weight | Số câu | File |
|--------|-------:|-------:|------|
| D1 Solution Design & Architecture | 17% | 11 | [d1-solution-design-architecture.md](d1-solution-design-architecture.md) |
| D2 Models, Prompting & Context Engineering | 13% | 8 | [d2-models-prompting-context.md](d2-models-prompting-context.md) |
| D3 Integration | 19% | 12 | [d3-integration.md](d3-integration.md) |
| D4 Evaluation, Testing & Optimization | 16% | 10 | [d4-evaluation-testing-optimization.md](d4-evaluation-testing-optimization.md) |
| D5 Governance, Safety & Risk | 14% | 9 | [d5-governance-safety-risk.md](d5-governance-safety-risk.md) |
| D6 Stakeholder Communication & Lifecycle | 14% | 9 | [d6-stakeholder-lifecycle.md](d6-stakeholder-lifecycle.md) |
| D7 Developer Productivity & Operational Enablement | 7% | 4 | [d7-developer-productivity.md](d7-developer-productivity.md) |
| **Tổng hợp tư duy** | | | [decision-patterns.md](decision-patterns.md) |

## 3 dạng câu hỏi
- **Multiple choice** — chọn 1/4. Phổ biến nhất. Distractor hợp lý: phải chọn giữa *good* và *best*.
- **Multiple response** — đề nói rõ chọn mấy đáp án (ở bộ này luôn là 2/5).
- **Scenario matching** — nhiều scenario ngắn, mỗi cái chọn từ cùng một bộ option; **option dùng lại được**, đừng giả định map 1:1.

## Bảng đáp án nhanh

| D1 | Đáp án | D2 | Đáp án | D3 | Đáp án | D4 | Đáp án |
|----|--------|----|--------|----|--------|----|--------|
| 1.1 | B | 2.1 | C | 3.1 | C | 4.1 | D |
| 1.2 | D | 2.2 | A | 3.2 | D | 4.2 | B |
| 1.3 | C | 2.3 | D | 3.3 | A | 4.3 | A |
| 1.4 | A | 2.4 | B | 3.4 | B | 4.4 | C |
| 1.5 | C | 2.5 | A | 3.5 | D | 4.5 | B |
| 1.6 | D | 2.6 | C | 3.6 | A | 4.6 | D |
| 1.7 | B | 2.7 | A, D | 3.7 | C | 4.7 | C |
| 1.8 | A | 2.8 | B, E | 3.8 | B | 4.8 | B, C |
| 1.9 | B, D | | | 3.9 | C, D | 4.9 | A, D |
| 1.10 | C, E | | | 3.10 | A, E | 4.10 | xem dưới |
| 1.11 | xem dưới | | | 3.11 | B, D | | |
| | | | | 3.12 | xem dưới | | |

| D5 | Đáp án | D6 | Đáp án | D7 | Đáp án |
|----|--------|----|--------|----|--------|
| 5.1 | C | 6.1 | B | 7.1 | B |
| 5.2 | D | 6.2 | C | 7.2 | D |
| 5.3 | B | 6.3 | A | 7.3 | A |
| 5.4 | A | 6.4 | D | 7.4 | C, D |
| 5.5 | D | 6.5 | C | | |
| 5.6 | B | 6.6 | A | | |
| 5.7 | C, E | 6.7 | A, C | | |
| 5.8 | B, D | 6.8 | B, E | | |
| 5.9 | xem dưới | 6.9 | xem dưới | | |

**Scenario matching:**
- **1.11:** 1 augmented call · 2 fixed workflow · 3 autonomous agent · 4 multi-agent · 5 augmented call
- **3.12:** 1 MCP · 2 direct API · 3 agent-to-agent · 4 MCP · 5 direct API
- **4.10:** 1 model mismatch · 2 prompt failure · 3 hallucination · 4 model mismatch · 5 hallucination
- **5.9:** 1 guardrail · 2 HITL · 3 monitoring & audit · 4 guardrail · 5 monitoring & audit
- **6.9:** 1 discovery · 2 design · 3 handoff · 4 monitoring & iteration · 5 discovery

## Đánh giá chung về bộ đề
- **Chất lượng tốt**, bám sát blueprint; đáp án của tác giả đều hợp lý — mình **đồng ý với toàn bộ 63 đáp án**.
  Một số chỗ mình bổ sung "góc nhìn thêm" (2.2 min cache length, 2.4 lớp bảo vệ dữ liệu, 4.10 item 5, 1.11 item 1).
- **Độ khó:** phần lớn câu có một đáp án "rõ là best" nếu nắm pattern; distractor chủ yếu là *blind fix*,
  *giáo điều (always/never)*, *làm lén*, hoặc *đúng cho pattern đối lập*. Đề thật có thể gài tinh hơn (hai đáp án
  đều hợp lý) → luôn tự hỏi **"cái nào giải quyết gốc rễ + đúng requirement được nêu?"**.
- **Chủ đề xuất hiện nhiều nhất:** diagnose-first, deterministic control cho guarantee, MCP vs A2A vs direct,
  RAG troubleshooting, HITL placement, evidence-based stakeholder communication.
