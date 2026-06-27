import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="fixed top-0 w-full bg-[#0A0F1F]/80 backdrop-blur-md border-b border-slate-800 z-50">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link
          href="/"
          className="text-2xl font-bold text-cyan-400"
        >
          PlanetX
        </Link>

        <div className="flex gap-8">
          <Link href="/" className="hover:text-cyan-400">
            Home
          </Link>

          <Link
            href="/Dashboard"
            className="hover:text-cyan-400"
          >
            Dashboard
          </Link>

          <Link
            href="/Analyze"
            className="hover:text-cyan-400"
          >
            Analyze
          </Link>

          <Link
            href="/Results"
            className="hover:text-cyan-400"
          >
            Results
          </Link>

          <Link
            href="/Docs"
            className="hover:text-cyan-400"
          >
            Docs
          </Link>
        </div>
      </div>
    </nav>
  );
}