"use client"

import React, { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import dynamic from 'next/dynamic'

// Dynamically import the download button which contains all the PDF logic
// This ensures that @react-pdf/renderer is never loaded on the server
const PDFDownloadButton = dynamic(() => import('../../components/PDFDownloadButton'), {
    ssr: false,
    loading: () => (
        <button className="flex items-center space-x-2 bg-cyber-blue/10 text-cyber-blue/50 px-4 py-2 rounded-lg border border-cyber-blue/30 cursor-wait">
            <span>Loading PDF Generator...</span>
        </button>
    )
})

export default function DocumentationPage() {
    const [isClient, setIsClient] = useState(false)

    useEffect(() => {
        setIsClient(true)
    }, [])

    return (
        <div className="max-w-4xl mx-auto pb-20 print:p-0 print:max-w-none print:mx-0">
            {/* Header / Actions - Hidden in Print */}
            <div className="flex justify-between items-center mb-8 print:hidden">
                <h1 className="text-3xl font-bold bg-gradient-to-r from-cyber-blue to-cyber-purple bg-clip-text text-transparent">
                    System Documentation
                </h1>

                {isClient && <PDFDownloadButton />}
            </div>

            {/* Content Container */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                className="space-y-8 bg-white dark:bg-gray-900/50 p-8 rounded-xl border border-gray-200 dark:border-white/10 shadow-xl print:shadow-none print:border-none print:p-0 print:bg-white print:text-black"
            >
                {/* Print Only Header */}
                <div className="hidden print:block mb-8 border-b-2 border-gray-300 pb-4">
                    <h1 className="text-4xl font-bold text-gray-900 mb-2">AI SOC Platform</h1>
                    <p className="text-xl text-gray-600">Technical Documentation & System Architecture</p>
                    <p className="text-sm text-gray-500 mt-2">Generated on {new Date().toLocaleDateString()}</p>
                </div>

                {/* 1. Overview */}
                <section>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 border-b border-gray-200 dark:border-white/10 pb-2 print:text-black print:border-gray-300">
                        1. System Overview
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 print:text-gray-800 leading-relaxed">
                        The AI SOC Platform is a production-grade Security Operations Center dashboard driven by advanced machine learning algorithms.
                        It provides real-time threat detection, anomaly scoring, and automated incident response capabilities.
                        Unlike traditional rule-based systems, this platform uses an ensemble of unsupervised detection models to identify novel attacks
                        and behavioral anomalies across simulated endpoint telemetry.
                    </p>
                </section>

                {/* 2. Telemetry & Parameters */}
                <section>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 border-b border-gray-200 dark:border-white/10 pb-2 print:text-black print:border-gray-300">
                        2. Monitoring Parameters
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 print:text-gray-800 mb-4">
                        The system ingests and analyzes 12 distinct telemetry features from every endpoint in real-time.
                        These parameters form the input vector for the ML models.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 print:grid-cols-2">
                        <div className="bg-gray-50 dark:bg-white/5 p-4 rounded-lg border border-gray-200 dark:border-white/5 print:border-gray-300 print:bg-gray-50">
                            <h3 className="font-semibold text-cyber-blue print:text-blue-800 mb-2">System Resources</h3>
                            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400 print:text-gray-800">
                                <li><strong>cpu_usage:</strong> Percentage of CPU utilization</li>
                                <li><strong>memory_usage:</strong> Percentage of RAM utilization</li>
                                <li><strong>disk_read:</strong> Bytes read from disk</li>
                                <li><strong>disk_write:</strong> Bytes written to disk</li>
                            </ul>
                        </div>
                        <div className="bg-gray-50 dark:bg-white/5 p-4 rounded-lg border border-gray-200 dark:border-white/5 print:border-gray-300 print:bg-gray-50">
                            <h3 className="font-semibold text-cyber-purple print:text-purple-800 mb-2">Network Activity</h3>
                            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400 print:text-gray-800">
                                <li><strong>network_in:</strong> Incoming traffic usage</li>
                                <li><strong>network_out:</strong> Outgoing traffic usage</li>
                                <li><strong>dns_queries:</strong> Frequency of DNS requests</li>
                                <li><strong>api_calls:</strong> Rate of internal/external API calls</li>
                            </ul>
                        </div>
                        <div className="bg-gray-50 dark:bg-white/5 p-4 rounded-lg border border-gray-200 dark:border-white/5 print:border-gray-300 print:bg-gray-50">
                            <h3 className="font-semibold text-red-500 print:text-red-800 mb-2">Security Events</h3>
                            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600 dark:text-gray-400 print:text-gray-800">
                                <li><strong>failed_logins:</strong> Count of failed authentication attempts</li>
                                <li><strong>auth_attempts:</strong> Total authentication attempts</li>
                                <li><strong>process_creation:</strong> Rate of new process spawning</li>
                                <li><strong>file_access:</strong> Rate of sensitive file access operations</li>
                            </ul>
                        </div>
                    </div>
                </section>

                {/* 3. Detection Architecture */}
                <section>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 border-b border-gray-200 dark:border-white/10 pb-2 print:text-black print:border-gray-300">
                        3. Detection Logic & Architecture
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 print:text-gray-800 mb-4">
                        The platform employs an <strong>Ensemble Detection Engine</strong> that combines four distinct algorithms to minimize false positives and maximize detection of subtle anomalies.
                    </p>

                    <div className="space-y-4">
                        <div className="border-l-4 border-cyber-blue pl-4 py-1 print:border-blue-600">
                            <h4 className="font-bold text-gray-900 dark:text-white print:text-black">Deep Autoencoder</h4>
                            <p className="text-sm text-gray-500 dark:text-gray-400 print:text-gray-700">Reconstruction-based detection. Learns the pattern of "normal" traffic and flags data that cannot be accurately reconstructed (high reconstruction error).</p>
                        </div>
                        <div className="border-l-4 border-cyber-purple pl-4 py-1 print:border-purple-600">
                            <h4 className="font-bold text-gray-900 dark:text-white print:text-black">Isolation Forest</h4>
                            <p className="text-sm text-gray-500 dark:text-gray-400 print:text-gray-700">Tree-based outlier detection. Efficiently isolates anomalies by randomly partitioning the dataset.</p>
                        </div>
                        <div className="border-l-4 border-emerald-500 pl-4 py-1 print:border-emerald-600">
                            <h4 className="font-bold text-gray-900 dark:text-white print:text-black">Local Outlier Factor (LOF)</h4>
                            <p className="text-sm text-gray-500 dark:text-gray-400 print:text-gray-700">Density-based detection. Identifies points that have a significantly lower density than their neighbors.</p>
                        </div>
                        <div className="border-l-4 border-amber-500 pl-4 py-1 print:border-amber-600">
                            <h4 className="font-bold text-gray-900 dark:text-white print:text-black">LSTM (Long Short-Term Memory)</h4>
                            <p className="text-sm text-gray-500 dark:text-gray-400 print:text-gray-700">Sequence-based detection. Analyzes temporal patterns over time to detect sequence anomalies.</p>
                        </div>
                    </div>
                </section>

                {/* 4. Incident Classification */}
                <section className="break-inside-avoid">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 border-b border-gray-200 dark:border-white/10 pb-2 print:text-black print:border-gray-300">
                        4. Incident Severity Classification
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 print:text-gray-800 mb-6">
                        The system calculates a unified <strong>Ensemble Score</strong> (0.0 to 1.0) by aggregating the outputs of all models.
                        This score represents the probability that the observed behavior is malicious. Incidents are classified based on this score:
                    </p>

                    <div className="overflow-hidden rounded-lg border border-gray-200 dark:border-white/10 print:border-gray-300">
                        <table className="min-w-full divide-y divide-gray-200 dark:divide-white/10">
                            <thead className="bg-gray-50 dark:bg-white/5 print:bg-gray-100">
                                <tr>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider print:text-black">Severity Level</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider print:text-black">Ensemble Score Range</th>
                                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider print:text-black">Description</th>
                                </tr>
                            </thead>
                            <tbody className="bg-white dark:bg-gray-900 divide-y divide-gray-200 dark:divide-white/10 print:bg-white print:divide-gray-300">
                                <tr>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-red-100 text-red-800 print:border print:border-red-200">
                                            CRITICAL
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        &ge; 0.80 (80%)
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        Highest certainty of malicious activity. Immediate action required.
                                    </td>
                                </tr>
                                <tr>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-orange-100 text-orange-800 print:border print:border-orange-200">
                                            HIGH
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        0.70 - 0.79
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        Strong indicators of attack. Priority investigation needed.
                                    </td>
                                </tr>
                                <tr>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-yellow-100 text-yellow-800 print:border print:border-yellow-200">
                                            MEDIUM
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        0.55 - 0.69
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        Suspicious behavior detected. Should be reviewed.
                                    </td>
                                </tr>
                                <tr>
                                    <td className="px-6 py-4 whitespace-nowrap">
                                        <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800 print:border print:border-blue-200">
                                            LOW / INFO
                                        </span>
                                    </td>
                                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        &lt; 0.55
                                    </td>
                                    <td className="px-6 py-4 text-sm text-gray-500 dark:text-gray-300 print:text-black">
                                        Events logged for auditing. Low probability.
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </section>

                {/* 5. MITRE Mapping */}
                <section className="break-inside-avoid">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4 border-b border-gray-200 dark:border-white/10 pb-2 print:text-black print:border-gray-300">
                        5. MITRE ATT&CK Support
                    </h2>
                    <p className="text-gray-600 dark:text-gray-300 print:text-gray-800 mb-4">
                        Detected anomalies are automatically mapped to known adversary tactics and techniques using feature contribution analysis.
                    </p>
                    <ul className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-600 dark:text-gray-400 print:text-gray-800 print:grid-cols-2">
                        <li className="flex items-center space-x-2">
                            <span className="font-mono bg-gray-100 dark:bg-white/10 px-1 rounded text-red-500 font-bold">T1110</span>
                            <span>Brute Force (Credential Access)</span>
                        </li>
                        <li className="flex items-center space-x-2">
                            <span className="font-mono bg-gray-100 dark:bg-white/10 px-1 rounded text-red-500 font-bold">T1496</span>
                            <span>Resource Hijacking (Crypto Mining)</span>
                        </li>
                        <li className="flex items-center space-x-2">
                            <span className="font-mono bg-gray-100 dark:bg-white/10 px-1 rounded text-red-500 font-bold">T1048</span>
                            <span>Data Exfiltration (Exfiltration)</span>
                        </li>
                        <li className="flex items-center space-x-2">
                            <span className="font-mono bg-gray-100 dark:bg-white/10 px-1 rounded text-red-500 font-bold">T1068</span>
                            <span>Privilege Escalation</span>
                        </li>
                        <li className="flex items-center space-x-2">
                            <span className="font-mono bg-gray-100 dark:bg-white/10 px-1 rounded text-red-500 font-bold">T1071</span>
                            <span>Command & Control (C2 Activity)</span>
                        </li>
                        <li className="flex items-center space-x-2">
                            <span className="font-mono bg-gray-100 dark:bg-white/10 px-1 rounded text-red-500 font-bold">T1021</span>
                            <span>Lateral Movement (Remote Services)</span>
                        </li>
                        <li className="flex items-center space-x-2">
                            <span className="font-mono bg-gray-100 dark:bg-white/10 px-1 rounded text-red-500 font-bold">T1190</span>
                            <span>Exploit Public-Facing Application</span>
                        </li>
                    </ul>
                </section>

                <div className="hidden print:block text-center text-xs text-gray-400 mt-12 pt-4 border-t border-gray-300">
                    <p>&copy; {new Date().getFullYear()} AI SOC Platform. Confidential Internal Documentation.</p>
                </div>
            </motion.div>
        </div>
    )
}
