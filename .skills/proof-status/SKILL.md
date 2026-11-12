---
description: Summarise a project's proof of done: criteria met and not met, criteria with no check or checker, MUST rules with no proof criterion, and whether a showcase is recorded. Use before briefing the user, before accepting work as done, and before a release.
---

# Proof status

```
python ~/.claude/skills/proof-status/scripts/proof.py [playbook_dir]
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library and prints a short result. It reads `playbook/proof.md` and `playbook/playbook.md` and never changes them.

- Run it before every briefing and before reporting any work as finished. Give the user the met and not met counts, and name each criterion that is not met.
- It reports what the proof file says. Before you rely on a criterion marked as met, spot-check the evidence behind it.
- "Gaps in the proof itself" are rules nobody is checking. Propose the missing criteria to the user; do not add them yourself without approval.
- No proof file means nothing can be reported as done against it.
