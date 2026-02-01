'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { automationAPI, incidentsAPI } from '@/lib/api'
import { useRouter, useSearchParams } from 'next/navigation'

export default function PlaybookEnginePage() {
    const [view, setView] = useState<'library' | 'session'>('library')
    const [playbooks, setPlaybooks] = useState<any[]>([])
    const [incidents, setIncidents] = useState<any[]>([])

    // Session State
    const [activeSession, setActiveSession] = useState<any>(null)
    const [activePlaybook, setActivePlaybook] = useState<any>(null)
    const [loading, setLoading] = useState(true)

    // Modal
    const [selectedPlaybook, setSelectedPlaybook] = useState<any | null>(null)
    const [targetIncidentId, setTargetIncidentId] = useState<string>('')

    const searchParams = useSearchParams()

    useEffect(() => {
        loadData()
    }, [])

    const loadData = async () => {
        try {
            const [pbRes, incRes] = await Promise.all([
                automationAPI.listPlaybooks(),
                incidentsAPI.list({ status: 'open', limit: 50 })
            ])
            setPlaybooks(pbRes.data)
            setIncidents(incRes.data.filter((i: any) => i.status !== 'resolved'))
            setLoading(false)

            // Check if incident ID in URL
            const incidentId = searchParams.get('incidentId')
            if (incidentId) {
                // Check if active session exists
                try {
                    const sessionRes = await automationAPI.getSessionByIncident(incidentId)
                    if (sessionRes.data) {
                        resumeSession(sessionRes.data)
                    }
                } catch { /* No session */ }
            }
        } catch (e) {
            console.error(e)
            setLoading(false)
        }
    }

    const startSession = async () => {
        if (!selectedPlaybook || !targetIncidentId) return
        try {
            setLoading(true)
            const res = await automationAPI.startSession(targetIncidentId, selectedPlaybook.id)
            resumeSession(res.data)
            setSelectedPlaybook(null)
        } catch (e) {
            console.error(e)
        } finally {
            setLoading(false)
        }
    }

    const resumeSession = (session: any) => {
        const pb = playbooks.find(p => p.id === session.playbook_id)
        if (pb) {
            setActivePlaybook(pb)
            setActiveSession(session)
            setView('session')
        } else {
            // If playbooks not loaded yet, wait? 
            // Simplified: Re-fetch list if needed or assume loaded.
            automationAPI.listPlaybooks().then(res => {
                const found = res.data.find((p: any) => p.id === session.playbook_id)
                setActivePlaybook(found)
                setActiveSession(session)
                setView('session')
            })
        }
    }

    return (
        <div className="min-h-screen text-white">
            <AnimatePresence mode="wait">
                {view === 'library' && (
                    <motion.div
                        key="library"
                        initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                        className="space-y-8"
                    >
                        <header>
                            <h1 className="text-4xl font-black bg-gradient-to-r from-cyber-blue to-purple-500 bg-clip-text text-transparent">
                                PLAYBOOK LIBRARY
                            </h1>
                            <p className="text-gray-400 font-mono mt-2">
                                SELECT A PROTOCOL TO INITIALIZE RESPONSE SEQUENCE
                            </p>
                        </header>

                        <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
                            {playbooks.map(pb => (
                                <PlaybookCard key={pb.id} playbook={pb} onSelect={() => setSelectedPlaybook(pb)} />
                            ))}
                        </div>
                    </motion.div>
                )}

                {view === 'session' && activeSession && activePlaybook && (
                    <MissionControl
                        session={activeSession}
                        playbook={activePlaybook}
                        onExit={() => setView('library')}
                        onUpdate={(s: any) => setActiveSession(s)}
                    />
                )}
            </AnimatePresence>

            {/* Start Modal */}
            {selectedPlaybook && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm">
                    <div className="glass-panel p-8 w-full max-w-md relative border border-cyber-blue">
                        <button onClick={() => setSelectedPlaybook(null)} className="absolute top-4 right-4 text-gray-400 hover:text-white">✕</button>
                        <h2 className="text-xl font-bold mb-1 text-cyber-blue">{selectedPlaybook.name}</h2>
                        <div className="w-full h-px bg-white/10 my-4"></div>

                        <label className="block text-xs font-bold text-gray-500 mb-2 uppercase">Target Incident</label>
                        <select
                            className="w-full bg-black/50 border border-white/20 p-3 rounded mb-6 text-sm"
                            value={targetIncidentId}
                            onChange={(e) => setTargetIncidentId(e.target.value)}
                        >
                            <option value="">Select Active Threat...</option>
                            {incidents.map(inc => (
                                <option key={inc.id} value={inc.id}>{inc.id}: {inc.attack_type} ({inc.severity})</option>
                            ))}
                        </select>

                        <button
                            disabled={!targetIncidentId || loading}
                            onClick={startSession}
                            className="w-full py-4 bg-cyber-blue hover:bg-cyber-blue/80 text-black font-bold uppercase tracking-widest transition-all"
                        >
                            {loading ? 'Initializing...' : 'Initialize Protocol'}
                        </button>
                    </div>
                </div>
            )}
        </div>
    )
}

function PlaybookCard({ playbook, onSelect }: any) {
    return (
        <div
            onClick={onSelect}
            className="glass-panel p-6 cursor-pointer hover:border-cyber-blue/50 transition-all group relative overflow-hidden"
        >
            <div className="absolute top-0 right-0 p-3 opacity-10 text-4xl group-hover:opacity-20 transition-opacity">
                {playbook.severity.includes('Critical') ? '☠️' : '🛡️'}
            </div>

            <div className="mb-4">
                <span className="text-[10px] font-mono border border-white/10 px-2 py-1 rounded text-cyber-blue">
                    {playbook.id}
                </span>
            </div>

            <h3 className="text-xl font-bold text-white mb-2 group-hover:text-cyber-blue transition-colors">{playbook.name}</h3>
            <p className="text-sm text-gray-400 line-clamp-2 mb-4">{playbook.description}</p>

            <div className="flex flex-wrap gap-2 mb-4">
                {playbook.mitreTechniques.slice(0, 3).map((m: string) => (
                    <span key={m} className="px-2 py-1 bg-white/5 rounded text-[10px] text-gray-500 font-mono">{m}</span>
                ))}
            </div>

            <div className="flex items-center justify-between text-xs text-gray-500 font-mono border-t border-white/5 pt-4">
                <span>{playbook.steps.length} STEPS</span>
                <span>~{playbook.estimatedDuration} MINS</span>
            </div>
        </div>
    )
}

function MissionControl({ session, playbook, onExit, onUpdate }: any) {
    const activeStepId = playbook.steps[session.current_step_index]?.id
    const activeStep = playbook.steps.find((s: any) => s.id === activeStepId)
    const [executing, setExecuting] = useState(false)
    const [incidentData, setIncidentData] = useState<any>(null)

    useEffect(() => {
        if (session.incident_id && !incidentData) {
            incidentsAPI.get(session.incident_id)
                .then(res => setIncidentData(res.data))
                .catch(console.error)
        }
    }, [session.incident_id, incidentData])

    const handleStepAction = async (action: 'complete' | 'skip' | 'execute') => {
        if (!activeStep) return
        setExecuting(true)
        try {
            if (action === 'execute') {
                await automationAPI.executeStep(session.session_id, activeStep.id)
                // Refresh session state
                const res = await automationAPI.getSession(session.session_id)
                onUpdate(res.data)
            } else {
                const status = action === 'complete' ? 'completed' : 'skipped'
                const res = await automationAPI.updateStep(session.session_id, activeStep.id, status)
                onUpdate(res.data)
            }
        } catch (e) {
            console.error(e)
        } finally {
            setExecuting(false)
        }
    }

    const progress = (Object.values(session.step_statuses).filter(s => s === 'completed' || s === 'skipped').length / playbook.steps.length) * 100

    return (
        <div className="grid grid-cols-12 gap-6 h-[calc(100vh-140px)]">
            {/* Sidebar / Timeline */}
            <div className="col-span-4 glass-panel flex flex-col h-full overflow-hidden">
                <div className="p-6 border-b border-white/10 bg-black/20">
                    <div className="flex justify-between items-start mb-2">
                        <button onClick={onExit} className="text-xs text-gray-500 hover:text-white mb-2">← LIBRARY</button>
                        <span className="text-xs font-mono text-green-400 animate-pulse">LIVE SESSION</span>
                    </div>
                    <h2 className="font-bold text-lg leading-tight mb-1">{playbook.name}</h2>

                    {incidentData ? (
                        <div className="mt-2 p-3 bg-red-500/10 border border-red-500/20 rounded">
                            <div className="text-[10px] text-gray-400 font-bold uppercase">Target Incident</div>
                            <div className="text-sm font-bold text-white">{incidentData.attack_type?.replace(/_/g, ' ').toUpperCase()}</div>
                            <div className="text-xs font-mono text-red-400">HOST: {incidentData.hostname || incidentData.endpoint_id}</div>
                            <div className="text-[10px] text-gray-500 mt-1">ID: {incidentData.id}</div>
                        </div>
                    ) : (
                        <div className="text-xs font-mono text-gray-400 animate-pulse">Loading Incident Data...</div>
                    )}

                    <div className="w-full bg-gray-800 h-1 mt-4 rounded-full overflow-hidden">
                        <div className="h-full bg-cyber-blue transition-all duration-500" style={{ width: `${progress}%` }}></div>
                    </div>
                </div>

                <div className="flex-1 overflow-y-auto p-4 space-y-4">
                    {playbook.steps.map((step: any, i: number) => {
                        const status = session.step_statuses[step.id]
                        const isActive = step.id === activeStepId
                        return (
                            <div key={step.id} className={`p-4 rounded border transition-all ${isActive ? 'bg-cyber-blue/5 border-cyber-blue shadow-[0_0_15px_rgba(34,211,238,0.1)]' : 'bg-white/5 border-transparent opacity-60'}`}>
                                <div className="flex justify-between items-center mb-2">
                                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${status === 'completed' ? 'bg-green-500/20 text-green-400' : 'bg-gray-700 text-gray-400'}`}>
                                        STEP {i + 1}
                                    </span>
                                    {status === 'completed' && <span>✅</span>}
                                </div>
                                <h4 className="font-bold text-sm mb-1">{step.title}</h4>
                                <div className="flex items-center gap-2 text-[10px] text-gray-500 font-mono">
                                    <span>{step.actionType === 'automated' ? '⚡ AUTO' : step.actionType === 'decision' ? '⚠️ DECISION' : '👤 MANUAL'}</span>
                                    <span>• {step.estimatedMinutes}m</span>
                                </div>
                            </div>
                        )
                    })}
                </div>
            </div>

            {/* Active Step Interface */}
            <div className="col-span-8 glass-panel h-full flex flex-col relative overflow-hidden">
                {!session.completed && activeStep ? (
                    <>
                        <div className="absolute top-0 right-0 p-32 bg-cyber-blue/5 blur-[100px] pointer-events-none rounded-full"></div>

                        <div className="p-12 z-10 flex-1 flex flex-col justify-center max-w-3xl mx-auto w-full">
                            <div className="mb-4">
                                <span className="text-cyber-blue font-mono text-xs tracking-widest border border-cyber-blue/30 px-3 py-1 rounded-full">
                                    CURRENT OBJECTIVE
                                </span>
                            </div>

                            <h1 className="text-4xl font-black mb-4 leading-tight">{activeStep.title}</h1>
                            <div className="bg-white/5 p-6 rounded-lg border border-white/10 mb-8 backdrop-blur-sm">
                                <div className="text-xs text-gray-500 font-bold mb-2 uppercase">Protocol Description</div>
                                <p className="text-lg text-gray-300 leading-relaxed font-mono">{activeStep.description}</p>
                            </div>

                            {activeStep.automationHook && (
                                <div className="bg-black/80 font-mono text-xs p-4 rounded-lg border border-white/20 mb-8 shadow-inner shadow-black/50 relative overflow-hidden group">
                                    <div className="absolute top-0 left-0 w-full h-1 bg-cyber-blue/20"></div>
                                    <div className="flex justify-between items-center mb-2 text-gray-500 border-b border-white/10 pb-2">
                                        <span>TERMINAL: SOC_AUTOMATION_V2</span>
                                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                                    </div>
                                    <div className="space-y-1 text-gray-300">
                                        <div>&gt; target_hook: <span className="text-cyber-blue">{activeStep.automationHook}</span></div>
                                        <div>&gt; status: <span className="text-green-400">READY</span></div>
                                        {executing && (
                                            <>
                                                <div className="animate-pulse">&gt; Executing script payload...</div>
                                                <div>&gt; Handshake established (latency: 12ms)</div>
                                                <div className="text-yellow-400">&gt; Awaiting agent response...</div>
                                            </>
                                        )}
                                    </div>
                                </div>
                            )}

                            <div className="flex gap-4">
                                {activeStep.actionType === 'automated' ? (
                                    <button
                                        disabled={executing}
                                        onClick={() => handleStepAction('execute')}
                                        className={`flex-1 py-4 font-bold rounded flex items-center justify-center gap-2 transition-all ${executing ? 'bg-gray-700 text-gray-500' : 'bg-cyber-blue text-black hover:bg-white'}`}
                                    >
                                        {executing ? <span className="animate-spin">⚡</span> : '⚡'}
                                        {executing ? 'EXECUTING PROTOCOL...' : 'EXECUTE AUTOMATION'}
                                    </button>
                                ) : (
                                    <button
                                        onClick={() => handleStepAction('complete')}
                                        className="flex-1 py-4 bg-green-500/20 text-green-400 border border-green-500/50 font-bold rounded hover:bg-green-500/30 transition-colors"
                                    >
                                        MARK COMPLETE
                                    </button>
                                )}

                                <button
                                    onClick={() => handleStepAction('skip')}
                                    className="px-8 py-4 border border-white/10 hover:bg-white/5 rounded text-gray-400 font-bold"
                                    title="Skip Step"
                                >
                                    SKIP
                                </button>
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="flex flex-col items-center justify-center h-full text-center p-12">
                        <div className="text-6xl mb-6">🎉</div>
                        <h2 className="text-4xl font-bold mb-4">Protocol Completed</h2>
                        <p className="text-gray-400 max-w-md mx-auto mb-8">
                            All objectives for {playbook.name} have been successfully achieved. The incident status has been updated.
                        </p>
                        <button
                            onClick={onExit}
                            className="px-8 py-3 bg-white/10 hover:bg-white/20 rounded text-white font-bold"
                        >
                            RETURN TO LIBRARY
                        </button>
                    </div>
                )}
            </div>
        </div>
    )
}
