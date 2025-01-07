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

    extra_chips: int = 0

    debuffed: bool = False

    def __str__(self) -> str:
        s = f"{self.rank.value} of {self.suit.value}"

        modifiers = []
        if self.edition is not Edition.BASE:
            modifiers.append(self.edition.value)
        if self.enhancement is not None:
            modifiers.append(self.enhancement.value)
        if self.seal is not None:
            modifiers.append(self.seal.value)
        if self.extra_chips > 0:
            modifiers.append(f"+{self.extra_chips} extra chips")

        if modifiers:
            s += f" ({modifiers[0]}"
            for modifier in modifiers[1:]:
                s += f", {modifier}"
            s += ")"

        return s

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)
