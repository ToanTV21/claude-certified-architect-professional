# Decision patterns rút ra từ 63 câu (Matthew Purcell set)

> Tổng hợp **cách tư duy** lặp lại xuyên suốt bộ đề — học cái này quan trọng hơn thuộc đáp án.
> Mỗi pattern có link về câu minh hoạ.

## 1. Meta-rules khi làm bài CCAR-P

| # | Rule | Câu minh hoạ |
|---|------|--------------|
| M1 | **Diagnose before treating** — câu hỏi "làm gì *first*" khi có sự cố → đo đạc / xem trace / audit trước khi sửa | [3.2](d3-integration.md), [4.5](d4-evaluation-testing-optimization.md), [4.9](d4-evaluation-testing-optimization.md), [7.3](d7-developer-productivity.md) |
| M2 | **Blind fix luôn sai**: "upgrade model", "giảm temperature", "viết CHỮ HOA", "prompt dài hơn" hiếm khi là đáp án đúng nếu chưa chẩn đoán | 1.3, 1.6, 2.4, 3.2 |
| M3 | Đáp án chứa **"always / never / platform-wide / all traffic at once"** thường sai; đáp án đúng hay có **"selectively / gradually / based on measured…"** | 2.3, 3.6, 4.4, 4.6 |
| M4 | Đề nêu **2 vấn đề** → chọn đáp án giải được **cả hai** | 2.6 |
| M5 | Đề liệt kê **"X, Y, Z không đổi"** → loại đáp án đổ lỗi cho X, Y, Z | 4.9 |
| M6 | Đề cho **số liệu** → làm phép tính (1.6s + 0.5s vs SLA 3s) | 3.6 |
| M7 | Câu multiple-response hay ghép **2 đáp án đúng + 3 đáp án "đúng cho pattern đối lập"** | 1.9, 1.10 |
| M8 | Câu hỏi về **phase X** → loại mọi đáp án là output của phase sau | 6.7 |
| M9 | Đáp án có **"silently / quietly"** → sai (domain 6) | 6.3, 6.8 |
| M10 | Requirement là **"guarantee / never / must not"** → cần cơ chế **deterministic** (code, access control, guardrail), không phải prompt | 1.4, 3.3, 5.7, 5.9 |

## 2. Chọn pattern kiến trúc

```
Task là 1 phép biến đổi + context?        → single augmented LLM call   (1.11-1,5)
Các bước biết trước, cố định, cần audit?  → fixed workflow              (1.1, 1.9, 1.11-2)
Path chỉ lộ ra khi đang làm?              → autonomous agent            (1.2, 1.11-3)
Nhiều chuyên môn/tool/context khác nhau
  hoặc sub-task độc lập chạy song song?   → multi-agent                 (1.10, 1.11-4)
  + cần thứ tự/audit/halt?                → supervisor/orchestrator     (1.4)
Một agent quá tải nhiều domain?           → split theo domain + router  (1.8)
```
**Không phải lý do chọn multi-agent:** volume cao, ngân sách lớn, stakeholder muốn "xịn" (1.10).

## 3. Integration

| Nhu cầu | Chọn | Câu |
|---------|------|-----|
| Nhiều app dùng chung, team khác nhau sở hữu, tool thay đổi, cần discover | **MCP server** | 3.1, 3.12 |
| Deterministic, scope hẹp, pipeline tự sở hữu, không cần discovery | **Direct API** | 3.12 |
| Agent ↔ agent **xuyên tổ chức**, không lộ nội bộ | **Agent-to-agent protocol** | 3.8, 3.12 |
| Tool chọn nhầm | Làm rõ description + gộp/gỡ tool chồng lấn | 3.10 |
| Quá nhiều tool | Audit & remove → progressive discovery | 3.2, 3.11 |
| "Ai được thấy gì" | **Access control ở system layer** (scoped credential / pass-through auth), **không phải prompt** | 3.3 |

## 4. RAG

| Triệu chứng | Fix | Câu |
|-------------|-----|-----|
| Data thay đổi hằng ngày | RAG, không fine-tune | 1.7 |
| Context stuffing → lost in the middle + đắt | Retrieve section liên quan | 2.6 |
| Chunk mất nghĩa (definition, cross-ref) | Structure-aware chunking + metadata liên kết | 3.4 |
| Exact ID/mã fail với vector search | Hybrid (keyword + semantic) | 3.5 |
| Trả lời nội dung cũ sau refresh | Re-index pipeline có validate + version metadata filter | 3.9 |
| Muốn cảnh báo sớm | Retrieval relevance + grounding rate (leading indicator) | 4.7 |

## 5. Prompting & context

- **Caching:** static first, dynamic last — giá trị động ở đầu = hit rate 0 (2.2).
- **Rule quan trọng:** đầu hoặc cuối, tách khỏi reference content bằng cấu trúc (2.4, 2.8).
- **Format chính xác:** few-shot example hoàn chỉnh (2.5). **Coverage/bỏ sót:** decomposition (1.3).
- **CoT:** chỉ cho multi-step reasoning (2.3).
- **Giảm cost:** caching + load instruction on-demand (Skills) (2.7); phân tích trace trước khi downsize (4.5).
- **Model:** smallest model that meets the eval target + ongoing eval (2.1).

## 6. Evaluation

| Câu hỏi | Trả lời | Câu |
|---------|---------|-----|
| "Good enough to launch?" | Task-specific metric gắn business outcome + ngưỡng thống nhất | 4.1 |
| Dataset | Query thật + edge case dựng có chủ đích | 4.2 |
| Chủ quan ở scale | LLM-as-judge + human calibration | 4.3 |
| Offline thắng → production? | A/B trên một phần traffic + guardrail metric | 4.4 |
| Đổi model version | Full eval suite → canary → cutover | 4.6 |
| Regulated pre-prod | Golden dataset (expert label) + adversarial test | 4.8 |
| Phân loại lỗi | Capability gap → *model mismatch* · instruction xung đột → *prompt failure* · bịa → *hallucination* | 4.10 |

## 7. Governance & safety

| Rủi ro | Control | Câu |
|--------|---------|-----|
| Hành động irreversible/high-impact | HITL **trước** hành động đó, không phải mọi hành động | 5.1 |
| Personal data rời boundary | Redact/pseudonymise tại nguồn (data minimisation) | 5.2 |
| PHI / regulated data | Compliance cho **toàn bộ data path** (kể cả logging, subprocessor) quyết định từ đầu | 5.3 |
| Bias dù đã bỏ thuộc tính nhạy cảm | Proxy variable → eval theo slice + monitoring | 5.4 |
| Prompt injection qua RAG | Retrieved = untrusted data **+** least privilege tool (defence in depth) | 5.5, 5.8 |
| Public-facing AI | Disclose AI + giới hạn + đường tới người thật | 5.6 |
| "Never reach customer" | Guardrail + human approval (preventative, không phải detective) | 5.7 |
| "Never / before displayed" | Preventative guardrail | 5.9 |
| "Consequential decision" | HITL | 5.9 |
| "Months later / trend" | Monitoring & audit | 5.9 |

## 8. Stakeholder & lifecycle

- **Yêu cầu tuyệt đối** (100% accurate, sub-second) → giải thích bằng bằng chứng + acceptance criteria/SLA khả thi + cải thiện trải nghiệm (6.1, 6.4).
- **"Chúng tôi cần chatbot"** → discovery trước (6.2).
- **Stakeholder quyết định trái bằng chứng** → trình bày trade-off (cost + risk + reversal), người chịu trách nhiệm quyết (6.3).
- **Report** → business success criteria trước, metric kỹ thuật sau (6.6).
- **Discovery output** → success criteria + data/compliance assessment (6.7).
- **Scope creep** → impact minh bạch + re-baseline có sign-off (6.8).
- **Handoff** → ADR + runbook + eval baseline (6.5).

## 9. Developer productivity

- Config chung version-controlled, cá nhân xếp lớp trên (7.1).
- Review độc lập với phiên tác giả, người giữ quyền merge (7.2).
- Debug bằng trace trước khi sửa prompt (7.3).
- Chân ga (standard chung) + phanh (allowed commands, protected branch, approval gate) (7.4).
