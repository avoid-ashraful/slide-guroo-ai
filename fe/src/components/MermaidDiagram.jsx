import { useEffect, useRef } from 'react'
import mermaid from 'mermaid'

// Initialize mermaid
mermaid.initialize({
  startOnLoad: true,
  theme: 'default',
  securityLevel: 'loose',
  themeVariables: {
    primaryColor: '#3b82f6',
    primaryTextColor: '#1f2937',
    primaryBorderColor: '#2563eb',
    lineColor: '#6366f1',
    secondaryColor: '#8b5cf6',
    tertiaryColor: '#ec4899',
  },
})

function MermaidDiagram({ code, id }) {
  const containerRef = useRef(null)

  useEffect(() => {
    if (containerRef.current && code) {
      const render = async () => {
        try {
          // Clear previous content
          containerRef.current.innerHTML = ''

          // Generate unique ID
          const uniqueId = `mermaid-${id || Math.random().toString(36).substr(2, 9)}`

          // Render diagram
          const { svg } = await mermaid.render(uniqueId, code)
          containerRef.current.innerHTML = svg
        } catch (error) {
          console.error('Mermaid rendering error:', error)
          containerRef.current.innerHTML = `
            <div class="p-4 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-red-700 text-sm">Failed to render diagram</p>
            </div>
          `
        }
      }

      render()
    }
  }, [code, id])

  if (!code) return null

  return (
    <div className="mermaid-container">
      <div ref={containerRef} className="mermaid" />
    </div>
  )
}

export default MermaidDiagram
