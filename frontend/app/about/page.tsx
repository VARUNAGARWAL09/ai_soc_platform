'use client'

import { motion } from 'framer-motion'

export default function AboutPage() {
    const team = [
        {
            name: 'Varun Agarwal',
            role: 'Security Engineer',
            initials: 'VA',
            code: 'SEC-01',
            skill: 'Network Forensics',
            stats: { off: 92, def: 88, int: 95 }
        },
    ]

    return (
        <div className="space-y-16 py-8">
            {/* Holographic Header */}
            <div className="relative text-center">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-full h-32 bg-cyber-blue/20 blur-[100px] pointer-events-none"></div>
                <h1 className="text-6xl md:text-8xl font-black text-transparent bg-clip-text bg-gradient-to-b from-gray-900 to-gray-500 dark:from-white dark:to-gray-600 tracking-tighter relative z-10">
                    CREATORS
                </h1>
                <div className="flex justify-center items-center gap-4 mt-4 font-mono text-cyber-blue relative z-10">
                    <span className="w-2 h-2 bg-cyber-blue rounded-full animate-ping"></span>
                    <span>RVCE BENGALURU // CYBER SECURITY DIVISION</span>
                    <span className="w-2 h-2 bg-cyber-blue rounded-full animate-ping"></span>
                </div>
            </div>

            {/* Personnel Grid */}
            <div className="flex justify-center flex-wrap gap-8 px-4">
                {team.map((member, index) => (
                    <motion.div
                        key={member.name}
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        transition={{ delay: index * 0.2 }}
                        className="group relative h-[450px] w-full md:w-[350px] Perspective-1000"
                    >
                        {/* Card Container */}
                        <div className="absolute inset-0 bg-white/90 dark:bg-black/60 backdrop-blur-md border border-gray-200 dark:border-white/10 overflow-hidden transform transition-all duration-500 group-hover:border-cyber-blue/50 group-hover:shadow-[0_0_30px_rgba(34,211,238,0.2)] rounded-xl">
                            {/* Animated Grid Background */}
                            <div className="absolute inset-0 bg-grid-pattern opacity-5 dark:opacity-10 group-hover:opacity-20 transition-opacity"></div>
                            <div className="absolute inset-0 bg-gradient-to-t from-gray-100 via-transparent to-transparent dark:from-black dark:via-transparent opacity-80"></div>

                            {/* ID Badge Layout */}
                            <div className="relative h-full p-6 flex flex-col items-center">
                                {/* Top Bar */}
                                <div className="w-full flex justify-between items-center text-[10px] font-mono text-gray-500 mb-8 border-b border-gray-200 dark:border-white/10 pb-2">
                                    <span>CLASSIFIED</span>
                                    <span>{member.code}</span>
                                </div>

                                {/* Avatar Hexagon */}
                                <div className="relative w-32 h-32 mb-6 pointer-events-none">
                                    <div className="absolute inset-0 bg-gradient-to-br from-cyber-blue to-cyber-purple opacity-10 blur-xl rounded-full group-hover:opacity-30 transition-opacity"></div>
                                    <div className="w-full h-full border-2 border-gray-200 dark:border-white/20 relative flex items-center justify-center bg-gray-50 dark:bg-black/50 overflow-hidden group-hover:border-cyber-blue transition-colors clip-path-hexagon">
                                        <span className="text-4xl font-black text-gray-400 dark:text-white/80 group-hover:text-cyber-blue transition-colors">
                                            {member.initials}
                                        </span>
                                    </div>
                                    {/* Spinner Ring */}
                                    <div className="absolute -inset-2 border border-dashed border-cyber-blue/30 rounded-full animate-spin-slow opacity-0 group-hover:opacity-100 transition-opacity"></div>
                                </div>

                                {/* Name & Role */}
                                <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-1 tracking-tight">{member.name}</h2>
                                <p className="text-cyber-purple font-mono text-xs tracking-widest uppercase mb-8">{member.role}</p>

                                {/* Stats Web */}
                                <div className="w-full space-y-3 mt-auto mb-4">
                                    <SkillBar label="OFFENSE" value={member.stats.off} color="bg-red-500" />
                                    <SkillBar label="DEFENSE" value={member.stats.def} color="bg-cyan-500" />
                                    <SkillBar label="INTEL" value={member.stats.int} color="bg-purple-500" />
                                </div>

                                {/* Expertise Chip */}
                                <div className="mt-2 px-3 py-1 bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10 rounded text-[10px] font-mono text-gray-500 dark:text-gray-300">
                                    EXP: {member.skill.toUpperCase()}
                                </div>
                            </div>
                        </div>

                        {/* Hover Glitch Decorations */}
                        <div className="absolute -top-1 -right-1 w-20 h-20 border-t-2 border-r-2 border-cyber-blue opacity-0 group-hover:opacity-100 transition-all duration-300"></div>
                        <div className="absolute -bottom-1 -left-1 w-20 h-20 border-b-2 border-l-2 border-cyber-blue opacity-0 group-hover:opacity-100 transition-all duration-300"></div>
                    </motion.div>
                ))}
            </div>

            {/* Footer Footer */}
            <div className="flex justify-center gap-8 text-xs font-mono text-gray-500 mt-12 border-t border-gray-200 dark:border-white/5 pt-8">
                <span>RVCE 2026</span>
                <span>CSE // SEM 7</span>
                <span>VER 1.0.4</span>
            </div>
        </div>
    )
}

function SkillBar({ label, value, color }: any) {
    return (
        <div className="flex items-center gap-2 text-[10px] font-mono font-bold">
            <span className="w-12 text-gray-400 dark:text-gray-500">{label}</span>
            <div className="flex-1 h-1.5 bg-gray-200 dark:bg-gray-800 rounded-full overflow-hidden">
                <motion.div
                    initial={{ width: 0 }}
                    whileInView={{ width: `${value}%` }}
                    transition={{ duration: 1, ease: "easeOut" }}
                    className={`h-full ${color}`}
                />
            </div>
            <span className="text-gray-900 dark:text-white w-6 text-right">{value}</span>
        </div>
    )
}
