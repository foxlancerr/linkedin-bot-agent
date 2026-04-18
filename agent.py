import os
import calendar
import requests
from datetime import datetime
from dotenv import load_dotenv

from config.gemini_client import generate_post
from config.formatter import format_for_linkedin
from config.hooks import improve_hook

load_dotenv()

# ─── CONFIG ───────────────────────────────────────────
LINKEDIN_ACCESS_TOKEN = os.environ["LINKEDIN_ACCESS_TOKEN"]

# ─── DAY THEMES ───────────────────────────────────────
DAY_THEMES = {
    "Monday":    "motivational story or career journey in tech",
    "Tuesday":   "backend concept in Node.js or NestJS",
    "Wednesday": "system design or architecture topic",
    "Thursday":  "React/Next.js performance or frontend topic",
    "Friday":    "database optimization or data modeling",
    "Saturday":  "AI agents, automation, or LLM use cases",
}

# ─── THEME ────────────────────────────────────────────
def get_todays_theme():
    day = calendar.day_name[datetime.now().weekday()]
    if day not in DAY_THEMES:
        return None, None
    return day, DAY_THEMES[day]

# ─── LINKEDIN PROFILE ────────────────────────────────
def get_profile_urn(token):
    resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    data = resp.json()
    return f"urn:li:person:{data['sub']}"

# ─── POST TO LINKEDIN ────────────────────────────────
def post_to_linkedin(content):
    token = LINKEDIN_ACCESS_TOKEN
    urn = get_profile_urn(token)

    payload = {
        "author": urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": content},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    resp = requests.post(
        "https://api.linkedin.com/v2/ugcPosts",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        },
        json=payload
    )

    if resp.status_code == 201:
        print("✅ Posted successfully to LinkedIn!")
    else:
        print("❌ Failed:", resp.text)
        raise Exception(resp.text)

# ─── GENERATE POST ───────────────────────────────────
def build_prompt(day, theme):

    return f"""
Today is {day}.

Pick a fresh topic from: {theme}

Write a LinkedIn post with:

HOOK RULES:
- Use ONE viral hook pattern:
  • This mistake is breaking your X
  • Most developers get X wrong
  • I improved X by Y%
  • 3 mistakes killing your X
  • If you're using X, read this
- First line under 12 words
- No emojis in first line

POST RULES:
- Conversational tone
- Real examples or code if needed
- No markdown formatting in final output
- Short paragraphs
- End with a question
- 8–10 hashtags at bottom
"""

# ─── MAIN ────────────────────────────────────────────
if __name__ == "__main__":
    print(f"🤖 Agent started at {datetime.now()}")

    day, theme = get_todays_theme()

    if not day:
        print("😴 No post today")
        exit()

    prompt = build_prompt(day, theme)

    # 1. Generate post using Gemini
    raw_post = generate_post(prompt)

    # 2. Improve hook
    improved = improve_hook(raw_post)

    # 3. Format for LinkedIn
    final_post = format_for_linkedin(improved)

    print("\n🚀 FINAL POST:\n")
    print(final_post)

    # 4. Post to LinkedIn
    post_to_linkedin(final_post)

    print(f"🏁 Finished at {datetime.now()}")