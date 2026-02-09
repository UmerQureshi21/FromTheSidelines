export default function Hero({ onTryIt }: { onTryIt: () => void }) {
  return (
    <section className="relative min-h-screen flex items-center justify-center px-5 sm:px-8 py-12 sm:py-20 overflow-hidden">
      {/* Animated gradient background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-48 sm:w-72 md:w-96 h-48 sm:h-72 md:h-96 bg-orange-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20" />
        <div className="absolute bottom-1/4 right-1/4 w-48 sm:w-72 md:w-96 h-48 sm:h-72 md:h-96 bg-yellow-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20" />
      </div>

      {/* Floating basketball elements */}
      <div className="absolute top-20 right-4 sm:right-10 opacity-10 text-6xl sm:text-7xl md:text-[128px]">
        🏀
      </div>
      <div className="absolute bottom-24 sm:bottom-32 left-4 sm:left-10 opacity-10 text-5xl sm:text-6xl md:text-[112px]">
        🏀
      </div>
      <div className="absolute top-1/2 right-1/4 text-4xl sm:text-5xl md:text-6xl opacity-10 animate-bounce hidden sm:block" style={{ animationDelay: "1s" }}>
        🏀
      </div>

      {/* Content */}
      <div className="relative z-10 max-w-4xl mx-auto text-center">
        {/* Main Headline */}
        <h1 className="poppins-thin mb-3 sm:mb-6 leading-[0.9] tracking-tight text-[15vw] sm:text-[80px] md:text-[110px] lg:text-[140px]">
          <span className="bg-gradient-to-r from-orange-400 via-yellow-300 to-orange-400 bg-clip-text text-transparent">
            FROM THE
          </span>
          <br />
          <span className="text-black">SIDELINES</span>
        </h1>

        {/* Subheading */}
        <p className="poppins-light text-black mb-5 sm:mb-8 leading-relaxed max-w-2xl mx-auto text-sm sm:text-lg md:text-2xl px-4 sm:px-2">
          Elevate your backyard trickshots with{" "}
          <span className="text-orange-500 poppins-semibold">
            NBA-style commentary
          </span>
          . Upload a video. Get AI-powered hype. Share the glory.
        </p>

        {/* CTA Button */}
        <div
          onClick={onTryIt}
          className="cursor-pointer group inline-flex justify-center gap-3 sm:gap-[20px] relative px-6 sm:px-8 md:px-12 py-3 sm:py-4 md:py-5 bg-gradient-to-r from-orange-500 to-yellow-500 text-slate-950 poppins-bold rounded-full overflow-hidden transition-all duration-300"
        >
          <span className="relative z-10 poppins-bold flex items-center justify-center gap-2 text-xl sm:text-2xl md:text-[30px]">
            TRY IT NOW
          </span>
          <div className="absolute inset-0 bg-white opacity-0 transition-opacity" />
        </div>
      </div>
    </section>
  );
}
