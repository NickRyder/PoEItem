from dataclasses import dataclass
from typing import List


@dataclass
class PoEItem:
    @dataclass
    class property:
        name: str = None
        values: List[List[int]] = None
        displayMode: int = None  # TODO: enum
        type: int = None  # TODO: enum

    verified: bool = False
    w: int = None
    h: int = None
    ilvl: int = None
    icon: str = None
    league: str = None
    sockets: int = None
    name: str = None
    typeLine: str = None  # basetype
    identified: bool = None
    note: str = None
    properties: List[property] = None
    requirements: List[property] = None
    explicitMods: List[str] = None  # TODO: type better List<string>
    frameType: int = None  # TODO: enum
    extended: dict = None  # TODO: need whole other data structure here...

