"""
Database models for incidents, logs, and endpoint data
"""
from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class EndpointMetadata(BaseModel):
    """Endpoint information"""
    id: str
    hostname: str
    ip: str
    role: str
    os: str
    status: str = "healthy"
    last_seen: datetime = Field(default_factory=datetime.now)


class TelemetryPoint(BaseModel):
    """Single telemetry data point"""
    endpoint_id: str
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    network_in: float
    network_out: float
    failed_logins: float
    process_creation: float
    disk_read: float
    disk_write: float
    file_access: float
    api_calls: float
    dns_queries: float
    auth_attempts: float
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class AnomalyScore(BaseModel):
    """ML model anomaly scores"""
    autoencoder_score: float
    isolation_forest_score: float
    lof_score: float
    lstm_score: Optional[float] = None
    ensemble_score: float
    is_anomaly: bool
    confidence: float


class MITRETechnique(BaseModel):
    """MITRE ATT&CK technique mapping"""
    technique_id: str
    name: str
    tactic: str
    confidence: float
    matched_features: List[str]
    description: str


class FeatureContribution(BaseModel):
    """Explainable AI feature contribution"""
    feature: str
    value: float
    baseline_mean: float
    deviation: float
    deviation_multiplier: float
    contribution_percent: float


class Incident(BaseModel):
    """Security incident"""
    id: str
    endpoint_id: str
    timestamp: datetime
    severity: str  # low, medium, high, critical
    status: str = "open"  # open, investigating, resolved, false_positive
    attack_type: Optional[str] = None
    anomaly_scores: AnomalyScore
    mitre_techniques: List[MITRETechnique]
    feature_contributions: List[FeatureContribution]
    explanation: str
    telemetry_snapshot: Dict
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class IncidentReport(BaseModel):
    """PDF incident report metadata"""
    incident_id: str
    generated_at: datetime
    file_path: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class DashboardStats(BaseModel):
    """Dashboard statistics"""
    total_endpoints: int
    healthy_endpoints: int
    at_risk_endpoints: int
    total_incidents: int
    critical_incidents: int
    risk_score: float
    active_threats: int
    false_positives: int
    detection_rate: float
    
    class Config:
        arbitrary_types_allowed = True
