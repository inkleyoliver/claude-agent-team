#!/usr/bin/env python3
"""Check a domain profile for missing sections, uncited or unrated requirements, old sources and points needing a qualified human.
Usage: python profile.py [expert/domain-profile.md] [--months 6] [--today YYYY-MM-DD]"""
import re, sys, pathlib
from datetime import date
sys.stdout.reconfigure(encoding="utf-8")
a = sys.argv[1:]; months = 6; today = date.today(); path = "expert/domain-profile.md"; i = 0
while i < len(a):
    if a[i] == "--months": months = int(a[i + 1]); i += 2
    elif a[i] == "--today": today = date.fromisoformat(a[i + 1]); i += 2
    else: path = a[i]; i += 1
p = pathlib.Path(path)
if not p.exists(): sys.exit(f"No profile at {path}")
t = p.read_text(encoding="utf-8"); issues = []
def age(d): return (today.year - d.year) * 12 + today.month - d.month
def sec(name):
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", t, re.S | re.M); return m.group(1).strip() if m else None
for s in ("The field in brief", "Why it works the way it does", "What success looks like", "People and their needs", "Rules, standards and obligations", "Key concepts and glossary", "How things go wrong", "What great looks like", "Open questions", "Sources", "Change log"):
    b = sec(s)
    if b is None: issues.append(f"Section missing: {s}")
    elif len(re.sub(r"[|\-\s]", "", b)) < 20: issues.append(f"Section empty or nearly empty: {s}")
m = re.search(r"\*\*Last reviewed:\*\*\s*(\d{4}-\d{2}-\d{2})", t)
if not m: issues.append("No 'Last reviewed' date")
elif age(date.fromisoformat(m.group(1))) > months: issues.append(f"Last reviewed {m.group(1)}: more than {months} months ago")
signoff = []
for row in re.findall(r"^\|(.+)\|\s*$", sec("Rules, standards and obligations") or "", re.M):
    c = [x.strip() for x in row.split("|")]
    if len(c) < 5 or c[0] in ("Requirement", "") or set(c[0]) <= set("-: "): continue
    if not c[1]: issues.append(f"Requirement with no source: {c[0][:60]}")
    if c[3] not in ("High", "Medium", "Low"): issues.append(f"Requirement with no confidence rating: {c[0][:60]}")
    if c[4].lower().startswith("y"): signoff.append(c[0])
src = sec("Sources") or ""; lines = [l for l in src.splitlines() if re.match(r"\s*(\d+[.)]|\[\d+\]|-)\s", l)]
old = 0
for l in lines:
    d = re.findall(r"\d{4}-\d{2}-\d{2}", l)
    if not d: issues.append(f"Source with no 'date checked': {l.strip()[:70]}")
    elif age(date.fromisoformat(d[-1])) > months: old += 1
    if not re.search(r"https?://", l): issues.append(f"Source with no link: {l.strip()[:70]}")
if old: issues.append(f"{old} source(s) last checked more than {months} months ago: check them again")
cited = set(re.findall(r"\[(\d+)\]", t.split("## Sources")[0])); have = set(re.findall(r"^\s*\[?(\d+)[\].)]", src, re.M))
for n in sorted(cited - have, key=int): issues.append(f"Citation [{n}] has no matching source")
print(f"Sources: {len(lines)}   Requirements needing qualified sign-off: {len(signoff)}")
for s in signoff: print(f"   sign-off: {s[:80]}")
print(f"To fix: {len(issues)}"); [print(" -", x) for x in issues]; sys.exit(1 if issues else 0)
