#!/bin/bash
# Score one model on the full grid (experiments: PLAN.md §3.8). Usage: bash run.sh <huggingface id> [tag]
set -euo pipefail
MODEL="${1:?huggingface model id}"; TAG="${2:-$(basename "$MODEL" | tr '[:upper:]' '[:lower:]')}"
mkdir -p results/raw
python3 -u scripts/stated_logit.py --model "$MODEL" --out "results/raw/orderforce_${TAG}.jsonl" --pct data/pct_issues.json \
    --grid data/orderforce_grid.json --anchors data/orderforce_anchors.json --include_null
