@echo off
rem run_keepalive.bat
rem Starts the keepAlive program in a new terminal window using the repository .venv

setlocal
set SCRIPT_DIR=%~dp0

rem Ensure trailing backslash is present
if not "%SCRIPT_DIR:~-1%"=="\" set SCRIPT_DIR=%SCRIPT_DIR%\

rem Prefer the virtual environment Python
if exist "%SCRIPT_DIR%.venv\Scripts\python.exe" (
    start "keepAlive" cmd /k ""%SCRIPT_DIR%.venv\Scripts\python.exe" "%SCRIPT_DIR%keepAlive.py" %*"
    goto :eof
)

rem If venv is missing but an exe exists, offer to run the exe
if exist "%SCRIPT_DIR%dist\keepAlive.exe" (
    echo Virtual environment not found, but packed exe exists. Starting exe...
    start "keepAlive" "%SCRIPT_DIR%dist\keepAlive.exe" %*
    goto :eof
)

rem If keepAlive.py exists but venv is missing, instruct user how to create venv
if exist "%SCRIPT_DIR%keepAlive.py" (
    echo Virtual environment (.venv) not found in "%SCRIPT_DIR%"
    echo To create and use the venv, run these commands in PowerShell from the project folder:
    echo.
    echo    python -m venv .venv
    echo    .\.venv\Scripts\Activate.ps1
    echo    pip install -r requirements.txt
    echo.
    echo Press any key to attempt to run keepAlive.py with the system python (fallback), or Ctrl+C to cancel.
    pause >nul
    if exist "%SYSTEMROOT%\system32\cmd.exe" (
        start "keepAlive" cmd /k "python "%SCRIPT_DIR%keepAlive.py" %*"
    ) else (
        echo Could not find cmd.exe to launch fallback. Exiting.
    )
    goto :eof
)

echo Could not find keepAlive.py or dist\keepAlive.exe in %SCRIPT_DIR%
echo Please check you are running this from the repository root.
pause
