from dotenv import load_dotenv
from openai import OpenAI
import os
import subprocess

load_dotenv()  # loads variables from .env into environment

client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=os.getenv("FEATHERLESS_API_KEY"),
)

LANGUAGE_NAMES = {
    "en": "English",
    "fr": "French",
    "ar": "Arabic",
    "ur": "Urdu",
    "es": "Spanish",
}

def get_video_duration(video_path):
    """Get video duration in seconds using ffprobe."""
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", video_path],
        capture_output=True, text=True,
    )
    import json
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


# ~3 words per second of spoken commentary
WORDS_PER_SECOND = 3


def getScript(trickshot, language="en", trickshot_name="", video_path=""):
    # Calculate target word count from video duration
    if video_path:
        duration = get_video_duration(video_path)
    else:
        duration = 10.0  # fallback
    max_words = int(duration * WORDS_PER_SECOND)
    max_words = max(10, min(max_words, 80))  # clamp between 10-80 words
    print(f"Video duration: {duration:.1f}s -> target {max_words} words")

    lang_name = LANGUAGE_NAMES.get(language, "English")
    lang_instruction = (
        f" You MUST write your entire commentary in {lang_name}."
        if language != "en"
        else ""
    )
    name_instruction = (
        f' Mention "{trickshot_name}" once.'
        if trickshot_name.strip()
        else ""
    )

    system_prompt = (
        f"You are a sports commentator. Write excited commentary in EXACTLY {max_words} words or fewer. "
        "Describe the key physical actions and the result. What makes this shot unique. "
        "Do NOT mention the crowd, do NOT say folks, do NOT add filler."
        f"{lang_instruction}{name_instruction}"
    )

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Summarize this trickshot in {max_words} words or fewer:\n\n{trickshot}"
                ),
            },
        ],
    )
    raw = response.choices[0].message.content.strip()
    print(f"RAW FROM MODEL ({len(raw.split())} words):\n{raw}")

    # Strip surrounding quotes if the model wrapped it
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1].strip()

    # Hard trim to max_words no matter what
    words = raw.split()
    text = " ".join(words[:max_words])

    # Try to end on a sentence boundary
    for end in ["!", "."]:
        idx = text.rfind(end)
        if idx > len(text) // 3:
            text = text[:idx + 1]
            break

    print(f"FINAL COMMENTARY SCRIPT ({len(text.split())} words):\n{text}")
    return text
