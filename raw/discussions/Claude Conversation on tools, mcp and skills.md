---
title: "Claude Conversation"
source: "https://claude.ai/share/c0f50999-24ce-4766-b35a-b90f1ca7ffd0"
author:
published:
created: 2026-06-01
description: "Claude conversation with 20 messages"
tags:
  - "clippings"
---
**You**

Help me understand mcp. I know it's a way of giving an interface to AIs. And I know it's hosted on a server. Which makes sense for stuff like mail or calenders, it comes with an endpoint and a set of tools it can use. It makes sense when it's external, it reaches and endpoint and performs actions, like an API. What i don't understand is what about when it's local? When an mcp can access a browser or an application that is in the same computer and not hosted on the internet. Is it just opening a local host that the ai can use or something else?

---

**Claude**

Your guess is close but mixes up two things: "server" in MCP doesn't mean "web server," and there are two different transports.

The key distinction is **transport**, i.e. how the AI client and the MCP server talk to each other:

1. **stdio (standard input/output)** — this is the local case. The client *launches the MCP server as a child process* on your machine and communicates by piping JSON-RPC messages over stdin/stdout. No network, no localhost, no ports. It's just two processes talking through pipes, the same way a shell pipes `ls | grep`. When you see a config like `command: "npx", args: ["@modelcontextprotocol/server-filesystem", ...]`, that's stdio — the client spawns that program and speaks to it directly.
2. **HTTP/SSE** — the remote case you already understand. The server is a web service at an endpoint; the client makes HTTP requests.

So "is it opening a localhost the AI can use?" — sometimes (a local server *can* use HTTP over localhost), but the more common local pattern is stdio, which has no socket at all.

The thing to internalize: **"MCP server" just means "the process exposing tools," not "a thing on the internet."** It's a role in the protocol, not a deployment model. A filesystem server, a browser-control server, a Postgres server — these are all just local programs the client spawns, and each advertises its tools/resources over the same JSON-RPC protocol regardless of transport.

The browser case specifically: the MCP server is a local process that talks to the browser through something like the Chrome DevTools Protocol or a driver, and exposes that as tools (`navigate`, `click`, `screenshot`) to the AI. The AI never touches the browser directly — it calls the tool, the local server does the actual driving.

Want the JSON-RPC message flow, or is the transport distinction what you needed?

---

**You**

How is the tools exposed though? And how are they being called? Is it using structured outputs? How is that different from just normal tool calling, like pydantic ai offers

---

**Claude**

Tools are exposed via a `tools/list` request. The client sends that JSON-RPC call to the server, and the server returns a list of tool definitions, each with a `name`, a `description`, and an `inputSchema` that is plain **JSON Schema**. That's the entire contract — name, what it does, what arguments it takes.

Calling them is the part worth getting precise about, because **MCP does not change how the model calls tools.** The flow:

1. Client calls `tools/list`, gets the schemas.
2. Client takes those schemas and injects them into the model API call as the `tools` parameter — exactly the format the Anthropic/OpenAI API already expects.
3. Model emits a normal `tool_use` block: the tool name plus arguments. This *is* the structured-output mechanism — the model is doing constrained generation against the JSON Schema, same as any function call.
4. Client intercepts that, translates it into a `tools/call` JSON-RPC request to the MCP server.
5. Server runs the actual code, returns a result, client feeds it back to the model as a `tool_result`.

So the model side is *identical* to ordinary tool calling. There's no special "MCP mode" the LLM is in — it just sees tools and emits tool calls. MCP is a layer between the **client and the tool provider**, not between the model and the client.

That's the exact difference from Pydantic AI's native tools. With Pydantic AI:

- You define a tool as a Python function, in-process.
- Pydantic generates the JSON Schema from your type hints/signature.
- When the model calls it, the framework directly invokes that Python function. Same address space, same language, a function call.

With MCP:

- The tool lives in a separate process (possibly a different language, possibly a remote service).
- The schema comes over the wire from `tools/list`.
- The "invocation" is a JSON-RPC `tools/call` round-trip across a process/network boundary, not a direct function call.

Both produce the same thing at the model layer — schemas in, structured tool calls out. The difference is purely architectural on the *other* side of the model: in-process function vs. out-of-process standardized protocol.

So the tradeoff is basically: Pydantic tools are simpler and faster (no boundary, no serialization, no separate process to manage) but locked to your Python runtime. MCP buys you a language-agnostic, swappable, reusable boundary — the same browser server works with any MCP client — at the cost of the protocol overhead and an extra moving part. This maps onto the MCP-vs-Pydantic-tools decision you've thought about before: MCP earns its keep when the tool provider is something you want to share, reuse, or keep out-of-process; native tools win when it's bespoke logic that only your agent needs.

---

**You**

Can you give an example of a flow from discovering tools to using one to reading the results? Do it for both normal tool calling, mcp and scripts in skills. I want to see what the json looks like as well. Show me the flow and logic, i want to get a cøear and intuitive grasp of this

---

**Claude**

Same task for the first two so you can see they're twins at the model layer. Skills I'll do on their own turf and explain why forcing the same task would mislead.

Task: "What's the weather in Oslo?"

---

### 1\. Normal tool calling (Pydantic AI / raw API)

**Discovery** happens at *dev time*, not runtime. You write a function; the framework generates a schema from its signature and puts it in the request:

```json
{
  "messages": [{"role": "user", "content": "What's the weather in Oslo?"}],
  "tools": [
    {
      "name": "get_weather",
      "description": "Get current weather for a city",
      "input_schema": {
        "type": "object",
        "properties": { "city": { "type": "string" } },
        "required": ["city"]
      }
    }
  ]
}
```

**Model decides to call it** — returns a `tool_use` block (this is the structured output):

```json
{
  "role": "assistant",
  "stop_reason": "tool_use",
  "content": [
    { "type": "tool_use", "id": "toolu_01ABC", "name": "get_weather", "input": { "city": "Oslo" } }
  ]
}
```

**Framework runs the actual Python function directly** — `get_weather(city="Oslo")` — no boundary crossed. Result wrapped and sent back:

```json
{
  "role": "user",
  "content": [
    { "type": "tool_result", "tool_use_id": "toolu_01ABC", "content": "12°C, cloudy" }
  ]
}
```

Model then produces final text. Done.

---

### 2\. MCP

The model-facing JSON (steps 2 and 3 above) is **byte-for-byte the same**. Two extra things wrap it: a real discovery step, and the call goes over JSON-RPC to a separate process.

**Discovery** — client asks the server at runtime:

```json
{ "jsonrpc": "2.0", "id": 1, "method": "tools/list" }
```

Server replies:

```json
{
  "jsonrpc": "2.0", "id": 1,
  "result": {
    "tools": [
      {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "inputSchema": {
          "type": "object",
          "properties": { "city": { "type": "string" } },
          "required": ["city"]
        }
      }
    ]
  }
}
```

The client now **translates** this into the API's `tools` format and sends it to the model. (Small tell: MCP says `inputSchema` camelCase, the Anthropic API wants `input_schema` snake\_case — the client does that conversion. Proof they're separate layers stitched together.)

**Model returns the identical `tool_use` block** as in case 1.

**Client translates that into a JSON-RPC call** to the server:

```json
{
  "jsonrpc": "2.0", "id": 2,
  "method": "tools/call",
  "params": { "name": "get_weather", "arguments": { "city": "Oslo" } }
}
```

Server runs the code, replies:

```json
{
  "jsonrpc": "2.0", "id": 2,
  "result": {
    "content": [{ "type": "text", "text": "12°C, cloudy" }],
    "isError": false
  }
}
```

**Client unwraps that and feeds it to the model** as the same `tool_result` block from case 1.

So MCP = case 1 with two seams added: `tools/list` instead of dev-time registration, and a `tools/call` JSON-RPC round-trip instead of a direct function call. The model never knows the difference.

---

### 3\. Skills

A skill isn't a calling protocol at all — that's the part to internalize. It's a **folder**: a `SKILL.md` (instructions + context) plus optional bundled scripts/resources. There's no `skills/list`, no `skills/call`. The model interacts with a skill using an ordinary tool it already has — usually a **bash / code-execution tool**. The skill is just packaged knowledge that tells the model *what to run*.

That's why forcing "weather" here would be artificial; skills shine for tasks like "convert this CSV to a formatted Excel file." So:

**Discovery** — only the skill's name + description sit in context (cheap). The model sees:

> `xlsx` — create/edit Excel files with formatting, formulas, charts...

**Model decides it's relevant and reads the instructions** using its file/view tool:

```json
{ "type": "tool_use", "id": "toolu_03AAA", "name": "view",
  "input": { "path": "/mnt/skills/public/xlsx/SKILL.md" } }
```

The returned file content says, in effect, "to build a spreadsheet, write the data and call `scripts/build.py`." This is **progressive disclosure** — the heavy instructions only enter context once the model commits to the skill.

**Model now uses its bash tool** to run the bundled script:

```json
{ "type": "tool_use", "id": "toolu_04BBB", "name": "bash",
  "input": { "command": "python /mnt/skills/public/xlsx/scripts/build.py data.csv out.xlsx" } }
```

**Result is just stdout**, returned as a normal `tool_result`:

```json
{ "type": "tool_result", "tool_use_id": "toolu_04BBB",
  "content": "Wrote out.xlsx (3 sheets, 1,204 rows)" }
```

---

### The mental model

Line up where "discovery" and "execution" actually live:

|  | Discovery | Execution mechanism | Boundary |
| --- | --- | --- | --- |
| Native tools | dev-time, from code | direct function call | none (in-process) |
| MCP | runtime `tools/list` | JSON-RPC `tools/call` | process / network |
| Skills | name+desc in context, then read `SKILL.md` | runs via an existing tool (bash) | filesystem + subprocess |

The unifying idea: **the model only ever does one thing — emit a `tool_use` with structured arguments and read back a `tool_result`.** Everything else (a Python function, a JSON-RPC server, a script in a folder) is just *what's on the other end of that one mechanism*. MCP and skills aren't new ways for the model to call things; they're different ways to *supply and package* the things it calls.

One sharp contrast to lock it in: MCP front-loads tool definitions into the model's context (every tool's schema is always present, costing tokens). Skills front-load almost nothing — just a one-line description — and only pull in detail when used. That token-economics difference is often the real deciding factor when you're choosing between exposing something as an MCP server vs. a skill.

---

**You**

I mean you could use skill for the same example right? You write a python script that uses the weather api, it just calls it through bash instead.

---

**Claude**

Right, you can. The xlsx example was just natural turf, not a constraint. A weather skill works fine:

```
weather-skill/
  SKILL.md          "to get weather, run scripts/get_weather.py <city>"
  scripts/
    get_weather.py  # hits the weather API, prints result
```

Model reads `SKILL.md`, then:

```json
{ "type": "tool_use", "id": "toolu_05CCC", "name": "bash",
  "input": { "command": "python weather-skill/scripts/get_weather.py Oslo" } }
```

stdout (`"12°C, cloudy"`) comes back as the `tool_result`. Same end result as the MCP and native versions.

So all three can wrap the identical weather API. What differs is the seam:

- **Native tool** — model emits `get_weather(city="Oslo")` directly; framework runs the function in-process.
- **MCP** — model emits `get_weather(city="Oslo")`; client relays it as JSON-RPC to a running server.
- **Skill** — model emits a *bash command* (`python get_weather.py Oslo`); the API call is buried inside the script, invisible to the model.

That last line is the real distinction. With native/MCP, the weather call is a **first-class tool the model named and parameterized** — the model "knows" it's calling a weather tool. With a skill, the model's actual tool call is just "run this script"; the fact that the script talks to a weather API is an implementation detail it never sees as structured arguments. The model isn't choosing `get_weather`, it's choosing "execute code that happens to do weather."

Which is exactly why each fits different jobs:

- **MCP/native** when you want the *parameters* exposed to the model's reasoning — it picks the city, the model can chain it, validate it, retry with a different arg.
- **Skill** when the logic is a multi-step procedure you'd rather the model *follow* than *parameterize* — "given a CSV, here's the 6-step pipeline to produce a report." Cramming that into one tool call's arguments would be awkward; a script is the right container.

A single weather lookup is genuinely a better fit for a tool than a skill — you'd only reach for the skill if "get weather" were really "get weather, then cross-reference three sources, reformat, and cache it," i.e. a procedure rather than a call. But mechanically, yes, you're correct: it's the same API either way, just reached through a different seam.

---

**You**

But the skill way seems simpler for all. It seems easier to hand a python script with a written explanation in skill.md to a generic harness with a bash tool you make once, rather than having to program a new tool Everytime you need to give it new functionality

---

**Claude**

You've spotted something real, and it's a big part of why skills exist as a pattern: if your agent already has a trusted code-execution sandbox, then "drop a script + SKILL.md in a folder" genuinely is the lowest-friction way to add capability. Write the bash harness once, extend forever, no per-capability boilerplate. That's a legitimate architectural win, not a hack.

But one correction to the framing first: "program a new tool every time" is the pain of **native/in-process** tools, not MCP. MCP already solves that same friction a different way — you write a server once, point the client at it, and the harness never changes. Any MCP client picks it up. So skills and MCP are *two different answers to the identical problem* ("don't make me modify the client to add capability"). The choice between them isn't about write-once convenience — they both have that. It's about three things skills-via-bash quietly assume:

**1\. You're handing the model a shell.** A bash tool is arbitrary code execution — the model can do *anything* on that machine, not just the thing you intended. A native/MCP tool is a keyhole: the model can call `get_weather`, full stop, it cannot `rm -rf` or exfiltrate a file. In a personal sandbox that's fine. In anything multi-tenant, enterprise, or user-facing, deliberately *not* granting a shell is the whole point. Skills trade a narrow capability surface for a universal one, and that trade is sometimes exactly backwards.

**2\. You need an execution environment at all.** Skills-via-bash presupposes a container where running scripts is acceptable. A consumer app, a phone client, a website backend often has no such thing. An MCP server can run somewhere else and expose a thin HTTP surface to a client that can't run code. You can't always "just add a bash tool."

**3\. State and connections.** A script is a cold start every call — re-auth, reconnect, nothing shared. MCP servers persist: hold a DB connection, an auth session, a live browser across ten steps. The browser case from earlier is the clean example — you want the browser to *stay open* between `click` and `screenshot`, which a fresh subprocess per call can't give you.

So your intuition is correct in its native habitat: **a coding/agentic setup with a sandbox** — which is precisely where skills were designed to live. Outside that — no shell to give, or you can't afford to give one, or you need persistent state — the script-in-a-folder model stops being simpler and starts being impossible, and MCP's "separate process behind a narrow protocol" is doing real work you were getting for free from the sandbox.

Rough rule: trusted sandbox + procedural logic → skills win on simplicity. Untrusted surface, no execution env, or stateful connections → MCP. Tight parameter reasoning the model should chain → native tool.

---

**You**

Imagine you want to make a chess app where humans can play llms. Woudk you rather have a board server with mcp endpoints of the LLM to use, or a harness with a run\_script(name, \[ARGS\]) where it can use scripts defined in a skill.md? Mcp might sound like the best approach first, but with skills you can get chess theory, and procedural instructions (there could be more tools or scripts than just make moves, it could be visualizing the board, identifying mate patterns, reading opening etc.). And if the harness just comes with a run\_script tool, it's not really a full sandbox, it just seems if the named python script exist or not and if the schema is correct. But llms are not fine tuned for this format, they are fine tuned for the tool json schema you described earlier. What are your thoughts?

---

**Claude**

My honest answer: it's not a pick, it's a split — and the split falls exactly along the line we drew two turns ago, stateful-authoritative vs. reference-knowledge. The mistake in the framing is treating "the board" and "chess knowledge" as one decision. They're two completely different beasts.

**The board is ground truth and must be server-authoritative.** Legality, current position, whose turn, is-this-mate — none of that can ever come from the model's head. The model *will* hallucinate a board state if you let it be the source of truth. So that layer wants a stateful engine (literally just wrap `python-chess`) exposed as **typed first-class tools**: `make_move(uci)`, `legal_moves()`, `board_state()`, `result()`. Each one validated — an illegal move gets rejected by the engine, not adjudicated by the LLM. This is MCP-or-native territory, and it's the part you must not compromise on.

**Chess theory, openings, mate patterns, "how to think about this position" — that's reference knowledge, not state.** It's the textbook the model consults, progressively disclosed. That's a skill, cleanly. It doesn't even all need to be tool calls; a lot of it is just markdown the model reads when relevant. Perfect fit, and you're right that this is where the skill model genuinely shines and MCP would be awkward (you don't want "the Najdorf" as an RPC endpoint).

So: **typed tools for the rules engine + a skill for the knowledge.** Use both, on opposite sides of the state/knowledge line.

Now your two sharp points, because both land and both deserve a real response:

**Your point 3 (run\_script isn't a real sandbox, just a dispatcher) — correct, and it kills my safety objection from last turn.** A `run_script(name, args)` with a fixed allowlist isn't a shell; it's a tool router. Fine. But notice what you've built: a dispatcher *is* a single tool with a JSON schema (`name: string, args: array`). You haven't escaped tool-calling — you've collapsed N capabilities into 1 tool.

**Your point 4 is the real insight, and it actually argues against your own run\_script design, not for it.** Yes, the model is fine-tuned for the typed-tool format. But `run_script` is still technically that format — it's one tool. The problem isn't that the model can't emit it. The problem is *where the discriminating information lives*. With N typed tools, "which capability, with what arguments" is encoded in N schemas + N descriptions, all in context, all exploiting exactly what the fine-tuning is good at — picking the right tool and filling typed slots. With `run_script(name, args)`, that same information gets demoted to: a stringly-typed `name` the model has to remember, and an untyped `args` array whose meaning lives in SKILL.md *prose*. You've taken the part the model is best at and pushed it out of the schema into free text. So your own observation — LLMs are tuned for typed schemas — is precisely why `run_script` is the weakest surface for the move-making layer. You're handing the model a worse interface for the thing that matters most.

And the state problem compounds it: where does the board live between two `run_script` calls? You'd be passing FEN in and out every invocation and trusting the model to carry it faithfully — i.e. reintroducing the hallucination risk you were trying to engineer out. The moment you fix that (a persistent board the scripts share), you've built a stateful service through a script dispatcher — which is the thing MCP/native tools just *hand* you.

One place I'll push back on the implied premise, though: for a chess app you control end to end, **MCP itself might be overkill** for the engine. MCP's protocol overhead pays off when you want the board server separable or reusable across clients. If it's one app, plain in-process typed tools (Pydantic AI style) for the engine + a knowledge skill is leaner and gets you the same correctness guarantees. So your instinct that "MCP sounds best first but maybe isn't" is right — just not for the reason that skills replace it. It's that native typed tools may beat *both* for the rules layer, while skills own the knowledge layer regardless.

Net: typed tools (native or MCP) for anything that touches the authoritative board; skill for the theory/openings/tactics. The single `run_script` dispatcher is the one option I'd actively avoid — for the engine specifically — and your point 4 is the reason why.

---

**You**

But think about this though. Let say the scenario is a bit different. With native tools at the board layer, you cannot ship chess capabilities as a single package. Of a skill.md says "use visualize\_position() to see threats" it assumes that the chess board application has such a tool. What if we want to ship the tool with the skill? I think the concerns here should be separated. Board server is purely interaction with the game, skill is how we tell the LLM to play. So in the skill is where we should define the helper functions to make it play better. And identifying positions or openings is better done with deterministic scripts than by llms just reading about them in an MD file

---

**Claude**

You're right, and you've actually fixed the flaw in what I said. Two turns ago I sloppily called the theory layer "just markdown to read" — that's wrong, and your correction is the important one: a skill is `SKILL.md` *plus a `scripts/` folder*, and the scripts are first-class members of the package. "Ship the tool with the skill" isn't a workaround, it's the skill model working as designed. So the coupling problem you identified is real and your fix is correct: if `SKILL.md` says "call `visualize_threats()` " and that lives on the board server, you've welded your playing-knowledge package to a specific engine's API. Bundle the helper into the skill and the package is self-contained and portable.

And the deterministic point is the strongest thing you've said in this whole thread. Opening identification is an ECO-book lookup. Fork/pin/skewer detection is a deterministic scan of a position. Mate-in-N is search. Letting the LLM "recognize the Najdorf from having read about it" is strictly worse than `identify_opening(fen)` hitting a book — slower, probabilistic, and wrong under pressure. Detection and tactics are exactly the things you should *never* leave to the model when a script can be exact.

So the clean principle your separation implies:

- **Board server owns the rules and the mutable state.** Legal moves, applying a move, whose turn, is-it-mate, game result. The authoritative substrate both players share. Typed tools, validated, stateful.
- **Skill owns playing strength, and ships its own analysis code.** Opening ID, tactical-motif detection, threat visualization, eval — bundled scripts. Plus the prose for the fuzzy part.

The load-bearing detail that makes this hold together: **the skill's scripts must be pure functions of a position.** They take the authoritative FEN from the server, compute over it, return analysis, and hold *no game state of their own*. The instant a skill script starts tracking its own board you have two sources of truth and you're back in hell. Server = mutable authority; skill scripts = stateless read-only analysis over that authority. That's why the split is sound, and it's worth stating explicitly as the invariant.

One refinement rather than a disagreement: "deterministic beats prose" is fully true for *identification and tactics*, but not for everything labeled "theory." A script can tell you "this is a Closed Sicilian, pawns locked on the c/d/e files" — deterministic, do it in code. What to *do* about a quiet, non-forcing position ("play on the kingside, my pawns point there") is genuinely fuzzy and has no exact function; that's where LLM judgment guided by strategic prose still earns its place. So the skill ends up being scripts (deterministic detection + engine eval) *and* prose (strategic judgment) — which is precisely why a skill is the right container. The board server can't hold prose; a bare tool API can't hold prose; only the skill fuses code and judgment, and playing well is exactly that fusion.

And here's the nice convergence with the worry I raised earlier: I objected that a loose `run_script` interface is bad because it throws away the typed schema the model is tuned for. Your separation *resolves* that — it puts the thing that needs typed validation (moves, where a malformed call corrupts authoritative state) on the server as typed tools, and puts the thing where loose invocation is harmless (analysis, where a botched `identify_opening` call just gets retried) in the skill. The typed-tool concern was always strongest for the move layer and weakest for the analysis layer, and you've drawn the line in exactly that place. The architecture is coherent on the very axis I was nervous about.

---

**You**

Think about this from a broader perspective. We have identified different ways of giving llms capabilities and deterministic tools. How do we decide what to apply when? What if we want the benefits of a skill which can come with explanatory descriptions and more files it can read through progressive disclosure, but the protocol of json schema for native tools/mcp? Think about this from a really broad perspective, what do we usually have? We have an LLM provider, some application the LLM should use, helper functions, interaction functions and explanatory MD files with hopefully progressive disclosure. Think about it from different scenarios, are we the provider of an application or are we a provider of knowledge (or both?) Should we build a harness, should the application come with tools or a harness? There are many questions, you can probably add some. Has the field even landed on a proper rulebook for this? To me everything seems a bit complicated and not settled on. Can we draw on insight from previous problems in hci for example or other fields?

---

**Claude**

Step back far enough and the reason it feels unsettled becomes clear: **MCP, native tools, and skills aren't three options on a spectrum — they're three preset bundles in a roughly six-dimensional space, and the presets are historical accidents, not a taxonomy.** The field feels messy because it's still discovering that the dimensions are separable. The "rulebook" you want isn't a list of "use X when Y"; it's the set of independent axes, because those survive whatever new bundle ships next quarter.

The axes I'd factor it into:

1. **Invocation format** — typed JSON-schema call vs. loose script command vs. free text. (The model is fine-tuned for the first.)
2. **Locality/transport** — in-process function, cross-process JSON-RPC, or filesystem+subprocess.
3. **State ownership** — stateless pure function vs. stateful authoritative service.
4. **Context economics** — eager (all schemas always resident) vs. progressive disclosure (name first, detail on demand).
5. **Packaging/ownership** — baked into the agent, standalone reusable service, or bundled-with-knowledge.
6. **Determinism** — deterministic code vs. model judgment. (Orthogonal to all the above; a deterministic function can ship any of these ways.)

Native tools bundle {typed, in-process, eager, agent-owned}. MCP bundles {typed, cross-process, eager, standalone}. Skills bundle {loose-script, subprocess, progressive, knowledge-bundled}. Notice nothing forces those groupings. What you reached for in the chess thread — progressive disclosure *and* typed schema *and* bundled files — is a perfectly coherent coordinate that simply has no clean off-the-shelf name. And it's partly buildable today: MCP already has a `resources` primitive (readable files/data) alongside `tools`, so "typed actions + read-through knowledge" is expressible as tools + resources in one server. Or a skill harness can auto-wrap each bundled script's `argparse` interface as a typed tool, giving you progressive-disclosure-over-bundled-code with real schemas. Neither is clean yet, which is the tell that the field is young, not that the combination is exotic.

**On "are we an app provider or a knowledge provider" — that's the actual strategic fork, and it determines harness-or-not:**

- *Capability/app provider* (you own the thing being acted on): ship the interaction surface as typed, validated, stateful tools. MCP if you want it reusable across clients; native if it's your own closed agent. You do *not* ship a harness — you ship the capability, the consumer brings the agent. MCP exists precisely so app providers stop each shipping their own agent loop.
- *Knowledge provider* (you know how to use something well but don't own it): ship a skill — prose + helper scripts — that assumes a substrate exists. Your value is the playbook, not the engine.
- *Both* (the realistic case, and the generalization of your chess conclusion): ship typed tools for the authoritative surface *and* a skill that documents how to use them well and bundles deterministic analysis helpers. The vendor who ships only terse tools makes the model guess usage; the one who ships only a skill lets the model corrupt state. Mature = tools + skill, co-shipped.

A harness is the agent loop itself (holds the model, dispatches calls, manages context). You build one only if you're the *agent* provider. Everyone else conforms to existing harnesses — and the gravitational pull toward a standard protocol is exactly "don't make every app reinvent the agent."

**Where the other fields earn their keep — and this is the part worth your attention as someone framing agent productivity as infrastructure:**

The strongest precedent isn't an analogy, it's the literal template: **LSP, the Language Server Protocol.** MCP is consciously LSP-for-tools. LSP solved "every editor reimplementing every language's analysis" by standardizing the editor↔backend conversation. Its history — what consolidated, what got over-engineered, how capabilities are negotiated — is the single most transferable case study you have, and it's not metaphor, it's the same move one domain earlier.

After that, three HCI/systems ideas map almost too cleanly:

*Norman's "knowledge in the head vs. knowledge in the world."* The context window is knowledge in the head — bounded, expensive, fast. Files/resources are knowledge in the world — cheap, large, retrieved on demand. Progressive disclosure *is* the retrieval discipline between them. Norman articulated this in the '80s for humans navigating with limited working memory; the structure is identical for a model with a bounded context. His **gulfs of execution and evaluation** map just as directly: a good tool description narrows the gulf of execution (the model knows it *can* do the thing and how), a clean `tool_result` narrows the gulf of evaluation (did it work, what's the state now). Tool surfaces are affordances for a bounded-rationality agent — which is the thing HCI has studied for forty years.

*HATEOAS / hypermedia from REST.* The idea that a response carries the available next actions, so the client discovers capability from state rather than hardcoding it, is exactly state-driven progressive tool disclosure — your `legal_moves()` returning what's possible *now*. REST mostly abandoned HATEOAS because human-coded clients couldn't exploit runtime affordances. The genuinely interesting question — thesis-grade — is whether the LLM is the first client that *can*, because it reads descriptions at runtime. If so, a 20-year-dead idea becomes live precisely because the consumer changed.

*OS kernel/userland and capability-based security.* Your chess board server is a kernel: authoritative state, narrow validated syscall ABI (the typed tools), no caller allowed to corrupt it. The skill is a userland program composing syscalls, holding no privileged state. A bash tool is handing out a shell instead of a capability. The whole "narrow keyhole vs. broad surface" trust axis is capability-based security, rediscovered.

(And underneath both run two older debates: Unix composability — many small typed tools vs. one `run_script` monolith, where the open empirical question is whether the LLM is a competent enough "shell user" to compose; and inversion of control — native tools are framework-style "we'll call your function," invoked scripts are library-style "you call us," which is just the harness question wearing different clothes.)

**Has the field landed a rulebook? No — and it's honest to say we're pre-paradigmatic.** MCP is ~2024, skills ~2025. My read: the *transport/protocol* axis is consolidating (MCP looks like the LSP-style winner), but the *packaging and disclosure* axes are still wild, and products keep bundling the six dimensions in incompatible ways. We're roughly where web APIs were around the SOAP/REST years, or editor tooling pre-LSP — enough working examples to see the shape, no agreed vocabulary.

A few open questions I'd add to yours, since you asked:

- **Versioning/coupling.** When the app's tools change, how does a bundled skill that references them stay in sync? This is dependency hell waiting to happen, and nobody has the equivalent of semver-for-tool-surfaces yet.
- **Where should validation live** — model (cheap, fallible), harness, or authoritative service? Probably defense-in-depth, but the layering isn't agreed.
- **Who pays the disclosure cost, and who should therefore own the disclosure decision** — the provider (who knows the tool) or the harness (who owns the context budget)? Token economics may dictate an architecture nobody's drawn yet.
- **Does runtime discovery actually help LLMs or just bloat context** versus a curated static toolset? That's empirically testable and largely untested.

If I were pushing your thesis framing, that last cluster is the high-value vein: the model-capability people treat "can the model use the tool" as the question, but every item above is an *infrastructure* decision that determines productivity independent of which model you plug in — which is precisely the bet you're making. The decomposition-into-axes move is itself the infrastructure lens applied to the tooling layer.

---

**You**

It does seem like something is missing. A way to ship a capability for llms that: 1. Comes with procedural knowledge, helper scripts and tools through progressive disclosure (like skills) 2. Has a stable reliable communication protocol (like the tool calling schema) 3. Can interact with external systems like applications or apis (like mcp) 4. Is safe and does not give the model permissions beyond what the harness permits. I think stuff like bash or reading/writing files etc should just be tools that are exposed, not just a sandbox with full permissions. You just give the tools for the allowed actions 5. User decides permissions in a reliable way. For a function that requires user permission LLM should just call it normally, the function contains a stop and wait for user permission, returns either an error I'd user says no or proper response if user say yes. A skill could explain about permissions 6. Provide schema for users. Right now we can force the LLM to give structured outputs, but the LLM should also be able to require structured inputs from users. Like forms or yes/no or allowed responses etc. 7. Single source of truth. Functions and instructions etc. Are only defined in one place not scattered across users. 8. Easy for developers to build, easy to scale, easy to authenticate, supports stateless and state, easy to sync/share across devices

There is probably some more stuff i haven't touched on. And my points might be about too loose or wide.

First of all, am i correct that this is missing? And it would be nice with a solution that just works for all cases. Is it maybe already solved by other disciplines? Like with gaming for example, you have a console, a tv, a controller, a game, the user learns as they play, they can read manuals/tutorials when they need, it's the same interface (the controller) for all games, the game has a single source of truth (lives in steam for example) and probably some more stuff that can apply. Can we maybe apply stuff like this to the emerging technology of ai? With ai though, there are three parties and two interfaces. Not just the game and the user and the controller as interface. With ai you would need user to ai, ai to application and potentially user to application.

---

**Claude**

Short version: you haven't identified a gap so much as independently re-derived the MCP roadmap — most of your eight points already exist as protocol primitives, several added in the last year. The one piece that genuinely isn't unified is the skill layer (your point 1). And the bigger correction is to the wish itself: "a solution that just works for all cases" is the wrong target, for structural reasons. Let me go through it.

**Where your spec already exists (and you should feel validated, because you reasoned your way to a real standards roadmap):**

- Point 6, structured input from users, is MCP **elicitation** — a standardized way for a server to ask the client, and through it the user, for structured information, added in the 2025-06-18 spec, enabling workflows where the server doesn't just execute calls but requests data from the user when needed. There's also a server-requests-the-model primitive, **sampling**, where the server asks for an LLM completion through the client rather than asking the user.
- Point 5, user-gated permissions, is being handled by adopting **OAuth 2.1** wholesale: the MCP server acts as an OAuth 2.1 resource server while a separate authorization server verifies identity, obtains user consent for the requested actions, and issues scoped access tokens. That is exactly your "stop and wait for consent, return yes/no" pattern, formalized.
- Points 7 and 8, single source of truth plus distribution and scale, are an **official registry** — about 3,012 unique servers registered at registry.modelcontextprotocol.io as of early 2026 — plus a just-released revision aimed squarely at your scaling/state requirements: the 2026-07-28 release candidate delivers a stateless core that scales on ordinary HTTP, server-rendered UIs through MCP Apps, long-running work through a Tasks extension, OAuth/OIDC-aligned authorization, and a formal deprecation policy. Concretely, a remote server that used to need sticky sessions and a shared session store can now run behind a plain round-robin load balancer while clients cache tools/list responses for as long as the server's TTL allows — that's "supports stateless and state" plus your single-source caching, conceded as eventual consistency rather than magic.

So points 2, 3, 5, 6, 7, 8 are substantially present. Your instinct was right that they *belong together*; the protocol has been bolting them on one revision at a time.

**What's genuinely still missing, and it's exactly the one you led with:** the **skill layer is not unified with the protocol.** MCP has tools, resources, prompts, elicitation, sampling, auth — but "procedural knowledge + bundled helper scripts + progressive disclosure of files, shipped as one self-contained playbook" is still a separate stack living next to MCP, not inside it. You can approximate it (resources for the readable knowledge, prompts for templated procedure, tools for the typed actions), but there's no first-class "here is how to *play well*, bundled with the capability" object. The packaging-of-judgment layer is the unintegrated piece. That's a real observation, and it's the most defensible part of your "something is missing."

**Why "works for all cases" is the wrong goal.** The tensions between your own points don't dissolve; they trade off. Point 7 (single source of truth) versus point 8 (offline, synced, stateless-and-stateful across devices) is the distributed-systems tradeoff — you get a center of authority *plus cached replicas with TTLs*, i.e. eventual consistency, never both purely. Point 1 (progressive disclosure) versus point 2 (stable schema) pull mildly apart — lazily revealed but stable is achievable, but only by paying for capability negotiation. Every prior attempt at a do-everything protocol (SOAP/WS-\* is the cautionary tale) collapsed under its own generality, and the survivors won by being a *thin minimal core plus layered conventions*. MCP is visibly choosing that path — a stateless core, then *extensions* (Apps, Tasks) layered on. So the thing that "just works" won't be one artifact; it'll be a stack, the way the web is TCP + HTTP + TLS + OAuth + a package registry, not one mega-protocol. The unification you want is architectural layering, and chasing a monolith is the failure mode, not the solution.

And the ecosystem proves it's unsettled in practice, not just in theory: only about 8.5% of registered MCP servers use OAuth, with the rest relying on static keys or nothing, and there have been critical CVEs including a 9.6-severity remote-code-execution and over a thousand unauthenticated endpoints found leaking credentials. The spec moved toward your point 4; the deployments haven't.

**Now the gaming analogy — it's generative, and it's exactly right about the plumbing and exactly wrong about the hard part.**

What maps cleanly: the **console is the trusted runtime** — it enforces least-privilege by construction (a game can't format your drive), which is your point 4 done properly: capability granted, not sandbox-with-everything. The **controller is the standardized interface** (one shape across all games = the typed tool-call schema, point 2). The **manual / in-game tutorial is progressive disclosure** (point 1). And **Steam is the distribution/auth/sync/versioning layer** — entitlement, cloud saves (state sync), patching (versioning), store as single source — which is a startlingly good model for points 7 and 8, and is essentially what the MCP registry is trying to become. Console certification (lotcheck/TRC) even maps to the security-vetting gap the registry currently lacks.

Where it breaks is precisely the seam you spotted. **In gaming the content is inert and the only agent is the human; in your system the agent is in the middle and partly autonomous.** A game doesn't act on your behalf against a third party while you're away. That delegated-agency problem is not a gaming problem — it's the **principal-agent problem** from economics and law (it's literally why we call these things "agents"): how does a principal grant a competent-but-not-fully-trusted agent *scoped, revocable* authority to act on their behalf, with the information asymmetry that the agent knows things the principal doesn't? Fiduciary scope, delegated authority, audit — your points 4 and 5 are the principal constraining the agent. And the field's *operational* answer to that exact three-party shape is **OAuth's three-legged flow**, which was invented for "a client acts on a user's behalf against a resource with user-granted scoped consent." That's why MCP reached for OAuth rather than inventing something — your three-party intuition is the reason the auth layer looks the way it does.

**Your three-interface decomposition is the sharpest thing in your message, and it has a security crux you should make explicit:**

- Interface A, user ↔ AI: natural language plus structured elicitation/forms (your point 6).
- Interface B, AI ↔ app: typed tool calls (points 2, 3).
- Interface C, user ↔ app: consent and authority — and **this one must be a direct trusted channel, not relayed through the AI.** The model is the untrusted party in the middle; you can't let it be the thing that asserts "the user said yes." The OAuth consent screen is rendered by the authorization server straight to the user, never by the client — and MCP added exactly this escape hatch: URL-mode elicitation, for user interactions that cannot safely happen inside the MCP client. So your point 5 is right, but the load-bearing refinement is *where the prompt renders*: in interface C, the trusted channel, bypassing the agent. A permission system that routes consent through the AI is the vulnerability, not the feature.

Has the field landed a rulebook? No — it's roughly where the web was during the SOAP/REST years: enough working pieces to see the shape, a core consolidating (MCP as the LSP-of-tools), and the packaging, security, and skill-integration layers still wild. For your thesis, that three-interface model with the trust asymmetry on interface C is, I think, the high-value frame: the productivity-determining decisions live at the *boundaries between the three parties*, not inside the model — which is your whole infrastructure-not-capability bet, now with a concrete place to plant the flag.

Open questions I'd add to the pile: how does a bundled skill stay version-synced with the tool surface it references (the coupling problem, still unsolved); where should authority be enforced — model, harness, or resource server (defense-in-depth, but the layering isn't agreed); and can the skill layer be folded into the protocol as a first-class object, or is "judgment" inherently too unstructured to standardize the way "actions" were? That last one might be the actual frontier.

---

**You**

Do you think it would be possible to make a harness that takes a skill witht he normal format, but turns the python scripts into excecutable tools in the tool format that native tools/mcp uses? would that not be a best of both worlds approach? and the tools are not listed untill the skill is loaded?

---

**Claude**

Yes, it's buildable, and it's the exact synthesis you've been circling for the last several turns. The "tools not listed until the skill loads" part is the important bit: that's revealing *typed schemas* lazily instead of revealing *files* lazily, which resolves the one tension I flagged earlier — eager-schema (native/MCP) vs. progressive-disclosure (skills). You don't have to choose. Reveal the schemas on skill-load and you get progressive disclosure *and* the typed format the model is tuned for. MCP's design already anticipates this — a tool list isn't required to be static; there's a list-changed notification precisely so the available toolset can grow at runtime. So "load skill → its tools appear" is a legitimate, supported move, not a hack.

But there's one engineering decision that makes or breaks it, and it's worth getting right rather than discovering later: **how each script declares its schema.** Don't reverse-engineer `argparse` — it's too thin (you lose nested objects, per-field descriptions, output schemas). Make the script's entrypoint a *typed signature* — a Pydantic model as input — and you get the JSON Schema generated *and* runtime validation *and* a single source of truth, all from one declaration. That directly satisfies your earlier point 7: the contract lives in one place, and both the model-facing schema and the actual execution validate against it. The per-tool *description* should be the docstring/manifest co-located with the script; SKILL.md's prose then does the cross-cutting job it's actually good at — orchestration and judgment ("run `detect_tactics` before `make_move`; in quiet positions, prefer..."). Clean division: per-tool affordance lives in the code, procedural glue lives in the markdown.

The place where "best of both worlds" stops being free is **state** — the same axis from before. A stateless analysis script (take a FEN, return tactics) wraps perfectly as a subprocess-per-call tool; cold-start cost is irrelevant for that workload. But a tool that needs persistent state or expensive init — a loaded model, a live DB connection, a browser that stays open — does *not* want a fresh process per call. At that point the skill shouldn't ship a one-shot script; it should ship a long-running server, and your harness needs to manage process lifecycle (warm pools, or just run the thing as a persistent local MCP server). And notice what that means: once your harness manages process lifecycle and auto-publishes typed toolsets from a loaded package, **it *is* an MCP host whose packaging format happens to be a skill.** That's the honest endpoint of your idea — not a third thing, but "MCP host + skill-as-package frontend," with skills reduced to a distribution/disclosure format over a tool protocol. Which is exactly the direction the ecosystem is drifting, so you'd be building with the grain.

Two smaller cautions, neither a blocker:

The permission gate (your points 4/5) needs to be declared per tool in the manifest — which tools are free, which require consent before execution — so the harness knows where to insert the stop-and-ask. Additive, but the skill format has to carry it.

And loading a skill that auto-publishes *executable* tools is a trust event, not a convenience. You're running third-party code and immediately handing the model live actions from it. Given the state of the ecosystem — a meaningful fraction of published servers ship with no auth and malicious packages exist — the harness should treat "install/load skill" like installing a plugin: signed source, and the script execution itself sandboxed (least-privilege at the *process* level, separate from the per-tool permission gate). In your gaming analogy this is the certification + entitlement moment, and skipping it is how the convenience becomes the attack surface.

So: yes, do it, the design is sound, and "lazy-revealed typed tools from a bundled package" is the right shape. The only honest asterisks are that it's fully free only for stateless tools, that the schema contract should be an explicit typed signature rather than scraped from argparse, and that auto-publishing executable tools turns skill-loading into a security boundary you have to actually defend.