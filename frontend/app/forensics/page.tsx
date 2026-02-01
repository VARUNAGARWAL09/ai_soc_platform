'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { automationAPI, incidentsAPI } from '@/lib/api'
import { useRouter } from 'next/navigation'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'

export default function ForensicsPage() {
    const [incidents, setIncidents] = useState<any[]>([])
    const [selectedIncident, setSelectedIncident] = useState<any>(null)

    useEffect(() => {
        // Determine incidents for the timeline
        const fetch = async () => {
            try {
                const params = new URLSearchParams(window.location.search)
                const targetId = params.get('id')

                const res = await incidentsAPI.list({ limit: 20 })
                setIncidents(res.data)

                if (targetId) {
                    const found = res.data.find((i: any) => i.id === targetId)
                    if (found) {
                        setSelectedIncident(found)
                    } else {
                        try {
                            const specific = await incidentsAPI.get(targetId)
                            if (specific.data) {
                                setIncidents(prev => [specific.data, ...prev.filter((i: any) => i.id !== targetId)])
                                setSelectedIncident(specific.data)
                            }
                        } catch (err) {
                            if (res.data.length > 0) setSelectedIncident(res.data[0])
                        }
                    }
                } else if (res.data.length > 0) {
                    setSelectedIncident(res.data[0])
                }
            } catch (e) { }
        }
        fetch()
    }, [])

    const timelineData = selectedIncident ? Array.from({ length: 20 }).map((_, i) => {
        const isSpike = i > 14 && i < 18
        const random = Math.random()
        return {
            time: `-${20 - i}m`,
            cpu: selectedIncident.telemetry_snapshot.cpu_usage * (isSpike ? 1.5 + random : 0.8 + random * 0.2),
            memory: selectedIncident.telemetry_snapshot.memory_usage * (isSpike ? 1.2 : 0.9 + random * 0.1),
            network: selectedIncident.telemetry_snapshot.network_out * (isSpike ? 3.0 + random : 0.5 + random * 0.5),
        }
    }) : []

    const handleExport = () => {
        if (!selectedIncident) return
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(selectedIncident, null, 2))
        const downloadAnchorNode = document.createElement('a')
        downloadAnchorNode.setAttribute("href", dataStr)
        downloadAnchorNode.setAttribute("download", `CASE-${selectedIncident.id}.json`)
        document.body.appendChild(downloadAnchorNode)
        downloadAnchorNode.click()
        downloadAnchorNode.remove()
    }

    const handleReport = () => {
        if (!selectedIncident) return
        window.open(`http://localhost:8000/api/incidents/${selectedIncident.id}/report/download`, '_blank')
    }

    return (
        <div className="space-y-6 h-[calc(100vh-100px)] flex flex-col">
            <header className="flex justify-between items-center">
                <h1 className="text-3xl font-black bg-gradient-to-r from-blue-500 to-purple-600 bg-clip-text text-transparent">
                    DIGITAL FORENSICS
                </h1>
                <div className="flex space-x-2">
                    <button onClick={handleExport} className="px-4 py-2 bg-gray-100 dark:bg-white/5 hover:bg-gray-200 dark:hover:bg-white/10 rounded border border-gray-200 dark:border-white/10 text-sm transition-all text-gray-700 dark:text-gray-200 uppercase font-mono tracking-wider">Export Case Data</button>
                    <button onClick={handleReport} className="px-4 py-2 bg-cyber-blue hover:bg-cyber-blue/80 text-white font-bold rounded text-sm transition-all shadow-lg shadow-cyber-blue/20">Generate Report</button>
                </div>
            </header>

            <div className="grid grid-cols-12 gap-6 flex-1 min-h-0">
                {/* Incident List */}
                <div className="col-span-3 glass-panel flex flex-col overflow-hidden relative">
                    <div className="absolute inset-0 bg-grid-pattern opacity-5 pointer-events-none"></div>
                    <div className="p-4 border-b border-gray-200 dark:border-white/10 bg-gray-50/50 dark:bg-white/5 flex justify-between items-center backdrop-blur-sm z-10">
                        <h3 className="font-bold text-gray-500 dark:text-gray-300 tracking-wider text-sm">CASE DIRECTORY</h3>
                        <span className="text-[10px] bg-blue-100 dark:bg-cyber-blue/10 text-blue-600 dark:text-cyber-blue px-2 py-0.5 rounded font-mono">
                            {incidents.length} FILES
                        </span>
                    </div>
                    <div className="overflow-y-auto flex-1 p-2 space-y-2 z-10">
                        {incidents.map(inc => (
                            <div
                                key={inc.id}
                                onClick={() => setSelectedIncident(inc)}
                                className={`p-4 rounded-sm cursor-pointer transition-all border-l-2 relative group overflow-hidden ${selectedIncident?.id === inc.id
                                    ? 'bg-blue-50 dark:bg-cyber-blue/10 border-cyber-blue shadow-sm'
                                    : 'bg-white dark:bg-white/5 border-transparent hover:bg-gray-50 dark:hover:bg-white/10'
                                    }`}
                            >
                                <div className="flex justify-between mb-1 relative z-10">
                                    <span className={`font-mono text-xs font-bold ${selectedIncident?.id === inc.id ? 'text-blue-600 dark:text-cyber-blue' : 'text-gray-500 dark:text-gray-400'
                                        }`}>
                                        {inc.id}
                                    </span>
                                    <span className="text-[10px] text-gray-400 dark:text-gray-500 font-mono">{new Date(inc.timestamp).toLocaleTimeString()}</span>
                                </div>
                                <div className="font-bold text-sm truncate text-gray-800 dark:text-gray-200 relative z-10">
                                    {inc.attack_type || 'Unknown Threat'}
                                </div>
                                <div className="text-[10px] text-gray-500 mt-2 flex items-center gap-2">
                                    <span className={`w-1.5 h-1.5 rounded-full ${inc.severity === 'critical' ? 'bg-red-500' : 'bg-yellow-500'}`}></span>
                                    {inc.endpoint_id}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* Main Analysis View */}
                <div className="col-span-9 flex flex-col gap-6 overflow-y-auto pr-2">
                    {selectedIncident ? (
                        <>
                            {/* Top Stats */}
                            <div className="grid grid-cols-4 gap-4">
                                <StatBox label="SEVERITY" value={selectedIncident.severity.toUpperCase()} color="red" />
                                <StatBox label="CONFIDENCE" value={`${(selectedIncident.anomaly_scores.confidence * 100).toFixed(1)}%`} color="blue" />
                                <StatBox label="DATA EXFIL" value={`${(selectedIncident.telemetry_snapshot.network_out / 1024).toFixed(1)} KB`} color="purple" />
                                <StatBox label="PROCESSES" value={selectedIncident.telemetry_snapshot.process_count} color="green" />
                            </div>

                            {/* Timeline Chart */}
                            <div className="glass-panel p-6">
                                <h3 className="font-bold mb-4 text-blue-600 dark:text-cyber-blue">ATTACK TIMELINE RECONSTRUCTION</h3>
                                <div className="h-64 w-full">
                                    <ResponsiveContainer>
                                        <LineChart data={timelineData}>
                                            <CartesianGrid strokeDasharray="3 3" stroke="#88888820" />
                                            <XAxis dataKey="time" stroke="#888" fontSize={12} />
                                            <YAxis yAxisId="left" stroke="#0ea5e9" fontSize={12} label={{ value: 'Usage %', angle: -90, position: 'insideLeft' }} />
                                            <YAxis yAxisId="right" orientation="right" stroke="#a855f7" fontSize={12} label={{ value: 'Network (KB)', angle: 90, position: 'insideRight' }} />
                                            <Tooltip
                                                contentStyle={{ backgroundColor: 'rgba(255, 255, 255, 0.9)', borderColor: '#ddd', borderRadius: '8px' }}
                                                itemStyle={{ color: '#333' }}
                                            />
                                            <Line yAxisId="left" type="monotone" name="CPU" dataKey="cpu" stroke="#0ea5e9" strokeWidth={2} dot={false} />
                                            <Line yAxisId="left" type="monotone" name="RAM" dataKey="memory" stroke="#22c55e" strokeWidth={2} dot={false} />
                                            <Line yAxisId="right" type="monotone" name="Net Out" dataKey="network" stroke="#a855f7" strokeWidth={2} dot={false} />
                                        </LineChart>
                                    </ResponsiveContainer>
                                </div>
                            </div>

                            {/* AI Analysis */}
                            <div className="glass-panel p-6">
                                <h3 className="font-bold mb-4 text-pink-600 dark:text-cyber-pink">AI ROOT CAUSE ANALYSIS</h3>
                                <div className="bg-white dark:bg-white/5 p-4 rounded font-mono text-sm text-gray-700 dark:text-gray-300 border-l-2 border-pink-500 shadow-sm">
                                    {selectedIncident.explanation}
                                </div>

                                <div className="mt-6">
                                    <h4 className="text-sm font-bold text-gray-500 dark:text-gray-400 mb-2">MITRE ATT&CK MAPPING</h4>
                                    <div className="flex flex-wrap gap-2">
                                        {selectedIncident.mitre_techniques?.map((tech: any) => (
                                            <span key={tech.technique_id} className="px-3 py-1 bg-white dark:bg-white/10 rounded border border-gray-200 dark:border-white/20 text-xs hover:bg-blue-50 dark:hover:bg-cyber-blue/20 hover:border-blue-300 dark:hover:border-cyber-blue transition-colors cursor-help">
                                                <b className="text-gray-900 dark:text-white">{tech.technique_id}:</b> <span className="text-gray-600 dark:text-gray-300">{tech.name}</span>
                                            </span>
                                        ))}
                                    </div>
                                </div>
                            </div>

                            {/* Response Playbooks */}
                            <PlaybookSection incidentId={selectedIncident.id} />
                        </>
                    ) : (
                        <div className="flex h-full items-center justify-center text-gray-500">
                            Select a case file to begin forensics analysis
                        </div>
                    )}
                </div>
            </div>
        </div>
    )
}

function PlaybookSection({ incidentId }: { incidentId: string }) {
    const router = useRouter()
    const [playbooks, setPlaybooks] = useState<any[]>([])
    const [executing, setExecuting] = useState<string | null>(null)
    const [results, setResults] = useState<any>({})

    useEffect(() => {
        incidentsAPI.getPlaybooks(incidentId).then(res => setPlaybooks(res.data)).catch(console.error)
        setResults({})
    }, [incidentId])

    const runPlaybook = async (pb: any) => {
        setExecuting(pb.id)
        try {
            await automationAPI.startSession(incidentId, pb.id)
            router.push(`/playbooks?incidentId=${incidentId}`)
        } catch (e) {
            console.error(e)
            router.push(`/playbooks?incidentId=${incidentId}`)
        }
        setExecuting(null)
    }

    return (
        <div className="glass-panel p-6 border-t-4 border-purple-500">
            <h3 className="font-bold mb-4 flex items-center gap-2">
                <span className="text-xl">🛡️</span>
                <span className="text-purple-600 dark:text-cyber-purple">AUTOMATED RESPONSE PLAYBOOKS</span>
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {playbooks.map(pb => (
                    <div key={pb.id} className="bg-white dark:bg-white/5 p-4 rounded border border-gray-200 dark:border-white/10 hover:border-purple-400 dark:hover:border-cyber-purple/50 transition-all shadow-sm">
                        <div className="flex justify-between items-start mb-3">
                            <div>
                                <h4 className="font-bold text-gray-900 dark:text-white text-lg leading-none mb-1">{pb.name}</h4>
                                <div className="flex gap-2 mt-2">
                                    {pb.severity.includes('Critical') && (
                                        <span className="text-[10px] font-bold bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-400 px-1.5 py-0.5 rounded border border-red-200 dark:border-red-500/30">CRITICAL</span>
                                    )}
                                    <span className="text-[10px] font-mono bg-blue-100 text-blue-600 dark:bg-blue-500/10 dark:text-blue-300 px-1.5 py-0.5 rounded border border-blue-200 dark:border-blue-500/30">
                                        ⏱ {pb.estimatedDuration}m
                                    </span>
                                </div>
                            </div>
                            {executing === pb.id ? (
                                <span className="text-xs text-blue-500 dark:text-cyber-blue font-mono animate-pulse border border-blue-300 dark:border-cyber-blue/30 px-2 py-1 rounded">RUNNING</span>
                            ) : results[pb.id] === 'success' ? (
                                <span className="text-xs text-green-500 dark:text-green-400 font-mono border border-green-300 dark:border-green-500/30 px-2 py-1 rounded">MITIGATED</span>
                            ) : (
                                <span className="text-[10px] text-gray-500 bg-gray-100 dark:bg-white/5 px-2 py-1 rounded border border-gray-200 dark:border-white/10 self-center">READY</span>
                            )}
                        </div>
                        <p className="text-xs text-gray-500 dark:text-gray-400 mb-4 bg-gray-50 dark:bg-black/20 p-2 rounded border border-gray-200 dark:border-white/5">
                            <span className="text-gray-700 dark:text-gray-500 font-bold">TARGET:</span> {(pb.incidentType || 'GENERAL').toUpperCase()}
                        </p>
                        <button
                            disabled={!!executing || results[pb.id] === 'success'}
                            onClick={() => runPlaybook(pb)}
                            className={`w-full py-2 text-xs font-bold rounded flex items-center justify-center gap-2 transition-all ${results[pb.id] === 'success' ? 'bg-green-100 text-green-600 cursor-not-allowed' :
                                executing ? 'bg-gray-200 text-gray-500 cursor-not-allowed' :
                                    'bg-purple-600 hover:bg-purple-700 text-white shadow-lg shadow-purple-500/20'
                                }`}
                        >
                            {results[pb.id] === 'success' ? 'THREAT MITIGATED' : executing === pb.id ? 'RUNNING AUTOMATION...' : '▶ EXECUTE PLAYBOOK'}
                        </button>
                    </div>
                ))}
            </div>
        </div>
    )
}

function StatBox({ label, value, color }: any) {
    const colors: any = {
        red: {
            border: 'border-red-200 dark:border-red-500/50',
            bg: 'bg-red-50 dark:bg-red-500/10',
            text: 'text-red-500 dark:text-red-400',
            glow: 'shadow-red-500/10',
            gradient: 'from-red-500/5 to-transparent'
        },
        blue: {
            border: 'border-cyan-200 dark:border-cyan-400/50',
            bg: 'bg-cyan-50 dark:bg-cyan-400/10',
            text: 'text-cyan-600 dark:text-cyan-300',
            glow: 'shadow-cyan-400/10',
            gradient: 'from-cyan-400/5 to-transparent'
        },
        purple: {
            border: 'border-purple-200 dark:border-purple-500/50',
            bg: 'bg-purple-50 dark:bg-purple-500/10',
            text: 'text-purple-600 dark:text-purple-300',
            glow: 'shadow-purple-500/10',
            gradient: 'from-purple-500/5 to-transparent'
        },
        green: {
            border: 'border-emerald-200 dark:border-emerald-400/50',
            bg: 'bg-emerald-50 dark:bg-emerald-400/10',
            text: 'text-emerald-600 dark:text-emerald-300',
            glow: 'shadow-emerald-400/10',
            gradient: 'from-emerald-400/5 to-transparent'
        },
    }

    const theme = colors[color] || colors.blue

    return (
        <div className={`relative p-5 border ${theme.border} ${theme.bg} overflow-hidden group transition-all hover:scale-[1.02] hover:shadow-lg rounded-xl`}>
            <div className={`absolute inset-0 bg-gradient-to-br ${theme.gradient} opacity-50`}></div>
            <div className="relative z-10">
                <div className="text-[10px] font-mono tracking-[0.2em] text-gray-500 dark:text-gray-400 mb-1 uppercase">
                    {label}
                </div>
                <div className="text-3xl font-black tracking-tighter text-gray-900 dark:text-white drop-shadow-sm">
                    {value !== undefined && value !== null ? value : '--'}
                </div>
            </div>
        </div>
    )
}
