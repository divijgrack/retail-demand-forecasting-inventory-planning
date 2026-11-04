#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "$0")"
PROJECT_DIR="$(cd -- "$(dirname -- "$SCRIPT_PATH")" && pwd)"
PYTHON="$PROJECT_DIR/.venv/bin/python"

if [[ ! -x "$PYTHON" ]]; then
    echo "Project environment not found. Create it with:"
    echo "  python3 -m venv .venv"
    echo "  .venv/bin/python -m pip install -r requirements-dashboard.txt"
    exit 1
fi

exec "$PYTHON" -m streamlit run "$PROJECT_DIR/src/app.py"
