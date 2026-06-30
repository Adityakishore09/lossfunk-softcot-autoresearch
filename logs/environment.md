# Environment audit

Audit date: 2026-06-22  
Status: complete before experiments. This log records observed information only; no secret values were printed or stored.

## Hardware

| Resource | Observed value |
|---|---|
| CPU | AMD Ryzen 5 5500U with Radeon Graphics |
| CPU cores / logical processors | 6 / 12 |
| Reported maximum clock | 2100 MHz |
| RAM | 15.35 GiB |
| System disk | C: 460.84 GiB total; 232.10 GiB free |
| GPU | AMD Radeon(TM) Graphics, 0.50 GiB reported adapter memory |
| GPU driver | 31.0.21921.1000 |
| CUDA-capable GPU | None detected; NVIDIA utilities unavailable |

## Installed software and local assets

| Item | Observed value |
|---|---|
| Python | Anaconda Python 3.12.4 |
| Conda | available |
| Git | available, but repository status is blocked by Git safe-directory ownership protection |
| PyTorch | not installed |
| Transformers / datasets / accelerate / PEFT / TRL | not installed |
| NumPy / SciPy | 1.26.4 / 1.13.1 |
| nvidia-smi / nvcc | unavailable |
| pdflatex / pandoc / Docker / uv | unavailable |
| Hugging Face CLI | unavailable |
| Hugging Face model cache | absent |
| Hugging Face dataset cache | absent |

Codex's bundled runtime provides a separate Python environment with pypdf, Pillow, and pdf2image; it does not provide a usable PDF renderer in the checked path.

## Credential indicators

No nonempty environment-variable indicators were found for OpenAI, Anthropic, Hugging Face, AWS, Azure, Google, Weights & Biases, or Kaggle credentials. CUDA_PATH, CUDA_PATH_V12_3, and CUDA_PATH_V12_4 are configured, but the available GPU is integrated AMD graphics and no NVIDIA runtime was found.

## Implication

The local computer cannot run a CUDA-based SoftCoT reproduction. Any model training/evaluation must either use a genuinely CPU-feasible setup or a hosted GPU. No hosted resource has been selected, provisioned, or billed. The project has a hard aggregate model/compute ceiling of US$50.00.

## Lab-server access status

The user placed SSH host 172.30.1.70 in scope and reported an A100 80GB. This report is not yet independently verified: a strictly read-only SSH command to the configured account gaurav@172.30.1.70 reached the server but authentication failed. The local user SSH configuration has no private-key file and the SSH agent exposes no identity. No remote command was executed after authentication.

Following the user's explicit authorization, an ephemeral local Ed25519 keypair was created at C:\Users\Dell\.ssh\codex_lossfunk_isl_20260622. The private key is intentionally not copied into this artifact or its logs. Its public-key SHA-256 fingerprint is SHA256:LTPD/NzSRO8apFys90Fl1UhTwMp861zbag1uIp3Gmig. Access remains pending until its public half is installed for gaurav on the remote server.

### Verified remote audit at 2026-06-22T21:09:14+05:30

| Resource | Observed value |
|---|---|
| Host / account | ISL-Shakti / gaurav |
| GPU | NVIDIA A100 80GB PCIe |
| GPU memory | 81,920 MiB total; 29,110 MiB used at audit |
| GPU utilization | 100% at audit |
| NVIDIA driver | 580.159.03 |
| System memory | 503 GiB total; 481 GiB available |
| Root filesystem | 187 GiB total; 109 GiB available |
| Data filesystem | /data3: 7.3 TiB total; 3.4 TiB available |
| Existing project | /data3/Aditya_Kishore369/SoftCoT |

The GPU was already fully utilized when access was verified. No process was started, stopped, inspected beyond aggregate GPU state, or otherwise disturbed by this project.

The interactive SoftCoT Python environment is registered by prefix at /data2/anaconda3/envs/softcot. The non-interactive SSH shell instead resolves conda to /opt/anaconda3, so name-based conda run -n softcot fails. Future remote audits/runs must use the explicit environment prefix or executable, never assume the interactive shell initialization.

Remote package audit using that explicit executable found Python 3.13.7, PyTorch 2.8.0, Transformers 4.57.3, datasets 4.1.1, accelerate 1.10.1, PEFT 0.13.2, and fastNLP 0.7.0.

At a final pre-run status query on 2026-06-23, the same A100 remained at 100% utilization with 37,122 MiB allocated. No experiment may start until this shared GPU is available.

A subsequent read-only query found the A100 with 44,982 MiB allocated, 36,171 MiB free, and 100% GPU utilization. Four active Python allocations accounted for the reported memory. This is below the user's stated 57 GiB estimate and is insufficient for a safe concurrent official batch-8 SoftCoT run.

User-supplied nvidia-smi output later showed 29,110 MiB allocated, 52,810 MiB free, and 99% utilization across three Python compute processes. Although the reduced batch-1 free-memory threshold was met, compute remained saturated and the run remains unsafe.
