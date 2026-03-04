#!/bin/bash
# ============================================================
#  WeldFatigue — Standalone launcher (macOS / Linux)
#  No Docker required! Works on older Macs.
# ============================================================
#  Just run:  ./run_standalone.sh
#  It will install everything needed automatically.
# ============================================================

set -e

APP_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$APP_DIR/.venv"
PORT=8501
URL="http://localhost:$PORT"
PYTHON_MIN="3.11"

echo ""
echo "  ⚙️  WeldFatigue — OPmobility C-Power"
echo "  ======================================"
echo ""

# ── Helper: compare versions ────────────────────────────────
version_ge() {
    # Returns 0 if $1 >= $2
    printf '%s\n%s' "$2" "$1" | sort -V -C
}

# ── Find a suitable Python (3.11+) ──────────────────────────
find_python() {
    for cmd in python3.12 python3.11 python3 python; do
        if command -v "$cmd" &> /dev/null; then
            ver=$("$cmd" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
            if version_ge "$ver" "$PYTHON_MIN"; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

PYTHON_CMD=$(find_python 2>/dev/null || true)

# ── Install Python if not found ──────────────────────────────
if [ -z "$PYTHON_CMD" ]; then
    echo "📦 Python 3.11+ not found. Installing automatically..."
    echo ""

    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS — use Homebrew
        if ! command -v brew &> /dev/null; then
            echo "📦 Installing Homebrew (macOS package manager)..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

            # Add brew to PATH for Apple Silicon and Intel Macs
            if [ -f /opt/homebrew/bin/brew ]; then
                eval "$(/opt/homebrew/bin/brew shellenv)"
            elif [ -f /usr/local/bin/brew ]; then
                eval "$(/usr/local/bin/brew shellenv)"
            fi
        fi

        echo "📦 Installing Python 3.12 via Homebrew..."
        brew install python@3.12
        PYTHON_CMD=$(find_python)
    else
        # Linux
        if command -v apt-get &> /dev/null; then
            echo "📦 Installing Python 3.12 via apt..."
            sudo apt-get update && sudo apt-get install -y python3.12 python3.12-venv python3-pip
        elif command -v dnf &> /dev/null; then
            echo "📦 Installing Python 3.12 via dnf..."
            sudo dnf install -y python3.12 python3.12-pip
        elif command -v yum &> /dev/null; then
            echo "📦 Installing Python 3.12 via yum..."
            sudo yum install -y python3.12 python3.12-pip
        else
            echo "❌ Could not auto-install Python. Please install Python 3.11+ manually:"
            echo "   https://www.python.org/downloads/"
            exit 1
        fi
        PYTHON_CMD=$(find_python)
    fi

    if [ -z "$PYTHON_CMD" ]; then
        echo "❌ Failed to install Python. Please install Python 3.11+ manually:"
        echo "   https://www.python.org/downloads/"
        exit 1
    fi
    echo "   ✅ Python installed: $($PYTHON_CMD --version)"
fi

echo "🐍 Using: $($PYTHON_CMD --version) ($PYTHON_CMD)"

# ── Create virtual environment (first time only) ────────────
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Setting up virtual environment (first time only)..."
    "$PYTHON_CMD" -m venv "$VENV_DIR"
fi

# Activate venv
source "$VENV_DIR/bin/activate"

# ── Install/update dependencies ──────────────────────────────
# Use a marker file to skip reinstall if requirements haven't changed
REQ_HASH=$(md5sum "$APP_DIR/requirements.txt" 2>/dev/null || md5 -q "$APP_DIR/requirements.txt" 2>/dev/null || echo "none")
MARKER="$VENV_DIR/.req_hash"

if [ ! -f "$MARKER" ] || [ "$(cat "$MARKER" 2>/dev/null)" != "$REQ_HASH" ]; then
    echo "📦 Installing dependencies (this may take a few minutes the first time)..."
    pip install --upgrade pip -q
    pip install -r "$APP_DIR/requirements.txt" -q
    pip install -e "$APP_DIR" -q
    echo "$REQ_HASH" > "$MARKER"
    echo "   ✅ Dependencies installed."
else
    echo "   ✅ Dependencies up to date."
fi

# ── Launch the app ───────────────────────────────────────────
echo ""
echo "🚀 Starting WeldFatigue..."
echo ""
echo "   App will open at:  $URL"
echo "   Press Ctrl+C to stop."
echo ""

# Open browser after a short delay
(sleep 3 && {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open "$URL"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "$URL"
    fi
}) &

# Run Streamlit
cd "$APP_DIR"
streamlit run app/main.py --server.port=$PORT --server.address=localhost
