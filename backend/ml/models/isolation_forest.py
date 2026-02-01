"""
Isolation Forest Model for Anomaly Detection
"""
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Tuple
from config import settings


class IsolationForestDetector:
    """Isolation Forest for anomaly detection"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.contamination = settings.ISOLATION_FOREST_CONTAMINATION
        self.n_estimators = settings.ISOLATION_FOREST_ESTIMATORS
    
    def train(self, X_train: np.ndarray):
        """
        Train Isolation Forest on normal data
        
        Args:
            X_train: Training data (should be mostly normal)
        """
        # Normalize data
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Train Isolation Forest
        self.model = IsolationForest(
            n_estimators=self.n_estimators,
            contamination=self.contamination,
            random_state=42,
            n_jobs=-1
        )
        
        self.model.fit(X_train_scaled)
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies
        
        Args:
            X: Input data
            
        Returns:
            Tuple of (anomaly_scores, is_anomaly)
        """
        X_scaled = self.scaler.transform(X)
        
        # Get predictions (-1 for anomaly, 1 for normal)
        predictions = self.model.predict(X_scaled)
        is_anomaly = predictions == -1
        
        # Get decision scores (negative means anomaly)
        decision_scores = self.model.decision_function(X_scaled)
        
        return decision_scores, is_anomaly
    
    def get_anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """
        Get normalized anomaly scores (0-1 range)
        
        Args:
            X: Input data
            
        Returns:
            Anomaly scores (higher = more anomalous)
        """
        decision_scores, _ = self.predict(X)
        
        # Convert decision scores to 0-1 range
        # Decision scores are typically in range [-0.5, 0.5]
        # More negative = more anomalous
        scores = 1 / (1 + np.exp(decision_scores * 10))  # Sigmoid transformation
        
        return scores
    
    def save(self, path: str):
        """Save model and scaler"""
        os.makedirs(path, exist_ok=True)
        
        with open(os.path.join(path, 'isolation_forest.pkl'), 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler
            }, f)
    
    def load(self, path: str):
        """Load model and scaler"""
        with open(os.path.join(path, 'isolation_forest.pkl'), 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']


if __name__ == "__main__":
    # Test Isolation Forest
    from data.telemetry_generator import TelemetryGenerator
    
    print("Generating test data...")
    gen = TelemetryGenerator(num_endpoints=10)
    df = gen.generate_normal_traffic(num_samples=1000)
    
    X = df[settings.FEATURES].values
    
    print(f"Training Isolation Forest on {len(X)} samples...")
    iforest = IsolationForestDetector()
    iforest.train(X)
    
    # Test prediction
    scores = iforest.get_anomaly_score(X[:10])
    print(f"\nSample anomaly scores: {scores}")
