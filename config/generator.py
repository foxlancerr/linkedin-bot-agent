# config/generator.py
import calendar
import random
from datetime import datetime
import os
from google import genai as google_genai
from google.genai import types
from config.gemini_client import generate_post

# ─── CLIENT SETUP ─────────────────────────────────────
client = google_genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY")
)

MODEL = "gemini-2.0-flash"

# ─── SYSTEM PROMPT ────────────────────────────────────
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
Line 7: CTA — one of: "Save this." / "Which one are you?" / "Seen this too?"

PROHIBITIONS:
- No emojis
- No "In today's world" / "Let's be honest" / "Game changer"
- No passive voice
- No more than 3 sentences per paragraph
- No abstract claims without a specific example

LENGTH: 120-180 words MAX
HASHTAGS: 5-7 only, lowercase, relevant
ALWAYS END WITH: #MuhammadAsim #MehfilAI
"""

# ─── DAY THEMES ───────────────────────────────────────
DAY_THEMES = {
    "Monday": {
        "category": "real career mistake or industry truth",
        "hook_type": "specific_loss",
        "angle": "emotional developer story tied to industry reality — layoffs, wrong tech stack choice, over-engineering, burnout",
        "seed": "I wasted 2 years on the wrong stack, got laid off after over-engineering, burned out chasing senior title",
        "industry_tie": "current job market, tech layoffs 2024-2025, hiring freeze reality",
        "example_hook": "I got laid off 3 days after my best performance review."
    },
    "Tuesday": {
        "category": "AI tools changing how developers actually work",
        "hook_type": "contrarian",
        "angle": "how real teams are using Cursor, Copilot, Claude, v0 in production — not demos, real workflows",
        "seed": "Cursor replacing junior devs, Claude for code review, Copilot making devs slower not faster, vibe coding consequences",
        "industry_tie": "AI replacing entry-level roles, developer productivity debate, vibe coding trend 2025",
        "example_hook": "Cursor didn't make our team faster. It made our codebase worse."
    },
    "Wednesday": {
        "category": "system design or architecture decision with real cost",
        "hook_type": "pattern_break",
        "angle": "architectural mistake that looks smart but breaks at scale — microservices too early, wrong DB choice, API design debt",
        "seed": "microservices killed our startup velocity, we moved back to monolith, chose MongoDB and regretted it",
        "industry_tie": "startups vs big tech architecture, cost of cloud bills, engineering efficiency trend",
        "example_hook": "We split into 12 microservices at 3 engineers. It nearly killed the company."
    },
    "Thursday": {
        "category": "industry shift — what skills actually matter in 2025",
        "hook_type": "assumption_challenge",
        "angle": "what the job market, AI, and product-focused engineering means for developer careers right now",
        "seed": "full-stack is dead, T-shaped skills, prompt engineering as core skill, product engineers replacing pure devs",
        "industry_tie": "hiring trends 2025, AI-era developer skills, what companies actually pay for now",
        "example_hook": "Companies stopped hiring developers. They started hiring product engineers."
    },
    "Friday": {
        "category": "concrete technical insight with measurable result",
        "hook_type": "specific_loss",
        "angle": "one specific optimization or fix with real measurable impact — DB query, API performance, React render, cost reduction",
        "seed": "N+1 query costing $3k/month, one index cutting response time 10x, removing useEffect fixing entire UX",
        "industry_tie": "engineering efficiency, cloud cost reduction trend, performance as product feature",
        "example_hook": "One missing database index was costing us $2,800 a month."
    },
    "Saturday": {
        "category": "what AI agents and automation are doing to the industry RIGHT NOW",
        "hook_type": "observation",
        "angle": "real patterns from teams building with LLMs, agents, RAG — not theory, actual production lessons",
        "seed": "agent loops failing silently, RAG garbage in garbage out, LLM cost spiraling, one prompt replacing pipelines",
        "industry_tie": "agentic AI wave 2025, AI startups failing, LLM in production reality vs hype",
        "example_hook": "We built a 6-agent pipeline. A single prompt replaced it."
    },
}

TRENDING_OVERLAYS = [
    "vibe coding consequences in production",
    "AI replacing junior developer roles",
    "tech layoffs and what survives them",
    "moving back from microservices to monolith",
    "Claude vs GPT-4 in real workflows",
    "developer burnout at AI-era pace",
    "prompt engineering as a core engineering skill",
    "cost of cloud bills killing startups",
]


# ─── THEME GETTER ─────────────────────────────────────
def get_todays_theme():
    day = calendar.day_name[datetime.now().weekday()]

    if day == "Sunday":
        print(f"📅 Today is {day} — No post scheduled.")
        return None, None, None

    if day not in DAY_THEMES:
        return None, None, None

    return day, DAY_THEMES[day], day != "Monday"


# ─── PROMPT BUILDER ───────────────────────────────────
def build_generation_prompt(day: str, theme_data: dict, is_technical: bool) -> str:
    trending = random.choice(TRENDING_OVERLAYS)

    hashtag_instruction = (
        "5-7 hashtags, lowercase, relevant to topic. Always end with #MuhammadAsim #MehfilAI"
        if is_technical else
        "3-4 hashtags max. Always end with #MuhammadAsim #MehfilAI"
    )

    return f"""DAY: {day}
TOPIC: {theme_data['category']}
ANGLE: {theme_data['angle']}
HOOK TYPE: {theme_data['hook_type']}
SEED IDEAS: {theme_data['seed']}
TRENDING OVERLAY: weave this in naturally — {trending}
EXAMPLE HOOK: {theme_data['example_hook']}

WRITE ONE LINKEDIN POST:
- Hook: ≤10 words, {theme_data['hook_type']} style, no emoji, no question
- Body: specific insight, one idea only, 120-180 words total
- CTA: natural, one line ("Save this." or "Which camp are you in?")
- Hashtags: {hashtag_instruction}
- Tone: peer-to-peer, direct, no jargon
- Code block: only if it proves the point in ≤8 lines

DO NOT explain your choices. Output the post only."""


# ─── STREAM GENERATOR ─────────────────────────────────
def generate_post_stream() -> str:
    day, theme_data, is_technical = get_todays_theme()

    if not day:
        return "No post scheduled for Sunday."

    prompt = build_generation_prompt(day, theme_data, is_technical)

    generate_post(prompt)

   


# ─── VALIDATOR ────────────────────────────────────────
def validate_post_quality(post_text: str) -> dict:
    issues = []
    warnings = []

    prohibited = [
        ("emojis", "😀"),
        ("let's be honest", "let's be honest"),
        ("in today's world", "in today"),
        ("have you ever", "have you ever"),
        ("comment below", "comment below"),
        ("tag someone", "tag someone"),
        ("dm me", "dm me"),
    ]

    post_lower = post_text.lower()
    for check_name, pattern in prohibited:
        if pattern.lower() in post_lower:
            issues.append(f"❌ Prohibited phrase: '{check_name}'")

    lines = post_text.split('\n')
    first_line = lines[0] if lines else ""
    first_line_words = len(first_line.split())

    if first_line_words > 12:
        warnings.append(f"⚠️  Hook is {first_line_words} words (keep ≤10)")

    if first_line.strip().endswith("?"):
        issues.append("❌ Hook is a question — use a statement")

    word_count = len(post_text.split())
    if word_count < 120:
        warnings.append(f"⚠️  Only {word_count} words (aim 120-180)")
    elif word_count > 200:
        warnings.append(f"⚠️  {word_count} words — trim it down")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "word_count": word_count,
        "first_line_words": first_line_words,
    }


# ─── ENFORCE TAGS ─────────────────────────────────────
def enforce_author_tags(post_text: str) -> str:
    if "#MuhammadAsim" not in post_text:
        post_text += " #MuhammadAsim"
    if "#MehfilAI" not in post_text:
        post_text += " #MehfilAI"
    return post_text


# ─── MAIN ─────────────────────────────────────────────
def main():
    print("\n" + "=" * 60)
    print("🤖 LINKEDIN POST GENERATOR")
    print("=" * 60)

    raw_post = generate_post_stream()

    post = enforce_author_tags(raw_post)

    print("\n\n📊 POST QUALITY CHECK:")
    print("─" * 60)

    validation = validate_post_quality(post)

    if validation["issues"]:
        print("🔴 ISSUES:")
        for issue in validation["issues"]:
            print(f"  {issue}")

    if validation["warnings"]:
        print("\n🟡 SUGGESTIONS:")
        for warning in validation["warnings"]:
            print(f"  {warning}")

    if not validation["issues"]:
        print("✅ Post passes quality checks!")

    print(f"\n📈 Stats:")
    print(f"  Word count : {validation['word_count']}")
    print(f"  Hook words : {validation['first_line_words']}")
    print(f"  Quality    : {'✅ READY' if validation['valid'] else '❌ NEEDS REVISION'}")

    return post


if __name__ == "__main__":
    main()