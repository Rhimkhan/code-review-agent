import { useRouter } from 'next/router'

interface NavbarProps {
  showDashboard?: boolean
}

export default function Navbar({ showDashboard = true }: NavbarProps) {
  const router = useRouter()
  return (
    <nav className="flex items-center justify-between px-8 py-5 border-b border-white/10">
      <button
        onClick={() => router.push('/')}
        className="text-sm font-bold tracking-widest text-[#00ff94]"
      >
        CodeReview<span className="text-white">.AI</span>
      </button>
      <div className="flex items-center gap-4">
        {showDashboard && (
          <button
            onClick={() => router.push('/dashboard')}
            className="text-xs border border-white/20 px-4 py-2 rounded hover:border-[#00ff94] hover:text-[#00ff94] transition-colors"
          >
            Dashboard
          </button>
        )}
        <button
          onClick={() => router.push('/about')}
          className="text-xs text-white/30 hover:text-white/60 transition-colors"
        >
          About
        </button>
        <button
          onClick={() => router.push('/faq')}
          className="text-xs text-white/30 hover:text-white/60 transition-colors"
        >
          FAQ
        </button>
      </div>
    </nav>
  )
}
