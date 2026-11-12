---
description: Read a project's approvals log and list decisions that are still awaiting an answer, have expired, are due for review soon, or are risk acceptances with no review date. Use before acting on any approval and when preparing a release.
---

# Approvals check

```
python ~/.claude/skills/approvals-check/scripts/approvals.py
python ~/.claude/skills/approvals-check/scripts/approvals.py approvals/approvals-log.md --soon 14
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result. It reads the Summary table in `approvals/approvals-log.md` and never writes to it.

- Run it at the start of every run and put expired and awaiting decisions in your reply.
- An expired or awaiting decision is **not approved**. Anything that depends on it is blocked.
- The script checks dates and status only. You still check that the approval covers this exact scope and that nothing has changed since it was given.
- It trusts the log's table. If the table and the detailed entries disagree, say so; that is a finding.
- No log means nothing has been approved.
