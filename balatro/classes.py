from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from balatro import Run

from .enums import *


@dataclass(eq=False)
class Sellable:
    extra_sell_value: int = field(default=0, init=False, repr=False)


@dataclass(eq=False)
class BaseJoker(Sellable, ABC):
    _perishable_rounds_left: int = field(default=5, init=False, repr=False)
    _run: Run | None = field(default=None, init=False, repr=False)

    edition: Edition = Edition.BASE

    eternal: bool = False
    perishable: bool = False
    rental: bool = False

    debuffed: bool = field(default=False, init=False, repr=False)
    flipped: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        assert not (self.eternal and self.perishable)

    def __eq__(self, other: BaseJoker | JokerType | Edition) -> bool:
        match other:
            case BaseJoker():
                return self is other
            case JokerType():
                return not self.debuffed and self.joker_type is other
            case Edition():
                return (
                    not self.debuffed or other is Edition.NEGATIVE
                ) and self.edition is other

        return NotImplemented

    def __str__(self) -> str:
        return f"{self.joker_type}"

    def _repr_png_(self, card_back: Deck = Deck.RED) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, card_back=card_back, as_image=False)

    def _blind_selected_ability(self) -> None:
        pass

    def _blind_selected_action(self) -> None:
        pass

    def _boss_blind_triggered_ability(self) -> None:
        pass

    def _boss_defeated_action(self) -> None:
        pass

    def _card_added_action(self, added_card: Card) -> None:
        pass

    def _card_destroyed_action(self, destroyed_card: Card) -> None:
        pass

    def _card_held_ability(self, held_card: Card) -> None:
        pass

    def _card_held_retriggers(self, held_card: Card) -> int:
        return 0

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        pass

    def _card_scored_action(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        pass

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return 0

    def _created_action(self) -> None:
        pass

    def _dependent_ability(self, other_joker: BaseJoker) -> None:
        pass

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        pass

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        pass

    def _end_hand_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        pass

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        pass

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        pass

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        pass

    def _item_sold_ability(self, sold_item: Sellable) -> None:
        pass

    def _item_sold_action(self, sold_item: Sellable) -> None:
        pass

    def _lucky_card_triggered_action(self) -> None:
        pass

    def _on_blind_selected(self) -> None:
        if self.debuffed:
            return

        self._blind_selected_ability()
        self._blind_selected_action()

    def _on_boss_blind_triggered(self) -> None:
        if self.debuffed:
            return

        self._boss_blind_triggered_ability()

    def _on_boss_defeated(self) -> None:
        if self.debuffed:
            return

        self._boss_defeated_action()

    def _on_card_added(self, added_card: Card) -> None:
        if self.debuffed:
            return

        self._card_added_action(added_card)

    def _on_card_destroyed(self, destroyed_card: Card) -> None:
        if self.debuffed:
            return

        self._card_destroyed_action(destroyed_card)

    def _on_card_held(self, held_card: Card) -> None:
        if self.debuffed:
            return

        self._card_held_ability(held_card)

    def _on_card_held_retriggers(self, held_card: Card) -> int:
        if self.debuffed:
            return 0
        return self._card_held_retriggers(held_card)

    def _on_card_scored(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.debuffed:
            return

        self._card_scored_action(
            scored_card, played_cards, scored_card_indices, poker_hands_played
        )
        self._card_scored_ability(
            scored_card, played_cards, scored_card_indices, poker_hands_played
        )

    def _on_card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        if self.debuffed:
            return 0
        return self._card_scored_retriggers(
            scored_card, played_cards, scored_card_indices, poker_hands_played
        )

    def _on_created(self) -> None:
        if self.debuffed:
            return

        self._created_action()

    def _on_dependent(self, other_joker: BaseJoker) -> None:
        if self.debuffed:
            return

        self._dependent_ability(other_joker)

    def _on_discard(self, discarded_cards: list[Card]) -> None:
        if self.debuffed:
            return

        self._discard_action(discarded_cards)
        self._discard_ability(discarded_cards)

    def _on_end_hand(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.debuffed:
            return

        self._end_hand_action(played_cards, scored_card_indices, poker_hands_played)

    def _on_hand_played(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.debuffed:
            return

        self._hand_played_action(played_cards, scored_card_indices, poker_hands_played)
        self._hand_played_ability(played_cards, scored_card_indices, poker_hands_played)

    def _on_independent(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.debuffed:
            return

        self._independent_ability(played_cards, scored_card_indices, poker_hands_played)

    def _on_item_sold(self, sold_item: Sellable) -> None:
        if self.debuffed:
            return

        self._item_sold_action(sold_item)
        self._item_sold_ability(sold_item)

    def _on_jokers_moved(self) -> None:
        pass

    def _on_lucky_card_triggered(self) -> None:
        if self.debuffed:
            return

        self._lucky_card_triggered_action()

    def _on_pack_opened(self) -> None:
        if self.debuffed:
            return

        self._pack_opened_ability()

    def _on_pack_skipped(self) -> None:
        if self.debuffed:
            return

        self._pack_skipped_action()

    def _on_planet_used(self) -> None:
        if self.debuffed:
            return

        self._planet_used_action()

    def _on_round_ended(self) -> None:
        if self.debuffed:
            return

        if self.rental:
            self._run.money -= 3

        if self.perishable:
            self._perishable_rounds_left -= 1
            if self._perishable_rounds_left == 0:
                self.debuffed = True
                return

        self._round_ended_action()

    def _on_shop_exited(self) -> None:
        if self.debuffed:
            return

        self._shop_exited_ability()

    def _on_shop_rerolled(self) -> None:
        if self.debuffed:
            return

        self._shop_rerolled_action()

    def _pack_opened_ability(self) -> None:
        pass

    def _pack_skipped_action(self) -> None:
        pass

    def _planet_used_action(self) -> None:
        pass

    def _round_ended_action(self) -> None:
        pass

    def _shop_exited_ability(self) -> None:
        pass

    def _shop_rerolled_action(self) -> None:
        pass

    @property
    @abstractmethod
    def joker_type(self) -> JokerType:
        pass


@dataclass(eq=False)
class CopyJoker(BaseJoker):
    _copy_loop: bool = field(default=False, init=False, repr=False)

    copied_joker: BaseJoker | None = field(default=None, init=False, repr=False)

    def _blind_selected_ability(self) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._blind_selected_ability()

    def _boss_blind_triggered_ability(self) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._boss_blind_triggered_ability()

    def _card_held_ability(self, held_card: Card) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._card_held_ability(held_card)

    def _card_held_retriggers(self, held_card: Card) -> int:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            return self.copied_joker._card_held_retriggers(held_card)
        return 0

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._card_scored_ability(
                scored_card, played_cards, scored_card_indices, poker_hands_played
            )

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            return self.copied_joker._card_scored_retriggers(
                scored_card, played_cards, scored_card_indices, poker_hands_played
            )
        return 0

    def _dependent_ability(self, other_joker: BaseJoker) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._dependent_ability(other_joker)

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._discard_ability(discarded_cards)

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._hand_played_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._independent_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def _item_sold_ability(self, sold_item: Sellable) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._item_sold_ability(sold_item)

    def _pack_opened_ability(self) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._pack_opened_ability()

    def _shop_exited_ability(self) -> None:
        if (
            not self._copy_loop
            and self.copied_joker is not None
            and not self.copied_joker.debuffed
        ):
            self.copied_joker._shop_exited_ability()

    @property
    @abstractmethod
    def joker_type(self) -> JokerType:
        pass


@dataclass(eq=False)
class Consumable(Sellable):
    card: Tarot | Planet | Spectral

    is_negative: bool = False

    def __eq__(self, other: Consumable | Tarot | Planet | Spectral) -> bool:
        match other:
            case Consumable():
                return self is other
            case Tarot() | Planet() | Spectral():
                return self.card is other

        return NotImplemented

    def _repr_png_(self) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, as_image=False)


@total_ordering
@dataclass(eq=False)
class Card:
    rank: Rank
    suit: Suit

    enhancement: Enhancement | None = None
    seal: Seal | None = None
    edition: Edition = Edition.BASE

    bonus_chips: int = field(default=0, init=False, repr=False)
    debuffed: bool = field(default=False, init=False, repr=False)
    flipped: bool = field(default=False, init=False, repr=False)

    def __eq__(self, other: Card | Rank | Suit | Enhancement | Seal | Edition) -> bool:
        match other:
            case Card():
                return self is other
            case Rank():
                return (
                    not self.debuffed and not self.is_stone_card and self.rank is other
                )
            case Suit():
                return (
                    not self.debuffed and not self.is_stone_card and self.suit is other
                )
            case Enhancement():
                return not self.debuffed and self.enhancement is other
            case Seal():
                return not self.debuffed and self.seal is other
            case Edition():
                return not self.debuffed and self.edition is other

        return NotImplemented

    def __lt__(self, other: Card) -> bool:
        match other:
            case Card():
                return self.rank.__lt__(other.rank)

        return NotImplemented

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def _repr_png_(self, card_back: Deck = Deck.RED) -> bytes:
        from .sprites import get_sprite

        return get_sprite(self, card_back=card_back, as_image=False)

    @property
    def chips(self) -> int:
        if self.debuffed:
            return 0
        return (50 if self.is_stone_card else self.rank.chips) + self.bonus_chips

    @property
    def is_stone_card(self) -> bool:
        return self.enhancement is Enhancement.STONE
