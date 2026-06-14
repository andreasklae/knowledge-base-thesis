---
type: literature
citekey: mirko2026gemma
title: Local recipe generator with Gemma 4 + Ollama + Pydantic AI + FLUX.1-schnell
authors: [Mirko (gammavibe)]
year: 2026
venue: gammavibe.com (personal blog)
raw_path: raw/other/2026-05-mirko-gemma-ollama-pydantic-recipe.md
related_concepts: [tools-component, deterministic-tools-hypothesis, framework-four-components]
related_work: [experiment-chess]
status: summarized
ingested: 2026-05-27
updated: 2026-05-27
---

# Mirko (2026) — Local recipe generator with Gemma 4 + Pydantic AI

## Summary

A blog-post write-up of a weekend project: a local recipe generator that wires Google's Gemma 4 (via Ollama) and FLUX.1-schnell (via Hugging Face `diffusers`) together with [pydantic-ai](https://pydantic.dev/pydantic-ai). The post's interest for this thesis is one specific finding about Gemma 4's structured-output reliability — not the recipes.

## Main claims

### 1. Gemma 4 + Pydantic AI defaults are unreliable

Pydantic AI's default structured-output mechanism is `ToolOutput` — the model returns structured data by emitting a tool call whose arguments are the desired object. This works well with Gemini. With Gemma 4 via Ollama it is unreliable: tool-call JSON is malformed often enough to break the loop. Two changes fixed it for him:

1. **Temperature 0.2** (down from the Pydantic AI default).
2. **Switch from `ToolOutput` to `NativeOutput`.** For Ollama, `NativeOutput` maps to the `format=` parameter with a JSON schema, which engages **server-side constrained decoding**: the model is forced to emit tokens that match the schema. "Less for a smaller model to get wrong."

### 2. Variant selection for programmatic use

Of the Gemma 4 family — E2B (2.3B), E4B (4.5B), 4-31B, and 26B-A4B MoE — Mirko reports **E4B (4.5B)** as the most reliable for programmatic Pydantic AI use. The smaller E2B runs on a phone; the larger MoE is for interactive chat. (The chess experiment uses 31B and remains the more capable model class; this datapoint is about the small-model end of the family.)

### 3. Build environment trivia

`uv` silently reinstalls CPU PyTorch on every `uv sync` if the CUDA index isn't pinned. Fix by adding a `[tool.uv.index]` block for `https://download.pytorch.org/whl/cu126` and pointing `torch`/`torchvision` at it under `[tool.uv.sources]`. Not directly thesis-relevant but worth recording — this pattern bites everyone using `uv` with CUDA.

## Relevance to this thesis

This is grey literature, captured to inform a specific design question in [[experiment-chess]]: whether the existing harness (skillful-agent + pydantic-ai + vLLM, running Gemma 4 31B) is fighting Gemma at the tool-call layer. The directly relevant claim is that **constrained decoding fixes Gemma 4 tool-call argument reliability**. The chess experiment has independently observed a related failure mode — vLLM 400 BadRequest on malformed tool-call JSON from Gemma ([[diary/experiment-chess/2026-05-26-stabilization]] problem 2) — for which the chess code now silently recovers but does not prevent. vLLM's analogue of Ollama's `format=` is `guided_json`. Mirko's post is independent confirmation that this is a real Gemma-family weakness and that schema-constrained decoding is the right shape of fix.

The post is also tangentially relevant to [[tools-component]]: it is a small case study of how the same model can succeed or fail at structured tool calls depending entirely on whether the framework engages constrained decoding. The model didn't get smarter; the contract between deterministic system and non-deterministic agent was tightened ([[aizawa2025tools]]'s framing).

## What this is NOT

Not an academic source. Not benchmarked. Not generalisable beyond the recipe-generator setup. N=1 anecdote from a personal blog. Useful as a corroborating signal, not as a finding. The companion repo (`gammavibe-labs/local-recipe-generator`) is the actual artefact if structured-output details need verification later.

## See also

- [[mayo2026gemma4tools]] — the Mayo / KDnuggets tutorial captured in the same session, sketching a from-scratch Gemma 4 tool-calling loop without pydantic-ai.
- [[diary/experiment-chess/2026-05-27]] — the diary entry that triggered this ingest.
