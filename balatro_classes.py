from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import astuple, dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from balatro import Balatro
from balatro_enums import *


@dataclass
class Joker(ABC):
    balatro: Balatro

    edition: Edition

    eternal: bool
    perishable: bool
    rental: bool

    debuffed: bool

    rounds_until_debuff: int | None

    def __eq__(self, other: JokerType) -> bool:
        if isinstance(other, JokerType):
            return self.joker_type is other
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)

    def on_acquire(self) -> None:
        pass

    def on_blind_select(self) -> None:
        pass

    def on_held(self) -> None:
        pass

    def on_edition_after(self) -> None:
        if self.edition is Edition.POLYCHROME:
            self.balatro.mult = int(self.balatro.mult * 1.5)

    def on_edition_before(self) -> None:
        match self.edition:
            case Edition.FOIL:
                self.balatro.chips += 50
            case Edition.HOLO:
                self.balatro.mult += 10

    def on_end_round(self) -> None:
        pass

    def on_leftmost_joker_changed(self) -> None:
        pass

    def on_independent_ability(self) -> None:
        pass

    def on_independent(self) -> None:
        self.on_edition_before()
        self.on_independent_ability()
        self.on_edition_after()

    def on_played(self) -> None:
        pass

    def on_right_joker_changed(self) -> None:
        pass

    def on_scored(self) -> None:
        pass

    def on_scored_retriggers(self) -> int:
        return 0

    @property
    @abstractmethod
    def joker_type(self) -> JokerType:
        pass

    @property
    def is_active(self) -> bool:
        return not self.debuffed

    @staticmethod
    def create(
        balatro: Balatro,
        joker_type: JokerType,
        edition: Edition = Edition.BASE,
        eternal: bool = False,
        perishable: bool = False,
        rental: bool = False,
        debuffed: bool = False,
        rounds_until_debuff: int | None = None,
    ) -> Joker:
        from balatro_constants import JOKER_CLASSES

        return JOKER_CLASSES[joker_type](
            balatro,
            edition,
            eternal,
            perishable,
            rental,
            debuffed,
            rounds_until_debuff,
        )


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
    _suit: Suit
    _rank: Rank

    edition: Edition = Edition.BASE
    enhancement: Enhancement | None = None
    seal: Seal | None = None

    bonus_chips: int = 0

    debuffed: bool = False

    def __eq__(self, other: Card) -> bool:
        if isinstance(other, Card):
            if (
                self.enhancement is Enhancement.STONE
                or other.enhancement is Enhancement.STONE
            ):
                return False
            return self._suit is other._suit and self._rank is other._rank
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)

    @property
    def base_chips(self) -> int:
        return (
            50 if self.enhancement is Enhancement.STONE else self._rank.chips
        ) + self.bonus_chips

    @property
    def rank(self) -> Rank | None:
        return None if self.enhancement is Enhancement.STONE else self._rank

    @rank.setter
    def rank(self, rank: Rank) -> None:
        self._rank = rank

    @property
    def suit(self) -> Suit | None:
        return None if self.enhancement is Enhancement.STONE else self._suit

    @suit.setter
    def suit(self, suit: Suit) -> None:
        self._suit = suit
