from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import astuple, dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from balatro import Balatro
from balatro_enums import *


@dataclass
class Sellable:
    extra_sell_value: int = field(default=0, init=False)


@dataclass
class Joker(Sellable, ABC):
    _balatro: Balatro

    edition: Edition

    eternal: bool
    perishable: bool
    rental: bool

    debuffed: bool = field(default=False, init=False)
    perishable_rounds_left: int = field(default=5, init=False)

    def __eq__(self, other: JokerType) -> bool:
        if isinstance(other, JokerType):
            return self.joker_type is other
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)

    def dependent_ability(self, joker: Joker) -> None:
        pass

    def on_blind_selected(self) -> None:
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

    def on_card_scored_retrigger(self, scored_card: Card) -> int:
        return 0

    def on_card_sold(self) -> None:
        pass

    def on_discard(self) -> None:
        pass

    def on_end_hand(self) -> None:
        pass

    def on_glass_card_destroyed(self) -> None:
        pass

    def on_hand_played(self) -> None:
        pass

    def on_hand_played_ability(self) -> None:
        pass

    def independent_ability(self) -> None:
        pass

    def on_leftmost_joker_changed(self) -> None:
        pass

    def on_lucky_card_triggered(self) -> None:
        pass

    def on_pack_opened(self) -> None:
        pass

    def on_pack_skipped(self) -> None:
        pass

    def on_planet_used(self) -> None:
        pass

    def on_right_joker_changed(self) -> None:
        pass

    def on_round_ended(self) -> None:
        pass

    def on_shop_exited(self) -> None:
        pass

    def on_shop_rerolled(self) -> None:
        pass

    def on_sold(self) -> None:
        pass

    @property
    @abstractmethod
    def joker_type(self) -> JokerType:
        pass

    @property
    def is_active(self) -> bool:
        return not self.debuffed


@dataclass
class Consumable(Sellable):
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

    def __eq__(self, other: Rank | Enhancement) -> bool:
        if isinstance(other, Rank):
            return not self.is_stone_card and self.rank is other
        if isinstance(other, Enhancement):
            return not self.debuffed and self.enhancement is other
        raise NotImplementedError  # TODO: remove
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
        return (50 if self.is_stone_card else self.rank.chips) + self.bonus_chips

    @property
    def is_stone_card(self) -> bool:
        return self.enhancement is Enhancement.STONE
