from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
from pathlib import Path
import shutil

from trickshot_summary import getSummary
from commentator_script import getScript
from eleven_sfx import generate_crowd_sfx_mp3
from tts_chris import generate_chris_mp3
from video_processor import VideoProcessor

app = FastAPI(title="From the Sidelines", description="AI-powered trickshot commentary generator")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate-commentary")
async def generate_commentary(video: UploadFile = File(...), language: str = Form("en")):
    """
    Upload a trickshot video and get back a commentated version with crowd noise.
    
    Returns the final video file with AI commentary and crowd audio.
    """
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Save uploaded video
        video_path = os.path.join(temp_dir, "trickshot.mp4")
        with open(video_path, "wb") as f:
            f.write(await video.read())
        
        print(f"Video saved: {video_path}")
        
        # Step 1: Analyze video
        print("Step 1: Analyzing video...")
        summary = getSummary(video_path)
        
        # Step 2: Generate script
        print("Step 2: Generating commentary script...")
        script = getScript(summary, language)
        
        # Step 3: Generate commentary audio
        print("Step 3: Generating commentary audio...")
        voice_file = os.path.join(temp_dir, "trickshot-voice.mp3")
        generate_chris_mp3(script, out_path=voice_file)
        
        # Step 4: Generate crowd noise
        print("Step 4: Generating crowd noise...")
        crowd_prompt = (
            "Background audio of a crowded basketball arena as heard through a TV broadcast. "
            "Include cheering, clapping, chanting, and natural crowd reactions. "
            "No narration or music."
        )
        crowd_file = os.path.join(temp_dir, "crowd-noises.mp3")
        generate_crowd_sfx_mp3(crowd_prompt, crowd_file, duration_seconds=20, loop=False)
        
        # Step 5: Process video with audio
        print("Step 5: Processing video with audio...")
        # Change to temp directory so VideoProcessor outputs files there
        original_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        processor = VideoProcessor(video_path, voice_file, crowd_file)
        processor.process(cleanup=True)
        
        os.chdir(original_cwd)
        
        # Get final video path
        final_video = os.path.join(temp_dir, processor.final_video)
        
        print(f"Final video: {final_video}")
        
        # Return the file
        return FileResponse(
            final_video,
            media_type="video/mp4",
            filename="commentated-trickshot.mp4"
        )
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    # finally:
    #     # Clean up temp directory
    #     shutil.rmtree(temp_dir, ignore_errors=True)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)