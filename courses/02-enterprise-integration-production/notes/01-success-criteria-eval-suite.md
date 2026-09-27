# C2.1 — Success criteria & eval suite trước khi code

> **Course:** 2 — Enterprise Integration & Production (158 min) · **Exam domain:** D4 (16%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Define success criteria and build an eval suite before writing the first line of production code, distinguishing model-based from code-based evals, selecting eval workflow stages, and using evals as the gating mechanism for any change to a production system

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- Module 1 cho ra **architecture decision** (pattern, integration point, cách hệ thống phản ứng với input) nhưng chưa chứng minh được các quyết định đó có "đứng vững" với input thật + user khó đoán. **Eval** (evaluation) là structured test để kiểm chứng behavior của hệ thống trước khi lên production hoặc sau model update — phát hiện vấn đề trước khi user gặp phải.
- **Evals before code, không phải sau:** cách làm phổ biến nhưng không tốt là build trước, test sau (QA step). Viết eval suite **trước** production code buộc 3 việc phải xảy ra: (1) phát biểu success bằng con số đo được, (2) lộ design assumption sớm lúc còn rẻ để sửa, (3) tạo ra một **gate** để biết model swap / prompt change / retrieval strategy mới có cải thiện hệ thống hay không. Nếu không viết được eval cho 1 behavior → không có cách nào đo được behavior đó có tồn tại, mọi thay đổi sau này không verify được.
- **Eval workflow — 5 stage tuần tự, mỗi stage ra 1 artifact feed cho stage sau:**
  1. **Define the task** — phát biểu behavior cụ thể + đo được, viết prompt test → task spec + pass criteria. Định nghĩa mơ hồ → eval mơ hồ.
  2. **Build golden dataset** — gom input hệ thống sẽ gặp, gồm edge case + counterexample → labeled dataset. Dataset không representative → score không có ý nghĩa.
  3. **Run automated checks** — so output với expected, dùng cho behavior rõ ràng (format compliance, schema validation, factual lookup) → pass/fail per item. Rẻ, nhanh.
  4. **Score with a judge** — behavior cần "diễn giải" (tone, reasoning accuracy, edge-case appropriateness) dùng model-based judge chấm ở scale → score + reasoning per item.
  5. **Interpret and act** — tổng hợp score biết hệ thống đang ở đâu, thay đổi có đúng hướng không. Lưu ý: mean score tăng nhưng edge case/adversarial input âm thầm tệ đi ≠ hệ thống tốt hơn.
- **3 loại eval — đánh đổi speed vs. flexibility:**
  - **Code-based**: hàm check tự động (schema validation, regex, JSON parse, length, assert với authoritative data). Chạy ms, gần như free. Không đánh giá được thứ cần judgment (tone, helpfulness, reasoning quality).
  - **Model-based (LLM-as-judge)**: judge model nhận prompt gốc + output + scoring rubric, trả score + reasoning. Judge prompt cũng phải được engineer + test như 1 prompt thật. Cost trung bình–cao (1 API call/item, theo per-token rate của judge model). Giới hạn: judge có thể inconsistent ở borderline case — nếu không ép judge sinh ra reasoning kèm score thì khó phát hiện inconsistency đó.
  - **Human-review**: người chấm theo rubric (structured scoring sheet hoặc unstructured annotation). Dùng cho behavior high-stakes/novel mà cả code lẫn judge chưa tin được: safety-critical edge case, capability area mới chưa có rubric, hoặc output mà đánh giá sai gây rủi ro lớn. Cũng dùng để **calibrate/validate model-based eval**. Cost rất cao, không scale, và người chấm cũng có inconsistency riêng.
- **Grading ladder** — luôn thử phương án rẻ nhất/đáng tin nhất trước, chỉ leo thang khi behavior đòi hỏi:
  1. Code-based grading bất cứ khi nào behavior cho phép — deterministic, không drift.
  2. LLM-as-judge khi cần interpretation — làm rigorous bằng: rubric chi tiết, **constrained verdict** (tập nhãn cố định nhỏ thay vì free-form score), **calibration** với human-labeled example, và **chấm bằng model khác** với model đang được đánh giá để tránh self-preference.
  3. Human grading là last resort — cho behavior high-stakes/novel mà code lẫn calibrated judge đều chưa tin được.
- **Judge calibration — bước nhiều team bỏ qua:** LLM judge tự nó cũng là 1 system có thể sai. Phải chạy judge trên tập human-labeled, xác nhận độ khớp với human judgment đủ cao mới tin. Judge chưa calibrate cho ra score "tự tin" nhưng chưa chắc chất lượng — **tệ hơn cả không có automated grade**, vì tạo cảm giác đáng tin cậy giả. Ưu tiên **volume over perfection**: nhiều case chấm tự động rẻ, coverage rộng bắt được nhiều regression hơn 1 tập nhỏ chấm tay kỹ, và chạy được trên mọi thay đổi.
- **Định nghĩa success criteria — biến business requirement thành ngưỡng đo được**, ví dụ "summarize claims accurately" không đo được, cần đi qua 4 bước:
  1. **Identify behavior cụ thể**: "extract filer's name, claim number, incident date, claimed amount from each document"
  2. **Set threshold**: từ business requirement quyết định pass/fail (VD: 100% accuracy trên structured field, <2% hallucination rate, 99.5% đúng schema) — threshold phải đến từ business requirement, không phải từ việc "prototype đầu tiên đạt được bao nhiêu thì lấy bấy nhiêu". Xem thêm platform.claude.com/docs/en/test-and-evaluate/develop-tests.
  3. **Identify failure mode**: mỗi failure mode (fake claim number, missing incident date, value từ claim sai) là 1 category trong eval dataset
  4. **Include adversarial input**: document thiếu field, viết tay, format lạ, layout không chuẩn — golden dataset chỉ có input sạch thì eval score không dự đoán được production performance
- **Evals là gating mechanism cho mọi thay đổi**: model swap, prompt revision, context strategy change, retrieval config update — đều phải chạy qua eval suite trong lúc dev trước khi lên production. Đây là cách duy nhất biết thay đổi có cải thiện hệ thống hay không.
- **Multi-turn eval** là category riêng — chấm cả conversation thay vì 1 prompt-response đơn: hệ thống có giữ đúng context qua các turn, trả lời follow-up không bịa chi tiết chưa từng nói trước đó, chất lượng output có giữ được khi conversation dài ra. Vì unit được chấm là cả conversation nên cần **golden dataset riêng** gồm full transcript với known-good response ở mỗi turn, phủ follow-up, topic shift, độ dài conversation mà hệ thống sẽ gặp ở production.
- **Case study cảnh báo** (document summarization workflow): team sửa summarization prompt nhưng **không update eval suite** đi kèm → eval pass hết các check bắt buộc. 2 ngày sau khi deploy, field report cho thấy câu pháp lý nhiều mệnh đề bị cắt cụt trong summary. Root cause: eval set được viết **trước** prompt change, không còn match behavior mới → false confidence. Bài học: chạy eval trước mọi thay đổi, và eval set phải luôn cập nhật theo hệ thống nó đang đo.
- **Cost · Complexity · Risk:**
  - **Cost**: mỗi model-based eval là 1 API call, đáng lưu ý nhưng không nên để cost kéo dataset nhỏ hơn mức use case cần — rủi ro **under-evaluating** (production-breaking change lọt qua eval suite thiếu) tốn kém hơn nhiều so với vài API call thêm. Size dataset theo mức độ tự tin cần có, coi cost là constraint thứ yếu.
  - **Complexity**: eval infra là 1 hệ thống song song cần maintain — golden dataset phải giữ current, judge prompt phải engineer + test, pass threshold phải revisit khi requirement hệ thống thay đổi. Tham khảo implementation pattern: [claude-cookbooks/building_evals.ipynb](https://github.com/anthropics/claude-cookbooks/blob/main/misc/building_evals.ipynb).
  - **Risk**: eval suite lỗi thời (out-of-date) tạo **false confidence** — tạo cảm giác thay đổi an toàn trong khi check đang đo 1 behavior không còn tồn tại trong hệ thống. Thời điểm rủi ro cao nhất cho regression là khi eval **có tồn tại nhưng outdated**, không phải khi hoàn toàn không có eval.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Code-based eval | Behavior không mơ hồ: format compliance, schema, factual lookup với authoritative data | Rất thấp (ms/check, không API call) | Không đánh giá được behavior cần judgment (tone, reasoning quality) | Rẻ — chỉ là hàm check, sửa/xoá assertion |
| Model-based eval (LLM-as-judge) | Behavior cần interpretation: response quality, instruction following, reasoning, safety, ambiguous input | Trung bình–cao — 1 API call/item theo rate judge model | Judge inconsistent ở borderline case nếu không ép sinh reasoning; cần calibrate, chưa calibrate = false confidence | Trung bình — phải viết lại/tune judge prompt + rubric, re-calibrate |
| Human-review eval | High-stakes/novel behavior mà code và judge model đều chưa tin được; dùng để calibrate judge | Rất cao — human time, không scale | Chậm, tốn, human evaluator cũng có inconsistency riêng | Cao — không thể tự động hoá lại nhanh, phụ thuộc lịch con người |
| Viết eval suite trước code (approach của lesson) | Mặc định cho mọi production system — muốn có gate đo được cho mọi thay đổi sau này | Chi phí thời gian ban đầu để định nghĩa task + build golden dataset | Nếu bỏ qua bước này: không đo được behavior nào, mọi thay đổi sau không verify được | Cao — nếu để dồn tới cuối mới viết eval, phải suy ngược ra threshold/behavior đã build sẵn |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Eval (evaluation) | Structured test kiểm tra hệ thống trả về output đúng/mong đợi, chạy trước production hoặc sau model update |
| Golden dataset | Tập input đại diện (kèm expected output) mà eval chạy trên đó, phải phủ cả edge case + adversarial input |
| Code-based eval | Check bằng hàm/deterministic logic (schema, regex, assert) |
| Model-based eval / LLM-as-judge | Dùng model khác chấm output theo rubric, trả score + reasoning |
| Human-review eval | Người chấm theo rubric, dùng cho high-stakes/novel behavior |
| Judge calibration | Kiểm chứng độ khớp của judge model với human-labeled data trước khi tin verdict của nó |
| Constrained verdict | Judge trả về 1 trong tập nhãn cố định nhỏ, thay vì free-form score, để giảm inconsistency |
| Gating mechanism | Cơ chế dùng eval suite làm điều kiện bắt buộc trước khi 1 thay đổi được đưa lên production |
| Multi-turn eval | Eval chấm trên toàn bộ conversation (giữ context, không bịa, chất lượng ổn định qua nhiều turn) thay vì 1 prompt-response |
| Failure mode | Một dạng cụ thể của việc hệ thống trả sai (VD: fake claim number, missing field) — mỗi failure mode là 1 category trong golden dataset |

## Gotchas / bẫy hay gặp
- [ ] Viết eval **sau** khi code xong (QA step) thay vì trước — mất luôn cơ hội expose design assumption sớm và không có gate đáng tin
- [ ] Mean score tăng nhưng edge case/adversarial input âm thầm tệ đi — vẫn coi là "cải thiện" trong khi thực tế không phải
- [ ] Dùng LLM-as-judge nhưng **không calibrate** với human-labeled data → false confidence, tệ hơn không có eval
- [ ] Chấm bằng chính model đang được đánh giá → self-preference bias, nên dùng model khác để judge
- [ ] Golden dataset chỉ có input sạch, thiếu adversarial input → eval score không dự đoán được production performance
- [ ] Đổi prompt/model/retrieval nhưng **không update eval suite tương ứng** → eval set lỗi thời, pass hết nhưng production vẫn lỗi (case study document summarization trong lesson)
- [ ] Coi single-turn eval là đủ cho hệ thống multi-turn (chatbot, agent) — cần golden dataset riêng dạng full transcript

## Exam tips
- Câu scenario dạng "chọn loại eval nào cho behavior X" → áp grading ladder: code-based trước, LLM-as-judge khi cần interpretation, human review là last resort.
- Câu hỏi về "tại sao production lỗi sau khi đổi prompt dù eval pass" → đáp án nhiều khả năng là **eval suite lỗi thời / không match behavior mới**, không phải do model yếu.
- Nhớ nguyên tắc: risk cao nhất không phải là "không có eval" mà là "**có eval nhưng outdated**" — tạo false confidence.
- Cost của eval không phải lý do chính đáng để giảm dataset — rủi ro under-evaluating luôn lớn hơn.

## Code / config snippets
```python
# Ví dụ minh hoạ cấu trúc 1 test case trong golden dataset (code-based eval)
# Dùng cho behavior "extract structured field từ claim document"
golden_case = {
    "input": "...nội dung claim document...",   # input mẫu (bao gồm cả case adversarial: thiếu field, viết tay...)
    "expected": {
        "filer_name": "Nguyen Van A",
        "claim_number": "CLM-2026-001",
        "incident_date": "2026-01-15",
        "claimed_amount": 1500.00,
    },
    "failure_mode": "missing_incident_date",  # category để trace khi eval fail
}

def code_based_check(output: dict, expected: dict) -> bool:
    # Check tự động (rẻ, nhanh) — dùng cho field có single correct answer
    return all(output.get(k) == v for k, v in expected.items())
```

## Câu hỏi chưa rõ
- ?
