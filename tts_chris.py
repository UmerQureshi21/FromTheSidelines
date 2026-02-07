import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY:
    raise SystemExit("Missing ELEVENLABS_API_KEY in environment or .env")

BASE_URL = "https://api.elevenlabs.io/v1"


def find_voice_id_by_name(target_name: str) -> str | None:
    """
    Tries to find a voice_id by matching the voice name (case-insensitive).
    Uses the voices list endpoint. (Your account may see default + saved voices.)
    """
    url = f"{BASE_URL}/voices"
    headers = {"xi-api-key": API_KEY}
    r = requests.get(url, headers=headers, timeout=30)
    r.raise_for_status()

    data = r.json()
    voices = data.get("voices", [])

    target = target_name.strip().lower()
    for v in voices:
        name = (v.get("name") or "").strip().lower()
        if name == target:
            return v.get("voice_id")

    # fallback: partial match
    for v in voices:
        name = (v.get("name") or "").strip().lower()
        if target in name:
            return v.get("voice_id")

    return None


def tts_to_mp3(voice_id: str, text: str, out_path: str = "output.mp3") -> None:
    """
    Calls ElevenLabs Create speech endpoint and writes returned MP3 bytes to disk.
    """
    # Docs show output_format as a query param (default mp3_44100_128). :contentReference[oaicite:3]{index=3}
    url = f"{BASE_URL}/text-to-speech/{voice_id}?output_format=mp3_44100_128"

    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json",
        # optional, but makes intent clear:
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": text,
        # Match what your UI screenshot shows:
        "model_id": "eleven_multilingual_v2",  # :contentReference[oaicite:4]{index=4}
        # Optional: tune to taste (these correspond to the UI sliders)
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.85,
            "style": 0.35,
            # "use_speaker_boost": True,  # include if you want; may depend on voice/model
        },
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    print("Status:", resp.status_code)
    print("Response:", resp.text)
    resp.raise_for_status()


    with open(out_path, "wb") as f:
        f.write(resp.content)

    print(f"Saved MP3 -> {out_path}")


if __name__ == "__main__":
    # Usage:
    #   python tts_chris.py "YOUR MONOLOGUE HERE" out.mp3
    text = sys.argv[1] if len(sys.argv) > 1 else None
    out = sys.argv[2] if len(sys.argv) > 2 else "output.mp3"

    if not text:
        raise SystemExit('Usage: python tts_chris.py "YOUR MONOLOGUE HERE" [out.mp3]')

    voice_name = "Chris - Sports Commentator"
    voice_id = "Anr9GtYh2VRXxiPplzxM"

    if not voice_id:
        raise SystemExit(
            f"Could not find voice named '{voice_name}'.\n"
            "Go to ElevenLabs UI and copy the voice_id (⋯ -> Copy voice ID), then hardcode it.\n"
            "Help: https://help.elevenlabs.io/.../How-do-I-find-the-voice-ID..."
        )

    tts_to_mp3(voice_id, text, out)
