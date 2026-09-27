# Domain 7 — Developer Productivity & Operational Enablement (7% · 4 câu)

> Nguồn: practice set của Matthew Purcell (xem [README](README.md)). Đề được **diễn giải lại bằng tiếng Việt**.

**Chủ đề xuyên suốt:** **shared, version-controlled config** (ví dụ `CLAUDE.md`, `.claude/settings.json` commit
vào repo) · **review độc lập** với phiên tác giả · **debug bằng trace trước khi sửa** · **guardrail cho tooling
tự động** (allowed commands, protected branches, approval gates).

Note liên quan: [C5.1 team configuration rollout](../../courses/05-team-enablement-operational-productivity/notes/01-team-configuration-rollout.md) ·
[C5.2 AI-assisted dev workflow & review](../../courses/05-team-enablement-operational-productivity/notes/02-ai-assisted-dev-workflow-review.md) ·
[C5.3 debugging & operational support](../../courses/05-team-enablement-operational-productivity/notes/03-debugging-operational-support.md)

---

## Q7.1 · Multiple choice · Rollout AI coding tool cho team 30 người

**Tình huống:** Early adopter mỗi người cấu hình tool một kiểu → code style không đồng nhất, trùng lặp công sức.

- A. Để mỗi dev giữ cấu hình riêng vì tool năng suất là chuyện cá nhân
- B. Thiết lập project config + standard **dùng chung, version-controlled** mà tool của mọi thành viên kế thừa; config cá nhân chỉ cho sở thích riêng
- C. Chỉ cho 2 senior dùng AI tooling
- D. Bắt viết tay lại mọi code AI sinh trước khi commit

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: B**

**Vì sao đúng:** Năng suất cấp team đến từ **config chung trong version control** (mọi người kế thừa), sở thích cá
nhân xếp lớp bên trên → *nhất quán ở chỗ quan trọng, tự do ở chỗ không quan trọng*.

Với Claude Code cụ thể: project `CLAUDE.md` + `.claude/settings.json` (commit) · `CLAUDE.local.md` /
`.claude/settings.local.json` / `~/.claude/` (cá nhân, không commit) — đúng như cách repo này đang làm.

| Option | Vì sao sai |
|--------|-----------|
| A | Chính là vấn đề hiện tại |
| C | Giảm năng suất mà rollout sinh ra để tạo |
| D | Vứt bỏ toàn bộ lợi ích năng suất |
</details>

---

## Q7.2 · Multiple choice · AI vừa viết vừa review code

**Tình huống:** Review của các thay đổi do AI viết hiếm khi phát hiện vấn đề, nhưng defect vẫn lọt production.

- A. Bỏ review cho code AI vì đã được máy kiểm
- B. Bảo chính session đã viết code review lại lần hai, cẩn thận hơn
- C. Chỉ cho AI viết file test để defect không vào production code
- D. Review **độc lập** với session/agent tác giả — context mới không bị neo vào lập luận đã tạo ra code — con người giữ quyền merge

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: D**

**Vì sao đúng:** Reviewer bị **neo (anchored)** vào lập luận tạo ra code sẽ thừa hưởng luôn điểm mù của nó. Review
độc lập (fresh context, session/subagent riêng) khôi phục sự soi xét thật; **human giữ merge authority**.

| Option | Vì sao sai |
|--------|-----------|
| A | Xoá review |
| B | Lặp lại đúng sự neo đó ("self-review bias") |
| C | Hạn chế authoring nhưng không cải thiện review |
</details>

---

## Q7.3 · Multiple choice · Agent production hành xử lạ

**Tình huống:** Agent bắt đầu làm hành động bất ngờ trên **một phần** request. On-call engineer muốn **viết lại system prompt ngay**.

- A. Xem trace của các session bị ảnh hưởng — input, retrieved context, tool call, output — để xác định failure mode thực sự trước khi đổi bất cứ gì
- B. Viết lại system prompt từ đầu vì prompt là nguyên nhân phổ biến nhất
- C. Rollback về model version 6 tháng trước cho chắc
- D. Tắt agent vĩnh viễn, trả workload về thủ công

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: A**

**Vì sao đúng:** **Diagnose before treating.** Trace cho biết lỗi nằm ở input, retrieval, tool behaviour hay prompt.
Sửa prompt trước có nguy cơ **che mất nguyên nhân thật** và làm mất ổn định hành vi đang đúng.

| Option | Vì sao sai |
|--------|-----------|
| B | Đoán mò |
| C | Can thiệp lớn không có bằng chứng nhắm đúng nguyên nhân |
| D | Bỏ cả hệ thống vì lỗi ở một phần request |

**Pattern lặp lại xuyên đề:** câu hỏi "làm gì **first**" khi có sự cố → gần như luôn là **inspect traces / đo đạc**
(Q3.7, Q4.5, Q4.9, Q7.3).
</details>

---

## Q7.4 · Multiple response (chọn 2) · Scale AI-assisted development an toàn

- A. Cấp credential không giới hạn cho AI tooling để bớt ma sát
- B. Cấm dev xem/sửa code AI sinh ra
- C. Duy trì config chung, prompt standard, workflow tái sử dụng trong version control để team kế thừa best practice
- D. Ràng buộc những gì tooling tự động được thực thi (allowed commands, protected branches, approval gate cho hành động phá huỷ)
- E. Áp dụng mọi AI dev tool mới ngay khi phát hành

<details><summary>👉 Đáp án & giải thích</summary>

**Đáp án: C, D**

**Vì sao đúng:** Scale an toàn cần cả **chân ga và phanh**: (C) standard dùng chung lan toả practice đã được chứng
minh (tăng tốc); (D) execution constraint giới hạn thứ automation có thể làm sai (phanh). Với Claude Code: permission
allow/deny list trong `settings.json`, hooks, branch protection.

| Option | Vì sao sai |
|--------|-----------|
| A | Tối đa hoá blast radius |
| B | Bỏ giám sát của con người |
| E | Tăng churn mà không thẩm định |
</details>
