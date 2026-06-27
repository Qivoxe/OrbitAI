"use client";

import { useState } from "react";

interface Parameters {
  period_days: number;
  depth_ppm: number;
  duration_hrs: number;
  snr: number;
  scatter_ppm: number;
  radius_ratio: number;
  fit_quality: string;
}

interface Quality {
  confidence: string;
  score: number;
  flags: string[];
}

interface Result {
  tic_id: number;
  classification: string;
  confidence: number;
  probabilities: Record<string, number>;
  parameters: Parameters;
  quality: Quality;
  figure_url: string | null;
}

const KNOWN_TARGETS = [
  { name: "WASP-126b", tic: "25155310" },
  { name: "TOI-700",   tic: "207141131" },
  { name: "Known EB",  tic: "318937509" },
];

const CLASS_COLORS: Record<string, string> = {
  "PLANET CANDIDATE": "text-green-400 border-green-400 bg-green-400/10",
  "ECLIPSING BINARY": "text-red-400 border-red-400 bg-red-400/10",
  "BLEND":            "text-yellow-400 border-yellow-400 bg-yellow-400/10",
  "NOISE / OTHER":    "text-slate-400 border-slate-400 bg-slate-400/10",
  "UNKNOWN":          "text-slate-400 border-slate-400 bg-slate-400/10",
};

const BAR_COLORS: Record<string, string> = {
  "PLANET CANDIDATE": "bg-green-400",
  "ECLIPSING BINARY": "bg-red-400",
  "BLEND":            "bg-yellow-400",
  "NOISE / OTHER":    "bg-slate-400",
};

const PIPELINE_STAGES = [
  "Data Ingestion",
  "Preprocessing",
  "BLS Detection",
  "Classification",
  "Parameter Fitting",
  "Visualization",
];

export default function Dashboard() {
  const [ticId,   setTicId]   = useState("");
  const [loading, setLoading] = useState(false);
  const [stage,   setStage]   = useState(-1);
  const [result,  setResult]  = useState<Result | null>(null);
  const [error,   setError]   = useState("");

  const runAnalysis = async () => {
    if (!ticId) return;
    try {
      setLoading(true);
      setError("");
      setResult(null);
      setStage(0);

      const timer = setInterval(() => {
        setStage(s => (s < 5 ? s + 1 : s));
      }, 8000);

      const response = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ tic_id: Number(ticId) }),
      });

      clearInterval(timer);
      setStage(5);

      const data: Result = await response.json();

      if (!response.ok) {
        throw new Error((data as any).detail || "Backend error");
      }

      const history: Result[] = JSON.parse(
        localStorage.getItem("PlanetX-history") || "[]"
      );
      history.unshift(data);
      localStorage.setItem("PlanetX-history", JSON.stringify(history.slice(0, 20)));

      setResult(data);
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : "Failed to connect to backend.";
      setError(message);
    } finally {
      setLoading(false);
      setStage(-1);
    }
  };

  return (
    <main className="min-h-screen bg-[#04080f] text-white px-6 py-12">
      <div className="max-w-6xl mx-auto">

        <div className="mb-10">
          <p className="text-cyan-400 font-mono text-sm mb-1">PlanetX / Analyze</p>
          <h1 className="text-4xl font-bold tracking-tight">Target Analysis</h1>
          <p className="text-slate-400 mt-2">
            Enter a TESS Input Catalog ID to run the full detection pipeline
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-8">

          {/* Input Panel */}
          <div className="md:col-span-2 bg-[#0a1628] border border-[#1a3a5c] rounded-lg p-6">
            <div className="border-t-2 border-cyan-400 -mt-6 mb-6 w-16"></div>
            <p className="text-xs text-slate-400 uppercase tracking-widest mb-2 font-mono">
              TIC Identifier
            </p>
            <input
              type="number"
              placeholder="e.g. 25155310"
              value={ticId}
              onChange={(e) => setTicId(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && runAnalysis()}
              className="w-full p-3 bg-[#04080f] border border-[#1a3a5c] focus:border-cyan-400 focus:outline-none text-white font-mono rounded mb-4 transition-all"
            />
            <button
              onClick={runAnalysis}
              disabled={loading || !ticId}
              className="w-full py-3 bg-cyan-400 hover:brightness-110 text-[#04080f] font-bold rounded transition-all disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {loading ? "Running Pipeline..." : "Run Pipeline"}
            </button>

            <div className="mt-6">
              <p className="text-xs text-slate-500 uppercase tracking-widest mb-3 font-mono">
                Known Targets
              </p>
              <div className="flex flex-col gap-2">
                {KNOWN_TARGETS.map((t) => (
                  <button
                    key={t.tic}
                    onClick={() => setTicId(t.tic)}
                    className="flex items-center gap-2 px-3 py-2 bg-[#04080f] border border-[#1a3a5c] hover:border-cyan-400 rounded text-sm font-mono text-left transition-all"
                  >
                    <span className="w-2 h-2 rounded-full bg-cyan-400 flex-shrink-0"></span>
                    <span className="text-cyan-300">{t.name}</span>
                    <span className="text-slate-500 ml-auto">{t.tic}</span>
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Pipeline Status */}
          <div className="md:col-span-3 bg-[#0a1628] border border-[#1a3a5c] rounded-lg p-6">
            <p className="text-xs text-slate-400 uppercase tracking-widest mb-6 font-mono">
              Pipeline Status
            </p>
            <div className="flex flex-col gap-5">
              {PIPELINE_STAGES.map((s, i) => {
                const done    = stage > i;
                const active  = stage === i;
                const pending = stage < i;
                return (
                  <div key={s} className="flex items-center gap-4">
                    <div className={`w-3 h-3 rounded-full border-2 flex-shrink-0 transition-all duration-500
                      ${done    ? "bg-cyan-400 border-cyan-400" : ""}
                      ${active  ? "border-cyan-400 animate-pulse" : ""}
                      ${pending ? "border-slate-600" : ""}
                    `}></div>
                    <span className={`font-mono text-sm transition-all
                      ${done    ? "text-cyan-400" : ""}
                      ${active  ? "text-white"    : ""}
                      ${pending ? "text-slate-500" : ""}
                    `}>
                      {String(i + 1).padStart(2, "0")} {s}
                    </span>
                    <span className="ml-auto text-xs font-mono">
                      {done   && <span className="text-cyan-400">✓</span>}
                      {active && <span className="text-white animate-pulse">running...</span>}
                    </span>
                  </div>
                );
              })}
            </div>
            {stage === -1 && !result && (
              <p className="text-slate-600 text-sm font-mono mt-6">
                Awaiting target input...
              </p>
            )}
          </div>
        </div>

        {error && (
          <div className="p-4 rounded border border-red-500 bg-red-500/10 text-red-400 font-mono text-sm mb-6">
            ✗ {error}
          </div>
        )}

        {result && (
          <div className="space-y-6">

            {/* Classification Banner */}
            <div className="bg-[#0a1628] border border-[#1a3a5c] rounded-lg p-6 flex items-center justify-between">
              <div>
                <p className="text-xs text-slate-400 font-mono uppercase tracking-widest mb-2">
                  TIC {result.tic_id}
                </p>
                <span className={`inline-block px-4 py-2 rounded border text-lg font-bold ${CLASS_COLORS[result.classification] ?? CLASS_COLORS["UNKNOWN"]}`}>
                  {result.classification}
                </span>
              </div>
              <div className="text-right">
                <p className="text-xs text-slate-400 font-mono mb-1">Confidence</p>
                <p className="text-4xl font-mono text-cyan-400">
                  {Number(result.confidence).toFixed(1)}%
                </p>
              </div>
            </div>

            {/* Parameter Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: "Period",   value: result.parameters.period_days,  unit: "days" },
                { label: "Depth",    value: result.parameters.depth_ppm,    unit: "ppm"  },
                { label: "Duration", value: result.parameters.duration_hrs, unit: "hrs"  },
                { label: "SNR",      value: result.parameters.snr,          unit: ""     },
              ].map((m) => (
                <div key={m.label} className="bg-[#0a1628] border-t-2 border-t-cyan-400 border border-[#1a3a5c] rounded-lg p-4">
                  <p className="text-xs text-slate-400 font-mono uppercase tracking-widest mb-2">{m.label}</p>
                  <p className="text-2xl font-mono text-cyan-400">{Number(m.value).toFixed(3)}</p>
                  <p className="text-xs text-slate-500 font-mono mt-1">{m.unit}</p>
                </div>
              ))}
            </div>

            {/* Probability Bars */}
            <div className="bg-[#0a1628] border border-[#1a3a5c] rounded-lg p-6">
              <p className="text-xs text-slate-400 font-mono uppercase tracking-widest mb-4">
                Signal Classification
              </p>
              <div className="space-y-4">
                {Object.entries(result.probabilities).map(([label, value]) => (
                  <div key={label}>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-mono text-slate-300">{label}</span>
                      <span className="text-sm font-mono text-slate-400">{Number(value).toFixed(1)}%</span>
                    </div>
                    <div className="w-full h-2 bg-slate-800 rounded">
                      <div
                        className={`h-2 rounded transition-all duration-700 ${BAR_COLORS[label] ?? "bg-slate-400"}`}
                        style={{ width: `${value}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Signal Quality */}
            <div className="bg-[#0a1628] border border-[#1a3a5c] rounded-lg p-6">
              <p className="text-xs text-slate-400 font-mono uppercase tracking-widest mb-4">
                Signal Quality
              </p>
              <div className="flex items-center gap-4 mb-4">
                <span className={`px-3 py-1 rounded border text-sm font-mono
                  ${result.quality.confidence === "HIGH"   ? "border-green-400 text-green-400 bg-green-400/10"  : ""}
                  ${result.quality.confidence === "MEDIUM" ? "border-yellow-400 text-yellow-400 bg-yellow-400/10" : ""}
                  ${result.quality.confidence === "LOW"    ? "border-red-400 text-red-400 bg-red-400/10"    : ""}
                `}>
                  {result.quality.confidence}
                </span>
                <span className="text-slate-400 font-mono text-sm">
                  Score: {result.quality.score}/100
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {result.quality.flags.length === 0 ? (
                  <span className="text-green-400 text-sm font-mono">✓ No flags</span>
                ) : (
                  result.quality.flags.map((flag) => (
                    <span key={flag} className="px-2 py-1 rounded border border-yellow-400/40 bg-yellow-400/10 text-yellow-400 text-xs font-mono">
                      ⚠ {flag}
                    </span>
                  ))
                )}
              </div>
            </div>

            {/* Light Curve Figure */}
            {result.figure_url && (
              <div className="bg-[#0a1628] border border-cyan-400/40 rounded-lg p-6">
                <p className="text-xs text-slate-400 font-mono uppercase tracking-widest mb-4">
                  Analysis Report — TIC {result.tic_id}
                </p>
                <img
                  src={`http://127.0.0.1:8000${result.figure_url}`}
                  alt="PlanetX Analysis Report"
                  className="w-full rounded border border-[#1a3a5c]"
                />
              </div>
            )}

          </div>
        )}
      </div>
    </main>
  );
}