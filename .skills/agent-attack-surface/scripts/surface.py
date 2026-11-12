#!/usr/bin/env python3
"""Static map of what each agent could do if it were manipulated: its tools, what it reads from outside, and missing safeguards.
Reads agent files only; runs nothing. Usage: python surface.py [agents_dir]   (default: ~/.claude/agents)"""
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "~/.claude/agents").expanduser(); notes = []
print(f"{'Agent':<24}{'Model':<9}{'Shell':<7}{'Write':<7}{'Edit':<6}{'Web':<5}{'Agents':<8}Reads outside content")
for f in sorted(root.glob("*.md")):
    t = f.read_text(encoding="utf-8"); m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if not m: continue
    fm = dict((k.strip(), v.strip()) for k, v in (l.split(":", 1) for l in m.group(1).splitlines() if ":" in l and not l.startswith(" ")))
    body = m.group(2); name = fm.get("name", f.stem); tools = [x.strip() for x in fm.get("tools", "").split(",") if x.strip()]
    has = lambda x: any(tl.split("(")[0] == x for tl in tools) or not tools
    web = has("WebFetch") or has("WebSearch"); outside = web or bool(re.search(r"(?i)feedback|support tickets|issues?\b|web pages|pull requests|third-party|survey|exports?\b|transcripts", fm.get("description", "") + body[:3000]))
    y = lambda b: "yes" if b else "-"
    print(f"{name:<24}{fm.get('model', 'session'):<9}{y(has('Bash')):<7}{y(has('Write')):<7}{y(has('Edit')):<6}{y(web):<5}{y(has('Agent')):<8}{y(outside)}")
    if not tools: notes.append(f"{name}: no tools line, so it inherits every tool, including connectors")
    if web and has("Bash") and (has("Write") or has("Edit")): notes.append(f"{name}: reads the web and can run commands and write files. Web content could try to steer both; test indirect injection here first")
    if has("Agent") and name != "chief-of-staff": notes.append(f"{name}: can start other agents, which the team reserves for the chief-of-staff")
    if has("Edit") and not re.search(r"(?i)only .{0,80}(edit|write)|write only|never (edit|change)|you may use `Edit` only", body): notes.append(f"{name}: can edit files but states no limit on which")
    if not re.search(r"(?i)as data|is data|not instructions|untrusted", body): notes.append(f"{name}: no 'content is data, not instructions' rule")
    if not re.search(r"(?i)human-in-the-loop|approv", body): notes.append(f"{name}: never mentions approval or human-in-the-loop")
print(f"\nPoints to test: {len(notes)}"); [print(" -", n) for n in notes]
print("\nThis reads what the files say, not how the agents behave. Each point is a place to test, not a finding.")
