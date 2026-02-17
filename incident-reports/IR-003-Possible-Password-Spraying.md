# 🛡️ Incident Report – Possible Password Spraying Activity

---

## Report Information
**Report ID:** IR-003  
**Date:** 2026-02-17  
**Analyst:** Angel Alberto Campos Pelayo  

---

## 1. Incident Summary
Multiple failed authentication attempts were detected from a single external IP address targeting **multiple user accounts** within a short time period.  
This pattern is consistent with a **password spraying attack**, where attackers attempt commonly used passwords across many accounts to avoid account lockouts.

---

## 2. Event Details
- **Source IP:** 198.51.100.50  
- **Destination System:** Authentication Server  
- **Affected Users:** Multiple user accounts  
- **Event Type:** Authentication Failures  
- **Log Source:** Authentication Logs  
- **Detection Method:** Log pattern analysis  

---

## 3. Log Evidence
2026-02-17 10:05:11 AUTH_FAIL user=user1 ip=198.51.100.50

2026-02-17 10:05:18 AUTH_FAIL user=user2 ip=198.51.100.50

2026-02-17 10:05:24 AUTH_FAIL user=user3 ip=198.51.100.50

2026-02-17 10:05:30 AUTH_FAIL user=user4 ip=198.51.100.50


---

## 4. Analysis
The authentication logs show repeated login failures targeting **multiple user accounts** from the same source IP address.  
Unlike brute-force attacks that focus on a single account, this behavior indicates an attempt to test a small number of common passwords across many accounts, which is characteristic of **password spraying techniques**.

---

## 5. Classification
- **Type:** Alert / Suspicious Activity  
- **Severity Level:** Medium  
- **Attack Type:** Password Spraying  

---

## 6. MITRE ATT&CK Mapping
- **T1110.003 – Password Spraying**

---

## 7. Impact Assessment
If successful, password spraying attacks may result in unauthorized access to one or more user accounts, potentially allowing attackers to escalate privileges or move laterally within the network.

---

## 8. Recommended Actions
- Monitor authentication activity for additional login attempts from the same IP address  
- Implement temporary IP blocking if suspicious activity continues  
- Enforce strong password policies and account lockout controls  
- Enable **multi-factor authentication (MFA)** where possible  

---

## 9. Conclusion
Authentication failures targeting multiple user accounts from the same IP address indicate a **likely password spraying attempt**. Continued monitoring and preventive authentication controls are recommended to reduce the risk of account compromise.
