# Offline Deployment Guide – Security Log Correlation & Flow Visualization System

## Purpose

This guide explains how to deploy and run the Security Log Correlation & Flow Visualization System on a completely offline Windows machine with no internet connectivity.

The deployment process is divided into two phases:

1. Preparation on an Online Machine
2. Installation and Execution on the Offline Machine

---

# Phase 1: Preparation on Online Machine

Perform all preparation steps on a machine that has internet access.

---

## Step 1: Download Required Software Installers

Download the following offline installers:

### Python

Download Python 3.10 or later from:

https://www.python.org/downloads/

Recommended:

* Python 3.10.x
* Windows x64 Installer

---

### PostgreSQL

Download PostgreSQL installer from:

https://www.postgresql.org/download/windows/

Recommended:

* PostgreSQL 15 or later
* Windows x64 Installer

---

## Step 2: Download Backend Dependencies

Navigate to the project root directory.

Create a folder:

```bash
mkdir offline_packages
```

Download all required Python packages:

```bash
pip download -r requirements.txt -d offline_packages
```

This command downloads all package files (.whl and .tar.gz) required by the backend.

Example contents:

```text
offline_packages/
├── fastapi
├── uvicorn
├── pandas
├── sqlalchemy
├── psycopg2-binary
├── python-dotenv
├── python-multipart
└── dependencies...
```

No installation occurs during this step.

---

## Step 3: Build the Frontend

Navigate to:

```bash
frontend/
```

Install frontend dependencies:

```bash
npm install
```

Build production frontend:

```bash
npm run build
```

This generates:

```text
frontend/
└── dist/
```

The dist folder contains the fully compiled frontend application.

---

## Step 4: Remove Unnecessary Files

To reduce transfer size, delete:

```text
frontend/node_modules
```

The compiled frontend inside:

```text
frontend/dist
```

is sufficient.

---

## Step 5: Prepare Transfer Package

The final directory structure should resemble:

```text
Log-analyzer/

├── backend/
├── frontend/
│   └── dist/
├── offline_packages/
├── requirements.txt
├── database.py
├── docker-compose.yml
└── other project files
```

Copy the entire project folder to:

* USB Drive
* External SSD
* External HDD

Transfer it to the offline machine.

---

# Phase 2: Installation on Offline Machine

No internet connection is required.

---

## Step 1: Install Python

Run:

```text
python-3.x.x-amd64.exe
```

During installation:

Enable:

✓ Add Python to PATH

Complete installation.

---

## Step 2: Install PostgreSQL

Run:

```text
postgresql-15.x-windows-x64.exe
```

Configure:

```text
Database User: postgres
Password: postgres
Port: 5432
```

Create database:

```sql
CREATE DATABASE security_log_analyzer;
```

---

## Step 3: Install Backend Packages Offline

Open Command Prompt.

Navigate to project root:

```bash
cd Log-analyzer
```

Install packages from local folder:

```bash
pip install --no-index --find-links=offline_packages -r requirements.txt
```

Explanation:

```text
--no-index
    Prevents internet access

--find-links
    Uses local package repository
```

All dependencies are installed completely offline.

---

## Step 4: Configure Environment Variables

Create:

```text
.env
```

Example:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=security_log_analyzer
DB_USER=postgres
DB_PASSWORD=postgres
```

---

## Step 5: Start Backend Server

Open Command Prompt.

Navigate to backend:

```bash
cd backend
```

Start FastAPI:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
```

Backend is now operational.

---

## Step 6: Start Frontend Server

Open a second Command Prompt.

Navigate to compiled frontend:

```bash
cd frontend/dist
```

Serve static files using Python:

```bash
python -m http.server 5173
```

Expected:

```text
Serving HTTP on 0.0.0.0 port 5173
```

Frontend is now available.

---

## Step 7: Launch Application

Open browser:

```text
http://localhost:5173
```

The application will load entirely from local resources.

Backend API:

```text
http://localhost:8000
```

Frontend:

```text
http://localhost:5173
```

---

# Offline Operation Workflow

```text
Upload Log Source 1
Upload Log Source 2
Upload Log Source 3
            │
            ▼
     Header Extraction
            │
            ▼
   Field Normalization
            │
            ▼
   Event Categorization
            │
            ▼
 PostgreSQL Storage
            │
            ▼
  Correlation Engine
            │
            ▼
 Incident Generation
            │
            ▼
 Flow Visualization
```

No internet connectivity, external APIs, cloud services, or third-party platforms are required.

---

# Components Running Offline

| Component            | Technology          |
| -------------------- | ------------------- |
| Frontend             | React + Material UI |
| Backend              | FastAPI             |
| Database             | PostgreSQL          |
| Normalization Engine | Python              |
| Correlation Engine   | Python              |
| Visualization Engine | React SVG Renderer  |
| Storage              | Local PostgreSQL    |
| Hosting              | Local Machine       |

---

# Result

After completing these steps, the Security Log Correlation & Flow Visualization System will run entirely on the offline machine and support:

* Uploading three log sources
* Header extraction
* Field normalization
* Event categorization
* Incident correlation
* PostgreSQL storage
* Flow-based visualization
* Investigation workflows

without requiring any internet access.
