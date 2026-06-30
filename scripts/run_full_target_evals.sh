#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/run_full_target_evals.sh SEED [MIN_GPU_FREE_MIB]" >&2
  echo "Optional env: TASKS='strategyqa asdiv-aug' CONDITIONS='learned baseline zero'" >&2
  exit 64
fi

SEED="$1"
MIN_GPU_FREE_MIB="${2:-30000}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON="${PYTHON:-/data2/anaconda3/envs/softcot/bin/python}"
BASE_MODEL="$ROOT/models/Qwen2.5-7B-Instruct"
ASSISTANT_MODEL="$ROOT/models/Qwen2.5-1.5B-Instruct"
RESULT_ROOT="$ROOT/results/full_target/seed_$SEED"
TRAIN_NAME="gsm8k-source-seed-$SEED"
CHECKPOINT="$ROOT/ckpt/$TRAIN_NAME-gsm8k-10.0-32-Qwen2.5-7B-Instruct-Qwen2.5-1.5B-Instruct/projection.bin"
TASKS="${TASKS:-strategyqa asdiv-aug}"
CONDITIONS="${CONDITIONS:-learned baseline}"

for required in "$PYTHON" "$BASE_MODEL/config.json" "$ASSISTANT_MODEL/config.json" \
  "$CHECKPOINT" "$ROOT/data/external/asdiv-aug-test.jsonl" "$ROOT/data/external/strategyqa-dev.json"; do
  if [[ ! -e "$required" ]]; then
    echo "Missing required path: $required" >&2
    exit 66
  fi
done

GPU_UTILIZATION="$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -n 1 | tr -d '[:space:]')"
GPU_MEMORY_FREE="$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -n 1 | tr -d '[:space:]')"
if (( GPU_UTILIZATION > 10 )); then
  echo "Warning: GPU utilization is $GPU_UTILIZATION%; proceeding under user-authorized contended/full-target protocol." >&2
fi
if (( GPU_MEMORY_FREE < MIN_GPU_FREE_MIB )); then
  echo "GPU memory is insufficient for full-target eval: free_memory=$GPU_MEMORY_FREE MiB; need at least $MIN_GPU_FREE_MIB MiB free." >&2
  exit 75
fi

mkdir -p "$RESULT_ROOT"
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu,driver_version --format=csv,noheader \
  > "$RESULT_ROOT/gpu_before.csv"
printf 'seed=%s\nmin_gpu_free_mib=%s\ngpu_utilization_before_percent=%s\ngpu_memory_free_before_mib=%s\ntasks=%s\nconditions=%s\n' \
  "$SEED" "$MIN_GPU_FREE_MIB" "$GPU_UTILIZATION" "$GPU_MEMORY_FREE" "$TASKS" "$CONDITIONS" \
  > "$RESULT_ROOT/run_config.txt"

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
    local archive_dir="$ROOT/failures/full_target_seed_${SEED}_${stamp}"
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

task_file() {
  case "$1" in
    strategyqa) printf '%s\n' "$ROOT/data/external/strategyqa-dev.json" ;;
    asdiv-aug) printf '%s\n' "$ROOT/data/external/asdiv-aug-test.jsonl" ;;
    *) echo "Unsupported full-target task: $1" >&2; exit 64 ;;
  esac
}

for task_name in $TASKS; do
  file="$(task_file "$task_name")"
  for condition in $CONDITIONS; do
    case "$condition" in
      learned) run_evaluation "$task_name" "$file" learned 4 "$CHECKPOINT" ;;
      zero) run_evaluation "$task_name" "$file" zero 4 "$CHECKPOINT" ;;
      baseline) run_evaluation "$task_name" "$file" baseline 0 None ;;
      *) echo "Unsupported full-target condition: $condition" >&2; exit 64 ;;
    esac
  done
done

nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu,driver_version --format=csv,noheader \
  > "$RESULT_ROOT/gpu_after.csv"
sha256sum "$CHECKPOINT" "$RESULT_ROOT"/*.json > "$RESULT_ROOT/checksums.sha256"
