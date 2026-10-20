@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "GRADIO_ANALYTICS_ENABLED=False"
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo [ERROR] No virtual environment. Double-click setup_windows.bat first.
  goto failed
)
".venv\Scripts\python.exe" -c "import gradio, openai, dotenv, PIL" >nul 2>&1
if errorlevel 1 (
  echo [ERROR] Dependencies are missing or damaged. Run setup_windows.bat again.
  goto failed
)
echo [INFO] Starting UniMind. The browser will open when the server is ready.
echo [INFO] Keep this window open while using the website. Press Ctrl+C to stop.
echo [INFO] If the browser does not open, use the local URL printed below.
".venv\Scripts\python.exe" -u app.py
if errorlevel 1 goto failed
exit /b 0

:failed
echo [ERROR] UniMind could not start. Check the error above.
if /i not "%~1"=="--no-pause" pause
exit /b 1