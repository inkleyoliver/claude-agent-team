#!/usr/bin/env python3
"""Read approvals/approvals-log.md and list decisions that are awaiting an answer, expired, or due for review soon.
Read only. Exit 1 if anything is awaiting or expired.
Usage: python approvals.py [path/to/approvals-log.md] [--soon 14] [--today YYYY-MM-DD]"""
import re, sys, pathlib, subprocess
from datetime import date, timedelta
sys.stdout.reconfigure(encoding="utf-8")
a = sys.argv[1:]; soon = 14; today = date.today(); path = "approvals/approvals-log.md"
i = 0
while i < len(a):
    if a[i] == "--soon": soon = int(a[i + 1]); i += 2
    elif a[i] == "--today": today = date.fromisoformat(a[i + 1]); i += 2
    else: path = a[i]; i += 1
p = pathlib.Path(path)
if not p.exists(): print(f"No approvals log at {path}. Nothing has been approved in this project."); sys.exit(1)
rows = []
for line in p.read_text(encoding="utf-8").splitlines():
    c = [x.strip() for x in line.strip().strip("|").split("|")]
    if len(c) >= 7 and re.fullmatch(r"D\d+", c[0]): rows.append(c)
awaiting, expired, due, nodate, notappr, ok = [], [], [], [], [], 0
seen = {}
for c in rows: seen[c[0]] = seen.get(c[0], 0) + 1
dups = [f"{k} appears {n} times" for k, n in seen.items() if n > 1]
for c in rows:
    did, when, what, gate, status, who, exp = c[:7]
    m = re.search(r"\d{4}-\d{2}-\d{2}", exp); d = date.fromisoformat(m.group(0)) if m else None
    if "Awaiting" in status: awaiting.append(f"{did}: {what} (asked {when})")
    elif re.search(r"(?i)\bnot[ -]+approved\b", status): notappr.append(f"{did}: {what} (status says Not approved)")
    elif re.search(r"(?<!Not )\bApproved\b", status):
        if d and d < today: expired.append(f"{did}: {what} (expired {d}; a new decision is needed)")
        elif d and d <= today + timedelta(days=soon): due.append(f"{did}: {what} (review by {d})")
        elif not d and re.search(r"(?i)risk|accept|defer|exception", what): nodate.append(f"{did}: {what}")
        else: ok += 1
    elif "Expired" in status: expired.append(f"{did}: {what} (marked expired)")
print(f"Decisions in the log: {len(rows)}   Approved and in date: {ok}   Checked on {today}")
warn = ""
try:
    r = subprocess.run(["git", "status", "--porcelain", "--", "."], capture_output=True, text=True, cwd=str(p.resolve().parent), timeout=20)
    if r.returncode == 0 and r.stdout.strip(): warn = "WARNING: the approvals folder has uncommitted changes. Check the log was not edited without a commit."
except Exception: pass
if warn: print(warn)
for title, items in (("Not approved (do not treat as approved)", notappr), ("Duplicate decision IDs (log may have been edited)", dups), ("Awaiting a human decision (not approved)", awaiting), ("Expired (no longer an approval)", expired), (f"Review due within {soon} days", due), ("Risk decisions with no expiry or review date", nodate)):
    if items: print(f"\n{title}:"); [print(" -", x) for x in items]
sys.exit(1 if awaiting or expired or dups or warn else 0)
