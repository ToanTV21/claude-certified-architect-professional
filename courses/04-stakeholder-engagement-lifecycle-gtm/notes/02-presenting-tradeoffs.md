# C4.2 — Trình bày trade-off theo cost / risk / reversal

> **Course:** 4 — Stakeholder Engagement, Lifecycle & GTM (178 min) · **Exam domain:** D6 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Present an architectural trade-off in terms a business stakeholder can act on by pairing each choice with a cost, a risk, and what a reversal would take, so executive and procurement reviews reach a decision instead of stalling

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Vai trò của Architect ở bước này:** Discovery (lesson trước) cho biết buyer cần gì; bước tiếp theo là biến requirement đó thành 1 quyết định mà stakeholder có thể ra. Nhưng job của Architect **KHÔNG** phải là tự resolve cái tradeoff trước khi vào meeting — job là **làm cho việc ra quyết định trở nên khả thi (make decisions POSSIBLE)**: mô tả các option rõ ràng đủ để stakeholder tự đưa ra informed choice. Mọi design decision có ý nghĩa đều đi kèm 1 tradeoff (giảm cost/complexity thì tăng latency/risk/compliance burden, hoặc ngược lại). Nếu chỉ trình bày phần kết luận (conclusion), quyết định trông có vẻ rõ ràng nhưng thực chất yếu — khi downside xuất hiện sau đó, stakeholder cảm thấy mình đã approve một recommendation mà không hiểu hết cái gì đi kèm với nó.
- **DECISION FRAME — 4 câu hỏi** dùng để trình bày bất kỳ tradeoff nào:
  1. Chúng ta được gì (gain)?
  2. Chúng ta phải đánh đổi gì (give up)?
  3. Nếu chọn phương án này bây giờ nhưng sau phải đảo ngược (reverse) thì chuyện gì xảy ra?
  4. Trong môi trường regulated, lựa chọn này ảnh hưởng gì tới compliance posture?
  - **Câu hỏi 3 (reversal cost) là câu hay bị SKIP nhất**, và cũng thường là câu **làm thay đổi cục diện cả buổi meeting** — nó chuyển câu chuyện từ "đâu là câu trả lời kỹ thuật tốt hơn?" sang "đâu là lựa chọn kinh doanh tốt hơn?". Technical precision là cần thiết nhưng không đủ: executive thường chỉ hỏi 1 câu đơn giản "Nếu chọn sai thì business bị ảnh hưởng thế nào?". Phòng họp không cần thêm detail kỹ thuật, cần được **TRANSLATE** sang ngôn ngữ mà một người không chuyên cũng hiểu được. Làm tốt việc này thì stakeholder không chỉ nghe recommendation của Architect, mà đang tự ra một quyết định họ có thể **defend lại sau này** (trước leadership của họ).
- **Frame quyết định như 1 "PACKAGE", không phải 1 "VERDICT":** package gồm — các option đã xem xét, criteria dùng để cân nhắc, recommendation của Architect, và risk còn lại (residual risk) sau khi chọn. Lý do phải làm vậy: stakeholder không "adopt kiến trúc" của Architect, họ đang **accept một quyết định mà chính họ sẽ phải defend với leadership của họ**. Đưa ra verdict (chỉ nói "nên chọn X") khiến stakeholder không có gì để bảo vệ quyết định khi bị hỏi lại; đưa ra package thì họ có đủ context để trả lời.
- **DESCRIPTION — competency làm cho package "land" được:** đây là 1 trong 4 AI Fluency competency (năng lực giao tiếp hiệu quả với AI), được mở rộng sang phía stakeholder: cùng 1 discipline — nói cho audience đúng cái họ cần biết, bằng ngôn ngữ họ hiểu. Áp dụng vào stakeholder communication: frame hành vi/limit/oversight của hệ thống bằng ngôn ngữ MỤC TIÊU (GOAL) của stakeholder, khớp với mức độ AI-familiarity của họ mà không hy sinh accuracy.
  - **3 rule khi áp dụng Description:**
    1. **Lead with business outcome** trước, không mở đầu bằng architecture.
    2. **Frame limitation một cách trung thực (honestly)** — một security stakeholder tin tưởng hệ thống có limit được nói rõ, hơn là hệ thống được vẽ ra như hoàn hảo.
    3. **Anticipate peer-proof demand** — stakeholder sẽ cần justify lựa chọn này với người khác (leadership, peer của họ), nên phải để họ ra khỏi phòng với đủ "justification trong tay".
- **TRADEOFF TRANSLATION MAP** — 3 ví dụ minh hoạ cách dịch architecture framing sang decision language cho stakeholder (đủ gain / give-up / reversal cost cho từng ví dụ):
  1. **Large context window per call vs. retrieval over chunks**: Gain = design đơn giản hơn, full document nằm trong context, ít moving part lúc đầu. Give up = per-call cost cao hơn + response chậm hơn khi production volume tăng (**chú ý:** prompt caching có thể recover phần lớn input cost cho static content như policy doc giữ nguyên qua nhiều call — phải đánh giá caching trước khi coi per-call cost là fixed). Reversal cost = phải rework lại architecture sau khi cost spike ở production, cộng thêm credibility hit vì phải giải thích 1 khoản chi phí bất ngờ mà lẽ ra tránh được.
  2. **Trade logging details để lấy latency thấp hơn**: Gain = response nhanh hơn, user experience mượt hơn. Give up = giảm visibility vào việc gì đã xảy ra trong mỗi interaction. Reversal cost = trong workload thuộc regulated industry, đây là 1 compliance gap cần remediation.
  3. **Single delivery route vs. multi-platform**: Gain = build complexity thấp hơn, 1 auth/logging profile nhất quán. Give up = kém linh hoạt hơn cho các nhu cầu regional/compliance/procurement khác nhau. Reversal cost = production cutover bị delay hoặc block nếu route đã chọn không đáp ứng được 1 data residency hay deployment requirement phát sinh muộn.
- **Case study "the approval that was not an informed choice":** Architect trình bày recommend larger context window (giữ full policy document trong context mỗi call) để giữ design đơn giản, tránh phải xây retrieval layer. CTO hỏi cost per call → Architect trả lời khoảng 4 cent/interaction, và nói nếu document là static thì prompt caching có thể giảm đáng kể phần input cost. CTO approve ngay: "Fine, approved. Let's keep it simple." **6 tuần sau khi lên production**, CTO nhận invoice và bất ngờ: 4 cent × call volume của họ ra thành 1 dòng chi phí **5 chữ số/tháng (five-figure monthly)**. CTO ghi lại: "Tôi approve một direction, không phải một con số. Không ai nói với tôi 4 cent nhân với call volume của chúng ta là 1 dòng chi phí 5 chữ số/tháng. Nếu document là static, sao không cache nó? Và nếu định build xung quanh full-context luôn, tôi cần biết unwind nó sẽ tốn bao nhiêu khi hệ thống đã phụ thuộc vào nó." → **Root cause: reversal cost chưa từng được đưa vào cuộc trò chuyện.** Presentation đã nêu được gain (đơn giản) và trả lời đúng câu hỏi per-call cost được hỏi — nhưng chưa bao giờ identify yếu tố thứ 3: chuyện gì xảy ra với business khi lựa chọn này gặp production volume và phải bị đảo ngược sau khi hệ thống đã được xây dựng dựa trên nó. CTO approve 1 con số per-call, không phải 1 monthly bill, không phải cost để unwind sau này. 2/3 yếu tố tradeoff đã communicate/hiểu đúng; yếu tố thứ 3 thì không — và hoá ra lại là yếu tố **load-bearing** (chịu tải chính) của cả quyết định. Bài học: 1 presentation chính xác về mặt kỹ thuật vẫn có thể trả lời **sai câu hỏi**. Một stakeholder approve mà không hiểu reversal cost thì **chưa thực sự đưa ra informed choice** — phải nêu đủ cả 3 yếu tố **MỖI LẦN**, đặc biệt là reversal cost khi design "trông có vẻ hiển nhiên đơn giản hơn".
- **Checkpoint — "recommend the option and name the missing element":** Bối cảnh: 1 công ty bảo hiểm quy mô vừa muốn dùng Claude để draft response cho adjuster trả lời policyholder query. Workflow chịu quản lý bởi state insurance regulation với audit-trail obligation, volume cao và ổn định, sponsor quan tâm cả response quality VÀ khả năng giữ được defensible record cho mỗi automated interaction.
  - Option A: có per-interaction logging built-in. Gain = full audit trail + quality gate trước khi gửi. Give up = latency nhỏ do bước logging. Reversal = nhỏ, logging có thể tune mà không cần redesign. → **Đây là option nên recommend** vì khớp đúng audit-trail obligation đã nêu.
  - Option B: bỏ logging để lấy latency thấp hơn. Gain = response nhanh hơn. Give up = mất audit detail per-interaction. **Không nêu reversal cost.**
  - Option C: 1 augmented call, không logging, không human gate, chọn vì build cost thấp nhất.
  - Part 1 đáp án: **A** (logging built-in, full audit trail — khớp đúng audit-trail obligation). Part 2 đáp án: **C — reversal cost là yếu tố duy nhất bị thiếu** trong presentation của Option B (chi phí để restore lại logging sau khi design đã phụ thuộc vào latency gain). Distractor: các lựa chọn khác (gain của B, give-up của B, compliance posture) đều đã có mặt hoặc không phải "yếu tố duy nhất còn thiếu" — điểm thiếu chính xác là reversal cost, nhất quán với case study CTO ở trên.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Large context window per call (full doc in context) | Muốn design đơn giản lúc đầu, ít moving part, chưa cần retrieval layer | Per-call cost cao hơn, tăng theo volume; **prompt caching** có thể giảm phần input cost nếu content static — phải evaluate trước khi coi cost là fixed | Latency tăng khi production volume lớn; dễ bị cost spike bất ngờ nếu không cache | Cao — phải rework architecture (thêm retrieval layer) sau khi cost spike, cộng credibility hit vì phải giải thích 1 khoản chi phí tránh được |
| Retrieval over chunks | Volume lớn, cần kiểm soát cost/latency dài hạn, document lớn/nhiều | Cần build + maintain retrieval layer (indexing, chunking, ranking) | Retrieval sai/miss chunk quan trọng → answer thiếu context | Thấp hơn so với chiều ngược lại — đã sẵn hạ tầng linh hoạt để mở rộng |
| Trim logging để giảm latency | Ưu tiên UX nhanh, workload không thuộc regulated/audit-heavy | Thấp hơn — bớt 1 bước xử lý | Giảm visibility vào từng interaction; trong regulated workload là 1 compliance gap | Cao trong regulated context — phải remediation, chứng minh lại audit trail đã thiếu trong khoảng thời gian nào |
| Full per-interaction logging | Workflow có audit-trail obligation, cần defensible record (VD: insurance, healthcare, finance) | Latency nhỏ tăng thêm do bước logging | Rủi ro thấp — logging là quality gate trước khi gửi output | Nhỏ — logging có thể tune lại mà không cần redesign hệ thống |
| Single delivery route | Buyer/scope đơn giản, chưa có yêu cầu đa nền tảng/đa khu vực rõ ràng | Build complexity thấp, 1 auth/logging profile nhất quán | Kém linh hoạt cho regional/compliance/procurement khác nhau phát sinh sau | Cao — production cutover có thể bị delay/block nếu route hiện tại không đáp ứng được data residency hoặc deployment requirement mới |
| Multi-platform delivery | Buyer đã biết trước cần phục vụ nhiều region/compliance regime khác nhau | Build complexity + maintenance cao hơn ngay từ đầu | Nhiều bề mặt cần đồng bộ auth/logging | Thấp hơn về sau — đã có sẵn flexibility, không phải build lại khi yêu cầu mới xuất hiện |
| Trình bày đủ 3 yếu tố gain / give-up / reversal cost | Luôn luôn — đây là default bắt buộc cho mọi tradeoff presentation | Tốn thêm thời gian chuẩn bị (phải tính trước reversal scenario) | Thấp — stakeholder ra được informed choice, có thể defend lại sau này | Không áp dụng — đây chính là cách để giảm reversal cost bất ngờ về sau |
| Chỉ trình bày gain + give-up, thiếu reversal cost (case study CTO) | Không nên chọn — đây là anti-pattern | Có vẻ "rẻ" hơn lúc present (bớt 1 phần chuẩn bị) | Cao — **false alignment**: stakeholder tưởng đã hiểu, approve 1 direction nhưng không approve 1 con số/1 chi phí unwind; hậu quả lộ ra ở production (VD: invoice 5 chữ số/tháng bất ngờ) | Rất cao — phải quay lại giải trình sau khi hệ thống đã build xung quanh lựa chọn, mất credibility với stakeholder |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Decision frame | Bộ 4 câu hỏi (gain / give up / reversal cost / compliance posture) dùng để trình bày 1 tradeoff cho stakeholder ra quyết định |
| Reversal cost | Chi phí phải trả nếu chọn 1 phương án bây giờ nhưng sau phải đảo ngược (reverse) nó — câu hỏi hay bị skip nhất, thường là yếu tố "load-bearing" của quyết định |
| Package framing (vs. verdict) | Trình bày quyết định dưới dạng package (options + criteria + recommendation + residual risk) thay vì chỉ đưa ra 1 verdict/kết luận đơn |
| Verdict | Chỉ đưa ra kết luận "nên chọn X" mà không kèm option/criteria/risk — cách trình bày yếu, khiến stakeholder không có gì để defend sau này |
| Description (AI Fluency competency) | 1 trong 4 AI Fluency competency (giao tiếp hiệu quả với AI), mở rộng sang giao tiếp với stakeholder: nói đúng điều audience cần biết bằng ngôn ngữ họ hiểu, khớp GOAL của họ |
| Tradeoff translation map | Bảng dịch 1 architecture framing (kỹ thuật) sang decision language cho stakeholder, gồm đủ gain/give-up/reversal cost |
| Peer-proof demand | Nhu cầu của stakeholder phải justify lại lựa chọn này với leadership/peer của họ — Architect cần chuẩn bị sẵn justification để họ mang theo |
| False alignment | Trạng thái 1 quyết định "trông như" đã được approve/hiểu đúng trong phòng họp, nhưng thực chất 1 yếu tố tradeoff (thường là reversal cost) chưa từng được làm rõ, hậu quả lộ ra sau đó |
| Compliance posture | Câu hỏi thứ 4 trong decision frame — lựa chọn này ảnh hưởng thế nào tới khả năng tuân thủ compliance của tổ chức, đặc biệt trong regulated environment |
| Prompt caching (trong context của lesson này) | Cơ chế có thể recover phần lớn input cost cho static content (VD: policy document) giữ nguyên qua nhiều call — cần evaluate trước khi coi per-call cost của large-context design là cố định |

## Ghi chú phạm vi lesson (out-of-scope)
Phần "Tradeoffs & GTM" trên Skilljar gộp chung nội dung trade-off framing (C4.2, lesson này) với nội dung GTM demo design / limit placement / joint scoping / objection handling (thuộc C4.4, Partner Track, không nằm trong exam scope theo course). Note này **chỉ** cover phần C4.2 — trade-off framing; phần demo design được note ở lesson C4.4 riêng.

## Gotchas / bẫy hay gặp
- [ ] Trình bày conclusion/recommendation mà không kèm options + criteria (verdict framing) → stakeholder "approve" nhưng không có gì để defend lại với leadership của họ sau này
- [ ] Bỏ qua câu hỏi 3 (reversal cost) trong decision frame vì design "trông có vẻ hiển nhiên đơn giản hơn" — đây chính là câu hỏi hay bị skip nhất và thường là yếu tố load-bearing
- [ ] Trả lời đúng câu hỏi được hỏi (VD: per-call cost) nhưng không chủ động nêu hệ quả ở scale production (monthly cost, cost để unwind) → stakeholder approve 1 number, không approve 1 direction có hiểu đầy đủ hệ quả
- [ ] Coi "stakeholder nói yes ở cuối buổi presentation" = đã hiểu đầy đủ tradeoff — đây là cái TRAP của case study CTO: cảm giác "room felt aligned" không đồng nghĩa với informed choice
- [ ] Đề xuất large-context design với per-call cost cố định mà không nhắc đến khả năng dùng prompt caching cho static content — bỏ lỡ 1 lựa chọn giảm cost hợp lý, khiến reversal cost bị đội lên khi phát hiện ra sau
- [ ] Trong workflow có audit-trail obligation (regulated), chọn phương án trade logging cho latency mà không nêu rõ đây tạo ra compliance gap và reversal cost để remediation
- [ ] Nhầm lẫn giữa "đã nêu gain + give-up" với "đã trình bày đủ tradeoff" — thiếu reversal cost vẫn là thiếu, dù 2/3 yếu tố khác đã communicate rõ

## Exam tips
- Gặp câu hỏi dạng "presentation này thiếu điều gì" (như checkpoint Option B) → mặc định soát theo đúng thứ tự 4 câu hỏi decision frame; nếu đề chỉ nêu gain + give-up mà không nói tới việc "phải đảo ngược lựa chọn sau này thì tốn gì" → đáp án gần như chắc là **thiếu reversal cost**.
- Câu hỏi chọn option đúng theo constraint đề bài (VD: có audit-trail obligation, regulated industry) → luôn ưu tiên option match trực tiếp với compliance/audit requirement đã nêu trong đề (như Option A ở checkpoint), không chọn theo option có build cost thấp nhất.
- Phân biệt rõ "package" framing (options + criteria + recommendation + residual risk) với "verdict" framing (chỉ đưa ra 1 recommendation) — đề thi có thể mô tả 1 tình huống presentation và hỏi nó thuộc kiểu framing nào, hoặc tại sao 1 buổi presentation "trông thành công" (room aligned) vẫn có thể là false alignment.
- Nhớ: reversal cost không phải lúc nào cũng lớn (VD: Option A ở checkpoint có reversal "minor, có thể tune không cần redesign") — điểm mấu chốt là phải NÊU RA nó mỗi lần, không phải nó luôn phải là con số lớn.

## Code / config snippets
```python
"""
Minh hoạ cấu trúc "tradeoff_presentation" theo đúng decision frame 4 câu hỏi
(gain / give_up / reversal_cost / compliance_impact), và 1 hàm kiểm tra
presentation nào bị thiếu field reversal_cost — mô phỏng đúng lỗi trong
case study "the approval that was not an informed choice" (CTO approve
per-call cost nhưng không ai nói reversal cost, 6 tuần sau invoice bất ngờ).
"""

# Presentation ĐÚNG: có đủ 4 yếu tố, bao gồm reversal_cost
tradeoff_presentation_full_context = {
    "option_name": "Larger context window per call (full policy doc in context)",
    "gain": "Design đơn giản hơn, full document trong context, ít moving part lúc đầu",
    "give_up": "Per-call cost cao hơn (~4 cent/call), tăng theo production volume",
    # reversal_cost: đây là câu hỏi số 3, hay bị skip nhất — PHẢI điền, không để None
    "reversal_cost": (
        "Phải rework architecture (thêm retrieval layer) sau khi cost spike ở "
        "production; credibility hit khi giải thích 1 khoản chi phí tránh được"
    ),
    "compliance_impact": None,  # ví dụ này không thuộc regulated context
}

# Presentation THIẾU (giống case study CTO thực tế đã xảy ra):
# chỉ có gain + give_up, KHÔNG có reversal_cost -> stakeholder approve
# "một direction", không approve "một con số" hay "chi phí unwind sau này"
tradeoff_presentation_missing_reversal = {
    "option_name": "Larger context window per call (as actually presented to CTO)",
    "gain": "Design đơn giản, tránh phải build retrieval layer",
    "give_up": "Khoảng 4 cent/interaction ở model tier đang dùng",
    "reversal_cost": None,  # <-- BUG: chưa từng được đưa vào cuộc trò chuyện
    "compliance_impact": None,
}


def find_missing_reversal_cost(presentations: list[dict]) -> list[str]:
    """
    Quét qua danh sách các tradeoff presentation, trả về tên option nào
    bị thiếu (None hoặc rỗng) field reversal_cost.
    Dùng như 1 checklist trước khi trình bày tradeoff cho stakeholder,
    để không lặp lại lỗi của case study CTO (2/3 yếu tố nêu đủ, thiếu
    đúng yếu tố "load-bearing" là reversal cost).
    """
    missing = []
    for p in presentations:
        if not p.get("reversal_cost"):  # None hoặc string rỗng đều coi là thiếu
            missing.append(p["option_name"])
    return missing


if __name__ == "__main__":
    all_presentations = [
        tradeoff_presentation_full_context,
        tradeoff_presentation_missing_reversal,
    ]
    # Kỳ vọng output: chỉ presentation "as actually presented to CTO" bị flag
    print(find_missing_reversal_cost(all_presentations))
```

## Câu hỏi chưa rõ
- ?
