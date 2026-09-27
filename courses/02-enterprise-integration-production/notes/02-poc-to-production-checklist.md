# C2.2 — POC-to-production checklist & reliability patterns

> **Course:** 2 — Enterprise Integration & Production (158 min) · **Exam domain:** D1 (17%) + D4 (16%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Work through the POC-to-production checklist, mapping cost and latency to a budget, specifying reliability patterns (retries, fallbacks, circuit breakers), naming failure modes for the chosen architecture, and articulating the mitigation for each, including how to make agentic workflows production-reliable

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **POC-to-production gap:** eval suite (lesson C2.1) chứng minh hệ thống *behave đúng*, nhưng không nói được hệ thống có *affordable* ở volume mà partner kỳ vọng hay không. Đó là gap giữa Proof of Concept (POC) và production, có **4 dimension**: cost, latency, reliability, failure modes — cả 4 đều **invisible trong demo**. Ngoài ra, POC cũng là tín hiệu đầu tiên cho biết hệ thống có move được business metric mà nó được thiết kế để cải thiện hay không — nên đo metric này trên POC sample **trước cả khi** model cost, vì một cost profile nằm trong budget nhưng không tạo improvement đo được vẫn là deployment thất bại.
- **Vì sao 4 dimension "vô hình" trong demo** — POC chạy volume thấp, input sạch, user kiên nhẫn; production chạy ở volume thật, input thật, user không tha thứ cho chậm/sai:
  | Dimension | Vì sao invisible trong demo | Khi fail trông như thế nào |
  |---|---|---|
  | Cost | POC 10-50 request/ngày ra bill không đáng kể; monthly cost projection ở production volume là phép tính hoàn toàn khác | Billing dashboard vượt budget đã sign-off lúc approve project → phải renegotiate architecture sau khi đã deploy |
  | Latency | Demo thường chạy 1 request/lần. Latency **p95** dưới concurrent load khác hẳn median latency của 1 request đơn | SLA breach, user abandonment — latency chấp nhận được cho demo có thể không chấp nhận được cho real-time user-facing workflow |
  | Reliability | POC không có retry, không fallback, không circuit breaker — dev tự refresh thử lại, không có user nào đang chờ | Không có retry/fallback → 1 transient API failure kéo sập cả workflow thay vì degrade gracefully |
  | Failure modes | Demo chỉ test trên input dev lường trước được; production đưa vào input dev không ngờ tới | Failure mode đặc thù theo architecture type: silent degradation, output bịa (made-up) trên edge-case input, hoặc fail hoàn toàn trên 1 class input chưa từng test |
- **Cost & latency modeling — biết số trước khi build**, thực hiện trước khi finalize architecture. 3 input cần: **call volume** (request/ngày hoặc /tháng), **token budget per request** (input tokens + expected output tokens), **model tier**. Từ 3 số này ước lượng được monthly cost và so với budget ceiling trước khi viết code.
  - **Token budget** là nơi cost model sai nhiều nhất: team hay tính average token trên input sẵn có rồi coi đó là distribution. Thực tế token distribution thường **skewed** — đa số request ngắn, nhưng 1 tail request dài chiếm tỷ trọng cost không tương xứng. Cost model dựa trên average có thể underestimate cost impact của tail này tới 2-3 lần.
  - **Latency** cũng theo pattern tương tự: median latency phản ánh phần giữa, nhưng SLA breach thường do nhóm request chậm ở đầu cao gây ra. Vì vậy **p95** (giá trị latency mà 95% request hoàn thành dưới mức đó, chỉ 5% chậm nhất nằm trên) là design target hữu ích hơn median.
  - **Prompt caching** là lever hiệu quả nhất cho cost + latency khi system prompt dài và ổn định (stable). Cache giữ lại prompt prefix đã processed cho các cached token, nên API không phải reprocess ở request sau. Saving tỷ lệ với cả độ dài cached prefix và tần suất reuse — VD nếu cache read được charge ở mức 10% giá input token chuẩn, 1 prefix dài được reuse qua nhiều request tạo effective saving lớn nhất. Tra rate hiện tại tại platform.claude.com/docs/en/about-claude/pricing. **Risk của caching là consistency**: nếu nội dung cached cần phản ánh live state, caching tạo ra 1 consistency window có thể vi phạm requirement của use case — lưu ý cái được cache là **prompt prefix**, không phải toàn bộ conversation.
- **3 reliability control cần build vào mọi model call** — mỗi control giải quyết 1 failure scenario khác nhau và nằm ở **layer khác nhau** trong call stack:
  - **Transient error recovery với exponential backoff**: khi model trả transient error (rate limit 429, timeout, 5xx), hệ thống retry với delay tăng dần giữa các attempt — tránh 1 flood retry biến hiccup ngắn thành outage kéo dài. Set max số attempt và total wait time theo mức delay use case chịu được được.
  - **Fallback chains**: nếu primary model/endpoint unavailable, hệ thống tự route request sang alternative (model tier khác hoặc cached response) — **không raise error cho user**. Fallback behavior phải được test trong eval suite.
  - **Circuit breakers**: đo error rate trên 1 downstream dependency, **trip** khi error vượt threshold đã định. Sau khi trip, request fail ngay lập tức thay vì chờ timeout — ngăn 1 dependency degraded kéo sập cả hệ thống rộng hơn.
  - **Layer đặt control phải đúng để có hiệu quả**: retry đặt **gần API call**, circuit breaker đặt ở **service boundary**, fallback chain đặt ở **orchestration layer**. Đặt sai layer = bảo vệ nhầm phần hệ thống, phần đúng vẫn bị exposed.
- **Failure mode theo architecture type** — Agent xử lý task không thể hoàn thành trong 1 model call: dùng tool, quan sát kết quả, chỉnh plan giữa chừng, hoàn thành multi-step process cần dynamic reasoning ở mỗi step (Claude Code là ví dụ production, navigate codebase, run test, apply fix, iterate — việc không thể làm trong single-turn architecture):
  | Architecture | Cái gãy trước | Mitigation |
  |---|---|---|
  | Agent | Unbounded tool use + context tăng không kiểm soát. Agent gọi tool không có budget constraint/turn limit sẽ đội cost + latency vô hình cho tới khi 1 request vượt budget ceiling | Set per-turn token budget, max tool call count, stopping criteria rõ ràng. Giới hạn tool set ở mức tối thiểu cần. Eval **stopping behavior** của agent, không chỉ output quality |
  | RAG | Retrieval quality drift — index không reindex khi document thêm/xoá, query và document representation lệch nhau, hoặc index refresh theo schedule tạo staleness cho live-state query | Giữ retrieval quality trong eval loop. Monitor retrieval precision/recall như system metric riêng, không chỉ output quality. Tách live-state query khỏi static knowledge query |
  | Document processing pipeline (Evaluator-optimizer) | Không có exception path cho low-confidence extraction — pipeline route mọi document qua cùng 1 flow bất kể confidence sẽ ra wrong output ở edge case cùng tỷ lệ với output đúng ở document sạch | Thêm confidence scoring vào bước extraction. Route low-confidence extraction sang human review queue thay vì downstream processing. Đưa edge-case/document khó vào eval set |
  | Orchestrator-workers | Failure boundary giữa orchestrator và subagent bị mờ, trace bị fragment, 1 subagent bị drop có thể fail silently lúc synthesis | Định nghĩa boundary recoverable (subagent: retry/flag) vs unrecoverable (orchestrator). Tạo shared trace ID cho mọi agent. Reconcile coverage ở synthesis để kết quả khớp số unit đã submit |
- **Cost · Complexity · Risk:**
  - **Cost**: đừng assume POC cost sẽ khớp production cost — model cost **trước khi** commit architecture, không phải sau billing cycle đầu tiên.
  - **Complexity**: retry, fallback chain, circuit breaker khó add vào hệ thống không thiết kế sẵn cho chúng hơn nhiều. Build reliability từ đầu, đừng scramble sửa sau incident production đầu tiên.
  - **Risk**: hệ thống không fallback, không circuit breaker chỉ có 1 single point of failure — primary model endpoint. Khi endpoint đó down lúc peak load, không có recovery path, cả user-facing workflow fail thay vì degrade gracefully.
- **Model version pinning** — note riêng: áp dụng cho **mọi** architecture trong bảng trên như nhau, đây là operational discipline, không phải architecture choice. Pin model version trong config, monitor Anthropic model deprecation page (platform.claude.com/docs/en/about-claude/model-deprecations), duy trì version-update runbook.
- **Case study "The demo cost profile that became the production bill"** (60 ngày sau khi 1 team đưa document triage system lên production) — 3 quote compound theo thứ tự thành 1 mistake:
  1. *"A POC running 10-50 requests per day can still inform a production cost estimate, but only if the numbers are scaled to expected production volume with appropriate error bounds."* → cost model sai vì build ở **volume sai**.
  2. *"We assumed the token distribution would be uniform. It wasn't. The long documents in the tail were consuming 80% of the total token spend."* → assumption token distribution sai vì build trên **input sai**.
  3. *"When the endpoint returned a 529 error at peak on day three, the whole workflow went down. We had no fallback because we'd never tested what happened when the call failed."* → reliability failure invisible trong dev vì **failure case chưa từng được test**.
  - Root cause chung: **POC bị đối xử như cost/reliability model, không chỉ là capability demonstration**. POC trả lời được "hệ thống có làm được việc này không", nhưng không trả lời được "làm ở scale này tốn bao nhiêu" hay "dependency fail thì sao" — 3 dimension (cost, input distribution, reliability) đều là production-system property phải được thiết kế **riêng**, POC không tự thiết lập dimension nào cả.
- **Checkpoint calculator** — scenario: customer service agent 50,000 request/tháng, system prompt 5,000 token ổn định, input trung bình 300 token, output trung bình 400 token, cost ceiling $800/tháng, p95 latency target ≤3s. Config ví dụ (Model = Sonnet, Prompt caching = On, max_tokens cap = 512, call-volume multiplier = 1.0x) → est. $720/tháng, p95 2.5s — đạt cả 2 target. Decision question "lever nào làm việc nhiều nhất": đáp án đúng là **B — turning prompt caching on**, vì system prompt 5,000 token stable across toàn bộ 50,000 request, cache nó cắt thẳng vào dominant input-cost driver (không phải Opus "luôn an toàn nhất", cũng không phải nâng max_tokens cap để "có headroom cho quality").

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Retry + exponential backoff (đặt gần API call) | Transient error: rate limit 429, timeout, 5xx — lỗi tự phục hồi nếu chờ | Thấp — chỉ thêm delay/latency cho request bị lỗi, không tốn thêm cost model call đáng kể (trừ khi retry tính phí lại full request) | Nếu set sai max attempt/wait time → flood retry biến hiccup ngắn thành outage kéo dài; retry không giải quyết được lỗi non-transient (bad input, auth) | Thấp — chỉ là config (max attempts, backoff multiplier), sửa/tắt dễ |
| Fallback chain (đặt ở orchestration layer) | Primary model/endpoint unavailable, cần route sang alternative (model tier khác/cached response) mà không lộ error cho user | Trung bình — cần maintain thêm 1 path xử lý + endpoint/model dự phòng, phải test riêng trong eval suite | Nếu fallback chưa được test → tưởng có failover nhưng thực tế fail âm thầm hoặc trả response kém chất lượng mà không cảnh báo | Trung bình — phải sửa lại orchestration logic, re-test fallback path |
| Circuit breaker (đặt ở service boundary) | Cần chặn 1 dependency degraded lan ra toàn hệ thống — dependency có pattern lỗi kéo dài, không phải lỗi tức thời đơn lẻ | Trung bình — cần theo dõi error rate + định nghĩa threshold trip/reset hợp lý (quá nhạy = false trip, quá chậm = không bảo vệ kịp) | Threshold sai (quá cao) → không trip kịp khi cần; threshold sai (quá thấp) → trip liên tục, tự gây outage | Trung bình — cần tune lại threshold dựa trên traffic pattern thực tế |
| Đặt reliability control sai layer (VD: circuit breaker ở API call, fallback ở service boundary) | Không nên chọn — nêu ra để đối chiếu | Không giảm cost so với đặt đúng layer nhưng không mang lại protection tương ứng | Cao — bảo vệ nhầm phần hệ thống, phần cần bảo vệ (đúng layer) vẫn exposed hoàn toàn | Cao — phải redesign lại vị trí control trong call stack, dễ bị bỏ sót khi system đã chạy production |
| Build cost/reliability model trước khi finalize architecture (đúng theo lesson) | Mặc định cho mọi production system, đặc biệt trước khi commit vào 1 model tier/architecture cụ thể | Chi phí thời gian ban đầu: ước lượng call volume, token budget (đúng distribution, không chỉ average), model tier | Nếu bỏ qua: POC cost bị present như production cost → renegotiate architecture sau billing cycle đầu, giống case study trong lesson | Cao — sau khi đã sign-off budget dựa trên POC cost sai, phải renegotiate với partner, tốn thời gian + credibility |
| Prompt caching cho system prompt dài, ổn định | System prompt lớn (VD 5,000 token) tái sử dụng qua rất nhiều request, nội dung không cần phản ánh live state | Giảm cost + latency đáng kể (cache read thường ~10% giá input token chuẩn) | Consistency window — nếu cached prefix cần phản ánh state live, cache có thể trả nội dung cũ | Thấp–trung bình — invalidate cache hoặc rút ngắn cache lifetime khi cần fresh state |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| POC-to-production gap | Khoảng cách giữa hệ thống chạy demo (volume thấp, input sạch) và hệ thống chạy production (volume thật, input thật, user không tha thứ) — invisible trên 4 dimension: cost, latency, reliability, failure modes |
| p95 latency | Giá trị latency mà 95% request hoàn thành dưới mức đó — chỉ 5% chậm nhất nằm trên; design target tốt hơn median vì SLA breach thường do nhóm request chậm gây ra |
| Token budget per request | Input token + expected output token dự tính cho 1 request, dùng làm input cho cost model — cần tính theo distribution thật (có tail dài), không chỉ average |
| Exponential backoff | Kỹ thuật retry với delay tăng dần theo cấp số (hoặc luỹ tiến) giữa các attempt khi gặp transient error, tránh flood retry gây outage |
| Fallback chain | Chuỗi route request sang alternative (model tier khác, cached response...) khi primary endpoint unavailable, không raise error ra user |
| Circuit breaker | Cơ chế đo error rate trên downstream dependency, trip khi vượt threshold để fail nhanh thay vì chờ timeout, ngăn lan lỗi sang toàn hệ thống |
| Prompt caching / cache_control | Cơ chế giữ lại prompt prefix đã processed để không phải reprocess ở request sau, giảm cost (thường ~10% giá input rate cho cache read) + latency; rủi ro consistency window nếu nội dung cần phản ánh live state |
| Model version pinning | Cố định version model đang dùng trong config (không tự động nhận update), theo dõi Anthropic model deprecation page, có runbook để cập nhật version có kiểm soát |
| Failure mode | Cách cụ thể hệ thống fail theo architecture type (VD: unbounded tool use ở Agent, retrieval drift ở RAG) — cần mitigation riêng cho mỗi loại |
| Service boundary | Điểm ranh giới giữa hệ thống và 1 dependency bên ngoài (API, service khác) — nơi đặt circuit breaker |
| Orchestration layer | Lớp điều phối logic tổng thể của hệ thống (routing, sequencing các call) — nơi đặt fallback chain |

## Gotchas / bẫy hay gặp
- [ ] Present raw demo cost (10-50 request/ngày) cho client như production cost estimate mà không scale theo volume thật + error bound — case study trong lesson bắt đầu từ chính lỗi này
- [ ] Tính token budget bằng average trên input sẵn có, giả định distribution uniform — thực tế thường skewed, tail request dài có thể chiếm 80% total token spend (như quote 2 trong case study)
- [ ] Không test failure case (endpoint trả lỗi, timeout) trong dev vì "chưa có user nào chờ" → reliability failure hoàn toàn invisible cho tới khi production gặp lỗi thật ở peak load
- [ ] Đặt reliability control sai layer — VD đặt circuit breaker gần API call thay vì service boundary, hoặc fallback chain ở tầng API call thay vì orchestration layer → bảo vệ nhầm phần hệ thống
- [ ] Xây agent không set per-turn token budget / max tool call count / stopping criteria — cost và latency đội lên vô hình cho tới khi 1 request vượt budget ceiling
- [ ] Coi model version là mặc định luôn cập nhật, không pin version trong config → risk khi Anthropic deprecate model đang dùng mà không có runbook update
- [ ] Dùng prompt caching cho nội dung cần phản ánh live state mà không tính đến consistency window — cache trả về nội dung đã cũ

## Exam tips
- Câu hỏi dạng "tại sao production cost vượt budget dù POC đã demo thành công" → nghĩ tới token distribution skewed (tail dài) và việc scale volume sai, không phải do model tier chọn sai.
- Câu hỏi "reliability control X nên đặt ở layer nào" → nhớ chính xác: retry/backoff gần **API call**, circuit breaker ở **service boundary**, fallback chain ở **orchestration layer**. Đặt sai layer là bẫy hay gặp trong câu hỏi scenario.
- Câu hỏi chọn "lever nào cắt cost nhiều nhất" khi có system prompt dài + stable + reused nhiều lần → prompt caching, không phải đổi model tier hay giảm max_tokens.
- Câu hỏi về failure mode theo architecture type → map đúng: Agent = unbounded tool use/context; RAG = retrieval quality drift; Document pipeline = thiếu exception path cho low-confidence; Orchestrator-workers = failure boundary mờ giữa orchestrator/subagent.
- Nhớ nguyên tắc: POC chỉ trả lời "có làm được không", không trả lời "cost ở scale nào" hay "dependency fail thì sao" — 2 câu này phải được model/test riêng.

## Code / config snippets
```python
"""
Minh hoạ 2 khối logic của lesson này:
1. Retry với exponential backoff (đặt gần API call) cho transient error.
2. Cost model đơn giản dùng call volume + token budget + model tier
   để check trước khi build (không gọi API thật, chỉ minh hoạ logic).
"""
import time
import random

# --- 1. Retry + exponential backoff ---
def call_with_retry(fn, max_attempts: int = 5, base_delay: float = 1.0):
    """
    fn: hàm thực hiện API call (ví dụ client.messages.create(...))
    max_attempts: số lần thử tối đa — set theo mức delay use case chịu được
    base_delay: delay cơ bản (giây) cho lần retry đầu tiên
    Chỉ nên retry với lỗi transient (429 rate limit, timeout, 5xx),
    KHÔNG retry lỗi non-transient (400 bad request, 401 auth).
    """
    for attempt in range(max_attempts):
        try:
            return fn()
        except TransientAPIError as e:  # giả định exception custom cho lỗi transient
            if attempt == max_attempts - 1:
                raise  # hết lượt retry, để lỗi propagate lên fallback chain
            # exponential backoff: delay tăng dần theo 2^attempt, cộng thêm jitter
            # để tránh nhiều client cùng retry đúng 1 thời điểm (thundering herd)
            delay = base_delay * (2 ** attempt) + random.uniform(0, 0.5)
            time.sleep(delay)


class TransientAPIError(Exception):
    """Đại diện cho rate limit 429 / timeout / 5xx — lỗi có thể tự phục hồi nếu chờ."""
    pass


# --- 2. Cost model đơn giản trước khi build (theo checkpoint calculator) ---
def estimate_monthly_cost(
    calls_per_month: int,          # call volume — input số 1 của cost model
    input_tokens_per_call: int,    # token budget input (nên lấy theo phân phối thật, không chỉ average)
    output_tokens_per_call: int,   # token budget output
    input_rate_per_mtok: float,    # giá $/1M input token theo model tier đã chọn
    output_rate_per_mtok: float,   # giá $/1M output token theo model tier đã chọn
    cached_system_prompt_tokens: int = 0,  # số token system prompt được cache (0 nếu không dùng caching)
    cache_read_discount: float = 0.1,      # cache read thường ~10% giá input chuẩn (tra rate mới nhất trên pricing page)
) -> float:
    # Token input "mới" mỗi call = input thường - phần đã được cache (chỉ tính 1 lần phí full, các lần sau discount)
    effective_input_cost_per_call = (
        (input_tokens_per_call - cached_system_prompt_tokens) * input_rate_per_mtok
        + cached_system_prompt_tokens * input_rate_per_mtok * cache_read_discount
    ) / 1_000_000
    output_cost_per_call = (output_tokens_per_call * output_rate_per_mtok) / 1_000_000
    return calls_per_month * (effective_input_cost_per_call + output_cost_per_call)


if __name__ == "__main__":
    # Scenario giống checkpoint calculator trong lesson: 50,000 request/tháng,
    # system prompt 5,000 token (cached), input 300 token, output 400 token, model Sonnet
    cost_with_caching = estimate_monthly_cost(
        calls_per_month=50_000,
        input_tokens_per_call=5_000 + 300,  # system prompt + user input
        output_tokens_per_call=400,
        input_rate_per_mtok=3.0,   # giá minh hoạ, không phải giá thật — tra pricing page
        output_rate_per_mtok=15.0,
        cached_system_prompt_tokens=5_000,
        cache_read_discount=0.1,
    )
    print(f"Est. monthly cost (caching ON): ${cost_with_caching:,.2f}")
```

## Câu hỏi chưa rõ
- ?
