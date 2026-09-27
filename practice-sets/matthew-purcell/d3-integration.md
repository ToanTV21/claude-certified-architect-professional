# Domain 3 — Integration (19% · 12 câu) — domain nặng nhất

> Nguồn: practice set của Matthew Purcell (xem [README](README.md)). Đề được **diễn giải lại bằng tiếng Việt**.

**Chủ đề xuyên suốt:** MCP vs direct API vs agent-to-agent · tool design (ít, rõ ràng, không chồng lấn) ·
**authorization ở system layer, không ở prompt** · RAG (chunking, hybrid retrieval, re-ranking, re-indexing) ·
observability ở quy mô lớn.

Note liên quan: [C2.4 enterprise integration architecture](../../courses/02-enterprise-integration-production/notes/04-enterprise-integration-architecture.md) ·
[C1.8 entry point, MCP reuse, compliance](../../courses/01-claude-platform-solution-design/notes/08-entry-point-mcp-compliance-case-study.md) ·
[C1.3 reference architecture patterns (chunking/indexing)](../../courses/01-claude-platform-solution-design/notes/03-reference-architecture-patterns.md)

---

## Q3.1 · Multiple choice · Kết nối 12 hệ thống nội bộ

**Tình huống:** Doanh nghiệp nối Claude với 12 hệ thống nội bộ (CRM, ticketing, HR, inventory...). Mỗi hệ thống
do **team khác nhau sở hữu**, tool được **thêm/bỏ thường xuyên**, và **nhiều AI app** trong công ty cần
**tái sử dụng** cùng kết nối.

- A. Hard-code REST API của từng hệ thống vào tool definition của từng app
- B. Dựng một middleware custom bọc cả 12 hệ thống sau một endpoint duy nhất
- C. Expose mỗi hệ thống qua MCP server, app nào cũng connect được
- D. Cấp cho Claude quyền truy cập database trực tiếp để khỏi bảo trì API

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** MCP sinh ra cho đúng "hình dạng" này: **N hệ thống × M app**, ownership phi tập trung, tool thay đổi
thường xuyên. Mỗi team maintain MCP server của mình **một lần**, mọi app tái sử dụng (giảm N×M thành N+M).

| Option | Vì sao sai |
|--------|-----------|
| A | Chi phí bảo trì nhân theo số app (N×M) |
| B | Tạo team "cổ chai" + single point of failure; ownership bị tập trung trái với thực tế tổ chức |
| D | Bypass business logic và access control — anti-pattern bảo mật |

**Signal keyword:** "multiple applications", "reuse", "different teams own", "added and retired frequently" → **MCP**.
</details>

---

## Q3.2 · Multiple choice · 45 tools, 1/3 chưa từng được gọi

**Tình huống:** Agent có **45 tools** trải 6 domain. Accuracy chọn tool giảm, latency tăng; phân tích cho thấy
**1/3 số tool chưa bao giờ được gọi** trong production. Architect nên làm gì **trước tiên**?

- A. Viết description dài hơn cho cả 45 tool
- B. Nâng cấp model mạnh hơn để chịu được catalogue lớn
- C. Bắt model liệt kê cả 45 tool và giải thích lựa chọn trước mỗi lần gọi
- D. Audit và gỡ tool không dùng/chồng lấn, cân nhắc progressive discovery để mỗi request chỉ thấy tool liên quan

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** Đây là **capability bloat**. Gỡ tool chết/trùng khôi phục accuracy trực tiếp; progressive discovery
(tool search, load theo nhu cầu) giữ "bề mặt tool" mỗi request nhỏ khi catalogue lớn dần.

| Option | Vì sao sai |
|--------|-----------|
| A | Thêm context mà không giảm nhầm lẫn |
| B | Chữa triệu chứng với giá cao hơn |
| C | Thêm latency + token cho *mọi* call |

**Liên hệ gotcha "least privilege":** gỡ hẳn capability không cần, đừng chỉ "mô tả kỹ hơn". So sánh với Q1.8.
</details>

---

## Q3.3 · Multiple choice · Authorization bằng prompt ⚠️ câu rất hay thi

**Tình huống:** Assistant truy vấn hệ thống HR thay mặt nhân viên. Nó xác thực bằng **một service account có
quyền đọc toàn tổ chức**, và system prompt dặn model **chỉ trả dữ liệu của chính nhân viên đang hỏi**.
Security review flag thiết kế này. Vấn đề cốt lõi?

- A. Authorization đang được thực thi bằng prompt thay vì access-control layer → prompt fail hoặc injection có thể lộ dữ liệu bất kỳ nhân viên nào
- B. Service account không được dùng với AI theo hầu hết compliance framework
- C. Service account nên có thêm quyền ghi để audit log đầy đủ
- D. Model nên xác thực trực tiếp vào HR bằng password của từng nhân viên

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** **Prompt instruction không phải security boundary.** Access control phải được enforce ở system
layer: credential scoped theo user, hoặc **pass-through auth** (OAuth on-behalf-of) → *model không thể trả về cái
nó không thể retrieve*.

| Option | Vì sao sai |
|--------|-----------|
| B | Không phải quy tắc compliance có thật |
| C | Mở rộng blast radius — ngược nguyên tắc least privilege |
| D | Anti-pattern xử lý credential (model không bao giờ được cầm password người dùng) |

**Rule vàng CCAR-P:** "Ai được thấy gì" → **enforce deterministically ở tầng hệ thống**. Prompt chỉ là lớp hướng
dẫn hành vi, không phải lớp bảo vệ. Liên hệ Q5.5, Q5.8.
</details>

---

## Q3.4 · Multiple choice · Chunking hợp đồng

**Tình huống:** RAG trên hợp đồng thương mại dùng chunk **cố định 300 tokens**. Retrieval hay trả về mảnh điều
khoản mà nghĩa **phụ thuộc vào definition và cross-reference** ở chỗ khác trong tài liệu.

- A. Giảm chunk xuống 100 tokens cho precise hơn
- B. Structure-aware chunking theo clause/section, kèm metadata liên kết definition và cross-reference
- C. Tăng số chunk retrieve từ 5 lên 50 để "chắc có" context thiếu
- D. Thay retrieval bằng keyword index chỉ trên heading điều khoản

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Lỗi mang tính **cấu trúc**: chunk cố định cắt đứt điều khoản khỏi definition. Chunk theo cấu trúc
tài liệu (clause/section) + metadata liên kết giữ được ngữ cảnh diễn giải. (Kỹ thuật liên quan: contextual
retrieval — thêm context mô tả vào mỗi chunk trước khi embed.)

| Option | Vì sao sai |
|--------|-----------|
| A | Làm phân mảnh tệ hơn |
| C | Nhồi context, trông vào may mắn; tốn token, gây nhiễu |
| D | Bỏ semantic retrieval vốn đang chạy tốt cho các query khác |
</details>

---

## Q3.5 · Multiple choice · Tìm theo mã part number

**Tình huống:** Assistant tra cứu linh kiện dùng **thuần semantic (vector) retrieval**. User tìm theo **mã chính
xác** như "KX-2481-B" thường nhận kết quả linh kiện *tương tự nhưng sai*; query ngôn ngữ tự nhiên thì tốt.

- A. Thuần keyword search, bỏ hẳn semantic
- B. Embedding model lớn hơn để part number embed khác biệt hơn
- C. Bảo user mô tả bằng ngôn ngữ tự nhiên thay vì mã
- D. Hybrid retrieval: keyword/exact match + semantic, weight theo loại query

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** **Exact identifier → lexical (BM25/keyword) thắng**, embedding làm "mờ" mã; **ngôn ngữ tự nhiên →
semantic thắng**. Hybrid ghép cả hai theo hình dạng query.

| Option | Vì sao sai |
|--------|-----------|
| A | Phá vỡ các query tự nhiên đang chạy tốt |
| B | Cải thiện biên cho một vấn đề bản chất là *lexical* |
| C | Đẩy lỗi hệ thống sang người dùng |

**Signal keyword:** ID/SKU/mã lỗi/tên riêng + vector search fail → **hybrid**.
</details>

---

## Q3.6 · Multiple choice · Re-ranking: accuracy vs latency

**Tình huống:** Thêm **re-ranking** tăng accuracy **86% → 93%** nhưng thêm **500 ms** latency. SLA hợp đồng:
**3 giây**; p95 hiện tại **1.6 giây**.

- A. Dùng re-ranking: lợi ích accuracy đáng kể, latency sau khi thêm vẫn còn dư headroom so với SLA
- B. Từ chối: không bao giờ chấp nhận tăng latency ở hệ thống customer-facing
- C. Chỉ dùng re-ranking cho nhóm nhỏ query không chịu SLA
- D. Hoãn quyết định đến khi đàm phán lại SLA

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** Framework: **lượng hoá cả hai phía so với SLA**. 1.6s + 0.5s ≈ **2.1s < 3s** → còn ~0.9s
headroom; +7 điểm accuracy là đáng kể → adopt và monitor p95.

| Option | Vì sao sai |
|--------|-----------|
| B | Giáo điều ("never"), không phải phân tích |
| C | Phân mảnh hành vi tuỳ tiện |
| D | Hoãn một quyết định mà dữ liệu đã đủ để ra |

**Mẹo làm bài:** đề cho số liệu → **làm phép tính**. Nếu 1.6 + 0.5 vượt SLA thì đáp án sẽ khác.
</details>

---

## Q3.7 · Multiple choice · Observability ở quy mô hàng chục nghìn session/ngày

**Tình huống:** Platform chạy **hàng chục nghìn agent session/ngày**. Đang log **toàn bộ** prompt, response, tool
payload — tốn kém mà vẫn khó tìm lỗi.

- A. Tắt logging ở production, tái hiện lỗi ở staging
- B. Chỉ log response cuối cùng của mỗi session
- C. Structured trace với correlation ID + key metrics cho mọi session; full payload chỉ capture theo sample và khi có lỗi
- D. Dựa vào phàn nàn của user làm cơ chế phát hiện lỗi chính

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Observability ở scale = **trace + metrics cho tất cả** (rẻ, tìm được) + **full payload có chọn lọc**
(sampled + error-triggered). Correlation ID nối các step của một session để dựng lại chuỗi agent.

| Option | Vì sao sai |
|--------|-----------|
| A | Mất đúng context production gây ra lỗi |
| B | Vứt các bước trung gian — nơi agent hay fail nhất |
| D | Lagging indicator, tổn hại uy tín |

Liên hệ Q7.3 (debug bằng trace) và Q4.9.
</details>

---

## Q3.8 · Multiple choice · Hai agent của hai công ty

**Tình huống:** Procurement agent của công ty A phải đàm phán lịch giao hàng với scheduling agent **do nhà cung
cấp vận hành độc lập**. Không bên nào chịu expose tool/hệ thống nội bộ cho bên kia.

- A. Đăng ký tool nội bộ của nhà cung cấp trực tiếp vào tool catalogue của procurement agent
- B. Agent-to-agent communication qua một protocol boundary thống nhất, mỗi agent tự làm trung gian truy cập hệ thống của tổ chức mình
- C. Cho mỗi agent quyền đọc database lịch của bên kia
- D. Thay cả hai bằng một agent dùng chung do bên thứ ba vận hành

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Phối hợp **xuyên tổ chức** mà **không lộ nội bộ** = use case định nghĩa của **agent-to-agent (A2A)**:
mỗi agent chính là ranh giới bảo vệ hệ thống của mình.

| Option | Vì sao sai |
|--------|-----------|
| A | Lộ đúng thứ mà hai bên không chịu lộ |
| C | Lộ hệ thống nội bộ qua trust boundary |
| D | Đòi hỏi mô hình vận hành không ai yêu cầu |

**Phân biệt nhanh:** MCP = *agent ↔ tool/data* (trong trust boundary). A2A = *agent ↔ agent* (thường xuyên trust boundary).
</details>

---

## Q3.9 · Multiple response (chọn 2) · RAG trả lời từ nội dung cũ sau refresh

**Tình huống:** Sau mỗi lần refresh tài liệu ban đêm, RAG assistant **thỉnh thoảng** trả lời từ nội dung đã bị thay thế.

- A. Context window lớn hơn để retrieve nhiều tài liệu hơn
- B. Spot-check thủ công 10 câu trả lời ngẫu nhiên mỗi tuần
- C. Pipeline re-index tự động, validate completeness và embedding consistency sau mỗi lần refresh
- D. Metadata versioning trong index, retrieval lọc bỏ version cũ
- E. Giảm temperature để model ít dựa vào retrieved content

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C, D**

**Vì sao đúng:** Lỗi nằm ở **retrieval/indexing**, không ở model (đúng gotcha trong CLAUDE.md: "RAG trả lời sai sau
data refresh → kiểm tra retrieval/indexing trước"). (C) chặn embedding stale đi vào index; (D) đảm bảo chunk cũ
còn sót cũng không được serve.

| Option | Vì sao sai |
|--------|-----------|
| A | Retrieve nhiều hơn… nội dung cũ |
| B | Quá chậm, quá thưa để bắt lỗi xảy ra hằng đêm |
| E | Không thay đổi *cái gì* được retrieve |
</details>

---

## Q3.10 · Multiple response (chọn 2) · Agent chọn nhầm tool giữa các tool na ná

- A. Viết lại description để mục đích, input, ranh giới của từng tool rõ ràng và không chồng lấn
- B. Thêm tool chi tiết hơn để mọi edge case có tool riêng
- C. Bảo model luôn chọn tool đầu tiên khi phân vân
- D. Dồn mọi tool call qua một tool `execute` chung nhận lệnh free-text
- E. Gộp hoặc gỡ các tool trùng chức năng

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A, E**

**Vì sao đúng:** Chọn nhầm giữa tool liên quan = do **overlap + ambiguity** → (A) làm rõ ranh giới (description
tốt: làm gì, *khi nào dùng*, *khi nào không dùng*, input), (E) xoá overlap tận gốc.

| Option | Vì sao sai |
|--------|-----------|
| B | Tăng bề mặt nhầm lẫn |
| C | Thể chế hoá lựa chọn sai |
| D | Bỏ typed interface (input schema) → lỗi khó bắt, rủi ro bảo mật cao |
</details>

---

## Q3.11 · Multiple response (chọn 2) · Progressive discovery vs monolithic context

- A. Solution dùng 3 tool, cả 3 đều cần cho mọi request
- B. Catalogue tool + tài liệu tham khảo lớn, mỗi request chỉ cần một phần nhỏ
- C. Request phải hoàn tất trong 1 lần gọi model, không có bước trung gian
- D. Context budget hạn chế, nhồi hết từ đầu làm giảm chất lượng
- E. Tài liệu tham khảo không bao giờ đổi và vừa vặn trong context window

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B, D**

**Vì sao đúng:** Progressive discovery có lợi khi **(B) chỉ một lát nhỏ của catalogue lớn là liên quan** và
**(D) nhồi hết làm hỏng chất lượng / vỡ budget**.

| Option | Vì sao sai |
|--------|-----------|
| A | Monolithic đơn giản và ổn |
| C | Progressive discovery *cần* bước trung gian (tìm → load → dùng) |
| E | Monolithic ổn (thậm chí cache được) |
</details>

---

## Q3.12 · Scenario matching · Chọn cơ chế kết nối

Options: `MCP server` · `direct API integration` · `agent-to-agent protocol`

1. Nhiều AI app trong công ty cần truy cập chuẩn hoá, tái sử dụng tới hệ thống ticketing nội bộ.
2. Batch job ban đêm deterministic đẩy record vào data warehouse, **không có model** tham gia việc chuyển dữ liệu.
3. Hai agent tự trị thuộc hai công ty cần phối hợp logistics mà không lộ hệ thống nội bộ.
4. Knowledge base nội bộ mới cần được **mọi agent hiện tại và tương lai** discover và dùng.
5. Một microservice có sẵn cần gọi model **một lần** để phân loại tài liệu trong pipeline kiểm soát chặt của nó.

<details><summary>👉 Đáp án & giải thích</summary>

| # | Đáp án | Lý do |
|---|--------|-------|
| 1 | MCP server | Nhiều consumer, reusable, chuẩn hoá |
| 2 | direct API integration | Deterministic, không có model → không cần lớp discovery |
| 3 | agent-to-agent protocol | Vượt trust boundary giữa các agent tự trị |
| 4 | MCP server | "Discoverable by any current or future agent" |
| 5 | direct API integration | Gọi Messages API trực tiếp, phạm vi hẹp, trong pipeline tự sở hữu |

**Rule:** *nhiều consumer + discover* → MCP · *deterministic, scope hẹp, pipeline riêng* → direct API ·
*agent ↔ agent xuyên tổ chức* → A2A.
</details>
