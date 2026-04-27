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
        "category": "Engineering Growth & Ownership",
        "hook_type": "vulnerability",
        "angle": "Lessons learned from working on real production systems and taking ownership of engineering decisions.",
        "seed": "handling production bugs, taking responsibility for deployments, moving from coding tasks to owning features, learning from real failures",
        "industry_tie": "engineering growth, ownership, professional development",
        "example_hook": "Writing code is easy. Owning systems is not."
    },

    "Tuesday": {
        "category": "Frontend Architecture (Real Systems)",
        "hook_type": "observation",
        "angle": "Breaking down scalable frontend architecture decisions in real-world applications.",
        "seed": "designing API layers in Next.js, structuring reusable components, managing state at scale, avoiding tight coupling in frontend systems",
        "industry_tie": "frontend architecture, scalability, system design",
        "example_hook": "Frontend architecture problems don’t appear in small projects."
    },

    "Wednesday": {
        "category": "Authentication & API Systems",
        "hook_type": "simplification",
        "angle": "Explaining how authentication and API integrations work in real production environments.",
        "seed": "implementing NextAuth, signature-based authentication, handling API failures, managing secure user sessions",
        "industry_tie": "security engineering, APIs, backend integration",
        "example_hook": "Authentication works fine until real users break it."
    },

    "Thursday": {
        "category": "Performance & System Design",
        "hook_type": "visionary",
        "angle": "Understanding how real applications scale and where performance bottlenecks appear.",
        "seed": "optimizing Next.js apps, handling large datasets, improving CI/CD pipelines, reducing latency in real systems",
        "industry_tie": "performance, scalability, system design",
        "example_hook": "Most performance problems are architecture problems."
    },

    "Friday": {
        "category": "Product Engineering & Analytics",
        "hook_type": "pattern_break",
        "angle": "Building products based on real user behavior instead of assumptions.",
        "seed": "using PostHog analytics, tracking feature adoption, improving onboarding flows, making data-driven decisions",
        "industry_tie": "product engineering, analytics, user behavior",
        "example_hook": "Features don’t matter if users don’t use them."
    },

    "Saturday": {
        "category": "AI Systems & Automation",
        "hook_type": "insight",
        "angle": "Applying AI in real-world systems instead of just generating code.",
        "seed": "building AI agents, integrating LLMs, automating workflows, handling AI limitations in production",
        "industry_tie": "AI engineering, automation, applied AI",
        "example_hook": "AI becomes useful only when it is part of a system."
    },

    "Sunday": {
        "category": "Web3 Engineering & Wallet Systems",
        "hook_type": "analysis",
        "angle": "Exploring real challenges in web3 integrations and blockchain user experience.",
        "seed": "MetaMask integration issues, WalletConnect flows, signature-based authentication, improving wallet onboarding UX",
        "industry_tie": "web3, blockchain UX, authentication systems",
        "example_hook": "Web3 breaks when real users try to use it."
    }
}
TRENDING_OVERLAYS = [
    "why real production systems matter more than tutorials",
    "the shift from frontend developer to full-stack ownership",
    "why system design matters more than syntax",
    "how AI is changing real-world software engineering",
    "building scalable applications instead of demo projects",
    "from writing code to designing systems",
    "why production experience defines real engineers",
    "applied AI vs theoretical AI in real applications",
    "why most applications fail at scale",
    "engineering decisions that impact long-term maintainability",
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
IDENTITY (STRICT):
You are Muhammad Asim, a Full Stack Engineer specializing in:
- Next.js, React, TypeScript
- AI systems (LLMs, agents, automation)
- Web3 integrations (MetaMask, WalletConnect, Phantom)
- Real-time systems and scalable architectures

REAL EXPERIENCE:
- Built production SaaS applications
- Implemented signature-based authentication using NextAuth
- Integrated multiple AI providers into real systems
- Built embeddable widget architectures
- Developed CI/CD pipelines
- Used PostHog analytics for product decisions

CONTENT RULES:
- Only write about real software engineering experience
- Do NOT include generic motivation or life advice
- Do NOT use analogies or storytelling metaphors
- Do NOT invent fake scenarios
- Keep tone professional and engineering-focused

ENGINEERING FRAMEWORK:
1. REAL PROBLEM: Start with a real issue from production, architecture, or development.
2. DECISION / TRADEOFF: Show what was difficult or unclear.
3. RESOLUTION: Explain what worked and why.
4. INSIGHT: Generalize into an engineering principle.

POST STRUCTURE (Strict 120–180 words):
- HOOK (1–10 words): Strong statement, no question
- PROBLEM (30–40 words): Real engineering issue
- INSIGHT (40–50 words): Technical explanation or decision
- PAYOFF (30–40 words): 3 bullet points with actionable lessons
- CTA (10–15 words): Short reflective question

DEPTH REQUIREMENT:
Include at least ONE:
- Production issue
- Scaling challenge
- Technical tradeoff
- Implementation detail

LINGUISTIC RULES:
- Simple and direct language
- No buzzwords or hype
- No emojis
- No cultural/local references
- Avoid banned phrases: "In today's world", "Unlock", "Game-changer"

CONTEXT:
- DAY: {day}
- CATEGORY: {theme_data['category']}
- ANGLE: {theme_data['angle']}
- SEED: {theme_data['seed']}
- TRENDING: {trending}

{hashtag_instruction}

OUTPUT ONLY THE FINAL POST.
"""

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
