import UploadVideo from "./UploadVideo";

export default function UploadSection() {
  return (
    <section
      id="upload-section"
      className="relative  min-h-screen bg-gradient-to-b from-[rgb(20,20,20)] to-[rgb(0,0,0)] flex items-center justify-center px-4 py-20"
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

        <UploadVideo />
      </div>
    </section>
  );
}
