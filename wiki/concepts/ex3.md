---
type: concept
sources: []
related_concepts: []
related_work: [module-llm-server, experiment-chess, experiment-math, experiment-riksantikvaren, experiment-vision-landmarks, experiment-incubation, experiment-wcag-skill]
status: stable
updated: 2026-06-01
---

# eX3 — Experimental Infrastructure for Exploration of Exascale Computing

**Status:** Active access
**Purpose:** Run local LLMs, expose an inference API for experiments
**Contact:** ex3-helpdesk@simula.no (Tore Larsen, sysadmin)
**Wiki:** http://wiki.ex3.simula.no/
**Modules repo:** https://github.com/jamtrott/ex3modules

---

## What is eX3?

eX3 is a national HPC research infrastructure hosted at Simula Research Laboratory, funded by the Research Council of Norway (contract 270053). It is a **heterogeneous experimental cluster** — meaning it has many different CPU/GPU/accelerator architectures, and is explicitly *not* a production system. It can be reconfigured or reserved at any time, and uptime is not guaranteed.

**Important:** eX3 is for public research and education only. No commercial use without explicit approval.

---

## SSH Access

```
Host ex3
  User <username>
  HostName dnat.simula.no
  Port 60441
```

Then: `ssh ex3`

Alternatively, connect via VPN and use `srl-login1.ex3.simula.no` directly (no port needed). The login node runs Ubuntu 18.04.5 LTS (x86_64). Change password on first login with `passwd`.

Set up public key auth by adding your public key to `~/.ssh/authorized_keys` on the login node.

**File transfer:**
```bash
# Via SSH tunnel (no VPN):
rsync -avrz -e "ssh -p 60441" <sourcedir> <user>@dnat.simula.no:D1/

# Via VPN or on-premise:
rsync -avrz <sourcedir> <user>@srl-login1.ex3.simula.no:D1/
```

---

## Hardware Overview

### GPU Nodes (relevant for LLMs)

| Hostname | CPUs | RAM | GPUs | Slurm Partition |
|----------|------|-----|------|-----------------|
| gh001–gh002 | 2x ARM Neoverse V2 | 480GB | 1x NVIDIA GH200 (96GB HBM3 each) | gh200q |
| g002 | 2x AMD EPYC 7763 | 2TB | 8x NVIDIA A100 (80GB each) | hgx2q |
| n013–n014 | 2x AMD EPYC 7763 | 2TB | 2x NVIDIA A100 (40GB each) | milanq, a100q |
| n015–n016 | 2x AMD EPYC 7763 | 2TB | 2x AMD Instinct Mi210 | milanq, mi210q |
| g001 | 2x Intel Xeon Platinum 8186 | 1.5TB | 16x NVIDIA V100 (32GB each) | dgx2q |
| n004 | 2x AMD EPYC 7601 | 2TB | 1x AMD Instinct Mi100 | defq, mi100q |
| n001–n003 | 2x AMD EPYC 7601 | 2TB | AMD Vega20 GPU | defq, amdgpuq |

**Best options for LLM inference:** g002 hgx2q (2× A100 80GB, TP=2, 128k context, no offload — **current default for [[module-llm-server]]**, reserve in advance), gh001/gh002 gh200q (GH200 96GB HBM3, aarch64, 64k with CPU offload — good fallback, usually idle), n013–n014 a100q (2× A100 40GB, 8k context only).

### Other Nodes (non-GPU)

| Hostname | Hardware | Partition |
|----------|----------|-----------|
| n005–n008 | 2x ARM Cavium ThunderX2, 1TB RAM | armq |
| n009–n012 | 2x HiSilicon KunPeng 920, 1TB RAM | huaq, a40q |
| n017–n020 | 2x AMD EPYC 7413 + FPGAs | fpgaq |
| h001 | 2x Intel Xeon SP 8360Y, 2TB RAM, 8x Habana Gaudi HL205 | habanaq |
| n041–n048 | 1x Intel Xeon Silver 4112 | slowq |
| n049–n060 | 1x AMD EPYC 7302P, 256GB RAM | rome16q |
| n061–n064 | 2x AMD EPYC 7302P, 512GB RAM, Xilinx Alveo U250/U280 | fpga32q |
| ipu-pod64-server1 | Graphcore IPU-POD64 (64x GC200 IPUs) | ipuq |
| srl-login1, srl-adm1, srl-mds1, srl-mds2 | 2x Intel Xeon Gold 6130 | xeongold16q (login/mgmt) |

### Interconnect
- 200 Gbps InfiniBand HDR (primary, ib1net — BeeGFS+MPI stable)
- 400 Gbps InfiniBand NDR (ib2net — AR/CC research: slowq, rome16q)
- Dolphin PCIe Gen3/Gen4 NTB
- 10/25/100 Gbps Ethernet

---

## Job Scheduler: Slurm

All real work **must** go through Slurm. Do not run compute jobs directly on the login node.

```bash
# Load Slurm first
module load slurm/21.08.8

# Key commands
squeue               # see all running/queued jobs
sinfo                # see partitions and node status
salloc -p a100q --gres=gpu:1 --time=02:00:00   # allocate interactively
srun -p a100q --gres=gpu:1 --pty /bin/bash      # interactive shell on GPU node
sbatch myjob.sbatch  # submit a batch job
scancel <jobid>      # cancel a job
```

### Example sbatch script

```bash
#!/bin/bash
#SBATCH --job-name="llm-serve"
#SBATCH --partition=a100q
#SBATCH --time=0-08:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --gres=gpu:1
#SBATCH --output=%j-%x-stdout.txt
#SBATCH --error=%j-%x-stderr.txt

# your commands here
srun python serve.py
```

### Key rules
- Always set `--time` to a reasonable limit — don't hog resources
- Only use the CPUs/GPUs you allocated (don't spawn more threads than allocated cores)
- Don't SSH directly into compute nodes — use `srun --pty` or `ssh <node>` while an allocation is active (see Gotchas below)
- Don't let allocations sit idle

---

## Software & Environment Modules

eX3 uses Environment Modules to manage software.

```bash
module use /cm/shared/ex3-modules/0.6.1/modulefiles  # add eX3-specific modules
module avail              # list available modules
module avail python       # search for python modules
module list               # show loaded modules
module load gcc/11.2.0    # load a module
module unload gcc/11.2.0  # unload
```

### Python

Python 2–3.11 are all available at `/usr/bin/python3.x`. **Use virtual environments** for project-specific packages:

```bash
python3.11 -m venv ~/myenv
source ~/myenv/bin/activate
pip install <package>
deactivate
```

For pre-installed scientific Python (numpy, etc.):
```bash
module use /cm/shared/ex3-modules/0.6.1/modulefiles
module load python-3.7.4 python-numpy-1.19.2
```

### Compilers available (x86_64)
- GCC 8.4–11.2 (default: gcc/11.2.0)
- Intel (icc, oneAPI 2021.2)
- NVIDIA nvhpc 20.11–22.3
- CUDA-enabled GCC: gcc/cu116, gcc/cu117

### Compilers available (ARM / arm64)
- ARM Clang (armclang 19.3–22.0), ARM Fortran (arm/ArmIE)
- GCC 9.1–11.2
- ARM Forge 21.0

---

## Storage

| Path | Type | Use |
|------|------|-----|
| `/global/D1/homes/<user>` | BeeGFS parallel FS | **Primary home — use for most storage** |
| `/global/D1/projects/` | BeeGFS parallel FS | Shared project data (request from admin) |
| `/home/<user>` | Network FS | Limited capacity — source code only, NOT large datasets |
| `/work` | Fast local NVMe per node | Temporary data during job; create `mkdir -p /work/$USER` in sbatch |
| `/work/docker` | Local node | Docker image cache |
| `/tmp` | Local disk | Small; do NOT use as TEMPDIR/TMPDIR |

**Total BeeGFS capacity:** ~1 PB. **No long-term storage** — eX3 is not a data archive. Back up important results elsewhere.

---

## LLM Serving Strategy

To run a local LLM and expose an API endpoint:

### 1. Allocate a GPU node
```bash
srun -p a100q --gres=gpu:1 --nodes=1 --ntasks=1 --cpus-per-task=16 \
     --time=08:00:00 --pty /bin/bash
```

### 2. Set up environment
```bash
mkdir -p /work/$USER
python3.11 -m venv /global/D1/homes/$USER/llm-env
source /global/D1/homes/$USER/llm-env/bin/activate
pip install vllm  # or: pip install llama-cpp-python, pip install ollama
```

### 3. Run inference server
```bash
# vLLM example (OpenAI-compatible API):
python -m vllm.entrypoints.openai.api_server \
    --model <model-path-or-hf-id> \
    --host 0.0.0.0 --port 8000
```

### 4. Access API from local machine
Forward the port via SSH:
```bash
ssh -N -L 8000:localhost:8000 -p 60441 <user>@dnat.simula.no
```
Then hit `http://localhost:8000/v1/...` from your local machine.

For a two-hop tunnel (laptop → login node → compute node):
```bash
ssh -N -L 11500:<compute-node>:28811 ex3
```

### 5. For a persistent service: use sbatch
Write an sbatch script that starts the server and keeps it running for the job duration. Standard output/error go to files named `<jobid>-<jobname>-stdout.txt` etc. in the working directory.

See [[module-llm-server]] for the full verified end-to-end procedure with Gemma 4 31B-it.

---

## Known Quirks / Operational Gotchas

Discovered during LLM bootstrap sessions (2026-05-23) and the context-window push session (2026-05-24). See [[module-llm-server]] for full context.

- **gh200q is aarch64.** Requires a separate venv (`venv-gh200`) built on a gh200q node — x86_64 vLLM binaries from a100q's venv won't run there.
- **`curand.h` missing on gh200q.** `/usr/local/cuda` symlink doesn't include it. flashinfer JIT compilation fails. Fix: set `CUDA_HOME=/usr/local/cuda-12.6` (or higher) before invoking vLLM.
- **vLLM CPU offload (`--cpu-offload-gb`) works well on GH200.** GH200 unified memory + 480 GB CPU RAM makes 120 GB offload painless and unlocks 64k context for a 31B BF16 model.
- **vLLM tool calling requires explicit flags.** `--enable-auto-tool-choice --tool-call-parser gemma4` — without these, `tool_choice: auto` requests return HTTP 400. **Use `gemma4` parser, not `pythonic`** — the latter causes Gemma 4 tool calls to leak as plain text (vLLM issue #39043).
- **hgx2q GPUs may be dirty even when Slurm says they're free.** Slurm tracks GPU *allocation* but not VRAM usage. Other users' processes can hold VRAM on a GPU without an active Slurm job. Symptom: vLLM fails immediately with `Free memory on device cuda:N (X/79.25 GiB) is less than desired GPU memory utilization`. Workaround: email ex3-helpdesk@simula.no to have the node cleaned, or fall back to gh200q which has no other VRAM consumers.
- **Slurm module name:** the correct module is `slurm/21.08.8`, not `slurm/20.02.7` (the older version is gone).
- **`hf` CLI corrupts large files on BeeGFS.** huggingface-cli v1.16.1 silently produces malformed tokenizer.json files on BeeGFS (8.8 MB vs correct 7 MB, deterministic byte-position corruption at 5 MiB boundary). Workaround: use `git clone` for small files and `curl -L` for safetensors weights directly.
- **git-lfs is NOT installed on the login node.** A bare `git clone` of a HuggingFace model repo returns LFS pointer files (tiny text files) rather than the actual weight tensors. Always curl the safetensors files explicitly after cloning.
- **`srun --jobid=X --pty bash` hangs.** Neither `srun --jobid=X --pty bash` nor `srun --jobid=X --overlap --pty bash` open an interactive shell inside an existing allocation. Workaround: `ssh <node>` directly from the login node once you have an active allocation on that node — the login node permits this.
- **Local port 11434 is blocked by Ollama.** If Ollama is running locally, port 11434 is occupied. Use a different local tunnel port (e.g. `11500`).
- **HuggingFace cache override.** The cluster sets `HF_HUB_CACHE=/global/D1/huggingface/cache/hub` system-wide (read-only for users). Setting only `HF_HOME` is not sufficient because `HF_HUB_CACHE` takes precedence. Must override all three: `HF_HOME`, `HF_HUB_CACHE`, and `HF_ASSETS_CACHE` to a user-writable path.

---

## Code of Conduct (Rules)

- **Research/education only.** No commercial use without prior approval from ex3-contact@simula.no.
- **File permissions:** You are responsible for setting appropriate access levels on your data. Don't peek at other users' files.
- **Sensitive data:** Contact ex3-contact@simula.no before loading confidential or sensitive data.
- **Ethics:** Follow NENT guidelines. Publications must comply with the Vancouver Convention.
- **System stability:** eX3 can be reconfigured or reserved for specific users at any time. Don't rely on it as a production system. Don't store data long-term.
- **Liability:** Simula/eX3 consortium is not liable for any damages arising from use.

---

## Publications

If you publish research using eX3, notify ex3-contact@simula.no and include this acknowledgment:

> "The research presented in this paper has benefited from the Experimental Infrastructure for Exploration of Exascale Computing (eX3), which is financially supported by the Research Council of Norway under contract 270053."

---

## Quick Reference

```bash
# Connect
ssh -p 60441 <user>@dnat.simula.no

# Check available GPU partitions
sinfo -p a100q,hgx2q,dgx2q,mi100q,mi210q

# Interactive GPU session
srun -p a100q --gres=gpu:1 --time=02:00:00 --pty /bin/bash

# Load modules
module use /cm/shared/ex3-modules/0.6.1/modulefiles
module avail

# Transfer files to eX3
rsync -avrz -e "ssh -p 60441" ./mydir/ <user>@dnat.simula.no:D1/

# Help
# Wiki: http://wiki.ex3.simula.no/
# Email: ex3-helpdesk@simula.no
```
