from dataclasses import dataclass

@dataclass
class CardEntry:
    img_link: str
    copies: int
    wide: bool