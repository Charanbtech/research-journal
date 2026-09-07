@echo off
echo Removing Windows Scheduled Task "GitHubActivityPulse"...
schtasks /delete /tn "GitHubActivityPulse" /f
echo Done.
pause
