"use client";

import Link from "next/link";

export default function Analyze() {
  return (
    <main className="min-h-screen  text-white px-6 py-24">
      <div className="max-w-5xl mx-auto text-center">
        <h1 className="text-6xl font-bold mb-6">
          Analyze New Star
        </h1>

        <p className="text-slate-400 text-xl mb-10">
          Launch PlanetX's exoplanet detection pipeline
          using NASA TESS observations.
        </p>

        <Link href="/Dashboard">
          <button
            className="
              px-10
              py-5
              rounded-xl
              bg-gradient-to-r
              from-purple-600
              to-cyan-500
              hover:scale-105
              transition-all
            "
          >
            Open Dashboard 🚀
          </button>
        </Link>
      </div>
    </main>
  );
}