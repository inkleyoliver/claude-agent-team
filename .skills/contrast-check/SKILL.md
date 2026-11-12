---
description: Calculate the WCAG 2.2 colour contrast ratio for a text and background colour pair and say whether it passes AA for normal text, large text and interface components. Use whenever colours are chosen, reviewed or tested.
---

# Contrast check

```
python ~/.claude/skills/contrast-check/scripts/contrast.py "#767676" "#ffffff"
python ~/.claude/skills/contrast-check/scripts/contrast.py --css styles.css
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result.

- Give the text colour, then the background. AA needs 4.5:1 for normal text and 3:1 for large text (24px, or 18.66px bold), icons, borders and focus indicators.
- Never state a contrast ratio you did not calculate. Put the pairs and ratios in your audit or test log.
- `--css` lists every hex colour against white and black to find candidates. It does not know which colours are used together, so check each real pair.
- Check every state: default, hover, focus, disabled, error, and text over images or gradients (use the worst-case background).
- Contrast is one success criterion. Passing it says nothing about keyboard use, labels, focus order or screen readers.
