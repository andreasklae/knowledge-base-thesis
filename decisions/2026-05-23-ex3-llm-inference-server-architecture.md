---
type: decision
status: accepted
---

# eX3 LLM Inference Server: Architecture and Access Pattern

## Context

The thesis requires access to local LLM inference for two purposes:

1. **Experiment workloads.** Several experiments need a controlled, self-hosted inference endpoint (consistent model, known sampling parameters, no commercial provider drift between runs).
2. **Working tooling during the thesis itself.** Pointing Cursor and Pydantic AI agents at a self-hosted base URL for coding and agent-construction tasks during day-to-day thesis work.

Hardware access is available via [[ex3]] (A100 partitions: `a100q` 40GB, `hgx2q` 80GB). The administrator gave verbal approval to "host a server" but the framing was ambiguous about whether that meant a persistent 24/7 service or on-demand inference.

The eX3 wiki and code-of-conduct constrain the design:

- Research/education use only.
- No production-system reliance; nodes can be reconfigured/reserved at any time.
- All compute must go through Slurm. Don't run jobs on the login node.
- "Don't let allocations sit idle." Slurm jobs are time-bounded.
- Compute nodes have no routable public IPs — external access is via the login node only.

An initial proposal of "always-on personal LLM API exposed to the internet, dynamically allocating GPUs only when inference is requested" was rejected during design discussion. Slurm allocations are not dynamic; a held GPU is held for the full reserved window regardless of utilisation. A persistent personal API also drifts toward production use, which conflicts with the research/education clause.

## Decision

**Architecture: on-demand Slurm job + SSH tunnel + local CLI.**

Concretely:

- **Server code lives in a GitHub repository, cloned to** `/global/D1/homes/$USER/llm-server/` on eX3. The repo contains an sbatch script, a pinned `requirements.txt`, configuration, and a README. It is *not* run locally; vLLM requires CUDA and the production model size requires A100-class VRAM, so the cluster is the only runtime environment.
- **Inference engine: [vLLM](https://docs.vllm.ai)**, not Ollama. vLLM is built for data-center GPU throughput and exposes a native OpenAI-compatible HTTP server at `/v1/...`. Ollama would leave A100 performance on the table without meaningfully simplifying the stack.
- **Model files on BeeGFS:** `/global/D1/homes/$USER/models/`, downloaded once via `huggingface-cli download` from inside an interactive `srun` session (not on the login node).
- **Per-session lifecycle.** When inference is needed, a local CLI on the laptop submits a time-bounded Slurm job (`sbatch --time=Nh start.sbatch`), polls `squeue` until the job reaches `RUNNING`, captures the assigned compute node hostname, and opens a two-hop SSH tunnel from the laptop through the login node to the compute node's vLLM port. When done, the CLI cancels the job and tears down the tunnel. No always-on process on eX3 — no daemon on the login node, no orchestrator service.
- **Port choice:** vLLM binds to a high uncommon port on the compute node (e.g. `28811`) to avoid conflicts. The local tunnel maps to a memorable laptop-side port (e.g. `11434`). Clients (Cursor, Pydantic AI's `OpenAIModel`, the `openai` SDK) point at `http://localhost:11434/v1` with `api_key="anything"` and behave as if talking to OpenAI.
- **Auth model: tunnel-private, not internet-exposed.** Because the inference port is reachable only through the SSH tunnel — i.e. only from the laptop that opened the tunnel — the service is not exposed to arbitrary clients. vLLM's `--api-key` is set as defence-in-depth, but the security perimeter is SSH, not application-layer auth.
- **Readiness check:** the CLI polls `GET /v1/models` over the tunnel after the Slurm job is `RUNNING`, because vLLM has a 1–3 minute model-load warmup before it answers. Job-running ≠ server-ready.

## Consequences

- **Rules compliance.** Each Slurm job is a discrete, time-bounded research allocation — the standard eX3 usage pattern. No idle holding of GPUs, no login-node service, no internet exposure. This matches the documented LLM-serving strategy in [[ex3]].
- **No 24/7 endpoint.** Cursor and Pydantic AI work only while a session is active. This is a feature, not a bug: it forces awareness of GPU consumption and aligns with the "research/education" framing.
- **Local CLI is the durable artefact.** Roughly 40–80 lines of bash or Python. It encodes the ssh → sbatch → poll → tunnel sequence and a teardown command. Lives in a separate (or sibling) local repo. Without this CLI the workflow is unergonomic; with it, starting a session is one command.
- **Bootstrap order is "small-model-first on real hardware,"** not "test locally then deploy." The first end-to-end run uses a tiny model (e.g. `Qwen/Qwen2.5-0.5B-Instruct`) so warmup is seconds, the moving parts (sbatch, tunnel, vLLM, CLI) can be debugged quickly, then the production model is swapped in afterward.
- **Two unresolved items, deferred to bootstrap phase:**
  - **Container runtime.** The eX3 wiki page mentions `/work/docker`, but most HPC sites require Singularity/Apptainer instead of Docker because compute-node `docker run` typically needs root. To be confirmed with `ex3-helpdesk@simula.no` before any container-based deployment is built. The fallback is bare venv + `pip install vllm`, which is sufficient for the planned workload.
  - **Administrator confirmation in writing.** The verbal "yes" should be followed up with a short email to `ex3-contact@simula.no` describing the actual usage pattern (per-session vLLM jobs in `a100q`/`hgx2q`, no persistent service, used for thesis experiments and coding-agent tooling) and confirming this is in scope.
- **No commercial-vendor dependency at inference time.** This preserves the experimental property that the inference endpoint is fully under the researcher's control — relevant for reproducibility claims and for experiments where commercial-API drift between runs would be a confound. (Anthropic remains the primary agent vendor under [[2026-05-13-vendor-choice-anthropic]]; this decision concerns self-hosted inference for separate experiment needs and coding tooling, not the primary agent stack.)
- **Pydantic AI compatibility is automatic** because vLLM's `/v1` interface is OpenAI-shaped. No bespoke adapter needed; `OpenAIModel(base_url=..., api_key=...)` suffices.

## Source

Design discussion 2026-05-23 (see [[diary/meta/2026-05-23]]). [[ex3]] wiki page for hardware and policy. Note: this decision concerns self-hosted inference for separate experiment needs and coding tooling, not the primary agent stack.
