"use client"
import { useEffect } from 'react'

export default function ElevenLabsWidget() {
    useEffect(() => {
        const script = document.createElement('script')
        script.src = "https://elevenlabs.io/convai-widget/index.js"
        script.async = true
        script.type = "text/javascript"
        document.body.appendChild(script)

        return () => {
            document.body.removeChild(script)
        }
    }, [])

    return (
        <elevenlabs-convai agent-id="agent_3201kfr4pbv0emmv8hx7180dr1sj"></elevenlabs-convai>
    )
}

declare global {
    namespace JSX {
        interface IntrinsicElements {
            'elevenlabs-convai': React.DetailedHTMLProps<React.HTMLAttributes<HTMLElement> & { 'agent-id': string }, HTMLElement>
        }
    }
}
