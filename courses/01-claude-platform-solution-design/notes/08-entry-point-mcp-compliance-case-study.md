# C1.8 — When Claude Code got picked outside engineering

> **Course:** 1 — Claude Platform & Solution Design (238 min) · **Exam domain:** D1 (17%) + D5 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Claude Code makes a strong first impression. It can execute complex, multi-step engineering tasks in a fraction of the time a developer would spend manually, and that capability is hard to unsee. The risk is that this leads teams to reach for Claude Code by default, even when the work doesn't require it and a simpler integration or Claude alone would be sufficient.

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)

### Case: regional bank "operations assistant"
- Bài toán: branch staff cần tra cứu customer balance, đặt appointment, trả lời policy question.
- Kiến trúc đề xuất (partner đưa để validate) có 3 thành phần: (1) **Claude Code** chạy trên branch
  laptop với `CLAUDE.md` riêng từng chi nhánh, (2) **MCP servers** cho customer database/appointment
  system/policy corpus, (3) **Subagents** chạy compliance check trên mỗi interaction.
- Đây là ví dụ thực tế của pattern lỗi: chọn công cụ vì nó **gây ấn tượng mạnh** (Claude Code làm
  engineering task rất nhanh) hoặc vì nó **được dùng ở project trước** (MCP), chứ không phải vì bài
  toán thực sự cần nó.

### Ba lỗi kiến trúc (three failure mechanisms)
1. **Sai entry point:** Claude Code là engineering tool (terminal-based). Branch staff không chạy
   terminal → entry point mismatch với user. **Nguyên tắc:** entry point phải được chọn **sau khi**
   xác định user và work, không phải trước.
2. **MCP dùng sai lý do:** MCP chỉ "earn its place" khi **cùng 1 tool entry point được reuse bởi
   nhiều client khác nhau**. Ở bank này chỉ có 1 client duy nhất — MCP ở đây chỉ tốn thêm integration
   cost (protocol layer) mà không đổi lại lợi ích reuse nào. MCP bị mang sang từ project trước như
   một **default integration layer**, không phải lựa chọn theo bài toán hiện tại.
3. **Compliance đặt sai layer:** compliance là high-consequence path nhưng lại giao cho **subagent**
   — cơ chế có **deterministic guarantee yếu nhất** trong toàn hệ thống (LLM reasoning, không phải
   code path cố định). Nguyên tắc: **task càng high-consequence, guarantee cần càng deterministic**
   → phải nằm ở server-side code, không phải ở agent/subagent layer.

### Kiến trúc đúng
- **Custom web app gọi API trực tiếp** — không qua Claude Code, không qua MCP layer trung gian.
- **Compliance nằm trong deterministic server-side code** — guarantee tường minh (explicit), không
  phải "emergent" từ agent reasoning.
- **Auth qua SSO của bank**, UI thiết kế cho banking workflow (không phải developer workflow).
- **Tool calls được audit ở server boundary** — audit trail nằm ở layer có control chắc chắn.

## Trade-off analysis

| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Claude Code làm entry point cho end-user nghiệp vụ | Không nên — chỉ phù hợp khi user là engineer/dev, thao tác qua terminal | Thấp lúc build (tận dụng sẵn CLI) | Rất cao — sai đối tượng sử dụng, staff không dùng được, phải build lại UI từ đầu | Cao — phải thiết kế lại toàn bộ entry point |
| Custom web app gọi API trực tiếp | User là nhân viên nghiệp vụ, cần UI phù hợp workflow + SSO | Cao hơn lúc đầu (phải tự build UI + backend) | Thấp — kiểm soát được auth, audit, compliance rõ ràng | Thấp — kiến trúc chuẩn, dễ mở rộng thêm feature |
| MCP server cho mỗi data source | Có ≥2 client khác nhau (VD: Claude Code + web app + Slack bot) cùng cần dùng chung 1 tool entry point | Tốn thêm 1 lớp protocol/maintenance | Nếu chỉ có 1 client: cost không đổi lại được lợi ích gì — pure overhead | Trung bình — phải gỡ layer MCP, nối thẳng client → API |
| Hard-code data access thẳng vào backend (không qua MCP) | Chỉ có 1 client/entry point duy nhất dùng data này | Thấp — ít moving part hơn | Nếu sau này có thêm client thứ 2 cần reuse → phải refactor thành MCP | Thấp lúc đầu, cost dồn lại nếu cần mở rộng sau |
| Compliance check ở subagent (LLM-based) | Không nên dùng cho path có hậu quả cao (regulatory, tài chính) — chỉ hợp cho task tư vấn/gợi ý không cần guarantee tuyệt đối | Thấp — tận dụng sẵn agent loop | Cao — subagent có thể bỏ sót/diễn giải sai, không có deterministic guarantee | Cao — phải viết lại logic compliance thành code path riêng |
| Compliance check ở deterministic server-side code | High-consequence path (compliance, tài chính, an toàn) | Cao hơn lúc build (phải code rule tường minh) | Thấp — guarantee rõ ràng, test được, audit được | Thấp — logic nằm sẵn trong codebase, dễ maintain/version |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Entry point | Điểm giao tiếp giữa user và hệ thống (terminal, web UI, chat, API) — phải chọn theo user, không theo công cụ có sẵn |
| Engineering entry point | Entry point thiết kế cho developer (VD: Claude Code/terminal) — sai nếu end-user là non-technical |
| MCP earns its place | Nguyên tắc: MCP chỉ đáng dùng khi tool entry point được **reuse across nhiều client** |
| Deterministic guarantee | Đảm bảo hành vi chắc chắn, lặp lại được — code path có deterministic guarantee cao hơn agent/subagent reasoning |
| High-consequence path | Luồng xử lý có hậu quả nghiêm trọng nếu sai (compliance, tài chính, an toàn) — cần đặt ở layer guarantee cao nhất |
| Server-side audit boundary | Điểm ghi log/audit đặt ở backend server, nơi kiểm soát được toàn bộ tool call, thay vì rải rác ở client |

## Gotchas / bẫy hay gặp
- [ ] Chọn Claude Code / MCP / Subagent chỉ vì "project trước dùng nó" hoặc vì nó gây ấn tượng mạnh,
      không phải vì bài toán hiện tại thực sự cần — đây là root cause của cả 3 lỗi trong case study.
- [ ] Expose data source qua MCP dù chỉ có 1 client duy nhất dùng — trả cost cho khả năng reuse không
      tồn tại.
- [ ] Giao compliance/high-consequence check cho subagent vì "agent nào cũng check được" — bỏ qua
      việc subagent là layer có deterministic guarantee yếu nhất trong hệ thống.
- [ ] Xác định giải pháp kỹ thuật (Claude Code, MCP, agent framework...) **trước khi** xác định rõ
      user là ai và họ tương tác với hệ thống như thế nào.

## Exam tips
- Gặp scenario "chọn entry point cho non-technical end-user" → luôn loại Claude Code/terminal-based
  tool ra khỏi đáp án, trừ khi user được mô tả rõ là developer/engineer.
- Gặp câu hỏi "có nên dùng MCP không" → kiểm tra đề bài có nhắc đến **nhiều client khác nhau** cùng
  cần dùng chung tool entry point hay không. Chỉ 1 client → MCP là over-engineering.
- Gặp câu hỏi về compliance/audit/high-consequence task → đáp án luôn nghiêng về **deterministic
  server-side code**, không phải agent/subagent, dù subagent "restricted tool access" nghe có vẻ an
  toàn hơn.
- Nguyên tắc tổng quát để nhớ: **"entry point choice should follow the user and the work"** — đây là
  câu keyword rất dễ bị hỏi lại dưới dạng nghịch đảo trong đề (VD: đưa ra 1 kiến trúc chọn tool trước,
  hỏi lỗi nằm ở đâu).

## Code / config snippets
```python
# Không có code source từ course cho lesson này (đây là case study kiến trúc,
# không phải bài tập code). Minh hoạ concept "compliance ở server-side, không phải subagent":

# SAI — compliance check nằm trong subagent (LLM reasoning, guarantee yếu)
def handle_request_wrong(user_request):
    result = compliance_subagent.run(user_request)  # LLM tự judge có vi phạm compliance không
    return result

# ĐÚNG — compliance check là deterministic code path ở server, tách khỏi agent loop
def handle_request_correct(user_request):
    if not compliance_rules.check(user_request):  # rule tường minh, test được, audit được
        raise ComplianceViolation(user_request)
    return claude_client.messages.create(...)  # Claude chỉ xử lý phần còn lại sau khi qua gate
```

## Câu hỏi chưa rõ
- ?
