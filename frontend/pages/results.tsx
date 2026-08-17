import { useEffect, useState } from "react";
import { useRouter } from "next/router";

interface Finding {
  type: string; subtype: string; line: number;
  severity: string; message: string; suggestion?: string;
}
interface ReviewResult {
  total_findings: number; summary: string;
  findings: Finding[]; severity_counts: Record<string, number>;
}

const SEV: Record<string, string> = {
  CRITICAL: "text-[#ff4d4d] border-[#ff4d4d]/30 bg-[#ff4d4d]/10",
  HIGH: "text-orange-400 border-orange-500/30 bg-orange-500/10",
  MEDIUM: "text-[#ffcc00] border-[#ffcc00]/30 bg-[#ffcc00]/10",
  LOW: "text-white/50 border-white/10 bg-white/5",
};

function Card({ f }: { f: Finding }) {
  const [open, setOpen] = useState(false);
  const s = SEV[f.severity?.toUpperCase()] || SEV.LOW;
  return (
    <div className="border border-white/10 rounded-lg overflow-hidden cursor-pointer hover:border-white/20 transition-colors" onClick={() => setOpen(!open)}>
      <div className="flex items-center gap-4 px-5 py-4">
        <span className="text-xs text-white/30 w-8">L{f.line}</span>
        <span className="text-sm text-white/80 flex-1">{f.message}</span>
        <span className={`text-xs font-bold px-2 py-0.5 rounded border ${s}`}>{f.severity}</span>
        <span className="text-xs text-white/20">{open ? "▲" : "▼"}</span>
      </div>
      {open && (
        <div className="border-t border-white/10 px-5 py-4 space-y-2">
          <div className="flex gap-3 text-xs"><span className="text-white/30 w-16">Type</span><span className="text-white/60">{f.type} / {f.subtype}</span></div>
          {f.suggestion && <div className="flex gap-3 text-xs"><span className="text-white/30 w-16">Fix</span><span className="text-[#00ff94]">{f.suggestion}</span></div>}
        </div>
      )}
    </div>
  );
}

export default function Results() {
  const router = useRouter();
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [tab, setTab] = useState("all");

  useEffect(() => {
    const raw = sessionStorage.getItem("review_result");
    if (!raw) { router.push("/dashboard"); return; }
    setResult(JSON.parse(raw));
  }, [router]);

  if (!result) return null;

  const tabs = [
    { key: "all", label: "All", items: result.findings },
    { key: "security", label: "Security", items: result.findings.filter(f => f.type === "Security") },
    { key: "quality", label: "Quality", items: result.findings.filter(f => f.type === "Quality") },
    { key: "bugs", label: "Bugs", items: result.findings.filter(f => f.type === "Bug") },
  ];
  const shown = tabs.find(t => t.key === tab)?.items || [];

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono">
      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/10">
        <span className="text-sm font-bold tracking-widest text-[#00ff94]">CodeReview<span className="text-white">.AI</span></span>
        <button onClick={() => router.push("/dashboard")} className="text-xs border border-white/20 px-4 py-2 rounded hover:border-[#00ff94] hover:text-[#00ff94] transition-colors">← New review</button>
      </nav>
      <main className="max-w-5xl mx-auto px-8 pt-12 pb-24">
        <h2 className="text-3xl font-bold mb-8">{result.summary}</h2>
        <div className="grid grid-cols-4 gap-3 mb-10">
          {["CRITICAL","HIGH","MEDIUM","LOW"].map(sev => (
            <div key={sev} className={`border rounded-lg p-4 text-center ${SEV[sev]}`}>
              <div className="text-2xl font-bold">{result.severity_counts?.[sev] || 0}</div>
              <div className="text-xs mt-1 opacity-60">{sev}</div>
            </div>
          ))}
        </div>
        <div className="flex gap-1 mb-6 border-b border-white/10">
          {tabs.map(t => (
            <button key={t.key} onClick={() => setTab(t.key)}
              className={`px-4 py-2.5 text-xs font-bold border-b-2 -mb-px transition-colors ${tab === t.key ? "border-[#00ff94] text-[#00ff94]" : "border-transparent text-white/30 hover:text-white/60"}`}>
              {t.label} <span className="text-white/20 ml-1">{t.items.length}</span>
            </button>
          ))}
        </div>
        {shown.length === 0
          ? <div className="text-center py-20 text-white/20">✅ No findings here</div>
          : <div className="space-y-2">{shown.map((f, i) => <Card key={i} f={f} />)}</div>
        }
      </main>
    </div>
  );
}