import { useState, useRef, type ChangeEvent} from "react";

const STEPS = [
  "Analyzing trickshot",
  "Writing commentary script",
  "Generating voice over",
  "Generating crowd audio",
  "Combining final video",
];

function UploadVideo({ language, trickshotName }: { language: string; trickshotName: string }) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<number>(0);
  const [stepMessage, setStepMessage] = useState<string>("");
  const wsRef = useRef<WebSocket | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>): void => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile) {
      setFile(selectedFile);
      setError(null);
    }
  };

  const handleDragOver = (e: any): void => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e: any): void => {
    e.preventDefault();
    e.stopPropagation();
    const droppedFile = e.dataTransfer.files?.[0];
    if (droppedFile && droppedFile.type.startsWith("video/")) {
      setFile(droppedFile);
      setError(null);
    } else {
      setError("Please drop a video file");
    }
  };

  const handleUpload = async (): Promise<void> => {
    if (!file) {
      setError("Please select a video");
      return;
    }

    setLoading(true);
    setError(null);
    setCurrentStep(0);
    setStepMessage("Uploading video...");

    const clientId = crypto.randomUUID();

    // Open WebSocket for progress updates
    const ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setCurrentStep(data.step);
      setStepMessage(data.message);
    };

    // Wait for WS to connect
    await new Promise<void>((resolve, reject) => {
      ws.onopen = () => resolve();
      ws.onerror = () => reject(new Error("WebSocket connection failed"));
    });

    try {
      const formData = new FormData();
      formData.append("video", file);
      formData.append("language", language);
      formData.append("client_id", clientId);
      if (trickshotName.trim()) {
        formData.append("trickshot_name", trickshotName.trim());
      }

      const response = await fetch("http://localhost:8000/generate-commentary", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Upload failed: ${response.statusText}`);
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      setVideoUrl(url);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Something went wrong";
      setError(errorMessage);
    } finally {
      ws.close();
      wsRef.current = null;
      setLoading(false);
      setCurrentStep(0);
      setStepMessage("");
    }
  };

  const handleReset = (): void => {
    setVideoUrl(null);
    setFile(null);
    setError(null);
  };

  const handleDownload = (): void => {
    if (videoUrl) {
      const link = document.createElement("a");
      link.href = videoUrl;
      link.download = "commentated-trickshot.mp4";
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  const progressPercent = (currentStep / 5) * 100;

  return (
    <div className="w-full max-w-2xl mx-auto">
      {!videoUrl ? (
        <div className="space-y-6">
          {loading ? (
            /* Progress bar while processing */
            <div className="border-2 border-orange-500/30 rounded-2xl p-10 bg-orange-500/5 space-y-6">
              {/* Step label */}
              <p
                className="text-center poppins-semibold"
                style={{
                  fontSize: 20,
                  background: "linear-gradient(to right, #f97316, #eab308)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                {stepMessage}
              </p>

              {/* Progress bar */}
              <div className="w-full h-4 rounded-full bg-gray-800 overflow-hidden">
                <div
                  className="h-full rounded-full transition-all duration-700 ease-out"
                  style={{
                    width: `${progressPercent}%`,
                    background: "linear-gradient(to right, #f97316, #eab308)",
                  }}
                />
              </div>

              {/* Step list */}
              <div className="space-y-2">
                {STEPS.map((label, i) => {
                  const stepNum = i + 1;
                  const isDone = currentStep > stepNum;
                  const isActive = currentStep === stepNum;
                  return (
                    <div key={i} className="flex items-center gap-3">
                      {/* Icon */}
                      {isDone ? (
                        <svg className="w-5 h-5 flex-shrink-0" style={{ color: "#22c55e" }} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M5 13l4 4L19 7" />
                        </svg>
                      ) : isActive ? (
                        <div className="w-5 h-5 flex-shrink-0 flex items-center justify-center">
                          <div
                            className="w-3 h-3 rounded-full animate-pulse"
                            style={{ backgroundColor: "#f97316" }}
                          />
                        </div>
                      ) : (
                        <div className="w-5 h-5 flex-shrink-0 flex items-center justify-center">
                          <div
                            className="w-2 h-2 rounded-full"
                            style={{ backgroundColor: "#4b5563" }}
                          />
                        </div>
                      )}
                      {/* Label */}
                      <span
                        className="poppins-regular"
                        style={{
                          fontSize: 14,
                          color: isDone ? "#22c55e" : isActive ? "#f97316" : "#6b7280",
                        }}
                      >
                        {label}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>
          ) : (
            /* Upload area */
            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className="border-2 border-dashed border-orange-500/30 rounded-2xl p-12 bg-orange-500/5 hover:bg-orange-500/10 transition-colors cursor-pointer"
            >
              <label className="cursor-pointer block">
                <div className="text-center">
                  <div style={{ fontSize: "96px" }} className="mb-4">

                  </div>
                  <p className="poppins-semibold text-black mb-2" style={{ fontSize: "18px" }}>
                    {file ? file.name : "Drag and drop your video here"}
                  </p>
                  <p className="poppins-light text-gray-400" style={{ fontSize: "14px" }}>
                    {file ? "Click to change" : "or click to select a file"}
                  </p>
                  <input
                    type="file"
                    accept="video/*"
                    onChange={handleFileChange}
                    className="hidden"
                  />
                </div>
              </label>
            </div>
          )}

          {/* Error message */}
          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-lg">
              <p className="poppins-regular text-red-400" style={{ fontSize: "14px" }}>
                {error}
              </p>
            </div>
          )}

          {/* Upload button */}
          <button
            onClick={handleUpload}
            disabled={!file || loading}
            className="w-full px-6 py-3 bg-gradient-to-r from-orange-500 to-yellow-500 text-slate-950 poppins-semibold rounded-full transition-all duration-300 hover:shadow-lg hover:shadow-orange-500/30 disabled:opacity-40 disabled:cursor-not-allowed"
            style={{ fontSize: "15px", letterSpacing: "0.5px" }}
          >
            {loading ? "Processing..." : "Generate Commentary"}
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Result video */}
          <div className="rounded-2xl overflow-hidden bg-black">
            <video
              src={videoUrl}
              controls
              className="w-full"
              style={{ maxHeight: "600px" }}
            />
          </div>

          {/* Download button */}
          <button
            onClick={handleDownload}
            className="block w-full group relative px-8 py-4 bg-gradient-to-r from-orange-500 to-yellow-500 text-slate-950 poppins-bold rounded-full overflow-hidden transition-all duration-300 hover:shadow-2xl hover:shadow-orange-500/50"
            style={{ fontSize: "18px" }}
          >
            <span className="relative z-10 flex items-center justify-center gap-2">
              DOWNLOAD VIDEO
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>
            </span>
            <div className="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 transition-opacity" />
          </button>

          {/* Try another */}
          <button
            onClick={handleReset}
            className="w-full poppins-semibold px-8 py-4 border-2 border-orange-500/50 text-orange-400 rounded-full hover:bg-orange-500/10 transition-colors"
            style={{ fontSize: "16px" }}
          >
            TRY ANOTHER TRICKSHOT
          </button>
        </div>
      )}
    </div>
  );
}

export default UploadVideo;
