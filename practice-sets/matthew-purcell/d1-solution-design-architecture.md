# Domain 1 — Solution Design & Architecture (17% · 11 câu)

> Nguồn: practice set của Matthew Purcell (xem [README](README.md)). Đề được **diễn giải lại bằng tiếng Việt**,
> không chép nguyên văn. Làm "cold" trước rồi mới mở phần `Đáp án & giải thích`.

**Chủ đề xuyên suốt domain này:** chọn đúng *pattern* cho bài toán — `single augmented LLM call` →
`fixed workflow` → `autonomous agent` → `multi-agent system`. Nguyên tắc vàng: **chọn pattern đơn giản nhất
giải được bài toán**, chỉ leo thang khi bài toán thực sự đòi hỏi.

Note liên quan: [C1.2 augmented vs workflow vs agent](../../courses/01-claude-platform-solution-design/notes/02-augmented-vs-workflow-vs-agent.md) ·
[C1.3 reference architecture patterns](../../courses/01-claude-platform-solution-design/notes/03-reference-architecture-patterns.md) ·
[C2.3 use-case sizing](../../courses/02-enterprise-integration-production/notes/03-use-case-sizing-feasibility.md)

---

## Q1.1 · Multiple choice · Workflow vs agent (bài toán ổn định)

**Tình huống:** Công ty logistics xử lý báo giá vận chuyển. Mọi request đều đi qua **đúng 3 bước giống nhau**:
extract thông tin từ email → validate với rate card → sinh tài liệu báo giá. Requirement ổn định, bước không bao giờ thay đổi.

- A. Multi-agent với supervisor giao việc cho các specialist agent
- B. Fixed workflow, mỗi bước là một LLM call riêng, chạy tuần tự
- C. Autonomous agent có tool, tự lên kế hoạch cho từng request
- D. Một prompt khổng lồ chứa toàn bộ instruction + cả rate card

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Khi các bước **biết trước, cố định, lặp lại** → đây là "sách giáo khoa" của `fixed workflow`
(còn gọi là *prompt chaining*). Lợi ích: predictable, audit được từng bước, dễ debug (biết bước nào hỏng),
có thể chèn validation giữa các bước (ví dụ check output của bước extract trước khi đi tiếp).

| Option | Vì sao sai |
|--------|-----------|
| A | Thêm overhead điều phối multi-agent mà bài toán không cần |
| C | Agent tự plan là để xử lý path *không biết trước* — ở đây path đã biết → thừa, kém predictable, tốn token |
| D | Mất khả năng kiểm soát và validate từng bước; một lỗi ở giữa không bắt được |

**Signal keyword:** "same steps", "never vary", "stable requirements" → **workflow**.
</details>

---

## Q1.2 · Multiple choice · Workflow vs agent (bài toán mở)

**Tình huống:** Research assistant cho consultancy trả lời câu hỏi mở của client. Số bước thay đổi rất nhiều:
có request cần 3 lần web search, có request cần phân tích tài liệu + tính toán + các query follow-up mà
**chỉ biết là cần khi đang làm dở**.

- A. Fixed workflow với thật nhiều bước định nghĩa sẵn để phủ phần lớn case
- B. Router phân loại request vào 1 trong 5 pipeline dựng sẵn
- C. Batch chạy mọi phân tích có thể cho mọi request rồi bỏ phần không dùng
- D. Autonomous agent chạy vòng lặp plan → act → observe → quyết định bước tiếp

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** Khi **đường đi chỉ lộ ra trong quá trình thực thi** (bước N+1 phụ thuộc kết quả bước N) thì
chỉ có agent loop (plan-act-observe) xử lý được. Đây chính là điều kiện "earn the complexity" của agent.

| Option | Vì sao sai |
|--------|-----------|
| A | Giả định enumerate được các bước từ trước — trái đề bài |
| B | Router vẫn yêu cầu biết path từ đầu; không xử lý được follow-up phát sinh giữa chừng |
| C | Lãng phí khủng khiếp và vẫn không "follow up" theo phát hiện trung gian được |

**Signal keyword:** "vary enormously", "only becomes clear mid-task" → **autonomous agent**.

**So sánh Q1.1 vs Q1.2:** cùng 1 câu hỏi "workflow hay agent", biến số quyết định là *path có biết trước không*.
</details>

---

## Q1.3 · Multiple choice · Task decomposition

**Tình huống:** Một prompt duy nhất bắt Claude đọc RFP 60 trang, đánh giá compliance với 40 policy nội bộ,
chấm điểm cơ hội, rồi viết khuyến nghị go/no-go. Kết quả không ổn định: **bỏ sót policy**, lý giải scoring
**hời hợt**. Team đã sửa wording prompt 2 lần rồi.

- A. Lên model lớn nhất và tăng max output tokens
- B. Thêm few-shot example về khuyến nghị go/no-go tốt
- C. Tách thành các subtask tuần tự (extract → assess theo nhóm policy → score → tổng hợp), truyền structured output giữa các bước
- D. Giảm temperature để model tuân thủ deterministic hơn

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Triệu chứng "**bỏ sót item** + **reasoning nông**" trên một task dài, nhiều phần = vấn đề
**cấu trúc**, không phải vấn đề wording hay năng lực model. Decompose giúp mỗi bước có context tập trung và
tạo **intermediate output kiểm chứng được** (ví dụ: bước assess xuất JSON 40 policy → dễ check thiếu cái nào).

| Option | Vì sao sai |
|--------|-----------|
| A | Coi "capacity" là nguyên nhân trong khi gốc là structure; tốn tiền mà không chắc hết |
| B | Few-shot giúp *format/style*, không giải quyết *coverage* của 40 policy |
| D | Temperature ảnh hưởng độ ngẫu nhiên, không ảnh hưởng độ bao phủ |

**Signal keyword:** "already refined the prompt wording" → loại các đáp án "sửa prompt tiếp";
"some policies are skipped" → decomposition.

**Bẫy hay gặp:** phản xạ "upgrade model" — đề CCAR-P gần như luôn coi đó là *blind fix* nếu chưa chẩn đoán gốc.
</details>

---

## Q1.4 · Multiple choice · Multi-agent orchestration

**Tình huống:** Hệ thống xử lý claim có 4 specialist agent: intake, fraud screening, policy validation, payout
calculation. Yêu cầu: **audit trail đầy đủ, có thứ tự** cho mọi quyết định, và agent sau **không được chạy**
nếu agent trước flag exception.

- A. Supervisor/orchestrator gọi từng specialist theo thứ tự, ghi lại kết quả, dừng chuỗi khi có exception
- B. Peer-to-peer handoff, mỗi agent tự quyết gọi agent nào tiếp
- C. Chạy song song cả 4 agent rồi merge output
- D. Shared message board, các agent tự theo dõi và phản hồi cơ hội

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** 3 yêu cầu (ordering, audit trail tập trung, halt-on-exception) đều cần **một điểm điều phối
trung tâm**. Supervisor là nơi duy nhất *đảm bảo* (guarantee) cả 3.

| Option | Vì sao sai |
|--------|-----------|
| B | Ordering và halting trở thành *emergent behaviour* — không được đảm bảo |
| C | Vi phạm trực tiếp "agent sau không chạy khi agent trước flag" |
| D | Sequencing và exception handling phó mặc cho may rủi |

**Signal keyword:** "ordered audit trail", "must not run if earlier flags" → **centralized orchestrator**.

**Góc nhìn architect:** Đây thực chất là *workflow có agent làm node*. Khi requirement là **guarantee** thì chọn
cơ chế deterministic (code điều phối), không để model tự quyết.
</details>

---

## Q1.5 · Multiple choice · Chọn use case đầu tiên

**Tình huống:** Executive sponsor muốn "đưa AI vào toàn công ty", có 12 use case ứng viên từ các phòng ban.
Điều gì nên quyết định việc chọn use case **đầu tiên**?

- A. Use case thể hiện được năng lực agentic tiên tiến nhất
- B. Phòng ban có stakeholder nhiệt tình nhất để đảm bảo adoption
- C. Business value đo được (cost, efficiency, SLA) kết hợp data access khả thi và rủi ro quản lý được
- D. Use case go-live nhanh nhất, bất kể impact, để tạo đà

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Công thức chọn use case = **Value (đo được) × Feasibility (data, tích hợp) × Risk (quản lý được)**.
Project đầu tiên phải chứng minh được giá trị bằng con số thì mới tạo được sự ủng hộ bền vững cho các project sau.

| Option | Vì sao sai |
|--------|-----------|
| A | Tối ưu cho "trình diễn" (spectacle), không phải giá trị |
| B | Tối ưu cho chính trị; nhiệt tình ≠ value |
| D | Tối ưu tốc độ, bỏ qua impact → thắng nhanh nhưng không chứng minh được gì |

**Liên hệ:** [C2.3 use-case sizing & feasibility](../../courses/02-enterprise-integration-production/notes/03-use-case-sizing-feasibility.md).
</details>

---

## Q1.6 · Multiple choice · Feedback loop trong production

**Tình huống:** Hệ thống document-triage chạy production 3 tháng. Có dashboard latency và cost, nhưng **không
có cách nào biết classification có đúng không**.

- A. Dùng model lớn hơn vì accuracy thường tăng theo capability
- B. Alert khi token tiêu thụ hằng ngày lệch chuẩn
- C. Review system prompt hằng tuần xem instruction còn đúng không
- D. Feedback loop: thu thập correction ở downstream + tín hiệu user, đưa một sample output production vào labelled evaluation set

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** Kiến trúc thiếu mắt xích **feedback** trong vòng `input → processing → output → feedback`.
Muốn biết *correctness* thì phải có ground truth: correction từ người dùng/downstream + sample có label.

| Option | Vì sao sai |
|--------|-----------|
| A | Đổi model nhưng vẫn không đo được gì |
| B | Giám sát cost, không phải correctness |
| C | Giám sát cấu hình, không phải correctness |

**Nguyên tắc:** "Cái gì không đo được thì không cải thiện được" — câu hỏi về *quality in production* → đáp án
gần như luôn có chữ **eval / feedback / labelled sample**.
Liên hệ: [C4.3 lifecycle feedback loops](../../courses/04-stakeholder-engagement-lifecycle-gtm/notes/03-lifecycle-feedback-loops.md).
</details>

---

## Q1.7 · Multiple choice · RAG vs fine-tune (dữ liệu thay đổi hằng ngày)

**Tình huống:** Catalogue sản phẩm, giá, khuyến mãi của retailer **thay đổi hằng ngày**. Muốn Claude trả lời
khách dựa trên thông tin này.

- A. Fine-tune model trên catalogue hiện tại, lặp lại mỗi quý
- B. Retrieval trên catalogue live để câu trả lời phản ánh data hiện tại
- C. Dán toàn bộ catalogue vào context mỗi request
- D. Dựa vào kiến thức base model + disclaimer "giá có thể thay đổi"

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Dữ liệu *factual, thay đổi thường xuyên* = trường hợp kinh điển của **retrieval augmentation**.
Model luôn trả lời từ data mới nhất, không cần retrain.

| Option | Vì sao sai |
|--------|-----------|
| A | Fine-tune dạy *hành vi/style*, không phải cách tốt để nạp *fact thay đổi*; stale sau vài ngày |
| C | Tốn kém, không scale khi catalogue lớn, dễ gặp "lost in the middle" |
| D | Chấp nhận trả lời sai |

**Rule nhớ nhanh:** *Knowledge thay đổi → RAG. Behaviour/format cần thay đổi → prompt/few-shot (fine-tune là lựa chọn cuối).*
</details>

---

## Q1.8 · Multiple choice · Agent quá tải (tool bloat)

**Tình huống:** Một "operations agent" xử lý HR + IT + finance. Có **35 tools**, system prompt 6,000 tokens
phủ cả 3 domain, **tool-selection accuracy giảm dần** khi thêm capability. Stakeholder muốn thêm procurement.

- A. Tách thành các domain-specific agent đứng sau router/supervisor, mỗi agent có toolset và prompt tập trung
- B. Thêm tools procurement ngay, lên kế hoạch viết lại prompt quý sau
- C. Giữ 1 agent nhưng nhân đôi độ dài system prompt để mô tả kỹ hơn
- D. Bắt model dùng tool ở mọi request để khỏi trả lời từ kiến thức chung

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** "Accuracy chọn tool giảm khi breadth tăng" = tín hiệu kinh điển của **agent overload**. Tách theo
domain + router khôi phục prompt/toolset tập trung, và procurement trở thành *thêm một agent mới* thay vì
đè thêm lên agent đang quá tải.

| Option | Vì sao sai |
|--------|-----------|
| B | Làm trầm trọng thêm vấn đề đang có |
| C | Prompt dài hơn → khó follow hơn, không dễ hơn |
| D | Chẩn đoán sai: vấn đề là chọn *nhầm tool*, không phải *không dùng tool* |

**So sánh với Q3.2:** Q3.2 cũng là tool bloat nhưng có dữ kiện "1/3 tools chưa bao giờ được gọi" → bước đầu là
**audit & remove**. Q1.8 có dữ kiện "3 domain khác nhau + sắp thêm domain thứ 4" → **split theo domain**.
Đọc kỹ dữ kiện để chọn đúng "first step".
</details>

---

## Q1.9 · Multiple response (chọn 2) · Khi nào chọn fixed workflow

**Tình huống:** Hai đặc điểm nào của bài toán **ủng hộ mạnh nhất** fixed workflow thay vì autonomous agent?

- A. Input đến với format khó đoán, cần xử lý động
- B. Các bước xử lý biết trước và giống nhau cho mọi request
- C. Task có lợi khi khám phá sáng tạo nhiều hướng giải
- D. Business yêu cầu mỗi bước audit được và reproducible
- E. Team muốn model tự phục hồi khi tool lỗi bất ngờ

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B, D**

**Vì sao đúng:** Workflow thắng khi (1) **steps known & identical**, (2) cần **auditability + reproducibility**
từng bước.

| Option | Vì sao sai |
|--------|-----------|
| A | Input khó đoán → nghiêng về agent (xử lý động) |
| C | Khám phá nhiều hướng → dynamic planning → agent |
| E | Tự phục hồi → autonomy → agent |

**Mẹo:** A, C, E đều là "đặc điểm của agent" — câu multiple-response thường ghép 2 đúng + 3 "đúng cho pattern kia".
</details>

---

## Q1.10 · Multiple response (chọn 2) · Khi nào multi-agent xứng đáng

**Tình huống:** Task due-diligence phức tạp. Hai đặc điểm nào cho thấy **multi-agent** là cần thiết thay vì
một augmented agent?

- A. Lưu lượng request dự kiến rất cao
- B. Ngân sách project đủ lớn để nuôi nhiều agent
- C. Các sub-task cần chuyên môn, tool và context khác nhau, dồn vào một agent sẽ quá tải
- D. Stakeholder yêu cầu kiến trúc "xịn" nhất
- E. Nhiều sub-task độc lập, chạy song song được để giảm thời gian end-to-end

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C, E**

**Vì sao đúng:** Multi-agent "earn its complexity" khi có **(1) specialization/context isolation** và
**(2) parallelism** giữa các sub-task độc lập.

| Option | Vì sao sai |
|--------|-----------|
| A | Volume là bài toán *scaling* (horizontal scale, rate limit), giải được ở mọi pattern |
| B | Ngân sách là *fact*, không phải *architectural driver* |
| D | Prestige, không phải driver kỹ thuật |

**Bẫy:** "high volume" nghe có vẻ liên quan nhưng không phải lý do chọn multi-agent.
</details>

---

## Q1.11 · Scenario matching · Chọn pattern

Options: `single augmented LLM call` · `fixed workflow` · `autonomous agent` · `multi-agent system`

1. Tóm tắt mỗi email support thành note CRM, có retrieve account record của khách làm context.
2. Báo cáo compliance hằng tháng, luôn 5 bước: gather → validate → analyse → format → distribute.
3. Điều tra production incident, đường chẩn đoán phụ thuộc hoàn toàn vào kết quả từng log query.
4. Merger review cần đánh giá legal + financial + technical, mỗi mảng có tool và context chuyên biệt, gộp thành 1 khuyến nghị.
5. Dịch mỗi tài liệu sang tiếng Anh với glossary thuật ngữ được duyệt đưa vào context.

<details><summary>👉 Đáp án & giải thích</summary>

| # | Đáp án | Lý do |
|---|--------|-------|
| 1 | single augmented LLM call | Một phép biến đổi (summarize) + context được bổ sung (retrieval) — "augmented" chính là có retrieval/tools/memory |
| 2 | fixed workflow | Chuỗi bước ổn định, lặp lại |
| 3 | autonomous agent | Path phụ thuộc kết quả từng bước |
| 4 | multi-agent system | Nhiều specialist với tool/context riêng, điều phối về một output |
| 5 | single augmented LLM call | Một phép biến đổi (translate) + glossary làm context |

**Lưu ý:** Item 1 có thể bị nghĩ là workflow (retrieve rồi summarize). Nhưng retrieval ở đây chỉ là *augmentation*
cho một bước LLM duy nhất — không có chuỗi nhiều bước LLM → **augmented LLM call**.
Options được dùng lại nhiều lần — đừng giả định map 1:1.
</details>
