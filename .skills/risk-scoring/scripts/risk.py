#!/usr/bin/env python3
"""Score risks on the team's 5x5 matrix (likelihood x impact) and give the rating band.
  python risk.py 4 3                     -> one risk
  python risk.py medium high             -> threat-modeller ratings (Low=2, Medium=3, High=4)
  python risk.py --inherent 4 5 --residual 2 5 [--target 1 5]"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
WORDS = {"low": 2, "medium": 3, "high": 4}
L = ["", "Rare", "Unlikely", "Possible", "Likely", "Almost certain"]; I = ["", "Negligible", "Minor", "Moderate", "Major", "Severe"]
REVIEW = {"Critical": "not acceptable: treat before release; only an executive may accept, for no more than 14 days", "High": "needs a named owner, human approval, a treatment plan and a review within 30 days", "Medium": "needs an owner and a treatment plan; review within 90 days", "Low": "acceptable; review annually"}
def num(v):
    v = v.lower(); n = WORDS.get(v) or (int(v) if v.isdigit() else 0)
    if not 1 <= n <= 5: sys.exit(f"'{v}' is not 1 to 5 or low/medium/high")
    return n
def score(l, i):
    l, i = num(l), num(i); s = l * i
    band = "Critical" if s >= 15 else "High" if s >= 8 else "Medium" if s >= 4 else "Low"
    icon = {"Critical": "\U0001F534", "High": "\U0001F7E0", "Medium": "\U0001F7E1", "Low": "\U0001F7E2"}[band]
    return f"{L[l]} ({l}) x {I[i]} ({i}) = {s}: {icon} {band}", band
a = sys.argv[1:]
if a and a[0].startswith("--"):
    last = None
    for k in range(0, len(a), 3):
        text, last = score(a[k + 1], a[k + 2]); print(f"{a[k][2:].capitalize()} risk: {text}")
    print(f"Default appetite for the last rating ({last}): {REVIEW[last]}")
elif len(a) == 2:
    text, band = score(*a); print(text); print(f"Default appetite: {REVIEW[band]}")
else: sys.exit(__doc__)
