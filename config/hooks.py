def improve_hook(text: str) -> str:
    lines = text.split("\n")
    if not lines:
        return text

    hook = lines[0].strip()

    if len(hook.split()) > 12:
        hook = "This mistake is slowing your app down."

    hook = hook.replace("What if I told you", "This might surprise you:")
    hook = hook.replace("Did you know", "Most developers miss this:")

    lines[0] = hook
    return "\n".join(lines)