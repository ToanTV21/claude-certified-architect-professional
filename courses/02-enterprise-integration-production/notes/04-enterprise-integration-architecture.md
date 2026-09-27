# C2.4 — Enterprise integration: compliance, SSO/OAuth, authz, observability

> **Course:** 2 — Enterprise Integration & Production (158 min) · **Exam domain:** D3 (19%) + D5 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Architect a Claude deployment that is ready for the enterprise by specifying integration patterns for compliance, identity (SSO/OAuth), authorization, data handling, and observability instrumentation, placing the right integration (API, SDK, MCP, Claude Code) at each integration point

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)

### Thứ tự quyết định: compliance trước, rồi mới 5 layer integration
Sizing (từ Module 1) cho biết hệ thống cần làm gì và có làm được trong constraint không. **Entry point selection** luôn đi trước — compliance constraint (HIPAA, GDPR, FedRAMP, attorney-client privilege, data-residency) **loại bỏ option trước khi bàn đến bất cứ quyết định nào khác**. Sau khi entry point còn lại được xác định, 5 layer integration mới vận hành từ đó. Đây là quyết định thuộc về Architect, không phải implementation team.

### 5 entry point — khi nào dùng cái nào
- **Direct API**: dùng khi cần full control toàn bộ pipeline — tự build request, tự xử lý response/error. Trade-off: chịu trách nhiệm tự viết/maintain retry logic, streaming, tool orchestration, error handling → implementation effort cao hơn SDK.
- **SDK (Python/TypeScript)**: convenience layer xử lý phần HTTP layer + typed interface, nhưng vẫn để orchestration cho code của mình — không mất design control. Trade-off: control chi tiết kém hơn raw API; SDK version upgrade có thể đổi behavior, cần review trước khi deploy.
- **Claude Code**: chỉ dùng khi primary user là developer, task là viết/review/navigate code. **KHÔNG phù hợp** làm backend cho product embedded/multi-user/customer-facing — product integration nên dùng Claude API, client SDK, hoặc Agent SDK.
- **Agent SDK**: dùng khi cần Claude hành động qua nhiều turn bên trong product của mình, với app tự kiểm soát workflow xung quanh. Agent SDK chạy managed loop (iteration, tool execution, termination) nên team không phải tự build infra đó. Không phù hợp khi chỉ cần single request/response, không cần multi-turn reasoning qua tool. Trade-off: managed loop đánh đổi fine-grained control ở mỗi iteration step để lấy tốc độ triển khai; raw API loop giữ được control đó nhưng tự chịu chi phí build/maintain.
- **MCP (Model Context Protocol)**: dùng khi cần kết nối Claude với tool/internal service đã có, muốn cách quản lý connection chuẩn hoá, tách biệt khỏi orchestration logic. Trade-off: thêm 1 protocol layer giữa Claude và tool → debug tool call phức tạp hơn gọi function trực tiếp.

### Constraint-to-integration matrix (áp compliance logic 1 tầng sâu hơn — không phải legal advice, luôn làm việc với legal/compliance team)
| Constraint | Route | Identity | Data handling | Observability |
|---|---|---|---|---|
| **Attorney-client privilege*** | API chạy sau app của firm, qua gateway firm tự approve, log mọi request | User login qua SSO; identity/permission do server gán, user không tự claim được | Toàn bộ privileged content đi qua gateway — gateway là official record | Log mọi request/response tại gateway, retain theo policy của firm |
| **HIPAA (PHI)** | Chỉ chạy trên config có **BAA** (Business Associate Agreement) — HIPAA-eligible path: Claude API trực tiếp (có BAA ký với Anthropic), AWS Bedrock, Google Vertex AI. BAA phải cover đúng **configuration cụ thể** đang dùng, không chỉ cover provider nói chung | User verify qua auth system của partner; access PHI giới hạn theo "minimum necessary" của HIPAA | PHI strip chỉ giữ field cần cho task trước khi gọi API; dùng reference ID thay full data field khi có thể | Log request, model version, user identity, data scope; retain theo yêu cầu HIPAA |
| **GDPR / data residency** | Model execution giới hạn trong region được approve — qua cloud route (Bedrock/Vertex) hoặc Claude API dùng param `inference_geo` (**hiện chỉ support "us" và "global", KHÔNG support EU pinning trực tiếp**). GDPR không bắt buộc EU residency (cross-border transfer hợp pháp nếu có transfer mechanism hợp lệ), nhưng nếu deployment CÓ yêu cầu EU data residency → phải dùng cloud route, không dùng direct API. Route Claude API: DPA ký trực tiếp với Anthropic. Route cloud: DPA kế thừa từ hợp đồng cloud. (Microsoft Foundry EU residency: "Coming 2026", chưa có timeline xác nhận — verify trước khi commit) | User verify trong đúng approved data region, theo GDPR | Personal data chỉ xử lý trong pinned region; cross-border move cần legal basis document rõ, chỉ build khi có justification | Log ai truy cập data gì, legal basis xử lý, thời điểm deletion |
| **FedRAMP / government** | Chạy trên cloud config có **FedRAMP authorization** đúng impact level — path hợp lệ: Claude for Government, AWS Bedrock GovCloud, Google Vertex Assured Workloads. **Claude Enterprise trên direct API KHÔNG có FedRAMP authorization, không thể thay thế** | User auth qua identity provider agency approve; access control theo role/policy layer của agency | Theo classification rule của agency; controlled unclassified information (CUI) phải nằm trong authorized boundary | Log đáp ứng continuous monitoring requirement của agency |
| **Internal data-residency policy** | Chạy trên cloud provider mà org của partner đã approve — route đúng là route CIO đã clear, bất kể convenience | User login qua SSO chuẩn của partner; role gán theo policy hiện có | Theo classification scheme hiện có của partner; Claude layer kế thừa control cũ, không tạo control mới | Log feed vào logging infra hiện có của partner, không tạo hệ thống riêng |

(*Attorney-client privilege: privilege preservation phụ thuộc contractual terms, retention setting, internal policy phù hợp — bảng chỉ giúp mitigate risk waiver, không phải guarantee.)

**Process bắt buộc**: đi theo thứ tự — (1) xác định regulation/policy đang govern, (2) xác định entry point/route nào còn khả dụng, (3) chọn integration pattern phù hợp, (4) document identity/data-handling/observability requirement theo sau. Bỏ qua bước nào cũng có risk build ra hệ thống chạy được về mặt kỹ thuật nhưng fail legal/security review. (Các nội dung trên chưa cover case **ZDR — Zero Data Retention**.)

### 5 layer integration bắt buộc (compliance = layer 1, loại route trước khi 4 layer sau vận hành)
1. **Compliance & regulated-industry constraints** — Decision: route/entry point nào sống sót qua constraint đang govern? BAA coverage, FedRAMP authorization, data-residency pinning, approved-vendor list đều loại option trước khi design bắt đầu. Hỏng khi sai: integration build trên route fail ở lần legal/security review kế tiếp — cost redesign = thời gian đã đầu tư + kiến trúc mới từ đầu.
2. **Identity & SSO** — Decision: identity boundary của user nằm ở đâu so với integration point? User là ai trong context của 1 Claude call, identity đó được đưa vào prompt AN TOÀN như thế nào? Hỏng khi sai: identity truyền sai → Claude không scope được response theo đúng authorization của user; identity truyền dưới dạng raw field trong user message là **manipulable**; server-side injection loại bỏ risk này.
3. **Authorization & policy** — Decision: user/role này có capability gì? Truy cập được data gì? Authorization model đang govern hệ thống hiện tại cũng phải govern luôn Claude layer. Hỏng khi sai: Claude integration bypass authorization model của hệ thống gốc → user có access vào data họ không được phép, qua 1 path không được design để enforce access policy.
4. **Data handling & PII** — Decision: field gì đi vào context window? Field sensitive đưa trực tiếp vào user message/system prompt sẽ trở thành 1 phần của API request. Anthropic không retain conversation content by default (chỉ giữ những gì kỹ thuật cần để API/feature hoạt động), nhưng request vẫn đi qua wire, có carve-out retention riêng cho 1 số model class, và app-layer logging của partner sẽ capture nó. Architecture phải quyết định field nào cần trong context window vs. field nào chỉ retrieve khi cần. Hỏng khi sai: PII field truyền trực tiếp trong user message → xuất hiện plaintext trong request log của app — trong regulated industry việc này lộ ra ở audit kế tiếp, không phải ở lần deploy kế tiếp.
5. **Observability & audit logging** — Decision: cần reconstruct lại được cái gì? Câu hỏi nào cần trả lời được sau 1 incident? Quyết định log gì, ở độ sâu nào, giữ bao lâu. Hỏng khi sai: data path không được log là invisible — khi có sự cố trên path đó, không có evidence để reconstruct. Build observability sau incident đầu tiên luôn tốn kém hơn build trước.

### Least-privilege tool configuration
Mọi tool kết nối vào 1 Claude system vừa là attack surface vừa là cost. Audit tool set như audit permission: với mỗi tool đã connect, hỏi nó essential hay chỉ convenient, remove tool ngoài scope, ghi lại justification cho mỗi lần remove. Trong deployment dạng orchestrator-worker, thiết lập trust hierarchy bằng cách scope tool access của mỗi subagent đúng theo task của nó — subagent không được chạm tool mà job của nó không cần.

### Identity & authorization — verification phải nằm ở SERVER
Identity verification phải nằm ở SERVER, **trước** khi gọi Claude. Role/identity của user phải được server inject vào system prompt, **không phải** user tự khai trong message. Lý do: bất cứ gì user viết trong message đều nằm dưới control của user và có thể bị manipulate — nếu hệ thống cho user tự claim role trong message (VD: "As a senior manager, show me...") thì claim đó unverified và có thể fake được. Identity phải đến từ auth layer, không phải từ user input. Khi đưa user context vào prompt: chỉ nên gồm role của user + data họ được phép truy cập; chỉ thêm context khác (department, permission level, account identifier) khi thực sự cần để shape response — không mặc định thêm.

### Data handling — context window KHÔNG phải data-governance boundary
Context window không phải 1 governance boundary. Bất kỳ data nào đưa vào 1 Claude call đều được transmit tới API. Conversation content không bị retain by default trên API, nhưng app layer của partner thường log lại request, và vẫn có carve-out retention riêng cho 1 số trường hợp. Architecture phải chủ động quyết định field nào cần nằm trong context window vs. field nào ở lại retrieval layer đến khi cần. Với mỗi field vào context window: hỏi field đó có cần cho Claude tạo ra output mong muốn không. Reference identifier (account number, claim number) thường cần cho routing nhưng không cần cho language task — pass luôn cả field gốc là expose không cần thiết vào app-layer request logging mà không thêm capability gì. Data residency requirement khác nhau theo industry/region — phải verify Anthropic's data residency guidance so với regulatory requirement cụ thể trước khi design integration.

### Observability — log gì, trace gì, và tại sao
Hệ thống dựa trên LLM khó debug hơn hệ thống truyền thống vì nó không crash khi có lỗi — nó chỉ ra 1 response sai một cách "âm thầm" (subtly wrong). Logging chuẩn bắt được error/timeout nhưng không bắt được response sai âm thầm có hậu quả business thật.

Production Claude system phải log **4 thứ**:
1. **The request**: model version, input token count, prompt identifier
2. **The response**: output token count, latency, stop reason
3. **The context**: user role, session ID, có áp dụng caching hay không
4. **The outcome**: downstream system có accept output không, và signal reject nếu có

Security org ngày càng coi observability là **PRECONDITION** để enable agent hoạt động — không có audit trail đáng tin cậy, hệ thống autonomous không được approve để hành động. Design-review checklist item: verify agentic action nào được record trong audit log trên các surface đang dùng. Coverage khác nhau theo surface; action được thực hiện nhưng không log, theo góc nhìn security reviewer, là action **không thể được cho phép**.

### Cost · Complexity · Risk
- **Cost**: integration thiếu PII redaction trước khi gọi API sẽ expose field sensitive vào app-layer request logging ở MỌI request. Retroactive redaction trên 1 log history không được design để support việc đó là data-handling fix tốn kém nhất trong 1 production Claude system.
- **Complexity**: observability layer thêm vào SAU incident production đầu tiên nghĩa là root cause phải reconstruct từ 1 hệ thống không được setup để trả lời câu hỏi mà incident đặt ra. Build logging để trả lời câu hỏi mình SẼ cần hỏi, trước khi cần hỏi.
- **Risk**: hệ thống multi-tenant chạy trên 1 SHARED API key không cách nào attribute rate-limit breach về đúng tenant gây ra. Khi org-level limit trip lúc peak load, spike thấy được nhưng source thì không, mọi tenant đều chịu impact. **Separate API key per tenant** là bắt buộc cho attribution/isolation trong mọi production multi-tenant deployment.

### Case study — "The PII field that went straight into the prompt"
Demo trap: khi mục tiêu là chạy demo nhanh, đường đi nhanh nhất là pass thẳng data có sẵn vào prompt. PII redaction, server-side identity injection, observability instrumentation đều tốn thêm thời gian mà không thêm capability nhìn thấy được — hệ thống vẫn chạy được khi thiếu chúng. Cost của việc skip chỉ xuất hiện ở lần audit đầu tiên, không phải lúc demo.

Trace excerpt (composite, healthcare-adjacent): team build tool summarize patient intake form. Summarization chạy đúng, nhưng data handling sai. API request bị capture trong app-layer request log gồm: Model claude-sonnet-4-6, System prompt yêu cầu extract presenting concerns/medications/allergies, nhưng **User message chứa cả SSN và Insurance ID** (VD: "SSN: 123-45-6789, Insurance ID: BCB-88712") — 2 field này không cần cho language task nhưng vẫn đi kèm request, exposed vào app-layer logging.

Điều đã hỏng: tool hoạt động đúng như design, nhưng data handling sai — nhiều field PHI dưới HIPAA (name, DOB, SSN, Insurance ID, chief complaint, medications, allergies) bị đưa vào API call và capture plaintext trong app-layer request log. Khi review trước production certification, log chứa **hàng nghìn entry có SSN bệnh nhân** trong field user message.

Fix: thay đổi data architecture — thêm bước **server-side redaction** strip field PII không cần thiết trước khi gọi Claude, cộng 1 retrieval function chỉ cung cấp field mà language task cần. Cả 2 điều này lẽ ra phải có trong design ban đầu.

Bài học: data handling architecture bị design theo cái gì CONVENIENT để pass, không phải cái gì NECESSARY để pass. **Necessity là filter đúng**: field không cần cho language task Claude đang làm thì không nên nằm trong context window.

### Checkpoint — "Critique the integration diagram"
Bài toán: Claude deployment cho customer-service agent tại 1 multi-tenant SaaS company. Chọn mọi component/connection là integration problem, để nguyên component sound.

**5 problem:**
1. Dùng **Claude Code làm backend** cho customer-facing chat product (Claude Code là developer tool, không phải multi-tenant product backend).
2. Dùng **shared API key** cho tất cả tenant (không attribution/isolation per-tenant cho rate limit).
3. Capability check dựa trên câu **"I am a premium customer"** viết trong user message (claim unverified, user-controlled — phải đến từ server-side auth).
4. **Account number và email** truyền trong user message và xuất hiện trong request log (PII exposure không cần thiết).
5. Claude response được pass sang **downstream CRM mà không log** ở integration layer (unlogged data path = không có audit trail).

**2 component sound:**
1. Server-side authentication layer đặt trước API.
2. Tenant data được isolate per tenant ở storage layer.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| **Direct API** | Cần full control toàn bộ pipeline (request/response/error/streaming/tool orchestration) | Implementation effort cao nhất — tự build + maintain retry, streaming, error handling | Dễ tự tạo bug ở phần infra tự viết (retry, backoff, stream parsing) | Trung bình — chuyển sang SDK cần refactor lại phần đã tự build, nhưng logic nghiệp vụ giữ được |
| **SDK (Python/TS)** | Cần convenience layer (typed interface, HTTP xử lý sẵn) nhưng vẫn tự control orchestration | Thấp hơn Direct API; vẫn phải tự viết orchestration | Version upgrade của SDK có thể đổi behavior ngầm — cần review trước deploy | Thấp — đổi qua Direct API hoặc Agent SDK vẫn giữ được business logic, đổi lại lớp gọi API |
| **Claude Code** | Chỉ khi primary user là developer, task là code review/write/navigate | Gần như 0 (dùng sẵn) nhưng SAI SCOPE nếu dùng làm backend | Rất cao nếu dùng nhầm làm backend multi-tenant/customer-facing — không được design cho việc đó | Rất cao — phải kiến trúc lại toàn bộ integration layer bằng API/SDK/Agent SDK |
| **Agent SDK** | Cần Claude hành động qua nhiều turn trong product của mình, app kiểm soát workflow xung quanh, không cần build lại agent loop | Thấp hơn tự build agent loop (managed loop có sẵn: iteration, tool exec, termination) | Mất fine-grained control ở mỗi iteration step so với raw API loop tự viết | Trung bình — bỏ managed loop để tự viết loop riêng tốn công nhưng logic tool vẫn tái dùng được |
| **MCP** | Cần kết nối Claude với tool/internal service có sẵn theo cách chuẩn hoá, tách biệt integration khỏi orchestration | Thêm 1 protocol layer cần setup/maintain server MCP | Debug tool call phức tạp hơn gọi function trực tiếp (thêm 1 lớp gián tiếp) | Trung bình — bỏ MCP để hard-code tool access lại mất tính reusable/maintainable đã có |
| **Route qua Claude API trực tiếp (HIPAA/GDPR)** | Khi có BAA covering đúng config, hoặc không có yêu cầu EU residency cứng | DPA ký trực tiếp với Anthropic — đơn giản hoá hợp đồng | Nếu sau này phát sinh yêu cầu EU data residency, route này KHÔNG hỗ trợ (`inference_geo` không pin EU) | Cao — phải chuyển toàn bộ traffic sang cloud route (Bedrock/Vertex), đổi cả DPA lẫn infra |
| **Route qua Cloud (Bedrock/Vertex Assured Workloads/GovCloud)** | Khi cần EU data residency, hoặc cần FedRAMP authorization, hoặc org đã approve cloud provider đó | Overhead tích hợp thêm 1 lớp cloud provider, DPA kế thừa từ hợp đồng cloud | Phải verify đúng config cụ thể có authorization (BAA/FedRAMP) — dùng sai config vẫn fail compliance dù đúng provider | Cao — đổi ngược lại route Claude API trực tiếp mất luôn compliance coverage đang có |
| **Server-side identity injection** | Luôn luôn chọn — mặc định bắt buộc cho mọi integration có multi-user | Cần thêm 1 bước ở server trước khi gọi Claude (lấy role từ auth layer, viết vào system prompt) | Nếu bỏ qua: user tự claim role trong message → authorization bị bypass hoàn toàn | Thấp về kỹ thuật nhưng cao về risk nếu phát hiện muộn (đã có data breach) |
| **Pass raw PII field vào prompt (convenient nhưng sai)** | Không nên chọn — chỉ xảy ra khi ưu tiên demo nhanh | Cost ẩn: rẻ lúc build, rất đắt lúc audit (redact retroactive log history) | Cao nhất — PHI/PII lộ plaintext trong app-layer log, fail compliance review | Rất cao — phải redact toàn bộ log history cũ, đổi kiến trúc retrieval, không thể "undo" data đã log |
| **Shared API key multi-tenant** | Không nên chọn cho production multi-tenant | Cost thấp lúc setup (1 key duy nhất) | Không attribute được rate-limit breach về đúng tenant, mọi tenant cùng chịu impact | Trung bình — cấp lại key riêng cho từng tenant, cần migration nhưng không ảnh hưởng data đã có |

**Lưu ý:** lesson này thuộc domain D3 (Integration) + D5 (Governance) — mọi trade-off ở trên đều bắt buộc đi kèm cost + risk + reversal cost theo công thức course, vì exam ra dạng scenario "chọn giải pháp tốt nhất".

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Entry point | Cách hệ thống kết nối tới Claude: Direct API, SDK, Claude Code, Agent SDK, hoặc MCP — chọn trước, bị compliance constraint loại bớt option |
| BAA (Business Associate Agreement) | Hợp đồng bắt buộc với Anthropic (hoặc cloud provider) để xử lý PHI hợp pháp theo HIPAA — phải cover đúng configuration cụ thể đang dùng |
| DPA (Data Processing Agreement) | Hợp đồng quy định cách xử lý personal data theo GDPR — nội dung khác nhau tuỳ route (Claude API trực tiếp vs. cloud) |
| `inference_geo` | Parameter của Claude API để pin region chạy inference — hiện chỉ support "us" và "global", KHÔNG hỗ trợ pin EU trực tiếp |
| FedRAMP | Chương trình authorization bảo mật cho cloud dùng trong chính phủ Mỹ — cần đúng impact level; Claude Enterprise trên direct API KHÔNG có authorization này |
| Data residency | Yêu cầu data/model execution phải nằm trong 1 vùng địa lý cụ thể — khác nhau theo industry/region, phải verify trước khi design |
| Least-privilege (tool configuration) | Nguyên tắc chỉ giữ tool essential, bỏ tool convenient-nhưng-không-cần, ghi lại lý do remove |
| Identity injection (server-side) | Server (không phải user) verify identity/role rồi inject vào system prompt — chống user tự claim role giả trong message |
| PII / PHI redaction | Bước loại field nhạy cảm (SSN, insurance ID...) trước khi đưa data vào context window/API call |
| ZDR (Zero Data Retention) | Chế độ Anthropic không giữ lại conversation content — lesson này không cover chi tiết case ZDR |
| Observability (4 thành phần) | Log bắt buộc: request (model version, token count, prompt id), response (output token, latency, stop reason), context (user role, session id, caching), outcome (downstream accept/reject) |
| Attribution / isolation (multi-tenant) | Khả năng gán 1 sự cố (VD rate-limit breach) về đúng tenant gây ra — cần API key riêng per tenant |
| Constraint-to-integration matrix | Bảng map từng compliance constraint (privilege, HIPAA, GDPR, FedRAMP, internal policy) sang route/identity/data-handling/observability tương ứng |
| Trust hierarchy (orchestrator-worker) | Scope tool access của mỗi subagent theo đúng task của nó, subagent không chạm được tool ngoài scope |

## Gotchas / bẫy hay gặp
- [ ] Cho user tự khai role trong message (VD: "As a senior manager, show me...") rồi tin luôn — claim này unverified, phải verify ở server, inject vào system prompt
- [ ] Pass field PII/PHI không cần thiết (SSN, Insurance ID...) vào user message chỉ vì "có sẵn data đó" — case study patient intake: field này lộ plaintext trong app-layer request log dù summarization task không cần
- [ ] Dùng shared API key cho multi-tenant system — không attribute được rate-limit breach về đúng tenant khi org-level limit trip
- [ ] Dùng Claude Code làm backend cho product customer-facing/multi-tenant — Claude Code là developer tool, sai scope hoàn toàn
- [ ] Downstream action (VD: response gửi qua CRM) không log ở integration layer — với security reviewer, action không log = action không được phép tồn tại
- [ ] Nghĩ rằng BAA/FedRAMP cover "provider nói chung" là đủ — phải verify đúng SPECIFIC configuration đang dùng có nằm trong scope authorization không
- [ ] Nhầm GDPR compliance = bắt buộc phải có EU residency — thực ra GDPR cho phép cross-border transfer với transfer mechanism hợp lệ; chỉ khi deployment CÓ yêu cầu EU residency riêng mới cần cloud route
- [ ] Build observability SAU khi có incident đầu tiên thay vì thiết kế trước — root cause không reconstruct được từ hệ thống chưa setup để trả lời đúng câu hỏi

## Exam tips
- Gặp scenario nêu rõ compliance constraint (HIPAA/GDPR/FedRAMP/privilege/internal policy) → luôn xử lý **entry point/route trước tiên** (constraint loại option), sau đó mới xét đến 5 layer (identity, authorization, data handling, observability) — đừng chọn integration pattern trước khi lọc theo compliance.
- Câu hỏi kiểu "region EU cho Claude API" → nhớ `inference_geo` chỉ support "us"/"global", KHÔNG pin EU trực tiếp; muốn EU residency thật phải qua cloud route (Bedrock/Vertex).
- Dạng "critique the diagram" (chọn component sai) → check đủ 4 dấu hiệu: identity tự-claim trong message, shared credential/API key cho multi-tenant, PII/field không cần thiết trong log, action không được log ở integration layer. Claude Code dùng làm backend luôn là problem.
- Identity verification luôn phải ở SERVER-SIDE, trước Claude call — bất kỳ đáp án nào để user tự khai role/permission trong message đều là đáp án sai.
- Với câu hỏi "log gì trong production Claude system" → nhớ đúng 4 nhóm: request, response, context, outcome — thiếu 1 trong 4 là đáp án không đầy đủ.

## Code / config snippets
```python
"""
Minh hoạ 2 nguyên tắc trong lesson này:
1. PII redaction TRƯỚC khi build prompt (Layer 4 — Data handling)
2. Server-side identity injection vào system prompt (Layer 2 — Identity/SSO)
Không phải code chạy thật của course, chỉ minh hoạ ý tưởng kiến trúc.
"""
from dotenv import load_dotenv
import anthropic
import os

load_dotenv()
client = anthropic.Anthropic()
MODEL_MAIN = "claude-sonnet-4-6"  # production dùng sonnet

# Danh sách field KHÔNG cần cho task "extract presenting concerns/medications/allergies"
# -> đây là field PHI/PII, nếu để lọt vào prompt sẽ bị app-layer log plaintext
UNNECESSARY_FIELDS = {"ssn", "insurance_id", "dob"}  # tuỳ task mà mở rộng danh sách này

def redact_pii(intake_form: dict) -> dict:
    """
    Strip field không cần thiết cho language task trước khi đưa vào context window.
    Nguyên tắc: necessity là filter đúng, không phải convenience.
    """
    return {k: v for k, v in intake_form.items() if k not in UNNECESSARY_FIELDS}


def get_user_identity_from_auth_server(session_token: str) -> dict:
    """
    Giả lập việc lấy identity/role từ auth layer phía SERVER,
    KHÔNG bao giờ lấy role từ user message (user tự khai role là unverified/manipulable).
    """
    # Trong hệ thống thật: verify session_token với SSO/OAuth provider ở đây
    # rồi trả về role + phạm vi data được phép truy cập.
    return {"role": "clinical_staff", "authorized_scope": "intake_summary_only"}


def build_system_prompt(user_identity: dict) -> str:
    """
    Inject identity đã verify ở server vào system prompt.
    Chỉ thêm field cần để shape response (role, authorized_scope),
    không mặc định nhồi thêm department/account_id nếu không cần.
    """
    return (
        "You are a clinical intake summarizer. "
        f"The requesting user has role: {user_identity['role']}, "
        f"authorized scope: {user_identity['authorized_scope']}. "
        "Extract only presenting concerns, medications, and allergies."
    )


def summarize_intake(session_token: str, raw_intake_form: dict) -> str:
    # Bước 1: identity verify ở server, không tin user tự khai (Layer 2)
    identity = get_user_identity_from_auth_server(session_token)

    # Bước 2: redact PII/PHI không cần thiết trước khi vào context window (Layer 4)
    safe_intake_form = redact_pii(raw_intake_form)

    # Bước 3: build request — identity đi trong system prompt, KHÔNG đi trong user message
    response = client.messages.create(
        model=MODEL_MAIN,
        system=build_system_prompt(identity),
        messages=[{"role": "user", "content": str(safe_intake_form)}],
        max_tokens=500,
    )

    # Bước 4 (Layer 5 — Observability): log đủ 4 nhóm request/response/context/outcome
    # (ví dụ log call, không implement chi tiết ở đây)
    # log_event(request=..., response=..., context=identity, outcome=...)

    return response.content[0].text


if __name__ == "__main__":
    pass  # ví dụ minh hoạ, không chạy trực tiếp trong bài học
```

## Câu hỏi chưa rõ
- ?
