# Cheat Sheet — CCAR-P

## Exam Blueprint (7 domains)
| Domain | Weight | Course phủ |
|--------|-------:|------------|
| 1. Solution Design & Architecture | 17% | C1, C2 |
| 2. Claude Models, Prompting & Context Engineering | 13% | C1.4 (mỏng — tự bù docs) |
| 3. Integration | 19% | C1, C2, C4 |
| 4. Evaluation, Testing & Optimization | 16% | C2, C5.3 |
| 5. Governance, Safety & Risk Management | 14% | C3, C1.6, C2.4, C4.3 |
| 6. Stakeholder Communication & Lifecycle Management | 14% | C4 |
| 7. Developer Productivity & Operational Enablement | 7% | C5, C1.5 |

Chi tiết từng lesson: [course-map.md](course-map.md).

## Decision frameworks của course (nhớ thuộc)

### 1. Scope một request (C1.1)
Chia 3 phần: **Claude làm gì** / **existing systems làm gì** / **humans làm gì** —
lens là *four properties of generative AI* (từ AI Fluency Foundations).

### 2. Chọn form (C1.2)
| Form | Khi nào | Cost phải nói ra |
|------|---------|------------------|
| Augmented call | 1 bước, deterministic input/output | rẻ nhất, nhưng không tự xử lý biến thể |
| Workflow | nhiều bước nhưng **biết trước** thứ tự | phải maintain graph; không thích ứng được |
| Agent | cần **dynamic decision** tại runtime | đắt, latency cao, khó dự đoán & khó debug |

> Không mặc định chọn agent. Hỏi: "bước tiếp theo có cần model quyết định không?"

### 3. Trình bày trade-off cho stakeholder (C4.2)
Mỗi option = **cost + risk + reversal cost** (đảo ngược tốn gì). Thiếu vế reversal → đáp án yếu.

### 4. Route quyết định cho người review (C3.4)
3 trục: **confidence** · **reversibility** · **cost of a wrong answer**.

### 5. Compliance (C3.5)
`obligation → named control → owner → evidence artifact`. Thiếu evidence artifact = không audit được.

### 6. Safety stack (C3.2)
`input screening → tool-call authorization → output screening`, mỗi lớp có blind spot lớp sau phải
bắt. Chọn **model-based** vs. **deterministic** check theo từng điểm. Hệ thống phải **fail closed**.

## Key Gotchas (luôn nhớ)
| Gotcha | Đúng | Sai |
|--------|------|-----|
| Least privilege | Gỡ bỏ hẳn capability không cần thiết | Chỉ thêm logging/confirmation (detective control, không phải preventive) |
| Safety rule | Enforce ở application layer | Giả định Claude tự enforce rule chưa bao giờ được cho |
| Fail mode | Fail **closed** | Fail open khi guardrail lỗi |
| Cost + latency cùng lúc | Static content trước + prompt caching | Truncate nội dung cần thiết hoặc downsize model mù quáng |
| RAG trả lời sai sau data refresh | Kiểm tra retrieval/indexing trước | Nghi ngờ model weights/temperature/context window |
| Dữ liệu thay đổi liên tục | Query **live-state** từ hệ thống nguồn | Index rồi retrieve (retrieval làm việc của live-state) |
| Integration mechanism | MCP cho reusable/maintainable tool access cross-app | Hard-code logic vào từng system prompt |
| Kiến trúc | Chọn pattern theo bài toán: workflow (deterministic) vs. agent (dynamic) | Luôn mặc định dùng agent |
| Đổi model / prompt / kiến trúc | Chạy eval suite làm **gate** trước | Swap vì "model mới nghe nói tốt hơn" |
| Đọc kết quả A/B test | Sample size không đủ → kết luận "chưa biết" | Overclaim từ kết quả mỏng |
| Deployment route | Loại trừ theo **governance/regulated constraint trước**, rồi mới so latency/cost | So cost trước rồi mới phát hiện không được phép dùng |

## Điều kiện thi
- 63 câu, 120 phút, passing 720/1000, lệ phí $175, hiệu lực 12 tháng.
