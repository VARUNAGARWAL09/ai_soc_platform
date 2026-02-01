"""
Realistic Synthetic Telemetry Data Generator
Simulates 50-100 endpoints with realistic behavior patterns
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from config import settings


class TelemetryGenerator:
    """Generates realistic endpoint telemetry data"""
    
    def __init__(self, num_endpoints: int = None):
        self.num_endpoints = num_endpoints or settings.NUM_ENDPOINTS
        self.features = settings.FEATURES
        
        # Define realistic baseline ranges for each feature
        self.baselines = {
            "cpu_usage": {"mean": 25.0, "std": 8.0, "min": 0, "max": 100},
            "memory_usage": {"mean": 45.0, "std": 12.0, "min": 0, "max": 100},
            "network_in": {"mean": 150.0, "std": 50.0, "min": 0, "max": 2000},  # MB/s
            "network_out": {"mean": 80.0, "std": 30.0, "min": 0, "max": 2000},
            "failed_logins": {"mean": 0.5, "std": 0.8, "min": 0, "max": 50},
            "process_creation": {"mean": 5.0, "std": 3.0, "min": 0, "max": 100},
            "disk_read": {"mean": 200.0, "std": 80.0, "min": 0, "max": 5000},  # MB/s
            "disk_write": {"mean": 100.0, "std": 50.0, "min": 0, "max": 5000},
            "file_access": {"mean": 50.0, "std": 20.0, "min": 0, "max": 1000},
            "api_calls": {"mean": 100.0, "std": 40.0, "min": 0, "max": 2000},
            "dns_queries": {"mean": 30.0, "std": 15.0, "min": 0, "max": 500},
            "auth_attempts": {"mean": 2.0, "std": 1.5, "min": 0, "max": 50}
        }
        
        # Endpoint metadata
        self.endpoints = self._generate_endpoint_metadata()
    
    def _generate_endpoint_metadata(self) -> List[Dict]:
        """Generate metadata for each endpoint"""
        endpoints = []
        roles = ["workstation", "server", "database", "web_server", "file_server"]
        
        for i in range(self.num_endpoints):
            endpoints.append({
                "id": f"EP-{i:04d}",
                "hostname": f"host-{i:04d}",
                "ip": f"10.{(i // 256) % 256}.{(i // 256) % 256}.{i % 256}",
                "role": np.random.choice(roles),
                "os": np.random.choice(["Windows 10", "Windows Server 2019", "Ubuntu 20.04", "CentOS 8"])
            })
        
        return endpoints
    
    def generate_normal_traffic(self, num_samples: int, time_series: bool = True) -> pd.DataFrame:
        """
        Generate normal traffic data with realistic patterns
        
        Args:
            num_samples: Number of samples to generate
            time_series: Whether to add temporal patterns
            
        Returns:
            DataFrame with normal telemetry data
        """
        data = []
        start_time = datetime.now() - timedelta(hours=24)
        
        for i in range(num_samples):
            sample = {}
            
            # Select random endpoint
            endpoint = np.random.choice(self.endpoints)
            sample["endpoint_id"] = endpoint["id"]
            sample["timestamp"] = start_time + timedelta(seconds=i * 2)
            
            # Generate features with realistic distributions
            for feature in self.features:
                baseline = self.baselines[feature]
                
                # Add time-based patterns (business hours have different patterns)
                hour = sample["timestamp"].hour
                time_multiplier = 1.0
                
                if time_series:
                    # Business hours (9-17): higher activity
                    if 9 <= hour <= 17:
                        time_multiplier = 1.3
                    # Night hours (22-6): lower activity
                    elif hour >= 22 or hour <= 6:
                        time_multiplier = 0.6
                
                # Generate value with Gaussian noise
                value = np.random.normal(
                    baseline["mean"] * time_multiplier,
                    baseline["std"]
                )
                
                # Add occasional spikes (normal variation)
                if np.random.random() < 0.05:  # 5% chance of spike
                    value *= np.random.uniform(1.5, 2.0)
                
                # Clip to realistic range
                value = np.clip(value, baseline["min"], baseline["max"])
                sample[feature] = value
            
            # Role-specific adjustments
            if endpoint["role"] == "web_server":
                sample["api_calls"] *= 2.0
                sample["network_in"] *= 1.5
            elif endpoint["role"] == "database":
                sample["disk_read"] *= 1.8
                sample["disk_write"] *= 1.5
            elif endpoint["role"] == "file_server":
                sample["file_access"] *= 2.5
            
            data.append(sample)
        
        df = pd.DataFrame(data)
        return df
    
    def generate_telemetry_point(self, endpoint_id: str = None) -> Dict:
        """
        Generate a single telemetry point for real-time streaming
        
        Args:
            endpoint_id: Specific endpoint ID, or random if None
            
        Returns:
            Dictionary with telemetry data
        """
        if endpoint_id is None:
            endpoint = np.random.choice(self.endpoints)
        else:
            endpoint = next((e for e in self.endpoints if e["id"] == endpoint_id), self.endpoints[0])
        
        sample = {
            "endpoint_id": endpoint["id"],
            "hostname": endpoint["hostname"],
            "ip": endpoint["ip"],
            "timestamp": datetime.now().isoformat(),
        }
        
        # Generate feature values
        hour = datetime.now().hour
        time_multiplier = 1.3 if 9 <= hour <= 17 else (0.6 if hour >= 22 or hour <= 6 else 1.0)
        
        for feature in self.features:
            baseline = self.baselines[feature]
            value = np.random.normal(
                baseline["mean"] * time_multiplier,
                baseline["std"]
            )
            value = np.clip(value, baseline["min"], baseline["max"])
            sample[feature] = round(value, 2)
        
        # Role adjustments
        if endpoint["role"] == "web_server":
            sample["api_calls"] = round(sample["api_calls"] * 2.0, 2)
        elif endpoint["role"] == "database":
            sample["disk_read"] = round(sample["disk_read"] * 1.8, 2)
        
        return sample
    
    def get_endpoint_list(self) -> List[Dict]:
        """Return list of all endpoints"""
        return self.endpoints
    
    def get_feature_baselines(self) -> Dict:
        """Return baseline values for all features"""
        return self.baselines


if __name__ == "__main__":
    # Test the generator
    gen = TelemetryGenerator(num_endpoints=75)
    
    print("Generating normal traffic...")
    normal_data = gen.generate_normal_traffic(num_samples=1000)
    print(f"Generated {len(normal_data)} normal samples")
    print(f"Features: {normal_data.columns.tolist()}")
    print("\nSample data:")
    print(normal_data.head())
    
    print("\n\nGenerating single telemetry point:")
    point = gen.generate_telemetry_point()
    print(point)
