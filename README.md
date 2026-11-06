# Incident Response Agent

## Overview

Incident Response Agent is an intelligent incident investigation system designed to help SRE and DevOps teams investigate production incidents using historical incident knowledge.

It integrates Hindsight memory with a FastAPI backend and MongoDB to store incident information, retrieve relevant historical experiences, and support incident analysis.

The central idea is simple: **an incident response agent that remembers, learns, and improves with every resolved production incident.**

## Problem Statement

During production failures, engineers often spend valuable time investigating issues that have occurred before. Previous root causes, troubleshooting steps, and recovery actions may be scattered across logs, tickets, and documentation.

This project explores how persistent agent memory can make historical incident knowledge reusable during future investigations.

## Key Features

- Create and track production incidents.
- Store incident information in MongoDB.
- Retain resolved incident knowledge using Hindsight.
- Retrieve potentially relevant historical incidents.
- Generate rule-based investigation suggestions.
- Provide REST API endpoints through FastAPI.
- Display incident information through a React dashboard.





## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React, Vite |
| Database | MongoDB Atlas |
| Agent Memory | Hindsight Cloud |
| API Testing | FastAPI Swagger UI |
| Version Control | Git, GitHub |

## System Architecture

The application follows a modular architecture:

1. **React Dashboard:** Provides the user interface for incident management.
2. **FastAPI Backend:** Handles API requests, incident analysis, and application logic.
3. **MongoDB Atlas:** Stores incident records and related information.
4. **Hindsight Cloud:** Retains and retrieves historical incident knowledge.
5. **Incident Analyzer:** Generates rule-based investigation suggestions and incorporates retrieved historical context.

```text
+----------------------+
|   React Dashboard    |
+----------+-----------+
           |
           v
+----------------------+
|    FastAPI Backend   |
+----------+-----------+
           |
     +-----+------+
     |            |
     v            v
+----------+  +----------------+
| MongoDB  |  | Hindsight Cloud|
|  Atlas   |  | Agent Memory   |
+----------+  +----------------+
     |            |
     +-----+------+
           |
           v
+----------------------+
|  Incident Analyzer   |
|  Rule-Based Analysis |
+----------------------+
```

## Project Structure

The repository is organized into two main application modules:

**Backend**
- `app/__init__.py` – Backend application package.
- `create_hindsight_bank.py` – Hindsight memory bank setup script.
- `test_grok.py` – xAI API connectivity test script.
- `.env.example` – Environment configuration template.
- `app/main.py` – FastAPI application entry point.
- `app/core/` – Database connection, Hindsight client, AI client, and incident analyzer.
- `app/incidents/` – Incident management API routes.
- `app/memory/` – Hindsight memory operations.
- `requirements.txt` – Python dependencies.

**Frontend**
- `src/App.jsx` – Main React dashboard.
- `src/App.css` – Dashboard styling.
- `src/index.css` – Global styles.
- `src/main.jsx` – React application entry point.
- `package.json` – Frontend dependencies and scripts.


## Installation and Setup

### Prerequisites

Make sure the following tools are installed:

- Python 3.10 or later
- Node.js and npm
- MongoDB Atlas account
- Hindsight Cloud API credentials

### 1. Clone the Repository

Clone the repository after it is published on GitHub:

`git clone YOUR_GITHUB_REPOSITORY_URL`

`cd microsoft`

### 2. Backend Setup

Navigate to the backend directory:

`cd backend`

Create and activate a virtual environment:

`python -m venv venv`

`.\venv\Scripts\Activate.ps1`

Install dependencies:

`pip install -r ..\requirements.txt`

Copy the example environment file and configure your credentials:

```powershell
Copy-Item .env.example .env
```

Required configuration:

- `MONGODB_URI`
- `HINDSIGHT_API_KEY`
- `HINDSIGHT_BASE_URL`
- `HINDSIGHT_BANK_ID`

Start the backend server:

`python -m uvicorn app.main:app --reload`

Backend API: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

### 3. Frontend Setup

Open another terminal and navigate to the frontend directory:

`cd frontend`

Install dependencies:

`npm install`

Start the development server:

`npm run dev`

Frontend dashboard: http://localhost:5173


## API Endpoints

The backend exposes the following REST API endpoints:

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check backend health |
| GET | `/db-health` | Check database connectivity |
| POST | `/incidents/` | Create an incident |
| GET | `/incidents/` | Retrieve incidents |
| POST | `/incidents/memory/search` | Search historical incident memory |
| PATCH | `/incidents/{incident_id}/resolve` | Resolve an incident |
| POST | `/incidents/{incident_id}/memory/store` | Store resolved incident knowledge |
| POST | `/incidents/{incident_id}/analyze` | Analyze an incident |

## Current Implementation Status

The current version demonstrates the integration of incident management with persistent agent memory.

**Implemented:**
- FastAPI backend and React dashboard.
- MongoDB Atlas incident storage.
- Hindsight Cloud memory integration.
- Retention of resolved incident information.
- Retrieval of potentially relevant historical incidents.
- Rule-based investigation suggestions.
- End-to-end incident analysis API.

**Current limitations:**
- Incident analysis currently uses rule-based logic rather than a fully autonomous AI reasoning model.
- Historical memory retrieval needs further evaluation to improve the relevance of retrieved root causes and recovery actions.
- Automated root-cause verification and advanced remediation recommendations are future enhancements.

## Future Enhancements

- Improve semantic retrieval of historical incidents.
- Integrate an operational AI reasoning model.
- Generate context-aware investigation recommendations.
- Add automated incident severity assessment.
- Introduce runbook recommendations and remediation workflows.
- Improve incident analytics and reporting.

## Hindsight Resources

- [Hindsight GitHub Repository](https://github.com/vectorize-io/hindsight)
- [Hindsight Documentation](https://hindsight.vectorize.io/)
- [What Is Agent Memory?](https://vectorize.io/what-is-agent-memory)









