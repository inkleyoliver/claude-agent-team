---
description: Check the product backlog for stories missing a user statement, acceptance criteria, security, accessibility and privacy criteria, priority or size, find duplicate story IDs and the next free ID, and calculate RICE scores. Use whenever stories are written or prioritised.
---

# Backlog check

```
python ~/.claude/skills/backlog-check/scripts/backlog.py check
python ~/.claude/skills/backlog-check/scripts/backlog.py rice 400 2 80 3
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library and prints a short result. `check` reads `product/backlog.md` (or a path you give) and never changes it.

- Run `check` before adding stories, to get the next free US number, and after, to prove every story is complete. Fix everything it lists before you reply.
- A story with no security, accessibility and privacy criteria is not ready. If none apply, say which you considered and why not; never leave the section empty.
- `rice` takes reach (people per period), impact (0.25, 0.5, 1, 2 or 3), confidence (0 to 100) and effort (person-weeks). Calculate every score with it and show the four inputs beside the score, with what each rests on.
- Security and compliance obligations are requirements. Never rank them against features with a score.
- The check proves a story has its parts, not that they are good. You still judge whether the criteria are testable.
