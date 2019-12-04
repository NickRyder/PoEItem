from PoEItem.poe_item import PoEItem
from RePoE import stat_translations

index_handlers = {
    "negate": -1,
    "canonical_stat": 1,
    "divide_by_fifteen_0dp": 15,
    "per_minute_to_per_second_1dp": 60,
    "divide_by_twenty_then_double_0dp": 10,
    "60%_of_value": 5.0 / 3,
    "divide_by_one_hundred_2dp": 100,
    "milliseconds_to_seconds_0dp": 1000,
    "per_minute_to_per_second_2dp_if_required": 60,
    "deciseconds_to_seconds": 10,
    "divide_by_ten_0dp": 10,
    "multiplicative_damage_modifier": 1,
    "milliseconds_to_seconds": 1000,
    "mod_value_to_item_class": 1,
    "old_leech_percent": 1,
    "old_leech_permyriad": 10000,
    "30%_of_value": 10.0 / 3,
    "per_minute_to_per_second_0dp": 60,
    "per_minute_to_per_second": 60,
    "divide_by_two_0dp": 2,
    "milliseconds_to_seconds_2dp": 1000,
    "divide_by_one_hundred": 100,
    "per_minute_to_per_second_2dp": 60,
    "divide_by_twelve": 10,
    "divide_by_six": 6,
    "times_twenty": 1 / 20,
}


# def dummy():
#     if format != "ignore":
#         string_index = insert_condition_indices.index(index)
#         value = defluffed_affix_line[string_index]
#         if format == "#%":
#             value = value[:-1]
#         elif format == "+#%":
#             value = value[1:-1]
#         elif format == "+#":
#             value = value[1:]
#         elif format != "#":
#             raise ValueError("unrecognized format string: " + format)
#         value = float(value)

#         for index_handler in index_handlers:
#             value *= index_handlers_multipliers[index_handler]
#         value = int(value)
#         if ("min" in condition and condition["min"] > value) or (
#             "max" in condition and condition["max"] < value
#         ):
#             pass

import re


def _return_stat_from_explicit_line(explicit_line):
    re.split("\d+\.?\\d*", explicit_line)
    for stat in stat_translations:
        stat_english = stat["English"]
        for stat_entry in stat_english:
            stat_entry["string"]


_return_stat_from_explicit_line("")

print(re.split("(\d+\.?\\d*)", "test +31% to Cold Resistance"))


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


numeric_and_format = set(
    ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "-", "+", "%", "."]
)


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
                numeric_and_format
            ), f"invalid property_value, {property_value}"


properties = set(
    [
        "Map Tier",
        "Item Quantity",
        "Item Rarity",
        "Monster Pack Size",
        "Level",
        "Quality",
        "Physical Damage",
        "Elemental Damage",
        "Chaos Damage",
        "Critical Strike Chance",
        "Attacks per Second",
        "Weapon Range",
        "Chance to Block",
        "Experience",
        "Evasion Rating",
        "Armour",
        "Energy Shield",
        "Genus",
        "Group",
        "Family",
        "Radius",
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

    # properties
    optional_properties_block = chunks.pop(0)
    if properties.intersection(set(optional_properties_block[0].keys())):
        item.properties = []
        for key, value in optional_properties_block[0].items():
            _unravel_property_values(value)
        # TODO: do something with properties
        optional_abyss_block = chunks.pop(0)
    else:
        optional_abyss_block = optional_properties_block

    # abyss
    if "Abyss" in optional_abyss_block[1]:
        optional_requirements_block = chunks.pop(0)
    else:
        optional_requirements_block = optional_abyss_block

    # requirements
    if "Requirements:" in optional_requirements_block[1]:
        assert (
            len(optional_requirements_block[1]) == 1
        ), f"{optional_requirements_block}"

        # TODO: parse requirements
        optional_sockets_block = chunks.pop(0)
    else:
        optional_sockets_block = optional_requirements_block

    # sockets
    if "Sockets" in optional_sockets_block[0]:
        assert (
            len(optional_sockets_block[0]) == 1 and len(optional_sockets_block[1]) == 0
        ), f"{optional_sockets_block}"
        # TODO: parse sockets
        ilvl_block = chunks.pop(0)
    else:
        ilvl_block = optional_sockets_block

    # ilvl
    assert "Item Level" in ilvl_block[0], f"{ilvl_block}"

    # start parsing from the end of chunks now:

    # descr
    # mirrored
    # corrupted
    # elder/shaper
    # note

    optional_note_block = chunks.pop()
    if "Note" in optional_note_block[0]:
        assert (
            len(optional_note_block[0]) == 1 and len(optional_note_block[1]) == 0
        ), str(optional_note_block)
        # TODO: parse Note
        optional_influence_block = chunks.pop()
    else:
        optional_influence_block = optional_note_block

    if optional_influence_block[1][0] in ["Shaper Item", "Elder Item"]:
        # TODO: parse influence
        optional_corrupted_block = chunks.pop()
    else:
        optional_corrupted_block = optional_influence_block

    if optional_corrupted_block[1][0] in ["Corrupted"]:
        # TODO: parse corrupted
        optional_mirrored_block = chunks.pop()
    else:
        optional_mirrored_block = optional_corrupted_block

    if optional_mirrored_block[1][0] in ["Mirrored"]:
        # TODO: parse mirrored
        optional_descr_block = chunks.pop()
    else:
        optional_descr_block = optional_mirrored_block
    print(chunks)
    print(optional_descr_block)


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
if __name__ == "__main__":
    print(parse_clipboard_text(talisman_entry))
