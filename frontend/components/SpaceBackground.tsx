export default function SpaceBackground() {
  return (
    <div className="fixed inset-0 overflow-hidden -z-50">
      {/* Deep Space */}
      <div className="absolute inset-0 bg-[#050816]" />

      {/* Nebula Glow */}
      <div className="absolute top-20 left-20 w-[500px] h-[500px] rounded-full bg-purple-600/20 blur-[150px]" />

      <div className="absolute bottom-20 right-20 w-[600px] h-[600px] rounded-full bg-cyan-500/20 blur-[180px]" />

      <div className="absolute top-1/2 left-1/2 w-[400px] h-[400px] rounded-full bg-pink-500/10 blur-[120px]" />

      {/* Main Planet */}
      <div
        className="
        absolute
        top-24
        right-24
        w-80
        h-80
        rounded-full
        bg-gradient-to-br
        from-cyan-300
        via-blue-500
        to-purple-800
        shadow-[0_0_100px_rgba(34,211,238,0.5)]
        animate-[float_8s_ease-in-out_infinite]
      "
      >
        {/* Highlight */}
        <div
          className="
          absolute
          top-10
          left-12
          w-24
          h-24
          rounded-full
          bg-white/20
          blur-xl
        "
        />

        {/* Saturn Ring */}
        <div
          className="
          absolute
          inset-0
          border
          border-cyan-200/30
          rounded-full
          scale-125
          rotate-12
        "
        />

        {/* Moon */}
        <div
          className="
          absolute
          w-5
          h-5
          bg-white
          rounded-full
          animate-[orbit_12s_linear_infinite]
        "
        />
      </div>

      {/* Small Planet */}
      <div
        className="
        absolute
        bottom-20
        left-20
        w-44
        h-44
        rounded-full
        bg-gradient-to-br
        from-purple-500
        to-pink-700
        shadow-[0_0_80px_rgba(168,85,247,0.5)]
        animate-[float_10s_ease-in-out_infinite]
      "
      />

      {/* Orbit Rings */}
      <div
        className="
        absolute
        top-32
        right-12
        w-[380px]
        h-[120px]
        border
        border-cyan-300/30
        rounded-full
        rotate-12
      "
      />

      <div
        className="
        absolute
        top-28
        right-8
        w-[450px]
        h-[160px]
        border
        border-purple-400/20
        rounded-full
        -rotate-12
      "
      />

      <div
        className="
        absolute
        top-36
        right-16
        w-[320px]
        h-[90px]
        border
        border-cyan-300/20
        rounded-full
        rotate-12
      "
      />

      {/* Stars */}
      {[...Array(120)].map((_, i) => (
        <div
          key={i}
          className="absolute bg-white rounded-full animate-pulse"
          style={{
            width: `${Math.random() * 3 + 1}px`,
            height: `${Math.random() * 3 + 1}px`,
            left: `${Math.random() * 100}%`,
            top: `${Math.random() * 100}%`,
            opacity: Math.random(),
          }}
        />
      ))}

      {/* Shooting Star */}
      <div
        className="
        absolute
        top-20
        left-0
        w-72
        h-[3px]
        bg-gradient-to-r
        from-white
        via-cyan-300
        to-transparent
        opacity-70
        animate-[shoot_6s_linear_infinite]
      "
      />
    </div>
  );
}