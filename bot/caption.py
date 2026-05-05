import re

def process_caption(text, config):
    if not text:
        text = ""

    text = re.sub(r"https?://t\.me/\S+", "", text)
    text = re.sub(r"https?://telegram\.me/\S+", "", text)
    text = re.sub(r"@\w+", "", text)

    if config.get("mode") == "replace":
        link = config.get("replacement_link", "")
        if link:
            text += f"\n\n🔗 {link}"

    if config.get("footer"):
        text += f"\n\n{config['footer']}"

    return text.strip()
