---
description: Calculate the UK GDPR 72-hour ICO notification deadline from the moment the organisation became aware of a personal data breach, with the time left and working milestones. Use as soon as a personal data breach is suspected.
---

# Breach clock

```
python ~/.claude/skills/breach-clock/scripts/clock.py "2026-11-12 09:30"
python ~/.claude/skills/breach-clock/scripts/clock.py "2026-11-12 09:30" --tz Europe/London --now "2026-11-13 10:00"
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result. On Windows it may need `pip install tzdata` once.

- The time you give is when the organisation became **aware** of the breach, not when it happened. If that time is uncertain, use the earliest plausible time and say so.
- Run it at the start of every response and put the deadline at the top of the incident file and of every reply.
- The 72 hours run through weekends and bank holidays, and the script handles clock changes. Never work the deadline out by hand.
- The two milestones it prints are working targets, not legal ones.
- You track the clock and draft the notice. A human decides whether the breach is reportable and sends it.
