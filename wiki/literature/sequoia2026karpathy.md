---
type: literature
citekey: sequoia2026karpathy
title: AI Ascent — Andrej Karpathy on vibe coding, agentic engineering, and Software 3.0
authors: [Karpathy, Andrej, Sequoia Capital (interviewer)]
year: 2026
venue: Sequoia Capital AI Ascent interview (transcript)
raw_path: raw/literature/Sequoia_Capital(2026).md
related_concepts: [agent-infrastructure-vs-capability, framework-four-components, deterministic-tools-hypothesis, prototypicality-bias, calibration-thread, data-component]
related_work: [interview-karpathy-analysis-1, interview-karpathy-analysis-2]
status: summarized
ingested: 2026-05-15
updated: 2026-05-15
---

# Sequoia (2026) — AI Ascent: Andrej Karpathy on vibe coding, agentic engineering, and Software 3.0

## Summary

A ~30 minute Sequoia Capital interview with Andrej Karpathy in 2026, transcribed and stored as a markdown source. Karpathy uses the platform to introduce, sharpen, or restate several concepts that have circulated in his recent writing: **Software 3.0** (programming via context), **vibe coding** (floor-raising) vs **agentic engineering** (ceiling-raising), **verifiability and jagged intelligence**, **ghosts vs animals** (LLMs as summoned statistical entities, not evolved organisms), and **LLM Wikis as understanding amplifiers**. The interview's two most thesis-relevant moves are: (1) framing **agentic engineering as a distinct discipline** focused on coordinating fallible, stochastic, but powerful agents at production-quality bars, and (2) the recurring motif that **agents are sensors-and-actuators over the world** and **today's infrastructure is human-first, not agent-native** — Karpathy's "favourite pet peeve" being documentation written for humans rather than copy-pasteable for agents. The interview closes on the **"you can outsource your thinking but you can't outsource your understanding"** maxim, which Karpathy positions as the human residual after most of programming is automated.

## Main claims

### 1. December 2025 as the agentic-coherence inflection point

The opening: Karpathy says he's "never felt more behind" as a programmer. Why? *"December was this uh clear point where for me … with the latest models uh the chunks just came out fine and then I kept asking for more and it just came out fine. And then I can't remember the last time I corrected it."* He explicitly frames this as a regime change distinct from "ChatGPT-adjacent" use — *"things have changed fundamentally and especially on this like agentic coherent workflow that really started to actually work."*

This is significant for the thesis's framing of *when* agentic productivity became a real phenomenon, not just an aspiration. December 2025 (post-Claude Sonnet 4.5, post-Opus 4.6 era) is the named inflection.

### 2. Software 3.0 — programming via context

The taxonomy Karpathy now uses:
- **Software 1.0** — explicit code (write rules).
- **Software 2.0** — learned weights (programming = arranging datasets + architectures + objectives).
- **Software 3.0** — programming via *context*: *"your programming now turns to prompting and what's in the context window is your lever over the interpreter that is the LLM."*

**The LLM is the interpreter; the context window is the program.** This is the deepest single-sentence framing of context engineering in industry voice. Pair with [[rajasekaran2025]].

### 3. Two illustrative examples — OpenClaw and MenuGen

**OpenClaw installation:** Traditionally a bash script. The Software 3.0 version is a copy-pasteable piece of text the user gives to their agent. The agent reads the environment, debugs in the loop, and installs. *"You don't have to precisely spell out all the individual details of that setup. The agent has its own intelligence."*

**MenuGen:** Karpathy vibe-coded a Vercel app that OCRs a menu, generates images of dishes. Then he saw the Software 3.0 version: *"literally just take your photo, give it to Gemini and say 'use Nano Banana to overlay the things onto the menu.'"* Realisation: *"all of my MenuGen is spurious. It's working in the old paradigm. That app shouldn't exist."*

**Operational lesson:** Don't reflexively reach for "build an app." Ask whether the model can just do it. The right question is *what is the piece of text to copy-paste to your agent?*

### 4. Vibe coding vs agentic engineering

- **Vibe coding** raises the *floor*: anyone can build software. The Karpathy term from 2024-2025.
- **Agentic engineering** raises the *ceiling*: professional software work with agents, while preserving quality (security, correctness, no vulnerabilities). *"How do you coordinate them to go faster without sacrificing your quality bar?"*

Quote: *"people used to talk about the 10x engineer previously. I think that this is magnified a lot more. 10x is not the speed up you gain."*

This is a direct claim that **infrastructure (tools, agents, agentic workflows) extends the productivity ceiling far beyond what individual capability allows**. The thesis's [[agent-infrastructure-vs-capability]] argument is here in industry-voice form.

### 5. Verifiability and jagged intelligence

- **Verifiable → automatable.** LLMs are trained via RL with verifiable rewards. They peak on math, code, and adjacent domains because those have verification signals.
- **Jagged.** Modern models simultaneously refactor 100k-line codebases *and* tell you to walk to a car wash 50 metres away because it's close. *"This is insane."*
- **Why jagged?** Combination of (a) what's verifiable + (b) what labs choose to put in the RL mix. Karpathy's chess-improvement anecdote (GPT-3.5 → GPT-4): a single lab decision to add chess data lifted a single capability dramatically. Capabilities are *not* uniform progress — they are *spotlight* progress.
- **Operational implication:** *"you have to actually explore this thing that they give you that has no manual. And it works in certain settings, but maybe not in some settings. … If you're in the circuits that were part of the RL, you fly. If you're in the circuits that are out of the data distribution, you're going to struggle."*

For founders: verifiability is a tractability test. *"Ultimately almost everything can be made verifiable to some extent"* — e.g. council-of-LLM-judges for writing. The question is what's cheap to verify.

### 6. Agent-native infrastructure as the missing layer

Karpathy's pet peeve: *"every time I'm told 'go to this URL' or something like that, it's just like 'ah.' … Why are people still telling me what to do? Like, I don't want to do anything. What is the thing I should copy-paste to my agent?"*

**Most current infrastructure is still human-first.** Docs for humans, settings GUIs, signup flows. Karpathy's MenuGen anecdote: writing the code was easy; deploying on Vercel was hard *because the configuration was UI-first, not agent-first*.

**The future:** *sensors and actuators over the world*, agent-native data structures, agent-readable docs (llms.txt etc.), one prompt that builds-and-deploys.

This is the thesis's [[framework-four-components]] argument applied to *the broader software ecosystem*: infrastructure has to change to admit agents, not just the inside of any single agent harness.

### 7. Ghosts vs animals

Earlier Karpathy writing distinguishes:
- **Animals**: evolved, embodied, intrinsically motivated (curiosity, fun, empowerment).
- **Ghosts**: LLMs are summoned, not evolved. Statistical simulation circuits with RL appendages. No intrinsic motivation; yelling at them does nothing.

Operational use: *"a way of coming to terms with what these things are"* so as to be more competent at using them. Karpathy hedges: *"I'm not sure if it actually has real power. It's a little bit of philosophizing."* But the framing protects against anthropomorphism that misleads design.

### 8. Taste, judgement, oversight, and design as the human residual

What the human is still in charge of, even at peak agentic engineering:
- **Aesthetics, judgement, taste.**
- **Spec / plan / design.** *"You have to work with your agent to design a spec that is very detailed and maybe it's basically the docs and then get the agents to write them."*
- **Oversight.** Catching agent errors (the MenuGen Stripe-vs-Google email-matching example).
- **Top-level architecture.** Knowing that there must be persistent unique user IDs; knowing that there's an underlying tensor view vs a copy.

What the human is *not* in charge of:
- **API surface details.** `keepdims` vs `keepdim`, `dim` vs `axis`, `reshape` vs `permute`. *"This is the kind of details that are handled by the intern because they have very good recall."*

### 9. Hiring has not caught up

*"What I'm seeing is that the most people have still not refactored their hiring process for agentic engineer capability. If you're giving out puzzles to solve and this is still the old paradigm. I would say that hiring has to look like 'give me a really big project and see someone implement that big project.'"* Example: build a Twitter clone for agents, secure it, and try to break it with 10 parallel Codex agents.

The skill being assessed is *coordinating multiple agents to deliver large secure systems*. Not algorithmic-puzzle-solving.

### 10. LLM Wiki as understanding amplifier

Karpathy returns to the LLM Wiki idea (see [[karpathy2025wiki]]):
- *"I really enjoy whenever I read an article I have my wiki that's being built up from these articles and I love asking questions about things."*
- *"Anytime I see a different projection onto information, I always feel like I gain insight."*
- The closing maxim: ***"you can outsource your thinking but you can't outsource your understanding."***

The Wiki is positioned as a *tool for understanding*, not just for retrieval. The human-bottleneck argument is: *I still have to direct, decide what's worth building, know why. That's bounded by my understanding.*

## Method / evidence

- **Conversational interview**, transcribed. No empirical claims with numbers; reasoning by anecdote and pattern.
- Authority rests on Karpathy's track record (OpenAI co-founder, Tesla Autopilot, deep teaching influence on the ML community).
- The interview is most useful as a *vocabulary and framing* source — Software 3.0, vibe coding vs agentic engineering, verifiability, jaggedness, ghosts vs animals — terms that have spread widely in agent engineering practice.

## Relevance to this thesis

### 1. Industry-voice articulation of the thesis's central claim

The thesis argues productivity is infrastructure-bound. Karpathy says it directly: *"How do you coordinate them to go faster without sacrificing your quality bar? … 10x is not the speed up you gain."* Agentic engineering is *the discipline of productivity-with-agents*. Cite this as a high-profile industry articulation.

### 2. Software 3.0 as the framing for context engineering

The thesis's [[context-engineering]] page should adopt Karpathy's "context window as program / LLM as interpreter" sentence. Pair with [[rajasekaran2025]] for the operational version.

### 3. Vibe-coding-vs-agentic-engineering as a discipline boundary

Useful for situating the thesis's experiments. The thesis is about *agentic engineering* (preserving quality bars), not *vibe coding* (raising the floor). Naming the distinction sharpens the thesis's contribution.

### 4. Verifiability + jaggedness ties calibration to capability

The jaggedness phenomenon is the surface form of [[kalai2024hallucinate]]: models calibrated on what they've seen, hallucinatory elsewhere. Karpathy's framing — *"in the circuits / out of the circuits"* — gives the calibration story a vivid operational vocabulary. Pair on [[calibration-thread]] and [[prototypicality-bias]].

### 5. Agent-native infrastructure as the gap

Karpathy's pet peeve about human-first docs is a direct articulation of the thesis's [[agent-infrastructure-vs-capability]] thesis at *ecosystem* scale: the bottleneck isn't model capability, it's the gap between agent affordances and ecosystem-wide infrastructure. **Most of the world isn't yet agent-native.** This is the productivity-headroom argument.

### 6. Spec-and-design as the durable human role

The thesis's discussion of where human work goes after automation can lift Karpathy's specific list: aesthetics, taste, spec, oversight, top-level architecture, design. *Detail-recall* is automated; *direction* is not.

### 7. Hiring has not caught up = market lag indicator

If hiring practices have not adapted, the market has not yet priced in agentic-engineering productivity. The thesis can cite this as evidence that *the productivity-from-infrastructure phenomenon is far from saturated* — early in the curve.

### 8. The LLM Wiki claim is restated and elevated

Karpathy explicitly connects the Wiki pattern to *understanding* rather than just retrieval. *"Tools to enhance understanding."* This pairs with [[karpathy2025wiki]] for a richer concept-page treatment.

### 9. "Outsource thinking, not understanding" — quotable maxim

A clean line for the thesis to use when discussing the residual human role. The thesis's conclusion section can pick this up.

## Notable concepts introduced

- **Software 3.0** — programming-via-context paradigm.
- **The context window is the program; the LLM is the interpreter.**
- **Vibe coding** — floor-raising; **Agentic engineering** — ceiling-raising. Different disciplines.
- **Jagged intelligence** — peaks-and-valleys capability map shaped by verifiability + lab focus.
- **Ghosts vs animals** — LLMs as statistical simulation circuits, not evolved organisms.
- **Agent-native infrastructure** — sensors-and-actuators over the world.
- **In-the-circuit vs out-of-the-circuit** — operational vocabulary for capability prediction.
- **"You can outsource your thinking but you can't outsource your understanding."**

## Concept-page reconciliation

1. **`wiki/concepts/agent-infrastructure-vs-capability.md`** — Karpathy's "agent-native vs human-native infrastructure" is the ecosystem-scale form of the thesis's argument. Add a paragraph quoting his pet peeve.
2. **`wiki/concepts/framework-four-components.md`** — Karpathy's sensors-and-actuators framing maps onto data (sensors) + tools (actuators) of the four-component framework. Useful synthesis.
3. **`wiki/concepts/context-engineering.md`** — Software 3.0 as the namesake; the context window as program. Pair with [[rajasekaran2025]] and [[zhang2025]].
4. **`wiki/concepts/calibration-thread.md`** — jaggedness as the surface form of [[kalai2024hallucinate]]-style calibration. Add Karpathy's car-wash example.
5. **`wiki/concepts/prototypicality-bias.md`** — "in-the-circuit / out-of-the-circuit" framing belongs here.
6. **`wiki/concepts/deterministic-tools-hypothesis.md`** — Karpathy: *"neural nets … are using tool use as this like historical appendage for some kinds of deterministic tasks."* Direct articulation.
7. **`wiki/concepts/data-component.md`** — Wiki-as-understanding reinforces [[karpathy2025wiki]]; add the "different projection on information" line.

## Tensions and qualifications

- **Anecdotal throughout.** No numbers, no controlled comparisons. The interview's value is conceptual, not empirical.
- **Karpathy hedges on ghosts/animals.** *"I'm not sure if it actually has real power. It's a little bit of philosophizing."* The thesis should reference the framing but not over-claim.
- **Software 3.0 is contested vocabulary.** Other practitioners use different terms. Adopt with attribution.
- **The "December 2025 inflection" claim is personal.** Whether this is a real industry-wide inflection or a Karpathy-experience inflection is open. The thesis should pair with empirical evidence (Peng 2023, etc.) rather than rest on the date.
- **Karpathy's prescriptions are oriented toward founders.** The thesis is academic. Some of the framing (founder advice, hiring practices) translates only partially.
- **The "ghosts" framing risks underestimating model coherence.** Calling LLMs "statistical simulation circuits" is accurate at one level and reductive at another. [[sofroniew2026emotions]] shows there's more structure than the framing suggests.
- **Verifiability-as-tractability is contested.** The "you can always make it verifiable with a council of judges" claim is glib in practice — judge councils have their own failure modes (sycophancy, bias).
- **Hiring claim is not measured.** The "people still give puzzles" claim is anecdotal; the actual state of agentic-engineering hiring practice is harder to nail down.

## Connections

- [[karpathy2025wiki]] — the LLM Wiki gist; this interview restates and elevates the framing.
- [[rajasekaran2025]] — context engineering as a discipline; Software 3.0 is the slogan version.
- [[zhang2025]] — agent skills as packaged procedural context.
- [[aizawa2025tools]] — agent-native tool design; mirrors Karpathy's pet peeve about human-first interfaces.
- [[anthropic2024mcp]] — MCP is one of the layers making infrastructure agent-native.
- [[martin2026managed]] — managed-agent harness as the unit Karpathy is implicitly describing.
- [[peng2023copilot]] — measured productivity for early-generation tools; Karpathy is describing the post-2024 acceleration.
- [[kalai2024hallucinate]] — jaggedness is the surface form of the calibration lower bound.
- [[sofroniew2026emotions]] — counterpoint to the "ghosts" framing: there is internal structure to LLMs that maps onto human-cognitive-science categories.
- [[simon1996artificial]] — Simon's bounded rationality precedent for the "understanding is the bottleneck" maxim.
- [[wallas1926art]] — Wallas's stages map onto the "human directs, agent fills" division of labour.
- [[lin2022truthfulqa]] — TruthfulQA's *jaggedness* (the car-wash example's mirror is GPT-3 telling you to drive somewhere walkable while it refactors codebases) is the surface form of Karpathy's in-the-circuit/out-of-the-circuit framing.
- [[fielding2000]] — the *agent-native infrastructure* gap Karpathy describes at ecosystem scale is REST-shaped: every URL is a resource, every action should be self-describing, every layer should be intermediary-aware. The thesis can argue that Karpathy's "what is the piece of text to copy-paste to your agent?" is REST's HATEOAS constraint reborn for agents.
- [[matarazzo2025survey]] — Matarazzo's substrate survey covers what the Sequoia interview describes at the meta-level; Karpathy's "ghosts" framing is the cognitive-science gloss on Matarazzo's System 1 / System 2 framing (via Kambhampati).
- User-authored analyses: [[interview-karpathy-analysis-1]] and [[interview-karpathy-analysis-2]] read this transcript through the thesis's framework. The literature page is the source; the work-folder analyses are how the thesis incorporates it.
- Concept pages: [[agent-infrastructure-vs-capability]], [[framework-four-components]], [[context-engineering]], [[calibration-thread]], [[prototypicality-bias]], [[deterministic-tools-hypothesis]], [[data-component]].

---
*Ingested 2026-05-15. Read in full (markdown transcript, 121 lines).*
