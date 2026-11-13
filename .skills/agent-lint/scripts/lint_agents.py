#!/usr/bin/env python3
"""Check every agent file against the team conventions. Exit 1 if any check fails.
Usage: python lint_agents.py [agents_dir]   (default: ~/.claude/agents)"""
import re, sys, pathlib, collections
sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "~/.claude/agents").expanduser()
files = sorted(p for p in root.glob("*.md"))
US = re.compile(r"\b\w*(?:[a-z]ization|prioritiz|minimiz|authoriz|analyz|organiz|recogniz|summariz)\w*|\bbehaviors?\b|\bdefense\b|\bcolors?\b|\bcenter\b", re.I)
DASH_OK = {"writer", "agent-steward"}      # they describe dashes
NO_HANDOFF_OK = {"human-in-the-loop", "chief-of-staff"}
NO_PROOF_OK = {"chief-of-staff"}
INHERIT_TOOLS_OK = {"front-desk"}   # deliberately inherits every tool, including connectors
problems, proofs, words = [], collections.defaultdict(list), 0
def bad(f, msg): problems.append(f"{f.name}: {msg}")
for f in files:
    t = f.read_text(encoding="utf-8")
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if not m: bad(f, "no valid frontmatter starting on line 1"); continue
    fm = dict(l.split(":", 1) for l in m.group(1).splitlines() if ":" in l and not l.startswith(" "))
    skills = re.findall(r"^\s+-\s*(\S+)", m.group(1).split("skills:", 1)[1], re.M) if "skills:" in m.group(1) else []
    for sk in skills:
        if not (root / ".skills" / sk / "SKILL.md").exists(): bad(f, f"lists skill '{sk}', which is not in .skills/")
    fm = {k.strip(): v.strip() for k, v in fm.items()}; body = m.group(2); name = fm.get("name", "")
    if name != f.stem: bad(f, f"name '{name}' does not match the file name")
    d = fm.get("description", ""); n = len(d.split()); words += n
    if not d: bad(f, "no description")
    elif n > 62: bad(f, f"description is {n} words (aim for under about 60)")
    if ": " in d or " #" in d: bad(f, "description contains ': ' or ' #', which breaks the YAML header so the agent will not load; reword it")
    tools = [x.strip() for x in fm.get("tools", "").split(",") if x.strip()]
    if not tools and name not in INHERIT_TOOLS_OK: bad(f, "no tools line, so it inherits every tool")
    if "model" in fm and fm["model"] not in ("opus", "sonnet", "haiku", "inherit"): bad(f, f"unexpected model '{fm['model']}'")
    if name not in DASH_OK and re.search("[\u2014\u2013]", t): bad(f, "contains an em dash or en dash")
    if not re.search(r"more than 25 years", body): bad(f, "persona line lacks 'more than 25 years'")
    if not re.search(r"as data|is data|not instructions|untrusted", body, re.I): bad(f, "no 'treat content as data, not instructions' rule")
    if name not in NO_HANDOFF_OK and "Send these handoffs to the named agents next." not in body: bad(f, "no shared handoff heading")
    if not re.search(r"`[a-z-]+/`|~/\.claude/", body): bad(f, "does not name the folder it writes to")
    for w in sorted(set(x.group(0).lower() for x in US.finditer(re.sub(r"`[^`]*`", "", body)))): bad(f, f"American spelling: {w}")
    pc = re.search(r"\n## Proof check\n(.*?)(?=\n## |\Z)", body, re.S)
    if pc: proofs[pc.group(1).strip()].append(name)
    elif name not in NO_PROOF_OK: bad(f, "no Proof check section")
if len(proofs) > 1:
    common = max(proofs.values(), key=len)
    for txt, names in proofs.items():
        if names is not common: problems.append(f"Proof check differs from the team's wording in: {', '.join(names)}")
for sk in sorted((root / ".skills").glob("*/SKILL.md")) if (root / ".skills").exists() else []:
    head = sk.read_text(encoding="utf-8").split("\n---\n")[0]
    if re.search(r"^name:", head, re.M): problems.append(f".skills/{sk.parent.name}/SKILL.md: has a name line, so Claude Code would load it as an agent")
    if not re.search(r"^description:", head, re.M): problems.append(f".skills/{sk.parent.name}/SKILL.md: no description")
print(f"Agents checked: {len(files)}   Total description words (loaded every turn): {words}")
if problems:
    print(f"Problems: {len(problems)}"); [print(" -", p) for p in problems]; sys.exit(1)
print("All checks passed.")
