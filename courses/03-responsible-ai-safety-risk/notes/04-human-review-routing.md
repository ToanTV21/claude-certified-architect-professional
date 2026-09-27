# C3.4 — Routing decision tới reviewer theo confidence / reversibility / cost

> **Course:** 3 — Responsible AI, Safety & Risk for Architects (114 min) · **Exam domain:** D5 (14%) + D1 (17%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Route decisions to the appropriate reviewer/decision maker based on confidence, reversibility, and the cost of a wrong answer, so review effort is focused on the decisions that warrant them

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Decision logging vs. routing rule — 2 việc khác nhau, không thay thế lẫn nhau:** lesson trước (decision logging) tạo ra 1 record giải thích quyết định tự động dựa trên cái gì — nhưng chỉ giải thích được **SAU khi** quyết định đã xảy ra. Log không tự quyết định quyết định nào cần người xem qua **TRƯỚC KHI** nó có hiệu lực. Routing rule mới là thứ **ngăn** quyết định sai có hiệu lực; log đã có sẵn chính là nguyên liệu thô để build view cho reviewer — việc còn lại là quyết định **cái gì cần surface và khi nào**, không phải instrument lại từ đầu.
- **3 biến quyết định STAKES của 1 decision** — coi human review như 1 **budget** hữu hạn (reviewer attention có giới hạn, phải dồn vào item stakes cao nhất):
  - **Reversibility**: quyết định sai dễ undo hay không.
  - **Cost of a wrong decision**: nếu sai mà đi qua không bị chặn thì gây thiệt hại gì. **Reversibility + cost cộng lại mới SET STAKES**: khó đảo ngược + tốn kém khi sai = high stakes, bất kể hệ thống đi tới output đó bằng cách nào.
  - **Confidence**: biến thứ 3, nằm **CHỒNG LÊN** 2 biến trên — là điểm tự tin của hệ thống về output của chính nó, chỉ có ý nghĩa khi nó **calibrated** (model vẫn có thể confidently wrong). Điểm mấu chốt: **confidence KHÔNG làm thay đổi stakes** của quyết định — nó chỉ ước lượng khả năng output này sai, từ đó quyết định **bao nhiêu volume** nên route tới người, không quyết định mức độ nghiêm trọng nếu sai.
- **Combined rule (quy tắc kết hợp)**: route tới người khi **LOW-CONFIDENCE AND (irreversible OR high-cost)**; để confident + reversible + low-cost đi qua tự động. Confident + dễ đảo ngược + low-cost thường chạy được không cần human. Low-confidence + irreversible + high-cost hầu như luôn cần human review.
- **Khi các biến "đấu nhau" (disagree)** — đây chính là phần tiêu tốn review budget nhiều nhất: cost cao nhưng dễ đảo ngược, hoặc confidence thấp trên việc nhỏ dễ sửa. Khi xung đột: **ưu tiên COST và REVERSIBILITY** (2 biến này quyết định hậu quả nếu sai); để **CONFIDENCE** quyết định bao nhiêu phần trong volume high-stakes đó có thể an toàn KHÔNG cần review. Caveat quan trọng: rule này chỉ đứng vững khi confidence signal đã **calibrated** — xác nhận calibration là 1 việc riêng, không tự nhiên có.
- **3 vị trí đặt human reviewer** — trade-off giữa safety và speed (đặt sớm hơn = an toàn hơn nhưng chậm hơn):
  1. **Pre-action approval**: action không có hiệu lực cho tới khi người approve — không có gì irreversible xảy ra mà chưa được review. Cost: thêm latency cho MỌI decision được route, cần người sẵn sàng túc trực, không scale được ở volume cao.
  2. **Post-action audit**: action chạy ngay, người review SAU. Throughput giữ cao. Cost: nếu sai, action đã có hiệu lực trước khi bị bắt — chỉ phù hợp cho decision reversible + cost thấp.
  3. **Sampled review**: chỉ review 1 fraction của decisions để monitor chất lượng chung, không làm chậm toàn bộ process. Cost: 1 bad decision có thể lọt qua nếu không nằm trong mẫu được sample — cơ chế này monitor cả hệ thống hơn là guard từng outcome riêng lẻ.
- **3 thứ reviewer BẮT BUỘC phải thấy để review chính xác**: (1) input đã dẫn tới decision, (2) output của model, (3) lý do vì sao nó bị flag route tới review. Thiếu lý do flag → không phân biệt được edge case với traffic thông thường. Thiếu input → không thể biết output đúng hay sai. Những gì đặt trước mặt reviewer quyết định review đó có "accurate" hay chỉ là hình thức.
- **Anthropic research về agent autonomy**: yêu cầu sign-off trên **MỌI** action mà agent thực hiện tạo ra friction mà **không** đi kèm safety gain tương xứng. Cách tốt hơn: để người **monitor** những gì đang xảy ra và can thiệp khi cần, thay vì approve từng bước. Pattern của Anthropic trong agent workflow: giảm per-step approval, dời review lên các checkpoint giá trị cao hơn (plan review, exception handling) để tránh **consent fatigue** — thiết kế chính xác phụ thuộc risk của từng workflow. (Tham khảo thêm anthropic.com/research/measuring-agent-autonomy và anthropic.com/research/trustworthy-agents — verify lại tại thời điểm publish vì đây là research đang phát triển.)
- **Consent fatigue**: khi hệ thống hỏi approval hàng chục lần liên tiếp, reviewer bắt đầu click-through/approve mà không đọc kỹ. Đây chính là lý do dẫn tới **plan-level review trong Claude Code** — người approve cả **plan** một lần, thay vì approve từng step riêng lẻ.
- **Diligence** — 1 trong 4 AI Fluency competency, đảm bảo AI collaboration có trách nhiệm. Áp dụng vào deployment: duy trì các **explicit human accountability checkpoint**, nhận ra khi automation pressure đang làm mòn oversight, chủ động audit workflow để tìm gap nơi AI hành động mà không có review — đặc biệt quan trọng khi automation ngày càng scale lên.
- **Checkpoint pattern cho agent workflow**: routing rule ở agent context trở thành 1 **gate** — dừng execution để chờ human review dựa trên risk/reversibility của task đó. Đặt gate TRƯỚC bất kỳ action irreversible/high-stakes nào agent định làm tự động; **sample** các action stakes thấp hơn thay vì gate từng cái. Đây cũng chính là vocabulary gate được dùng lại khi thiết kế multi-agent system.
- **Case study "routing everything to review" (Watch Out)**: setup — quyết định cái gì là "high stakes" đòi hỏi judgment; route TẤT CẢ mọi thứ vào review né được bước judgment đó, và trông có vẻ conservative/dễ defend trước compliance auditor. Thực tế trong transcript: reviewer nhận 400 item/ngày, chỉ có output + nút approve, KHÔNG thấy input, KHÔNG thấy lý do bị flag → sau 1 giờ reviewer buộc phải approve liên tục để theo kịp pace → review sụp đổ thành rubber-stamp. 1 decision high-stakes nhận đúng mức độ approval hời hợt như 1 decision trivial.
  - Root cause là **2 lỗi độc lập cùng xảy ra**, và **MỖI lỗi riêng lẻ đã đủ để làm review thất bại**:
    1. **Volume**: khi số item route vượt quá khả năng đọc của người trong thời gian họ có, "review tất cả" thực chất **review không cái nào cả** (reviewer disengage để theo kịp). Fix: dùng routing rule theo stakes (confidence, reversibility, cost) để queue chỉ chứa decision đáng được chú ý.
    2. **Missing context**: reviewer chỉ thấy output + nút approve, không có gì để đối chiếu — dù queue NGẮN cũng khó judge chính xác. Fix: surface input đã dẫn tới decision + lý do bị flag.
  - Nếu chỉ fix 1 trong 2, review vẫn có thể fail: queue nhỏ mà thiếu context, HOẶC 1 reviewer view build tốt nhưng ngập trong volume — cả 2 case đều fail.
- **Checkpoint "Build the review-routing rule"**: đáp án đúng là **B — route decision low-confidence AND (irreversible OR high-cost) vào pre-action review; để confident/reversible/low-cost đi qua tự động**. Các lựa chọn A (route theo confidence threshold bất kể stakes), C (route theo confidence alone, set thấp để giữ queue nhỏ), D (route mọi thứ) đều sai vì coi confidence hoặc volume là deciding factor thay vì stakes thật.
  - Follow-up: control quyết định thật sự là gì khi 1 case low-confidence vẫn phải route dù confidence "trong tolerance"? Model answer: **reversibility và cost of a wrong answer** mới là deciding control, KHÔNG phải confidence. Confidence chỉ filter volume được route, không đổi stakes của decision. 1 case có thể confident mà vẫn phải route tới người nếu nó đủ irreversible hoặc high-cost.
- **Cost · Complexity · Risk** (từ lesson):
  - **Cost**: pre-action review thêm latency vào mọi decision được route + cần reviewer time — 1 operating cost lặp lại.
  - **Complexity**: cần routing logic + reviewer interface hiển thị input/flag reason + 3 phương án đặt vị trí review → phức tạp hơn hẳn 1 review queue đơn giản.
  - **Risk**: route theo VOLUME thay vì STAKES dẫn tới 1 trong 2 kết quả xấu — overwhelm reviewer (quality review giảm) hoặc để lọt 1 action high-stakes/irreversible mà không có gate nào cả.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Pre-action approval | Decision irreversible và/hoặc high-cost, low-confidence — cần chặn TRƯỚC khi có hiệu lực | Latency thêm cho mọi decision được route + cần reviewer sẵn sàng liên tục | Không scale với volume cao; nếu overload → dễ rơi vào consent fatigue | Thấp về mặt kỹ thuật (chưa gì xảy ra để undo) nhưng cao về mặt vận hành nếu queue quá tải phải re-thiết kế throughput |
| Post-action audit | Decision reversible, cost thấp–trung bình, cần giữ throughput cao | Vận hành rẻ hơn pre-action (không block action) nhưng vẫn cần reviewer time định kỳ | Action sai đã có hiệu lực trước khi bị bắt — chỉ an toàn nếu reversibility thật sự cao | Trung bình — phải rollback/undo action đã chạy, tốn công tuỳ mức độ đã lan toả |
| Sampled review | Muốn monitor chất lượng hệ thống ở scale lớn mà không review từng item | Thấp nhất trong 3 phương án — chỉ review 1 fraction | Bad decision ngoài mẫu sample có thể lọt hoàn toàn không ai biết | Thấp cho từng item lọt lưới, nhưng cao nếu phải audit lại toàn bộ population sau khi phát hiện lỗi hệ thống |
| Route theo stakes (confidence + reversibility + cost) | Default nên dùng — mọi hệ thống có human review đều cần định nghĩa stakes trước khi route | Chi phí thiết kế ban đầu: xây rule kết hợp + đảm bảo confidence calibrated | Nếu rule sai/confidence chưa calibrated → false sense of safety | Trung bình — sửa lại threshold/rule dễ hơn sửa lại cả pipeline routing |
| Route theo volume (route everything / route theo confidence alone để giữ queue nhỏ) | KHÔNG nên chọn — chỉ "cảm thấy" an toàn vì né được việc phải judge stakes | Vận hành có vẻ rẻ (không cần thiết kế rule) nhưng thực chất cực tốn vì reviewer time bị lãng phí trên item trivial | Cao — review sụp đổ thành rubber-stamp (case study 400 item/ngày), high-stakes decision lọt qua với mức attention như trivial decision | Cao — phải redesign lại toàn bộ routing + rebuild trust của reviewer team |
| Per-step approval (agent workflow) | Agent risk rất cao, mọi step đều gần như irreversible | Cực cao — mỗi step đều thêm latency + review effort | Consent fatigue rất cao ở workflow nhiều step → reviewer click-through không đọc | Trung bình — có thể refactor về checkpoint pattern, nhưng cần redesign cả review interface |
| Plan-level checkpoint (agent workflow, pattern của Claude Code) | Agent workflow nhiều step nhưng risk tổng thể do đúng bởi cái plan, không phải từng action nhỏ | Thấp hơn per-step — chỉ review 1 lần ở plan, không lặp lại mỗi step | Nếu agent lệch khỏi plan đã approve giữa lúc thực thi thì không bị bắt kịp thời — cần cơ chế exception handling riêng | Thấp — dễ áp dụng lại checkpoint mới nếu risk profile thay đổi (thêm exception-handling checkpoint) |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Decision logging | Ghi lại record giải thích 1 quyết định tự động dựa trên cái gì — chỉ giải thích được SAU khi decision đã xảy ra |
| Routing rule | Rule quyết định decision nào cần route tới người TRƯỚC khi có hiệu lực, dựa trên stakes |
| Reversibility | 1 trong 2 biến set stakes — quyết định sai dễ undo hay không |
| Cost of a wrong decision | 1 trong 2 biến set stakes — thiệt hại nếu decision sai đi qua không bị chặn |
| Confidence | Điểm tự tin của hệ thống về output của chính nó — không đổi stakes, chỉ lọc volume route tới người; chỉ hữu ích khi calibrated |
| Confidence calibration | Việc xác nhận điểm confidence của model phản ánh đúng khả năng sai thực tế, không phải chỉ là số "tự tin" vô nghĩa |
| Combined rule | Route khi LOW-CONFIDENCE AND (irreversible OR high-cost); để phần còn lại đi qua tự động |
| Pre-action approval | Vị trí reviewer đặt TRƯỚC khi action có hiệu lực — an toàn nhất, chậm nhất, không scale |
| Post-action audit | Vị trí reviewer đặt SAU khi action đã chạy — throughput cao, chỉ hợp với decision reversible/cost thấp |
| Sampled review | Chỉ review 1 fraction decision để monitor chất lượng hệ thống, không guard từng outcome |
| Consent fatigue | Hiện tượng reviewer bị hỏi approval quá nhiều lần liên tiếp, dẫn tới click-through/approve mà không đọc |
| Plan-level review | Pattern trong Claude Code — người approve cả plan 1 lần thay vì approve từng step của agent |
| Diligence | 1 trong 4 AI Fluency competency — duy trì human accountability checkpoint, phát hiện khi automation pressure làm mòn oversight |
| Checkpoint pattern | Gate dừng execution của agent để chờ human review, đặt trước action irreversible/high-stakes, sample các action thấp stakes hơn |
| Review budget | Cách hình dung reviewer attention là tài nguyên hữu hạn, phải ưu tiên dồn vào decision stakes cao nhất |

## Gotchas / bẫy hay gặp
- [ ] Nhầm confidence là biến quyết định STAKES — thực ra confidence chỉ quyết định VOLUME route, còn stakes do reversibility + cost quyết định
- [ ] Dùng confidence signal chưa calibrated để route — model có thể "confidently wrong", route sai cả 2 chiều (bỏ lọt case nguy hiểm hoặc route dư case an toàn)
- [ ] Khi 2 biến đấu nhau (VD: cost cao nhưng dễ đảo ngược), quên rule ưu tiên: cost + reversibility quyết định mức độ nghiêm trọng, confidence chỉ quyết định bao nhiêu volume trong đó cần review
- [ ] Route TẤT CẢ decision vào review (conservative default giả) — tưởng an toàn nhưng volume quá tải khiến review collapse thành rubber-stamp, không bảo vệ được gì
- [ ] Cho reviewer thấy output + nút approve mà KHÔNG có input và lý do bị flag — dù queue ngắn cũng không judge được chính xác
- [ ] Yêu cầu sign-off trên MỌI step của agent workflow → consent fatigue, reviewer approve mà không đọc — nên dời review lên checkpoint giá trị cao hơn (plan review)
- [ ] Chỉ fix 1 trong 2 lỗi của case study "routing everything" (chỉ giảm volume HOẶC chỉ thêm context) mà nghĩ là đủ — cả 2 lỗi đều đủ để làm review fail độc lập với nhau

## Exam tips
- Câu scenario "decision X có confidence Y%, reversible/irreversible, cost cao/thấp — route vào đâu?" → luôn áp combined rule: low-confidence AND (irreversible OR high-cost) → pre-action review; ngược lại cho qua tự động. Đừng bị đánh lừa bởi confidence cao — nếu irreversible + high-cost vẫn có thể cần route.
- Câu hỏi "biến nào là deciding control thật sự khi routing decision" → đáp án luôn là **reversibility + cost of a wrong answer**, KHÔNG phải confidence (confidence chỉ lọc volume).
- Câu hỏi nhận diện consent fatigue trong đề: mô tả agent/hệ thống hỏi approval liên tục ở mọi step, reviewer bắt đầu approve nhanh không đọc kỹ → đây là consent fatigue, giải pháp đúng là chuyển sang checkpoint pattern (VD: plan-level review) chứ không phải thêm nhiều bước approval hơn.
- Câu hỏi "route everything to review là best practice?" → SAI, vì đây chính là anti-pattern trong Watch Out: route theo volume (không phải stakes) khiến review mất ý nghĩa — luôn có 2 lỗi độc lập cần tránh: quá tải volume và thiếu context cho reviewer.

## Code / config snippets
```python
# Minh hoạ rule kết hợp (combined rule) để route 1 decision tới đúng chỗ
# dựa trên confidence, reversibility, cost of a wrong decision.
# Lưu ý: confidence KHÔNG quyết định stakes — nó chỉ lọc volume;
# reversibility + cost mới là deciding control thật sự.

def route_decision(confidence: float, reversible: bool, cost_high: bool) -> str:
    """
    confidence: điểm tự tin của model (0.0 - 1.0), PHẢI đã được calibrated
    reversible: True nếu decision sai có thể undo dễ dàng
    cost_high: True nếu decision sai gây thiệt hại lớn nếu không bị chặn

    Trả về 1 trong 3 hành động:
    - "pre_action_review": chặn action lại, chờ người approve trước khi chạy
    - "post_action_audit": cho action chạy ngay, review lại sau (sampled/async)
    - "auto_approve": để đi qua tự động, không cần người xem
    """
    # Stakes được set bởi 2 biến này, KHÔNG phải confidence
    is_irreversible = not reversible
    high_stakes = is_irreversible or cost_high

    # Ngưỡng "low confidence" — trong thực tế nên tune theo calibration data,
    # đây chỉ là ví dụ minh hoạ đơn giản
    LOW_CONFIDENCE_THRESHOLD = 0.8
    low_confidence = confidence < LOW_CONFIDENCE_THRESHOLD

    # Combined rule: route khi low-confidence AND high-stakes (irreversible OR high-cost)
    if low_confidence and high_stakes:
        return "pre_action_review"

    # Confident nhưng vẫn high-stakes -> vẫn đáng theo dõi, nhưng không cần chặn trước
    # (post-action audit phù hợp khi reversible dù cost có thể cao)
    if high_stakes and reversible:
        return "post_action_audit"

    # Confident + reversible + low-cost -> để qua tự động
    return "auto_approve"


# Ví dụ dùng thử:
print(route_decision(confidence=0.6, reversible=False, cost_high=True))   # pre_action_review
print(route_decision(confidence=0.95, reversible=True, cost_high=True))  # post_action_audit
print(route_decision(confidence=0.97, reversible=True, cost_high=False)) # auto_approve
```

## Câu hỏi chưa rõ
- ?
