# C2.5 — A/B test & structured experiment trên hệ thống live

> **Course:** 2 — Enterprise Integration & Production (158 min) · **Exam domain:** D4 (16%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Plan and interpret an A/B test or structured experiment on a live Claude system, setting the hypothesis, selecting metrics, estimating the required sample size, and reading a result without overclaiming

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Bối cảnh:** integration pattern (module trước) đưa Claude vào enterprise stack, nhưng chưa trả lời được hệ thống có đang chạy đúng không (câu hỏi của **observability**) và thay đổi có thực sự cải thiện hệ thống không (câu hỏi của **structured A/B testing**). Thiếu 1 trong 2 → hoặc "fly blind", hoặc thay đổi mà không đo được.
- **A/B test cho Claude system** theo cấu trúc kinh điển (hypothesis, treatment, control, metric, sample size) nhưng khác software A/B test truyền thống: LLM output là **probabilistic** → result noisier, interaction effect giữa treatment và input type khó control hơn.
  - Hypothesis phải **specific + falsifiable**: "prompt mới tốt hơn" là hypothesis vô nghĩa (không named treatment, không metric, không threshold). Hypothesis dùng được: "Đổi instruction summarize → instruction extract 3 action items quan trọng nhất sẽ tăng task success rate ít nhất 5% mà không làm giảm latency p95" — có treatment, metric, threshold, và constraint trên secondary metric.
- **4 thành phần bắt buộc của 1 A/B test hợp lệ** (thiếu bất kỳ cái nào là thiếu 1 chân của experiment):
  1. **Hypothesis** — specific, falsifiable, named treatment + expected direction của primary metric + constraint trên secondary metric. Thiếu: kết quả nào cũng có thể diễn giải thành "win" vì luôn tìm được 1 metric di chuyển đúng hướng nếu nhìn đủ nhiều metric sau khi đã có kết quả.
  2. **Treatment/control assignment** — random, và phải **consistent cho cùng 1 user/session** (tránh cùng 1 user vừa vào treatment vừa vào control gây contamination). Thiếu random: nhóm không comparable — VD treatment nhóm ngẫu nhiên nhận nhiều query phức tạp hơn → "win" quan sát được chỉ là artifact của input distribution, không phải effect thật.
  3. **Primary metric** — CHỈ 1 metric, chọn **trước khi** experiment chạy (task success rate, cost/completion, latency p95, satisfaction proxy). Chọn metric sau khi thấy kết quả = **outcome-shopping** — biến experiment thành retrospective correlation, cơ sở ra quyết định yếu hơn nhiều.
  4. **Sample size** — tính từ **minimum detectable effect (MDE)**, baseline metric value, confidence level yêu cầu. Variance của LLM output cao hơn hệ thống deterministic → sample size cần lớn hơn. Thiếu: experiment underpowered không phân biệt được effect thật với noise — team cứ chạy tới khi thấy điều mình muốn thấy sẽ luôn "thấy", thật hay không thật.
- **Đọc kết quả không overclaim:** statistical significance chỉ nghĩa là "kết quả khó xảy ra do random chance với sample size này" — KHÔNG đồng nghĩa với "đủ lớn để đáng làm". Một thay đổi có thể significant nhưng quá nhỏ để bù chi phí vận hành/maintain version mới. 2 câu hỏi phải trả lời trước khi tuyên bố winner: (1) effect đủ lớn để đáng chi phí operational overhead của việc maintain version mới không? (2) có secondary metric nào degrade không (VD task success rate tăng nhưng cost +30% có thể không phải net win, tuỳ budget constraint)?
- **Interaction effect — failure mode đặc thù của LLM experiment** mà classical A/B test ít gặp: prompt change cải thiện performance trên input điển hình trong test period, nhưng có thể làm tệ hơn trên edge-case input hiếm gặp lúc test nhưng phổ biến ở 1 seasonal spike tương lai. Sự khớp giữa test-period input distribution và input distribution thực tế/tương lai quan trọng hơn trong LLM experiment so với hầu hết context software khác.
- **Shadow testing — validate thay đổi trước khi user nào thấy nó:** Live A/B test gửi user thật vào version mới → 1 regression sẽ chạm tới 1 phần user trước khi experiment đóng. Shadow testing: chạy version mới **song song** với version hiện tại, gửi nó **1 copy của live request**, nhưng luôn trả user response của version HIỆN TẠI. Output của version mới được **log (không return)**, chấm **offline** sau đó. Quyết định deploy được đưa ra trước khi user nào từng thấy version mới.
  - **Live A/B test** phù hợp khi: deployment chịu được 1 exposure nhỏ, bounded tới version tệ hơn, và traffic volume đủ cao để đạt sample size ý nghĩa trong khoảng thời gian hợp lý. Payoff: đo được version mới so với real user behavior kể cả downstream signal (user có accept câu trả lời, có follow-up không).
  - **Shadow testing** phù hợp khi: 1 output tệ mang risk quá lớn, hoặc traffic quá thấp để support live split trước deadline của thay đổi. Cost: mất downstream signal — scoring phải dựa vào offline rubric/golden answer thay vì real user behavior. Với regulated industry, nơi expose user tới 1 model change chưa validate có thể **không được phép**, shadow testing thường là cách DUY NHẤT chấp nhận được để validate thay đổi.
- **Observability at scale — 4 câu hỏi, mỗi câu cần 1 instrumentation layer riêng** (system đang làm gì? đang chạy tốt tới đâu? thay đổi khi nào? tại sao thay đổi?):
  1. **Request-level tracing** — mỗi request tạo 1 trace: model, model version, input/output token count, latency, stop reason, tool call. Đây là raw material cho mọi thứ sau.
  2. **Metric aggregation** — aggregate trace-level data thành dashboard metric: cost/request, latency p50/p95, task success rate (nếu có downstream acceptance signal), error rate theo type. **Per-request decomposition** quan trọng: aggregate metric có thể trông healthy trong khi 1 fraction nhỏ request tiêu tốn phần lớn budget.
  3. **Anomaly detection** — threshold alert trên metric quan trọng (VD cost spike >150% so với 7-day average nên alert; latency p95 vượt SLA threshold nên alert). **Model drift** (thay đổi dần trong output distribution theo thời gian) khó phát hiện bằng threshold alert đơn giản, cần **periodic distribution comparison**.
  4. **Change attribution** — khi 1 metric di chuyển, instrumentation phải phân biệt được 3 nguyên nhân, vì mỗi nguyên nhân có fix khác nhau (nhầm lẫn 3 cái này ra fix sai):
     - **Model drift**: hành vi của model trên input ổn định thay đổi (model behavior tự thay đổi dù input như cũ).
     - **Data drift**: input distribution thay đổi (input khác đi, model vẫn vậy).
     - **Model update effect**: model version bị đổi (kể cả tự động qua provider), version mới hành xử khác trên cùng input cũ.
- **Failure taxonomy — phân loại KIND của failure** (instrumentation chỉ báo metric di chuyển, diagnosis mới nói được nó là loại failure gì, mỗi loại fix khác nhau):
  - **Prompt failure** — instruction ambiguous/underspecified, model tự lấp khoảng trống. Fix: sửa prompt, không phải sửa model.
  - **Hallucination** — model tạo ra content tự tin, trôi chảy nhưng không grounded trong input hay 1 nguồn đáng tin. Fix: grounding qua retrieval, tool use, hoặc verification — instruction mạnh hơn KHÔNG giải quyết được.
  - **Model mismatch** — chọn model tier sai cho task, hoặc bị swap mà không re-evaluate. Fix: model selection, gated bằng 1 eval.
  - **Orchestrator-workers failure** — trong multi-agent system, phải trace xuyên orchestrator + subagent: 1 subagent failure recoverable (retry/flag) trông khác 1 orchestrator failure unrecoverable. Muốn attribute đúng cần trace bao trùm cả 2 tầng.
- **Discernment** — 1 trong 4 AI Fluency competency: kỷ luật đánh giá chất lượng thật của output model tạo ra, thay vì chấp nhận nó "as is". Áp dụng cho production system: thói quen classify mỗi output là acceptable / needs revision / needs override, rồi feed judgment đó ngược lại vào eval và monitoring. Team thiếu Discernment sẽ nhìn metric di chuyển mà không bao giờ tự hỏi output bên dưới có thực sự tốt hay không.
- **Translation layer — nối technical metric với business KPI:** người tài trợ deployment đọc KPI dashboard đo outcome mà deployment được thiết kế để cải thiện, không đọc request-level trace. Observability stack cần 1 translation layer map technical metric → business metric. VD customer service agent: business metric = average handle time / first-contact resolution rate / CSAT; observability stack đo latency, task success rate, error rate; translation layer map task success rate → first-contact resolution, latency → handle time. Layer này phải build **lúc design hệ thống**, không phải sau business review đầu tiên — nếu để sau, trả lời "cái gì đang drive thay đổi handle time" đòi hỏi retrospective reconstruction thay vì 1 live query.
- **Case study "50-session winner" (screen 15):** team test customer service agent, so 50 session new vs 50 session old, task success rate 68% (new) vs 62% (old) → tuyên bố winner, deploy. 2 tuần sau, task success rate của new version rơi về 61% — cái gain 6 điểm biến mất. 3 lỗi, mỗi lỗi đủ để invalidate kết quả:
  1. **Sample size quá nhỏ** — 1 khác biệt 6 điểm trên metric high-variance cần sample size ở mức HÀNG TRĂM để statistically significant; ở 50/nhóm, khác biệt quan sát được nằm trong noise floor.
  2. **Input distribution không control** — 50 session treatment tình cờ chứa ít edge-case input hơn 50 session control → "improvement" 1 phần là artifact của input nào rơi vào nhóm nào.
  3. **Primary metric không pre-specify** — team so task success rate vì nó di chuyển đúng hướng; nếu nó di chuyển sai hướng, họ đã nhìn metric khác. Chọn metric sau khi thấy kết quả biến 1 test thành đi tìm bất kỳ metric nào tình cờ di chuyển. → Kết luận chung: underpowered experiment + metric selection sau khi có kết quả tạo ra **confirmation, không phải evidence** — kết quả chỉ phản ánh lại đúng hypothesis ban đầu, không phải bằng chứng độc lập.
- **Checkpoint "experiment-design plane" (screen 16):** 2 trục — **expected effect size** (small ↔ large) và **confidence requirement** (low/moderate/high). Vị trí trên plane quyết định experimental posture đúng, từ đó quyết định minimum sample size. 5 scenario minh hoạ:
  - A. Sửa nhẹ 1 clarification message trong FAQ chatbot low-stakes → Small effect, Low/Moderate confidence (low stakes, chấp nhận iterate nhanh).
  - B. Đổi prompt architecture cho 1 medical intake summarizer, lỗi có thể delay treatment → Large-effect-risk, High confidence required (high stakes).
  - C. Thêm 1 classification category mới cho routing model, dự kiến chiếm 30% traffic → Large effect, High confidence (volume share lớn).
  - D. Test đổi Sonnet → Haiku cho task formatting đơn giản, xem có save cost mà không giảm quality → Small/moderate effect, Moderate confidence.
  - E. Sửa nhẹ retrieval prompt trong RAG system chỉ 200 request/ngày → Small effect, traffic thấp → khó đạt high confidence nhanh, có thể cần shadow testing hoặc window dài hơn.
  - Nguyên tắc chung: large expected effect + high confidence requirement = cần experimental design rigorous nhất + sample lớn nhất; small effect + low stakes = test nhẹ hơn, thậm chí shadow test là đủ.
- **Cost · Complexity · Risk:**
  - **Cost:** chạy A/B test không pre-specify primary metric nghĩa là luôn có thể tìm được kết quả mình muốn thấy. Underpowered experiment tạo false positive. Thay đổi trông như improvement được deploy, team cuối cùng maintain 1 version không tốt hơn version cũ mà vẫn gánh full operational overhead.
  - **Complexity:** thêm observability instrumentation SAU incident đầu tiên nghĩa là câu hỏi root-cause không trả lời được từ log data hiện có. Complexity của việc build instrumentation đúng ngay từ đầu thấp hơn việc reconstruct log retroactively.
  - **Risk:** hệ thống LLM chỉ có aggregate-only observability metric có thể trông healthy trong khi 1 fraction nhỏ request tiêu tốn phần lớn budget và trả wrong output. Aggregate metric bảo vệ khỏi failure rõ ràng; per-request decomposition bảo vệ khỏi failure không rõ ràng.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Live A/B test | Deployment chịu được exposure nhỏ, bounded tới version tệ hơn; traffic đủ cao để đạt sample size ý nghĩa trong window hợp lý | Vận hành 2 version song song trong thời gian test; cần đủ traffic/thời gian để đạt significance | User thật bị exposed tới regression trước khi experiment đóng | Trung bình — route lại 100% traffic về control, nhưng user đã bị ảnh hưởng trong lúc test không undo được |
| Shadow testing | 1 output tệ mang risk quá lớn để expose user; traffic quá thấp cho live split; regulated industry cấm expose model chưa validate | Chạy version mới song song + infra log/score offline, nhưng không cần route traffic thật | Mất downstream signal (không có real user acceptance), scoring dựa vào offline rubric/golden answer nên có thể lệch so với real-world | Thấp — không ai từng thấy version mới, dừng bất cứ lúc nào không ảnh hưởng user |
| Pre-specify primary metric trước khi test | Luôn luôn — đây là 1 trong 4 thành phần bắt buộc của A/B test hợp lệ | Chi phí thời gian để xác định threshold + metric trước khi chạy | Không làm: outcome-shopping — chọn metric sau khi thấy kết quả, biến test thành retrospective correlation yếu | Cao — nếu đã chạy xong mới nhận ra chưa pre-specify, phải chạy lại experiment từ đầu để có evidence hợp lệ |
| Chạy đủ sample size theo MDE calculation | Luôn luôn trước khi bắt đầu test, đặc biệt hiệu ứng nhỏ / metric high-variance | Thời gian chờ đủ traffic/sample (có thể là ngày–tuần) | Bỏ qua: underpowered experiment, false positive như case study 50-session — deploy 1 version không tốt hơn mà vẫn gánh operational overhead | Cao — kết quả sai đã dẫn tới quyết định deploy, phải rollback + chạy lại test đúng sample size |
| Đầu tư observability instrumentation ngay từ khi design | Luôn luôn — nên làm trước production, không phải sau incident đầu tiên | Chi phí engineering ban đầu để build 4 layer (tracing, aggregation, anomaly detection, change attribution) | Không làm: khi có incident, root-cause question không trả lời được từ log hiện có → phải retrospective reconstruction | Rất cao — không thể tái tạo lại data lịch sử đã mất, chỉ có thể bắt đầu instrument từ thời điểm hiện tại |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Hypothesis (falsifiable) | Phát biểu cụ thể, có thể bị bác bỏ, named treatment + expected direction của primary metric + constraint trên secondary metric |
| Treatment / control assignment | Random assignment vào nhóm test/nhóm đối chứng; phải consistent cho cùng 1 user/session để tránh contamination |
| Primary metric | Metric DUY NHẤT được chọn trước khi experiment chạy, dùng để quyết định winner |
| Outcome-shopping | Chọn metric để báo cáo SAU khi đã thấy kết quả — biến test thành retrospective correlation, không phải evidence |
| Minimum detectable effect (MDE) | Effect size nhỏ nhất muốn phát hiện được; dùng cùng baseline value + confidence level để tính sample size cần |
| Statistical significance | Kết quả khó xảy ra do random chance với sample size đã có — KHÔNG đồng nghĩa với "đủ lớn để đáng deploy" |
| Interaction effect | Hiệu ứng khác nhau của treatment trên các loại input khác nhau — LLM experiment dễ gặp vì input distribution lúc test khác lúc production |
| Shadow testing | Chạy version mới song song, gửi copy live request, log output nhưng KHÔNG return cho user, chấm offline trước khi quyết định deploy |
| Request-level tracing | Log từng request: model, model version, token count, latency, stop reason, tool call — nguyên liệu cho mọi metric khác |
| Metric aggregation | Tổng hợp trace-level data thành dashboard metric (cost/request, latency p50/p95, error rate...) |
| p95 (latency) | Giá trị latency mà 95% request nhanh hơn hoặc bằng — dùng để bắt outlier mà average che khuất |
| Anomaly detection | Threshold alert trên metric quan trọng (cost spike, latency vượt SLA); model drift cần periodic distribution comparison thay vì threshold đơn giản |
| Model drift | Hành vi của model trên input ổn định tự thay đổi theo thời gian (input như cũ, output khác đi) |
| Data drift | Input distribution thay đổi (input khác đi, model behavior không đổi) |
| Model update effect | Model version bị đổi (kể cả tự động từ provider), version mới hành xử khác trên cùng input cũ |
| Change attribution | Khả năng phân biệt model drift / data drift / model update effect khi 1 metric di chuyển, để chọn đúng fix |
| Failure taxonomy | Phân loại KIND of failure: prompt failure, hallucination, model mismatch, orchestrator-workers failure — mỗi loại fix khác nhau |
| Prompt failure | Instruction ambiguous/underspecified, model tự lấp khoảng trống — fix bằng sửa prompt |
| Hallucination | Model tạo content tự tin, trôi chảy nhưng không grounded — fix bằng retrieval/tool use/verification, KHÔNG fix bằng instruction mạnh hơn |
| Model mismatch | Chọn sai model tier cho task, hoặc swap model mà không re-evaluate — fix bằng model selection gated by eval |
| Orchestrator-workers failure | Trong multi-agent system, subagent failure recoverable khác orchestrator failure unrecoverable — cần trace xuyên cả 2 tầng |
| Discernment | 1 trong 4 AI Fluency competency: kỷ luật đánh giá chất lượng thật của output, không chấp nhận as-is; feed judgment ngược vào eval/monitoring |
| Translation layer | Tầng map technical metric (latency, task success rate) sang business KPI (handle time, CSAT, first-contact resolution) |
| Per-request decomposition | Nhìn từng request riêng lẻ thay vì chỉ nhìn aggregate metric — bắt được fraction nhỏ request "ăn" hết budget/gây lỗi mà aggregate che khuất |

## Gotchas / bẫy hay gặp
- [ ] So sánh 50 session mới vs 50 session cũ và tuyên bố "winner" — sample size quá nhỏ cho metric high-variance, kết quả nằm trong noise floor (case study "50-session winner")
- [ ] Không control input distribution giữa 2 nhóm — 1 nhóm tình cờ nhận ít edge-case hơn khiến "improvement" chỉ là artifact của việc input nào rơi vào nhóm nào
- [ ] Chọn primary metric SAU khi thấy kết quả (outcome-shopping) — nếu metric ban đầu di chuyển sai hướng thì đã tìm metric khác để "declare win"
- [ ] Dừng test ngay khi thấy statistical significance mà không hỏi "effect có đủ lớn để đáng maintain version mới không" và "secondary metric nào degrade không"
- [ ] Bỏ qua interaction effect: prompt change tốt trên input điển hình lúc test nhưng tệ hơn trên edge-case sẽ phổ biến ở tương lai (seasonal spike) — test-period input distribution không đại diện
- [ ] Chỉ dùng threshold alert để bắt model drift — model drift là thay đổi DẦN theo thời gian, threshold alert đơn giản khó bắt được, cần periodic distribution comparison
- [ ] Nhầm lẫn model drift / data drift / model update effect khi 1 metric di chuyển — 3 nguyên nhân có 3 fix khác nhau, chọn sai fix không giải quyết được gì
- [ ] Thêm observability instrumentation SAU incident đầu tiên — lúc đó không còn log data để trả lời root-cause question, phải retrospective reconstruction (tốn kém hơn build đúng từ đầu)
- [ ] Chỉ nhìn aggregate metric (cost/request trung bình, latency trung bình) mà bỏ qua per-request decomposition — 1 fraction nhỏ request có thể tiêu tốn phần lớn budget và trả wrong output trong khi dashboard vẫn "xanh"

## Exam tips
- Câu scenario dạng "đặt tình huống X vào đâu trên experiment-design plane" → xác định 2 trục: expected effect size (small/large) và confidence requirement (low/moderate/high); traffic volume thấp + cần confidence cao → gợi ý shadow testing hoặc window dài hơn thay vì live A/B vội vàng.
- Câu hỏi "metric di chuyển, nguyên nhân là gì" → luôn phân biệt rõ 3 loại: model drift (model tự thay đổi trên input ổn định) vs data drift (input thay đổi) vs model update effect (version bị đổi) — và failure taxonomy riêng: prompt failure vs hallucination vs model mismatch vs orchestrator-workers failure. Đề thường test khả năng chọn đúng category để chọn đúng fix.
- Khi thấy đáp án dạng "kết quả statistically significant nên deploy ngay" → cảnh giác, đây thường là distractor; đáp án đúng cần thêm câu hỏi "effect đủ lớn để đáng operational overhead không" + "secondary metric có degrade không".
- Case study 50-session winner hay bị hỏi dạng "lỗi nào trong 3 lỗi là nghiêm trọng nhất" — nhớ rằng đề nhấn mạnh CẢ 3 lỗi (sample size, input distribution, metric chọn sau) đều ĐỦ để invalidate kết quả độc lập với nhau, không phải chỉ 1 lỗi là nguyên nhân chính.
- Regulated industry (y tế, tài chính...) mà câu hỏi nhắc tới compliance/risk cao → shadow testing thường là đáp án đúng thay vì live A/B test, vì có thể live A/B không được phép về mặt quy định.

## Code / config snippets
```python
# Ví dụ minh hoạ 2 khối cần cho structured A/B test / observability:
# (1) hàm ước lượng sample size tối thiểu từ minimum detectable effect (MDE)
# (2) cấu trúc log 1 request cho observability (request/response/context/outcome)

import math


def required_sample_size(baseline_rate: float, mde: float, confidence: float = 0.95) -> int:
    """
    Ước lượng sample size TỐI THIỂU cho mỗi nhóm (treatment/control)
    trong 1 A/B test so sánh tỷ lệ (VD: task success rate).

    baseline_rate: tỷ lệ hiện tại của primary metric (VD 0.62 = 62%)
    mde: minimum detectable effect muốn phát hiện, tuyệt đối (VD 0.05 = 5 điểm %)
    confidence: confidence level yêu cầu (default 95%)

    Đây là công thức xấp xỉ (two-proportion z-test, power ~80%) — dùng để
    minh hoạ khái niệm "sample size phải tính từ MDE + baseline + confidence",
    KHÔNG dùng số 50/nhóm tuỳ tiện như case study "50-session winner".
    """
    # z-score tương ứng confidence level (two-sided), z=1.96 cho 95%
    z_alpha = 1.96 if confidence == 0.95 else 2.576  # 99% dùng z=2.576
    z_beta = 0.84  # tương ứng power 80% (chuẩn phổ biến khi thiết kế experiment)

    p1 = baseline_rate
    p2 = baseline_rate + mde
    p_bar = (p1 + p2) / 2

    # Công thức two-proportion z-test cho sample size mỗi nhóm
    numerator = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar)) + z_beta * math.sqrt(
        p1 * (1 - p1) + p2 * (1 - p2)
    )) ** 2
    denominator = mde ** 2

    return math.ceil(numerator / denominator)


# VD: baseline task success rate 62%, muốn phát hiện effect 6 điểm % (case study 50-session)
# → sample size cần thiết PER GROUP, so với 50 session thực tế đã dùng
n_needed = required_sample_size(baseline_rate=0.62, mde=0.06)
print(f"Sample size cần mỗi nhóm: {n_needed}")  # ra số hàng trăm, không phải 50


# Cấu trúc 1 record log cho request-level tracing (layer 1 của observability)
# — nền tảng để build metric aggregation, anomaly detection, change attribution
request_log_entry = {
    "request": {
        "model": "claude-sonnet-4-6",          # model + version dùng cho request này
        "input_token_count": 512,               # để tính cost và trace prompt size
        "prompt_version": "v3-extract-actions",  # để làm change attribution (model update vs prompt change)
    },
    "response": {
        "output_token_count": 128,
        "latency_ms": 840,                       # raw material cho latency p50/p95
        "stop_reason": "end_turn",
        "tool_calls": [],                        # log tool call nếu có, để trace orchestrator-workers failure
    },
    "context": {
        "experiment_group": "treatment",          # treatment/control — PHẢI consistent cho cùng session_id
        "session_id": "sess_abc123",
    },
    "outcome": {
        # downstream acceptance signal — nền cho Discernment: acceptable / needs_revision / needs_override
        "task_success": None,   # điền sau khi có eval/human judgment, KHÔNG suy đoán tại thời điểm log
        "user_follow_up": False,
    },
}
```

## Câu hỏi chưa rõ
- ?
