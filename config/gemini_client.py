import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()

API_KEY =os.environ.get("GEMINI_API_KEY")
print(API_KEY)

client = genai.Client(
    api_key=API_KEY,
)

MODEL = "gemini-3-flash-preview"


def generate_post(prompt: str) -> str:
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)],
        )
    ]

    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(
            thinking_level="LOW"
        ),
    )

    result = ""

    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config=config,
    ):
        if chunk.text:
            result += chunk.text


    print(result)
    return result