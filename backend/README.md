# AI-Powered SOC Platform - Backend

Production-grade cybersecurity threat detection platform using machine learning and MITRE ATT&CK mapping.

## Features

- **Multi-Model ML Detection**: Deep Autoencoder, Isolation Forest, LOF, and LSTM
- **MITRE ATT&CK Mapping**: Automatic mapping to 7 attack techniques
- **Explainable AI**: Feature contribution analysis and natural language explanations
- **Real-time Streaming**: WebSocket-based live telemetry and alerts
- **PDF Reports**: Professional incident reports with charts and recommendations
- **Realistic Metrics**: Target 85-92% precision, 80-90% recall

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train ML Models

```bash
python ml/trainer.py
```

This will:
- Generate 10,000 normal traffic samples
- Train all 4 ML models
- Save models to `models_saved/` directory

### 3. (Optional) Evaluate Models

```bash
python ml/evaluator.py
```

### 4. Start API Server

```bash
python main.py
```

Server will start at `http://localhost:8000`

### 5. Access API Documentation

Open `http://localhost:8000/docs` for interactive Swagger API documentation.

## API Endpoints

### Dashboard
- `GET /api/dashboard/stats` - Overall SOC statistics
- `GET /api/dashboard/risk-score` - Current risk score
- `GET /api/dashboard/endpoint-health` - Endpoint health summary

### Incidents
- `GET /api/incidents/` - List all incidents
- `GET /api/incidents/{id}` - Get incident details
- `POST /api/incidents/{id}/report` - Generate PDF report
- `GET /api/incidents/{id}/report/download` - Download PDF

### Logs
- `WS /api/logs/stream` - WebSocket for live logs
- `GET /api/logs/history` - Historical logs

### Threats
- `GET /api/threats/analyze/{endpoint_id}` - Analyze endpoint
- `GET /api/threats/mitre/{incident_id}` - MITRE mapping
- `GET /api/threats/explain/{incident_id}` - AI explanation

## Architecture

```
backend/
├── main.py                 # FastAPI application
├── config.py               # Configuration
├── models.py               # Pydantic models
├── database.py             # In-memory data store
├── data/
│   ├── telemetry_generator.py    # Synthetic data generation
│   └── attack_simulator.py       # Attack scenario simulation
├── ml/
│   ├── models/
│   │   ├── autoencoder.py        # Deep Autoencoder
│   │   ├── isolation_forest.py   # Isolation Forest
│   │   ├── lof.py                # Local Outlier Factor
│   │   └── lstm_detector.py      # LSTM Sequence Detector
│   ├── trainer.py          # Model training orchestrator
│   ├── detector.py         # Ensemble detector
│   └── evaluator.py        # Model evaluation
├── mitre/
│   ├── techniques.py       # MITRE ATT&CK database
│   ├── mapper.py           # Technique mapper
│   └── explainer.py        # Explainable AI
├── reports/
│   └── generator.py        # PDF report generation
└── api/
    ├── websocket.py        # WebSocket manager
    └── routes/             # API route handlers
```

## Configuration

Edit `config.py` to customize:
- Number of endpoints (default: 75)
- ML model parameters
- Detection thresholds
- False positive/negative rates

## Background Detection

The main application runs a background task that:
1. Monitors all endpoints
2. Periodically injects simulated attacks (10% chance per cycle)
3. Detects anomalies using ensemble models
4. Creates incidents automatically
5. Broadcasts alerts via WebSocket

## Development

Run tests:
```bash
# Test data generation
python data/telemetry_generator.py
python data/attack_simulator.py

# Test ML models
python ml/models/autoencoder.py

# Test MITRE mapping
python mitre/mapper.py
python mitre/explainer.py
```

## Notes

- Models must be trained before starting the server
- PDF reports are saved to `reports/generated/`
- WebSocket connections have a 2-second streaming interval
- Attack simulation runs every 10 seconds in background
