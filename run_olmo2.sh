#!/bin/bash
# Score the four OLMo 2 7B training stages (base, SFT, DPO, Instruct = RLVR) on the full grid and compare them, apart from
# the 19-model panel: raw rows in <dir>/raw/, gates, ladder and the paired stage comparison in <dir>/. Revisions and the
# base model's chat template are pinned in scripts/sweep_models.json. Resumable: rerun the same command after an interruption.
# Usage: bash run_olmo2.sh [dir, default results/olmo2]
set -euo pipefail
DIR="${1:-results/olmo2}"
if [ -d /workspace ] && [ -z "${HF_HOME:-}" ]; then
    export HF_HOME=/workspace/hf   # RunPod: keep the ~73 GB of weights on the volume, not the container disk
fi
python3 scripts/olmo2_compare.py --check_prompts   # stop before any GPU time if the stages would not see identical prompts
for s in $(python3 scripts/olmo2_compare.py --list); do
    RAW_DIR="$DIR/raw" bash run.sh "${s%:*}" "${s##*:}"
done
gzip -kf "$DIR"/raw/orderforce_*.jsonl
python3 scripts/orderforce_gates.py --raw "$DIR/raw" --out "$DIR"
python3 scripts/orderforce_analyze.py --raw "$DIR/raw" --out "$DIR"
python3 scripts/olmo2_compare.py --dir "$DIR"
