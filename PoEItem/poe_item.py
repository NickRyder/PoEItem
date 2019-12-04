from dataclasses import dataclass
from typing import List, Any, Tuple
from enum import Enum


@dataclass
class PoEItem:
    class Property:
        class Type(Enum):
            MAP_TIER = 1
            ITEM_QUANTITY = 2
            ITEM_RARITY = 3
            MONSTER_PACK_SIZE = 4
            LEVEL = 5
            QUALITY = 6
            UNKNOWN_7 = 7
            UNKNOWN_8 = 8
            PHYSICAL_DAMAGE = 9
            ELEMENTAL_DAMAGE = 10
            CHAOS_DAMAGE = 11
            CRITICAL_STRIKE_CHANCE = 12
            ATTACKS_PER_SECOND = 13
            WEAPON_RANGE = 14
            CHANCE_TO_BLOCK = 15
            ARMOUR = 16
            EVASION_RATING = 17
            ENERGY_SHIELD = 18
            UNKNOWN_19 = 19
            EXPERIENCE = 20
            GENUS = 21
            GROUP = 22
            FAMILY = 23
            RADIUS_SMALL = 24
            RADIUS_MEDIUM = 25
            RADIUS_LARGE = 26

        class DisplayMode(Enum):
            DISPLAY_AFTER_TEXT = 0  # Level 28
            DISPLAY_BEFORE_TEXT = 1  # 67 Str
            DISPLAY_EXPERIENCE = 2  # (exp bar) 1/199345
            DISPLAY_WITHIN_TEXT = 3  # Consumes 30 of 60 Charges on use

        class Colour(Enum):
            DEFAULT = 0
            AUGMENTED = 1
            UNMET = 2
            PHYSICAL = 3
            FIRE = 4
            COLD = 5
            LIGHTNING = 6
            CHAOS = 7
            IMPRINTED_MAGIC = 8
            IMPRINTED_RARE = 9

        def __init__(
            self,
            name: str,
            values: List[Tuple[str, int]],
            displayMode: int,
            type: int = None,
        ):
            self.name = name
            self.values = []
            for value in values:
                self.values.append([value[0], Colour(value[1])])
            self.displayMode = DisplayMode(displayMode)

            if type is not None:
                self.type = Type(type)

    class Socket:
        class Attr(Enum):
            WHITE = "G"
            GREEN = "D"
            BLUE = "I"
            RED = "S"
            ABYSS = "A"

        class Colour(Enum):
            WHITE = "W"
            GREEN = "G"
            BLUE = "B"
            RED = "R"
            ABYSS = "A"

        def __init__(self, attr: str, group: int, sColour: str):
            self.attr = Attr(attr)
            self.group = group
            self.sColour = Colour(sColour)

    @dataclass
    class IncubatedItem:
        level: int
        name: str
        progress: int
        total: int

    @dataclass
    class FlavourTextParsed:
        class_: str
        id: str
        type: str

    class FrameType(Enum):
        NORMAL = 0
        MAGIC = 1
        RARE = 2
        UNIQUE = 3
        GEM = 4
        CURRENCY = 5
        DIVINATION = 6
        QUEST = 7
        PROPHECY = 8
        RELIC = 9

    verified: bool = False

    w: int = None
    h: int = None
    ilvl: int = None
    icon: str = None
    name: str = None
    typeLine: str = None  # basetype
    properties: List[Property] = None
    additionalProperties: List[Property] = None
    nextLevelRequirements: List[Property] = None
    requirements: List[Property] = None
    sockets: List[Socket] = None
    frameType: FrameType = None

    incubatedItem: IncubatedItem = None

    league: str = None

    talismanTier: int = None

    note: str = None
    flavourText: List[str] = None
    flavourTextParsed: List[FlavourTextParsed] = None
    descrText: str = None
    secDescrText: str = None
    prophecyText: str = None
    artFilename: str = None

    maxStackSize: int = None
    stackSize: int = None

    corrupted: bool = False
    duplicated: bool = False
    identified: bool = True
    shaper: bool = False
    elder: bool = False
    veiled: bool = False
    synthesised: bool = False
    delve: bool = False
    abyssJewel: bool = False
    support: bool = False
    fractured: bool = False
    isRelic: bool = False

    implicitMods: List[str] = None
    explicitMods: List[str] = None
    craftedMods: List[str] = None
    enchantMods: List[str] = None
    veiledMods: List[str] = None
    utilityMods: List[str] = None
    fracturedMods: List[str] = None

    hybrid: Any = None  # Takes a PoEItem

    extended: dict = None  # TODO: need whole other data structure here...
