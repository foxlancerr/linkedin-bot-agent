# config/generator.py
import calendar
import random
from datetime import datetime
import os
from google import genai as google_genai
from google.genai import types
from config.gemini_client import generate_post

# ─── DAY THEMES ───────────────────────────────────────
DAY_THEMES = {
    "Monday": {
        "category": "The Human Code (Motivation)",
        "hook_type": "vulnerability",
        "angle": "Consistency over talent. Why your first language doesn't matter as much as your first logic loop.",
        "seed": "I struggled with C++ pointers for a month, why Python isn't 'cheating,' the first app I built was 100 lines of spaghetti code",
        "industry_tie": "learning to learn, mindset, beginner path",
        "example_hook": "Your first 1000 lines of code will be terrible."
    },
    "Tuesday": {
        "category": "The AI Language Tutor",
        "hook_type": "observation",
        "angle": "Using AI (Cursor/Claude) to explain the 'DNA' of code. Teaching how to ask 'Why' instead of 'Write'.",
        "seed": "Using Claude to explain recursion like a story, why AI is the best pair programmer for students, moving from syntax to architecture",
        "industry_tie": "AI literacy, junior dev 2.0, deep learning",
        "example_hook": "Stop using AI to write code. Use it to understand code."
    },
    "Wednesday": {
        "category": "The Logic Blueprint (All Languages)",
        "hook_type": "simplification",
        "angle": "Explaining universal concepts (Arrays, Loops, Objects) using analogies. Showing that 'Logic is Language-Agnostic'.",
        "seed": "An Array is just a bookshelf, a Variable is a labeled box, think of an Object like a person with properties (name, height)",
        "industry_tie": "CS fundamentals, mental models, cross-language skills",
        "example_hook": "If you master logic, you can learn any language in a week."
    },
    "Thursday": {
        "category": "The Agentic Shift",
        "hook_type": "visionary",
        "angle": "Education on 'Agentic Logic'. How we go from 'If/Else' to 'Autonomous Reasoning'.",
        "seed": "Why agents are the next step after Web Dev, building logic loops in MehfilAI, the difference between a script and an agent",
        "industry_tie": "Agentic AI wave 2026, future-proofing, AI Orchestration",
        "example_hook": "We are moving from writing code to managing intelligence."
    },
    "Friday": {
        "category": "The 'Real World' Portfolio",
        "hook_type": "pattern_break",
        "angle": "Teaching the youth to build 'Full-Stack' projects that solve local problems in Islamabad.",
        "seed": "Build a tracking app for the Metro, a transparency tool for your school, why one 'real' app beats 10 certificates",
        "industry_tie": "hiring reality, building in public, portfolio strategy",
        "example_hook": "Recruiters don't care about your GPA. They care about your GitHub."
    },
    "Saturday": {
        "category": "Mehfil Culture & Community",
        "hook_type": "emotional_connection",
        "angle": "The social side of coding. Why the best engineers are the ones who can explain their code to others.",
        "seed": "Why I started MehfilAI, finding your tribe, tech is a team sport, the 'Big Brother' energy in Islamabad tech",
        "industry_tie": "networking, soft skills, community growth",
        "example_hook": "The best code is written in a room full of friends."
    },
}

TRENDING_OVERLAYS = [
    "why junior developers must become 'AI Architects' today",
    "the end of the 'Tutorial Hell' era for Pakistani youth",
    "building in public: why your GitHub is your real degree",
    "how to use AI to read 1000 pages of documentation in 5 minutes",
    "the shift from 'Syntax' to 'Logic': why the language doesn't matter",
    "Agentic AI: moving from writing code to managing intelligence",
    "The 'Dhaba' guide to System Design: simple analogies for big tech",
    "Product Engineering: why the best devs solve business problems",
    "Vibe coding vs. Deep understanding: how to stay relevant in 2026",
    "Mehfil culture: why networking in Islamabad is your secret weapon",
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
        "5-7 hashtags, lowercase. Always end with #MuhammadAsim #MehfilAI"
        if is_technical else
        "3-4 hashtags max. Always end with #MuhammadAsim #MehfilAI"
    )


    return f"""
ROLE:
You are Muhammad Asim, a Software Architect & Industrial Psychologist. You don't just "post"; you build systems of thought that solve professional frustrations. You are the "Big Brother" of Pakistani Tech, translating complex AI into human logic.

PSYCHOLOGICAL FRAMEWORK:
1. THE VULNERABILITY GAP: Start with a technical "scar." A bug that broke you, a deadline missed, or a prompt that failed. This kills the "AI-bot" feel.
2. THE US VS. THEM LOGIC: Old Way = Manual, Burnout, Brute-force. New Way = Agentic, Orchestrated, Intelligent. 
3. THE "SEE MORE" MYSTERY: Lines 1-3 must contain a "Conflict" and a "Closer." The reader must feel that the solution is hidden behind that click.

POST STRUCTURE (Strict 120-180 words):
- THE HOOK (1-10 words): A confession or a contrarian truth. No emojis. No questions.
- THE FRICTION (30-40 words): Describe the "Messy Middle." The specific struggle in building Agentic AI or Full-stack apps.
- THE MENTAL MODEL (40-50 words): Use a local analogy (Dhaba waiter, Metro traffic, Bazaar bargaining) to explain a technical concept. This is where you EDUCATE.
- THE REFRAME (20-30 words): Show why this logic applies to Python, JS, and C++ equally. Logic is the DNA; syntax is just the skin.
- THE PAYOFF (30-40 words): 3 punchy, "Save-worthy" bullet points (-) for the youth.
- THE LOW-FRICTION CTA (10-15 words): A status-check question (e.g., "Are you building for speed or building for trust?").

LINGUISTIC RULES:
- Grade 8 Simplicity: Use "Build" over "Implement." Use "Fix" over "Optimize."
- 5-Word Explainer: If you use a tech term (e.g., 'RAG'), explain it in 5 words in parentheses immediately after.
- Banned Terms: "In today's world," "Unlock," "Harness," "Game-changer," "Dive deep."
- Formatting: No Emojis. Use line breaks for visual breathing.

CONTEXT:
- DAY: {day}
- TOPIC: {theme_data['category']}
- ANGLE: {theme_data['angle']}
- SEED: {theme_data['seed']}
- TRENDING OVERLAY: {trending}

{hashtag_instruction}

DO NOT explain your choices. Output the post only."""

# ─── STREAM GENERATOR ─────────────────────────────────
def generate_post_stream() -> str:
    day, theme_data, is_technical = get_todays_theme()

    if not day:
        return "No post scheduled for Sunday."

    prompt = build_generation_prompt(day, theme_data, is_technical)

    return generate_post(prompt)

   


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