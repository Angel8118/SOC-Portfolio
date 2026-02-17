# TryHackMe Writeup – Agent Sudo

---

## Room Information
- **Platform:** TryHackMe
- **Room Name:** Agent Sudo
- **Difficulty:** Medium
- **Focus Area:** Privilege Escalation / Sudo Misconfiguration
- **Date Completed:** 2026-02-15

---

## Overview
This lab demonstrates how improper privilege configurations and incorrect handling of numeric user IDs in sudo policies can allow attackers to escalate privileges and obtain unauthorized root access. The scenario highlights the importance of proper sudo configuration, patching, and monitoring of privilege escalation activity.

---

## Initial Findings
During the enumeration phase, sudo permissions were inspected to determine whether any commands could be executed with elevated privileges. The system contained a sudo configuration that restricted the use of root but allowed execution of commands using numeric user identifiers.

---

## Vulnerability Identified
The system was vulnerable due to improper validation of numeric user identifiers in sudo command execution. By specifying a negative numeric UID value, the system incorrectly handled the request and allowed execution of commands with root-level privileges due to integer overflow/underflow behavior in certain sudo versions.

Example technique:
sudo -u#-1 /bin/bash


This resulted in execution of a shell with elevated privileges.

---

## Exploitation Summary (High-Level)
An attacker could exploit the improper UID validation by executing commands using specially crafted numeric identifiers, causing the system to incorrectly assign root privileges and allow unauthorized administrative access.

---

## Detection Opportunities
Security teams could detect similar attacks by monitoring:

- Unusual sudo command executions using numeric UID values
- Privilege escalation attempts recorded in authentication logs
- Suspicious shell spawning activity executed via sudo
- Repeated privilege escalation attempts from non-administrative users

Relevant logs:
- `/var/log/auth.log`
- sudo execution logs
- SIEM alerts related to privilege escalation behavior

---

## Mitigation Recommendations
- Update sudo to patched versions that properly validate UID inputs
- Restrict sudo permissions according to the principle of least privilege
- Monitor privileged command execution activity
- Implement logging and alerting for abnormal sudo usage patterns

---

## Lessons Learned
This lab demonstrates how subtle configuration errors and software vulnerabilities in privilege management tools can allow attackers to escalate privileges. Continuous patch management, strict privilege assignment, and monitoring of administrative command usage are essential to prevent unauthorized root access.
