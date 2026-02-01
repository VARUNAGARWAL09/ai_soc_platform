"""
Incidents API Routes
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from typing import List
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models import Incident
from database import data_store
from reports.generator import PDFReportGenerator
from automation.playbooks import playbook_manager

router = APIRouter(prefix="/api/incidents", tags=["incidents"])





@router.get("/", response_model=List[Incident])
async def list_incidents(
    limit: int = 100,
    severity: str = None,
    status: str = None
):
    """List all incidents with optional filters"""
    
    incidents = data_store.get_all_incidents()
    
    # Apply filters
    if severity:
        incidents = [i for i in incidents if i.severity == severity]
    
    if status:
        incidents = [i for i in incidents if i.status == status]
    
    # Sort by timestamp descending
    incidents.sort(key=lambda x: x.timestamp, reverse=True)
    
    # Limit results
    return incidents[:limit]


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str):
    """Get specific incident details"""
    
    incident = data_store.get_incident(incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident


@router.get("/{incident_id}/timeline")
async def get_incident_timeline(incident_id: str):
    """Get forensic timeline for incident"""
    
    incident = data_store.get_incident(incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Create timeline events
    timeline = [
        {
            "timestamp": incident.timestamp.isoformat(),
            "event": "Anomaly Detected",
            "description": f"Unusual activity detected with {incident.anomaly_scores.confidence:.1%} confidence",
            "severity": incident.severity
        },
        {
            "timestamp": incident.timestamp.isoformat(),
            "event": "ML Analysis",
            "description": f"Ensemble score: {incident.anomaly_scores.ensemble_score:.3f}",
            "severity": "info"
        }
    ]
    
    # Add MITRE technique events
    for tech in incident.mitre_techniques:
        timeline.append({
            "timestamp": incident.timestamp.isoformat(),
            "event": f"MITRE {tech.technique_id}",
            "description": f"{tech.name} detected with {tech.confidence:.1%} confidence",
            "severity": "warning"
        })
    
    return {"incident_id": incident_id, "timeline": timeline}


@router.post("/{incident_id}/report")
async def generate_report(incident_id: str):
    """Generate PDF report for incident"""
    
    incident = data_store.get_incident(incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Generate PDF
    generator = PDFReportGenerator()
    pdf_path = generator.generate_report(incident)
    
    return {
        "incident_id": incident_id,
        "report_path": pdf_path,
        "download_url": f"/api/incidents/{incident_id}/report/download"
    }


@router.get("/{incident_id}/report/download")
async def download_report(incident_id: str):
    """Download PDF report"""
    
    incident = data_store.get_incident(incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    # Generate report
    generator = PDFReportGenerator()
    pdf_path = generator.generate_report(incident)
    
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="Report not found")
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"incident_{incident_id}.pdf"
    )


@router.put("/{incident_id}/status")
async def update_status(incident_id: str, status: str):
    """Update incident status"""
    
    incident = data_store.get_incident(incident_id)
    
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    valid_statuses = ["open", "investigating", "resolved", "false_positive"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    incident.status = status
    data_store.add_incident(incident)
    
    return {"incident_id": incident_id, "status": status}


@router.get("/{incident_id}/playbooks")
async def get_incident_playbooks(incident_id: str):
    """Get recommended playbooks for incident"""
    incident = data_store.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    # Combine context for better matching
    context = f"{incident.attack_type} {incident.explanation or ''}"
    if incident.mitre_techniques:
        context += " " + " ".join([t.name for t in incident.mitre_techniques])
        
    playbooks = playbook_manager.get_recommendations(context)
    return playbooks


@router.post("/{incident_id}/playbooks/{playbook_id}/execute")
async def execute_incident_playbook(incident_id: str, playbook_id: str):
    """Execute a response playbook"""
    incident = data_store.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    try:
        result = await playbook_manager.execute_playbook(playbook_id, incident_id)
        
        # Auto-update status if successful
        if result["status"] == "success":
            incident.status = "resolved"
            data_store.add_incident(incident)
            
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



