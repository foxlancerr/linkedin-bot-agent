# agent.py
import os
import calendar
import requests
from datetime import datetime
from dotenv import load_dotenv

from config.generator import generate_post_stream

from config.hooks import improve_hook

load_dotenv()

LINKEDIN_ACCESS_TOKEN = os.environ["LINKEDIN_ACCESS_TOKEN"]


def get_profile_urn(token):
    resp = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={"Authorization": f"Bearer {token}"}
    )
    data = resp.json()
    return f"urn:li:person:{data['sub']}"


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

    print("\n📤 Posting to LinkedIn...")

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


if __name__ == "__main__":
    print(f"🤖 Agent started at {datetime.now()}")

    # 1. Generate post
    final_post = generate_post_stream()

    # 2. Improve hook
    # final_post = improve_hook(raw_post)

 
    print("\n🚀 FINAL POST:\n")
    print(final_post)

    # 4. Post to LinkedIn
    post_to_linkedin(final_post)

    print(f"🏁 Finished at {datetime.now()}")