# 🚀 DevPulse: Continuous AI Research & Code Lab

> Authentic technical research notes, deep learning benchmarks, and algorithms lab for Charan B (@Charanbtech).

---

## 📌 Overview

When deeply engaged in confidential, complex, or long-cycle software and research stages, your public GitHub profile may appear dormant despite continuous work behind the scenes.

**DevPulse** maintains an authentic, living public repository representing your AI & computer science exploration with **natural, human-like activity patterns**:
- **No mechanical 48-hour robot schedules**: Commits occur with organic, randomized intervals (1 to 2.8 days apart).
- **Variable timing**: Commits fire across varying hours of the day rather than an exact fixed minute.
- **Authentic content**: Changes consist of genuine Python tensor operations, segmentation metrics, attention algorithms, and AI research notes.
- **Natural commit messages**: Uses human developer commit formats (e.g. `feat: add causal attention mask helper`, `perf: optimize triangular masking logic`, `notes: add observations on DP-SGD gradient clipping`) without robotic dates or AI tags.

---

## ⚙️ How the Randomization Works

```
GitHub Actions Wakeup (4x Daily: 03:17, 09:17, 15:17, 21:17 UTC)
                    │
                    ▼
     Is randomized wait elapsed? (26 to 68 hrs)
         ┌──────────┴──────────┐
         ▼                     ▼
       [ NO ]                [ YES ]
  (Silent exit)        Random probability check (85%)
                               │
                               ▼
                    Pick natural code/note action
                               │
                               ▼
                    Commit & Push as Charanbtech
                               │
                               ▼
                    Roll new random wait (e.g. 41.2 hrs)
```

- **Cloud-Native**: Runs 100% on GitHub Actions for free. Your computer doesn't need to be kept on or awake.
- **Verified Attribution**: All commits are authored by `Charanbtech <charanbsd25@gmail.com>`.

---

## 🚀 Quick Setup (3 Steps)

### Step 1: Push Repository to GitHub

Create a new repository on your GitHub account (named e.g. `devpulse` or `ai-research-lab`), then run:

```bash
git remote add origin https://github.com/Charanbtech/<REPO-NAME>.git
git push -u origin main
```

---

### Step 2: Grant Workflow Write Permissions

1. In your GitHub repository, open **Settings** (top tab).
2. On the left menu, select **Actions** ➔ **General**.
3. Under **Workflow permissions**, choose **"Read and write permissions"**.
4. Click **Save**.

---

### Step 3: Test First Commit

1. Go to the **Actions** tab in your repository.
2. Select **Activity Pulse** from the left list.
3. Click **Run workflow** ➔ **Run workflow**.
4. The workflow will execute, apply an authentic change, and push. Your profile heatmap will instantly register the activity!

---

## 🖥️ Local Execution (Optional)

If you wish to trigger or test commits locally:

```bash
# Force a commit right now
python scripts/local_runner.py --force

# Check if randomized interval is currently ready
python scripts/generator.py --check-only
```

To register with Windows Task Scheduler:
- Double-click [`scripts/setup_scheduler.bat`](scripts/setup_scheduler.bat).
