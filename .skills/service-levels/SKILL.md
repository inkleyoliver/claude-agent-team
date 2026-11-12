---
description: Service level arithmetic: downtime allowed by an availability target, error budget used and burn rate, and p50, p95 and p99 from a file of response times. Use when setting service levels or reporting test and monitoring results.
---

# Service levels

```
python ~/.claude/skills/service-levels/scripts/slo.py budget 99.9 --days 30
python ~/.claude/skills/service-levels/scripts/slo.py burn 99.9 --total 1200000 --failed 900 --days 30 --elapsed 12
python ~/.claude/skills/service-levels/scripts/slo.py percentiles times.txt
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result.

- `budget` turns a target into the downtime it allows, so the user can see what they are agreeing to. Show it whenever you propose a target.
- `burn` takes requests and failures so far; `--elapsed` is days into the period. A burn rate above 1 means the target will be missed.
- `percentiles` reads one number per line. Report percentiles, never the mean alone, and say how many samples there were.
- Never quote a downtime figure, error budget or percentile you did not calculate.
- The script does not run load tests. Tests still need a named test environment and an approved scope.
