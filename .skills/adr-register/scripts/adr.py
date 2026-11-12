#!/usr/bin/env python3
"""Create numbered architecture decision records and list their status.
  python adr.py new "Use a managed identity provider for sign-in"
  python adr.py status
Run from the project root. Writes only inside architecture/decisions/."""
import re, sys, pathlib
from datetime import date
sys.stdout.reconfigure(encoding="utf-8")
D = pathlib.Path("architecture/decisions")
TEMPLATE = """# {id}: {title}
**Status:** Proposed  **Date:** {today}

## Context

## Options considered
| Option | Pros | Cons | Security impact | Cost and effort |
|--------|------|------|-----------------|-----------------|

## Decision

## Consequences
"""
a = sys.argv[1:]; files = sorted(D.glob("ADR-*.md")) if D.exists() else []
if len(a) == 2 and a[0] == "new":
    D.mkdir(parents=True, exist_ok=True)
    n = max([int(re.match(r"ADR-(\d+)", f.name).group(1)) for f in files], default=0) + 1
    aid = f"ADR-{n:03d}"; slug = re.sub(r"[^a-z0-9]+", "-", a[1].lower()).strip("-")[:50]
    f = D / f"{aid}-{slug}.md"; f.write_text(TEMPLATE.format(id=aid, title=a[1], today=date.today().isoformat()), encoding="utf-8"); print(f"Created {f}")
elif a == ["status"]:
    issues = []; ids = {re.match(r"ADR-\d+", f.name).group(0) for f in files}
    for f in files:
        t = f.read_text(encoding="utf-8"); aid = re.match(r"ADR-\d+", f.name).group(0)
        status = (re.search(r"\*\*Status:\*\*\s*(.+?)(?:\s{2,}|\*\*|\n)", t) or [None, "?"])[1].strip()
        title = (re.search(r"^# ADR-\d+:\s*(.+)", t, re.M) or [None, f.stem])[1]
        print(f"{aid}  {status:<28} {title}")
        if status.startswith("Proposed"): issues.append(f"{aid} is still Proposed: it is not a decision yet")
        if status.startswith("Accepted") and not re.search(r"D\d+", status): issues.append(f"{aid} is Accepted with no D-number: check whether it needed human approval")
        m = re.search(r"Superseded by (ADR-\d+)", status)
        if m and m.group(1) not in ids: issues.append(f"{aid} is superseded by {m.group(1)}, which does not exist")
        for sec in ("Context", "Options considered", "Decision", "Consequences"):
            body = re.search(rf"## {sec}\n(.*?)(?=\n## |\Z)", t, re.S)
            if not body or not re.sub(r"[|\-\s]|Option|Pros|Cons|Security impact|Cost and effort", "", body.group(1)): issues.append(f"{aid}: '{sec}' is empty")
    print(f"\nDecision records: {len(files)}   To look at: {len(issues)}"); [print(" -", i) for i in issues]; sys.exit(1 if issues else 0)
else: sys.exit(__doc__)
