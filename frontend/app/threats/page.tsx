'use client'

import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { threatsAPI } from '@/lib/api'

export default function ThreatsPage() {
    const [endpoints, setEndpoints] = useState<any[]>([])
    const [selectedEndpoint, setSelectedEndpoint] = useState<string>('')
    const [analysis, setAnalysis] = useState<any>(null)
    const [loading, setLoading] = useState(false)

    useEffect(() => {
        fetchEndpoints()
    }, [])

    const fetchEndpoints = async () => {
        try {
            const response = await threatsAPI.listEndpoints()
            setEndpoints(response.data.endpoints || [])
            /* Don't auto-select, let user choose */
        } catch (error) {
            console.error('Error:', error)
        }
    }

    const analyzeEndpoint = async (id: string) => {
        setSelectedEndpoint(id)
        setLoading(true)
        setAnalysis(null)
        try {
            const response = await threatsAPI.analyzeEndpoint(id)
            setAnalysis(response.data)
        } catch (error) {
            console.error('Error:', error)
        }
        setLoading(false)
    }

    return (
        <div className="space-y-8 pb-12">
            <div className="text-center space-y-2">
                <h1 className="text-4xl text-gray-900 dark:text-white font-black tracking-tight">
                    THREAT <span className="text-cyber-blue">ANALYZER</span>
                </h1>
                <p className="text-gray-500 dark:text-gray-400 max-w-2xl mx-auto">
                    Select an endpoint node to initiate deep generative analysis and MITRE mapping.
                </p>
            </div>

            {/* Endpoint Grid Selector */}
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
                {endpoints.map((ep) => (
                    <motion.button
                        key={ep.id}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => analyzeEndpoint(ep.id)}
                        className={`p-4 rounded-xl border transition-all relative overflow-hidden group ${selectedEndpoint === ep.id
                            ? 'bg-cyber-blue/10 border-cyber-blue ring-2 ring-cyber-blue/50'
                            : 'bg-white dark:bg-white/5 border-gray-200 dark:border-white/10 hover:border-cyber-blue/50'
                            }`}
                    >
                        {/* Status Dot */}
                        <div className={`absolute top-3 right-3 w-2 h-2 rounded-full ${ep.status === 'compromised' ? 'bg-red-500 animate-ping' : 'bg-green-500'
                            }`} />

                        <div className="text-3xl mb-2">🖥️</div>
                        <div className="font-mono font-bold text-sm text-gray-900 dark:text-white">{ep.hostname}</div>
                        <div className="text-xs text-gray-500 dark:text-gray-400 font-mono">{ep.id}</div>

                        {/* Hover Effect */}
                        <div className="absolute inset-0 bg-cyber-blue/5 opacity-0 group-hover:opacity-100 transition-opacity" />
                    </motion.button>
                ))}
            </div>

            {/* Analysis Loading State */}
            {loading && (
                <div className="glass-panel p-12 flex flex-col items-center justify-center space-y-4">
                    <div className="w-16 h-16 border-4 border-cyber-blue border-t-transparent rounded-full animate-spin"></div>
                    <div className="font-mono text-cyber-blue animate-pulse">RUNNING HEURISTIC ANALYSIS...</div>
                </div>
            )}

            {/* Analysis Results */}
            <AnimatePresence>
                {analysis && !loading && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-6"
                    >
                        {/* Header Box */}
                        <div className={`glass-panel p-6 border-l-4 ${analysis.anomaly_score.is_anomaly
                                ? 'border-l-red-500'
                                : analysis.anomaly_score.ensemble_score > 0.35
                                    ? 'border-l-orange-500'
                                    : 'border-l-green-500'
                            } flex justify-between items-center`}>
                            <div>
                                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Analysis Report: {selectedEndpoint}</h2>
                                <p className="text-gray-500 dark:text-gray-400">
                                    Confidence: <span className="font-mono font-bold text-cyber-blue">{(analysis.anomaly_score.confidence * 100).toFixed(1)}%</span>
                                </p>
                            </div>
                            <div className={`px-4 py-2 rounded-lg font-bold text-xl ${analysis.anomaly_score.is_anomaly
                                    ? 'bg-red-100 text-red-600 dark:bg-red-500/20 dark:text-red-400'
                                    : analysis.anomaly_score.ensemble_score > 0.35
                                        ? 'bg-orange-100 text-orange-600 dark:bg-orange-500/20 dark:text-orange-400'
                                        : 'bg-green-100 text-green-600 dark:bg-green-500/20 dark:text-green-400'
                                }`}>
                                {analysis.anomaly_score.is_anomaly
                                    ? 'THREAT DETECTED'
                                    : analysis.anomaly_score.ensemble_score > 0.35
                                        ? 'SUSPICIOUS ACTIVITY'
                                        : 'CLEAN'}
                            </div>
                        </div>

                        {/* Scores Grid */}
                        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
                            <ScoreCard title="Autoencoder" score={analysis.anomaly_score.autoencoder_score} />
                            <ScoreCard title="Isolation Forest" score={analysis.anomaly_score.isolation_forest_score} />
                            <ScoreCard title="LOF" score={analysis.anomaly_score.lof_score} />
                            {analysis.anomaly_score.lstm_score && (
                                <ScoreCard title="LSTM" score={analysis.anomaly_score.lstm_score} />
                            )}
                            <ScoreCard title="Ensemble" score={analysis.anomaly_score.ensemble_score} highlight />
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            {/* Feature Contributions */}
                            <div className="glass-panel p-6">
                                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                                    <span>📊</span> Feature Impact
                                </h3>
                                <div className="space-y-3">
                                    {analysis.feature_contributions.slice(0, 5).map((contrib: any) => (
                                        <div key={contrib.feature} className="space-y-1">
                                            <div className="flex justify-between text-xs font-mono">
                                                <span className="text-gray-600 dark:text-gray-400">{contrib.feature.toUpperCase()}</span>
                                                <span className="text-gray-900 dark:text-white font-bold">{contrib.value.toFixed(2)}</span>
                                            </div>
                                            <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                                                <motion.div
                                                    initial={{ width: 0 }}
                                                    animate={{ width: `${Math.min(contrib.contribution_percent, 100)}%` }}
                                                    className="h-full bg-cyber-blue"
                                                />
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>

                            {/* MITRE Mapping */}
                            <div className="glass-panel p-6">
                                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                                    <span>🎯</span> MITRE ATT&CK Mapping
                                </h3>
                                <div className="space-y-3">
                                    {analysis.mitre_techniques && analysis.mitre_techniques.length > 0 ? (
                                        analysis.mitre_techniques.map((tech: any) => (
                                            <div key={tech.technique_id} className="p-3 bg-red-50 dark:bg-red-500/10 border border-red-100 dark:border-red-500/20 rounded-lg">
                                                <div className="flex justify-between items-center mb-1">
                                                    <span className="font-mono font-bold text-red-600 dark:text-red-400">{tech.technique_id}</span>
                                                    <span className="text-xs text-red-500">{(tech.confidence * 100).toFixed(0)}% Match</span>
                                                </div>
                                                <div className="font-bold text-gray-900 dark:text-white text-sm">{tech.name}</div>
                                                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">{tech.tactic}</div>
                                            </div>
                                        ))
                                    ) : (
                                        <div className="text-center py-8 text-gray-400">
                                            No explicit MITRE techniques mapped.
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* Explanation */}
                        <div className="glass-panel p-6 bg-blue-50/50 dark:bg-blue-900/10 border-blue-100 dark:border-blue-500/20">
                            <h3 className="font-bold text-blue-900 dark:text-blue-200 mb-2">🤖 AI Analysis</h3>
                            <p className="text-blue-800 dark:text-blue-100 leading-relaxed">
                                {analysis.explanation}
                            </p>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    )
}

function ScoreCard({ title, score, highlight }: any) {
    return (
        <div className={`p-4 rounded-xl border transition-all ${highlight
            ? 'bg-cyber-blue/10 border-cyber-blue shadow-lg shadow-cyber-blue/10'
            : 'bg-white dark:bg-white/5 border-gray-200 dark:border-white/10'
            }`}>
            <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">{title}</div>
            <div className="text-xl font-black text-gray-900 dark:text-white">{score.toFixed(3)}</div>
            <div className="mt-2 h-1.5 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                <div
                    className={`h-full rounded-full ${score > 0.7 ? 'bg-red-500' : score > 0.4 ? 'bg-yellow-500' : 'bg-green-500'}`}
                    style={{ width: `${score * 100}%` }}
                />
            </div>
        </div>
    )
}
