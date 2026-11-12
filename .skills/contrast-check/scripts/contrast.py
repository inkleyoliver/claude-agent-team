#!/usr/bin/env python3
"""WCAG 2.2 colour contrast. Exit 1 if a pair fails AA for normal text.
  python contrast.py "#767676" "#ffffff"            -> one pair (text colour, background colour)
  python contrast.py --css styles.css               -> list every hex colour in a file against white and black"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
def rgb(h):
    h = h.strip().lstrip("#")
    if len(h) in (3, 4): h = "".join(c * 2 for c in h[:3])
    if not re.fullmatch(r"[0-9a-fA-F]{6}([0-9a-fA-F]{2})?", h): sys.exit(f"'{h}' is not a hex colour")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
def lum(h): return sum(w * (c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4) for w, c in zip((0.2126, 0.7152, 0.0722), rgb(h)))
def ratio(a, b):
    x, y = sorted((lum(a), lum(b)), reverse=True); return (x + 0.05) / (y + 0.05)
def verdict(r):
    return f"{r:.2f}:1  normal text {'pass' if r >= 4.5 else 'FAIL'} (4.5)  large text {'pass' if r >= 3 else 'FAIL'} (3)  icons, borders and focus {'pass' if r >= 3 else 'FAIL'} (3)  AAA {'pass' if r >= 7 else 'no'} (7)"
a = sys.argv[1:]
if len(a) == 2 and a[0] == "--css":
    cols = sorted(set(m.lower() for m in re.findall(r"#[0-9a-fA-F]{3,8}\b", pathlib.Path(a[1]).read_text(errors="replace")) if len(m) in (4, 7)))
    for c in cols: print(f"{c:<8} on white {ratio(c, '#fff'):5.2f}:1 {'ok  ' if ratio(c, '#fff') >= 4.5 else 'FAIL'}   on black {ratio(c, '#000'):5.2f}:1 {'ok' if ratio(c, '#000') >= 4.5 else 'FAIL'}")
    print("This lists colours, not pairs. Check each real text and background pair before reporting a failure.")
elif len(a) == 2:
    r = ratio(*a); print(f"{a[0]} on {a[1]}: {verdict(r)}"); sys.exit(0 if r >= 4.5 else 1)
else: sys.exit(__doc__)
