#!/usr/bin/env python3
"""Business case arithmetic: net present value, payback and a sensitivity table. The numbers in are assumptions; show them.
  python case.py --upfront 20000 --benefit 1500 --running 400 --months 36 [--rate 0.035] [--ramp 6]
--benefit and --running are per month. --rate is the yearly discount rate. --ramp is months for benefits to reach full level."""
import argparse, sys
sys.stdout.reconfigure(encoding="utf-8")
p = argparse.ArgumentParser()
for n, d in (("upfront", None), ("benefit", None), ("running", 0.0), ("rate", 0.035)): p.add_argument("--" + n, type=float, default=d, required=d is None)
p.add_argument("--months", type=int, default=36); p.add_argument("--ramp", type=int, default=0)
x = p.parse_args()
def run(upfront, benefit, running, months=x.months):
    m_rate = (1 + x.rate) ** (1 / 12) - 1; npv = -upfront; cum = -upfront; payback = None
    for m in range(1, months + 1):
        b = benefit * (min(m / x.ramp, 1) if x.ramp else 1); net = b - running
        npv += net / (1 + m_rate) ** m; cum += net
        if payback is None and cum >= 0: payback = m
    return npv, payback, cum
def show(label, r): print(f"{label:<34} NPV {r[0]:>12,.0f}   payback {(str(r[1]) + ' months') if r[1] else 'not within the period':<22} net cash {r[2]:>12,.0f}")
base = run(x.upfront, x.benefit, x.running)
print(f"Assumptions: upfront {x.upfront:,.0f}; benefit {x.benefit:,.0f} a month; running cost {x.running:,.0f} a month; {x.months} months; discount rate {x.rate:.1%} a year; ramp {x.ramp} months\n")
show("Base case", base)
print("\nSensitivity (one thing changed at a time):")
for label, r in (("Benefits 20% lower", run(x.upfront, x.benefit * 0.8, x.running)), ("Benefits 50% lower", run(x.upfront, x.benefit * 0.5, x.running)),
                 ("Upfront cost 30% higher", run(x.upfront * 1.3, x.benefit, x.running)), ("Running cost 50% higher", run(x.upfront, x.benefit, x.running * 1.5)),
                 ("Benefits 20% lower, costs 30% higher", run(x.upfront * 1.3, x.benefit * 0.8, x.running * 1.3))): show(label, r)
life = x.upfront + x.running * x.months
be = life / x.months
print(f"\nBreak-even benefit: {be:,.0f} a month over {x.months} months (before discounting). Your figure is {x.benefit / be:.1f} times that." if be else "")
