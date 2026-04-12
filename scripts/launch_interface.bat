@echo off
REM LENLU AI+ Batch Launcher
REM Windows batch script to launch the PowerShell styled interface

setlocal enabledelayedexpansion

REM Colors setup (requires Windows 10+ for virtual terminal processing)
for /f %%A in ('echo prompt $H ^| cmd') do set "BS=%%A"

cls
echo.
echo.
echo     ╔════════════════════════════════════════════════════════════╗
echo     ║                   LENLU AI+ Launcher                       ║
echo     ║            Advanced Terminal Management System              ║
echo     ╚════════════════════════════════════════════════════════════╝
echo.
echo     Starting PowerShell Interface...
echo.

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"

REM Check if PowerShell is available
where powershell >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo     ERROR: PowerShell not found!
    pause
    exit /b 1
)

REM Check if the PowerShell script exists
if not exist "%SCRIPT_DIR%LENLU_Interface.ps1" (
    echo     ERROR: LENLU_Interface.ps1 not found!
    pause
    exit /b 1
)

REM Launch PowerShell with the interface script
REM Using -ExecutionPolicy Bypass to run without restrictions
powershell.exe -ExecutionPolicy Bypass -NoProfile -File "%SCRIPT_DIR%LENLU_Interface.ps1"

endlocal
