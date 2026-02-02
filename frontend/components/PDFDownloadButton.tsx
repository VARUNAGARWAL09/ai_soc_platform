"use client"

import React from 'react'
import { PDFDownloadLink } from '@react-pdf/renderer'
import DocumentationDoc from './DocumentationPDF'

const PDFDownloadButton = () => {
    return (
        <PDFDownloadLink
            document={<DocumentationDoc />}
            fileName="AI_SOC_Platform_Documentation.pdf"
            className="flex items-center space-x-2 bg-cyber-blue/10 hover:bg-cyber-blue/20 text-cyber-blue px-4 py-2 rounded-lg transition-colors border border-cyber-blue/30"
        >
            {({ blob, url, loading, error }) =>
                loading ? (
                    <span className="flex items-center space-x-2">
                        <svg className="animate-spin h-5 w-5 text-cyber-blue" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <span>Generating...</span>
                    </span>
                ) : (
                    <span className="flex items-center space-x-2">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
                        </svg>
                        <span>Download PDF</span>
                    </span>
                )
            }
        </PDFDownloadLink>
    )
}

export default PDFDownloadButton
