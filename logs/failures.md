# Failures and limitations

## 2026-06-22 — Initial Windows management inventory blocked

The first Get-CimInstance audit ran in the filesystem sandbox and received Access denied for CPU, memory, disk, and GPU classes. A read-only approved retry outside the sandbox succeeded. The final environment values are in environment.md.

## 2026-06-22 — PDF visual renderer unavailable

The bundled runtime did not expose pdfinfo.exe at the checked path; PyMuPDF (fitz) was unavailable; and no pdftoppm, pdfinfo, mutool, ImageMagick, or other renderer was discoverable. The first text extraction also failed after page 2 because Windows stdout used CP1252 and could not encode a Unicode right-arrow. Re-running pypdf with UTF-8 output extracted all ten pages successfully. The proposal's textual scientific content was read; a visual PDF render was not available.

## 2026-06-22 — Local ML reproduction environment absent

The local Python environment has no PyTorch, Transformers, datasets, accelerate, PEFT, TRL, cached Hugging Face assets, or CUDA-capable GPU. This is a setup limitation, not an experimental outcome.

## 2026-06-22 — Git status inspection blocked

git status --short did not run because Git considers the parent repository owned by a different Windows SID and recommended a global safe.directory change. No Git configuration was changed, because that change was not necessary for the selected scope.

## 2026-06-22 — First log-file patch construction failed

The first attempt to write the selected-spike logs failed in the agent-side JavaScript wrapper before applying any filesystem change: a Markdown code fence prematurely ended the JavaScript template literal and produced SyntaxError: Unexpected identifier 'pypdf'. The patch was reconstructed with tilde code fences and then applied successfully. No research data or prior user file was overwritten.

## 2026-06-22 — Web search endpoint blocked

A read-only search for the SoftCoT paper and official code failed with HTTP 403 from the search endpoint's Cloudflare challenge. This is a literature-access failure, not evidence about SoftCoT. No source has yet been accepted as authoritative.

## 2026-06-22 — Direct arXiv lookup through the web endpoint also blocked

Direct requests to arXiv through the web endpoint returned the same HTTP 403 challenge. The primary paper was subsequently obtained through a permitted direct read-only request to arXiv and is documented in notes/implementation-feasibility.md.

## 2026-06-22 — Sandbox blocked direct GitHub API access

Two read-only GitHub API attempts in the sandbox failed with a socket-permission error. Approved external read-only requests then succeeded. No repository was cloned and no files were written from GitHub.

## 2026-06-22 — Lab-server SSH authentication unavailable to Codex

The configured account, gaurav@172.30.1.70, rejected a strict non-interactive connection with "Permission denied (publickey,password)." A read-only diagnostic then established that C:\Users\Dell\.ssh contains config and known-hosts files only, with no private key, and that no SSH agent identity is available. The server itself was not modified and no remote audit command ran.

## 2026-06-22 — Lab GPU busy at first verified audit

The A100 was at 100% utilization with 29.1 GiB allocated before any project command ran. This is shared-server state, not an experiment failure. The project will not launch work until a subsequent audit shows capacity is available or the user explicitly directs otherwise.

## 2026-06-22 — Non-interactive Conda environment-name lookup failed

The remote interactive terminal activates softcot, but the SSH shell resolves conda to /opt/anaconda3 while the environment exists at /data2/anaconda3/envs/softcot. Consequently, conda run -n softcot reported "EnvironmentLocationNotFound." No package import or model call occurred. This will be addressed by using the explicit environment-prefix executable for all non-interactive commands.

## 2026-06-22 — Target datasets absent from the current remote project

The remote data directory contains only the official GSM8K-style source files. ASDiv-Aug and StrategyQA are not present. This is a setup gap, not a negative result; no target data will be substituted or generated without recording source, licence, checksum, and deterministic selection rule.

## 2026-06-22 — Tasksource StrategyQA mirror documentation absent

The public tasksource/strategy-qa Hugging Face mirror has no README.md; the attempted documentation request returned HTTP 404. The project instead traced StrategyQA to the official MIT-licensed eladsegal/strategyqa repository and downloaded its canonical dev.json for target-only evaluation.

## 2026-06-22 — Fixed-split execution wrapper did not parse

The first PowerShell wrapper intended to transfer and execute build_fixed_splits.py failed locally with a ParserError caused by nested quoting in a post-run manifest-summary expression. PowerShell rejected the full script before any SSH, SCP, remote write, or split execution occurred. The split artifacts therefore do not exist yet and the retry will separate verification from execution.

## 2026-06-22 — Local Git clone path transport failure

An attempt to create a local clean transfer fork with git clone --no-hardlinks treated the Windows source path as a remote Git transport, reported "git-upload-pack: command not found," and did not create the destination. The vendored upstream source remains unchanged. A plain filesystem copy will be used for the local experiment fork instead.

## 2026-06-22 — Remote harness preflight stopped on CRLF formatting

The three modified Python files were copied into the isolated Linux runtime, but their Windows CRLF line endings made git diff --check flag every line as trailing whitespace. The command stopped before the planned help-only imports. No model was loaded and no GPU work ran. The isolated files will be converted mechanically to LF before the retry.

## 2026-06-23 — Model-download command rejected

The request to download the pinned public Qwen model pair into the isolated runtime was rejected before execution. No model directory, weight file, model load, GPU work, or cost was created by that command. The download script is provided for the user to run manually if they approve it.

## 2026-06-23 — First runbook patch construction failed locally

The initial attempt to write the guarded shell runner and runbook failed in the agent-side JavaScript wrapper because Bash parameter-expansion syntax was interpreted as a JavaScript template expression. No filesystem or server action occurred. The shell script was rewritten to avoid that conflict.

## 2026-06-23 — Local Bash syntax checker unavailable

The Windows workspace has no bash executable, so the local bash -n check for run_seed.sh did not execute even though PowerShell returned success after the preceding Python check. The script was subsequently syntax-checked successfully with Linux bash on the isolated server.

## 2026-06-23 — Shared A100 unavailable for experiment

Read-only GPU telemetry showed 36,171 MiB free but 100% GPU utilization, with four active Python allocations. The project intentionally did not attempt source training or evaluation beside these jobs. This is a shared-resource constraint, not an experimental outcome.

## 2026-06-23 — Batch-1 runner correctly refused a saturated GPU

The user invoked bash scripts/run_seed.sh 41 1. The runner observed 52,043 MiB free but 100% utilization and exited before model loading, as designed. This is a successful resource-safety check, not a completed experiment or a negative scientific result.

## 2026-06-23 — Local sandbox blocked two server-access attempts

The sandboxed `scp` copy and read-only `ssh` verification attempts each failed before server connection because the environment could not access the ephemeral private key or SSH port. After user-approved external access, the copy and verification were retried successfully. These sandbox failures did not alter the server, start a model, consume GPU compute, or constitute experimental failures.

## 2026-06-24 — Seed 41 stopped at the first Trainer checkpoint

Seed 41 (batch size 1) completed source-data preprocessing and one training epoch (7,473/74,730 steps). At the scheduled epoch checkpoint, Hugging Face Trainer attempted generic safetensors serialization of the full wrapper model. It rejected the Qwen assistant model's tied `lm_head.weight` and `embed_tokens.weight` tensors with a `RuntimeError`; the wrapped process then ended with a reported segmentation fault. This was not an OOM error and produced no usable final projection or evaluation result. The raw runner record, training log, and incomplete `checkpoint-7473` directory were preserved at `failures/seed_41_attempt_01_2026-06-24_tied_weight_checkpoint/` in the isolated server runtime.

## 2026-06-24 — First tmux restart attempt blocked by a false positive

The restart command initially matched its own remote-shell command line when checking for a pre-existing `train_softcot.py` process, so it refused to launch. No training process was created. The check was changed to use the standard bracketed process-name pattern and the retry launched successfully.

## 2026-06-25 — Seed 41 evaluation stopped on FastNLP Instance metadata access

The `lossfunk_seed41_retry` tmux session ended because the runner command exited. Inspection showed the source-training stage completed successfully:

- `train_runtime`: 47,383.1714 seconds
- `train_loss`: 0.22973810336555675
- final epoch: 10.0
- saved checkpoint: `/data3/Aditya_Kishore369/lossfunk-autoresearch-runtime/gsm8k-asdiv-strategyqa-transfer/ckpt/gsm8k-source-seed-41-gsm8k-10.0-32-Qwen2.5-7B-Instruct-Qwen2.5-1.5B-Instruct/projection.bin`

The subsequent first evaluation (`gsm8k_learned`) loaded the saved projection and processed the first fixed GSM8K example correctly, but then crashed while constructing the JSON result row:

~~~text
AttributeError: 'Instance' object has no attribute 'get'
~~~

Cause: `evaluate_softcot.py` used `ins.get('qid')`, but rows returned by FastNLP loaders are `Instance` objects rather than normal dictionaries. This is a logging/result-serialization bug, not a model-training failure and not an OOM. The partial evaluation produced no JSON result file, so it is not a scientific result. The evaluator was patched to use a helper that supports both dict-like rows and FastNLP `Instance` rows, and the patch compiled locally and on the lab server.

## 2026-06-25 — Local Git status check unavailable

An attempted `git diff --stat` verification failed because the `autovoila` workspace is not currently a Git repository. This was only a local status-check failure. It did not alter research files, server files, model checkpoints, results, or compute state.

## 2026-06-25 — Evaluation-resume tmux exited at memory guard

The user's attempt to start `lossfunk_seed41_eval` exited before attachment. Server inspection showed 72,121 MiB used, 9,032 MiB free, and 100% utilization on the A100. The resume script requires 50,000 MiB free by default for evaluation, so this was a resource-guard refusal, not a model/evaluation crash. No new raw result JSON file was produced.

## 2026-06-26 — StrategyQA evaluation stopped on JSONL/JSON loader mismatch

The resumed seed-41 evaluation completed the GSM8K and ASDiv conditions and then failed at `strategyqa_learned` before processing StrategyQA examples. The fixed StrategyQA split is newline-delimited JSON:

~~~text
data/fixed/strategyqa_target_dev.jsonl
~~~

but `StrategyQALoader._load()` attempted `json.load(file)`, which expects a single JSON document. Python raised:

~~~text
json.decoder.JSONDecodeError: Extra data: line 2 column 1 (char 1024)
~~~

This is a dataset-loader bug, not a model-quality result and not an OOM. The loader was patched to read `.jsonl` paths line-by-line and retain the old `json.load()` behavior for non-JSONL paths. A server-side smoke test verified that the fixed StrategyQA split loads 200 examples and preserves boolean labels. The stale `strategyqa_learned.log` remains in `results/raw/seed_41` until the resume script archives it on the next run.

## 2026-06-27 — Seed-42 launch guard false positive

The first automated seed-42 tmux launch attempt refused to start after `pgrep` matched the SSH wrapper command that contained the guard's own pattern. No tmux session, result directory, model load, training, evaluation, GPU allocation, or scientific result was created. A simpler GPU-memory guard was prepared, but the approval request to run it was rejected, so seed 42 was not started by the agent.

## 2026-06-27 — Summary rerun refused existing output and directory

After seed 42 completed, the first attempt to rerun `scripts/summarize_results.py --runtime-root .` failed because `results/analysis/summary.json` already existed and the script intentionally refuses to overwrite outputs. The agent preserved the old summary as `summary_before_seed42_2026-06-27_234438.json` and `summary_previous.json`. A second attempt then failed because the script also uses `mkdir(..., exist_ok=False)` for `results/analysis`, so the pre-existing analysis directory caused `FileExistsError`. No raw results were modified. The agent repaired this by archiving the existing analysis directory to `results/analysis_archive_before_combined_2026-06-27_234516`, regenerating a fresh combined `results/analysis/summary.json`, and copying the seed-comparison files back.

## 2026-06-27 — Seed-43 start refused by memory guard

The user attempted `bash scripts/run_seed.sh 43 1` while the A100 had 30,850 MiB free and 92% utilization. The runner warned about contended utilization but exited before model loading because batch-size-one training requires at least 50,000 MiB free. This is a resource-guard refusal, not a training or scientific failure. Since the guard exits before result-directory creation, seed 43 can be started later with the same command when sufficient memory is free.

## 2026-06-27 — First seed-43 override tmux-send produced shell continuation prompt

The first attempt to send the overridden seed-43 launch command into tmux landed as an incomplete quoted shell command and left the pane at a `>` continuation prompt. No model process started from that malformed command. The agent sent `Ctrl-C` and resent the command without path quoting. The second command started seed 43 successfully.

## 2026-06-28 — Local PowerShell inspection used Bash heredoc syntax

An attempted local inspection command used Bash-style `python - <<'PY'` syntax in PowerShell and failed with a parser error before reading results. The command was rerun using a PowerShell here-string piped into Python. No result file, server file, or artifact was changed by the failed inspection command.

## 2026-06-28 — Remote full-target preflight blocked by SSH timeout

Two attempts to inspect the remote data/checkpoint/GPU state before full-target evaluation failed with:

~~~text
ssh: connect to host 172.30.1.70 port 22: Connection timed out
~~~

No remote command ran, no file was changed, and no GPU/model process was started. Full-target evaluation remains pending until the VPN/SSH path is reachable from the agent or the user runs the prepared commands manually in their already-connected VS Code terminal.

## 2026-06-30 — Local TeX compiler unavailable

During paper drafting, the local workspace had no `pdflatex`, `xelatex`, `lualatex`, `latexmk`, `tectonic`, or `pandoc` executable. The agent therefore produced the canonical LaTeX source (`paper/main.tex`) and generated a fallback viewing PDF (`paper/main.pdf`) with the bundled Python/reportlab runtime. This is recorded in `paper/COMPILE_NOTES.md` and in the paper appendix. A true LaTeX rebuild remains possible on a machine with TeX installed.

## 2026-06-30 — Non-material paper-drafting command errors

Several local inspection commands failed without altering scientific results:

- A `Select-String` regex search for checklist macros used unescaped backslashes and failed with an invalid-regex error. It was rerun with literal pattern strings.
- A first public arXiv metadata fetch command had a PowerShell parenthesis error before any network request was made. It was rerun successfully after read-only network approval.
- A `Select-Object -Index 190..205` range was parsed as a string instead of a range expression. It was rerun as `Select-Object -Index (190..205)`.
- The bundled Poppler wrapper commands initially printed "The system cannot find the path specified." The actual Poppler executables under `dependencies/native/poppler/Library/bin/` were then called directly, and PDF rendering succeeded.
- An ACL Anthology ID guessed for ASDiv returned an unrelated mental-health paper. The result was treated as a false citation lookup and was not used as the ASDiv citation.

These were local drafting/verification issues only. They did not modify raw results, launch experiments, spend money, or affect the reported scientific conclusion.

## 2026-06-30 — GitHub repository preparation limitations

The local GitHub CLI command `gh` was not installed, so the agent could not create the remote GitHub repository directly from this environment. A parent-workspace `git status` inspection also hit Git's dubious-ownership protection because the broader OneDrive folder is not trusted as a Git repository root. The agent avoided modifying that parent state and instead prepared a fresh standalone local repository under `github-submission/lossfunk-softcot-autoresearch`.

During the first copy, nested `.git` directories from upstream code snapshots were copied into the submission folder. Those nested repositories would make a confusing GitHub submission, so the paths were resolved and verified to be inside the new submission folder before removal. No research result, log, paper, or code file was deleted.

## 2026-06-30 — First checkpoint-copy attempt timed out

While adding the small server-side SoftCoT projection checkpoints to the submission artifact, the first `scp` loop timed out. Seeds 41 and 42 had already copied successfully, but `seed_43/projection.bin` was left as a zero-byte locked partial file. The stale local `scp` and its associated `ssh` process from that transfer were stopped, and seed 43 was retried successfully with a longer timeout and keepalive options. No model training, evaluation, or server-side file modification occurred.
