from dataclasses import dataclass, field
import random as r

from balatro_classes import *
from balatro_enums import *


# ---- base classes/ ---- #


@dataclass
class CopierJoker:
    copied: Joker | None = field(default=None, init=False)

    def __eq__(self, other: JokerType) -> bool:
        if isinstance(other, JokerType):
            return self.copied == other
        return NotImplemented

    def _set_copied_joker(self, copied_joker: Joker) -> None:
        from balatro_constants import NON_COPYABLE_JOKERS

        if copied_joker.joker_type not in NON_COPYABLE_JOKERS:
            self.copied = copied_joker

    def on_card_scored(self, scored_card: Card) -> None:
        if self.copied is not None:
            self.copied.on_card_scored(scored_card)

    def on_card_scored_check_retrigger(self, scored_card: Card) -> int:
        if self.copied is not None:
            return self.copied.on_card_scored_check_retrigger(scored_card)

    def on_dependent_ability(self, joker: Joker) -> None:
        if self.copied is not None:
            self.copied.on_dependent_ability(joker)

    def on_hand_played(self) -> None:
        if self.copied is not None:
            self.copied.on_hand_played()

    def on_independent_ability(self) -> None:
        if self.copied is not None:
            self.copied.on_independent_ability()

    @property
    def is_active(self) -> bool:
        return self.copied.is_active


# ---- /base classes ---- #

# ---- copiers/ ---- #


@dataclass(eq=False)
class Blueprint(CopierJoker, Joker):
    def on_right_joker_changed(self) -> None:
        self.copied = None
        for i, joker in self._balatro.jokers:
            if joker is self:
                break
        if i < len(self._balatro.jokers) - 1:
            self._set_copied_joker(self._balatro.jokers[i + 1])

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLUEPRINT


@dataclass(eq=False)
class Brainstorm(CopierJoker, Joker):
    def on_leftmost_joker_changed(self) -> None:
        self.copied = None
        self._set_copied_joker(self._balatro.jokers[0])

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BRAINSTORM


# ---- /copiers ---- #

# ---- on-played/ ---- #


@dataclass(eq=False)
class SpaceJoker(Joker):
    def on_hand_played(self) -> None:
        if self._balatro._chance(1, 4):
            self._balatro.poker_hand_info[self._balatro.poker_hands[0]][0] += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SPACE


@dataclass(eq=False)
class DNA(Joker):
    def on_hand_played(self) -> None:
        if self._balatro.first_hand and len(self._balatro.played_cards) == 1:
            card_copy = self._balatro.played_cards[0].copy()
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

    def on_hand_played(self) -> None:
        if self._balatro.poker_hands[0] is self.poker_hand:
            self._balatro.money += 4

    def on_round_end(self) -> None:
        self._set_random_poker_hand()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TODO_LIST


@dataclass(eq=False)
class MidasMask(Joker):
    def on_hand_played(self) -> None:
        for i in self._balatro.scored_card_indices:
            scored_card = self._balatro.played_cards[i]
            if self._balatro._is_face_card(scored_card):
                scored_card.enhancement = Enhancement.GOLD

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIDAS_MASK


# ---- /on-played ---- #

# ---- on-scored/ ---- #


@dataclass(eq=False)
class GreedyJoker(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Suit.DIAMONDS:
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GREEDY_JOKER


@dataclass(eq=False)
class LustyJoker(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Suit.HEARTS:
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUSTY_JOKER


@dataclass(eq=False)
class WrathfulJoker(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Suit.SPADES:
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WRATHFUL_JOKER


@dataclass(eq=False)
class GluttonousJoker(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Suit.CLUBS:
            self._balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GLUTTENOUS_JOKER


@dataclass(eq=False)
class EightBall(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
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
    def on_card_scored_check_retrigger(self, scored_card: Card) -> int:
        return int(self._balatro.hands == 0)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DUSK


@dataclass(eq=False)
class Fibonacci(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
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
    def on_card_scored(self, scored_card: Card) -> None:
        if self._balatro._is_face_card(scored_card):
            self._balatro.chips += 30

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCARY_FACE


@dataclass(eq=False)
class Hack(Joker):
    def on_card_scored_check_retrigger(self, scored_card: Card) -> int:
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
    def on_card_scored(self, scored_card: Card) -> None:
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
    def on_card_scored(self, scored_card: Card) -> None:
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
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Rank.ACE:
            self._balatro.chips += 20
            self._balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCHOLAR


@dataclass(eq=False)
class BusinessCard(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if self._balatro._is_face_card(scored_card) and self._balatro._chance(1, 2):
            self._balatro.money += 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BUSINESS


@dataclass(eq=False)
class Hiker(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        scored_card.bonus_chips += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HIKER


@dataclass(eq=False)
class Photograph(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        first_scored_face_card = next(
            (
                self._balatro.played_cards[i]
                for i in self._balatro.scored_card_indices
                if self._balatro._is_face_card(self._balatro.played_cards[i])
            ),
            None,
        )
        if scored_card is first_scored_face_card:
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

    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == self.suit:
            self._balatro.mult *= 1.5

    def on_round_end(self) -> None:
        self._set_random_suit()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ANCIENT


@dataclass(eq=False)
class WalkieTalkie(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card in [Rank.TEN, Rank.FOUR]:
            self._balatro.chips += 10
            self._balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WALKIE_TALKIE


@dataclass(eq=False)
class Seltzer(Joker):
    hands_left: int = field(default=10, init=False)

    def on_card_scored_check_retrigger(self, scored_card: Card) -> int:
        self.hands_left -= 1
        if self.hands_left == 0:
            self._balatro._destroy_joker(self)
        return 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SELTZER


@dataclass(eq=False)
class SmileyFace(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if self._balatro._is_face_card(scored_card):
            self._balatro.mult += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SMILEY


@dataclass(eq=False)
class GoldenTicket(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Enhancement.GOLD:
            self._balatro.money += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TICKET


@dataclass(eq=False)
class SockAndBuskin(Joker):
    def on_card_scored_check_retrigger(self, scored_card: Card) -> int:
        return int(self._balatro._is_face_card(scored_card))

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SOCK_AND_BUSKIN


@dataclass(eq=False)
class HangingChad(Joker):
    def on_card_scored_check_retrigger(self, scored_card: Card) -> int:
        return (
            2
            if (
                scored_card
                is self._balatro.played_cards[self._balatro.scored_card_indices[0]]
            )
            else 0
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HANGING_CHAD


@dataclass(eq=False)
class RoughGem(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Suit.DIAMONDS:
            self._balatro.money += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ROUGH_GEM


@dataclass(eq=False)
class Bloodstone(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if (scored_card == Suit.HEARTS) and self._balatro._chance(1, 2):
            self._balatro.mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLOODSTONE


@dataclass(eq=False)
class Arrowhead(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Suit.SPADES:
            self._balatro.chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ARROWHEAD


@dataclass(eq=False)
class OnyxAgate(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Suit.CLUBS:
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

    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == self.card:
            self._balatro.mult *= 2

    def on_round_end(self) -> None:
        self._set_random_card()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.IDOL


@dataclass(eq=False)
class Triboulet(Joker):
    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card in [Rank.KING, Rank.QUEEN]:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIBOULET


# ---- /on-scored ---- #

# ---- on-held/ ---- #


@dataclass(eq=False)
class Mime(Joker):
    def on_card_held(self, held_card: Card) -> None:
        raise NotImplementedError

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIME


@dataclass(eq=False)
class RaisedFist(Joker):
    def on_card_held(self, held_card: Card) -> None:
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
    def on_card_held(self, held_card: Card) -> None:
        if held_card == Rank.KING:
            self._balatro.mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BARON


@dataclass(eq=False)
class ReservedParking(Joker):
    def on_card_held(self, held_card: Card) -> None:
        if self._balatro._is_face_card(held_card) and self._balatro._chance(1, 2):
            self._balatro.money += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RESERVED_PARKING


@dataclass(eq=False)
class ShootTheMoon(Joker):
    def on_card_held(self, held_card: Card) -> None:
        if held_card == Rank.QUEEN:
            self._balatro.mult += 13

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SHOOT_THE_MOON


# ---- /on-held ---- #

# ---- independent/ ---- #


@dataclass(eq=False)
class Jimbo(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOKER


@dataclass(eq=False)
class JollyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.PAIR in self._balatro.poker_hands:
            self._balatro.mult += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOLLY


@dataclass(eq=False)
class ZanyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.THREE_OF_A_KIND in self._balatro.poker_hands:
            self._balatro.mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ZANY


@dataclass(eq=False)
class MadJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.TWO_PAIR in self._balatro.poker_hands:
            self._balatro.mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MAD


@dataclass(eq=False)
class CrazyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.STRAIGHT in self._balatro.poker_hands:
            self._balatro.mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAZY


@dataclass(eq=False)
class DrollJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.FLUSH in self._balatro.poker_hands:
            self._balatro.mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DROLL


@dataclass(eq=False)
class SlyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.PAIR in self._balatro.poker_hands:
            self._balatro.chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SLY


@dataclass(eq=False)
class WilyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.THREE_OF_A_KIND in self._balatro.poker_hands:
            self._balatro.chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WILY


@dataclass(eq=False)
class CleverJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.TWO_PAIR in self._balatro.poker_hands:
            self._balatro.chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CLEVER


@dataclass(eq=False)
class DeviousJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.STRAIGHT in self._balatro.poker_hands:
            self._balatro.chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DEVIOUS


@dataclass(eq=False)
class CraftyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.FLUSH in self._balatro.poker_hands:
            self._balatro.chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAFTY


@dataclass(eq=False)
class HalfJoker(Joker):
    def on_independent_ability(self) -> None:
        if len(self._balatro.played_cards) <= 3:
            self._balatro.mult += 20

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HALF


@dataclass(eq=False)
class JokerStencil(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult *= (
            self._balatro.effective_joker_slots - len(self._balatro.jokers)
        ) + self._balatro.jokers.count(JokerType.STENCIL)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STENCIL


@dataclass(eq=False)
class CeremonialDagger(Joker):
    mult: int = field(default=0, init=False)

    def on_blind_selected(self) -> None:
        for i, joker in self._balatro.jokers:
            if joker is self:
                break
        if i < len(self._balatro.jokers) - 1:
            right_joker = self._balatro.jokers[i + 1]
            self.mult += self._balatro._calculate_sell_value(right_joker)
            self._balatro._destroy_joker(right_joker)

    def on_independent_ability(self) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CEREMONIAL


@dataclass(eq=False)
class Banner(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.chips += 30 * self._balatro.discards

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BANNER


@dataclass(eq=False)
class MysticSummit(Joker):
    def on_independent_ability(self) -> None:
        if self._balatro.discards == 0:
            self._balatro.mult += 15

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MYSTIC_SUMMIT


@dataclass(eq=False)
class LoyaltyCard(Joker):
    hands_remaining: int = field(default=5, init=False)

    def on_end_hand(self) -> None:
        if self.hands_remaining == 0:
            self.hands_remaining = 5
        else:
            self.hands_remaining -= 1

    def on_independent_ability(self) -> None:
        if self.hands_remaining == 0:
            self._balatro.mult *= 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LOYALTY_CARD


@dataclass(eq=False)
class Misprint(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult += r.randint(0, 23)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MISPRINT


@dataclass(eq=False)
class SteelJoker(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult *= 1 + (
            0.2
            * sum(
                deck_card._enhancement is Enhancement.STEEL
                for deck_card in self._balatro.deck_cards
            )
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STEEL_JOKER


@dataclass(eq=False)
class AbstractJoker(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult += 3 * len(self._balatro.jokers)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ABSTRACT


@dataclass(eq=False)
class GrosMichel(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult += 15

    def on_round_end(self) -> None:
        if self._balatro._chance(1, 6):
            self._balatro._destroy_joker(self)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GROS_MICHEL


@dataclass(eq=False)
class Supernova(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult += self._balatro.poker_hand_info[
            self._balatro.poker_hands[0]
        ][1]

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SUPERNOVA


@dataclass(eq=False)
class Blackboard(Joker):
    def on_independent_ability(self) -> None:
        if all(
            held_card.suit in [Suit.SPADES, Suit.CLUBS] or held_card == Enhancement.WILD
            for held_card in self._balatro.hand
        ):
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLACKBOARD


@dataclass(eq=False)
class IceCream(Joker):
    chips: int = field(default=100, init=False)

    def on_end_hand(self) -> None:
        self.chips -= 5
        if self.chips == 0:
            self._balatro._destroy_joker(self)

    def on_independent_ability(self) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ICE_CREAM


@dataclass(eq=False)
class BlueJoker(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.chips += 2 * len(self._balatro.deck_cards_left)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLUE_JOKER


@dataclass(eq=False)
class Constellation(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    def on_planet_used(self) -> None:
        self.xmult += 0.1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CONSTELLATION


@dataclass(eq=False)
class Superposition(Joker):
    def on_independent_ability(self) -> None:
        if (
            PokerHand.STRAIGHT in self._balatro.poker_hands
            and any(
                self._balatro.played_cards[i] == Rank.ACE
                for i in self._balatro.scored_card_indices
            )
            and self._balatro.effective_consumable_slots
            > len(self._balatro.consumables)
        ):
            self._balatro.consumables.append(self._balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SUPERPOSITION


@dataclass(eq=False)
class Cavendish(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult *= 3

    def on_round_end(self) -> None:
        if self._balatro._chance(1, 1000):
            self._balatro._destroy_joker(self)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CAVENDISH


@dataclass(eq=False)
class CardSharp(Joker):
    def on_independent_ability(self) -> None:
        if self._balatro.poker_hands[0] in self._balatro.round_poker_hands:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CARD_SHARP


@dataclass(eq=False)
class RedCard(Joker):
    mult: int = field(default=0, init=False)

    def on_independent_ability(self) -> None:
        self._balatro.mult += self.mult

    def on_pack_skipped(self) -> None:
        self.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RED_CARD


@dataclass(eq=False)
class Madness(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_blind_selected(self) -> None:
        if self._balatro.blind in [Blind.SMALL, Blind.BIG]:
            self.xmult += 0.5
            valid_destroys = [
                joker
                for joker in self._balatro.jokers
                if joker is not self and not joker.eternal
            ]
            if valid_destroys:
                self._balatro._destroy_joker(r.choice(valid_destroys))

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MADNESS


@dataclass(eq=False)
class Seance(Joker):
    def on_independent_ability(self) -> None:
        if self._balatro.poker_hands[
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

    def on_card_added(self, added_card: Card) -> None:
        self.xmult += 0.25

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HOLOGRAM


@dataclass(eq=False)
class Vagabond(Joker):
    will_create: bool = field(default=False, init=False)

    def on_hand_played(self) -> None:
        self.will_create = self._balatro.money <= 4

    def on_independent_ability(self) -> None:
        if self.will_create and self._balatro.effective_consumable_slots > len(
            self._balatro.consumables
        ):
            self._balatro.consumables.append(self._balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.VAGABOND


@dataclass(eq=False)
class Erosion(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult += 4 * max(
            0,
            (40 if self._balatro.deck is Deck.ABANDONED else 52)
            - len(self._balatro.deck_cards),
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EROSION


@dataclass(eq=False)
class FortuneTeller(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.mult += self._balatro.tarot_cards_used

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FORTUNE_TELLER


@dataclass(eq=False)
class StoneJoker(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.chips += 25 * sum(
            deck_card.is_stone_card for deck_card in self._balatro.deck_cards
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STONE


@dataclass(eq=False)
class Bull(Joker):
    def on_independent_ability(self) -> None:
        self._balatro.chips += 2 * max(0, self._balatro.money)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BULL


@dataclass(eq=False)
class FlashCard(Joker):
    mult: int = field(default=0, init=False)

    def on_independent_ability(self) -> None:
        self._balatro.mult += self.mult

    def on_reroll(self) -> None:
        self.mult += 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FLASH


@dataclass(eq=False)
class Popcorn(Joker):
    mult: int = field(default=20, init=False)

    def on_independent_ability(self) -> None:
        self._balatro.mult += self.mult

    def on_round_end(self) -> None:
        self.mult -= 4
        if self.mult == 0:
            self._balatro._destroy_joker(self)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.POPCORN


@dataclass(eq=False)
class Campfire(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_boss_defeated(self) -> None:
        self.xmult = 1.0

    def on_card_sold(self) -> None:
        self.xmult += 0.25

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CAMPFIRE


@dataclass(eq=False)
class Acrobat(Joker):
    def on_independent_ability(self) -> None:
        if self._balatro.hands == 0:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ACROBAT


@dataclass(eq=False)
class Swashbuckler(Joker):
    def on_independent_ability(self) -> None:
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
    def on_independent_ability(self) -> None:
        self._balatro.mult *= 1 + (0.25 * self._balatro.blinds_skipped)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.THROWBACK


@dataclass(eq=False)
class GlassJoker(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_glass_card_destroyed(self) -> None:
        self.xmult += 0.75

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GLASS


@dataclass(eq=False)
class FlowerPot(Joker):
    def on_independent_ability(self) -> None:
        suits = set()
        num_wilds = 0
        for i in self._balatro.scored_card_indices:
            scored_card = self._balatro.played_cards[i]
            if scored_card == Enhancement.WILD:
                num_wilds += 1
            elif not scored_card.is_stone_card:
                suits.add(scored_card.suit)
        if len(suits) + num_wilds >= 4:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FLOWER_POT


@dataclass(eq=False)
class SeeingDouble(Joker):
    def on_independent_ability(self) -> None:
        club = False
        other = False
        num_wilds = 0
        for i in self._balatro.scored_card_indices:
            scored_card = self._balatro.played_cards[i]
            if scored_card == Enhancement.WILD:
                num_wilds += 1
            elif not scored_card.is_stone_card:
                if scored_card.suit is Suit.CLUBS and not scored_card.debuffed:
                    club = True
                elif scored_card.suit is not Suit.CLUBS:
                    other = True
        if club + other + num_wilds >= 2:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SEEING_DOUBLE


@dataclass(eq=False)
class Matador(Joker):
    will_earn: bool = field(default=False, init=False)

    def on_hand_played(self) -> None:
        raise NotImplementedError

    def on_independent_ability(self) -> None:
        if self.will_earn:
            self._balatro.money += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MATADOR


@dataclass(eq=False)
class TheDuo(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.PAIR in self._balatro.poker_hands:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DUO


@dataclass(eq=False)
class TheTrio(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.THREE_OF_A_KIND in self._balatro.poker_hands:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIO


@dataclass(eq=False)
class TheFamily(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.FOUR_OF_A_KIND in self._balatro.poker_hands:
            self._balatro.mult *= 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FAMILY


@dataclass(eq=False)
class TheOrder(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.STRAIGHT in self._balatro.poker_hands:
            self._balatro.mult *= 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ORDER


@dataclass(eq=False)
class TheTribe(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.FLUSH in self._balatro.poker_hands:
            self._balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIBE


@dataclass(eq=False)
class Stuntman(Joker):
    def on_blind_selected(self) -> None:  # TODO: fix with copiers
        self._balatro.hand_size -= 2

    def on_independent_ability(self) -> None:
        self._balatro.chips += 250

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STUNTMAN


@dataclass(eq=False)
class DriversLicense(Joker):
    def on_independent_ability(self) -> None:
        if (
            sum(
                deck_card._enhancement is not None
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
    def on_independent_ability(self) -> None:
        self._balatro.mult += 2 * max(0, self._balatro.money // 5)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BOOTSTRAPS


@dataclass(eq=False)
class Canio(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_card_destroyed(self, destroyed_card: Card):
        if self._balatro._is_face_card(destroyed_card):
            self.xmult += 1.0

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CANIO


# ---- /independent ---- #

# ---- mixed/ ---- #


@dataclass(eq=False)
class RideTheBus(Joker):
    mult: int = field(default=0, init=False)

    def on_hand_played(self) -> None:
        for i in self._balatro.scored_card_indices:
            if self._balatro._is_face_card(self._balatro.played_cards[i]):
                self.mult = 0
                break
        else:
            self.mult += 1

    def on_independent_ability(self) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RIDE_THE_BUS


@dataclass(eq=False)
class Runner(Joker):
    chips: int = field(default=0, init=False)

    def on_hand_played(self) -> None:
        if PokerHand.STRAIGHT in self._balatro.poker_hands:
            self.chips += 15

    def on_independent_ability(self) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RUNNER


@dataclass(eq=False)
class GreenJoker(Joker):
    mult: int = field(default=0, init=False)

    def on_discard(self) -> None:
        self.mult = max(0, self.mult - 1)

    def on_hand_played(self) -> None:
        self.mult += 1

    def on_independent_ability(self) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GREEN_JOKER


@dataclass(eq=False)
class SquareJoker(Joker):
    chips: int = field(default=0, init=False)

    def on_hand_played(self) -> None:
        if len(self._balatro.played_cards) == 4:
            self.chips += 4

    def on_independent_ability(self) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SQUARE


@dataclass(eq=False)
class Vampire(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_hand_played(self) -> None:
        for i in self._balatro.scored_card_indices:
            scored_card = self._balatro.played_cards[i]
            if scored_card.enhancement is not None and not scored_card.debuffed:
                self.xmult += 0.1
                scored_card.enhancement = None

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.VAMPIRE


@dataclass(eq=False)
class Obelisk(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_hand_played(self) -> None:
        if self._balatro.poker_hand_info[self._balatro.poker_hands[0]][1] < max(
            times_played for hand_level, times_played in self._balatro.poker_hand_info
        ):
            self.xmult += 0.2
        else:
            self.xmult = 1.0

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.OBELISK


@dataclass(eq=False)
class LuckyCat(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_lucky_card_trigger(self) -> None:
        self.xmult += 0.25

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUCKY_CAT


@dataclass(eq=False)
class SpareTrousers(Joker):
    mult: int = field(default=0, init=False)

    def on_hand_played(self) -> None:
        if PokerHand.TWO_PAIR in self._balatro.poker_hands:
            self.mult += 2

    def on_independent_ability(self) -> None:
        self._balatro.mult += self.mult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TROUSERS


@dataclass(eq=False)
class Ramen(Joker):
    xmult: float = field(default=2.0, init=False)

    def on_discard(self) -> None:
        self.xmult -= 0.01 * len(self._balatro.discard_indices)
        if self.xmult <= 1.0:
            self._balatro._destroy_joker(self)

    def on_independent_ability(self) -> None:
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

    def on_discard(self) -> None:
        for i in self._balatro.discard_indices:
            if self._balatro.hand[i] == self.suit:
                self.chips += 3

    def on_independent_ability(self) -> None:
        self._balatro.chips += self.chips

    def on_round_end(self) -> None:
        self._set_random_suit()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CASTLE


@dataclass(eq=False)
class WeeJoker(Joker):
    chips: int = field(default=0, init=False)

    def on_card_scored(self, scored_card: Card) -> None:
        if scored_card == Rank.TWO:
            self.chips += 8

    def on_independent_ability(self) -> None:
        self._balatro.chips += self.chips

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WEE


@dataclass(eq=False)
class HitTheRoad(Joker):
    xmult: float = field(default=1.0, init=False)

    def on_discard(self) -> None:
        for i in self._balatro.discard_indices:
            if self._balatro.hand[i] == Rank.JACK:
                self.xmult += 0.5

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    def on_round_end(self) -> None:
        self.xmult = 1.0

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HIT_THE_ROAD


@dataclass(eq=False)
class Yorick(Joker):
    xmult: float = field(default=1.0, init=False)
    discards_remaining: int = field(default=23, init=False)

    def on_discard(self) -> None:
        self.discards_remaining -= len(self._balatro.discard_indices)
        while self.discards_remaining <= 0:
            self.xmult += 1.0
            self.discards_remaining += 23

    def on_independent_ability(self) -> None:
        self._balatro.mult *= self.xmult

    @property
    def joker_type(self) -> JokerType:
        return JokerType.YORICK


# ---- /mixed ---- #

# ---- on-other-jokers/ ---- #


@dataclass(eq=False)
class BaseballCard(Joker):
    def on_dependent_ability(self, joker: Joker) -> None:
        from balatro_constants import JOKER_TYPE_RARITIES

        if joker in JOKER_TYPE_RARITIES[Rarity.UNCOMMON]:
            self._balatro.mult *= 1.5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BASEBALL


# ---- /on-other-jokers ---- #

# ---- on-discard/ ---- #


@dataclass(eq=False)
class FacelessJoker(Joker):
    def on_discard(self) -> None:
        if (
            sum(
                self._balatro._is_face_card(self._balatro.hand[i])
                for i in self._balatro.discard_indices
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

    def on_discard(self) -> None:
        for i in self._balatro.discard_indices:
            if self._balatro.hand[i] == self.rank:
                self._balatro.money += 5

    def on_round_end(self) -> None:
        self._set_random_rank()

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MAIL


@dataclass(eq=False)
class TradingCard(Joker):
    def on_discard(self) -> None:
        if self._balatro.first_discard and len(self._balatro.discard_indices) == 1:
            self._balatro.money += 3
            self._balatro._destroy_card(
                self._balatro.hand[self._balatro.discard_indices[0]]
            )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRADING


@dataclass(eq=False)
class BurntJoker(Joker):
    def on_discard(self) -> None:
        if self._balatro.first_discard:
            self._balatro.poker_hand_info[self._balatro.poker_hand_discarded][1] += 1

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
    def on_blind_selected(self) -> None:
        stone_card = self._balatro._get_random_card()
        stone_card.enhancement = Enhancement.STONE
        self._balatro._add_card(stone_card)

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
    def on_round_end(self) -> None:
        if self._balatro.first_discard:
            self._balatro.money += 2 * self._balatro.discards

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DELAYED_GRAT


# ---- /other ---- #
