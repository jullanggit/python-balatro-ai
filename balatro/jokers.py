from dataclasses import dataclass, field, replace
import random as r

from .classes import *
from .enums import *


# ---- copiers/ ---- #


@dataclass(eq=False)
class Blueprint(CopyJoker):
    def _on_jokers_moved(self) -> None:
        i = self._run._jokers.index(self)
        self.copied_joker = (
            self._run._jokers[i + 1] if i < len(self._run._jokers) - 1 else None
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLUEPRINT


@dataclass(eq=False)
class Brainstorm(CopyJoker):
    def _on_jokers_moved(self) -> None:
        self.copied_joker = self._run._jokers[0]

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BRAINSTORM


# ---- /copiers ---- #

# ---- on-played/ ---- #


@dataclass(eq=False)
class SpaceJoker(BaseJoker):
    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._chance(1, 4):
            self._run._poker_hand_info[poker_hands_played[0]][0] += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SPACE


@dataclass(eq=False)
class DNA(BaseJoker):
    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._first_hand and len(played_cards) == 1:
            card_copy = replace(played_cards[0])
            self._run._add_card(card_copy)
            self._run._hand.append(card_copy)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DNA


@dataclass(eq=False)
class ToDoList(BaseJoker):
    poker_hand: PokerHand = field(
        default_factory=lambda: r.choice(list(PokerHand)[3:]), init=False, repr=False
    )

    def _hand_played_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[0] is self.poker_hand:
            self._run._money += 4

    def _on_created_action(self) -> None:
        self._set_random_poker_hand()

    def _round_ended_action(self) -> None:
        self._set_random_poker_hand()

    def _set_random_poker_hand(self) -> None:
        self.poker_hand = r.choice(self._run._unlocked_poker_hands)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TODO_LIST


@dataclass(eq=False)
class MidasMask(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIDAS_MASK


# ---- /on-played ---- #

# ---- on-scored/ ---- #


@dataclass(eq=False)
class GreedyJoker(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.DIAMONDS in self._run._get_card_suits(scored_card):
            self._run._mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GREEDY_JOKER


@dataclass(eq=False)
class LustyJoker(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.HEARTS in self._run._get_card_suits(scored_card):
            self._run._mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUSTY_JOKER


@dataclass(eq=False)
class WrathfulJoker(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.SPADES in self._run._get_card_suits(scored_card):
            self._run._mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WRATHFUL_JOKER


@dataclass(eq=False)
class GluttonousJoker(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.CLUBS in self._run._get_card_suits(scored_card):
            self._run._mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GLUTTONOUS_JOKER


@dataclass(eq=False)
class EightBall(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            scored_card == Rank.EIGHT
            and self._run.consumable_slots > len(self._run._consumables)
            and self._run._chance(1, 4)
        ):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EIGHT_BALL


@dataclass(eq=False)
class Dusk(BaseJoker):
    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return int(self._run._hands == 0)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DUSK


@dataclass(eq=False)
class Fibonacci(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FIBONACCI


@dataclass(eq=False)
class ScaryFace(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._is_face_card(scored_card):
            self._run._chips += 30

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCARY_FACE


@dataclass(eq=False)
class Hack(BaseJoker):
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
class EvenSteven(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EVEN_STEVEN


@dataclass(eq=False)
class OddTodd(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ODD_TODD


@dataclass(eq=False)
class Scholar(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCHOLAR


@dataclass(eq=False)
class BusinessCard(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._is_face_card(scored_card) and self._run._chance(1, 2):
            self._run._money += 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BUSINESS_CARD


@dataclass(eq=False)
class Hiker(BaseJoker):
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
class Photograph(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.PHOTOGRAPH


@dataclass(eq=False)
class AncientJoker(BaseJoker):
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

    def _on_created_action(self) -> None:
        self._set_random_suit()

    def _round_ended_action(self) -> None:
        self._set_random_suit()

    def _set_random_suit(self) -> None:
        new_suit = None
        while new_suit is None or new_suit is self.suit:
            new_suit = r.choice(list(Suit))
        self.suit = new_suit

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ANCIENT_JOKER


@dataclass(eq=False)
class WalkieTalkie(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WALKIE_TALKIE


@dataclass(eq=False)
class Seltzer(BaseJoker):
    hands_left: int = field(default=10, init=False, repr=False)

    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        self.hands_left -= 1
        return 1

    def _end_hand_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.hands_left == 0:
            self._run._destroy_joker(self)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SELTZER


@dataclass(eq=False)
class SmileyFace(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._is_face_card(scored_card):
            self._run._mult += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SMILEY_FACE


@dataclass(eq=False)
class GoldenTicket(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card == Enhancement.GOLD:
            self._run._money += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GOLDEN_TICKET


@dataclass(eq=False)
class SockAndBuskin(BaseJoker):
    def _card_scored_retriggers(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> int:
        return int(self._run._is_face_card(scored_card))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SOCK_AND_BUSKIN


@dataclass(eq=False)
class HangingChad(BaseJoker):
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
class RoughGem(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.DIAMONDS in self._run._get_card_suits(scored_card):
            self._run._money += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ROUGH_GEM


@dataclass(eq=False)
class Bloodstone(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLOODSTONE


@dataclass(eq=False)
class Arrowhead(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.SPADES in self._run._get_card_suits(scored_card):
            self._run._chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ARROWHEAD


@dataclass(eq=False)
class OnyxAgate(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if Suit.CLUBS in self._run._get_card_suits(scored_card):
            self._run._mult += 7

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ONYX_AGATE


@dataclass(eq=False)
class TheIdol(BaseJoker):
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

    def _on_created_action(self) -> None:
        self._set_random_card()

    def _round_ended_action(self) -> None:
        self._set_random_card()

    def _set_random_card(self) -> None:
        valid_deck_cards = [
            deck_card
            for deck_card in self._run._full_deck
            if not deck_card.is_stone_card
        ]
        if valid_deck_cards:
            random_deck_card = r.choice(valid_deck_cards)
            self.card = Card(random_deck_card.rank, random_deck_card.suit)
        else:
            self.card = Card(Rank.ACE, Suit.SPADES)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THE_IDOL


@dataclass(eq=False)
class Triboulet(BaseJoker):
    def _card_scored_ability(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if scored_card in [Rank.KING, Rank.QUEEN]:
            self._run._mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIBOULET


# ---- /on-scored ---- #

# ---- on-held/ ---- #


@dataclass(eq=False)
class Mime(BaseJoker):
    def _card_held_retriggers(self, held_card: Card) -> int:
        return 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIME


@dataclass(eq=False)
class RaisedFist(BaseJoker):
    def _card_held_ability(self, held_card: Card) -> None:
        valid_hand_cards = [
            hand_card for hand_card in self._run._hand if not hand_card.is_stone_card
        ]
        if valid_hand_cards and held_card is min(reversed(valid_hand_cards)):
            self._run._mult += held_card.chips * 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RAISED_FIST


@dataclass(eq=False)
class Baron(BaseJoker):
    def _card_held_ability(self, held_card: Card) -> None:
        if held_card == Rank.KING:
            self._run._mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BARON


@dataclass(eq=False)
class ReservedParking(BaseJoker):
    def _card_held_ability(self, held_card: Card) -> None:
        if self._run._is_face_card(held_card) and self._run._chance(1, 2):
            self._run._money += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RESERVED_PARKING


@dataclass(eq=False)
class ShootTheMoon(BaseJoker):
    def _card_held_ability(self, held_card: Card) -> None:
        if held_card == Rank.QUEEN:
            self._run._mult += 13

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SHOOT_THE_MOON


# ---- /on-held ---- #

# ---- independent/ ---- #


@dataclass(eq=False)
class Joker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOKER


@dataclass(eq=False)
class JollyJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._run._mult += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOLLY_JOKER


@dataclass(eq=False)
class ZanyJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._run._mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ZANY_JOKER


@dataclass(eq=False)
class MadJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self._run._mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MAD_JOKER


@dataclass(eq=False)
class CrazyJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._run._mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAZY_JOKER


@dataclass(eq=False)
class DrollJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._run._mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DROLL_JOKER


@dataclass(eq=False)
class SlyJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._run._chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SLY_JOKER


@dataclass(eq=False)
class WilyJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._run._chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WILY_JOKER


@dataclass(eq=False)
class CleverJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.TWO_PAIR in poker_hands_played:
            self._run._chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CLEVER_JOKER


@dataclass(eq=False)
class DeviousJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._run._chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DEVIOUS_JOKER


@dataclass(eq=False)
class CraftyJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._run._chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAFTY_JOKER


@dataclass(eq=False)
class HalfJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if len(played_cards) <= 3:
            self._run._mult += 20

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HALF_JOKER


@dataclass(eq=False)
class JokerStencil(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= (
            self._run.joker_slots - len(self._run._jokers)
        ) + self._run._jokers.count(JokerType.JOKER_STENCIL)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOKER_STENCIL


@dataclass(eq=False)
class CeremonialDagger(BaseJoker):
    mult: int = field(default=0, init=False, repr=False)

    def _blind_selected_action(self) -> None:
        i = self._run._jokers.index(self)
        if i < len(self._run._jokers) - 1:
            right_joker = self._run._jokers[i + 1]
            if not right_joker.eternal:
                self.mult += self._run._calculate_sell_value(right_joker)
                self._run._destroy_joker(right_joker)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CEREMONIAL_DAGGER


@dataclass(eq=False)
class Banner(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 30 * self._run._discards

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BANNER


@dataclass(eq=False)
class MysticSummit(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._discards == 0:
            self._run._mult += 15

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MYSTIC_SUMMIT


@dataclass(eq=False)
class LoyaltyCard(BaseJoker):
    hands_remaining: int = field(default=5, init=False, repr=False)

    def _end_hand_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
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
            self._run._mult *= 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LOYALTY_CARD


@dataclass(eq=False)
class Misprint(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += r.randint(0, 23)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MISPRINT


@dataclass(eq=False)
class SteelJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= 1 + (
            0.2
            * sum(
                deck_card.enhancement is Enhancement.STEEL
                for deck_card in self._run._full_deck
            )
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STEEL_JOKER


@dataclass(eq=False)
class AbstractJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 3 * len(self._run._jokers)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ABSTRACT_JOKER


@dataclass(eq=False)
class GrosMichel(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GROS_MICHEL


@dataclass(eq=False)
class Supernova(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self._run._poker_hand_info[poker_hands_played[0]][1]

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SUPERNOVA


@dataclass(eq=False)
class Blackboard(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLACKBOARD


@dataclass(eq=False)
class IceCream(BaseJoker):
    chips: int = field(default=100, init=False, repr=False)

    def _end_hand_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self.chips -= 5
        if self.chips == 0:
            self._run._destroy_joker(self)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ICE_CREAM


@dataclass(eq=False)
class BlueJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 2 * len(self._run._full_deck_left)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLUE_JOKER


@dataclass(eq=False)
class Constellation(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    def _planet_used_action(self) -> None:
        self.xmult += 0.1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CONSTELLATION


@dataclass(eq=False)
class Superposition(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            PokerHand.STRAIGHT in poker_hands_played
            and any(played_cards[i] == Rank.ACE for i in scored_card_indices)
            and self._run.consumable_slots > len(self._run._consumables)
        ):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SUPERPOSITION


@dataclass(eq=False)
class Cavendish(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CAVENDISH


@dataclass(eq=False)
class CardSharp(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[0] in self._run._round_poker_hands:
            self._run._mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CARD_SHARP


@dataclass(eq=False)
class RedCard(BaseJoker):
    mult: int = field(default=0, init=False, repr=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self.mult

    def _pack_skipped_action(self) -> None:
        self.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RED_CARD


@dataclass(eq=False)
class Madness(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _blind_selected_action(self) -> None:
        if self._run._blind in [Blind.SMALL_BLIND, Blind.BIG_BLIND]:
            self.xmult += 0.5
            valid_destroys = [
                joker
                for joker in self._run._jokers
                if joker is not self and not joker.eternal
            ]
            if valid_destroys:
                self._run._destroy_joker(r.choice(valid_destroys))

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MADNESS


@dataclass(eq=False)
class Seance(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if poker_hands_played[
            0
        ] is PokerHand.STRAIGHT_FLUSH and self._run.consumable_slots > len(
            self._run._consumables
        ):
            self._run._consumables.append(self._run._get_random_consumable(Spectral))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SEANCE


@dataclass(eq=False)
class Hologram(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _card_added_action(self, added_card: Card) -> None:
        self.xmult += 0.25

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HOLOGRAM


@dataclass(eq=False)
class Vagabond(BaseJoker):
    will_create: bool = field(default=False, init=False, repr=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self.will_create = self._run._money <= 4

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self.will_create and self._run.consumable_slots > len(
            self._run._consumables
        ):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.VAGABOND


@dataclass(eq=False)
class Erosion(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 4 * max(
            0,
            self._run._deck.starting_size - len(self._run._full_deck),
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EROSION


@dataclass(eq=False)
class FortuneTeller(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self._run._num_tarot_cards_used

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FORTUNE_TELLER


@dataclass(eq=False)
class StoneJoker(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 25 * sum(
            deck_card.is_stone_card for deck_card in self._run._full_deck
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STONE


@dataclass(eq=False)
class Bull(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 2 * max(0, self._run._money)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BULL


@dataclass(eq=False)
class FlashCard(BaseJoker):
    mult: int = field(default=0, init=False, repr=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self.mult

    def _shop_rerolled_action(self) -> None:
        self.mult += 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FLASH_CARD


@dataclass(eq=False)
class Popcorn(BaseJoker):
    mult: int = field(default=20, init=False, repr=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += self.mult

    def _round_ended_action(self) -> None:
        self.mult -= 4
        if self.mult == 0:
            self._run._destroy_joker(self)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.POPCORN


@dataclass(eq=False)
class Campfire(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _boss_defeated_action(self) -> None:
        self.xmult = 1.0

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    def _item_sold_action(self, sold_item: Sellable) -> None:
        self.xmult += 0.25

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CAMPFIRE


@dataclass(eq=False)
class Acrobat(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._hands == 0:
            self._run._mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ACROBAT


@dataclass(eq=False)
class Swashbuckler(BaseJoker):
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SWASHBUCKLER


@dataclass(eq=False)
class Throwback(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= 1 + (0.25 * self._run._num_blinds_skipped)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THROWBACK


@dataclass(eq=False)
class GlassJoker(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _card_destroyed_action(self, destroyed_card: Card) -> None:
        if destroyed_card == Enhancement.GLASS:
            self.xmult += 0.75

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GLASS_JOKER


@dataclass(eq=False)
class FlowerPot(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        scored_suits = set()
        possible_suits = [
            self._run._get_card_suits(played_cards[i], force_base_suit=True)
            for i in scored_card_indices
        ]
        possible_suits.sort(key=lambda suits: len(suits))
        for suits in possible_suits:
            for suit in suits:
                if suit not in scored_suits:
                    scored_suits.add(suit)
                    break
        if len(scored_suits) == 4:
            self._run._mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FLOWER_POT


@dataclass(eq=False)
class SeeingDouble(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        club, other = False, False
        possible_suits = [
            self._run._get_card_suits(played_cards[i], force_base_suit=True)
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
            self._run._mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SEEING_DOUBLE


@dataclass(eq=False)
class Matador(BaseJoker):
    will_earn: bool = field(default=False, init=False, repr=False)

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
            self._run._money += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MATADOR


@dataclass(eq=False)
class TheDuo(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.PAIR in poker_hands_played:
            self._run._mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THE_DUO


@dataclass(eq=False)
class TheTrio(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.THREE_OF_A_KIND in poker_hands_played:
            self._run._mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THE_TRIO


@dataclass(eq=False)
class TheFamily(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FOUR_OF_A_KIND in poker_hands_played:
            self._run._mult *= 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THE_FAMILY


@dataclass(eq=False)
class TheOrder(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.STRAIGHT in poker_hands_played:
            self._run._mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THE_ORDER


@dataclass(eq=False)
class TheTribe(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if PokerHand.FLUSH in poker_hands_played:
            self._run._mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THE_TRIBE


@dataclass(eq=False)
class Stuntman(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += 250

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STUNTMAN


@dataclass(eq=False)
class DriversLicense(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if (
            sum(deck_card.enhancement is not None for deck_card in self._run._full_deck)
            >= 16
        ):
            self._run._mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DRIVERS_LICENSE


@dataclass(eq=False)
class Bootstraps(BaseJoker):
    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult += 2 * max(0, self._run._money // 5)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BOOTSTRAPS


@dataclass(eq=False)
class Canio(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _card_destroyed_action(self, destroyed_card: Card) -> None:
        if self._run._is_face_card(destroyed_card):
            self.xmult += 1.0

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CANIO


# ---- /independent ---- #

# ---- mixed/ ---- #


@dataclass(eq=False)
class RideTheBus(BaseJoker):
    mult: int = field(default=0, init=False, repr=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        for i in scored_card_indices:
            if self._run._is_face_card(played_cards[i]):
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
        self._run._mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RIDE_THE_BUS


@dataclass(eq=False)
class Runner(BaseJoker):
    chips: int = field(default=0, init=False, repr=False)

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
        self._run._chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RUNNER


@dataclass(eq=False)
class GreenJoker(BaseJoker):
    mult: int = field(default=0, init=False, repr=False)

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
        self._run._mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GREEN_JOKER


@dataclass(eq=False)
class SquareJoker(BaseJoker):
    chips: int = field(default=0, init=False, repr=False)

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
        self._run._chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SQUARE_JOKER


@dataclass(eq=False)
class Vampire(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

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
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.VAMPIRE


@dataclass(eq=False)
class Obelisk(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _hand_played_action(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        if self._run._poker_hand_info[poker_hands_played[0]][1] < max(
            times_played for hand_level, times_played in self._run._poker_hand_info
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
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.OBELISK


@dataclass(eq=False)
class LuckyCat(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    def _lucky_card_triggered_action(self) -> None:
        self.xmult += 0.25

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUCKY_CAT


@dataclass(eq=False)
class SpareTrousers(BaseJoker):
    mult: int = field(default=0, init=False, repr=False)

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
        self._run._mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SPARE_TROUSERS


@dataclass(eq=False)
class Ramen(BaseJoker):
    xmult: float = field(default=2.0, init=False, repr=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        self.xmult -= 0.01 * len(discarded_cards)
        if self.xmult <= 1.0:
            self._run._destroy_joker(self)

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RAMEN


@dataclass(eq=False)
class Castle(BaseJoker):
    chips: int = field(default=0, init=False, repr=False)
    suit: Suit = field(default=Suit.SPADES, init=False, repr=False)

    def _discard_action(self, discarded_cards: list[Card]) -> None:
        for discarded_card in discarded_cards:
            if self.suit in self._run._get_card_suits(discarded_card):
                self.chips += 3

    def _independent_ability(
        self,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._run._chips += self.chips

    def _on_created_action(self) -> None:
        self._set_random_suit()

    def _round_ended_action(self) -> None:
        self._set_random_suit()

    def _set_random_suit(self) -> None:
        valid_suits = [
            deck_card.suit
            for deck_card in self._run._full_deck
            if not deck_card.is_stone_card
        ]
        self.suit = r.choice(valid_suits) if valid_suits else Suit.SPADES

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CASTLE


@dataclass(eq=False)
class WeeJoker(BaseJoker):
    chips: int = field(default=0, init=False, repr=False)

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
        self._run._chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WEE_JOKER


@dataclass(eq=False)
class HitTheRoad(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)

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
        self._run._mult *= self.xmult

    def _round_ended_action(self) -> None:
        self.xmult = 1.0

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HIT_THE_ROAD


@dataclass(eq=False)
class Yorick(BaseJoker):
    xmult: float = field(default=1.0, init=False, repr=False)
    discards_remaining: int = field(default=23, init=False, repr=False)

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
        self._run._mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.YORICK


# ---- /mixed ---- #

# ---- on-other-jokers/ ---- #


@dataclass(eq=False)
class BaseballCard(BaseJoker):
    def _dependent_ability(self, other_joker: BaseJoker) -> None:
        from .constants import JOKER_TYPE_RARITIES

        if other_joker in JOKER_TYPE_RARITIES[Rarity.UNCOMMON]:
            self._run._mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BASEBALL_CARD


# ---- /on-other-jokers ---- #

# ---- on-discard/ ---- #


@dataclass(eq=False)
class FacelessJoker(BaseJoker):
    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if (
            sum(
                self._run._is_face_card(discarded_card)
                for discarded_card in discarded_cards
            )
            >= 3
        ):
            self._run._money += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FACELESS_JOKER


@dataclass(eq=False)
class MailInRebate(BaseJoker):
    rank: Rank = field(default=Rank.ACE, init=False, repr=False)

    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        for discarded_card in discarded_cards:
            if discarded_card == self.rank:
                self._run._money += 5

    def _on_created_action(self) -> None:
        self._set_random_rank()

    def _round_ended_action(self) -> None:
        self._set_random_rank()

    def _set_random_rank(self) -> None:
        valid_ranks = [
            deck_card.rank
            for deck_card in self._run._full_deck
            if not deck_card.is_stone_card
        ]
        self.rank = r.choice(valid_ranks) if valid_ranks else Rank.ACE

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MAIL_IN_REBATE


@dataclass(eq=False)
class TradingCard(BaseJoker):
    def _discard_action(self, discarded_cards: list[Card]) -> None:
        if self._run._first_discard and len(discarded_cards) == 1:
            self._run._money += 3
            self._run._destroy_card(self._run._hand[discarded_cards[0]])

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRADING_CARD


@dataclass(eq=False)
class BurntJoker(BaseJoker):
    def _discard_ability(self, discarded_cards: list[Card]) -> None:
        if self._run._first_discard:
            self._run._poker_hand_info[
                max(self._run._get_poker_hands(discarded_cards))
            ][1] += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BURNT_JOKER


# ---- /on-discard ---- #

# ---- other/ ---- #


@dataclass(eq=False)
class FourFingers(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.FOUR_FINGERS


@dataclass(eq=False)
class CreditCard(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.CREDIT_CARD


@dataclass(eq=False)
class MarbleJoker(BaseJoker):
    def _blind_selected_ability(self) -> None:
        added_card = self._run._get_random_card()
        added_card.enhancement = Enhancement.STONE
        self._run._add_card(added_card)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MARBLE_JOKER


@dataclass(eq=False)
class ChaosTheClown(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.CHAOS_THE_CLOWN


@dataclass(eq=False)
class DelayedGratification(BaseJoker):
    def _round_ended_action(self) -> None:
        if self._run._first_discard:
            self._run._money += 2 * self._run._discards

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DELAYED_GRATIFICATION


@dataclass(eq=False)
class Pareidolia(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.PAREIDOLIA


@dataclass(eq=False)
class Egg(BaseJoker):
    def _round_ended_action(self) -> None:
        self.extra_sell_value += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EGG


@dataclass(eq=False)
class Burglar(BaseJoker):
    def _blind_selected_ability(self) -> None:
        self._run._hands += 3
        self._run._discards = 0

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BURGLAR


@dataclass(eq=False)
class Splash(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SPLASH


@dataclass(eq=False)
class SixthSense(BaseJoker):
    def _end_hand_action(
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

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SIXTH_SENSE


@dataclass(eq=False)
class RiffRaff(BaseJoker):
    def _blind_selected_ability(self) -> None:
        for _ in range(min(2, self._run.joker_slots - len(self._run._jokers))):
            self._run._add_joker(self._run._get_random_joker(Rarity.COMMON))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RIFF_RAFF


@dataclass(eq=False)
class Shortcut(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SHORTCUT


@dataclass(eq=False)
class CloudNine(BaseJoker):
    def _round_ended_action(self) -> None:
        self._run._money += self._run._full_deck.count(Rank.NINE)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CLOUD_NINE


@dataclass(eq=False)
class Rocket(BaseJoker):
    payout: int = field(default=1, init=False, repr=False)

    def _boss_defeated_action(self) -> None:
        self.payout += 2

    def _round_ended_action(self) -> None:
        self._run._money += self.payout

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ROCKET


@dataclass(eq=False)
class Luchador(BaseJoker):
    def _item_sold_ability(self, sold_item: Sellable) -> None:
        if sold_item is self and self._run._blind is self._run._boss_blind:
            self._run._disable_boss_blind()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUCHADOR


@dataclass(eq=False)
class GiftCard(BaseJoker):
    def _round_ended_action(self) -> None:
        for joker in self._run._jokers:
            joker.extra_sell_value += 1
        for consumable in self._run._consumables:
            consumable.extra_sell_value += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GIFT_CARD


@dataclass(eq=False)
class TurtleBean(BaseJoker):
    hand_size_increase: int = field(default=5, init=False, repr=False)

    def _round_ended_action(self) -> None:
        self.hand_size_increase -= 1
        if self.hand_size_increase == 0:
            self._run._destroy_joker(self)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TURTLE_BEAN


@dataclass(eq=False)
class ToTheMoon(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.TO_THE_MOON


@dataclass(eq=False)
class Hallucination(BaseJoker):
    def _pack_opened_ability(self) -> None:
        if self._run.consumable_slots > len(
            self._run._consumables
        ) and self._run._chance(1, 2):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HALLUCINATION


@dataclass(eq=False)
class Juggler(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.JUGGLER


@dataclass(eq=False)
class Drunkard(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.DRUNKARD


@dataclass(eq=False)
class GoldenJoker(BaseJoker):
    def _round_ended_action(self) -> None:
        self._run._money += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GOLDEN_JOKER


@dataclass(eq=False)
class DietCola(BaseJoker):
    def _item_sold_ability(self, sold_item: Sellable) -> None:
        if sold_item is self:
            self._run._tags.append(Tag.DOUBLE)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DIET_COLA


@dataclass(eq=False)
class MrBones(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.MR_BONES


@dataclass(eq=False)
class Troubadour(BaseJoker):
    def _blind_selected_action(self) -> None:
        self._run._hands -= 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TROUBADOUR


@dataclass(eq=False)
class Certificate(BaseJoker):
    def _blind_selected_ability(self) -> None:
        added_card = self._run._get_random_card()
        added_card.seal = r.choice(list(Seal))
        self._run._add_card(added_card)
        self._run._hand.append(added_card)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CERTIFICATE


@dataclass(eq=False)
class SmearedJoker(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SMEARED_JOKER


@dataclass(eq=False)
class Showman(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.SHOWMAN


@dataclass(eq=False)
class MerryAndy(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.MERRY_ANDY


@dataclass(eq=False)
class OopsAllSixes(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.OOPS_ALL_SIXES


@dataclass(eq=False)
class InvisibleJoker(BaseJoker):
    rounds_remaining: int = field(default=2, init=False, repr=False)

    def _round_ended_action(self) -> None:
        if self.rounds_remaining > 0:
            self.rounds_remaining -= 1

    def _item_sold_action(self, sold_item: Sellable) -> None:
        if sold_item is self and self.rounds_remaining == 0 and self._run._jokers:
            duplicated_joker = replace(r.choice(self._run._jokers))
            if duplicated_joker.edition is Edition.NEGATIVE:
                duplicated_joker.edition = Edition.BASE
                if duplicated_joker.joker_type is JokerType.INVISIBLE_JOKER:
                    duplicated_joker.rounds_remaining = 2
            self._run._add_joker(duplicated_joker)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.INVISIBLE_JOKER


@dataclass(eq=False)
class Satellite(BaseJoker):
    def _round_ended_action(self) -> None:
        self._run._money += len(self._run._planet_cards_used)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SATELLITE


@dataclass(eq=False)
class Cartomancer(BaseJoker):
    def _blind_selected_ability(self) -> None:
        if self._run.consumable_slots > len(self._run._consumables):
            self._run._consumables.append(self._run._get_random_consumable(Tarot))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CARTOMANCER


@dataclass(eq=False)
class Astronomer(BaseJoker):
    @property
    def joker_type(self) -> JokerType:
        return JokerType.ASTRONOMER


@dataclass(eq=False)
class Chicot(BaseJoker):
    def _blind_selected_action(self) -> None:
        if self._run._blind is self._run._boss_blind:
            self._run._disable_boss_blind()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CHICOT


@dataclass(eq=False)
class Perkeo(BaseJoker):
    def _shop_exited_ability(self) -> None:
        self._run._consumables.append(
            replace(r.choice(self._run._consumables), is_negative=True)
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.PERKEO


# ---- /other ---- #
