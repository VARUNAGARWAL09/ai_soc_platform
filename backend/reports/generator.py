"""
PDF Incident Report Generator
Generates professional incident reports
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, Image
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import os
import sys
from typing import Dict, List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings
from models import Incident, MITRETechnique, FeatureContribution


class PDFReportGenerator:
    """Generate professional PDF incident reports"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._create_custom_styles()
    
    def _create_custom_styles(self):
        """Create custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))
        
        # Section header
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#16213e'),
            spaceBefore=20,
            spaceAfter=12,
            borderWidth=1,
            borderColor=colors.HexColor('#e94560'),
            borderPadding=5
        ))
        
        # Alert style
        self.styles.add(ParagraphStyle(
            name='Alert',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#e94560'),
            leftIndent=20
        ))
    
    def generate_report(self, incident: Incident, output_path: str = None) -> str:
        """
        Generate complete incident report
        
        Args:
            incident: Incident object
            output_path: Output file path (auto-generated if None)
            
        Returns:
            Path to generated PDF
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"incident_{incident.id}_{timestamp}.pdf"
            output_path = os.path.join(settings.REPORT_DIR, filename)
        
        # Create PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build content
        story = []
        
        # Title page
        story.extend(self._create_title_page(incident))
        
        # Executive summary
        story.extend(self._create_executive_summary(incident))
        
        # Incident details
        story.extend(self._create_incident_details(incident))
        
        # MITRE ATT&CK mapping
        story.extend(self._create_mitre_section(incident))
        
        # Feature analysis
        story.extend(self._create_feature_analysis(incident))
        
        # AI explanation
        story.extend(self._create_ai_explanation(incident))
        
        # Recommendations
        story.extend(self._create_recommendations(incident))
        
        # Build PDF
        doc.build(story)
        
        return output_path
    
    def _create_title_page(self, incident: Incident) -> List:
        """Create title page"""
        elements = []
        
        # Title
        title = Paragraph(
            "SECURITY INCIDENT REPORT",
            self.styles['CustomTitle']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Incident ID and classification
        severity_color = self._get_severity_color(incident.severity)
        
        info_data = [
            ['Incident ID:', incident.id],
            ['Severity:', incident.severity.upper()],
            ['Status:', incident.status.upper()],
            ['Detection Time:', incident.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC")],
            ['Endpoint:', incident.endpoint_id],
            ['Attack Type:', incident.attack_type or "Unknown"],
        ]
        
        info_table = Table(info_data, colWidths=[2.5*inch, 3.5*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#f0f0f0')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1a1a2e')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('BACKGROUND', (1, 1), (1, 1), severity_color),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(info_table)
        elements.append(Spacer(1, 0.5 * inch))
        
        # Generated timestamp
        gen_time = Paragraph(
            f"<para align=center><i>Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</i></para>",
            self.styles['Normal']
        )
        elements.append(gen_time)
        
        elements.append(PageBreak())
        
        return elements
    
    def _create_executive_summary(self, incident: Incident) -> List:
        """Create executive summary"""
        elements = []
        
        header = Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeader'])
        elements.append(header)
        
        summary_text = f"""
        A security incident was detected on endpoint <b>{incident.endpoint_id}</b> at 
        {incident.timestamp.strftime('%Y-%m-%d %H:%M:%S UTC')}. The anomaly detection system 
        identified suspicious behavior with an ensemble confidence of 
        <b>{incident.anomaly_scores.confidence:.1%}</b>.
        <br/><br/>
        The system detected <b>{len(incident.mitre_techniques)}</b> MITRE ATT&CK technique(s) 
        associated with this incident, with the primary technique being 
        <b>{incident.mitre_techniques[0].name if incident.mitre_techniques else 'Unknown'}</b>.
        <br/><br/>
        Current Status: <b>{incident.status.upper()}</b><br/>
        Severity Classification: <b>{incident.severity.upper()}</b>
        """
        
        summary = Paragraph(summary_text, self.styles['Normal'])
        elements.append(summary)
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _create_incident_details(self, incident: Incident) -> List:
        """Create incident details section"""
        elements = []
        
        header = Paragraph("INCIDENT DETAILS", self.styles['SectionHeader'])
        elements.append(header)
        
        # ML Model Scores
        score_data = [
            ['Model', 'Anomaly Score'],
            ['Autoencoder', f"{incident.anomaly_scores.autoencoder_score:.3f}"],
            ['Isolation Forest', f"{incident.anomaly_scores.isolation_forest_score:.3f}"],
            ['LOF', f"{incident.anomaly_scores.lof_score:.3f}"],
        ]
        
        if incident.anomaly_scores.lstm_score is not None:
            score_data.append(['LSTM', f"{incident.anomaly_scores.lstm_score:.3f}"])
        
        score_data.append(['', ''])
        score_data.append(['Ensemble', f"{incident.anomaly_scores.ensemble_score:.3f}"])
        score_data.append(['Confidence', f"{incident.anomaly_scores.confidence:.1%}"])
        
        score_table = Table(score_data, colWidths=[3*inch, 2*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, -2), (-1, -1), colors.HexColor('#f0f0f0')),
            ('FONTNAME', (0, -2), (-1, -1), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(score_table)
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _create_mitre_section(self, incident: Incident) -> List:
        """Create MITRE ATT&CK mapping section"""
        elements = []
        
        header = Paragraph("MITRE ATT&CK TECHNIQUES", self.styles['SectionHeader'])
        elements.append(header)
        
        if not incident.mitre_techniques:
            elements.append(Paragraph("No MITRE techniques mapped.", self.styles['Normal']))
            return elements
        
        for technique in incident.mitre_techniques:
            # Technique header
            tech_title = f"<b>{technique.technique_id}: {technique.name}</b>"
            elements.append(Paragraph(tech_title, self.styles['Heading3']))
            
            # Details
            details = f"""
            <b>Tactic:</b> {technique.tactic}<br/>
            <b>Confidence:</b> {technique.confidence:.1%}<br/>
            <b>Matched Features:</b> {', '.join(technique.matched_features)}<br/>
            <b>Description:</b> {technique.description}
            """
            elements.append(Paragraph(details, self.styles['Normal']))
            elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_feature_analysis(self, incident: Incident) -> List:
        """Create feature analysis section"""
        elements = []
        
        header = Paragraph("FEATURE ANALYSIS", self.styles['SectionHeader'])
        elements.append(header)
        
        # Top features table
        feat_data = [['Feature', 'Value', 'Baseline', 'Deviation', 'Contribution']]
        
        for contrib in incident.feature_contributions[:7]:
            feat_data.append([
                contrib.feature.replace('_', ' ').title(),
                f"{contrib.value:.2f}",
                f"{contrib.baseline_mean:.2f}",
                f"{contrib.deviation_multiplier:.2f}x",
                f"{contrib.contribution_percent:.1f}%"
            ])
        
        feat_table = Table(feat_data, colWidths=[1.7*inch, 1*inch, 1*inch, 1*inch, 1*inch])
        feat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#16213e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
        ]))
        
        elements.append(feat_table)
        elements.append(Spacer(1, 0.2 * inch))
        
        return elements
    
    def _create_ai_explanation(self, incident: Incident) -> List:
        """Create AI explanation section"""
        elements = []
        
        header = Paragraph("AI EXPLANATION", self.styles['SectionHeader'])
        elements.append(header)
        
        explanation = Paragraph(incident.explanation.replace('\n', '<br/>'), self.styles['Normal'])
        elements.append(explanation)
        elements.append(Spacer(1, 0.3 * inch))
        
        return elements
    
    def _create_recommendations(self, incident: Incident) -> List:
        """Create recommendations section"""
        elements = []
        
        header = Paragraph("RECOMMENDED ACTIONS", self.styles['SectionHeader'])
        elements.append(header)
        
        recommendations = [
            "Isolate the affected endpoint from the network immediately",
            "Conduct a forensic analysis of the endpoint",
            "Review and analyze related logs for the affected timeframe",
            "Check for lateral movement to other systems",
            "Update detection rules based on this incident",
            "Implement recommended MITRE ATT&CK mitigations"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            rec_text = f"{i}. {rec}"
            elements.append(Paragraph(rec_text, self.styles['Normal']))
            elements.append(Spacer(1, 0.1 * inch))
        
        return elements
    
    def _get_severity_color(self, severity: str):
        """Get color for severity level"""
        severity_colors = {
            'critical': colors.HexColor('#d32f2f'),
            'high': colors.HexColor('#f57c00'),
            'medium': colors.HexColor('#fbc02d'),
            'low': colors.HexColor('#388e3c')
        }
        return severity_colors.get(severity.lower(), colors.grey)


if __name__ == "__main__":
    # Test PDF generation (would need a real incident object)
    print("PDF Report Generator initialized")
    print("Run with real incident data to generate report")
