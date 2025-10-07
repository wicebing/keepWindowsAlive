<#
build_exe.ps1

Simple PowerShell script to build a single-file exe using PyInstaller.
Usage: run in repository root: .\build_exe.ps1
#>

param()

# Ensure script runs from repository root
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptPath

Write-Host "Creating virtual environment (optional) and installing requirements if missing..."
if (-not (Get-Command pyinstaller -ErrorAction SilentlyContinue)) {
    Write-Host "PyInstaller not found on PATH. Installing into .venv..."
    if (-not (Test-Path .venv)) {
        python -m venv .venv
    }
    .\.venv\Scripts\Activate.ps1; pip install --upgrade pip; pip install -r requirements.txt
    Remove-Item Env:\PYTHONHOME -ErrorAction SilentlyContinue -Force
}

# Build with PyInstaller: single-file, console (so logs visible)
Write-Host "Building keepAlive.exe with PyInstaller..."
pyinstaller --onefile --name keepAlive keepAlive.py --clean

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build finished. Output: dist\keepAlive.exe"
} else {
    Write-Host "Build failed with exit code $LASTEXITCODE"
}