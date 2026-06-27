import Link from "next/link";

export default function Hero() {
return (
   <section className="relative min-h-screen flex items-center overflow-hidden">
{/* Background Glow */} 
<div className="absolute top-0 left-1/2 -translate-x-1/2 w-[900px] h-[900px] rounded-full bg-gradient-to-r from-cyan-500/20 via-purple-500/20 to-pink-500/20 blur-[180px]" />


  {/* Planet */}
  <div className="absolute right-[-100px] top-1/2 -translate-y-1/2 w-[500px] h-[500px] rounded-full bg-gradient-to-br from-cyan-300 via-blue-500 to-purple-800 shadow-[0_0_120px_rgba(34,211,238,0.4)] opacity-80">
    <div className="absolute inset-0 border border-cyan-200/30 rounded-full scale-125 rotate-12" >
  </div>
  </div>

  <div className="relative z-10 max-w-7xl mx-auto px-6 w-full">
    <div className="max-w-3xl">
      {/* Badge */}
      <div className="inline-flex items-center gap-2 px-5 py-2 rounded-full border border-cyan-500/30 bg-slate-900/50 backdrop-blur-xl text-cyan-300 mb-8">
        🚀 NASA TESS + AI Powered Detection
      </div>

      {/* Heading */}
      <div className="mb-10">
  <h1 className="text-6xl font-black">
    Mission Control
  </h1>

  <p className="text-slate-400 mt-3 text-xl">
    Analyze NASA TESS stars and discover potential exoplanets.
  </p>
</div>

      {/* Subtitle */}
      <p className="mt-8 text-xl md:text-2xl text-slate-300 leading-relaxed max-w-2xl">
        Discover hidden exoplanets using machine learning,
        transit detection algorithms, and NASA TESS observations.
      </p>

      {/* Buttons */}
      <div className="mt-10 flex flex-wrap gap-4">
        <Link href="/Dashboard">
          <button className="px-8 py-4 rounded-xl bg-gradient-to-r from-purple-600 to-cyan-500 font-semibold hover:scale-105 transition-all shadow-[0_0_40px_rgba(139,92,246,0.5)]">
            Analyze Star 🚀
          </button>
        </Link>

        <Link href="/Results">
          <button className="px-8 py-4 rounded-xl border border-cyan-500 bg-slate-900/40 backdrop-blur-xl hover:bg-cyan-500/10 transition-all">
            View Results 📊
          </button>
        </Link>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-16">
        <div
  className="
  p-6
  rounded-3xl
  bg-slate-900/50
  backdrop-blur-xl
  border
  border-cyan-500/30
  shadow-[0_0_30px_rgba(6,182,212,0.25)]
  hover:scale-105
  hover:-translate-y-2
  transition-all
  duration-300
"
>
          <h3 className="text-3xl font-bold text-cyan-400">196k+</h3>
          <p className="text-slate-400">Stars Processed</p>
        </div>

        <div
  className="
  p-6
  rounded-3xl
  bg-slate-900/50
  backdrop-blur-xl
  border
  border-cyan-500/30
  shadow-[0_0_30px_rgba(6,182,212,0.25)]
  hover:scale-105
  hover:-translate-y-2
  transition-all
  duration-300
"
>
          <h3 className="text-3xl font-bold text-cyan-400">97%</h3>
          <p className="text-slate-400">Accuracy</p>
        </div>

        <div
  className="
  p-6
  rounded-3xl
  bg-slate-900/50
  backdrop-blur-xl
  border
  border-cyan-500/30
  shadow-[0_0_30px_rgba(6,182,212,0.25)]
  hover:scale-105
  hover:-translate-y-2
  transition-all
  duration-300
"
>
          <h3 className="text-3xl font-bold text-cyan-400">4</h3>
          <p className="text-slate-400">Signal Classes</p>
        </div>

        <div
  className="
  p-6
  rounded-3xl
  bg-slate-900/50
  backdrop-blur-xl
  border
  border-cyan-500/30
  shadow-[0_0_30px_rgba(6,182,212,0.25)]
  hover:scale-105
  hover:-translate-y-2
  transition-all
  duration-300
"
>
          <h3 className="text-3xl font-bold text-cyan-400">NASA</h3>
          <p className="text-slate-400">TESS Data</p>
        </div>
      </div>
    </div>
  </div>
</section>


);
}
