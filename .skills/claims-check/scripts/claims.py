#!/usr/bin/env python3
"""Find marketing claims that need evidence or a check before publishing. Reports only; never edits.
Usage: python claims.py <file> [<file> ...]      Exit 1 if anything is found."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
RULES = [
 ("Superlative or absolute claim: needs proof it is true of every competitor or every case", r"(?i)\b(best|fastest|cheapest|lowest|leading|number one|no\.? ?1|#1|unbeatable|unrivalled|most (?:trusted|secure|popular|advanced)|world[- ]class|award[- ]winning|only (?:platform|app|service|tool|product))\b"),
 ("Guarantee or certainty: needs terms, or should be removed", r"(?i)\b(guarantee[ds]?|risk[- ]free|100\s?%|always|never fails?|completely (?:safe|secure)|fully (?:secure|compliant)|bank[- ]grade|military[- ]grade|unhackable|zero risk)\b"),
 ("Number or statistic: needs a source, a date and the basis of the comparison", r"(?i)\b\d+(?:\.\d+)?\s?(?:%|per ?cent|x\b|times (?:faster|more|cheaper))|\b(?:over|more than|up to|as many as)\s+[\d,]+\b|\bsaves? (?:you )?(?:up to )?[£$€]?\d"),
 ("Comparison: needs evidence and must compare like with like", r"(?i)\b(better|faster|cheaper|safer|easier|more (?:secure|reliable|accurate)) than\b|\bcompared (?:to|with)\b|\bunlike (?:other|our competitors)"),
 ("'Free': every condition and later cost must be clear at the same point", r"(?i)\bfree\b(?! of charge to change)|\bno (?:hidden )?(?:fees|costs|charges)\b"),
 ("Urgency or scarcity: must be real, or it is a pressure tactic", r"(?i)\b(only \d+ (?:left|remaining|spaces|places)|limited time|ends (?:soon|today|tonight)|last chance|hurry|don'?t miss out|act now|while stocks last|selling fast)\b"),
 ("Price: the full price including unavoidable fees must be shown up front", r"(?i)\bfrom (?:just |only )?[£$€]\d|[£$€]\d[\d,.]*\s?(?:\+|plus)\s?(?:vat|fees|booking)|\bwas [£$€]\d"),
 ("Testimonial, review or endorsement: must be real, held on file and used with permission", r"(?i)\b(trusted by|loved by|recommended by|as (?:seen|featured) (?:in|on)|rated \d|\d(?:\.\d)? ?(?:stars?|/5)|customers say|our users say)\b|[\"“][^\"”]{20,}[\"”]\s*[-–—]?\s*[A-Z][a-z]+"),
 ("Compliance, security or health claim: needs the certificate or a qualified sign-off", r"(?i)\b(gdpr[- ]compliant|iso ?27001|certified|accredited|approved by|endorsed by|clinically proven|scientifically proven|safeguarding[- ]compliant|ofsted|dbs[- ]checked)\b"),
 ("Environmental claim: needs evidence for the whole life cycle", r"(?i)\b(eco[- ]friendly|sustainable|carbon[- ]neutral|net[- ]zero|green(?:er)?|environmentally friendly)\b"),
]
n = 0
for name in sys.argv[1:]:
    for i, line in enumerate(pathlib.Path(name).read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        for why, rx in RULES:
            m = re.search(rx, line)
            if m: print(f"{name}:{i}: '{m.group(0).strip()}': {why}"); n += 1
print(f"Claims to verify: {n}")
sys.exit(1 if n else 0)
