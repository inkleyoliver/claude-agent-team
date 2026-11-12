#!/usr/bin/env python3
"""Check the product backlog and score priorities.
  python backlog.py check [product/backlog.md]     -> stories missing required parts, duplicate IDs, the next free ID
  python backlog.py rice <reach> <impact> <confidence> <effort>
RICE: reach = people per period; impact = 0.25, 0.5, 1, 2 or 3; confidence = 0 to 100 (%); effort = person-weeks."""
import re, sys, pathlib, collections
sys.stdout.reconfigure(encoding="utf-8")
a = sys.argv[1:]
if a and a[0] == "rice" and len(a) == 5:
    r, i, c, e = map(float, a[1:])
    if e <= 0: sys.exit("effort must be more than 0")
    print(f"RICE score: {r * i * (c / 100) / e:,.1f}   (reach {r:g} x impact {i:g} x confidence {c:g}% / effort {e:g})")
    if c < 50: print("Confidence is under 50%: treat this as an assumption to test, not a priority.")
elif a and a[0] == "check":
    p = pathlib.Path(a[1] if len(a) > 1 else "product/backlog.md")
    if not p.exists(): sys.exit(f"No backlog at {p}")
    t = p.read_text(encoding="utf-8"); parts = re.split(r"^### (US-\d+):?\s*(.*)$", t, flags=re.M)
    stories = [(parts[k], parts[k + 1].strip(), parts[k + 2]) for k in range(1, len(parts), 3)]
    issues = []; status = collections.Counter(); seen = collections.Counter(s[0] for s in stories)
    for sid, n in seen.items():
        if n > 1: issues.append(f"{sid} is used {n} times")
    for sid, title, body in stories:
        st = (re.search(r"\*\*Status:\*\*\s*([A-Za-z ]+)", body) or [None, "missing"])[1].strip(); status[st] += 1
        def miss(msg): issues.append(f"{sid} ({title[:40]}): {msg}")
        if not re.search(r"(?i)as an? .+?, I (want|need) .+?, so that", body): miss("no 'As a..., I want..., so that...' statement")
        if not re.search(r"(?i)given .+ when .+ then ", body.replace("\n", " ")): miss("no Given / When / Then acceptance criterion")
        sec = re.search(r"\*\*Security, accessibility and privacy\*\*\s*\n((?:\s*-.*\n?)*)", body)
        if not sec or not re.sub(r"[-\s<>]|criteria", "", sec.group(1)): miss("no security, accessibility or privacy criteria")
        if not re.search(r"\*\*Priority:\*\*\s*[^\s*<]", body): miss("no priority")
        if not re.search(r"\*\*Size:\*\*\s*[SML]\b", body): miss("no size")
        if st in ("Ready", "In progress") and not re.search(r"\*\*Analytics\*\*\s*\n\s*-\s*[^\s<]", body): miss(f"is '{st}' with no analytics need stated (write 'none' if none)")
    nums = [int(s[0][3:]) for s in stories]
    print(f"Stories: {len(stories)}   " + "   ".join(f"{k}: {v}" for k, v in status.most_common()) + f"   Next free ID: US-{max(nums, default=0) + 1}")
    print(f"To fix: {len(issues)}"); [print(" -", i) for i in issues]; sys.exit(1 if issues else 0)
else: sys.exit(__doc__)
