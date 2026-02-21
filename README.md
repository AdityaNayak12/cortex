# Cortex — AI Study Tracker

> Track your learning activity on YouTube and LeetCode, and get AI-powered insights and personalised study plans.

## Components

| Layer | Tech |
|---|---|
| **Backend** | FastAPI · SQLAlchemy · Google Gemini |
| **Extension** | Chrome MV3 · Vanilla JS |
| **Dashboard** | HTML · CSS · Vanilla JS |

## Quick Start

### Backend
```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # fill in GEMINI_API_KEY
uvicorn app.main:app --reload
```
API docs: http://127.0.0.1:8000/docs

### Chrome Extension
1. Open `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked** → select the `extension/` folder

### Dashboard
Open `dashboard/index.html` in your browser (backend must be running).

## Docs
See [`docs/architecture.md`](docs/architecture.md) for full architecture details.
