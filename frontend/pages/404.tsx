import { useRouter } from 'next/router'
export default function NotFound() {
  const router = useRouter()
  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono flex items-center justify-center">
      <div className="text-center">
        <div className="text-8xl font-bold text-[#00ff94] mb-4">404</div>
        <p className="text-white/40 mb-8">Page not found</p>
        <button onClick={() => router.push('/')} className="bg-[#00ff94] text-black px-6 py-3 rounded font-bold">Go Home</button>
      </div>
    </div>
  )
}
