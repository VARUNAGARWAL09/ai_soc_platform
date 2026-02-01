import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
    (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8000');

export const apiClient = axios.create({
    baseURL: API_BASE_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Dashboard API
export const dashboardAPI = {
    getStats: () => apiClient.get('/api/dashboard/stats'),
    getRiskScore: () => apiClient.get('/api/dashboard/risk-score'),
    getActiveThreats: () => apiClient.get('/api/dashboard/active-threats'),
    getEndpointHealth: () => apiClient.get('/api/dashboard/endpoint-health'),
};

// Incidents API
export const incidentsAPI = {
    list: (params?: { limit?: number; severity?: string; status?: string }) =>
        apiClient.get('/api/incidents/', { params }),
    get: (id: string) => apiClient.get(`/api/incidents/${id}`),
    getTimeline: (id: string) => apiClient.get(`/api/incidents/${id}/timeline`),
    generateReport: (id: string) => apiClient.post(`/api/incidents/${id}/report`),
    updateStatus: (id: string, status: string) =>
        apiClient.put(`/api/incidents/${id}/status`, null, { params: { status } }),
    getPlaybooks: (id: string) => apiClient.get(`/api/incidents/${id}/playbooks`),
    executePlaybook: (incidentId: string, playbookId: string) =>
        apiClient.post(`/api/incidents/${incidentId}/playbooks/${playbookId}/execute`),
};

// Logs API
export const logsAPI = {
    getHistory: (limit: number = 100) =>
        apiClient.get('/api/logs/history', { params: { limit } }),
};

// Threats API
export const threatsAPI = {
    analyzeEndpoint: (endpointId: string) =>
        apiClient.get(`/api/threats/analyze/${endpointId}`),
    getMitreMapping: (incidentId: string) =>
        apiClient.get(`/api/threats/mitre/${incidentId}`),
    getExplanation: (incidentId: string) =>
        apiClient.get(`/api/threats/explain/${incidentId}`),
    listEndpoints: () => apiClient.get('/api/threats/endpoints'),
};

// Automation API
export const automationAPI = {
    listPlaybooks: () => apiClient.get('/api/automation/playbooks'),
    // executePlaybook (Legacy) - potentially deprecated but keeping for now if used elsewhere? 
    // Actually forcing new flow.
    startSession: (incidentId: string, playbookId: string) =>
        apiClient.post('/api/automation/sessions/start', { incident_id: incidentId, playbook_id: playbookId }),
    getSession: (sessionId: string) => apiClient.get(`/api/automation/sessions/${sessionId}`),
    getSessionByIncident: (incidentId: string) => apiClient.get(`/api/automation/sessions/incident/${incidentId}`),
    updateStep: (sessionId: string, stepId: string, status: string, notes?: string) =>
        apiClient.post(`/api/automation/sessions/${sessionId}/steps/${stepId}/update`, { status, notes }),
    executeStep: (sessionId: string, stepId: string) =>
        apiClient.post(`/api/automation/sessions/${sessionId}/steps/${stepId}/execute`, {})
};

// WebSocket utility
export function createWebSocket(path: string): WebSocket {
    const wsUrl = API_BASE_URL.replace('http', 'ws') + path;
    return new WebSocket(wsUrl);
}

export default apiClient;
