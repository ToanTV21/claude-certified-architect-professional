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

## Domain 6 — Stakeholder Communication & Lifecycle Management

### Bài tập: Find the undocumented assumption
> Nguồn: Course 4 (Stakeholder Engagement, Lifecycle & GTM), checkpoint gắn với [C4.1](../courses/04-stakeholder-engagement-lifecycle-gtm/notes/01-structured-discovery.md).

**Đề bài:** So sánh requirements document dưới đây với đúng nguyên văn stakeholder đã nói, tìm ra item nào là **assumption chưa được document** (không có statement nào của stakeholder support nó).

Requirements document:
1. Claude drafts the customer email, but a person actually sends it.
2. Responses must return within a two-second perceived budget.
3. Refunds above the threshold route to a human approver.
4. Conversation transcripts are retained for sixty days for analytics.

Stakeholder đã nói:
- "Anything big requires a person's sign off."
- "Draft the reply, but we send it ourselves."
- "It has to feel instant to the user."

**Đáp án mẫu:** Item 4 (giữ transcript 60 ngày cho analytics) là assumption — không câu nào trong 3 câu stakeholder nói nhắc tới retention period hay mục đích analytics. Item 1↔"Draft the reply, but we send it ourselves", item 2↔"It has to feel instant", item 3↔"Anything big requires sign off" đều có nguồn rõ ràng.

**Bẫy hay gặp:** đây chính là lỗi "discovery call turned into design session" — Architect tự thêm 1 requirement nghe có vẻ hợp lý (retention cho analytics) mà không quay lại hỏi stakeholder, y hệt case study "quick check" bị đánh giá thấp trong lesson (rule ẩn chỉ lộ ra 2 tuần sau ở compliance review).

### Bài tập tổng hợp (capstone): Architect a regulated multi-platform deployment end to end
> Nguồn: Course 4, Cumulative Module Exercise — tổng hợp cả 5 lesson C4.1-C4.5.

**Bối cảnh:** Mạng lưới bệnh viện khu vực (2 bang) có nghĩa vụ health-privacy, triển khai clinical documentation assistant trên 2 cloud platform. Architect gốc đang rotate off, CFO khách hàng đòi bằng chứng giá trị kinh doanh. Nurse đọc (dictate) tương tác bệnh nhân, assistant soạn clinical note có cấu trúc; 1 clinician có license phải authorize mỗi note trước khi vào patient record. Deployment có audit-trail requirement + data-residency rule. Partner chuẩn hoá trên AWS nhưng vẫn chạy 1 số việc back-end không regulated trên direct API. Đã 4 tuần kể từ khi deploy.

Trả lời 7 quyết định theo đúng thứ tự (mỗi quyết định xây trên quyết định trước):
1. **Discovery:** must-prove constraint nào chi phối kiến trúc nhiều nhất? Viết 1 requirement row nó buộc phải có.
2. **Tradeoff framing:** network muốn latency thấp nhất — frame trade-off giữa cắt logging để giảm latency vs giữ audit trail, đủ 3 yếu tố kể cả reversal cost.
3. **Feedback loop:** viết 1 governance-table row map output audit bắt buộc → stakeholder-review trigger CHẠY THEO LỊCH, độc lập với mọi metric.
4. **Documentation:** decision-log row nào nếu thiếu sẽ khiến successor đảo ngược 1 quyết định load-bearing về compliance? Nêu rejected alternative nó phải mang theo.
5. **Entry point selection:** chọn route chính/phụ với AWS standardization + obligation nghiêm ngặt + residency rule; nêu bước config ngăn lỗi residency phổ biến nhất.
6. **Outcome document:** nêu before/after business metric + control auditable giúp document dùng được cho case mở rộng trước CFO.
7. **Phase transition:** artifact nào gate bước chuyển phase tiếp theo? Đánh giá gate đã thoả mãn chưa ở tuần 4.

**Đáp án mẫu (rút gọn):**
1. Must-prove: health-privacy obligation + audit-trail requirement. Requirement row: hệ thống phải tạo record auditable cho mọi note do model tạo đã được clinician có license review, trace được về đúng interaction — vì workflow mang formal proof obligation theo health-privacy regime.
2. Gain (cắt logging): phản hồi nhanh hơn, workflow clinician mượt hơn. Give up: audit detail per-interaction cần cho health-privacy obligation. Reversal cost: khi hệ thống đã build quanh latency gain, khôi phục logging cần redesign lại interaction layer, và bất kỳ gap period nào cũng tạo compliance exposure phải disclose + remediate.
3. Signal: periodic output audit theo health-privacy documentation standard. Trigger: theo lịch (quarterly, theo obligation), fire bất kể eval score/error rate. Owner: Compliance lead. Action: stakeholder review với audit record nộp cho compliance officer.
4. Decision row: context strategy — thực thi in-region tường minh qua Bedrock, không dùng global endpoint. Rejected alternative: global Bedrock endpoint (đơn giản hơn). Vì sao load-bearing: successor không thấy rationale này sẽ revert về global config để fix performance issue và phá vỡ residency — y hệt postmortem financial-services trong lesson.
5. Primary: AWS Bedrock, config thực thi in-region tường minh (không phải global endpoint) — vì partner chuẩn hoá AWS và residency rule chi phối; verify đúng compliance requirement cụ thể (HIPAA BAA hoặc data sovereignty) được thoả bởi chính config Bedrock đang dùng. Secondary: Direct API cho task back-end không regulated. Config step: set region parameter tường minh trong Bedrock client, không dựa vào default endpoint resolution.
6. Before metric: thời gian trung bình từ lúc nurse dictate tới khi có clinical note hoàn chỉnh đã được clinician authorize (đo baseline trước deploy). After metric: cùng metric, cùng định nghĩa đo, sau deploy. Auditable control: clinician-authorization log — mỗi note có authorization record gắn timestamp nối clinician/note/interaction, biến so sánh before-after thành auditable thay vì chỉ là assertion.
7. Gate artifact: outcome document (đủ before/after metric + control auditable + measurement owner) — gate quyết định mở rộng mà CFO đang hỏi. Đánh giá: **chưa thoả mãn** ở tuần 4 — before metric đã có từ baseline, nhưng after metric cần đủ thời gian vận hành production để đo. Hành động đúng: đặt tên measurement owner, xác nhận control đang log, lên lịch hoàn thành outcome document ở 1 mốc post-launch xác định.

**Điểm mấu chốt:** câu trả lời tốt luôn nối liền 7 quyết định — must-prove constraint (bước 1) là thứ trade-off (bước 2) đang bảo vệ; governance row (bước 3) chạy trên chính constraint đó; decision log (bước 4) giải thích tại sao entry point (bước 5) được chọn vậy; outcome document (bước 6) đo đúng metric mà cả module đang xây tới; và biết nói "chưa xong" (bước 7) khi dữ liệu chưa đủ, thay vì vội chốt gate cho có.

---
Thêm câu hỏi mới khi luyện tập theo từng domain.
