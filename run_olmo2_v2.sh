#!/bin/bash
# OLMo 2 7B across training stages, v2 (PLAN_OLMO2.md): the seven completion-format runs (base, SFT, DPO, Instruct with
# ending A; the base model with endings B, C, D) on data/olmo2_v2_grid.json, then the gates, the ladder and the
# comparisons. Raw rows in <dir>/raw/, everything else in <dir>/. Revisions, heads and endings are pinned in
# scripts/sweep_models.json ("study": "olmo2_v2"). Resumable: rerun the same command after an interruption.
# Usage: bash run_olmo2_v2.sh [dir, default results/olmo2_v2]
set -euo pipefail
DIR="${1:-results/olmo2_v2}"
if [ -d /workspace ] && [ -z "${HF_HOME:-}" ]; then
    export HF_HOME=/workspace/hf   # RunPod: keep the ~73 GB of weights under /workspace
fi
python3 - <<'EOF'   # PLAN_OLMO2.md §2.5 fixes the software
import torch, transformers
print("transformers", transformers.__version__, "torch", torch.__version__)
if transformers.__version__ != "4.57.6" or tuple(int(x) for x in torch.__version__.split("+")[0].split(".")[:2]) < (2, 6):
    raise SystemExit("PLAN_OLMO2.md needs transformers 4.57.6 and torch >= 2.6: pip install transformers==4.57.6 'torch>=2.6'")
EOF
python3 scripts/olmo2_compare.py --check_prompts   # gates 1-2 and the prompt counts, before any GPU time
mkdir -p "$DIR/raw"
for t in $(python3 scripts/olmo2_compare.py --list); do
    python3 -u scripts/stated_logit.py --tag "$t" --out "$DIR/raw/orderforce_$t.jsonl" --pct data/pct_issues.json \
        --grid data/olmo2_v2_grid.json --anchors data/orderforce_anchors.json --include_null
done
gzip -kf "$DIR"/raw/orderforce_*.jsonl
python3 scripts/orderforce_gates.py --raw "$DIR/raw" --out "$DIR"
python3 scripts/orderforce_analyze.py --raw "$DIR/raw" --out "$DIR"
python3 scripts/olmo2_compare.py --dir "$DIR"
python3 scripts/olmo2_explore.py --dir "$DIR"
