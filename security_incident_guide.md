# Incident Prevention, Detection, and Response Guide
A concise operational guide to prevent, detect, and respond to five incident types:
RansomLock Attack (ransomware/extortion), SQL Breach, DDoS Storm,
Privilege Escalation, and Credential Leak.

---

## Table of Contents
1. Global Controls (apply to all incidents)
2. RansomLock Attack
3. SQL Breach
4. DDoS Storm
5. Privilege Escalation
6. Credential Leak
7. Playbooks and Runbooks
8. Post-Incident: Recovery and Lessons Learned
9. Quick Checklists

---

## 1. Global Controls
**Objective:** reduce attack surface, detect anomalies early, shorten mean time to contain.

- **Backups**
  - Immutable, air-gapped snapshots.
  - RPO/RTO aligned to business impact.
  - Quarterly restore tests and integrity checks.
- **Patch Management**
  - Prioritize critical patches within 1–7 days.
  - Staged rollout and automated rollback.
- **Identity**
  - Enforce MFA for all administrative and cloud console access.
  - Implement least privilege and periodic access reviews.
  - Just-in-time (JIT) privilege elevation.
- **Logging & Monitoring**
  - Centralized logging: auth, application, DB, network, EDR telemetry.
  - Retain logs 90+ days; store immutable copies.
  - SIEM with alerts and workflows.
- **Network**
  - Strong segmentation: separate internet-facing, app, DB, backup, and admin zones.
  - Zero Trust model for east-west traffic.
- **Endpoint & App Protection**
  - EDR/XDR with containment and telemetry.
  - WAF, RASP, and runtime protections for apps.
  - Application allowlisting where feasible.
- **Secrets Management**
  - Vault solutions for credentials and keys.
  - No secrets in code or config repos.
- **Supply Chain**
  - Vendor security requirements in contracts.
  - Third-party risk assessments and logging integration.
- **Training & Exercises**
  - Quarterly phishing simulation.
  - Tabletop IR exercises twice per year.

---

## 2. RansomLock Attack
**Overview:** Malware that encrypts or exfiltrates data to extort organizations.

**Prevention**
- Immutable, offline backups.
- Restrict write privileges on file shares.
- EDR with behavioral detection and rollback.
- Disable SMBv1; restrict SMB access to approved hosts.
- Macro/attachment controls in email gateway.
- Application allowlisting for critical hosts.

**Detection**
- Rapid, mass file modifications or high file I/O.
- Unusual process spawning (e.g., Office -> cmd/PowerShell).
- EDR alerts for known ransomware behaviors.
- Presence of ransom notes or staged archives.

**Immediate Response (Containment)**
1. Isolate affected hosts and network segments.
2. Quarantine suspected malware via EDR.
3. Disable lateral movement mechanisms (admin shares, RDP).
4. Preserve forensic images and logs.
5. Suspend backup connections to affected systems.

**Eradication & Recovery**
- Rebuild systems from clean images where necessary.
- Restore from validated immutable backups.
- Rotate credentials and secrets for impacted accounts.
- Apply patches and hardening fixes.

**Legal & Communications**
- Notify legal and compliance; follow breach notification laws.
- Prepare external communications and coordination with law enforcement.

---

## 3. SQL Breach
**Overview:** Exploitation of application or DB vulnerabilities leading to unauthorized access or exfiltration.

**Prevention**
- Parameterized queries and ORMs. No dynamic SQL built from user input.
- WAF tuned for SQLi patterns.
- Network ACLs: DB accessible only from app tiers.
- Least-privilege DB accounts and role separation.
- Column-level encryption for sensitive data.
- SAST/DAST in CI/CD pipeline.

**Detection**
- Unexpected large `SELECT` queries or export patterns.
- New DB connections from unusual IPs or service identities.
- Abnormal query timing or heavy scan activity.
- Alerts from Database Activity Monitoring (DAM) or SIEM.

**Immediate Response**
1. Block offending source IPs and app instances via network controls.
2. Snapshot the DB for forensic analysis.
3. Rotate compromised application and DB credentials.
4. Patch vulnerable application code or components immediately.
5. Assess data exfiltration scope and notify stakeholders.

**Remediation**
- Apply secure coding fixes and deploy with tests.
- Perform focused pentest on affected app area.
- Harden DB access and review roles.

---

## 4. DDoS Storm
**Overview:** Overwhelming traffic or request floods to degrade or deny service.

**Prevention**
- Use CDN and DDoS mitigation services (Cloudflare, AWS Shield, Azure DDoS).
- Rate limiting, SYN cookies, and connection limits at edge.
- Design for elasticity: autoscaling and queueing at application layer.
- Cache static content at CDN.
- Separate control plane and data plane endpoints.

**Detection**
- Sudden spike in inbound traffic from many sources.
- High connection counts and SYN flood patterns.
- Increased error rates (5xx) and elevated latency.

**Immediate Response**
1. Activate DDoS mitigation provider protections or redirect via scrubbing center.
2. Apply traffic filters and rate limits at WAF/CDN.
3. Throttle or disable non-essential features to reduce load.
4. If applicable, shift traffic to alternate regions.

**Post-Attack**
- Analyze attack vectors and signatures.
- Update mitigation rules and prepare a traffic whitelist for critical clients.

---

## 5. Privilege Escalation
**Overview:** Unauthorized elevation of privileges on hosts or services.

**Prevention**
- Patch OS and SUID binaries promptly.
- Use least-privilege and JIT access.
- Restrict sudoers and use role-based access control.
- Use MFA for privileged sessions and require bastion hosts for admin access.
- Apply kernel hardening and exploit mitigations.

**Detection**
- Unexpected use of `sudo` or elevation APIs.
- New administrative accounts or changes in group memberships.
- Creation of persistent backdoors or scheduled tasks.
- EDR alerts on suspicious process injections or token manipulations.

**Immediate Response**
1. Disable compromised admin accounts and revoke sessions.
2. Revoke tokens and rotate affected secrets.
3. Snapshot and isolate affected hosts.
4. Investigate lateral movement and privilege abuse path.

**Remediation**
- Remove unauthorized accounts, revert unauthorized changes.
- Harden permission models and remove excessive rights.
- Conduct root cause analysis and remediate vulnerabilities.

---

## 6. Credential Leak
**Overview:** Exposure of passwords, API keys, or tokens via code, repos, or logs.

**Prevention**
- Centralized secrets management and short-lived tokens.
- Pre-commit and CI secret scanning.
- No credentials in plaintext in repos, configs, or logs.
- Enforce MFA and monitor for leaked credentials.

**Detection**
- Repo scanning alerts and external leak monitoring (paste sites, public repos).
- Login anomalies and sudden authentication failures or bursts.
- SIEM alerts for token misuse.

**Immediate Response**
1. Revoke leaked secrets and rotate keys immediately.
2. Invalidate sessions and force password resets for affected users.
3. Search codebases and infra for other instances of the secret.
4. If API keys leaked, restrict scopes and issue replacements.

**Remediation**
- Strengthen secret rotation and audit schedules.
- Harden CI/CD pipelines and secret handling.
- Educate developers on secure secrets usage.

---

## 7. Playbooks and Runbooks (templates)
Use the following minimal runbook structure per incident type.

**Runbook: [Incident Type]**
- **Trigger:** (example: EDR ransomware detection)
- **Owner:** (team/person)
- **Initial Actions (0–15 min):** isolate host, gather volatile logs, notify IR lead.
- **Containment actions (15–120 min):** network isolation, block credentials, engage provider.
- **Forensics (2–24 hrs):** snapshot, collect logs, timeline activity.
- **Recovery (24–72 hrs):** restore from backups, apply fixes, monitor.
- **Communication:** legal, leadership, customers, regulators.
- **Post-mortem:** timeline, root cause, mitigations, lessons.

---

## 8. Post-Incident: Recovery and Lessons Learned
- Conduct structured post-mortem within 7 days.
- Record timeline, decisions, and evidence.
- Track remediation as action items with owners and deadlines.
- Update playbooks and run tabletop exercises for the same scenario.

---

## 9. Quick Checklists
**Daily**
- SIEM health checks.  
- Backup success verification.  
- MFA and critical alerts review.

**Weekly**
- Patch status and exceptions.  
- High-risk account access review.

**Monthly**
- Restore test for backups.  
- Phishing simulation result review.

**Quarterly**
- Tabletop IR exercise.  
- External pentest or red-team exercise.

---

### Appendix: Useful Commands and Tools
- EDR: isolate host, export forensic image.  
- DB: `pg_dump --schema-only` or snapshot, audit logs.  
- Network: ACL update, iptables rules, cloud security groups.  
- Secrets: rotate keys via vault API.

---

*This document is intentionally concise and operational. Integrate it into your incident response platform and adapt runbooks to your environment.*
