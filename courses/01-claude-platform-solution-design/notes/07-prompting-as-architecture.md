# C1.7 — Designing system prompts, templates, and guardrails

> **Course:** 1 — Claude Platform & Solution Design (238 min) · **Exam domain:** D2 (13%) · **Status:** 🟨 Đang học

## Learning objective (nguyên văn từ course)
> The model and context screen covered choosing a model tier and a context strategy. The other major lever in that decision area is the prompt itself. At enterprise scale the prompt is not a sentence you type, but an asset you design: a system prompt, a reusable template, and the guardrails that keep both safe and consistent.

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)

### Screen 1 — System-prompt architecture cho enterprise reuse
- System prompt cho 1 lần chat khác hẳn system prompt được hàng trăm request/ngày phụ thuộc vào —
  bản dùng ở enterprise phải có **structure**: role & scope rõ ràng, các **constraint** (phải làm gì /
  không được làm gì), và **output contract** (hình dạng response bắt buộc phải có).
- Khi 1 system prompt được reuse ở scale lớn, **ambiguity là 1 defect bị nhân bản** qua từng request —
  không phải lỗi nhỏ 1 lần mà là lỗi hệ thống.
- **Template** = system prompt có **parameterized slots** (phần thay đổi theo request) + fixed
  scaffolding cố định xung quanh. Mục tiêu thiết kế: fixed scaffolding gánh consistency + safety
  guarantee, để việc điền slot **không thể vô tình xoá mất constraint**. Template tốt biến safe path
  thành default path — người dùng chỉ điền nội dung biến đổi và tự động kế thừa guardrail, không cần
  tự viết lại.
- **Description** (1 trong 4 AI Fluency competency) áp vào prompt design = nói chính xác model cần
  làm gì: scope (cái gì in/out of bounds), format (output contract chính xác), constraints (rule
  không bao giờ được vi phạm).
- **Underspecification** = khoảng trống mà model tự lấp bằng assumption của chính nó, mỗi lần một
  kiểu khác nhau — đây chính là failure mode cần canh chừng, vì nó tạo ra non-determinism không mong
  muốn trong 1 asset được tái sử dụng.
- Kỹ năng của architect: đọc prompt để tìm ra cái nó **không nói** (not what it says). Với mỗi
  requirement output phải đạt, tự hỏi: prompt có **state** rõ ràng hay chỉ "hope" (ngầm mong đợi)?
  Fix = làm implicit thành explicit: restate goal cùng instruction, đặt tên format, bound constraint.

### Screen 2 — Prompt engineering technique theo model
- Technique chọn theo **độ phức tạp của task**, không phải theo thói quen.

| Technique | Là gì | Khi nào dùng |
|---|---|---|
| Zero-shot | Chỉ instruction, không ví dụ | Task đã well-specified, model xử lý ổn định — luôn thử đầu tiên |
| Few-shot | Vài input/output example trong prompt | Task mà format/judgment mong muốn dễ **show** hơn là **describe** |
| Chain-of-thought | Yêu cầu model reasoning từng bước trước khi trả lời | Multi-step reasoning, logic kiểu arithmetic, hoặc task mà path quan trọng bằng answer |

- Progression có chủ đích: bắt đầu zero-shot → thêm example nếu task cần → thêm explicit reasoning
  nếu structure của task đòi hỏi. Mỗi bước thêm đều tốn thêm token + latency → luôn chọn technique
  **nhẹ nhất** vừa đủ đáp ứng requirement.
- **Behavioral differences across models:** cùng 1 prompt không hoạt động giống nhau giữa các model
  tier/generation. Model mạnh hơn thường cần ít scaffolding hơn (ít example hơn, ít step-by-step
  explicit hơn) để đạt cùng chất lượng; model yếu hơn cần nhiều hơn. Prompt tune cho 1 model chỉ là
  **starting point** cho model khác, không phải artifact hoàn chỉnh — đây là lý do **model swap phải
  được coi như 1 release** và gate bằng evaluation: cái architect thực sự ship ra là **cặp
  prompt-model**, không phải prompt đơn lẻ.
- **Avoiding bias trong prompt construction:** leading phrasing, few-shot set không cân bằng (chỉ
  show 1 loại case), và assumption ẩn trong instruction đều lái output theo hướng khó nhận ra. Kỷ luật
  cần có: phrase trung lập, cân bằng example theo đúng các case hệ thống sẽ thực sự gặp, và tự hỏi
  prompt có đang **presume** (giả định sẵn) 1 câu trả lời mà lẽ ra nó phải **elicit** (khơi gợi) hay không.

### Screen 3 — Caching mechanics, modular prompt library, và Skills
- **Case "cache that never hits":** 1 team đặt reusable prompt lên production nhưng không thấy tiết
  kiệm cost nào từ caching. Nguyên nhân: họ đặt per-request content (document cần phân tích) lên
  **đầu** prompt, trước cả fixed instruction block lớn. Vì cache match theo **stable prefix**, đặt
  dynamic content lên đầu khiến prefix đổi mỗi request → cache **không bao giờ hit**. Fix: reorder lại
  — **fixed content trước, dynamic content sau**.
- Caching mechanics architect cần thiết kế quanh: **cache breakpoint**, **content ordering**,
  **TTL selection**, và biết khi nào **write overhead không đáng** (task chạy 1 lần, không đủ
  request lặp lại để hoàn vốn write cost).
- **Modular prompt library** vs **Skill** — 2 cách làm prompt reusable across team:
  - Prompt library: tập hợp prompt fragment/template dùng chung, engineer tự **assemble** trong code
    của họ.
  - Skill: unit chính thức hơn, **versioned**, self-contained — 1 `SKILL.md` đóng gói instruction +
    optional executable script + version management, cả procedure di chuyển như **1 governed
    artifact** duy nhất. Skill chính là reuse primitive "packaging a repeatable procedure" áp vào
    prompting.

## Trade-off analysis

| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Zero-shot | Task well-specified, model đã xử lý ổn định | Thấp nhất (ít token) | Model có thể improvise nếu task thực ra phức tạp hơn tưởng | Rất rẻ — thêm example/reasoning sau cũng dễ |
| Few-shot | Format/judgment dễ show hơn describe | Tốn thêm token cho example; example là content phải maintain | Example stale khi task evolve → âm thầm lái model sai | Trung bình — phải rà soát lại toàn bộ example set |
| Chain-of-thought | Multi-step reasoning, path quan trọng bằng answer | Tốn nhiều token + latency nhất | Áp dụng cho task không cần → "tax" lặp lại mỗi call vô ích | Dễ bỏ nếu benchmark cho thấy không cần |
| Prompt library (assembled trong code) | Dùng trong 1 team/codebase, hay tweak | Thấp, lightweight, engineer tự own | Dễ drift thành nhiều bản copy-paste hơi khác nhau, mỗi bản hành xử khác | Thấp nếu còn nhỏ; tăng dần theo số bản sao |
| Skill (SKILL.md versioned) | Procedure ổn định, chạy giống nhau mỗi lần, phân phối cross-team/product | Cao hơn ban đầu (cần versioning, approval, rollback process) | Thấp hơn về lâu dài — governance tập trung 1 chỗ | Có rollback sẵn theo version — dễ đảo ngược hơn prompt rải rác |
| Fixed content trước, dynamic content sau (cache-friendly ordering) | Bất kỳ prompt nào gọi lặp lại nhiều lần với phần cố định lớn | Cần thiết kế lại cấu trúc prompt 1 lần | Nếu đặt sai thứ tự (dynamic trước) → cache never hit, mất hết lợi ích cost | Rẻ — chỉ là đổi thứ tự block trong prompt |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| System-prompt architecture | Thiết kế system prompt có structure: role/scope, constraint, output contract — để dùng ở scale lớn |
| Template (prompt) | System prompt với parameterized slot + fixed scaffolding đảm bảo consistency/safety |
| Output contract | Phần system prompt quy định chính xác hình dạng/format response phải có |
| Description (AI Fluency) | Competency mô tả chính xác scope, format, constraint khi giao task cho model |
| Underspecification | Khoảng trống trong prompt mà model tự lấp bằng assumption riêng, khác nhau mỗi lần |
| Zero-shot / Few-shot / Chain-of-thought | 3 technique prompt engineering theo độ phức tạp task tăng dần |
| Model swap as a release | Nguyên tắc: đổi model phải qua evaluation gate như 1 lần release, vì prompt-model là 1 cặp |
| Cache breakpoint | Điểm đánh dấu trong prompt để hệ thống cache biết prefix nào có thể tái sử dụng |
| Stable prefix | Phần đầu prompt không đổi giữa các request — điều kiện để cache hit |
| Modular prompt library | Tập fragment/template prompt dùng chung, engineer tự assemble trong code |
| Skill (packaging) | Unit versioned, self-contained (SKILL.md + script) đóng gói 1 procedure để governance/distribute |

## Gotchas / bẫy hay gặp
- [ ] Đặt dynamic content (document, input theo request) lên **đầu** prompt trước fixed instruction
      block → phá stable prefix → cache **never hits**, mất hết lợi ích cost dù đã set up caching.
- [ ] Coi model swap là việc "đổi tên model string" đơn giản — thực ra prompt tune cho model cũ có
      thể fail âm thầm trên model mới nếu không gate bằng evaluation.
- [ ] Few-shot set không cân bằng (chỉ toàn case tích cực hoặc toàn 1 loại) → bias không nhìn thấy
      trong từng output riêng lẻ, chỉ lộ ra khi nhìn aggregate.
- [ ] Dùng chain-of-thought cho task đơn giản (vd summarize 400 từ thành 2 câu) → tốn token/latency
      vô ích, không tăng chất lượng.
- [ ] Nhầm "prompt library" và "Skill" là như nhau — prompt library thiếu governance/versioning nên
      dễ drift thành nhiều bản khác nhau không ai kiểm soát.
- [ ] Một guardrail bị underspecify (nói mập mờ) nguy hiểm hơn không có guardrail — nó tạo cảm giác
      có kiểm soát trong khi model có thể âm thầm lách qua.

## Exam tips
- Gặp câu hỏi dạng "chọn technique nào cho task X" → luôn áp progression: thử zero-shot trước, chỉ
  lên few-shot nếu cần show format/judgment, chỉ lên chain-of-thought nếu path reasoning ảnh hưởng
  answer (multi-condition, multi-step logic).
- Gặp câu hỏi về cache không hit dù đã cache → nghĩ ngay đến **content ordering** (dynamic content
  bị đặt trước fixed block), không nghĩ tới model/temperature.
- Gặp câu hỏi "làm sao chia sẻ 1 procedure prompt cho nhiều team, cần version + rollback" → đáp án
  đúng hướng là **Skill**, không phải prompt library.
- Câu hỏi về "model đổi version, output bắt đầu khác" → đáp án đúng: gate bằng evaluation trước khi
  swap, coi như 1 release — không phải do model "tệ hơn" hay do "cần retrain prompt từ đầu".

## Code / config snippets
```python
# Ví dụ minh hoạ content ordering để cache hit (không phải code thật từ course,
# chỉ minh hoạ ý "fixed content trước, dynamic content sau")

# SAI — dynamic content (document) đặt trước → cache prefix đổi mỗi request → never hit
prompt_wrong = f"{user_document}\n\n{large_fixed_instruction_block}"

# ĐÚNG — fixed instruction (large, ổn định) đặt trước, dynamic content đặt sau
# → prefix ổn định giữa các request → cache có thể hit
prompt_correct = f"{large_fixed_instruction_block}\n\n{user_document}"
```

## Câu hỏi chưa rõ
- Checkpoint "technique-selection matrix" (4 task: ticket classification / receipt extraction /
  contract liability / summarize) — cần tự làm lại để confirm đáp án trước khi thi:
  1. Ticket classification (5 category cố định, well-specified) → zero-shot.
  2. Extract structured fields từ receipt layout đa dạng → few-shot (format khó describe, dễ show).
  3. Xác định liability từ 3 condition tương tác nhau → chain-of-thought (path reasoning quan trọng).
  4. Summarize 400 từ → 2 câu → zero-shot (task đơn giản, không cần example hay reasoning).
