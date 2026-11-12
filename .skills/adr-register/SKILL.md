---
description: Create a numbered architecture decision record from the team's template and list every record's status, flagging ones still proposed, accepted without a D-number, or with empty sections. Use whenever a significant design choice is made or reviewed.
---

# Decision records

```
python ~/.claude/skills/adr-register/scripts/adr.py new "Use a managed identity provider for sign-in"
python ~/.claude/skills/adr-register/scripts/adr.py status
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library and prints a short result. Run it from the project root. It writes only inside `architecture/decisions/`.

- Always create a record with `new`, so numbers are never reused. Fill in every section; give at least two real options, including the one you rejected.
- Run `status` before you reply and list every record that is still Proposed. A Proposed record is not a decision, and nothing may be built on it.
- A record that changes risk, cost or a security control goes to human-in-the-loop. Mark it Accepted only with the D-number of that decision.
- Never edit an Accepted record to change the decision. Write a new one and mark the old one "Superseded by ADR-NNN".
