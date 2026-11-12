#!/usr/bin/env python3
"""Create and track feature files so IDs are never reused and the register matches the files.
  python features.py new "Export attendance list" [--type new|upgrade] [--of "existing feature"] [--source FB-3]
  python features.py status          -> every feature and its stage, with anything out of step
Run from the project root. Writes only inside features/."""
import argparse, re, sys, pathlib
from datetime import date
sys.stdout.reconfigure(encoding="utf-8")
D = pathlib.Path("features"); REG = D / "register.md"
HEAD = "# Feature register\n\n| ID | Feature | Type | Source | Stage | Decision | Stories | Last changed |\n|----|---------|------|--------|-------|----------|---------|--------------|\n"
TEMPLATE = """# {id}: {title}
**Stage:** Intake
**Type:** {type}  **Source:** {source}  **Last changed:** {today}

## Brief
**Problem:**
**Outcome:**
**Users and access:**
**Data:**
**In scope (first version):**
**Out of scope / later:**
**What must not change:**
**Constraints:**
**Confirmed by the user:** not yet

## Questions and answers
| # | Question | Answer | Date |
|---|----------|--------|------|

## Security design input
**From:**
**Architecture changes:**
**Security requirements for the build:**
**Threat model:**

## Plan
**Summary:**

| Slice | What it delivers | Agents | Depends on | Size (S / M / L) |
|-------|------------------|--------|------------|------------------|

**Acceptance criteria:**
**Proof:**
**Risks and open decisions:**
**Route and rough budget:**

## Approval and backlog
**Decision:** not yet requested  **Stories:** none yet
"""
def files(): return sorted(D.glob("FT-*.md"))
def num(p): return int(re.match(r"FT-(\d+)", p.name).group(1))
p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
n = sub.add_parser("new"); n.add_argument("title"); n.add_argument("--type", choices=["new", "upgrade"], default="new"); n.add_argument("--of"); n.add_argument("--source", default="User request")
sub.add_parser("status"); x = p.parse_args()
if x.cmd == "new":
    D.mkdir(exist_ok=True)
    used = [num(f) for f in files()] + [int(m) for m in re.findall(r"\|\s*FT-(\d+)", REG.read_text(encoding="utf-8"))] if REG.exists() else [num(f) for f in files()]
    fid = f"FT-{max(used, default=0) + 1:03d}"; slug = re.sub(r"[^a-z0-9]+", "-", x.title.lower()).strip("-")[:40]
    typ = "New feature" if x.type == "new" else f"Upgrade to {x.of or '<existing feature>'}"; today = date.today().isoformat()
    f = D / f"{fid}-{slug}.md"; f.write_text(TEMPLATE.format(id=fid, title=x.title, type=typ, source=x.source, today=today), encoding="utf-8")
    if not REG.exists(): REG.write_text(HEAD, encoding="utf-8")
    with REG.open("a", encoding="utf-8") as r: r.write(f"| {fid} | {x.title} | {typ} | {x.source} | Intake | | | {today} |\n")
    print(f"Created {f} and added {fid} to {REG}")
else:
    reg = {m.group(1): [c.strip() for c in m.group(0).strip("|").split("|")] for m in re.finditer(r"^\|\s*(FT-\d+)\s*\|.*$", REG.read_text(encoding="utf-8") if REG.exists() else "", re.M)}
    issues = []
    for f in files():
        t = f.read_text(encoding="utf-8"); fid = re.match(r"FT-\d+", f.name).group(0)
        stage = (re.search(r"\*\*Stage:\*\*\s*([^\n*]+)", t) or [None, "?"])[1].strip()
        title = (re.search(r"^# FT-\d+:\s*(.+)", t, re.M) or [None, f.stem])[1]
        print(f"{fid}  {stage:<18} {title}")
        row = reg.get(fid)
        if not row: issues.append(f"{fid} has a file but no row in the register")
        elif row[4] != stage: issues.append(f"{fid}: the file says '{stage}' but the register says '{row[4]}'")
        if stage in ("Plan", "Awaiting approval", "In backlog") and re.search(r"\*\*Confirmed by the user:\*\*\s*not yet", t): issues.append(f"{fid} is at '{stage}' but the brief is not confirmed by the user")
        if stage in ("Plan", "Awaiting approval", "In backlog") and not re.search(r"\*\*From:\*\*[ \t]*\S", t): issues.append(f"{fid} is at '{stage}' with no security design input recorded")
        if stage == "In backlog" and not re.search(r"\*\*Decision:\*\*\s*D\d+", t): issues.append(f"{fid} is in the backlog with no approval (D-number) recorded")
        if stage == "In backlog" and not re.search(r"US-\d+", t.split("## Approval and backlog")[-1]): issues.append(f"{fid} is in the backlog with no story IDs recorded")
    for fid in reg:
        if not any(f.name.startswith(fid) for f in files()): issues.append(f"{fid} is in the register but has no file")
    print(f"\nFeatures: {len(files())}   Out of step: {len(issues)}"); [print(" -", i) for i in issues]; sys.exit(1 if issues else 0)
