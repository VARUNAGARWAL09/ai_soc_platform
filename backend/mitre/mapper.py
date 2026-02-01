"""
MITRE ATT&CK Technique Mapper
Maps anomalous features to MITRE techniques
"""
import numpy as np
from typing import List, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from mitre.techniques import MITRE_TECHNIQUES, get_technique
from models import MITRETechnique


class MITREMapper:
    """Maps anomalous behavior to MITRE ATT&CK techniques"""
    
    def __init__(self):
        self.techniques = MITRE_TECHNIQUES
        # Get baseline values for normalization
        from data.telemetry_generator import TelemetryGenerator
        gen = TelemetryGenerator()
        self.baselines = gen.get_feature_baselines()
    
    def map_to_techniques(self, features: Dict[str, float], 
                         top_k: int = 3) -> List[MITRETechnique]:
        """
        Map feature values to MITRE techniques
        
        Args:
            features: Dictionary of feature values
            top_k: Number of top techniques to return
            
        Returns:
            List of MITRETechnique objects sorted by confidence
        """
        technique_scores = []
        
        for technique_id, technique_data in self.techniques.items():
            score, matched_features = self._score_technique(features, technique_data)
            
            if score > 0.3:  # Minimum confidence threshold
                technique = MITRETechnique(
                    technique_id=technique_id,
                    name=technique_data["name"],
                    tactic=technique_data["tactic"],
                    confidence=score,
                    matched_features=matched_features,
                    description=technique_data["description"]
                )
                technique_scores.append((score, technique))
        
        # Sort by score descending
        technique_scores.sort(key=lambda x: x[0], reverse=True)
        
        # Return top K
        return [t[1] for t in technique_scores[:top_k]]
    
    def _score_technique(self, features: Dict[str, float], 
                        technique_data: Dict) -> tuple[float, List[str]]:
        """
        Calculate how well features match a technique
        
        Args:
            features: Feature values
            technique_data: Technique definition
            
        Returns:
            Tuple of (score, matched_features)
        """
        feature_map = technique_data["features"]
        total_weight = 0.0
        weighted_score = 0.0
        matched_features = []
        
        for feature_name, params in feature_map.items():
            if feature_name not in features:
                continue
            
            # Get baseline and actual value
            baseline = self.baselines[feature_name]["mean"]
            actual = features[feature_name]
            
            # Calculate deviation multiplier
            deviation_multiplier = actual / (baseline + 0.001)  # Avoid division by zero
            
            # Check if feature is elevated
            threshold = params["threshold"]
            weight = params["weight"]
            
            if deviation_multiplier >= threshold:
                # Feature matches this technique
                # Score based on how much it exceeds threshold
                feature_score = min((deviation_multiplier - threshold) / threshold, 1.0)
                weighted_score += feature_score * weight
                total_weight += weight
                matched_features.append(feature_name)
        
        # Normalize score
        if total_weight > 0:
            final_score = weighted_score / total_weight
            # Add bonus for multiple matched features
            match_bonus = min(len(matched_features) * 0.05, 0.2)
            final_score = min(final_score + match_bonus, 0.95)
        else:
            final_score = 0.0
        
        return final_score, matched_features
    
    def get_remediation(self, technique_id: str) -> List[str]:
        """Get remediation steps for a technique"""
        technique = get_technique(technique_id)
        return technique.get("remediation", [])


if __name__ == "__main__":
    # Test mapper
    mapper = MITREMapper()
    
    # Test with crypto mining patterns
    test_features = {
        "cpu_usage": 85.0,
        "memory_usage": 60.0,
        "network_in": 180.0,
        "network_out": 250.0,
        "failed_logins": 0.5,
        "process_creation": 15.0,
        "disk_read": 220.0,
        "disk_write": 110.0,
        "file_access": 55.0,
        "api_calls": 105.0,
        "dns_queries": 35.0,
        "auth_attempts": 2.0
    }
    
    print("Testing MITRE mapper with crypto mining pattern...")
    techniques = mapper.map_to_techniques(test_features, top_k=3)
    
    print(f"\nFound {len(techniques)} matching techniques:\n")
    for tech in techniques:
        print(f"{tech.technique_id} - {tech.name}")
        print(f"  Tactic: {tech.tactic}")
        print(f"  Confidence: {tech.confidence:.2%}")
        print(f"  Matched features: {', '.join(tech.matched_features)}")
        print()
