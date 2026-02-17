# 📊 Failed Login Pattern Analysis

---

## Overview
Analyzing failed login patterns is a key activity for SOC analysts, as repeated authentication failures often indicate malicious attempts to gain unauthorized access.  
Recognizing patterns such as brute-force attacks and password spraying allows analysts to quickly identify suspicious activity and prioritize investigations.

---

## Common Failed Login Patterns

### 1. Brute Force Attack Pattern
A brute-force attack typically targets **a single user account** with many password attempts in a short time period.

**Indicators:**
- Multiple failed login attempts for the same username
- Attempts occurring within seconds or minutes
- Attempts often originating from the same IP address

**Example:**
AUTH_FAIL user=jdoe ip=203.0.113.10

AUTH_FAIL user=jdoe ip=203.0.113.10

AUTH_FAIL user=jdoe ip=203.0.113.10


---

### 2. Password Spraying Pattern
Password spraying attacks attempt **one or a few common passwords across many user accounts**.

**Indicators:**
- Failed login attempts targeting multiple usernames
- Same IP address used across many accounts
- Attempts spread over time to avoid detection

**Example:**
AUTH_FAIL user=user1 ip=198.51.100.50

AUTH_FAIL user=user2 ip=198.51.100.50

AUTH_FAIL user=user3 ip=198.51.100.50


---

### 3. Suspicious Successful Login After Failures
A successful login occurring immediately after multiple failed attempts may indicate a **credential compromise**.

**Indicators:**
- Several failed login attempts followed by a successful authentication
- Same source IP performing both failed and successful logins

---

## Basic Investigation Steps
When analyzing failed login patterns, analysts should:

1. Identify the number of failed login attempts
2. Determine whether the attempts target single or multiple accounts
3. Review source IP addresses involved
4. Check whether any successful login occurred after failures
5. Escalate the activity if suspicious patterns are confirmed

---

## Importance for SOC Analysts
Recognizing failed login patterns enables SOC analysts to detect early-stage account compromise attempts, reduce the likelihood of unauthorized access, and improve the effectiveness of incident triage and response.
