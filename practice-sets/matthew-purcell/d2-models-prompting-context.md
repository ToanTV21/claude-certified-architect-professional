# Domain 2 — Claude Models, Prompting & Context Engineering (13% · 8 câu)

> Nguồn: practice set của Matthew Purcell (xem [README](README.md)). Đề được **diễn giải lại bằng tiếng Việt**.

**Chủ đề xuyên suốt:** model selection dựa trên **eval** (không theo cảm tính), **prompt caching** (prefix phải
tĩnh), **context engineering** (đưa đúng thứ cần, đúng vị trí), và **áp dụng kỹ thuật có chọn lọc** (CoT,
few-shot) theo lợi ích đo được.

Note liên quan: [C1.4 model & context strategy](../../courses/01-claude-platform-solution-design/notes/04-model-context-strategy.md) ·
[C1.7 prompting as architecture](../../courses/01-claude-platform-solution-design/notes/07-prompting-as-architecture.md)

---

## Q2.1 · Multiple choice · Model selection cho high-volume classification

**Tình huống:** Hệ thống routing phân loại **400,000 tin nhắn ngắn/ngày** vào 8 category. Accuracy trên labelled
test set **tương đương nhau** giữa các model trong family. Business nhạy cảm với cả latency lẫn cost.

- A. Dùng model mạnh nhất vì lỗi phân loại luôn đắt hơn compute
- B. Dùng model tầm trung cho "an toàn", khỏi cần eval
- C. Dùng model nhỏ nhất đạt accuracy target, và xác nhận lựa chọn bằng evaluation liên tục
- D. Luân phiên ngẫu nhiên giữa các model để trung hoà điểm yếu

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Khi accuracy đã *đo được là tương đương*, ở volume 400k/ngày thì lựa chọn có kỷ luật là
**smallest model that meets the target** (ví dụ Haiku) — nhưng phải có **ongoing eval** để chắc nó tiếp tục đạt.

| Option | Vì sao sai |
|--------|-----------|
| A | "Luôn luôn" = giả định thay cho đo lường; dữ kiện đã cho thấy accuracy ngang nhau |
| B | Né tránh chính cái eval đáng ra phải quyết định lựa chọn |
| D | Hành vi khó đoán, không debug được |

**Signal keyword:** "comparable accuracy" + "sensitive to latency and cost" → **smallest model that passes eval**.
Chữ "validate with ongoing evaluation" là dấu hiệu đáp án chuẩn của CCAR-P.
</details>

---

## Q2.2 · Multiple choice · Prompt caching hit rate ≈ 0

**Tình huống:** App chèn **timestamp + request ID ở đầu** system prompt, sau đó là 9,000 tokens policy tĩnh,
rồi tới message của user. Đã bật prompt caching nhưng **cache hit rate gần như 0**.

- A. Giá trị động ở đầu prompt làm prefix thay đổi mỗi request → không prefix nào khớp cache
- B. Policy content quá dài nên không đủ điều kiện cache
- C. Prompt caching chỉ áp dụng cho user message, không cho system prompt
- D. Cache bị evict vì request gửi quá thường xuyên

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** Prompt caching match theo **prefix** (từ đầu prompt đến cache breakpoint). Timestamp/request ID ở
vị trí 0 làm mọi prefix đều unique → không bao giờ hit. **Fix:** đưa nội dung tĩnh lên đầu (tools → system →
static docs), đặt giá trị động *sau* cache breakpoint.

| Option | Vì sao sai |
|--------|-----------|
| B | Caching có **minimum** length (ví dụ ~1024 tokens tuỳ model), không có giới hạn "quá dài" kiểu này — 9k tokens là rất lý tưởng để cache |
| C | Sai — system prompt (và tools) chính là nơi thường cache nhất |
| D | Request thường xuyên còn giúp cache "ấm" (TTL được refresh mỗi lần hit), không làm hit rate về 0 |

**Rule nhớ nhanh:** *Static first, dynamic last.* Cũng xuất hiện trong bảng Gotcha của CLAUDE.md:
"Cost + latency cùng lúc → Static content trước + prompt caching".
</details>

---

## Q2.3 · Multiple choice · Chain-of-thought áp dụng tràn lan

**Tình huống:** Team áp CoT **đồng loạt** toàn platform. Feature phân tích hợp đồng phức tạp tốt lên, nhưng
endpoint **extract field đơn giản** chậm hơn, đắt hơn, accuracy không tăng.

- A. Bỏ CoT toàn platform vì nó gấp đôi token
- B. Endpoint extraction cần CoT dài hơn mới thấy lợi
- C. CoT chỉ hoạt động trên model lớn nhất
- D. CoT có giá trị cho reasoning nhiều bước, nhưng tốn cost/latency vô ích cho extraction đơn giản → áp dụng chọn lọc

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** Kỹ thuật prompting là **per-task decision dựa trên measured benefit**. CoT (hoặc extended
thinking) đáng tiền với multi-step reasoning, vô ích với extraction đơn giản.

| Option | Vì sao sai |
|--------|-----------|
| A | Vứt bỏ lợi ích đã được chứng minh ở contract analysis |
| B | Tăng đầu tư đúng chỗ không có lợi |
| C | Sai sự thật |

**Pattern CCAR-P:** các đáp án "platform-wide", "always", "never" thường sai — đáp án đúng hay là "selectively,
based on measured benefit".
</details>

---

## Q2.4 · Multiple choice · Rule quan trọng bị chôn giữa context

**Tình huống:** Rule quan trọng "never quote internal pricing" nằm **giữa** 12,000 tokens product context. Rule
được tuân thủ thất thường. Sửa wording không giúp.

- A. Lặp lại rule nguyên văn sau mỗi đoạn context
- B. Chuyển rule lên đầu hoặc cuối prompt, tách rule khỏi reference content bằng cấu trúc rõ ràng
- C. Temperature = 0 để model deterministic
- D. Viết rule bằng CHỮ HOA để model ưu tiên

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Hiện tượng **"lost in the middle"** — thông tin ở giữa context dài được chú ý kém hơn đầu/cuối.
Fix đòn bẩy cao nhất: đặt rule ở **vị trí nổi bật** + **tách cấu trúc** (ví dụ `<rules>` vs `<product_context>` bằng XML tags).

| Option | Vì sao sai |
|--------|-----------|
| A | Phình prompt, làm loãng thêm |
| C | Temperature ảnh hưởng sampling randomness, không ảnh hưởng độ "nổi bật" của rule |
| D | Mê tín — CAPS không phải cơ chế ưu tiên đáng tin (và dễ gây over-trigger) |

**Góc nhìn thêm (quan trọng hơn cho architect):** rule kiểu "never quote internal pricing" là rule **bảo mật dữ liệu**.
Prompt chỉ là lớp đầu; lớp chắc chắn hơn là *không đưa internal pricing vào context* ngay từ đầu, hoặc có
output guardrail chặn. Nếu đề có đáp án kiểu đó, hãy cân nhắc nó (xem Q3.3, Q5.9).
</details>

---

## Q2.5 · Multiple choice · Output format chính xác

**Tình huống:** Report phải đúng house style: thứ tự section cố định, tên heading quy định, bảng theo layout riêng.
Mô tả format bằng lời thì output **gần đúng nhưng không nhất quán**.

- A. Thêm 1–2 few-shot example là output hoàn chỉnh, đúng format
- B. Tăng max output tokens để model có chỗ follow format
- C. Tăng temperature để model linh hoạt hơn khi hiểu style
- D. Tách report thành nhiều request, mỗi section một request rồi ghép

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** Với format compliance, **show beats tell** — ví dụ hoàn chỉnh cho model một target cụ thể mà mô
tả bằng văn xuôi không làm được.

| Option | Vì sao sai |
|--------|-----------|
| B | Giải quyết độ dài, không phải độ chính xác format |
| C | Tăng biến thiên — ngược với nhu cầu |
| D | Thêm engineering mà format từng section vẫn không cố định |

**So sánh với Q1.3:** Q1.3 few-shot là *sai* (vấn đề coverage/structure); Q2.5 few-shot là *đúng* (vấn đề format).
→ Few-shot = công cụ cho **format/style/edge-case behaviour**, không phải cho **thiếu sót/coverage**.
</details>

---

## Q2.6 · Multiple choice · Context stuffing 150k tokens

**Tình huống:** Assistant trả lời câu hỏi về bộ tiêu chuẩn kỹ thuật 150,000 tokens bằng cách **nhét cả bộ vào
context mỗi request**. Câu trả lời trích dẫn nội dung **ở giữa** kém tin cậy, và cost/request cao.

- A. Chuyển câu hỏi của user lên đầu prompt, trên bộ tài liệu
- B. Bảo model đọc tài liệu hai lần trước khi trả lời
- C. Chỉ retrieve các section liên quan tới câu hỏi và đưa vào
- D. Nén tài liệu bằng cách bỏ heading và whitespace

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Một thay đổi giải quyết **cả 2 vấn đề**: tránh "lost in the middle" (context ngắn, liên quan) và
giảm token/request mạnh.

| Option | Vì sao sai |
|--------|-----------|
| A | Gần như không cải thiện recall; không giảm cost. (Thực tế Anthropic khuyên đặt *query ở cuối*, sau tài liệu dài) |
| B | Không giảm cost, tăng latency |
| D | Tiết kiệm không đáng kể, phá cấu trúc tài liệu (heading giúp model định vị) |

**Signal keyword:** đề nêu **2 vấn đề** → chọn đáp án giải được **cả hai** cùng lúc.
</details>

---

## Q2.7 · Multiple response (chọn 2) · Giảm cost/request mà giữ capability

**Tình huống:** App volume lớn, prompt lớn và phần lớn tĩnh, cost/request tăng.

- A. Cấu trúc prompt để static prefix cache được, bật prompt caching
- B. Tăng max output tokens để giảm số follow-up request
- C. Thêm few-shot để model đúng ngay lần đầu
- D. Load instruction chuyên biệt khi cần (modular prompt hoặc Skills) thay vì đưa mọi instruction vào mọi request
- E. Chuyển toàn bộ static content từ system prompt sang user message

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A, D**

**Vì sao đúng:** (A) cache làm phần lặp lại rẻ đi đáng kể (cache read rẻ hơn nhiều so với input thường);
(D) **progressive disclosure** — mỗi request chỉ trả tiền cho instruction nó cần (đây chính là triết lý của Agent Skills).

| Option | Vì sao sai |
|--------|-----------|
| B | Tăng token usage |
| C | Thêm token vào *mọi* request |
| E | Chỉ dời chỗ cùng số token, không giảm gì (còn có thể phá cache nếu đặt sau phần động) |
</details>

---

## Q2.8 · Multiple response (chọn 2) · Cải thiện instruction adherence

**Tình huống:** System prompt cho hành vi không nhất quán. Hai practice nào cải thiện adherence tốt nhất?

- A. Tăng temperature để model khám phá nhiều cách hiểu
- B. Tổ chức prompt thành section phân tách rõ, có thứ tự ưu tiên tường minh khi rule xung đột
- C. Đặt rule quan trọng nhất ở giữa prompt vì model chú ý nhiều nhất ở đó
- D. Bỏ hết cấu trúc để prompt đọc như văn xuôi tự nhiên
- E. Thêm ví dụ cụ thể về cách xử lý đúng cho các case model hay sai

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B, E**

**Vì sao đúng:** (B) cấu trúc + **explicit conflict priority** loại bỏ mơ hồ (liên hệ Q4.10 item 2: "concise" vs
"explain in detail" xung đột → prompt failure); (E) ví dụ đúng cho *đúng các case đang fail* neo hành vi mong muốn.

| Option | Vì sao sai |
|--------|-----------|
| A | Thêm variance |
| C | Ngược — giữa là vị trí chú ý **yếu nhất** (lost in the middle) |
| D | Bỏ đi cấu trúc vốn giúp adherence |
</details>
