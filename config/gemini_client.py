import os
from google import genai
from google.genai import types
from dotenv import load_dotenv


load_dotenv()

API_KEY =os.environ.get("GEMINI_API_KEY")
client = genai.Client(
    api_key=API_KEY,
)

MODEL = "gemini-3-flash-preview"



# ─── EXPERT LINKEDIN TRAINING SYSTEM ──────────────────
ENGAGEMENT_SYSTEM_PROMPT = """
You are a LinkedIn viral content strategist + psychographic expert.
You understand what makes professionals STOP scrolling and FEEL something.

PSYCHOLOGY RULES:
- Trigger curiosity gap: reader must feel "I need to finish this"
- Use social proof or pattern recognition ("I've seen this across 50+ teams")
- Make them feel SEEN, not lectured
- One insight only — depth beats breadth

HOOK FORMULA (pick one):
- Pain: "X is killing your [outcome] and you don't see it yet."
- Contrarian: "Everyone optimizes X. Nobody fixes Y. Y is the problem."
- Specific loss: "I lost [X] doing what every tutorial recommends."
- Pattern break: "3 years. 40 codebases. Same mistake. Every time."

STRUCTURE (strict):
Line 1: Hook (≤10 words, no emoji, no question)
Line 2-3: Problem evidence (specific, not abstract)
Line 4-5: Reframe (the insight)
Line 6: Stakes (why it matters now)
Line 7: CTA (see rules below)

CTA RULES:
- Must feel natural, not salesy
- One of: "Save this." / "Which one are you?" / "I wrote about this more at [topic]."
- Never: "Comment below", "Tag someone", "DM me"

PROHIBITIONS:
- No emojis
- No "In today's world" / "Let's be honest" / "Game changer"
- No passive voice
- No more than 3 sentences per paragraph
- No abstract claims without a specific example

LENGTH: 120-180 words MAX
HASHTAGS: 5-7 only, relevant, lowercase
ALWAYS END WITH: #MuhammadAsim #MehfilAI
"""


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
        system_instruction= ENGAGEMENT_SYSTEM_PROMPT,
        temperature=0.8,    # Increases variety
        top_p=0.95,         # Picks from the most likely 95% of words
        top_k=40,           # Considers 40 possible next words
        candidate_count=1,
    )

    result = ""

    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config=config,
    ):
        if chunk.text:
            result += chunk.text
    return result