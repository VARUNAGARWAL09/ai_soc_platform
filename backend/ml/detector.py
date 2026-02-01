"""
Ensemble Anomaly Detector
Combines multiple models for robust detection with realistic accuracy
"""
import numpy as np
import pandas as pd
from typing import Dict, Tuple, List
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from ml.models.autoencoder import DeepAutoencoder
from ml.models.isolation_forest import IsolationForestDetector
from ml.models.lof import LOFDetector
from ml.models.lstm_detector import LSTMDetector
from models import AnomalyScore


class EnsembleDetector:
    """Ensemble detector combining multiple ML models"""
    
    def __init__(self):
        self.autoencoder = DeepAutoencoder()
        self.isolation_forest = IsolationForestDetector()
        self.lof = LOFDetector()
        self.lstm = LSTMDetector()
        self.models_loaded = False
        self.ensemble_threshold = settings.ENSEMBLE_THRESHOLD
    
    def load_models(self, model_dir: str = None):
        """Load all trained models"""
        model_dir = model_dir or settings.MODEL_DIR
        
        print(f"Loading models from {model_dir}...")
        
        self.autoencoder.load(model_dir)
        self.isolation_forest.load(model_dir)
        self.lof.load(model_dir)
        self.lstm.load(model_dir)
        
        self.models_loaded = True
        print("All models loaded successfully.")
    
    def detect(self, X: np.ndarray, apply_realism: bool = True) -> List[AnomalyScore]:
        """
        Detect anomalies using ensemble of models
        
        Args:
            X: Input data [samples, features]
            apply_realism: Whether to apply realistic false positive/negative rates
            
        Returns:
            List of AnomalyScore objects
        """
        if not self.models_loaded:
            raise RuntimeError("Models not loaded. Call load_models() first.")
        
        # Get scores from each model
        ae_scores = self.autoencoder.get_anomaly_score(X)
        if_scores = self.isolation_forest.get_anomaly_score(X)
        lof_scores = self.lof.get_anomaly_score(X)
        
        # LSTM requires sequences, so handle differently
        lstm_scores = None
        if len(X) >= self.lstm.sequence_length:
            lstm_scores = self.lstm.get_anomaly_score(X)
            # Pad LSTM scores to match length (sequences are shorter)
            if len(lstm_scores) > 0:
                padding = len(X) - len(lstm_scores)
                lstm_scores = np.pad(lstm_scores, (padding, 0), mode='edge')
        
        results = []
        
        for i in range(len(X)):
            # Individual scores
            ae_score = float(ae_scores[i])
            if_score = float(if_scores[i])
            lof_score = float(lof_scores[i])
            lstm_score = float(lstm_scores[i]) if lstm_scores is not None and i < len(lstm_scores) else None
            
            # Ensemble score (average of available models)
            scores_list = [ae_score, if_score, lof_score]
            if lstm_score is not None:
                scores_list.append(lstm_score)
            
            ensemble_score = np.mean(scores_list)
            
            # Determine if anomaly
            is_anomaly = ensemble_score > self.ensemble_threshold
            
            # Apply realism: introduce false positives and false negatives
            if apply_realism:
                is_anomaly = self._apply_realism(is_anomaly, ensemble_score)
            
            # Calculate confidence (variance-based)
            confidence = self._calculate_confidence(scores_list, ensemble_score)
            
            # Create AnomalyScore object
            anomaly_score = AnomalyScore(
                autoencoder_score=ae_score,
                isolation_forest_score=if_score,
                lof_score=lof_score,
                lstm_score=lstm_score,
                ensemble_score=ensemble_score,
                is_anomaly=is_anomaly,
                confidence=confidence
            )
            
            results.append(anomaly_score)
        
        return results
    
    def _apply_realism(self, is_anomaly: bool, ensemble_score: float) -> bool:
        """
        Apply realistic false positive and false negative rates
        
        Args:
            is_anomaly: Initial detection result
            ensemble_score: Ensemble score
            
        Returns:
            Adjusted detection result
        """
        # False positives: normal flagged as anomaly
        if not is_anomaly and np.random.random() < settings.FALSE_POSITIVE_RATE:
            # Lower scores more likely to be false positives
            if ensemble_score > 0.4:
                return True
        
        # False negatives: anomaly missed
        if is_anomaly and np.random.random() < settings.MISSED_DETECTION_RATE:
            # Borderline cases more likely to be missed
            if ensemble_score < 0.75:
                return False
        
        return is_anomaly
    
    def _calculate_confidence(self, scores_list: List[float], ensemble_score: float) -> float:
        """
        Calculate confidence based on model agreement
        
        Args:
            scores_list: Individual model scores
            ensemble_score: Ensemble score
            
        Returns:
            Confidence value (0-1)
        """
        # Variance-based confidence: low variance = high confidence
        variance = np.var(scores_list)
        
        # Normalize variance to confidence
        # High variance (disagreement) = low confidence
        confidence = 1.0 / (1.0 + variance * 5)
        
        # Boost confidence for extreme scores
        if ensemble_score > 0.8 or ensemble_score < 0.2:
            confidence *= 1.1
        
        # Realistic confidence range: 0.65 - 0.95
        confidence = np.clip(confidence, 0.65, 0.95)
        
        return float(confidence)
    
    def detect_single(self, features: Dict[str, float]) -> AnomalyScore:
        """
        Detect anomaly for a single sample
        
        Args:
            features: Feature dictionary
            
        Returns:
            AnomalyScore object
        """
        # Convert to array
        X = np.array([[features[f] for f in settings.FEATURES]])
        
        # Detect
        results = self.detect(X, apply_realism=True)
        
        return results[0]


if __name__ == "__main__":
    # Test ensemble detector
    from data.telemetry_generator import TelemetryGenerator
    from data.attack_simulator import AttackSimulator
    
    # Generate test data
    gen = TelemetryGenerator(num_endpoints=10)
    sim = AttackSimulator(gen)
    
    # Load models (assumes models are trained)
    detector = EnsembleDetector()
    try:
        detector.load_models()
        
        # Test on normal data
        df_normal = gen.generate_normal_traffic(num_samples=10)
        X_normal = df_normal[settings.FEATURES].values
        
        print("Testing on normal data...")
        results = detector.detect(X_normal)
        
        anomalies = sum([1 for r in results if r.is_anomaly])
        print(f"Detected {anomalies}/{len(results)} anomalies in normal data")
        
        # Test on attack data
        print("\nTesting on attack data...")
        attack_seq = sim.generate_attack_sequence("brute_force", duration_seconds=20)
        df_attack = pd.DataFrame(attack_seq)
        X_attack = df_attack[settings.FEATURES].values
        
        results = detector.detect(X_attack)
        anomalies = sum([1 for r in results if r.is_anomaly])
        print(f"Detected {anomalies}/{len(results)} anomalies in attack data")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Models not trained yet. Run trainer.py first.")
