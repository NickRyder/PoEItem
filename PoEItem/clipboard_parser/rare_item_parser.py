from PoEItem.poe_item import PoEItem
from RePoE import base_items

descr_text = set()
for base_item in base_items.values():
    descr_text.add(base_item["properties"].get("directions", ""))
descr_text.remove("")


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
        "Limited to",
        "Stack Size",
        "Applies To",
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

    # flavourText
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

    if optional_descr_block[1][0] in descr_text:
        optional_flavour_block = chunks.pop()
        # TODO: parse descr
    else:
        optional_flavour_block = optional_descr_block

    print(optional_descr_block)


import RePoE

generation_types = set()
for mod in RePoE.mods.values():
    generation_types.add(mod["generation_type"])

print(generation_types)
