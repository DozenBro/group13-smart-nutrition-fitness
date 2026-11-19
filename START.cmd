@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo Follow README.md to install project dependencies first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" manage.py run
pause

