# 🛡️ Incident Report – Suspicious Login Activity After Multiple Failures

---

## Report Information
**Report ID:** IR-002  
**Date:** 2026-02-02 
**Analyst:** Angel Alberto Campos Pelayo  

---

## 1. Incident Summary
Multiple failed login attempts were observed for a user account, followed by a **successful authentication** from the same source IP address.  
This pattern suggests a potential **credential compromise** resulting from repeated password guessing attempts.

---

## 2. Event Details
- **Source IP:** 203.0.113.10  
- **Destination System:** Authentication Server  
- **Affected User:** jdoe  
- **Event Type:** Authentication Attempts  
- **Log Source:** Authentication Logs  
- **Detection Method:** Manual log analysis  

---

## 3. Log Evidence
2026-02-17 09:10:01 AUTH_FAIL user=jdoe ip=203.0.113.10
2026-02-17 09:10:05 AUTH_FAIL user=jdoe ip=203.0.113.10
2026-02-17 09:10:11 AUTH_FAIL user=jdoe ip=203.0.113.10
2026-02-17 09:10:20 LOGIN_SUCCESS user=jdoe ip=203.0.113.10

---

## 4. Analysis
The logs show **repeated authentication failures** targeting the same user account, followed shortly by a successful login from the same IP address.  
This sequence suggests that the attacker may have successfully guessed or obtained the correct password after multiple attempts, indicating a **possible credential compromise**.

---

## 5. Classification
- **Type:** Incident  
- **Severity Level:** Medium  
- **Attack Type:** Suspicious Login / Possible Credential Compromise  

---

## 6. MITRE ATT&CK Mapping
- **T1110 – Brute Force**  
- **T1078 – Valid Accounts**  

---

## 7. Impact Assessment
If the credentials were compromised, unauthorized access to the affected account could allow attackers to access sensitive systems or perform additional malicious actions.

---

## 8. Recommended Actions
- Force password reset for the affected account  
- Review account activity following the successful login  
- Monitor for additional suspicious login attempts  
- Consider enabling **multi-factor authentication (MFA)**  

---

## 9. Conclusion
Repeated failed login attempts followed by a successful authentication from the same IP address indicate a **likely credential compromise scenario**. Immediate monitoring and account security measures are recommended.