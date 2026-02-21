# Cortex Architecture

## Overview

Cortex is an AI-powered study tracker consisting of three main components:

```
cortex/
├── backend/       FastAPI + SQLAlchemy + Gemini AI
├── extension/     Chrome Extension (MV3)
└── dashboard/     Standalone HTML/JS dashboard
```

---

## Component Details

### Backend (`backend/`)
- **Framework**: FastAPI (Python)
- **Database**: SQLite (dev) / PostgreSQL (prod) via SQLAlchemy ORM
- **AI**: Google Gemini via `google-generativeai` SDK

| Endpoint | Method | Description |
|---|---|---|
| `/api/track/` | POST | Log a study activity |
| `/api/analyze/{user_id}` | GET | AI-generated learning insights |
| `/api/plan/{user_id}` | GET | AI-generated daily study plan |

### Chrome Extension (`extension/`)
- **Manifest Version**: 3
- **Content Scripts**: `youtube.js` (tracks video sessions), `leetcode.js` (tracks problem sessions)
- **Background Worker**: Receives messages from content scripts and POSTs to backend
- **Popup**: Quick access to insights and today's plan

### Dashboard (`dashboard/`)
- Plain HTML / CSS / JS — no framework
- Fetches insights and plan from the backend REST API

---

## Data Flow

```
YouTube / LeetCode (content script)
        │  chrome.runtime.sendMessage
        ▼
background.js  ──POST /api/track/──▶  FastAPI backend
                                              │
                                     SQLite / Postgres
                                              │
                             GET /api/analyze  │  GET /api/plan
                                              ▼
                                       Gemini AI
                                              │
                              popup / dashboard (display)
```
