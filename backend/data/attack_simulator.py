"""
Attack Scenario Simulator
Generates realistic attack patterns mapped to MITRE ATT&CK techniques
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
from data.telemetry_generator import TelemetryGenerator


class AttackSimulator:
    """Simulates various attack scenarios with MITRE ATT&CK mappings"""
    
    def __init__(self, telemetry_gen: TelemetryGenerator):
        self.telemetry_gen = telemetry_gen
        self.baselines = telemetry_gen.get_feature_baselines()
        
        # Attack type definitions with MITRE mappings
        self.attack_types = {
            "brute_force": {
                "mitre_id": "T1110",
                "name": "Brute Force",
                "tactic": "Credential Access",
                "features": {
                    "failed_logins": {"multiplier": (8, 15), "spike": True},
                    "auth_attempts": {"multiplier": (6, 12), "spike": True},
                    "network_in": {"multiplier": (1.5, 2.0), "spike": False}
                }
            },
            "crypto_mining": {
                "mitre_id": "T1496",
                "name": "Resource Hijacking",
                "tactic": "Impact",
                "features": {
                    "cpu_usage": {"multiplier": (3.5, 5.0), "spike": False},
                    "network_out": {"multiplier": (2.0, 3.5), "spike": False},
                    "process_creation": {"multiplier": (2.5, 4.0), "spike": False}
                }
            },
            "data_exfiltration": {
                "mitre_id": "T1048",
                "name": "Exfiltration Over Alternative Protocol",
                "tactic": "Exfiltration",
                "features": {
                    "network_out": {"multiplier": (4.0, 8.0), "spike": True},
                    "disk_read": {"multiplier": (3.0, 5.0), "spike": False},
                    "file_access": {"multiplier": (3.5, 6.0), "spike": False},
                    "dns_queries": {"multiplier": (2.0, 3.0), "spike": False}
                }
            },
            "privilege_escalation": {
                "mitre_id": "T1068",
                "name": "Exploitation for Privilege Escalation",
                "tactic": "Privilege Escalation",
                "features": {
                    "process_creation": {"multiplier": (4.0, 7.0), "spike": True},
                    "api_calls": {"multiplier": (3.0, 5.0), "spike": False},
                    "memory_usage": {"multiplier": (2.0, 3.0), "spike": False},
                    "failed_logins": {"multiplier": (2.0, 4.0), "spike": False}
                }
            },
            "command_control": {
                "mitre_id": "T1071",
                "name": "Application Layer Protocol",
                "tactic": "Command and Control",
                "features": {
                    "network_out": {"multiplier": (2.5, 4.0), "spike": False},
                    "network_in": {"multiplier": (2.0, 3.5), "spike": False},
                    "dns_queries": {"multiplier": (4.0, 8.0), "spike": True},
                    "api_calls": {"multiplier": (2.5, 4.5), "spike": False}
                }
            },
            "lateral_movement": {
                "mitre_id": "T1021",
                "name": "Remote Services",
                "tactic": "Lateral Movement",
                "features": {
                    "network_in": {"multiplier": (3.0, 5.0), "spike": False},
                    "auth_attempts": {"multiplier": (3.0, 6.0), "spike": True},
                    "process_creation": {"multiplier": (2.5, 4.0), "spike": False},
                    "failed_logins": {"multiplier": (2.0, 4.0), "spike": False}
                }
            },
            "zero_day_blend": {
                "mitre_id": "T1190",
                "name": "Exploit Public-Facing Application",
                "tactic": "Initial Access",
                "features": {
                    "cpu_usage": {"multiplier": (2.0, 3.5), "spike": False},
                    "memory_usage": {"multiplier": (2.5, 4.0), "spike": False},
                    "network_in": {"multiplier": (3.0, 5.0), "spike": True},
                    "api_calls": {"multiplier": (4.0, 7.0), "spike": True},
                    "process_creation": {"multiplier": (2.0, 3.5), "spike": False}
                }
            },
            "sql_injection": {
                "mitre_id": "T1190",
                "name": "SQL Injection Attack",
                "tactic": "Initial Access",
                "features": {
                    "api_calls": {"multiplier": (5.0, 9.0), "spike": True},
                    "network_in": {"multiplier": (2.0, 3.0), "spike": False},
                    "cpu_usage": {"multiplier": (1.5, 2.5), "spike": False},
                    "failed_logins": {"multiplier": (1.0, 1.2), "spike": False}
                }
            },
            "ransomware_deployment": {
                "mitre_id": "T1486",
                "name": "Data Encrypted for Impact",
                "tactic": "Impact",
                "features": {
                    "disk_read": {"multiplier": (5.0, 10.0), "spike": True},
                    "disk_write": {"multiplier": (5.0, 10.0), "spike": True},
                    "cpu_usage": {"multiplier": (4.0, 6.0), "spike": False},
                    "process_creation": {"multiplier": (2.0, 3.0), "spike": False}
                }
            },
            "phishing_execution": {
                "mitre_id": "T1204",
                "name": "User Execution: Malicious File",
                "tactic": "Execution",
                "features": {
                    "process_creation": {"multiplier": (3.0, 5.0), "spike": True},
                    "network_out": {"multiplier": (2.0, 4.0), "spike": False},
                    "memory_usage": {"multiplier": (1.5, 2.5), "spike": False},
                    "dns_queries": {"multiplier": (2.0, 3.0), "spike": True}
                }
            },
             "insider_threat": {
                "mitre_id": "T1078",
                "name": "Valid Accounts: Local Accounts",
                "tactic": "Defense Evasion",
                "features": {
                    "file_access": {"multiplier": (5.0, 8.0), "spike": True},
                    "network_out": {"multiplier": (3.0, 5.0), "spike": False},
                    "auth_attempts": {"multiplier": (1.0, 2.0), "spike": False},
                    "disk_read": {"multiplier": (3.0, 5.0), "spike": False} 
                }
            }
        }
    
    def generate_attack_sequence(self, attack_type: str, endpoint_id: str = None, 
                                 duration_seconds: int = 60) -> List[Dict]:
        """
        Generate a time-series attack sequence
        
        Args:
            attack_type: Type of attack to simulate
            endpoint_id: Target endpoint, or random if None
            duration_seconds: Duration of attack
            
        Returns:
            List of telemetry dictionaries forming attack sequence
        """
        if attack_type not in self.attack_types:
            raise ValueError(f"Unknown attack type: {attack_type}")
        
        attack_def = self.attack_types[attack_type]
        sequence = []
        
        # Select endpoint
        if endpoint_id is None:
            endpoint = np.random.choice(self.telemetry_gen.endpoints)
            endpoint_id = endpoint["id"]
        
        start_time = datetime.now()
        
        # Generate attack progression
        num_points = duration_seconds // 2  # One point every 2 seconds
        
        for i in range(num_points):
            # Get normal baseline
            point = self.telemetry_gen.generate_telemetry_point(endpoint_id)
            point["timestamp"] = (start_time + timedelta(seconds=i * 2)).isoformat()
            
            # Apply attack modifications
            intensity = self._calculate_attack_intensity(i, num_points)
            
            for feature, params in attack_def["features"].items():
                if feature in point:
                    baseline_value = point[feature]
                    multiplier_range = params["multiplier"]
                    multiplier = np.random.uniform(multiplier_range[0], multiplier_range[1])
                    
                    # Apply intensity curve
                    effective_multiplier = 1.0 + (multiplier - 1.0) * intensity
                    
                    # Add spike behavior
                    if params["spike"] and np.random.random() < 0.3:
                        effective_multiplier *= np.random.uniform(1.2, 1.5)
                    
                    point[feature] = round(baseline_value * effective_multiplier, 2)
                    
                    # Clip to max
                    feature_max = self.baselines[feature]["max"]
                    point[feature] = min(point[feature], feature_max)
            
            # Add attack metadata
            point["attack_type"] = attack_type
            point["mitre_technique"] = attack_def["mitre_id"]
            point["is_attack"] = True
            
            sequence.append(point)
        
        return sequence
    
    def _calculate_attack_intensity(self, current_step: int, total_steps: int) -> float:
        """
        Calculate attack intensity over time (realistic progression)
        
        Returns:
            Intensity value between 0 and 1
        """
        progress = current_step / total_steps
        
        # Bell curve: slow start, peak in middle, taper off
        if progress < 0.3:
            # Ramp up
            return progress / 0.3 * 0.7
        elif progress < 0.7:
            # Peak
            return 0.7 + (progress - 0.3) / 0.4 * 0.3  # Up to 1.0
        else:
            # Taper
            return 1.0 - (progress - 0.7) / 0.3 * 0.4  # Down to 0.6
    
    def generate_mixed_dataset(self, num_normal: int, num_attacks: int) -> pd.DataFrame:
        """
        Generate a mixed dataset with normal and attack data
        
        Args:
            num_normal: Number of normal samples
            num_attacks: Number of attack samples
            
        Returns:
            DataFrame with mixed data
        """
        # Generate normal data
        normal_data = self.telemetry_gen.generate_normal_traffic(num_normal)
        normal_data["is_attack"] = False
        normal_data["attack_type"] = "normal"
        normal_data["mitre_technique"] = None
        
        # Generate attack data
        attack_samples = []
        attack_types = list(self.attack_types.keys())
        
        attacks_per_type = num_attacks // len(attack_types)
        
        for attack_type in attack_types:
            for _ in range(attacks_per_type):
                # Generate short attack sequence (5-10 points)
                sequence_length = np.random.randint(5, 11)
                sequence = self.generate_attack_sequence(
                    attack_type,
                    duration_seconds=sequence_length * 2
                )
                attack_samples.extend(sequence)
        
        attack_df = pd.DataFrame(attack_samples)
        
        # Combine and shuffle
        combined = pd.concat([normal_data, attack_df], ignore_index=True)
        combined = combined.sample(frac=1).reset_index(drop=True)
        
        return combined
    
    def get_attack_info(self, attack_type: str) -> Dict:
        """Get information about a specific attack type"""
        return self.attack_types.get(attack_type, {})
    
    def list_attack_types(self) -> List[str]:
        """List all available attack types"""
        return list(self.attack_types.keys())


if __name__ == "__main__":
    # Test the attack simulator
    from data.telemetry_generator import TelemetryGenerator
    
    gen = TelemetryGenerator(num_endpoints=10)
    simulator = AttackSimulator(gen)
    
    print("Available attack types:")
    for attack in simulator.list_attack_types():
        info = simulator.get_attack_info(attack)
        print(f"  - {attack}: {info['name']} ({info['mitre_id']})")
    
    print("\n\nGenerating brute force attack sequence...")
    sequence = simulator.generate_attack_sequence("brute_force", duration_seconds=30)
    print(f"Generated {len(sequence)} attack points")
    print("\nFirst point:")
    print(sequence[0])
    
    print("\n\nGenerating mixed dataset...")
    dataset = simulator.generate_mixed_dataset(num_normal=100, num_attacks=50)
    print(f"Total samples: {len(dataset)}")
    print(f"Normal: {len(dataset[dataset['is_attack'] == False])}")
    print(f"Attacks: {len(dataset[dataset['is_attack'] == True])}")
