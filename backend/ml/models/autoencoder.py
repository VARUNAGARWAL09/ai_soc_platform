"""
Deep Autoencoder Model for Anomaly Detection
"""
import numpy as np
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
except ImportError:
    tf = None
    keras = None
    layers = None

from sklearn.preprocessing import StandardScaler
import pickle
import os
from typing import Tuple
from config import settings


class DeepAutoencoder:
    """Deep Autoencoder for unsupervised anomaly detection"""
    
    def __init__(self, input_dim: int = None):
        self.input_dim = input_dim or len(settings.FEATURES)
        self.encoding_dim = settings.AUTOENCODER_ENCODING_DIM
        self.model = None
        self.scaler = StandardScaler()
        self.threshold = None
        self.mean_reconstruction_error = None
        self.std_reconstruction_error = None
    
    def build_model(self):
        """Build the autoencoder architecture"""
        if tf is None:
            print("TensorFlow not installed. Skipping model build.")
            return None

        # Encoder
        input_layer = layers.Input(shape=(self.input_dim,))
        
        # Deep encoder
        encoded = layers.Dense(32, activation='relu')(input_layer)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dropout(0.2)(encoded)
        
        encoded = layers.Dense(16, activation='relu')(encoded)
        encoded = layers.BatchNormalization()(encoded)
        encoded = layers.Dropout(0.2)(encoded)
        
        # Bottleneck
        encoded = layers.Dense(self.encoding_dim, activation='relu', name='bottleneck')(encoded)
        
        # Deep decoder
        decoded = layers.Dense(16, activation='relu')(encoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        
        decoded = layers.Dense(32, activation='relu')(decoded)
        decoded = layers.BatchNormalization()(decoded)
        decoded = layers.Dropout(0.2)(decoded)
        
        # Output layer
        decoded = layers.Dense(self.input_dim, activation='linear')(decoded)
        
        # Build model
        self.model = keras.Model(input_layer, decoded)
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='mse'
        )
        
        return self.model
    
    def train(self, X_train: np.ndarray, validation_split: float = 0.2) -> dict:
        """
        Train the autoencoder on normal data only
        
        Args:
            X_train: Training data (normal traffic only)
            validation_split: Validation split ratio
            
        Returns:
            Training history
        """
        if tf is None:
            return {}

        # Normalize data
        X_train_scaled = self.scaler.fit_transform(X_train)
        
        # Build model if not exists
        if self.model is None:
            self.build_model()
        
        # Train
        early_stopping = keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True
        )
        
        history = self.model.fit(
            X_train_scaled, X_train_scaled,
            epochs=settings.AUTOENCODER_EPOCHS,
            batch_size=settings.AUTOENCODER_BATCH_SIZE,
            validation_split=validation_split,
            callbacks=[early_stopping],
            verbose=1
        )
        
        # Calculate reconstruction error threshold
        self._calculate_threshold(X_train_scaled)
        
        return history.history
    
    def _calculate_threshold(self, X: np.ndarray):
        """Calculate anomaly threshold using Z-score"""
        if self.model is None:
            return

        reconstructed = self.model.predict(X, verbose=0)
        reconstruction_errors = np.mean(np.square(X - reconstructed), axis=1)
        
        self.mean_reconstruction_error = np.mean(reconstruction_errors)
        self.std_reconstruction_error = np.std(reconstruction_errors)
        
        # Set threshold at Z-score (configurable)
        z_score = settings.AUTOENCODER_THRESHOLD
        self.threshold = self.mean_reconstruction_error + z_score * self.std_reconstruction_error
    
    def predict(self, X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict anomalies
        
        Args:
            X: Input data
            
        Returns:
            Tuple of (reconstruction_errors, is_anomaly)
        """
        if tf is None or self.model is None:
             # Mock behavior for deployment without TF
            return np.zeros(len(X)), np.zeros(len(X), dtype=bool)

        X_scaled = self.scaler.transform(X)
        reconstructed = self.model.predict(X_scaled, verbose=0)
        
        # Calculate reconstruction error
        reconstruction_errors = np.mean(np.square(X_scaled - reconstructed), axis=1)
        
        # Determine anomalies
        is_anomaly = reconstruction_errors > self.threshold
        
        return reconstruction_errors, is_anomaly
    
    def get_anomaly_score(self, X: np.ndarray) -> np.ndarray:
        """
        Get normalized anomaly scores (0-1 range)
        
        Args:
            X: Input data
            
        Returns:
            Anomaly scores
        """
        reconstruction_errors, _ = self.predict(X)
        
        if self.mean_reconstruction_error is None:
             return np.zeros(len(X))

        # Z-score normalization
        z_scores = (reconstruction_errors - self.mean_reconstruction_error) / self.std_reconstruction_error
        
        # Convert to 0-1 range using sigmoid
        scores = 1 / (1 + np.exp(-z_scores))
        
        return scores
    
    def save(self, path: str):
        """Save model and scaler"""
        if self.model is None:
            return

        os.makedirs(path, exist_ok=True)
        
        # Save Keras model
        self.model.save(os.path.join(path, 'autoencoder_model.keras'))
        
        # Save scaler and stats
        with open(os.path.join(path, 'autoencoder_metadata.pkl'), 'wb') as f:
            pickle.dump({
                'scaler': self.scaler,
                'threshold': self.threshold,
                'mean_error': self.mean_reconstruction_error,
                'std_error': self.std_reconstruction_error,
                'input_dim': self.input_dim
            }, f)
    
    def load(self, path: str):
        """Load model and scaler"""
        if tf is None:
            print("TensorFlow not installed. Skipping model load.")
            return

        # Load Keras model
        if os.path.exists(os.path.join(path, 'autoencoder_model.keras')):
            self.model = keras.models.load_model(os.path.join(path, 'autoencoder_model.keras'))
        
        # Load scaler and stats
        if os.path.exists(os.path.join(path, 'autoencoder_metadata.pkl')):
            with open(os.path.join(path, 'autoencoder_metadata.pkl'), 'rb') as f:
                metadata = pickle.load(f)
                self.scaler = metadata['scaler']
                self.threshold = metadata['threshold']
                self.mean_reconstruction_error = metadata['mean_error']
                self.std_reconstruction_error = metadata['std_error']
                self.input_dim = metadata['input_dim']


if __name__ == "__main__":
    # Test the autoencoder
    from data.telemetry_generator import TelemetryGenerator
    
    print("Generating test data...")
    gen = TelemetryGenerator(num_endpoints=10)
    df = gen.generate_normal_traffic(num_samples=1000)
    
    X = df[settings.FEATURES].values
    
    print(f"Training autoencoder on {len(X)} samples...")
    ae = DeepAutoencoder(input_dim=X.shape[1])
    history = ae.train(X)
    
    print(f"\nFinal training loss: {history['loss'][-1]:.4f}")
    print(f"Threshold: {ae.threshold:.4f}")
    
    # Test prediction
    scores = ae.get_anomaly_score(X[:10])
    print(f"\nSample anomaly scores: {scores}")
