# C5.2 — Dev workflow với AI tooling & review discipline

> **Course:** 5 — Team Enablement & Operational Productivity (45 min) · **Exam domain:** D7 (7%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Improve developer workflows with AI tooling and define the review discipline that keeps AI-generated work trustworthy before it reaches production

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Vấn đề đặt ra:** một team có thể configure Claude hoàn hảo (đúng model, đúng system prompt, đúng tool access) mà vẫn thu được rất ít giá trị. Sự khác biệt nằm ở **workflow** — cách AI assistance được dệt (woven) vào cách developer làm việc thực tế — và ở **discipline** giữ cho output của AI đáng tin cậy. Bài học này nâng "workflow bar" nhưng KHÔNG được hạ "quality bar"; bỏ qua nửa sau (quality bar) chính là failure mode nguy hiểm nhất.

- **Nguyên tắc cốt lõi: tích hợp AI assistance VÀO workflow đã có sẵn.** AI tooling chỉ thực sự trả về giá trị khi nó sống TRONG editor, review process, test loop hiện có — thay vì là một chat window riêng biệt mà developer chỉ ghé qua "khi rảnh". Việc của architect là tìm ra điểm nào trong workflow hiện tại đang có friction thật (real friction) và AI có thể loại bỏ friction đó mà không cần developer đổi cách làm việc.
- Integration còn có một vai trò sâu hơn: đây là cách **encode team knowledge**. Convention, review standard, quy trình lặp lại — những thứ thường chỉ nằm trong đầu vài người senior — khi được đưa vào Skills và project configuration thì trở thành thứ Claude áp dụng CONSISTENTLY cho mọi người dùng. Nhờ vậy, good practice đi theo tooling, không còn phụ thuộc vào "ai đang có mặt trong phòng" (tie-in trực tiếp với C5.1: đây chính là cơ chế khiến enablement bền vững sau khi champion rời đi).

- **3 workflow stage — Claude giúp gì và review discipline nào vẫn cần giữ:**

| Stage | Claude giúp gì | Review discipline vẫn cần |
|---|---|---|
| Writing code | Draft boilerplate, tests, first-pass implementation từ 1 spec rõ ràng | Correctness + security review; **author phải hiểu** những gì vừa được generate, không chỉ accept vì "nhìn ổn" |
| Reviewing code | Summarize diff, flag các issue khả nghi, giải thích đoạn code lạ | Human judgment vẫn là người quyết định cuối; AI flag chỉ là **INPUT**, không phải verdict |
| Debugging | Đề xuất hypothesis từ 1 symptom + 1 trace | Phải **verify hypothesis với evidence** trước khi hành động, không hành động ngay theo gợi ý |

  → Điểm chung ở cả 3 stage: Claude làm nhanh hơn phần "sinh ra khả năng" (draft, summary, hypothesis), còn phần "xác nhận đúng" luôn phải là con người — AI không thay thế review, nó chỉ thay đổi tốc độ tạo ra thứ cần review.

- **2 failure mode phổ biến khi triển khai AI tooling cho dev workflow:**
  1. **Lumpy adoption** — một vài dev dùng AI tooling rất nhiều, phần còn lại hầu như không đụng tới → cả team KHÔNG BAO GIỜ nhận ra lợi ích thật, và practice không bao giờ standardize được. Đây chính là lý do C5.1 dạy **champion-and-batch rollout**: chủ động lan toả usage theo từng batch có kiểm soát, thay vì để việc adoption trôi tự nhiên và chỉ rơi vào tay early adopter.
  2. **Stalling at basic chat** — team dùng Claude như một "hộp hỏi-đáp" (question-answering box) và không bao giờ tiến lên các workflow giá trị cao hơn (tool use, repository-aware assistance, packaged Skills) vì không ai enable họ vượt qua bước đầu tiên. Bài học quan trọng: **có access KHÔNG đồng nghĩa với adoption thật** — cần configure chủ động để enablement diễn ra trong đúng workflow hiện tại, không chỉ mở quyền truy cập rồi để đó.

- **Diligence — discipline giữ cho AI-generated work đáng tin cậy.** Đây là 1 trong **4 AI Fluency competency** của Anthropic. Định nghĩa chính thức: *"taking responsibility for what we do with AI and how we do it"*. Trong ngữ cảnh **deployment diligence** cụ thể: chịu trách nhiệm **VERIFYING** (xác minh) và **VOUCHING FOR** (đứng ra bảo đảm) output mà mình dùng hoặc chia sẻ.
  - Áp vào dev workflow: một habit cụ thể — giữ AI-generated code ở CÙNG một chuẩn với code viết tay (correctness, security, maintainability), và luôn cảnh giác với failure mode tinh vi: engineer accept output mà họ KHÔNG còn hiểu đầy đủ, chỉ vì nó "nhìn đúng" và pass một check nông (shallow check).

- **Verification checklist — deliverable cụ thể của Diligence.** Là tập câu hỏi/check rõ ràng mà một AI-generated output phải pass trước khi vào production. Mỗi team tự xây checklist này dựa theo nhu cầu riêng, nhưng checklist phải phủ đủ **4 dimension**: **correctness, security, maintainability, human understanding**.
  - Nguyên tắc quan trọng: **bất cứ check nào automate được thì nên automate.** Một regression test suite + một eval set biến việc verify correctness/behavior từ "judgment call của reviewer mỗi lần" thành một **GATE** chạy trên mọi thay đổi. Nói cách khác: checklist định nghĩa **WHAT** phải đúng; test/eval là **HOW** để team chứng minh điều đó lặp lại được (repeatably) mà không cần suy luận lại tay mỗi lần.
  - Team có checklist = đã biến good intention thành repeatable gate. Team không có checklist = đang **trust AI output by default** và chỉ hy vọng reviewer tự bắt được vấn đề — một chiến lược không đáng tin ở scale.

- **Case study: "The merge nobody could explain".** Một team adopt AI-assisted coding, ship nhanh hơn rõ rệt. 3 tuần sau, một change do AI generate PASS code review, PASS tests, lên production — rồi **leak data** qua một input mà code chưa từng validate. Trong post-incident review, tác giả của change **không thể giải thích** vì sao code lại xử lý input đó theo cách đó — nó "nhìn hợp lý" (plausible), tests xanh, và không ai từng hỏi câu hỏi mà checklist sẽ buộc phải hỏi: *"người merge change này có thể giải thích code làm gì và vì sao không?"*. Speed đã lặng lẽ thay thế understanding — đây chính là **judgment erosion** mà diligence tồn tại để chặn lại. Bài học map trực tiếp vào dimension thứ 4 (human understanding) — dimension duy nhất bị bỏ qua trong case study này dù correctness (tests) và một phần security check đã pass.

- **Cost · Complexity · Risk:**
  - **Cost:** AI assistance làm giảm cost để sinh ra code, kéo theo **volume code đến review tăng lên** — verification checklist chính là thứ giữ cho volume này không overwhelm quality bar.
  - **Complexity:** phần khó không phải là công nghệ, mà là **văn hoá** (cultural) — giữ AI-generated code ở đúng chuẩn review như code viết tay, đặc biệt khi nó ship nhanh hơn và "nhìn đúng".
  - **Risk:** failure mode lớn nhất là **judgment erosion** — team ship ra output mà họ không còn hiểu, vì nó chỉ pass được các shallow check, cho đến khi một input chưa ai từng reason tới lọt vào production.

- **Exercise "define the verification checklist"** — yêu cầu: với mỗi 1 trong 4 dimension, viết 1 check cụ thể bằng lời của mình. Model answer của course:
  - **Correctness:** Tests exist and pass, và behavior khớp với requirement đã nêu, kể cả edge case.
  - **Security:** Không có secret trong code; input được validate; mọi tool/external call dùng least-privilege access.
  - **Maintainability:** Code đọc rõ ràng, theo đúng team convention, không có complexity chưa được giải thích.
  - **Human understanding:** Developer submit change có thể giải thích code làm gì và vì sao, kể cả cách nó xử lý input mà nó CHƯA từng được test explicit.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Có verification checklist (4 dimension) trước khi merge | Mặc định cho mọi team dùng AI-assisted coding ở production — muốn giữ quality bar khi volume code tăng | Chi phí thời gian ban đầu để định nghĩa checklist + duy trì nó theo convention team | Nếu bỏ qua: judgment erosion — team ship code không ai hiểu, chỉ phát hiện khi incident xảy ra (case study data leak) | Thấp — checklist là artifact sống, sửa/thêm dimension bất kỳ lúc nào, không lock kiến trúc |
| Không có checklist, để reviewer tự judgment mỗi lần | Team nhỏ, low-stakes, chưa scale AI-assisted coding | Thấp trước mắt — không tốn công định nghĩa | Cao — mỗi reviewer tự quyết chuẩn khác nhau, dễ lọt case như "merge nobody could explain"; risk tăng theo volume code AI sinh ra | Cao — khi incident xảy ra mới quay lại viết checklist, phải retrofit vào review process đã chạy |
| Automate check bằng test suite + eval set (biến checklist thành gate) | Behavior correctness/security có thể kiểm bằng rule/test rõ ràng, cần chạy trên MỌI change | Chi phí xây + maintain test/eval song song với code | Test/eval không cập nhật theo behavior mới → false confidence (tương tự outdated eval ở C2.1) | Trung bình — sửa lại test case khi requirement đổi |
| Để correctness/behavior là judgment call thủ công mỗi lần review | Prototype/one-off, chưa cần lặp lại nhiều lần | Thấp ban đầu, không cần viết test | Không repeatable — mỗi review tốn effort như lần đầu, dễ bỏ sót khi reviewer mệt/vội | Cao — muốn scale lại phải viết test suite từ đầu |
| AI tooling tích hợp vào workflow có sẵn (editor/review/test loop) | Muốn AI thực sự giảm friction hàng ngày, muốn convention/review standard được encode nhất quán qua Skills/config | Chi phí setup Skills + project configuration ban đầu | Nếu tích hợp sai điểm friction → vẫn ít giá trị dù đã "configure Claude perfectly" | Trung bình — điều chỉnh lại Skills/config, không cần đổi hạ tầng |
| AI tooling dùng như chat window riêng (stalling at basic chat) | Giai đoạn onboarding rất sớm, trước khi team quen với AI | Thấp — không cần setup gì thêm | Cao — không bao giờ tiến lên tool use/repository-aware/Skills; team lãng phí năng lực thật của AI | Thấp về công sức kỹ thuật, nhưng cao về công sức thay đổi thói quen/văn hoá đã hình thành |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Diligence | 1 trong 4 AI Fluency competency của Anthropic; định nghĩa: "taking responsibility for what we do with AI and how we do it" — chịu trách nhiệm về việc dùng AI và cách dùng nó |
| Deployment diligence | Áp dụng cụ thể của Diligence: chịu trách nhiệm **verifying** và **vouching for** output trước khi dùng/chia sẻ |
| Verification checklist | Deliverable cụ thể của Diligence — tập check rõ ràng AI-generated output phải pass trước khi vào production, phủ 4 dimension |
| 4 dimension (correctness/security/maintainability/human understanding) | Bốn khía cạnh checklist phải phủ đủ; thiếu dimension nào (đặc biệt human understanding) là lỗ hổng ẩn dù test vẫn xanh |
| Human understanding check | Dimension yêu cầu người submit change giải thích được code làm gì và vì sao, kể cả với input chưa test explicit — dimension dễ bị bỏ qua nhất |
| Judgment erosion | Failure mode lớn nhất: team ship output không còn hiểu vì nó chỉ pass shallow check, tới khi 1 input chưa ai reason tới lọt vào production |
| Lumpy adoption | Failure mode: vài dev dùng AI tooling nhiều, phần còn lại gần như không dùng → team không nhận ra lợi ích thật, practice không standardize |
| Stalling at basic chat | Failure mode: team dừng ở dùng Claude như hộp hỏi-đáp, không tiến lên tool use/repository-aware/Skills vì chưa được enable đúng cách |
| Champion-and-batch rollout | Chiến lược từ C5.1 để tránh lumpy adoption — lan toả usage có kiểm soát theo batch, không để rơi hết vào early adopter |
| Gate (vs. judgment call) | Check được automate (test suite + eval set) chạy trên MỌI change, thay cho việc reviewer phải tự quyết định lại mỗi lần |
| AI Fluency competency | Khung 4 năng lực của Anthropic khi làm việc với AI (Diligence là 1 trong 4; 3 competency còn lại không nêu chi tiết trong lesson này) |
| Encode team knowledge | Vai trò của integration: đưa convention/review standard/quy trình lặp lại (thường chỉ nằm trong đầu người) vào Skills + project config để Claude áp dụng nhất quán |

## Gotchas / bẫy hay gặp
- [ ] Checklist chỉ phủ correctness (tests pass) nhưng bỏ qua **human understanding** — đúng lỗi trong case study "the merge nobody could explain": tests xanh, review pass, nhưng không ai hỏi "explain what it does and why" trước khi merge
- [ ] Coi "có access tới Claude" = "đã adoption" — thực ra team có thể vẫn stall at basic chat, chưa từng chạm tới tool use/repository-aware assistance/packaged Skills
- [ ] Để adoption trôi tự nhiên, chỉ rơi vào tay vài early adopter (lumpy adoption) → team không bao giờ đo được lợi ích thật, không chuẩn hoá được practice
- [ ] Đưa AI tooling vào như một chat window tách biệt, không tích hợp vào editor/review process/test loop hiện có → giảm friction ảo, không đổi được cách team thực sự làm việc
- [ ] Hạ quality bar khi nâng workflow bar — chấp nhận AI-generated code với chuẩn review thấp hơn code viết tay vì nó "ship nhanh hơn và nhìn đúng"
- [ ] Không automate được check nào automate được — để correctness/behavior verification là judgment call thủ công mỗi lần thay vì biến thành gate (test suite + eval set) chạy trên mọi change
- [ ] Nhầm AI flag (khi Claude review code) là verdict cuối cùng, thay vì chỉ là input để human judgment quyết định

## Exam tips
- Câu hỏi dạng "tests pass, code review pass, nhưng vẫn nên hold lại change này vì sao?" → đáp án nhiều khả năng là thiếu dimension **human understanding** trong verification checklist (author không giải thích được code) — không phải do test suite yếu.
- Phân biệt 2 failure mode: **lumpy adoption** = vấn đề về PHÂN BỔ usage trong team (vài người dùng nhiều, số còn lại không dùng); **stalling at basic chat** = vấn đề về TẦNG usage (cả team đứng ở mức chat hỏi-đáp, chưa lên tool use/Skills). Đề dễ đánh lừa hai khái niệm này với nhau.
- Câu hỏi "checklist nào đang thiếu dimension gì" → luôn map về đúng 4 nhóm: correctness (test/behavior), security (secrets/input validation/least-privilege), maintainability (convention/complexity), human understanding (author giải thích được). Nếu case study chỉ mô tả test pass + review pass mà vẫn xảy ra incident → thiếu human understanding.
- Nhớ nguyên tắc: "wherever a check can be made automatic, it should be" — nếu đề đưa ra 2 phương án (automate bằng test/eval vs. để reviewer tự judgment), chọn automate vì nó biến thành GATE lặp lại được, không phụ thuộc từng reviewer.

## Code / config snippets
```python
# Ví dụ minh hoạ verification checklist đủ 4 dimension (correctness/security/
# maintainability/human understanding) và hàm chặn merge nếu thiếu dimension.
# Dùng cho AI-generated code trước khi vào production (theo model answer của exercise C5.2).

verification_checklist = {
    "correctness": {
        "check": "Tests exist and pass; behavior khớp requirement, bao gồm edge case",
        "passed": True,   # kết quả check thực tế, do CI hoặc reviewer set
    },
    "security": {
        "check": "Không có secret trong code; input được validate; tool/external call dùng least-privilege",
        "passed": True,
    },
    "maintainability": {
        "check": "Code đọc rõ, theo team convention, không có complexity chưa giải thích",
        "passed": True,
    },
    "human_understanding": {
        # dimension dễ bị bỏ qua nhất — chính là lỗ hổng trong case study "the merge nobody could explain"
        "check": "Author có thể giải thích code làm gì, vì sao, và xử lý input chưa test explicit ra sao",
        "passed": False,  # ví dụ: chưa ai hỏi câu này trước khi merge -> phải block
    },
}


def can_merge(checklist: dict) -> tuple[bool, list[str]]:
    """
    Kiểm tra checklist đã đủ 4 dimension bắt buộc và tất cả đều passed chưa.
    Trả về (True, []) nếu được phép merge, ngược lại (False, [danh sách dimension thiếu/fail]).
    """
    # 4 dimension bắt buộc theo Diligence competency (deployment diligence)
    required_dimensions = {"correctness", "security", "maintainability", "human_understanding"}

    missing_or_failed = []

    # Kiểm tra thiếu dimension nào so với 4 dimension bắt buộc
    for dim in required_dimensions:
        if dim not in checklist:
            missing_or_failed.append(f"{dim} (chưa có trong checklist)")
        elif not checklist[dim].get("passed", False):
            missing_or_failed.append(f"{dim} (có trong checklist nhưng chưa pass)")

    can_go = len(missing_or_failed) == 0
    return can_go, missing_or_failed


# --- ví dụ chạy gate trước khi merge (mô phỏng CI gate, không phải chat/judgment call) ---
allowed, problems = can_merge(verification_checklist)
if not allowed:
    # Block merge và báo rõ dimension nào chưa đạt — tránh judgment erosion
    print("BLOCK MERGE. Chưa đạt các dimension sau:", problems)
else:
    print("OK to merge — đủ 4 dimension và tất cả đã pass.")
```

## Câu hỏi chưa rõ
- ?
