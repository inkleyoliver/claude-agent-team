#!/usr/bin/env python3
"""Summarise a project's proof of done: criteria met and not met, criteria with no check or checker, and rules with no proof.
Read only. Exit 1 if any criterion is not met. Usage: python proof.py [playbook_dir]   (default: playbook)"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
d = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "playbook"); pf = d / "proof.md"
if not pf.exists(): print(f"No proof file at {pf}. Nothing can be reported as done against it."); sys.exit(1)
def rows(path, prefix):
    out = []
    for line in path.read_text(encoding="utf-8").splitlines() if path.exists() else []:
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if re.fullmatch(prefix + r"-\d+", c[0]): out.append(c)
    return out
met, notmet, issues = [], [], []
proofs = rows(pf, "PR")
for c in proofs:
    c += [""] * (6 - len(c)); pid, means, rules, how, who, status = c[:6]
    (met if (status.startswith("\u2705") or status.lower().startswith("met")) else notmet).append(f"{pid}: {means[:70]} ({who or 'no checker'})")
    if not how: issues.append(f"{pid} does not say how it is checked")
    if not who: issues.append(f"{pid} has no agent named to check it")
    if not re.search(r"PB-\d+", rules): issues.append(f"{pid} is not tied to a playbook rule")
covered = set(re.findall(r"PB-\d+", " ".join(c[2] for c in proofs)))
for c in rows(d / "playbook.md", "PB"):
    if c[0] not in covered and "MUST" in (c[1] if len(c) > 1 else ""): issues.append(f"{c[0]} is a MUST rule with no proof criterion")
text = pf.read_text(encoding="utf-8"); show = re.search(r"## Showcase\s*\n(.*?)(?=\n## |\Z)", text, re.S)
print(f"Proof criteria: {len(proofs)}   Met: {len(met)}   Not met: {len(notmet)}   Showcase recorded: {'yes' if show and len(show.group(1).strip()) > 120 else 'no'}")
if notmet: print("\nNot met:"); [print(" -", x) for x in notmet]
if issues: print("\nGaps in the proof itself:"); [print(" -", x) for x in issues]
sys.exit(1 if notmet else 0)
