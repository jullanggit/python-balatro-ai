from copy import copy
from dataclasses import dataclass, field
import random as r

from .classes import *
from .enums import *


# ---- copiers/ ---- #


@dataclass(eq=False)
class Blueprint(CopyJoker):
    """
    Copies ability of Joker to the right
    """

    def _on_jokers_moved(self) -> None:
        i = self._run._jokers.index(self)
        self._copied_joker = (
            self._run._jokers[i + 1] if i < len(self._run._jokers) - 1 else None
        )


@dataclass(eq=False)
class Brainstorm(CopyJoker):
    """
    Copies the ability of leftmost Joker
    """

    def _on_jokers_moved(self) -> None:
        self._copied_joker = self._run._jokers[0]

        self._copy_loop = False
        visited_jokers = set()
        joker = self
        while isinstance(joker, CopyJoker):
            if joker in visited_jokers:
                self._copy_loop = True
                return

            visited_jokers.add(joker)
            joker = joker._copied_joker


# ---- /copiers ---- #

# ---- on-played/ ---- #


@dataclass(eq=False)
class SpaceJoker(BalatroJoker):
    """
    1 in 4 chance to upgrade level of played poker hand
    """

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._chance(1, 4):
            self._run._poker_hand_info[poker_hands_played[0]][0] += 1


@dataclass(eq=False)
class DNA(BalatroJoker):
    """
    If first hand of round has only 1 card, add a permanent copy to deck and draw it to hand
    """

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._first_hand and len(played_cards) == 1:
            card_copy = copy(played_cards[0])
            self._run._add_card(card_copy, draw_to_hand=True)


@dataclass(eq=False)
class ToDoList(DynamicJoker):
    """
    Earn $4 if poker hand is a [poker hand], poker hand changes at end of round
    """

    poker_hand: PokerHand = field(
        default_factory=lambda: r.choice(list(PokerHand)[3:]), init=False, repr=False
    )

    def _change_state(self) -> None:
        self.poker_hand = r.choice(self._run._unlocked_poker_hands)

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[0] is self.poker_hand:
            self._run._money += 4


@dataclass(eq=False)
class MidasMask(BalatroJoker):
    """
    All played face cards become Gold cards when scored
    """

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for i in scored_card_indices:
            scored_card = played_cards[i]
            if self._run._is_face_card(scored_card):
                scored_card.enhancement = Enhancement.GOLD


# ---- /on-played ---- #

# ---- on-scored/ ---- #


@dataclass(eq=False)
class GreedyJoker(BalatroJoker):
    """
    Played cards with Diamond suit give +3 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.DIAMONDS in self._run._get_card_suits(scored_card):
            self._run._mult += 3


@dataclass(eq=False)
class LustyJoker(BalatroJoker):
    """
    Played cards with Heart suit give +3 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.HEARTS in self._run._get_card_suits(scored_card):
            self._run._mult += 3


@dataclass(eq=False)
class WrathfulJoker(BalatroJoker):
    """
    Played cards with Spade suit give +3 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.SPADES in self._run._get_card_suits(scored_card):
            self._run._mult += 3


@dataclass(eq=False)
class GluttonousJoker(BalatroJoker):
    """
    Played cards with Club suit give +3 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.CLUBS in self._run._get_card_suits(scored_card):
            self._run._mult += 3


@dataclass(eq=False)
class EightBall(BalatroJoker):
    """
    1 in 4 chance for each played 8 to create a Tarot card when scored
    (Must have room)
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            self._run.consumable_slots > len(self._run._consumables)
            and scored_card == Rank.EIGHT
            and self._run._chance(1, 4)
        ):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))


@dataclass(eq=False)
class Dusk(BalatroJoker):
    """
    Retrigger all played cards in final hand of the round
    """

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return int(self._run._hands == 0)


@dataclass(eq=False)
class Fibonacci(BalatroJoker):
    """
    Each played Ace, 2, 3, 5, or 8 gives +8 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [
            Rank.ACE,
            Rank.TWO,
            Rank.THREE,
            Rank.FIVE,
            Rank.EIGHT,
        ]:
            self._run._mult += 8


@dataclass(eq=False)
class ScaryFace(BalatroJoker):
    """
    Played face cards give +30 Chips when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._is_face_card(scored_card):
            self._run._chips += 30


@dataclass(eq=False)
class Hack(BalatroJoker):
    """
    Retrigger each played 2, 3, 4, or 5
    """

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return int(
            scored_card
            in [
                Rank.TWO,
                Rank.THREE,
                Rank.FOUR,
                Rank.FIVE,
            ]
        )


@dataclass(eq=False)
class EvenSteven(BalatroJoker):
    """
    Played cards with even rank give +4 Mult when scored
    (10, 8, 6, 4, 2)
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [
            Rank.TWO,
            Rank.FOUR,
            Rank.SIX,
            Rank.EIGHT,
            Rank.TEN,
        ]:
            self._run._mult += 4


@dataclass(eq=False)
class OddTodd(BalatroJoker):
    """
    Played cards with odd rank give +31 Chips when scored
    (A, 9, 7, 5, 3)
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [
            Rank.THREE,
            Rank.FIVE,
            Rank.SEVEN,
            Rank.NINE,
            Rank.ACE,
        ]:
            self._run._chips += 31


@dataclass(eq=False)
class Scholar(BalatroJoker):
    """
    Played Aces give +20 Chips and +4 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card == Rank.ACE:
            self._run._chips += 20
            self._run._mult += 4


@dataclass(eq=False)
class BusinessCard(BalatroJoker):
    """
    Played face cards have a 1 in 2 chance to give $2 when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._is_face_card(scored_card) and self._run._chance(1, 2):
            self._run._money += 2


@dataclass(eq=False)
class Hiker(BalatroJoker):
    """
    Every played card permanently gains +5 Chips when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        scored_card.extra_chips += 5


@dataclass(eq=False)
class Photograph(BalatroJoker):
    """
    First played face card gives X2 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card is next(
            (
                played_cards[i]
                for i in scored_card_indices
                if self._run._is_face_card(played_cards[i])
            ),
            None,
        ):
            self._run._mult *= 2


@dataclass(eq=False)
class AncientJoker(DynamicJoker):
    """
    Each played card with [suit] suit gives X1.5 Mult when scored,
    suit changes at end of round
    """

    suit: Suit = field(default=Suit.SPADES, init=False, repr=False)

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.suit in self._run._get_card_suits(scored_card):
            self._run._mult *= 1.5

    def _change_state(self) -> None:
        self.suit = r.choice([suit for suit in Suit if suit is not self.suit])


@dataclass(eq=False)
class WalkieTalkie(BalatroJoker):
    """
    Each played 10 or 4 gives +10 Chips and +4 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [Rank.TEN, Rank.FOUR]:
            self._run._chips += 10
            self._run._mult += 4


@dataclass(eq=False)
class Seltzer(BalatroJoker):
    """
    Retrigger all cards played for the next 10 hands
    """

    hands_left: int = field(default=10, init=False, repr=False)

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return 1

    def _scoring_completed_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self.hands_left -= 1
        if self.hands_left == 0:
            self._run._destroy_joker(self)


@dataclass(eq=False)
class SmileyFace(BalatroJoker):
    """
    Played face cards give +5 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._is_face_card(scored_card):
            self._run._mult += 5


@dataclass(eq=False)
class GoldenTicket(BalatroJoker):
    """
    Played Gold cards earn $4 when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card == Enhancement.GOLD:
            self._run._money += 4


@dataclass(eq=False)
class SockAndBuskin(BalatroJoker):
    """
    Retrigger all played face cards
    """

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return int(self._run._is_face_card(scored_card))


@dataclass(eq=False)
class HangingChad(BalatroJoker):
    """
    Retrigger first played card used in scoring 2 additional times
    """

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return 2 if (scored_card is played_cards[scored_card_indices[0]]) else 0


@dataclass(eq=False)
class RoughGem(BalatroJoker):
    """
    Played cards with Diamond suit earn $1 when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.DIAMONDS in self._run._get_card_suits(scored_card):
            self._run._money += 1


@dataclass(eq=False)
class Bloodstone(BalatroJoker):
    """
    1 in 2 chance for played cards with Heart suit to give X1.5 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            Suit.HEARTS in self._run._get_card_suits(scored_card)
        ) and self._run._chance(1, 2):
            self._run._mult *= 1.5


@dataclass(eq=False)
class Arrowhead(BalatroJoker):
    """
    Played cards with Spade suit give +50 Chips when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.SPADES in self._run._get_card_suits(scored_card):
            self._run._chips += 50


@dataclass(eq=False)
class OnyxAgate(BalatroJoker):
    """
    Played cards with Club suit give +7 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.CLUBS in self._run._get_card_suits(scored_card):
            self._run._mult += 7


@dataclass(eq=False)
class TheIdol(DynamicJoker):
    """
    Each played [card] gives X2 Mult when scored
    Card changes every round
    """

    card: Card = field(
        default_factory=lambda: Card(Rank.ACE, Suit.SPADES), init=False, repr=False
    )

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            scored_card == self.card.rank
            and self.card.suit in self._run._get_card_suits(scored_card)
        ):
            self._run._mult *= 2

    def _change_state(self) -> None:
        valid_deck_cards = [
            deck_card
            for deck_card in self._run._deck_cards
            if not deck_card.is_stone_card
        ]
        if valid_deck_cards:
            random_deck_card = r.choice(valid_deck_cards)
            self.card = Card(random_deck_card.rank, random_deck_card.suit)
        else:
            self.card = Card(Rank.ACE, Suit.SPADES)


@dataclass(eq=False)
class Triboulet(BalatroJoker):
    """
    Played Kings and Queens each give X2 Mult when scored
    """

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [Rank.KING, Rank.QUEEN]:
            self._run._mult *= 2


# ---- /on-scored ---- #

# ---- on-held/ ---- #


@dataclass(eq=False)
class Mime(BalatroJoker):
    """
    Retrigger all card held in hand abilities
    """

    def _card_held_retriggers(self, held_card: Card) -> int:
        return 1


@dataclass(eq=False)
class RaisedFist(BalatroJoker):
    """
    Adds double the rank of lowest ranked card held in hand to Mult
    """

    def _card_held_ability(self, held_card: Card) -> None:
        valid_hand_cards = [
            hand_card for hand_card in self._run._hand if not hand_card.is_stone_card
        ]
        if (
            valid_hand_cards
            and held_card is min(reversed(valid_hand_cards))
            and not held_card.is_debuffed
        ):
            self._run._mult += held_card.rank.chips * 2


@dataclass(eq=False)
class Baron(BalatroJoker):
    """
    Each King held in hand gives X1.5 Mult
    """

    def _card_held_ability(self, held_card: Card) -> None:
        if held_card == Rank.KING:
            self._run._mult *= 1.5


@dataclass(eq=False)
class ReservedParking(BalatroJoker):
    """
    Each face card held in hand has a 1 in 2 chance to give $1
    """

    def _card_held_ability(self, held_card: Card) -> None:
        if self._run._is_face_card(held_card) and self._run._chance(1, 2):
            self._run._money += 1


@dataclass(eq=False)
class ShootTheMoon(BalatroJoker):
    """
    Each Queen held in hand gives +13 Mult
    """

    def _card_held_ability(self, held_card: Card) -> None:
        if held_card == Rank.QUEEN:
            self._run._mult += 13


# ---- /on-held ---- #

# ---- independent/ ---- #


@dataclass(eq=False)
class Joker(BalatroJoker):
    """
    +4 Mult
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 4


@dataclass(eq=False)
class JollyJoker(BalatroJoker):
    """
    +8 Mult if played hand contains a Pair
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._run._mult += 8


@dataclass(eq=False)
class ZanyJoker(BalatroJoker):
    """
    +12 Mult if played hand contains a Three of a Kind
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._run._mult += 12


@dataclass(eq=False)
class MadJoker(BalatroJoker):
    """
    +10 Mult if played hand contains a Two Pair
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self._run._mult += 10


@dataclass(eq=False)
class CrazyJoker(BalatroJoker):
    """
    +12 Mult if played hand contains a Straight
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._run._mult += 12


@dataclass(eq=False)
class DrollJoker(BalatroJoker):
    """
    +10 Mult if played hand contains a Flush
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._run._mult += 10


@dataclass(eq=False)
class SlyJoker(BalatroJoker):
    """
    +50 Chips if played hand contains a Pair
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._run._chips += 50


@dataclass(eq=False)
class WilyJoker(BalatroJoker):
    """
    +100 Chips if played hand contains a Three of a Kind
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._run._chips += 100


@dataclass(eq=False)
class CleverJoker(BalatroJoker):
    """
    +80 Chips if played hand contains a Two Pair
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self._run._chips += 80


@dataclass(eq=False)
class DeviousJoker(BalatroJoker):
    """
    +100 Chips if played hand contains a Straight
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._run._chips += 100


@dataclass(eq=False)
class CraftyJoker(BalatroJoker):
    """
    +80 Chips if played hand contains a Flush
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._run._chips += 80


@dataclass(eq=False)
class HalfJoker(BalatroJoker):
    """
    +20 Mult if played hand contains 3 or fewer cards.
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if len(played_cards) <= 3:
            self._run._mult += 20


@dataclass(eq=False)
class JokerStencil(BalatroJoker):
    """
    X1 Mult for each empty Joker slot
    Joker Stencil included
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= max(
            1.0,
            1.0
            * (
                (self._run.joker_slots - len(self._run._jokers))
                + sum(isinstance(joker, JokerStencil) for joker in self._run._jokers)
            ),
        )


@dataclass(eq=False)
class CeremonialDagger(MultScalingJoker):
    """
    When Blind is selected, destroy Joker to the right and permanently add double its sell value to this Mult
    """

    def _blind_selected_action(self) -> None:
        i = self._run._jokers.index(self)
        if i < len(self._run._jokers) - 1:
            right_joker = self._run._jokers[i + 1]
            if self._run._destroy_joker(right_joker):
                self.mult += self._run._calculate_sell_value(right_joker) * 2


@dataclass(eq=False)
class Banner(BalatroJoker):
    """
    +30 Chips for each remaining discard
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 30 * self._run._discards


@dataclass(eq=False)
class MysticSummit(BalatroJoker):
    """
    +15 Mult when 0 discards remaining
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._discards == 0:
            self._run._mult += 15


@dataclass(eq=False)
class LoyaltyCard(BalatroJoker):
    """
    X4 Mult every 6 hands played
    """

    hands_remaining: int = field(default=5, init=False, repr=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.hands_remaining == 0:
            self._run._mult *= 4

    def _scoring_completed_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.hands_remaining == 0:
            self.hands_remaining = 5
        else:
            self.hands_remaining -= 1


@dataclass(eq=False)
class Misprint(BalatroJoker):
    """
    +0-23 Mult
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += r.randint(0, 23)


@dataclass(eq=False)
class SteelJoker(BalatroJoker):
    """
    Gives X0.2 Mult for each Steel Card in your full deck
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= 1.0 + (
            0.2
            * sum(
                deck_card.enhancement is Enhancement.STEEL
                for deck_card in self._run._deck_cards
            )
        )


@dataclass(eq=False)
class AbstractJoker(BalatroJoker):
    """
    +3 Mult for each Joker card
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 3 * len(self._run._jokers)


@dataclass(eq=False)
class GrosMichel(BalatroJoker):
    """
    +15 Mult
    1 in 6 chance this is destroyed at the end of round.
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 15

    def _round_ended_action(self) -> None:
        if self._run._chance(1, 6):
            self._run._destroy_joker(self)
            self._run._gros_michel_extinct = True


@dataclass(eq=False)
class Supernova(BalatroJoker):
    """
    Adds the number of times poker hand has been played this run to Mult
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self._run._poker_hand_info[poker_hands_played[0]][1]


@dataclass(eq=False)
class Blackboard(BalatroJoker):
    """
    X3 Mult if all cards held in hand are Spades or Clubs
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for held_card in self._run._hand:
            held_card_suits = self._run._get_card_suits(held_card, force_base_suit=True)
            if Suit.SPADES not in held_card_suits and Suit.CLUBS not in held_card_suits:
                break
        else:
            self._run._mult *= 3


@dataclass(eq=False)
class IceCream(ChipsScalingJoker):
    """
    +100 Chips
    -5 Chips for every hand played
    """

    chips: int = field(default=100, init=False, repr=False)

    def _scoring_completed_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self.chips -= 5
        if self.chips == 0:
            self._run._destroy_joker(self)


@dataclass(eq=False)
class BlueJoker(BalatroJoker):
    """
    +2 Chips for each remaining card in deck
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 2 * len(self._run._deck_cards_left)


@dataclass(eq=False)
class Constellation(XMultScalingJoker):
    """
    This Joker gains X0.1 Mult every time a Planet card is used
    """

    def _planet_used_action(self) -> None:
        self.xmult += 0.1


@dataclass(eq=False)
class Superposition(BalatroJoker):
    """
    Create a Tarot card if poker hand contains an Ace and a Straight
    (Must have room)
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            self._run.consumable_slots > len(self._run._consumables)
            and PokerHand.STRAIGHT in poker_hands_played
            and any(played_cards[i] == Rank.ACE for i in scored_card_indices)
        ):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))


@dataclass(eq=False)
class Cavendish(BalatroJoker):
    """
    X3 Mult
    1 in 1000 chance this card is destroyed at the end of round
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= 3

    def _round_ended_action(self) -> None:
        if self._run._chance(1, 1000):
            self._run._destroy_joker(self)


@dataclass(eq=False)
class CardSharp(BalatroJoker):
    """
    X3 Mult if played poker hand has already been played this round
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[0] in self._run._round_poker_hands:
            self._run._mult *= 3


@dataclass(eq=False)
class RedCard(MultScalingJoker):
    """
    This Joker gains +3 Mult when any Booster Pack is skipped
    """

    def _pack_skipped_action(self) -> None:
        self.mult += 3


@dataclass(eq=False)
class Madness(XMultScalingJoker):
    """
    When Small Blind or Big Blind is selected, gain X0.5 Mult and destroy a random Joker
    """

    def _blind_selected_action(self) -> None:
        if not self._run._is_boss_blind:
            self.xmult += 0.5

            valid_destroys = [
                joker
                for joker in self._run._jokers
                if joker is not self and not joker.is_eternal
            ]
            if valid_destroys:
                self._run._destroy_joker(r.choice(valid_destroys))


@dataclass(eq=False)
class Seance(BalatroJoker):
    """
    If poker hand is a Straight Flush, create a random Spectral card
    (Must have room)
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            self._run.consumable_slots > len(self._run._consumables)
            and poker_hands_played[0] is PokerHand.STRAIGHT_FLUSH
        ):
            self._run._consumables.append(self._run._get_random_consumable(Spectral))


@dataclass(eq=False)
class Hologram(XMultScalingJoker):
    """
    This Joker gains X0.25 Mult every time a playing card is added to your deck
    """

    def _card_added_action(self, added_card: Card) -> None:
        self.xmult += 0.25


@dataclass(eq=False)
class Vagabond(BalatroJoker):
    """
    Create a Tarot card if hand is played with $4 or less
    """

    _will_create: bool = field(default=False, init=False, repr=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._will_create = self._run._money <= 4

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._will_create and self._run.consumable_slots > len(
            self._run._consumables
        ):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))


@dataclass(eq=False)
class Erosion(BalatroJoker):
    """
    +4 Mult for each card below [the deck's starting size] in your full deck
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 4 * max(
            0,
            self._run._deck.starting_size - len(self._run._deck_cards),
        )


@dataclass(eq=False)
class FortuneTeller(BalatroJoker):
    """
    +1 Mult per Tarot card used this run
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self._run._num_tarot_cards_used


@dataclass(eq=False)
class StoneJoker(BalatroJoker):
    """
    Gives +25 Chips for each Stone Card in your full deck
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 25 * sum(
            deck_card.is_stone_card for deck_card in self._run._deck_cards
        )


@dataclass(eq=False)
class Bull(BalatroJoker):
    """
    +2 Chips for each $1 you have
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 2 * max(0, self._run._money)


@dataclass(eq=False)
class FlashCard(MultScalingJoker):
    """
    This Joker gains +2 Mult per reroll in the shop
    """

    def _shop_rerolled_action(self) -> None:
        self.mult += 2


@dataclass(eq=False)
class Popcorn(MultScalingJoker):
    """
    +20 Mult
    -4 Mult per round played
    """

    mult: int = field(default=20, init=False, repr=False)

    def _round_ended_action(self) -> None:
        self.mult -= 4
        if self.mult == 0:
            self._run._destroy_joker(self)


@dataclass(eq=False)
class Campfire(XMultScalingJoker):
    """
    This Joker gains X0.25 Mult for each card sold, resets when Boss Blind is defeated
    """

    def _boss_defeated_action(self) -> None:
        self.xmult = 1.0

    def _item_sold_action(self, sold_item: Sellable) -> None:
        self.xmult += 0.25


@dataclass(eq=False)
class Acrobat(BalatroJoker):
    """
    X3 Mult on final hand of round
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._hands == 0:
            self._run._mult *= 3


@dataclass(eq=False)
class Swashbuckler(BalatroJoker):
    """
    Adds the sell value of all other owned Jokers to Mult
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += sum(
            self._run._calculate_sell_value(joker)
            for joker in self._run._jokers
            if joker is not self
        )


@dataclass(eq=False)
class Throwback(BalatroJoker):
    """
    X0.25 Mult for each Blind skipped this run
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= 1.0 + (0.25 * self._run._num_blinds_skipped)


@dataclass(eq=False)
class GlassJoker(XMultScalingJoker):
    """
    This Joker gains X0.75 Mult for every Glass Card that is destroyed
    """

    def _card_destroyed_action(self, destroyed_card: Card) -> None:
        if destroyed_card == Enhancement.GLASS:
            self.xmult += 0.75


@dataclass(eq=False)
class FlowerPot(BalatroJoker):
    """
    X3 Mult if poker hand contains a Diamond card, Club card, Heart card, and Spade card
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        scored_suits = set()
        possible_suits = sorted(
            (
                self._run._get_card_suits(played_cards[i], force_base_suit=True)
                for i in scored_card_indices
            ),
            key=len,
        )

        for suits in possible_suits:
            for suit in suits:
                if suit not in scored_suits:
                    scored_suits.add(suit)
                    break

        if len(scored_suits) == 4:
            self._run._mult *= 3


@dataclass(eq=False)
class SeeingDouble(BalatroJoker):
    """
    X2 Mult if played hand has a scoring Club card and a scoring card of any other suit
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        club, other = False, False
        possible_suits = sorted(
            (
                self._run._get_card_suits(played_cards[i], force_base_suit=True)
                for i in scored_card_indices
            ),
            key=len,
        )

        for suits in possible_suits:
            if not club and Suit.CLUBS in suits:
                club = True
            elif not other and any(
                suit in suits for suit in Suit if suit is not Suit.CLUBS
            ):
                other = True

        if club and other:
            self._run._mult *= 2


@dataclass(eq=False)
class Matador(BalatroJoker):
    """
    Earn $8 if played hand triggers the Boss Blind ability
    """

    def _boss_blind_triggered_ability(self) -> None:
        self._run._money += 8


@dataclass(eq=False)
class TheDuo(BalatroJoker):
    """
    X2 Mult if played hand contains a Pair
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._run._mult *= 2


@dataclass(eq=False)
class TheTrio(BalatroJoker):
    """
    X3 Mult if played hand contains a Three of a Kind
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._run._mult *= 3


@dataclass(eq=False)
class TheFamily(BalatroJoker):
    """
    X4 Mult if played hand contains a Four of a Kind
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FOUR_OF_A_KIND in poker_hands_played:
            self._run._mult *= 4


@dataclass(eq=False)
class TheOrder(BalatroJoker):
    """
    X3 Mult if played hand contains a Straight
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._run._mult *= 3


@dataclass(eq=False)
class TheTribe(BalatroJoker):
    """
    X2 Mult if played hand contains a Flush
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._run._mult *= 2


@dataclass(eq=False)
class Stuntman(BalatroJoker):
    """
    +250 Chips,
    -2 hand size
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 250


@dataclass(eq=False)
class DriversLicense(BalatroJoker):
    """
    X3 Mult if you have at least 16 Enhanced cards in your full deck
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            sum(
                deck_card.enhancement is not None for deck_card in self._run._deck_cards
            )
            >= 16
        ):
            self._run._mult *= 3


@dataclass(eq=False)
class Bootstraps(BalatroJoker):
    """
    +2 Mult for every $5 you have
    """

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 2 * max(0, self._run._money // 5)


@dataclass(eq=False)
class Canio(XMultScalingJoker):
    """
    This Joker gains X1 Mult when a face card is destroyed
    """

    def _card_destroyed_action(self, destroyed_card: Card) -> None:
        if self._run._is_face_card(destroyed_card):
            self.xmult += 1.0


# ---- /independent ---- #

# ---- mixed/ ---- #


@dataclass(eq=False)
class RideTheBus(MultScalingJoker):
    """
    This Joker gains +1 Mult per consecutive hand played without a scoring face card
    """

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if not any(
            self._run._is_face_card(played_cards[i]) for i in scored_card_indices
        ):
            self.mult += 1
        else:
            self.mult = 0


@dataclass(eq=False)
class Runner(ChipsScalingJoker):
    """
    Gains +15 Chips if played hand contains a Straight
    """

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self.chips += 15


@dataclass(eq=False)
class GreenJoker(MultScalingJoker):
    """
    +1 Mult per hand played
    -1 Mult per discard
    """

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.mult = max(0, self.mult - 1)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self.mult += 1


@dataclass(eq=False)
class SquareJoker(ChipsScalingJoker):
    """
    This Joker gains +4 Chips if played hand has exactly 4 cards
    """

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if len(played_cards) == 4:
            self.chips += 4


@dataclass(eq=False)
class Vampire(XMultScalingJoker):
    """
    This Joker gains X0.1 Mult per scoring Enhanced card played, removes card Enhancement
    """

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for i in scored_card_indices:
            scored_card = played_cards[i]
            if scored_card.enhancement is not None:
                self.xmult += 0.1
                scored_card.enhancement = None


@dataclass(eq=False)
class Obelisk(XMultScalingJoker):
    """
    This Joker gains X0.2 Mult per consecutive hand played without playing your most played poker hand
    """

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._poker_hand_info[poker_hands_played[0]][1] < max(
            times_played
            for hand_level, times_played in self._run._poker_hand_info.values()
        ):
            self.xmult += 0.2
        else:
            self.xmult = 1.0


@dataclass(eq=False)
class LuckyCat(XMultScalingJoker):
    """
    This Joker gains X0.25 Mult every time a Lucky card successfully triggers
    """

    def _lucky_card_triggered_action(self) -> None:
        self.xmult += 0.25


@dataclass(eq=False)
class SpareTrousers(MultScalingJoker):
    """
    This Joker gains +2 Mult if played hand contains a Two Pair
    """

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self.mult += 2


@dataclass(eq=False)
class Ramen(XMultScalingJoker):
    """
    X2 Mult, loses X0.01 Mult per card discarded
    """

    xmult: float = field(default=2.0, init=False, repr=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.xmult -= 0.01 * len(discarded_cards)
        if self.xmult <= 1.0:
            self._run._destroy_joker(self)


@dataclass(eq=False)
class Castle(ChipsScalingJoker, DynamicJoker):
    """
    This Joker gains +3 Chips per discarded [suit] card, suit changes every round
    """

    suit: Suit = field(default=Suit.SPADES, init=False, repr=False)

    def _change_state(self) -> None:
        valid_suits = [
            deck_card.suit
            for deck_card in self._run._deck_cards
            if not deck_card.is_stone_card
        ]
        self.suit = r.choice(valid_suits) if valid_suits else Suit.SPADES

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.chips += 3 * sum(
            self.suit in self._run._get_card_suits(discarded_card)
            for discarded_card in discarded_cards
        )


@dataclass(eq=False)
class WeeJoker(ChipsScalingJoker):
    """
    This Joker gains +8 Chips when each played 2 is scored
    """

    def _card_scored_action(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card == Rank.TWO:
            self.chips += 8


@dataclass(eq=False)
class HitTheRoad(XMultScalingJoker):
    """
    This Joker gains X0.5 Mult for every Jack discarded this round
    """

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.xmult += 0.5 * (discarded_cards.count(Rank.JACK))

    def _round_ended_action(self) -> None:
        self.xmult = 1.0


@dataclass(eq=False)
class Yorick(XMultScalingJoker):
    """
    This Joker gains X1 Mult every 23 cards discarded
    """

    discards_remaining: int = field(default=23, init=False, repr=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.discards_remaining -= len(discarded_cards)
        while self.discards_remaining <= 0:
            self.xmult += 1.0
            self.discards_remaining += 23


# ---- /mixed ---- #

# ---- on-other-jokers/ ---- #


@dataclass(eq=False)
class BaseballCard(BalatroJoker):
    """
    Uncommon Jokers each give X1.5 Mult
    """

    def _dependent_ability(self, other_joker: BalatroJoker) -> None:
        from .constants import JOKER_RARITIES

        if other_joker in JOKER_RARITIES[Rarity.UNCOMMON]:
            self._run._mult *= 1.5


# ---- /on-other-jokers ---- #

# ---- on-discard/ ---- #


@dataclass(eq=False)
class FacelessJoker(BalatroJoker):
    """
    Earn $5 if 3 or more face cards are discarded at the same time
    """

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if (
            sum(
                self._run._is_face_card(discarded_card)
                for discarded_card in discarded_cards
            )
            >= 3
        ):
            self._run._money += 5


@dataclass(eq=False)
class MailInRebate(DynamicJoker):
    """
    Earn $5 for each discarded [rank], rank changes every round
    """

    rank: Rank = field(default=Rank.ACE, init=False, repr=False)

    def _change_state(self) -> None:
        valid_ranks = [
            deck_card.rank
            for deck_card in self._run._deck_cards
            if not deck_card.is_stone_card
        ]
        self.rank = r.choice(valid_ranks) if valid_ranks else Rank.ACE

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        self._run._money += 5 * discarded_cards.count(self.rank)


@dataclass(eq=False)
class TradingCard(BalatroJoker):
    """
    If first discard of round has only 1 card, destroy it and earn $3
    """

    # TODO: check this running along with other discard jokers
    def _discard_action(self, discarded_cards: list[Card]) -> None:
        if self._run._first_discard and len(discarded_cards) == 1:
            self._run._money += 3
            self._run._destroy_card(discarded_cards[0])
            discarded_cards.pop()


@dataclass(eq=False)
class BurntJoker(BalatroJoker):
    """
    Upgrade the level of the first discarded poker hand each round
    """

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if self._run._first_discard:
            self._run._poker_hand_info[
                max(self._run._get_poker_hands(discarded_cards))
            ][1] += 1


# ---- /on-discard ---- #

# ---- other/ ---- #


@dataclass(eq=False)
class FourFingers(BalatroJoker):
    """
    All Flushes and Straights can be made with 4 cards
    """


@dataclass(eq=False)
class CreditCard(BalatroJoker):
    """
    Go up to -$20 in debt
    """


@dataclass(eq=False)
class MarbleJoker(BalatroJoker):
    """
    Adds one Stone card to the deck when Blind is selected
    """

    def _blind_selected_ability(self) -> None:
        added_card = self._run._get_random_card()
        added_card.enhancement = Enhancement.STONE
        self._run._add_card(added_card)


@dataclass(eq=False)
class ChaosTheClown(BalatroJoker):
    """
    1 free Reroll per shop
    """


@dataclass(eq=False)
class DelayedGratification(BalatroJoker):
    """
    Earn $2 per discard if no discards are used by end of the round
    """

    def _round_ended_money(self) -> int:
        return 2 * self._run._discards if self._run._first_discard else 0


@dataclass(eq=False)
class Pareidolia(BalatroJoker):
    """
    All cards are considered face cards
    """


@dataclass(eq=False)
class Egg(BalatroJoker):
    """
    Gains $3 of sell value at end of round
    """

    def _round_ended_action(self) -> None:
        self._extra_sell_value += 3


@dataclass(eq=False)
class Burglar(BalatroJoker):
    """
    When Blind is selected, gain +3 Hands and lose all discards
    """

    def _blind_selected_ability(self) -> None:
        self._run._hands += 3
        self._run._discards = 0


@dataclass(eq=False)
class Splash(BalatroJoker):
    """
    Every played card counts in scoring
    """


@dataclass(eq=False)
class SixthSense(BalatroJoker):
    """
    If first hand of round is a single 6, destroy it and create a Spectral card
    (Must have room)
    """

    def _scoring_completed_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            self._run._first_hand
            and len(played_cards) == 1
            and played_cards[0] == Rank.SIX
        ):
            self._run._destroy_card(played_cards[0])
            if self._run.consumable_slots > len(self._run._consumables):
                self._run._consumables.append(
                    self._run._get_random_consumable(Spectral)
                )
            played_cards.pop()
            scored_card_indices.pop()


@dataclass(eq=False)
class RiffRaff(BalatroJoker):
    """
    When Blind is selected, create 2 Common Jokers
    (Must have room)
    """

    def _blind_selected_ability(self) -> None:
        for _ in range(min(2, max(0, self._run.joker_slots - len(self._run._jokers)))):
            self._run._add_joker(self._run._get_random_joker(Rarity.COMMON))


@dataclass(eq=False)
class Shortcut(BalatroJoker):
    """
    Allows Straights to be made with gaps of 1 rank
    (ex: 10 8 6 5 3)
    """


@dataclass(eq=False)
class CloudNine(BalatroJoker):
    """
    Earn $1 for each 9 in your full deck at end of round
    """

    def _round_ended_money(self) -> int:
        return self._run._deck_cards.count(Rank.NINE)


@dataclass(eq=False)
class Rocket(BalatroJoker):
    """
    Earn $1 at end of round. Payout increases by $2 when Boss Blind is defeated
    """

    payout: int = field(default=1, init=False, repr=False)

    def _boss_defeated_action(self) -> None:
        self.payout += 2

    def _round_ended_money(self) -> int:
        return self.payout


@dataclass(eq=False)
class Luchador(BalatroJoker):
    """
    Sell this card to disable the current Boss Blind
    """

    def _sold_ability(self) -> None:
        self._run._disable_boss_blind()


@dataclass(eq=False)
class GiftCard(BalatroJoker):
    """
    Add $1 of sell value to every Joker and Consumable card at end of round
    """

    def _round_ended_action(self) -> None:
        for joker in self._run._jokers:
            joker._extra_sell_value += 1
        for consumable in self._run._consumables:
            consumable._extra_sell_value += 1


@dataclass(eq=False)
class TurtleBean(BalatroJoker):
    """
    +5 hand size, reduces by 1 each round
    """

    hand_size_increase: int = field(default=5, init=False, repr=False)

    def _round_ended_action(self) -> None:
        self.hand_size_increase -= 1
        if self.hand_size_increase == 0:
            self._run._destroy_joker(self)


@dataclass(eq=False)
class ToTheMoon(BalatroJoker):
    """
    Earn an extra $1 of interest for every $5 you have at end of round
    """


@dataclass(eq=False)
class Hallucination(BalatroJoker):
    """
    1 in 2 chance to create a Tarot card when any Booster Pack is opened
    (Must have room)
    """

    def _pack_opened_ability(self) -> None:
        if self._run.consumable_slots > len(
            self._run._consumables
        ) and self._run._chance(1, 2):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))


@dataclass(eq=False)
class Juggler(BalatroJoker):
    """
    +1 hand size
    """


@dataclass(eq=False)
class Drunkard(BalatroJoker):
    """
    +1 discard each round
    """


@dataclass(eq=False)
class GoldenJoker(BalatroJoker):
    """
    Earn $4 at end of round
    """

    def _round_ended_money(self) -> int:
        return 4


@dataclass(eq=False)
class DietCola(BalatroJoker):
    """
    Sell this card to create a free Double Tag
    """

    def _sold_ability(self) -> None:
        self._run._tags.append(Tag.DOUBLE)


@dataclass(eq=False)
class MrBones(BalatroJoker):
    """
    Prevents Death if chips scored are at least 25% of required chips
    self destructs
    """


@dataclass(eq=False)
class Troubadour(BalatroJoker):
    """
    +2 hand size,
    -1 hand each round
    """


@dataclass(eq=False)
class Certificate(BalatroJoker):
    """
    When round begins, add a random playing card with a random seal to your hand
    """

    def _blind_selected_ability(self) -> None:
        added_card = self._run._get_random_card()
        added_card.seal = r.choice(list(Seal))
        self._run._add_card(added_card, draw_to_hand=True)


@dataclass(eq=False)
class SmearedJoker(BalatroJoker):
    """
    Hearts and Diamonds count as the same suit, Spades and Clubs count as the same suit
    """


@dataclass(eq=False)
class Showman(BalatroJoker):
    """
    Joker, Tarot, Planet, and Spectral cards may appear multiple times
    """


@dataclass(eq=False)
class MerryAndy(BalatroJoker):
    """
    +3 discards each round,
    -1 hand size
    """


@dataclass(eq=False)
class OopsAllSixes(BalatroJoker):
    """
    Doubles all listed probabilities
    (ex: 1 in 3 -> 2 in 3)
    """


@dataclass(eq=False)
class InvisibleJoker(BalatroJoker):
    """
    After 2 rounds, sell this card to Duplicate a random Joker
    (Removes Negative from copy)
    """

    rounds_remaining: int = field(default=2, init=False, repr=False)

    def _round_ended_action(self) -> None:
        self.rounds_remaining = max(0, self.rounds_remaining - 1)

    def _sold_action(self) -> None:
        if self.rounds_remaining == 0 and len(self._run._jokers) > 1:
            duplicated_joker = copy(
                r.choice([joker for joker in self._run._jokers if joker is not self])
            )

            if duplicated_joker.edition is Edition.NEGATIVE:
                duplicated_joker.edition = Edition.BASE
            if isinstance(duplicated_joker, InvisibleJoker):
                duplicated_joker.rounds_remaining = 2

            self._run._add_joker(duplicated_joker)


@dataclass(eq=False)
class Satellite(BalatroJoker):
    """
    Earn $1 at end of round per unique Planet card used this run
    """

    def _round_ended_money(self) -> int:
        return len(self._run._unique_planet_cards_used)


@dataclass(eq=False)
class Cartomancer(BalatroJoker):
    """
    Create a Tarot card when Blind is selected
    (Must have room)
    """

    def _blind_selected_ability(self) -> None:
        if self._run.consumable_slots > len(self._run._consumables):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))


@dataclass(eq=False)
class Astronomer(BalatroJoker):
    """
    All Planet cards and Celestial Packs in the shop are free
    """


@dataclass(eq=False)
class Chicot(BalatroJoker):
    """
    Disables effect of every Boss Blind
    """

    def _blind_selected_action(self) -> None:
        self._run._disable_boss_blind()


@dataclass(eq=False)
class Perkeo(BalatroJoker):
    """
    Creates a Negative copy of 1 random consumable card in your possession at the end of the shop
    """

    def _shop_exited_ability(self) -> None:
        copied_consumable = copy(r.choice(self._run._consumables))
        copied_consumable.is_negative = True
        self._run._consumables.append(copied_consumable)


# ---- /other ---- #
