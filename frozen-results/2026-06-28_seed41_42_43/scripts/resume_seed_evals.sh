#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/resume_seed_evals.sh SEED [MIN_GPU_FREE_MIB]" >&2
  exit 64
fi

SEED="$1"
MIN_GPU_FREE_MIB="${2:-50000}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON="${PYTHON:-/data2/anaconda3/envs/softcot/bin/python}"
BASE_MODEL="$ROOT/models/Qwen2.5-7B-Instruct"
ASSISTANT_MODEL="$ROOT/models/Qwen2.5-1.5B-Instruct"
RESULT_ROOT="$ROOT/results/raw/seed_$SEED"
TRAIN_NAME="gsm8k-source-seed-$SEED"
CHECKPOINT="$ROOT/ckpt/$TRAIN_NAME-gsm8k-10.0-32-Qwen2.5-7B-Instruct-Qwen2.5-1.5B-Instruct/projection.bin"

for required in "$PYTHON" "$BASE_MODEL/config.json" "$ASSISTANT_MODEL/config.json" \
  "$ROOT/data/fixed/manifest.json" "$RESULT_ROOT/run_config.txt" "$CHECKPOINT"; do
  if [[ ! -e "$required" ]]; then
    echo "Missing required path: $required" >&2
    exit 66
  fi
done

GPU_UTILIZATION="$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -n 1 | tr -d '[:space:]')"
GPU_MEMORY_FREE="$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -n 1 | tr -d '[:space:]')"
if (( GPU_UTILIZATION > 10 )); then
  echo "Warning: GPU utilization is $GPU_UTILIZATION%; proceeding under user-authorized contended-GPU protocol." >&2
fi
if (( GPU_MEMORY_FREE < MIN_GPU_FREE_MIB )); then
  echo "GPU memory is insufficient for eval resume: free_memory=$GPU_MEMORY_FREE MiB; need at least $MIN_GPU_FREE_MIB MiB free." >&2
  exit 75
fi

cd "$ROOT"
export CUDA_VISIBLE_DEVICES=0
export PYTHONUNBUFFERED=1

archive_stale_log_if_needed() {
  local label="$1"
  local result_file="$RESULT_ROOT/$label.json"
  local log_file="$RESULT_ROOT/$label.log"

  if [[ ! -f "$result_file" && -f "$log_file" ]]; then
    local stamp
    stamp="$(date +%Y-%m-%d_%H%M%S)"
    local archive_dir="$ROOT/failures/seed_${SEED}_eval_resume_${stamp}"
    mkdir -p "$archive_dir"
    mv "$log_file" "$archive_dir/$label.log"
    echo "Archived stale incomplete log to $archive_dir/$label.log" >&2
  fi
}

run_evaluation() {
  local task_name="$1"
  local test_file="$2"
  local condition="$3"
  local thought_tokens="$4"
  local params_file="$5"
  local soft_control="learned"
  local label="$task_name""_""$condition"
  local result_file="$RESULT_ROOT/$label.json"

  if [[ -f "$result_file" ]]; then
    echo "Skipping existing completed result: $result_file" >&2
    return 0
  fi

  if [[ "$condition" == "zero" ]]; then
    soft_control="zero"
  fi

  archive_stale_log_if_needed "$label"

  "$PYTHON" evaluate_softcot.py \
    --base_model_id "$BASE_MODEL" \
    --assistant_model_id "$ASSISTANT_MODEL" \
    --params_file_name "$params_file" \
    --num_thought_tokens "$thought_tokens" \
    --num_return_sequences 1 \
    --task_name "$task_name" \
    --test_file "$test_file" \
    --seed "$SEED" \
    --soft_thought_control "$soft_control" \
    --max_new_tokens 512 \
    --results_file "$result_file" \
    2>&1 | tee "$RESULT_ROOT/$label.log"
}

for task_and_file in \
  "gsm8k:$ROOT/data/fixed/gsm8k_source_test.jsonl" \
  "asdiv-aug:$ROOT/data/fixed/asdiv_aug_target_test.jsonl" \
  "strategyqa:$ROOT/data/fixed/strategyqa_target_dev.jsonl"; do
  TASK="$(printf '%s' "$task_and_file" | cut -d: -f1)"
  FILE="$(printf '%s' "$task_and_file" | cut -d: -f2-)"
  run_evaluation "$TASK" "$FILE" learned 4 "$CHECKPOINT"
  run_evaluation "$TASK" "$FILE" zero 4 "$CHECKPOINT"
  run_evaluation "$TASK" "$FILE" baseline 0 None
done

nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu,driver_version --format=csv,noheader \
  > "$RESULT_ROOT/gpu_after.csv"
sha256sum "$CHECKPOINT" "$RESULT_ROOT"/*.json > "$RESULT_ROOT/checksums.sha256"
