#!/usr/bin/env python3
"""Scan for committed secrets. Never prints a full secret. Exit 1 if anything is found.
Usage: python secret_scan.py [--staged | --diff <ref> | --all]   (default: changes against HEAD plus untracked files)"""
import re, subprocess, sys, pathlib, math
sys.stdout.reconfigure(encoding="utf-8")
RULES = [
 ("Private key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
 ("AWS access key ID", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
 ("GitHub token", r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{50,}\b"),
 ("Stripe live key", r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}\b"),
 ("Slack token", r"\bxox[abpors]-[A-Za-z0-9-]{10,}\b"),
 ("Anthropic or OpenAI key", r"\bsk-(?:ant-|proj-)?[A-Za-z0-9_-]{32,}\b"),
 ("Google API key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
 ("JSON Web Token", r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\b"),
 ("Connection string with password", r"\b[a-z][a-z0-9+]{2,}://[^\s:/@'\"]+:[^\s@'\"]{3,}@[^\s'\"]+"),
 ("Secret exposed to the browser", r"\b(?:NEXT_PUBLIC|VITE|REACT_APP)_[A-Z0-9_]*(?:SECRET|PRIVATE|PASSWORD|SERVICE_ROLE)[A-Z0-9_]*\s*="),
]
ASSIGN = re.compile(r"(?i)\b([a-z0-9_.-]*(?:secret|token|passw(?:or)?d|api[_-]?key|private[_-]?key|credential|auth)[a-z0-9_.-]*)\b\s*[:=]\s*[\"']([^\"'\s]{12,})[\"']")
PLACEHOLDER = re.compile(r"(?i)example|changeme|placeholder|your[_-]|xxx+|<.*>|\$\{|dummy|test|fake|sample|redacted|\*\*\*|process\.env|os\.environ")
RISKY_FILES = re.compile(r"(^|/)(\.env(\..+)?|id_rsa|id_ed25519|.*\.pem|.*\.key|.*\.p12|.*\.pfx|credentials(\.json)?|.*\.keystore)$")
def entropy(s): return -sum(s.count(c)/len(s)*math.log2(s.count(c)/len(s)) for c in set(s))
def mask(s): return s[:6] + "..." + s[-4:] if len(s) > 14 else s[:3] + "..."
def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, errors="replace").stdout
mode = sys.argv[1] if len(sys.argv) > 1 else ""
lines = []   # (file, lineno, text)
if mode == "--all":
    for f in git("ls-files").splitlines():
        try:
            for i, l in enumerate(pathlib.Path(f).read_text(errors="replace").splitlines(), 1): lines.append((f, i, l))
        except OSError: pass
    names = git("ls-files").splitlines()
else:
    args = ["diff", "--cached", "-U0"] if mode == "--staged" else ["diff", "-U0", sys.argv[2] if mode == "--diff" else "HEAD"]
    f, n = "?", 0
    for l in git(*args).splitlines():
        if l.startswith("+++ "): f = l[6:] if l.startswith("+++ b/") else l[4:]
        elif l.startswith("@@"): n = int(re.search(r"\+(\d+)", l).group(1)) - 1
        elif l.startswith("+"): n += 1; lines.append((f, n, l[1:]))
    untracked = git("ls-files", "--others", "--exclude-standard").splitlines() if mode != "--staged" else []
    for u in untracked:
        try:
            for i, l in enumerate(pathlib.Path(u).read_text(errors="replace").splitlines(), 1): lines.append((u, i, l))
        except OSError: pass
    names = sorted({x[0] for x in lines} | set(untracked))
found = []
for f in names:
    if RISKY_FILES.search(f) and not f.endswith((".example", ".sample", ".template")): found.append((f, 0, "File that usually holds secrets is tracked or about to be", ""))
for f, n, l in lines:
    if len(l) > 2000: continue
    for label, rx in RULES:
        for m in re.finditer(rx, l):
            if not PLACEHOLDER.search(m.group(0)): found.append((f, n, label, mask(m.group(0))))
    for m in ASSIGN.finditer(l):
        v = m.group(2)
        if not PLACEHOLDER.search(v) and not PLACEHOLDER.search(l) and entropy(v) >= 3.5: found.append((f, n, f"High-entropy value assigned to '{m.group(1)}'", mask(v)))
gi = pathlib.Path(".gitignore").read_text(errors="replace") if pathlib.Path(".gitignore").exists() else ""
if ".env" not in gi: print("Note: .gitignore has no .env rule.")
print(f"Lines scanned: {len(lines)}   Possible secrets: {len(found)}")
for f, n, label, shown in sorted(set(found)): print(f" - {f}:{n}: {label} {shown}".rstrip())
if found: print("If any of these is real and was ever committed, removing it is not enough: it must be rotated."); sys.exit(1)
