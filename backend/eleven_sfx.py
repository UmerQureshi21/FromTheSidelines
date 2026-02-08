# eleven_sfx.py, makes the crowd noises mp3 file
import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api.elevenlabs.io/v1"

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing ELEVENLABS_API_KEY in environment or .env")


def generate_crowd_sfx_mp3(
    prompt: str,
    out_path: str = "crowd.mp3",
    duration_seconds: float | None = 10.0,
    loop: bool = False,
    prompt_influence: float = 0.3,
    output_format: str = "mp3_44100_128",
    model_id: str = "eleven_text_to_sound_v2",
) -> str:
    """
    Generates a crowd/ambience sound effect from a text prompt and saves it as an MP3.

    Endpoint: POST /v1/sound-generation :contentReference[oaicite:2]{index=2}
    """
    url = f"{BASE_URL}/sound-generation?output_format={output_format}"  # :contentReference[oaicite:3]{index=3}
    headers = {
        "xi-api-key": API_KEY,  # required :contentReference[oaicite:4]{index=4}
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": prompt,  # required :contentReference[oaicite:5]{index=5}
        "model_id": model_id,  # defaults to eleven_text_to_sound_v2 :contentReference[oaicite:6]{index=6}
        "loop": loop,  # optional :contentReference[oaicite:7]{index=7}
        "duration_seconds": duration_seconds,  # optional :contentReference[oaicite:8]{index=8}
        "prompt_influence": prompt_influence,  # optional :contentReference[oaicite:9]{index=9}
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()

    with open(out_path, "wb") as f:
        f.write(resp.content)

    return out_path
