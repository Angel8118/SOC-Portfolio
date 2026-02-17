# Scripts – SOC Helper Tools

This folder contains simple scripts developed to support **basic security log analysis** and **authentication activity investigation**.  
These tools are intended for educational and portfolio demonstration purposes, simulating small automation tasks commonly performed by SOC analysts.

---

## Available Scripts

### login-failure-parser.py
Analyzes authentication log entries to detect suspicious failed login patterns such as:

- Possible brute-force attempts (multiple failures targeting a single account)
- Possible password spraying (multiple accounts targeted from the same IP)
- Authentication failure statistics by user and IP address

---

## Example Usage

Run the script using a log file:

python login-failure-parser.py --file logs.txt


Generate a JSON output report:

python login-failure-parser.py --file logs.txt --json report.json


Adjust detection thresholds:

python login-failure-parser.py --file logs.txt --window 10 --threshold 5


---

## Example Log Format

2026-02-17 09:10:01 AUTH_FAIL user=jdoe ip=203.0.113.10

2026-02-17 09:10:05 AUTH_FAIL user=jdoe ip=203.0.113.10

2026-02-17 09:10:11 AUTH_FAIL user=jdoe ip=203.0.113.10

2026-02-17 09:10:20 LOGIN_SUCCESS user=jdoe ip=203.0.113.10


---

## Purpose
The objective of these scripts is to demonstrate:

- Basic log parsing automation
- Pattern detection for authentication attacks
- Security analysis workflow automation at an entry-level SOC perspective
