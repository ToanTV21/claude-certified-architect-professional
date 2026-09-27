# C3.1 — Model training giảm gì vs. application layer phải enforce gì

> **Course:** 3 — Responsible AI, Safety & Risk for Architects (114 min) · **Exam domain:** D5 (14%) · **Status:** ✅ Đã học

## Learning objective (nguyên văn từ course)
> Distinguish between what the model's training reduces and what your application layer must still enforce

## Tóm tắt nội dung (tiếng Việt, keyword giữ nguyên tiếng Anh)
- **Bối cảnh module (chỉ để hiểu, không phải nội dung chính của lesson):** Module 3 (Responsible AI, Safety & Risk for Architects) bắt đầu từ điểm module 1–2 đã kết thúc — hệ thống đã có architecture, model, use-case sizing, eval suite, và đã wire Claude vào enterprise stack. Module 3 hỏi câu hỏi tiếp theo: cái gì đang chặn hệ thống refuse sai 1 request hợp lệ, tạo ra outcome không công bằng, hoặc thực hiện 1 action không ai approve? Module chia 5 phần tuần tự, phần sau build trên phần trước: (1) **Alignment boundary** — ranh giới training vs application layer (chính là lesson C3.1 này), (2) Guardrail placement (input/output screening, tool-call authorization), (3) Fairness & transparency, (4) Human-review routing, (5) Compliance control register. Lesson C3.1 nằm ở vị trí đầu tiên vì nó ảnh hưởng đến mọi quyết định phía sau — nếu vẽ sai ranh giới alignment, tất cả layer guardrail dựng sau đó đều dựa trên giả định sai.
- **Constitution — nền của trained behavior:** Anthropic train Claude dựa trên một **Constitution**: văn bản mô tả value/behavior mà model nên thể hiện. Model được deploy với broad safety behavior đã có sẵn từ bước này — Anthropic revise document này theo thời gian (bản public gần nhất tính đến thời điểm học là tháng 1/2026). Constitution được dùng trong training để sinh ví dụ cho model học và để rank các candidate response với nhau; nó **định hình** cách model phản hồi request ambiguous/sensitive nhưng **không nhất thiết bắt được** mọi bad output — tức Constitution là cơ chế shaping hành vi ở training time, không phải 1 bộ filter runtime.
- **Priority order khi goal xung đột:** Constitution đặt ra thứ tự ưu tiên: **be broadly safe > be ethical > comply with guidelines > be genuinely helpful** (đối với operator và user). Thứ tự này quan trọng vì 1 câu trả lời "helpful" đôi khi lại "unsafe". Điểm cần nhớ: ordering này là **holistic, không phải strict sequence** — goal ưu tiên cao hơn thường được model ưu tiên hơn khi xung đột, nhưng model cân nhắc (weigh) các goal cùng nhau chứ không áp dụng tuần tự cứng nhắc kiểu if-else. Nhờ Constitution, model đến tay Architect với 1 class harmful output đã được giảm sẵn trước khi Architect viết prompt đầu tiên — nhưng layer này chỉ cover harm ở mức broad, general-purpose, **không cover domain-specific policy** của product/partner cụ thể.
- **Training-time alignment vs inference-time control — 2 layer mục đích khác nhau:**
  - **Training-time alignment**: định hình behavior của model **trước khi deploy**, giảm broad classes of harmful output bằng cách steer Claude refuse request nguy hiểm, default về response an toàn hơn. Vì được set trước khi bất kỳ deployment nào tồn tại → nó mang tính **general by design**. Đây vừa là strength vừa là weakness: model không biết domain policy của partner, data-handling rule, hay authorization model của riêng deployment đó. Một request có thể hoàn toàn "fit" với general alignment của Claude nhưng vẫn vi phạm 1 rule specific cho deployment (ví dụ: disclose order info của customer khác, advise ngoài script đã approved). Nguyên tắc cốt lõi: **Claude không thể enforce 1 rule nó chưa từng được cho biết.**
  - **Inference-time control**: enforce các rule specific cho deployment, gồm runtime guardrail do Architect config: system instructions, input/output check, tool permission, human review gate. System instructions có thể shape behavior, nhưng policy specific cho deployment chỉ thực sự được enforce khi **đi kèm** runtime control (screening, authorization, review) — nói cách khác, system prompt tự nó không phải enforcement. Tóm gọn: training-time alignment hạ baseline risk chung; inference-time control enforce rule riêng của deployment.
- **A layered view — 4 layer xếp từ trong (Claude) ra ngoài (Architect), mỗi layer cover 1 phần layer dưới không cover, và fail theo cách layer sau phải bắt được:**

  | Layer | Reliably covers | Does not cover | Owner |
  |-------|------------------|-----------------|-------|
  | 1. Trained behavior | Broad classes of harmful/unsafe output, áp dụng cho mọi request không cần config | Domain policy, data rule, authorization model riêng của bạn | Anthropic |
  | 2. System-prompt instruction | Role, tone, các constraint được nêu để steer Claude trong 1 request | Bất cứ gì mà input adversarial/bất thường có thể "nói" Claude bỏ qua — instruction không phải enforcement | Architect |
  | 3. Runtime screening | Input/output screening phát hiện disallowed content | Action có side effect (screening không authorize hành động), và attack mới mà classifier miss | Architect |
  | 4. Authorization | Một action cụ thể có side effect có được phép cho caller này, trong context này, hay không | Content quality và fairness | Architect |

- **Cost · Complexity · Risk của kiến trúc 4 layer:**
  - **Cost**: mỗi layer thêm vào tốn latency + engineering effort. Ví dụ pre-screen input + check output = thêm 2 API call/rule cho mỗi request.
  - **Complexity**: 4 layer = 4 nơi phải design, version, test riêng. System prompt và screening logic có thể **drift độc lập** với nhau nếu không được governance đồng bộ.
  - **Risk**: failure nguy hiểm nhất là **silent failure** — giả định Claude đã enforce 1 domain rule mà nó chưa từng được cho biết. Vì rule đó không tồn tại ở **bất kỳ** layer nào, không có gì ngăn được vi phạm — hệ thống vẫn "trông" an toàn cho tới khi có audit hoặc incident.
- **Case study "Watch Out" — trained refusal bị nhầm là domain policy:** 1 team deploy internal assistant cho partner có data-handling policy cấm user truy cập record thuộc business unit khác. Trong review, Claude refuse mọi harmful prompt team thử → team **suy diễn** rằng cross-unit disclosure cũng đã được safety behavior này cover, nên không build authorization check riêng cho rule đó. Khi lên production: 1 request bình thường, đúng domain, nhưng hỏi 1 record bị cấm — không có gì "harmful" ở mức general nên Claude trả lời luôn. Rule mà team tin là đã được enforce **thực ra không tồn tại ở đâu cả** — chưa từng nằm trong training, chưa từng được encode vào classifier/system prompt/application control, vì team đã giả định model tự động cover nó. Bài học: domain policy bị conflate (nhầm lẫn) với trained alignment — trained refusal chỉ cover broad harm, không cover rule specific-cho-deployment; bất kỳ rule nào specific cho partner **phải** được enforce ở 1 layer do chính Architect xây.
- **Checkpoint "Sort the responsibility"** — 5 obligation, phân vào 2 bucket theo nguyên tắc "broad universal harm = trained behavior; bất cứ gì deployment/domain/partner-specific = application layer, Architect own":
  - Refusing to help synthesize a dangerous weapon → **Claude's trained behavior** (broad universal harm).
  - Never returning another tenant's data → **Application layer** (domain/tenant-specific rule).
  - Declining to produce plainly hateful content → **Claude's trained behavior** (broad universal harm).
  - Blocking advice outside the partner's approved script → **Application layer** (rule cụ thể theo partner).
  - Requiring a sign-off before a refund is issued → **Application layer** (business process/authorization cụ thể).

## Trade-off analysis
| Option | Khi nào chọn | Cost | Risk | Reversal (đảo ngược tốn gì) |
|--------|--------------|------|------|------------------------------|
| Giả định trained behavior đã cover domain/partner policy (không build enforcement riêng) | Không nên chọn — chỉ hợp lý khi rule thực sự là broad universal harm (weapon synthesis, hate content) mà Anthropic đã train sẵn | Thấp lúc build (không tốn effort thêm) | **Rất cao** — silent failure: rule không tồn tại ở layer nào, production request bình thường vẫn vi phạm domain policy mà không ai biết cho tới audit/incident (case study cross-tenant data) | Cao — phải phát hiện gap trước (thường là sau incident), rồi mới thiết kế + build lại authorization layer từ đầu, kèm retro-audit các request đã lọt qua |
| Tự build application-layer enforcement (system prompt + runtime screening + authorization) cho mọi domain/partner-specific rule | Mặc định bắt buộc cho bất kỳ rule nào specific-cho-deployment: tenant isolation, script phạm vi tư vấn, sign-off trước khi thực hiện action | Trung bình–cao — thêm latency (extra check/API call mỗi request) + engineering effort để design/version/test từng layer | Thấp hơn — rule được enforce chủ động, risk chỉ còn ở việc layer bị misconfigure/bị bypass (không phải "rule không tồn tại") | Trung bình — sửa 1 layer (VD: đổi rule authorization) không kéo theo phải retrain hay đổi model |
| Layer 1 — Trained behavior (Anthropic own) | Broad, universal harm áp dụng cho mọi request, không cần config gì thêm | Không tốn cost triển khai (đã có sẵn khi dùng Claude) | Không cover domain policy, data rule, authorization riêng — Architect không có quyền chỉnh sửa layer này | Không thể "đảo ngược" — đây là behavior cố định của model, chỉ đổi được bằng cách Anthropic revise Constitution/train lại |
| Layer 2 — System-prompt instruction (Architect own) | Khi cần steer role/tone/constraint cho 1 request, mức độ rủi ro thấp–trung bình | Thấp — chỉ là text trong prompt, không thêm call | Không phải enforcement thật — input adversarial/unusual có thể khiến Claude bỏ qua instruction | Rất thấp — sửa system prompt là thay đổi rẻ, áp dụng ngay |
| Layer 3 — Runtime screening (Architect own) | Cần phát hiện disallowed content ở input/output, cho behavior có thể check bằng classifier/rule | Trung bình — thêm 1 call/check mỗi request (latency + engineering) | Không authorize được action có side effect; attack mới/novel có thể lách qua classifier | Trung bình — thay/update rule hoặc classifier, cần test lại trước khi rollout |
| Layer 4 — Authorization (Architect own) | Khi action có side effect thật (data access, refund, gọi tool) cần permission check theo caller + context | Trung bình — cần thiết kế authorization model (role, scope, tenant) và maintain nó | Không đánh giá được content quality/fairness — chỉ trả lời "được phép hay không" | Trung bình–cao — thay đổi authorization model có thể ảnh hưởng nhiều flow đang chạy, cần audit lại permission hiện có |

## Key terms
| Term (EN) | Giải thích (VN) |
|-----------|-----------------|
| Constitution | Văn bản Anthropic dùng để train Claude, mô tả value/behavior model nên thể hiện; dùng để sinh training example và rank candidate response; được revise theo thời gian |
| Priority order (holistic ordering) | Thứ tự ưu tiên khi goal xung đột: broadly safe > ethical > compliant with guidelines > genuinely helpful; là holistic (model cân nhắc cùng nhau) không phải strict sequence (if-else cứng) |
| Training-time alignment | Lớp behavior được shape **trước khi deploy**, giảm broad classes of harmful output; general by design nên không biết domain policy riêng của deployment |
| Inference-time control | Lớp enforcement **tại runtime**, do Architect config: system instruction, input/output screening, tool permission, human review gate — enforce rule specific-cho-deployment |
| Alignment boundary | Đường ranh giới giữa "cái training đã giảm sẵn" và "cái application layer phải tự enforce" — vẽ sai boundary này ảnh hưởng mọi guardrail xây phía sau |
| System-prompt instruction | Chỉ dẫn đặt trong system prompt để steer role/tone/constraint; chỉ là shaping, không phải enforcement thật (có thể bị adversarial input "nói" Claude bỏ qua) |
| Runtime screening | Kiểm tra input/output tại thời điểm chạy để phát hiện disallowed content, bằng model-based hoặc deterministic check |
| Authorization (layer) | Cơ chế xác định 1 action có side effect (data access, tool call, refund...) có được phép cho caller/context cụ thể hay không |
| Fail closed / silent failure | Failure nguy hiểm nhất trong lesson này: giả định 1 rule đã được enforce trong khi nó không tồn tại ở layer nào — hệ thống vẫn "trông" an toàn cho tới khi bị phát hiện |
| Domain / deployment-specific policy | Rule chỉ áp dụng cho 1 partner/product cụ thể (VD: tenant isolation, script tư vấn được approve) — luôn thuộc trách nhiệm Architect, không phải trained behavior |

## Gotchas / bẫy hay gặp
- [ ] Thấy Claude refuse mọi harmful prompt trong testing → suy diễn rằng model cũng đã cover luôn domain/partner policy (VD: cross-tenant data) → không build authorization check riêng (case study "Watch Out" trong lesson)
- [ ] Conflate (nhầm lẫn) "trained alignment cho broad harm" với "domain policy cụ thể của deployment" — 2 thứ hoàn toàn khác nhau, trained refusal không tự động mở rộng sang rule chưa từng được dạy
- [ ] Coi system-prompt instruction là enforcement thật — thực chất nó chỉ shape behavior trong điều kiện bình thường, input adversarial/bất thường vẫn có thể khiến Claude bỏ qua
- [ ] Chỉ đặt 1 filter/check ở cuối request path (VD: chỉ check output) mà bỏ qua input screening và tool-call authorization — 1 layer không cover được 2 điểm còn lại
- [ ] Risk cao nhất không phải "hệ thống trông thiếu an toàn" mà là **silent failure**: rule không tồn tại ở bất kỳ layer nào nên request bình thường, đúng domain vẫn vi phạm mà không ai biết cho tới audit/incident
- [ ] Quên rằng ordering của priority order (broadly safe > ethical > compliant > helpful) là holistic — không nên áp dụng như if-else tuần tự cứng khi phân tích scenario

## Exam tips
- Câu scenario hỏi "obligation X thuộc Claude's trained behavior hay application layer" → áp nguyên tắc: **broad universal harm** (weapon, hate content, general dangerous instructions) = trained behavior (Anthropic own); **bất cứ gì domain/partner/deployment-specific** (tenant isolation, script phạm vi, sign-off trước action) = application layer (Architect own).
- Câu hỏi dạng "hệ thống pass mọi harmful-prompt test nhưng vẫn vi phạm 1 rule cụ thể ở production, vì sao" → đáp án đúng thường là: rule đó **chưa từng được encode ở bất kỳ layer nào** (không phải model yếu, không phải cần retrain) — team đã giả định trained alignment cover nó.
- Phân biệt rõ training-time alignment (general, set trước deployment, Anthropic own, không biết domain policy) vs inference-time control (system instruction + runtime screening + authorization + human review, Architect config, enforce rule riêng deployment) — đề hay test khả năng gọi đúng tên layer nào chịu trách nhiệm.
- Nhớ layer nào "does not cover" gì: System-prompt instruction không phải enforcement (bị bypass bởi adversarial input); Runtime screening không authorize action có side effect; Authorization không đánh giá content quality/fairness — đề có thể hỏi "layer nào phù hợp để chặn hành động X" dựa trên bảng 4-layer này.
- Priority order (broadly safe > ethical > compliant with guidelines > helpful) là **holistic, không phải strict sequence** — nếu đề đưa ra option mô tả ordering như if-else cứng nhắc, đó là distractor.

## Code / config snippets
```python
"""
Minh hoạ sự khác biệt giữa:
1) System-prompt instruction (Layer 2) — chỉ SHAPE behavior, không enforce
2) Authorization check riêng (Layer 4) — enforcement thật cho 1 domain rule cụ thể

Domain rule ví dụ (giống case study trong lesson):
"Never return another tenant's data" — rule này KHÔNG nằm trong Claude's
trained behavior, vì nó specific cho deployment/partner này. Nếu chỉ dựa
vào system prompt thì vẫn có thể bị adversarial input "nói" Claude bỏ qua.
"""

# Layer 2 — System-prompt instruction: chỉ là text hướng dẫn, KHÔNG phải enforcement
SYSTEM_PROMPT = """
Bạn là trợ lý nội bộ cho công ty X.
Chỉ trả lời dựa trên dữ liệu thuộc về tenant (business unit) của người hỏi.
Không được tiết lộ dữ liệu của tenant khác.
"""
# -> Đây chỉ là "lời nhắc". Nó KHÔNG chặn được request nếu Claude bị
#    thuyết phục / hiểu nhầm request là hợp lệ trong domain.

# Layer 4 — Authorization: enforcement THẬT, tách biệt hoàn toàn khỏi model call
def authorize_record_access(caller_tenant_id: str, record_tenant_id: str) -> bool:
    """
    Check authorization độc lập với Claude — chạy TRƯỚC khi trả bất kỳ record nào.
    Đây là control mà Architect PHẢI tự xây, vì trained behavior của Claude
    không hề biết khái niệm "tenant" của hệ thống này.
    """
    # So sánh tenant của người gọi với tenant của record được yêu cầu
    return caller_tenant_id == record_tenant_id


def handle_request(caller_tenant_id: str, requested_record: dict) -> str:
    # Gọi Claude để lấy câu trả lời (đã có system prompt ở trên hỗ trợ shaping)
    # response = client.messages.create(system=SYSTEM_PROMPT, ...)

    # Nhưng dù Claude trả lời gì, vẫn PHẢI qua authorization check riêng
    # trước khi cho phép trả record về cho user — đây là điểm enforcement thật
    if not authorize_record_access(caller_tenant_id, requested_record["tenant_id"]):
        # Fail closed: từ chối thay vì "tin tưởng" Claude đã tự chặn đúng
        return "Access denied: record does not belong to your tenant."

    return requested_record["content"]
```

## Câu hỏi chưa rõ
- ?
