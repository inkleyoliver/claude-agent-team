---
description: Create a new feature file with the next free FT number from the team's template, and check that every feature's stage matches the register and that no stage was skipped. Use when a feature request arrives and at the start of every product-manager feature run.
---

# Feature register

```
python ~/.claude/skills/feature-register/scripts/features.py new "Export attendance list" --source FB-3
python ~/.claude/skills/feature-register/scripts/features.py new "Badge progress by child" --type upgrade --of "Badges"
python ~/.claude/skills/feature-register/scripts/features.py status
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library and prints a short result. Run it from the project root. It writes only inside `features/`.

- Always create a feature with `new`. Never pick an FT number or copy the template by hand: the script gives the next free number, the file and the register row.
- Run `status` at the start of every run to find the stage to pick up from, and again before you reply.
- `status` flags a stage that was skipped: a plan with no confirmed brief, a plan with no security design input, or a backlog entry with no D-number or story IDs. Never fix a flag by editing the stage. Go back and do the missing step.
- When you change a feature's stage, change it in the file and in the register in the same run.
