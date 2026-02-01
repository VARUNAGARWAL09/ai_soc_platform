"use client"
import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import axios from 'axios'
import Link from 'next/link'

interface Message {
    role: 'user' | 'ai'
    content: string
    timestamp: Date
    actions?: { label: string; url: string }[]
}

const API_base = 'http://localhost:8000/api'

export default function AIChatbot() {
    const [isOpen, setIsOpen] = useState(false)
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const [messages, setMessages] = useState<Message[]>([
        { role: 'ai', content: 'Hello! I am your AI SOC Assistant. How can I help you today?', timestamp: new Date() }
    ])
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
    }

    useEffect(scrollToBottom, [messages])

    const sendMessage = async () => {
        if (!input.trim()) return

        const userMsg: Message = { role: 'user', content: input, timestamp: new Date() }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setIsLoading(true)

        try {
            const res = await axios.post(`${API_base}/chat/`, {
                message: userMsg.content,
                role: 'user'
            })

            const aiMsg: Message = {
                role: 'ai',
                content: res.data.response,
                timestamp: new Date(),
                actions: res.data.actions
            }
            setMessages(prev => [...prev, aiMsg])
        } catch (err) {
            setMessages(prev => [...prev, { role: 'ai', content: 'Error: Could not connect to AI Neural Core.', timestamp: new Date() }])
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="fixed bottom-6 left-6 z-[100] flex flex-col items-start pointer-events-none">

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9, y: 20 }}
                        animate={{ opacity: 1, scale: 1, y: 0 }}
                        exit={{ opacity: 0, scale: 0.9, y: 20 }}
                        className="glass-panel w-[350px] h-[500px] mb-4 pointer-events-auto rounded-2xl shadow-2xl border border-white/20 flex flex-col overflow-hidden"
                    >
                        {/* Header */}
                        <div className="bg-gradient-to-r from-cyber-blue/20 to-cyber-purple/20 p-4 border-b border-white/10 flex justify-between items-center backdrop-blur-md">
                            <div className="flex items-center gap-2">
                                <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse"></div>
                                <span className="font-bold text-white tracking-wide">SOC AI ASSISTANT</span>
                            </div>
                            <button onClick={() => setIsOpen(false)} className="text-gray-400 hover:text-white">✕</button>
                        </div>

                        {/* Messages */}
                        <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar bg-black/40">
                            {messages.map((msg, idx) => (
                                <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                                    <div className={`max-w-[85%] p-3 rounded-2xl text-sm ${msg.role === 'user'
                                        ? 'bg-cyber-blue text-black font-medium rounded-tr-none'
                                        : 'bg-white/10 text-gray-200 border border-white/5 rounded-tl-none'
                                        }`}>
                                        <p>{msg.content}</p>
                                        {msg.actions && (
                                            <div className="mt-2 flex flex-wrap gap-2">
                                                {msg.actions.map((act, i) => (
                                                    <Link key={i} href={act.url} className="text-xs bg-black/30 hover:bg-black/50 text-cyber-blue px-2 py-1 rounded border border-cyber-blue/30 transition-colors">
                                                        {act.label} →
                                                    </Link>
                                                ))}
                                            </div>
                                        )}
                                        <div className="text-[9px] opacity-50 mt-1 text-right">
                                            {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </div>
                                    </div>
                                </div>
                            ))}
                            {isLoading && (
                                <div className="flex justify-start">
                                    <div className="bg-white/5 px-4 py-3 rounded-2xl rounded-tl-none flex space-x-1">
                                        <div className="w-1.5 h-1.5 bg-cyber-blue rounded-full animate-bounce"></div>
                                        <div className="w-1.5 h-1.5 bg-cyber-blue rounded-full animate-bounce delay-100"></div>
                                        <div className="w-1.5 h-1.5 bg-cyber-blue rounded-full animate-bounce delay-200"></div>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                        {/* Input */}
                        <div className="p-3 border-t border-white/10 bg-black/20 backdrop-blur-sm">
                            <div className="flex gap-2">
                                <input
                                    type="text"
                                    value={input}
                                    onChange={e => setInput(e.target.value)}
                                    onKeyDown={e => e.key === 'Enter' && sendMessage()}
                                    placeholder="Ask about threats..."
                                    className="flex-1 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-sm text-white focus:outline-none focus:border-cyber-blue/50"
                                />
                                <button
                                    onClick={sendMessage}
                                    disabled={!input.trim() || isLoading}
                                    className="bg-cyber-blue text-black p-2 rounded-xl hover:bg-white transition-colors disabled:opacity-50"
                                >
                                    ➤
                                </button>
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => setIsOpen(!isOpen)}
                className="w-14 h-14 rounded-full bg-gradient-to-br from-cyber-blue to-cyber-purple shadow-lg shadow-cyber-blue/20 flex items-center justify-center pointer-events-auto border border-white/20"
            >
                {isOpen ? (
                    <span className="text-xl font-bold text-white">✕</span>
                ) : (
                    <span className="text-2xl">🤖</span>
                )}
            </motion.button>
        </div>
    )
}
