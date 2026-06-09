@echo off
REM Manual push fallback for cmd.exe (no execution-policy issues).
REM Usage:
REM   1) Create the repo at https://github.com/new
REM        Name: STUPIDMEI   Visibility: Public   (no README/gitignore/license)
REM   2) Double-click this file, or run from cmd:  push.bat

cd /d "%~dp0"

git remote get-url origin >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    git remote add origin https://github.com/srqt2/STUPIDMEI.git
)

git push -u origin main
if %ERRORLEVEL% EQU 0 (
    echo.
    echo Pushed. Live at https://github.com/srqt2/STUPIDMEI
) else (
    echo.
    echo Push failed. Make sure you created the repo at github.com/new first.
)
pause
