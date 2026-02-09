from dotenv import load_dotenv
from openai import OpenAI
import os

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

def getScript(trickshot, language="en", trickshot_name=""):
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
        "You are a sports commentator. Read the trickshot description and write a single excited sentence "
        "summarizing the key move and the result. Mention what makes this shot unique. "
        "Do NOT mention the crowd, do NOT say folks, do NOT add filler. "
        "Maximum 20 words."
        f"{lang_instruction}{name_instruction}"
    )

    response = client.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"Summarize this trickshot in ONE sentence, max 20 words:\n\n{trickshot}"
                ),
            },
        ],
    )
    raw = response.choices[0].message.content.strip()
    print(f"RAW FROM MODEL ({len(raw.split())} words):\n{raw}")

    # Strip surrounding quotes if the model wrapped it
    if raw.startswith('"') and raw.endswith('"'):
        raw = raw[1:-1].strip()

    # Always force trim to 25 words max (~10 seconds spoken)
    words = raw.split()
    text = " ".join(words[:25])

    # Try to end on a sentence boundary
    for end in ["!", "."]:
        idx = text.rfind(end)
        if idx > len(text) // 3:
            text = text[:idx + 1]
            break

    print(f"FINAL COMMENTARY SCRIPT ({len(text.split())} words):\n{text}")
    return text
