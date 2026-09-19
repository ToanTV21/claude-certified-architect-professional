CCAR-P TIP & TRICK
Format: Keyword/Trigger -> Pattern đáp án -> Bẫy thường gặp

==================================================
1. TOOL SEARCH / MANY MCP TOOLS
==================================================

Keyword / Trigger:
- many MCP tools
- too many tool definitions
- context pressure
- hundreds of tools
- don't want to remove capabilities
- discover tools only when needed

-> Tool Search / on-demand discovery

Pattern đúng:
- Không load toàn bộ tool schema upfront
- Chỉ discover/expose tool cần thiết tại thời điểm cần dùng
- Giảm context overhead nhưng vẫn giữ capability

Bẫy:
- Remove most tools
- Put all MCP definitions into the system prompt
- Increase context window only
- Load every tool schema every turn

Mẹo nhớ:
Many tools + context pressure -> Tool Search


==================================================
2. MCP: TOOL VS RESOURCE
==================================================

Keyword:
- external integration
- reusable service integration
- expose data
- action/function
- context/data source

Pattern:
Tool     -> thực hiện action/function
Resource -> cung cấp data/context

Bẫy:
- Xem mọi thứ trong MCP đều là Tool
- Dùng Resource cho thao tác side-effect
- Dùng Tool chỉ để expose static context khi resource phù hợp hơn

Mẹo:
Need action -> Tool
Need data/context -> Resource


==================================================
3. CLAUDE CODE PROJECT CONFIG
==================================================

Keyword:
- same repository
- team-wide configuration
- shared project setup
- commit configuration to repo

Pattern:
- .claude/settings.json
- .mcp.json

Bẫy:
- Chỉ đặt config ở user scope
- Mỗi developer tự cấu hình thủ công
- Hard-code machine-specific config vào project khi không cần

Mẹo:
Shared by team/repository -> Project scope


==================================================
4. PERMISSION DENIED / CONFIG PRECEDENCE
==================================================

Keyword:
- permission denied unexpectedly
- command should be allowed
- multiple scopes
- user/project/local permission rules

Pattern đúng:
- Inspect effective permission rules across scopes
- Kiểm tra precedence / deny rule / inherited config

Bẫy:
- Allow all Bash
- Disable permission checks
- Retry cùng lệnh liên tục
- Assume project config is the only source

Mẹo:
Unexpected deny -> inspect effective rules, not bypass security


==================================================
5. HUMAN-IN-THE-LOOP
==================================================

Keyword:
- AI-assisted
- preserve human approval
- reviewer still decides
- branch protection remains

Pattern:
AI -> analyze / comment / suggest
Human -> approve / merge / final decision

Bẫy:
- Auto merge
- AI final approval
- Disable branch protection
- Replace reviewer completely

Mẹo:
AI recommends, Human decides


==================================================
6. HARD SECURITY CONSTRAINT
==================================================

Keyword:
- must not connect to public internet
- compliance requirement
- security boundary
- network restriction
- hard rule

Pattern đúng:
- Enforce deterministically through architecture / policy / runtime controls
- Treat as non-negotiable constraint

Bẫy:
- Put only in prompt
- Let model decide when exception is acceptable
- Trade off security for convenience

Mẹo:
Hard security/compliance -> deterministic enforcement


==================================================
7. SYSTEM PROMPT VS SOFT GUIDANCE
==================================================

Keyword:
- always behave this way
- persistent rule
- across all requests
- avoid specific behavior

Pattern:
Persistent behavioral rule -> System prompt

Bẫy:
- Put recurring rule only in one user prompt
- Rely on examples alone when rule must always apply

Mẹo:
Always / across all tasks -> System prompt


==================================================
8. FEW-SHOT FOR RECURRING MISTAKES
==================================================

Keyword:
- repeated classification error
- model keeps making same type of mistake
- needs to learn pattern
- examples available

Pattern:
- Give representative positive/negative examples
- Show expected input -> output behavior

Bẫy:
- Only say "be careful"
- Increase temperature
- Add unrelated context

Mẹo:
Recurring pattern error -> Few-shot


==================================================
9. EXPLICIT CRITERIA
==================================================

Keyword:
- high confidence
- conservative
- be careful
- ambiguous decision boundary

Pattern đúng:
Replace vague wording with explicit criteria / thresholds / conditions

Ví dụ:
"Be conservative"
-> yếu

"Flag only when conditions X, Y, Z are satisfied"
-> mạnh hơn

Bẫy:
- Dùng adjective mơ hồ thay cho rule
- Assume model hiểu "strict" giống business

Mẹo:
Explicit > vague


==================================================
10. STRUCTURED OUTPUT
==================================================

Keyword:
- strict JSON
- downstream parser
- machine-readable
- fixed fields
- schema

Pattern:
- Use schema-enforced structured output / tool schema
- Define required/optional fields clearly

Bẫy:
- Free-form text rồi regex parse
- Chỉ yêu cầu "return JSON" nhưng không có schema
- Mix explanation ngoài JSON khi parser yêu cầu strict format

Mẹo:
Machine consumes output -> Schema


==================================================
11. MISSING VALUE -> NULL
==================================================

Keyword:
- source does not provide value
- field unknown
- missing evidence

Pattern:
- Return null / explicit missing status
- Do not fabricate a plausible value

Bẫy:
- Guess
- Infer unsupported value
- Fill placeholder as if factual

Mẹo:
No evidence -> null, not hallucination


==================================================
12. SCHEMA VALID != SEMANTICALLY CORRECT
==================================================

Keyword:
- JSON valid but value wrong
- schema-valid but impossible
- business rule violated
- invalid range

Pattern:
- Add semantic/business validation after schema validation

Ví dụ:
{"age": -500}
-> syntactically valid integer
-> semantically invalid

Bẫy:
- Assume schema guarantees correctness
- Retry blindly without identifying semantic issue

Mẹo:
Schema correctness != semantic correctness


==================================================
13. RETRY: WHEN TO RETRY
==================================================

Transient errors:
- timeout
- temporary unavailable
- rate limit

-> retry/backoff

Non-retryable errors:
- invalid permission
- bad request
- unsupported action
- missing mandatory information

-> reason / change request / escalate

Bẫy:
- Retry every error
- Infinite loop
- Treat policy/permission error as transient

Mẹo:
Temporary -> Retry
Invalid request/permission -> Reason


==================================================
14. RETRIEVAL: DENSE / SPARSE / STRUCTURED / HYBRID
==================================================

Dense retrieval:
Keyword:
- semantic meaning
- paraphrase
- concept similarity

-> Dense

Sparse / BM25:
Keyword:
- exact phrase
- rare token
- identifier
- error code
- exact keyword

-> Sparse

Structured retrieval:
Keyword:
- SQL filters
- exact field conditions
- aggregation
- relational data

-> Structured

Hybrid:
Keyword:
- need semantic meaning + exact term matching

-> Hybrid

Bẫy:
- Dense-only cho exact identifier
- Sparse-only cho paraphrase
- Random sampling cho production retrieval

Mẹo:
Meaning -> Dense
Exact -> Sparse
DB/filter -> Structured
Meaning + Exact -> Hybrid


==================================================
15. RAG: RETRIEVE RELEVANT, NOT EVERYTHING
==================================================

Keyword:
- huge knowledge base
- too much context
- only small portion relevant

Pattern:
- Retrieve only the relevant chunks
- Rerank/filter if needed

Bẫy:
- Load entire corpus into context
- Randomly sample documents
- Assume bigger context automatically improves answer

Mẹo:
Relevant evidence > maximum context


==================================================
16. GROUNDING REGRESSION
==================================================

Keyword:
- retrieval results unchanged
- source is correct
- model starts contradicting source
- behavior changed after model/prompt update

Pattern:
- Check grounding/system instructions
- Compare against previous model/version
- Isolate whether regression is model-side vs retrieval-side

Bẫy:
- Rebuild vector database immediately
- Increase context window first
- Assume retrieval is broken when retrieved evidence is unchanged

Mẹo:
Retrieval same + answer changed
-> investigate grounding/model regression


==================================================
17. EVALUATION FRAMEWORK
==================================================

Keyword:
- compare prompt versions
- compare model versions
- regression
- measure quality over iterations

Pattern:
- Use stable evaluation framework
- Reuse reference set
- Compare results consistently across versions

Bẫy:
- Judge based on a few anecdotes
- Change eval dataset every iteration
- Rebuild benchmark from scratch each time

Mẹo:
Iteration -> same baseline/reference set


==================================================
18. CONTINUITY ACROSS LIFECYCLE
==================================================

Keyword:
- continuity practices
- deployment lifecycle
- next phase
- lessons learned
- iterations

Strong patterns:
1. Carry evaluation framework/reference set forward
2. Capture lessons learned and feed them into next phase

Bẫy:
- Archive every artifact just for completeness
- Notify every stakeholder at every phase transition
- Lock early decisions forever

Mẹo:
Carry forward what works
+
Feed lessons forward


==================================================
19. MULTI-AGENT ORCHESTRATION
==================================================

Keyword:
- investigate multiple evidence areas
- ownership / litigation / cybersecurity / market evidence
- parallel research
- distinct sources
- final synthesis

Pattern:
- Give each area a specialized worker
- Bounded context
- Clear output schema
- Area-specific tools
- Coordinator combines/reconciles results

Bẫy:
- All workers edit one shared conclusion continuously
- No ownership boundary
- No conflict handling
- Sequentialize every independent task

Mẹo:
Independent domains -> parallel specialized workers


==================================================
20. SUBAGENT DESIGN
==================================================

Keyword:
- recurring specialization
- reusable reviewer role
- repeat same expert task across sessions
- database reviewer / security reviewer / test reviewer

Pattern:
Use a dedicated subagent with:
- system prompt
- trigger/description
- permitted tools
- model choice
- review criteria

Bẫy:
- Recreate long ad-hoc prompt every time
- Give subagent every tool by default
- No clear responsibility boundary

Mẹo:
Recurring specialized role -> dedicated subagent


==================================================
21. BOUNDED CONTEXT
==================================================

Keyword:
- specialized worker
- separate evidence area
- context isolation
- avoid irrelevant information

Pattern:
Each worker gets only context needed for its task

Bẫy:
- Give every agent the full case file
- Duplicate entire conversation into all agents

Mẹo:
Scoped task -> scoped context


==================================================
22. CLEAR OUTPUT SCHEMA FOR AGENTS
==================================================

Keyword:
- coordinator must combine outputs
- multiple workers
- preserve citations
- compare evidence

Pattern:
Require structured worker output, e.g.:
- findings
- evidence
- citations
- confidence
- gaps
- unresolved conflicts

Bẫy:
- Free-form essays from every worker
- No distinction between evidence and inference

Mẹo:
Multi-agent synthesis -> standardized output contract


==================================================
23. COVERAGE GAPS
==================================================

Keyword:
- missing evidence
- incomplete source coverage
- unavailable records
- final report must state limitations

Pattern:
Explicitly report:
- what was searched
- what was found
- what was unavailable
- resulting coverage gap

Bẫy:
- Fill gap with assumption
- Hide missing evidence
- Treat no evidence as evidence of absence

Mẹo:
Missing evidence -> disclose gap, don't guess


==================================================
24. CONFLICT RECONCILIATION
==================================================

Keyword:
- workers disagree
- conflicting evidence
- contradictory findings

Pattern:
Coordinator:
1. compare evidence
2. preserve citations
3. reconcile or mark unresolved
4. synthesize final result

Bẫy:
- Let latest worker overwrite previous result
- Average conflicting claims
- Pick one without evidence

Mẹo:
Conflict -> reconcile before synthesis


==================================================
25. PARALLEL VS SEQUENTIAL
==================================================

Parallel:
- independent evidence areas
- tasks do not depend on each other's outputs

Sequential:
- step B requires output from step A
- transformation pipeline

Bẫy:
- Run all tasks sequentially just because they are separate
- Run dependent steps in parallel

Mẹo:
Independent -> Parallel
Dependent -> Sequential


==================================================
26. WORKFLOW VS AGENT
==================================================

Workflow:
- deterministic
- fixed steps
- predictable sequence
- low ambiguity

Agent:
- dynamic reasoning
- choose tools/actions
- open-ended investigation

Bẫy:
- Use agent for simple deterministic pipeline
- Use rigid workflow when adaptive reasoning is essential

Mẹo:
Fixed path -> Workflow
Adaptive path -> Agent


==================================================
27. SEPARATION OF RESPONSIBILITIES
==================================================

Keyword:
- planning
- searching
- citation capture
- writing
- ownership boundaries

Pattern:
Separation is useful when it improves:
- specialization
- verification
- accountability

But:
Do not split blindly into excessive sequential stages if tasks are independent.

Mẹo:
Separate by responsibility, not for the sake of separation


==================================================
28. CITATION PRESERVATION
==================================================

Keyword:
- due diligence
- final report
- source traceability
- preserve citations

Pattern:
Evidence worker output should carry citation/source metadata into synthesis

Bẫy:
- Remove source metadata during summarization
- Let final writer invent/reattach citations from memory

Mẹo:
Evidence and citation should travel together


==================================================
29. ARCHITECTURE / DESIGN DOCUMENT FIRST
==================================================

Keyword:
- architecture guide
- design document
- intended audience
- technical depth
- structure/outline

Pattern:
Before drafting:
- identify audience
- define purpose/scope
- establish outline / sections

Bẫy:
- Start writing immediately with no audience model
- Optimize prose before structure

Mẹo:
Audience + purpose + outline before full draft


==================================================
30. GUARDRAILS
==================================================

Keyword:
- policy enforcement
- risky action
- forbidden behavior
- compliance boundary

Pattern:
- Prompt guidance for soft behavior
- Deterministic controls for hard constraints

Bẫy:
- Trust model self-restraint for hard compliance
- Replace policy enforcement with natural language only

Mẹo:
Soft -> prompt
Hard -> deterministic guardrail


==================================================
31. EVIDENCE VS ASSUMPTION
==================================================

Keyword:
- insufficient evidence
- unsupported conclusion
- due diligence
- confidence

Pattern:
Separate clearly:
- fact/evidence
- inference
- uncertainty
- gap

Bẫy:
- Phrase inference as fact
- Hide uncertainty
- Fill unknown fields with plausible content

Mẹo:
Evidence > assumption


==================================================
32. TOOL DESCRIPTION QUALITY
==================================================

Keyword:
- agent chooses wrong tool
- tools seem similar
- tool misuse

Pattern:
Improve:
- name
- description
- usage conditions
- input schema
- examples/boundaries

Bẫy:
- Add more tools
- Increase model temperature
- Blame orchestration before fixing unclear tool semantics

Mẹo:
Wrong tool choice often starts with unclear tool description


==================================================
33. MULTI-AGENT SHARED STATE
==================================================

Bad pattern:
All agents continuously edit the same conclusion/document
without ownership or conflict handling

Why bad:
- race/conflict
- provenance lost
- hard to know who changed what
- contradictions overwrite each other

Better:
- each agent owns its output
- coordinator synthesizes later

Mẹo:
Shared artifact can be useful,
but ownership + merge logic must be explicit


==================================================
34. ON-DEMAND TOOL DISCOVERY
==================================================

Keyword:
- preserve capability
- reduce token overhead
- large tool catalog

Pattern:
Discover tools only when task indicates they are relevant

Bẫy:
- expose all tools all the time
- remove capabilities permanently

Mẹo:
Need capability without context overload -> deferred/on-demand discovery


==================================================
35. BUSINESS VALUE / DESIGN CHOICE
==================================================

When choosing between architecture options:
Prefer the option that:
- addresses root cause
- scales operationally
- preserves observability/evidence
- keeps human control where required
- minimizes unnecessary context/tool exposure

Bẫy:
- solutions that only hide symptoms
- brute-force more tokens/context
- remove safeguards for convenience


==================================================
CHEAT SHEET SIÊU NGẮN
==================================================

many MCP tools / context pressure
-> Tool Search / on-demand discovery

shared repo config
-> .claude/settings.json + .mcp.json

unexpected permission deny
-> inspect effective permission rules across scopes

AI-assisted review + human approval
-> AI suggest, human decides

hard security/compliance
-> deterministic enforcement

recurring model mistake
-> Few-shot

persistent behavior
-> System prompt

vague "be careful"
-> explicit criteria

strict machine-readable output
-> schema-enforced structured output

missing source value
-> null / explicit missing

valid JSON but impossible value
-> semantic validation

semantic meaning
-> Dense retrieval

exact token / code / ID
-> Sparse/BM25

DB filter / aggregate
-> Structured retrieval

semantic + exact
-> Hybrid retrieval

retrieval unchanged but answer changed
-> grounding/model regression

compare iterations
-> stable eval framework + same reference set

lifecycle continuity
-> carry eval baseline + lessons forward

independent evidence areas
-> parallel specialized workers

recurring expert role
-> dedicated subagent

specialized worker
-> bounded context

multi-agent synthesis
-> clear output schema

missing evidence
-> report coverage gap

conflicting worker outputs
-> coordinator reconciles

independent tasks
-> parallel

dependent tasks
-> sequential

fixed deterministic steps
-> workflow

adaptive reasoning
-> agent

citations required
-> preserve source metadata with evidence

wrong tool selection
-> improve tool description/boundaries

hard guardrail
-> code/policy/runtime control

unsupported conclusion
-> state uncertainty, don't invent


==================================================
META-RULES CẦN NHỚ
==================================================

1. Explicit > vague
   Specific criteria thắng các instruction kiểu "be careful".

2. Scoped > everything
   Chỉ đưa tool/context cần thiết.

3. Structured > free-form
   Schema/output contract giúp downstream và multi-agent đáng tin cậy hơn.

4. Deterministic > prompt-only
   Khi liên quan hard security/compliance.

5. Specialized > giant generalist
   Khi role chuyên môn lặp lại và có giá trị vận hành.

6. Evidence > assumption
   Thiếu evidence thì nói thiếu, không đoán.

7. Human control > full automation
   Khi đề yêu cầu approval/review của con người.

8. Evaluate > assume
   So sánh bằng stable eval/reference set thay vì cảm tính.

9. Root cause > brute force
   Đừng mặc định tăng context, thêm tools, retry nhiều hơn.

10. Independent -> Parallel
    Dependent -> Sequential
