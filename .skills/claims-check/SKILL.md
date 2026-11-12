---
description: Find marketing claims that need evidence or a check before publishing: superlatives, guarantees, statistics, comparisons, 'free', urgency, prices, testimonials, and compliance or environmental claims. Use on any launch plan, messaging or marketing copy before it goes for approval.
---

# Claims check

```
python ~/.claude/skills/claims-check/scripts/claims.py <file> [<file> ...]
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library and prints a short result. It never edits.

- Run it on messaging and copy before it goes to human-in-the-loop. Put every hit in the "Claims to verify" table with the evidence that supports it, or remove the claim.
- A claim with no evidence held on file before publication does not go out. "We believe" does not fix an unproven claim.
- The script matches wording. It cannot tell whether a claim is true, and it will miss claims made by implication, images or omission. Read the copy yourself as a sceptical customer would.
- Rules it reflects, for the UK: advertising must be legal, decent, honest and truthful, with evidence held for objective claims (CAP Code); no fake urgency, hidden or drip-fed prices, or fake reviews (consumer protection law); marketing by email or text needs consent or a valid soft opt-in (PECR). This is a prompt to check, not legal advice: uncertain points go to grc and a qualified human.
- Never rewrite a claim so that it passes the check while still misleading.
