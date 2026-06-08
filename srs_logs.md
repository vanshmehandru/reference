# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

# Unified Security Log Analysis, Correlation and Investigation Platform (USLCIP)

Version: 1.0

Prepared By: Development Team

Date: June 2026

---

# 1. Introduction

## 1.1 Purpose

The purpose of this project is to develop a centralized security log analysis platform capable of ingesting, parsing, normalizing, correlating, storing, and visualizing security events from multiple security monitoring solutions.

The platform shall provide security analysts with a unified investigation interface capable of correlating related events from multiple sources and presenting them as a single incident.

The system shall initially support CSV-based log ingestion and later support real-time integrations with SIEM, NDR, Cisco Stealthwatch, Syslog servers, APIs, and streaming platforms.

---

# 1.2 Problem Statement

Organizations deploy multiple security monitoring solutions such as:

* SIEM
* NDR
* Cisco Stealthwatch
* Endpoint Monitoring Tools
* System Monitoring Solutions

Each tool generates logs in different formats.

Security analysts face challenges such as:

* Large log volumes
* Different schemas
* Lack of centralized visibility
* Manual event correlation
* Time-consuming investigations
* Difficulty identifying attack chains

The proposed platform will solve these challenges through centralized log analysis and correlation.

---

# 1.3 Objectives

The system shall:

* Centralize security logs
* Normalize heterogeneous log formats
* Correlate related events
* Generate incidents automatically
* Provide graphical investigation capabilities
* Support efficient log storage and retention
* Improve analyst visibility

---

# 2. Scope

## Included Features

### Log Ingestion

* CSV Upload
* Multi-source ingestion
* Source identification

### Data Processing

* Parsing
* Normalization
* Validation
* Correlation

### Storage

* Raw log storage
* Normalized event storage
* Incident storage
* Relationship storage

### Analytics

* Event analytics
* Asset analytics
* Security analytics
* Incident analytics

### Investigation

* IP investigation
* Event investigation
* Timeline analysis
* Relationship visualization

---

## Future Scope

* Syslog Collection
* API Integrations
* Kafka Integration
* Elasticsearch Integration
* Threat Intelligence Integration
* MITRE ATT&CK Mapping
* Machine Learning Anomaly Detection
* SOAR Integration

---

# 3. System Overview

The system shall support two ingestion modes.

---

# 4. Ingestion Mode A: Separate Source Upload

## Description

Logs from different sources are uploaded individually.

Example:

SIEM.csv

NDR.csv

Stealthwatch.csv

---

## Workflow

Upload File
↓
Source Selection
↓
Source-Specific Parser
↓
Normalization Engine
↓
Database Storage
↓
Correlation Engine
↓
Incident Generation
↓
Dashboard

---

## Functional Requirements

### FR-A001 Upload Source File

Users shall upload source-specific log files.

Supported Types:

* SIEM
* NDR
* Stealthwatch

Priority: High

---

### FR-A002 Source Identification

Users shall specify the source type during upload.

Priority: High

---

### FR-A003 Source Parser Selection

The system shall invoke the corresponding parser.

Examples:

SIEM → SIEM Parser

NDR → NDR Parser

Stealthwatch → Stealthwatch Parser

Priority: High

---

### FR-A004 Event Normalization

Parsed records shall be transformed into a common event schema.

Priority: High

---

# 5. Ingestion Mode B: Unified Log Upload

## Description

A single file may contain events from multiple security sources.

Example:

source_type,event_name,source_ip

SIEM,Failed Login,10.1.1.5

NDR,Large Transfer,10.1.1.5

STEALTHWATCH,Exfiltration Alert,10.1.1.5

---

## Workflow

Upload File
↓
Row Reader
↓
Source Detection Engine
↓
Parser Router
↓
Source Parser
↓
Normalization Engine
↓
Database Storage
↓
Correlation Engine
↓
Incident Generation
↓
Dashboard

---

## Functional Requirements

### FR-B001 Mixed Log Upload

The system shall accept files containing records from multiple sources.

Priority: High

---

### FR-B002 Source Detection

The system shall identify the source of each record.

Methods:

* Source_Type field
* Log Source field
* Signature Detection Rules

Priority: High

---

### FR-B003 Dynamic Parser Routing

The system shall route records to the appropriate parser.

Priority: High

---

### FR-B004 Event Normalization

All events shall be converted into the common event schema.

Priority: High

---

# 6. Common Processing Engine

Both ingestion modes shall use the same processing pipeline after normalization.

Workflow:

Normalized Events
↓
Database Storage
↓
Correlation Engine
↓
Incident Generator
↓
Analytics Engine
↓
Frontend Dashboard

---

# 7. Common Event Schema

Every log shall be transformed into the following schema.

| Field            | Description             |
| ---------------- | ----------------------- |
| event_id         | Unique Event Identifier |
| source_type      | SIEM/NDR/Stealthwatch   |
| event_name       | Event Name              |
| timestamp        | Event Time              |
| source_ip        | Source Address          |
| destination_ip   | Destination Address     |
| source_port      | Source Port             |
| destination_port | Destination Port        |
| category         | Event Category          |
| magnitude        | Risk Magnitude          |
| raw_event_id     | Raw Event Reference     |

---

# 8. Correlation Engine

## Purpose

The correlation engine shall identify related events across multiple security tools.

---

## Correlation Criteria

### IP Correlation

Same Source IP

### Destination Correlation

Same Destination IP

### Time Correlation

Events occurring within a configurable time window.

Default:

10 Minutes

### Event Correlation

Related event types.

Example:

Failed Login

↓

Successful Login

↓

Large Data Transfer

↓

Exfiltration Alert

---

## Functional Requirements

### FR-C001 Event Correlation

The system shall correlate related events.

Priority: High

---

### FR-C002 Incident Creation

The system shall automatically create incidents from correlated events.

Priority: High

---

### FR-C003 Incident Risk Scoring

The system shall calculate a risk score.

Priority: Medium

---

# 9. Incident Management

## Incident Structure

| Field       | Description              |
| ----------- | ------------------------ |
| incident_id | Unique Incident          |
| severity    | Critical/High/Medium/Low |
| risk_score  | Incident Risk            |
| created_at  | Creation Time            |

---

## Incident Events

An incident may contain:

* SIEM Events
* NDR Events
* Stealthwatch Events

simultaneously.

---

## Example

Incident #001

Evidence:

SIEM → Failed Login

NDR → Large Transfer

Stealthwatch → Exfiltration Alert

---

# 10. Database Requirements

## Raw Uploads

Stores uploaded files.

Fields:

* upload_id
* filename
* upload_time
* source_type

---

## Events

Stores normalized events.

Fields:

* event_id
* source_type
* event_name
* timestamp
* source_ip
* destination_ip
* category
* magnitude

---

## Assets

Stores discovered entities.

Fields:

* asset_id
* asset_type
* asset_value
* first_seen
* last_seen

---

## Incidents

Stores generated incidents.

Fields:

* incident_id
* risk_score
* severity

---

## Incident Events

Maps incidents to events.

Fields:

* incident_id
* event_id

---

## Relationships

Stores entity relationships.

Fields:

* source_entity
* destination_entity
* relationship_type

---

# 11. Search and Investigation

## Functional Requirements

### FR-I001 Search by IP

Users shall search events using IP addresses.

---

### FR-I002 Search by Event Name

Users shall search using event names.

---

### FR-I003 Search by Source

Users shall search by source type.

---

### FR-I004 Incident Investigation

Users shall view all events associated with an incident.

---

### FR-I005 Asset Investigation

Users shall investigate:

* IP Addresses
* Hosts
* Users

---

# 12. Dashboard Analytics

## Event Analytics

### Event Trend

Line Chart

Shows event volume over time.

---

### Event Distribution

Pie Chart

Shows event categories.

---

### Top Event Types

Bar Chart

Shows most frequent events.

---

## Network Analytics

### Top Source IPs

Bar Chart

Shows highest event-generating IPs.

---

### Top Destination IPs

Bar Chart

Shows communication targets.

---

### Communication Heatmap

Displays communication density.

---

### Network Relationship Graph

Displays IP-to-IP relationships.

---

## Security Analytics

### Severity Distribution

Pie Chart

Displays severity levels.

---

### Risk Distribution

Histogram

Displays risk score spread.

---

### Alert Trends

Line Chart

Displays alert volume over time.

---

## Investigation Analytics

### Incident Timeline

Shows chronological sequence of events.

Example:

10:00 Failed Login

10:03 Large Transfer

10:05 Exfiltration Alert

---

### Incident Relationship Graph

Displays:

User
↓
Host
↓
IP
↓
Event
↓
Incident

---

# 13. Non-Functional Requirements

## Performance

* Process 100,000 events per upload
* Search response under 2 seconds
* Dashboard response under 3 seconds

---

## Scalability

* Support millions of events
* Modular architecture
* Horizontal scalability support

---

## Reliability

* Backup support
* Error recovery
* Data validation

---

## Security

* JWT Authentication
* Role-Based Access Control
* Password Hashing
* HTTPS

---

## Availability

Target Availability:

99%

---

# 14. Technology Stack

Frontend:

* React
* TypeScript
* Chart.js / Recharts
* Cytoscape.js

Backend:

* FastAPI

Database:

* PostgreSQL

Future Database:

* Neo4j

Authentication:

* JWT

Containerization:

* Docker

---

# 15. Acceptance Criteria

The system shall be accepted when:

✓ Source-specific uploads function correctly

✓ Mixed-source uploads function correctly

✓ Logs are parsed successfully

✓ Events are normalized successfully

✓ Events are stored correctly

✓ Correlation engine identifies related events

✓ Incidents are generated automatically

✓ Incident timelines are displayed

✓ Investigation graphs are displayed

✓ Dashboard analytics function correctly

✓ Search and filtering function correctly

✓ Retention policies remove expired logs

✓ Export functionality works correctly

✓ Authentication and authorization function correctly
