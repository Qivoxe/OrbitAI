export default function Docs() {
  return (
    <main className="min-h-screen  text-white px-6 py-24">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-5xl font-bold mb-10">
          PlanetX Documentation
        </h1>

        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-4">
            About PlanetX
          </h2>

          <p className="text-slate-400">
            PlanetX is an AI-powered exoplanet
            detection platform that analyzes
            NASA TESS light curves and identifies
            transit signals automatically.
          </p>
        </section>

        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-4">
            Detection Pipeline
          </h2>

          <ul className="space-y-3 text-slate-400">
            <li>1. Download TESS Data</li>
            <li>2. Clean Light Curve</li>
            <li>3. Transit Detection (BLS)</li>
            <li>4. Feature Extraction</li>
            <li>5. AI Classification</li>
            <li>6. Report Generation</li>
          </ul>
        </section>

        <section className="mb-12">
          <h2 className="text-3xl font-bold mb-4">
            Signal Classes
          </h2>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="bg-slate-900/50 backdrop-blur-xl p-4 rounded-xl">
              🪐 Planet Candidate
            </div>

            <div className="bg-slate-900/50 backdrop-blur-xl p-4 rounded-xl">
              🌗 Eclipsing Binary
            </div>

            <div className="bg-slate-900/50 backdrop-blur-xl p-4 rounded-xl">
              ⭐ Blend
            </div>

            <div className="bg-slate-900/50 backdrop-blur-xl p-4 rounded-xl">
              📡 Noise
            </div>
          </div>
        </section>

        <section>
          <h2 className="text-3xl font-bold mb-4">
            API Endpoints
          </h2>

          <div className="bg-slate-900 p-6 rounded-xl">
            <p>POST /analyze</p>
            <p>GET /results</p>
            <p>GET /result/{`{tic_id}`}</p>
          </div>
        </section>
      </div>
    </main>
  );
}