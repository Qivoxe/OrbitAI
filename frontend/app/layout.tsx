import "./globals.css";
import Navbar from "@/components/Navbar";
import SpaceBackground from "@/components/SpaceBackground";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="text-white overflow-x-hidden">
        <SpaceBackground />

        <Navbar />

        <div className="pt-20">
          {children}
        </div>
      </body>
    </html>
  );
}