# makes a mp3 file of the commentary to be overlayed on the video
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing ELEVENLABS_API_KEY in environment or .env")

BASE_URL = "https://api.elevenlabs.io/v1"

# Hardcode Chris voice id (works now that you're paid)
CHRIS_VOICE_ID = "Anr9GtYh2VRXxiPplzxM"


def generate_chris_mp3(
    text: str,
    out_path: str = "chris.mp3",
    *,
    stability: float = 0.55,
    similarity_boost: float = 0.85,
    style: float = 0.35,
    model_id: str = "eleven_multilingual_v2",
    output_format: str = "mp3_44100_128",
) -> str:
    print(f"This is what Chris will say: \n\n{text}")

    """
    Generate an MP3 using the ElevenLabs 'Chris - Sports Commentator' voice.

    Args:
        text: What Chris should say.
        out_path: Where to save the mp3.
        stability/similarity_boost/style: Voice settings (like UI sliders).
        model_id: ElevenLabs model id.
        output_format: Audio output format.

    Returns:
        The path to the saved mp3 file.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must be a non-empty string")

    url = f"{BASE_URL}/text-to-speech/{CHRIS_VOICE_ID}?output_format={output_format}"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": text,
        "model_id": model_id,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
            "style": style,
        },
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)

    # Helpful error message without printing mp3 bytes
    if not resp.ok:
        raise RuntimeError(f"ElevenLabs TTS failed ({resp.status_code}): {resp.text}")

    with open(out_path, "wb") as f:
        f.write(resp.content)

    return out_path
