# C3.5 — Compliance obligation → control → owner → evidence artifact

> **Course:** 3 — Responsible AI, Safety & Risk for Architects (114 min) · **Exam domain:** D5 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Map each compliance obligation to a named control, an owner, and an evidence artifact, so the architecture can be accurately audited

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Nhắc lại từ Course 2 — compliance chỉ là PRE-FILTER, chưa phải proof:** ở lesson integration architecture (Course 2), governing obligation (HIPAA, GDPR, FedRAMP, attorney-client privilege, data-residency policy) được dùng để **loại bỏ** delivery route/entry point không hợp lệ TRƯỚC KHI cost/engineering preference được xét tới. Kết quả của bước đó là 1 entry point/route **sống sót** qua obligation — nhưng đó chỉ là **điều kiện cần**, chưa phải điều kiện đủ. Reviewer không coi "đã chọn entry point compliant" là bằng chứng rule đang được tuân thủ trong thực tế — họ hỏi thêm: ai own control này, và evidence nào cho thấy nó đang chạy.
- **Nguyên tắc trung tâm — "regulation nêu outcome, Architect cung cấp control + proof":** framework như GDPR/HIPAA/FedRAMP chỉ phát biểu **outcome** phải đạt được (dữ liệu nhạy cảm được xử lý theo cách nào đó, access được kiểm soát, processing diễn ra trong environment được authorize) — KHÔNG chỉ định implementation kỹ thuật cụ thể. Việc chọn technical control là trách nhiệm của Architect. Mỗi obligation phải được biến thành **3 thứ** do Architect sở hữu:
  1. **Technical control** cụ thể đạt được outcome đó
  2. **Owner** — người chịu trách nhiệm cho control đó
  3. **Evidence artifact** — thứ chứng minh control đang **LIVE** (đang chạy thật, không chỉ có trên giấy)
  - Evidence artifact là phần **hay bị bỏ sót nhất** — nhưng lại là phần reviewer kiểm tra kỹ nhất, nên luôn phải có mặt trong mapping, không phải optional.
- **Bảng mapping 4 obligation → control/owner/evidence** (ví dụ cốt lõi của lesson):

  | Obligation | Technical control | Evidence artifact reviewer chấp nhận | Owner |
  |---|---|---|---|
  | Protected health data xử lý theo agreement (HIPAA) | Chỉ dùng HIPAA-ready Enterprise plan hoặc first-party API configuration nằm dưới signed BAA, bật HIPAA compliance, chỉ scope các feature eligible | Signed BAA + admin setting cho thấy HIPAA compliance đã enable + danh sách eligible-feature | Security lead |
  | US government workload ở impact level yêu cầu (FedRAMP) | Deliver qua route đã được Anthropic document là authorized ở đúng impact level, không dùng entry point chưa authorize | Authorization record của route đã chọn + xác nhận workload chạy độc quyền trên route đó | Platform owner |
  | Dữ liệu lưu/xử lý trong approved region (data residency) | Config regional processing/storage cho approved region, validate xem log/cache/monitoring/retention path có nằm trong boundary đã approve hay không | Residency configuration + data-flow record cho biết mọi copy của dữ liệu đang nằm ở đâu | Data owner |
  | Decision phải reconstruct được khi cần (transparency, cross-framework — liên quan cluster fairness) | Decision logging đã build trong fairness cluster, retain và query được trong khoảng thời gian yêu cầu | Một bản sample reconstruction của 1 decision lấy trực tiếp từ live log | Architect |

- **Training-use vs retention — 2 claim khác nhau, KHÔNG được gộp:** "data không dùng để train model theo default" và "data có được retain/lưu lại hay không" là hai câu trả lời **độc lập**. Dữ liệu có thể bị **exclude khỏi training by default** nhưng vẫn bị **retained** (giữ lại) hoặc monitor cho mục đích logging, abuse prevention, legal compliance, hoặc audit theo config. Nếu đưa "không dùng để train" ra làm evidence cho obligation về retention (hoặc ngược lại) là sai loại claim — reviewer sẽ bắt bài ngay vì 2 câu trả lời cho 2 câu hỏi khác nhau.
- **Evidence artifact là thứ reviewer INSPECT được — khác hẳn design document:** security/legal reviewer chỉ chấp nhận proof dạng: signed agreement, configuration screen, authorization record, hoặc kết quả trả về từ 1 log query. Họ **không** chấp nhận 1 design document chỉ "identify" ra control mà không có owner, không có evidence — vì 1 control không ai chứng minh được là đang chạy thì **không thể phân biệt** với 1 control không tồn tại/không chạy. Đây chính là điểm nối lại với logic "constraint-elimination" đã dùng ở Course 2: hồi đó loại route không sống sót được constraint; bây giờ phải **record** — cho từng obligation — control nào thỏa nó và artifact nào chứng minh điều đó.
- **Cost · Complexity · Risk của việc duy trì mapping này:**
  - **Cost**: sản xuất + maintain evidence cho mọi obligation là công việc **liên tục** (ongoing), không làm 1 lần rồi xong — configuration có thể drift, artifact có thể stale, nên control register phải được **revalidate theo cadence định kỳ**.
  - **Complexity**: control + owner + living evidence artifact cho từng obligation là mức độ governance cao hơn hẳn so với chỉ chọn 1 entry point — cần sự đồng thuận giữa security/legal/platform owner về ai giữ phần nào.
  - **Risk**: 1 control ghi ra nhưng không có owner, không có evidence là **invisible tại audit** — nó có thể ngừng hoạt động mà không ai biết, và gap đó lộ ra ở bước **review** (khi đã quá muộn, tốn kém nhất) thay vì lộ ra lúc **design** (khi sửa còn rẻ).
- **Case study "passing entry point ≠ finishing compliance" (Watch Out screen):** 1 team chọn 1 delivery route compliant cho regulated workload rồi coi compliance là **settled**. Họ map obligation → control **một lần**, tại thời điểm design, ghi vào document — không gắn owner, không wire logging nào để chứng minh control đang hoạt động. Obligation data-residency là nơi lỗi tập trung: control **đúng trên giấy** lúc design (processing pin vào approved region), nhưng vài tháng sau, 1 thay đổi trong logging configuration bắt đầu ghi request metadata sang 1 store ở **region thứ hai**. Không ai phát hiện thay đổi này — vì không ai own residency control, không có artifact nào theo dõi dữ liệu đang nằm ở đâu. Gap chỉ lộ ra tại **audit**, khi reviewer hỏi evidence cho thấy data ở đúng region và team chỉ có 1 design document (không phải data-flow record sống). Bài học: sống sót qua pre-filter bị nhầm thành **đã đạt compliance** — 1 route compliant chỉ là **prerequisite**, không phải proof; mỗi obligation cần control + owner + evidence **sống** được revalidate khi deployment thay đổi, vì control có thể đúng lúc design và **âm thầm sai (silently false)** ở production mà không ai bắt được nếu không có artifact nào đang "canh".
- **Checkpoint "Justify the control choice" (đáp án đúng: A):** obligation "protected health data phải xử lý theo formal agreement (HIPAA)". Control đúng là **HIPAA-ready plan/first-party API dưới signed BAA**, và lý do load-bearing để reviewer chấp nhận nó là proof là: **signed agreement + configuration đã enable là artifact reviewer inspect được** — không phải vì "model được instruct cẩn thận với health data" (instruction không phải evidence enforceable) và không phải vì dùng content filter runtime bắt sensitive term (filter đó không tự thỏa mãn obligation "xử lý theo formal agreement"). Nguyên tắc chốt: control phải **fit đúng obligation**, và lý do đưa ra phải **nêu tên 1 artifact inspect được** — 1 instruction hay 1 runtime filter không phải evidence verify được đối với chính obligation "handled under a formal agreement".

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Document control 1 lần lúc design, không owner/không evidence sống (cách team trong case study làm) | KHÔNG nên chọn — chỉ liệt kê ở đây làm anti-pattern để so sánh; đôi khi bị chọn nhầm vì "route đã compliant" tạo cảm giác đã xong | Thấp lúc design (chỉ viết document 1 lần) | Cao — control có thể silently false ở production (VD: logging config đổi region), gap chỉ lộ ra lúc audit, sửa ở giai đoạn này tốn kém + mất uy tín nhất | Rất cao — phải dựng lại toàn bộ owner + evidence pipeline sau khi đã bị audit bắt lỗi, kèm remediation cho khoảng thời gian control đã fail |
| Control register sống, có owner + evidence artifact, revalidate theo cadence định kỳ | Default cho mọi obligation compliance trong production system — đặc biệt obligation có thể drift theo config (residency, BAA scope) | Cao hơn, liên tục (ongoing) — phải maintain artifact, lên lịch revalidate, phối hợp security/legal/platform owner | Thấp hơn nhiều — gap bị bắt ở lúc revalidate/design thay vì lúc audit; luôn có người chịu trách nhiệm | Trung bình — đổi cadence/owner/artifact tương đối rẻ vì đã có process, không phải dựng từ đầu |
| HIPAA-ready plan + signed BAA (entry point cho protected health data) | Workload có protected health data, cần agreement chính thức với vendor | Cost hợp đồng (BAA) + giới hạn scope chỉ dùng eligible feature | Nếu BAA hết hạn/scope đổi mà không revalidate → mất evidence, control coi như không tồn tại | Trung bình — renegotiate/renew BAA, nhưng route kỹ thuật không cần đổi nhiều |
| FedRAMP-authorized route (entry point cho US government workload) | Government workload cần impact level cụ thể | Cost cao hơn để đảm bảo chạy exclusively trên route đã authorize (không lẫn route khác) | Nếu workload âm thầm chạy qua entry point không-authorized (kể cả 1 phần) → evidence "chạy exclusively" bị vô hiệu, gap khó phát hiện nếu không có confirmation record | Cao — phải re-route toàn bộ traffic + re-issue authorization record |
| Regional pinning (entry point cho data residency) | Dữ liệu phải nằm trong 1 approved region | Cost để validate toàn bộ path phụ (log/cache/monitoring/retention) cùng nằm trong boundary, không chỉ path chính | Rủi ro cao nhất trong 4 loại — dễ bị phá vỡ bởi thay đổi tưởng như không liên quan (VD: đổi logging config) mà không ai để ý nếu thiếu data-flow record sống | Cao — phải audit lại toàn bộ data-flow, di dời data đã lỡ ghi sai region (có thể vướng thêm nghĩa vụ pháp lý khác) |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Compliance pre-filter | Bước dùng governing obligation để loại route/entry point không hợp lệ TRƯỚC khi xét cost/engineering preference (từ Course 2) — điều kiện cần, chưa phải proof |
| Control register | Danh sách sống (living) ghi obligation → control → owner → evidence artifact, phải revalidate định kỳ, không phải document viết 1 lần |
| Evidence artifact | Vật chứng cụ thể reviewer inspect được để xác nhận control đang LIVE: signed agreement, configuration screen, authorization record, log query result |
| BAA (Business Associate Agreement) | Hợp đồng ký kết bắt buộc theo HIPAA khi 1 bên xử lý protected health data thay cho covered entity |
| FedRAMP impact level | Mức độ rủi ro (Low/Moderate/High) mà US government workload yêu cầu route xử lý phải đáp ứng, được Anthropic document route nào đạt |
| Data residency | Yêu cầu dữ liệu (bao gồm log/cache/monitoring/retention path) phải được xử lý/lưu trữ trong 1 region địa lý được approve |
| Data-flow record | Evidence artifact cho obligation residency — ghi lại mọi nơi 1 bản copy dữ liệu đang tồn tại, dùng để chứng minh không có copy lạc ra ngoài region |
| Training-use vs retention | 2 claim độc lập: "data không dùng để train model" (default exclusion) khác với "data có bị retain/lưu lại" (logging, abuse prevention, legal, audit) — không được gộp làm 1 evidence |
| Decision reconstructable | Yêu cầu transparency cross-framework: có thể tái tạo lại 1 decision cụ thể từ log, dùng decision logging đã build ở fairness cluster làm control |
| Owner (control owner) | Cá nhân/role chịu trách nhiệm cho 1 control cụ thể (VD: Security lead cho HIPAA, Platform owner cho FedRAMP, Data owner cho residency, Architect cho decision logging) |
| Constraint-elimination reasoning | Logic đã dùng ở Course 2 khi loại route không sống sót qua constraint; ở lesson này áp dụng tiếp để "record" control/evidence cho route đã sống sót |

## Gotchas / bẫy hay gặp
- [ ] Coi entry point/route "compliant" (đã pass pre-filter) là compliance đã **xong** — thực ra đó chỉ là prerequisite, chưa có control + owner + evidence thì chưa chứng minh được gì
- [ ] Map obligation → control **một lần** lúc design rồi ghi vào document, không gắn owner, không wire evidence sống — control có thể đúng trên giấy nhưng silently false ở production (case study data-residency trong lesson)
- [ ] Gộp claim "training-use" và "retention" thành 1 — nói "data không dùng để train" như thể đó cũng là evidence cho việc "data không bị retain/lưu lại", trong khi đây là 2 câu hỏi độc lập
- [ ] Đưa 1 design document (chỉ "identify" control, không owner, không evidence) ra làm proof cho reviewer — reviewer không chấp nhận, vì control không ai chứng minh được = không phân biệt được với control không chạy
- [ ] Dùng "model được instruct cẩn thận" hoặc "có content filter runtime" làm evidence cho obligation dạng agreement (HIPAA/BAA) — instruction/filter không phải artifact enforceable/inspectable cho đúng loại obligation đó
- [ ] Không revalidate control register theo cadence — configuration drift (VD: đổi logging config ghi data sang region khác) mà không ai phát hiện vì thiếu owner + data-flow record sống
- [ ] Nghĩ risk compliance nằm ở lúc design — thực ra risk cao nhất là gap giữa lúc control "đúng lúc design" và lúc nó "âm thầm sai ở production", chỉ lộ ra khi audit hỏi evidence

## Exam tips
- Câu hỏi dạng "control X có đủ làm evidence cho obligation Y không" → check control có nêu tên được 1 **artifact reviewer inspect được** (signed agreement, config screen, authorization record, log query) không; nếu chỉ là instruction/design intent/runtime filter chung → SAI, không đủ làm evidence.
- Câu hỏi phân biệt "đã chọn entry point compliant" vs "đã proof compliance" → nhớ nguyên tắc route compliant là **prerequisite**, không phải proof; câu trả lời đúng luôn cần thêm owner + evidence sống, không chỉ route.
- Câu hỏi chọn owner đúng cho 1 loại obligation → map theo pattern của lesson: HIPAA/BAA → Security lead; FedRAMP → Platform owner; data residency → Data owner; decision reconstructable/transparency → Architect (vì gắn với control kỹ thuật — decision logging — mà Architect thiết kế).
- Câu hỏi tình huống "control đúng lúc design nhưng lỗi ở production, không ai phát hiện" → nguyên nhân gốc luôn là thiếu **owner** hoặc thiếu **living evidence artifact revalidate định kỳ**, không phải do chọn sai control ban đầu.
- Đề có thể gài "training-use" và "retention" làm 2 lựa chọn trông giống nhau để đánh lừa — luôn tách 2 claim này ra khi đọc câu hỏi.

## Code / config snippets
```python
"""
Minh hoạ cấu trúc 1 record trong "control register" — không phải code production,
chỉ để hình dung cách track obligation -> control -> owner -> evidence artifact
sống được, thay vì ghi 1 lần vào design document rồi bỏ quên.
"""
from datetime import date, timedelta

# Mỗi obligation là 1 record trong control register.
# "evidence_artifact" phải là thứ INSPECT được (đường dẫn tới BAA đã ký,
# tên config screen, id của authorization record, query log...),
# không phải 1 câu mô tả ý định hay "model đã được instruct".
control_register = [
    {
        "obligation": "HIPAA - protected health data handled under agreement",
        "control": "HIPAA-ready Enterprise plan / first-party API dưới signed BAA",
        "owner": "Security lead",
        "evidence_artifact": "contracts/baa_signed_2026.pdf + admin_console:hipaa_enabled=true",
        "last_revalidated": date(2026, 6, 1),
    },
    {
        "obligation": "Data residency - approved region only",
        "control": "Regional processing/storage pinned to APAC region",
        "owner": "Data owner",
        "evidence_artifact": "data_flow_record:apac_only_2026Q2.json",
        "last_revalidated": date(2026, 1, 10),  # <-- đã lâu, dễ bị stale
    },
]

# Cadence revalidate: obligation nào cũng phải được check lại định kỳ,
# vì configuration (logging, retention, routing...) có thể drift âm thầm
# như trong case study data-residency của lesson này.
REVALIDATION_CADENCE_DAYS = 90

def find_stale_controls(register: list[dict], today: date = None) -> list[dict]:
    """
    Trả về danh sách control đã quá hạn revalidate.
    Đây chính là cách biến control register từ "document tĩnh"
    thành "artifact sống" — nếu không có hàm này (hoặc tương đương),
    register sẽ rơi vào đúng lỗi của case study: đúng lúc design,
    không ai biết nó còn đúng ở production hay không.
    """
    today = today or date.today()
    stale = []
    for record in register:
        deadline = record["last_revalidated"] + timedelta(days=REVALIDATION_CADENCE_DAYS)
        if today > deadline:
            stale.append(record)
    return stale


if __name__ == "__main__":
    # Giả lập ngày hiện tại để test — trong thực tế lấy date.today()
    stale_records = find_stale_controls(control_register, today=date(2026, 9, 28))
    for r in stale_records:
        print(f"[STALE] {r['obligation']} — owner: {r['owner']} cần revalidate evidence")
```

## Câu hỏi chưa rõ
- ?
