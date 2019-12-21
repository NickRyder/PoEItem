from rare_item_parser import parse_rare_item


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
        except Exception as error:
            print("----")
            print(error)
            print(clipboard_text)
    else:
        # print("Warning: not implemented")
        return None


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


map_entry = """Rarity: Rare
Mystic Abode
Arcade Map
--------
Map Tier: 2
Item Quantity: +77% (augmented)
Item Rarity: +39% (augmented)
--------
Item Level: 70
--------
Area has increased monster variety
Area has patches of shocking ground
Area contains many Totems
Monsters deal 55% extra Damage as Fire
Monsters gain 1 Endurance Charge every 20 seconds
Monsters take 28% reduced Extra Damage from Critical Strikes
--------
Travel to this Map by using it in the Templar Laboratory or a personal Map Device. Maps can only be used once."""

talisman_entry = """Rarity: Rare
Dread Clasp
Splitnewt Talisman
--------
Requirements:
Level: 26
--------
Item Level: 76
--------
Talisman Tier: 2
--------
6% chance to Freeze, Shock and Ignite
--------
+8 to Strength
+25 to Dexterity
7% increased Fire Damage
+21 to maximum Life
--------
From flesh and ferocity,
the First Ones roamed
through the realm of Spirit,
and into the darkness beyond. 
- The Wolven King
--------
Corrupted
"""

enchanted_entry="""
Rarity: Rare
Kraken Dash
Mesh Boots
--------
Armour: 96 (augmented)
Energy Shield: 19 (augmented)
--------
Requirements:
Level: 57
Str: 28
Int: 28
--------
Sockets: R-B B 
--------
Item Level: 77
--------
0.4% of Damage Leeched as Life if you've Killed Recently
--------
+14 to Strength
+22 to Intelligence
88% increased Armour and Energy Shield
+41 to maximum Life
"""

if __name__ == "__main__":
    # pass
    print(parse_clipboard_text(talisman_entry))
    print(parse_clipboard_text(map_entry))
    print(parse_clipboard_text(enchanted_entry))