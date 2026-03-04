@echo off
REM ============================================================
REM  WeldFatigue — One-click launcher (Windows)
REM ============================================================
REM  Double-click this file to start the app.
REM ============================================================

echo.
echo   WeldFatigue — OPmobility C-Power
echo   ======================================
echo.

REM ── Check Docker ───────────────────────────────────────────
where docker >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed.
    echo.
    echo Please install Docker Desktop first:
    echo   https://www.docker.com/products/docker-desktop/
    echo.
    echo After installing, re-run this script.
    pause
    exit /b 1
)

REM ── Check Docker is running ────────────────────────────────
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is installed but not running.
    echo Please open Docker Desktop and wait for it to start, then re-run this script.
    pause
    exit /b 1
)

REM ── Build & Run ────────────────────────────────────────────
cd /d "%~dp0"

echo Building the application (first time may take a few minutes)...
docker compose up --build -d

echo.
echo WeldFatigue is running!
echo.
echo   Open your browser at:  http://localhost:8501
echo.
echo   To stop:  docker compose down
echo.

timeout /t 3 >nul
start http://localhost:8501

pause
