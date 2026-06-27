"use client";

import { useState } from "react";

export default function Dashboard() {
  const [ticId, setTicId] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState("");

  const runAnalysis = async () => {
  try {
    setLoading(true);
    setError("");
    setResult(null);

    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        tic_id: Number(ticId),
      }),
    });

    const data = await response.json();

    console.log("Status:", response.status);
    console.log("API Response:", data);

    if (!response.ok) {
      throw new Error(data.detail || "Backend error");
    }

    const history = JSON.parse(
      localStorage.getItem("PlanetX-history") || "[]"
    );

    history.unshift({
      ...data,
      date: new Date().toLocaleString(),
    });

    localStorage.setItem(
      "PlanetX-history",
      JSON.stringify(history.slice(0, 20))
    );

    setResult(data);
  } catch (err: any) {
    console.error(err);
    setError(err.message || "Failed to connect to backend.");
  } finally {
    setLoading(false);
  }
};

  return (
    <main className="min-h-screen text-white px-6 py-12">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold mb-8">
          PlanetX Dashboard
        </h1>

        <div
  className="
  bg-slate-900/60
  backdrop-blur-xl
  p-8
  rounded-3xl
  border
  border-cyan-500/30
  shadow-[0_0_50px_rgba(6,182,212,0.15)]
"
>
          <label className="block mb-3 text-slate-300">
            Enter TIC ID
          </label>

          <input
            type="number"
            placeholder="Example: 278892590"
            value={ticId}
            onChange={(e) => setTicId(e.target.value)}
            className="
              w-full
              p-4
              rounded-xl
              bg-slate-800
              border
              border-slate-600
              text-white
              mb-4
              outline-none
            "
          />

          <button
            onClick={runAnalysis}
            disabled={loading || !ticId}
            className="
              px-8
              py-4
              rounded-xl
              bg-gradient-to-r
              from-purple-600
              to-cyan-500
              hover:scale-105
              transition-all
              duration-300
              disabled:opacity-50
            "
          >
            {loading ? "Analyzing..." : "Run Analysis 🚀"}
          </button>
        </div>

        {loading && (
          <div className="mt-8">
            <p className="text-cyan-400 animate-pulse">
              Analyzing TESS Data...
            </p>

            <div className="w-full h-3 bg-slate-800 rounded-full mt-3 overflow-hidden">
              <div className="h-full w-full bg-gradient-to-r from-purple-500 to-cyan-400 animate-pulse"></div>
            </div>
          </div>
        )}

        {error && (
          <div className="mt-8 p-6 rounded-xl bg-red-900/30 border border-red-500">
            {error}
          </div>
        )}

        {result && (
          <div
  className="
  mt-8
  p-8
  rounded-3xl
  bg-slate-900/70
  backdrop-blur-xl
  border
  border-cyan-500/40
  shadow-[0_0_60px_rgba(6,182,212,0.15)]
"
>
            <h2 className="text-3xl font-bold mb-4">
              🪐 {result.classification}
            </h2>

            <div className="space-y-2">
              <p className="text-cyan-400">
                Confidence: {Number(result.confidence).toFixed(2)}%
              </p>

              <p>
                TIC ID: {result.tic_id}
              </p>
            </div>

            {result.parameters && (
              <div className="mt-6">
                <h3 className="text-xl font-semibold mb-4">
                  Detected Parameters
                </h3>

                <div className="grid md:grid-cols-2 gap-4">
                  <div className="bg-slate-800 p-4 rounded-xl">
                    Period: {result.parameters.period_days} days
                  </div>

                  <div className="bg-slate-800 p-4 rounded-xl">
                    Depth: {result.parameters.depth_ppm} ppm
                  </div>

                  <div className="bg-slate-800 p-4 rounded-xl">
                    Duration: {result.parameters.duration_hrs} hrs
                  </div>

                  <div className="bg-slate-800 p-4 rounded-xl">
                    SNR: {result.parameters.snr}
                  </div>
                </div>
              </div>
            )}

            {result.probabilities && (
              <div className="mt-8">
                <h3 className="text-xl font-bold mb-4">
                  Classification Probabilities
                </h3>

                {Object.entries(result.probabilities).map(
                  ([label, value]: any) => (
                    <div key={label} className="mb-4">
                      <div className="flex justify-between mb-1">
                        <span>{label}</span>
                        <span>
                          {Number(value).toFixed(1)}%
                        </span>
                      </div>

                      <div className="w-full h-3 bg-slate-700 rounded">
                        <div
                          className="h-3 bg-cyan-500 rounded"
                          style={{
                            width: `${value}%`,
                          }}
                        />
                      </div>
                    </div>
                  )
                )}
              </div>
            )}

            {result.quality && (
              <div className="mt-8 p-5 rounded-xl bg-slate-800">
                <h3 className="text-xl font-bold mb-3">
                  Signal Quality
                </h3>

                <pre className="text-sm text-slate-300 whitespace-pre-wrap">
                  {JSON.stringify(result.quality, null, 2)}
                </pre>
              </div>
            )}

            {result.figure_url && (
  <div className="mt-8">
    <h3 className="text-2xl font-bold mb-4">
      PlanetX Analysis Report
    </h3>

    <img
      src={`http://127.0.0.1:8000${result.figure_url}`}
      alt="PlanetX Report"
      className="
        w-full
        rounded-2xl
        border
        border-cyan-500
        shadow-[0_0_40px_rgba(6,182,212,0.4)]
      "
    />
  </div>
)}
          </div>
        )}
      </div>
    </main>
  );
}