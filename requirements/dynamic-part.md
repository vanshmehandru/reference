# CONTINUATION PROMPT – OFFLINE MALWARE ANALYSIS SYSTEM

Do NOT redesign or rewrite the existing static-analysis architecture.

Before making changes, assume the following components are already fully implemented and working:

* Intake Analyzer
* PE Analyzer
* Security Analyzer
* Entropy Analyzer
* Import Analyzer
* Strings Analyzer
* Manifest Analyzer
* YARA Analyzer
* Findings Aggregator
* Risk Engine
* PDF Generator
* GUI Analysis Worker
* Report Viewer
* Settings Controller

The static analysis pipeline already performs:

File Intake
↓
PE Analysis
↓
Security Mitigation Analysis
↓
Entropy Analysis
↓
Import Analysis
↓
String Extraction
↓
Manifest Analysis
↓
YARA Analysis
↓
Aggregation
↓
Risk Assessment
↓
PDF Report Generation

Do not replace these modules.

Do not create alternative analyzer pipelines.

Do not introduce databases.

Do not introduce cloud integrations.

Do not introduce VirusTotal or online services.

---

# PRIMARY OBJECTIVE

Expand the project while preserving the existing architecture.

Current focus:

1. Improve Static Analysis Quality
2. Improve Code Quality
3. Prepare For Dynamic Analysis Integration
4. Reduce Technical Debt

---

# TASK 1 – ADD JSON EXPORT PIPELINE

Currently reports are generated only as PDFs.

Implement machine-readable output generation.

Create:

malware_analyzer/reporting/json_exporter.py

Output:

storage/static_results/

Example:

{
"analysis_id": "...",
"sample_name": "...",
"hashes": {},
"pe_analysis": {},
"security_analysis": {},
"entropy_analysis": {},
"imports": {},
"strings": {},
"manifest": {},
"yara": {},
"risk_assessment": {}
}

The JSON schema should mirror analyzer output structures.

This JSON will later be consumed by Dynamic Analysis correlation modules.

---

# TASK 2 – ANALYSIS SESSION MODEL

Create a centralized AnalysisSession model.

Location:

malware_analyzer/models/analysis_session.py

Purpose:

Store:

* Analysis ID
* Sample Path
* Filename
* Start Time
* End Time
* Analysis Type
* Results

Both Static Analysis and Dynamic Analysis must use this model in the future.

Do not modify analyzer outputs.

Wrap them inside the session object.

---

# TASK 3 – IMPROVE STATIC ANALYSIS DETECTORS

Add additional PE intelligence.

Implement:

## Section Permission Anomalies

Detect:

Writable + Executable sections

Flag:

WX Section Detected

---

## Suspicious Section Names

Examples:

UPX0
UPX1
.aspack
.pedata

---

## Timestamp Validation

Detect:

* Future timestamps
* Extremely old timestamps

---

## Certificate Presence

Detect:

* Signed
* Unsigned

No signature validation yet.

Only presence detection.

---

## Resource Analysis

Collect:

* Number of resources
* Resource types

Examples:

ICON
VERSION
MANIFEST

---

# TASK 4 – IMPROVE STRING EXTRACTION

Add:

* Base64-like strings
* PowerShell Encoded Commands
* File Paths
* UNC Paths

Keep existing IOC extraction intact.

---

# TASK 5 – RISK ENGINE HARDENING

Do not redesign scoring.

Improve:

* Duplicate indicator suppression
* Category caps
* Score explanation fields

Add:

{
"score": 75,
"verdict": "HIGH RISK",
"contributing_factors": []
}

---

# TASK 6 – CREATE DYNAMIC ANALYSIS FOUNDATION

Do not implement dynamic analysis yet.

Only create architecture.

Create folders:

malware_analyzer/dynamic_analysis/

├── controller/
├── agent/
├── models/
├── parsers/
├── reporting/

Create placeholder classes and interfaces.

No execution logic yet.

Purpose:

Prepare project structure for future implementation.

---

# TASK 7 – GUI ARCHITECTURE CLEANUP

Current inconsistency:

StaticAnalysisPage directly creates AnalysisWorker.

Instead:

StaticAnalysisPage
↓
AnalysisController
↓
AnalysisWorker

Refactor so GUI never directly instantiates workers.

Maintain existing functionality.

---

# TASK 8 – TESTING FRAMEWORK

Create:

tests/

Add unit tests for:

* Entropy Analyzer
* Import Analyzer
* Strings Analyzer
* Risk Engine
* Findings Aggregator

Use pytest.

Create fixture-based tests.

No malware samples required.

Use mocked analyzer outputs.

---

# TASK 9 – REPORT IMPROVEMENTS

Keep current PDF structure.

Add:

* Analysis ID
* Generation Timestamp
* Tool Version

Improve section ordering where necessary.

Do not redesign report layout.

Only improve clarity and consistency.

---

# IMPORTANT CONSTRAINTS

Do NOT implement:

* Dynamic Analysis Execution
* Sandbox Agent
* Sysmon Integration
* TShark Integration
* SQLite
* MITRE ATT&CK
* Memory Analysis
* Procmon
* AI Classification
* Cloud Services

Only prepare the codebase so those features can be integrated later without major refactoring.

Preserve all existing functionality while expanding capability.
