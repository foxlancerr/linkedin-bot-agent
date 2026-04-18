def improve_hook(text: str) -> str:
    if not text:
        return text

    lines = text.split("\n")
    hook = lines[0].strip()
    words = hook.split()

    # Replace weak openers
    weak_openers = {
        "what if i told you": "Here's what nobody tells you:",
        "did you know": "Most developers never learn this:",
        "have you ever": "This cost me 6 months.",
        "in today's world": "Right now,",
        "let's be honest": "The honest truth:",
        "i'm going to share": "One pattern I keep seeing:",
        "this is important": "This is slowing your app down.",
    }

    hook_lower = hook.lower()
    for weak, strong in weak_openers.items():
        if hook_lower.startswith(weak):
            hook = strong + " " + hook[len(weak):].strip()
            break

    # Trim if too long
    if len(hook.split()) > 12:
        hook = " ".join(hook.split()[:10]) + "."

    # Remove trailing question mark on hook
    if hook.endswith("?"):
        hook = hook.rstrip("?") + "."

    lines[0] = hook
    return "\n".join(lines)