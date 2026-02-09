import { useState } from "react";
import Hero from "./components/Hero";
import UploadSection from "./components/UploadSection";

function App() {
  const [showUpload, setShowUpload] = useState(false);

  return (
    <div className="poppins-regular text-white overflow-hidden">
      <Hero onTryIt={() => setShowUpload(true)} />

      <UploadSection isOpen={showUpload} onClose={() => setShowUpload(false)} />
    </div>
  );
}

export default App;
