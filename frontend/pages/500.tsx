import { useRouter } from 'next/router'

export default function ServerError() {
  const router = useRouter()
  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono flex items-center justify-center">
      <div className="text-center">
        <div className="text-8xl font-bold text-[#ff4d4d] mb-4">500</div>
        <p className="text-white/40 mb-8">Something went wrong on our end</p>
        <button
          onClick={() => router.push('/')}
          className="bg-[#00ff94] text-black px-6 py-3 rounded font-bold hover:bg-white transition-colors"
        >
          Go Home
        </button>
      </div>
    </div>
  )
}
