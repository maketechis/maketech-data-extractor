#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
source .venv/bin/activate
mkdir -p "$ROOT/data"
export DATABASE_URL="sqlite:///$ROOT/data/extractor.db"\nexport ENVIRONMENT="desktop"
(cd backend && python -m alembic upgrade head && uvicorn app.main:app --host 127.0.0.1 --port 8000) &
BACKEND_PID=$!
trap 'kill $BACKEND_PID 2>/dev/null || true' EXIT
cd desktop
npm install
npm run dev
