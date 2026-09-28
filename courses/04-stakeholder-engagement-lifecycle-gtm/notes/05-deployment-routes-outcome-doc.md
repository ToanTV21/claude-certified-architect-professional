# C4.5 — API vs. Bedrock vs. Vertex vs. third-party + outcome document

> **Course:** 4 — Stakeholder Engagement, Lifecycle & GTM (178 min) · **Exam domain:** D3 (19%) + D6 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Select the deployment entry point and cross-platform strategy for a multi-platform production system, comparing the direct API, Bedrock, Vertex, and third-party routes on latency, compliance, and cost, then produce an outcome document that makes the value legible to a non-technical sponsor and reusable as partner IP

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Entry-point selection quay lại nhưng câu hỏi đã đổi.** Ở module trước, việc chọn route (Direct Anthropic API / AWS Bedrock / GCP Vertex AI / Microsoft Foundry) đóng vai trò một **entry-point-and-compliance pre-filter**: chỉ hỏi "route nào SỐNG SÓT qua compliance filter" (partner procurement posture, regional compliance requirement nào loại route nào ra). Ở lesson này, hệ thống đã **live trên nhiều platform**, nên câu hỏi chuyển thành "route nào **PERFORM TỐT NHẤT** trên latency/cost/compliance của một multi-platform deployment đang chạy thật". Vì entry-point capability thay đổi liên tục, mọi claim cụ thể phải re-verify với platform.claude.com/docs và anthropic.com tại thời điểm build — không dùng số liệu cũ.
- **Cross-platform deployment lộ ra nhóm vấn đề mà hệ thống 1-entry-point không bao giờ thấy:**
  - **Model identifier string khác nhau giữa route** — cùng một model nhưng tên gọi trong API call khác nhau tuỳ Direct API / Bedrock / Vertex / Foundry, dễ gây lỗi khi copy code giữa route.
  - **Feature availability lag trên route đi qua CSP (Cloud Service Provider)** — Bedrock/Vertex/Foundry thường nhận feature mới **sau** Direct API vì phải qua lớp trung gian của cloud partner.
  - **Regional availability trên Bedrock/Vertex cần config TƯỜNG MINH (explicit)** — đây là gotcha quan trọng nhất: nếu để mặc định (default) về **global endpoint**, đây là lỗi phổ biến **phá vỡ (breaks) data-residency requirement** một cách âm thầm, vì hệ thống vẫn chạy bình thường, chỉ có dữ liệu bị route sai region.
  - Vì vậy, Architect thiết kế multi-entry-point **bắt buộc** phải có một **entry-point-responsibility map** đã viết ra trước khi viết dòng integration code đầu tiên.
- **Entry-point-responsibility map — vì sao cần:** một app tích hợp nhiều Claude entry-point trong cùng 1 workflow phải nói rõ **entry-point nào own task nào và vì sao**. Ví dụ enterprise scale không hiếm: dùng Direct API cho back-end inference, Claude Code cho một sub-task kỹ thuật, và một Bedrock endpoint riêng cho regulated data path. Mỗi ranh giới giữa 2 entry-point là **1 integration point riêng** với authentication, logging, và failure-mode profile của chính nó. Map này làm ranh giới đó thành **explicit** — mục đích chính là chặn lỗi multi-entry-point phổ biến nhất: một entry-point được chọn cho 1 task **dần dần "leo thang" nhận thêm task khác** chỉ vì routing logic chưa từng được document lại, khiến hệ thống trôi dần ra khỏi thiết kế ban đầu mà không ai nhận ra.
- **Outcome document — làm value hiểu được ngoài phạm vi team build.** Customer outcome documentation là thứ giúp người **không tham gia build** (sponsor, CFO, procurement...) hiểu được giá trị deployment mang lại. Document đầy đủ phải có **6 field**:
  1. Use case + scope boundary — deployment làm gì và **không** làm gì.
  2. Metric before deployment — con số business metric trước khi deploy.
  3. Metric after deployment — cùng metric đó, đo bằng **cùng definition**, sau khi deploy.
  4. Control in place — cái gì làm cho so sánh before/after **auditable** thay vì chỉ là lời khẳng định (assertion).
  5. Measurement owner — ai chịu trách nhiệm đo lường **tiếp tục** sau khi engagement đã đóng.
  6. Reuse potential — pattern này chuyển giao (transfer) sang customer/engagement khác được không, dưới dạng IP.
  - Điểm nhấn quan trọng: **technical metrics một mình KHÔNG đủ** để tạo ra document này — chính before/after trên business outcome + reuse note mới là thứ biến nó thành một **reusable asset**, không chỉ là báo cáo kỹ thuật.
  - (Partner Track note: phần "reuse the pattern for other customers/engagements" và field Reuse-potential là nội dung liên quan Partner Track; phần còn lại của outcome document nằm on-blueprint ở mục 6.4.)
- **Deployment-entry-point decision matrix (4 route):**
  1. **Direct Anthropic API** — Latency: nhận feature mới nhất trước tiên, ít hop nhất. Compliance: mặc định mạnh nhưng vẫn phải confirm coverage bằng configuration. Khi chọn: dùng làm default trừ khi có procurement rule hoặc residency rule chỉ định route khác.
  2. **AWS Bedrock** — Latency: region-configurable, có thể feature lag so với Direct API. Compliance: phù hợp AWS-centric procurement + region rule **khi được config tường minh**. Khi chọn: partner đã standardize trên AWS, cần in-region execution.
  3. **GCP Vertex AI** — Latency: region-configurable, có thể feature lag so với Direct API. Compliance: phù hợp GCP-centric procurement + region rule khi config tường minh. Khi chọn: partner standardize trên GCP có sẵn Vertex procurement path.
  4. **Microsoft Foundry (Azure)** — Latency: **thay đổi theo hosting form** — hosted-on-Azure model chạy inference trong Azure environment của partner (đã GA — General Availability); hosted-on-Anthropic model thì route sang infrastructure của Anthropic. Compliance: phải verify residency + coverage **theo từng route riêng**, **không được suy (assume) từ tên platform**. Khi chọn: procurement/residency posture của partner yêu cầu đúng route cụ thể đó.
- **Case study "Watch Out" — outcome document đo sai thứ:** deployment chạy tốt trong controlled rollout, có data trong tay. Architect đóng engagement viết outcome document nhanh từ metrics sẵn có — cảm giác đúng nhưng engagement kết thúc trước khi ai nhận ra document **không trả lời được câu gì**. Architect chọn metric dễ export nhất: request volume, average latency, error rate. Sponsor mang document này lên gặp CFO để xin mở rộng deployment. Sponsor nói: "40,000 requests/tháng, latency trung bình dưới 2 giây, error rate dưới 0.5%." CFO hỏi lại: "Điều đó cho tôi biết hệ thống chạy được. Nhưng nó làm được GÌ cho chúng ta? Claim processing time trước đây là bao nhiêu, giờ là bao nhiêu? Vì đó là số quyết định có nên chi thêm tiền hay không." Sponsor không có gì để trả lời — document đo việc hệ thống **WORKED** (chạy được), không đo việc nó **CHANGED** (thay đổi) gì.
  - Cái gãy: document chỉ có technical metric, thiếu business outcome. Volume/latency/error rate là số thật và đáng track, nhưng không cái nào là business outcome. Field còn thiếu để document dùng được: before-and-after trên business metric mà use case nhắm tới (claims-processing time), và control làm cho so sánh đó auditable. Không có số before → không có "story". Không có control → số after chỉ là assertion. Document hoàn chỉnh như một technical record nhưng **vô dụng** như một case xin mở rộng ngân sách.
  - Vì sao lỗi này xảy ra: metric dễ export nhất hiếm khi là metric justify được chi phí. Observability stack thu thập technical metric "miễn phí", nhưng nếu không anchor vào business data thì chỉ còn lại dashboard trông có vẻ informative mà **không có nghĩa** cho người ra quyết định ngân sách. Outcome document tồn tại cho một **reader khác** — sponsor phải justify deployment lên cấp trên. Bài học: capture metric before **ngay từ đầu** (trước khi deploy), gọi tên control làm comparison auditable, và thêm reuse note — để document làm được việc mà một technical dashboard không làm được.
- **Checkpoint — chọn platform + required outcome field, decision model 3 input:** Primary cloud platform (AWS / GCP / Microsoft Foundry / Direct — no cloud) × Regulatory obligation level (None / Moderate / Strict) × Primary performance constraint (Latency-sensitive / Cost-sensitive / Compliance-sensitive) → suy ra Primary platform, Secondary platform, và required outcome fields. Checkpoint này **không có đáp án cố định** (raw content không chốt 1 answer key) — đây là interactive decision-model, kết quả phụ thuộc vào 3 input đã chọn. Cách suy luận (reasoning) khi gặp dạng câu này trong exam:
  - **Primary platform**: bám decision matrix ở trên — cloud preference quyết định route (AWS→Bedrock, GCP→Vertex, Microsoft→Foundry, không có cloud preference→Direct API), sau đó refine bằng regulatory level (Strict + có yêu cầu cloud/region cụ thể → route của cloud đó; None/Moderate không có cloud preference → default Direct API) và bằng performance constraint (Latency-sensitive thường nghiêng về Direct API vì ít hop nhất, trừ khi residency buộc phải qua cloud route).
  - **Secondary platform**: "Direct Anthropic API" hợp lý làm fallback/secondary khi primary là route qua CSP (Bedrock/Vertex/Foundry) — vì feature có thể lag; chọn "None required" khi Direct API đã là primary.
  - **Required outcome fields**: base luôn là "Metric before + Metric after" (bài học trung tâm của case study screen 15); thêm "Reuse potential" khi scenario nói rõ về tạo reusable IP cho customer/engagement khác (Partner-Track framing); thêm "Control in place + Measurement owner" khi deployment có regulatory/audit obligation (Strict hoặc Moderate), vì so sánh phải auditable, không chỉ được assert.
  - Điểm mấu chốt khi làm bài dạng này: luôn quay lại **decision matrix (screen 14)** để chọn platform, và **6-field outcome template** để chọn field cần — không học vẹt 1 tổ hợp cố định.
- **Cost · Complexity · Risk (theo lesson):**
  - **Cost**: chọn sai deployment platform hoặc viết outcome document sơ sài là rẻ để làm nhưng đắt để sửa — residency mismatch có thể block cutover; document chỉ có metrics thì không justify được expansion.
  - **Complexity**: multi-platform routing nhân số integration point lên, mỗi cái có auth/logging/failure profile riêng — entry-point-responsibility map là thứ duy nhất giữ cho hệ thống này còn hiểu được theo thời gian.
  - **Risk**: rủi ro tốn kém nhất là (1) default configuration âm thầm phá data-residency, hoặc (2) outcome document mà sponsor không thể mang lên gặp CFO vì nó chưa từng capture business value.

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Direct Anthropic API | Default khi không có procurement/residency rule nào chỉ định route khác; cần feature mới nhất, latency thấp nhất (ít hop) | Thấp — không qua lớp CSP trung gian, setup đơn giản nhất | Không fit khi partner có policy "phải qua cloud của họ" (AWS/GCP/Azure procurement) — có thể bị loại ngay từ compliance pre-filter | Thấp — đổi sang route khác chủ yếu là đổi model identifier string + auth, ít lock-in |
| AWS Bedrock | Partner đã standardize trên AWS, cần in-region execution, procurement đi qua AWS marketplace | Trung bình — cần config region tường minh, có thể tốn thời gian setup IAM/VPC | Feature lag so với Direct API; **default về global endpoint phá data-residency** nếu quên config region rõ ràng | Trung bình–cao — đã tích hợp theo AWS IAM/logging thì đổi route phải làm lại auth + observability layer |
| GCP Vertex AI | Partner standardize trên GCP, có sẵn Vertex procurement path, cần region rule theo GCP | Trung bình — tương tự Bedrock, cần config region + IAM tường minh | Feature lag so với Direct API; cùng rủi ro default global endpoint phá residency | Trung bình–cao — tương tự Bedrock, gắn với GCP IAM/logging riêng |
| Microsoft Foundry (Azure) | Procurement/residency posture của partner yêu cầu đúng route Foundry (thường đi kèm hệ sinh thái Azure) | Trung bình–cao — phải verify riêng **từng hosting form** (hosted-on-Azure GA vs hosted-on-Anthropic), không suy từ tên platform | Risk cao nhất nếu nhầm 2 hosting form với nhau — compliance/residency claim đúng cho form này có thể sai cho form kia | Cao — sai hosting form ảnh hưởng trực tiếp residency, phải re-verify + có thể re-migrate route |
| Outcome document chỉ có technical metrics (volume/latency/error rate) | Không nên chọn làm final deliverable — chỉ là raw data thu thập được, chưa phải outcome document hoàn chỉnh | Rẻ — observability stack xuất ra "miễn phí", không cần thêm công đo business metric | Cao — sponsor không trả lời được câu hỏi "trước/sau thế nào" của CFO, mất luôn case xin mở rộng ngân sách (case study screen 15) | Cao — phải quay lại đo business metric **before** đã trôi qua mất, không thể tái tạo "before" sau khi deploy |
| Outcome document đủ 6 field (use case+scope, before, after, control, owner, reuse potential) | Chuẩn bắt buộc khi đóng engagement, đặc biệt khi sponsor cần justify expansion hoặc khi cần tạo reusable IP | Cao hơn — phải capture metric before **từ đầu**, định nghĩa control auditable, xác định owner + reuse note | Thấp — document đứng vững trước câu hỏi CFO, dùng lại được cho engagement/customer khác như partner IP | Thấp — chỉ cần update lại theo engagement mới, không phải làm lại từ đầu |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Entry point | Con đường truy cập Claude: Direct Anthropic API, AWS Bedrock, GCP Vertex AI, Microsoft Foundry — mỗi route có compliance posture + latency profile riêng |
| Entry-point-and-compliance pre-filter | Cách dùng entry-point selection ở giai đoạn sớm: chỉ hỏi route nào "sống sót" qua compliance/procurement requirement, chưa xét performance |
| Full production picture | Góc nhìn khi hệ thống đã live multi-platform: câu hỏi chuyển từ "route nào hợp lệ" sang "route nào perform tốt nhất trên latency/cost/compliance" |
| Entry-point-responsibility map | Document nói rõ entry-point nào own task nào và vì sao, viết trước khi code integration — chặn lỗi 1 entry-point "leo thang" nhận thêm task ngoài phạm vi |
| Model identifier string | Tên gọi model trong API call — khác nhau giữa Direct API/Bedrock/Vertex/Foundry, dễ gây lỗi khi port code giữa route |
| Feature lag | Feature mới ra chậm hơn trên route đi qua CSP (Bedrock/Vertex/Foundry) so với Direct API vì phải qua lớp trung gian |
| Regional availability / global endpoint default | Bedrock/Vertex cần config region tường minh; default về global endpoint là lỗi phổ biến phá vỡ data-residency requirement |
| Outcome document | Tài liệu 6 field làm value của deployment hiểu được với người không tham gia build, đồng thời là reusable IP |
| Metric before / Metric after | Business metric đo trước và sau deployment, dùng cùng definition — phần bắt buộc để so sánh có nghĩa (không phải technical metric) |
| Control in place | Cơ chế làm cho so sánh before/after auditable (kiểm chứng được) thay vì chỉ là lời khẳng định |
| Measurement owner | Người chịu trách nhiệm đo lường tiếp tục sau khi engagement đã đóng |
| Reuse potential | Khả năng pattern deployment chuyển giao sang customer/engagement khác dưới dạng IP (nội dung liên quan Partner Track) |
| Microsoft Foundry hosting form | 2 dạng khác nhau trong cùng route Foundry: hosted-on-Azure (chạy trong Azure environment của partner, GA) vs hosted-on-Anthropic (route sang infra Anthropic) — compliance phải verify riêng từng form |
| Technical metrics vs business outcome | Volume/latency/error rate là technical metric (đo hệ thống "chạy được"); business outcome là before/after trên metric mà use case nhắm tới (VD claims-processing time) |

## Gotchas / bẫy hay gặp
- [ ] Để **default về global endpoint** trên Bedrock/Vertex thay vì config region tường minh — hệ thống vẫn chạy bình thường nhưng âm thầm phá vỡ data-residency requirement
- [ ] Copy nguyên model identifier string giữa các route (Direct API ↔ Bedrock ↔ Vertex ↔ Foundry) — mỗi route có tên gọi model khác nhau, dễ lỗi khi port code
- [ ] Thiết kế multi-entry-point mà **không có entry-point-responsibility map** trước khi code — một entry-point được chọn cho 1 task dần "leo thang" nhận thêm task khác không ai document
- [ ] Suy compliance/residency của Microsoft Foundry từ **tên platform** thay vì verify riêng từng hosting form (hosted-on-Azure GA vs hosted-on-Anthropic) — 2 form có compliance posture khác nhau
- [ ] Viết outcome document chỉ từ **metrics dễ export** (volume/latency/error rate) mà không có before/after trên business metric — document "hoàn chỉnh" về kỹ thuật nhưng vô dụng để justify expansion
- [ ] Bỏ qua field **Control in place** trong outcome document — không có control, số "after" chỉ là assertion, không auditable
- [ ] Không capture metric **before** ngay từ đầu (trước khi deploy) — sau khi deploy rồi mới muốn viết outcome document thì không còn cách nào tái tạo lại con số before
- [ ] Coi entry-point selection ở giai đoạn production là **giống hệt** compliance pre-filter ban đầu — quên rằng câu hỏi đã đổi từ "route nào hợp lệ" sang "route nào perform tốt nhất"

## Exam tips
- Câu scenario "chọn deployment route cho partner X" → luôn map theo compliance/procurement posture trước (partner standardize trên cloud nào, có region rule không), rồi mới xét latency/feature; Direct API là default khi không có rule nào chỉ định route khác.
- Câu hỏi cho một outcome document mẫu và hỏi "còn thiếu gì" → kiểm tra đủ 6 field; thiếu **Metric before/after** hoặc **Control in place** là đáp án phổ biến nhất (bám case study CFO ở screen 15).
- Câu hỏi về Bedrock/Vertex và region → cảnh giác đáp án nào ngụ ý "cứ dùng default/global endpoint" — đó chính là lỗi phá data-residency mà lesson cảnh báo.
- Câu hỏi liên quan Microsoft Foundry → phân biệt rõ 2 hosting form (hosted-on-Azure GA vs hosted-on-Anthropic); không chọn đáp án suy compliance/latency chung cho cả "Foundry" mà không nói rõ form nào.

## Code / config snippets
```python
# Ví dụ minh hoạ 2 công cụ nên có trước khi build 1 multi-entry-point deployment:
# (1) entry-point-responsibility map — map rõ task nào do entry-point nào own + lý do
# (2) outcome document 6 field + hàm kiểm tra field nào còn thiếu

# --- (1) Entry-point-responsibility map ---
# Mục đích: viết ra TRƯỚC khi code integration, để routing logic không bị "leo thang"
# (1 entry-point nhận thêm task ngoài phạm vi ban đầu mà không ai để ý)
entry_point_responsibility_map = {
    "backend_inference": {
        "entry_point": "direct_api",
        "reason": "Cần feature mới nhất + latency thấp nhất, không có residency rule ràng buộc",
    },
    "engineering_subtask": {
        "entry_point": "claude_code",
        "reason": "Sub-task kỹ thuật nội bộ, không đi qua data path của khách hàng",
    },
    "regulated_data_path": {
        "entry_point": "aws_bedrock",
        "reason": "Partner standardize trên AWS + cần in-region execution cho dữ liệu regulated",
    },
}


# --- (2) Outcome document — đủ 6 field theo template của lesson ---
outcome_document = {
    "use_case_scope": "Tự động trích xuất field từ claim document; KHÔNG xử lý claim tranh chấp (dispute)",
    "metric_before": None,  # con số claims-processing time TRƯỚC deploy — phải capture từ đầu
    "metric_after": None,   # cùng metric, đo bằng cùng definition, SAU deploy
    "control_in_place": None,  # cơ chế làm so sánh before/after auditable (VD: audit log, sampling)
    "measurement_owner": None,  # ai chịu trách nhiệm đo lường tiếp sau khi engagement đóng
    "reuse_potential": None,   # pattern này chuyển giao sang customer/engagement khác thế nào
}


def missing_outcome_fields(doc: dict) -> list[str]:
    """
    Kiểm tra outcome document đã đủ 6 field bắt buộc chưa.
    Chỉ có technical metrics (volume/latency/error rate) KHÔNG đủ —
    thiếu metric_before/metric_after/control_in_place là lỗi hay gặp nhất
    (xem case study CFO ở screen 15: document không trả lời được "trước/sau thế nào").
    """
    required_fields = [
        "use_case_scope",
        "metric_before",
        "metric_after",
        "control_in_place",
        "measurement_owner",
        "reuse_potential",
    ]
    # Field coi là "thiếu" nếu không tồn tại trong dict hoặc giá trị là None
    return [field for field in required_fields if doc.get(field) is None]


if __name__ == "__main__":
    missing = missing_outcome_fields(outcome_document)
    if missing:
        print(f"Outcome document CHƯA hoàn chỉnh, còn thiếu: {missing}")
    else:
        print("Outcome document đủ 6 field — sẵn sàng đưa cho sponsor/CFO.")
```

## Câu hỏi chưa rõ
- ?
