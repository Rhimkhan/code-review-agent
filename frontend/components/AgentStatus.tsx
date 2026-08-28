interface Agent {
  name: string
  color: string
  status: 'idle' | 'running' | 'done'
}

const AGENTS: Agent[] = [
  { name: 'SecurityAgent', color: '#ff4d4d', status: 'idle' },
  { name: 'QualityAgent', color: '#ffcc00', status: 'idle' },
  { name: 'AnalystAgent', color: '#00ff94', status: 'idle' },
]

export default function AgentStatus({ loading }: { loading: boolean }) {
  return (
    <div className="grid grid-cols-3 gap-3 mt-6">
      {AGENTS.map((agent) => (
        <div
          key={agent.name}
          className="border border-white/10 rounded-lg p-4 flex items-center gap-3"
        >
          <span
            className={`w-2 h-2 rounded-full ${loading ? 'animate-pulse' : ''}`}
            style={{ backgroundColor: loading ? agent.color : '#333' }}
          />
          <span className="text-xs text-white/50">{agent.name}</span>
          <span className="text-xs text-white/20 ml-auto">
            {loading ? 'running...' : 'idle'}
          </span>
        </div>
      ))}
    </div>
  )
}
