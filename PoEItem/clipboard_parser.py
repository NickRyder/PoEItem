from PoEItem.poe_item import PoEItem


def _parse_text_chunk(text_chunk, sep=": "):
    text_chunk_lines = text_chunk.splitlines()
    properties_named = {}
    properties_unnamed = []
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
                properties_unnamed.append(text_chunk_line)
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
        try:
            return parse_rare_item(properties)
        except AssertionError:
            print(clipboard_text)
    else:
        print("Warning: not implemented")
        return None


def _unravel_property_values(property_value):
    """
    Takes in property values such as the RHS of the following
    Physical Damage: 32-60
    Elemental Damage: 16-30 (augmented), 6-136 (augmented)
    Critical Strike Chance: 6.60% (augmented)
    Attacks per Second: 1.78 (augmented)
    Weapon Range: 14

    produces PoEItem.property out of them
    """
    property_values = property_value.split(", ")
    for property_value in property_values:
        augmented = False
        aug_string = " (augmented)"
        if aug_string == property_value[-len(aug_string) :]:
            augmented = True
            property_value = property_value[: -len(aug_string)]
            assert set([c for c in property_value]).issubset(
                set(["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", "%"])
            ), f"invalid property_value, {property_value}"


properties = set(
    [
        "Evasion Rating",
        "Armour",
        "Energy Shield",
        "Physical Damage",
        "Elemental Damage",
        "Chaos Damage",
        "Attacks per Second",
        "Weapon Range",
        "Genus",
        "Group",
        "Family",
    ]
)


def parse_rare_item(chunks):
    # chunks[0]
    # Rarity: Rare
    # Horror Lock
    # Stygian Vise
    item = PoEItem(verified=False)
    chunk_zero = chunks.pop(0)
    assert len(chunk_zero[0]) == 1, f"expected only Rarity, {chunk_zero}"
    if len(chunk_zero[1]) == 1:
        item.typeLine = chunk_zero[1][0]
    elif len(chunk_zero[1]) == 2:
        item.name = chunk_zero[1][0]
        item.typeLine = chunk_zero[1][1]
    else:
        raise ValueError(f"expected name and/or base type, got {chunk_zero}")

    # check if optional property block is there, if so parse
    optional_properties_block = chunks.pop(0)
    if properties.intersection(set(optional_properties_block[0].keys())):
        item.properties = []
        for key, value in optional_properties_block[0].items():
            _unravel_property_values(value)

        requirements_block = chunks.pop(0)
    else:
        requirements_block = optional_properties_block

    assert (
        "Requirements:" in requirements_block[1] and len(requirements_block[1]) == 1
    ), f"expected requirements chunk, got {print(requirements_block)}"
    # chunks[1]
    # Requirements:
    # Level: 46


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
