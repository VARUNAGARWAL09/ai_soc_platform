"""
LSTM-based Sequence Anomaly Detector
"""
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Tuple
from config import settings


class LSTMDetector:
    """LSTM for temporal sequence anomaly detection"""
    
    def __init__(self, input_dim: int = None):
        self.input_dim = input_dim or len(settings.FEATURES)
        self.sequence_length = settings.LSTM_SEQUENCE_LENGTH
        self.model = None
        self.scaler = StandardScaler()
        self.threshold = None
        self.mean_error = None
        self.std_error = None
    
    def build_model(self):
        """Build LSTM autoencoder"""
        # Input
        input_layer = layers.Input(shape=(self.sequence_length, self.input_dim))
        
        # Encoder
        encoded = layers.LSTM(64, activation='relu', return_sequences=True)(input_layer)
        encoded = layers.Dropout(0.2)(encoded)
        encoded = layers.LSTM(32, activation='relu', return_sequences=False)(encoded)
        encoded = layers.Dropout(0.2)(encoded)
        
        # Repeat vector for decoder
        decoded = layers.RepeatVector(self.sequence_length)(encoded)
        
        # Decoder
        decoded = layers.LSTM(32, activation='relu', return_sequences=True)(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        decoded = layers.LSTM(64, activation='relu', return_sequences=True)(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        
        # Output
        output = layers.TimeDistributed(layers.Dense(self.input_dim))(decoded)
        
        self.model = keras.Model(input_layer, output)
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse'
        )
        
        return self.model
    
    def create_sequences(self, X: np.ndarray) -> np.ndarray:
        """
        Create sequences for LSTM input
        
        Args:
            X: Input data [samples, features]
            
        Returns:
            Sequences [samples - seq_length, seq_length, features]
        """
        sequences = []
        for i in range(len(X) - self.sequence_length + 1):
            sequences.append(X[i:i + self.sequence_length])
        
        return np.array(sequences)
    
    def train(self, X_train: np.ndarray, validation_split: float = 0.2) -> dict:
        """
        Train LSTM on normal sequences
        
        Args:
            X_train: Training data
            validation_split: Validation ratio
            
        Returns:
            Training history
        """
        # Normalize
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Create sequences
        X_sequences = self.create_sequences(X_train_scaled)
        
        print(f"Created {len(X_sequences)} sequences of length {self.sequence_length}")
        
        # Build model
        if self.model is None:
            self.build_model()
        
        # Train
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        history = self.model.fit(
            X_sequences, X_sequences,
            epochs=settings.LSTM_EPOCHS,
            batch_size=32,
            validation_split=validation_split,
            callbacks=[early_stopping],
            verbose=1
        )
        
        # Calculate threshold
        self._calculate_threshold(X_sequences)
        
        return history.history
    
    def _calculate_threshold(self, X_sequences: np.ndarray):
        """Calculate reconstruction error threshold"""
        reconstructed = self.model.predict(X_sequences, verbose=0)
        errors = np.mean(np.square(X_sequences - reconstructed), axis=(1, 2))
        
        self.mean_error = np.mean(errors)
        self.std_error = np.std(errors)
        
        # Set threshold at 2.5 standard deviations
        self.threshold = self.mean_error + 2.5 * self.std_error
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies in sequences
        
        Args:
            X: Input data
            
        Returns:
            Tuple of (reconstruction_errors, is_anomaly)
        """
        X_scaled = self.scaler.transform(X)
        X_sequences = self.create_sequences(X_scaled)
        
        if len(X_sequences) == 0:
            return np.array([]), np.array([])
        
        reconstructed = self.model.predict(X_sequences, verbose=0)
        errors = np.mean(np.square(X_sequences - reconstructed), axis=(1, 2))
        
        is_anomaly = errors > self.threshold
        
        return errors, is_anomaly
    
    def get_anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """
        Get normalized anomaly scores
        
        Args:
            X: Input data
            
        Returns:
            Anomaly scores (0-1 range)
        """
        errors, _ = self.predict(X)
        
        if len(errors) == 0:
            return np.array([])
        
        # Z-score normalization
        z_scores = (errors - self.mean_error) / self.std_error
        
        # Sigmoid
        scores = 1 / (1 + np.exp(-z_scores))
        
        return scores
    
    def save(self, path: str):
        """Save model"""
        os.makedirs(path, exist_ok=True)
        
        self.model.save(os.path.join(path, 'lstm_model.keras'))
        
        with open(os.path.join(path, 'lstm_metadata.pkl'), 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'threshold': self.threshold,
                'mean_error': self.mean_error,
                'std_error': self.std_error,
                'input_dim': self.input_dim,
                'sequence_length': self.sequence_length
            }, f)
    
    def load(self, path: str):
        """Load model"""
        self.model = keras.models.load_model(os.path.join(path, 'lstm_model.keras'))
        
        with open(os.path.join(path, 'lstm_metadata.pkl'), 'rb') as f:
            metadata = pickle.load(f)
            self.scaler = metadata['scaler']
            self.threshold = metadata['threshold']
            self.mean_error = metadata['mean_error']
            self.std_error = metadata['std_error']
            self.input_dim = metadata['input_dim']
            self.sequence_length = metadata['sequence_length']


if __name__ == "__main__":
    # Test LSTM
    from data.telemetry_generator import TelemetryGenerator
    
    print("Generating test data...")
    gen = TelemetryGenerator(num_endpoints=10)
    df = gen.generate_normal_traffic(num_samples=200)
    
    X = df[settings.FEATURES].values
    
    print(f"Training LSTM on {len(X)} samples...")
    lstm = LSTMDetector(input_dim=X.shape[1])
    history = lstm.train(X)
    
    print(f"\nFinal training loss: {history['loss'][-1]:.4f}")
    
    # Test prediction
    errors, anomalies = lstm.predict(X)
    print(f"Detected {anomalies.sum()} anomalies")
