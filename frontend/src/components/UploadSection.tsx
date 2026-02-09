import { useState } from "react";
import UploadVideo from "./UploadVideo";

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "fr", label: "French" },
  { code: "ar", label: "Arabic" },
  { code: "ur", label: "Urdu" },
  { code: "es", label: "Spanish" },
];

export default function UploadSection() {
  const [language, setLanguage] = useState("en");

  return (
    <section
      id="upload-section"
      className="relative  min-h-screen flex items-center justify-center px-4 py-20"
    >
      <div className="max-w-2xl w-full text-center">
        <h2
          className="poppins-thin mb-4 text-black"
          style={{ fontSize: "64px" }}
        >
          Upload Your Trickshot
        </h2>
        <p
          className="poppins-light text-gray-400 mb-8"
          style={{ fontSize: "18px" }}
        >
          Drop your video here to generate AI commentary.
        </p>

        {/* Language selector */}
        <div className="flex items-center justify-center gap-3 mb-12">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => setLanguage(lang.code)}
              className={`px-5 py-2 rounded-full poppins-semibold text-sm transition-all duration-200 ${
                language === lang.code
                  ? "bg-gradient-to-r from-orange-500 to-yellow-500 text-slate-950"
                  : "border border-orange-500/30 text-gray-500 hover:bg-orange-500/10"
              }`}
            >
              {lang.label}
            </button>
          ))}
        </div>

        <UploadVideo language={language} />
      </div>
    </section>
  );
}
