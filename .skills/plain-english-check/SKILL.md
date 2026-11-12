---
description: Find em dashes and en dashes, AI writing tells, American spellings and over-long sentences in text files. Use before and after editing any content, and before committing agent files or documents.
---

# Plain English check

```
python ~/.claude/skills/plain-english-check/scripts/check_text.py <file> [<file> ...]
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result. It skips code blocks, code spans and links, and it never edits.

- Run it before you edit, to find the problems, and again after, to prove they are gone. Put both counts in your change log.
- Each hit is a prompt to look, not an order to change. A listed word can stay if it is the clearest choice, and never change quotes, legal wording, code, or the meaning.
- "program", "license" and "-ize" inside product names, code or American proper nouns are correct; leave them.
- A clean result does not mean the text is good. You still judge structure, reading age, tone and accessibility.
