---
description: Total token use across Claude Code session transcripts and show the largest tool results, the tools that cost most, cache-read share and files read repeatedly. Use when measuring where tokens go, before proposing any saving.
---

# Token usage

```
python ~/.claude/skills/token-usage/scripts/usage.py                       # newest 20 sessions, all projects
python ~/.claude/skills/token-usage/scripts/usage.py <project_folder>
python ~/.claude/skills/token-usage/scripts/usage.py <transcript.jsonl>
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result. Transcripts live in `~/.claude/projects/<project-folder>/`.

- It prints numbers, tool names and file paths only. Never open transcripts to read their content: they may hold secrets or personal data.
- Token counts come from the transcripts' own usage fields. Tool result sizes are estimates at 4 characters a token; label them as estimates.
- A low cache-read share, one tool dominating, or the same file read three or more times are the usual places to look first.
- Measure before and after any change you propose, with the same command.
