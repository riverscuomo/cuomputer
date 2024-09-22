import re


def wiki_to_markdown(text):

    # Remove everything from "See also" or "References" downward
    text = re.split(r"==See also==", text)[0]
    # Remove Wikipedia-style image placeholders entirely
    text = re.sub(r"\[\[Image:.+?\]\]", "", text)

    # Remove wiki formatting for templates (e.g., {{Infobox}})
    text = re.sub(r"\{\{.*?\}\}", "", text, flags=re.DOTALL)

    # Convert '''bold''' to **bold**, ensuring no extra spaces between words
    text = re.sub(r"'''(\S.*?\S)'''", r"**\1**", text)

    # Convert ''italic'' to *italic*, ensuring no extra spaces between words
    text = re.sub(r"''(\S.*?\S)''", r"*\1*", text)

    # Convert ==Header== to # Header for Markdown headers (support multiple levels)
    text = re.sub(r"={2,}(.*?)={2,}", lambda m: "#" * (7 -
                  m.group(0).count("=")) + " " + m.group(1).strip(), text)

    # Convert [https://example.com description] to [description](https://example.com) for Markdown links
    text = re.sub(r"\[(https?://[^\s]+)\s(.+?)\]", r"[\2](\1)", text)

    # Convert * ListItem to Markdown list - ListItem, only if it starts at the beginning of a line
    text = re.sub(r"^\*\s(.+)", r"- \1", text, flags=re.MULTILINE)

    # Remove <ref> tags, <references />, and any other unsupported HTML-like tags
    text = re.sub(r"<.*?>", "", text)

    # Remove Category tags [[Category:Something]] entirely
    text = re.sub(r"\[\[Category:.+?\]\]", "", text)

    # Ensure single newline between paragraphs, no excessive line breaks
    text = re.sub(r"\n\s*\n", r"\n\n", text)  # Removes extra blank lines

    # Optional: Ensure only single newline before headers (avoid adding newlines where not needed)
    # Ensure headers are spaced properly with only one newline before and after
    text = re.sub(r"\n*(#+ .+)\n*", r"\n\1\n", text)

    # Trim any leading or trailing whitespaces
    text = text.strip()

    return text
