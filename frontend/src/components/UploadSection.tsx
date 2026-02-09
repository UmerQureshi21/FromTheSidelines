import { useState, useEffect } from "react";
import UploadVideo from "./UploadVideo";

const LANGUAGES = [
  { code: "en", label: "English" },
  { code: "fr", label: "French" },
  { code: "ar", label: "Arabic" },
  { code: "ur", label: "Urdu" },
  { code: "es", label: "Spanish" },
];

export default function UploadSection({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  const [language, setLanguage] = useState("en");
  const [trickshotName, setTrickshotName] = useState("");

  // Close on Escape key
  useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    if (isOpen) window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      onClick={onClose}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />

      {/* Modal */}
      <div
        className="relative w-full max-w-xl bg-white rounded-3xl p-8 shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 w-8 h-8 flex items-center justify-center rounded-full text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        <h2
          className="poppins-thin mb-2 text-black text-center"
          style={{ fontSize: "36px" }}
        >
          Upload Your Trickshot
        </h2>
        <p
          className="poppins-light text-gray-400 mb-6 text-center"
          style={{ fontSize: "15px" }}
        >
          Drop your video here to generate AI commentary.
        </p>

        {/* Language selector */}
        <div className="flex items-center justify-center gap-2 mb-6 flex-wrap">
          {LANGUAGES.map((lang) => (
            <button
              key={lang.code}
              onClick={() => setLanguage(lang.code)}
              className={`px-4 py-1.5 rounded-full poppins-semibold text-sm transition-all duration-200 ${
                language === lang.code
                  ? "bg-gradient-to-r from-orange-500 to-yellow-500 text-slate-950"
                  : "border border-orange-500/30 text-gray-500 hover:bg-orange-500/10"
              }`}
            >
              {lang.label}
            </button>
          ))}
        </div>

        {/* Trickshot name input */}
        <input
          type="text"
          value={trickshotName}
          onChange={(e) => setTrickshotName(e.target.value)}
          placeholder="Name your trickshot (optional)"
          className="w-full mb-5 px-5 py-3 rounded-full border border-orange-500/30 bg-orange-500/5 text-black poppins-regular placeholder-gray-400 outline-none focus:border-orange-500 transition-colors"
          style={{ fontSize: "14px" }}
        />

        <UploadVideo language={language} trickshotName={trickshotName} />
      </div>
    </div>
  );
}
