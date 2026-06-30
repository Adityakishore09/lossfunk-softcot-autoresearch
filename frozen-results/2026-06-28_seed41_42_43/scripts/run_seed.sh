#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: bash scripts/run_seed.sh SEED [BATCH_SIZE]" >&2
  exit 64
fi

SEED="$1"
BATCH_SIZE=8
if [[ $# -eq 2 ]]; then
  BATCH_SIZE="$2"
fi
if [[ "$BATCH_SIZE" != 1 && "$BATCH_SIZE" != 2 && "$BATCH_SIZE" != 4 && "$BATCH_SIZE" != 8 ]]; then
  echo "BATCH_SIZE must be one of: 1, 2, 4, 8" >&2
  exit 64
fi
MIN_GPU_FREE_MIB=70000
MIN_GPU_FREE_MIB_SOURCE="default"
if (( BATCH_SIZE <= 2 )); then
  MIN_GPU_FREE_MIB=50000
fi
if [[ -n "${MIN_GPU_FREE_MIB_OVERRIDE:-}" ]]; then
  if [[ ! "$MIN_GPU_FREE_MIB_OVERRIDE" =~ ^[0-9]+$ ]]; then
    echo "MIN_GPU_FREE_MIB_OVERRIDE must be a non-negative integer MiB value" >&2
    exit 64
  fi
  MIN_GPU_FREE_MIB="$MIN_GPU_FREE_MIB_OVERRIDE"
  MIN_GPU_FREE_MIB_SOURCE="override"
fi
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PYTHON="${PYTHON:-/data2/anaconda3/envs/softcot/bin/python}"
BASE_MODEL="$ROOT/models/Qwen2.5-7B-Instruct"
ASSISTANT_MODEL="$ROOT/models/Qwen2.5-1.5B-Instruct"
RESULT_ROOT="$ROOT/results/raw/seed_$SEED"
TRAIN_NAME="gsm8k-source-seed-$SEED"
CHECKPOINT="$ROOT/ckpt/$TRAIN_NAME-gsm8k-10.0-32-Qwen2.5-7B-Instruct-Qwen2.5-1.5B-Instruct/projection.bin"

for required in "$PYTHON" "$BASE_MODEL/config.json" "$ASSISTANT_MODEL/config.json" \
  "$ROOT/data/fixed/manifest.json" "$ROOT/data/gsm8k/train_socratic.jsonl"; do
  if [[ ! -e "$required" ]]; then
    echo "Missing required path: $required" >&2
    exit 66
  fi
done

if [[ -e "$RESULT_ROOT" ]]; then
  echo "Refusing to overwrite existing result directory: $RESULT_ROOT" >&2
  exit 73
fi

GPU_UTILIZATION="$(nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits | head -n 1 | tr -d '[:space:]')"
GPU_MEMORY_FREE="$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits | head -n 1 | tr -d '[:space:]')"
GPU_CONTENTION="idle"
if (( GPU_UTILIZATION > 10 )); then
  GPU_CONTENTION="contended"
  echo "Warning: GPU utilization is $GPU_UTILIZATION%; proceeding under user-authorized contended-GPU protocol." >&2
fi
if (( GPU_MEMORY_FREE < MIN_GPU_FREE_MIB )); then
  echo "GPU memory is insufficient: free_memory=$GPU_MEMORY_FREE MiB; need at least $MIN_GPU_FREE_MIB MiB free." >&2
  exit 75
fi

mkdir -p "$RESULT_ROOT"
nvidia-smi --query-gpu=index,name,memory.total,memory.used,utilization.gpu,driver_version --format=csv,noheader \
  > "$RESULT_ROOT/gpu_before.csv"
printf 'seed=%s\nbatch_size=%s\nmin_gpu_free_mib=%s\nmin_gpu_free_mib_source=%s\ngpu_utilization_before_percent=%s\ngpu_memory_free_before_mib=%s\ngpu_contention=%s\n' "$SEED" "$BATCH_SIZE" "$MIN_GPU_FREE_MIB" "$MIN_GPU_FREE_MIB_SOURCE" "$GPU_UTILIZATION" "$GPU_MEMORY_FREE" "$GPU_CONTENTION" \
  > "$RESULT_ROOT/run_config.txt"

cd "$ROOT"
export CUDA_VISIBLE_DEVICES=0
export PYTHONUNBUFFERED=1

"$PYTHON" train_softcot.py \
  --large_model_id "$BASE_MODEL" \
  --small_model_id "$ASSISTANT_MODEL" \
  --output_name "$TRAIN_NAME" \
  --batch_size "$BATCH_SIZE" \
  --task_name gsm8k \
  --num_thought_tokens 32 \
  --n_epochs 10 \
  --data_dir "$ROOT/data/gsm8k" \
  --seed "$SEED" \
  2>&1 | tee "$RESULT_ROOT/train.log"

if [[ ! -f "$CHECKPOINT" ]]; then
  echo "Expected source-trained checkpoint was not created: $CHECKPOINT" >&2
  exit 1
fi

run_evaluation() {
  local task_name="$1"
  local test_file="$2"
  local condition="$3"
  local thought_tokens="$4"
  local params_file="$5"
  local soft_control="learned"
  local label="$task_name""_""$condition"
  local result_file="$RESULT_ROOT/$label.json"

  if [[ "$condition" == "zero" ]]; then
    soft_control="zero"
  fi

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
