#!/usr/bin/env python3
"""A/B test maths for two proportions, using only the standard library.
  python abtest.py size --baseline 0.10 --mde 0.02 [--alpha 0.05] [--power 0.8] [--daily 400]
  python abtest.py analyse --a 120/1000 --b 150/1010 [--alpha 0.05] [--split 0.5]
--mde is the absolute change that would matter (0.02 = 2 percentage points). --a and --b are conversions/users."""
import argparse, math, sys
from statistics import NormalDist
sys.stdout.reconfigure(encoding="utf-8")
N = NormalDist()
p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
s = sub.add_parser("size"); s.add_argument("--baseline", type=float, required=True); s.add_argument("--mde", type=float, required=True)
s.add_argument("--alpha", type=float, default=0.05); s.add_argument("--power", type=float, default=0.8); s.add_argument("--daily", type=float)
a = sub.add_parser("analyse"); a.add_argument("--a", required=True); a.add_argument("--b", required=True)
a.add_argument("--alpha", type=float, default=0.05); a.add_argument("--split", type=float, default=0.5)
x = p.parse_args()
if x.cmd == "size":
    p1, p2 = x.baseline, x.baseline + x.mde
    if not (0 < p1 < 1 and 0 < p2 < 1): sys.exit("baseline and baseline + mde must be between 0 and 1")
    n = math.ceil((N.inv_cdf(1 - x.alpha / 2) + N.inv_cdf(x.power)) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p1 - p2) ** 2)
    print(f"Sample size: {n} per variant ({2 * n} in total) to detect {p1:.2%} to {p2:.2%}, alpha {x.alpha} two-sided, power {x.power:.0%}")
    if x.daily:
        days = math.ceil(2 * n / x.daily); weeks = math.ceil(days / 7)
        print(f"Duration: {days} days at {x.daily:g} users a day; run for {weeks} whole week(s) ({weeks * 7} days)")
else:
    (ca, na), (cb, nb) = [tuple(int(v) for v in t.split("/")) for t in (x.a, x.b)]
    tot = na + nb; ea, eb = tot * x.split, tot * (1 - x.split)
    chi = (na - ea) ** 2 / ea + (nb - eb) ** 2 / eb
    srm_p = 2 * (1 - N.cdf(math.sqrt(chi)))
    print(f"Sample ratio check: A {na}, B {nb}, expected {ea:.0f} and {eb:.0f}, p = {srm_p:.4f}")
    if srm_p < 0.001: print("FAILED: sample ratio mismatch. Stop and investigate the allocation before reading any result."); sys.exit(1)
    pa, pb = ca / na, cb / nb; diff = pb - pa
    pool = (ca + cb) / tot; se0 = math.sqrt(pool * (1 - pool) * (1 / na + 1 / nb))
    z = diff / se0 if se0 else 0.0; pv = 2 * (1 - N.cdf(abs(z)))
    se = math.sqrt(pa * (1 - pa) / na + pb * (1 - pb) / nb); h = N.inv_cdf(1 - x.alpha / 2) * se
    print(f"A: {pa:.2%} ({ca}/{na})   B: {pb:.2%} ({cb}/{nb})")
    print(f"Difference (B minus A): {diff:+.2%} points, {1 - x.alpha:.0%} confidence interval {diff - h:+.2%} to {diff + h:+.2%}")
    if pa: print(f"Relative change: {diff / pa:+.1%}")
    print(f"z = {z:.2f}, p = {pv:.4f}: {'statistically significant' if pv < x.alpha else 'not statistically significant'} at alpha {x.alpha}")
    print("Check this against the pre-registered minimum effect before calling it a win. With several metrics, apply the Holm correction.")
