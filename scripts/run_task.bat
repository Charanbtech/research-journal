@echo off
:: Runs the local runner silently
cd /d "%~dp0\.."
python scripts\local_runner.py >> data\task_run.log 2>&1
