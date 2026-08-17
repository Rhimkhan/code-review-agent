import { useRouter } from 'next/router'

export default function Terms() {
  const router = useRouter()
  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono">
      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/10">
        <button onClick={() => router.push('/')} className="text-sm font-bold tracking-widest text-[#00ff94]">
          CodeReview<span className="text-white">.AI</span>
        </button>
      </nav>
      <main className="max-w-3xl mx-auto px-8 pt-20">
        <h1 className="text-4xl font-bold mb-6">Terms of Service</h1>
        <div className="space-y-6 text-white/60 leading-relaxed">
          <p>By using CodeReview.AI, you agree to these terms.</p>
          <p>Do not submit malicious code or attempt to abuse the service.</p>
          <p>This service is provided as-is for educational purposes.</p>
          <p>Rate limits apply: 100 requests per minute per IP.</p>
        </div>
      </main>
    </div>
  )
}
