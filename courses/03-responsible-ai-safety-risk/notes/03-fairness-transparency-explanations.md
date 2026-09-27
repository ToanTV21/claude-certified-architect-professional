# C3.3 — Fairness & transparency: giải thích cho user / regulator / debug team

> **Course:** 3 — Responsible AI, Safety & Risk for Architects (114 min) · **Exam domain:** D5 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Identify where unequal outcomes can arise within a system and define the explanations required for users, regulators, and your own debugging team, so fairness and transparency are built into the design

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Vì sao runtime control (C3.2) không bắt được unequal outcome:** runtime control chặn output bị disallow — output vi phạm policy rõ ràng (nội dung độc hại, leak PII...). Nhưng có một loại lỗi khác: output **pass hết mọi check** (đúng format, không độc hại, đúng policy) nhưng lại **tạo ra outcome khác nhau cho các nhóm người khác nhau** — VD hai applicant hồ sơ tương đương nhưng bị model xử lý khác nhau vì thuộc nhóm khác nhau. Loại lỗi này khó phát hiện và khó attribute hơn hẳn, vì bề ngoài nó là một output hoàn toàn "bình thường" — không có rule nào trong runtime control được viết ra để bắt nó.

- **4 injection point — nơi unequal outcome đi vào hệ thống:** đây là điểm mấu chốt biến fairness từ "model attribute" thành "architectural property" — vì cả 4 điểm này đều nằm trong tầm kiểm soát của người **thiết kế hệ thống**, không phải của model provider:
  1. **Retrieval corpus** — corpus over-represent hoặc under-represent một số nhóm/case → context mà model nhìn thấy đã bị skew từ trước khi model kịp suy luận.
  2. **Framing của prompt** — cách đặt câu hỏi/instruction có thể ngầm encode một assumption đẩy outcome theo một hướng nhất định.
  3. **Few-shot examples** — ví dụ minh hoạ dùng trong prompt có thể mang cùng skew như corpus (VD toàn ví dụ về một nhóm đối tượng).
  4. **Downstream routing** — sau khi model ra output, bước routing tiếp theo (đưa case đi hướng nào, escalate hay auto-approve) có thể dẫn các nhóm khác nhau đi theo path khác nhau.
  Mỗi injection point là một nơi **có thể inspect được** — đây là lý do fairness phải được xử lý ở tầng architecture (instrument từng điểm) thay vì chỉ tin vào "model đã được test fairness rồi".

- **3 audience cần giải thích khác nhau — cùng một quyết định, câu hỏi khác nhau, dữ liệu cần capture khác nhau:**

  | Audience | Câu hỏi họ hỏi | Cần gì để trả lời |
  |---|---|---|
  | Affected user | "Vì sao quyết định này ảnh hưởng tới tôi?" | Explanation rõ ràng, ở dạng họ **hành động được** — inputs nào đã drive quyết định + reason ở dạng dễ hiểu (digestible), không cần raw log kỹ thuật |
  | Regulator | "Các case tương đương có được xử lý consistent không? Truy lại được quyết định cụ thể này không?" | Một **record durable, queryable** của inputs/outputs/decision path — phải tồn tại lâu dài và tra cứu được theo yêu cầu |
  | Build/debug team | "Vì sao case bị flag này lại sai, sửa ở đâu?" | **Full trace**: prompt, retrieved context, model output, từng bước routing — gắn với observability instrumentation sẵn có |

  Ba nhu cầu này không thể trả lời bằng một audit log chung đơn giản — mỗi audience cần một "lát cắt" khác nhau của cùng một bản ghi.

- **Decision logging** là cơ chế duy nhất làm được cả 3 việc trên: capture **inputs** đã drive quyết định, **retrieved context**, **model output**, và **routing path** đã đi qua. Điểm quan trọng: đây dùng **cùng observability instrumentation** đã có từ production monitoring (Course 2) — nhưng áp cho **câu hỏi khác**: không phải "hệ thống có healthy không" mà là "**vì sao quyết định cụ thể này lại ra như vậy**". Cơ chế instrument (capture point) giống nhau, chỉ khác **retention** (giữ lâu hơn, theo mục đích cụ thể) và **query path** (tra theo decision/session, không chỉ theo metric aggregate).

- **Fairness-and-transparency checklist** (ví dụ áp cho credit-decision support system) — 4 câu hỏi, "no" ở bất kỳ đâu là một **design gap**:
  1. Injection point nào trong 4 điểm có thể skew outcome này, và điểm đó **đã được instrument** chưa?
  2. Với một adverse decision, có xuất được inputs + reason ở dạng applicant **hành động được** không?
  3. Nếu regulator hỏi "các applicant tương đương có được xử lý consistent không", có **query được log** để trả lời không?
  4. Team có pull được **full trace** cho bất kỳ decision bị flag nào không?

- **Discernment** — một trong 4 AI Fluency competency: năng lực **đánh giá** output/behavior của AI (chấp nhận được / cần sửa / cần override) thay vì chỉ xác nhận "model đã trả ra một giá trị". Áp vào fairness: discernment là năng lực giúp reviewer **nhận ra** một outcome bị skew/không có justification, thay vì chỉ thấy "có kết quả là được". Nhưng discernment chỉ phát huy được khi có **transparency record** (decision log) làm cơ sở để nhận ra — không có log thì không có gì để discern trên.

- **Case study "fairness treated as vendor's problem":** team giả định fairness đã được xử lý ở tầng model (provider đã train, đã chạy bias evaluation, đã publish kết quả) — hợp lý nếu model được dùng nguyên bản. Nhưng hệ thống của team **pair model với retrieval corpus riêng của họ**, và corpus đó **over-represent một số case** — injection point mà model provider không bao giờ test được và không thể thấy được, vì nó không nằm trong phạm vi của provider. Khi outcome bị đặt câu hỏi, team **đã log quá ít** — không đủ để reconstruct quyết định, không chứng minh được (và cũng không loại trừ được) corpus là nguồn gốc skew. Kết quả: không trả lời được câu hỏi duy nhất mà regulator hỏi — "skew đến từ đâu?". Root cause thật sự: gán fairness là property của model/vendor, nên **không ai monitor injection point mà chính team kiểm soát** (retrieval corpus).

- **Checkpoint "critique decision-logging design"** — với 1 system sketch cho decision-support flow, xác định 3 gap + 2 adequate + 1 gap:
  - **GAP** — routing step đưa một số case đi path khác mà **không có log entry**.
  - **GAP** — retrieval step mà **returned context không được capture**.
  - **GAP** — model output được lưu **thiếu inputs đã tạo ra nó**.
  - **ADEQUATE** — inputs, outputs, routing đều được log và **gắn với session ID**.
  - **ADEQUATE** — log **query được theo từng decision** và retain **90 ngày**.
  - **GAP** — aggregate accuracy dashboard **không có per-subgroup breakdown** — đây chính là gap nguy hiểm nhất vì dễ bị bỏ qua: dashboard "trông ổn" ở mức tổng nhưng có thể đang che một nhóm bị đối xử tệ hơn hẳn.
  Principle rút ra: **aggregate-only metric có thể che unfairness ở cấp subgroup** — cùng pattern "per-request/per-subgroup decomposition tốt hơn aggregate-only" đã học ở Course 2 (observability).

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Log đầy đủ cả 4 injection point (retrieval corpus, prompt framing, few-shot examples, downstream routing) | Hệ thống ra quyết định ảnh hưởng người thật (credit, hiring, healthcare, moderation) — cần trả lời được cho user/regulator/build team | Storage + query path tăng theo traffic (không cố định); công sức instrument 4 điểm khác nhau, mỗi điểm khác cấu trúc data | Thấp — nếu skew xảy ra ở injection point đã log thì reconstruct/attribute được, tránh lặp lại case "log quá ít không chứng minh được" | Cao — nếu bỏ log rồi mới cần thêm, phải đợi traffic mới đi qua mới có dữ liệu; log lịch sử đã mất không tái tạo được |
| Chỉ tin vào model provider's fairness eval (không log injection point của riêng mình) | Hệ thống dùng model nguyên bản, không có retrieval corpus/few-shot/routing riêng — rủi ro thực sự nằm ngoài tầm ảnh hưởng của mình | Thấp ban đầu — không tốn công instrument | Cao — không thấy được skew phát sinh từ corpus/framing/routing riêng của mình; khi bị hỏi "skew từ đâu" thì không trả lời được (case study trong lesson) | Rất cao — phải build lại decision logging sau khi incident xảy ra, không cứu được các quyết định đã ra trong quá khứ |
| Aggregate metric only (1 dashboard accuracy tổng) | Giai đoạn prototype/demo, chưa phục vụ quyết định ảnh hưởng người thật, hoặc traffic quá nhỏ để chia subgroup có ý nghĩa | Thấp — 1 dashboard, không cần breakdown | Cao — có thể "trông ổn" ở mức tổng trong khi harm tập trung ở 1 subgroup; đây là gap bị checkpoint đánh dấu rõ nhất | Trung bình — thêm được per-subgroup breakdown nếu đã log đủ field nhóm/attribute, nhưng dữ liệu lịch sử thiếu field đó thì không breakdown lại được |
| Per-subgroup breakdown (đo riêng theo nhóm/attribute liên quan) | Hệ thống ra quyết định có thể ảnh hưởng khác nhau theo nhóm (credit, hiring...) — bắt buộc theo checklist fairness-transparency | Cao hơn — cần xác định subgroup liên quan, đảm bảo đủ sample size mỗi nhóm, thêm chiều phân tích | Thấp hơn về fairness risk, nhưng bản thân việc lưu group/attribute lại làm tăng phạm vi dữ liệu nhạy cảm cần bảo vệ | Trung bình — cần định nghĩa lại subgroup nếu quy định/đối tượng thay đổi, nhưng hạ tầng log đã có sẵn thì dễ mở rộng |
| Governance riêng cho decision log (minimization, retention limit, access control, đưa vào compliance register) | Bất cứ khi nào decision log chứa input/context có personal data (HIPAA/GDPR context) — tức hầu hết hệ thống ra quyết định về người | Thêm review pháp lý/compliance, thêm cơ chế enforce retention + access control | Nếu bỏ qua: decision log (vốn được tạo ra để tăng transparency) lại chính là nguồn vi phạm compliance vì giữ personal data không kiểm soát | Trung bình — retention/access policy áp dụng được lên log đã có sẵn, không cần đổi cấu trúc log, nhưng phải audit lại dữ liệu đã lưu trước đó |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Unequal outcome | Output pass hết mọi runtime check nhưng tạo ra kết quả khác nhau cho các nhóm người khác nhau — không phải "output sai" theo nghĩa policy violation |
| Injection point | 1 trong 4 điểm mà unequal outcome có thể đi vào hệ thống: retrieval corpus, prompt framing, few-shot examples, downstream routing — đều nằm trong tầm kiểm soát của architect |
| Retrieval corpus skew | Corpus over-represent hoặc under-represent một số nhóm/case, khiến context model nhìn thấy đã lệch trước khi model suy luận |
| Decision logging | Capture inputs, retrieved context, model output, và routing path của một quyết định cụ thể — dùng để trả lời "vì sao" thay vì "hệ thống có khoẻ không" |
| Decision-level record (durable, queryable) | Bản ghi giữ đủ lâu và tra cứu được theo từng quyết định cụ thể — thứ regulator cần để kiểm tra consistency |
| Full trace | Toàn bộ chuỗi: prompt → retrieved context → model output → từng bước routing, gắn với observability instrumentation sẵn có — thứ build team cần để debug |
| Discernment | 1 trong 4 AI Fluency competency: năng lực đánh giá output AI là acceptable / cần sửa / cần override, không chỉ xác nhận có kết quả |
| Per-subgroup breakdown | Đo metric riêng theo từng nhóm/attribute, thay vì chỉ 1 số aggregate — cần để phát hiện harm tập trung ở 1 nhóm |
| Aggregate-only metric | Metric tổng hợp (VD accuracy trung bình) có thể "trông ổn" trong khi che mất unfairness ở cấp subgroup |
| Fairness as architectural property | Quan điểm cốt lõi của lesson: fairness không phải thuộc tính riêng của model, mà là thuộc tính của toàn bộ hệ thống (corpus, prompt, routing do architect kiểm soát) |

## Gotchas / bẫy hay gặp
- [ ] Coi fairness là "vấn đề của model provider" vì họ đã publish bias evaluation — bỏ qua việc hệ thống của mình pair model với retrieval corpus/prompt/routing riêng, là những injection point provider không thể thấy
- [ ] Runtime control (từ C3.2) đã pass hết check → yên tâm là "output ổn" — nhưng runtime control không được thiết kế để bắt unequal outcome giữa các nhóm, chỉ bắt output vi phạm policy rõ ràng
- [ ] Chỉ có aggregate metric (1 dashboard accuracy tổng) mà không có per-subgroup breakdown → harm tập trung ở 1 nhóm bị che khuất hoàn toàn
- [ ] Log input/output nhưng không log **retrieved context** hoặc **routing path** → khi bị hỏi "vì sao quyết định này ra như vậy" thì không đủ dữ kiện trả lời, dù có vẻ như "đã có logging"
- [ ] Xây decision logging chỉ để phục vụ 1 audience (VD chỉ phục vụ debug team) mà quên rằng regulator và affected user cần lát cắt dữ liệu khác — dẫn tới thiếu field cần cho 2 audience còn lại
- [ ] Giữ decision log vô thời hạn "cho chắc" mà không áp minimization/retention limit — trong khi log chứa personal data thuộc phạm vi HIPAA/GDPR, tự biến log thành rủi ro compliance
- [ ] Nghĩ rằng "logging nhiều để transparency" và "giới hạn dữ liệu để compliance" là hai mục tiêu xung đột — thực ra chúng dùng chung 1 log, chỉ cần **governance khác nhau** (access control, retention, minimization) trên cùng dữ liệu đó

## Exam tips
- Câu hỏi dạng "hệ thống pass hết eval/runtime check nhưng vẫn bị nghi fairness issue — nên nhìn ở đâu?" → đáp án là kiểm tra 4 injection point (retrieval corpus, prompt framing, few-shot examples, downstream routing), không phải nghi model weights hay quay lại runtime control.
- Câu hỏi dạng "team đổ lỗi model provider vì họ đã test bias, nhưng bị regulator hỏi không trả lời được" → nhận diện đây là case fairness bị coi là vendor's problem trong khi injection point (thường là retrieval corpus riêng của hệ thống) nằm trong tầm kiểm soát của architect.
- Câu hỏi phân biệt "aggregate metric trông lành mạnh" vs "per-subgroup bị lệch" → luôn chọn đáp án ưu tiên per-subgroup breakdown; aggregate-only là một design gap, không phải một lựa chọn chấp nhận được cho hệ thống ra quyết định ảnh hưởng người.
- Câu hỏi "3 audience khác nhau cần gì" → nhớ đúng mapping: user cần explanation hành động được, regulator cần record durable/queryable để chứng minh consistency, build team cần full trace gắn observability — không dùng lẫn nhu cầu của audience này cho audience khác.
- Nếu đề bài mô tả một decision-logging design, áp checklist "3 GAP quen thuộc": routing không log, retrieved context không capture, output lưu thiếu input đi kèm — đây là 3 lỗi hay bị đưa vào distractor.

## Code / config snippets
```python
# Minh hoạ cấu trúc 1 decision_log record — đủ chi tiết để trả lời cho cả 3 audience
# (affected user / regulator / build team) từ CÙNG một bản ghi, chỉ khác cách query/slice.

decision_log_record = {
    "session_id": "sess_2026_0928_00042",   # khoá để build team join với observability trace sẵn có
    "timestamp": "2026-09-28T09:15:00Z",

    # --- Phần build team cần để debug (full trace) ---
    "prompt_framing": "Đánh giá hồ sơ vay dựa trên thu nhập và lịch sử tín dụng...",
    "retrieved_context": [
        {"doc_id": "policy_2025_v3", "score": 0.91},
        {"doc_id": "case_precedent_118", "score": 0.77},
    ],  # capture NGUYÊN VẸN context được retrieval trả về — injection point #1
    "few_shot_examples_used": ["example_042", "example_017"],  # injection point #3
    "routing_path": ["auto_screen", "manual_review_queue"],    # injection point #4, log MỌI bước routing

    # --- Phần regulator cần: record durable, query theo decision ---
    "model_output_raw": "DENY - insufficient income stability",
    "decision_final": "DENY",
    "applicant_group_attributes": {"region": "region_A"},  # để tra per-subgroup breakdown, KHÔNG dùng để quyết định

    # --- Phần affected user cần: reason ở dạng hành động được ---
    "user_facing_reason": (
        "Hồ sơ bị từ chối do thu nhập 6 tháng gần nhất không ổn định. "
        "Có thể nộp lại kèm sao kê thu nhập bổ sung."
    ),

    # --- Governance: retention/minimization áp lên chính record này ---
    "retention_expires_at": "2026-12-27",   # retention limit — không giữ vô thời hạn
    "pii_fields": ["applicant_group_attributes"],  # đánh dấu field nhạy cảm để áp access control riêng
}

# Query theo decision cụ thể (đáp ứng nhu cầu regulator: "reconstruct quyết định này")
def get_decision_trace(log_store: list[dict], session_id: str) -> dict | None:
    # Trả về đúng 1 record theo session_id — regulator/build team dùng chung hàm này,
    # chỉ khác là họ được cấp quyền xem field khác nhau (access control theo audience)
    for record in log_store:
        if record["session_id"] == session_id:
            return record
    return None
```

## Câu hỏi chưa rõ
- ?
