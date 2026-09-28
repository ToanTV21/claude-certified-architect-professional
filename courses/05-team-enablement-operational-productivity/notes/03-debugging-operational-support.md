# C5.3 — Debug & operational issue resolution, team self-sufficiency

> **Course:** 5 — Team Enablement & Operational Productivity (45 min) · **Exam domain:** D7 (7%) + D4 (16%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Support debugging and operational issue resolution by connecting symptoms to architecture causes and building the team toward self-sufficiency

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)

### Support role là TRANSLATION, không phải firefighting
- Khi một deployment đang live gặp sự cố bất ngờ, team thường chỉ nhận diện được **symptom** (latency spike, output degrade, tool lỗi) mà **không thấy được cause**. Team kéo Architect vào — giá trị của Architect nằm ở việc **connect symptom với architecture cause**, chứ không phải tự tay đi sửa incident.
- Đây chính là **diagnostic discipline** đã xây ở Course 2 (Module 2 — success criteria & eval suite, debugging production system): cùng một nguyên tắc "đo được → tìm root cause → verify bằng eval" giờ được áp dụng ở giai đoạn support, cho một team đã own deployment.
- Phân biệt 2 kiểu support:
  - **Firefighting** = Architect tự resolve 1 incident cụ thể → hết sự cố này, sự cố tương tự lần sau team vẫn phải gọi Architect lại.
  - **Support bền vững (lasts)** = Architect dạy team cái **symptom-to-cause path**, để lần sau gặp lại pattern tương tự, team tự resolve được — đây là mục tiêu thật của vai trò support.

### Connect symptoms to architecture causes — bảng 4 symptom → cause → first action
Nhiều operational symptom khác nhau thực ra trace về một tập nhỏ architecture cause. Đây là bảng nền tảng cho runbook:

| # | Symptom | Likely architecture cause | First action |
|---|---------|---------------------------|---------------|
| 1 | Output quality degrade dần dần, không có code change | Model/prompt change, hoặc **retrieval drift** khi corpus tăng trưởng | So sánh với eval set; check xem model, prompt, hay corpus đã thay đổi gì |
| 2 | Latency spike | Context size tăng, 1 tool bị chậm, hoặc cache stopped hitting | Dùng telemetry/request traces tìm slowest span — check token count/request, tool call chậm nhất, confirm cache behavior |
| 3 | Intermittent tool failures | Authorization issue, rate limit, hoặc unhandled error path | Inspect auth + limit của tool đang fail; trace 1 failed call end-to-end |
| 4 | Cost tăng mà usage không đổi | Model tier bị "creep" lên cao hơn dự kiến, hoặc caching regress | Check model tier per-request + cache hit rate, so với budget model |

### Build self-sufficiency: runbook + escalation path
Self-sufficiency không tự nhiên xuất hiện — nó phải được **engineer vào** cách team vận hành, qua 2 công cụ:
- **Runbook**: ghi lại các symptom-to-cause-to-action path đã biết, để team resolve được issue lặp lại **mà không cần Architect**. Bảng 4 dòng ở trên chính là nền (foundation) của một runbook tốt.
- **Escalation path**: định nghĩa rõ ai xử lý cái gì, và **khi nào** một issue cần leo thang ra khỏi team — để mọi người biết ranh giới giữa "team tự resolve được" và "phải escalate".
- Mục tiêu cuối: team chỉ cần gọi Architect khi gặp **problem MỚI**, không phải cho những vấn đề đã được dạy cách xử lý rồi.

### Case study: "The drift that waited for a quarterly review"
Một support team nhìn dashboard **xanh (green)** suốt cả quý, trong khi answer quality âm thầm tuột dốc. Không ai nối được cái decline chậm này với cause của nó: **retrieval corpus** tăng trưởng nhưng index không kịp reindex theo. Symptom đã hiện diện suốt thời gian đó, nhưng runbook thiếu đúng 1 dòng: "gradual quality decline, no code change → point tới model/prompt/retrieval drift". Nếu có dòng đó, một first-line engineer có thể resolve trong 1 buổi chiều; vì thiếu, nó phải chờ đến kỳ **quarterly review** mới bị phát hiện.
- **Cost**: dạy symptom-to-cause path tốn nhiều thời gian Architect hơn tự đi fix trực tiếp lúc đó, nhưng đây là kiểu support DUY NHẤT giảm tải cho tương lai, thay vì lặp lại vô hạn.
- **Complexity**: khó nhất là cưỡng lại cảm giác muốn firefight — fix nhanh thì dễ, nhưng fix bền (durable fix) đòi hỏi cùng team viết runbook entry + xác định escalation path.
- **Risk**: failure mode lớn nhất là 1 degradation chậm không ai connect được với cause, nên nó chạy ngầm cho tới khi 1 scheduled review vô tình bắt được, thay vì team tự phát hiện ngay ngày nó bắt đầu.

### Module Quiz & Recap (module 5)
> Đây là **lesson cuối cùng** của toàn bộ prep course 5 module (Skilljar CCAR-P). Module Quiz gồm 5 câu scenario trải khắp cả 3 lesson của Module 5 (team setup, adoption, skills distribution, developer workflow diligence, operational support) — ghi lại ở đây để không bị lạc mất nội dung ôn tập cuối course.

**Module Quiz (5 câu, đáp án đúng bôi đậm):**
1. **Team setup** — Team rollout Claude cho 4 department cùng lúc, adoption không đều. Nước đi tốt nhất? → **Enable 1 champion mỗi department trước, prove workflow, rồi seed adoption theo batch.** (Nguyên tắc: adoption phải được engineer qua champion + batch, không mandate target hay chờ người ta tự hỏi.)
2. **Skills distribution** — 1 procedure phải chạy giống nhau ở mọi department và phải revoke được từ 1 chỗ. Cách phân phối đúng? → **Bundle vào 1 org-managed plugin, distribute cho các department với group/org targeting, version-controlled update, và rollback.** (Nguyên tắc: cần versioning + revocation tập trung → plugin distribution, không phải paste prompt/email tài liệu.)
3. **Developer workflows** — Team ship code AI-generated nhanh hơn nhưng lọt 1 security issue. Thứ gì nhiều khả năng đã thiếu? → **1 verification checklist mà AI-generated code phải pass trước production, bao gồm cả dimension security.** (Nguyên tắc: gate trước production phải cover đủ correctness/security/maintainability/human-understanding, không chỉ dựa vào linter hay SLA miễn trừ.)
4. **Judgment** — Trong review, developer không giải thích được vì sao 1 đoạn code AI-generated xử lý input theo cách đó, nhưng test pass. Nên làm gì? → **Hold lại cho đến khi author giải thích được behavior + rationale — human-understanding check.** (Nguyên tắc: test pass không thay thế được việc author phải hiểu code mình ship.)
5. **Operational support** — Output quality trên 1 live deployment degrade suốt 2 tháng, không có code change. Architect nên nhìn vào đâu đầu tiên? → **Model/prompt change, hoặc retrieval drift khi corpus tăng — connect symptom với architecture cause.** (Nguyên tắc: đúng bảng symptom→cause ở lesson này — không phải tăng model tier hay disable caching hay rollback code.)

**Recap toàn Module 5 (4 điểm xuyên suốt):**
1. **Team setup** = shared configuration + distribution + spend posture quyết định từ đầu: baseline chung (CLAUDE.md, tool được duyệt, permission posture) + 1 trong 4 cơ chế Skills distribution (org-provisioned / plugin / project Skills / API Skills) + guardrail về model & budget.
2. **Adoption** = engineer qua champion + batch: 1 champion/team prove workflow trước rồi mới seed batch tiếp; access mà không có enablement thì dừng ở mức "basic chat", adoption lụp cụp (lumpy) thì không bao giờ chuẩn hoá được gain.
3. **Diligence** = verification checklist giữ AI-assisted work đáng tin: gate correctness/security/maintainability + author phải explain được cái mình ship, trước khi lên production.
4. **Operational support** = translation + self-sufficiency: connect symptom với architecture cause, để lại runbook + escalation path để team chỉ cần Architect cho problem MỚI, không phải problem đã quen.

Đây cũng là điểm kết của toàn bộ Architect track: từ câu nói đầu tiên của stakeholder → design → integration → governance → handoff → đến team tự adopt và vận hành được deployment.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Firefighting (Architect tự fix incident) | Cần unblock production NGAY, không còn thời gian dạy team giữa lúc sự cố đang cháy | Thấp ở lần này (nhanh, không tốn thời gian dạy) | Cao về lâu dài — cùng loại issue lặp lại, team vẫn phải gọi Architect mỗi lần → tải không giảm | Thấp để "undo" (chỉ là 1 lần fix) nhưng không undo được việc team vẫn thiếu năng lực tự resolve |
| Teach symptom-to-cause path (viết runbook entry cùng team) | Mặc định nên chọn — biến 1 incident thành capability lâu dài cho team | Cao hơn ở lần đầu (Architect tốn thời gian giải thích + cùng viết runbook) | Thấp hơn theo thời gian — risk giảm dần vì team tự bắt được issue tương tự sớm hơn | Cao nếu phải "undo" — vì đã đầu tư thời gian dạy, nhưng đây là investment một lần, ít khi cần đảo ngược |
| Có runbook (symptom→cause→action đã ghi) | Team đã gặp qua ít nhất 1 lần các failure mode phổ biến (quality drift, latency, tool failure, cost) | Chi phí duy trì: phải update runbook khi architecture đổi | Nếu runbook thiếu đúng 1 dòng (case study drift) → issue chạy ngầm tới khi có scheduled review mới bắt được | Thấp — chỉ cần sửa/thêm 1 dòng runbook khi phát hiện gap |
| Không có runbook, chỉ dựa vào trí nhớ/kinh nghiệm cá nhân | Team mới, deployment mới chưa đủ dữ liệu incident để rút ra pattern | Thấp trước mắt (không tốn effort viết doc) | Cao — kiến thức "đi cùng người", ai nghỉ/đổi team thì mất; issue quen vẫn phải escalate lại Architect | Cao — phải build lại runbook từ đầu khi nhận ra thiếu nó |
| Escalation path rõ ràng (ai xử lý gì, khi nào leo thang) | Team có nhiều role/level (first-line engineer, Architect, vendor) cùng tham gia support | Chi phí thiết kế + thống nhất ranh giới trách nhiệm giữa các role | Nếu thiếu: issue bị giữ ở sai tầng quá lâu (first-line cố xử lý issue lẽ ra phải escalate, hoặc escalate cả issue lẽ ra tự xử lý được) | Trung bình — cần renegotiate ranh giới trách nhiệm giữa role khi thay đổi |
| Không có escalation path, mọi issue đều gọi thẳng Architect | Team rất nhỏ, chỉ có 1-2 người, chưa cần phân tầng | Thấp trong ngắn hạn | Cao khi team scale lên — Architect thành bottleneck cho mọi issue dù nhỏ hay lớn | Trung bình — cần thiết kế lại phân tầng khi team lớn hơn |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Symptom vs. cause | Symptom = biểu hiện quan sát được (latency spike, output degrade, tool fail); cause = nguyên nhân architecture đứng sau symptom đó. Việc của Architect là connect 2 cái này |
| Translation (support role) | Vai trò của Architect trong support: dịch symptom mà team quan sát thành architecture cause, thay vì tự tay fix (firefighting) |
| Firefighting | Tự resolve 1 incident cụ thể ngay lúc đó — hết sự cố này nhưng không giảm tải lần sau |
| Runbook | Tập hợp các symptom-to-cause-to-action path đã biết, giúp team resolve issue lặp lại mà không cần Architect |
| Escalation path | Định nghĩa ai xử lý cái gì và khi nào 1 issue phải leo thang ra khỏi team |
| Self-sufficiency | Năng lực team tự resolve operational issue đã biết, không cần gọi Architect — phải được engineer vào chứ không tự nhiên có |
| Retrieval drift | Corpus của hệ thống RAG tăng trưởng nhưng index/retrieval logic không theo kịp, khiến quality degrade dần dù không đổi code |
| Diagnostic discipline | Nguyên tắc "đo được → tìm root cause → verify" đã xây ở Course 2 (eval suite), áp dụng lại ở giai đoạn operational support |
| Telemetry / request traces | Dữ liệu quan sát runtime (token count/request, span latency, cache hit) dùng để tìm slowest span khi debug latency spike |
| Quarterly review (case study) | Chu kỳ review định kỳ — nếu runbook thiếu 1 dòng, drift chỉ bị phát hiện tới kỳ review này thay vì ngay khi bắt đầu |
| Champion-per-department rollout | Adoption pattern: enable 1 champion mỗi team trước để prove workflow, rồi mới seed adoption theo batch cho cả department |
| Skills distribution (4 mechanism) | 4 cách đưa 1 Skill tới đúng người: org-provisioned Skills, plugin theo group/org, Claude Code project Skills, API Skills — khác nhau về access/versioning/rollback |
| Verification checklist | Tập check correctness/security/maintainability/human-understanding mà AI-generated output phải pass trước khi lên production |
| Human-understanding check | Yêu cầu author phải giải thích được vì sao đoạn code AI-generated hoạt động như vậy, dù test đã pass |
| Shared configuration | Baseline chung mọi member bắt đầu từ đó (VD: CLAUDE.md, tool đã duyệt, permission posture) — thay cho setup cá nhân rời rạc |
| Spend posture | Model default, model allowlist/restriction, effort guidance, spend/rate/per-user cap — set sẵn trong team configuration để giữ consumption trong ngân sách |
| Module Quiz | 5 câu scenario cuối Module 5, trải khắp team setup / skills distribution / developer workflow / judgment / operational support |

## Gotchas / bẫy hay gặp
- [ ] Architect tự tay fix mọi incident (firefighting) mà không dạy lại symptom-to-cause path → team không bao giờ tự đứng được, tải lặp lại vô hạn
- [ ] Dashboard "xanh" bị hiểu nhầm là hệ thống ổn — dashboard thường chỉ track uptime/error rate, không track quality drift chậm dạng retrieval/prompt drift (case study "drift that waited for a quarterly review")
- [ ] Runbook thiếu đúng 1 entry cho 1 failure mode phổ biến (VD: gradual quality decline không code change) → issue phải chờ tới scheduled review mới bị bắt, thay vì resolve trong 1 buổi chiều
- [ ] Không có escalation path rõ ràng → first-line engineer giữ issue quá lâu (lẽ ra phải escalate) hoặc escalate cả issue nhỏ lẽ ra tự resolve được
- [ ] Nhầm lẫn "latency spike" là do model chậm, quên check cache hit rate và slowest tool call span trước — bỏ sót nguyên nhân phổ biến nhất
- [ ] Nhầm "cost tăng" là do usage tăng, không check model tier creep hoặc cache regression — 2 cause phổ biến hơn usage change
- [ ] Coi verification checklist (Diligence) và runbook (Operational support) là 2 việc tách biệt hoàn toàn — thực ra cả 2 đều là dạng "đóng gói discipline thành artifact tái sử dụng được" cho team
- [ ] Đánh giá thấp Module Quiz vì nghĩ nó chỉ ôn lại 1 lesson — thực ra 5 câu trải đều khắp cả 3 lesson của Module 5, cần nắm cả team setup + adoption + diligence + operational support

## Exam tips
- Câu scenario dạng "output quality degrade dần, không có code change, Architect nhìn đâu đầu tiên?" → đáp án luôn là **model/prompt change hoặc retrieval drift**, không phải tăng model tier hay rollback code (xem Q5 module quiz).
- Câu scenario về "latency spike" → nghĩ ngay tới bộ 3: context size tăng / tool chậm / cache miss — không phải "cần model mạnh hơn".
- Câu scenario về "cost tăng mà usage không đổi" → nghĩ tới model tier creep hoặc cache regression, không phải do traffic.
- Nguyên tắc chốt của lesson: support đúng nghĩa = teaching symptom-to-cause path (durable), firefighting chỉ là fix tạm — câu hỏi judgment thường test đúng sự phân biệt này.
- Với 5 câu Module Quiz dạng tương tự khi ôn thi: luôn map câu hỏi về đúng 1 trong 4 chủ đề của Module 5 (team setup/adoption → champion+batch; skills distribution → chọn đúng 1/4 mechanism theo yêu cầu versioning/rollback; developer workflow diligence → verification checklist + human-understanding check; operational support → symptom-to-cause + runbook/escalation) rồi áp nguyên tắc cốt lõi của chủ đề đó, thay vì suy luận lại từ đầu.

## Code / config snippets
```python
"""
Minh hoạ đơn giản 1 RUNBOOK dạng dict, map symptom -> (cause, first_action)
theo đúng bảng 4 dòng "symptom -> likely architecture cause -> first action"
trong lesson C5.3. Mục tiêu: cho thấy runbook có thể được code hoá thành
1 lookup table nhỏ, dễ mở rộng khi team gặp thêm failure mode mới.
"""

# Mỗi key là 1 symptom (string ngắn, dễ nhận diện khi report issue).
# Value là tuple (likely_cause, first_action) — action luôn là bước ĐẦU TIÊN
# để confirm cause, không phải bước fix cuối cùng.
RUNBOOK = {
    "quality_degraded_gradual_no_code_change": (
        "Model/prompt change, hoặc retrieval drift khi corpus tăng trưởng",
        "So sánh output với eval set; check model/prompt/corpus đã đổi gì",
    ),
    "latency_spike": (
        "Context size tăng, tool chậm, hoặc cache stopped hitting",
        "Dùng telemetry/request traces tìm slowest span; check token count "
        "per request, tool call chậm nhất, cache hit rate",
    ),
    "intermittent_tool_failure": (
        "Authorization issue, rate limit, hoặc unhandled error path",
        "Inspect auth + limit của tool đang fail; trace 1 failed call end-to-end",
    ),
    "cost_rose_no_usage_change": (
        "Model tier bị creep lên, hoặc caching regress",
        "Check model tier per-request + cache hit rate, so với budget model",
    ),
}


def lookup_runbook(symptom: str):
    """
    Tra runbook theo symptom, trả về first_action để engineer bắt đầu debug.
    Nếu symptom chưa có trong runbook -> đây chính là "problem MỚI" mà
    Architect cần vào cùng team, thay vì 1 issue đã biết cách xử lý.
    """
    entry = RUNBOOK.get(symptom)
    if entry is None:
        # Không tìm thấy path đã biết -> escalate theo escalation path,
        # KHÔNG tự đoán fix — đây là ranh giới self-sufficiency vs escalation.
        return "UNKNOWN_SYMPTOM: escalate theo escalation path, chưa có trong runbook"
    cause, first_action = entry
    return first_action


if __name__ == "__main__":
    # Ví dụ: team report "quality tụt dần, không đổi code" -> tra runbook ngay
    action = lookup_runbook("quality_degraded_gradual_no_code_change")
    print(action)
    # -> "So sánh output với eval set; check model/prompt/corpus đã đổi gì"
```

## Câu hỏi chưa rõ
- ?
