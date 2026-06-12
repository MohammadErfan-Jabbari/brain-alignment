#!/usr/bin/env bash
# I1 — launch the E015 expansion across 4 L40S, size-balanced (heavies spread). Each shard runs its
# models sequentially (load/free), so peak GPU mem ~= the largest single fp32 model (<31GB < 46GB).
set -u
cd /home/centcom/data/brain-alignment
export HF_HOME=/home/centcom/data/hf-cache HF_HUB_OFFLINE=1
OUT=outputs/E015_expand; mkdir -p $OUT

declare -a S0=(mistralai/Mistral-7B-v0.1 facebook/opt-6.7b Qwen/Qwen2.5-7B)
declare -a S1=(Qwen/Qwen2.5-3B facebook/opt-2.7b EleutherAI/pythia-2.8b meta-llama/Llama-3.2-3B)
declare -a S2=(gpt2-large gpt2-medium gpt2 distilgpt2 Qwen/Qwen2.5-1.5B EleutherAI/pythia-1.4b)
declare -a S3=(EleutherAI/pythia-70m EleutherAI/pythia-160m EleutherAI/pythia-410m EleutherAI/pythia-1b \
               facebook/opt-125m facebook/opt-350m facebook/opt-1.3b Qwen/Qwen2.5-0.5B meta-llama/Llama-3.2-1B)

for g in 0 1 2 3; do
  declare -n arr=S$g
  CUDA_VISIBLE_DEVICES=$g uv run python scripts/run_ppl_alignment_law_expand.py \
    --models "${arr[@]}" --out $OUT/shard_$g.json > $OUT/run_shard_$g.log 2>&1 &
  echo "shard $g (GPU $g, ${#arr[@]} models) PID $!"
done
wait
echo "=== ALL SHARDS DONE $(date +%T) ==="
