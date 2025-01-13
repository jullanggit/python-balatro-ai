from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from balatro import Run

from enums import *


@dataclass(eq=False)
class Sellable:
    extra_sell_value: int = field(default=0, init=False, repr=False)


@dataclass(eq=False)
class BaseJoker(Sellable, ABC):
    _run: Run | None = field(default=None, init=False, repr=False)

    edition: Edition = Edition.BASE

    eternal: bool = False
    perishable: bool = False
    rental: bool = False

    debuffed: bool = field(default=False, init=False, repr=False)
    face_down: bool = field(default=False, init=False, repr=False)
    perishable_rounds_left: int = field(default=5, init=False, repr=False)

    def __eq__(self, other: BaseJoker | JokerType | Edition) -> bool:
        match other:
            case BaseJoker():
                return self is other
            case JokerType():
                return self.joker_type is other
            case Edition():
                return not self.debuffed and self.edition is other
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.joker_type}"

    def _repr_png_(self) -> bytes:
        from sprites import get_sprite

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

    def _dependent_ability(self, other_joker: BaseJoker) -> None:
        pass

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        pass

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        pass

    def _end_hand_action(self) -> None:
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

    def _on_blind_selected(self) -> None:
        self._blind_selected_action()
        if not self.debuffed:
            self._blind_selected_ability()

    def _on_boss_defeated(self) -> None:
        self._boss_defeated_action()

    def _on_card_added(self, added_card: Card) -> None:
        self._card_added_action(added_card)

    def _on_card_destroyed(self, destroyed_card: Card) -> None:
        self._card_destroyed_action(destroyed_card)

    def _on_card_held(self, held_card: Card) -> None:
        if not self.debuffed:
            self._card_held_ability(held_card)

    def _on_card_held_retriggers(self, held_card: Card) -> int:
        return 0 if self.debuffed else self._card_held_retriggers(held_card)

    def _on_card_scored(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._card_scored_action(
            scored_card, played_cards, scored_card_indices, poker_hands_played
        )
        if not self.debuffed:
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
        return (
            0
            if self.debuffed
            else self._card_scored_retriggers(
                scored_card, played_cards, scored_card_indices, poker_hands_played
            )
        )

    def _on_created(self) -> None:
        pass

    def _on_dependent(self, other_joker: BaseJoker) -> None:
        if not self.debuffed:
            self._dependent_ability(other_joker)

    def _on_discard(self, discarded_cards: list[Card]) -> None:
        self._discard_action(discarded_cards)
        if not self.debuffed:
            self._discard_ability(discarded_cards)

    def _on_end_hand(self) -> None:
        self._end_hand_action()

    def _on_hand_played(
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

    def _on_independent(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not self.debuffed:
            self._independent_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def _on_item_sold(self) -> None:
        self._item_sold_action()

    def _on_leftmost_joker_changed(self) -> None:
        self._leftmost_joker_changed_action()

    def _on_lucky_card_triggered(self) -> None:
        self._lucky_card_triggered_action()

    def _on_pack_opened(self) -> None:
        if not self.debuffed:
            self._pack_opened_ability()

    def _on_pack_skipped(self) -> None:
        self._pack_skipped_action()

    def _on_planet_used(self) -> None:
        self._planet_used_action()

    def _on_right_joker_changed(self) -> None:
        self._right_joker_changed_action()

    def _on_round_ended(self) -> None:
        self._round_ended_action()
        if not self.debuffed:
            self._round_ended_ability()

    def _on_shop_exited(self) -> None:
        if not self.debuffed:
            self._shop_exited_ability()

    def _on_shop_rerolled(self) -> None:
        self._shop_rerolled_action()

    def _on_sold(self) -> None:
        self._sold_action()
        if not self.debuffed:
            self._sold_ability()

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

    @property
    @abstractmethod
    def joker_type(self) -> JokerType:
        pass


@dataclass(eq=False)
class CopyJoker(BaseJoker):
    copied_joker: BaseJoker | None = field(default=None, init=False, repr=False)

    def __eq__(self, other: BaseJoker | JokerType) -> bool:
        match other:
            case BaseJoker():
                return self is other
            case JokerType():
                return self.copied_joker == other
        return NotImplemented

    def _blind_selected_ability(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._blind_selected_ability()

    def _card_held_ability(self, held_card: Card) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._card_held_ability(held_card)

    def _card_held_retriggers(self, held_card: Card) -> int:
        return (
            0
            if self.debuffed or self.copied_joker is None
            else self.copied_joker._card_held_retriggers(held_card)
        )

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not self.debuffed and self.copied_joker is not None:
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
        return (
            0
            if self.debuffed or self.copied_joker is None
            else self.copied_joker._card_scored_retriggers(
                scored_card, played_cards, scored_card_indices, poker_hands_played
            )
        )

    def _dependent_ability(self, other_joker: BaseJoker) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._dependent_ability(other_joker)

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._discard_ability(discarded_cards)

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._hand_played_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._independent_ability(
                played_cards, scored_card_indices, poker_hands_played
            )

    def _pack_opened_ability(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._pack_opened_ability()

    def _round_ended_ability(self) -> None:
        # left out by design - end of round jokers (which all seem to be economy) aren't copyable for some reason
        # if not self.debuffed and self.copied_joker is not None:
        #     self.copied_joker._round_ended_ability()
        pass

    def _shop_exited_ability(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._shop_exited_ability()

    def _sold_ability(self) -> None:
        if not self.debuffed and self.copied_joker is not None:
            self.copied_joker._sold_ability()

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
        from sprites import get_sprite

        return get_sprite(self, False)


@dataclass(eq=False)
class Card:
    rank: Rank
    suit: Suit

    enhancement: Enhancement | None = None
    seal: Seal | None = None
    edition: Edition = Edition.BASE

    bonus_chips: int = field(default=0, init=False, repr=False)
    debuffed: bool = field(default=False, init=False, repr=False)
    face_down: bool = field(default=False, init=False, repr=False)

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
                return self.rank < other.rank
        return NotImplemented

    def __str__(self) -> str:
        return f"{self.rank} of {self.suit}"

    def _repr_png_(self) -> bytes:
        from sprites import get_sprite

        return get_sprite(self, False)

    @property
    def chips(self) -> int:
        if self.debuffed:
            return 0
        return (50 if self.is_stone_card else self.rank.chips) + self.bonus_chips

    @property
    def is_stone_card(self) -> bool:
        return self.enhancement is Enhancement.STONE
