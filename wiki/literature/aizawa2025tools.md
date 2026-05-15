---
type: literature
citekey: aizawa2025tools
title: Writing effective tools for agents — with agents
authors: [Aizawa, Ken, and Anthropic contributors]
year: 2025
venue: Anthropic Engineering Blog (Sep 11, 2025)
raw_path: raw/literature/Aizawa(2025).pdf
related_concepts: [tools-component, deterministic-tools-hypothesis, framework-four-components, context-engineering, agent-infrastructure-vs-capability]
related_work: []
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Aizawa (2025) — Writing effective tools for agents — with agents

## Summary

An Anthropic engineering post (Sep 11, 2025) by Ken Aizawa describing a **systematic, evaluation-driven workflow for designing high-quality MCP tools**, with the additional twist that Claude itself is in the loop as a co-author and tool optimiser. The opening framing is the most thesis-relevant single sentence in the Anthropic tools canon: *"Tools are a new kind of software which reflects a contract between deterministic systems and non-deterministic agents."* Traditional software is a contract between deterministic systems; tools are a contract across the deterministic/non-deterministic boundary. From this premise the post derives a workflow (prototype → evaluate → iterate with Claude Code) and a set of design principles (choose the right tools, namespace, return high-signal context, optimise token efficiency, prompt-engineer descriptions). Two reported numbers anchor the empirical claims: Claude-optimised internal Slack tools moved from **67.4% → 80.1%** on held-out test set accuracy; Asana tools from **79.6% → 85.7%**. For the thesis, this is the canonical Anthropic statement of *tools as a designed artefact*, the operational complement to [[anthropic2024mcp]]'s protocol-level description.

## Main claims

### 1. Tools are a contract across the deterministic/non-deterministic boundary

The post's central conceptual move. Compare:
- `getWeather("NYC")` — deterministic function, called by deterministic caller, returns the same thing every time.
- A *tool* "weather" exposed to an agent — non-deterministic caller, may or may not call, may call with the wrong parameters, may hallucinate the response, may ask a clarifying question instead.

**Implication:** "writing software for agents" is not the same activity as "writing software for systems or developers." The discipline of API design for humans does not transfer wholesale; tools must be *designed for agents*.

This is the operational form of the thesis's [[deterministic-tools-hypothesis]]: deterministic primitives sit at the interface; an LLM orchestrator chooses among them; the design of that interface is where productivity is won or lost.

### 2. The workflow — prototype, evaluate, iterate with Claude

**Prototype.**
- Stand up local MCP server or DXT (Desktop Extension).
- Test in Claude Code via `claude mcp add <name> <command> [args...]` or in Claude Desktop via Settings > Extensions.
- LLM-friendly docs (flat `llms.txt`) help Claude Code generate one-shot prototypes.

**Evaluation.**
- Generate dozens of prompt/response pairs grounded in **real-world tasks** (not sandbox toys).
- Strong tasks require multiple, sometimes dozens of tool calls. Examples:
  - *"Schedule a meeting with Jane next week to discuss our latest Acme Corp project. Attach the notes from our last project planning meeting and reserve a conference room."*
  - *"Customer ID 9182 reported they were charged three times for a single purchase attempt. Find all relevant log entries and determine if any other customers were affected."*
- Weak tasks (don't use): *"Schedule a meeting with jane@acme.corp next week."* — single tool call, no judgement.
- Each task paired with a **verifiable** response. Verifier can be string-compare or Claude-as-judge. Avoid overly strict verifiers.
- Run with simple agentic loops (one while-loop per task). Instruct evaluation agents to emit reasoning + feedback blocks *before* tool calls (triggers chain-of-thought). For Claude, turn on **interleaved thinking**.
- Collect: accuracy, runtime, tool-call counts, token consumption, error rates. Tool-call patterns reveal consolidation opportunities.

**Iterate with Claude Code.**
- Paste evaluation transcripts into Claude Code; it analyses, identifies issues, refactors tools.
- Held-out test sets prevent overfitting to "training" evaluations.
- Per the post: *"most of the advice in this post came from repeatedly optimizing our internal tool implementations with Claude Code."*
- **Concrete metrics:** Slack tools 67.4% → 80.1%; Asana tools 79.6% → 85.7% on held-out tests. The Claude-optimised version *beat researcher-written versions*.

### 3. Five principles for high-quality tools

**Principle 1 — Choose the right tools for agents.**
- "More tools don't always lead to better outcomes." Common error: wrapping every API endpoint as a tool.
- Agents have *limited context*; computer memory is cheap. A `list_contacts` tool that returns all contacts wastes context. Implement `search_contacts` or `message_contact` instead.
- Consolidate: instead of `list_users` + `list_events` + `create_event`, expose `schedule_event`. Instead of `read_logs`, expose `search_logs`. Instead of `get_customer_by_id` + `list_transactions` + `list_notes`, expose `get_customer_context`.
- Tools should *enable subdivisions of tasks the way a human would subdivide them*, while reducing context consumed by intermediate outputs.

**Principle 2 — Namespacing.**
- Dozens of MCP servers, hundreds of tools. Naming is routing.
- Group with prefixes: `asana_search`, `jira_search`, or by resource: `asana_projects_search`, `asana_users_search`.
- **Empirical:** "Prefix- vs suffix-based namespacing has non-trivial effects on tool-use evaluations." Effects vary by LLM. Test for your setting.
- Good naming offloads agent reasoning from context to the tool selection itself.

**Principle 3 — Return meaningful context.**
- Prefer `name`, `image_url`, `file_type` over `uuid`, `256px_image_url`, `mime_type`.
- **Resolve UUIDs to semantically meaningful identifiers** — even 0-indexed scheme — improves Claude's retrieval precision and reduces hallucinations.
- For tasks that need both views, expose a `response_format` enum: `DETAILED` vs `CONCISE` (the post's example: 206 tokens vs 72 tokens for a Slack thread search — ~⅓ the tokens).
- **Response *structure* matters:** XML vs JSON vs Markdown affects evaluation performance. LLMs are trained on next-token prediction; formats that match training data perform better. No universal answer; measure.

**Principle 4 — Token efficiency.**
- Pagination, range selection, filtering, truncation with sensible defaults.
- Claude Code restricts tool responses to **25,000 tokens by default**.
- "We expect the effective context length of agents to grow over time, but the need for context-efficient tools to remain."
- **Helpful truncation includes steering instructions:** "Results truncated. Showing first 3 of 2,847. To refine: use `transactions_search(payee: 'Acme Corp')`, or filter by amount range, or `transactions_search(query: <query>, page: 2)`."
- **Error responses should be prompt-engineered.** Don't return `{"error": {"code": "RESOURCE_NOT_FOUND", "status": 422, "message": "Invalid value"}}`. Return: *"Resource Not Found: Invalid `userId`. The request to `/api/user/info` failed because the `userId` `john.doe@acme.corp` does not exist or is in the wrong format. Valid User IDs are 12-digit numbers (e.g., `1928298149291729`). To resolve: call `user_search()`."*

**Principle 5 — Prompt-engineer tool descriptions.**
- "Think of how you would describe your tool to a new hire on your team."
- Make implicit context explicit: query formats, niche terminology, resource relationships.
- Strict data models on inputs. Parameter named `user_id` not `user`.
- **Concrete impact:** Claude Sonnet 3.5 achieved SOTA on SWE-bench Verified after refinements to tool descriptions, dramatically reducing error rates.

### 4. Read between the lines on agent feedback

A subtle but important point: when Claude debugs your tools, *"what agents omit can be more important than what they include. LLMs don't always say what they mean."* Read raw transcripts, not just CoT.

Concrete example: at web-search-tool launch, Claude was appending `2025` to the `query` parameter unprompted, biasing results. Fixed via description, not via model change.

### 5. The forward-looking framing

*"To build effective tools for agents, we need to re-orient our software development practices from predictable, deterministic patterns to non-deterministic ones."*

The tools community needs the same shift that software engineering already went through with eventual consistency, retries, distributed systems: *design for probabilistic counterparties*.

## Method / evidence

- **Engineering blog post**, not peer-reviewed research. But unusually rich in numbers for an Anthropic engineering post: two held-out-test bar charts (Slack 67.4 → 80.1; Asana 79.6 → 85.7).
- The methodology is described concretely enough to *replicate* internally: prototype → evals → iterate with Claude Code → held-out test set.
- Authority rests on the team that ships Anthropic's internal tool stack; the advice is descriptive of practice, not speculative.

## Relevance to this thesis

### 1. Canonical reference for the [[tools-component]]

[[anthropic2024mcp]] is the protocol-level reference. **Aizawa 2025 is the *design-level* reference** — what makes a tool good once you've decided to build it. The thesis's [[tools-component]] concept page should cite Aizawa as the primary practical source.

### 2. Empirical anchor for "tool design has compounding effects"

Slack tools 67.4 → 80.1 (+12.7 pp); Asana tools 79.6 → 85.7 (+6.1 pp). Same model, same protocol, same task — only the tools changed. **These are direct empirical evidence for the thesis's [[agent-infrastructure-vs-capability]] claim that infrastructure quality dominates model quality at the margin.** Cite explicitly.

### 3. The deterministic/non-deterministic contract framing

The thesis's [[deterministic-tools-hypothesis]] argues that *deterministic primitives* combined with *non-deterministic orchestration* is the right design point. Aizawa frames this as the *defining property of tools*: they sit on the boundary. The framing is more vivid than the thesis's current language and worth borrowing.

### 4. Evaluation methodology lifted directly

The thesis's own experimental work involves measuring agent performance under varying infrastructure. **Aizawa's workflow (real-world tasks, multi-tool-call requirement, agentic-loop evaluation, Claude-as-judge, held-out tests, metrics beyond accuracy) is a directly usable template.** The thesis can cite Aizawa as the methodology reference for its own evaluations.

### 5. The "Choose the right tools" principle is the central tension of the thesis

The thesis argues infrastructure matters. Aizawa makes the more specific claim: *less infrastructure, designed better, beats more infrastructure designed worse.* `search_contacts` beats `list_contacts`. `schedule_event` beats `list_users + list_events + create_event`. This is **a hypothesis about productivity-curve shape**: the marginal returns of adding tools turn negative when tools overlap or expose too-granular APIs.

### 6. UUIDs → semantic identifiers as a hallucination intervention

A surprising specific claim: *resolving UUIDs to semantically meaningful identifiers reduces hallucination*. Pairs directly with [[kalai2024hallucinate]] and [[kadavath2022know]]: the model's calibration is operating on the *surface form* of identifiers, not on abstract pointers. Tool design can route around the calibration problem by making identifiers themselves more interpretable. Worth surfacing on [[calibration-thread]].

### 7. Response format as a tunable parameter

The `DETAILED`/`CONCISE` enum is operationally important: it lets the agent itself trade depth for token cost. **This is progressive disclosure pushed into the tool's response signature**, complementing the just-in-time retrieval pattern of [[rajasekaran2025]] and the description/body/resources pattern of [[zhang2025]].

## Notable concepts introduced

- **Tool as cross-boundary contract** — between deterministic systems and non-deterministic agents.
- **Tools are not API wrappers** — they should be designed for agent affordances.
- **Eval-driven tool design loop** — prototype, evaluate, iterate with Claude Code.
- **Held-out test sets for tools** — borrowing ML methodology for tool design.
- **Namespacing as routing** — prefixes/suffixes, service/resource taxonomy.
- **DETAILED/CONCISE response_format enum** — agent-controlled verbosity.
- **Helpful truncation** — truncation responses that include steering hints.
- **Prompt-engineered error responses** — errors that teach the agent how to fix the call.
- **Semantic identifiers beat UUIDs** — for retrieval precision.

## Concept-page reconciliation

1. **`wiki/concepts/tools-component.md`** — Aizawa is *the* practical reference. The page should cite it as primary, lift the five principles, and include the Slack/Asana evaluation numbers as empirical support. Promote `status: draft → summarized`.
2. **`wiki/concepts/deterministic-tools-hypothesis.md`** — the cross-boundary contract framing is the most direct industry articulation of this concept. Cite explicitly and consider quoting.
3. **`wiki/concepts/framework-four-components.md`** — Aizawa names "increase the surface area over which agents can be effective in solving a wide range of tasks." This is the framework's productivity-curve claim in industry voice.
4. **`wiki/concepts/context-engineering.md`** — token efficiency, response-format enums, helpful truncation all belong here. Pair with [[rajasekaran2025]].
5. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — the empirical numbers (Slack +12.7pp, Asana +6.1pp) are direct evidence the thesis can cite.
6. **`wiki/concepts/calibration-thread.md`** — UUIDs→semantic identifiers as a hallucination-reduction intervention. Pair with [[kalai2024hallucinate]] and [[kadavath2022know]].

## Tensions and qualifications

- **Two data points are not a study.** Slack and Asana are real internal applications, but n=2 environments inside Anthropic. No external replication.
- **"Claude-optimised beat researcher-written" is striking but underspecified.** What does "researcher-written" mean here? How much effort went in? Was the researcher trying to optimise for the same eval? The post doesn't say.
- **The eval is self-judged.** Anthropic's evals on Anthropic's tools optimised by Anthropic's model. Risk of overfitting to internal taste even with held-out test sets.
- **Namespacing recommendations are model-specific.** "Prefix vs suffix has non-trivial effects, vary by LLM." So the prescriptions don't generalise cleanly.
- **The "design tools for agents" advice is hard to operationalise without examples.** The post leans on examples; absent enough examples, "design for agents" can degenerate into "trial and error."
- **The post assumes English-language and Anthropic-flavoured agents.** Whether the same conventions hold for other model families is open.
- **No comparison to alternatives.** GPT or Gemini tool-call patterns may benefit from different design principles. The post is honest about this but does not address it.
- **Tool-call cost is not equal to LLM-token cost.** A tool that returns 10K tokens is much more expensive than the description that names it. The post collapses these in places.

## Connections

- [[anthropic2024mcp]] — protocol layer; Aizawa is the design-quality layer on top.
- [[rajasekaran2025]] — context engineering; explicitly cites Aizawa for tool design.
- [[zhang2025]] — skills as packaged procedures; complementary abstraction layer above tools.
- [[martin2026managed]] — managed-agent harness; tools run inside that harness.
- [[krishnan2025multiagent]] — multi-agent MCP; Aizawa is the tool-quality story Krishnan glosses over.
- [[kalai2024hallucinate]] — Kalai's calibration lower bound; Aizawa's "semantic identifiers reduce hallucination" is a behavioural intervention.
- [[kadavath2022know]] — P(IK); semantic identifiers may shift the model's internal confidence signal.
- [[peng2023copilot]] — measured productivity gains from tooling for *human* developers; Aizawa is the analogue for agents.
- [[fielding2000]] — REST as the protocol-design ancestor. Aizawa's authoring principles (namespacing, response-format enums, self-descriptive error responses, semantic identifiers) are operational instantiations of REST's *uniform interface* + *self-descriptive messages* constraints.
- [[lin2022truthfulqa]] — Aizawa's UUIDs → semantic-identifiers finding is a calibration intervention at the tool layer; pair with TruthfulQA's evidence that retrieval/prompt infrastructure outperforms scale for factuality.
- Concept pages: [[tools-component]], [[deterministic-tools-hypothesis]], [[framework-four-components]], [[context-engineering]], [[agent-infrastructure-vs-capability]], [[calibration-thread]].

---
*Ingested 2026-05-15. Read in full (19-page blog PDF export; substantive content pages 1-15).*
