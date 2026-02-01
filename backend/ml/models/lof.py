"""
Local Outlier Factor (LOF) Model for Anomaly Detection
"""
import numpy as np
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Tuple
from config import settings


class LOFDetector:
    """Local Outlier Factor for density-based anomaly detection"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.n_neighbors = settings.LOF_NEIGHBORS
        self.contamination = settings.LOF_CONTAMINATION
        self.X_train_scaled = None  # LOF needs training data for prediction
    
    def train(self, X_train: np.ndarray):
        """
        Train LOF on normal data
        
        Args:
            X_train: Training data (should be mostly normal)
        """
        # Normalize data
        self.X_train_scaled = self.scaler.fit_transform(X_train)
        
        # LOF with novelty=True allows predict on new data
        self.model = LocalOutlierFactor(
            n_neighbors=self.n_neighbors,
            contamination=self.contamination,
            novelty=True  # Allows prediction on new samples
        )
        
        self.model.fit(self.X_train_scaled)
    
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
        # LOF decision scores are typically in range [-2, 2]
        # More negative = more anomalous
        scores = 1 / (1 + np.exp(decision_scores * 3))  # Sigmoid transformation
        
        return scores
    
    def save(self, path: str):
        """Save model and scaler"""
        os.makedirs(path, exist_ok=True)
        
        with open(os.path.join(path, 'lof.pkl'), 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler
            }, f)
    
    def load(self, path: str):
        """Load model and scaler"""
        with open(os.path.join(path, 'lof.pkl'), 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']


if __name__ == "__main__":
    # Test LOF
    from data.telemetry_generator import TelemetryGenerator
    
    print("Generating test data...")
    gen = TelemetryGenerator(num_endpoints=10)
    df = gen.generate_normal_traffic(num_samples=1000)
    
    X = df[settings.FEATURES].values
    
    print(f"Training LOF on {len(X)} samples...")
    lof = LOFDetector()
    lof.train(X)
    
    # Test prediction
    scores = lof.get_anomaly_score(X[:10])
    print(f"\nSample anomaly scores: {scores}")
