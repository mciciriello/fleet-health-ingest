#!/usr/bin/env bash
set -euo pipefail

BASE="${1:-http://127.0.0.1:8080}"

curl -sS -X POST "$BASE/ingest" \
  -H "Content-Type: application/json" \
  -d '{"host":"navi-01","cpu_pct":12.4,"mem_pct":41.0,"ok":true}'
echo
curl -sS "$BASE/latest?limit=5"
echo
