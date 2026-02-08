import { useEffect, useState } from "react";

function App() {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const scrollToUpload = () => {
    document
      .getElementById("upload-section")
      ?.scrollIntoView({ behavior: "smooth" });
  };

  return (
    <div className="bg-slate-950 poppins-regular text-white overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center px-4 py-20 overflow-hidden">
        {/* Animated gradient background */}
        <div className="absolute inset-0 overflow-hidden">
          <div
            className="absolute top-1/4 left-1/4 w-96 h-96 bg-orange-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"
            style={{ transform: `translateY(${scrollY * 0.5}px)` }}
          />
          <div
            className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-yellow-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"
            style={{ transform: `translateY(${scrollY * 0.3}px)` }}
          />
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-slate-950/80 to-slate-950" />
        </div>

        {/* Floating basketball elements */}
        <div
          className="absolute top-20 right-10 opacity-10"
          style={{ fontSize: "128px" }}
        >
          🏀
        </div>
        <div
          className="absolute bottom-32 left-10 opacity-10"
          style={{ fontSize: "112px" }}
        >
          🏀
        </div>
        <div
          className="absolute top-1/2 right-1/4 text-6xl opacity-10 animate-bounce"
          style={{ animationDelay: "1s" }}
        >
          🏀
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-4xl mx-auto text-center">
          {/* Main Headline */}
          <h1
            className="poppins-thin mb-6 leading-tight tracking-tight"
            style={{ fontSize: "140px" }}
          >
            <span className="bg-gradient-to-r from-orange-400 via-yellow-300 to-orange-400 bg-clip-text text-transparent">
              FROM THE
            </span>
            <br />
            <span className="text-white">SIDELINES</span>
          </h1>

          {/* Subheading */}
          <p
            className="poppins-light text-gray-300 mb-8 leading-relaxed max-w-2xl mx-auto"
            style={{ fontSize: "24px" }}
          >
            Turn your backyard trickshots into{" "}
            <span className="text-orange-300 poppins-semibold">
              NBA-style commentary
            </span>
            . Upload a video. Get AI-powered hype. Share the glory.
          </p>

          {/* CTA Button */}
          <button
            onClick={scrollToUpload}
            className="group relative px-8 md:px-12 py-4 md:py-5 bg-gradient-to-r from-orange-500 to-yellow-500 text-slate-950 poppins-bold rounded-full overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-orange-500/50 hover:scale-105 active:scale-95"
            style={{ fontSize: "18px" }}
          >
            <span className="relative z-10 flex items-center justify-center gap-2">
              TRY IT NOW
              <svg
                className="w-5 h-5 transition-transform group-hover:translate-y-1"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 19V5M5 12l7 7 7-7"
                />
              </svg>
            </span>
            <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity" />
          </button>
        </div>
      </section>

      {/* Upload Section (MVP placeholder) */}
      <section
        id="upload-section"
        className="relative min-h-screen bg-gradient-to-b from-slate-950 to-slate-900 flex items-center justify-center px-4 py-20"
      >
        <div className="max-w-2xl w-full text-center">
          <h2
            className="poppins-thin mb-4 text-white"
            style={{ fontSize: "64px" }}
          >
            Upload Your Trickshot
          </h2>
          <p
            className="poppins-light text-gray-400 mb-12"
            style={{ fontSize: "18px" }}
          >
            Coming soon. Drop your video here to generate AI commentary.
          </p>

          {/* Upload placeholder */}
          <div className="border-2 border-dashed border-orange-500/30 rounded-2xl p-12 bg-orange-500/5 hover:bg-orange-500/10 transition-colors cursor-pointer">
            <div style={{ fontSize: "96px" }} className="mb-4">
              📹
            </div>
            <p
              className="poppins-light text-gray-400"
              style={{ fontSize: "16px" }}
            >
              Video upload coming soon
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}

export default App;
