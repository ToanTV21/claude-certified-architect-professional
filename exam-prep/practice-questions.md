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

## Domain 5 — Governance, Safety & Risk Management

### Bài tập: Sort the responsibility — Claude's trained behavior vs. Application layer
> Nguồn: Course 3 (Responsible AI, Safety & Risk for Architects), checkpoint gắn với [C3.1](../courses/03-responsible-ai-safety-risk/notes/01-training-vs-application-layer.md).

**Đề bài:** Phân loại 5 obligation dưới đây vào đúng 1 trong 2 bucket: **Claude's trained behavior** hoặc **Application layer (bạn phải tự enforce)**.
1. Refusing to help synthesize a dangerous weapon
2. Never returning another tenant's data
3. Declining to produce plainly hateful content
4. Blocking advice outside the partner's approved script
5. Requiring a sign-off before a refund is issued

**Đáp án mẫu:**
| Obligation | Bucket | Vì sao |
|---|---|---|
| Refuse dangerous-weapon synthesis | Claude's trained behavior | Harm phổ quát (broad harm), đã nằm trong Constitution/training — không cần build riêng |
| Never return another tenant's data | Application layer | Domain/deployment-specific rule (multi-tenant isolation) — Claude chưa từng được dạy khái niệm "tenant" của bạn |
| Decline plainly hateful content | Claude's trained behavior | Harm phổ quát, model đã refuse mặc định |
| Block advice outside approved script | Application layer | Policy riêng của partner (scope cụ thể của sản phẩm) — phải enforce bằng system prompt + runtime control |
| Require sign-off before refund | Application layer | Action có side effect, cần tool-call authorization riêng — không phải content safety |

**Bẫy hay gặp:** thấy Claude "test pass" mọi prompt harmful rồi suy ra nó cũng tự động cover luôn domain policy (VD: cross-tenant data, approved script) — đây chính là root cause của case study "trained refusals mistaken for a domain policy" trong lesson: rule chưa từng được encode ở bất kỳ layer nào thì không tồn tại, bất kể Claude "trông có vẻ an toàn" tới đâu.

### Bài tập tổng hợp (capstone): Assemble a responsible deployment — Public-sector benefits assistant
> Nguồn: Course 3, Cumulative Module Exercise — tổng hợp cả 5 lesson C3.1-C3.5.

**Bối cảnh:** Một benefits assistant cho cơ quan chính phủ giúp xác định eligibility chương trình phúc lợi, đề xuất approve/deny/refer.
- Framework: FedRAMP ở đúng impact level agency yêu cầu, cộng quy định của agency là applicant bị deny phải được cho biết lý do cụ thể.
- Case high-stakes/low-confidence: applicant gần ngưỡng eligibility, thiếu giấy tờ — deny sai sẽ cắt mất phúc lợi của một người.
- Output dễ bị skew: recommendation + lý do đính kèm khi deny.
- Data: field applicant tự khai, record của agency tra cứu lúc quyết định, derived feature.

Trả lời 5 quyết định theo đúng thứ tự 5 lesson đã học (mỗi quyết định đặt nền cho quyết định sau — chọn sai ở bước 1 thì không bước nào sau cứu lại được):
1. Đặt boundary giữa trained behavior và application layer.
2. Đặt vị trí runtime control (input/output screening, tool-call authorization).
3. Xác định fairness & transparency control.
4. Định nghĩa human-review routing.
5. Xây control register.

**Đáp án mẫu:**
1. Trained behavior chỉ refuse broad harm, chưa từng biết rule eligibility riêng của chương trình này → rule đó thuộc **application layer**. Để lọt vào "tin tưởng trained behavior" ở bước này thì không control nào phía sau lấy lại được.
2. Đặt input screening / output screening / tool-call authorization, chọn model-based hay deterministic cho từng điểm, và set **fail closed** — vì fail open nghĩa là 1 quyết định deny chưa được screen vẫn tới tay applicant.
3. Chỉ rõ injection point nào (corpus / prompt framing / examples / routing) có thể làm skew outcome; xây decision logging **một lần duy nhất** — vì applicant bị ảnh hưởng, regulator, build team, và control register đều dùng chung log này.
4. Route theo confidence + reversibility + cost — không theo volume; case "gần ngưỡng, thiếu giấy tờ, khó đảo ngược" phải vào **pre-action approval**. Nếu chỉ route theo volume, hàng đợi im lặng có thể để lọt 1 quyết định deny high-stakes mà không ai xem.
5. Map từng FedRAMP obligation sang 1 control + 1 owner + 1 evidence artifact reviewer có thể kiểm tra được. Control không có evidence artifact là 1 lời tuyên bố không chứng minh được, không phải bằng chứng.

**Điểm mấu chốt:** câu trả lời tốt luôn gọi tên cụ thể — injection point nào, fail direction nào, biến routing nào, evidence artifact nào — chứ không mô tả khái niệm chung chung. Đây là cách CCAR-P kiểm tra khả năng áp cả 5 lesson vào 1 tình huống liền mạch, giống hệt cách bài capstone Course 2 kiểm tra D1/D3/D4.

---
Thêm câu hỏi mới khi luyện tập theo từng domain.
