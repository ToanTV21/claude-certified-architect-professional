# Flashcards — CCAR-P

Format: **Q:** ... / **A:** ...

## Domain 3 — Integration
- **Q:** Agent hỗ trợ khách hàng có tool đọc ticket, soạn reply, hoàn tiền, xóa account — nhưng support staff chỉ cần đọc + soạn reply. Áp dụng least-privilege thì nên làm gì?
  **A:** Gỡ bỏ hoàn toàn tool hoàn tiền và xóa account khỏi config của agent (loại bỏ capability thừa, không chỉ log/confirm).

## Domain 2 — Models, Prompting & Context
- **Q:** App gửi cùng 1 system prompt + policy doc 8000 token mỗi request, kèm user message ngắn thay đổi. Cần giảm cả latency lẫn cost — làm gì?
  **A:** Đặt static content (system prompt + policy) trước, dynamic content sau, và bật prompt caching.

## Domain 4 — Evaluation & Optimization
- **Q:** RAG system trả lời confident nhưng sai sau khi refresh document, latency và model version không đổi — nên kiểm tra đâu đầu tiên?
  **A:** Bước retrieval/indexing — khả năng cao đang trả về chunks không liên quan hoặc stale (broken re-index, mismatched embeddings).

---
Thêm flashcard mới khi học domain mới hoặc gặp câu hỏi sai trong mock exam.
