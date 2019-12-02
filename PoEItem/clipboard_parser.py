def _parse_text_chunk(text_chunk, sep=": "):
    text_chunk_lines = text_chunk.splitlines()
    properties_named = {}
    properties_unnamed = set()
    for text_chunk_line in text_chunk_lines:
        if text_chunk_line != "":
            if sep in text_chunk_line:
                text_chunk_line_parts = text_chunk_line.split(sep)
                assert (
                    len(text_chunk_line_parts) == 2
                ), f"expected a type and value pair, got {text_chunk_line}"
                name, value = text_chunk_line_parts
                properties_named[name] = value
            else:
                properties_unnamed.add(text_chunk_line)
    return properties_named, properties_unnamed


def parse_clipboard_text(clipboard_text, sep="--------"):
    """
    takes in a clipboard text and returns a dictionary of the named properties of the form
    name: value

    and unnamed properties which are just lines of text
    """
    text_chunks = clipboard_text.split(sep)
    properties = []
    for text_chunk in text_chunks:
        properties.append(_parse_text_chunk(text_chunk))

    assert "Rarity" in properties[0][0].keys(), "Rarity must be a property of the item"
    rarity = properties[0][0]["Rarity"]
    if rarity == "Rare":
        return parse_rare_item(properties)
    else:
        print("Warning: not implemented")
        return None


def parse_rare_item(chunks):

    pass


# Rarity: Divination Card
# Name
# --------
# Stack Size: stack_size/total_stack
# --------
# Explicit Mods
# --------
# Flavor Text
# --------
# note(optional)

# Rarity: Gem
# Name
# --------
# Gem tags
# Header Information
# --------
# Requirements
# --------
# Gem description
# --------
# Explicit Mods
# --------
# vaal gem header, description, explicit mods (optional)
# --------
# Instructions
# --------
# Corrupted (optional)
# --------
# Notes (optional)

# Rarity: Currency
# Name
# --------
# Stack Size: stack_size/total_stack
# extra_description (optional)
# --------
# sockets (optional)
# --------
# Description
# --------
# Instructions
# --------
# Note(optional)


class ClipboardItem:
    def __init__(self):
        pass


if __name__ == "__main__":
    clipboard_entry = """Rarity: Rare
Cloth Belt
--------
Item Level: 71
--------
23% increased Stun and Block Recovery
--------
Unidentified
--------
Note: ~price 0.5 alch"""

    print(parse_clipboard_text(clipboard_entry))
