import { useState } from "react";
import { useRouter } from "next/router";

const EXAMPLE_CODE = `import sqlite3
SECRET_KEY = "supersecret123"

def get_user(username):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE name = '" + username + "'")
    return cursor.fetchone()

def process_data(a, b, c, d, e, f, g):
    try:
        result = a + b + c + d + e + f + g
        return result
    except:
        pass
`;

export default function Dashboard() {
  const router = useRouter();
  const [code, setCode] = useState("");
  const [filename, setFilename] = useState("main.py");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleReview = async () => {
    if (!code.trim()) { setError("Paste some code first."); return; }
    setError("");
    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/api/review/code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, filename }),
      });
      const data = await res.json();
      if (data.status !== "success") throw new Error(data.error || "Review failed");
      sessionStorage.setItem("review_result", JSON.stringify(data.review));
      router.push("/results");
    } catch (err: any) {
      setError(err.message || "Cannot connect to backend.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0d0d0d] text-white font-mono">
      <nav className="flex items-center justify-between px-8 py-5 border-b border-white/10">
        <button onClick={() => router.push("/")} className="text-sm font-bold tracking-widest text-[#00ff94]">
          CodeReview<span className="text-white">.AI</span>
        </button>
        <span className="text-xs text-white/30">Dashboard</span>
      </nav>
      <main className="max-w-5xl mx-auto px-8 pt-14 pb-24">
        <div className="mb-10">
          <h2 className="text-3xl font-bold mb-2">Paste your code</h2>
          <p className="text-white/40 text-sm">All three agents analyze in parallel.</p>
        </div>
        <div className="mb-4 flex items-center gap-3">
          <label className="text-xs text-white/40 uppercase tracking-widest w-20">Filename</label>
          <input type="text" value={filename} onChange={(e) => setFilename(e.target.value)}
            className="bg-white/5 border border-white/10 rounded px-3 py-2 text-sm text-white focus:outline-none focus:border-[#00ff94] w-48 transition-colors" />
          <button onClick={() => setCode(EXAMPLE_CODE)} className="text-xs text-white/30 hover:text-[#00ff94] transition-colors ml-auto">
            Load example →
          </button>
        </div>
        <textarea value={code} onChange={(e) => setCode(e.target.value)}
          placeholder="# Paste your code here..."
          rows={22} spellCheck={false}
          className="w-full bg-[#111] border border-white/10 rounded-lg p-5 text-sm text-white/80 placeholder-white/15 focus:outline-none focus:border-[#00ff94] resize-none leading-relaxed transition-colors"
          style={{ fontFamily: "monospace" }} />
        {error && (
          <div className="mt-4 text-sm text-[#ff4d4d] border border-[#ff4d4d]/30 bg-[#ff4d4d]/5 rounded px-4 py-3">⚠ {error}</div>
        )}
        <div className="mt-6 flex items-center gap-4">
          <button onClick={handleReview} disabled={loading}
            className={`px-8 py-4 rounded font-bold text-sm tracking-wide transition-all ${loading ? "bg-white/10 text-white/30 cursor-not-allowed" : "bg-[#00ff94] text-black hover:bg-white"}`}>
            {loading ? "Agents running…" : "Run code review →"}
          </button>
          {code && <button onClick={() => { setCode(""); setError(""); }} className="text-xs text-white/30 hover:text-white/60 transition-colors">Clear</button>}
        </div>
        {loading && (
          <div className="mt-8 grid grid-cols-3 gap-3">
            {[{name:"SecurityAgent",color:"#ff4d4d"},{name:"QualityAgent",color:"#ffcc00"},{name:"AnalystAgent",color:"#00ff94"}].map((a) => (
              <div key={a.name} className="border border-white/10 rounded p-4 flex items-center gap-3">
                <span className="w-2 h-2 rounded-full animate-pulse" style={{backgroundColor:a.color}} />
                <span className="text-xs text-white/50">{a.name}</span>
                <span className="text-xs text-white/20 ml-auto">running…</span>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
