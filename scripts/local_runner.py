"""
Local Runner for GitHub Activity Automation
Allows running the commit cycle locally, with automatic verification of
Git author email (Charanbtech / charanbsd25@gmail.com) and support for Windows Task Scheduler.
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
import json

TARGET_NAME = "Charanbtech"
TARGET_EMAIL = "charanbsd25@gmail.com"

def get_base_dir() -> Path:
    return Path(__file__).resolve().parent.parent

def run_cmd(cmd_list, cwd=None) -> tuple[int, str]:
    """Runs a shell command and returns (returncode, stdout)."""
    try:
        res = subprocess.run(
            cmd_list,
            cwd=cwd or get_base_dir(),
            capture_output=True,
            text=True,
            check=False
        )
        return res.returncode, res.stdout.strip()
    except Exception as e:
        return 1, str(e)

def ensure_git_config():
    """Sets local repository git author config to ensure correct GitHub attribution."""
    base_dir = get_base_dir()
    run_cmd(["git", "config", "--local", "user.name", TARGET_NAME], cwd=base_dir)
    run_cmd(["git", "config", "--local", "user.email", TARGET_EMAIL], cwd=base_dir)
    print(f"Verified local Git identity: {TARGET_NAME} <{TARGET_EMAIL}>")

def should_commit(force: bool = False) -> bool:
    """Checks if at least 2 days (48 hours) have passed since the last recorded commit."""
    if force:
        return True
        
    telemetry_path = get_base_dir() / "data" / "telemetry.json"
    if not telemetry_path.exists():
        return True
        
    try:
        with open(telemetry_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        last_updated_str = data.get("last_updated")
        if not last_updated_str:
            return True
            
        last_dt = datetime.fromisoformat(last_updated_str)
        now_dt = datetime.now(timezone.utc)
        
        # 48 hours = 2 days interval
        if (now_dt - last_dt) >= timedelta(days=2):
            return True
        else:
            remaining = timedelta(days=2) - (now_dt - last_dt)
            hours = remaining.total_seconds() / 3600
            print(f"Skipping: Last commit was made recently. Next commit eligible in {hours:.1f} hours.")
            return False
    except Exception as e:
        print(f"Warning checking telemetry: {e}. Proceeding with commit.")
        return True

def perform_commit(force_push: bool = True):
    """Generates an entry, stages changes, commits, and pushes."""
    ensure_git_config()
    base_dir = get_base_dir()
    
    # 1. Run generator
    code, commit_msg = run_cmd([sys.executable, str(base_dir / "scripts" / "generator.py")])
    if code != 0 or not commit_msg:
        print(f"Error running generator: {commit_msg}")
        return False
        
    print(f"Generated commit message: {commit_msg}")
    
    # 2. Stage files
    run_cmd(["git", "add", "LOGBOOK.md", "data/telemetry.json"], cwd=base_dir)
    
    # 3. Check for changes
    diff_code, _ = run_cmd(["git", "diff", "--staged", "--quiet"], cwd=base_dir)
    if diff_code == 0:
        print("No staged changes to commit.")
        return True
        
    # 4. Commit
    commit_code, commit_out = run_cmd([
        "git", "commit",
        f"--author={TARGET_NAME} <{TARGET_EMAIL}>",
        "-m", commit_msg
    ], cwd=base_dir)
    
    if commit_code != 0:
        print(f"Git commit failed: {commit_out}")
        return False
        
    print("Git commit successful!")
    
    # 5. Push if remote configured
    if force_push:
        print("Pushing to remote origin...")
        push_code, push_out = run_cmd(["git", "push"], cwd=base_dir)
        if push_code == 0:
            print("Successfully pushed to GitHub! Heatmap will update shortly.")
        else:
            print(f"Push notice (if remote not set yet): {push_out}")
            
    return True

def main():
    parser = argparse.ArgumentParser(description="Local runner for GitHub automated commits.")
    parser.add_argument("--force", action="store_true", help="Force commit now regardless of 2-day timer.")
    parser.add_argument("--no-push", action="store_true", help="Commit locally without pushing.")
    args = parser.parse_args()
    
    if should_commit(force=args.force):
        success = perform_commit(force_push=not args.no_push)
        sys.exit(0 if success else 1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
