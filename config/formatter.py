import re

NORMAL = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

BOLD = (
    "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘷𝘄𝘅𝘆𝘇"
    "𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭"
    "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵"
)

# safety check (VERY IMPORTANT)
assert len(NORMAL) == len(BOLD), "Bold mapping length mismatch!"

BOLD_MAP = str.maketrans(NORMAL, BOLD)


def to_bold(text):
    return text.translate(BOLD_MAP)


def format_for_linkedin(text: str) -> str:

    # Convert code blocks
    def replace_code(match):
        code = match.group(1).strip()
        return f"\n🔹 Code Example:\n{code}\n"

    text = re.sub(r"```(?:\w+)?\n?(.*?)```", replace_code, text, flags=re.DOTALL)

    # Inline code
    text = re.sub(r"`(.*?)`", r"\1", text)

    # Bold markdown
    text = re.sub(r"\*\*(.*?)\*\*", lambda m: to_bold(m.group(1)), text)

    # Italics remove
    text = re.sub(r"\*(.*?)\*", r"\1", text)

    # spacing cleanup
    lines = text.split("\n")
    clean = []

    for line in lines:
        line = line.strip()
        if line:
            clean.append(line)
            clean.append("")

    return "\n".join(clean).strip()