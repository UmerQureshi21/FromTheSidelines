export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-4 py-20 overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-orange-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 " />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-yellow-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 " />
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
          <span className="text-black">SIDELINES</span>
        </h1>

        {/* Subheading */}
        <p
          className="poppins-light text-black mb-8 leading-relaxed max-w-2xl mx-auto"
          style={{ fontSize: "24px" }}
        >
          Elevate your backyard trickshots with{" "}
          <span className="text-orange-500 poppins-semibold">
            NBA-style commentary
          </span>
          . Upload a video. Get AI-powered hype. Share the glory.
        </p>

        {/* CTA Button */}
        <div
          className="group flex justify-center gap-[20px] relative px-8 md:px-12 py-4 md:py-5 bg-gradient-to-r from-orange-500 to-yellow-500 text-slate-950 poppins-bold rounded-full overflow-hidden transition-all duration-300 "
          style={{ fontSize: "18px" }}
        >
          <span className="relative text-[30px] z-10 poppins-bold flex items-center justify-center gap-2">
            TRY IT NOW
          </span>
          <svg
            className="w-10 h-10 transition-transform "
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
          <div className="absolute inset-0 bg-white opacity-0 transition-opacity" />
        </div>
      </div>
    </section>
  );
}
