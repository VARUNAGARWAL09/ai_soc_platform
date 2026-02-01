'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { incidentsAPI } from '@/lib/api'

export default function IncidentsPage() {
    const [incidents, setIncidents] = useState<any[]>([])
    const [loading, setLoading] = useState(true)
    const [filter, setFilter] = useState<string>('all')

    useEffect(() => {
        fetchIncidents()
        // Auto-refresh every 8 seconds to prevent timeout
        const interval = setInterval(fetchIncidents, 8000)
        return () => clearInterval(interval)
    }, [filter])

    const fetchIncidents = async () => {
        try {
            const params = filter !== 'all' ? { severity: filter } : {}
            const response = await incidentsAPI.list({ ...params, limit: 50 })
            setIncidents(response.data)
            setLoading(false)
        } catch (error) {
            console.error('Error:', error)
            setLoading(false)
        }
    }

    const downloadReport = async (incidentId: string) => {
        try {
            window.open(`http://localhost:8000/api/incidents/${incidentId}/report/download`, '_blank')
        } catch (error) {
            console.error('Error downloading report:', error)
        }
    }

    const filters = [
        { id: 'all', label: 'All Events' },
        { id: 'critical', label: 'Critical', color: 'text-red-500' },
        { id: 'high', label: 'High', color: 'text-orange-500' },
        { id: 'medium', label: 'Medium', color: 'text-yellow-500' },
        { id: 'low', label: 'Low', color: 'text-green-500' },
    ]

    return (
        <div className="space-y-8">
            {/* Header */}
            <div className="flex flex-col md:flex-row justify-between items-center gap-4">
                <div className="flex items-center space-x-3">
                    <h1 className="text-3xl font-black bg-gradient-to-r from-red-500 to-purple-600 bg-clip-text text-transparent">
                        INCIDENT FEED
                    </h1>
                    <span className="flex h-3 w-3 relative">
                        <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"></span>
                        <span className="relative inline-flex rounded-full h-3 w-3 bg-red-500"></span>
                    </span>
                </div>

                {/* Filter Tabs */}
                <div className="flex bg-gray-200 dark:bg-white/5 p-1 rounded-xl">
                    {filters.map((f) => (
                        <button
                            key={f.id}
                            onClick={() => setFilter(f.id)}
                            className={`px-4 py-2 rounded-lg text-sm font-bold transition-all relative ${filter === f.id ? 'text-gray-900 dark:text-white' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'
                                }`}
                        >
                            {filter === f.id && (
                                <motion.div
                                    layoutId="filter-pill"
                                    className="absolute inset-0 bg-white dark:bg-white/10 shadow-sm rounded-lg"
                                    transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                                />
                            )}
                            <span className="relative z-10 flex items-center gap-2">
                                {f.label}
                                {f.color && <span className={`w-2 h-2 rounded-full ${f.color} bg-current`} />}
                            </span>
                        </button>
                    ))}
                </div>
            </div>

            {loading ? (
                <div className="flex justify-center py-20">
                    <div className="w-12 h-12 border-4 border-gray-300 border-t-blue-500 rounded-full animate-spin"></div>
                </div>
            ) : incidents.length === 0 ? (
                <div className="glass-panel p-16 text-center">
                    <div className="text-6xl mb-4 text-gray-200 dark:text-gray-700">🛡️</div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white">Secure Perimeter</h3>
                    <p className="text-gray-500">No active incidents matching your filter.</p>
                </div>
            ) : (
                <div className="grid gap-4">
                    {incidents.map((incident, index) => (
                        <motion.div
                            key={incident.id}
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: index * 0.05 }}
                            className="glass-panel p-8 border-l-4 group relative overflow-hidden transition-all hover:shadow-lg"
                            style={{ borderLeftColor: getSeverityColorHex(incident.severity) }}
                        >
                            <div className="flex flex-col md:flex-row justify-between gap-8">
                                <div className="flex-1 space-y-6">
                                    {/* Top Row: ID, Status, Severity */}
                                    <div className="flex items-center gap-3">
                                        <span className="font-mono text-lg font-bold text-gray-900 dark:text-white">{incident.id}</span>
                                        <div className="flex items-center gap-2 px-2 py-1 bg-gray-100 dark:bg-white/10 rounded border border-gray-200 dark:border-white/10">
                                            <span className="text-[10px] font-bold text-gray-500 dark:text-gray-400">HOST</span>
                                            <span className="text-xs font-mono font-bold text-cyber-blue">{incident.endpoint_id || 'UNKNOWN'}</span>
                                        </div>
                                        <Badge severity={incident.severity} />
                                        <span className="text-xs font-mono px-2 py-1 bg-gray-100 dark:bg-white/10 rounded text-gray-500 dark:text-gray-400">
                                            {incident.status.toUpperCase()}
                                        </span>
                                    </div>

                                    {/* Description */}
                                    <div className="text-base text-gray-800 dark:text-gray-200 font-medium">
                                        {incident.explanation || "Anomaly detected in endpoint behavior pattern."}
                                    </div>

                                    {/* Technique Chips */}
                                    {incident.mitre_techniques && (
                                        <div className="flex flex-wrap gap-2">
                                            {incident.mitre_techniques.map((tech: any) => (
                                                <span key={tech.technique_id} className="text-xs font-mono px-2 py-1 bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-300 border border-red-100 dark:border-red-900/30 rounded">
                                                    {tech.name}
                                                </span>
                                            ))}
                                        </div>
                                    )}
                                    {/* History Section */}
                                    {incidents.filter(i => i.endpoint_id === incident.endpoint_id && i.id !== incident.id).length > 0 && (
                                        <div className="mt-4 pt-4 border-t border-gray-100 dark:border-white/5">
                                            <h4 className="text-xs font-bold text-gray-500 dark:text-gray-400 mb-2 uppercase tracking-wide">
                                                Detected History on {incident.endpoint_id}
                                            </h4>
                                            <div className="flex flex-wrap gap-2">
                                                {incidents.filter(i => i.endpoint_id === incident.endpoint_id && i.id !== incident.id).slice(0, 3).map(past => (
                                                    <div key={past.id} className="flex items-center gap-2 bg-gray-50 dark:bg-black/20 px-2 py-1 rounded border border-gray-200 dark:border-white/5 text-xs">
                                                        <span className={`w-1.5 h-1.5 rounded-full ${past.severity === 'critical' ? 'bg-red-500' : 'bg-orange-500'}`}></span>
                                                        <span className="font-mono text-gray-700 dark:text-gray-300">{past.id}</span>
                                                        <span className="text-gray-400">({new Date(past.timestamp).toLocaleTimeString()})</span>
                                                    </div>
                                                ))}
                                                {incidents.filter(i => i.endpoint_id === incident.endpoint_id && i.id !== incident.id).length > 3 && (
                                                    <span className="text-xs text-gray-400 self-center pl-1">
                                                        +{incidents.filter(i => i.endpoint_id === incident.endpoint_id && i.id !== incident.id).length - 3} more
                                                    </span>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </div>

                                {/* Actions & Stats */}
                                <div className="flex flex-col items-end gap-3 min-w-[200px]">
                                    <div className="text-xs text-gray-500 dark:text-gray-400 font-mono text-right">
                                        <div>{new Date(incident.timestamp).toLocaleTimeString()}</div>
                                        <div className="font-bold text-cyber-blue">{(incident.anomaly_scores.confidence * 100).toFixed(0)}% Confidence</div>
                                    </div>

                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => window.location.href = `/forensics?id=${incident.id}`}
                                            className="px-3 py-1.5 text-sm bg-gray-100 dark:bg-white/10 hover:bg-gray-200 dark:hover:bg-white/20 rounded text-gray-700 dark:text-gray-200 transition-colors"
                                        >
                                            Investigate
                                        </button>
                                        <button
                                            onClick={() => downloadReport(incident.id)}
                                            className="px-3 py-1.5 text-sm bg-cyber-blue text-white rounded hover:bg-cyber-blue/90 shadow-lg shadow-cyber-blue/20"
                                        >
                                            Report
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    ))}
                </div>
            )}
        </div>
    )
}

function Badge({ severity }: { severity: string }) {
    const styles: any = {
        critical: 'bg-red-100 dark:bg-red-500/20 text-red-700 dark:text-red-300 border-red-200 dark:border-red-500/50',
        high: 'bg-orange-100 dark:bg-orange-500/20 text-orange-700 dark:text-orange-300 border-orange-200 dark:border-orange-500/50',
        medium: 'bg-yellow-100 dark:bg-yellow-500/20 text-yellow-700 dark:text-yellow-300 border-yellow-200 dark:border-yellow-500/50',
        low: 'bg-green-100 dark:bg-green-500/20 text-green-700 dark:text-green-300 border-green-200 dark:border-green-500/50',
    }
    return (
        <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border ${styles[severity] || styles.low}`}>
            {severity}
        </span>
    )
}

function getSeverityColorHex(severity: string) {
    switch (severity) {
        case 'critical': return '#ef4444'
        case 'high': return '#f97316'
        case 'medium': return '#eab308'
        case 'low': return '#22c55e'
        default: return '#94a3b8'
    }
}
