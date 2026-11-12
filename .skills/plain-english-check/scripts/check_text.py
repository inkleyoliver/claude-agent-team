#!/usr/bin/env python3
"""Find dashes, AI writing tells, American spellings and long sentences. Reports only; never edits.
Usage: python check_text.py <file> [<file> ...]      Exit 1 if anything is found."""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
WORDS = "delve|dive into|leverage|utili[sz]e|robust|seamless(?:ly)?|crucial|pivotal|landscape|realm|tapestry|foster|holistic|embark|unlock|unleash|elevate|empower|supercharge|streamline|cutting-edge|game-chang\\w+|testament|underscore[sd]?|showcas\\w+|meticulous(?:ly)?|intricate|vibrant|bustling|ever-evolving|ever-changing|myriad|plethora|paramount"
PHRASES = ["it's important to note", "it is important to note", "it's worth noting", "it is worth noting", "in today's fast-paced", "in the ever-changing world", "when it comes to", "at the end of the day", "let's dive in", "here's the thing", "in conclusion", "great question", "i hope this helps", "certainly!", "absolutely!", "feel free to", "not just", "rest assured", "look no further"]
US = [(r"\b(\w*[a-z])iz(e[ds]?|ing|ation|ations)\b", "use -ise / -isation"), (r"\b(behavior|color|favor|honor|labor|neighbor)(s|al|ed|ing|ite)?\b", "use -our"), (r"\b(center|meter|theater|fiber)s?\b", "use -re"), (r"\b(defense|offense|license)\b", "check UK spelling (defence, offence, licence as a noun)"), (r"\b(program)\b", "use 'programme' unless it is software"), (r"\b(catalog|dialog|analog)\b", "use -ogue"), (r"\b(canceled|traveled|labeled|modeling|modeled)\b", "double the l")]
US_OK = re.compile(r"(?i)^(size|sized|sizes|sizing|prize|prizes|seize|seized|capsize|resize|resized|resizing|citizen|horizon|organization_id|authorization)$")
bad = 0
for name in sys.argv[1:]:
    text = pathlib.Path(name).read_text(encoding="utf-8", errors="replace"); in_code = False
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith(("```", "~~~")): in_code = not in_code; continue
        if in_code: continue
        prose = re.sub(r"`[^`]*`|https?://\S+", "", line); hits = []
        if "\u2014" in prose: hits.append("em dash")
        if "\u2013" in prose: hits.append("en dash (use 'to' for ranges)")
        if re.search(r"\w -- \w", prose): hits.append("double hyphen used as a dash")
        for m in re.finditer(rf"\b(?:{WORDS})\b", prose, re.I): hits.append(f"AI tell: '{m.group(0)}'")
        low = prose.lower()
        for p in PHRASES:
            if p in low: hits.append(f"AI tell: '{p}'")
        if re.search(r"\b(very|really|truly|incredibly)\b", low): hits.append("filler intensifier")
        for rx, why in US:
            for m in re.finditer(rx, prose, re.I):
                if not US_OK.match(m.group(0)): hits.append(f"American spelling '{m.group(0)}': {why}")
        for s in re.split(r"(?<=[.!?])\s+", re.sub(r"^[\s>#*\-\d.|]+", "", prose)):
            n = len(s.split())
            if n > 25 and "|" not in s: hits.append(f"sentence of {n} words (aim for 25 or fewer)")
        for h in dict.fromkeys(hits): print(f"{name}:{i}: {h}"); bad += 1
print(f"Issues found: {bad}")
sys.exit(1 if bad else 0)
