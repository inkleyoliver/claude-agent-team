---
description: Check a domain profile for missing sections, requirements with no source or confidence rating, sources with no link or date, sources not checked recently, citations with no source, and points that need a qualified human. Use before relying on a profile and after updating one.
---

# Domain profile check

```
python ~/.claude/skills/domain-profile-check/scripts/profile.py
python ~/.claude/skills/domain-profile-check/scripts/profile.py expert/domain-profile.md --months 6
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library and prints a short result. It reads the profile and never changes it.

- Run it at the start of every run after the first. If the profile or its sources are older than the limit, check the sources on the web again before you rely on them, and update the dates.
- Run it again before you reply and fix what it lists. Every requirement needs a source and a confidence rating; every source needs a link and the date you checked it.
- Number sources and cite them as `[1]`, `[2]` in the text, so the check can match them.
- It lists the requirements marked as needing qualified sign-off. Repeat that list in your reply every time, until a qualified human has confirmed each one.
- It checks that sources exist, not that they are right or authoritative. That is still your judgement.
