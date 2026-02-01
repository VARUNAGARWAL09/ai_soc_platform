"""
Configuration management for AI SOC Platform
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # API Configuration
    API_TITLE: str = "AI SOC Platform API"
    API_VERSION: str = "1.0.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # Data Generation
    NUM_ENDPOINTS: int = 75
    NORMAL_DATA_POINTS: int = 10000
    ATTACK_DATA_POINTS: int = 1200
    FEATURES: List[str] = [
        "cpu_usage",
        "memory_usage",
        "network_in",
        "network_out",
        "failed_logins",
        "process_creation",
        "disk_read",
        "disk_write",
        "file_access",
        "api_calls",
        "dns_queries",
        "auth_attempts"
    ]
    
    # ML Model Parameters
    AUTOENCODER_ENCODING_DIM: int = 6
    AUTOENCODER_EPOCHS: int = 5
    AUTOENCODER_BATCH_SIZE: int = 32
    
    ISOLATION_FOREST_CONTAMINATION: float = 0.1
    ISOLATION_FOREST_ESTIMATORS: int = 100
    
    LOF_NEIGHBORS: int = 20
    LOF_CONTAMINATION: float = 0.1
    
    LSTM_SEQUENCE_LENGTH: int = 10
    LSTM_EPOCHS: int = 5
    
    # Anomaly Detection Thresholds
    AUTOENCODER_THRESHOLD: float = 2.5  # Z-score threshold
    ENSEMBLE_THRESHOLD: float = 0.55  # Percentage of models agreeing
    
    # Paths
    BASE_DIR: str = os.path.dirname(os.path.abspath(__file__))
    MODEL_DIR: str = os.path.join(BASE_DIR, "models_saved")
    REPORT_DIR: str = os.path.join(BASE_DIR, "reports", "generated")
    
    # Streaming
    TELEMETRY_STREAM_INTERVAL: float = 2.0  # seconds
    MAX_WEBSOCKET_CONNECTIONS: int = 100
    
    # Realism Settings
    FALSE_POSITIVE_RATE: float = 0.08  # 8% false positive rate
    MISSED_DETECTION_RATE: float = 0.12  # 12% false negative rate
    
    class Config:
        env_file = ".env"


settings = Settings()

# Ensure directories exist
os.makedirs(settings.MODEL_DIR, exist_ok=True)
os.makedirs(settings.REPORT_DIR, exist_ok=True)
