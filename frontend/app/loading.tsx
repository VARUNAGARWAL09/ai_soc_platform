export default function Loading() {
    return (
        <div className="flex flex-col items-center justify-center min-h-[60vh] space-y-6">
            <div className="relative">
                <div className="w-16 h-16 border-4 border-cyber-blue/30 border-t-cyber-blue rounded-full animate-spin"></div>
                <div className="absolute top-0 left-0 w-16 h-16 border-4 border-transparent border-b-cyber-purple/50 rounded-full animate-spin-reverse"></div>
            </div>
            <div className="flex flex-col items-center space-y-2">
                <h2 className="text-xl font-bold text-cyber-blue animate-pulse">SYSTEM LOADING</h2>
                <div className="flex space-x-1">
                    <span className="w-2 h-2 bg-cyber-blue/50 rounded-full animate-bounce delay-75"></span>
                    <span className="w-2 h-2 bg-cyber-blue/50 rounded-full animate-bounce delay-150"></span>
                    <span className="w-2 h-2 bg-cyber-blue/50 rounded-full animate-bounce delay-300"></span>
                </div>
                <p className="text-sm text-gray-500 font-mono">Initializing secure connection...</p>
            </div>
        </div>
    )
}
