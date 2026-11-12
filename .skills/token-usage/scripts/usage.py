#!/usr/bin/env python3
"""Total token use from Claude Code transcripts. Prints numbers and tool names only, never content.
Usage: python usage.py [transcript.jsonl | project_folder]   (default: every project in ~/.claude/projects, newest 20 sessions)"""
import json, sys, pathlib, collections
sys.stdout.reconfigure(encoding="utf-8")
arg = pathlib.Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else pathlib.Path("~/.claude/projects").expanduser()
files = [arg] if arg.is_file() else sorted(arg.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)[:20]
grand = collections.Counter(); results = []; reads = collections.Counter()
for f in files:
    c = collections.Counter(); tools = {}; seen = set()
    for line in f.open(encoding="utf-8", errors="replace"):
        try: e = json.loads(line)
        except ValueError: continue
        msg = e.get("message") or {}
        if not isinstance(msg, dict): continue
        u = msg.get("usage")
        if u and msg.get("id") not in seen:
            seen.add(msg.get("id"))
            for k in ("input_tokens", "output_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"): c[k] += u.get(k) or 0
        content = msg.get("content")
        for b in content if isinstance(content, list) else []:
            if not isinstance(b, dict): continue
            if b.get("type") == "tool_use":
                tools[b.get("id")] = b.get("name", "?")
                if b.get("name") == "Read": reads[(f.stem[:8], str((b.get("input") or {}).get("file_path", ""))[-60:])] += 1
            elif b.get("type") == "tool_result":
                size = len(json.dumps(b.get("content", ""), ensure_ascii=False))
                results.append((size, tools.get(b.get("tool_use_id"), "?"), f.stem[:8]))
    total_in = c["input_tokens"] + c["cache_read_input_tokens"] + c["cache_creation_input_tokens"]
    ratio = c["cache_read_input_tokens"] / total_in if total_in else 0
    print(f"{f.stem[:8]}  input {c['input_tokens']:>9,}  cache write {c['cache_creation_input_tokens']:>10,}  cache read {c['cache_read_input_tokens']:>11,}  output {c['output_tokens']:>8,}  cache-read share {ratio:.0%}")
    grand.update(c)
print(f"\nSessions: {len(files)}   Output tokens: {grand['output_tokens']:,}   Uncached input: {grand['input_tokens']:,}   Cache writes: {grand['cache_creation_input_tokens']:,}   Cache reads: {grand['cache_read_input_tokens']:,}")
print("\nLargest tool results (estimated tokens at 4 characters each):")
for size, tool, sess in sorted(results, reverse=True)[:10]: print(f"  ~{size // 4:>7,}  {tool:<20} session {sess}")
by = collections.Counter()
for size, tool, _ in results: by[tool] += size
print("\nTool results by tool (estimated tokens):")
for tool, size in by.most_common(8): print(f"  ~{size // 4:>8,}  {tool}")
rep = [(n, k) for k, n in reads.items() if n >= 3]
if rep:
    print("\nFiles read three or more times in one session:")
    for n, (sess, path) in sorted(rep, reverse=True)[:10]: print(f"  {n}x  ...{path}  (session {sess})")
