interface Props {
  severity: string
  count?: number
}

const STYLES: Record<string, string> = {
  CRITICAL: 'text-red-400 border-red-400/30 bg-red-400/10',
  HIGH: 'text-orange-400 border-orange-400/30 bg-orange-400/10',
  MEDIUM: 'text-yellow-400 border-yellow-400/30 bg-yellow-400/10',
  LOW: 'text-white/50 border-white/10 bg-white/5',
}

export default function SeverityBadge({ severity, count }: Props) {
  const style = STYLES[severity?.toUpperCase()] || STYLES.LOW
  return (
    <span className={`text-xs font-bold px-2 py-0.5 rounded border ${style}`}>
      {count !== undefined ? `${count} ${severity}` : severity}
    </span>
  )
}
