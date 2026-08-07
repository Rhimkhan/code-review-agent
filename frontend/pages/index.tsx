import { useState } from 'react';

interface Finding {
  type: string;
  subtype: string;
  line: number;
  severity: string;
  message: string;
  suggestion?: string;
}

interface ReviewResult {
  total_findings: number;
  summary: string;
  findings: Finding[];
  severity_counts: Record<string, number>;
}

export default function Home() {
  const [code, setCode] = useState("");
  const [filename, setFilename] = useState("code.py");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ReviewResult | null>(null);
  const [error, setError] = useState("");

  const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const handleReview = async () => {
    if (!code.trim()) {
      setError("Please enter some code");
      return;
    }

    setLoading(true);
    setError("");
    setResult(null);

    try {
      console.log("===== REVIEW BUTTON CLICKED =====");

      const response = await fetch(`${API_BASE}/api/review/code`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          code,
          filename,
        }),
      });

      console.log("HTTP Status:", response.status);

      const data = await response.json();

      console.log("Backend Response:", data);

      if (!response.ok) {
        setError(data.detail || "Backend returned an error");
      } else if (data.status === "success") {
        setResult(data.review);
      } else {
        setError(data.error || "Unknown backend error");
      }
    } catch (err: any) {
      console.error("FETCH ERROR:", err);
      setError(err.message || "Cannot connect to backend.");
    }

    setLoading(false);
  };

  const handleDemo = async () => {
    try {
      console.log("Demo clicked");

      const response = await fetch(`${API_BASE}/api/review/demo`);

      const data = await response.json();

      console.log(data);

      if (data.status === "success") {
        setResult(data.review);
      }
    } catch (err) {
      console.error(err);
      setError("Cannot connect to backend.");
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity.toUpperCase()) {
      case "CRITICAL":
        return "bg-red-100 text-red-800 border-red-200";
      case "HIGH":
        return "bg-orange-100 text-orange-800 border-orange-200";
      case "MEDIUM":
        return "bg-yellow-100 text-yellow-800 border-yellow-200";
      case "LOW":
        return "bg-blue-100 text-blue-800 border-blue-200";
      default:
        return "bg-gray-100 text-gray-800 border-gray-200";
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="border-b border-gray-800 px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🤖</span>
            <div>
              <h1 className="text-xl font-bold">Code Review Agent</h1>
              <p className="text-xs text-gray-400">
                AI-powered multi-agent code analysis
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <span className="w-2 h-2 bg-green-400 rounded-full"></span>
            <span className="text-sm text-gray-400">3 Agents Active</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        <div className="text-center mb-10">
          <h2 className="text-4xl font-bold mb-3">
            Review Code with{" "}
            <span className="text-blue-400">AI Agents</span>
          </h2>

          <p className="text-gray-400 text-lg">
            SecurityAgent + QualityAgent + AnalystAgent working together
          </p>
        </div>

        <div className="bg-gray-900 rounded-xl border border-gray-800 p-6 mb-6">

          <div className="flex gap-4 mb-4">

            <input
              type="text"
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              className="w-48 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg"
            />

            <button
              onClick={handleDemo}
              className="px-4 py-2 bg-gray-700 rounded-lg"
            >
              Try Demo
            </button>

          </div>

          <textarea
            rows={12}
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Paste your code here..."
            className="w-full px-4 py-3 bg-gray-800 border border-gray-700 rounded-lg font-mono"
          />

          {error && (
            <div className="mt-4 p-3 bg-red-900 border border-red-700 rounded">
              {error}
            </div>
          )}

          <button
            onClick={handleReview}
            disabled={loading}
            className="mt-4 w-full py-3 bg-blue-600 rounded-lg"
          >
            {loading ? "Analyzing..." : "🚀 Review Code"}
          </button>

        </div>

        {result && (
          <div className="bg-gray-900 rounded-xl border border-gray-800 p-6">

            <h2 className="text-xl font-bold mb-4">
              Review Results
            </h2>

            <p className="mb-6 text-green-400">
              {result.summary}
            </p>

            {result.findings.map((f, i) => (
              <div
                key={i}
                className="border border-gray-700 rounded-lg p-4 mb-3"
              >
                <span
                  className={`px-2 py-1 rounded text-xs font-bold ${getSeverityColor(
                    f.severity
                  )}`}
                >
                  {f.severity}
                </span>

                <p className="mt-3">{f.message}</p>

                <p className="text-gray-400 text-sm">
                  Line {f.line}
                </p>

                {f.suggestion && (
                  <p className="text-green-400 mt-2">
                    💡 {f.suggestion}
                  </p>
                )}
              </div>
            ))}

          </div>
        )}

      </main>
    </div>
  );
}