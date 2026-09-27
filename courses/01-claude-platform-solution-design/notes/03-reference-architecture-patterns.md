# C1.3 — Reference architecture patterns & retrieval vs. live-state

> **Course:** 1 — Claude Platform & Solution Design (238 min) · **Exam domain:** D1 (17%) + D3 (19%) · **Status:** 🟨 Đang học

## Learning objective (nguyên văn từ course)
> Pick a reference architecture pattern for the problem shape in front of you and recognize when retrieval is doing a job that live-state should own

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)

### Screen: Chunking and indexing
Đây là screen đào sâu vào bên trong pipeline retrieval của RAG (tiếp nối screen trước về
reference architectures đã gọi tên RAG là một known-good shape, và chỉ ra khi nào nó bị
misapplied). Hai quyết định thiết kế cốt lõi: **chunking** (chia corpus) và **indexing**
(đánh index để tìm được chunk).

**Chunking — chia theo cấu trúc của corpus, không chia theo default size:**
- **Fixed-size**: chia thành các đoạn đều nhau (có overlap), bất kể cấu trúc văn bản.
  Dùng khi corpus là text đồng nhất, không có structure rõ ràng (natural boundaries yếu) —
  đơn giản nhất để vận hành.
- **Semantic**: chia theo ranh giới ý nghĩa (topic shift, nhóm câu có liên kết ngữ nghĩa).
  Dùng cho prose mà chunk trả về phải tự đủ nghĩa (self-contained) để trả lời được — giảm
  tình trạng cắt giữa ý (mid-idea cuts).
- **Hierarchical**: giữ nguyên cấu trúc document (section, subsection), retrieve ở đúng
  level phù hợp. Dùng cho document có structure rõ (hợp đồng, manual, policy) — nơi ngữ
  cảnh section mang ý nghĩa quan trọng.

**Indexing — chọn theo query pattern, vì indexing quyết định "similar" nghĩa là gì khi có
query tới:**
- **Dense (embeddings)**: match theo semantic similarity (ý nghĩa, không phải từ). Dùng khi
  query được diễn đạt khác với nguồn — paraphrase, intent, concept matching.
- **Sparse (keyword, vd BM25)**: match theo exact terms — identifier, mã, tên riêng. Dùng
  khi query phụ thuộc vào token cụ thể: part number, statute citation, error code.
- **Hybrid**: kết hợp cả hai, rồi merge kết quả. Dùng cho mixed query pattern — trường hợp
  phổ biến nhất trong production; hybrid cứu lại các exact-match result mà dense-only bỏ sót.

Khi hybrid index trả về 2 ranked list (từ dense và sparse), phải merge thành 1. **Reciprocal
rank fusion (RRF)** là cách chuẩn, ít phải tune: mỗi kết quả được chấm điểm theo rank của nó
trong từng list, điểm tổng hợp ưu tiên item rank tốt ở cả hai. Điểm mấu chốt cho architect:
việc combine dense + sparse là một design decision có default đã được kiểm chứng
(known, defensible default), không phải việc tự phát minh lại.

**Articulating the trade-off — mọi retrieval design đều đánh đổi giữa 3 trục:**
1. **Retrieval quality** — chunk đúng có được trả về không?
2. **Latency** — retrieval cộng thêm bao nhiêu thời gian cho mỗi request?
3. **Maintenance** — pipeline tốn bao nhiêu công để giữ đúng khi corpus phình ra / thay đổi?

Chunk nhỏ hơn + hybrid indexing → tăng quality và latency cùng lúc. Chunk lớn hơn +
dense-only → giảm latency và maintenance nhưng bỏ sót exact-match query. Không có điểm
"đúng tuyệt đối" — chỉ có điểm phù hợp với corpus và query pattern cụ thể, và phải trình
bày được nó như một trade-off có thể bảo vệ (defensible) trước stakeholder.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Fixed-size chunking | Corpus text đồng nhất, không có structure rõ; cần đơn giản, dễ vận hành | Thấp nhất — không cần parse structure | Cắt giữa ý (mid-idea cut) → chunk thiếu ngữ cảnh, trả lời sai/thiếu | Thấp — chỉ cần re-chunk lại, không đổi kiến trúc |
| Semantic chunking | Prose cần chunk tự đủ nghĩa để trả lời đúng | Trung bình — cần thêm bước phân tích ranh giới ngữ nghĩa (thường dùng model/embedding) | Ranh giới ngữ nghĩa có thể sai nếu văn bản phức tạp | Trung bình — re-chunk + re-index toàn bộ corpus |
| Hierarchical chunking | Document có structure rõ (hợp đồng, manual, policy) | Cao hơn — phải parse & giữ structure document | Nếu document gốc đổi structure, pipeline parse có thể vỡ âm thầm | Cao — phải thiết kế lại schema chunk theo structure |
| Dense indexing (embeddings) | Query diễn đạt khác nguồn (paraphrase, intent) | Compute cho embedding + vector store | Bỏ sót exact-match (mã, ID, tên riêng) | Trung bình — thêm sparse index song song, không cần bỏ dense |
| Sparse indexing (BM25) | Query phụ thuộc token cụ thể (part number, citation, error code) | Thấp — không cần embedding | Bỏ sót paraphrase/intent query | Trung bình — thêm dense index song song |
| Hybrid indexing (dense + sparse + RRF) | Mixed query pattern — case phổ biến ở production | Cao nhất — chạy cả 2 pipeline + bước merge (RRF) | Ít risk về miss quality hơn, nhưng risk về latency/cost nếu size sai theo query pattern thực tế | Cao — đã đầu tư 2 pipeline, khó rút gọn lại về 1 index mà không đánh đổi quality |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Chunk | Đơn vị nội dung được retrieve; kích thước/ranh giới do cấu trúc corpus quyết định |
| Fixed-size chunking | Chia đều theo span cố định (có overlap), không quan tâm structure |
| Semantic chunking | Chia theo ranh giới ý nghĩa/topic shift để chunk tự đủ nghĩa |
| Hierarchical chunking | Giữ nguyên section/subsection của document, retrieve đúng level |
| Dense retrieval (embeddings) | Tìm theo semantic similarity, khớp ý nghĩa chứ không khớp từ |
| Sparse retrieval (BM25) | Tìm theo exact keyword/token match |
| Hybrid retrieval | Kết hợp dense + sparse, merge kết quả |
| Reciprocal Rank Fusion (RRF) | Thuật toán merge 2 ranked list bằng cách chấm điểm theo rank ở từng list, ưu tiên item tốt ở cả hai — default chuẩn cho hybrid, ít cần tune |
| Retrieval quality / Latency / Maintenance | 3 trục trade-off cốt lõi của mọi retrieval pipeline design |

## Gotchas / bẫy hay gặp
- [ ] Chọn chunk size theo "default" (vd luôn 512 token) thay vì theo cấu trúc corpus thực tế
- [ ] Dùng dense-only index cho domain có nhiều exact-match query (mã lỗi, part number) → miss kết quả đúng
- [ ] Nghĩ rằng retrieval quality "nhìn output là biết đúng/sai" — thực ra phải đo bằng labeled set (tie thẳng vào Evaluation, domain D4)
- [ ] Không re-index/re-chunk khi corpus có structure mới thêm vào → pipeline đúng lúc launch nhưng degrade âm thầm theo thời gian

## Exam tips
- Câu hỏi dạng scenario sẽ mô tả corpus (structured/unstructured) + query pattern (paraphrase vs exact-match) → chọn đúng chunking + indexing strategy tương ứng, không chọn theo "mặc định nghe quen"
- Nếu đề bài nhắc "queries hinge on specific tokens/IDs/codes" → đáp án đúng thường là sparse hoặc hybrid, không phải dense-only
- Nếu đề bài nhắc RAG trả lời sai sau khi answer sai do data đã đúng nhưng model "confident answer built on wrong chunk" → hướng xử lý là kiểm tra retrieval/indexing, đo bằng labeled eval set, không phải nghi ngờ model weights/temperature (đã ghi ở Key Gotchas trong CLAUDE.md)
- RRF là "known, defensible default" khi hybrid — nếu đề hỏi cách merge kết quả dense+sparse, đây là câu trả lời chuẩn để nêu ra

## Code / config snippets
```python
# snippet
```

## Câu hỏi chưa rõ
- ?
