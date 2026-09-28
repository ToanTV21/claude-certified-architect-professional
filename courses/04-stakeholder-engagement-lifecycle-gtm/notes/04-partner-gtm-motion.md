# C4.4 — Partner go-to-market: demo, objection handling, joint scoping

> **Course:** 4 — Stakeholder Engagement, Lifecycle & GTM (178 min) · **Exam domain:** D6 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Lead the Architect's role in a partner go-to-market motion through discovery, a scenario-based demo, technical objection handling, and joint scoping with the Anthropic Applied AI team, so an enterprise opportunity does not stall on questions only you can answer

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
⚠️ Partner Track — nội dung này KHÔNG nằm trong phạm vi thi CCAR-P chính thức, nhưng vẫn được course dạy đầy đủ nên ghi lại để tham khảo.

- **Demo design là 1 kỹ năng riêng, không phải "làm demo cho xong"**: discovery làm tốt (team align được problem/use-case/value) nhưng nếu demo yếu thì có thể phá hỏng toàn bộ thành quả đó. Kịch bản hay gặp: demo mở đầu bằng feature "đẹp nhưng generic" thay vì world của buyer → phản ứng lịch sự kiểu "interesting but not quite what we envisioned" → buyer bắt đầu nghi ngờ liệu team có thật sự hiểu core problem của họ không.
- **Phân biệt 2 loại demo — nhầm lẫn 2 job này là root cause của demo yếu:**
  - **Capabilities demo**: trả lời câu "hệ thống này làm được gì?" (what CAN this system do) — mang tính giới thiệu chung, tạo **interest**.
  - **Scenario-specific demo**: trả lời câu "hệ thống này làm gì với vấn đề CỦA TÔI, workflow CỦA TÔI, constraint CỦA TÔI?" — chỉ loại này mới tạo ra **confidence** thật sự cho buyer.
  - Nói cách khác: capabilities demo gây tò mò, nhưng chỉ scenario-specific demo mới khiến buyer tin là "họ hiểu đúng bài toán của mình".
- **4 quyết định thiết kế demo phải chốt TRƯỚC khi build bất kỳ screen nào:**
  1. **Scenario selection** — chọn 1 workflow mà buyer nhận ra ngay từ chính operations của họ (đúng data shape, đúng approval step, đúng edge case họ hay gặp), tránh document task/query flow generic. Lý do: buyer tin vào cái gì họ thấy "quen" hơn là 1 feature tour làm đẹp nhưng xa lạ — recognition thường có sức thuyết phục hơn polish.
  2. **Limit placement** — quyết định trước 1-2 limitation nào demo sẽ chủ động nêu ra, và frame nó như 1 scope boundary có chủ đích (nói rõ hệ thống KHÔNG làm gì và tại sao). Lý do: nếu buyer tự phát hiện ra limitation giữa demo, confidence sẽ giảm; còn nếu Architect nêu limitation sớm, nó lại đọc như sự honesty/discipline. Trong regulated setting, việc chủ động disclose boundary từ đầu thường là 1 **positive signal**, không phải điểm yếu.
  3. **Sales team collaboration** — cùng sales team dựng narrative của demo trước khi build bất cứ thứ gì: sales biết buyer đã raise câu hỏi gì trước đó, Architect biết hệ thống thực tế show được gì dưới production condition. Lý do: demo thiếu input từ sales có thể trả lời câu hỏi mà buyer chưa từng hỏi; demo thiếu Architect thì dễ overpromise — cả hai đều làm mất credibility và làm chậm deal.
  4. **Data preparation** — dùng data giống buyer về structure/volume; với buyer thuộc regulated industry thì dùng anonymized data nhưng vẫn giữ đúng structural constraint như môi trường thật. Lý do: buyer đánh giá demo qua chính data hiển thị trong đó — field name/pattern thực tế khiến scenario "tự nó thuyết phục" (argues for itself).
- **Limit placement xứng đáng được nhấn mạnh riêng** vì nó đi NGƯỢC instinct tự nhiên: nêu ra 1 weakness cảm giác rủi ro, nên có xu hướng muốn giấu/làm nhẹ đi — nhưng cách này thường backfire. Tình huống điển hình: buyer hỏi "hệ thống này không handle tốt cái gì?" — trả lời vague thì confidence giảm ngay; trả lời rõ ràng/có scope thì buyer thấy đó là discipline, không phải defensiveness. Cần chuẩn bị trước với **3 câu hỏi**:
  1. Limit đó cụ thể là gì?
  2. Vì sao limit đó tồn tại?
  3. Điều gì xảy ra nếu use case của buyer cần vượt qua limit đó?
  Việc này càng quan trọng hơn trong regulated industry (healthcare, financial services, public sector) — 1 boundary rõ ràng tín hiệu là rigor, còn deflection (né tránh) tín hiệu là risk.
- **Joint scoping với Applied AI team (Anthropic) — thành công bắt đầu TRƯỚC khi session diễn ra**, không phải trong lúc họp. Cùng discipline như demo: session scoping tốt không phải là nơi để "figure out basics lần đầu tiên" mà là nơi refine choice đã có, test assumption, và resolve câu hỏi cần chuyên môn specialist. Nếu demo chứng minh Architect hiểu đúng problem của buyer, thì scoping session chứng minh Architect sẵn sàng để shape ra 1 solution đáng tin. Cần mang theo **3 thứ chuẩn bị sẵn**:
  1. **Documented requirements/constraints** từ discovery — use case, workflow, stakeholder, data condition, technical environment, compliance concern, success criteria — để session có 1 điểm bắt đầu chung (shared starting point), không mất thời gian recap từ đầu.
  2. **Proposed pattern (hoặc vài candidate pattern) kèm trade-off đã được name rõ** — đi vào session với 1 point of view sẵn, chỉ ra option khả thi, mỗi option gain/give up gì, risk nằm ở đâu.
  3. **Danh sách câu hỏi mở** mà Applied AI team là bên phù hợp nhất để trả lời — model behavior, architecture implication, scaling constraint, evaluation approach, safety consideration, pattern fit.
  Ý chính: demo giúp earn trust bằng cách identify limitation rõ ràng; joint scoping giữ được trust đó bằng cách mang theo 1 structured view về problem/option/open question, không đến tay trắng.
- **3 loại objection, mỗi loại cần cách trả lời khác nhau:**
  1. **Capability objection** — buyer hỏi liệu hệ thống có làm được việc đó hay không (feasibility thuần kỹ thuật).
  2. **Governance/compliance objection** — buyer hỏi liệu deployment có thể được trust/control/evidence theo cách họ có thể defend trước leadership/regulator của họ.
  3. **Design-choice objection** — buyer hỏi tại sao chọn phương án này chứ không phải phương án khác. Loại này cần NHIỀU hơn 1 lời giải thích/justification đơn thuần — phải giải thích rõ trade-off mà lựa chọn đó tạo ra và alternative sẽ tốn gì, dùng lại đúng structure translation đã dùng khi present trade-off (gain / give up / reversal cost) — nghĩa là lesson C4.2 và objection handling ở đây liên kết trực tiếp với nhau về kỹ thuật trình bày.
- **Go-to-market engagement map nên coi demo design là 1 workstream có tracked deliverable** (Partner Track): 1 cột "demo-design" với các deliverable rõ ràng — scenario đã chọn, limitation đã identify, data source đã confirm, sales-team sign-off. Việc này quan trọng nhất khi partner chạy nhiều opportunity song song, hoặc khi Architect handoff giữa cycle — continuity của deal phụ thuộc vào những gì đã được document lại, không phụ thuộc vào ký ức của 1 người.
- **Cost · Complexity · Risk của toàn bộ motion này:** chuẩn bị tradeoff presentation + scenario-specific demo tốn thời gian Architect thật, nhưng rẻ hơn nhiều so với 1 opportunity bị stall hoặc 1 approval bị rút lại. Complexity nằm ở 3 kỹ năng riêng biệt cần luyện (demo design, limit placement, joint scoping prep), trong đó 2 cái đi ngược instinct tự nhiên (naming reversal cost, nêu limit rõ ràng). Risk lớn nhất vẫn là **false alignment** — buổi họp cảm giác như đã approved, nhưng có yếu tố (ví dụ reversal cost, hoặc 1 limitation quan trọng) chưa được nói rõ, và hậu quả chỉ lộ ra sau đó.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Capabilities demo | Giai đoạn đầu tạo awareness, buyer chưa xác định rõ use case cụ thể, hoặc audience là nhiều buyer khác nhau cùng lúc | Thấp — build 1 lần, dùng lại nhiều nơi, không cần data/scenario riêng cho từng buyer | Chỉ tạo interest, không tạo confidence; nếu dùng sai lúc (buyer đã qua discovery, mong đợi thấy problem của họ) sẽ đọc như "generic feature tour" và làm buyer nghi ngờ team hiểu đúng bài toán không | Thấp — không gắn với 1 buyer cụ thể nên dễ bỏ, không ảnh hưởng deal |
| Scenario-specific demo | Sau discovery, buyer đã align về use case/value — cần tạo confidence để tiến sang joint scoping/approval | Cao hơn — cần data resembling buyer, cần sales-team collaboration trước khi build, cần chọn đúng scenario | Nếu chọn sai scenario (không match đúng workflow buyer nhận ra) thì tốn effort mà vẫn không tạo confidence, coi như phải làm lại | Trung bình-cao — build lại theo đúng scenario khác, mất thời gian + có thể trễ deal cycle |
| Named-limit-upfront (chủ động nêu 1-2 limitation trong demo) | Hầu hết trường hợp, đặc biệt regulated industry (healthcare, financial services, public sector) | Thấp — chỉ cần chuẩn bị trước 3 câu hỏi (limit là gì / vì sao / nếu vượt thì sao), không cần thay đổi kỹ thuật | Rủi ro thấp — đọc như discipline/honesty, giúp giữ trust; rủi ro duy nhất là chọn nêu limit không đúng trọng tâm buyer quan tâm | Thấp — chỉ là cách frame trong lúc present, không ảnh hưởng kiến trúc |
| Hide-the-limit (để buyer tự phát hiện limitation) | Hầu như không nên chọn — chỉ có thể "hợp lý hoá" khi thực sự chưa xác định được limitation nào đáng nói (rất hiếm) | Thấp trước mắt (không cần chuẩn bị) | Cao — nếu buyer tự phát hiện giữa demo, confidence giảm ngay; trong regulated setting còn đọc như deflection = tín hiệu risk, có thể chặn cả joint scoping tiếp theo | Cao — phải rebuild lại trust đã mất, thường cần 1 buổi làm rõ lại riêng, tốn thời gian deal cycle |
| Chuẩn bị đủ 3 thứ trước joint scoping (requirements/pattern+trade-off/open questions) | Luôn nên làm — đây là default trước mọi joint scoping session với Applied AI team | Cao hơn trước session — cần document lại discovery, tự đề xuất pattern, tự liệt kê open question | Thấp — session tập trung refine/resolve, không lãng phí thời gian Applied AI team vào việc "dựng lại basics" | Thấp — nếu thiếu 1 phần vẫn có thể bổ sung ngay trong session mà không mất nhiều |
| Vào session "figure out basics" (không chuẩn bị trước) | Không nên chọn — chỉ xảy ra khi Architect chưa kịp làm discovery đầy đủ | Thấp trước mắt (không tốn effort chuẩn bị) | Cao — mất trust vừa earn được từ demo, Applied AI team phải dành thời gian dựng lại context thay vì đóng góp chuyên môn, session kém hiệu quả | Cao — phải xin lại 1 session khác sau khi chuẩn bị đầy đủ, kéo dài deal cycle |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Capabilities demo | Demo trả lời "hệ thống làm được gì" — tạo interest, mang tính giới thiệu chung, không gắn vào problem cụ thể của buyer |
| Scenario-specific demo | Demo trả lời "hệ thống làm gì với vấn đề CỦA buyer" — tạo confidence, dựa trên workflow/data/constraint thật của buyer |
| Limit placement | Quyết định chủ động trước demo về 1-2 limitation sẽ được nêu ra và cách frame nó như 1 scope boundary có chủ đích |
| Scenario selection | 1 trong 4 quyết định thiết kế demo — chọn workflow buyer nhận ra ngay từ operations của họ, tránh generic task |
| Sales team collaboration (demo design) | Cùng sales dựng narrative demo trước khi build, để tránh trả lời câu hỏi buyer chưa hỏi hoặc overpromise |
| Data preparation (demo design) | Dùng data giống buyer về structure/volume (hoặc anonymized nếu regulated) để scenario "tự thuyết phục" |
| Joint scoping | Buổi làm việc chung giữa Architect và Anthropic Applied AI team để refine pattern/trade-off/resolve specialist question |
| Applied AI team | Team chuyên môn của Anthropic hỗ trợ scoping kỹ thuật sâu (model behavior, scaling, evaluation, safety) trong partner motion |
| Capability objection | Loại objection hỏi hệ thống có làm được việc đó hay không (feasibility) |
| Governance/compliance objection | Loại objection hỏi deployment có thể trust/control/evidence theo cách buyer defend được với leadership/regulator |
| Design-choice objection | Loại objection hỏi vì sao chọn phương án này — cần trả lời bằng translation structure (gain/give up/reversal cost) như khi present trade-off |
| Go-to-market engagement map | Bản theo dõi các workstream của 1 GTM motion; demo design nên là 1 cột riêng có deliverable rõ (scenario/limitation/data source/sales sign-off) |
| False alignment | Rủi ro lớn nhất của cả motion — buổi họp cảm giác approved nhưng có yếu tố quan trọng chưa được nói rõ, hậu quả lộ ra sau |

## Gotchas / bẫy hay gặp
- [ ] Nhầm capabilities demo với scenario-specific demo — show "hệ thống làm được gì nói chung" trong khi buyer đã qua discovery và mong đợi thấy chính problem của họ
- [ ] Không chốt 4 quyết định thiết kế demo (scenario/limit/sales collaboration/data) TRƯỚC khi build screen — dẫn tới demo lệch hướng, phải build lại
- [ ] Cố tình giấu/làm nhẹ limitation vì sợ mất điểm — thực tế backfire nặng hơn, đặc biệt khi buyer tự phát hiện ra giữa demo hoặc trong regulated industry
- [ ] Build demo mà không sync với sales team trước — dễ trả lời câu hỏi buyer chưa từng hỏi, hoặc overpromise những gì hệ thống chưa show được dưới production condition
- [ ] Dùng data quá abstract/không giống buyer (sai structure, sai volume) khiến scenario không "tự thuyết phục" được buyer
- [ ] Vào joint scoping session mà chưa document requirements/chưa có proposed pattern/chưa có open question list — biến session thành nơi "dựng basics" thay vì refine
- [ ] Trả lời design-choice objection chỉ bằng justification đơn thuần ("tôi chọn vậy vì tốt hơn") mà không nêu rõ trade-off + cost của alternative — buyer không có đủ thông tin để defend lựa chọn đó với leadership của họ
- [ ] Không track demo-design workstream trong GTM engagement map — khi Architect handoff giữa cycle, người sau không biết scenario/limitation nào đã được confirm, mất continuity

## Exam tips
- Phần này thuộc Partner Track, khả năng xuất hiện trong đề CCAR-P chính thức là THẤP (course tự đánh dấu "not tested by exam") — không cần học sâu cho mục đích thi, ưu tiên thời gian cho C4.2 (trade-off framing) vì đó là phần chắc chắn thuộc D6.
- Nếu vẫn gặp câu hỏi liên quan demo/GTM trong đề, áp nguyên tắc chung: ưu tiên phương án nào tạo "informed confidence" cho buyer hơn là phương án tạo ấn tượng bề ngoài — tức là chọn scenario-specific/named-limit-upfront thay vì capabilities-demo-chung/hide-the-limit.
- Nếu câu hỏi hỏi về cách trả lời 1 objection dạng "vì sao anh chọn X mà không chọn Y" (design-choice objection) — liên kết lại với kỹ thuật translation structure (gain/give up/reversal cost) của C4.2, vì đó là phần chắc chắn nằm trong exam.

## Code / config snippets
```python
# Minh hoạ cấu trúc "demo design plan" theo 4 quyết định thiết kế demo
# (scenario selection / limit placement / sales collaboration / data preparation)
# và 1 hàm kiểm tra plan còn thiếu field nào trước khi bắt đầu build demo.

# Mỗi demo cho 1 buyer nên có 1 plan như dict dưới đây,
# thay vì build screen trực tiếp mà chưa chốt các quyết định.
demo_design_plan = {
    "scenario": "Xử lý claim bảo hiểm auto — đúng workflow buyer đang làm tay",  # scenario selection: workflow buyer nhận ra ngay
    "named_limitations": [
        "Không tự động approve claim > $10,000 — cần human review",  # limit placement: nêu chủ động, không để buyer tự phát hiện
    ],
    "data_source": "anonymized_claims_sample_v2",  # data preparation: giống structure/volume thật, đã anonymize vì buyer thuộc regulated industry
    "sales_signoff": True,  # sales team collaboration: đã review narrative cùng sales trước khi build
}

def check_demo_plan_ready(plan: dict) -> list[str]:
    """
    Kiểm tra demo_design_plan đã đủ 4 field bắt buộc chưa,
    trả về danh sách field còn thiếu (rỗng = plan đã sẵn sàng để build demo).
    Dùng như 1 gate đơn giản trước khi cho phép bắt đầu build screen.
    """
    required_fields = ["scenario", "named_limitations", "data_source", "sales_signoff"]
    missing = []
    for field in required_fields:
        value = plan.get(field)
        # coi field là "thiếu" nếu không tồn tại, rỗng, hoặc sales_signoff chưa = True
        if value in (None, "", []) or (field == "sales_signoff" and value is not True):
            missing.append(field)
    return missing


if __name__ == "__main__":
    missing_fields = check_demo_plan_ready(demo_design_plan)
    if missing_fields:
        print(f"Chưa sẵn sàng build demo, còn thiếu: {missing_fields}")
    else:
        print("Demo design plan đầy đủ 4 quyết định — có thể bắt đầu build demo.")
```

## Câu hỏi chưa rõ
- ?
