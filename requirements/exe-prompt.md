# MASTER DEVELOPMENT PROMPT

## Offline Malware Analysis System

You are a Senior Python Software Engineer, Malware Analysis Platform Architect, and Cybersecurity Product Developer.

Build a professional Offline Malware Analysis System consisting of Static Analysis and Dynamic Analysis modules.

The platform must operate entirely offline in an air-gapped environment.

No cloud services, external APIs, VirusTotal integration, online reputation services, or internet connectivity may be used.

The system must be modular, scalable, maintainable, and suitable for future expansion.

---

# PROJECT OBJECTIVE

Develop a desktop-based malware analysis platform capable of:

* Static Malware Analysis
* Dynamic Malware Analysis
* Evidence Collection
* Behavioral Detection
* PDF Report Generation

The platform should support future expansion without architectural redesign.

---

# TECHNOLOGY STACK

Language:

* Python 3.14+

GUI:

* PySide6

PDF Generation:

* ReportLab

Static Analysis Libraries:

* pefile
* yara-python
* hashlib
* re
* xml
* zipfile

Dynamic Analysis Components:

* Sysmon
* TShark
* Python Sandbox Agent

Virtualization:

* VMware Workstation

---

# STORAGE MODEL

Use directory-based storage.

No database in the initial version.

Store:

storage/

├── samples/
├── static_results/
├── dynamic_results/
├── reports/
└── logs/

All analysis results should be stored as JSON.

Reports should be stored as PDF.

The architecture must allow future integration of SQLite without requiring major redesign.

---

# SUPPORTED FILE TYPES

Static Analysis:

* .exe
* .dll
* .zip

Dynamic Analysis:

* .exe
* .dll

ZIP archives must support recursive extraction up to 3 levels.

---

# SYSTEM ARCHITECTURE

Host Machine

├── VM A (Analyst Workstation)
│
│   Malware Analysis Platform
│
└── VM B (Sandbox)
Windows 10
Sysmon
TShark
Sandbox Agent

Communication:

* Host-Only VMware Network
* No Internet
* No Cloud
* No Shared Folders
* No SMB Shares

---

# GUI ARCHITECTURE

Framework:
PySide6

Navigation:

* Dashboard
* Static Analysis
* Dynamic Analysis
* Reports
* Settings

Use:

* QMainWindow
* QStackedWidget
* QThread

The GUI must never perform analysis directly.

All analysis must be performed through controller classes.

---

# STATIC ANALYSIS MODULES

## Intake Module

Validate:

* File Size
* File Type
* Magic Bytes

Generate:

* MD5
* SHA1
* SHA256
* SHA512

Collect:

* Metadata
* File Information

---

## Package Analysis Module

ZIP Support:

* Recursive extraction
* Maximum depth: 3

Discover:

* EXE
* DLL

Generate:

* Lineage information

---

## PE Analysis Module

Parse:

* DOS Header
* COFF Header
* Optional Header

Extract:

* Machine Type
* Compile Timestamp
* Entry Point
* Characteristics

---

## Security Mitigation Analysis

Detect:

* DEP
* ASLR
* CFG
* SafeSEH

---

## Entropy Analysis

Calculate Shannon Entropy for every PE section.

Flag:

Entropy > 7.0

---

## Import Analysis

Detect:

* CreateRemoteThread
* VirtualAllocEx
* WriteProcessMemory
* ShellExecute
* WinExec
* InternetOpen

---

## String Analysis

Extract:

* IPv4
* IPv6
* URLs
* Domains
* Email Addresses
* Registry Keys

---

## Manifest Analysis

Extract:

* requestedExecutionLevel
* uiAccess

---

## YARA Analysis

Implement categories:

* Runtime Injection
* PowerShell
* Anti-Debugging
* Packers
* Execution
* Network
* Ransomware
* Crypto

Rules stored under:

yara_rules/

Rules must be loaded recursively.

Fault tolerant loading required.

---

# DYNAMIC ANALYSIS ARCHITECTURE

VM B (Sandbox)

Windows 10

Components:

* Sysmon
* TShark
* Sandbox Agent

---

# SANDBOX AGENT WORKFLOW

Receive Sample
↓
Create Analysis Session
↓
Start Monitoring
↓
Execute Sample
↓
Track Process Tree
↓
Collect Events
↓
Determine Completion
↓
Generate JSON Results
↓
Cleanup

---

# ANALYSIS PROFILES

Quick:

60 seconds

Standard:

120 seconds

Deep:

300 seconds

Default:

Standard

---

# COMPLETION LOGIC

Analysis completes when:

Entire Process Tree Exits

AND

10 Seconds Inactivity

OR

Maximum Timeout Reached

---

# PROCESS MONITORING

Capture:

* Process Name
* PID
* Parent PID
* Command Line
* Timestamp

Track:

Entire Process Tree

Example:

sample.exe
├── cmd.exe
├── powershell.exe
└── payload.exe

---

# FILE MONITORING

Capture:

* Created
* Modified
* Deleted

Classify:

* Executable
* Script
* Document
* Archive
* Image
* Other

---

# REGISTRY MONITORING

Monitor only:

* Run
* RunOnce
* Services
* Winlogon
* Policies

Capture:

* Create
* Modify
* Delete

---

# NETWORK MONITORING

Capture:

* DNS Queries
* Destination IP
* Destination Port
* Protocol
* Connection Attempts

Source:

TShark

Do NOT store PCAP files.

---

# DYNAMIC BEHAVIORAL FINDINGS

Implement:

1. PowerShell Spawned
2. Command Shell Spawned
3. Script Host Spawned
4. Rundll32 Spawned
5. Regsvr32 Spawned
6. Persistence Mechanism Created
7. Windows Service Installed
8. Executable Dropped
9. DLL Dropped
10. Outbound Network Communication
11. Multiple Child Processes
12. Suspicious Process Chain

Each finding must contain:

* Finding Name
* Category
* Severity
* Evidence
* Description

---

# COMMUNICATION MODEL

VM A communicates with VM B through a Sandbox Agent Service.

Endpoints:

POST /submit

GET /status/{analysis_id}

GET /results/{analysis_id}

Return:

JSON only.

Do not transfer:

* EVTX Files
* PCAP Files
* Raw Sysmon Logs

---

# PDF REPORT STRUCTURE

1. Cover Page

2. Executive Summary

3. Key Findings

4. YARA Detections

5. Suspicious Imports

6. Strings & Indicators

7. PE Analysis

8. Security Mitigations

9. Entropy Analysis

10. Manifest Analysis

11. Dynamic Behavioral Findings

12. Process Activity

13. File Activity

14. Registry Activity

15. Network Activity

16. Sample Information

17. Module Execution Summary

18. Final Verdict

19. Recommendations

Important:

Findings must appear before raw evidence.

Evidence must appear before technical details.

Avoid raw data dumps.

---

# CODING REQUIREMENTS

Use:

* Type Hints
* Dataclasses
* Structured Logging
* Error Handling
* Modular Architecture
* Separation of Concerns

Avoid:

* Monolithic Files
* Business Logic Inside GUI
* Tight Coupling Between Modules

---

# FUTURE COMPATIBILITY

The architecture must support future integration of:

* SQLite
* Memory Analysis
* Screenshot Capture
* Procmon
* MITRE ATT&CK Mapping
* Static + Dynamic Correlation
* AI Classification
* Behavior Correlation Engine

Do not implement these features now.

Only ensure the architecture can support them later.

---

# DELIVERABLE

Produce a production-quality Offline Malware Analysis Platform suitable for academic demonstration and future expansion into a complete malware analysis framework.
