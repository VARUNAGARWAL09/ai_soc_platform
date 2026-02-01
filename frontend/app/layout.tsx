import './globals.css'
import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import Link from 'next/link'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
    title: 'AI SOC Platform - Cybersecurity Threat Detection',
    description: 'Production-grade AI-powered Security Operations Center',
}

import AIChatbot from '../components/AIChatbot'
import ElevenLabsWidget from '../components/ElevenLabsWidget'

import ThemeProvider from '../components/ThemeProvider'
import ThemeToggle from '../components/ThemeToggle'

export default function RootLayout({
    children,
}: {
    children: React.ReactNode
}) {
    return (
        <html lang="en">
            <body className={inter.className}>
                <ThemeProvider>
                    <div className="min-h-screen bg-gray-50 dark:bg-cyber-darker text-gray-900 dark:text-white">
                        {/* Navigation */}
                        <nav className="glass-panel border-b border-white/10 sticky top-0 z-50">
                            <div className="container mx-auto px-6 py-4">
                                <div className="flex items-center justify-between">
                                    <Link href="/" className="flex items-center space-x-3">
                                        <div className="w-10 h-10 bg-gradient-to-br from-cyber-blue to-cyber-purple rounded-lg flex items-center justify-center">
                                            <span className="text-xl font-bold">⚡</span>
                                        </div>
                                        <span className="text-xl font-bold bg-gradient-to-r from-cyber-blue to-cyber-purple bg-clip-text text-transparent">
                                            AI SOC Platform
                                        </span>
                                    </Link>

                                    <div className="flex space-x-6">
                                        <NavLink href="/">Dashboard</NavLink>
                                        <NavLink href="/logs">Live Logs</NavLink>
                                        <NavLink href="/threats">Threat Analyzer</NavLink>
                                        <NavLink href="/incidents">Incidents</NavLink>
                                        <NavLink href="/playbooks">Playbooks</NavLink>
                                        <NavLink href="/forensics">Forensics</NavLink>
                                        <NavLink href="/about">About Team</NavLink>
                                        <div className="pl-4 border-l border-white/10 flex items-center">
                                            <ThemeToggle />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </nav>

                        {/* Main Content */}
                        <main className="container mx-auto px-6 py-8">
                            {children}
                        </main>

                        {/* AI Chatbot */}
                        {/* <AIChatbot /> */}
                        {/* <ElevenLabsWidget /> */}
                    </div>
                </ThemeProvider>
            </body>
        </html>
    )
}

function NavLink({ href, children }: { href: string; children: React.ReactNode }) {
    return (
        <Link
            href={href}
            className="text-gray-300 hover:text-cyber-blue transition-colors duration-200 font-medium"
        >
            {children}
        </Link>
    )
}
