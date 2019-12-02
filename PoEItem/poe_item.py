from dataclasses import dataclass
from typing import List, Any


@dataclass
class PoEItem:
    @dataclass
    class Property:
        name: str
        values: List[List[int]]
        displayMode: int  # TODO: enum
        type: int = None  # TODO: enum

    @dataclass
    class Socket:
        attr: str  # TODO: enum
        group: int
        sColour: str  # TODO: enum

    @dataclass
    class IncubatedItem:
        level: int
        name: str
        progress: int
        total: int

    @dataclass
    class FlavourTextParsed:
        _class: str
        id: str
        type: str

    verified: bool = False

    w: int = None
    h: int = None
    ilvl: int = None
    icon: str = None
    league: str = None
    sockets: int = None
    name: str = None
    typeLine: str = None  # basetype
    properties: List[Property] = None
    additionalProperties: List[Property] = None
    nextLevelRequirements: List[Property] = None
    requirements: List[Property] = None
    sockets: List[Socket] = None
    frameType: int = None  # TODO: enum

    incubatedItem: IncubatedItem = None

    league: str = None

    talismanTier: int = None

    note: str = None
    flavourText: List[str] = None
    flavourTextParsed = List[FlavourTextParsed] = None
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

    implicitMods: List[str] = None
    explicitMods: List[str] = None
    craftedMods: List[str] = None
    enchantMods: List[str] = None
    veiledMods: List[str] = None
    utilityMods: List[str] = None
    fracturedMods: List[str] = None

    hybrid: Any = None  # Takes a PoEItem

    extended: dict = None  # TODO: need whole other data structure here...
