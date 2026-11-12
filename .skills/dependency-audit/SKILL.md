---
description: First-pass supply chain check: finds dependency manifests, missing lockfiles, unpinned dependencies, install scripts, unpinned CI actions and base images, and runs npm audit or pip-audit when they are installed. Use when dependencies change and before a release.
---

# Dependency audit

```
python ~/.claude/skills/dependency-audit/scripts/audit.py [project_dir]
```

Run it with `python` (on Windows, `py -3` if `python` is not found). It uses only Python's standard library, changes nothing, and prints a short result. It installs nothing.

- Run it first, then go deeper on what it lists. Put its output in your report with the date.
- It only runs audit tools that are already installed, and it says which were not run. A tool that was not run checked nothing: list that under "Not checked", and ask for approval before installing any tool.
- It reads npm and Python requirements in detail, and only points at Go, Rust, Ruby, PHP and `pyproject.toml` projects. Check those with their own tools.
- It does not judge whether a package is abandoned, typosquatted or badly licensed. That is still your job.
- Each line is something to look at, not a confirmed finding. Rate what you confirm with the team's severity bands.
