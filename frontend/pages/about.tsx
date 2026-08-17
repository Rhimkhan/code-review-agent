import { useRouter } from 'next/router'

export default function About() {
  const router = useRouter()
  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono">
      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/10">
        <button onClick={() => router.push('/')} className="text-sm font-bold tracking-widest text-[#00ff94]">
          CodeReview<span className="text-white">.AI</span>
        </button>
      </nav>
      <main className="max-w-3xl mx-auto px-8 pt-20">
        <h1 className="text-4xl font-bold mb-6">About</h1>
        <p className="text-white/60 leading-relaxed mb-6">
          Code Review Agent is a multi-agent AI system that analyzes your code
          using three specialized agents running in parallel.
        </p>
        <div className="space-y-4">
          {[
            { name: "SecurityAgent", desc: "Detects vulnerabilities using Bandit and pattern matching" },
            { name: "QualityAgent", desc: "Analyzes code structure using Python AST" },
            { name: "AnalystAgent", desc: "Deep review using Groq Llama3-70b LLM" },
          ].map(a => (
            <div key={a.name} className="border border-white/10 rounded-lg p-5">
              <h3 className="text-[#00ff94] font-bold mb-2">{a.name}</h3>
              <p className="text-white/50 text-sm">{a.desc}</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
