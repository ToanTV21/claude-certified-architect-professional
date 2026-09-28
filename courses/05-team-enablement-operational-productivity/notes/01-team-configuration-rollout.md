# C5.1 — Team setup: shared config, rollout, Skills distribution, spend controls

> **Course:** 5 — Team Enablement & Operational Productivity (45 min) · **Exam domain:** D7 (7%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Configure Claude tooling and environments for a team, including the shared configuration, the rollout pattern, the Skills distribution strategy, and the spend controls that belong in team setup

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Bối cảnh module 5** (chỉ để hiểu framing, không tách mục riêng): 4 module trước tạo ra một Architect biết đi từ câu nói đầu tiên của stakeholder qua design → integration → governance → handoff. Module 5 giả định hệ thống đã **BUILT** rồi, và hỏi: team adopt nó tốt thế nào, và nó có "sống khoẻ" mà không kéo Architect vào mọi issue không? 3 phần của module build lên nhau theo thứ tự: **team setup** (lesson này — set đúng environment/reusable asset/spend posture trước khi ai login) → **developer workflow** (nâng bar làm việc hàng ngày mà không hạ bar chất lượng, dùng chính skill đã distribute ở setup) → **operational support** (xử lý khi có issue bất ngờ — chính là lúc review discipline của workflow bị test dưới áp lực).
- **4 quyết định team-setup mà Architect sở hữu**, bỏ qua cái nào cũng có failure mode riêng: (1) **environment** — deploy dưới dạng shared configuration; (2) **rollout** — pattern triển khai theo champion rồi batch; (3) **skills distribution** — cách phân phối reusable skill cho cả team; (4) **spend** — guardrail chi phí đặt trước khi có bill đầu tiên.
- **(1) Environment = shared configuration, không phải personal setup riêng lẻ từng người:** với Claude Code, team thống nhất 1 baseline ở project-level — 1 `CLAUDE.md` chung, 1 bộ tool/MCP server đã đồng ý, 1 permission posture — để mọi người xuất phát từ cùng 1 điểm thay vì mỗi người tự dò setting rồi drift dần theo thời gian. Baseline này review/version/cải tiến **1 lần** cho tất cả, thay vì N lần cho N người.
- **(2) Rollout = champion rồi batch, không all-hands 1 lần:** adoption hiếm khi thành công nếu "switch-on" toàn team cùng lúc. Pattern hiệu quả: chọn 1 **champion** mỗi department/team, cấp access trước, để champion chứng minh workflow bằng thực tế, rồi mới seed adoption theo từng batch. Champion hấp thụ friction ban đầu, tạo local example thật, trở thành first line of support — Architect không còn là người duy nhất trả lời câu hỏi.
  - **Worked example:** org kỹ thuật 200 người, 4 department, muốn rollout Claude Code. Thay vì mở cho cả 4 dept cùng lúc: Architect enable 1 champion/dept, cho 2 tuần để convert 1 workflow thật (VD: code-review assist, bước test-generation); mỗi champion chạy 1 session 45 phút cho batch đầu (5 peers). Kết quả khi rollout rộng: mỗi dept đã có 1 working example, 1 local expert, và 1 `CLAUDE.md` chung đã được champion tinh chỉnh sẵn. Cùng 1 rollout mà gửi mass email 1 lần → spike prompt hỏi lộn xộn lúc mới dùng, rồi âm thầm quay lại thói quen cũ.
- **(3) Skills distribution = bản team-scale của reuse.** Skill package là quy trình lặp lại đóng gói thành unit versioned, reusable. Ở scale team, câu hỏi architecture là: phân phối 1 skill cho cả team thế nào — tạo/version/publish ra sao để team access được; grant/revoke access thế nào; rollback thế nào nếu skill "hư".
  - **4 cơ chế phân phối 1 skill cho team** (khác nhau ở ai access được + Architect giữ được bao nhiêu control):
    1. **Org-provisioned Skill** (Organization settings › Skills) — upload 1 lần, available cho **TOÀN BỘ** member trong org ngay lập tức. Đường đơn giản nhất khi 1 capability thực sự nên đến với tất cả mọi người. Governance/rollback: owner quản lý availability/removal ở cấp org; user có thể tự toggle skill off nhưng không remove được; **KHÔNG có version pinning hay native rollback** — update phải re-upload tay.
    2. **Plugin gán cho 1 group** — gói 1+ Skill vào 1 plugin, gán cho 1 group; chỉ member của group đó access được. Đây là nơi **governed distribution** thực sự sống: install preference (required / installed-by-default / available / not available), group targeting, version-controlled update từ 1 connected repository. Best when: 1 procedure/tool set cần đến specific team, hoặc cần rollout có governance. Đây là cơ chế governance **mạnh nhất** cho group-scoped distribution.
    3. **Claude Code project Skill** — filesystem artifact sống trong project repository (`.claude/skills/`), version **CÙNG** với repo, scope theo project nào mang nó. Best when: 1 tool/convention mà 1 team share trên chính các project của họ.
    4. **API Skill** — được gọi programmatically bởi chính product của partner (Messages API container). Best when: capability cần machine-to-machine reuse, không phải human-facing. Governance nằm ở calling system, hỗ trợ **explicit version pinning**.
  - **Lưu ý phân biệt quan trọng — dễ nhầm trong đề thi:** **Centrally managed Claude Code configuration** (server-managed settings được deliver từ server của Anthropic khi user authenticate, refresh theo hourly polling cycle) là 1 **SETTINGS mechanism riêng**, **KHÔNG PHẢI** là 1 trong 4 con đường Skills distribution.
  - Đóng gói 1 team workflow tốt thành skill distributable = cách 1 local best practice trở thành team standard: procedure di chuyển như **1 governed artifact** duy nhất thay vì know-how không văn bản hoá; update lan truyền qua versioning thay vì phải giải thích lại từ đầu cho từng người.
- **(4) Spend posture phải set TRƯỚC bill đầu tiên, không nên inherit default.** 4 thành phần admin cần set **có chủ đích**: (a) **model default** — session bắt đầu bằng model nào; (b) **model allowlist/restriction** — team được phép switch sang model nào; (c) **effort guidance** — model nên "làm việc" cứng tay đến đâu cho 1 task; (d) **spend/rate/per-user cap** — giữ consumption trong giới hạn. Module 2 đã chỉ ra: để model choice không được quản lý sẽ âm thầm route work sang tier mạnh hơn/đắt hơn mức task cần — ở scale team, hiệu ứng này **nhân lên theo từng member và từng request**.
- **Case study "the skill that shipped with no way back":** 1 platform team đóng gói release-notes procedure thành skill, bundle vào plugin, gán cho group 40 engineer. 1 tuần sau, 1 edit "có ý tốt" đổi prompt bên trong và skill bắt đầu sinh notes **sai format** cho toàn bộ team đang dùng. Vấn đề gốc: skill được push như 1 **flat bundle**, KHÔNG đi qua version-controlled update + rollback mà 1 plugin đáng lẽ cung cấp — nên fix phải manual re-edit trong khi bad output vẫn tiếp tục ship ra ngoài. Bài học: 1 shared asset không version, không đường lùi là 1 **liability** ngay khi có hơn 1 người phụ thuộc vào nó. Khi 1 shared asset cần versioning/group targeting/rollback → phải distribute trong 1 **organization-managed plugin** và chỉ định rõ 1 owner.
- **Cost · Complexity · Risk (nguyên bản lesson):**
  - **Cost:** đứng lên 1 team environment tốn thời gian setup (shared config, rollout plan, skills packaging) ngay từ đầu — nhưng rẻ hơn nhiều so với sau này phải reconcile 40 configuration đã drift khác nhau.
  - **Complexity:** phần khó nhất là **distribution governance** — ai có thể reach/update/revoke từng shared asset. Quyết định theo **per-asset**, không có 1 rule chung cho tất cả.
  - **Risk:** failure mode lớn nhất là 1 shared asset (skill, config) **không có versioning/rollback** — 1 thay đổi xấu lan ra cả team trước khi ai kịp chặn.
- **Checkpoint "design the team distribution strategy"** — chọn mechanism + đúng lý do (chọn đúng mechanism nhưng lý do sai = không pass):
  - **A.** Compliance-review procedure mọi department phải chạy giống nhau, cần centrally updatable + roll-back-able → **Plugin distributed org-wide (hoặc tới các group liên quan)** — vì cần version-controlled update từ connected repo (governance mạnh nhất), điều Org-provisioned Skill không có (không version pinning/native rollback).
  - **B.** Capability nên available cho mọi member, không cần versioning/rollback → **Org-provisioned Skill** — đường đơn giản nhất, reach mọi người ngay, khớp đúng yêu cầu "không cần versioning/rollback".
  - **C.** Coding convention + tool set mà engineering team share trên mọi project → **Claude Code project Skill** — filesystem artifact trong project repo, version cùng repo, scope theo project của team.
  - **D.** Reusable capability mà nhiều product của partner phải gọi programmatically → **API Skill** (Messages API container) — machine-to-machine reuse, hỗ trợ explicit version pinning.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Org-provisioned Skill (Organization settings › Skills) | Capability thực sự nên reach TOÀN BỘ org, không cần version/rollback | Thấp — upload 1 lần, không cần setup group/plugin | Không version pinning/native rollback — 1 bad update phải re-upload tay, propagate cho toàn org ngay lập tức | Cao — sửa lỗi = re-upload thủ công, không có version cũ để quay lại |
| Plugin gán cho group/org | Procedure/tool set cần reach specific team HOẶC cần governed rollout (required nhất khi cần centrally updatable + roll-back-able) | Trung bình — cần setup plugin, connected repo, install preference, group targeting | Thấp nhất trong 4 cơ chế nếu setup đúng — nhưng nếu bị push như flat bundle bỏ qua plugin governance (case study) thì risk lại cao nhất | Thấp — version-controlled update từ connected repo, rollback về version trước dễ |
| Claude Code project Skill (`.claude/skills/`) | Tool/convention 1 team share trên chính project repo của họ | Thấp — chỉ là file trong repo, không cần hạ tầng org riêng | Scope hẹp (chỉ project mang nó) nên ít lan rộng ngoài ý muốn, nhưng phụ thuộc discipline của repo | Thấp — rollback cùng cơ chế version control của repo (git revert) |
| API Skill (Messages API container) | Capability được gọi programmatically bởi product của partner, machine-to-machine | Trung bình — cần tích hợp ở calling system, không human-facing setup | Governance nằm ở calling system bên ngoài, không kiểm soát trực tiếp qua Claude Code/org settings | Thấp — hỗ trợ explicit version pinning, quay lại version cũ có chủ đích |
| Rollout theo champion-rồi-batch | Default cho mọi team rollout — cần local expert + working example trước khi mở rộng | Cost thời gian: 2 tuần cho champion convert workflow + session 45 phút/batch | Risk thấp — friction ban đầu được champion hấp thụ, ít "spike" prompt hỏi lộn xộn | Thấp — mở rộng dần từng batch, dễ dừng/điều chỉnh giữa đường |
| Rollout all-hands 1 lần (mass email) | Không nên chọn — chỉ là anti-pattern để đối chiếu | Cost thấp lúc launch (gửi 1 email) nhưng cao về sau (support quá tải) | Risk cao — spike prompt hỏi lộn xộn lúc mới dùng, dễ âm thầm quay lại thói quen cũ, không ai local support | Cao — khó "rút lại" 1 lần launch đã gây confusion, phải làm lại theo cách champion-batch |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Shared configuration | Baseline chung (CLAUDE.md, tool/MCP server set, permission posture) mọi member trong team xuất phát từ đó, thay vì tự setup riêng rồi drift |
| Team setup | 4 quyết định Architect sở hữu khi chuẩn bị team dùng Claude: environment, rollout, skills distribution, spend |
| Champion | Người được cấp access trước, chứng minh workflow bằng thực tế, trở thành local expert + first line of support cho department mình |
| Champion-then-batch rollout | Pattern rollout: 1 champion/department chứng minh trước, rồi mới mở rộng theo từng batch nhỏ, không all-hands 1 lần |
| Skills distribution | Bài toán architecture ở team-scale: làm sao tạo/version/publish/grant/revoke/rollback 1 skill cho cả team |
| Org-provisioned Skill | Skill upload ở Organization settings › Skills, available ngay cho toàn org, không version pinning/rollback native |
| Plugin (assigned to a group) | Bundle 1+ Skill, gán cho 1 group, có install preference + group targeting + version-controlled update từ connected repo — governance mạnh nhất |
| Claude Code project Skill | Skill là filesystem artifact trong `.claude/skills/` của project repo, version cùng repo, scope theo project |
| API Skill | Skill gọi programmatically qua Messages API container, dùng bởi product của partner, hỗ trợ version pinning |
| Centrally managed Claude Code configuration | Settings mechanism riêng — server-managed setting delivered từ Anthropic server khi user authenticate, refresh theo hourly polling; KHÔNG phải Skills distribution |
| Install preference | Thuộc tính của plugin: required / installed-by-default / available / not available, kiểm soát mức độ bắt buộc khi rollout tới group |
| Spend posture | Tập 4 cấu hình cost guardrail: model default, model allowlist, effort guidance, spend/rate/per-user cap |
| Model default | Model mà 1 session Claude bắt đầu dùng khi chưa ai chọn gì khác |
| Model allowlist/restriction | Danh sách model mà team được phép switch sang, chặn việc tự do chọn model đắt hơn cần thiết |
| Effort guidance | Hướng dẫn mức độ "làm việc" (compute/reasoning effort) model nên bỏ ra cho 1 task |
| Governed distribution | Phân phối shared asset có kiểm soát: ai access, version nào, rollback ra sao — đối lập với flat bundle không governance |
| Flat bundle | Cách push skill KHÔNG qua plugin/version control — không có rollback, chính là nguyên nhân case study "no way back" |

## Gotchas / bẫy hay gặp
- [ ] Nhầm **centrally managed Claude Code configuration** (settings mechanism, hourly polling từ server) là 1 trong 4 cách Skills distribution — đây là 2 khái niệm khác nhau hoàn toàn
- [ ] Chọn đúng mechanism nhưng nêu sai lý do trong câu hỏi scenario — checkpoint của lesson nói rõ "a correct mechanism with wrong reason does not pass"
- [ ] Push 1 skill như flat bundle (không qua plugin) cho cả group vì "cho nhanh" — mất version-controlled update + rollback, 1 edit sai lan ra toàn team ngay (case study 40 engineer)
- [ ] Rollout theo kiểu all-hands/mass email 1 lần cho cả org/department — gây spike prompt hỏi lộn xộn và dễ khiến người dùng quay lại thói quen cũ
- [ ] Nghĩ Org-provisioned Skill có version pinning/rollback như plugin — thực tế nó KHÔNG có, update phải re-upload tay
- [ ] Bỏ qua spend posture, để model default/allowlist trôi theo mặc định — hiệu ứng "âm thầm route sang tier đắt hơn" nhân lên theo từng member × từng request ở scale team
- [ ] Coi shared config là việc cá nhân mỗi dev tự lo (mỗi người tự set CLAUDE.md/tool riêng) thay vì baseline chung được review/version tập trung 1 lần
- [ ] Không chỉ định rõ 1 owner cho shared asset (skill/config) — khi cần version/rollback thì không ai chịu trách nhiệm cập nhật

## Exam tips
- Gặp scenario "chọn mechanism phân phối skill nào" → luôn bám 2 trục: (1) **ai cần access** (toàn org / 1 group / 1 project / product khác gọi qua API) và (2) **có cần version pinning + rollback không**. Plugin luôn là câu trả lời khi đề bài nói rõ "centrally updatable and roll-back-able" ở group/org scope.
- Nếu đề bài mô tả rollout gây "confused first-time prompts" hoặc "quiet retreat to old habits" ngay sau khi launch → đó là dấu hiệu rollout **all-hands 1 lần**, sai cách; đáp án đúng luôn là champion-rồi-batch.
- Đừng nhầm 2 khái niệm: **centrally managed configuration** = settings mechanism (server-managed, hourly polling) khác hoàn toàn với **Skills distribution** = 4 cơ chế org-provisioned/plugin/project Skill/API Skill. Đề có thể gài "distractor" liệt centrally managed config vào như 1 lựa chọn Skills distribution.
- Case study "skill shipped with no way back" là pattern hay lặp lại trong đề: hễ thấy "shared asset không version, 1 người sửa làm hỏng cho tất cả" → nguyên nhân luôn là thiếu governance của plugin (flat bundle), giải pháp luôn là organization-managed plugin + rõ owner.

## Code / config snippets
```python
# Minh hoạ logic "chọn đúng Skills distribution mechanism theo scenario"
# tương tự bảng mapping trong checkpoint "design the team distribution strategy"

from dataclasses import dataclass

@dataclass
class SkillScenario:
    # Mô tả ngắn tình huống cần phân phối skill
    description: str
    needs_everyone: bool          # capability có cần reach TOÀN BỘ org không
    needs_version_rollback: bool  # có cần centrally updatable + roll-back-able không
    scoped_to_repo: bool          # có phải convention/tool riêng của 1 project repo không
    called_by_other_products: bool  # có phải gọi programmatically từ product khác không


def choose_distribution_mechanism(s: SkillScenario) -> str:
    """Trả về mechanism đúng + rơi đúng thứ tự ưu tiên của checkpoint."""
    # D: API Skill — machine-to-machine, không phải human-facing
    if s.called_by_other_products:
        return "API Skill (Messages API container)"
    # C: Claude Code project Skill — version cùng repo, scope theo project
    if s.scoped_to_repo:
        return "Claude Code project Skill (.claude/skills/)"
    # A: cần version-controlled update + rollback ở group/org scope -> Plugin
    if s.needs_version_rollback:
        return "Plugin distributed org-wide / to relevant groups"
    # B: reach mọi người, không cần versioning/rollback -> Org-provisioned Skill
    if s.needs_everyone:
        return "Org-provisioned Skill (Organization settings > Skills)"
    return "Chưa đủ thông tin — cần hỏi thêm về scope/governance"


# 4 scenario của checkpoint, dùng để tự kiểm tra hàm trên
scenarios = {
    "A_compliance_review": SkillScenario(
        description="Compliance-review procedure mọi department phải chạy giống nhau",
        needs_everyone=False, needs_version_rollback=True,
        scoped_to_repo=False, called_by_other_products=False,
    ),
    "B_everyone_no_version": SkillScenario(
        description="Capability nên available cho mọi member, không cần version/rollback",
        needs_everyone=True, needs_version_rollback=False,
        scoped_to_repo=False, called_by_other_products=False,
    ),
    "C_project_convention": SkillScenario(
        description="Coding convention + tool set share trên mọi project của team",
        needs_everyone=False, needs_version_rollback=False,
        scoped_to_repo=True, called_by_other_products=False,
    ),
    "D_partner_products": SkillScenario(
        description="Nhiều product của partner phải gọi programmatically",
        needs_everyone=False, needs_version_rollback=False,
        scoped_to_repo=False, called_by_other_products=True,
    ),
}

if __name__ == "__main__":
    for name, sc in scenarios.items():
        print(name, "->", choose_distribution_mechanism(sc))
```

## Câu hỏi chưa rõ
- ?
