# Cheat Sheet — CCAR-P

## Exam Blueprint (7 domains)
| Domain | Weight |
|--------|--------|
| 1. Solution Design & Architecture | 17% |
| 2. Claude Models, Prompting & Context Engineering | 13% |
| 3. Integration | 19% |
| 4. Evaluation, Testing & Optimization | 16% |
| 5. Governance, Safety & Risk Management | 14% |
| 6. Stakeholder Communication & Lifecycle Management | 14% |
| 7. Developer Productivity & Operational Enablement | 7% |

## Key Gotchas (luôn nhớ)
| Gotcha | Đúng | Sai |
|--------|------|-----|
| Least privilege | Gỡ bỏ hẳn capability không cần thiết | Chỉ thêm logging/confirmation (detective control, không phải preventive) |
| Cost + latency cùng lúc | Static content trước + prompt caching | Truncate nội dung cần thiết hoặc downsize model mù quáng |
| RAG trả lời sai sau data refresh | Kiểm tra retrieval/indexing trước | Nghi ngờ model weights/temperature/context window (không liên quan) |
| Integration mechanism | MCP cho reusable/maintainable tool access cross-app | Hard-code logic vào từng system prompt |
| Kiến trúc | Chọn pattern theo bài toán: workflow (deterministic) vs. agent (dynamic) | Luôn mặc định dùng agent cho mọi task |

## Điều kiện thi
- 63 câu, 120 phút, passing 720/1000, lệ phí $175, hiệu lực 12 tháng.
