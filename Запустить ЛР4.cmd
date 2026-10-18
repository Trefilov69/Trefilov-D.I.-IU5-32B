@echo off
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
if not exist "%~dp0.venv\Scripts\python.exe" (
    echo Python environment .venv not found. See README.md for setup.
    pause
    exit /b 1
)
"%~dp0.venv\Scripts\python.exe" "%~dp0main.py" --lab 4
pause
