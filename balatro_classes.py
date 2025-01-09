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

    def on_blind_select(self) -> None:
        pass

    def on_boss_defeated(self) -> None:
        pass

    def on_card_added(self, added_card: Card) -> None:
        pass

    def on_card_destroyed(self, destroyed_card: Card) -> None:
        pass

    # def on_card_discarded(self, discarded_card: Card) -> None:
    #     pass

    def on_card_held(self, held_card: Card) -> None:
        pass

    def on_card_scored(self, scored_card: Card) -> None:
        pass

    def on_card_scored_check_retrigger(self, scored_card: Card) -> int:
        return 0

    def on_card_sold(self) -> None:
        pass

    def on_dependent_ability(self, joker: Joker) -> None:
        pass

    def on_discard(self) -> None:
        pass

    def on_end_hand(self) -> None:
        pass

    def on_glass_card_destroyed(self) -> None:
        pass

    def on_hand_played(self) -> None:
        pass

    def on_joker_added(self) -> None:
        pass

    def on_leftmost_joker_changed(self) -> None:
        pass

    def on_independent_ability(self) -> None:
        pass

    def on_lucky_card_trigger(self) -> None:
        pass

    def on_pack_skipped(self) -> None:
        pass

    def on_planet_used(self) -> None:
        pass

    def on_reroll(self) -> None:
        pass

    def on_right_joker_changed(self) -> None:
        pass

    def on_round_end(self) -> None:
        pass

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
    _enhancement: Enhancement | None = None
    seal: Seal | None = None

    bonus_chips: int = 0

    debuffed: bool = False

    def __eq__(self, other: Suit | Rank | Enhancement | Card) -> bool:
        if isinstance(other, Suit):
            return self.suit is other or (self == Enhancement.WILD)
        if isinstance(other, Rank):
            return self.rank is other
        if isinstance(other, Enhancement):
            return not self.debuffed and self.enhancement is other
        if isinstance(other, Card):
            if self.is_stone_card or other.is_stone_card:
                return False
            return self == other._suit and self._rank is other._rank
        return NotImplemented

    def __lt__(self, other: Card) -> bool:
        if isinstance(other, Card):
            return self.rank < other.rank
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)

    @property
    def base_chips(self) -> int:
        return (50 if self.is_stone_card else self._rank.chips) + self.bonus_chips

    @property
    def enhancement(self) -> Enhancement | None:
        return None if self.debuffed else self._enhancement

    @enhancement.setter
    def enhancement(self, enhancement: Enhancement) -> None:
        self._enhancement = enhancement

    @property
    def is_stone_card(self) -> bool:
        return self._enhancement is Enhancement.STONE

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
