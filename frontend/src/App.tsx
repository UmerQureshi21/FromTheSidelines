import Hero from "./components/Hero";
import UploadVideo from "./components/UploadVideo";

function App() {
  return (
    <div className="poppins-regular text-white overflow-hidden">
      <Hero />

      <div className="h-[200px]"></div>

      <UploadVideo />
      <div className="h-[200px]"></div>
    </div>
  );
}

export default App;
