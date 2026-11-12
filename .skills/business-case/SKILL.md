---
description: Calculate net present value, payback period, break-even and a sensitivity table for a business case from upfront cost, monthly benefit and monthly running cost. Use whenever a business case, pricing or payback figure is produced.
---

# Business case arithmetic

```
python ~/.claude/skills/business-case/scripts/case.py --upfront 20000 --benefit 1500 --running 400 --months 36 --ramp 6
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result.

- `--benefit` and `--running` are per month. `--rate` is the yearly discount rate (default 3.5%). `--ramp` is how many months benefits take to reach their full level.
- Never do this arithmetic in your head. Paste the command and its output into the business case so anyone can re-run it.
- The script only does arithmetic. Every input is an assumption: give its source and how confident you are, and run it once per option, including "do nothing".
- Always show the sensitivity table, and say plainly which change makes the case fail.
- It does not handle tax, inflation, financing or irregular cash flows. Where those matter, say so under "Needs professional confirmation".
