# 🚀 DevPulse: Continuous Research & Engineering Journal

> Automated technical checkpoints, AI/ML research notes, and algorithmic discoveries.

[![Auto Activity Pulse](https://github.com/Charanbtech/devpulse/actions/workflows/auto-commit.yml/badge.svg)](https://github.com/Charanbtech)
[![GitHub Streak](https://img.shields.io/badge/Activity-Continuous%20(2--Day%20Interval)-success.svg)](#)
[![Attribution](https://img.shields.io/badge/Author-Charanbtech-blue.svg)](https://github.com/Charanbtech)

---

## 📌 Overview

When working on complex, confidential, or long-cycle software projects, long intervals between production releases can lead to sparse activity on your GitHub profile heatmap.

**DevPulse** solves this elegantly by:
1. Maintaining a live **Research & Engineering Logbook** ([`LOGBOOK.md`](LOGBOOK.md)) and machine-readable telemetry ([`data/telemetry.json`](data/telemetry.json)).
2. Running an automated workflow **every 2 days** in the GitHub cloud (via GitHub Actions) or locally.
3. Writing authentic, curated AI/ML, computer vision, systems, and algorithms notes with conventional commits (`docs(research)`, `feat(algorithms)`, `perf(pipeline)`).

---

## ⚙️ Architecture & Features

- **Cloud-Native Automation (Recommended)**: Runs completely on **GitHub Actions** 24/7. Your computer does **not** need to be on or connected to the internet.
- **Strict Attribution**: Guaranteed author attribution to `Charanbtech` (`charanbsd25@gmail.com`) so GitHub counts every commit toward your profile heatmap and streaks.
- **Local Fallback**: Includes a local Python runner (`scripts/local_runner.py`) and Windows Task Scheduler integration (`scripts/setup_scheduler.bat`).

---

## 🚀 Quick Setup (3 Easy Steps)

### Step 1: Initialize Git and Push to GitHub

Create a new repository on your GitHub account (named e.g. `devpulse` or `research-journal`, can be **Public** or **Private**):

```bash
git init
git branch -M main
git remote add origin https://github.com/Charanbtech/<REPO-NAME>.git
git add .
git commit -m "feat: initialize devpulse activity automator"
git push -u origin main
```

> **Note:** If you make the repository **Private**, make sure your GitHub profile settings have **"Include private contributions on my profile"** enabled (GitHub Settings -> Profile -> Contributions & Activity).

---

### Step 2: Grant GitHub Actions Write Permissions

To allow GitHub Actions to commit and push back to your repository:

1. Open your repository on GitHub.
2. Click **Settings** (tab at the top).
3. In the left sidebar, click **Actions** ➔ **General**.
4. Scroll down to **Workflow permissions**.
5. Select **"Read and write permissions"** and click **Save**.

---

### Step 3: Trigger First Run & Verify

1. Go to the **Actions** tab in your GitHub repository.
2. In the left sidebar, select **Auto Activity Pulse**.
3. Click **Run workflow** ➔ **Run workflow**.
4. Once completed (takes ~20 seconds), check your GitHub profile page to see the new contribution recorded!

---

## 🖥️ Alternative: Running Locally on Windows

If you prefer executing commits directly from your local machine:

1. **Instant Manual Commit:**
   ```bash
   python scripts/local_runner.py --force
   ```
2. **Register Windows Task Scheduler (Runs every 2 days automatically):**
   - Double-click [`scripts/setup_scheduler.bat`](scripts/setup_scheduler.bat) (or run as Administrator).
   - This registers a silent background task `GitHubActivityPulse` that triggers every 2 days at 11:00 AM.
   - To remove the scheduled task anytime: double-click [`scripts/remove_scheduler.bat`](scripts/remove_scheduler.bat).

---

## 📂 Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── auto-commit.yml    # GitHub Actions cron workflow (runs every 2 days)
├── data/
│   └── telemetry.json         # Automated activity metadata & history
├── scripts/
│   ├── generator.py           # Generates curated research entries & commit messages
│   ├── local_runner.py        # Local Python commit & push runner
│   ├── run_task.bat           # Task runner for Windows Task Scheduler
│   ├── setup_scheduler.bat    # 1-click Windows Task Scheduler installer
│   └── remove_scheduler.bat   # Uninstaller for Windows Task Scheduler
├── LOGBOOK.md                 # Markdown engineering journal updated every 2 days
└── README.md                  # Documentation and setup guide
```

---

## 📝 Customization

- **Change Frequency**: Edit [`.github/workflows/auto-commit.yml`](.github/workflows/auto-commit.yml) cron expression.
  - Every 2 days: `cron: '0 14 */2 * *'`
  - Every day: `cron: '0 14 * * *'`
  - Specific days (e.g. Mon, Wed, Fri): `cron: '0 14 * * 1,3,5'`
- **Add Your Own Research Topics**: Add new topics and notes to the `ENTRIES` list inside [`scripts/generator.py`](scripts/generator.py).
