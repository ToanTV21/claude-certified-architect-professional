# C3.2 — Safety stack: input screening, output screening, tool-call authorization

> **Course:** 3 — Responsible AI, Safety & Risk for Architects (114 min) · **Exam domain:** D5 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Place input screening, output screening, and tool-call authorization at the appropriate points in the request path and determine when to use model-based versus deterministic checks, so the system fails closed instead of failing open

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)

### 1. 5 risk category hay lặp lại trong LLM system
Trước khi đặt control, Architect phải biết mình đang defend chống lại cái gì. Đây là input cho **risk assessment** — 1 deliverable bắt buộc phải có trong security review, không phải optional nice-to-have:
- **Direct prompt injection**: user chủ động viết input để override system instruction, redirect behavior của model.
- **Indirect prompt injection**: instruction độc hại đến qua **retrieved content** (RAG) hoặc **tool output** — model coi nội dung này là trusted vì nó không phải do user gõ trực tiếp. Input screening thông thường (chỉ soi user message) **không bắt được** loại này — đây là điểm dễ bị hiểu sai nhất trong lesson.
- **Token-budget exhaustion**: input bị làm quá khổ hoặc padding có chủ đích để ăn hết context/output budget, khiến work bị truncate hoặc cost bị đội lên.
- **Tool and action abuse**: model bị dẫn dụ (qua injection hoặc prompt khéo) để gọi 1 tool có side-effect ngoài policy cho phép — đây chính là failure mode mà **action-authorization control** sinh ra để chặn.
- **Data exposure**: dữ liệu nhạy cảm lọt vào context window hoặc vào logs mà không nên ở đó — rủi ro này độc lập với hành vi của model, tồn tại kể cả khi model làm đúng 100%.

**Cách tìm vulnerability**: đi dọc theo cả request path và data path, tại mỗi entry point (user input, retrieved content, tool output, model output, logs) tự hỏi "adversary có thể làm gì ở đây, và control nào đang chặn nó". Bất kỳ điểm nào không có control mà có thể bị tấn công hợp lý → đó là gap.

**Risk assessment phải là 1 văn bản** (không chỉ nói miệng), với mỗi risk ghi đủ 4 trường: category, component bị ảnh hưởng, likelihood-and-impact judgment, và mitigation control kèm owner + evidence artifact. Đây là tài liệu mà security reviewer ký duyệt, và cũng là cái mà bài tập tổng hợp cuối module yêu cầu nộp.

**Checkpoint "Assess the risks"** — case customer-support agent: retrieve answer từ partner knowledge base + issue refund qua tool + ghi request log. Model answer liệt kê 4 risk:
1. Indirect prompt injection qua knowledge base → mitigation: coi retrieved text là untrusted, screen cả tool/content input chứ không chỉ user input.
2. Tool and action abuse trên refund tool → mitigation: action-authorization check chạy TRƯỚC khi refund tool execute, độc lập với output của model.
3. Token-budget exhaustion từ document lớn trong knowledge base → mitigation: chunking + input limit + budget monitoring để 1 document lớn không âm thầm truncate work.
4. Data exposure trong request log → mitigation: redaction phía server cho field nhạy cảm trước khi log ghi bất cứ gì.

### 2. Nguyên tắc "fail open vs fail closed" — guardrail failure có thể silent
Một control screening cũng là 1 dependency, nên nó fail giống mọi dependency khác: timeout, error, unreachable khi tải cao. Điểm khác biệt nguy hiểm: **1 guardrail fail vẫn có thể LOOK healthy** — khi screening service lỗi nhưng vẫn cho traffic đi qua, request vẫn chạy bình thường trong khi control không làm gì cả việc nó được đặt ra để làm. Khi guardrail lỗi, hệ thống phải làm 1 trong 2 việc: **cho qua** (fail open) hoặc **chặn lại** (fail closed). Nếu Architect không chọn rõ, code phía sau sẽ tự quyết — và default gần như luôn luôn là **fail open** (rơi về unprotected path). Cùng logic với retry/circuit breaker quanh model call trong course trước: phải quyết định hành vi của control khi nó fail, không để nó "kế thừa" bất cứ hành vi nào miễn requests vẫn chạy.

Rule quan trọng: fail open/closed là lựa chọn của Architect **chỉ áp dụng cho control do team tự build/host/config** — tách biệt với built-in model safety control của Anthropic (không operator-configurable, và các control đó KHÔNG fail open). Một operator-built guardrail âm thầm pass traffic khi lỗi còn TỆ HƠN 1 guardrail chặn traffic — nó tạo cảm giác yên tâm giả trong khi không cung cấp bảo vệ nào cả.

### 3. 3 decision point — mỗi điểm trả lời 1 câu hỏi khác nhau
- **Input screening** — chạy TRƯỚC model call, quyết định request có được đưa tới model hay không.
- **Output screening** — chạy TRƯỚC khi response tới user, quyết định thứ model tạo ra có an toàn để trả về không.
- **Tool-call authorization** — chạy TRƯỚC bất kỳ action có side-effect (gửi email, ghi DB, issue refund), quyết định caller này có được phép thực hiện action này trong context này hay không.

Vì 3 điểm nằm ở vị trí khác nhau và check thứ khác nhau, control ở 1 điểm **không làm gì** cho 2 điểm còn lại — đây là lý do 1 filter đơn lẻ không thể cover toàn bộ path (liên hệ trực tiếp tới case study "single output filter" ở phần sau).

### 4. Model-based vs deterministic — theo từng decision point
| Decision point | Model-based khi nào | Deterministic khi nào |
|---|---|---|
| Input screening | Intent mơ hồ, cần bắt jailbreak/prompt-injection pattern không thể liệt kê hết bằng rule (lightweight model classify input) | Rule rõ ràng/đã định nghĩa: blocklist, regex, length/format check — nhanh, predictable, không thể "nói chuyện" để đổi quyết định |
| Output screening | Đánh giá tính chất cần language understanding: toxicity, policy compliance (judge model chấm output) | Check chuỗi cụ thể, forbidden field, schema violation — validator bắt được với độ chắc chắn tuyệt đối |
| Tool-call authorization | **HIẾM khi dùng** — authorization cần deterministic để auditable | **GẦN NHƯ LUÔN LUÔN**: allowlist action được phép, identity check, scope validation — authorization phải là 1 quyết định chứng minh được và replay lại được |

**Tại sao chain 2 loại lại với nhau**: model-based classifier có thể bị evade — user luôn có thể phrase input để lách qua cả judge model mạnh nhất. Deterministic rule thì brittle — chỉ chặn đúng cái nó được lập trình để phát hiện, miss mọi thứ chưa được anticipate, và over-block bất cứ gì giống pattern bị hạn chế. Không control nào bắt được hết, nên 2 loại được deploy **IN SERIES** (nối tiếp) — xác định rõ mỗi loại miss cái gì để đảm bảo gap đó được 1 control khác cover có chủ đích, không bị bỏ trống.

### 5. Vector injection thứ hai: qua retrieved content và tool output
Input screening thông thường chỉ bắt instruction mà **user gửi trực tiếp**. Nó KHÔNG bắt được instruction gắn trong content mà hệ thống retrieve hoặc nhận từ tool. Trong RAG system, instruction độc hại nằm trong document retrieved sẽ đến model **SAU KHI** input screening đã pass request rồi. Trong agentic system, tool response có thể chứa instruction mà model coi là authoritative. Đây là **vector injection chủ đạo (dominant)** trong enterprise deployment có retrieval hoặc tool use — cần 1 control RIÊNG: screen retrieved content và tool output trước khi append vào context của model, dùng cùng loại model-based classifier áp cho user input. Blind spot này khác vì nguồn khác — phải identify rõ trong control design để đảm bảo coverage, không được coi input screening là đã "xong việc".

### 6. Cách API trả về refusal
Khi streaming classifier can thiệp, API trả refusal qua `stop_reason: "refusal"` kèm object `stop_details` (có từ **Claude Opus 4.7**). Object này chứa **policy category** + explanation dạng đọc được; cả 2 field null nếu refusal không map vào category có tên. Category set hiện tại (theo doc, phải re-check lúc publish, không hardcode) gồm: `cyber`, `bio`, `frontier_llm`, `reasoning_extraction`. Application nên đọc category để route xử lý khác nhau theo từng loại refusal, không coi mọi refusal là 1 event đồng nhất. Với model không có `stop_details`, handler phải tolerate việc object vắng mặt, fallback về xử lý generic. Rule bắt buộc: sau khi nhận refusal, phải **RESET context** trước khi tiếp tục — xoá/rephrase turn gây refusal, hoặc clear history. Gửi tiếp request trên context đã bị refuse sẽ tiếp tục nhận refusal khác.

### 7. Full guarded request path — nhìn như 1 hệ thống thống nhất
Request đi theo thứ tự: request đến → **input screening** quyết định có tới model không → model tạo response → **output screening** quyết định có trả về user không → tool call nào cũng phải qua **tool-call authorization** trước khi chạy. Mỗi gate có thể pass/block/fail, mỗi fail resolve theo hướng đã chọn trước (fail open/closed). Mọi gate bị block/fail đều phải được **LOG** để có thể reconstruct lại incident sau này.

Full path cụ thể: User request → Input screening (model-based cho intent mơ hồ, deterministic cho rule rõ, set **FAIL CLOSED**) → Model call → Output screening (judge model hoặc validator, set **FAIL CLOSED**) → Tool-call authorization (deterministic: allowlist + identity + scope) trước mọi side-effecting action → Response tới user, mọi gate blocked/failed đều được log.

### 8. Skill supply-chain security
Field objection thường gặp: "Skill là black box, tôi không thấy hết bên trong nó cho tới khi nó chạy, làm sao trust được?" — việc của Architect là build ra control để bù đắp cho điều đó.

Skill = code reusable/distributable đi kèm 1 instruction set, bundle lại, drop vào environment. Chính mô hình distribution đó **LÀ** supply-chain risk. 1 skill không trusted có thể mang code-execution exploit — logic chạy command, gọi network, hoặc đụng vào file ngay khi được invoke. Nguy hiểm vì skill có thể chứa instruction độc hại ẩn mà input filter/prompt screening **không thấy được** — các filter đó theo dõi conversation, nhưng threat đã được bake sẵn vào bundle từ upstream. Output monitoring có thể bắt được downstream effect sau khi việc đã xảy ra, nhưng lúc đó code đã chạy rồi.

Defense phải dịch chuyển SỚM HƠN trong chain. Trước khi trust/call 1 skill, phải **AUDIT** nó — mở bundle, đọc để tìm 2 thứ:
1. **Anomalous calls**: network request, shell execution, file-system access, credential read.
2. **Out-of-scope operations**: hành vi không match với job nó tuyên bố làm (skill formatting mà phone home = out of scope; skill summarize mà viết ra disk = out of scope).
Mục đích tuyên bố (stated purpose) của skill = baseline audit; bất cứ gì vượt ra ngoài đó là 1 finding cần điều tra.

Audit chỉ cho biết cái gì có trong bundle bạn đọc; 1 skill audit sạch vẫn có thể reach out ở **RUNTIME** để fetch code chưa từng có trong package đã audit. Vì vậy gate cần thêm 1 lớp lưới: chạy skill với **LEAST PRIVILEGE** trong 1 **SANDBOX** — hạn chế file access, hạn chế network, không có standing credential nào không cần thiết. Audit quyết định cái gì được vào; runtime confinement chặn nó lại nếu audit bỏ lỡ. Dùng CẢ HAI — không control đơn lẻ nào hoàn hảo một mình.

Cũng cần xem xét skill **được phép đến từ đâu**: chỉ trust skill từ vetted internal registry, verified publisher, signed release. Trusted-source policy giúp thu nhỏ surface phải audit và chặn bundle không trusted trước khi tới bước review. Rule of candor: không giả định platform đã screen skill sẵn cho mình — phải verify automated vetting nào thực sự tồn tại, đọc docs, xác nhận scope của bất kỳ scanning nào, tìm hiểu nó bắt được gì và không bắt được gì.

Mỗi audit phải kết thúc bằng 1 **VERDICT** được ghi lại rõ ràng: approve, reject, hoặc remediate.
- **Approve**: sạch, cho phép sử dụng.
- **Reject**: không được vào environment.
- **Remediate**: tìm ra vấn đề có thể fix — bỏ call vi phạm, sandbox hoá operation, pin version an toàn hơn, rồi audit lại.
Dù không bao giờ thấy hết được skill có thể làm gì, verdict + trusted-source policy chính là compensating control giúp Architect hành động có trách nhiệm.

### 9. "Watch Out": single output filter — trường hợp cảnh báo
Output filtering trông như 1 control rõ ràng — hiện ra như 1 ô sạch trên architecture diagram, chạy ở nơi reviewer quan sát được, nằm ở cuối path nơi risk cảm thấy cụ thể nhất (ngay trước khi user thấy response). Thêm 1 classifier ở output → diagram nhìn hoàn chỉnh, review pass. Vấn đề: việc quan trọng nhất hệ thống làm có thể đã xảy ra **TRƯỚC** khi classifier đó chạy.

Trace case cụ thể: customer service agent có tool `issue_refund`.
1. Request nhận vào (không có input screening).
2. Model emit `tool_use: issue_refund(order=...)`.
3. Tool execute, refund được issue (không có authorization gate trước side-effect).
4. Output filter kiểm tra generated text — pass, vì action nó miêu tả đã xảy ra rồi.

Refund là 1 financial action, đảo ngược 1 charge, chuyển tiền từ công ty về account khách — **không thể undo dễ dàng**. Filter output chỉ soi text, không soi action. Lý do hệ thống này bị lỗi: 1 control đặt ở ĐÚNG 1 điểm bị coi như nó cover được CẢ BA điểm. Output screening judge text, không judge action. Tool có side-effect cần authorization trước khi chạy; input chưa screen thì không có gate nào ở đầu vào. 1 filter ở cuối không phải là 1 guarded path — phải thêm đủ cả 3 filter khi cần thiết.

### 10. Checkpoint "Place the controls on the path"
Grid 2 trục: hàng ngang = placement point (Input Screening / Action Authorization trước khi tool chạy / Output Filtering), hàng dọc = check type (Model-based / Deterministic). 4 control cần đặt đúng ô:
- **A.** Jailbreak/prompt-injection screen → **Input Screening × Model-based**.
- **B.** Banned term blocklist trên user message → **Input Screening × Deterministic**.
- **C.** Toxicity judge trên generated response → **Output Screening × Model-based**.
- **D.** Refund authorization policy check trước khi tool chạy → **Action Authorization × Deterministic**.

2 ô còn trống trong grid: **Action Authorization × Model-based** (không được offer vì authorization nên deterministic, hiếm khi model-based) và **Output Screening × Deterministic** (có thể fill bằng schema/forbidden-string check, nhưng checkpoint không đưa option này) — khớp với nguyên tắc chính của lesson: authorization gần như luôn deterministic vì cần auditable.

### 11. Cost · Complexity · Risk
- **Cost**: mỗi điểm screening thêm 1 call/rule evaluation vào mọi request. 1 judge model trên output làm cost model của turn đó gần như **GẤP ĐÔI**.
- **Complexity**: 3 control point, mỗi điểm có check type riêng, fail direction riêng, log line riêng — nhiều việc build/test hơn hẳn so với 1 filter đơn lẻ.
- **Risk**: fail open là sai lầm đắt giá nhất — dưới tải cao hệ thống âm thầm mất bảo vệ trong khi vẫn nhìn như được guard, gap chỉ lộ ra khi có incident. Risk này KHÔNG áp dụng cho control API-level của Anthropic (ngoài phạm vi config của Architect) — chỉ áp dụng cho component do team tự build/operate.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Input screening (trước model call) | Muốn chặn request nguy hiểm/jailbreak trước khi tốn 1 lần model call | Thấp–trung bình: deterministic rẻ (regex/blocklist), model-based tốn thêm 1 call nhẹ | Chỉ bắt được instruction từ **user trực tiếp** — không bắt được indirect injection qua retrieved content/tool output; thiếu control này để lộ toàn bộ path phía sau | Thấp — thêm/sửa rule hoặc đổi classifier không ảnh hưởng response đã trả |
| Output screening (trước khi trả user) | Muốn chặn response không an toàn/vi phạm policy trước khi user thấy | Trung bình–cao nếu dùng judge model (gần gấp đôi cost model call của turn) | Chỉ judge **text**, không judge **action** đã xảy ra — nếu tool side-effect đã chạy trước đó thì output screening không cứu được (case "single output filter") | Trung bình — đổi rubric/judge prompt cần re-test lại |
| Tool-call authorization (trước side-effecting action) | Bất kỳ tool có side-effect thật (refund, gửi email, ghi DB) — hầu như luôn bắt buộc | Thấp — deterministic check (allowlist, identity, scope), rẻ và nhanh | Thiếu control này = tool/action abuse có thể gây hậu quả **không đảo ngược được** (tiền đã chuyển, email đã gửi) | Cao nếu thiếu ngay từ đầu — action đã có side-effect thật thì không "reverse" được bằng code, phải xử lý ngoài hệ thống (hoàn tiền tay, thu hồi email...) |
| Fail open khi guardrail lỗi | Hầu như không nên chọn chủ động — chỉ xảy ra khi không set rõ, hoặc khi ưu tiên tuyệt đối là uptime hơn safety (hiếm, cần approval rõ ràng) | Thấp về mặt uptime ngắn hạn (request vẫn chạy) | Cao — hệ thống "trông" vẫn được guard trong khi hoàn toàn không có bảo vệ; gap chỉ lộ ra khi có incident xảy ra thật | Cao — phải phát hiện qua incident/audit rồi mới sửa lại default, tổn thất đã xảy ra trong lúc đó |
| Fail closed khi guardrail lỗi | Default nên chọn cho control do team tự build (input/output screening) | Cao hơn ngắn hạn — request bị block/degrade khi control lỗi, ảnh hưởng UX/uptime | Thấp hơn — an toàn được giữ nguyên khi control degrade, đúng bản chất "guardrail" | Thấp — chỉ là switch fail-direction, không ảnh hưởng dữ liệu đã xử lý |
| Model-based check | Intent/quality cần judgment: jailbreak pattern không liệt kê hết được, toxicity, policy compliance | Trung bình–cao (thêm 1 API call), latency tăng | Có thể bị **evade** bằng cách phrase khéo input | Trung bình — sửa prompt/threshold của classifier, cần re-eval |
| Deterministic check | Rule rõ ràng, đã định nghĩa: blocklist, regex, schema, allowlist, identity/scope | Rất thấp — gần như free, chạy nhanh | **Brittle**: chỉ bắt đúng cái được lập trình, miss cái chưa anticipate, có thể over-block | Thấp — sửa rule/list trực tiếp, không cần re-train/re-calibrate |
| Chain model-based + deterministic (thứ tự tuỳ decision point) | Mặc định nên làm ở input & output screening — không control nào bắt hết mọi thứ | Cộng thêm cost/latency của cả 2 loại | Nếu chỉ dùng 1 loại: gap của loại đó bị bỏ trống hoàn toàn (evade hoặc miss-unanticipated) | Trung bình — thêm 1 lớp check mới vào pipeline đã có |
| Audit skill trước khi trust (approve/reject/remediate) | Bắt buộc trước khi đưa 1 skill mới vào environment, đặc biệt skill không từ nguồn đã vetted | Trung bình — thời gian đọc bundle, review code | Không audit = code-execution exploit ẩn trong skill có thể chạy ngay khi invoke, input filter không thấy được | Thấp nếu remediate sớm (strip call, pin version); cao nếu skill đã chạy production rồi mới phát hiện |
| Runtime sandbox least-privilege cho skill | Luôn nên có, kể cả sau khi audit đã approve — vì audit chỉ biết bundle đã đọc, không biết runtime fetch thêm gì | Trung bình — công sức setup sandbox/permission boundary | Không có = skill sạch lúc audit vẫn có thể reach network/fetch code mới ngoài tầm audit ban đầu | Thấp — sandbox là lớp hạ tầng, không phụ thuộc skill cụ thể |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Input screening | Control chạy TRƯỚC model call, quyết định request có được đưa tới model hay không |
| Output screening | Control chạy TRƯỚC khi response tới user, quyết định output của model có an toàn để trả về không |
| Tool-call authorization | Control chạy TRƯỚC bất kỳ action có side-effect, quyết định caller có được phép thực hiện action đó trong context này không |
| Direct prompt injection | User chủ động viết input để override system instruction |
| Indirect prompt injection | Instruction độc hại đến qua retrieved content hoặc tool output, model coi là trusted; input screening thông thường không bắt được |
| Token-budget exhaustion | Input bị làm quá khổ/padding để ăn hết context/output budget, gây truncate work hoặc tăng cost |
| Tool and action abuse | Model bị dẫn dụ gọi tool side-effecting ngoài policy cho phép |
| Data exposure | Dữ liệu nhạy cảm lọt vào context window hoặc logs, độc lập với hành vi model |
| Fail open | Khi guardrail lỗi, hệ thống cho traffic đi qua không được screen (default ngầm nếu không chọn rõ) |
| Fail closed | Khi guardrail lỗi, hệ thống chặn action/request lại cho tới khi control khoẻ lại |
| Model-based check | Dùng model (classifier/judge) để đánh giá input/output cần judgment/interpretation |
| Deterministic check | Dùng rule cố định (blocklist, regex, schema, allowlist) để đánh giá, kết quả predictable |
| stop_reason: "refusal" | Giá trị trả về của Messages API khi streaming classifier can thiệp và chặn response |
| stop_details | Object kèm refusal (từ Claude Opus 4.7) chứa policy category + explanation đọc được |
| Policy category (refusal) | Nhãn phân loại lý do refusal, ví dụ cyber / bio / frontier_llm / reasoning_extraction |
| Context reset (sau refusal) | Yêu cầu bắt buộc: xoá/rephrase turn gây refusal hoặc clear history trước khi tiếp tục, tránh refusal lặp lại |
| Risk assessment (deliverable) | Văn bản ghi category, component, likelihood-impact, mitigation+owner+evidence cho mỗi risk — security reviewer ký duyệt |
| Skill supply-chain security | Rủi ro từ việc skill là code + instruction bundle distributable, có thể mang exploit ẩn |
| Anomalous calls (skill audit) | Network request, shell execution, file-system access, credential read phát hiện khi audit skill |
| Out-of-scope operations | Hành vi của skill không match với job nó tuyên bố làm — dấu hiệu cần điều tra khi audit |
| Least-privilege sandbox | Chạy skill với quyền tối thiểu (hạn chế file/network/credential) làm lớp phòng vệ thứ 2 sau audit |
| Trusted-source policy | Chỉ cho phép skill từ registry đã vetted/verified publisher/signed release, giảm surface phải audit |
| Audit verdict | Kết luận bắt buộc sau mỗi audit skill: approve / reject / remediate |
| Single output filter (anti-pattern) | Chỉ đặt 1 control ở output nhưng coi như nó cover cả input + tool-call — bỏ lọt side-effect đã xảy ra trước đó |
| Chaining controls (in series) | Đặt model-based + deterministic nối tiếp nhau vì mỗi loại miss theo cách khác nhau, không loại nào bắt hết |

## Gotchas / bẫy hay gặp
- [ ] Chỉ screen **user input** rồi nghĩ đã cover injection — quên rằng indirect prompt injection qua retrieved content/tool output là vector CHỦ ĐẠO trong enterprise deployment có RAG/tool use, cần control riêng
- [ ] Guardrail lỗi nhưng không set rõ fail-direction → default rơi về **fail open**, hệ thống mất bảo vệ mà vẫn "trông" như đang được guard (silent failure)
- [ ] Đặt duy nhất 1 output filter ở cuối path rồi coi diagram là "hoàn chỉnh" — side-effecting tool (refund, gửi email) đã chạy xong TRƯỚC khi filter đó nhìn thấy bất cứ gì
- [ ] Dùng model-based check cho **tool-call authorization** — sai nguyên tắc: authorization phải deterministic để auditable/replayable, model-based ở đây gần như không dùng
- [ ] Coi fail-open/fail-closed là lựa chọn áp dụng luôn cho built-in model safety control của Anthropic — sai, đó là control operator-configurable của TEAM, tách biệt với control platform-level (không fail open)
- [ ] Sau khi nhận `stop_reason: "refusal"`, gửi tiếp request trên cùng context đã bị refuse — sẽ tiếp tục nhận refusal khác, phải reset/rephrase context trước
- [ ] Audit 1 skill xong rồi tin tưởng hoàn toàn, không chạy trong sandbox — bỏ qua việc skill sạch lúc audit vẫn có thể fetch code mới ở runtime, ngoài phạm vi bundle đã đọc
- [ ] Giả định platform tự động screen/vet skill cho mình mà không verify actual scope của automated vetting đó — vi phạm "rule of candor"

## Exam tips
- Câu scenario cho 1 control cụ thể (ví dụ "toxicity judge trên response") → xác định đúng **placement point** (input/output/tool-call authorization) trước, rồi mới xác định **check type** (model-based/deterministic) — 2 trục độc lập, đề hay bẫy bằng cách gộp nhầm.
- Nếu đề nói đến "authorization" hoặc "before a side-effecting action executes" → mặc định trả lời **deterministic**, gần như không có trường hợp đúng là model-based (vì cần auditable/replayable).
- Nếu đề mô tả injection đến từ **retrieved document** hoặc **tool response** (không phải user gõ trực tiếp) → đáp án là control riêng để screen retrieved content/tool output, KHÔNG phải "input screening đã cover rồi".
- Câu hỏi "guardrail service timeout/lỗi thì hệ thống nên làm gì" → nhận diện đây là câu hỏi fail-open vs fail-closed; đáp án đúng thường là **fail closed** cho control team tự build, và nhấn mạnh im lặng fail-open là bẫy nguy hiểm nhất (trông vẫn an toàn nhưng không bảo vệ gì).
- Case có tool side-effect (refund, gửi email...) mà chỉ có 1 control ở output → nhận diện ngay đây là anti-pattern "single output filter", thiếu tool-call authorization trước khi action chạy.

## Code / config snippets
```python
# Minh hoạ thứ tự 3 decision point trong "full guarded request path":
# input screening -> model call -> output screening -> tool-call authorization
# Nguyên tắc áp dụng: FAIL CLOSED ở mọi bước cho control do team tự build
# (khác với built-in safety control của Anthropic, không operator-configurable).

class GuardrailError(Exception):
    """Raise khi 1 control lỗi (timeout/unreachable) -> luôn fail closed, không âm thầm pass."""
    pass


def input_screening(user_message: str) -> bool:
    # Deterministic check trước (rẻ, nhanh): blocklist / regex / length check
    if len(user_message) > MAX_INPUT_LEN or contains_banned_term(user_message):
        return False
    # Model-based check sau: bắt jailbreak/prompt-injection pattern không liệt kê hết được bằng rule
    try:
        verdict = jailbreak_classifier(user_message)  # lightweight model classify input
    except Exception as e:
        # Guardrail lỗi -> FAIL CLOSED, không cho request đi tiếp
        raise GuardrailError("input_screening unavailable") from e
    return verdict == "safe"


def screen_retrieved_content(chunks: list[str]) -> bool:
    # Control RIÊNG cho indirect prompt injection qua retrieved content / tool output
    # KHÔNG được coi input_screening() ở trên đã cover việc này
    return all(jailbreak_classifier(c) == "safe" for c in chunks)


def output_screening(model_output: str) -> bool:
    # Deterministic: schema/forbidden-string check trước nếu áp dụng được
    if violates_schema(model_output):
        return False
    # Model-based: judge model chấm toxicity/policy compliance (cost ~ gấp đôi turn này)
    try:
        score = judge_model_score(model_output)
    except Exception as e:
        raise GuardrailError("output_screening unavailable") from e
    return score.passes_threshold()


def tool_call_authorization(caller_identity: str, action: str, scope: dict) -> bool:
    # GẦN NHƯ LUÔN deterministic vì authorization phải auditable + replayable
    # allowlist + identity check + scope validation, KHÔNG dùng model-based ở đây
    return (
        action in ALLOWED_ACTIONS
        and caller_identity in AUTHORIZED_CALLERS
        and scope_is_valid(scope)
    )


def guarded_call(user_message: str, retrieved_chunks: list[str], tool_request: dict | None):
    """
    Full guarded path, fail-closed ở mọi bước, log mọi gate bị block/fail
    để có thể reconstruct incident sau này.
    """
    try:
        if not input_screening(user_message):
            log_blocked("input_screening", user_message)
            return refuse_response()

        if not screen_retrieved_content(retrieved_chunks):
            log_blocked("retrieved_content_screening", retrieved_chunks)
            return refuse_response()

        model_output = call_model(user_message, retrieved_chunks)

        if not output_screening(model_output):
            log_blocked("output_screening", model_output)
            return refuse_response()

        # Tool-call authorization PHẢI chạy trước khi tool có side-effect thực thi
        # (đây là chỗ case study "single output filter" bị thiếu -> refund chạy trước khi check)
        if tool_request:
            if not tool_call_authorization(
                tool_request["caller"], tool_request["action"], tool_request["scope"]
            ):
                log_blocked("tool_call_authorization", tool_request)
                return refuse_response()
            execute_tool(tool_request)

        return model_output

    except GuardrailError as e:
        # Bất kỳ control nào lỗi -> FAIL CLOSED, không rơi về unprotected path
        log_blocked("guardrail_error", str(e))
        return refuse_response()
```

## Câu hỏi chưa rõ
- ?
