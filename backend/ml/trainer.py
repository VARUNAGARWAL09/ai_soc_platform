"""
Model Training Orchestrator
Trains all ML models on normal traffic data
"""
import numpy as np
import pandas as pd
from typing import Dict
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from data.telemetry_generator import TelemetryGenerator
from data.attack_simulator import AttackSimulator
from ml.models.autoencoder import DeepAutoencoder
from ml.models.isolation_forest import IsolationForestDetector
from ml.models.lof import LOFDetector
from ml.models.lstm_detector import LSTMDetector


class ModelTrainer:
    """Orchestrates training of all ML models"""
    
    def __init__(self):
        self.models = {}
        self.telemetry_gen = TelemetryGenerator(num_endpoints=settings.NUM_ENDPOINTS)
        self.attack_sim = AttackSimulator(self.telemetry_gen)
    
    def generate_training_data(self) -> pd.DataFrame:
        """Generate pure normal traffic for training"""
        print(f"Generating {settings.NORMAL_DATA_POINTS} normal traffic samples...")
        
        df = self.telemetry_gen.generate_normal_traffic(
            num_samples=settings.NORMAL_DATA_POINTS,
            time_series=True
        )
        
        print(f"Generated {len(df)} samples with {len(settings.FEATURES)} features")
        return df
    
    def train_all_models(self) -> Dict:
        """Train all detection models"""
        # Generate training data
        df_train = self.generate_training_data()
        X_train = df_train[settings.FEATURES].values
        
        print(f"\nTraining data shape: {X_train.shape}")
        print(f"Features: {settings.FEATURES}\n")
        
        results = {}
        
        # Train Autoencoder
        print("=" * 60)
        print("Training Deep Autoencoder...")
        print("=" * 60)
        ae = DeepAutoencoder(input_dim=len(settings.FEATURES))
        ae_history = ae.train(X_train, validation_split=0.2)
        results['autoencoder'] = {
            'final_loss': ae_history['loss'][-1],
            'final_val_loss': ae_history['val_loss'][-1],
            'threshold': ae.threshold
        }
        self.models['autoencoder'] = ae
        print(f"Autoencoder trained. Threshold: {ae.threshold:.4f}\n")
        
        # Train Isolation Forest
        print("=" * 60)
        print("Training Isolation Forest...")
        print("=" * 60)
        iforest = IsolationForestDetector()
        iforest.train(X_train)
        self.models['isolation_forest'] = iforest
        print("Isolation Forest trained.\n")
        
        # Train LOF
        print("=" * 60)
        print("Training LOF...")
        print("=" * 60)
        lof = LOFDetector()
        lof.train(X_train)
        self.models['lof'] = lof
        print("LOF trained.\n")
        
        # Train LSTM
        print("=" * 60)
        print("Training LSTM Sequence Detector...")
        print("=" * 60)
        lstm = LSTMDetector(input_dim=len(settings.FEATURES))
        lstm_history = lstm.train(X_train, validation_split=0.2)
        results['lstm'] = {
            'final_loss': lstm_history['loss'][-1],
            'final_val_loss': lstm_history['val_loss'][-1],
            'threshold': lstm.threshold
        }
        self.models['lstm'] = lstm
        print(f"LSTM trained. Threshold: {lstm.threshold:.4f}\n")
        
        return results
    
    def save_models(self):
        """Save all trained models"""
        print("=" * 60)
        print("Saving models...")
        print("=" * 60)
        
        model_dir = settings.MODEL_DIR
        
        for name, model in self.models.items():
            print(f"Saving {name}...")
            model.save(model_dir)
        
        print(f"\nAll models saved to: {model_dir}")
    
    def run(self):
        """Run complete training pipeline"""
        print("\n" + "=" * 60)
        print("AI SOC PLATFORM - MODEL TRAINING")
        print("=" * 60)
        print(f"Endpoints: {settings.NUM_ENDPOINTS}")
        print(f"Normal samples: {settings.NORMAL_DATA_POINTS}")
        print(f"Features: {len(settings.FEATURES)}")
        print("=" * 60 + "\n")
        
        # Train models
        results = self.train_all_models()
        
        # Save models
        self.save_models()
        
        print("\n" + "=" * 60)
        print("TRAINING COMPLETE")
        print("=" * 60)
        print("\nTraining Results:")
        for model_name, metrics in results.items():
            print(f"\n{model_name.upper()}:")
            for metric_name, value in metrics.items():
                print(f"  {metric_name}: {value:.4f}")
        
        return results


if __name__ == "__main__":
    trainer = ModelTrainer()
    trainer.run()
