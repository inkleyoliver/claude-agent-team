#!/usr/bin/env python3
"""Work out the UK GDPR 72-hour deadline for telling the ICO about a personal data breach.
The clock starts when the organisation became AWARE of the breach, not when it happened.
Usage: python clock.py "2026-11-12 09:30" [--tz Europe/London] [--now "2026-11-13 10:00"]"""
import argparse, sys
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
sys.stdout.reconfigure(encoding="utf-8")
p = argparse.ArgumentParser(); p.add_argument("aware"); p.add_argument("--tz", default="Europe/London"); p.add_argument("--now")
x = p.parse_args()
try: tz = ZoneInfo(x.tz)
except Exception: sys.exit(f"Unknown time zone '{x.tz}'. On Windows, run: pip install tzdata")
aware = datetime.fromisoformat(x.aware).replace(tzinfo=tz)
now = datetime.fromisoformat(x.now).replace(tzinfo=tz) if x.now else datetime.now(tz)
deadline = (aware.astimezone(ZoneInfo("UTC")) + timedelta(hours=72)).astimezone(tz)
left = deadline - now; f = "%A %d %B %Y, %H:%M %Z"
print(f"Became aware:  {aware.strftime(f)}")
print(f"ICO deadline:  {deadline.strftime(f)}  (72 hours, counted through weekends and bank holidays)")
if left.total_seconds() > 0:
    h = left.total_seconds() / 3600
    print(f"Time left:     {int(h)} hours {int(h % 1 * 60)} minutes")
    for label, hrs in (("Decide whether it is reportable by", 24), ("Have the draft notice with the human by", 48)):
        print(f"{label}: {(deadline - timedelta(hours=72 - hrs)).strftime(f)}")
else:
    print(f"OVERDUE by {int(-left.total_seconds() // 3600)} hours. Report now and include the reasons for the delay (Article 33(1)).")
print("A human decides whether to report and sends the notice. If people face a high risk, they must also be told without undue delay.")
