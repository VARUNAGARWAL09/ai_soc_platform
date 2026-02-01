from typing import List, Dict, Optional
from enum import Enum
import time
import uuid
from pydantic import BaseModel

class ActionType(str, Enum):
    MANUAL = 'manual'
    AUTOMATED = 'automated'
    DECISION = 'decision'

class PlaybookStepStatus(str, Enum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    SKIPPED = 'skipped'

class PlaybookStep(BaseModel):
    id: str
    order: int
    title: str
    description: str
    actionType: ActionType
    estimatedMinutes: int
    required: bool
    automationHook: Optional[str] = None

class Playbook(BaseModel):
    id: str
    name: str
    description: str
    incidentType: str
    severity: List[str]
    mitreTechniques: List[str]
    steps: List[PlaybookStep]
    estimatedDuration: int

class PlaybookSession(BaseModel):
    session_id: str
    playbook_id: str
    incident_id: str
    start_time: float
    current_step_index: int = 0
    step_statuses: Dict[str, PlaybookStepStatus] = {}
    step_notes: Dict[str, str] = {}
    completed: bool = False

class PlaybookManager:
    def __init__(self):
        self.playbooks: List[Playbook] = self._load_library()
        self.sessions: Dict[str, PlaybookSession] = {} # session_id -> Session

    def get_all_playbooks(self) -> List[Playbook]:
        return self.playbooks

    def get_recommendations(self, attack_type: str) -> List[Playbook]:
        """Return playbooks relevant to the specific attack with keyword mapping"""
        attack_lower = attack_type.lower()
        recommended = []

        # 1. Direct Match
        for pb in self.playbooks:
            if pb.incidentType.lower() in attack_lower or attack_lower in pb.incidentType.lower():
                recommended.append(pb)
        
        # 2. Keyword Mapping (if no direct match)
        if not recommended:
            keyword_map = {
                "brute_force": ["PB-ATO-11", "PB-UA-03"], 
                "password": ["PB-ATO-11"],
                "scanning": ["PB-UA-03"],
                "discovery": ["PB-UA-03"],
                "mimikatz": ["PB-UA-03", "PB-MAL-05"],
                "credential": ["PB-ATO-11"],
                "c2": ["PB-MAL-05"],
                "command_control": ["PB-MAL-05"],
                "lateral": ["PB-UA-03"],
                "rootkit": ["PB-MAL-05"],
                "trojan": ["PB-MAL-05"],
                "virus": ["PB-MAL-05"],
                "worm": ["PB-MAL-05"],
                "exfiltration": ["PB-DATA-04"],
                "leak": ["PB-DATA-04"],
                "dos": ["PB-DDOS-06"],
                "flood": ["PB-DDOS-06"],
                "insider": ["PB-INSIDE-07"],
                "sql": ["PB-SQLI-08"],
                "injection": ["PB-SQLI-08"],
                "xss": ["PB-SQLI-08"],
                "chain": ["PB-SUPPLY-09"],
                "dependency": ["PB-SUPPLY-09"],
                "crypto": ["PB-CRYPTO-10"],
                "miner": ["PB-CRYPTO-10"],
                "login": ["PB-ATO-11"],
                "privilege": ["PB-ATO-11", "PB-UA-03"],
                "escalation": ["PB-ATO-11"],
                "zero_day": ["PB-MAL-05", "PB-RANSOM-02"],
                "exploit": ["PB-MAL-05"],
                "vulnerability": ["PB-SUPPLY-09"]
            }

            for key, pb_ids in keyword_map.items():
                if key in attack_lower:
                    for pb_id in pb_ids:
                        pb = self.get_playbook(pb_id)
                        if pb and pb not in recommended:
                            recommended.append(pb)
        
        # 3. Fallback
        if not recommended:
           return [self.playbooks[0]]
            
        return recommended

    def get_playbook(self, playbook_id: str) -> Optional[Playbook]:
        return next((p for p in self.playbooks if p.id == playbook_id), None)

    def start_session(self, incident_id: str, playbook_id: str) -> PlaybookSession:
        pb = self.get_playbook(playbook_id)
        if not pb:
            raise ValueError("Playbook not found")
        
        session_id = str(uuid.uuid4())
        # Init statuses
        statuses = {step.id: PlaybookStepStatus.PENDING for step in pb.steps}
        # Mark first as in_progress
        if pb.steps:
            statuses[pb.steps[0].id] = PlaybookStepStatus.IN_PROGRESS

        session = PlaybookSession(
            session_id=session_id,
            playbook_id=playbook_id,
            incident_id=incident_id,
            start_time=time.time(),
            step_statuses=statuses
        )
        self.sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> Optional[PlaybookSession]:
        return self.sessions.get(session_id)
    
    def get_session_by_incident(self, incident_id: str) -> Optional[PlaybookSession]:
        # Return most recent active session
        return next((s for s in reversed(list(self.sessions.values())) if s.incident_id == incident_id and not s.completed), None)

    def update_step(self, session_id: str, step_id: str, status: PlaybookStepStatus, notes: Optional[str] = None) -> PlaybookSession:
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")
        
        session.step_statuses[step_id] = status
        if notes:
            session.step_notes[step_id] = notes

        # Logic to advance step if completed/skipped
        if status in [PlaybookStepStatus.COMPLETED, PlaybookStepStatus.SKIPPED]:
             # Find next step
             pb = self.get_playbook(session.playbook_id)
             if pb:
                 step_ids = [s.id for s in pb.steps]
                 try:
                     curr_idx = step_ids.index(step_id)
                     if curr_idx + 1 < len(step_ids):
                         next_step_id = step_ids[curr_idx + 1]
                         session.current_step_index = curr_idx + 1
                         session.step_statuses[next_step_id] = PlaybookStepStatus.IN_PROGRESS
                     else:
                         session.completed = True
                 except ValueError:
                     pass
        
        return session

    def execute_automation(self, session_id: str, step_id: str):
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError("Session not found")
        pb = self.get_playbook(session.playbook_id)
        step = next((s for s in pb.steps if s.id == step_id), None)
        
        if not step or not step.automationHook:
            return {"status": "failed", "message": "No automation hook"}

        # Simulate Execution
        time.sleep(1) 
        
        # Auto-complete step
        self.update_step(session_id, step_id, PlaybookStepStatus.COMPLETED, notes="Automated execution successful")
        
        return {"status": "success", "action": step.automationHook}

    def _load_library(self) -> List[Playbook]:
        library = []
        
        # Helper to create steps locally
        def mk_step(id, order, title, desc, action, mins, req=True, hook=None):
            return PlaybookStep(id=id, order=order, title=title, description=desc, 
                              actionType=action, estimatedMinutes=mins, required=req, automationHook=hook)

        # 1. Phishing Response
        library.append(Playbook(
            id="PB-PHISH-01", name="Phishing Response", description="Standard response to reported phishing email",
            incidentType="phishing", severity=["Critical", "High", "Medium"], mitreTechniques=["T1566", "T1204", "T1114"], estimatedDuration=30,
            steps=[
                mk_step("s1", 1, "Analyze Headers", "Check SPF/DKIM/DMARC alignment", ActionType.MANUAL, 5),
                mk_step("s2", 2, "Extract IOCs", "Identify URLs, attachments, and sender IPs", ActionType.AUTOMATED, 2, True, "extractIOCs"),
                mk_step("s3", 3, "Threat Intelligence Check", "Query VirusTotal/AlienVault for reputation", ActionType.AUTOMATED, 3, True, "checkReputation"),
                mk_step("s4", 4, "Block Sender", "Add sender verification block on gateway", ActionType.AUTOMATED, 1, True, "blockSender"),
                mk_step("s5", 5, "Purge Inbox", "Remove email from all user inboxes", ActionType.AUTOMATED, 10, True, "purgeEmail"),
                mk_step("s6", 6, "Reset User Creds", "Force password reset if click detected", ActionType.DECISION, 5),
                mk_step("s7", 7, "User Awareness", "Assign training to reported user", ActionType.MANUAL, 5, False)
            ]
        ))

        # 2. Ransomware Response
        library.append(Playbook(
            id="PB-RANSOM-02", name="Ransomware Response", description="Immediate containment of ransomware outbreak",
            incidentType="ransomware", severity=["Critical"], mitreTechniques=["T1486", "T1489", "T1059"], estimatedDuration=45,
            steps=[
                mk_step("s1", 1, "Isolate Endpoint", "Cut network access to infected host", ActionType.AUTOMATED, 1, True, "isolateEndpoint"),
                mk_step("s2", 2, "Snapshot VM", "Take forensic memory/disk snapshot", ActionType.AUTOMATED, 5, True, "snapshotSystem"),
                mk_step("s3", 3, "Identify Variant", "Determine ransomware family based on extension/note", ActionType.MANUAL, 10),
                mk_step("s4", 4, "Disable SMB/RDP", "Close propagation ports laterally", ActionType.AUTOMATED, 3, True, "blockPropagation"),
                mk_step("s5", 5, "Check Backups", "Verify integrity of latest backups", ActionType.MANUAL, 15),
                mk_step("s6", 6, "Kill Process", "Terminate suspicious processes", ActionType.AUTOMATED, 2, True, "killProcess"),
                mk_step("s7", 7, "Reset Credentials", "Force password reset for compromised accounts", ActionType.AUTOMATED, 5, True, "resetCredentials"),
                mk_step("s8", 8, "Legal/PR Notify", "Draft breach notification if data exfiltrated", ActionType.MANUAL, 30)
            ]
        ))
        
        # 3. Unauthorized Access
        library.append(Playbook(
            id="PB-AUTH-03", name="Unauthorized Access", description="Response to suspicious login activity",
            incidentType="unauthorized_access", severity=["Critical", "High", "Medium"], mitreTechniques=["T1078", "T1110"], estimatedDuration=35,
            steps=[
                mk_step("s1", 1, "Verify Activity", "Contact user to confirm login attempt", ActionType.MANUAL, 5),
                mk_step("s2", 2, "Geo-IP Correlation", "Check logic distance vs travel time", ActionType.AUTOMATED, 1, False, "geoCheck"),
                mk_step("s3", 3, "Lock Account", "Disable user account in AD", ActionType.AUTOMATED, 1, True, "disableUser"),
                mk_step("s4", 4, "Revoke Sessions", "Kill active sessions and tokens", ActionType.AUTOMATED, 2, True, "revokeSessions"),
                mk_step("s5", 5, "Device Integrity", "Check MDM status of source device", ActionType.MANUAL, 10),
                mk_step("s6", 6, "Analyze Source", "Analyze source IP reputation and history", ActionType.AUTOMATED, 2, False, "analyzeIP")
            ]
        ))

        # 4. Data Breach
        library.append(Playbook(
            id="PB-DATA-04", name="Data Breach", description="DLP alert response protocol",
            incidentType="data_leak", severity=["Critical", "High"], mitreTechniques=["T1005", "T1041"], estimatedDuration=60,
            steps=[
                mk_step("s1", 1, "Classify Data", "Determine sensitivity of leaked data (PII/PHI)", ActionType.DECISION, 10),
                mk_step("s2", 2, "Content Search", "Scan egress logs for similar patterns", ActionType.AUTOMATED, 15, True, "searchLogs"),
                mk_step("s3", 3, "Block Transfer", "Terminate active file transfers", ActionType.AUTOMATED, 1, True, "blockTransfer"),
                mk_step("s4", 4, "Lock Cloud Access", "Suspend SaaS API tokens", ActionType.AUTOMATED, 2, True, "suspendTokens"),
                mk_step("s5", 5, "Interview User", "Determine intent vs accident", ActionType.MANUAL, 30),
                mk_step("s6", 6, "Legal Notification", "Notify legal/compliance team", ActionType.MANUAL, 30)
            ]
        ))

        # 5. Malware Response
        library.append(Playbook(
            id="PB-MAL-05", name="Malware Response", description="General malware infection cleanup",
            incidentType="malware", severity=["Critical", "High", "Medium"], mitreTechniques=["T1059", "T1547"], estimatedDuration=25,
            steps=[
                mk_step("s1", 1, "Get Sample", "Retrieve file sample for sandbox analysis", ActionType.AUTOMATED, 5, True, "collectSample"),
                mk_step("s2", 2, "Sandbox Analysis", "Run sample in detonation chamber", ActionType.AUTOMATED, 10, True, "detonateSample"),
                mk_step("s3", 3, "Cleanup Artifacts", "Remove files and registry keys", ActionType.MANUAL, 10)
            ]
        ))
        
        # 6. DDoS
        library.append(Playbook(
            id="PB-DDOS-06", name="DDoS Mitigation", description="Response to volumetric attacks",
            incidentType="ddos", severity=["Critical", "High"], mitreTechniques=["T1498", "T1499"], estimatedDuration=15,
            steps=[
                mk_step("s1", 1, "Analyze Traffic", "Identify attack vector and sources", ActionType.AUTOMATED, 5, True, "analyzeTraffic"),
                mk_step("s2", 2, "Activate WAF", "Enable 'Under Attack' mode", ActionType.AUTOMATED, 1, True, "enableUnderAttackMode"),
                mk_step("s3", 3, "Rate Limiting", "Apply aggressive rate limiting rules", ActionType.MANUAL, 5)
            ]
        ))

        # 7. Insider Threat
        library.append(Playbook(
            id="PB-INSIDE-07", name="Insider Threat", description="Investigate anomalous user behavior",
            incidentType="insider_threat", severity=["High", "Medium"], mitreTechniques=["T1078", "T1530"], estimatedDuration=120,
            steps=[
                mk_step("s1", 1, "Snapshot User Activity", "Pull logs for last 30 days", ActionType.AUTOMATED, 10, True, "pullUserLogs"),
                mk_step("s2", 2, "HR Consultation", "Check for recent employment status changes", ActionType.MANUAL, 60),
                mk_step("s3", 3, "Enhanced Monitoring", "Enable full packet capture for user", ActionType.MANUAL, 15)
            ]
        ))

        # 8. SQL Injection
        library.append(Playbook(
            id="PB-SQLI-08", name="SQL Injection", description="Web application attach response",
            incidentType="sqli", severity=["Critical", "High"], mitreTechniques=["T1190", "T1059"], estimatedDuration=20,
            steps=[
                mk_step("s1", 1, "Block IP", "Add attacking IP to firewall blocklist", ActionType.AUTOMATED, 1, True, "blockIP"),
                mk_step("s2", 2, "Check DB Logs", "Look for successful query execution", ActionType.MANUAL, 10),
                mk_step("s3", 3, "Patch Vulnerability", "Coordinate with dev team for hotfix", ActionType.MANUAL, 60)
            ]
        ))

        # 9. Supply Chain Attack
        library.append(Playbook(
            id="PB-SUPPLY-09", name="Supply Chain Attack", description="Compromised vendor software response",
            incidentType="supply_chain", severity=["Critical"], mitreTechniques=["T1195", "T1199"], estimatedDuration=240,
            steps=[
                mk_step("s1", 1, "Identify Scope", "List all systems running affected software", ActionType.AUTOMATED, 15, True, "inventoryScan"),
                mk_step("s2", 2, "Network Segmentation", "Isolate affected VLANs", ActionType.MANUAL, 30),
                mk_step("s3", 3, "Vendor Comm", "Contact vendor for updates/IOCs", ActionType.MANUAL, 15)
            ]
        ))

        # 10. Cryptomining
        library.append(Playbook(
            id="PB-CRYPTO-10", name="Cryptomining", description="Unauthorized resource usage",
            incidentType="crypto_mining", severity=["Medium", "Low"], mitreTechniques=["T1496", "T1059"], estimatedDuration=15,
            steps=[
                mk_step("s1", 1, "Kill Miner", "Terminate CPU high-usage process", ActionType.AUTOMATED, 1, True, "killProcess"),
                mk_step("s2", 2, "Block Pool", "Block outbound traffic to mining pools", ActionType.AUTOMATED, 1, True, "updateFirewall"),
                mk_step("s3", 3, "Persistence Check", "Look for scheduled tasks", ActionType.MANUAL, 10)
            ]
        ))

        # 11. Account Takeover
        library.append(Playbook(
            id="PB-ATO-11", name="Account Takeover", description="Full account compromise recovery",
            incidentType="account_takeover", severity=["Critical", "High"], mitreTechniques=["T1078", "T1110"], estimatedDuration=40,
            steps=[
                mk_step("s1", 1, "Force Logout", "Revoke all active sessions", ActionType.AUTOMATED, 1, True, "revokeSessions"),
                mk_step("s2", 2, "Reset MFA", "Clear existing MFA tokens", ActionType.AUTOMATED, 2, True, "resetMFA"),
                mk_step("s3", 3, "Audit Access", "Review access logs for lateral movement", ActionType.MANUAL, 20)
            ]
        ))

        return library

playbook_manager = PlaybookManager()

