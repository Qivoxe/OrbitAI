export default function Pipeline() {
const steps = [
{ icon: "📡", title: "NASA TESS Data" },
{ icon: "🧹", title: "Lightcurve Cleaning" },
{ icon: "📈", title: "Transit Detection" },
{ icon: "🤖", title: "AI Classification" },
{ icon: "🪐", title: "Exoplanet Report" },
];

return ( <section className="max-w-7xl mx-auto px-6 py-24 text-center"> <h2 className="text-6xl font-black text-center mb-6"> <span className="bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-400 bg-clip-text text-transparent">
Detection Pipeline </span> </h2>


  <p className="text-center text-slate-400 max-w-2xl mx-auto mb-20">
    From NASA observations to AI-powered exoplanet classification.
  </p>

  <div className="flex flex-col md:flex-row items-center justify-center gap-8 flex-wrap">
    {steps.map((step, index) => (
      <div
        key={step.title}
        className="flex items-center justify-center"
      >
        <div
          className="
          w-60
          p-8
          rounded-3xl
          bg-slate-900/40
          backdrop-blur-xl
          border
          border-cyan-500/20
          shadow-[0_0_30px_rgba(6,182,212,0.15)]
          hover:shadow-[0_0_50px_rgba(6,182,212,0.35)]
          hover:-translate-y-3
          hover:scale-105
          transition-all
          duration-500
        "
        >
          <div
            className="
            w-14
            h-14
            mx-auto
            mb-4
            rounded-full
            flex
            items-center
            justify-center
            bg-gradient-to-r
            from-cyan-500
            to-purple-500
            font-black
            text-xl
          "
          >
            {index + 1}
          </div>

          <div className="text-5xl mb-4 text-center">
            {step.icon}
          </div>

          <p className="text-white font-medium text-center">
            {step.title}
          </p>
        </div>

        {index < steps.length - 1 && (
          <div className="hidden md:flex items-center">
            <div
              className="
              w-20
              h-[3px]
              bg-gradient-to-r
              from-cyan-400
              via-blue-400
              to-purple-500
              shadow-[0_0_20px_rgba(6,182,212,0.5)]
            "
            />
          </div>
        )}
      </div>
    ))}
  </div>
</section>


);
}
