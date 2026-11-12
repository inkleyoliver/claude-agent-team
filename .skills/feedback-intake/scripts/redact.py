#!/usr/bin/env python3
"""Redact personal data from text. Best effort: it catches patterns, not names in free text, so still read the result.
Usage: python redact.py <file>          (prints the redacted text; the original is not changed)"""
import re, sys, pathlib
RULES = [
 ("[email]", r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
 ("[link]", r"https?://\S+|\bwww\.\S+"),
 ("[card number]", r"\b(?:\d[ -]?){13,19}\b"),
 ("[phone]", r"(?<!\w)(?:\+44\s?\d|0\d|\(0\d)[\d\s().-]{8,13}\d\b|\+\d{1,3}[\s-]?\d[\d\s-]{7,13}\d\b"),
 ("[postcode]", r"\b[A-Z]{1,2}\d[A-Z\d]?\s?\d[A-Z]{2}\b"),
 ("[NI number]", r"\b[A-CEGHJ-PR-TW-Z]{2}\s?\d{2}\s?\d{2}\s?\d{2}\s?[A-D]\b"),
 ("[date of birth]", r"(?i)\b(?:dob|date of birth|born)\b[:\s]*\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}"),
 ("[IP address]", r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
 ("[name]", r"(?i)(?<=\bmy name is )[A-Z][a-z'-]+(?: [A-Z][a-z'-]+)?|(?<=\bI am )[A-Z][a-z'-]+ [A-Z][a-z'-]+|(?<=\bI'm )[A-Z][a-z'-]+ [A-Z][a-z'-]+"),
]
def redact(text, counts=None):
    for label, rx in RULES:
        flags = 0 if label in ("[postcode]", "[NI number]") else 0
        text, n = re.subn(rx, label, text, flags=flags)
        if counts is not None and n: counts[label] = counts.get(label, 0) + n
    return text
if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    c = {}; print(redact(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8-sig", errors="replace"), c))
    print("Redacted: " + (", ".join(f"{v} {k}" for k, v in c.items()) or "nothing"), file=sys.stderr)
