"""
In-memory storage for incidents and endpoint data
"""
from typing import Dict, List
from datetime import datetime
from models import Incident, EndpointMetadata
import threading


class DataStore:
    """Thread-safe in-memory data storage"""
    
    def __init__(self):
        self.incidents: Dict[str, Incident] = {}
        self.endpoints: Dict[str, EndpointMetadata] = {}
        self._lock = threading.Lock()
        self.incident_counter = 0
    
    def add_incident(self, incident: Incident):
        """Add incident to storage"""
        with self._lock:
            self.incidents[incident.id] = incident
    
    def get_incident(self, incident_id: str) -> Incident:
        """Get incident by ID"""
        return self.incidents.get(incident_id)
    
    def get_all_incidents(self) -> List[Incident]:
        """Get all incidents"""
        return list(self.incidents.values())
    
    def update_endpoint(self, endpoint: EndpointMetadata):
        """Update endpoint metadata"""
        with self._lock:
            self.endpoints[endpoint.id] = endpoint
    
    def get_endpoint(self, endpoint_id: str) -> EndpointMetadata:
        """Get endpoint status"""
        return self.endpoints.get(endpoint_id)
    
    def get_all_endpoints(self) -> List[EndpointMetadata]:
        """Get all endpoints"""
        return list(self.endpoints.values())
    
    def get_next_incident_id(self) -> str:
        """Generate next incident ID"""
        import uuid
        with self._lock:
            return f"INC-{uuid.uuid4().hex[:6].upper()}"


# Global data store instance
data_store = DataStore()
