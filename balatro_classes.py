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

    def __eq__(self, other: JokerType | Edition) -> bool:
        match other:
            case JokerType():
                return self.joker_type is other
            case Edition():
                return not self.debuffed and self.edition is other
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)

    def _blind_selected_ability(self) -> None:
        pass

    def _blind_selected_action(self) -> None:
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

    def _card_scored_ability(self, scored_card: Card) -> None:
        pass

    def _card_scored_action(self, scored_card: Card) -> None:
        pass

    def _card_scored_retriggers(self, scored_card: Card) -> int:
        return 0

    def _dependent_ability(self, other_joker: Joker) -> None:
        pass

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        pass

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        pass

    def _end_hand_action(self) -> None:
        pass

    def _glass_card_destroyed_action(self) -> None:
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

    def _item_sold_action(self) -> None:
        pass

    def _leftmost_joker_changed_action(self) -> None:
        pass

    def _lucky_card_triggered_action(self) -> None:
        pass

    def _pack_opened_ability(self) -> None:
        pass

    def _pack_skipped_action(self) -> None:
        pass

    def _planet_used_action(self) -> None:
        pass

    def _right_joker_changed_action(self) -> None:
        pass

    def _round_ended_ability(self) -> None:
        pass

    def _round_ended_action(self) -> None:
        pass

    def _shop_exited_ability(self) -> None:
        pass

    def _shop_rerolled_action(self) -> None:
        pass

    def _sold_ability(self) -> None:
        pass

    def _sold_action(self) -> None:
        pass

    def on_blind_selected(self) -> None:
        self._blind_selected_action()
        if not self.debuffed:
            self._blind_selected_ability()

    def on_boss_defeated(self) -> None:
        self._boss_defeated_action()

    def on_card_added(self, added_card: Card) -> None:
        self._card_added_action(added_card)

    def on_card_destroyed(self, destroyed_card: Card) -> None:
        self._card_destroyed_action(destroyed_card)

    def on_card_held(self, held_card: Card) -> None:
        if not self.debuffed:
            self._card_held_ability(held_card)

    def on_card_held_retriggers(self, held_card: Card) -> int:
        return 0 if self.debuffed else self._card_held_retriggers(held_card)

    def on_card_scored(self, scored_card: Card) -> None:
        self._card_scored_action(scored_card)
        if not self.debuffed:
            self._card_scored_ability(scored_card)

    def on_card_scored_retriggers(self, scored_card: Card) -> int:
        return 0 if self.debuffed else self._card_scored_retriggers(scored_card)

    def on_dependent(self, other_joker: Joker) -> None:
        if not self.debuffed:
            self._dependent_ability(other_joker)

    def on_discard(self, discarded_cards: list[Card]) -> None:
        self._discard_action(discarded_cards)
        if not self.debuffed:
            self._discard_ability(discarded_cards)

    def on_end_hand(self) -> None:
        self._end_hand_action()

    def on_glass_card_destroyed(self) -> None:
        self._glass_card_destroyed_action()

    def on_hand_played(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._hand_played_action(played_cards, scored_card_indices, poker_hands_played)
        if not self.debuffed:
            self._hand_played_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def on_independent(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not self.debuffed:
            self._independent_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def on_item_sold(self) -> None:
        self._item_sold_action()

    def on_leftmost_joker_changed(self) -> None:
        self._leftmost_joker_changed_action()

    def on_lucky_card_triggered(self) -> None:
        self._lucky_card_triggered_action()

    def on_pack_opened(self) -> None:
        if not self.debuffed:
            self._pack_opened_ability()

    def on_pack_skipped(self) -> None:
        self._pack_skipped_action()

    def on_planet_used(self) -> None:
        self._planet_used_action()

    def on_right_joker_changed(self) -> None:
        self._right_joker_changed_action()

    def on_round_ended(self) -> None:
        self._round_ended_action()
        if not self.debuffed:
            self._round_ended_ability()

    def on_shop_exited(self) -> None:
        if not self.debuffed:
            self._shop_exited_ability()

    def on_shop_rerolled(self) -> None:
        self._shop_rerolled_action()

    def on_sold(self) -> None:
        self._sold_action()
        if not self.debuffed:
            self._sold_ability()

    @property
    @abstractmethod
    def joker_type(self) -> JokerType:
        pass


@dataclass
class CopyJoker(Joker):
    copied_joker: Joker | None = field(default=None, init=False)

    def __eq__(self, other: JokerType) -> bool:
        match other:
            case JokerType():
                return self.copied_joker == other
        return NotImplemented

    def on_blind_selected(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._blind_selected_ability()

    def on_boss_defeated(self) -> None:
        pass

    def on_card_added(self, added_card: Card) -> None:
        pass

    def on_card_destroyed(self, destroyed_card: Card) -> None:
        pass

    def on_card_held(self, held_card: Card) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._card_held_ability(held_card)

    def on_card_held_retriggers(self, held_card: Card) -> int:
        return (
            0
            if self.debuffed or self.copied_joker is None
            else self.copied_joker._card_held_retriggers(held_card)
        )

    def on_card_scored(self, scored_card: Card) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._card_scored_ability(scored_card)

    def on_card_scored_retriggers(self, scored_card: Card) -> int:
        return (
            0
            if self.debuffed or self.copied_joker is None
            else self.copied_joker._card_scored_retriggers(scored_card)
        )

    def on_dependent(self, other_joker: Joker) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._dependent_ability(other_joker)

    def on_discard(self, discarded_cards: list[Card]) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._discard_ability(discarded_cards)

    def on_end_hand(self) -> None:
        pass

    def on_glass_card_destroyed(self) -> None:
        pass

    def on_hand_played(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._hand_played_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def on_independent(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._independent_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def on_item_sold(self) -> None:
        pass

    def on_leftmost_joker_changed(self) -> None:
        pass

    def on_lucky_card_triggered(self) -> None:
        pass

    def on_pack_opened(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._pack_opened_ability()

    def on_pack_skipped(self) -> None:
        pass

    def on_planet_used(self) -> None:
        pass

    def on_right_joker_changed(self) -> None:
        pass

    def on_round_ended(self) -> None:
        # by design - end of round economy jokers aren't copyable
        # if not self.debuffed and self.copied_joker is not None:
        #     self.copied_joker._round_ended_ability()
        pass

    def on_shop_exited(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._shop_exited_ability()

    def on_shop_rerolled(self) -> None:
        pass

    def on_sold(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._sold_ability()

    @property
    @abstractmethod
    def joker_type(self) -> JokerType:
        pass


@dataclass
class Consumable(Sellable):
    consumable_type: Tarot | Planet | Spectral

    is_negative: bool = False

    def __eq__(self, other: Consumable | Tarot | Planet | Spectral) -> bool:
        match other:
            case Consumable():
                return astuple(self) == astuple(other)
            case Tarot() | Planet() | Spectral():
                return self.consumable_type is other
        return NotImplemented

    def _repr_png_(self) -> bytes:
        from balatro_resources import get_sprite

        return get_sprite(self, False)


@dataclass
class Card:
    suit: Suit
    rank: Rank

    enhancement: Enhancement | None = None
    seal: Seal | None = None
    edition: Edition = Edition.BASE

    bonus_chips: int = 0

    debuffed: bool = False

    def __eq__(self, other: Suit | Rank | Enhancement | Seal | Edition) -> bool:
        match other:
            case Suit():
                return (
                    not self.debuffed and not self.is_stone_card and self.suit is other
                )
            case Rank():
                return (
                    not self.debuffed and not self.is_stone_card and self.rank is other
                )
            case Enhancement():
                return not self.debuffed and self.enhancement is other
            case Seal():
                return not self.debuffed and self.seal is other
            case Edition():
                return not self.debuffed and self.edition is other
        raise NotImplementedError  # TODO: remove
        return NotImplemented

    def __lt__(self, other: Card) -> bool:
        match other:
            case Card():
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
