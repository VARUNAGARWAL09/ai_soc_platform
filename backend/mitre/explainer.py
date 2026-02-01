"""
Explainable AI Engine
Provides human-readable explanations for anomaly detections
"""
import numpy as np
from typing import List, Dict
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from models import FeatureContribution


class ExplainableAI:
    """Generates explanations for anomaly detections"""
    
    def __init__(self):
        # Get baseline values
        from data.telemetry_generator import TelemetryGenerator
        gen = TelemetryGenerator()
        self.baselines = gen.get_feature_baselines()
    
    def explain_anomaly(self, features: Dict[str, float], 
                       top_k: int = 5) -> tuple[List[FeatureContribution], str]:
        """
        Generate explanation for an anomaly
        
        Args:
            features: Feature values
            top_k: Number of top contributing features to return
            
        Returns:
            Tuple of (feature_contributions, natural_language_explanation)
        """
        contributions = []
        
        for feature_name in settings.FEATURES:
            if feature_name not in features:
                continue
            
            value = features[feature_name]
            baseline = self.baselines[feature_name]["mean"]
            
            # Calculate deviation
            deviation = value - baseline
            deviation_multiplier = value / (baseline + 0.001)
            
            # Calculate contribution percentage based on how unusual the deviation is
            # More unusual = higher contribution
            contribution_score = max(0, np.abs(np.log(deviation_multiplier + 0.1)))
            
            contrib = FeatureContribution(
                feature=feature_name,
                value=value,
                baseline_mean=baseline,
                deviation=deviation,
                deviation_multiplier=deviation_multiplier,
                contribution_percent=0.0  # Will calculate later
            )
            
            contributions.append((contribution_score, contrib))
        
        # Sort by contribution score
        contributions.sort(key=lambda x: x[0], reverse=True)
        
        # Calculate percentages
        total_score = sum([c[0] for c in contributions])
        if total_score > 0:
            for score, contrib in contributions:
                contrib.contribution_percent = (score / total_score) * 100
        
        # Get top K
        top_contributions = [c[1] for c in contributions[:top_k]]
        
        # Generate natural language explanation
        explanation = self._generate_explanation(top_contributions, features)
        
        return top_contributions, explanation
    
    def _generate_explanation(self, contributions: List[FeatureContribution], 
                            features: Dict[str, float]) -> str:
        """Generate human-readable explanation"""
        if not contributions:
            return "No significant deviations detected."
        
        explanation_parts = ["Anomalous behavior detected:"]
        
        for i, contrib in enumerate(contributions[:3]):  # Top 3 features
            feature_name = contrib.feature.replace("_", " ").title()
            
            if contrib.deviation_multiplier > 1.5:
                severity = "significantly elevated"
            elif contrib.deviation_multiplier > 1.2:
                severity = "moderately elevated"
            elif contrib.deviation_multiplier > 1.0:
                severity = "slightly elevated"
            elif contrib.deviation_multiplier < 0.6:
                severity = "significantly reduced"
            elif contrib.deviation_multiplier < 0.8:
                severity = "moderately reduced"
            else:
                severity = "slightly reduced"
            
            part = (
                f"• {feature_name} is {severity} "
                f"({contrib.deviation_multiplier:.1f}x baseline, "
                f"{contrib.contribution_percent:.1f}% contribution)"
            )
            explanation_parts.append(part)
        
        # Add context-specific insights
        context = self._add_context(contributions, features)
        if context:
            explanation_parts.append(f"\n{context}")
        
        return "\n".join(explanation_parts)
    
    def _add_context(self, contributions: List[FeatureContribution], 
                    features: Dict[str, float]) -> str:
        """Add contextual insights based on feature patterns"""
        context_parts = []
        
        # Check for specific attack patterns
        cpu_high = any(c.feature == "cpu_usage" and c.deviation_multiplier > 2.5 for c in contributions)
        network_out_high = any(c.feature == "network_out" and c.deviation_multiplier > 2.5 for c in contributions)
        failed_logins_high = any(c.feature == "failed_logins" and c.deviation_multiplier > 2.0 for c in contributions)
        
        if cpu_high and network_out_high:
            context_parts.append("⚠️ Pattern consistent with cryptocurrency mining or resource hijacking")
        
        if failed_logins_high:
            context_parts.append("⚠️ Possible brute force attack or credential stuffing attempt")
        
        if network_out_high and not cpu_high:
            disk_read = features.get("disk_read", 0)
            baseline_disk = self.baselines["disk_read"]["mean"]
            if disk_read > baseline_disk * 2:
                context_parts.append("⚠️ Large data transfer detected - possible data exfiltration")
        
        return " ".join(context_parts)


if __name__ == "__main__":
    # Test explainer
    explainer = ExplainableAI()
    
    # Test with brute force pattern
    test_features = {
        "cpu_usage": 30.0,
        "memory_usage": 50.0,
        "network_in": 200.0,
        "network_out": 100.0,
        "failed_logins": 12.0,
        "process_creation": 6.0,
        "disk_read": 210.0,
        "disk_write": 105.0,
        "file_access": 52.0,
        "api_calls": 110.0,
        "dns_queries": 32.0,
        "auth_attempts": 15.0
    }
    
    print("Testing Explainable AI with brute force pattern...")
    contributions, explanation = explainer.explain_anomaly(test_features, top_k=5)
    
    print("\nTop Contributing Features:")
    for contrib in contributions:
        print(f"  {contrib.feature}: {contrib.value:.1f} "
              f"(baseline: {contrib.baseline_mean:.1f}, "
              f"deviation: {contrib.deviation_multiplier:.2f}x, "
              f"contribution: {contrib.contribution_percent:.1f}%)")
    
    print(f"\nExplanation:\n{explanation}")
