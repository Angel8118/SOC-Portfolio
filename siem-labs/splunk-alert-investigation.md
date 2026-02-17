# 📡 Splunk Alert Investigation – Basic SIEM Analysis

---

## Overview
Security Information and Event Management (SIEM) platforms such as Splunk generate alerts when suspicious activity matches predefined detection rules.  
SOC analysts must investigate these alerts to determine whether they represent false positives, suspicious activity, or confirmed security incidents.

---

## Investigation Objective
The purpose of this investigation is to review a SIEM alert related to authentication activity and determine whether the detected behavior represents a legitimate security concern.

---

## Alert Details
- **SIEM Platform:** Splunk  
- **Alert Type:** Multiple Failed Login Attempts  
- **Detection Rule:** Excessive authentication failures detected within a short time period  
- **Affected System:** Authentication Server  
- **Severity:** Medium  

---

## Sample Log Evidence
2026-02-17 11:05:01 AUTH_FAIL user=jdoe ip=203.0.113.10

2026-02-17 11:05:05 AUTH_FAIL user=jdoe ip=203.0.113.10

2026-02-17 11:05:11 AUTH_FAIL user=jdoe ip=203.0.113.10

2026-02-17 11:05:18 AUTH_FAIL user=jdoe ip=203.0.113.10


---

## Investigation Steps

1. Validate the alert detection rule to confirm it triggered correctly.
2. Review the related authentication logs.
3. Identify the source IP address and affected user account.
4. Determine whether the activity shows a repeated or automated pattern.
5. Check whether a successful login occurred after the failed attempts.
6. Classify the activity based on investigation findings.

---

## Analysis
The logs indicate multiple failed authentication attempts targeting a single user account from the same IP address within a short time interval.  
This pattern is consistent with a potential **brute-force login attempt**.

---

## Classification
- **Type:** Suspicious Activity  
- **Severity:** Medium  
- **Potential Attack Type:** Brute Force Authentication Attempt  

---

## Recommended Actions
- Continue monitoring authentication activity from the source IP
- Implement temporary IP blocking if activity persists
- Notify security team if suspicious behavior escalates
- Enforce strong password policies and multi-factor authentication

---

## Conclusion
The SIEM alert correctly identified suspicious authentication activity consistent with repeated login failures. Continued monitoring and preventive controls are recommended to mitigate the risk of credential compromise.
