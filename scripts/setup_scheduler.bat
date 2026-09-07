@echo off
setlocal
echo ======================================================
echo  Setting up Windows Scheduled Task: GitHubActivityPulse
echo  Frequency: Every 2 Days
echo ======================================================

set SCRIPT_PATH=%~dp0run_task.bat

:: Create scheduled task running every 2 days at 11:00 AM
schtasks /create /tn "GitHubActivityPulse" /tr "\"%SCRIPT_PATH%\"" /sc daily /mo 2 /st 11:00 /f

if %errorlevel% equ 0 (
    echo.
    echo [SUCCESS] Task "GitHubActivityPulse" registered successfully!
    echo It will run automatically every 2 days at 11:00 AM.
) else (
    echo.
    echo [NOTE] If permission denied, please right-click this script and select "Run as Administrator".
)

pause
