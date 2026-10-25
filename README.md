# NeuralForge — Predictive Maintenance Digital Twin

Sensor telemetry, anomaly screening, and explainable maintenance prioritization.

## What is included
- Synthetic sensor telemetry generator for demo mode
- IsolationForest anomaly scoring on vibration, temperature, and pressure
- SQLite equipment and telemetry history
- Equipment health dashboard and maintenance recommendation
- Simple what-if analysis for operating conditions

## Architecture
- `frontend/`: responsive HTML/CSS/JavaScript dashboard
- `backend/app/main.py`: FastAPI REST API, model baseline, SQLite persistence
- `backend/tests/`: API smoke tests
- `backend/.env.example`: local configuration template

## Quick start (Windows PowerShell)

1. Install Python 3.10+.
2. Open PowerShell in `backend`:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   Copy-Item .env.example .env
   uvicorn app.main:app --reload
   ```
3. Open `frontend/index.html` in a browser, or use VS Code Live Server. Keep the backend running on `http://127.0.0.1:8000`.
4. API docs: http://127.0.0.1:8000/docs
5. Run tests from `backend`:
   ```powershell
   pytest -q
   ```

## macOS/Linux
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Then open `frontend/index.html` in your browser.

## Model and data honesty
**Model status:** IsolationForest trained on synthetic sensor readings. Use real labelled machine data and validation before operational use.
The dashboard and API are runnable locally. SQLite storage and local analysis are implemented. Live provider feeds, production-grade model training, authentication, and cloud deployment are **not** configured in this starter. Do not use this demo for real emergency, security, industrial safety, or financial decisions without validation, domain review, security hardening, and appropriate data integrations.

## API examples
- `GET /api/health`
- `GET /api/summary`
- `POST /api/analyze`
- `POST /api/events`
- `GET /api/events`

Example analysis body:
```json
{"vibration":4.8,"temperature_c":92,"pressure":8.2}
```

## Suggested next steps
1. Replace demo inputs with licensed/verified real datasets.
2. Add authentication and role-based access control before exposing the API.
3. Add model evaluation, drift monitoring, structured logging, and deployment CI.
4. Add provider-specific integrations through documented API clients and environment variables.
