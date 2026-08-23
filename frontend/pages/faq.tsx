import { useState } from 'react'
import { useRouter } from 'next/router'

const faqs = [
  { q: "What languages are supported?", a: "Python (full analysis), JavaScript, TypeScript, Java, Go, Rust and more (AI review)." },
  { q: "Is my code stored?", a: "No. Code is analyzed in real-time and never stored permanently." },
  { q: "How accurate is the AI review?", a: "The AnalystAgent uses Groq Llama3-70b with ~85% confidence on common issues." },
  { q: "What is the rate limit?", a: "100 requests per minute per IP address." },
  { q: "How many agents run?", a: "3 agents run in parallel: SecurityAgent, QualityAgent, and AnalystAgent." },
]

export default function FAQ() {
  const router = useRouter()
  const [open, setOpen] = useState<number | null>(null)
  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono">
      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/10">
        <button onClick={() => router.push('/')} className="text-sm font-bold tracking-widest text-[#00ff94]">
          CodeReview<span className="text-white">.AI</span>
        </button>
      </nav>
      <main className="max-w-3xl mx-auto px-8 pt-20">
        <h1 className="text-4xl font-bold mb-10">FAQ</h1>
        <div className="space-y-3">
          {faqs.map((faq, i) => (
            <div key={i} className="border border-white/10 rounded-lg overflow-hidden">
              <button onClick={() => setOpen(open === i ? null : i)}
                className="w-full text-left px-6 py-4 flex justify-between items-center hover:bg-white/5">
                <span className="text-sm font-bold">{faq.q}</span>
                <span className="text-[#00ff94]">{open === i ? "▲" : "▼"}</span>
              </button>
              {open === i && (
                <div className="px-6 py-4 text-white/50 text-sm border-t border-white/10">
                  {faq.a}
                </div>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  )
}
