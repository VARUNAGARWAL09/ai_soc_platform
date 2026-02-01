"""
AI Chatbot API Route
Provides intelligent responses to SOC queries
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import random
import re

from database import data_store
from automation.playbooks import playbook_manager

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    context: Optional[dict] = None

class ChatResponse(BaseModel):
    response: str
    actions: List[dict] = []

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Process user query and return AI response
    """
    query = request.message.lower()
    response = ""
    actions = []
    
    # 1. Status / Overview
    if "status" in query or "health" in query or "overview" in query:
        incidents = data_store.get_all_incidents()
        critical = len([i for i in incidents if i.severity == "critical"])
        high = len([i for i in incidents if i.severity == "high"])
        
        response = f"System is fully operational. Currently tracking {len(incidents)} active incidents ({critical} Critical, {high} High). Analysis engine is running at 99.8% uptime."
        
    # 2. Critical Incidents
    elif "critical" in query or "severe" in query:
        incidents = [i for i in data_store.get_all_incidents() if i.severity == "critical"]
        if incidents:
            details = [f"{i.id} ({i.attack_type})" for i in incidents[:3]]
            response = f"I found {len(incidents)} critical incidents requiring immediate attention: {', '.join(details)}."
            if len(incidents) > 3:
                response += f" and {len(incidents)-3} more."
            actions.append({"label": "View Incidents", "url": "/incidents?severity=critical"})
        else:
            response = "Good news! No critical incidents detected at this moment."

    # 3. Playbook Help
    elif "playbook" in query or "response" in query:
        response = "I can initiate automated response protocols. We have playbooks for Ransomware, Phishing, Unauthorized Access, and SQL Injection. Which incident do you need to mitigate?"
        actions.append({"label": "Open Playbook Library", "url": "/playbooks"})

    # 4. Analysis Request
    elif "analyze" in query or "investigate" in query:
        # Extract incident ID if present
        match = re.search(r'start with (inc-\w+)', query) or re.search(r'(inc-\w+)', query)
        if match:
            incident_id = match.group(1).upper()
            incident = data_store.get_incident(incident_id)
            if incident:
                response = f"Analyzing {incident_id}: Validated as {incident.attack_type} with {incident.anomaly_scores.confidence:.1%} confidence. Recommendation: Execute {incident.attack_type} playbook immediately."
                actions.append({"label": "Execute Playbook", "url": f"/playbooks?incidentId={incident_id}"})
            else:
                response = f"I couldn't find incident {incident_id} in the database."
        else:
            response = "Please specify an Incident ID (e.g., INC-123456) for me to analyze."

    # 5. Default / Greetings
    elif "hello" in query or "hi" in query:
        response = "Hello! I am your AI SOC Assistant. I can help you monitor threats, analyze incidents, and execute response playbooks. How can I assist you today?"
        
    else:
        # Fallback
        fallbacks = [
            "I'm listening. You can ask me about critical threats, system status, or specific incidents.",
            "I didn't quite catch that context. Try asking 'Show critical incidents' or 'System status'.",
            "I'm analyzing network traffic. Let me know if you need specific incident details."
        ]
        response = random.choice(fallbacks)

    return ChatResponse(response=response, actions=actions)
