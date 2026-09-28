# C4.1 — Structured discovery với non-technical stakeholder

> **Course:** 4 — Stakeholder Engagement, Lifecycle & GTM (178 min) · **Exam domain:** D6 (14%) + D1 (17%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Run a structured discovery conversation with a non-technical stakeholder and translate what you learn into architectural requirements and documented assumptions, so the design traces back to the business case rather than to your own technical preference

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Discovery không phải là 1 conversation bình thường, mà là 1 structured elicitation.** Ba module trước (design, integration, governance) giúp biết cách đánh giá pattern/deployment platform/control posture, nhưng discovery mới trả lời câu hỏi: có đang giải đúng vấn đề không. Stakeholder thường mô tả problem bằng business language — việc của Architect là nghe ra ý nghĩa thật phía sau, phát hiện constraint ẩn trong đó, và rời khỏi call với 1 record mà design có thể bám theo. Discovery chính là bước tạo ra artifact mà toàn bộ design sẽ phụ thuộc vào.
- **3-step filter chạy trong suốt discovery call:**
  1. **Listen** — nghe business goal bằng plain language, chú ý vào ý nghĩa (meaning) phía sau từ ngữ. Stakeholder mô tả outcome họ muốn, không tự mô tả constraint mà Architect cần để design.
  2. **Translate** — dịch điều nghe được thành requirement, assumption, và unresolved constraint — tách ra: design phải support cái gì, cái gì cần confirm thêm, cái gì có thể block solution về sau.
  3. **Write down** — ghi lại ngay trước khi conversation trôi qua topic khác. Nếu bỏ filter này, design sẽ kế thừa assumption của chính Architect chứ không phải của business; mismatch này có thể không lộ ra cho tới khi đổi hướng đã tốn kém và khó hơn nhiều.
- **Core move của discovery là translation: một preference gần như luôn ẩn 1 constraint bên trong.** Ví dụ kinh điển trong lesson: stakeholder nói "We want this to feel seamless." Nếu ghi luôn "seamless" thành requirement thì Architect chưa học được gì cả — chỉ có summary cảm nhận mong muốn của stakeholder, chưa có gì để design bám vào.
  - Việc thật sự bắt đầu bằng câu hỏi tiếp theo: **điều gì sẽ làm nó KHÔNG seamless?** Đó là nơi các constraint ẩn lộ ra — ví dụ: user không nên chờ quá 1-2 giây cho bước kế tiếp; user không nên phải nhập lại info đã có sẵn upstream; exception nên được chuyển lặng lẽ cho human reviewer thay vì hiện lỗi kỹ thuật; toàn bộ workflow phải nằm trong 1 application duy nhất. Mỗi câu trả lời làm design sắc nét hơn.
  - Qua đó "seamless" được biến thành các requirement mà architecture phải support: 1 latency target, 1 integration requirement, 1 handoff rule, 1 safe-failure path. Stakeholder gọi tên outcome bằng business language; Architect dịch nó thành thứ hệ thống build được và đo được.
- **Preference nằm ở tầng trên, constraint nằm ở tầng dưới.** Bất cứ khi nào stakeholder dùng 1 "experience word" (seamless, easy, fast, simple, intuitive) — coi đó là **signal cần discovery thêm**, chưa phải requirement. Hỏi tiếp: điều gì sẽ phá vỡ experience đó, user không được phép nhận ra điều gì, cái gì phải xảy ra ở background, điều gì vẫn phải đúng khi có lỗi xảy ra. Các câu trả lời đó mới là thứ đi vào design record. Một constraint hữu ích phải **testable + bounded** — đó là điều design build được; preference chỉ cho biết WHERE cần điều tra, câu hỏi tiếp theo mới tạo ra constraint thật.
- **4 câu hỏi biến 1 statement mơ hồ thành requirement, ép statement vào đúng 1 trong 4 bucket:**
  1. **Must do** — capability mà deployment phải deliver, diễn đạt theo business outcome (không phải feature) — tách rõ phần Claude sở hữu vs. phần vẫn thuộc hệ thống/con người hiện có.
  2. **Must not do** — boundary, hành động bị cấm, case phải route sang human. Stakeholder hiếm khi tự nói ra nhóm này — phải hỏi trực tiếp.
  3. **Must cost** — budget constraint theo ngôn ngữ stakeholder kiểm soát: latency target, cost ceiling mỗi interaction, volume forecast — trở thành design constraint quan trọng.
  4. **Must prove** — evidence deployment phải sản sinh ra được. Trong regulated workflow, proof obligation là 1 phần của requirement set; phát hiện lúc discovery rẻ hơn rất nhiều so với phát hiện lúc legal review vài tuần sau.
  - Với ví dụ "seamless": có thể thực chất là latency budget mà user không nhận ra, 1 handoff không làm gián đoạn flow, 1 failure state không được để lộ system internals. Một khi đã discover ra, team có requirement để design, test, và defend được.
- **Output của discovery là 1 translation table** — mỗi item phát hiện thành 1 row gồm: stakeholder statement (nguyên văn), implied constraint, required architectural decision, và assumption được document lại (nếu constraint chưa confirm). Giữ 1 row/item để reasoning không đứt đoạn khi đi từ discovery sang design, và giữ assumption luôn ở trạng thái visible.
  - Translation table 4 ví dụ trong lesson:
    1. "We want this to feel seamless." → constraint: experience phải nằm trong latency budget đã đồng thuận, failure không được lộ system internals hoặc phá flow → decision: set p95 latency target làm design constraint, design 1 graceful internal-safe failure state → assumption: "seamless" ám chỉ perceived responsiveness + continuity of flow, cần confirm lại với stakeholder.
    2. "It just needs to read the form and route it." → constraint: routing có thể là 1 deterministic business rule → decision: giữ routing decision trong rule engine, Claude chỉ extract, hệ thống route → assumption: routing logic được owned/maintained ngoài model, cần confirm owner.
    3. "Clinicians will review the output anyway." → constraint: 1 licensed human phải authorize output trước khi nó trở thành 1 phần của record có legal/financial/clinical consequence → decision: build human-in-the-loop authorization step làm mandatory checkpoint → assumption: review là 1 architectural gate, cần confirm authority + timing.
    4. "We are in healthcare, so be careful with data." → constraint: workflow nhiều khả năng mang proof obligation dưới 1 health-privacy regime → decision: coi audit-trail + data-handling evidence là core requirement từ ngày đầu → assumption: đây là covered workflow có formal obligation, cần confirm scope với compliance.
- **Cost · Complexity · Risk của discovery:** Cost — 1 discovery call chạy đủ lâu để tìm ra constraint thật rẻ hơn rất nhiều so với redesign sau khi hidden constraint lộ ra lúc legal/compliance review. Complexity — làm việc qua 4 bucket câu hỏi thêm structure cần thiết; translate preference thành constraint theo thời gian thực đòi hỏi luyện tập có chủ đích. Risk — thất bại đắt nhất là 1 unstated constraint sống sót qua toàn bộ quá trình test và trở thành blocker ở production review, đúng lúc cost để đổi design đang ở mức cao nhất.
- **Case study "Watch Out": discovery call biến thành design session (hospital dictation).** Setup: discovery là nơi công việc bắt đầu, design là nơi nó tăng tốc — 1 Architect giỏi thường bắt đầu hình thành solution ngay giữa call, việc sketch cảm giác productive và stakeholder có vẻ hài lòng. Đó chính xác là lúc câu hỏi dừng lại.
  - Bối cảnh: regional hospital network, Claude draft clinical note từ nurse dictation. Stakeholder mô tả vấn đề (nurse mất quá nhiều thời gian viết note) và nói có "a review step ... just a quick check". Architect nhận diện ngay đây là augmented pattern quen thuộc, chốt luôn prototype timeline và chuyển sang design mà không hỏi thêm về "quick check" đó là gì.
  - 3 constraint chỉ lộ ra quá muộn:
    1. "Quick check" không phải convenience feature — nursing workflow yêu cầu 1 **licensed clinician phải authorize** mọi model output trước khi nó vào patient record → human authorization là 1 required architectural gate, không phải optional add-on.
    2. Dictation chứa **PHI (protected health information)** — PHI đã đi qua context window mà không có handling mà workflow này đòi hỏi.
    3. Network trải rộng **2 state có record-retention rule khác nhau** — thiết kế single-region ban đầu chưa từng account cho điều này.
  - Không có constraint nào trong 3 cái trên là hiếm hoặc khó tìm — mỗi cái đều sẽ lộ ra từ 1 câu hỏi trực tiếp trong nhóm **must-prove** và **must-not-do**, nếu call không chuyển sang sketching trước khi các câu hỏi đó được hỏi.
  - **Root cause:** 1 sketch proposal đủ competent đã kết thúc chuỗi câu hỏi mà 1 discovery call tồn tại để hỏi. Sketch đó plausible, và chính plausibility là điều làm nó nguy hiểm — stakeholder nghe 1 architecture tự tin thì mặc định Architect đã có đủ thông tin để build nó. Cách phòng vệ rất "boring": hoàn tất hết 4-category question set trước khi propose bất cứ gì, và coi mọi câu "it's just a review" là 1 constraint cần truy tới cùng.
- **Checkpoint "find the undocumented assumption":** so 1 discovery-call summary với 1 requirements document được sản sinh ra từ đó — 3 item trace được về đúng 1 câu stakeholder đã nói, 1 item là assumption Architect tự thêm vào mà không surface constraint bên dưới.
  - Requirements document: (1) Claude draft customer email, người thật gửi; (2) response phải trong two-second perceived budget; (3) refund trên threshold route sang human approver; (4) conversation transcript retained 60 ngày cho analytics.
  - Stakeholder chỉ nói: "Anything big requires a person's sign off." / "Draft the reply, but we send it ourselves." / "It has to feel instant to the user."
  - **Part 1 — đáp án: D (item 4, 60-day retention).** Item 1, 2, 3 đều trace ngược được về đúng 1 câu nói của stakeholder; item 4 (60-day retention cho analytics) không hề được nói ra.
  - **Part 2 — đáp án: D (không có statement nào support item 4).** Đây chính là failure mode "design sketch before translation is done" ở case study trên, tái hiện dưới dạng 1 checkpoint: retention period và analytics purpose là do Architect tự invented, không phải điều stakeholder yêu cầu.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Ghi preference thành requirement luôn (không translate) | Không nên chọn — chỉ xảy ra khi Architect vội, muốn "gọn" discovery call | Thấp ngay lúc discovery (call ngắn, kết thúc sớm) | Cao — requirement mơ hồ ("seamless" = requirement) không testable/bounded, design không có gì để build/test/defend against; hidden constraint (latency, PHI, retention...) chỉ lộ ra ở QA/legal/production review | Rất cao — phải quay lại discovery từ đầu sau khi design/code đã tồn tại, sửa architecture đã build thay vì sửa 1 câu hỏi chưa hỏi |
| Translate preference → constraint qua 4-bucket question set (must do/must not do/must cost/must prove) | Mặc định cho mọi discovery call, đặc biệt khi stakeholder dùng experience word (seamless, easy, fast, simple, intuitive) | Trung bình — call dài hơn, cần luyện tập để translate real-time, thêm bước write-down ngay trong call | Thấp hơn nhiều — constraint được surface sớm lúc rẻ nhất để sửa; vẫn có risk nếu bỏ sót 1 bucket (thường là must-not-do/must-prove vì stakeholder không tự nói ra) | Thấp — nếu thiếu 1 row, chỉ cần hỏi lại đúng câu đó, chưa phải sửa design đã build |
| Discovery call kết thúc bằng sketch/prototype sớm (như case study hospital dictation) | Không nên chọn — cảm giác productive, stakeholder có vẻ hài lòng nên dễ bị cuốn theo, nhưng đây chính là anti-pattern lesson cảnh báo | Thấp trước mắt — "prototype next week" nghe nhanh, stakeholder pleased ngay tại call | Cao — sketch plausible khiến stakeholder tin Architect đã có đủ info; constraint thật (human authorization gate, PHI handling, multi-state retention) lộ ra sau khi design/code đã tồn tại, đúng lúc cost thay đổi cao nhất | Rất cao — phải thêm architectural gate (human-in-the-loop), redesign data handling cho PHI, và re-architect cho multi-region retention sau khi hệ thống đã được xây theo giả định sai |
| Hoàn tất hết 4-category question set trước khi propose bất cứ sketch nào | Mặc định — "boring but protective move" mà lesson khuyến nghị, áp dụng mọi discovery call có khả năng liên quan compliance/safety | Trung bình — trì hoãn cảm giác "tiến độ" trong mắt stakeholder, cần kỷ luật không sketch sớm | Thấp — mọi "it's just a review"/"it's just a quick check" được truy tới cùng trước khi commit vào 1 architecture | Thấp — nếu phát hiện thiếu constraint, vẫn đang ở giai đoạn discovery, chưa phải sửa lại thứ đã build |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Structured elicitation | Discovery không phải free-flow conversation mà là 1 quy trình có cấu trúc (3-step filter) để lấy ra requirement/constraint/assumption |
| 3-step filter (Listen / Translate / Write down) | Vòng lặp áp dụng liên tục trong discovery call: nghe ý nghĩa thật, dịch thành requirement/assumption/unresolved constraint, ghi lại ngay trước khi chuyển topic |
| Preference vs. constraint | Preference (seamless, easy, fast...) là tầng bề mặt business ngôn ngữ nói ra; constraint là tầng thật design phải build against — phải translate từ preference ra constraint |
| Experience word | Từ mô tả cảm nhận mong muốn (seamless, easy, fast, simple, intuitive) — luôn là signal cần hỏi thêm, không phải requirement sẵn sàng dùng |
| Testable + bounded constraint | Tiêu chuẩn của 1 constraint "useful" — đo được (testable) và có giới hạn rõ (bounded), khác với 1 preference mơ hồ |
| 4 question buckets (must do / must not do / must cost / must prove) | Khung 4 câu hỏi ép 1 statement mơ hồ thành requirement thuộc đúng 1 category: capability phải deliver, boundary bị cấm, budget constraint, evidence phải sản sinh |
| Must-not-do | Bucket dễ bị bỏ sót nhất — stakeholder hiếm khi tự nói ra boundary/prohibited action, Architect phải hỏi trực tiếp |
| Must-prove | Bucket chứa proof obligation trong regulated workflow (audit trail, compliance evidence) — rẻ hơn rất nhiều nếu phát hiện lúc discovery so với lúc legal review |
| Translation table | Artifact output của discovery: mỗi row gồm stakeholder statement / implied constraint / architectural decision / assumption documented |
| Assumption (documented) | Phần constraint chưa được stakeholder confirm — vẫn phải ghi lại rõ ràng để biết cần đi confirm lại, tránh trở thành undocumented assumption |
| Undocumented assumption | Assumption Architect tự invent mà không trace được về statement nào của stakeholder — failure mode chính của lesson (case study + checkpoint) |
| Design sketch before translation is done | Anti-pattern: bắt đầu propose/sketch solution trước khi hoàn tất 4-bucket question set, khiến discovery call dừng lại quá sớm |
| Human authorization gate | Ví dụ 1 required architectural gate hay bị hiểu lầm thành "quick check"/convenience feature trong khi thực chất là mandatory checkpoint |
| PHI (protected health information) | Loại data nhạy cảm trong ví dụ hospital dictation — cần handling riêng khi đi qua context window, không tự nhiên có nếu không được discover |

## Gotchas / bẫy hay gặp
- [ ] Ghi thẳng preference ("seamless", "easy", "fast"...) làm requirement mà không hỏi "điều gì sẽ làm nó KHÔNG seamless?" — mất luôn cơ hội tìm ra latency budget/handoff rule/failure path thật
- [ ] Bắt đầu sketch/propose solution ngay khi vừa nghe đủ để nhận diện pattern quen thuộc (VD "à đây là augmented pattern") — chính là lúc câu hỏi discovery dừng lại sớm nhất, dù sketch rất plausible
- [ ] Coi câu nói kiểu "there's a review step, but it's just a quick check" là chi tiết nhỏ có thể thêm sau — thực chất phải truy tới cùng vì có thể là 1 required architectural gate (human authorization) chứ không phải convenience feature
- [ ] Không hỏi riêng nhóm **must-not-do** và **must-prove** vì nghĩ 2 nhóm này ít quan trọng hơn must-do/must-cost — đây là 2 nhóm stakeholder gần như không tự nói ra, và cũng là 2 nhóm chứa constraint dạng human authorization gate / proof obligation / PHI handling
- [ ] Tự thêm 1 requirement (retention period, analytics purpose, v.v.) vào requirements document mà không trace được về đúng 1 câu nói của stakeholder — tạo ra 1 undocumented assumption giống checkpoint item 4 (60-day retention)
- [ ] Bỏ qua bước "write down" ngay trong call, định ghi lại sau — dễ làm design vô tình kế thừa assumption của Architect thay vì của business
- [ ] Chỉ design cho 1 region/1 luồng dữ liệu vì stakeholder không chủ động nhắc đến scope địa lý/pháp lý — trường hợp hospital network trải 2 state với retention rule khác nhau là ví dụ điển hình

## Exam tips
- Gặp câu hỏi dạng "đâu là undocumented assumption trong requirements document" → so từng item với nguyên văn statement của stakeholder; item nào không trace về được câu nào (dù nghe hợp lý, VD retention cho analytics) chính là đáp án, không phải item nghe "kỹ thuật" nhất.
- Gặp scenario mô tả 1 discovery call mà Architect nhận diện pattern nhanh, chốt timeline, chuyển sang sketch ngay — nhận diện đây là anti-pattern "design sketch before translation is done"; đáp án đúng thường là "tiếp tục hỏi hết 4 bucket trước khi propose", không phải "tăng tốc build prototype".
- Khi đề cho 1 statement mơ hồ và yêu cầu phân loại vào must-do/must-not-do/must-cost/must-prove: từ khoá "review/approval/sign-off/route to human" → must-not-do hoặc must-do (tuỳ hướng); từ khoá "budget/latency/volume/cost ceiling" → must-cost; từ khoá "audit/compliance/regulated/evidence/healthcare/legal" → must-prove.
- Nhớ nguyên tắc cost: chi phí phát hiện 1 constraint (PHI handling, retention rule, authorization gate) ở discovery luôn thấp hơn phát hiện cùng constraint đó ở QA/legal/production review — exam thường test khả năng nhận ra "thời điểm phát hiện" chứ không chỉ "loại constraint".

## Code / config snippets
```python
# Minh hoạ cấu trúc 1 row trong "translation table" — output chính của discovery
# và 1 hàm kiểm tra row nào bị thiếu nguồn statement (undocumented assumption)

from dataclasses import dataclass
from typing import Optional


@dataclass
class TranslationTableRow:
    # Câu nói nguyên văn của stakeholder — bắt buộc phải có, đây là "nguồn" của row
    stakeholder_statement: Optional[str]
    # Constraint ẩn suy ra được từ statement (VD: latency budget, human authorization gate)
    implied_constraint: str
    # Quyết định architecture tương ứng (VD: set p95 latency target, thêm human-in-the-loop step)
    architectural_decision: str
    # Assumption chưa được confirm — nếu None nghĩa là constraint đã confirm chắc chắn
    assumption: Optional[str] = None


def find_undocumented_rows(rows: list[TranslationTableRow]) -> list[TranslationTableRow]:
    """Trả về các row KHÔNG trace được về statement nào của stakeholder.

    Đây chính là bẫy trong checkpoint "find the undocumented assumption":
    item 4 (60-day retention) không có stakeholder_statement nào support,
    nghĩa là Architect đã tự invent ra requirement đó.
    """
    return [row for row in rows if not row.stakeholder_statement]


# Ví dụ dùng lại đúng 4 item trong checkpoint của lesson
rows = [
    TranslationTableRow(
        stakeholder_statement="Draft the reply, but we send it ourselves.",
        implied_constraint="Claude chỉ draft, con người phải là người gửi thật",
        architectural_decision="Claude tạo draft email, human-in-the-loop trước khi send",
    ),
    TranslationTableRow(
        stakeholder_statement="It has to feel instant to the user.",
        implied_constraint="Perceived latency phải trong ngưỡng ~2 giây",
        architectural_decision="Set two-second perceived latency budget làm design target",
    ),
    TranslationTableRow(
        stakeholder_statement="Anything big requires a person's sign off.",
        implied_constraint="Refund/transaction lớn hơn threshold phải có human approver",
        architectural_decision="Route refund vượt threshold sang human approver",
    ),
    TranslationTableRow(
        stakeholder_statement=None,  # <-- không có câu nói nào của stakeholder support item này
        implied_constraint="(tự suy ra) cần giữ transcript cho mục đích analytics",
        architectural_decision="Retain conversation transcript 60 ngày",
        assumption="Retention period + analytics purpose do Architect tự thêm, chưa confirm",
    ),
]

# find_undocumented_rows(rows) -> trả về đúng row thứ 4, khớp đáp án checkpoint (D / D)
```

## Câu hỏi chưa rõ
- ?
