from dataclasses import dataclass, field, replace
import random as r

from balatro_classes import *
from balatro_enums import *


# ---- copiers/ ---- #


@dataclass(eq=False)
class Blueprint(CopyJoker):
    def _right_joker_changed_action(self) -> None:
        self.copied_joker = None
        for i, joker in enumerate(self._balatro.jokers):
            if joker is self:
                break
        if i < len(self._balatro.jokers) - 1:
            self.copied_joker = self._balatro.jokers[i + 1]

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLUEPRINT


@dataclass(eq=False)
class Brainstorm(CopyJoker):
    def _leftmost_joker_changed_action(self) -> None:
        self.copied_joker = self._balatro.jokers[0]

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BRAINSTORM


# ---- /copiers ---- #

# ---- on-played/ ---- #


@dataclass(eq=False)
class SpaceJoker(Joker):
    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro._chance(1, 4):
            self._balatro.poker_hand_info[poker_hands_played[0]][0] += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SPACE


@dataclass(eq=False)
class DNA(Joker):
    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro.first_hand and len(played_cards) == 1:
            card_copy = replace(played_cards[0])
            self._balatro._add_card(card_copy)
            self._balatro.hand.append(card_copy)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DNA


@dataclass(eq=False)
class ToDoList(Joker):
    poker_hand: PokerHand = field(init=False)

    def __post_init__(self) -> None:
        self._set_random_poker_hand()

    def _set_random_poker_hand(self) -> None:
        self.poker_hand = r.choice(self._balatro.unlocked_poker_hands)

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[0] is self.poker_hand:
            self._balatro.money += 4

    def _round_ended_action(self) -> None:
        self._set_random_poker_hand()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TODO_LIST


@dataclass(eq=False)
class MidasMask(Joker):
    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for i in scored_card_indices:
            scored_card = played_cards[i]
            if self._balatro._is_face_card(scored_card):
                scored_card.enhancement = Enhancement.GOLD

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIDAS_MASK


# ---- /on-played ---- #

# ---- on-scored/ ---- #


@dataclass(eq=False)
class GreedyJoker(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.DIAMONDS in self._balatro._get_card_suits(scored_card):
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GREEDY_JOKER


@dataclass(eq=False)
class LustyJoker(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.HEARTS in self._balatro._get_card_suits(scored_card):
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUSTY_JOKER


@dataclass(eq=False)
class WrathfulJoker(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.SPADES in self._balatro._get_card_suits(scored_card):
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WRATHFUL_JOKER


@dataclass(eq=False)
class GluttonousJoker(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.CLUBS in self._balatro._get_card_suits(scored_card):
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GLUTTENOUS_JOKER


@dataclass(eq=False)
class EightBall(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            scored_card == Rank.EIGHT
            and self._balatro.effective_consumable_slots
            > len(self._balatro.consumables)
            and self._balatro._chance(1, 4)
        ):
            self._balatro.consumables.append(self._balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EIGHT_BALL


@dataclass(eq=False)
class Dusk(Joker):
    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return int(self._balatro.hands == 0)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DUSK


@dataclass(eq=False)
class Fibonacci(Joker):
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
            self._balatro.mult += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FIBONACCI


@dataclass(eq=False)
class ScaryFace(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro._is_face_card(scored_card):
            self._balatro.chips += 30

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCARY_FACE


@dataclass(eq=False)
class Hack(Joker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HACK


@dataclass(eq=False)
class EvenSteven(Joker):
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
            self._balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EVEN_STEVEN


@dataclass(eq=False)
class OddTodd(Joker):
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
            self._balatro.chips += 31

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ODD_TODD


@dataclass(eq=False)
class Scholar(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card == Rank.ACE:
            self._balatro.chips += 20
            self._balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCHOLAR


@dataclass(eq=False)
class BusinessCard(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro._is_face_card(scored_card) and self._balatro._chance(1, 2):
            self._balatro.money += 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BUSINESS


@dataclass(eq=False)
class Hiker(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        scored_card.bonus_chips += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HIKER


@dataclass(eq=False)
class Photograph(Joker):
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
                if self._balatro._is_face_card(played_cards[i])
            ),
            None,
        ):
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.PHOTOGRAPH


@dataclass(eq=False)
class AncientJoker(Joker):
    suit: Suit = field(init=False)

    def __post_init__(self) -> None:
        self._set_random_suit()

    def _set_random_suit(self) -> None:
        new_suit = None
        while new_suit is None or new_suit is self.suit:
            new_suit = r.choice(list(Suit))
        self.suit = new_suit

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.suit in self._balatro._get_card_suits(scored_card):
            self._balatro.mult *= 1.5

    def _round_ended_action(self) -> None:
        self._set_random_suit()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ANCIENT


@dataclass(eq=False)
class WalkieTalkie(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [Rank.TEN, Rank.FOUR]:
            self._balatro.chips += 10
            self._balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WALKIE_TALKIE


@dataclass(eq=False)
class Seltzer(Joker):
    hands_left: int = field(default=10, init=False)

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        self.hands_left -= 1
        if self.hands_left == 0:
            raise NotImplementedError
        return 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SELTZER


@dataclass(eq=False)
class SmileyFace(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro._is_face_card(scored_card):
            self._balatro.mult += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SMILEY


@dataclass(eq=False)
class GoldenTicket(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card == Enhancement.GOLD:
            self._balatro.money += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TICKET


@dataclass(eq=False)
class SockAndBuskin(Joker):
    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return int(self._balatro._is_face_card(scored_card))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SOCK_AND_BUSKIN


@dataclass(eq=False)
class HangingChad(Joker):
    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return 2 if (scored_card is played_cards[scored_card_indices[0]]) else 0

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HANGING_CHAD


@dataclass(eq=False)
class RoughGem(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.DIAMONDS in self._balatro._get_card_suits(scored_card):
            self._balatro.money += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ROUGH_GEM


@dataclass(eq=False)
class Bloodstone(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            Suit.HEARTS in self._balatro._get_card_suits(scored_card)
        ) and self._balatro._chance(1, 2):
            self._balatro.mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLOODSTONE


@dataclass(eq=False)
class Arrowhead(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.SPADES in self._balatro._get_card_suits(scored_card):
            self._balatro.chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ARROWHEAD


@dataclass(eq=False)
class OnyxAgate(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.CLUBS in self._balatro._get_card_suits(scored_card):
            self._balatro.mult += 7

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ONYX_AGATE


@dataclass(eq=False)
class TheIdol(Joker):
    card: Card = field(init=False)

    def __post_init__(self) -> None:
        self._set_random_card()

    def _set_random_card(self) -> None:
        valid_deck_cards = [
            deck_card
            for deck_card in self._balatro.deck_cards
            if not deck_card.is_stone_card
        ]
        if valid_deck_cards:
            random_deck_card = r.choice(valid_deck_cards)
            self.card = Card(random_deck_card.suit, random_deck_card.rank)
        else:
            self.card = Card(Suit.SPADES, Rank.ACE)

    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            scored_card == self.card.rank
            and self.card.suit in self._balatro._get_card_suits(scored_card)
        ):
            self._balatro.mult *= 2

    def _round_ended_action(self) -> None:
        self._set_random_card()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.IDOL


@dataclass(eq=False)
class Triboulet(Joker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [Rank.KING, Rank.QUEEN]:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIBOULET


# ---- /on-scored ---- #

# ---- on-held/ ---- #


@dataclass(eq=False)
class Mime(Joker):
    def _card_held_retriggers(self, held_card: Card) -> int:
        return 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIME


@dataclass(eq=False)
class RaisedFist(Joker):
    def _card_held_ability(self, held_card: Card) -> None:
        valid_hand_cards = [
            hand_card for hand_card in self._balatro.hand if not hand_card.is_stone_card
        ]
        if valid_hand_cards and held_card is min(reversed(valid_hand_cards)):
            self._balatro.mult += held_card.base_chips * 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RAISED_FIST


@dataclass(eq=False)
class Baron(Joker):
    def _card_held_ability(self, held_card: Card) -> None:
        if held_card == Rank.KING:
            self._balatro.mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BARON


@dataclass(eq=False)
class ReservedParking(Joker):
    def _card_held_ability(self, held_card: Card) -> None:
        if self._balatro._is_face_card(held_card) and self._balatro._chance(1, 2):
            self._balatro.money += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RESERVED_PARKING


@dataclass(eq=False)
class ShootTheMoon(Joker):
    def _card_held_ability(self, held_card: Card) -> None:
        if held_card == Rank.QUEEN:
            self._balatro.mult += 13

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SHOOT_THE_MOON


# ---- /on-held ---- #

# ---- independent/ ---- #


@dataclass(eq=False)
class Jimbo(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOKER


@dataclass(eq=False)
class JollyJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._balatro.mult += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOLLY


@dataclass(eq=False)
class ZanyJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._balatro.mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ZANY


@dataclass(eq=False)
class MadJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self._balatro.mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MAD


@dataclass(eq=False)
class CrazyJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._balatro.mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAZY


@dataclass(eq=False)
class DrollJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._balatro.mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DROLL


@dataclass(eq=False)
class SlyJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._balatro.chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SLY


@dataclass(eq=False)
class WilyJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._balatro.chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WILY


@dataclass(eq=False)
class CleverJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self._balatro.chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CLEVER


@dataclass(eq=False)
class DeviousJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._balatro.chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DEVIOUS


@dataclass(eq=False)
class CraftyJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._balatro.chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAFTY


@dataclass(eq=False)
class HalfJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if len(played_cards) <= 3:
            self._balatro.mult += 20

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HALF


@dataclass(eq=False)
class JokerStencil(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= (
            self._balatro.effective_joker_slots - len(self._balatro.jokers)
        ) + self._balatro.jokers.count(JokerType.STENCIL)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STENCIL


@dataclass(eq=False)
class CeremonialDagger(Joker):
    mult: int = field(default=0, init=False)

    def _blind_selected_action(self) -> None:
        for i, joker in self._balatro.jokers:
            if joker is self:
                break
        if i < len(self._balatro.jokers) - 1:
            right_joker = self._balatro.jokers[i + 1]
            self.mult += self._balatro._calculate_sell_value(right_joker)
            self._balatro._destroy_joker(right_joker)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CEREMONIAL


@dataclass(eq=False)
class Banner(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += 30 * self._balatro.discards

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BANNER


@dataclass(eq=False)
class MysticSummit(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro.discards == 0:
            self._balatro.mult += 15

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MYSTIC_SUMMIT


@dataclass(eq=False)
class LoyaltyCard(Joker):
    hands_remaining: int = field(default=5, init=False)

    def _end_hand_action(self) -> None:
        if self.hands_remaining == 0:
            self.hands_remaining = 5
        else:
            self.hands_remaining -= 1

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.hands_remaining == 0:
            self._balatro.mult *= 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LOYALTY_CARD


@dataclass(eq=False)
class Misprint(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += r.randint(0, 23)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MISPRINT


@dataclass(eq=False)
class SteelJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= 1 + (
            0.2
            * sum(
                deck_card.enhancement is Enhancement.STEEL
                for deck_card in self._balatro.deck_cards
            )
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STEEL_JOKER


@dataclass(eq=False)
class AbstractJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += 3 * len(self._balatro.jokers)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ABSTRACT


@dataclass(eq=False)
class GrosMichel(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += 15

    def _round_ended_action(self) -> None:
        if self._balatro._chance(1, 6):
            raise NotImplementedError

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GROS_MICHEL


@dataclass(eq=False)
class Supernova(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self._balatro.poker_hand_info[poker_hands_played[0]][1]

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SUPERNOVA


@dataclass(eq=False)
class Blackboard(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for held_card in self._balatro.hand:
            held_card_suits = self._balatro._get_card_suits(
                held_card, include_base=True
            )
            if Suit.SPADES not in held_card_suits and Suit.CLUBS not in held_card_suits:
                break
        else:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLACKBOARD


@dataclass(eq=False)
class IceCream(Joker):
    chips: int = field(default=100, init=False)

    def _end_hand_action(self) -> None:
        self.chips -= 5
        if self.chips == 0:
            raise NotImplementedError

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ICE_CREAM


@dataclass(eq=False)
class BlueJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += 2 * len(self._balatro.deck_cards_left)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLUE_JOKER


@dataclass(eq=False)
class Constellation(Joker):
    xmult: float = field(default=1.0, init=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    def _planet_used_action(self) -> None:
        self.xmult += 0.1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CONSTELLATION


@dataclass(eq=False)
class Superposition(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            PokerHand.STRAIGHT in poker_hands_played
            and any(played_cards[i] == Rank.ACE for i in scored_card_indices)
            and self._balatro.effective_consumable_slots
            > len(self._balatro.consumables)
        ):
            self._balatro.consumables.append(self._balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SUPERPOSITION


@dataclass(eq=False)
class Cavendish(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= 3

    def _round_ended_action(self) -> None:
        if self._balatro._chance(1, 1000):
            raise NotImplementedError

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CAVENDISH


@dataclass(eq=False)
class CardSharp(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[0] in self._balatro.round_poker_hands:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CARD_SHARP


@dataclass(eq=False)
class RedCard(Joker):
    mult: int = field(default=0, init=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self.mult

    def _pack_skipped_action(self) -> None:
        self.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RED_CARD


@dataclass(eq=False)
class Madness(Joker):
    xmult: float = field(default=1.0, init=False)

    def _blind_selected_action(self) -> None:
        if self._balatro.blind in [Blind.SMALL, Blind.BIG]:
            self.xmult += 0.5
            valid_destroys = [
                joker
                for joker in self._balatro.jokers
                if joker is not self and not joker.eternal
            ]
            if valid_destroys:
                self._balatro._destroy_joker(r.choice(valid_destroys))

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MADNESS


@dataclass(eq=False)
class Seance(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[
            0
        ] is PokerHand.STRAIGHT_FLUSH and self._balatro.effective_consumable_slots > len(
            self._balatro.consumables
        ):
            self._balatro.consumables.append(self._balatro._get_random_spectral())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SEANCE


@dataclass(eq=False)
class Hologram(Joker):
    xmult: float = field(default=1.0, init=False)

    def _card_added_action(self, added_card: Card) -> None:
        self.xmult += 0.25

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HOLOGRAM


@dataclass(eq=False)
class Vagabond(Joker):
    will_create: bool = field(default=False, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self.will_create = self._balatro.money <= 4

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.will_create and self._balatro.effective_consumable_slots > len(
            self._balatro.consumables
        ):
            self._balatro.consumables.append(self._balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.VAGABOND


@dataclass(eq=False)
class Erosion(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += 4 * max(
            0,
            self._balatro.deck.starting_size - len(self._balatro.deck_cards),
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EROSION


@dataclass(eq=False)
class FortuneTeller(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self._balatro.tarot_cards_used

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FORTUNE_TELLER


@dataclass(eq=False)
class StoneJoker(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += 25 * sum(
            deck_card.is_stone_card for deck_card in self._balatro.deck_cards
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STONE


@dataclass(eq=False)
class Bull(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += 2 * max(0, self._balatro.money)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BULL


@dataclass(eq=False)
class FlashCard(Joker):
    mult: int = field(default=0, init=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self.mult

    def _shop_rerolled_action(self) -> None:
        self.mult += 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FLASH


@dataclass(eq=False)
class Popcorn(Joker):
    mult: int = field(default=20, init=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self.mult

    def _round_ended_action(self) -> None:
        self.mult -= 4
        if self.mult == 0:
            raise NotImplementedError

    @property
    def joker_type(self) -> JokerType:
        return JokerType.POPCORN


@dataclass(eq=False)
class Campfire(Joker):
    xmult: float = field(default=1.0, init=False)

    def _boss_defeated_action(self) -> None:
        self.xmult = 1.0

    def _item_sold_action(self) -> None:
        self.xmult += 0.25

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CAMPFIRE


@dataclass(eq=False)
class Acrobat(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro.hands == 0:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ACROBAT


@dataclass(eq=False)
class Swashbuckler(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += sum(
            self._balatro._calculate_sell_value(joker)
            for joker in self._balatro.jokers
            if joker is not self
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SWASHBUCKLER


@dataclass(eq=False)
class Throwback(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= 1 + (0.25 * self._balatro.blinds_skipped)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THROWBACK


@dataclass(eq=False)
class GlassJoker(Joker):
    xmult: float = field(default=1.0, init=False)

    def _glass_card_destroyed_action(self) -> None:
        self.xmult += 0.75

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GLASS


@dataclass(eq=False)
class FlowerPot(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        scored_suits = set()
        possible_suits = [
            self._balatro._get_card_suits(played_cards[i], include_base=True)
            for i in scored_card_indices
        ]
        possible_suits.sort(key=lambda suits: len(suits))
        for suits in possible_suits:
            for suit in suits:
                if suit not in scored_suits:
                    scored_suits.add(suit)
                    break
        if len(scored_suits) == 4:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FLOWER_POT


@dataclass(eq=False)
class SeeingDouble(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        club, other = False, False
        possible_suits = [
            self._balatro._get_card_suits(played_cards[i], include_base=True)
            for i in scored_card_indices
        ]
        possible_suits.sort(key=lambda suits: len(suits))
        for suits in possible_suits:
            if not club and Suit.CLUBS in suits:
                club = True
            elif not other and any(
                suit in possible_suits for suit in Suit if suit is not Suit.CLUBS
            ):
                other = True
        if club and other:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SEEING_DOUBLE


@dataclass(eq=False)
class Matador(Joker):
    will_earn: bool = field(default=False, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        raise NotImplementedError

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.will_earn:
            self._balatro.money += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MATADOR


@dataclass(eq=False)
class TheDuo(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DUO


@dataclass(eq=False)
class TheTrio(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIO


@dataclass(eq=False)
class TheFamily(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FOUR_OF_A_KIND in poker_hands_played:
            self._balatro.mult *= 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FAMILY


@dataclass(eq=False)
class TheOrder(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ORDER


@dataclass(eq=False)
class TheTribe(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIBE


@dataclass(eq=False)
class Stuntman(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += 250

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STUNTMAN


@dataclass(eq=False)
class DriversLicense(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            sum(
                deck_card.enhancement is not None
                for deck_card in self._balatro.deck_cards
            )
            >= 16
        ):
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DRIVERS_LICENSE


@dataclass(eq=False)
class Bootstraps(Joker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += 2 * max(0, self._balatro.money // 5)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BOOTSTRAPS


@dataclass(eq=False)
class Canio(Joker):
    xmult: float = field(default=1.0, init=False)

    def _card_destroyed_action(self, destroyed_card: Card):
        if self._balatro._is_face_card(destroyed_card):
            self.xmult += 1.0

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CANIO


# ---- /independent ---- #

# ---- mixed/ ---- #


@dataclass(eq=False)
class RideTheBus(Joker):
    mult: int = field(default=0, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for i in scored_card_indices:
            if self._balatro._is_face_card(played_cards[i]):
                self.mult = 0
                break
        else:
            self.mult += 1

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RIDE_THE_BUS


@dataclass(eq=False)
class Runner(Joker):
    chips: int = field(default=0, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self.chips += 15

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RUNNER


@dataclass(eq=False)
class GreenJoker(Joker):
    mult: int = field(default=0, init=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.mult = max(0, self.mult - 1)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self.mult += 1

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GREEN_JOKER


@dataclass(eq=False)
class SquareJoker(Joker):
    chips: int = field(default=0, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if len(played_cards) == 4:
            self.chips += 4

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SQUARE


@dataclass(eq=False)
class Vampire(Joker):
    xmult: float = field(default=1.0, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for i in scored_card_indices:
            scored_card = played_cards[i]
            if scored_card.enhancement in Enhancement:
                self.xmult += 0.1
                scored_card.enhancement = None

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.VAMPIRE


@dataclass(eq=False)
class Obelisk(Joker):
    xmult: float = field(default=1.0, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._balatro.poker_hand_info[poker_hands_played[0]][1] < max(
            times_played for hand_level, times_played in self._balatro.poker_hand_info
        ):
            self.xmult += 0.2
        else:
            self.xmult = 1.0

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.OBELISK


@dataclass(eq=False)
class LuckyCat(Joker):
    xmult: float = field(default=1.0, init=False)

    def _lucky_card_triggered_action(self) -> None:
        self.xmult += 0.25

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUCKY_CAT


@dataclass(eq=False)
class SpareTrousers(Joker):
    mult: int = field(default=0, init=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self.mult += 2

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TROUSERS


@dataclass(eq=False)
class Ramen(Joker):
    xmult: float = field(default=2.0, init=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.xmult -= 0.01 * len(discarded_cards)
        if self.xmult <= 1.0:
            raise NotImplementedError

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RAMEN


@dataclass(eq=False)
class Castle(Joker):
    chips: int = field(default=0, init=False)
    suit: Suit = field(init=False)

    def __post_init__(self) -> None:
        self._set_random_suit()

    def _set_random_suit(self) -> None:
        valid_suits = [
            deck_card.suit
            for deck_card in self._balatro.deck_cards
            if not deck_card.is_stone_card
        ]
        self.suit = r.choice(valid_suits) if valid_suits else Suit.SPADES

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        for discarded_card in discarded_cards:
            if self.suit in self._balatro._get_card_suits(discarded_card):
                self.chips += 3

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += self.chips

    def _round_ended_action(self) -> None:
        self._set_random_suit()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CASTLE


@dataclass(eq=False)
class WeeJoker(Joker):
    chips: int = field(default=0, init=False)

    def _card_scored_action(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card == Rank.TWO:
            self.chips += 8

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WEE


@dataclass(eq=False)
class HitTheRoad(Joker):
    xmult: float = field(default=1.0, init=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        for discarded_card in discarded_cards:
            if discarded_card == Rank.JACK:
                self.xmult += 0.5

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    def _round_ended_action(self) -> None:
        self.xmult = 1.0

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HIT_THE_ROAD


@dataclass(eq=False)
class Yorick(Joker):
    xmult: float = field(default=1.0, init=False)
    discards_remaining: int = field(default=23, init=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.discards_remaining -= len(discarded_cards)
        while self.discards_remaining <= 0:
            self.xmult += 1.0
            self.discards_remaining += 23

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.YORICK


# ---- /mixed ---- #

# ---- on-other-jokers/ ---- #


@dataclass(eq=False)
class BaseballCard(Joker):
    def _dependent_ability(self, other_joker: Joker) -> None:
        from balatro_constants import JOKER_TYPE_RARITIES

        if other_joker in JOKER_TYPE_RARITIES[Rarity.UNCOMMON]:
            self._balatro.mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BASEBALL


# ---- /on-other-jokers ---- #

# ---- on-discard/ ---- #


@dataclass(eq=False)
class FacelessJoker(Joker):
    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if (
            sum(
                self._balatro._is_face_card(discarded_card)
                for discarded_card in discarded_cards
            )
            >= 3
        ):
            self._balatro.money += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FACELESS


@dataclass(eq=False)
class MailInRebate(Joker):
    rank: Rank = field(init=False)

    def __post_init__(self) -> None:
        self._set_random_rank()

    def _set_random_rank(self) -> None:
        valid_ranks = [
            deck_card.rank
            for deck_card in self._balatro.deck_cards
            if not deck_card.is_stone_card
        ]
        self.rank = r.choice(valid_ranks) if valid_ranks else Rank.ACE

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        for discarded_card in discarded_cards:
            if discarded_card == self.rank:
                self._balatro.money += 5

    def _round_ended_action(self) -> None:
        self._set_random_rank()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MAIL


@dataclass(eq=False)
class TradingCard(Joker):
    def _discard_action(self, discarded_cards: list[Card]) -> None:
        if self._balatro.first_discard and len(discarded_cards) == 1:
            self._balatro.money += 3
            self._balatro._destroy_card(self._balatro.hand[discarded_cards[0]])

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRADING


@dataclass(eq=False)
class BurntJoker(Joker):
    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if self._balatro.first_discard:
            self._balatro.poker_hand_info[
                max(self._balatro._get_poker_hands(discarded_cards))
            ][1] += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BURNT


# ---- /on-discard ---- #

# ---- other/ ---- #


@dataclass(eq=False)
class FourFingers(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.FOUR_FINGERS


@dataclass(eq=False)
class CreditCard(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.CREDIT_CARD


@dataclass(eq=False)
class MarbleJoker(Joker):
    def _blind_selected_ability(self) -> None:
        added_card = self._balatro._get_random_card()
        added_card.enhancement = Enhancement.STONE
        self._balatro._add_card(added_card)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MARBLE


@dataclass(eq=False)
class ChaosTheClown(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.CHAOS


@dataclass(eq=False)
class DelayedGratification(Joker):
    def _round_ended_ability(self) -> None:
        if self._balatro.first_discard:
            self._balatro.money += 2 * self._balatro.discards

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DELAYED_GRAT


@dataclass(eq=False)
class Pareidolia(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.PAREIDOLIA


@dataclass(eq=False)
class Egg(Joker):
    def _round_ended_ability(self) -> None:
        self.extra_sell_value += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EGG


@dataclass(eq=False)
class Burglar(Joker):
    def _blind_selected_ability(self) -> None:
        self._balatro.hands += 3
        self._balatro.discards = 0

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BURGLAR


@dataclass(eq=False)
class Splash(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SPLASH


@dataclass(eq=False)
class SixthSense(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SIXTH_SENSE


@dataclass(eq=False)
class RiffRaff(Joker):
    def _blind_selected_ability(self) -> None:
        for _ in range(
            min(2, self._balatro.effective_joker_slots - len(self._balatro.jokers))
        ):
            self._balatro._add_joker(self._balatro._get_random_joker(Rarity.COMMON))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RIFF_RAFF


@dataclass(eq=False)
class Shortcut(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SHORTCUT


@dataclass(eq=False)
class CloudNine(Joker):
    def _round_ended_ability(self) -> None:
        self._balatro.money += self._balatro.deck_cards.count(Rank.NINE)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CLOUD_9


@dataclass(eq=False)
class Rocket(Joker):
    payout: int = field(default=1, init=False)

    def _boss_defeated_action(self) -> None:
        self.payout += 2

    def _round_ended_ability(self) -> None:
        self._balatro.money += self.payout

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ROCKET


@dataclass(eq=False)
class Luchador(Joker):
    def _sold_ability(self) -> None:
        raise NotImplementedError

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUCHADOR


@dataclass(eq=False)
class GiftCard(Joker):
    def _round_ended_ability(self) -> None:
        for joker in self._balatro.jokers:
            joker.extra_sell_value += 1
        for consumable in self._balatro.consumables:
            consumable.extra_sell_value += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GIFT


@dataclass(eq=False)
class TurtleBean(Joker):
    hand_size_increase: int = field(default=5, init=False)

    def _round_ended_action(self) -> None:
        self.hand_size_increase -= 1
        if self.hand_size_increase == 0:
            raise NotImplementedError

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TURTLE_BEAN


@dataclass(eq=False)
class ToTheMoon(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.TO_THE_MOON


@dataclass(eq=False)
class Hallucination(Joker):
    def _pack_opened_ability(self) -> None:
        if self._balatro.effective_consumable_slots > len(
            self._balatro.consumables
        ) and self._balatro._chance(1, 2):
            self._balatro.consumables.append(self._balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HALLUCINATION


@dataclass(eq=False)
class Juggler(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.JUGGLER


@dataclass(eq=False)
class Drunkard(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.DRUNKARD


@dataclass(eq=False)
class GoldenJoker(Joker):
    def _round_ended_ability(self) -> None:
        self._balatro.money += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GOLDEN


@dataclass(eq=False)
class DietCola(Joker):
    def _sold_ability(self) -> None:
        self._balatro.tags.append(Tag.DOUBLE)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DIET_COLA


@dataclass(eq=False)
class MrBones(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.MR_BONES


@dataclass(eq=False)
class Troubadour(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.TROUBADOUR


@dataclass(eq=False)
class Certificate(Joker):
    def _blind_selected_ability(self) -> None:
        added_card = self._balatro._get_random_card()
        added_card.seal = r.choice(list(Seal))
        self._balatro._add_card(added_card)
        self._balatro.hand.append(added_card)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CERTIFICATE


@dataclass(eq=False)
class SmearedJoker(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SMEARED


@dataclass(eq=False)
class Showman(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.RING_MASTER


@dataclass(eq=False)
class MerryAndy(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.MERRY_ANDY


@dataclass(eq=False)
class OopsAllSixes(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.OOPS


@dataclass(eq=False)
class InvisibleJoker(Joker):
    rounds_remaining: int = field(default=2, init=False)

    def _round_ended_action(self) -> None:
        if self.rounds_remaining > 0:
            self.rounds_remaining -= 1

    def _sold_action(self) -> None:
        if (
            self.rounds_remaining == 0
            and self._balatro.effective_joker_slots - len(self._balatro.jokers) > 1
        ):
            duplicated_joker = replace(
                r.choice([joker for joker in self._balatro.jokers if joker is not self])
            )
            if duplicated_joker.edition is Edition.NEGATIVE:
                duplicated_joker.edition = Edition.BASE
                if duplicated_joker.joker_type is JokerType.INVISIBLE:
                    duplicated_joker.rounds_remaining = 2
            self._balatro._add_joker(duplicated_joker)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.INVISIBLE


@dataclass(eq=False)
class Satellite(Joker):
    def _round_ended_ability(self) -> None:
        self._balatro.money += len(self._balatro.planet_cards_used)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SATELLITE


@dataclass(eq=False)
class Cartomancer(Joker):
    def _blind_selected_ability(self) -> None:
        if self._balatro.effective_consumable_slots > len(self._balatro.consumables):
            self._balatro.consumables.append(self._balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CARTOMANCER


@dataclass(eq=False)
class Astronomer(Joker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.ASTRONOMER


@dataclass(eq=False)
class Chicot(Joker):
    # TODO

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CHICOT


@dataclass(eq=False)
class Perkeo(Joker):
    def _shop_exited_ability(self) -> None:
        self._balatro.consumables.append(
            replace(r.choice(self._balatro.consumables), is_negative=True)
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.PERKEO


# ---- /other ---- #
