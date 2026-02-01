from fastapi import APIRouter, HTTPException, Body, Depends
from typing import List, Optional
from pydantic import BaseModel
from automation.playbooks import playbook_manager, Playbook, PlaybookSession, PlaybookStepStatus
from database import data_store

router = APIRouter(prefix="/api/automation", tags=["automation"])

class StartSessionRequest(BaseModel):
    incident_id: str
    playbook_id: str

class UpdateStepRequest(BaseModel):
    status: PlaybookStepStatus
    notes: Optional[str] = None

@router.get("/playbooks", response_model=List[Playbook])
async def list_playbooks():
    """Get library of all response playbooks"""
    return playbook_manager.get_all_playbooks()

@router.post("/sessions/start", response_model=PlaybookSession)
async def start_session_endpoint(payload: StartSessionRequest):
    try:
        session = playbook_manager.start_session(payload.incident_id, payload.playbook_id)
        return session
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sessions/{session_id}", response_model=PlaybookSession)
async def get_session_endpoint(session_id: str):
    session = playbook_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@router.get("/sessions/incident/{incident_id}", response_model=Optional[PlaybookSession])
async def get_incident_session(incident_id: str):
    return playbook_manager.get_session_by_incident(incident_id)

@router.post("/sessions/{session_id}/steps/{step_id}/update", response_model=PlaybookSession)
async def update_step_status(session_id: str, step_id: str, payload: UpdateStepRequest):
    try:
        session = playbook_manager.update_step(session_id, step_id, payload.status, payload.notes)
        return session
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/sessions/{session_id}/steps/{step_id}/execute")
async def execute_step_automation(session_id: str, step_id: str):
    try:
        result = playbook_manager.execute_automation(session_id, step_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
