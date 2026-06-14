---
type: module
status: in-progress
related_concepts: [ex3]
related_work: [experiment-chess, experiment-math, experiment-riksantikvaren, experiment-vision-landmarks, experiment-incubation, experiment-wcag-skill, module-skillful-agent]
sources: []
updated: 2026-06-02
---

# module-llm-server

Self-hosted LLM inference on the eX3 HPC cluster (Simula), exposed as an OpenAI-compatible HTTP endpoint that experiments can hit from anywhere via SSH tunnel. All experiments that need an LLM target this module rather than a public API.

## How to start the server (current)

```bash
python3 software/ex3/serve.py
```

The script handles everything: cancels any leftover jobs, submits a new Slurm job, waits for the node, polls until vLLM is ready, opens the SSH tunnel. See `software/ex3/README.md` for setup requirements (SSH config, venvs on eX3, HF token).

To attach to an already-running Slurm job (e.g. a long reservation) without resubmitting:

```bash
python3 software/ex3/serve.py --attach <job_id>
```

**API endpoint once running:** `http://localhost:11500/v1`

```bash
curl http://localhost:11500/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"google/gemma-4-31B-it",
       "messages":[{"role":"user","content":"Hello"}],
       "max_tokens":100}'
```

Press **Ctrl+C** to cancel the Slurm job and close the tunnel. With `--attach`, Ctrl+C closes only the tunnel — the Slurm job keeps running.

## Current working configuration (as of 2026-06-01)

- **Recommended partition**: `hgx2q` (2× A100 80GB, x86_64). Uses `venv`. No CPU offload — lower latency.
- **Fallback partition**: `gh200q` (1× GH200 96GB, aarch64). Uses `venv-gh200`. Requires CPU offload; higher latency.
- **Last resort**: `a100q` (2× A100 40GB, x86_64, 8k context only). Uses `venv`.
- **Model**: `google/gemma-4-31B-it` (BF16, multimodal).
- **Context window**: **128k on hgx2q** (no offload). **64k on gh200q** with `--cpu-offload-gb 120`. 8k on a100q.
- **Tool calling**: enabled via `--enable-auto-tool-choice --tool-call-parser gemma4`.
- **Serving**: vLLM 0.21.0, OpenAI-compatible HTTP on `0.0.0.0:28811` of the compute node.
- **Access from laptop**: SSH tunnel `localhost:11500 → <node>:28811`.
- **HF token**: stored at `/global/D1/homes/$USER/.hf_token` on eX3 (chmod 600).

## Partition comparison

| Partition | Node | VRAM | Arch | TP | Max context | Latency | Notes |
|-----------|------|------|------|----|-------------|---------|-------|
| hgx2q | g002 | 2×80 GB (of 8 total) | x86_64 | 2 | **128k** (no offload) | **Fast** | **Recommended**; often occupied — reserve in advance |
| gh200q | gh001/gh002 | 96 GB HBM3 | aarch64 | 1 | 64k (120 GB CPU offload) | Slower (offload) | Good fallback; usually idle |
| a100q | n013/n014 | 2×40 GB | x86_64 | 2 | 8k | Fast | Last resort; 8k is tight for most workloads |

**Why hgx2q is preferred over gh200q:** Both fit the 31B model, but hgx2q uses no CPU offload — all KV cache stays on GPU. gh200q's `--cpu-offload-gb 120` swaps KV cache blocks to CPU RAM during inference, adding latency per token. For single-request workloads (chess experiment, interactive use) this difference is noticeable.

**TP size must be a power of 2.** vLLM tensor parallelism requires the TP size to divide evenly into the model's attention heads. Valid options: 1, 2, 4, 8. Using 3 or any odd number > 1 will fail.

**Reserving hgx2q for longer runs:** g002 is often occupied by other users' long jobs. When it is free, submit with `--time=7-00:00:00` to hold the allocation. The Slurm max for hgx2q appears to allow at least 7 days. Use `--attach <job_id>` in serve.py to reconnect to a reserved job across sessions.

## Critical flag explanations

- `--tensor-parallel-size 2` (hgx2q/a100q) — required for multi-GPU. 31B BF16 ~58GB does not fit on a single 40GB or 80GB card with KV cache headroom at scale.
- `--tensor-parallel-size 1` (gh200q) — single GH200 96GB fits the full 31B model (~58GB weights + overhead).
- `--max-num-batched-tokens N` — must match `--max-model-len`. Gemma 4 is multimodal; default 2048 < 2496 (mm token budget) raises ValueError.
- `--gpu-memory-utilization 0.95` — maximises KV cache slice of GPU VRAM.
- `--cpu-offload-gb 120` (gh200q only) — offloads KV cache blocks to CPU RAM. GH200 node has hundreds of GiB free. 120 GB offload buys ~55 GiB of effective KV cache memory (vLLM reports `Available KV cache memory: 60.25 GiB`), enough for 64k context. Not needed on hgx2q.
- `--enable-auto-tool-choice --tool-call-parser gemma4` — required for tool/function calling. **Must use `gemma4` parser, not `pythonic`.** Gemma 4 uses its own tool-call format (`<|tool_call>...<tool_call|>` with bare-key args). Using `--tool-call-parser pythonic` (the Llama 3.2/4 parser) causes tool calls to leak as plain text content (vLLM issue #39043).

## Context window limits — what was tried

On **a100q** (2× A100 40GB), after model load only ~3.89 GiB remains for KV cache:
- 8k ✅ works (KV cache ~3.44 GiB needed)
- 32k ❌ OOM (needs ~15 GiB)
- 64k ❌ OOM
- 128k ❌ OOM
- 32k + `--cpu-offload-gb 20` ❌ OOM (base KV cache too small to bootstrap offload)

On **gh200q** (1× GH200 96GB), after model load ~5.34 GiB remains for KV cache on GPU. CPU offload buys back KV cache memory:
- 128k (no offload) ❌ OOM (needs 110 GiB KV cache vs 5.34 GiB available)
- 32k + `--cpu-offload-gb 30` ✅ works (early test, before tuning)
- 128k + `--cpu-offload-gb 120` ❌ OOM (110 GiB needed, 60.25 GiB available)
- **64k + `--cpu-offload-gb 120` ✅ works** — final gh200q configuration
- vLLM reports estimated max context of 71,760 tokens with 120 GB offload, so 64k has headroom

On **hgx2q** (2× A100 80GB, TP=2), total 160 GB VRAM:
- **128k ✅ works** (no offload needed) — verified 2026-06-01

## Things that did not work

- **`--tool-call-parser pythonic` with Gemma 4**: tool calls leak into chat content as raw text. Must use `--tool-call-parser gemma4`. See vLLM issue #39043.
- **`--enable-auto-tool-choice` missing**: vLLM rejects all tool-call requests with `status 400: "auto" tool choice requires --enable-auto-tool-choice and --tool-call-parser to be set`. Must be in the launch flags.
- **False-positive health check**: original `wait_for_vllm` used a temporary tunnel on port 11501. If a previous job was still running, port 11501 returned a stale 200 and the script declared "vLLM ready" before the new node was up. Fixed: health poll now uses the real tunnel on port 11500 directly.
- **`ExitOnForwardFailure=yes` on tunnel**: SSH closed the tunnel immediately if vLLM hadn't opened its port yet. Fixed: `ExitOnForwardFailure=no` with auto-restart if the tunnel dies.
- **`curand.h` missing on gh200q**: flashinfer JIT compilation failed because `/usr/local/cuda` symlink doesn't include curand headers. Fixed: sbatch script sets `CUDA_HOME=/usr/local/cuda-12.6` on gh200q nodes.
- **Stale jobs blocking the node**: relaunching `serve.py` without cancelling the previous job left the node occupied. Fixed: `serve.py` now cancels all `llm-serve` jobs at startup (unless using `--attach`).
- **gh200q aarch64 incompatibility**: x86_64 venv at `.../venv` cannot run on GH200 (ARM). Fixed: separate `venv-gh200` built on gh002 with `pip install vllm` (aarch64 wheel, vLLM 0.21.0).
- **`HF_HOME` alone**: cluster-wide `HF_HUB_CACHE` env var overrides it. Must set all three: `HF_HOME`, `HF_HUB_CACHE`, `HF_ASSETS_CACHE`.

## pydantic-ai profile configuration

When consuming the vLLM endpoint through pydantic-ai (either via the skillful-agent SDK or directly), the default `OpenAIProvider` profile has two fields that cause problems with Gemma 4 on vLLM:

- **`openai_supports_strict_tool_definition=True`** (default) — causes pydantic-ai to send `"strict": true` inside every tool definition. Gemma's chat template ignores this field, but vLLM may reject or mishandle it, producing intermittent HTTP 400 errors with malformed JSON messages.
- **`openai_supports_tool_choice_required=True`** (default) — causes pydantic-ai to send `tool_choice: "required"` when the model must call a tool. vLLM behaviour with this flag is undefined for Gemma; `tool_choice: "auto"` (what `--enable-auto-tool-choice` handles) is safer.

**Fix** — pass a custom profile when constructing the model:
```python
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIModelProfile

profile = OpenAIModelProfile(
    openai_supports_strict_tool_definition=False,
    openai_supports_tool_choice_required=False,
)
model = OpenAIChatModel(model_name, provider=provider, profile=profile)
```

**Do not** set `openai_chat_thinking_field` — Gemma's vLLM template strips thinking from history automatically when it arrives in `content`; routing it through a separate field breaks multi-turn thinking-stripping.

For the full explanation of Gemma's native tool format, the chat template mechanics, and the thinking channel behavior, see [[gemma4-vllm-pydantic-ai-integration]].

## Downstream integration

The same backend-selection pattern is used in two places:

### 1. `software/skillful-agent/` (the SDK server itself)
Configured via `.env`:
```
SKILL_AGENT_EX3_BASE_URL=http://localhost:11500/v1
SKILL_AGENT_OPENAI_MODEL=google/gemma-4-31B-it
```
`server/app.py` branches on `SKILL_AGENT_EX3_BASE_URL` (highest priority) → `SKILL_AGENT_AZURE_ENDPOINT` → OpenAI. Uses `OpenAIProvider(base_url=..., api_key="dummy")` — vLLM doesn't require auth.

### 2. `experiments/chess/backend/` (chess experiment)
The chess experiment imports skillful-agent as a git dependency (`skill-agent` from `github.com/andreasklae/skillful-agent`) but **builds its own `Agent` instance** in `app/agent_player.py:_build_agent` rather than going through the skillful-agent HTTP server. This means the chess backend must replicate the backend-selection logic locally. Updated 2026-05-24 to mirror the skillful-agent priority order.

Configured via `experiments/chess/backend/.env`:
```
SKILL_AGENT_EX3_BASE_URL=http://localhost:11500/v1
SKILL_AGENT_OPENAI_MODEL=google/gemma-4-31B-it
```

To switch back to Azure for either consumer, comment out the EX3 line in the relevant `.env`.

## Files and paths

- **Launcher script**: `software/ex3/serve.py` (local, runs from laptop)
- **Launcher README**: `software/ex3/README.md`
- **x86 venv** (hgx2q/a100q): `/global/D1/homes/$USER/llm-server/venv/` (vLLM 0.21.0)
- **ARM venv** (gh200q): `/global/D1/homes/$USER/llm-server/venv-gh200/` (vLLM 0.21.0, aarch64)
- **User HF cache**: `/global/D1/homes/$USER/.cache/huggingface/`
- **HF token**: `/global/D1/homes/$USER/.hf_token` (chmod 600)
- **Slurm logs**: `/global/D1/homes/$USER/llm-server/logs/<jobid>-stderr.txt`

## Open todos

- ~~Set up SSH key auth~~ ✓ Done 2026-05-24
- ~~Write the wrapper script~~ ✓ Done 2026-05-24
- ~~Revoke the leaked HF token~~ ✓ Done 2026-05-24
- ~~Add tool-call support~~ ✓ Done 2026-05-24
- ~~Wire skillful-agent to eX3 endpoint~~ ✓ Done 2026-05-24
- ~~Set up gh200q ARM venv~~ ✓ Done 2026-05-24
- ~~Push context beyond 32k via CPU offload~~ ✓ Done 2026-05-24 (64k on gh200q)
- ~~Re-attempt hgx2q for full-precision serving~~ ✓ Done 2026-06-01 (128k, no offload, faster than gh200q)
- Try 128k with `--cpu-offload-gb 240` on gh200q if a workload needs it.
- Try Llama 3.3 70B AWQ on a100q with TP=2 (quantized 70B may fit within 80GB).
- Email ex3-contact@simula.no to convert verbal approval to written.
- Recreate HF token: `/global/D1/homes/$USER/.hf_token` was missing on 2026-05-24; needs to be regenerated and placed there (chmod 600).
