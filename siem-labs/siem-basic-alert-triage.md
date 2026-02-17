# 📡 SIEM Basic Alert Triage Process

---

## Overview
Security Information and Event Management (SIEM) platforms generate large volumes of alerts based on predefined detection rules.  
SOC analysts must perform **alert triage** to determine whether an alert represents normal activity, suspicious behavior, or a confirmed security incident.

---

## Objective
The objective of SIEM alert triage is to quickly evaluate alerts, validate their accuracy, determine potential impact, and prioritize response actions based on severity.

---

## Basic Alert Triage Workflow

### Step 1 – Alert Validation
Confirm that the alert was generated correctly and corresponds to the intended detection rule.

**Actions:**
- Review alert description
- Verify detection rule conditions
- Confirm relevant log sources

---

### Step 2 – Context Gathering
Collect additional information related to the alert to better understand the activity.

**Actions:**
- Identify affected user, host, or system
- Review related log entries
- Determine source IP addresses involved

---

### Step 3 – Event Correlation
Check whether related events exist that indicate a broader suspicious pattern.

**Actions:**
- Search for similar alerts
- Correlate authentication, network, or system logs
- Identify repeated or automated behavior

---

### Step 4 – Classification
Determine whether the alert should be classified as:

- Informational Event
- Suspicious Activity
- Confirmed Security Incident

Assign an initial **severity level** based on potential impact.

---

### Step 5 – Documentation and Escalation
Document findings clearly and escalate the alert if necessary.

**Actions:**
- Record investigation results
- Assign severity level
- Escalate to higher-level analysts if incident is confirmed

---

## Importance for SOC Analysts
A structured alert triage process allows SOC teams to efficiently manage large volumes of alerts, reduce false positives, and ensure that critical threats are prioritized for investigation and response.
