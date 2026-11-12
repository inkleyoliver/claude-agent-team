#!/usr/bin/env python3
"""Service level arithmetic.
  python slo.py budget 99.9 [--days 30]                       -> downtime allowed by an availability target
  python slo.py burn 99.9 --total 1200000 --failed 900 [--days 30] [--elapsed 12]   -> error budget used so far
  python slo.py percentiles times.txt                         -> p50, p95, p99 from a file of response times (one number per line)"""
import sys, math, pathlib
sys.stdout.reconfigure(encoding="utf-8")
a = sys.argv[1:]
def opt(name, default):
    return float(a[a.index(name) + 1]) if name in a else default
def dur(mins):
    return f"{mins / 1440:.1f} days" if mins >= 2880 else f"{mins / 60:.1f} hours" if mins >= 120 else f"{mins:.1f} minutes" if mins >= 2 else f"{mins * 60:.0f} seconds"
if len(a) >= 2 and a[0] == "budget":
    t = float(a[1]); days = opt("--days", 30); bad = (100 - t) / 100
    print(f"{t}% availability allows {dur(days * 1440 * bad)} of downtime in {days:g} days ({dur(1440 * bad)} a day, {dur(365 * 1440 * bad)} a year).")
elif len(a) >= 2 and a[0] == "burn":
    t = float(a[1]); total = opt("--total", 0); failed = opt("--failed", 0); days = opt("--days", 30); elapsed = opt("--elapsed", days)
    allowed = total * (100 - t) / 100 * (days / elapsed); used = failed / allowed if allowed else float("inf"); rate = used / (elapsed / days)
    print(f"Success rate so far: {100 * (1 - failed / total):.3f}% against a target of {t}%")
    print(f"Error budget used: {used:.0%} with {elapsed / days:.0%} of the period gone (burn rate {rate:.1f}x)")
    print("On track." if rate <= 1 else f"Burning too fast: at this rate the budget runs out on day {days / rate:.0f} of {days:g}." if used < 1 else "Budget spent: the target is missed for this period. Reliability work should come before new features.")
elif len(a) == 2 and a[0] == "percentiles":
    v = sorted(float(l) for l in pathlib.Path(a[1]).read_text().split() if l.strip())
    q = lambda p: v[min(len(v) - 1, math.ceil(p / 100 * len(v)) - 1)]
    print(f"Samples: {len(v)}   p50 {q(50):g}   p95 {q(95):g}   p99 {q(99):g}   max {v[-1]:g}   mean {sum(v) / len(v):.1f}")
else: sys.exit(__doc__)
