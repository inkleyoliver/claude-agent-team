---
description: Calculate A/B test sample size and duration, and analyse results for two proportions with a sample ratio check, confidence interval and p-value. Use when planning or analysing any experiment, so the numbers are calculated, not estimated.
---

# Experiment statistics

```
python ~/.claude/skills/experiment-stats/scripts/abtest.py size --baseline 0.10 --mde 0.02 --daily 400
python ~/.claude/skills/experiment-stats/scripts/abtest.py analyse --a 120/1000 --b 150/1010
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result.

- `--mde` is the absolute change that would matter (0.02 is 2 percentage points). `--a` and `--b` are conversions/users. Defaults: alpha 0.05 two-sided, power 80%, a 50/50 split (`--split` changes it).
- Never do this arithmetic in your head or quote a sample size you did not calculate. Paste the command and its output into the pre-registration or the analysis.
- `analyse` checks the sample ratio first and stops if it fails. Do not work round that: investigate the allocation.
- It covers one primary metric with two variants. For more variants or metrics, apply the Holm correction and say so. For continuous metrics, or sequential designs, say the script does not cover them and state the method you used.
- Significance is not the decision. Compare the interval with the pre-registered minimum effect and check the guardrails.
