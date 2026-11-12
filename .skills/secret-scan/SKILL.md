---
description: Scan a change or a whole repository for committed secrets (keys, tokens, passwords, connection strings, risky files) without ever printing a full secret. Use before every commit, at the start of every code review, and before a release.
---

# Secret scan

```
python ~/.claude/skills/secret-scan/scripts/secret_scan.py            # changes against HEAD, plus untracked files
python ~/.claude/skills/secret-scan/scripts/secret_scan.py --staged   # what is about to be committed
python ~/.claude/skills/secret-scan/scripts/secret_scan.py --diff main
python ~/.claude/skills/secret-scan/scripts/secret_scan.py --all      # every tracked file
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result. Exit code 1 means something was found.

- Run it first, before any other check. A leaked secret is the most urgent finding there is.
- It is a first pass, not proof of absence. Still read the change for secrets in logs, error messages, URLs and client-side bundles.
- Check each hit: say which are real and which you dismissed as placeholders, and why.
- Never repeat a full secret in a report. Use the masked form the script prints.
- A real secret that was ever committed must be rotated; removing it is not enough. Rotation is a human decision through human-in-the-loop.
