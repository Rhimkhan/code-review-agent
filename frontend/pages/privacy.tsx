import { useRouter } from 'next/router'

export default function Privacy() {
  const router = useRouter()
  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono">
      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/10">
        <button onClick={() => router.push('/')} className="text-sm font-bold tracking-widest text-[#00ff94]">
          CodeReview<span className="text-white">.AI</span>
        </button>
      </nav>
      <main className="max-w-3xl mx-auto px-8 pt-20">
        <h1 className="text-4xl font-bold mb-6">Privacy Policy</h1>
        <div className="space-y-6 text-white/60 leading-relaxed">
          <p>Your code is analyzed in real-time and never stored permanently.</p>
          <p>We use Groq API for AI analysis. No personal data is collected.</p>
          <p>All review results are cleared after your session ends.</p>
        </div>
      </main>
    </div>
  )
}
