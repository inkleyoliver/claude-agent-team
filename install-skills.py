#!/usr/bin/env python3
"""Copy the team's skills from this repository into ~/.claude/skills, where Claude Code loads them.
Run it after cloning or pulling:   python install-skills.py      (Windows: py -3 install-skills.py)
Skills already there with the same name are replaced. Other skills are left alone."""
import pathlib, shutil
src = pathlib.Path(__file__).resolve().parent / ".skills"
dest = pathlib.Path.home() / ".claude" / "skills"
dest.mkdir(parents=True, exist_ok=True)
names = sorted(p.name for p in src.iterdir() if (p / "SKILL.md").exists())
for n in names:
    shutil.rmtree(dest / n, ignore_errors=True)
    shutil.copytree(src / n, dest / n, ignore=shutil.ignore_patterns("__pycache__"))
print(f"Installed {len(names)} skills into {dest}:")
for n in names: print(" -", n)
