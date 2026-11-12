#!/usr/bin/env python3
"""Find a project's dependency manifests, flag unpinned or missing lockfiles and unpinned CI actions, and run
whichever audit tools are already installed. Installs nothing and changes nothing.
Usage: python audit.py [project_dir]"""
import json, re, shutil, subprocess, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "."); issues = []
SKIP = {"node_modules", ".git", "vendor", "dist", "build", ".venv", "venv", "__pycache__"}
def find(name): return [p for p in root.rglob(name) if not SKIP & set(p.parts)]
def run(cmd, cwd):
    try: return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=180).stdout
    except Exception as e: return ""
for pj in find("package.json"):
    d = pj.parent; print(f"\nnpm project: {d}")
    try: pkg = json.loads(pj.read_text(encoding="utf-8"))
    except ValueError: issues.append(f"{pj}: not valid JSON"); continue
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    print(f"  Direct dependencies: {len(deps)}")
    if not any((d / l).exists() for l in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb")): issues.append(f"{d}: no lockfile, so installs are not repeatable")
    for n, v in deps.items():
        if re.match(r"^(\*|latest|git|http|github:)", str(v)): issues.append(f"{pj}: '{n}' is set to '{v}' (not a fixed, registry version)")
    scripts = pkg.get("scripts", {})
    for hook in ("preinstall", "install", "postinstall"):
        if hook in scripts: issues.append(f"{pj}: has a '{hook}' script that runs on install: read it")
    if shutil.which("npm") and (d / "package-lock.json").exists():
        try:
            v = json.loads(run(["npm", "audit", "--json"], d) or "{}").get("metadata", {}).get("vulnerabilities", {})
            print("  npm audit: " + ", ".join(f"{k} {v.get(k, 0)}" for k in ("critical", "high", "moderate", "low")))
            if v.get("critical") or v.get("high"): issues.append(f"{d}: npm audit reports {v.get('critical', 0)} critical and {v.get('high', 0)} high vulnerabilities")
        except ValueError: print("  npm audit: could not read the result")
    else: print("  npm audit: not run (npm or package-lock.json missing)")
for rq in find("requirements*.txt"):
    print(f"\nPython requirements: {rq}")
    for l in rq.read_text(errors="replace").splitlines():
        l = l.split("#")[0].strip()
        if l and not l.startswith("-") and "==" not in l and "@" not in l: issues.append(f"{rq}: '{l}' is not pinned to an exact version")
    if shutil.which("pip-audit"):
        out = run(["pip-audit", "-r", str(rq.name), "-f", "json"], rq.parent)
        try:
            n = sum(len(x.get("vulns", [])) for x in json.loads(out).get("dependencies", []))
            print(f"  pip-audit: {n} known vulnerabilities")
            if n: issues.append(f"{rq}: pip-audit reports {n} known vulnerabilities")
        except ValueError: print("  pip-audit: could not read the result")
    else: print("  pip-audit: not installed, so known vulnerabilities were NOT checked")
for other, tool in (("go.mod", "govulncheck"), ("Cargo.toml", "cargo-audit"), ("Gemfile", "bundler-audit"), ("composer.json", "composer audit"), ("pyproject.toml", "pip-audit")):
    for f in find(other): print(f"\n{other}: {f}  (check with {tool}; not run by this script)")
for wf in list(root.glob(".github/workflows/*.yml")) + list(root.glob(".github/workflows/*.yaml")):
    t = wf.read_text(errors="replace")
    for m in re.finditer(r"uses:\s*([\w./-]+)@([\w.-]+)", t):
        if not re.fullmatch(r"[0-9a-f]{40}", m.group(2)) and not m.group(1).startswith("./"): issues.append(f"{wf}: action {m.group(1)}@{m.group(2)} is not pinned to a commit SHA")
    if "pull_request_target" in t: issues.append(f"{wf}: uses pull_request_target, which runs with secrets on untrusted code: review carefully")
    if not re.search(r"^permissions:", t, re.M): issues.append(f"{wf}: no top-level permissions block, so the token may have more access than needed")
for df in find("Dockerfile*"):
    for m in re.finditer(r"(?im)^FROM\s+(\S+)", df.read_text(errors="replace")):
        img = m.group(1)
        if "@sha256:" not in img and (":" not in img or img.endswith(":latest")) and img.lower() != "scratch": issues.append(f"{df}: base image '{img}' has no fixed version")
print(f"\nThings to look at: {len(issues)}"); [print(" -", i) for i in issues]
print("\nThis is a first pass, not a clean bill of health: a tool that was not installed checked nothing.")
sys.exit(1 if issues else 0)
