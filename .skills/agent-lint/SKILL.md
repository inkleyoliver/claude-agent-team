---
description: Check every agent file against the team's conventions (frontmatter, description length, dashes, UK spelling, persona, safeguard rules, handoff block, identical proof check, skills that exist). Use after creating or changing any agent, and before committing.
---

# Agent lint

```
python ~/.claude/skills/agent-lint/scripts/lint_agents.py [agents_dir]
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result. The default folder is `~/.claude/agents`.

- Run it before every commit to the agents repository. Fix every problem it lists, or say in your reply why one is a deliberate exception.
- It checks form, not judgement. You still check overlap between agents, least-privilege tools, and that no safeguard was weakened.
- Report the "total description words" figure in your reply, because descriptions load every turn.
- If a check is wrong for a new convention, propose a change to the script; don't skip the check.
