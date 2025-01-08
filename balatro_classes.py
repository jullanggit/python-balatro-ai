from __future__ import annotations
from dataclasses import astuple, dataclass

from balatro_enums import *


@dataclass
class Joker:
    joker_type: JokerType

    edition: Edition = Edition.BASE

    eternal: bool = False
    perishable: bool = False
    rental: bool = False

    debuffed: bool = False

    rounds_until_debuff: int | None = None

    def __eq__(self, other: Joker | JokerType) -> bool:
        if isinstance(other, Joker):
            return astuple(self) == astuple(other)
        elif isinstance(other, JokerType):
            return not self.debuffed and self.joker_type is other
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)


@dataclass
class Consumable:
    consumable_type: Tarot | Planet | Spectral

    is_negative: bool = False

    def __eq__(self, other: Consumable | Tarot | Planet | Spectral) -> bool:
        if isinstance(other, Consumable):
            return astuple(self) == astuple(other)
        elif (
            isinstance(other, Tarot)
            or isinstance(other, Planet)
            or isinstance(other, Spectral)
        ):
            return self.consumable_type is other
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)


@dataclass
class Card:
    suit: Suit
    rank: Rank

    edition: Edition = Edition.BASE
    enhancement: Enhancement | None = None
    seal: Seal | None = None

    bonus_chips: int = 0

    debuffed: bool = False

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)
