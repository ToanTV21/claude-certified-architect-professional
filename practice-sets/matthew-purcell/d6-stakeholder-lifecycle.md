# Domain 6 — Stakeholder Communication & Lifecycle Management (14% · 9 câu)

> Nguồn: practice set của Matthew Purcell (xem [README](README.md)). Đề được **diễn giải lại bằng tiếng Việt**.

**Chủ đề xuyên suốt:** **discovery trước solution** · biến yêu cầu tuyệt đối thành **acceptance criteria đo được** ·
**trình bày trade-off có bằng chứng**, để người chịu trách nhiệm quyết định · report theo **business outcome** ·
**change control** minh bạch · handoff = **ADR + runbook + eval baseline**.

Note liên quan: [C4.1 structured discovery](../../courses/04-stakeholder-engagement-lifecycle-gtm/notes/01-structured-discovery.md) ·
[C4.2 presenting trade-offs](../../courses/04-stakeholder-engagement-lifecycle-gtm/notes/02-presenting-tradeoffs.md) ·
[C4.3 lifecycle feedback loops](../../courses/04-stakeholder-engagement-lifecycle-gtm/notes/03-lifecycle-feedback-loops.md)

**Công thức chung cho mọi câu "stakeholder đòi X không khả thi":**
> Không đồng ý mù quáng · không từ chối thẳng · không làm lén → **đưa bằng chứng + đề xuất phương án + để người có thẩm quyền quyết định**.

---

## Q6.1 · Multiple choice · Sponsor đòi "100% accurate"

- A. Đồng ý và thêm giai đoạn test đến khi đạt 100%
- B. Giải thích LLM là probabilistic, rồi cùng sponsor định nghĩa acceptance criteria đo được + chiến lược xử lý lỗi theo mức rủi ro nghiệp vụ
- C. Từ chối dự án vì không đáp ứng được
- D. Đề xuất model nhỏ hơn để giảm rủi ro lỗi

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Việc của architect là **chuyển một yêu cầu tuyệt đối không đạt được thành một thoả thuận đạt được**:
hệ thống probabilistic + tiêu chí đo được + error handling (HITL, fallback, escalation) tương xứng rủi ro.

| Option | Vì sao sai |
|--------|-----------|
| A | Cam kết điều bất khả |
| C | Bỏ đi một cuộc trò chuyện giải quyết được |
| D | Model nhỏ thường *tăng* lỗi; và dù sao cũng chỉ đổi error rate, không đổi kỳ vọng |
</details>

---

## Q6.2 · Multiple choice · "Chúng tôi cần một chatbot cho intranet"

- A. Làm báo giá fixed-price cho chatbot intranet chuẩn
- B. Build prototype ngay để có cái cụ thể mà bàn
- C. Structured discovery: xác định vấn đề nghiệp vụ gốc, người dùng, thước đo thành công, bức tranh dữ liệu, ràng buộc — chatbot có thể đúng hoặc không
- D. Hỏi client đã thấy chatbot nào của đối thủ rồi làm y hệt

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** "Cần chatbot" là **giải pháp được đề xuất**, không phải **problem statement**. Discovery xác lập
vấn đề, user, success measure, constraints → chatbot có thể sống sót qua quá trình đó, hoặc lộ ra thứ tốt hơn
(ví dụ: search tốt hơn, workflow tự động, hay chỉ cần sửa tài liệu).

| Option | Vì sao sai |
|--------|-----------|
| A | Định giá một giải pháp chưa được kiểm chứng |
| B | Neo mọi người vào giải pháp (anchoring) trước khi hiểu vấn đề |
| D | Giao phó tư duy cho đối thủ |
</details>

---

## Q6.3 · Multiple choice · CFO bắt dùng model rẻ nhất cho báo cáo pháp định

**Tình huống:** CFO chỉ đạo dùng model rẻ nhất cho giải pháp phân tích tài liệu phục vụ **regulatory reporting**.
Test nội bộ cho thấy model rẻ nhất có **error rate cao hơn đáng kể**.

- A. Trình bày trade-off có bằng chứng — error rate, rework downstream, rủi ro pháp lý so với khoản tiết kiệm — đề xuất decision framework, để stakeholder chịu trách nhiệm quyết định với đầy đủ thông tin
- B. Âm thầm dùng model mạnh hơn và bù chi phí chỗ khác
- C. Làm theo không bình luận vì cost là việc của CFO
- D. Escalate vượt cấp lên audit committee của board

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** **Evidence-based trade-off communication**: lượng hoá quality, rework, regulatory exposure so với
khoản tiết kiệm → khuyến nghị → **người chịu trách nhiệm quyết định có thông tin**. Theo công thức course:
mỗi option kèm **cost + risk + reversal cost**.

| Option | Vì sao sai |
|--------|-----------|
| B | Lừa dối — phá niềm tin |
| C | Giấu thông tin quan trọng với người ra quyết định |
| D | Escalate khi chưa hề nói chuyện trực tiếp |

**Ghi nhớ:** Architect **advise**, business owner **decide**. Đáp án đúng hiếm khi là "tự quyết thay" hoặc "im lặng làm theo".
</details>

---

## Q6.4 · Multiple choice · Stakeholder đòi phản hồi dưới 1 giây

**Tình huống:** Pipeline multi-step retrieval + reasoning, phân tích cho thấy **không thể dưới 3 giây**, stakeholder đòi **sub-second**.

- A. Nhận yêu cầu, hy vọng tối ưu sau sẽ bù
- B. Bỏ bước retrieval và reasoning để đạt target
- C. Cam kết sub-second chỉ cho demo
- D. Trình bày latency breakdown, đàm phán SLA phản ánh thực tế pipeline, đề xuất cải thiện trải nghiệm như streaming và progress indicator

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** Quản lý kỳ vọng dựa trên **thực tế kỹ thuật** (latency budget từng bước) + SLA khả thi + cải thiện
**perceived latency** (streaming → time-to-first-token thấp, progress indicator).

| Option | Vì sao sai |
|--------|-----------|
| A | Ký cam kết để trượt |
| B | Hy sinh chính năng lực biện minh cho hệ thống |
| C | Đảm bảo khoảng cách sẽ lộ ra ở production |
</details>

---

## Q6.5 · Multiple choice · Handoff cho team nội bộ của client

- A. Bản ghi hình buổi demo cuối
- B. Toàn bộ lịch sử các bản nháp prompt
- C. Tài liệu kiến trúc + decision record giải thích trade-off, operational runbook, eval baseline team có thể chạy lại
- D. Danh sách feature đã cân nhắc nhưng không làm

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C**

**Vì sao đúng:** Team nhận cần **vận hành + tiến hoá** hệ thống: **ADR** = *vì sao* nó như vậy; **runbook** = *làm
sao* giữ nó chạy; **eval baseline** = *kiểm chứng* thay đổi an toàn (không có baseline thì không biết thay đổi sau
làm tốt hơn hay tệ hơn).

A, B, D: là "hiện vật của hành trình", không phải công cụ để sở hữu và vận hành.
</details>

---

## Q6.6 · Multiple choice · Sponsor mất hứng vì report toàn metric kỹ thuật

**Tình huống:** 2 tháng sau launch, report 2 tuần/lần chỉ có token spend, latency, uptime → sponsor giảm nhiệt.

- A. Report theo business success criteria đã thống nhất ở discovery (giờ tiết kiệm, resolution rate, giảm lỗi), metric kỹ thuật làm phụ lục
- B. Tăng tần suất report lên hằng ngày
- C. Bỏ report, dựa vào trao đổi ad-hoc
- D. Thêm metric kỹ thuật cho report trông kỹ hơn

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** Sponsor **tài trợ cho business outcome** → report phải dẫn đầu bằng success criteria đã thống nhất,
kỹ thuật làm bằng chứng phụ. Điều này **khép vòng feedback** duy trì sự tài trợ.

B, D: nhiều hơn của *nội dung sai*. C: xoá luôn vòng feedback.

**Liên kết:** success criteria ở discovery (Q6.7) → được dùng lại để report (Q6.6) → và để ưu tiên iteration (Q6.9 item 4). Đây là một mạch xuyên suốt lifecycle.
</details>

---

## Q6.7 · Multiple response (chọn 2) · Output của discovery trước khi design

- A. Success criteria đo được và ngưỡng chấp nhận gắn với vấn đề nghiệp vụ
- B. System prompt production cuối cùng
- C. Đánh giá data availability, quality, access constraint, và nghĩa vụ compliance
- D. Model version cụ thể sẽ pin ở production
- E. Thiết kế giao diện UI

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A, C**

**Vì sao đúng:** Mọi quyết định design treo vào **2 cái neo**: (A) thành công nghĩa là gì (đo được), (C) bức tranh
dữ liệu cho phép gì (availability, quality, access, compliance).

| Option | Vì sao sai |
|--------|-----------|
| B | Output của design/build |
| D | Output của design/build — quá sớm ở discovery (chọn model phải dựa trên eval) |
| E | Nằm downstream của cả A và C |

**Mẹo:** câu hỏi về "phase X" → loại mọi đáp án thuộc phase sau.
</details>

---

## Q6.8 · Multiple response (chọn 2) · Scope creep giữa dự án

**Tình huống:** Giữa lúc build, stakeholder liên tục xin thêm: data source mới, nhóm user mới, format output mới.

- A. Âm thầm nhận hết để stakeholder vui
- B. Đánh giá từng request so với success criteria và scope baseline, **làm rõ impact** trước khi nhận
- C. Từ chối mọi thay đổi đến khi scope gốc ship xong
- D. Nhận làm nhưng lặng lẽ giảm testing để kịp tiến độ
- E. Re-baseline timeline, cost, risk có sponsor sign-off khi thay đổi được chấp nhận làm thay đổi đáng kể kế hoạch

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B, E**

**Vì sao đúng:** Change management lành mạnh: **(B) impact minh bạch** so với baseline, **(E) re-baseline chính thức**
khi thay đổi làm dịch kế hoạch → quan hệ bền vì **không có gì bị giấu**.

| Option | Vì sao sai |
|--------|-----------|
| A | Âm thầm bào mòn dự án |
| C | Bào mòn quan hệ (quá cứng) |
| D | Đánh đổi chất lượng lấy tiến độ trong bóng tối |

**Pattern:** các đáp án có chữ **"silently / quietly"** gần như luôn sai trong domain 6.
</details>

---

## Q6.9 · Scenario matching · Hoạt động thuộc phase nào

Options: `discovery` · `design` · `handoff` · `monitoring and iteration`

1. Phỏng vấn nhân viên tuyến đầu để hiểu hiện nay báo giá được làm thế nào và mất thời gian ở đâu.
2. Chọn retrieval strategy và định nghĩa guardrail architecture cho use case đã thống nhất.
3. Hướng dẫn engineer của client qua runbook và chuyển giao quyền sở hữu vận hành.
4. Xem xu hướng eval ở production và ưu tiên vòng cải tiến prompt tiếp theo.
5. Tổ chức workshop thống nhất "thành công" nghĩa là gì và đo thế nào.

<details><summary>👉 Đáp án & giải thích</summary>

| # | Đáp án | Lý do |
|---|--------|-------|
| 1 | discovery | Hiểu hiện trạng, pain point |
| 2 | design | Lựa chọn kiến trúc theo requirement đã thống nhất |
| 3 | handoff | Chuyển giao ownership vận hành |
| 4 | monitoring and iteration | Dùng bằng chứng production để lái vòng cải tiến |
| 5 | discovery | Định nghĩa success criteria |

**Bẫy:** item 5 dễ bị xếp vào design vì "workshop" nghe như hoạt động thiết kế — nhưng *định nghĩa thành công* luôn thuộc **discovery**.
</details>
