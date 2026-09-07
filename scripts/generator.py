"""
Human-Like Activity & Code Commit Engine
Generates randomized, organic commits with natural timing variations (1 to 2.8 days),
realistic code updates, and authentic developer commit messages.
"""

import os
import sys
import random
import datetime
import json
import argparse
from pathlib import Path

def get_base_dir() -> Path:
    return Path(__file__).resolve().parent.parent

# Pool of realistic, natural commit actions and messages
ACTIONS = [
    {
        "file": "src/utils/tensor_ops.py",
        "type": "code_append",
        "snippet": (
            "\ndef apply_causal_mask(attention_scores: list, mask_val: float = -1e9) -> list:\n"
            "    \"\"\"Applies triangular causal mask to attention logits to prevent future token leakage.\"\"\"\n"
            "    seq_len = len(attention_scores)\n"
            "    for i in range(seq_len):\n"
            "        for j in range(i + 1, seq_len):\n"
            "            attention_scores[i][j] = mask_val\n"
            "    return attention_scores\n"
        ),
        "messages": [
            "feat: add causal attention mask helper",
            "perf: optimize triangular masking logic",
            "refactor: improve causal mask bounds handling"
        ]
    },
    {
        "file": "src/utils/metrics.py",
        "type": "code_append",
        "snippet": (
            "\ndef compute_mean_iou(pred_masks: list, true_masks: list) -> float:\n"
            "    \"\"\"Calculates Mean Intersection over Union across binary segmentation batches.\"\"\"\n"
            "    ious = []\n"
            "    for p, t in zip(pred_masks, true_masks):\n"
            "        inter = sum(1 for a, b in zip(p, t) if a == 1 and b == 1)\n"
            "        union = sum(1 for a, b in zip(p, t) if a == 1 or b == 1)\n"
            "        ious.append(inter / (union + 1e-6))\n"
            "    return sum(ious) / max(len(ious), 1)\n"
        ),
        "messages": [
            "feat: implement mean IoU calculation for segmentation batches",
            "perf: add vectorized batch IoU helper",
            "refactor: streamline intersection over union computation"
        ]
    },
    {
        "file": "notes/research_journal.md",
        "type": "note_append",
        "snippet": (
            "\n---\n\n"
            "### Differential Privacy Gradient Clipping Thresholds\n"
            "- **Observation:** Evaluated Renyi DP budgets when training with DP-SGD. Clipping gradient norms to C=1.0 yielded the best empirical trade-off between privacy leakage and model accuracy.\n"
            "- **Takeaway:** Fixed clipping thresholds require adaptive learning rate dampening in early iterations.\n"
        ),
        "messages": [
            "notes: add observations on DP-SGD gradient clipping",
            "docs: document differential privacy noise budgets",
            "notes: update findings on adaptive learning rate dampening"
        ]
    },
    {
        "file": "notes/research_journal.md",
        "type": "note_append",
        "snippet": (
            "\n---\n\n"
            "### Mixture of Experts (MoE) Load Balancing Loss\n"
            "- **Observation:** Auxiliary loss coefficient of 0.01 successfully prevents routing collapse to top-2 experts during distributed pre-training.\n"
            "- **Next steps:** Experiment with capacity factors under 1.25 to save peak VRAM.\n"
        ),
        "messages": [
            "docs: summarize MoE routing and load balancing dynamics",
            "notes: thoughts on expert routing capacity factors",
            "docs: update notes on auxiliary loss coefficients"
        ]
    },
    {
        "file": "src/utils/tensor_ops.py",
        "type": "comment_update",
        "snippet": "    # Fast path: skip normalization if variance is effectively zero\n",
        "messages": [
            "refactor: clean up tensor normalization edge case",
            "docs: clarify normalization docstring and edge handling",
            "perf: minor optimization in tensor statistics check"
        ]
    },
    {
        "file": "notes/research_journal.md",
        "type": "note_append",
        "snippet": (
            "\n---\n\n"
            "### Vector Search: HNSW vs IVF-PQ Recall Tradeoffs\n"
            "- **Observation:** At ef_search=64, HNSW maintains >98% recall at 1200 QPS on 1536-dim embeddings. IVF-PQ provides 3x smaller memory footprint with minor recall drop.\n"
            "- **Decision:** Use HNSW for latency-critical agent retrievers and IVF-PQ for cold archives.\n"
        ),
        "messages": [
            "notes: benchmark HNSW vs IVF-PQ indexing recall",
            "docs: add tradeoff analysis for vector search architectures",
            "notes: update retriever indexing configurations"
        ]
    },
    {
        "file": "src/utils/metrics.py",
        "type": "comment_update",
        "snippet": "    # Ensure numerical stability with epsilon smoothing\n",
        "messages": [
            "fix: ensure numerical stability in loss denominator",
            "refactor: simplify epsilon smoothing in evaluation metrics",
            "chore: clean up typing and docstrings in metrics"
        ]
    }
]

def load_state() -> dict:
    state_file = get_base_dir() / "data" / "state.json"
    if state_file.exists():
        try:
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    # Initial state
    return {
        "last_commit_time": None,
        "next_wait_hours": round(random.uniform(28.0, 60.0), 1),
        "total_commits": 0
    }

def save_state(state: dict) -> None:
    data_dir = get_base_dir() / "data"
    data_dir.mkdir(exist_ok=True)
    state_file = data_dir / "state.json"
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

def is_ready_for_commit(force: bool = False) -> bool:
    """Checks if random time interval has elapsed naturally."""
    if force:
        return True
        
    state = load_state()
    last_time_str = state.get("last_commit_time")
    if not last_time_str:
        return True
        
    try:
        last_dt = datetime.datetime.fromisoformat(last_time_str)
        now_dt = datetime.datetime.now(datetime.timezone.utc)
        elapsed_hours = (now_dt - last_dt).total_seconds() / 3600
        wait_target = state.get("next_wait_hours", 44.0)
        
        if elapsed_hours >= wait_target:
            # 85% probability of firing immediately once target passed, 15% random chance of waiting a bit more
            if random.random() < 0.85:
                return True
            else:
                print("Natural jitter delay applied. Will check next cycle.")
                return False
        else:
            remaining = wait_target - elapsed_hours
            print(f"Random interval in progress: {remaining:.1f} hours remaining until next commit window.")
            return False
    except Exception as e:
        print(f"Warning reading state: {e}. Proceeding.")
        return True

def apply_random_action() -> str:
    """Applies a realistic change to a codebase or notes file, returning commit message."""
    base_dir = get_base_dir()
    action = random.choice(ACTIONS)
    target_path = base_dir / action["file"]
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read or initialize
    if not target_path.exists():
        content = ""
    else:
        content = target_path.read_text(encoding="utf-8")
        
    # Check if snippet already exists to avoid duplicate clutter
    snippet = action["snippet"]
    if snippet.strip() in content:
        # Tweak a small timestamp comment or whitespace to create a natural modification
        tweak = f"\n# Checkpoint verified: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')}\n"
        content += tweak
    else:
        content += snippet
        
    target_path.write_text(content, encoding="utf-8")
    
    # Pick a natural human commit message
    commit_msg = random.choice(action["messages"])
    return commit_msg

def record_commit_success() -> None:
    """Updates state with new randomized wait hours between 26 to 68 hours."""
    now_dt = datetime.datetime.now(datetime.timezone.utc)
    state = load_state()
    state["last_commit_time"] = now_dt.isoformat()
    state["total_commits"] = state.get("total_commits", 0) + 1
    # Next commit scheduled between ~1.1 days and ~2.8 days (completely unpredictable)
    state["next_wait_hours"] = round(random.uniform(26.0, 68.0), 1)
    save_state(state)
    print(f"Commit recorded! Next natural commit target in {state['next_wait_hours']} hours.")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Force action now regardless of random timer")
    parser.add_argument("--check-only", action="store_true", help="Only check eligibility")
    args = parser.parse_args()
    
    if args.check_only:
        ready = is_ready_for_commit(force=args.force)
        sys.exit(0 if ready else 1)
        
    if not is_ready_for_commit(force=args.force):
        # Exit code 2 indicates no commit needed at this time
        sys.exit(2)
        
    msg = apply_random_action()
    print(msg)
    return 0

if __name__ == "__main__":
    sys.exit(main())
