# Domain 4 — Evaluation, Testing & Optimization (16% · 10 câu)

> Nguồn: practice set của Matthew Purcell (xem [README](README.md)). Đề được **diễn giải lại bằng tiếng Việt**.

**Chủ đề xuyên suốt:** eval gắn với **business outcome** · dataset từ **dữ liệu thật + edge case** ·
**LLM-as-judge có calibrate bằng người** · offline eval → **A/B / canary** trước khi full rollout ·
tối ưu cost **dựa trên trace**, không đoán mò · **leading vs lagging indicator**.

Note liên quan: [C2.1 success criteria & eval suite](../../courses/02-enterprise-integration-production/notes/01-success-criteria-eval-suite.md) ·
[C2.2 PoC → production checklist](../../courses/02-enterprise-integration-production/notes/02-poc-to-production-checklist.md) ·
[C2.5 A/B testing experiments](../../courses/02-enterprise-integration-production/notes/05-ab-testing-experiments.md)

---

## Q4.1 · Multiple choice · "Đủ tốt để launch chưa?"

**Tình huống:** Steering committee hỏi contract-review assistant đã "good enough to launch" chưa. Team chỉ có
**giai thoại** từ pilot user, không có chỉ số chính thức. Architect nên thiết lập gì trước?

- A. Benchmark tổng quát của model do bên thứ ba công bố
- B. Đếm số pilot user nói assistant "hữu ích"
- C. So sánh token cost với quy trình thủ công hiện tại
- D. Metric đánh giá theo task, gắn với business outcome (accuracy trích xuất điều khoản, giảm thời gian review, tỷ lệ escalation) với ngưỡng launch đã thống nhất

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** "Good enough" chỉ có nghĩa khi so với **task-specific metrics + agreed thresholds** gắn với business
outcome. Định nghĩa này phải có **trước** quyết định launch (eval = acceptance criteria / gating mechanism).

| Option | Vì sao sai |
|--------|-----------|
| A | Đo *model*, không đo *solution* của bạn |
| B | Giai thoại, không phải đo lường |
| C | Đo cost, không đo quality |
</details>

---

## Q4.2 · Multiple choice · Thành phần eval dataset

- A. 1,000 câu hỏi synthetic do model sinh từ tài liệu sản phẩm
- B. Query thật (đã anonymise) lấy từ kênh giống production, bổ sung edge case và scenario dễ fail được dựng có chủ đích
- C. Chính các example đang nằm trong system prompt
- D. Câu hỏi do chính engineer xây assistant viết ra

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Query thật phản ánh **phân phối input thật**; edge case dựng có chủ đích dò **bề mặt thất bại**.
Kết hợp = test cả đường thường lẫn chỗ vỡ.

| Option | Vì sao sai |
|--------|-----------|
| A | Thừa hưởng điểm mù của tài liệu; synthetic ổn để *bổ sung*, không nên là *nguồn chính* |
| C | Chỉ chứng minh model "thuộc bài" (data leakage giữa prompt và test) |
| D | Test giả định của người xây bằng chính giả định đó |
</details>

---

## Q4.3 · Multiple choice · Đánh giá tone/brand ở quy mô hàng nghìn output/tuần

- A. LLM-as-judge chấm theo rubric brand guideline, định kỳ calibrate với điểm của human expert trên một sample
- B. So khớp chuỗi chính xác với thư viện copy đã duyệt
- C. Người review toàn bộ output, chấp nhận chi phí
- D. Bỏ qua đánh giá tone vì chủ quan, không đo được

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** Chất lượng *chủ quan* ở *quy mô lớn* → phương pháp hỗn hợp: LLM judge áp rubric cho **mọi** output,
human calibration định kỳ để **giữ judge trung thực** (đo agreement giữa judge và người).

| Option | Vì sao sai |
|--------|-----------|
| B | Không chấm được copy mới (exact match chỉ hợp với output có đáp án cố định) |
| C | Không scale |
| D | Bỏ một requirement đo được |

**Chọn grader:** code-based (exact/regex/schema) → khi có đáp án xác định · LLM-as-judge → chủ quan, scale ·
human → gold standard, calibrate, case rủi ro cao.
</details>

---

## Q4.4 · Multiple choice · Prompt mới thắng offline 6 điểm

- A. Deploy toàn bộ traffic ngay vì offline eval đã validate
- B. Chạy lại offline suite nhiều lần để tăng độ tin cậy thống kê
- C. A/B test có kiểm soát trên một phần traffic, theo dõi quality + guardrail metric rồi mới ramp up
- D. Nhờ 3 stakeholder senior so sánh output mẫu và duyệt

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Offline gain **không chắc chuyển được** sang phân phối production. A/B có giới hạn + guardrail
metric biến "hứa hẹn offline" thành "bằng chứng production" với rủi ro bị chặn trên.

| Option | Vì sao sai |
|--------|-----------|
| A | Bỏ qua kiểm soát rủi ro |
| B | Đo lại **cùng một phân phối** — không thêm thông tin về production |
| D | Lấy ý kiến, không phải đánh giá |
</details>

---

## Q4.5 · Multiple choice · Yêu cầu giảm 40% inference cost

**Tình huống:** Leadership đòi giảm 40% cost. Đề xuất đầu tiên của team: chuyển **mọi** workload sang model nhỏ nhất.

- A. Duyệt luôn vì model là đòn bẩy cost duy nhất
- B. Phân tích token usage và cost theo workload từ production trace, nhắm vào driver cost lớn nhất (caching, cắt context, downsize có chọn lọc) kèm eval tác động chất lượng
- C. Từ chối mọi nỗ lực giảm cost vì chất lượng luôn giảm
- D. Giảm max output tokens 40% cho mọi workload

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** **Optimise from evidence.** Trace cho biết tiền đang đi vào đâu: context size, cache miss, output
length hay model choice → dùng đúng đòn bẩy cho driver lớn nhất, eval chất lượng ở mỗi bước.

| Option | Vì sao sai |
|--------|-----------|
| A | Một đòn bẩy áp dụng mù quáng (gotcha "downsize model mù quáng") |
| C | Từ chối nhiệm vụ |
| D | Cắt output bất chấp hậu quả (truncate) |

**Đòn bẩy cost nên nhớ:** prompt caching · Batch API (async, rẻ hơn ~50%) · model routing theo độ khó ·
cắt/thu gọn context (RAG thay vì stuffing) · giới hạn output hợp lý.
</details>

---

## Q4.6 · Multiple choice · Chuyển sang model version mới

- A. Chuyển hết traffic một lần vì version mới mạnh hơn hẳn
- B. Hoãn 6 tháng chờ công ty khác kiểm chứng
- C. Chỉ dùng version mới cho khách hàng mới
- D. Chạy full eval suite trên version mới, rồi rollout dần (canary) với regression monitoring trước khi cutover

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** Đổi model version = **rủi ro regression**. Full suite bắt regression mà spot check bỏ sót; canary
chặn blast radius của những gì suite không bắt được. (Liên hệ: **pin model version** trong production, đổi version
là một change có kiểm soát.)

| Option | Vì sao sai |
|--------|-----------|
| A | "Mới hơn" ≠ "tốt hơn cho task của bạn" |
| B | Mất cải tiến mà không thêm an toàn |
| C | Chia đôi fleet mà không bảo vệ nửa nào |
</details>

---

## Q4.7 · Multiple choice · Leading indicator cho RAG

**Tình huống:** Muốn **cảnh báo sớm** chất lượng RAG giảm, lý tưởng là **trước khi user nhận ra**.

- A. Số complaint chính thức tăng
- B. Hoá đơn inference hằng tháng
- C. Retrieval relevance score giảm và tỷ lệ "no grounded answer found" tăng trong telemetry
- D. Số DAU giảm so với quý trước

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Tín hiệu **nội bộ pipeline** (retrieval relevance, grounding rate) dịch chuyển **trước** khi chất
lượng user thấy được thay đổi → định nghĩa của *leading indicator*.

| Option | Vì sao sai |
|--------|-----------|
| A | Lagging — thiệt hại đã xảy ra |
| B | Cost, không phải quality |
| D | Lagging và quá thô |
</details>

---

## Q4.8 · Multiple response (chọn 2) · Eval pre-production cho domain có quản lý (regulated)

- A. Demo live cho ban điều hành bằng example chọn lọc
- B. Golden dataset do domain expert gán nhãn, phủ cả case thông thường lẫn case rủi ro cao
- C. Adversarial test: dò ranh giới an toàn, prompt injection, request vi phạm policy
- D. Benchmark kiến thức tổng quát so với model đối thủ
- E. Khảo sát mức hài lòng sau khi launch

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B, C**

**Vì sao đúng:** Regulated domain cần cả hai mặt: **(B) chứng minh năng lực** trên case thường + rủi ro cao, **(C)
chứng minh ranh giới đứng vững** khi bị tấn công.

| Option | Vì sao sai |
|--------|-----------|
| A | "Diễn kịch" trên example chọn sẵn |
| D | Đo sai thứ |
| E | Đến sau khi rủi ro đã ship ("pre-production" là keyword loại E) |
</details>

---

## Q4.9 · Multiple response (chọn 2) · Chất lượng giảm thất thường, mọi thứ "không đổi"

**Tình huống:** Chất lượng giảm lúc có lúc không trong 2 tuần. **Latency, model version, prompt không đổi.**

- A. End-to-end trace của các session bị ảnh hưởng, gồm retrieved context và tool input/output
- B. Tổng số request/ngày
- C. Billing dashboard theo model
- D. Phân tích drift của input distribution (loại query, format, ngôn ngữ mới mà hệ thống không được thiết kế cho)
- E. Uptime của API endpoint

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A, D**

**Vì sao đúng:** Code/model/prompt không đổi → nguyên nhân gần như chắc chắn nằm ở **thứ đang chảy qua hệ thống**:
(A) trace cho thấy hệ thống *thực sự* làm gì ở session lỗi (retrieval trả gì, tool trả gì), (D) drift cho thấy input
có thay đổi "dưới chân" hệ thống không.

| Option | Vì sao sai |
|--------|-----------|
| B | Volume, không giải thích thay đổi quality |
| C | Chi phí, không phải quality |
| E | Availability, không phải quality |

**Tư duy loại trừ:** đề liệt kê "X, Y, Z không đổi" → loại mọi đáp án đổ lỗi cho X, Y, Z và tìm biến số *còn lại*.
</details>

---

## Q4.10 · Scenario matching · Phân loại lỗi

Options: `prompt failure` · `hallucination` · `model mismatch`

1. Model nhỏ, nhanh tóm tắt email ngắn tốt nhưng **luôn mất chi tiết** với hợp đồng 40 trang.
2. Assistant được dặn "respond concisely" nhưng trả 3 đoạn vì system prompt **cũng** dặn "explain your reasoning in detail".
3. Bot Q&A sản phẩm tự tin trích một điều khoản bảo hành **không hề tồn tại** trong tài liệu.
4. Assistant dùng model general-purpose làm kém ở task chuyên biệt cần suy luận pháp lý sâu, **dù prompt được cấu trúc tốt**.
5. Agent CSKH **bịa ra mã vận đơn** khi tool lookup trả về rỗng.

<details><summary>👉 Đáp án & giải thích</summary>

| # | Đáp án | Lý do |
|---|--------|-------|
| 1 | model mismatch | Khoảng cách năng lực giữa model được chọn và độ khó task (long doc) |
| 2 | prompt failure | Instruction xung đột — lỗi nằm ở prompt |
| 3 | hallucination | Bịa tự tin, không có căn cứ trong source |
| 4 | model mismatch | "Despite well-structured prompts" = đã loại trừ prompt → năng lực model không khớp task |
| 5 | hallucination | Bịa dữ liệu khi tool trả rỗng |

**Góc nhìn thêm (item 5):** hiện tượng là *hallucination*, nhưng **fix** thường nằm ở prompt/tool design: dặn rõ
"nếu tool trả rỗng thì nói không tìm thấy", và trả về kết quả rỗng có cấu trúc rõ (ví dụ `{"found": false}`).
Câu hỏi hỏi *loại lỗi* nên chọn hallucination.
</details>
