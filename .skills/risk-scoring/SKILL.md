---
description: Score a risk on the team's 5x5 likelihood and impact matrix and get the rating band and default appetite, including conversion from threat-modeller Low/Medium/High ratings. Use whenever a risk or threat is rated or added to the risk register.
---

# Risk scoring

```
python ~/.claude/skills/risk-scoring/scripts/risk.py 4 3
python ~/.claude/skills/risk-scoring/scripts/risk.py medium high
python ~/.claude/skills/risk-scoring/scripts/risk.py --inherent 4 5 --residual 2 5 --target 1 5
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result.

- Likelihood then impact, each 1 to 5. The words low, medium and high map to 2, 3 and 4, which is the team's default for threat-modeller ratings; adjust with a written reason.
- Bands: 15 to 25 Critical, 8 to 12 High, 4 to 6 Medium, 1 to 3 Low.
- The script does the multiplication and the band. You choose the likelihood and impact, and you must give the reason for each.
- The appetite it prints is the team default. An approved `governance/risk-appetite.md` in the project overrides it.
- Only a human accepts risk. A score is never an approval.
