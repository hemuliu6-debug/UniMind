@echo off
setlocal
chcp 65001 >nul
set "PYTHONUTF8=1"
set "PYTHONIOENCODING=utf-8"
set "PIP_DISABLE_PIP_VERSION_CHECK=1"
set "PIP_PROGRESS_BAR=off"
set "GRADIO_ANALYTICS_ENABLED=False"
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" goto check_venv

rem Find a 64-bit Python 3.13 even when py.exe is missing from PATH.
set "UNIMIND_PYTHON="
set "UNIMIND_PYTHON_ARGS="
call :try_python "%LOCALAPPDATA%\Programs\Python\Python313\python.exe"
if defined UNIMIND_PYTHON goto create_venv
call :try_python "%ProgramFiles%\Python313\python.exe"
if defined UNIMIND_PYTHON goto create_venv
call :try_launcher "%LOCALAPPDATA%\Programs\Python\Launcher\py.exe"
if defined UNIMIND_PYTHON goto create_venv
call :try_launcher "%SystemRoot%\py.exe"
if defined UNIMIND_PYTHON goto create_venv
where py >nul 2>&1
if not errorlevel 1 call :try_launcher "py"
if defined UNIMIND_PYTHON goto create_venv
where python >nul 2>&1
if not errorlevel 1 call :try_python "python"
if defined UNIMIND_PYTHON goto create_venv

echo [ERROR] Python 3.13 64-bit was not found.
echo Install Python 3.13 using the Windows installer ^(64-bit^), then run this file again.
goto failed

:create_venv
echo [INFO] Creating environment with "%UNIMIND_PYTHON%" %UNIMIND_PYTHON_ARGS%
"%UNIMIND_PYTHON%" %UNIMIND_PYTHON_ARGS% -m venv .venv
if errorlevel 1 (
  echo [ERROR] Could not create the virtual environment.
  goto failed
)

:check_venv
".venv\Scripts\python.exe" -c "import sys, struct; print('Python:', sys.version.split()[0], '|', struct.calcsize('P') * 8, 'bit'); sys.exit(0 if sys.version_info[:2] == (3, 13) and struct.calcsize('P') == 8 else 1)"
if errorlevel 1 (
  echo [ERROR] The existing .venv is not a working 64-bit Python 3.13 environment.
  echo Rename .venv to .venv-old and run setup_windows.bat again.
  goto failed
)

echo [INFO] Installing project dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
  echo [ERROR] Dependency installation failed. Check the network and the error above.
  goto failed
)
if not exist ".env" copy ".env.example" ".env" >nul
if not exist ".env" (
  echo [ERROR] Could not create .env. Check that .env.example exists.
  goto failed
)
echo [INFO] Running offline tests...
".venv\Scripts\python.exe" -m unittest discover -s tests -v
if errorlevel 1 (
  echo [ERROR] Tests failed. See the error above.
  goto failed
)
echo.
echo [OK] Setup completed. Double-click start_windows.bat to open UniMind.
if /i not "%~1"=="--no-pause" pause
exit /b 0

:failed
if /i not "%~1"=="--no-pause" pause
exit /b 1

:try_python
"%~1" -c "import sys, struct; sys.exit(0 if sys.version_info[:2] == (3, 13) and struct.calcsize('P') == 8 else 1)" >nul 2>&1
if errorlevel 1 exit /b 0
set "UNIMIND_PYTHON=%~1"
set "UNIMIND_PYTHON_ARGS="
exit /b 0

:try_launcher
"%~1" -3.13 -c "import sys, struct; sys.exit(0 if sys.version_info[:2] == (3, 13) and struct.calcsize('P') == 8 else 1)" >nul 2>&1
if errorlevel 1 exit /b 0
set "UNIMIND_PYTHON=%~1"
set "UNIMIND_PYTHON_ARGS=-3.13"
exit /b 0