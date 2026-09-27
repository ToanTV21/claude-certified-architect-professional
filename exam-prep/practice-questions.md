# Practice Questions — CCAR-P

Câu hỏi tự soạn hoặc từ resources khác, theo format multiple-choice/multiple-response (scenario-based, architecture trade-off). Ghi domain và số đáp án cần chọn cho mỗi câu, giống format đề thi thật.

## Domain 3 — Integration
1. (Chọn 1) ...

## Domain 4 — Evaluation, Testing & Optimization

### Bài tập: Thiết kế eval framework cho hệ thống xử lý claim bảo hiểm
> Nguồn: Course 2 (Enterprise Integration & Production), Exercise "Eval Framework", gắn với [C2.1](../courses/02-enterprise-integration-production/notes/01-success-criteria-eval-suite.md).

**Đề bài:** Một công ty bảo hiểm khu vực triển khai hệ thống Claude đọc claim được nộp, extract structured field (claimant, policy number, loss amount, date of loss), tóm tắt narrative cho adjuster, và flag claim nghi ngờ fraud. Hệ thống phải phản hồi trong vài giây, giữ trong ngân sách per-claim đã định, không bao giờ để lộ data của claimant này sang summary của claimant khác, và không bao giờ tự động từ chối (auto-deny) 1 claim.

Với mỗi dimension dưới đây, xác định: metric đo, grading method (code-based eval / LLM judge / human review), và lý do chọn:
1. Accuracy — field extraction
2. Latency — response time
3. Safety — summary faithfulness và không auto-deny
4. Security — không leak data chéo giữa các claimant
5. Cost — per-claim spend

**Đáp án mẫu (bám grading ladder — code trước, judge khi cần interpretation, human là last resort):**
| Dimension | Grading method | Vì sao |
|---|---|---|
| Accuracy (field extraction) | Code-based eval | Expected value (tên, policy number, loss amount, date) đã biết trước, so khớp exact/schema — không cần diễn giải |
| Latency (response time) | Code-based eval | p95 là 1 con số, chỉ cần so với target — không cần judgment |
| Safety — auto-deny | Code-based eval | Hành động deny là binary (có/không) — deterministic check |
| Safety — summary faithfulness | LLM-as-judge | Đánh giá narrative có bám sát nguồn, không bịa, là task cần interpretation — hàm code không encode được |
| Security (no cross-claimant leak) | Code-based eval | Quét summary tìm identifier thuộc claim khác — deterministic, không cần interpretation dù stakes cao |
| Cost (per-claim spend) | Code-based eval | Giá trị numeric tính từ input/output token + model tier + caching — so với ngưỡng |

**Bẫy hay gặp khi làm bài này:** dùng LLM judge cho field extraction (sai — đây là deterministic, code xử lý được); coi auto-deny check là cần interpretation (sai — đây là binary). Ghi nhớ: Security dimension vẫn dùng code-based dù high-stakes, vì bản chất check là deterministic — "high-stakes" không tự động nghĩa là "cần judge".

### Bài tập tổng hợp (capstone): Production readiness builder — Internal knowledge assistant cho công ty tư vấn
> Nguồn: Course 2, Cumulative Module Exercise "Production readiness builder" — tổng hợp cả 5 lesson C2.1-C2.5.

**Bối cảnh:** Công ty tư vấn 600 người muốn triển khai internal knowledge assistant: giúp consultant tra cứu excerpt từ báo cáo engagement cũ, trả lời câu hỏi về methodology của firm, và soạn draft response cho RFP dựa trên công việc cũ. Corpus 12,000 documents (5-80 trang/doc). Peak 800 request/ngày. Ngân sách $3,000/tháng. Response time p95 < 8 giây. Firm có sẵn SSO (Okta) và document management system (SharePoint). Một số document chứa thông tin khách hàng thuộc diện NDA.

Trả lời 5 quyết định kiến trúc theo đúng thứ tự 5 lesson đã học:

**1. Eval strategy (D4):** primary eval task là gì? Đo retrieval relevance và RFP draft quality bằng cách nào, dùng loại eval nào? Golden dataset strategy? Xử lý constraint client-confidentiality ra sao?

**2. POC-to-production checklist (D1+D4):** Build cost model. Có nằm trong ngân sách $3,000/tháng không? Reliability pattern nào quan trọng nhất và vì sao? Failure mode đặc thù của architecture này là gì?

**3. Use-case sizing & feasibility (D1):** Chạy qua 4 AI properties. Working memory: 80-trang document có phải là constraint không? Knowledge: methodology riêng của firm không có trong training data — mitigation là gì? Feasibility verdict + boundary condition load-bearing?

**4. Integration pattern (D3+D5):** Identity boundary của Okta đặt ở đâu so với Claude call? Document confidential trong SharePoint xử lý constraint data-handling thế nào? Observability log những gì?

**5. A/B testing posture (D4):** Firm muốn test 1 retrieval config mới. Hypothesis là gì? Treatment, primary metric, constraint trên secondary metric? Baseline task success rate 70%, muốn detect cải thiện 5 điểm — sample size cần bao nhiêu? Ở 800 request/ngày thì mất bao lâu?

**Đáp án mẫu (rút gọn, xem raw đầy đủ trong lesson C2.1-C2.5 tương ứng):**
1. Code-based eval cho schema compliance của citation (tên doc, số trang, section); model-based eval cho relevance/độ phù hợp của RFP draft. Golden dataset từ RFP cũ đã redact tên khách hàng; document confidential loại khỏi eval set trừ khi khách hàng approve.
2. Cost model: 800/ngày × 30 = 24,000 request/tháng; ~5,200 input token + ~600 output token/request; Sonnet + caching system prompt ổn định → trong ngân sách **nếu** tính theo average phẳng — nhưng corpus 5-80 trang nên context retrieved khả năng phân bố 2 đỉnh (bimodal), đuôi request lớn có thể làm cost bị underestimate → phải chạy sensitivity analysis trước khi chốt. Reliability quan trọng nhất: fallback chain Sonnet→Haiku khi latency tăng đột biến. Failure mode đặc thù (RAG): retrieval quality drift khi document mới được thêm vào corpus mà không reindex.
3. Working memory: không document nào (tối đa ~29,000 token/80 trang) vượt context window 1M token — nhưng **constraint thật sự** là quy mô corpus (12,000 doc ≈ 175M token) không thể nhét hết vào 1 context → đây là lý do bắt buộc dùng kiến trúc RAG. Knowledge: methodology riêng không có trong training data → mitigation là index methodology doc vào cùng RAG layer, retrieval precision trên methodology query phải là metric riêng trong eval/observability. Verdict: **Feasible with constraints** — boundary condition load-bearing là "retrieval index phải coverage đầy đủ + luôn cập nhật (fresh)".
4. Identity: verify Okta token ở server-side, role + document set được authorize inject vào system prompt bởi server (không phải user tự khai). Data handling: document gắn nhãn confidential trong SharePoint chỉ retrieve được bởi consultant có role đúng engagement đó — access control enforce ở retrieval layer trước khi đưa vào Claude; tên khách hàng được anonymize trước khi vào context window. Observability: log model version, input token (cache hit/miss), retrieval precision/request, output token, user role, session ID, tín hiệu outcome (consultant accept/revise draft); alert khi p95 > 8s hoặc retrieval precision dưới ngưỡng.
5. Hypothesis: retrieval config mới tăng task success rate (đo bằng việc consultant chấp nhận draft không cần sửa lớn) từ 70% lên ≥75%, không tăng p95 latency quá 8s hoặc cost/request quá 10%. Sample size: detect cải thiện 5 điểm từ baseline 70%, power 80%, significance 5% → cần ~1,500 session/nhóm → ở 800 request/ngày chia đều 2 nhóm mất khoảng ~4 ngày, khả thi. Input distribution control: đảm bảo 2 nhóm có phân bố độ phức tạp RFP tương đương (proxy: độ dài document, số document nguồn được retrieve).

**Điểm mấu chốt khi làm bài dạng capstone:** câu trả lời tốt luôn nêu con số cụ thể VÀ nối các quyết định với nhau — sizing model nuôi cost ceiling, feasibility boundary condition (retrieval coverage/freshness) nuôi observability, eval nuôi A/B primary metric. Đây chính là cách đề thi CCAR-P kiểm tra khả năng tư duy end-to-end thay vì từng domain rời rạc.

---
Thêm câu hỏi mới khi luyện tập theo từng domain.
