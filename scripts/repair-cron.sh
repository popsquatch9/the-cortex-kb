#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

LOG_DIR="${CORTEX_LOG_DIR:-$ROOT_DIR/logs}"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/repair-$(date +%F).log"

PYTHON_BIN="${PYTHON_BIN:-python}"

{
  echo "[$(date -Iseconds)] Starting Cortex repair"
  "$PYTHON_BIN" cortex.py repair --json
  echo "[$(date -Iseconds)] Repair finished"
} >>"$LOG_FILE" 2>&1
