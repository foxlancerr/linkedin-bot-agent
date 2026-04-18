import google.generativeai as genai
import calendar
from datetime import datetime
import os
from google import genai as google_genai
from google.genai import types

# ─── CONFIGURATION ────────────────────────────────────
client = google_genai.Client(
    api_key=os.environ.get("GEMINI_API_KEY"),
)

MODEL = "gemini-1.5-flash"


# ─── EXPERT LINKEDIN TRAINING SYSTEM ──────────────────
ENGAGEMENT_SYSTEM_PROMPT = """
You are an expert LinkedIn post writer trained to create HIGH-ENGAGEMENT, 
HUMAN-TONE posts that make professionals think differently.

CRITICAL RULES (Never break these):
1. HOOK FIRST: Opening line must use ONE of these patterns:
   - Identify tension: "Most X assume Y, but actually..."
   - Contrarian take: "The assumption is wrong. Here's why..."
   - Vulnerability: "I wasted 3 years learning something simple..."
   - Market observation: "I'm seeing this pattern across X companies..."
   - Challenge assumption: "Everyone believes Y but data shows..."

2. SENTENCE STRUCTURE:
   - First line: 12-15 words MAXIMUM
   - Average all sentences: 12-15 words
   - Mix short + medium + long for rhythm
   - Break paragraphs: 2-3 sentences MAX before line break

3. TONE RULES:
   - Conversational (like explaining to a peer)
   - Contractions welcome: "that's", "you're", "don't"
   - No corporate jargon or buzzwords
   - Show with examples, don't abstract
   - Assume reader is thoughtful and busy

4. ABSOLUTE PROHIBITIONS (Don't do these):
   - ❌ NO emojis (kill credibility in professional context)
   - ❌ NO questions as hooks ("Have you ever felt...")
   - ❌ NO generic openers ("In today's world", "Let's be honest")
   - ❌ NO forced engagement ("Comment below", "Tag someone")
   - ❌ NO multiple scattered ideas
   - ❌ NO false humility ("I'm no expert but...")
   - ❌ NO vague statements ("This is important")

5. ENGAGEMENT COMES FROM:
   - Identifying a real tension they FEEL
   - Offering a fresh frame on familiar problem
   - Sharing specific evidence/pattern (not abstract)
   - Making them feel UNDERSTOOD, not targeted
   - Leaving them thinking differently

6. STRUCTURE:
   [HOOK - tension/observation/contrast]
   [SETUP - context/evidence of problem]
   [INSIGHT - reframed perspective]
   [STAKES - why this matters]
   [CLOSING - memorable thought, NOT call-to-action]

7. LENGTH: 150-240 words (tight, focused)

8. CLOSING: NEVER ask "what do you think?" or "DM me"
   - Instead, end with reflection that invites thinking
   - Close with insight they can sit with

QUALITY CHECK:
- Read aloud: Does it sound like a person?
- Specificity: Any concrete examples?
- Clarity: One insight or scattered ideas?
- Authenticity: Genuine insight or performance?
"""


# ─── DAY THEMES WITH ENGAGEMENT ANGLES ────────────────
DAY_THEMES = {
    "Monday": {
        "category": "motivational story or personal experience",
        "hook_type": "vulnerability",
        "context": "coding, office life, career, or tech journey",
        "example": "I spent 2 years learning what took 30 minutes to understand"
    },
    "Tuesday": {
        "category": "technical explanation of a backend concept",
        "hook_type": "problem_insight",
        "context": "NestJS, Node.js with practical examples",
        "example": "Most developers architect this wrong, causing scaling issues later"
    },
    "Wednesday": {
        "category": "software architecture or system design concept",
        "hook_type": "contrarian",
        "context": "explained clearly with real world use cases",
        "example": "The architectural pattern everyone uses is backwards for your use case"
    },
    "Thursday": {
        "category": "frontend React/Next.js or web security/performance",
        "hook_type": "pattern_observation",
        "context": "development topic with practical examples",
        "example": "I'm seeing the same performance mistake across X teams"
    },
    "Friday": {
        "category": "advanced database concept or data modeling",
        "hook_type": "assumption_challenge",
        "context": "query optimization or data modeling technique",
        "example": "The indexing strategy everyone teaches is slowing you down"
    },
    "Saturday": {
        "category": "building with AI, agents, automation, LLM use cases",
        "hook_type": "observation",
        "context": "practical developer-focused examples",
        "example": "The way most teams use LLMs is missing 80% of the value"
    },
}


# ─── GET TODAY'S THEME ────────────────────────────────
def get_todays_theme():
    """Get today's theme with engagement angle"""
    day = calendar.day_name[datetime.now().weekday()]
    
    if day == "Sunday":
        print(f"📅 Today is {day} — No post scheduled for Sunday.")
        return None, None, None
    
    if day not in DAY_THEMES:
        return None, None, None
    
    theme_data = DAY_THEMES[day]
    return day, theme_data, day != "Monday"  # is_technical


# ─── PROMPT GENERATOR ────────────────────────────────
def build_generation_prompt(day: str, theme_data: dict, is_technical: bool) -> str:
    """Build the detailed prompt for post generation"""
    
    hook_examples = {
        "vulnerability": "I spent years learning something simple. Here's what I finally understood.",
        "problem_insight": "Most X assume Y without realizing...",
        "contrarian": "The assumption is wrong. The reality is different.",
        "pattern_observation": "I'm seeing this pattern across multiple teams/companies...",
        "assumption_challenge": "Everyone believes X, but the evidence shows Y..."
    }
    
    example_hook = hook_examples.get(theme_data["hook_type"], "")
    
    prompt = f"""
YOU ARE AN EXPERT LINKEDIN ENGAGEMENT WRITER.
Follow EVERY rule in your system prompt. No exceptions.

TODAY: {day}

TOPIC DIRECTION:
- Category: {theme_data['category']}
- Context: {theme_data['context']}
- Hook type: {theme_data['hook_type']}
- Example: "{example_hook}"

WRITE A LINKEDIN POST:

HOOK (most critical):
- Opening line MUST use the {theme_data['hook_type']} pattern
- Example: {example_hook}
- 12-15 words maximum
- NO questions, NO clichés

POST STRUCTURE:
1. Hook line (tension/observation)
2. Evidence/setup (2-3 sentences showing the problem)
3. Insight (what people get wrong or what changes perspective)
4. Stakes/implication (why this matters practically)
5. Closing (memorable reflection, NOT a question or CTA)

TONE:
- Conversational like explaining to a colleague
- Specific examples over abstract claims
- One clear insight, not scattered ideas
- Short paragraphs (2-3 sentences max)

TECHNICAL POSTS:
- Include a code block ONLY if it directly illustrates the point (not required)
- Code should be <10 lines and immediately understandable
- Explain the code in plain language

ENGAGEMENT RULES:
- Average 12-15 words per sentence
- Mix short + medium + long sentences
- Read naturally aloud
- NO emojis
- NO engagement asks ("DM me", "comment below")
- NO generic phrases

LENGTH: 150-240 words

CLOSE WITH: A thought or insight that makes them think differently
(NOT a question, NOT a CTA)

{"# INCLUDE HASHTAGS: 8-10 relevant hashtags for searchability" if is_technical else "# NO hashtags for Monday motivational posts"}

WRITE NOW:
"""
    
    return prompt


# ─── STREAM-BASED GENERATION ──────────────────────────
def generate_post_stream() -> str:
    """Generate post using streaming with Gemini"""
    
    day, theme_data, is_technical = get_todays_theme()
    
    if not day:
        return "No theme for today. Sunday posts are not scheduled."
    
    # Build the prompt
    prompt = build_generation_prompt(day, theme_data, is_technical)
    
    # Create content with system prompt
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
        system_instruction=ENGAGEMENT_SYSTEM_PROMPT,
    )
    
    response_text = ""
    
    print(f"\n🚀 Generating {day}'s post...")
    print(f"📋 Theme: {theme_data['category']}")
    print(f"🎯 Hook type: {theme_data['hook_type']}\n")
    print("─" * 60)
    
    # Stream the response
    for chunk in client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config=config,
    ):
        if chunk.text:
            response_text += chunk.text
            print(chunk.text, end="", flush=True)
    
    print("\n" + "─" * 60)
    return response_text


# ─── POST QUALITY VALIDATOR ───────────────────────────
def validate_post_quality(post_text: str) -> dict:
    """Check if post follows engagement rules"""
    
    issues = []
    warnings = []
    
    # Check for prohibited patterns
    prohibited = [
        ("emojis", r"[😀-🙏🌀-🗿🚀-🛿]"),
        ("Let's be honest", "let's be honest"),
        ("In today's", "in today"),
        ("Have you ever", "have you ever"),
        ("Comment below", "comment below"),
        ("Tag someone", "tag someone"),
        ("DM me", "dm me"),
    ]
    
    post_lower = post_text.lower()
    
    for check_name, pattern in prohibited:
        if pattern.lower() in post_lower:
            issues.append(f"❌ Found prohibited phrase: '{check_name}'")
    
    # Check word counts
    lines = post_text.split('\n')
    first_line = lines[0] if lines else ""
    first_line_words = len(first_line.split())
    
    if first_line_words > 15:
        warnings.append(f"⚠️  First line is {first_line_words} words (should be ≤15)")
    
    # Check for questions as hooks
    if first_line.strip().endswith("?"):
        issues.append("❌ Hook is a question (use statements instead)")
    
    # Check paragraph length
    paragraphs = post_text.split('\n\n')
    for i, para in enumerate(paragraphs):
        sentences = [s for s in para.split('.') if s.strip()]
        if len(sentences) > 4:
            warnings.append(f"⚠️  Paragraph {i+1} has {len(sentences)} sentences (keep ≤3)")
    
    # Word count
    word_count = len(post_text.split())
    if word_count < 150:
        warnings.append(f"⚠️  Post is {word_count} words (aim for 150-240)")
    elif word_count > 280:
        warnings.append(f"⚠️  Post is {word_count} words (keep under 280)")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "warnings": warnings,
        "word_count": word_count,
        "first_line_words": first_line_words,
    }


# ─── MAIN EXECUTION ──────────────────────────────────
def main():
    """Main execution function"""
    
    print("\n" + "="*60)
    print("🤖 LINKEDIN POST GENERATOR (Expert-Trained)")
    print("="*60)
    
    # Generate post
    post = generate_post_stream()
    
    # Validate quality
    print("\n\n📊 POST QUALITY CHECK:")
    print("─" * 60)
    
    validation = validate_post_quality(post)
    
    if validation["issues"]:
        print("🔴 ISSUES FOUND:")
        for issue in validation["issues"]:
            print(f"  {issue}")
    
    if validation["warnings"]:
        print("\n🟡 SUGGESTIONS:")
        for warning in validation["warnings"]:
            print(f"  {warning}")
    
    if not validation["issues"]:
        print("✅ Post passes quality checks!")
    
    print(f"\n📈 Stats:")
    print(f"  - Word count: {validation['word_count']}")
    print(f"  - First line: {validation['first_line_words']} words")
    print(f"  - Quality: {'✅ READY' if validation['valid'] else '❌ NEEDS REVISION'}")
    
    return post


if __name__ == "__main__":
    generated_post = main()
    
    # Save to file for reference
    day = calendar.day_name[datetime.now().weekday()]
    if day != "Sunday":
        filename = f"linkedin_post_{day}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(generated_post)
        print(f"\n💾 Post saved to: {filename}")