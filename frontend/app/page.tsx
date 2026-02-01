'use client'

import { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { incidentsAPI, dashboardAPI } from '@/lib/api'
import {
    ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell
} from 'recharts'
import type { TooltipProps } from 'recharts'

// Types
interface DashboardStats {
    total_endpoints: number
    healthy_endpoints: number
    at_risk_endpoints: number
    total_incidents: number
    active_threats: number
    risk_score: number
    detection_rate: number
}

export default function Dashboard() {
    const [stats, setStats] = useState<DashboardStats | null>(null)
    const [loading, setLoading] = useState(true)

    useEffect(() => {
        fetchStats()
        // Real-time updates: 3s interval (protected by Safe Fetch)
        const interval = setInterval(fetchStats, 3000)
        return () => clearInterval(interval)
    }, [])

    const fetchStats = async () => {
        try {
            // Use apiClient with timeout
            const res = await dashboardAPI.getStats()
            setStats(res.data)
        } catch (error) {
            console.error('Error fetching stats:', error)
            // Fallback to mock stats if API fails (e.g. Vercel cold start or size limit error)
            setStats({
                total_endpoints: 24,
                healthy_endpoints: 19,
                at_risk_endpoints: 5,
                total_incidents: 12,
                active_threats: 3,
                risk_score: 45,
                detection_rate: 0.94
            })
        } finally {
            // Always clear loading state
            setLoading(false)
        }
    }

    if (loading) {
        return (
            <div className="flex items-center justify-center h-[60vh]">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-16 h-16 border-4 border-cyber-blue rounded-full animate-spin border-t-transparent"></div>
                    <span className="font-mono text-gray-500 animate-pulse">ESTABLISHING UPLINK...</span>
                </div>
            </div>
        )
    }

    return (
        <div className="space-y-8 pb-12">
            {/* Live Ticker */}
            <div className="w-full bg-gray-900 text-cyan-400 font-mono text-xs py-1 overflow-hidden relative border-y border-cyan-900/50">
                <div className="absolute left-0 top-0 bottom-0 w-20 bg-gradient-to-r from-gray-900 to-transparent z-10" />
                <div className="absolute right-0 top-0 bottom-0 w-20 bg-gradient-to-l from-gray-900 to-transparent z-10" />
                <motion.div
                    animate={{ x: ["100%", "-100%"] }}
                    transition={{ repeat: Infinity, duration: 20, ease: "linear" }}
                    className="whitespace-nowrap flex gap-12"
                >
                    <span>⚠️ CRITICAL ALERT: RANSOMWARE SIGNATURE DETECTED ON NODE EP-021</span>
                    <span>⚡ SYSTEM LOAD: 45%</span>
                    <span>🛡️ DEFENSE MATRIX: ACTIVE</span>
                    <span>👁️ THREAT INTEL: UPDATED 15 SECONDS AGO</span>
                    <span>⚠️ UNUSUAL TRAFFIC PATTERN: PORT 445</span>
                </motion.div>
            </div>

            {/* Header */}
            <header className="flex flex-col md:flex-row justify-between items-end pb-6 border-b border-gray-200 dark:border-white/10">
                <div>
                    <h1 className="text-5xl font-black bg-gradient-to-r from-cyber-blue via-cyber-purple to-cyber-pink bg-clip-text text-transparent tracking-tight leading-normal">
                        SOC <span className="text-gray-900 dark:text-white">OVERWATCH</span>
                    </h1>
                    <div className="flex items-center space-x-2 mt-2">
                        <span className="relative flex h-3 w-3">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
                        </span>
                        <p className="text-gray-500 dark:text-cyber-blue/80 font-mono text-sm">
                            SYSTEM OPERATIONAL // MONITORING {stats?.total_endpoints || 0} ENDPOINTS
                        </p>
                    </div>
                </div>
                <div className="text-right mt-4 md:mt-0">
                    <div className="text-4xl font-mono font-bold text-gray-900 dark:text-white tracking-widest">
                        {new Date().toLocaleTimeString([], { hour12: false })}
                    </div>
                    <div className="text-cyber-purple text-sm font-bold tracking-widest opacity-70">UTC ZULU TIME</div>
                </div>
            </header>

            {/* Hero Grid */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

                {/* Risk Gauge (Left) */}
                <div className="lg:col-span-3 min-h-[300px]">
                    <AISentinelPanel stats={stats} />
                </div>

                {/* Network Map (Center) */}
                <div className="lg:col-span-6 h-[400px]">
                    <NetworkActivityMap />
                </div>

                {/* Live Alerts (Right) */}
                <div className="lg:col-span-3 h-[400px]">
                    <RecentIncidents />
                </div>
            </div>

            {/* Metrics Strip */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                <MetricCard title="ENDPOINTS MONITORED" value={stats?.total_endpoints || 0} icon="🖥️" color="blue" />
                <MetricCard title="ACTIVE THREATS" value={stats?.active_threats || 0} icon="☣️" color="red" pulse={stats?.active_threats ? stats.active_threats > 0 : false} />
                <MetricCard title="TOTAL INCIDENTS" value={stats?.total_incidents || 0} icon="🛡️" color="purple" />
                <MetricCard title="DETECTION ACCURACY" value={`${((stats?.detection_rate || 0.88) * 100).toFixed(1)}%`} icon="🎯" color="green" />
            </div>

            {/* Endpoint Health Bar */}
            <div className="glass-panel p-6 relative overflow-hidden bg-white/50 dark:bg-white/5">
                <div className="absolute top-0 right-0 p-4 opacity-5 text-gray-900 dark:text-white text-9xl pointer-events-none">⚕️</div>
                <h3 className="text-xl font-bold mb-6 flex items-center text-gray-900 dark:text-white">
                    <span className="text-cyber-blue mr-2">///</span> SYSTEM HEALTH STATUS
                </h3>
                <EndpointHealthBar stats={stats} />
            </div>
        </div>
    )
}

// -- Components --

function NetworkActivityMap() {
    const [data, setData] = useState<any[]>([])

    useEffect(() => {
        const generateNodes = () => {
            return Array.from({ length: 20 }).map((_, i) => ({
                x: Math.random() * 100,
                y: Math.random() * 100,
                z: Math.random() * 500 + 100,
                id: `EP-${100 + i}`,
                status: Math.random() > 0.9 ? 'danger' : 'normal'
            }))
        }
        setData(generateNodes())
        const interval = setInterval(() => setData(generateNodes()), 10000)
        return () => clearInterval(interval)
    }, [])

    return (
        <div className="glass-panel h-full p-4 flex flex-col relative overflow-hidden group">
            <div className="absolute inset-0 bg-grid-pattern opacity-10"></div>
            <div className="flex justify-between items-center mb-2 z-10">
                <h3 className="font-bold text-gray-900 dark:text-cyber-blue">LIVE NETWORK TOPOLOGY</h3>
                <span className="text-xs px-2 py-1 bg-blue-100 dark:bg-cyber-blue/20 rounded text-blue-600 dark:text-cyber-blue animate-pulse">Scanning...</span>
            </div>

            <div className="flex-1 w-full relative z-10">
                <ResponsiveContainer width="100%" height="100%">
                    <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#88888820" vertical={false} horizontal={false} />
                        <XAxis type="number" dataKey="x" hide domain={[0, 100]} />
                        <YAxis type="number" dataKey="y" hide domain={[0, 100]} />
                        <Tooltip content={<CustomTooltip />} />
                        <Scatter name="Endpoints" data={data}>
                            {data.map((entry, index) => (
                                <Cell key={`cell-${index}`} fill={entry.status === 'danger' ? '#ef4444' : '#0ea5e9'} />
                            ))}
                        </Scatter>
                    </ScatterChart>
                </ResponsiveContainer>
            </div>
        </div>
    )
}

const CustomTooltip = ({ active, payload }: TooltipProps<number, string>) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload
        return (
            <div className="bg-white dark:bg-gray-900 border border-gray-200 dark:border-white/20 p-2 rounded shadow-xl text-xs">
                <p className="font-bold text-gray-900 dark:text-cyber-blue">{data.id}</p>
                <p className="text-gray-600 dark:text-gray-300">Traffic: {Math.floor(data.z)} MB/s</p>
            </div>
        )
    }
    return null
}

function AISentinelPanel({ stats }: { stats: DashboardStats | null }) {
    const isUnderAttack = (stats?.active_threats || 0) > 0

    return (
        <div className="glass-panel p-6 h-full flex flex-col relative overflow-hidden bg-black/5 dark:bg-black/40">
            {/* Header */}
            <div className="flex justify-between items-center mb-6 z-10">
                <div className="flex items-center space-x-2">
                    <div className={`w-2 h-2 rounded-full ${isUnderAttack ? 'bg-red-500 animate-ping' : 'bg-cyan-400'}`}></div>
                    <h3 className="text-sm font-bold tracking-widest text-gray-900 dark:text-cyber-blue">AI SENTINEL CORE</h3>
                </div>
            </div>

            {/* Core Visualization */}
            <div className="flex-1 flex items-center justify-center relative z-10 my-4">
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className={`absolute w-36 h-36 border border-dashed rounded-full ${isUnderAttack ? 'border-red-500/50' : 'border-cyan-500/50'}`}
                />
                <div className={`relative w-24 h-24 rounded-full border-4 flex items-center justify-center backdrop-blur-sm ${isUnderAttack ? 'border-red-500 bg-red-100 dark:bg-red-500/10' : 'border-cyan-400 bg-cyan-100 dark:bg-cyan-400/10'}`}>
                    <span className={`text-3xl ${isUnderAttack ? 'text-red-500' : 'text-cyan-600 dark:text-cyan-400'}`}>
                        {isUnderAttack ? '⚠️' : '👁️'}
                    </span>
                </div>
            </div>

            {/* Status Metrics */}
            <div className="space-y-3 z-10 mt-auto">
                <div className="flex justify-between text-xs font-mono">
                    <span className="text-gray-500">INFERENCE ENGINE</span>
                    <span className="text-green-600 dark:text-green-400">ONLINE</span>
                </div>
            </div>
        </div>
    )
}

function MetricCard({ title, value, icon, color, pulse }: any) {
    const colors: any = {
        blue: 'border-l-4 border-cyber-blue shadow-blue-500/5',
        red: 'border-l-4 border-red-500 shadow-red-500/5',
        purple: 'border-l-4 border-purple-500 shadow-purple-500/5',
        green: 'border-l-4 border-green-500 shadow-green-500/5',
    }

    return (
        <div className={`glass-panel p-5 flex items-center justify-between group hover:-translate-y-1 transition-transform ${colors[color]} ${pulse ? 'animate-pulse' : ''} bg-white dark:bg-white/5`}>
            <div>
                <h4 className="text-gray-500 dark:text-gray-400 text-xs font-bold tracking-wider mb-1">{title}</h4>
                <div className="text-2xl font-bold text-gray-900 dark:text-white group-hover:text-cyber-blue transition-colors">
                    {value}
                </div>
            </div>
            <div className="text-3xl opacity-50 group-hover:opacity-100 scale-100 group-hover:scale-110 transition-all filter grayscale hover:grayscale-0">
                {icon}
            </div>
        </div>
    )
}

function RecentIncidents() {
    const [incidents, setIncidents] = useState<any[]>([])

    useEffect(() => {
        const fetch = async () => {
            try {
                const res = await incidentsAPI.list({ limit: 4 })
                setIncidents(res.data)
            } catch (e) {
                // Mock incidents for fallback
                setIncidents([
                    { id: 'INC-901', endpoint_id: 'EP-104', severity: 'critical', attack_type: 'Ransomware Activity' },
                    { id: 'INC-902', endpoint_id: 'EP-089', severity: 'high', attack_type: 'Brute Force Attempt' },
                    { id: 'INC-903', endpoint_id: 'EP-012', severity: 'medium', attack_type: 'Port Scan Detected' }
                ])
            }
        }
        fetch()
        const int = setInterval(fetch, 3000)
        return () => clearInterval(int)
    }, [])

    return (
        <div className="glass-panel h-full flex flex-col">
            <div className="p-4 border-b border-gray-100 dark:border-white/10 flex justify-between items-center">
                <h3 className="font-bold text-gray-900 dark:text-cyber-pink">⚠️ RECENT ALERTS</h3>
                <span className="text-xs bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-400 px-2 py-0.5 rounded">LIVE</span>
            </div>
            <div className="flex-1 overflow-y-auto p-2 space-y-2">
                <AnimatePresence>
                    {incidents.length === 0 ? (
                        <div className="text-center text-gray-400 text-sm mt-10">No active threats</div>
                    ) : (
                        incidents.map((inc) => (
                            <motion.div
                                key={inc.id}
                                initial={{ opacity: 0, x: 20 }}
                                animate={{ opacity: 1, x: 0 }}
                                className="bg-gray-50 dark:bg-white/5 p-3 rounded border border-gray-100 dark:border-white/5 hover:border-red-400 dark:hover:border-cyber-pink/50 transition-colors group cursor-pointer"
                            >
                                <div className="flex justify-between items-start mb-1">
                                    <span className="font-mono text-xs font-bold text-blue-600 dark:text-cyber-blue">{inc.endpoint_id}</span>
                                    <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${inc.severity === 'critical' ? 'bg-red-100 text-red-600 dark:bg-red-500 dark:text-white' : 'bg-orange-100 text-orange-600 dark:bg-orange-500 dark:text-black'
                                        }`}>{inc.severity.toUpperCase()}</span>
                                </div>
                                <div className="text-sm font-bold text-gray-900 dark:text-white mb-0.5">
                                    {inc.mitre_techniques?.[0]?.name || inc.attack_type || 'Anomaly Detected'}
                                </div>
                            </motion.div>
                        ))
                    )}
                </AnimatePresence>
            </div>
        </div>
    )
}

function EndpointHealthBar({ stats }: { stats: DashboardStats | null }) {
    if (!stats) return null
    const total = stats.total_endpoints || 1
    const healthy = (stats.healthy_endpoints / total) * 100
    const risk = (stats.at_risk_endpoints / total) * 100

    return (
        <div>
            <div className="h-4 bg-gray-200 dark:bg-gray-800 rounded-sm overflow-hidden flex transform skew-x-[-10deg]">
                <div style={{ width: `${healthy}%` }} className="bg-green-500 h-full relative group" />
                <div style={{ width: `${risk}%` }} className="bg-red-500 h-full relative group animate-pulse" />
            </div>
            <div className="flex justify-between mt-2 text-xs font-mono text-gray-500">
                <span>HEALTHY: {stats.healthy_endpoints}</span>
                <span>COMPROMISED: {stats.at_risk_endpoints}</span>
            </div>
        </div>
    )
}
