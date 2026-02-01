"""
Threats Analysis API Routes
"""
from fastapi import APIRouter, HTTPException
from typing import List
import numpy as np
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models import MITRETechnique, FeatureContribution
from database import data_store
from ml.detector import EnsembleDetector
from mitre.mapper import MITREMapper
from mitre.explainer import ExplainableAI
from data.telemetry_generator import TelemetryGenerator
from config import settings

router = APIRouter(prefix="/api/threats", tags=["threats"])

# Initialize components
detector = EnsembleDetector()
mitre_mapper = MITREMapper()
explainer = ExplainableAI()
telemetry_gen = TelemetryGenerator()


@router.get("/analyze/{endpoint_id}")
async def analyze_endpoint(endpoint_id: str):
    """Analyze specific endpoint for threats"""
    
    # Generate current telemetry for endpoint
    telemetry = telemetry_gen.generate_telemetry_point(endpoint_id)
    
    # Extract features
    features = {f: telemetry[f] for f in settings.FEATURES}
    
    # Detect anomaly
    try:
        if not detector.models_loaded:
            detector.load_models()
        
        anomaly_score = detector.detect_single(features)
    except Exception as e:
        # Model not trained yet, return default
        from models import AnomalyScore
        anomaly_score = AnomalyScore(
            autoencoder_score=0.3,
            isolation_forest_score=0.25,
            lof_score=0.28,
            lstm_score=None,
            ensemble_score=0.28,
            is_anomaly=False,
            confidence=0.75
        )
    
    # MITRE mapping
    mitre_techniques = mitre_mapper.map_to_techniques(features, top_k=3)
    
    # Explainability
    feature_contributions, explanation = explainer.explain_anomaly(features, top_k=5)
    
    return {
        "endpoint_id": endpoint_id,
        "telemetry": telemetry,
        "anomaly_score": anomaly_score,
        "mitre_techniques": mitre_techniques,
        "feature_contributions": feature_contributions,
        "explanation": explanation
    }


@router.get("/mitre/{incident_id}", response_model=List[MITRETechnique])
async def get_mitre_mapping(incident_id: str):
    """Get MITRE ATT&CK mapping for incident"""
    
    incident = data_store.get_incident(incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident.mitre_techniques


@router.get("/explain/{incident_id}")
async def get_explanation(incident_id: str):
    """Get AI explanation for incident"""
    
    incident = data_store.get_incident(incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return {
        "incident_id": incident_id,
        "explanation": incident.explanation,
        "feature_contributions": incident.feature_contributions,
        "confidence": incident.anomaly_scores.confidence
    }


@router.get("/endpoints")
async def list_endpoints():
    """List all endpoints"""
    
    endpoints = telemetry_gen.get_endpoint_list()
    return {"endpoints": endpoints}
