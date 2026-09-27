# C2.3 — Sizing use case: volume, token, cost & feasibility

> **Course:** 2 — Enterprise Integration & Production (158 min) · **Exam domain:** D1 (17%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Create a use case by estimating call volume, token consumption, and cost, assess technical feasibility against the four AI properties from AI Fluency Foundations, and translate a business problem into a scoped solution architecture with explicit boundary conditions

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Bối cảnh:** production readiness checklist (lesson trước) nói hệ thống phải đạt gì để viable — quality (đo bằng eval) + reliability (đo bằng architecture control: retry, fallback, circuit breaker). **Sizing** là bước trả lời: bài toán business cụ thể này có đạt được bar đó không, và constraint nào chi phối design. Feasibility luôn rơi vào 1 trong 3 state: **feasible as scoped / feasible with constraints / not feasible** — gọi đúng state là thứ làm scoping document có giá trị.

- **Sizing a use case — xây cost model TRƯỚC khi viết code, 4 bước:**
  1. **Estimate call volume**: số request/ngày hoặc /tháng — lấy từ business requirement (business owner cung cấp), KHÔNG suy từ intuition của developer, không suy từ sample dataset. VD: agent xử lý 1.000 conversation/ngày → 1.000+ Claude call/ngày (chưa tính multi-turn continuation call).
  2. **Set token budget per request**: gồm input token (system prompt + retrieved context + user message) và output token (response length kỳ vọng). Phải model **distribution**, không chỉ average — nếu document length dao động mạnh, cost model phải tính cả case điển hình và case cực đại (tail). Nếu system prompt dài và ổn định → dùng **prompt caching** để giảm input cost, nhưng phải có `cache_control` marker rõ ràng trong request; **cache write** tốn per-token cao hơn input thường (phải tính write cost cho lần dùng đầu); **cache TTL** mặc định 5 phút — workload có tần suất request thấp hơn TTL sẽ không hiện thực hoá được saving từ cache một cách ổn định.
  3. **Project monthly cost**: (call volume × input token count × input rate) + (call volume × output token count × output rate) — input/output luôn có rate khác nhau ở mọi model tier. Nếu có caching, dùng cache read rate cho token đã cache (không dùng standard input rate). Verify rate hiện tại tại platform.claude.com/docs/en/about-claude/pricing trước khi finalize. So kết quả với cost ceiling từ production readiness checklist — nếu vượt ceiling, phải đổi architecture trước khi viết code. Batch API (ví dụ giảm 50% giá, hỗ trợ tới 100.000 request/batch — số thực tế phải verify tại link trên) là 1 cost alternative cho workload mà SLA cho phép xử lý asynchronous; với workload regulated (PHI...), phải verify Batch API có nằm trong BAA/compliance configuration của partner trước khi route data qua.
  4. **Run sensitivity analysis**: cost thay đổi ra sao nếu call volume gấp đôi? Nếu token distribution lệch về tail? Sensitivity analysis cho biết cost model fragile tới đâu, assumption nào cần verify lại với business owner trước khi commit design.

- **Scoping a use case — 4 bước discovery, bỏ bước nào cũng tạo ra commitment không sống được qua lần trao đổi tiếp theo với business owner:**
  1. **Business requirement → capability list**: tách từng capability riêng biệt, không để ở dạng goal mơ hồ. "Process insurance claims" là goal; capability cụ thể là: extract structured field từ claim document, lookup policy coverage, route claim theo type/value, draft adjuster notification. Tách riêng để assign đúng owner cho từng capability.
  2. **Capability list → architecture sketch**: với mỗi capability, quyết định nó thuộc về đâu — Claude own? hệ thống hiện có? cần human-in-the-loop? Đây chính là bước decomposition (từ Module 1) áp vào use case cụ thể.
  3. **Architecture sketch → boundary conditions**: phát biểu rõ điều kiện mà architecture hoạt động và điều kiện mà nó KHÔNG hoạt động. Feasibility = verdict + constraint làm verdict đó đúng. VD: architecture chạy tốt với document ≤ 20 trang nhưng fail với document dài hơn — đó là boundary condition phải document lại.
  4. **Boundary conditions → scope trong SOW**: SOW (statement of work) chứa các boundary condition này, để cả dev team và business owner cùng hiểu hệ thống được thiết kế xử lý gì và cái gì explicitly out of scope.

- **Technical feasibility assessment qua 4 AI properties** (từ AI Fluency Foundations) — hỏi "Claude làm được task này không" chỉ là capability check; 4 property cho cách xác định design cần compensating control ở đâu và control đó là gì:
  1. **Next-token prediction**: câu hỏi feasibility — task cần probabilistic generation (classification, summarization, drafting — model làm tốt) hay cần precision trên giá trị cụ thể (account number, policy date, claim amount — cần verify với source of truth)? Compensating control: generator-verifier loop, code-based eval trên giá trị extract được, tool call để lấy quantitative data.
  2. **Knowledge**: task có phụ thuộc thông tin rare/contested/recent/domain-specific mà training data có thể không có? Nếu có, design phải mang knowledge vào context window, không dựa vào model tự "biết". Compensating control: RAG cho stable knowledge, tool call cho live-state data, flag uncertainty với contested claim.
  3. **Working memory**: input có nằm gọn trong context window, hay task cần xử lý input tổng hợp vượt window (long document, multi-document task, extended conversation)? Compensating control: chunking strategy, progressive context loading, summarization qua các turn, pipeline architecture cho input vượt context limit.
  4. **Steerability**: instruction có specific/concrete/verifiable không? Instruction abstract/ambiguous, reasoning chain dài, task cần tính toán numerical/logical chính xác đều là nơi model dễ drift khỏi intent. Compensating control: system prompt với explicit output schema, structured output, code execution cho độ chính xác số học, evaluator-optimizer loop.

- **3 feasibility verdict và cách document:**
  1. **Feasible as scoped**: cả 4 AI property đều thuận cho mỗi capability, cost model trong ceiling, latency p95 trong SLA, không capability nào cần compensating control làm đổi architecture. Document: state rõ assumption — verdict này sẽ chuyển thành "infeasible with constraints" nếu assumption thay đổi.
  2. **Feasible with constraints**: design chỉ hoạt động đúng dưới điều kiện cụ thể phải enforce (VD: ngưỡng độ dài document, lịch refresh retrieval index, human review gate cho output confidence thấp). Document từng constraint rõ ràng, và với mỗi constraint bị vi phạm, nêu rõ failure mode tương ứng.
  3. **Not feasible**: có ít nhất 1 capability gặp giới hạn AI property không thể compensate trong phạm vi scope/budget, hoặc cost model vượt ceiling ở mức không thể đóng lại bằng đổi model tier/caching/architecture. Verdict "not feasible" là 1 đánh giá ĐÚNG, cứu engagement khỏi 1 thất bại tốn kém hơn về sau. Document rõ constraint nào disqualifying và vì sao; nếu giảm scope có thể đổi verdict, nêu rõ phương án đó và để business owner chọn.

- **Business value & ROI mapping — nối feasible design với justified investment:** feasibility verdict chỉ nói hệ thống CÓ THỂ build trong budget/constraint, không nói việc build có ĐÁNG hay không. ROI mapping nối scoped architecture với outcome tài chính/vận hành theo ngôn ngữ business owner đang dùng: hours saved, error rate giảm, cycle time ngắn lại, revenue được bảo vệ.
  - **5 pillar của business case**: efficiency (cùng việc, nhanh/rẻ hơn), transformation (việc trước đây infeasible giờ làm được), productivity (nhiều output hơn với cùng người), solution cost (chi phí vận hành hệ thống), performance SLA (service level deployment phải giữ).
  - **Mechanism**: so sánh baseline state (hiện tại) với projected state (có Claude), đo cùng 1 business unit. Value = hiệu số 2 state, trừ đi cost vận hành hệ thống (tái dùng cost figure từ sizing model).
  - **4 bước xây ROI mapping:**
    1. Name baseline bằng business unit — lấy từ operational data thật của business owner (VD: analyst hours/claim, số ngày trung bình để resolve), không lấy từ intuition.
    2. Predict projected state cùng unit — nếu feasibility verdict yêu cầu human review, projection phải tính cả cost đó vào, không được project full automation khi design có human-in-the-loop.
    3. Trừ run cost khỏi sizing model — lấy projected monthly cost từ sizing làm recurring cost của state mới; value = gain ở bước 2 trừ run cost này. Build cost tách riêng, tính ở payback period bước 4.
    4. State payback period + sensitivity — payback period = thời gian operational gain tích lũy đủ bù build cost + run cost; nêu luôn period đó dịch chuyển ra sao nếu assumption về volume/gain sai.
  - **Output**: 1 value statement ngắn gửi kèm feasibility verdict cho business owner — nối "Có build được không?" và "Có đáng build không?" lại với nhau; cả 2 artifact đều đi vào SOW.
  - **3 lỗi ROI map thường gặp:**
    1. Baseline ước lượng thay vì đo thật — khi business owner không có clean operational data, baseline bị lấy từ intuition, làm gain có vẻ lớn hơn thực tế; lộ ra khi finance hỏi nguồn của baseline lúc review business case.
    2. Projection giả định full automation khi design cần human review — verdict có human review gate nghĩa là labor GIẢM, không phải BIẾN MẤT; gap lộ ra ở operational period đầu tiên sau launch khi hours thực tế không giảm như đã hứa.
    3. Run cost lấy từ average thay vì sizing distribution — dùng average token cost thay vì distribution làm understate recurring cost, overstate net value; nặng nhất ở workflow có input heavy-tailed.

- **Cost · Complexity · Risk:**
  - Cost: sizing dựa trên average token count sẽ underestimate cost khi có request lớn hơn nhiều so với số còn lại — sai ở đây nghĩa là phải renegotiate architecture SAU KHI contract đã ký.
  - Complexity: feasibility assessment bỏ qua bất kỳ AI property nào có nguy cơ bỏ lỡ 1 constraint làm đổi design. Working memory là property bị overlook nhiều nhất — vì nó ít lộ ra lúc dev trên input nhỏ/sạch, nhưng sẽ lộ ra ở production.
  - Risk: verdict "feasible with constraints" mà không được document sẽ trở thành hệ thống infeasible khi constraint bị vi phạm ở production. Constraint là 1 phần của design, có trọng lượng như chính architecture mà nó qualify.

- **Case study "Scoping call bỏ qua constraint" (Watch Out):** Partner mô tả use case document review assistant cho legal contract. Architect confirm feasibility ("We can do that") và cam kết timeline (6 tuần) ngay — TRƯỚC KHI hỏi volume/SLA/input size. 2 tuần vào build, partner mới tiết lộ: 800 contract/ngày, một số framework agreement dài tới 300 trang, cần kết quả dưới 30 giây.
  - **Điều gì sai**: verdict feasibility bị issue trước khi gom đủ 3 constraint cốt lõi: call volume (800/ngày), input size (tới 300 trang), latency (30 giây).
  - Document 300 trang có fit context window hay không phụ thuộc model tier — model 1M token context xử lý được không cần chunk; model 200k token context cần chunking strategy cho document dài nhất. → context window capacity là 1 phần của quyết định model tier, không phải assumption đã settle sẵn.
  - Ở volume 800 request/ngày, yêu cầu latency 30 giây thực ra KHÔNG khắt khe như tưởng — trung bình 1 request/108 giây, xử lý sequential vẫn viable, không cần parallelize. Ở rate này, volume gây áp lực lên COST, không phải latency. Latency thực ra do task complexity, model size, output length quyết định — đó là các biến cần dùng để quyết định model tier.
  - Architect trả lời câu hỏi capability đúng là bước cần thiết ĐẦU TIÊN, nhưng lại biến nó thành bước CUỐI CÙNG luôn — commitment được đưa ra trước khi design thực sự khả thi.
  - **Bài học (Watch Out chính):** capability question bị trả lời trước khi constraint question được hỏi. Volume, latency, input-size là INPUT cho feasibility verdict, không phải thứ hỏi sau. Verdict chỉ đáng tin bằng đúng mức constraint đã gom được trước khi ra verdict — **thứ tự đúng là hỏi constraint trước, xác nhận capability sau, không phải ngược lại**.

- **Checkpoint "Justify the feasibility call" — 3 scenario, chọn đúng verdict + đúng load-bearing constraint (verdict đơn lẻ không đủ, phải kèm constraint làm nó defensible):**
  1. Research assistant tóm tắt report 10-40 trang, draft briefing; 50 report/tuần, 24h turnaround, ceiling $500/tháng → **Feasible as scoped** — input size fit context window, volume/latency/cost đều trong range ở Sonnet tier, không AI property nào tạo constraint disqualifying.
  2. Delay predictor đọc carrier email unstructured, extract delay reason + ETA mới, ghi vào order-management system; 5.000 email/ngày, dưới 10 giây, $1.000/tháng → **Feasible with constraints** — load-bearing constraint là extraction accuracy trên 1 transactional write (ghi trực tiếp vào system of record), nên cần code-based eval trên extraction accuracy CỘNG human review gate cho low-confidence extraction trước khi ghi.
  3. Trading recommendation real-time từ market condition hiện tại + proprietary model, dưới 2 giây → **Not feasible as described** — load-bearing constraint là live-state knowledge gap: real-time market data cần tool call tới live feed, và việc round-trip đó có fit trong budget 2 giây hay không PHẢI được validate trước khi issue bất kỳ verdict nào.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| **Feasible as scoped** | Cả 4 AI property thuận, cost/latency trong ceiling/SLA, không capability nào cần compensating control đổi architecture | Thấp — chỉ cần state rõ assumption khi document | Assumption thay đổi (volume tăng, document dài hơn) → verdict tự động rơi xuống "feasible with constraints" mà không ai nhận ra nếu không document assumption | Thấp nếu đã document assumption rõ; cao nếu không — phải điều tra lại từ đầu khi production lệch |
| **Feasible with constraints** | Design chỉ đúng dưới điều kiện cụ thể (document length threshold, retrieval refresh schedule, human review gate cho low-confidence output) | Trung bình — cần thêm compensating control (eval, human gate, chunking...) và enforce constraint trong runtime | Constraint không được document/enforce → hệ thống thành infeasible ngay khi constraint bị vi phạm ở production, nhưng không ai phát hiện sớm | Trung bình — thêm/sửa constraint + control tương ứng, không cần đổi cả architecture |
| **Not feasible** | ≥1 capability gặp giới hạn AI property không compensate được trong scope/budget, hoặc cost vượt ceiling mà không tier/cache/architecture nào đóng lại được | Cost cơ hội (mất engagement) nhưng tránh được chi phí lớn hơn về sau | Nếu ra verdict sai (thật ra feasible) → mất cơ hội kinh doanh; nếu đúng → cứu engagement khỏi failure tốn kém hơn | Cao — cần thu hẹp scope và chạy lại toàn bộ feasibility assessment để đổi verdict |
| Sizing dựa trên **average token count** | Không nên chọn làm mặc định — chỉ tạm dùng khi chưa có dữ liệu phân phối input | Rẻ, nhanh để làm cost model ban đầu | Underestimate cost khi có request lớn hơn nhiều số còn lại (heavy-tailed input); lỗi lộ ra SAU khi contract đã ký | Cao — phải renegotiate architecture/budget sau khi đã commit |
| Sizing dựa trên **distribution + sensitivity analysis** | Mặc định nên chọn cho mọi cost model nghiêm túc, đặc biệt khi document/input length dao động mạnh | Cao hơn một chút về effort (phải model tail case, chạy what-if volume x2, token shift) | Vẫn có risk nếu business owner cung cấp data volume sai, nhưng risk thấp hơn hẳn so với dùng average | Thấp — sensitivity analysis đã sẵn có câu trả lời "nếu assumption sai thì cost đổi thế nào" |
| **Batch API** cho workload async-tolerant | SLA cho phép xử lý bất đồng bộ, cần giảm cost (VD ~50% so với standard API) | Giảm cost đáng kể nhưng tăng latency (không real-time) | Với workload regulated (PHI...) cần verify BAA/compliance trước — route sai có thể vi phạm compliance | Trung bình — đổi lại standard API cần tính lại cost model và latency SLA |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Sizing (a use case) | Xây cost model (call volume × token budget × model tier) trước khi viết code, để validate architecture với budget |
| Call volume | Số request/ngày hoặc /tháng — phải lấy từ business owner, không suy từ intuition hoặc sample dataset |
| Token budget | Tổng input token (system prompt + context + user message) + output token (response length) cho mỗi request |
| Prompt caching / `cache_control` | Cơ chế cache phần input ổn định (system prompt dài) để giảm cost input token ở các lần gọi sau |
| Cache write cost | Chi phí per-token cao hơn input thường, tính cho lần đầu ghi vào cache |
| Cache TTL | Thời gian cache còn hiệu lực, mặc định 5 phút — request thưa hơn TTL sẽ không có saving ổn định |
| Batch API | API xử lý bất đồng bộ, giá rẻ hơn (ví dụ ~50%) đổi lại không real-time; có giới hạn số request/batch |
| Sensitivity analysis | Kiểm tra cost model phản ứng thế nào khi assumption thay đổi (volume x2, token distribution lệch tail) |
| Capability list | Danh sách các khả năng cụ thể tách ra từ 1 business goal mơ hồ, mỗi capability gán 1 owner |
| Boundary condition | Điều kiện mà architecture hoạt động đúng / không đúng — 1 phần bắt buộc của feasibility verdict |
| SOW (Statement of Work) | Văn bản chứa boundary condition, xác định phạm vi hệ thống được thiết kế xử lý và cái gì out of scope |
| 4 AI properties | Next-token prediction, Knowledge, Working memory, Steerability — khung đánh giá feasibility theo từng giới hạn của model |
| Next-token prediction (property) | Model mạnh ở task probabilistic (classify, summarize, draft), yếu ở việc cần precision trên giá trị cụ thể |
| Working memory (property) | Giới hạn context window — input/multi-document/conversation dài có thể vượt quá khả năng xử lý gọn trong 1 lượt |
| Steerability (property) | Khả năng model bám đúng instruction — abstract/ambiguous instruction hoặc numerical precision dễ làm model drift |
| Compensating control | Cơ chế design (RAG, tool call, chunking, generator-verifier loop, evaluator-optimizer...) bù cho giới hạn của 1 AI property |
| Feasibility verdict | Kết luận feasible as scoped / feasible with constraints / not feasible, LUÔN đi kèm constraint làm verdict đó defensible |
| Load-bearing constraint | Constraint cụ thể quyết định verdict đúng hay sai — nếu bỏ constraint này, verdict không còn đứng vững |
| ROI mapping | Nối feasibility verdict (build được) với value statement (đáng build) bằng baseline vs projected state |
| Baseline state | Trạng thái vận hành hiện tại, đo bằng business unit thật (VD: hours/claim) từ data của business owner, không phải ước lượng |
| Projected state | Trạng thái vận hành dự kiến sau khi triển khai Claude, đo cùng business unit với baseline |
| Payback period | Thời gian operational gain tích lũy đủ bù build cost + run cost |
| 5 pillars of business case | Efficiency, transformation, productivity, solution cost, performance SLA |

## Gotchas / bẫy hay gặp
- [ ] Confirm feasibility/capability ("we can do that") NGAY khi demo chạy tốt, trước khi hỏi volume/latency/input-size — case study "scoping call" trong lesson: cam kết timeline 6 tuần rồi 2 tuần sau mới biết 800 contract/ngày, document 300 trang, SLA 30 giây
- [ ] Sizing cost model dựa trên **average token count** thay vì distribution — bỏ lỡ request lớn bất thường (tail), lỗi chỉ lộ ra sau khi contract đã ký, phải renegotiate
- [ ] Bỏ qua property **Working memory** khi feasibility assessment — property này ít lộ lúc dev trên input nhỏ/sạch nhưng chắc chắn lộ ở production với document dài/multi-document
- [ ] Verdict "feasible with constraints" nhưng KHÔNG document constraint tường minh — constraint bị vi phạm ở production thì hệ thống thành infeasible mà không ai kịp phát hiện
- [ ] Nhầm latency constraint với volume constraint — volume cao không tự động nghĩa là latency gấp; phải chia call volume ra request/giây thực tế rồi mới đánh giá (VD 800/ngày ≈ 1 request/108s, không cần parallelize)
- [ ] ROI mapping lấy baseline từ ước lượng/intuition thay vì đo thật từ operational data của business owner
- [ ] ROI mapping giả định full automation khi feasibility verdict có human review gate — labor giảm, không biến mất hoàn toàn
- [ ] Dùng cache khi request frequency thấp hơn cache TTL (5 phút) — kỳ vọng saving ổn định nhưng thực tế không đạt được

## Exam tips
- Câu scenario hỏi "chọn feasibility verdict đúng" luôn có bẫy: verdict đúng nhưng đi kèm constraint SAI (hoặc thiếu). Luôn tìm đáp án có **verdict + load-bearing constraint** khớp nhau, verdict đứng một mình không đủ điểm.
- Nếu task cần data real-time / live-state (market data, inventory tức thời...) mà chưa validate được tool-call round-trip có fit latency budget hay không → xu hướng đáp án đúng là **not feasible as described** (property Knowledge — live-state gap), không phải "feasible, Claude đã biết".
- Nếu task ghi trực tiếp vào system of record (transactional write) dựa trên extraction từ unstructured input → xu hướng đáp án đúng là **feasible with constraints**, load-bearing constraint là accuracy trên extraction + cần human review gate cho low-confidence case, không phải "not feasible" hay "feasible as scoped" trơn.
- Volume cao không đồng nghĩa latency khắt khe — luôn quy đổi ra request/giây trước khi đánh giá liệu sequential processing có viable, tránh chọn nhầm đáp án "cần parallelize/model nhỏ hơn vì volume cao".
- Nhớ thứ tự đúng của quy trình: gom constraint (volume, latency, input size) TRƯỚC, issue feasibility verdict SAU — đề thi hay đảo ngược thứ tự này trong distractor.

## Code / config snippets
```python
# Minh hoạ đơn giản Step 1-3 của "How to size a use case":
# ước tính monthly cost từ call volume + token budget + model tier,
# có so sánh giữa sizing theo average vs. có áp dụng cache rate cho phần input được cache.

# Giá minh hoạ (USD / 1 triệu token) — LUÔN verify số thật tại
# platform.claude.com/docs/en/about-claude/pricing trước khi dùng số liệu này để ra quyết định
PRICING = {
    "sonnet": {"input": 3.0, "output": 15.0, "cache_read": 0.30},  # cache_read rẻ hơn input thường
    "haiku":  {"input": 0.80, "output": 4.0, "cache_read": 0.08},
}

def project_monthly_cost(
    call_volume_per_day: int,      # Step 1: call volume — lấy từ business owner
    input_tokens: int,             # Step 2: token budget - phần input (chưa cache)
    cached_input_tokens: int,      # phần input được prompt caching hit (VD: system prompt dài, ổn định)
    output_tokens: int,            # Step 2: token budget - phần output
    model_tier: str = "sonnet",    # model tier quyết định rate áp dụng
) -> dict:
    rates = PRICING[model_tier]
    monthly_calls = call_volume_per_day * 30  # quy đổi call/ngày -> call/tháng (xấp xỉ)

    # Step 3: project monthly cost — input, cached input, và output tính rate riêng
    cost_input = monthly_calls * input_tokens * rates["input"] / 1_000_000
    cost_cached = monthly_calls * cached_input_tokens * rates["cache_read"] / 1_000_000
    cost_output = monthly_calls * output_tokens * rates["output"] / 1_000_000
    total = cost_input + cost_cached + cost_output

    # So sánh nếu KHÔNG dùng cache (toàn bộ input tính rate thường) để thấy caching saving
    cost_without_cache = monthly_calls * (input_tokens + cached_input_tokens) * rates["input"] / 1_000_000 \
        + cost_output

    return {
        "monthly_calls": monthly_calls,
        "projected_cost_with_cache": round(total, 2),
        "projected_cost_without_cache": round(cost_without_cache, 2),
        "caching_saving": round(cost_without_cache - total, 2),
    }

# Ví dụ: legal contract review — 800 contract/ngày (case study "scoping call"),
# system prompt ổn định 2.000 token (cache được), input còn lại 3.000 token, output 500 token
result = project_monthly_cost(
    call_volume_per_day=800,
    input_tokens=3_000,
    cached_input_tokens=2_000,
    output_tokens=500,
    model_tier="sonnet",
)
print(result)
# So kết quả này với cost ceiling từ production readiness checklist (Step 3):
# nếu vượt ceiling -> phải đổi model tier / tăng cache hit / xét Batch API trước khi code
```

## Câu hỏi chưa rõ
- ?
