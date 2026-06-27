export default function Footer() {
return ( <footer className="border-t border-slate-800 mt-24"> <div className="max-w-7xl mx-auto px-6 py-12"> <div className="flex flex-col md:flex-row justify-between gap-10"> <div> <h2 className="text-3xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 bg-clip-text text-transparent">
PlanetX </h2>


        <p className="text-slate-400 mt-3 max-w-md">
          AI-powered exoplanet detection platform built using
          NASA TESS observations, machine learning, and
          transit analysis algorithms.
        </p>
      </div>

      <div className="text-slate-400">
        <p>🪐 NASA TESS Dataset</p>
        <p>⚡ FastAPI Backend</p>
        <p>🚀 Next.js + Tailwind</p>
        <p>🤖 Machine Learning Classification</p>
      </div>
    </div>

    <div className="border-t border-slate-800 mt-10 pt-6 text-center text-slate-500">
      © 2026 PlanetX • Discover New Worlds
    </div>
  </div>
</footer>


);
}
