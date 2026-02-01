'use client'

import { useEffect, useState, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

interface LogEntry {
    id: string
    timestamp: string
    endpoint_id: string
    hostname: string
    severity: 'info' | 'warning' | 'error' | 'critical'
    message: string
    data?: any
}

export default function LogsPage() {
    const [logs, setLogs] = useState<LogEntry[]>([])
    const [connected, setConnected] = useState(false)
    const [autoScroll, setAutoScroll] = useState(true)
    const logsEndRef = useRef<HTMLDivElement>(null)
    const wsRef = useRef<WebSocket | null>(null)

    useEffect(() => {
        connectWebSocket()
        return () => {
            if (wsRef.current) wsRef.current.close()
        }
    }, [])

    useEffect(() => {
        if (autoScroll && logsEndRef.current) {
            logsEndRef.current.scrollIntoView({ behavior: 'auto', block: 'end' })
        }
    }, [logs, autoScroll])

    const connectWebSocket = () => {
        const ws = new WebSocket('ws://localhost:8000/api/logs/stream')

        ws.onopen = () => {
            console.log('WebSocket connected')
            setConnected(true)
        }

        ws.onmessage = (event) => {
            const log = JSON.parse(event.data)
            setLogs((prev) => [...prev.slice(-200), log]) // Keep last 200 logs
        }

        ws.onclose = () => {
            setConnected(false)
            setTimeout(connectWebSocket, 3000)
        }

        wsRef.current = ws
    }

    return (
        <div className="h-[calc(100vh-100px)] flex flex-col space-y-4">
            {/* Header */}
            <header className="flex justify-between items-center border-b border-white/10 pb-4">
                <div>
                    <h1 className="text-3xl font-black bg-gradient-to-r from-green-400 to-cyber-blue bg-clip-text text-transparent font-mono tracking-tighter">
                        {'>'} LIVE_TELEMETRY_STREAM
                    </h1>
                    <div className="flex items-center space-x-2 mt-1 text-xs font-mono text-gray-400">
                        <span className={connected ? 'text-green-500' : 'text-red-500'}>
                            [{connected ? 'CONNECTED' : 'OFFLINE'}]
                        </span>
                        <span>:: PORT 8000 :: SECURE CHANNEL</span>
                    </div>
                </div>

                <div className="flex space-x-3">
                    <button
                        onClick={() => setAutoScroll(!autoScroll)}
                        className={`px-4 py-2 rounded text-xs font-mono border ${autoScroll
                            ? 'bg-cyber-blue/20 border-cyber-blue text-cyber-blue'
                            : 'bg-white/5 border-white/10 text-gray-400'
                            }`}
                    >
                        {autoScroll ? 'AUTO_SCROLL: ON' : 'AUTO_SCROLL: OFF'}
                    </button>
                    <button
                        onClick={() => setLogs([])}
                        className="px-4 py-2 rounded text-xs font-mono border border-red-500/30 bg-red-500/10 text-red-400 hover:bg-red-500/20"
                    >
                        CLEAR_BUFFER
                    </button>
                </div>
            </header>

            {/* Terminal Window */}
            <div className="flex-1 glass-panel relative overflow-hidden flex flex-col font-mono text-sm bg-[#05070a]">
                {/* CRT Scanline Effect */}
                <div className="absolute inset-0 pointer-events-none bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] z-10 bg-[length:100%_4px,6px_100%] opacity-20"></div>

                {/* Mac OS / Terminal Controls decoration */}
                <div className="h-8 bg-white/5 border-b border-white/10 flex items-center px-4 space-x-2">
                    <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500/50"></div>
                    <div className="ml-4 text-xs text-gray-600">user@soc-console:~/streams/endpoint_logs</div>
                </div>

                {/* Logs Container */}
                <div className="flex-1 overflow-y-auto p-4 space-y-1 scrollbar-hide">
                    {logs.length === 0 ? (
                        <div className="h-full flex items-center justify-center text-gray-600 animate-pulse">
                            WAITING_FOR_DATA_PACKETS...
                        </div>
                    ) : (
                        logs.map((log, index) => (
                            <LogLine key={index} log={log} />
                        ))
                    )}
                    <div ref={logsEndRef} />
                </div>
            </div>

            {/* Footer Stats */}
            <div className="grid grid-cols-4 gap-4 text-xs font-mono text-gray-500">
                <div className="bg-white/5 p-2 rounded border border-white/5">
                    BUFFER_SIZE: {logs.length}/200
                </div>
                <div className="bg-white/5 p-2 rounded border border-white/5">
                    LAST_PACKET: {logs.length > 0 ? new Date(logs[logs.length - 1].timestamp).toLocaleTimeString() : 'N/A'}
                </div>
            </div>
        </div>
    )
}

function LogLine({ log }: { log: LogEntry }) {
    const getSeverityColor = (sev: string) => {
        switch (sev) {
            case 'critical': return 'text-red-500 bg-red-500/10'
            case 'error': return 'text-orange-500 bg-orange-500/10'
            case 'warning': return 'text-yellow-500 bg-yellow-500/10'
            default: return 'text-blue-400'
        }
    }

    return (
        <div className="flex space-x-3 hover:bg-white/5 p-0.5 rounded transition-colors group">
            <span className="text-gray-600 whitespace-nowrap min-w-[80px]">
                {new Date(log.timestamp).toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' })}.{(new Date(log.timestamp).getMilliseconds()).toString().padStart(3, '0')}
            </span>

            <span className={`px-1.5 rounded uppercase text-[10px] font-bold h-fit mt-0.5 ${getSeverityColor(log.severity)}`}>
                {log.severity.substring(0, 4)}
            </span>

            <span className="text-purple-400 font-bold min-w-[80px]">
                {log.endpoint_id}
            </span>

            <div className="flex-1 text-gray-300 flex flex-wrap gap-2">
                <span>{log.message}</span>
                {log.data && (
                    <span className="text-gray-500 text-xs hidden group-hover:inline-flex items-center">
                        {Object.entries(log.data).slice(0, 3).map(([k, v]: any) => (
                            <span key={k} className="mr-2">
                                [{k}:{typeof v === 'number' ? v.toFixed(1) : v}]
                            </span>
                        ))}
                    </span>
                )}
            </div>
        </div>
    )
}
