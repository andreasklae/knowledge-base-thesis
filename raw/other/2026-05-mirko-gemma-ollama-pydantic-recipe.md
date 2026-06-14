---
source_type: blog-post
author: Mirko (gammavibe.com)
title: Local recipe generator with Gemma 4 + Ollama + Pydantic AI + FLUX.1-schnell
url_note: User-pasted excerpt; URL not recorded — appears to be a gammavibe.com post
captured: 2026-05-27
captured_via: pasted into /kb session by user
---

# Local recipe generator (Mirko / gammavibe)

User-pasted blog post. Key technical points relevant to the chess experiment / Gemma harness question:

## Picking a Gemma 4 variant

- E2B (2.3B) runs on a phone (Pixel 10 Pro).
- 26B A4B MoE works for interactive chat on a laptop.
- **E4B (4.5B) reportedly the most reliable for programmatic Pydantic AI use.**

## Getting structured output to work with Gemma 4 via Ollama

Pydantic AI defaults to `ToolOutput` (tool-call-based structured data). That works for Gemini but unreliable with Gemma 4 via Ollama. Two changes fixed it:

1. **Temperature 0.2.**
2. **Switch from `ToolOutput` to `NativeOutput`.** For Ollama this maps to the `format` parameter with a JSON schema, which uses **server-side constrained decoding**. The model is forced to emit tokens that match the schema. "Less for a smaller model to get wrong."

## Image generation (not relevant to chess; noted for completeness)

FLUX.1-schnell via Hugging Face `diffusers`. On a 4090, a few seconds per image, no memory tricks. `uv` silently installs CPU PyTorch — fix by pinning the CUDA wheel index in `pyproject.toml`.

## Companion repo

`gammavibe-labs/local-recipe-generator` on GitHub (digitalhobbit).

---

## Why this is in raw/other/

User is questioning whether the skillful-agent harness is the right substrate for Gemma 4 in [[experiment-chess]]. This post is one of two external references they pasted alongside that question; the other is the KDnuggets Gemma 4 tool-calling article. Both are sub-academic — captured as grey literature for potential wiki summary.
