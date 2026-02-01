"""
Logs Streaming API Routes
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.websocket import manager
from data.telemetry_generator import TelemetryGenerator
from config import settings

router = APIRouter(prefix="/api/logs", tags=["logs"])

# Initialize telemetry generator
telemetry_gen = TelemetryGenerator(num_endpoints=settings.NUM_ENDPOINTS)


@router.websocket("/stream")
async def logs_stream(websocket: WebSocket):
    """WebSocket endpoint for live log streaming"""
    
    await manager.connect(websocket)
    
    try:
        while True:
            # Keep connection alive, data is sent via manager.broadcast() from main.py
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        await manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        await manager.disconnect(websocket)


@router.get("/history")
async def get_log_history(limit: int = 100):
    """Get historical log data"""
    
    # Generate historical data
    df = telemetry_gen.generate_normal_traffic(num_samples=min(limit, 200))
    
    logs = []
    for _, row in df.iterrows():
        log_entry = {
            "id": f"log-{row['timestamp'].timestamp()}",
            "timestamp": row["timestamp"].isoformat(),
            "endpoint_id": row["endpoint_id"],
            "severity": "info",
            "message": f"Historical telemetry data",
            "data": row.to_dict()
        }
        logs.append(log_entry)
    
    return {"logs": logs[:limit]}
