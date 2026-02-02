/* eslint-disable jsx-a11y/alt-text */
"use client"

import React from 'react'
import { Page, Text, View, Document, StyleSheet, Font, Image } from '@react-pdf/renderer'

// Register Fonts (using standard fonts for reliability, could import others if files existed)
// We'll use Helvetica as base, and Times-Roman for a more formal alternate if needed.
// For a "better font", we rely on clean typography hierarchies.

const styles = StyleSheet.create({
    page: {
        flexDirection: 'column',
        backgroundColor: '#FFFFFF',
        padding: 40,
        fontFamily: 'Helvetica',
    },
    // Cover Page
    coverPage: {
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        height: '100%',
        padding: 20,
    },
    coverTitle: {
        fontSize: 32,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 20,
        color: '#1a365d', // Dark blue
    },
    coverSubtitle: {
        fontSize: 18,
        color: '#4a5568',
        marginBottom: 40,
        textAlign: 'center',
    },
    coverDate: {
        fontSize: 12,
        color: '#718096',
        marginTop: 100,
    },
    // Content Pages
    header: {
        fontSize: 10,
        color: '#a0aec0',
        marginBottom: 20,
        textAlign: 'right',
        borderBottomWidth: 1,
        borderBottomColor: '#e2e8f0',
        paddingBottom: 5,
    },
    sectionTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        marginTop: 25,
        marginBottom: 10,
        color: '#2d3748',
        borderBottomWidth: 1,
        borderBottomColor: '#cbd5e0',
        paddingBottom: 5,
    },
    subSectionTitle: {
        fontSize: 14,
        fontWeight: 'bold',
        marginTop: 15,
        marginBottom: 8,
        color: '#4a5568',
    },
    text: {
        fontSize: 11,
        marginBottom: 8,
        lineHeight: 1.5,
        color: '#2d3748',
        textAlign: 'justify',
    },
    listItem: {
        flexDirection: 'row',
        marginBottom: 4,
    },
    bulletPoint: {
        width: 10,
        fontSize: 11,
        color: '#2d3748',
    },
    listItemContent: {
        flex: 1,
        fontSize: 11,
        lineHeight: 1.5,
        color: '#2d3748',
    },
    tableContainer: {
        marginTop: 15,
        borderWidth: 1,
        borderColor: '#e2e8f0',
    },
    tableHeaderRow: {
        flexDirection: 'row',
        backgroundColor: '#f7fafc',
        borderBottomWidth: 1,
        borderBottomColor: '#e2e8f0',
        padding: 8,
    },
    tableRow: {
        flexDirection: 'row',
        borderBottomWidth: 1,
        borderBottomColor: '#e2e8f0',
        padding: 8,
    },
    tableHeaderCell: {
        flex: 1,
        fontSize: 10,
        fontWeight: 'bold',
        color: '#4a5568',
    },
    tableCell: {
        flex: 1,
        fontSize: 10,
        color: '#2d3748',
    },
    severityCritical: { color: '#e53e3e', fontWeight: 'bold' },
    severityHigh: { color: '#dd6b20', fontWeight: 'bold' },
    severityMedium: { color: '#d69e2e', fontWeight: 'bold' },
    severityLow: { color: '#3182ce', fontWeight: 'bold' },
    footer: {
        position: 'absolute',
        bottom: 30,
        left: 40,
        right: 40,
        fontSize: 9,
        color: '#a0aec0',
        textAlign: 'center',
        borderTopWidth: 1,
        borderTopColor: '#e2e8f0',
        paddingTop: 10,
    },
});

const DocumentationDoc = () => (
    <Document>
        {/* Cover Page */}
        <Page size="A4" style={styles.page}>
            <View style={styles.coverPage}>
                <Text style={styles.coverTitle}>AI SOC Platform</Text>
                <Text style={styles.coverSubtitle}>Technical Documentation & Architecture Reference</Text>
                <Text style={{ marginTop: 20, fontSize: 14, color: '#2b6cb0' }}>Version 1.0.0</Text>
                <Text style={styles.coverDate}>Generated on {new Date().toLocaleDateString()}</Text>
            </View>
        </Page>

        {/* Content Page 1 */}
        <Page size="A4" style={styles.page}>
            <Text style={styles.header}>AI SOC Platform - System Documentation</Text>

            <Text style={styles.sectionTitle}>1. System Overview</Text>
            <Text style={styles.text}>
                The AI SOC Platform is a production-grade Security Operations Center dashboard driven by advanced machine learning algorithms.
                It provides real-time threat detection, anomaly scoring, and automated incident response capabilities.
                Unlike traditional rule-based systems, this platform uses an ensemble of unsupervised detection models to identify novel attacks
                and behavioral anomalies across simulated endpoint telemetry.
            </Text>

            <Text style={styles.sectionTitle}>2. Monitoring Parameters</Text>
            <Text style={styles.text}>
                The system ingests and analyzes 12 distinct telemetry features from every endpoint in real-time.
                These parameters form the input vector for the ML models.
            </Text>

            <View style={{ marginTop: 10 }}>
                <Text style={styles.subSectionTitle}>System Resources</Text>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>cpu_usage: Percentage of CPU utilization</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>memory_usage: Percentage of RAM utilization</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>disk_read: Bytes read from disk</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>disk_write: Bytes written to disk</Text></View>

                <Text style={styles.subSectionTitle}>Network Activity</Text>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>network_in: Incoming traffic usage</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>network_out: Outgoing traffic usage</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>dns_queries: Frequency of DNS requests</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>api_calls: Rate of internal/external API calls</Text></View>

                <Text style={styles.subSectionTitle}>Security Events</Text>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>failed_logins: Count of failed authentication attempts</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>auth_attempts: Total authentication attempts</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>process_creation: Rate of new process spawning</Text></View>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={styles.listItemContent}>file_access: Rate of sensitive file access operations</Text></View>
            </View>

            <Text style={styles.footer}>Confidential - Internal Use Only</Text>
        </Page>

        {/* Content Page 2 */}
        <Page size="A4" style={styles.page}>
            <Text style={styles.header}>AI SOC Platform - System Documentation</Text>

            <Text style={styles.sectionTitle}>3. Detection Logic & Architecture</Text>
            <Text style={styles.text}>
                The platform employs an Ensemble Detection Engine that combines four distinct algorithms to minimize false positives
                and maximize detection of subtle anomalies.
            </Text>

            <View style={{ marginTop: 10 }}>
                <Text style={{ fontSize: 12, fontWeight: 'bold', marginBottom: 4 }}>Deep Autoencoder</Text>
                <Text style={styles.text}>Reconstruction-based detection. Learns the pattern of "normal" traffic and flags data that cannot be accurately reconstructed (high reconstruction error).</Text>

                <Text style={{ fontSize: 12, fontWeight: 'bold', marginBottom: 4, marginTop: 8 }}>Isolation Forest</Text>
                <Text style={styles.text}>Tree-based outlier detection. Efficiently isolates anomalies by randomly partitioning the dataset.</Text>

                <Text style={{ fontSize: 12, fontWeight: 'bold', marginBottom: 4, marginTop: 8 }}>Local Outlier Factor (LOF)</Text>
                <Text style={styles.text}>Density-based detection. Identifies points that have a significantly lower density than their neighbors.</Text>

                <Text style={{ fontSize: 12, fontWeight: 'bold', marginBottom: 4, marginTop: 8 }}>LSTM (Long Short-Term Memory)</Text>
                <Text style={styles.text}>Sequence-based detection. Analyzes temporal patterns over time to detect sequence anomalies.</Text>
            </View>

            <Text style={styles.sectionTitle}>4. Incident Severity Classification</Text>
            <Text style={styles.text}>
                Incidents are classified based on the Ensemble Score (0.0 to 1.0), representing the probability of malicious activity.
            </Text>

            <View style={styles.tableContainer}>
                <View style={styles.tableHeaderRow}>
                    <Text style={styles.tableHeaderCell}>Severity</Text>
                    <Text style={styles.tableHeaderCell}>Score Range</Text>
                    <Text style={[styles.tableHeaderCell, { flex: 2 }]}>Description</Text>
                </View>
                <View style={styles.tableRow}>
                    <Text style={[styles.tableCell, styles.severityCritical]}>CRITICAL</Text>
                    <Text style={styles.tableCell}>≥ 0.80</Text>
                    <Text style={[styles.tableCell, { flex: 2 }]}>Highest certainty. Immediate action required.</Text>
                </View>
                <View style={styles.tableRow}>
                    <Text style={[styles.tableCell, styles.severityHigh]}>HIGH</Text>
                    <Text style={styles.tableCell}>0.70 - 0.79</Text>
                    <Text style={[styles.tableCell, { flex: 2 }]}>Strong indicators of attack. Priority investigation needed.</Text>
                </View>
                <View style={styles.tableRow}>
                    <Text style={[styles.tableCell, styles.severityMedium]}>MEDIUM</Text>
                    <Text style={styles.tableCell}>0.55 - 0.69</Text>
                    <Text style={[styles.tableCell, { flex: 2 }]}>Suspicious behavior detected. Should be reviewed.</Text>
                </View>
                <View style={styles.tableRow}>
                    <Text style={[styles.tableCell, styles.severityLow]}>LOW</Text>
                    <Text style={styles.tableCell}>&lt; 0.55</Text>
                    <Text style={[styles.tableCell, { flex: 2 }]}>Events logged for auditing. Low probability.</Text>
                </View>
            </View>

            <Text style={styles.footer}>Confidential - Internal Use Only</Text>
        </Page>

        {/* Content Page 3 - MITRE */}
        <Page size="A4" style={styles.page}>
            <Text style={styles.header}>AI SOC Platform - System Documentation</Text>

            <Text style={styles.sectionTitle}>5. MITRE ATT&CK Mapping</Text>
            <Text style={styles.text}>
                Detected anomalies are automatically mapped to known adversary tactics and techniques using feature contribution analysis.
            </Text>

            <View style={{ marginTop: 10 }}>
                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={[styles.listItemContent, { fontWeight: 'bold' }]}>T1110 - Brute Force</Text></View>
                <Text style={[{ marginLeft: 15, marginBottom: 8, fontSize: 10, color: '#4a5568' }]}>Credential Access: Attempting to access accounts.</Text>

                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={[styles.listItemContent, { fontWeight: 'bold' }]}>T1496 - Resource Hijacking</Text></View>
                <Text style={[{ marginLeft: 15, marginBottom: 8, fontSize: 10, color: '#4a5568' }]}>Impact: Crypto mining activity.</Text>

                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={[styles.listItemContent, { fontWeight: 'bold' }]}>T1048 - Data Exfiltration</Text></View>
                <Text style={[{ marginLeft: 15, marginBottom: 8, fontSize: 10, color: '#4a5568' }]}>Exfiltration: Sending data over alternative protocols.</Text>

                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={[styles.listItemContent, { fontWeight: 'bold' }]}>T1068 - Privilege Escalation</Text></View>
                <Text style={[{ marginLeft: 15, marginBottom: 8, fontSize: 10, color: '#4a5568' }]}>Privilege Escalation: Exploiting software vulnerabilities.</Text>

                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={[styles.listItemContent, { fontWeight: 'bold' }]}>T1071 - Command & Control</Text></View>
                <Text style={[{ marginLeft: 15, marginBottom: 8, fontSize: 10, color: '#4a5568' }]}>Command and Control: Communication using app layer protocols.</Text>

                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={[styles.listItemContent, { fontWeight: 'bold' }]}>T1021 - Lateral Movement</Text></View>
                <Text style={[{ marginLeft: 15, marginBottom: 8, fontSize: 10, color: '#4a5568' }]}>Lateral Movement: Remote services access.</Text>

                <View style={styles.listItem}><Text style={styles.bulletPoint}>•</Text><Text style={[styles.listItemContent, { fontWeight: 'bold' }]}>T1190 - Exploit Public Application</Text></View>
                <Text style={[{ marginLeft: 15, marginBottom: 8, fontSize: 10, color: '#4a5568' }]}>Initial Access: Exploiting weaknesses in internet-facing apps.</Text>
            </View>

            <Text style={styles.footer}>Confidential - Internal Use Only</Text>
        </Page>
    </Document>
)

export default DocumentationDoc
