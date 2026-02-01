"""
MITRE ATT&CK Techniques Database
"""
from typing import Dict, List


MITRE_TECHNIQUES = {
    "T1110": {
        "id": "T1110",
        "name": "Brute Force",
        "tactic": "Credential Access",
        "description": "Adversaries may use brute force techniques to gain access to accounts when passwords are unknown or when password hashes are obtained.",
        "features": {
            "failed_logins": {"threshold": 3.0, "weight": 0.35},
            "auth_attempts": {"threshold": 3.0, "weight": 0.35},
            "network_in": {"threshold": 1.5, "weight": 0.15},
            "network_out": {"threshold": 1.5, "weight": 0.15}
        },
        "remediation": [
            "Monitor for multiple failed authentication attempts",
            "Implement account lockout policies",
            "Use multi-factor authentication",
            "Monitor for unusual authentication patterns"
        ]
    },
    "T1496": {
        "id": "T1496",
        "name": "Resource Hijacking",
        "tactic": "Impact",
        "description": "Adversaries may leverage the resources of co-opted systems to solve resource intensive problems, which may impact system availability.",
        "features": {
            "cpu_usage": {"threshold": 2.5, "weight": 0.40},
            "network_out": {"threshold": 2.0, "weight": 0.25},
            "process_creation": {"threshold": 2.0, "weight": 0.25},
            "memory_usage": {"threshold": 1.8, "weight": 0.10}
        },
        "remediation": [
            "Monitor for unusual CPU usage patterns",
            "Investigate unauthorized processes",
            "Check for cryptocurrency mining activity",
            "Review outbound network connections"
        ]
    },
    "T1048": {
        "id": "T1048",
        "name": "Exfiltration Over Alternative Protocol",
        "tactic": "Exfiltration",
        "description": "Adversaries may steal data by exfiltrating it over a different protocol than that of the existing command and control channel.",
        "features": {
            "network_out": {"threshold": 3.0, "weight": 0.35},
            "disk_read": {"threshold": 2.5, "weight": 0.25},
            "file_access": {"threshold": 2.5, "weight": 0.25},
            "dns_queries": {"threshold": 2.0, "weight": 0.15}
        },
        "remediation": [
            "Monitor for large outbound data transfers",
            "Inspect unusual DNS traffic",
            "Review file access patterns",
            "Implement data loss prevention (DLP)"
        ]
    },
    "T1068": {
        "id": "T1068",
        "name": "Exploitation for Privilege Escalation",
        "tactic": "Privilege Escalation",
        "description": "Adversaries may exploit software vulnerabilities in an attempt to elevate privileges.",
        "features": {
            "process_creation": {"threshold": 3.0, "weight": 0.35},
            "api_calls": {"threshold": 2.5, "weight": 0.25},
            "memory_usage": {"threshold": 2.0, "weight": 0.20},
            "failed_logins": {"threshold": 2.0, "weight": 0.20}
        },
        "remediation": [
            "Monitor for unusual process creation",
            "Investigate privilege escalation attempts",
            "Apply security patches promptly",
            "Review API call patterns"
        ]
    },
    "T1071": {
        "id": "T1071",
        "name": "Application Layer Protocol",
        "tactic": "Command and Control",
        "description": "Adversaries may communicate using application layer protocols to avoid detection/network filtering.",
        "features": {
            "network_out": {"threshold": 2.0, "weight": 0.25},
            "network_in": {"threshold": 2.0, "weight": 0.25},
            "dns_queries": {"threshold": 3.5, "weight": 0.35},
            "api_calls": {"threshold": 2.0, "weight": 0.15}
        },
        "remediation": [
            "Monitor DNS for suspicious queries",
            "Inspect application layer traffic",
            "Analyze beaconing behavior",
            "Block known C2 domains"
        ]
    },
    "T1021": {
        "id": "T1021",
        "name": "Remote Services",
        "tactic": "Lateral Movement",
        "description": "Adversaries may use valid accounts to log into a service specifically designed to accept remote connections.",
        "features": {
            "network_in": {"threshold": 2.5, "weight": 0.30},
            "auth_attempts": {"threshold": 2.5, "weight": 0.30},
            "process_creation": {"threshold": 2.0, "weight": 0.25},
            "failed_logins": {"threshold": 2.0, "weight": 0.15}
        },
        "remediation": [
            "Monitor for unusual remote access",
            "Review authentication logs",
            "Restrict lateral movement",
            "Segment the network"
        ]
    },
    "T1190": {
        "id": "T1190",
        "name": "Exploit Public-Facing Application",
        "tactic": "Initial Access",
        "description": "Adversaries may attempt to exploit a weakness in an Internet-facing computer or program using software, data, or commands.",
        "features": {
            "cpu_usage": {"threshold": 1.8, "weight": 0.20},
            "memory_usage": {"threshold": 2.0, "weight": 0.20},
            "network_in": {"threshold": 2.5, "weight": 0.25},
            "api_calls": {"threshold": 3.0, "weight": 0.25},
            "process_creation": {"threshold": 1.8, "weight": 0.10}
        },
        "remediation": [
            "Patch public-facing applications",
            "Implement web application firewall",
            "Monitor for exploitation attempts",
            "Review API security"
        ]
    }
}


def get_technique(technique_id: str) -> Dict:
    """Get technique information by ID"""
    return MITRE_TECHNIQUES.get(technique_id, {})


def list_all_techniques() -> List[Dict]:
    """Get all techniques"""
    return list(MITRE_TECHNIQUES.values())


def get_techniques_by_tactic(tactic: str) -> List[Dict]:
    """Get techniques by tactic"""
    return [t for t in MITRE_TECHNIQUES.values() if t["tactic"] == tactic]
