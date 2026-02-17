#!/usr/bin/env python3
"""
login-failure-parser.py
Simple SOC helper to analyze authentication log lines and detect:
- Brute Force (many failures against one user from one IP)
- Password Spraying (many users targeted from one IP)

Expected log format (examples):
2026-02-17 09:10:01 AUTH_FAIL user=jdoe ip=203.0.113.10
2026-02-17 09:10:20 LOGIN_SUCCESS user=jdoe ip=203.0.113.10

Usage:
  python scripts/login-failure-parser.py --file logs.txt
  python scripts/login-failure-parser.py --file logs.txt --json out.json
  python scripts/login-failure-parser.py --file logs.txt --window 10 --threshold 5
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime
from typing import Deque, Dict, List, Optional, Tuple

# Regex for the simple lab format used in your portfolio
LOG_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+"
    r"(?P<etype>AUTH_FAIL|LOGIN_SUCCESS)\s+user=(?P<user>[^\s]+)\s+ip=(?P<ip>[^\s]+)\s*$"
)

TS_FMT = "%Y-%m-%d %H:%M:%S"


@dataclass
class LogEvent:
    ts: datetime
    etype: str
    user: str
    ip: str


def parse_line(line: str) -> Optional[LogEvent]:
    m = LOG_RE.match(line.strip())
    if not m:
        return None
    try:
        ts = datetime.strptime(m.group("ts"), TS_FMT)
    except ValueError:
        return None
    return LogEvent(ts=ts, etype=m.group("etype"), user=m.group("user"), ip=m.group("ip"))


def load_events(path: str) -> List[LogEvent]:
    events: List[LogEvent] = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            ev = parse_line(line)
            if ev:
                events.append(ev)
    events.sort(key=lambda e: e.ts)
    return events


def analyze(
    events: List[LogEvent],
    window_minutes: int,
    fail_threshold: int,
    spray_user_threshold: int,
) -> Dict:
    """
    window_minutes: time window for detection
    fail_threshold: failures in window for brute-force suspicion (same user+ip)
    spray_user_threshold: distinct users targeted from same ip in window for spraying suspicion
    """
    window = deque()  # type: Deque[LogEvent]

    # Rolling counts inside the window
    fail_by_user_ip: Dict[Tuple[str, str], int] = defaultdict(int)
    users_by_ip: Dict[str, set] = defaultdict(set)
    fail_by_ip: Dict[str, int] = defaultdict(int)
    fail_by_user: Dict[str, int] = defaultdict(int)

    brute_force_hits = []  # list of dicts
    spraying_hits = []     # list of dicts

    def pop_old(current_ts: datetime):
        cutoff = current_ts.timestamp() - (window_minutes * 60)
        while window and window[0].ts.timestamp() < cutoff:
            old = window.popleft()
            if old.etype == "AUTH_FAIL":
                key = (old.user, old.ip)
                fail_by_user_ip[key] -= 1
                if fail_by_user_ip[key] <= 0:
                    del fail_by_user_ip[key]

                fail_by_ip[old.ip] -= 1
                if fail_by_ip[old.ip] <= 0:
                    del fail_by_ip[old.ip]

                fail_by_user[old.user] -= 1
                if fail_by_user[old.user] <= 0:
                    del fail_by_user[old.user]

                # users_by_ip set maintenance (safe rebuild for correctness if needed)
                # We'll keep it simple: rebuild users_by_ip for that ip from window when necessary
                if old.user in users_by_ip.get(old.ip, set()):
                    # Rebuild distinct users for this IP within the current window
                    s = set()
                    for e in window:
                        if e.ip == old.ip and e.etype == "AUTH_FAIL":
                            s.add(e.user)
                    if s:
                        users_by_ip[old.ip] = s
                    elif old.ip in users_by_ip:
                        del users_by_ip[old.ip]

    # Process events
    for ev in events:
        pop_old(ev.ts)
        window.append(ev)

        if ev.etype == "AUTH_FAIL":
            fail_by_user_ip[(ev.user, ev.ip)] += 1
            fail_by_ip[ev.ip] += 1
            fail_by_user[ev.user] += 1
            users_by_ip[ev.ip].add(ev.user)

            # Brute force: many failures for same user+ip within window
            if fail_by_user_ip[(ev.user, ev.ip)] == fail_threshold:
                brute_force_hits.append({
                    "type": "possible_bruteforce",
                    "ip": ev.ip,
                    "user": ev.user,
                    "failures_in_window": fail_threshold,
                    "window_minutes": window_minutes,
                    "first_seen": window[0].ts.strftime(TS_FMT),
                    "last_seen": ev.ts.strftime(TS_FMT),
                })

            # Password spraying: many distinct users from same ip within window
            if len(users_by_ip[ev.ip]) == spray_user_threshold:
                spraying_hits.append({
                    "type": "possible_password_spraying",
                    "ip": ev.ip,
                    "distinct_users_in_window": spray_user_threshold,
                    "window_minutes": window_minutes,
                    "users_sample": sorted(list(users_by_ip[ev.ip]))[:10],
                    "first_seen": window[0].ts.strftime(TS_FMT),
                    "last_seen": ev.ts.strftime(TS_FMT),
                })

    return {
        "summary": {
            "total_events": len(events),
            "total_auth_failures": sum(1 for e in events if e.etype == "AUTH_FAIL"),
            "total_login_success": sum(1 for e in events if e.etype == "LOGIN_SUCCESS"),
            "unique_ips_with_failures": len(set(e.ip for e in events if e.etype == "AUTH_FAIL")),
            "unique_users_targeted": len(set(e.user for e in events if e.etype == "AUTH_FAIL")),
        },
        "top_failed_ips": sorted(
            [{"ip": ip, "failures": cnt} for ip, cnt in fail_by_ip.items()],
            key=lambda x: x["failures"],
            reverse=True
        ),
        "top_targeted_users": sorted(
            [{"user": user, "failures": cnt} for user, cnt in fail_by_user.items()],
            key=lambda x: x["failures"],
            reverse=True
        ),
        "detections": {
            "possible_bruteforce": brute_force_hits,
            "possible_password_spraying": spraying_hits,
        },
        "parameters": {
            "window_minutes": window_minutes,
            "fail_threshold": fail_threshold,
            "spray_user_threshold": spray_user_threshold,
        }
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze auth logs for failed login patterns (SOC helper).")
    parser.add_argument("--file", required=True, help="Path to log file")
    parser.add_argument("--window", type=int, default=10, help="Time window in minutes (default: 10)")
    parser.add_argument("--threshold", type=int, default=5, help="Failures threshold for brute-force (default: 5)")
    parser.add_argument("--spray-users", type=int, default=5, help="Distinct user threshold for spraying (default: 5)")
    parser.add_argument("--json", dest="json_out", default=None, help="Write results to JSON file")
    args = parser.parse_args()

    events = load_events(args.file)
    if not events:
        print("No valid events parsed. Check log format.")
        return

    result = analyze(
        events=events,
        window_minutes=args.window,
        fail_threshold=args.threshold,
        spray_user_threshold=args.spray_users,
    )

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"[OK] Wrote JSON report to: {args.json_out}")
    else:
        # Console report
        s = result["summary"]
        print("\n=== Summary ===")
        for k, v in s.items():
            print(f"- {k}: {v}")

        print("\n=== Detections ===")
        bf = result["detections"]["possible_bruteforce"]
        ps = result["detections"]["possible_password_spraying"]

        if not bf and not ps:
            print("No detections triggered with current parameters.")
        else:
            for item in bf:
                print(f"[BruteForce?] ip={item['ip']} user={item['user']} "
                      f"failures_in_window={item['failures_in_window']} window={item['window_minutes']}m "
                      f"first_seen={item['first_seen']} last_seen={item['last_seen']}")
            for item in ps:
                print(f"[Spraying?] ip={item['ip']} distinct_users_in_window={item['distinct_users_in_window']} "
                      f"window={item['window_minutes']}m users_sample={item['users_sample']} "
                      f"first_seen={item['first_seen']} last_seen={item['last_seen']}")

        print("\n=== Notes ===")
        print("Tune --window / --threshold / --spray-users based on environment baselines.")

if __name__ == "__main__":
    main()
