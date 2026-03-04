#!/bin/bash
# ============================================================
#  WeldFatigue — One-click launcher (macOS / Linux)
# ============================================================
#  Just double-click this file or run:  ./run.sh
#  It will install Docker if needed, build the app, and open it.
# ============================================================

set -e

APP_NAME="weldfatigue"
PORT=8501
URL="http://localhost:$PORT"

echo ""
echo "  ⚙️  WeldFatigue — OPmobility C-Power"
echo "  ======================================"
echo ""

# ── Check Docker ─────────────────────────────────────────────
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed."
    echo ""
    echo "Please install Docker Desktop first:"
    echo "  👉 https://www.docker.com/products/docker-desktop/"
    echo ""
    echo "After installing, re-run this script."
    exit 1
fi

# Check Docker daemon is running
if ! docker info &> /dev/null 2>&1; then
    echo "⏳ Docker is installed but not running. Starting Docker Desktop..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open -a Docker
    fi
    echo "   Waiting for Docker to start (this may take a moment)..."
    for i in {1..30}; do
        if docker info &> /dev/null 2>&1; then
            break
        fi
        sleep 2
    done
    if ! docker info &> /dev/null 2>&1; then
        echo "❌ Could not start Docker. Please open Docker Desktop manually and re-run."
        exit 1
    fi
    echo "   ✅ Docker is ready."
fi

# ── Build & Run ──────────────────────────────────────────────
cd "$(dirname "$0")"

echo "🔨 Building the application (first time may take a few minutes)..."
docker compose up --build -d

echo ""
echo "✅ WeldFatigue is running!"
echo ""
echo "   Open your browser at:  $URL"
echo ""
echo "   To stop:  docker compose down"
echo ""

# Try to open the browser automatically
sleep 2
if [[ "$OSTYPE" == "darwin"* ]]; then
    open "$URL"
elif command -v xdg-open &> /dev/null; then
    xdg-open "$URL"
fi
