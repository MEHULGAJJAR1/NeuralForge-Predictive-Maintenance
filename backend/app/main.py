from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import sqlite3, os
import numpy as np
from sklearn.ensemble import IsolationForest

from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="NeuralForge — Predictive Maintenance Digital Twin", version="1.0.0", description="Sensor telemetry, anomaly screening, and explainable maintenance prioritization.")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
DB_PATH = os.getenv("DATABASE_PATH", "app.db")

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, kind TEXT NOT NULL, payload TEXT NOT NULL, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
init_db()

class SensorInput(BaseModel):
    vibration: float = Field(ge=0, le=100)
    temperature_c: float = Field(ge=-40, le=300)
    pressure: float = Field(ge=0, le=1000)


rng = np.random.default_rng(42)
normal = np.column_stack([rng.normal(1.0, .25, 500), rng.normal(55, 8, 500), rng.normal(5, .6, 500)])
model = IsolationForest(contamination=0.04, random_state=42).fit(normal)


@app.get("/api/health")
def health():
    return {"status":"ok","project":"NeuralForge","data_mode":"demo/local","database":"sqlite"}

@app.get("/api/summary")
def summary():
    with sqlite3.connect(DB_PATH) as conn:
        count = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    return {"project":"NeuralForge","records_analyzed":count,"status":"operational","mode":"demo"}

@app.post("/api/analyze")
def analyze(payload: SensorInput):
    features = np.array([[payload.vibration, payload.temperature_c, payload.pressure]])
    pred = int(model.predict(features)[0] == -1)
    score = float(model.decision_function(features)[0])
    health = max(0, min(100, 100 - (payload.vibration * 15 + max(0, payload.temperature_c-65) * 0.7 + abs(payload.pressure-5) * 5)))
    return {"anomaly": bool(pred), "anomaly_score": round(score, 4), "health_score": round(health, 1), "recommendation": "Inspect machine and verify sensor calibration." if pred or health < 70 else "Continue routine monitoring.", "model_status": "SYNTHETIC_TRAINING_DEMO"}

@app.post("/api/events")
def save_event(payload: dict):
    import json
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("INSERT INTO events(kind,payload) VALUES (?,?)", ("analysis", json.dumps(payload)))
        event_id = cur.lastrowid
    return {"id":event_id,"saved":True}

@app.get("/api/events")
def events():
    import json
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute("SELECT id,kind,payload,created_at FROM events ORDER BY id DESC LIMIT 50").fetchall()
    return [{"id":r[0],"kind":r[1],"payload":json.loads(r[2]),"created_at":r[3]} for r in rows]
