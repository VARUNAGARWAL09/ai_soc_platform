"use client"
import { motion } from 'framer-motion'
import { useTheme } from './ThemeProvider'

export default function ThemeToggle() {
    const { theme, toggleTheme } = useTheme()

    return (
        <button
            onClick={toggleTheme}
            className="p-2 rounded-full glass-panel hover:bg-white/10 dark:hover:bg-white/10 border-0 transition-all active:scale-95 text-xl"
            title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
        >
            <motion.div
                initial={false}
                animate={{ rotate: theme === 'dark' ? 0 : 180 }}
                transition={{ duration: 0.3 }}
            >
                {theme === 'dark' ? '🌙' : '☀️'}
            </motion.div>
        </button>
    )
}
