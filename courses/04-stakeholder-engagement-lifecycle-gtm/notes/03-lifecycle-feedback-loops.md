# C4.3 — Stakeholder feedback loop & governance checkpoint trong lifecycle

> **Course:** 4 — Stakeholder Engagement, Lifecycle & GTM (178 min) · **Exam domain:** D6 (14%) + D5 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Build and operate a stakeholder feedback loop across the deployment lifecycle, naming what triggers review, what an SLA breach requires, and when to iterate versus re-architect, with governance checkpoints built into the same loop

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
> **Lưu ý gộp nội dung:** file này có tên "...trong lifecycle" (rộng hơn feedback loop) vì course Skilljar Module 4 có 2 section liên tiếp trong cùng lifecycle — **Feedback Loops** (stage monitoring-and-iteration) và **Documentation** (stage handoff) — và cả 2 KHÔNG có lesson file riêng nào khác trong repo. Vì 2 stage này liền kề nhau trong deployment lifecycle (feedback loop giữ hệ thống healthy lúc Architect còn ở đó, documentation giữ hệ thống healthy sau khi Architect đi), note gộp chung làm 1 file, chia rõ 2 phần A/B dưới đây.

### A. Feedback loop (monitoring-and-iteration)
- **Bối cảnh:** production observability + audit trail chỉ ghi lại hệ thống đang làm gì (raw signal). Feedback loop trả lời câu hỏi tiếp theo: signal nào cần lọc ra, khi nào escalate ra ngoài team, SLA yêu cầu gì khi performance tụt dưới chuẩn. Lifecycle term: feedback loop = stage **monitoring-and-iteration**.
- **Vấn đề gốc — drift không ồn ào:** một deployment sống ổn lúc launch có thể **drift dần** (usage pattern đổi, prompt style mới, issue phức tạp hơn) mà không có sự cố "gãy" rõ ràng. Chất lượng xói mòn từ từ, không phải sập một lần — nên team không có feedback loop thường KHÔNG thấy suy giảm cho tới khi user đã cảm nhận được.
- **Feedback loop là decision layer NẰM TRÊN observability stack.** Observability chỉ cho raw material (latency, error rate, eval score, usage pattern) — 1 signal đơn lẻ chưa phải là quyết định: 1 spike có thể là noise, 1 spike khác có thể là vấn đề thật, 1 spike thứ ba chỉ đáng chú ý nếu nó lặp lại.
- **5-step loop:** Signals (hệ thống đang show gì?) → Triage (cái gì cần chú ý ngay, cái gì chờ được?) → Decide (cần team fix, stakeholder review, hay không cần action?) → Act (correction / guardrail update / escalation nào cần làm?) → Review (response đó có work không, rule có cần đổi không?).
- **Analogy — control room nhà ga:** sensor chỉ cho biết tàu nào trễ ở đâu, nhưng phải có người quyết định trễ đó là minor hay cần thông báo hành khách hay cần đổi lịch. Chính JUDGMENT LAYER đó biến hệ thống từ "chỉ đo được" thành "quản lý được".
- **SLA nêu đúng 3 thứ**, và threshold KHÔNG BAO GIỜ được đặt tùy ý — phải trace về nguồn cụ thể:
  1. Đo cái gì? (what are we measuring)
  2. Breach là gì? (what counts as a breach)
  3. Khi breach xảy ra thì sao? (what happens when a breach occurs)
  - Traceability của threshold: latency → user-experience expectation đã xác định ở discovery; availability → mức critical của deployment với business; quality → eval result + acceptance criteria đã thiết lập từ trước. Nếu 1 con số không trace được về 1 trong 3 nguồn này, nó chỉ là target "nghe hợp lý" chứ không defensible.
- **Cost là expectation hay vỡ nhất sau launch** — production volume thường gấp **10-100x** (1-2 order of magnitude) so với POC/pilot, nên cost tầm thường lúc POC có thể thành một dòng chi phí 5 chữ số/tháng ở scale. Đối phó trước: đưa stakeholder consumption forecast ở production volume kỳ vọng, đặt tên rõ spend-control posture (caching, model tiering, budget alert), và đưa narrative model-tiering ra TRƯỚC hoá đơn đầu tiên, không phải sau.
- **Regulated deployment thêm review checkpoint chạy THEO LỊCH, độc lập với threshold.** Observability ghi lại chuyện đã xảy ra; feedback loop quyết định làm gì với nó. Trong deployment bị regulate, một số review phải diễn ra dù không có gì sai (VD: healthcare workflow có nghĩa vụ documentation cần periodic output audit theo lịch cố định; deployment liên quan data-residency cần scheduled confirmation môi trường vẫn đáp ứng residency rule). Đây là nghĩa vụ **DESIGN-TIME**, không phải thứ thêm sau — nếu không build sớm, sẽ đắt hơn rất nhiều khi có người yêu cầu proof.
- **Governance table** — map mỗi signal → trigger → Architect response → regulatory checkpoint. Table này phải tồn tại TRƯỚC launch — đây là cơ chế biến policy thành operating routine hàng ngày. 4 signal type chuẩn trong governance table:
  1. **Output quality (eval score):** trigger = score vượt threshold rút ra từ eval suite; Architect action = chẩn đoán nguyên nhân prompt/data/model drift, quyết định iterate vs. re-architect; regulated checkpoint = periodic output audit theo documentation standard, chạy theo lịch cố định BẤT KỂ score thế nào.
  2. **Latency p95:** trigger = vượt budget đặt từ user-experience requirement; action = investigate bottleneck, tune hoặc escalate lên stakeholder review nếu budget bản thân nó sai; regulated checkpoint = thường không có, trừ khi latency che mất 1 gap logging/traceability.
  3. **Cost per interaction:** trigger = vượt budget envelope đã thống nhất ở discovery; action = xác định driver, mang tradeoff lên stakeholder nếu cần revisit budget; regulated checkpoint = thường không có, trừ khi cost control là 1 constraint bị regulate.
  4. **Data-residency configuration:** trigger = scheduled confirmation; action = confirm + record residency posture, flag drift ngay nếu có; regulated checkpoint = residency confirmation theo lịch cố định.
- **Cost · Complexity · Risk:** Cost — loop tạo ra effort liên tục cho Architect, nhưng rẻ hơn nhiều so với phát hiện suy giảm ở 1 quarterly review sau khi mọi dashboard "trông vẫn ổn". Complexity — phần khó nhất là quyết định signal nào đáng chú ý vs. chỉ là noise, observability tooling không thể tự đưa ra judgment đó. Risk — failure mode lớn nhất là 1 compliance checkpoint không bao giờ được wire vào trigger, cho phép 1 vi phạm documentation standard chạy âm thầm nhiều tuần trước khi 1 routine review phát hiện ra.
- **Case study — "observability stack thay thế feedback loop":** Architect dựng observability stack chỉn chu (dashboard live, alert cấu hình, data chảy đều) → dễ (và SAI) khi kết luận stakeholder feedback đã "được cover". Trace 90 ngày alert log vs. lịch stakeholder review:
  - Tuần 1-3: eval score ổn định ở baseline, latency/cost nominal, launch review diễn ra tuần 1 → không cần escalate.
  - Tuần 4-7: eval score drift xuống dần từng tuần, nhưng **error rate FLAT nên không alert nào bắn** → không có review nào được schedule/tổ chức. Theo đúng thiết kế, 1 quality-drift trigger LẼ RA phải escalate lên Architect review từ tuần 5, rồi lên stakeholder review khi diagnosis xác nhận drift.
  - Tuần 8-12: score vẫn giảm, stakeholder tự báo output "gần đây kém hữu ích hơn". Quarterly review tuần 12 mới phát hiện ra — chậm **7 tuần** so với khi loop lẽ ra phải bắt được.
  - Root cause: signal đã tồn tại (eval score drift từ tuần 4) nhưng KHÔNG có gì quyết định nó quan trọng — thiếu DECISION LAYER, không có governance rule map slow quality drift → review trigger. Drift chưa bao giờ vượt error-rate threshold nên không alert nào bắn — 1 drift không có trigger thì vô hình cho tới khi có người tình cờ để ý.
  - **Bài học cốt lõi:** monitoring KHÔNG PHẢI là feedback loop. Dashboard chỉ collect + display signal. Feedback loop map mỗi signal → 1 trigger, 1 owner, 1 required action. Phải xây governance table map signal → trigger → action → owner, bao gồm cả slow drift VÀ hard failure.
- **Checkpoint "triage the production signals"** (9 signal, drag vào 1 trong 4 bucket: Internal monitoring / Architect review / Stakeholder review / Noise) — raw source không có answer key cố định (đây là bài tập interactive drag-drop), nên note chỉ tập trung vào REASONING áp nguyên tắc bài học, không phải đáp án cứng:
  - Signal có nguyên nhân benign đã biết / vẫn trong budget / giải thích được bởi factor đã biết → **Noise / Internal monitoring** (VD: latency p99 tăng 40ms nhưng vẫn trong budget; 1 malformed request từ known bad client; batch job retry rồi thành công; token usage tăng do seasonal bump đã biết; prompt template mới ship với error rate flat).
  - Trend rõ, kéo dài nhiều tuần trên 1 quality signal → giống case study drift ở trên → **Architect review** (chẩn đoán), có thể escalate tiếp lên **Stakeholder review** khi diagnosis xác nhận drift (VD: eval score giảm liên tục 3 tuần).
  - Breach 1 threshold đã AGREED trong governance table (VD: cost per interaction vượt budget đã thống nhất) → theo governance table, Architect xác định driver rồi mang tradeoff lên → **Stakeholder review**.
  - Scheduled regulated checkpoint đến hạn (data-residency confirmation due, quarterly output audit due) → đây là nghĩa vụ DESIGN-TIME theo lịch từ governance table → xử lý như **Architect action / Internal monitoring routine**, chỉ escalate tiếp nếu phát hiện drift/violation thật.
  - Nguyên tắc thi: gặp câu hỏi dạng "signal X thuộc bucket nào" — đáp án đúng bám vào việc signal đó có breach 1 threshold/agreement cụ thể hay không, có phải trend kéo dài hay 1 lần đơn lẻ, và có nằm trong 1 nghĩa vụ theo lịch đã biết trước hay không — không phải học vẹt 1 bảng cố định.

### B. Documentation cho handoff & audit (handoff phase)
- **Bối cảnh:** feedback loop giữ hệ thống healthy khi CHÍNH BẠN đang vận hành nó. Documentation là thứ giữ hệ thống chạy đúng SAU KHI bạn đi. Lifecycle term: documentation = stage **handoff**. Nguyên tắc gốc: hoặc design mang theo reasoning của nó vào handoff, hoặc reasoning đó biến mất ngay khi người thiết kế rời đi.
- **Một document phải phục vụ 3 reader khác nhau** — chỉ phục vụ 1 reader là document chưa đủ dù chi tiết đến đâu:
  1. **Handoff recipient** (inheriting engineer) — nhận 1 deployment mà họ không tham gia xây dựng.
  2. **Compliance reviewer** (auditor) — đến sau, tìm evidence 1 control cụ thể đang sống và có accountability.
  3. **Returning architect** (thường là chính bạn) — quay lại sau vài tháng, không còn nhớ session thiết kế.
- **Với handoff recipient: rejected alternatives quan trọng ngang decisions made.** Document phải mang: decision đã ra, alternative đã bị reject, và lý do reject mỗi alternative đó. Một design giao đi mà thiếu rejected alternatives thì người không có mặt lúc đó không thể hiểu được — họ sẽ đảo ngược đúng quyết định vì lý do sai, hoặc bảo vệ sai quyết định vì không biết nó đang giải quyết tradeoff nào. Rejected option giải thích TẠI SAO design có hình dạng như vậy.
- **Với compliance reviewer: evidence quan trọng hơn assertion.** Document phải mang: mỗi regulatory obligation, technical control đáp ứng nó, owner của control đó, và evidence artifact chứng minh control đang hoạt động. Đây chính là **control register** (regulated deployment, đã học ở Course 3) được carry forward vào living document quản trị production life của deployment. Reviewer KHÔNG chấp nhận assertion đơn thuần ("control exists" nói ra thôi là chưa đủ) — cần evidence cụ thể.
- **Với returning architect: document phải navigable mà không cần briefing.** Document phải tự đứng vững: decision được **DATED** (ghi ngày), assumption được **LABEL rõ là assumption** (không lẫn vào như fact), open item có owner + resolution criteria. **Practical test:** sau khi đọc document, 1 Architect có năng lực nhưng KHÔNG có mặt lúc design có thể tạo ra 1 SAFE change cho hệ thống không? Nếu không → document chưa complete.
- **Documentation completeness checklist — 6 field, mỗi field có primary reader riêng:**
  1. **Decision** — architectural choice đã chọn, kèm ngày. Primary reader: cả 3.
  2. **Rejected alternatives** — option đã xem xét nhưng không chọn. Primary reader: handoff recipient.
  3. **Tradeoff named** — tradeoff mà decision đó giải quyết (gain, cost, reversal implication). Primary reader: handoff recipient + returning architect.
  4. **Owner** — người/team chịu trách nhiệm cho decision hoặc control đi tới. Primary reader: compliance reviewer + handoff recipient.
  5. **Evidence artifact** — artifact chứng minh 1 control đang thực sự hoạt động. Primary reader: compliance reviewer.
  6. **Audit-ready status** — evidence hiện có đã current và đủ cho review hay chưa. Primary reader: compliance reviewer.
- **Cost · Complexity · Risk:** Cost — viết rationale + evidence lúc design mất thời gian, nhưng reconstruct lại sau này từ email thread (hoặc không reconstruct được) tốn kém hơn — bằng 1 lần reversal sai trong production. Complexity — cái khó là discipline ghi lại TẠI SAO (không chỉ CÁI GÌ) và label rõ assumption là assumption — dễ bị bỏ qua vì reasoning "hiển nhiên" với người đã sống cùng nó. Risk — failure tốn kém nhất là 1 successor đảo ngược 1 load-bearing decision vì rationale chưa từng được ghi lại, tái tạo lại 1 constraint violation mà design gốc đã giải quyết.
- **Case study — "the design rationale that lived in the Architect's head":** postmortem 1 handoff financial-services. Architect gốc thiết kế context strategy CỐ Ý để giữ regulated data in-region — document chỉ mang architecture diagram cho final design, không có rationale. Architect gốc rời đi ở tuần 12 sau launch, không có design session nào được record — document vẫn chỉ có diagram, không rejected alternative, không rationale. Replacement gặp performance issue, đổi context strategy để fix — document không có gì giải thích tại sao strategy gốc được chọn. Việc đổi này vô tình tái tạo lại 1 data-handling pattern VI PHẠM data-residency constraint của deployment. Root cause: diagram cho thấy CÁI GÌ nhưng mất đi TẠI SAO. Replacement hoàn toàn competent, hành động hợp lý với thông tin họ có — nhưng không ai nói cho họ biết strategy đang đổi là LOAD-BEARING cho compliance, nên họ đảo ngược đúng decision vì 1 lý do sai dễ hiểu. Bài học: 1 design thiếu rationale là 1 design không thể thay đổi an toàn — nếu không viết ra, nó rời đi cùng người thiết kế.
- **Checkpoint "place the documentation artifacts"** (plane 2 trục: handoff recipient ↔ compliance reviewer, và documents intention ↔ documents evidence; xếp 6 artifact vào 4 zone) — raw source cũng không có answer key cố định (interactive drag-drop), reasoning để áp dụng:
  - **Architecture diagram** — cho thấy CÁI GÌ (intention/design), nghiêng về phía handoff recipient, nhưng lesson cảnh báo rõ 1 diagram đơn thuần KHÔNG PHẢI rationale → **Handoff · Intention**.
  - **Decision log with rationale** — chứa decision + rejected alternative + tradeoff (TẠI SAO), chủ yếu cho handoff recipient/returning architect; rationale vẫn thuộc "intention" (lý do đằng sau 1 lựa chọn), không phải "evidence 1 control đang live" → **Handoff · Intention**.
  - **Assumption register** — ghi assumption được label rõ (phía intention, constraint chưa confirm), chủ yếu phục vụ handoff/returning architect → **Handoff · Intention** (có thể xem như companion nhẹ hơn cho decision log).
  - **Control register with evidence links** — theo định nghĩa mang obligation → control → owner → evidence artifact → **Compliance · Evidence**.
  - **Test-result summary / eval score** — có thể là evidence 1 control (VD: quality gate) đang hoạt động → **Compliance · Evidence**, hoặc **Handoff · Evidence** nếu dùng để justify outcome của 1 decision.
  - **Deployment runbook** — document vận hành "cách chạy/vận hành hệ thống", gần intention/procedure hơn evidence, chủ yếu phục vụ handoff recipient/returning architect để operate hệ thống → **Handoff · Intention**, dù trong 1 số framing có thể mang evidence về operational readiness cho compliance.
  - Nguyên tắc thi: câu hỏi dạng "artifact X thuộc zone nào" — bám vào 2 câu hỏi: (1) artifact này chủ yếu giúp NGƯỜI KẾ NHIỆM hiểu design, hay giúp AUDITOR xác nhận control đang chạy? (2) artifact này ghi lại Ý ĐỊNH/lý do, hay BẰNG CHỨNG cụ thể? — không học vẹt 1 lưới cố định.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Route theo signal threshold (governance table mặc định) | Signal có threshold rõ, trace được về nguồn (UX/business criticality/eval criteria) | Cần công đặt threshold đúng ngay từ đầu, effort liên tục để triage | Threshold sai (quá lỏng/quá chặt) → bỏ lọt drift chậm (như case study) hoặc alert fatigue | Trung bình — chỉ cần tune lại threshold + rule trong governance table |
| Route theo lịch cố định (regulated review) | Deployment bị regulate, cần proof định kỳ bất kể score (VD: healthcare audit, data-residency confirmation) | Chi phí cố định lặp lại theo lịch, không phụ thuộc có sự cố hay không | Nếu chỉ dựa threshold mà bỏ review theo lịch → vi phạm nghĩa vụ compliance dù hệ thống "trông vẫn ổn" | Cao — nếu không build từ design-time, dựng lại checkpoint theo lịch sau này tốn nhiều hơn, đặc biệt khi bị hỏi proof ngược |
| Build governance table TRƯỚC launch | Mặc định cho mọi production deployment — biến policy thành operating routine | Thời gian định nghĩa signal/trigger/owner/action trước khi có dữ liệu thực | Nếu bỏ qua: observability có signal nhưng không ai quyết signal đó quan trọng (chính là root cause case study 90 ngày) | Cao — thêm governance table sau khi đã có incident phải vừa vá lỗ hổng vừa giải trình vì sao chưa có |
| Chỉ dựng observability stack, coi đó là feedback loop | Sai lầm phổ biến cần tránh — KHÔNG nên chọn, chỉ liệt kê để đối chiếu | Rẻ hơn trước mắt (không cần thêm governance layer) | Rủi ro cao nhất trong lesson: drift chậm không vượt threshold cứng → vô hình nhiều tuần, phát hiện trễ (7 tuần trong case study) | Rất cao — phải audit lại toàn bộ lịch sử alert/score để tìm điểm drift bắt đầu, rồi mới thêm được governance rule |
| Ghi rationale + rejected alternatives ngay lúc quyết định (decision log) | Mặc định cho mọi architectural decision, đặc biệt decision load-bearing cho compliance/constraint | Thời gian viết thêm lúc đang thiết kế, cảm giác "dư thừa" vì đang nhớ rõ | Nếu bỏ qua: reasoning chỉ tồn tại "trong đầu" Architect, mất khi người đó rời đi (case study financial-services) | Rất cao — không thể phục dựng rationale đã mất; chỉ phát hiện khi đã reverse sai decision trong production |
| Chỉ giữ architecture diagram cuối cùng, không ghi rejected alternative | Diagram đơn thuần đủ nếu hệ thống sẽ không bao giờ đổi tay — thực tế KHÔNG khuyến nghị | Rẻ hơn trước mắt, ít việc viết lách | Successor không phân biệt được decision nào load-bearing vs. tuỳ chọn → dễ đảo ngược sai (đúng case study C4.3) | Cao — phải điều tra lại toàn bộ lý do thiết kế sau khi đã xảy ra sự cố, thường là sau khi vi phạm đã xảy ra |
| Viết control register carry-forward từ Course 3 vào living document | Deployment có regulatory obligation cần audit — compliance reviewer sẽ cần evidence, không phải assertion | Duy trì evidence artifact liên tục cập nhật theo mỗi control | Nếu chỉ ghi "control exists" mà không có evidence artifact → reviewer reject, coi như chưa chứng minh được | Trung bình-cao — phải backfill evidence artifact cho từng control đã tồn tại, tốn công hơn nếu để dồn |

**Ghi chú:** 3 dòng đầu + dòng 4 thuộc Phần A (feedback loop/governance), 3 dòng cuối thuộc Phần B (documentation/handoff).

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Feedback loop | Decision layer nằm trên observability stack — quyết định signal nào quan trọng, cần escalate, và phải làm gì tiếp theo |
| Observability stack | Hạ tầng thu thập raw signal (latency, error rate, eval score, usage pattern) — chỉ đo, KHÔNG tự quyết định gì |
| 5-step loop (Signals → Triage → Decide → Act → Review) | Quy trình xử lý signal thành hành động cụ thể trong feedback loop |
| Control room analogy | Ví dụ nhà ga: sensor chỉ đo được, phải có người (judgment layer) quyết định delay có đáng thông báo/đổi lịch không |
| SLA (Service Level Agreement) | Cam kết nêu rõ 3 thứ: đo gì, breach là gì, điều gì xảy ra khi breach |
| Threshold traceability | Nguyên tắc: mọi threshold phải trace về nguồn cụ thể (UX expectation, business criticality, eval criteria), không đặt tùy ý |
| Governance table | Bảng map signal → trigger → Architect action → regulatory checkpoint, phải tồn tại trước launch |
| Production-signal governance table | Governance table cụ thể với 4 signal type: output quality, latency p95, cost per interaction, data-residency |
| Design-time obligation | Nghĩa vụ (VD: scheduled review theo lịch) phải build từ lúc thiết kế, không phải thêm sau khi bị hỏi proof |
| Quality drift | Suy giảm chất lượng output diễn ra từ từ, không kèm hard failure, nên dễ không bị alert bắt được |
| Decision layer | Phần "phán đoán" biến observability (chỉ đo) thành feedback loop (biết phải làm gì) |
| Documentation (handoff stage) | Tài liệu giữ hệ thống chạy đúng SAU KHI Architect gốc rời đi — lifecycle stage kế tiếp feedback loop |
| 3 audience của documentation | Handoff recipient (inheriting engineer), compliance reviewer (auditor), returning architect |
| Rejected alternatives | Các option đã xem xét nhưng không chọn, kèm lý do — quan trọng ngang decisions made cho handoff recipient |
| Control register | Bảng obligation → control → owner → evidence artifact (carry forward từ Course 3), phục vụ compliance reviewer |
| Evidence vs. assertion | Nguyên tắc compliance reviewer: cần evidence artifact cụ thể, "control exists" nói ra thôi chưa đủ |
| Documentation completeness checklist | 6 field: decision, rejected alternatives, tradeoff named, owner, evidence artifact, audit-ready status |
| Assumption labeling | Nguyên tắc: assumption phải được ghi rõ là assumption, không lẫn vào như fact, để returning architect không hiểu nhầm |
| Load-bearing decision | Decision mà nếu đảo ngược sẽ phá vỡ 1 constraint quan trọng (VD: data-residency) — phải được đánh dấu rõ trong rationale |
| Practical completeness test | Sau khi đọc document, 1 Architect không có mặt lúc design có tạo được 1 safe change không? Nếu không → chưa complete |

**Ghi chú:** term từ dòng 1-11 thuộc Phần A (feedback loop), dòng 12-20 thuộc Phần B (documentation).

## Gotchas / bẫy hay gặp
- [ ] Xây observability stack chỉn chu (dashboard, alert) rồi coi như "stakeholder feedback đã covered" — monitoring KHÔNG PHẢI feedback loop, thiếu governance rule map signal → trigger → owner → action
- [ ] Chỉ set alert theo hard threshold (error rate), bỏ qua slow drift không vượt threshold cứng — drift 4-7 tuần trong case study không alert vì error rate flat, dù eval score đã drift từ tuần 4
- [ ] Đặt threshold SLA tùy ý ("nghe hợp lý") thay vì trace về UX expectation / business criticality / eval criteria — threshold không defensible khi bị hỏi lại
- [ ] Không chuẩn bị consumption forecast + spend-control posture trước launch — cost vỡ trận khi production volume gấp 10-100x POC, biết được narrative này TRƯỚC hoá đơn đầu, không phải sau
- [ ] Coi regulated review checkpoint là việc "thêm sau nếu cần" thay vì design-time obligation — dựng lại sau khi bị audit hỏi proof tốn kém hơn nhiều
- [ ] Giao handoff chỉ kèm architecture diagram cuối cùng, không có rejected alternatives/rationale — successor không phân biệt được decision nào load-bearing, dễ đảo ngược sai (case study data-residency)
- [ ] Ghi control "exists" như 1 assertion, không kèm evidence artifact cụ thể — compliance reviewer không chấp nhận assertion đơn thuần
- [ ] Nhúng assumption vào document như thể nó là fact đã confirm, không label rõ "assumption" — returning architect hiểu nhầm, ra quyết định sai trên 1 giả định chưa kiểm chứng

## Exam tips
- Câu hỏi dạng "hệ thống có dashboard/alert đầy đủ, vẫn miss 1 vấn đề kéo dài nhiều tuần" → đáp án khả năng cao là THIẾU governance rule map signal → trigger (monitoring ≠ feedback loop), không phải do thiếu metric.
- Câu hỏi về threshold SLA "tại sao chọn số X" → đáp án đúng phải trace về 1 trong 3 nguồn: UX expectation (latency), business criticality (availability), eval acceptance criteria (quality) — nếu answer choice không nêu được nguồn thì loại.
- Câu hỏi về cost sau launch → nhớ đúng magnitude: production volume gấp 10-100x (1-2 order of magnitude) so với POC, và hành động đúng là forecast + spend-control posture TRƯỚC khi launch.
- Câu hỏi dạng "handoff chỉ có diagram, sau đó xảy ra vi phạm compliance" → đáp án đúng là thiếu rejected alternatives/rationale (decision log), không phải do successor thiếu năng lực.
- Phân biệt 2 nhóm document theo 2 trục (handoff vs. compliance) và (intention vs. evidence) — control register luôn rơi vào Compliance·Evidence, decision log luôn rơi vào Handoff·Intention, dù cả 2 đều "quan trọng".

## Code / config snippets
```python
# Minh hoạ 1 dòng trong PRODUCTION-SIGNAL GOVERNANCE TABLE (Phần A)
# Dùng để map mỗi signal -> trigger -> owner -> action, phải làm TRƯỚC launch
governance_row = {
    "signal": "output_quality_eval_score",       # loại signal đang theo dõi
    "trigger": "score_below_eval_suite_threshold",  # điều kiện kích hoạt review (trace về eval criteria)
    "owner": "architect_on_call",                # ai chịu trách nhiệm phản ứng khi trigger nổ ra
    "action": "diagnose_prompt_vs_data_vs_model_drift",  # hành động cụ thể: chẩn đoán rồi quyết định iterate/re-architect
    "regulated_checkpoint": "periodic_output_audit",  # checkpoint chạy theo lịch, độc lập với score (regulated deployment)
}

# Minh hoạ 1 entry trong decision log (Phần B) - phục vụ handoff recipient + compliance reviewer
decision_log_entry = {
    "decision": "keep_regulated_data_in_region_via_context_strategy",  # quyết định đã chọn
    "date": "2026-01-15",                         # luôn DATE decision để returning architect biết mốc thời gian
    "rejected_alternatives": [
        "cross_region_context_caching_for_lower_latency",  # option bị loại, kèm lý do bên dưới
    ],
    "tradeoff_named": "latency_gain_vs_data_residency_violation_risk",  # tradeoff mà decision này giải quyết
    "owner": "architect_of_record",                # người chịu trách nhiệm cho decision này
    "evidence_artifact": "residency_config_audit_log_2026Q1",  # bằng chứng cụ thể, không phải assertion suông
    "audit_ready": True,                           # evidence hiện tại đã đủ mới/đủ cho compliance review chưa
}
```

## Câu hỏi chưa rõ
- ?
