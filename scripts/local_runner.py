"""
Local Runner for GitHub Activity Automation
Allows running the commit cycle locally with randomized timing variations
and strict author attribution to Charanbtech <charanbsd25@gmail.com>.
"""

import sys
import subprocess
import argparse
import random
from pathlib import Path

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

def perform_single_commit(force: bool = False) -> tuple[bool, str]:
    base_dir = get_base_dir()
    gen_script = base_dir / "scripts" / "generator.py"
    
    cmd = [sys.executable, str(gen_script)]
    if force:
        cmd.append("--force")
        
    code, out = run_cmd(cmd)
    if code == 2:
        print(f"Timing check: {out}")
        return False, "Not ready yet"
    elif code != 0:
        print(f"Error from generator: {out}")
        return False, out
        
    commit_msg = out.strip()
    print(f"Applying change with message: '{commit_msg}'")
    
    # Stage relevant source files and data
    run_cmd(["git", "add", "-A"], cwd=base_dir)
    
    diff_code, _ = run_cmd(["git", "diff", "--staged", "--quiet"], cwd=base_dir)
    if diff_code == 0:
        print("No staged changes detected.")
        return False, "No changes"
        
    # Commit with explicit author
    c_code, c_out = run_cmd([
        "git", "commit",
        f"--author={TARGET_NAME} <{TARGET_EMAIL}>",
        "-m", commit_msg
    ], cwd=base_dir)
    
    if c_code != 0:
        print(f"Git commit failed: {c_out}")
        return False, c_out
        
    # Update state file with new randomized wait interval
    update_code, _ = run_cmd([
        sys.executable, "-c",
        "import sys; sys.path.insert(0, 'scripts'); import generator; generator.record_commit_success()"
    ], cwd=base_dir)
    
    return True, commit_msg

def main():
    parser = argparse.ArgumentParser(description="Organic commit runner for GitHub profile.")
    parser.add_argument("--force", action="store_true", help="Force commit now regardless of random timer.")
    parser.add_argument("--no-push", action="store_true", help="Commit locally without pushing.")
    args = parser.parse_args()
    
    ensure_git_config()
    base_dir = get_base_dir()
    
    success, msg = perform_single_commit(force=args.force)
    if not success:
        sys.exit(0)
        
    # Natural human session burst: 25% chance of making a second small follow-up commit
    if not args.force and random.random() < 0.25:
        print("Simulating follow-up dev commit in this session...")
        perform_single_commit(force=True)
        
    if not args.no_push:
        print("Pushing to remote repository...")
        push_code, push_out = run_cmd(["git", "push"], cwd=base_dir)
        if push_code == 0:
            print("Successfully pushed to GitHub! Contributions updated naturally.")
        else:
            print(f"Push response: {push_out}")
            
    sys.exit(0)

if __name__ == "__main__":
    main()
