from fastapi import FastAPI, UploadFile, File, Form, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import asyncio

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

# Active WebSocket connections keyed by client_id
ws_connections: dict[str, WebSocket] = {}


async def send_progress(client_id: str, step: int, message: str):
    ws = ws_connections.get(client_id)
    if ws:
        try:
            await ws.send_json({"step": step, "total": 5, "message": message})
        except Exception:
            pass


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    ws_connections[client_id] = websocket
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        pass
    finally:
        ws_connections.pop(client_id, None)


@app.post("/generate-commentary")
async def generate_commentary(
    video: UploadFile = File(...),
    language: str = Form("en"),
    trickshot_name: str = Form(""),
    client_id: str = Form(""),
):
    """
    Upload a trickshot video and get back a commentated version with crowd noise.
    Progress updates sent via WebSocket if client_id is connected.
    """

    temp_dir = tempfile.mkdtemp()

    try:
        # Save uploaded video
        video_path = os.path.join(temp_dir, "trickshot.mp4")
        with open(video_path, "wb") as f:
            f.write(await video.read())

        print(f"Video saved: {video_path}")

        # Step 1: Analyze video
        await send_progress(client_id, 1, "Analyzing trickshot...")
        print("Step 1: Analyzing video...")
        summary = await asyncio.to_thread(getSummary, video_path)

        # Step 2: Generate script
        await send_progress(client_id, 2, "Generating commentary script...")
        print("Step 2: Generating commentary script...")
        script = await asyncio.to_thread(getScript, summary, language, trickshot_name, video_path)

        # Step 3: Generate commentary audio
        await send_progress(client_id, 3, "Generating voice over...")
        print("Step 3: Generating commentary audio...")
        voice_file = os.path.join(temp_dir, "trickshot-voice.mp3")
        await asyncio.to_thread(generate_chris_mp3, script, out_path=voice_file)

        # Step 4: Generate crowd noise
        await send_progress(client_id, 4, "Generating crowd audio...")
        print("Step 4: Generating crowd noise...")
        crowd_prompt = (
            "Background audio of a crowded basketball arena as heard through a TV broadcast. "
            "Include cheering, clapping, chanting, and natural crowd reactions. "
            "No narration or music."
        )
        crowd_file = os.path.join(temp_dir, "crowd-noises.mp3")
        await asyncio.to_thread(
            generate_crowd_sfx_mp3, crowd_prompt, crowd_file,
            duration_seconds=20, loop=False
        )

        # Step 5: Process video with audio
        await send_progress(client_id, 5, "Combining final video...")
        print("Step 5: Processing video with audio...")

        def run_video_processing():
            original_cwd = os.getcwd()
            os.chdir(temp_dir)
            try:
                processor = VideoProcessor(video_path, voice_file, crowd_file)
                processor.process(cleanup=True)
                return processor.final_video
            finally:
                os.chdir(original_cwd)

        final_video_name = await asyncio.to_thread(run_video_processing)
        final_video = os.path.join(temp_dir, final_video_name)

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

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
