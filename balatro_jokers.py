from dataclasses import dataclass, field
import random as r

from balatro import *
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

    def on_played(self) -> None:
        if self.copied is not None:
            self.copied.on_played()

    def on_scored(self) -> None:
        if self.copied is not None:
            self.copied.on_scored()

    def on_scored_retriggers(self) -> int:
        if self.copied is not None:
            return self.copied.on_scored_retriggers()

    @property
    def is_active(self) -> bool:
        return self.copied.is_active


# ---- /base classes ---- #

# ---- copiers/ ---- #


@dataclass(eq=False)
class Blueprint(CopierJoker, Joker):
    def on_right_joker_changed(self) -> None:
        self.copied = None
        i = self.balatro.jokers.index(self)
        if i < len(self.balatro.jokers) - 1:
            self._set_copied_joker(self.balatro.jokers[i + 1])

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLUEPRINT


@dataclass(eq=False)
class Brainstorm(CopierJoker, Joker):
    def on_leftmost_joker_changed(self) -> None:
        self.copied = None
        self._set_copied_joker(self.balatro.jokers[0])

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BRAINSTORM


# ---- /copiers ---- #

# ---- on-played/ ---- #


@dataclass(eq=False)
class SpaceJoker(Joker):
    def on_played(self) -> None:
        if self.balatro._chance(1, 4):
            self.balatro.poker_hand_info[self.balatro.poker_hand][0] += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SPACE


@dataclass(eq=False)
class DNA(Joker):
    def on_played(self) -> None:
        if self.balatro.played_hands_round == 1 and len(self.balatro.played_cards) == 1:
            card_copy = self.balatro.played_cards[0].copy()
            self.balatro.deck_cards.append(card_copy)
            self.balatro.hand.append(card_copy)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DNA


@dataclass(eq=False)
class ToDoList(Joker):
    poker_hand: PokerHand = field(init=False)

    def __post_init__(self) -> None:
        self._set_random_poker_hand()

    def _set_random_poker_hand(self) -> None:
        self.poker_hand = r.choice(self.balatro.unlocked_poker_hands)

    def on_end_round(self) -> None:
        self._set_random_poker_hand()

    def on_played(self) -> None:
        if self.balatro.poker_hand is self.poker_hand:
            self.balatro.money += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TODO_LIST


@dataclass(eq=False)
class MidasMask(Joker):
    def on_played(self) -> None:
        for i in self.balatro.scored_card_indices:
            self.balatro.played_cards[i].enhancement = Enhancement.GOLD

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIDAS_MASK


# ---- /on-played ---- #

# ---- on-scored/ ---- #


@dataclass(eq=False)
class GreedyJoker(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.DIAMONDS
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ):
            self.balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GREEDY_JOKER


@dataclass(eq=False)
class LustyJoker(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.HEARTS
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ):
            self.balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.LUSTY_JOKER


@dataclass(eq=False)
class WrathfulJoker(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.SPADES
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ):
            self.balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WRATHFUL_JOKER


@dataclass(eq=False)
class GluttonousJoker(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.CLUBS
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ):
            self.balatro.mult += 3

    @property
    def joker_type(self) -> JokerType:
        return JokerType.GLUTTENOUS_JOKER


@dataclass(eq=False)
class EightBall(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.rank is Rank.EIGHT
            and self.balatro.effective_consumable_slots > len(self.balatro.consumables)
            and self.balatro._chance(1, 4)
        ):
            self.balatro.consumables.append(self.balatro._get_random_tarot())

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EIGHT_BALL


@dataclass(eq=False)
class Dusk(Joker):
    def on_scored_retriggers(self) -> int:
        return int(self.balatro.hands == 0)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DUSK


@dataclass(eq=False)
class Fibonacci(Joker):
    def on_scored(self) -> None:
        if self.balatro.scored_card.rank in [
            Rank.ACE,
            Rank.TWO,
            Rank.THREE,
            Rank.FIVE,
            Rank.EIGHT,
        ]:
            self.balatro.mult += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.FIBONACCI


@dataclass(eq=False)
class ScaryFace(Joker):
    def on_scored(self) -> None:
        if (
            JokerType.PAREIDOLIA in self.balatro.jokers
            or self.balatro.scored_card.rank
            in [
                Rank.KING,
                Rank.QUEEN,
                Rank.JACK,
            ]
        ):
            self.balatro.chips += 30

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCARY_FACE


@dataclass(eq=False)
class Hack(Joker):
    def on_scored_retriggers(self) -> int:
        return int(
            self.balatro.scored_card.rank
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
    def on_scored(self) -> None:
        if self.balatro.scored_card.rank in [
            Rank.TWO,
            Rank.FOUR,
            Rank.SIX,
            Rank.EIGHT,
            Rank.TEN,
        ]:
            self.balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.EVEN_STEVEN


@dataclass(eq=False)
class OddTodd(Joker):
    def on_scored(self) -> None:
        if self.balatro.scored_card.rank in [
            Rank.THREE,
            Rank.FIVE,
            Rank.SEVEN,
            Rank.NINE,
            Rank.ACE,
        ]:
            self.balatro.chips += 31

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ODD_TODD


@dataclass(eq=False)
class Scholar(Joker):
    def on_scored(self) -> None:
        if self.balatro.scored_card.rank is Rank.ACE:
            self.balatro.chips += 20
            self.balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SCHOLAR


@dataclass(eq=False)
class BusinessCard(Joker):
    def on_scored(self) -> None:
        if (
            JokerType.PAREIDOLIA in self.balatro.jokers
            or self.balatro.scored_card.rank
            in [
                Rank.KING,
                Rank.QUEEN,
                Rank.JACK,
            ]
        ) and self.balatro._chance(1, 2):
            self.balatro.money += 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BUSINESS


@dataclass(eq=False)
class Hiker(Joker):
    def on_scored(self) -> None:
        self.balatro.scored_card.bonus_chips += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HIKER


@dataclass(eq=False)
class Photograph(Joker):
    def on_scored(self) -> None:
        for i in self.balatro.scored_card_indices:
            scored_card = self.balatro.played_cards[i]

            if JokerType.PAREIDOLIA in self.balatro.jokers or scored_card.rank in [
                Rank.KING,
                Rank.QUEEN,
                Rank.JACK,
            ]:
                if scored_card is self.balatro.scored_card:
                    self.balatro.mult *= 2
                return

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

    def on_end_round(self) -> None:
        self._set_random_suit()

    def on_scored(self) -> None:
        if self.balatro.scored_card.suit is self.suit:
            self.balatro.mult = int(self.balatro.mult * 1.5)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ANCIENT


@dataclass(eq=False)
class WalkieTalkie(Joker):
    def on_scored(self) -> None:
        if self.balatro.scored_card.rank in [Rank.TEN, Rank.FOUR]:
            self.balatro.chips += 10
            self.balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WALKIE_TALKIE


@dataclass(eq=False)
class Seltzer(Joker):
    hands_left: int = field(default=10, init=False)

    def on_scored_retriggers(self) -> int:
        self.hands_left -= 1
        if self.hands_left == 0:
            raise NotImplementedError  # TODO: drank
        return 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SELZER


@dataclass(eq=False)
class SmileyFace(Joker):
    def on_scored(self) -> None:
        if (
            JokerType.PAREIDOLIA in self.balatro.jokers
            or self.balatro.scored_card.rank
            in [
                Rank.KING,
                Rank.QUEEN,
                Rank.JACK,
            ]
        ):
            self.balatro.mult += 5

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SMILEY


@dataclass(eq=False)
class GoldenTicket(Joker):
    def on_scored(self) -> None:
        if self.balatro.scored_card.enhancement is Enhancement.GOLD:
            self.balatro.money += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TICKET


@dataclass(eq=False)
class SockAndBuskin(Joker):
    def on_scored_retriggers(self) -> int:
        return int(
            JokerType.PAREIDOLIA in self.balatro.jokers
            or self.balatro.scored_card.rank
            in [
                Rank.KING,
                Rank.QUEEN,
                Rank.JACK,
            ]
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SOCK_AND_BUSKIN


@dataclass(eq=False)
class HangingChad(Joker):
    def on_scored_retriggers(self) -> int:
        return (
            2
            if (
                self.balatro.scored_card
                is self.balatro.played_cards[self.balatro.scored_card_indices[0]]
            )
            else 0
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HANGING_CHAD


@dataclass(eq=False)
class RoughGem(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.DIAMONDS
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ):
            self.balatro.money += 1

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ROUGH_GEM


@dataclass(eq=False)
class Bloodstone(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.HEARTS
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ) and self.balatro._chance(1, 2):
            self.balatro.mult = int(self.balatro.mult * 1.5)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BLOODSTONE


@dataclass(eq=False)
class Arrowhead(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.SPADES
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ):
            self.balatro.chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ARROWHEAD


@dataclass(eq=False)
class OnyxAgate(Joker):
    def on_scored(self) -> None:
        if (
            self.balatro.scored_card.suit is Suit.CLUBS
            or self.balatro.scored_card.enhancement is Enhancement.WILD
        ):
            self.balatro.mult += 7

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
            for deck_card in self.balatro.deck_cards
            if deck_card.enhancement is not Enhancement.STONE
        ]
        if valid_deck_cards:
            random_deck_card = r.choice(valid_deck_cards)
            self.card = Card(random_deck_card.suit, random_deck_card.rank)
        else:
            self.card = Card(Suit.SPADES, Rank.ACE)

    def on_end_round(self) -> None:
        self._set_random_card()

    def on_scored(self) -> None:
        if self.balatro.scored_card == self.card:
            self.balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.IDOL


@dataclass(eq=False)
class Triboulet(Joker):
    def on_scored(self) -> None:
        if self.balatro.scored_card.rank in [Rank.KING, Rank.QUEEN]:
            self.balatro.mult *= 2

    @property
    def joker_type(self) -> JokerType:
        return JokerType.TRIBOULET


# ---- /on-scored ---- #

# ---- on-held/ ---- #


@dataclass(eq=False)
class Mime(Joker):
    def on_held(self) -> None:
        raise NotImplementedError

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MIME


@dataclass(eq=False)
class RaisedFist(Joker):
    def on_held(self) -> None:
        self.balatro.mult += (
            min(
                [
                    int(held_card.rank)
                    for held_card in self.balatro.hand
                    if held_card.enhancement is not Enhancement.STONE
                    and not held_card.debuffed
                ],
                default=0,
            )
            * 2
        )

    @property
    def joker_type(self) -> JokerType:
        return JokerType.RAISED_FIST


@dataclass(eq=False)
class Baron(Joker):
    def on_held(self) -> None:
        for held_card in self.balatro.hand:
            if held_card.rank is Rank.KING and not held_card.debuffed:
                self.balatro.mult = int(self.balatro.mult * 1.5)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.BARON


@dataclass(eq=False)
class ReservedParking(Joker):
    def on_held(self) -> None:
        pass

    @property
    def joker_type(self) -> JokerType:
        for held_card in self.balatro.hand:
            if (
                (
                    JokerType.PAREIDOLIA in self.balatro.jokers
                    or held_card.rank
                    in [
                        Rank.KING,
                        Rank.QUEEN,
                        Rank.JACK,
                    ]
                )
                and not held_card.debuffed
                and self.balatro._chance(1, 2)
            ):
                self.balatro.money += 1


@dataclass(eq=False)
class ShootTheMoon(Joker):
    def on_held(self) -> None:
        for held_card in self.balatro.hand:
            if held_card.rank is Rank.QUEEN and not held_card.debuffed:
                self.balatro.mult += 13

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SHOOT_THE_MOON


# ---- /on-held ---- #

# ---- independent/ ---- #


@dataclass(eq=False)
class Jimbo(Joker):
    def on_independent_ability(self) -> None:
        self.balatro.mult += 4

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOKER


@dataclass(eq=False)
class JollyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.PAIR in self.balatro.poker_hand_contains:
            self.balatro.mult += 8

    @property
    def joker_type(self) -> JokerType:
        return JokerType.JOLLY


@dataclass(eq=False)
class ZanyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.THREE_OF_A_KIND in self.balatro.poker_hand_contains:
            self.balatro.mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.ZANY


@dataclass(eq=False)
class MadJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.TWO_PAIR in self.balatro.poker_hand_contains:
            self.balatro.mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.MAD


@dataclass(eq=False)
class CrazyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.STRAIGHT in self.balatro.poker_hand_contains:
            self.balatro.mult += 12

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAZY


@dataclass(eq=False)
class DrollJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.FLUSH in self.balatro.poker_hand_contains:
            self.balatro.mult += 10

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DROLL


@dataclass(eq=False)
class SlyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.PAIR in self.balatro.poker_hand_contains:
            self.balatro.chips += 50

    @property
    def joker_type(self) -> JokerType:
        return JokerType.SLY


@dataclass(eq=False)
class WilyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.THREE_OF_A_KIND in self.balatro.poker_hand_contains:
            self.balatro.chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.WILY


@dataclass(eq=False)
class CleverJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.TWO_PAIR in self.balatro.poker_hand_contains:
            self.balatro.chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CLEVER


@dataclass(eq=False)
class DeviousJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.STRAIGHT in self.balatro.poker_hand_contains:
            self.balatro.chips += 100

    @property
    def joker_type(self) -> JokerType:
        return JokerType.DEVIOUS


@dataclass(eq=False)
class CraftyJoker(Joker):
    def on_independent_ability(self) -> None:
        if PokerHand.FLUSH in self.balatro.poker_hand_contains:
            self.balatro.chips += 80

    @property
    def joker_type(self) -> JokerType:
        return JokerType.CRAFTY


@dataclass(eq=False)
class HalfJoker(Joker):
    def on_independent_ability(self) -> None:
        if len(self.balatro.played_cards) <= 3:
            self.balatro.mult += 20

    @property
    def joker_type(self) -> JokerType:
        return JokerType.HALF


@dataclass(eq=False)
class JokerStencil(Joker):
    def on_independent_ability(self) -> None:
        self.balatro.mult *= (
            self.balatro.effective_joker_slots - len(self.balatro.jokers)
        ) + self.balatro.jokers.count(JokerType.STENCIL)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STENCIL


@dataclass(eq=False)
class JokerStencil(Joker):
    def on_independent_ability(self) -> None:
        self.balatro.mult *= (
            self.balatro.effective_joker_slots - len(self.balatro.jokers)
        ) + self.balatro.jokers.count(JokerType.STENCIL)

    @property
    def joker_type(self) -> JokerType:
        return JokerType.STENCIL


# ---- /independent ---- #

# ---- mixed/ ---- #

# ---- /mixed ---- #

# ---- on-other-jokers/ ---- #

# ---- /on-other-jokers ---- #

# ---- on-discard/ ---- #

# ---- /on-discard ---- #

# ---- other/ ---- #

# ---- /other ---- #
