import Hero from "@/components/Hero";
import Pipeline from "@/components/Pipeline";
import Footer from "@/components/Footer";

export default function Home() {
  return (
    <main className="bg-[#050816] text-white min-h-screen">
      <Hero />
      <Pipeline />
      <Footer />
    </main>
  );
}