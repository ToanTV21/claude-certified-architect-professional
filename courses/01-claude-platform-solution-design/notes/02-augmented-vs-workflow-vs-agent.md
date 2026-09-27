# C1.2 — Augmented call vs. workflow vs. agent

> **Course:** 1 — Claude Platform & Solution Design (238 min) · **Exam domain:** D1 (17%) · **Status:** 🟨 Đang học

## Learning objective (nguyên văn từ course)
> Choose between an augmented call, a workflow, and an agent by naming what each choice costs

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)

### 2 trục xác định pattern
Mọi use case đặt lên 2 trục:
- **Predictability** (trục ngang): đường đi qua task có liệt kê trước được không.
- **Model autonomy** (trục dọc): bạn giao bao nhiêu quyền tự quyết *bước tiếp theo* cho model
  (chứ không chỉ *cách làm một bước*).

Hai trục này thường nghịch nhau: đường đi càng khó đoán trước, càng phải giao nhiều quyền cho
model vì không tự script được.

### 3 pattern
- **Augmented LLM** (predictability cao, autonomy thấp): gọi model **1 lần**, có giới hạn rõ.
  Có thể gắn tool use / retrieval / extended thinking, nhưng model vẫn chỉ làm **một job bounded,
  một pass**. Control flow **không rẽ nhánh** theo quyết định của model. Dùng khi task đã định
  nghĩa rõ, output verify được, không cần chia nhiều bước.
- **Workflow** (dải giữa): shape tổng thể **cố định trong code của bạn** (chaining/routing/
  parallel/loop), nhưng mỗi bước có thể chứa phán đoán của model trong phạm vi hẹp (*bounded
  judgment*).
- **Agent** (autonomy cao, predictability thấp): model **tự sở hữu trajectory**, tự quyết bước kế
  tiếp dựa trên kết quả bước trước. Chỉ đáng dùng khi **việc liệt kê trước các bước chính là phần
  đắt/khó nhất** của bài toán: open-ended investigation, long-horizon work, bước sau phụ thuộc kết
  quả bước trước. Ví dụ production-proven: Claude Code (tự khám phá codebase lạ, tự quyết đọc file
  nào tiếp theo). Cái giá: **non-deterministic failures tập trung ở đây**, vì trajectory của model
  *chính là* control flow — không có code boundary nào để đặt guard.

### 4 sub-pattern của Workflow (không loại trừ nhau)
| Sub-pattern | Shape | Khi dùng | Ví dụ |
|---|---|---|---|
| **Chaining** | Bước 2 nhận output bước 1 làm input, tuần tự | Task tách tự nhiên thành stage có handoff rõ | Review hợp đồng: extract obligations → classify risk → draft memo |
| **Routing** | Classifier (thường là Claude) quyết định đi nhánh nào | Input đa dạng loại, mỗi loại cần xử lý khác nhau | Ticket support: billing → retrieval account data, technical → retrieval docs, escalation → human queue |
| **Parallelization** | Nhiều model call chạy song song, kết quả aggregate/vote | Sub-task độc lập, không phụ thuộc nhau | Due diligence 12 hợp đồng: gửi song song → gộp thành 1 risk report |
| **Evaluator-optimizer** | Model A draft → Model B evaluate & yêu cầu sửa → lặp đến khi đạt tiêu chí/hết retry | Chất lượng verify được nhưng 1 lần thử chưa đủ tin cậy | Code gen chạy test suite; draft reply → chấm theo rubric → rewrite |

Nguyên tắc chọn: pattern **đơn giản nhất** đáp ứng error tolerance + observability của task; xem
lại lựa chọn khi có **production data**; chỉ leo thang khi đo được pattern đơn giản không đủ.

### Framework 5 yếu tố (đi tuần tự — yếu tố đầu tiên loại trừ 1 pattern là yếu tố quyết định)
| Factor | Câu hỏi | Augmented LLM | Workflow | Agent |
|---|---|---|---|---|
| Predictability | Liệt kê được các bước trước không? | Task đơn, giới hạn | Bạn tự viết path | Trajectory không đoán trước được (theo thiết kế) |
| Error cost | Sai thì tốn gì: retry / audit / lawsuit? | Medium — lộ output distribution, không guard cấp bước | Low — guard xác định nằm giữa các bước | High — lộ toàn bộ output distribution qua nhiều turn |
| Observability | Ops team thấy & tái hiện được lý do không? | Medium — 1 call dễ log nhưng bên trong mờ | Low (rủi ro thấp) — mỗi bước log như code, dùng tooling chuẩn | High (rủi ro cao) — trajectory đọc như transcript, tooling hiện tại không alert được |
| Latency budget | Deadline user thấy được là gì? | Low — nhanh nhất (trừ khi extended thinking/retrieval) | Medium — đoán trước được nhưng cộng dồn | High — runtime mở, budget theo worst case chứ không phải median |
| Cost | Token cost/request ở volume kỳ vọng? | Low — ít token nhất | Medium — scale theo số bước | High — reasoning lặp, tool use nhiều turn, retry, context phình; agent thiết kế kém thường đắt nhất |

### Trước khi nghĩ tới fine-tuning
Thứ tự bắt buộc: **(1) tối ưu prompt → (2) thêm tool use/retrieval → (3) chuyển pattern mạnh hơn
(vd. evaluator-optimizer) → (4) mới xét fine-tuning**. Fine-tuning chỉ hợp lý khi: volume rất cao
và inference cost là ràng buộc thật; latency critical và model nhỏ chuyên biệt outperform model
chung; output cần format nhất quán mà prompting chưa giải quyết ổn định. Ngoài các case đó,
fine-tuning khoá bạn vào 1 phiên bản model cố định. **Availability hạn chế** — phải xác nhận với
Anthropic account team trước khi đề xuất.

### Pattern = lắp ráp lại primitive
Augmented call = model + tools. Workflow = primitive nối dây trong code của bạn. Agent = model tự
chọn chuỗi tool call của chính nó. Chọn pattern = chọn cách lắp ráp các phần đó.

### Skills-based architecture (packaging option)
Song song với chọn pattern, quyết định **đóng gói năng lực thế nào** — 3 option trên 1 spectrum:
prompt-only → direct tool use (model gọi function trong code) → **Skills-based architecture** (Skill
versioned, tái sử dụng, đóng gói procedure + instructions + script thành 1 unit governed). Dùng
Skill khi: procedure chạy lặp lại, cần phân phối nhiều team/product, cần versioning & governance.

Áp **Delegation lens** vào chính pattern: pattern này trao quyền quyết định phù hợp hay quá mức so
với risk profile? Agent tự chủ chỉ đúng đắn khi stakes + reversibility của hành động biện minh
được mức autonomy đó.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Augmented LLM | Task well-defined, output verify được, 1 pass đủ | Thấp nhất (ít token/request) | Medium — lộ output distribution nhưng không nhiều turn | Rẻ — đổi lại 1 prompt/call |
| Workflow (chaining/routing/parallel/evaluator-optimizer) | Shape task biết trước, mỗi bước cần model judgment giới hạn | Medium — scale theo số bước | Low — guard đặt được giữa các bước, fail = 1 bước code fail | Trung bình — sửa 1 bước trong pipeline, không đổ vỡ toàn hệ thống |
| Agent | Không liệt kê trước được bước; long-horizon; bước sau phụ thuộc kết quả bước trước | High — reasoning lặp, nhiều turn, context phình, retry | High — non-deterministic failure, trajectory = control flow, không code boundary để guard | Đắt — phải giới hạn tool (least privilege), giới hạn budget/step, human-in-the-loop mới giảm được risk |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Predictability | Đường đi qua task có liệt kê trước được không |
| Model autonomy | Mức độ model tự quyết bước tiếp theo, không chỉ cách làm 1 bước |
| Bounded judgment | Phán đoán của model bị giới hạn trong phạm vi 1 bước của workflow |
| Trajectory | Chuỗi quyết định/tool call mà agent tự chọn, đóng vai trò control flow |
| Chaining | Sub-pattern workflow: bước sau nhận output bước trước làm input, tuần tự |
| Routing | Sub-pattern workflow: classifier chọn nhánh xử lý khác nhau |
| Parallelization | Sub-pattern workflow: nhiều model call chạy song song, aggregate/vote kết quả |
| Evaluator-optimizer | Sub-pattern workflow: generator + evaluator lặp đến khi đạt tiêu chí hoặc hết retry |
| Liability surface | Không gian rủi ro mà autonomy của agent mở ra, giới hạn bởi tool permission |
| Delegation lens | Câu hỏi kiểm tra: pattern có trao quyền quyết định phù hợp với risk profile không |
| Skills-based architecture | Đóng gói procedure + instructions + script thành 1 Skill versioned, governed |

## Gotchas / bẫy hay gặp
- [ ] "Agent linh hoạt hơn nên luôn dùng agent" — SAI. Luôn bắt đầu từ pattern đơn giản nhất
      (Augmented LLM → Workflow → Agent), chỉ leo thang khi measurement chứng minh pattern đơn
      giản không đủ.
- [ ] "Agent luôn đắt hơn workflow" — SAI. Cost phụ thuộc **design** (context tích luỹ + số model
      call), không phụ thuộc nhãn pattern. Workflow thiết kế kém có thể đắt hơn agent thiết kế tốt.
- [ ] Bỏ qua **error cost** khi task có tác động tài chính/pháp lý — nếu sai một bước có thể dẫn
      tới lawsuit/audit, error cost cao thường loại Agent ngay từ factor này (Workflow có guard
      xác định giữa các bước).
- [ ] Nhầm "predictability thấp" của Agent là nhược điểm cần tránh hoàn toàn — thực ra đó là lý do
      **duy nhất** để chọn Agent: khi việc liệt kê bước trước là bất khả thi.
- [ ] Coi fine-tuning là fix nhanh cho prompt chưa ổn — course dạy rõ: prompt → tool/retrieval →
      pattern mạnh hơn → fine-tuning là bước **cuối cùng**, không phải bước 1.

## Exam tips
- Đề dạng scenario: đi qua 5-factor **theo đúng thứ tự** (Predictability → Error cost →
  Observability → Latency → Cost). Factor đầu tiên loại được 1 pattern chính là câu trả lời —
  không cần xét hết 5 factor nếu factor 1 hoặc 2 đã quyết định xong.
- Câu hỏi dễ bẫy: mô tả task có error cost cao (financial/legal) + đường đi rõ ràng → đáp án đúng
  là **Workflow** dù đề gợi ý "cần linh hoạt".
- Nhớ đúng 2 câu công thức hay bị hỏi lắt léo: *"Agent không tự động đắt hơn workflow — design mới
  quyết định cost"* và *"Risk = liability surface qua tool permission, không phải qua bản thân
  pattern"*.
- Workflow fail = 1 bước code fail (dễ debug). Agent fail = model ra quyết định sai giữa chuỗi turn
  (khó phát hiện, tooling debug thông thường không bắt được) — đây là câu phân biệt "Complexity"
  hay bị hỏi.

## Code / config snippets
```python
# Không có code snippet riêng cho lesson này (lesson thuộc về decision framework,
# không phải implementation). Sub-pattern cụ thể (chaining/routing/parallelization/
# evaluator-optimizer) sẽ có code mẫu ở exercises/ khi thực hành C1.3.
```

## Câu hỏi chưa rõ
- ?
