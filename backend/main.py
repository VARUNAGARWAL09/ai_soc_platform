"""
FastAPI Main Application
AI-Powered SOC Platform Backend
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from contextlib import asynccontextmanager
import numpy as np
from datetime import datetime

from config import settings
from api.routes import dashboard, incidents, logs, threats, automation, chatbot
from api.websocket import manager
from database import data_store
from data.telemetry_generator import TelemetryGenerator
from data.attack_simulator import AttackSimulator
from ml.detector import EnsembleDetector
from mitre.mapper import MITREMapper
from mitre.explainer import ExplainableAI
from models import Incident, EndpointMetadata, FeatureContribution, MITRETechnique


# Global components
telemetry_gen = None
attack_sim = None
detector = None
mitre_mapper = None
explainer = None
background_task = None


async def threat_detection_loop():
    """Background task for continuous threat detection"""
    global telemetry_gen, attack_sim, detector, mitre_mapper, explainer
    
    print("Starting threat detection loop...")
    
    # Initialize components
    telemetry_gen = TelemetryGenerator(num_endpoints=settings.NUM_ENDPOINTS)
    attack_sim = AttackSimulator(telemetry_gen)
    detector = EnsembleDetector()
    mitre_mapper = MITREMapper()
    explainer = ExplainableAI()
    
    # Load models
    try:
        detector.load_models()
        print("Models loaded successfully")
    except Exception as e:
        print(f"Warning: Could not load models: {e}")
        print("Run trainer.py first to train models")
        return
    
    # Initialize endpoints
    for endpoint in telemetry_gen.get_endpoint_list():
        ep_metadata = EndpointMetadata(
            id=endpoint["id"],
            hostname=endpoint["hostname"],
            ip=endpoint["ip"],
            role=endpoint["role"],
            os=endpoint["os"],
            status="healthy",
            last_seen=datetime.now()
        )
        data_store.update_endpoint(ep_metadata)
    
    iteration = 0
    
    while True:
        try:
            iteration += 1
            
            # 1. Generate Background Traffic (Normal)
            # Pick a few random endpoints to generate traffic for
            active_endpoints = np.random.choice(telemetry_gen.endpoints, size=3, replace=False)
            
            for endpoint in active_endpoints:
                # Generate normal point
                # We use generate_telemetry_point with spec for normal behavior
                normal_point = telemetry_gen.generate_telemetry_point(endpoint["id"])
                
                # Broadcast as INFO log
                log_entry = {
                    "id": f"log-{datetime.now().timestamp()}",
                    "timestamp": normal_point["timestamp"],
                    "endpoint_id": normal_point["endpoint_id"],
                    "hostname": normal_point["hostname"],
                    "ip": normal_point["ip"],
                    "severity": "info",
                    "message": f"Normal telemetry received",
                    "data": normal_point
                }
                await manager.broadcast(log_entry)

            # 2. Attack Simulation
            # Periodically inject attacks (40% chance every cycle)
            should_attack = np.random.random() < 0.40
            
            if should_attack:
                attack_type = np.random.choice(attack_sim.list_attack_types())
                endpoint = np.random.choice(telemetry_gen.endpoints)
                
                print(f"[{datetime.now()}] Simulating {attack_type} on {endpoint['id']}")
                
                # Shorter duration for real-time feel
                attack_sequence = attack_sim.generate_attack_sequence(
                    attack_type,
                    endpoint_id=endpoint["id"],
                    duration_seconds=15
                )
                
                for point in attack_sequence:
                    telemetry = {f: point[f] for f in settings.FEATURES if f in point}
                    
                    # Detect anomaly
                    anomaly_score = detector.detect_single(telemetry)
                    
                    # Log every step of attack as Warning or Critical based on score
                    severity = "warning"
                    if anomaly_score.ensemble_score >= 0.8: max_sev = "critical"
                    elif anomaly_score.ensemble_score >= 0.6: max_sev = "high"
                    else: max_sev = "warning"
                    
                    # Broadcast log for this step
                    await manager.broadcast({
                        "id": f"log-attack-{datetime.now().timestamp()}",
                        "timestamp": point["timestamp"],
                        "endpoint_id": point["endpoint_id"],
                        "hostname": "Simulated-Host",
                        "severity": max_sev,
                        "message": f"Suspicious activity detection: {attack_type}",
                        "data": point
                    })

                    if anomaly_score.is_anomaly:
                        mitre_techniques = mitre_mapper.map_to_techniques(telemetry, top_k=3)
                        feature_contributions, explanation = explainer.explain_anomaly(telemetry, top_k=7)
                        
                        severity_inc = "low"
                        if anomaly_score.ensemble_score >= 0.80: severity_inc = "critical"
                        elif anomaly_score.ensemble_score >= 0.70: severity_inc = "high"
                        elif anomaly_score.ensemble_score >= 0.55: severity_inc = "medium"
                        
                        incident = Incident(
                            id=data_store.get_next_incident_id(),
                            endpoint_id=point["endpoint_id"],
                            timestamp=datetime.fromisoformat(point["timestamp"]),
                            severity=severity_inc,
                            status="open",
                            attack_type=attack_type,
                            anomaly_scores=anomaly_score,
                            mitre_techniques=mitre_techniques,
                            feature_contributions=feature_contributions,
                            explanation=explanation,
                            telemetry_snapshot=point
                        )
                        data_store.add_incident(incident)
                        
                        # Broadcast Alert (Incident)
                        # Note: Frontend handles this if it listens to same websocket
                        await manager.broadcast({
                            "type": "alert",
                            "incident_id": incident.id,
                            "endpoint_id": incident.endpoint_id,
                            "severity": incident.severity,
                            "message": f"Threat detected: {mitre_techniques[0].name if mitre_techniques else 'Unknown'}",
                            "timestamp": incident.timestamp.isoformat()
                        })
                        
                        print(f"  🚨 INCIDENT {incident.id}: {severity_inc.upper()} - {attack_type}")
                        await asyncio.sleep(0.5) # Pace out the attack logs
                    
                    # Only create ONE incident per sequence to avoid spamming database
                    if anomaly_score.is_anomaly:
                        break 
            
            # Wait before next cycle
            await asyncio.sleep(1)
            
        except Exception as e:
            print(f"Error in detection loop: {e}")
            await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    global background_task
    background_task = asyncio.create_task(threat_detection_loop())
    
    yield
    
    # Shutdown
    if background_task:
        background_task.cancel()


# Create FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    lifespan=lifespan,
    description="AI-Powered Cybersecurity Threat Detection Platform"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(dashboard.router)
app.include_router(incidents.router)
app.include_router(logs.router)
app.include_router(threats.router)
app.include_router(automation.router)
app.include_router(chatbot.router)


@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "active_connections": manager.get_connection_count(),
        "total_incidents": len(data_store.get_all_incidents()),
        "total_endpoints": len(data_store.get_all_endpoints()) or settings.NUM_ENDPOINTS
    }


if __name__ == "__main__":
    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║   AI-POWERED SOC PLATFORM - BACKEND SERVER                ║
    ║                                                           ║
    ║   API: http://{settings.API_HOST}:{settings.API_PORT}                         ║
    ║   Docs: http://{settings.API_HOST}:{settings.API_PORT}/docs                  ║
    ║                                                           ║
    ║   Endpoints: {settings.NUM_ENDPOINTS}                                ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
