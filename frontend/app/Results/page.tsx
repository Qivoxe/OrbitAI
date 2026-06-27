"use client";

import { useEffect, useState } from "react";

export default function Results() {
  const [history, setHistory] = useState<any[]>([]);

  useEffect(() => {
    const saved = JSON.parse(
      localStorage.getItem("PlanetX-history") || "[]"
    );

    setHistory(saved);
  }, []);

  return (
    <main className="min-h-screen text-white px-6 py-20">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-5xl font-bold mb-8">
          Analysis History
        </h1>

        <div className="grid gap-6">
          {history.map((item, index) => (
            <div
              key={index}
              className="
                bg-slate-900
                border
                border-cyan-500
                p-6
                rounded-2xl
              "
            >
              <h2 className="text-2xl font-bold">
                TIC {item.tic_id}
              </h2>

              <p className="text-cyan-400 mt-2">
                {item.classification}
              </p>

              <p>
                Confidence: {item.confidence}%
              </p>

              <p className="text-slate-400 mt-2">
                {item.date}
              </p>
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}