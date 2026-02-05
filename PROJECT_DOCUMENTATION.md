# AI SOC Platform - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technical Architecture](#technical-architecture)
3. [Frontend Pages & Features](#frontend-pages--features)
4. [Backend API Documentation](#backend-api-documentation)
5. [Machine Learning Models](#machine-learning-models)
6. [Data Flow & System Integration](#data-flow--system-integration)

---

## Project Overview

**Project Name:** AI-Powered Cybersecurity Threat Detection Platform  
**Type:** Production-grade Security Operations Center (SOC) Dashboard  
**Tech Stack:** Next.js 14 (Frontend) + FastAPI (Backend) + TensorFlow/scikit-learn (ML)

### Core Purpose
Real-time threat detection and incident response platform using AI/ML models to analyze endpoint telemetry, detect anomalies, map threats to MITRE ATT&CK framework, and provide automated response playbooks.

### Key Capabilities
- **Multi-Model ML Detection**: Ensemble of 4 ML algorithms
- **Real-Time Monitoring**: 75 simulated endpoints
- **MITRE ATT&CK Mapping**: 7 attack techniques supported
- **Explainable AI**: Natural language explanations
- **Live Streaming**: WebSocket-based telemetry
- **Automated Response**: Guided playbook execution
- **Professional Reporting**: PDF generation with charts

---

## Technical Architecture

### Frontend Structure
```
frontend/
├── app/
│   ├── page.tsx              # Dashboard (Main landing page)
│   ├── layout.tsx             # Root layout with navigation
│   ├── globals.css            # Global styles & animations
│   ├── loading.tsx            # Loading state component
│   ├── incidents/page.tsx     # Incidents management page
│   ├── logs/page.tsx          # Live telemetry streaming page
│   ├── threats/page.tsx       # Endpoint analyzer page
│   ├── playbooks/page.tsx     # Automated response page
│   ├── forensics/page.tsx     # Digital forensics page
│   ├── about/page.tsx         # Team information page
│   └── documentation/page.tsx # System documentation page
├── components/
│   ├── AIChatbot.tsx          # AI assistant component
│   ├── ThemeProvider.tsx      # Dark/light theme manager
│   ├── ThemeToggle.tsx        # Theme switcher button
│   ├── PDFDownloadButton.tsx  # PDF export functionality
│   └── ElevenLabsWidget.tsx   # Voice assistant integration
└── lib/
    └── api.ts                 # API client & axios setup
```

### Backend Structure
```
backend/
├── main.py                   # FastAPI application entry
├── config.py                  # Configuration settings
├── database.py                # In-memory data store
├── models.py                  # Data models (Pydantic)
├── api/
│   ├── routes/
│   │   ├── dashboard.py       # Dashboard metrics API
│   │   ├── incidents.py       # Incident management API
│   │   ├── logs.py            # Log streaming API
│   │   ├── threats.py         # Threat analysis API
│   │   ├── automation.py      # Playbook execution API
│   │   └── chatbot.py         # AI chatbot API
│   └── websocket.py           # WebSocket manager
├── data/
│   ├── telemetry_generator.py # Synthetic data generator
│   └── attack_simulator.py    # Attack scenario simulator
├── ml/
│   ├── models/               # ML model implementations
│   ├── detector.py           # Ensemble detector
│   ├── trainer.py            # Model training
│   └── evaluator.py          # Performance evaluation
├── mitre/
│   ├── techniques.py         # MITRE ATT&CK database
│   ├── mapper.py             # Technique mapper
│   └── explainer.py          # AI explainability
└── reports/                  # PDF report generation
```

---

## Frontend Pages & Features

### 1. Dashboard Page (`/`)

**Purpose:** Main SOC command center with real-time metrics and visualizations

#### Header Section
- **Title:** "SOC OVERWATCH" with gradient effect
- **Live Status Indicator:** 
  - Green pulsing dot when system operational
  - Real-time endpoint count display
  - UTC timestamp (updates every second)

#### Live Ticker
- **Scrolling Banner:** Displays critical alerts and system status
  - Ransomware detections
  - System load percentage
  - Defense matrix status
  - Threat intel update time
  - Unusual traffic patterns
- **Animation:** Infinite horizontal scroll (20s duration)

#### Main Grid Layout (3-Column)

**Left Column: AI Sentinel Core**
- **Visual:** Rotating circular border with central icon
- **Status Indicators:**
  - Icon changes: ⚠️ (under attack) or 👁️ (normal)
  - Color coding: Red (threat) or Cyan (secure)
  - Border animation: Rotating dashed circle (20s)
- **Metrics Display:**
  - "INFERENCE ENGINE" status
  - Shows "ONLINE" in green

**Center Column: Live Network Topology**
- **Visualization:** Scatter chart showing all endpoints
- **Chart Features:**
  - Scatter plot of 20 random nodes
  - Color coding: Red dots (danger) | Blue dots (normal)
  - Regenerates every 10 seconds
  - Interactive tooltips showing endpoint ID and traffic (MB/s)
- **Header:** "LIVE NETWORK TOPOLOGY" with "Scanning..." badge

**Right Column: Recent Alerts**
- **Header:** "⚠️ RECENT ALERTS" with LIVE badge
- **Alert Cards:** Real-time incident feed (top 4 incidents)
  - Endpoint ID (blue monospace font)
  - Severity badge (CRITICAL/HIGH with color coding)
  - Attack type or MITRE technique name
  - Auto-updates every 3 seconds
- **Empty State:** "No active threats" message

#### Metrics Strip (4 Cards)
- **Endpoints Monitored:** Total count with 🖥️ icon
- **Active Threats:** Count with ☣️ icon (pulses if > 0)
- **Total Incidents:** Historical count with 🛡️ icon
- **Detection Accuracy:** Percentage with 🎯 icon
- **Hover Effects:** Cards lift up on hover, icon scales

#### System Health Bar
- **Visual:** Skewed progress bar showing endpoint status
- **Color Segments:**
  - Green: Healthy endpoints
  - Red: Compromised endpoints (animated pulse)
- **Stats:** Displays counts below bar

#### Data Updates
- Fetches dashboard stats every 3 seconds
- All metrics update in real-time
- Loading state with animated spinner

---

### 2. Incidents Page (`/incidents`)

**Purpose:** View, filter, and manage all security incidents

#### Header
- **Title:** "INCIDENT FEED" with gradient (red to purple)
- **Live Indicator:** Pulsing red dot animation

#### Filter Tabs
- **Filters Available:**
  - All Events
  - Critical (red indicator)
  - High (orange indicator)
  - Medium (yellow indicator)
  - Low (green indicator)
- **Animation:** Smooth sliding pill follows selection (spring animation, 300ms)
- **Button Style:** Pills with background transitions

#### Incident Cards Grid
- **Auto-refresh:** Updates every 8 seconds
- **Card Information per Incident:**
  - **Incident ID:** Monospace font, prominent
  - **Endpoint ID/Hostname:** With "HOST" label
  - **Severity Badge:** Color-coded pill (CRITICAL/HIGH/MEDIUM/LOW)
  - **Status:** Open/Closed indicator
  - **Explanation:** AI-generated description
  - **MITRE Techniques:** Red chips showing mapped techniques
  - **Timestamp:** Relative time display
  - **Confidence Score:** Percentage in blue
  - **Attack History:** Shows previous incidents on same endpoint (max 3)

- **Buttons on Each Card:**
  1. **"Investigate" Button:** 
     - Gray background with hover effect
     - Links to `/forensics?id={incident.id}`
  2. **"Report" Button:**
     - Blue cyber theme with shadow
     - Downloads PDF report from backend

#### Loading/Empty States
- **Loading:** Centered spinning loader (12x12px)
- **No Results:** Shield emoji with "Secure Perimeter" message

#### Animations
- **Card Entry:** Stagger fade-in (20ms delay per card)
- **Initial Animation:** Cards slide up from y:5px, opacity 0→1
- **Duration:** 200ms per card

---

### 3. Live Logs Page (`/logs`)

**Purpose:** Real-time terminal-style streaming of endpoint telemetry

#### Header
- **Title:** "> LIVE_TELEMETRY_STREAM" (green to blue gradient)
- **Connection Status:**
  - [CONNECTED] in green when WebSocket active
  - [OFFLINE] in red when disconnected
  - Connection details: "PORT 8000 :: SECURE CHANNEL"

#### Control Buttons
1. **Auto-Scroll Toggle:**
   - Active: Blue background "AUTO_SCROLL: ON"
   - Inactive: Gray background "AUTO_SCROLL: OFF"
   - Toggles automatic scrolling to bottom

2. **Clear Buffer Button:**
   - Red themed "CLEAR_BUFFER"
   - Clears all logs from display

#### Terminal Window
- **Design:** Mimics macOS terminal
- **Window Controls:** Red/Yellow/Green dots (decorative)
- **Title Bar:** `user@soc-console:~/streams/endpoint_logs`
- **CRT Effect:** Scanline overlay for retro look
- **Background:** Black (#05070a) with grid pattern

#### Log Display
- **Format per Line:**
  - Timestamp: HH:mm:ss.milliseconds (gray, 80px width)
  - Severity Badge: 4-letter code (CRIT/ERR/WARN/INFO)
    - CRITICAL: Red background
    - ERROR: Orange background
    - WARNING: Yellow background
    - INFO: Blue text
  - Endpoint ID: Purple monospace (80px width)
  - Message: Gray text with details
  - Hover Effect: Shows additional data fields

- **Buffer:** Keeps last 200 logs maximum
- **Auto-scroll:** Scrolls to bottom on new logs (if enabled)

#### Footer Stats (2 panels)
- **Buffer Size:** Current/200 logs
- **Last Packet:** Timestamp of most recent log

#### WebSocket Connection
- **URL:** `ws://localhost:8000/api/logs/stream`
- **Reconnection:** Auto-reconnects after 3s on disconnect
- **Real-time streaming:** Logs appear instantly

---

### 4. Threat Analyzer Page (`/threats`)

**Purpose:** Deep analysis of individual endpoints using ML models

#### Header
- **Title:** "THREAT ANALYZER" (blue highlight)
- **Subtitle:** Instructions to select endpoint

#### Endpoint Grid Selector
- **Layout:** Responsive grid (2-6 columns based on screen size)
- **Endpoint Cards:**
  - **Icon:** 🖥️ computer emoji
  - **Hostname:** Bold text
  - **Endpoint ID:** Small monospace below
  - **Status Dot:** 
    - Red pulsing: Compromised
    - Green: Healthy
  - **Selected State:** Blue border + ring effect
  - **Hover Effects:** Scale 1.05, blue glow overlay
  - **Click Action:** Triggers analysis

#### Analysis Loading State
- **Spinner:** 16x16px rotating border
- **Message:** "RUNNING HEURISTIC ANALYSIS..."
- **Animation:** Pulsing text

#### Analysis Results Panel

**Header Box:**
- **Title:** "Analysis Report: {endpoint_id}"
- **Confidence Score:** Percentage in blue monospace
- **Status Badge:** Large pill with verdict
  - CRITICAL (≥0.80): Red background
  - SUSPICIOUS (0.35-0.79): Orange background
  - CLEAN (<0.35): Green background
- **Border Color:** Matches severity (left border 4px)

**Model Scores Grid (5 Cards):**
1. Autoencoder score
2. Isolation Forest score
3. LOF score
4. LSTM score (if available)
5. Ensemble score (highlighted)

**Score Card Details:**
- Score value (3 decimals)
- Progress bar visualization
- Color coding: Red (>0.7) | Yellow (0.4-0.7) | Green (<0.4)

**Feature Impact Section:**
- **Title:** "📊 Feature Impact"
- **Top 5 Features Listed:**
  - Feature name (uppercase, gray)
  - Actual value (2 decimals)
  - Contribution percentage (blue progress bar)
  - Animated bar fills on load

**MITRE ATT&CK Mapping:**
- **Title:** "🎯 MITRE ATT&CK Mapping"
- **Technique Cards:**
  - Technique ID (red monospace, e.g., T1110)
  - Technique name (bold)
  - Tactic category
  - Confidence match percentage
  - Red-themed boxes

**AI Analysis Box:**
- **Title:** "🤖 AI Analysis"
- **Blue themed panel**
- **Content:** Natural language explanation of findings

---

### 5. Playbooks Page (`/playbooks`)

**Purpose:** Automated incident response workflow execution

#### View Modes
**Mode 1: Library View**

**Header:**
- **Title:** "PLAYBOOK LIBRARY" (blue to purple gradient)
- **Subtitle:** "SELECT A PROTOCOL TO INITIALIZE RESPONSE SEQUENCE"

**Playbook Grid (3 columns):**
Each playbook card shows:
- **Playbook ID:** Small monospace chip
- **Icon:** Based on severity (☠️ critical or 🛡️ normal)
- **Name:** Large bold title
- **Description:** 2-line clamped summary
- **MITRE Techniques:** First 3 techniques as chips
- **Footer Stats:**
  - Number of steps
  - Estimated duration in minutes
- **Hover Effect:** Border glows blue, title changes color

**Click Action:** Opens initialization modal

**Start Modal:**
- **Playbook Name** at top
- **Dropdown:** Select target incident
  - Lists all open incidents
  - Shows: ID, attack type, severity
- **"Initialize Protocol" Button:**
  - Disabled until incident selected
  - Creates new playbook session
  - Redirects to Mission Control view

---

**Mode 2: Mission Control View (Active Session)**

**Left Sidebar (Timeline):**
- **Header:**
  - Back button "← LIBRARY"
  - "LIVE SESSION" badge (green, pulsing)
  - Playbook name
- **Target Incident Card:**
  - Attack type (uppercase)
  - Hostname/Endpoint ID
  - Incident ID
  - Red-themed styling
- **Progress Bar:** Shows completion percentage
- **Step List:** Scrollable timeline
  - Each step shows:
    - Step number badge
    - Title
    - Action type icon (⚡ AUTO | ⚠️ DECISION | 👤 MANUAL)
    - Duration estimate
    - Completion checkmark (if done)
  - Active step: Blue glow + border
  - Completed steps: Green badge

**Main Panel (Active Step Interface):**
- **Current Objective Badge** at top
- **Step Title:** Large (4xl font)
- **Description Panel:**
  - Gray background box
  - Protocol description text
  - Large readable font

**Automation Hook Display (If Automated):**
- Terminal-style code block
- Shows automation script details:
  - Hook name
  - Status indicator
  - Execution logs (when running)
- Green pulse indicator when ready

**Action Buttons:**
1. **For Automated Steps:**
   - **"EXECUTE AUTOMATION" Button:**
     - Blue cyber theme
     - Spinner when executing
     - Runs backend automation
     - Updates to next step automatically

2. **For Manual/Decision Steps:**
   - **"MARK COMPLETE" Button:**
     - Green theme
     - Marks step done, advances to next

3. **"SKIP" Button** (always available):
   - Gray border style
   - Skips current step

**Completion Screen:**
- 🎉 emoji (large)
- "Protocol Completed" heading
- Success message
- "RETURN TO LIBRARY" button

---

### 6. Forensics Page (`/forensics`)

**Purpose:** Deep-dive analysis and case management for incidents

#### Header
- **Title:** "DIGITAL FORENSICS" (blue to purple gradient)
- **Action Buttons:**
  1. **"Export Case Data":** Downloads JSON of incident
  2. **"Generate Report":** Downloads PDF report

#### Layout (2-Column Grid)

**Left Sidebar: Case Directory**
- **Header:** "CASE DIRECTORY" with file count
- **Incident List:** Scrollable
  - Each case card shows:
    - Incident ID (monospace)
    - Timestamp
    - Attack type name (bold)
    - Severity dot (red/yellow)
    - Endpoint ID
  - Selected card: Blue background + border
  - Click to load case details

**Main Panel: Analysis View**

**Top Stats (4 Cards):**
1. **Severity:** Uppercase, red theme
2. **Confidence:** Percentage, blue theme
3. **Data Exfil:** Network out in KB, purple theme
4. **Processes:** Process count, green theme

**Attack Timeline Chart:**
- **Title:** "ATTACK TIMELINE RECONSTRUCTION"
- **Chart Type:** Multi-line chart (Recharts)
- **Lines:**
  - CPU usage (cyan, left Y-axis)
  - RAM usage (green, left Y-axis)
  - Network out (purple, right Y-axis)
- **X-Axis:** Time markers (20 data points, -20m to 0m)
- **Features:**
  - Spike visualization around attack time (last 3-4 points)
  - Grid lines
  - Interactive tooltips
- **Height:** 64 (256px)

**AI Root Cause Analysis:**
- **Title:** "AI ROOT CAUSE ANALYSIS" (pink)
- **Content Box:**
  - White/dark background
  - Monospace font
  - Pink left border
  - Shows AI explanation text
- **MITRE Mapping:**
  - Technique chips below
  - Hover effect on chips
  - Shows technique ID + name

**Automated Response Playbooks Section:**
- **Title:** "🛡️ AUTOMATED RESPONSE PLAYBOOKS" (purple)
- **Grid:** 2 columns of playbook cards
  - Each playbook shows:
    - Name (large, bold)
    - CRITICAL badge (if applicable)
    - Duration estimate
    - Target incident type
    - Status: READY | RUNNING | MITIGATED
    - **"▶ EXECUTE PLAYBOOK" Button:**
      - Purple theme with shadow
      - Disabled when running/complete
      - Starts playbook session
      - Redirects to `/playbooks?incidentId={id}`

---

### 7. About Page (`/about`)

**Purpose:** Team member showcase

#### Header
- **Title:** "CREATORS" (8xl font, gradient)
- **Subtitle Banner:**
  - Pulsing blue dots on sides
  - "RVCE BENGALURU // CYBER SECURITY DIVISION"

#### Team Grid (3 Columns)
**Each Team Card:**
- **Design:** Glassmorphic card with grid background
- **ID Badge Style** with classification header
- **Top Bar:** "CLASSIFIED" | Member code (e.g., "SEC-01")

**Avatar:**
- Hexagon-clipped container
- Member initials (2 letters, large)
- Animated spinning ring on hover
- Blue glow effect on hover

**Member Info:**
- Name (large, bold)
- Role (purple, uppercase, small)
- Skill stats (3 bars):
  - OFFENSE (red bar)
  - DEFENSE (cyan bar)  
  - INTEL (purple bar)
  - Each shows percentage value
  - Animated fill on scroll into view
- Expertise chip at bottom

**Hover Effects:**
- Border glows blue
- Corner decorations appear
- Inner glow increases

**Team Members:**
1. **Varun Agarwal** - Security Engineer (Network Forensics)
2. **Yuvraj Kumar** - Threat Analyst (Malware Analysis)
3. **Ronit Ranjan** - System Architect (Cloud Security)

#### Footer
- "RVCE 2026 | CSE // SEM 7 | VER 1.0.4"

---

### 8. Documentation Page (`/documentation`)

**Purpose:** Technical system documentation with PDF export

#### Header
- **Title:** "System Documentation" (gradient)
- **PDF Download Button:**
  - Dynamic import (client-side only)
  - Generates PDF of entire documentation
  - Loading state while PDF library loads

#### Content Sections

**1. System Overview:**
- Description of AI SOC Platform
- Key differentiators from traditional systems
- Ensemble ML approach

**2. Monitoring Parameters:**
- **System Resources:** CPU, Memory, Disk read/write
- **Network Activity:** Traffic in/out, DNS, API calls
- **Security Events:** Failed logins, auth attempts, process creation, file access
- Displayed in 3-column grid with color-coded panels

**3. Detection Logic & Architecture:**
- **4 ML Models:**
  1. Deep Autoencoder (blue border)
  2. Isolation Forest (purple border)
  3. Local Outlier Factor (emerald border)
  4. LSTM (amber border)
- Each with description

**4. Incident Severity Classification:**
- **Table Format:**
  - Severity level badges
  - Ensemble score ranges
  - Descriptions
- **Levels:**
  - CRITICAL (≥0.80): Red badge
  - HIGH (0.70-0.79): Orange badge
  - MEDIUM (0.55-0.69): Yellow badge
  - LOW/INFO (<0.55): Blue badge

**5. MITRE ATT&CK Support:**
- **7 Supported Techniques:**
  - T1110: Brute Force
  - T1496: Resource Hijacking (Crypto Mining)
  - T1048: Data Exfiltration
  - T1068: Privilege Escalation
  - T1071: Command & Control
  - T1021: Lateral Movement
  - T1190: Exploit Public-Facing Application
- 2-column grid layout

**Print Styling:**
- Separate print-only header
- Removes interactive elements
- Black text on white background
- Page break controls

---

## Global Navigation & Layout

### Navigation Bar
**Location:** Top of all pages (sticky)

**Logo/Brand:**
- ⚡ emoji in gradient box
- "AI SOC Platform" text (gradient)
- Clickable, links to dashboard

**Navigation Links:**
- Dashboard (/
)
- Live Logs (/logs)
- Threat Analyzer (/threats)
- Incidents (/incidents)
- Playbooks (/playbooks)
- Forensics (/forensics)
- About Team (/about)
- Documentation (/documentation)

**Features:**
- **Link Prefetch:** All links pre-load on hover
- **Transition Duration:** 150ms (optimized)
- **Active State:** Text color changes
- **Hover Effect:** Color changes to cyber-blue

**Theme Toggle:**
- Border separator before toggle
- Sun/Moon icon button
- Switches between light/dark mode
- Persists in localStorage

### Global Styles
**Glass Panel Effect:**
- Semi-transparent backgrounds
- Backdrop blur
- Subtle borders
- Shadow effects

**Color Scheme:**
- **Cyber Blue:** #0ea5e9
- **Cyber Purple:** #a855f7
- **Cyber Pink:** #ec4899
- **Dark Background:** Custom grays

**Animations:**
- All transitions: 150ms (reduced from 300ms for speed)
- Framer Motion spring animations
- GPU-accelerated transforms
- Stagger animations on lists

---

## Backend API Documentation

### Base URL
- Development: `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs` (Swagger UI)

### API Endpoints

#### Dashboard API (`/api/dashboard`)

**GET /api/dashboard/stats**
- **Purpose:** Get overall SOC statistics
- **Response:**
  ```json
  {
    "total_endpoints": 75,
    "healthy_endpoints": 68,
    "at_risk_endpoints": 7,
    "total_incidents": 42,
    "active_threats": 3,
    "risk_score": 0.45,
    "detection_rate": 0.88
  }
  ```

#### Incidents API (`/api/incidents`)

**GET /api/incidents/**
- **Query Parameters:**
  - `status`: "open" | "resolved"
  - `severity`: "critical" | "high" | "medium" | "low"
  - `limit`: Number (default: 50)
- **Response:** Array of incidents with full details

**GET /api/incidents/{id}**
- **Purpose:** Get single incident details
- **Response:** Complete incident object with:
  - Anomaly scores (all 4 models + ensemble)
  - MITRE techniques  
  - Feature contributions
  - AI explanation
  - Telemetry snapshot

**GET /api/incidents/{id}/playbooks**
- **Purpose:** Get recommended playbooks for incident
- **Response:** Array of applicable playbooks

**POST /api/incidents/{id}/report**
- **Purpose:** Generate PDF report
- **Response:** Report metadata

**GET /api/incidents/{id}/report/download**
- **Purpose:** Download PDF file
- **Response:** Binary PDF file

#### Logs API (`/api/logs`)

**WS /api/logs/stream**
- **Type:** WebSocket endpoint
- **Purpose:** Real-time log streaming
- **Message Format:**
  ```json
  {
    "id": "log-{timestamp}",
    "timestamp": "ISO-8601",
    "endpoint_id": "EP-021",
    "hostname": "WEB-SERVER-01",
    "severity": "critical",
    "message": "Suspicious activity detected",
    "data": { ...telemetry }
  }
  ```
- **Connection:** Auto-reconnects on disconnect

#### Threats API (`/api/threats`)

**GET /api/threats/endpoints**
- **Purpose:** List all monitored endpoints
- **Response:**
  ```json
  {
    "endpoints": [
      {
        "id": "EP-001",
        "hostname": "WEB-SERVER-01",
        "ip": "192.168.1.10",
        "role": "web_server",
        "os": "Ubuntu 22.04",
        "status": "healthy" | "compromised"
      }
    ]
  }
  ```

**GET /api/threats/analyze/{endpoint_id}**
- **Purpose:** Run ML analysis on specific endpoint
- **Process:**
  1. Generates current telemetry snapshot
  2. Runs through ensemble detector
  3. Maps to MITRE techniques
  4. Generates AI explanation
- **Response:**
  ```json
  {
    "endpoint_id": "EP-021",
    "anomaly_score": {
      "autoencoder_score": 0.85,
      "isolation_forest_score": 0.78,
      "lof_score": 0.82,
      "lstm_score": 0.79,
      "ensemble_score": 0.81,
      "is_anomaly": true,
      "confidence": 0.94
    },
    "mitre_techniques": [...],
    "feature_contributions": [...],
    "explanation": "AI-generated text"
  }
  ```

#### Automation API (`/api/automation`)

**GET /api/automation/playbooks**
- **Purpose:** List all available playbooks
- **Response:** Array of playbook definitions

**POST /api/automation/sessions**
- **Body:**
  ```json
  {
    "incident_id": "INC-042",
    "playbook_id": "PB-001"
  }
  ```
- **Purpose:** Start new playbook session
- **Response:** Session object with current state

**GET /api/automation/sessions/{session_id}**
- **Purpose:** Get session state
- **Response:** Current step, status, progress

**POST /api/automation/sessions/{session_id}/steps/{step_id}/execute**
- **Purpose:** Execute automated step
- **Response:** Updated session state

**POST /api/automation/sessions/{session_id}/steps/{step_id}/status**
- **Body:**  `{ "status": "completed" | "skipped" }`
- **Purpose:** Manually update step status

---

## Machine Learning Models

### Model Architecture

**1. Deep Autoencoder**
- **Architecture:** 
  - Input layer: 12 features
  - Encoder: 12 → 8 → 4 neurons
  - Decoder: 4 → 8 → 12 neurons
  - Activation: ReLU
- **Detection Method:** Reconstruction error
- **Threshold:** Z-score based (configurable)
- **Purpose:** Learns normal behavior patterns

**2. Isolation Forest**
- **Type:** Tree-based anomaly detector
- **Parameters:**
  - n_estimators: 100
  - contamination: 0.1
  - max_features: 12
- **Purpose:** Efficiently isolates outliers

**3. Local Outlier Factor (LOF)**
- **Type:** Density-based detector
- **Parameters:**
  - n_neighbors: 20
  - contamination: 0.1
- **Purpose:** Finds low-density data points

**4. LSTM (Long Short-Term Memory)**
- **Architecture:**
  - Input: Sequence of 10 timesteps
  - LSTM layers: 50 → 25 units
  - Output: Reconstructed sequence
- **Purpose:** Temporal pattern analysis
- **Note:** Optional, sequence-based

### Ensemble Detection
- **Method:** Weighted average of all model scores
- **Thresholding:** Configurable per model
- **Final Score:** 0.0 (normal) to 1.0 (anomaly)
- **Classification:**
  - CRITICAL: ≥ 0.80
  - HIGH: 0.70 - 0.79
  - MEDIUM: 0.55 - 0.69
  - LOW: < 0.55

### Training Data
- **Normal Samples:** 10,000 synthetic data points
- **Features:** 12 telemetry metrics
- **Validation:** 20% holdout set
- **Storage:** `backend/models_saved/`

---

## Data Flow & System Integration

### Real-Time Detection Loop

**Cycle:** Runs continuously every 1 second

1. **Telemetry Generation:**
   - Select 3 random endpoints
   - Generate normal telemetry point
   - Broadcast as INFO log via WebSocket

2. **Attack Simulation (40% chance):**
   - Random attack type selected
   - Random endpoint targeted
   - Generate attack sequence (15s duration)
   - Each point in sequence:
     - Run through ensemble detector
     - Calculate anomaly score
     - Broadcast as WARNING/CRITICAL log
     - If anomaly detected:
       - Map to MITRE techniques
       - Generate AI explanation
       - Create incident record
       - Broadcast alert

3. **State Updates:**
   - Update endpoint status
   - Increment incident counters
   - Update risk scores

### WebSocket Architecture
- **Manager:** Centralized connection manager
- **Broadcast:** Fan-out to all connected clients
- **Topics:**
  - Telemetry logs
  - Incident alerts
  - System status

### Data Storage
- **Type:** In-memory data store
- **Collections:**
  - Incidents (with full ML results)
  - Endpoints (metadata + status)
  - Playbook sessions (state tracking)
- **Persistence:** None (resets on restart)

### MITRE ATT&CK Mapping

**Mapping Logic:**
- Feature-based rules:
  - High failed_logins → T1110 (Brute Force)
  - High CPU → T1496 (Crypto Mining)
  - High network_out → T1048 (Data Exfil)
  - High process_creation → T1068 (Privilege Escalation)
  - High dns_queries → T1071 (C2 Activity)
  - Lateral movement indicators → T1021
  - Exploit patterns → T1190
- **Confidence Scoring:** Based on feature deviation
- **Top-K Selection:** Returns top 3 techniques

### PDF Report Generation
- **Library:** ReportLab
- **Sections:**
  1. Executive summary
  2. Incident timeline
  3. ML model scores (bar charts)
  4. Feature analysis (tables)
  5. MITRE mapping
  6. Recommendations
- **Format:** Professional multi-page PDF
- **Storage:** Generated on-demand, served via download endpoint

---

## Configuration & Deployment

### Environment Variables
- `API_HOST`: Backend host (default: 0.0.0.0)
- `API_PORT`: Backend port (default: 8000)
- `NUM_ENDPOINTS`: Endpoint count (default: 75)
- `CORS_ORIGINS`: Allowed origins (default: localhost:3000)

### Performance Settings
- **Detection Cycle:** 1s
- **WebSocket Update:** Real-time
- **Dashboard Refresh:** 3s
- **Incident Refresh:** 8s
- **Log Buffer:** 200 messages max

### Realistic Metrics
- **Precision:** 85-92%
- **Recall:** 80-90%
- **F1 Score:** ~0.88
- **False Positive Rate:** ~8%
- **Missed Detection Rate:** ~12%

---

## Summary

This AI SOC Platform is a comprehensive, production-ready threat detection system featuring:
- **8 Frontend Pages** with rich, interactive UIs
- **6 Major API Modules** with 20+ endpoints
- **4 ML Models** in an ensemble architecture
- **7 MITRE ATT&CK Techniques** with automated mapping
- **Real-time Streaming** via WebSockets
- **Automated Response** with guided playbooks
- **Professional Reporting** with PDF generation

Built with modern technologies (Next.js 14, FastAPI, TensorFlow) and designed for both demonstration and educational purposes in cybersecurity and AI/ML applications.
