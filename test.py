from typing import Any
import unittest

from balatro import *


class TestBalatro(unittest.TestCase):
    def _check_expected(self, test_config: dict[str, Any]) -> None:
        expected = test_config["expected"]

        if "round_score" in expected:
            self.assertEqual(
                Run.format_number(self.run.round_score),
                expected["round_score"],
            )
            del expected["round_score"]
        if "custom" in expected:
            self.assertTrue(expected["custom"](self.run))
            del expected["custom"]

        for attr, value in expected.items():
            self.assertEqual(getattr(self.run, attr), value)

    def _set_up_hand(self, test_config: dict[str, Any]) -> Run:
        if "deck" in test_config:
            deck = Deck[test_config["deck"]]
            del test_config["deck"]
        else:
            deck = Deck.RED
        if "stake" in test_config:
            stake = Stake[test_config["stake"]]
            del test_config["stake"]
        else:
            stake = Stake.WHITE

        self.run = Run(
            deck,
            stake=stake,
        )
        self.run.select_blind()

        if "poker_hand_levels" in test_config:
            for poker_hand, level in test_config["poker_hand_levels"].items():
                self.run.poker_hand_info[PokerHand[poker_hand]][0] = level
            del test_config["poker_hand_levels"]
        if "poker_hand_times_played" in test_config:
            for poker_hand, times_played in test_config[
                "poker_hand_times_played"
            ].items():
                self.run.poker_hand_info[PokerHand[poker_hand]][1] = times_played
            del test_config["poker_hand_times_played"]
        if "num_deck_cards_left" in test_config:
            assert len(self.run.deck_cards) >= test_config["num_deck_cards_left"]
            self.run.deck_cards = self.run.deck_cards[
                : test_config["num_deck_cards_left"]
            ]
            del test_config["num_deck_cards_left"]
        if "custom_setup" in test_config:
            test_config["custom_setup"](self.run)
            del test_config["custom_setup"]

        if "hand" in test_config:
            hand = []
            for card_str in test_config["hand"]:
                match card_str[0]:
                    case "A":
                        rank = Rank.ACE
                    case "K":
                        rank = Rank.KING
                    case "Q":
                        rank = Rank.QUEEN
                    case "J":
                        rank = Rank.JACK
                    case "T":
                        rank = Rank.TEN
                    case "9":
                        rank = Rank.NINE
                    case "8":
                        rank = Rank.EIGHT
                    case "7":
                        rank = Rank.SEVEN
                    case "6":
                        rank = Rank.SIX
                    case "5":
                        rank = Rank.FIVE
                    case "4":
                        rank = Rank.FOUR
                    case "3":
                        rank = Rank.THREE
                    case "2":
                        rank = Rank.TWO

                match card_str[1]:
                    case "S":
                        suit = Suit.SPADES
                    case "H":
                        suit = Suit.HEARTS
                    case "C":
                        suit = Suit.CLUBS
                    case "D":
                        suit = Suit.DIAMONDS

                modifiers = card_str[3:].split(",")
                enhancement, seal, edition, bonus_chips, debuffed = (
                    None,
                    None,
                    Edition.BASE,
                    0,
                    False,
                )
                for modifier in modifiers:
                    if modifier == "bonus":
                        enhancement = Enhancement.BONUS
                    elif modifier == "mult":
                        enhancement = Enhancement.MULT
                    elif modifier == "wild":
                        enhancement = Enhancement.WILD
                    elif modifier == "glass":
                        enhancement = Enhancement.GLASS
                    elif modifier == "steel":
                        enhancement = Enhancement.STEEL
                    elif modifier == "stone":
                        enhancement = Enhancement.STONE
                    elif modifier == "gold":
                        enhancement = Enhancement.GOLD
                    elif modifier == "lucky":
                        enhancement = Enhancement.LUCKY

                    if modifier == "redseal":
                        seal = Seal.RED
                    elif modifier == "blueseal":
                        seal = Seal.BLUE
                    elif modifier == "goldseal":
                        seal = Seal.GOLD
                    elif modifier == "purpleseal":
                        seal = Seal.PURPLE

                    if modifier == "foil":
                        edition = Edition.FOIL
                    elif modifier == "holo":
                        edition = Edition.HOLO
                    elif modifier == "polychrome":
                        edition = Edition.POLYCHROME
                    elif modifier == "negative":
                        edition = Edition.NEGATIVE

                    if modifier.startswith("+"):
                        bonus_chips = int(modifier[1:])

                    if modifier == "debuffed":
                        debuffed = True

                card = Card(
                    suit,
                    rank,
                    enhancement=enhancement,
                    seal=seal,
                    edition=edition,
                    bonus_chips=bonus_chips,
                    debuffed=debuffed,
                )
                hand.append(card)
            self.run.hand = hand
            del test_config["hand"]

        if "jokers" in test_config:
            for joker_config in test_config["jokers"]:
                joker = self.run._create_joker(JokerType[joker_config["joker_type"]])
                del joker_config["joker_type"]
                for attr, value in joker_config.items():
                    setattr(joker, attr, value)
                self.run._add_joker(joker)
            del test_config["jokers"]

        for attr, value in test_config.items():
            setattr(self.run, attr, value)

    def run_balatro_test_discarded(self, test_config: dict[str, Any]) -> None:
        self._set_up_hand(test_config)

        self.run.discard(test_config["discard_indices"])

        self._check_expected(test_config)

    def run_balatro_test_scored(self, test_config: dict[str, Any]) -> None:
        self._set_up_hand(test_config)

        self.run.play_hand(test_config["played_card_indices"])

        self._check_expected(test_config)


def create_test_method(test_name, test_config, test_type):
    def test_method_discarded(self):
        self.run_balatro_test_discarded(test_config)

    def test_method_scored(self):
        self.run_balatro_test_scored(test_config)

    match test_type:
        case "discarded":
            test_method = test_method_discarded
        case "round_end":
            test_method = test_method_scored
        case "scored":
            test_method = test_method_scored

    test_method.__name__ = test_name
    return test_method


def test_sixth_sense_scored_simple_custom_setup(run: Run) -> None:
    c = Card(Suit.CLUBS, Rank.SIX)
    run.deck_cards.append(c)
    run.hand.insert(0, c)


test_cases = {
    "discarded": [
        {
            "test_name": "test_mail_in_rebate_discarded_simple",
            "config": {
                "jokers": [
                    {"joker_type": "GROS_MICHEL"},
                    {"joker_type": "RIFF_RAFF"},
                    {"joker_type": "SHOOT_THE_MOON"},
                    {"joker_type": "MAIL_IN_REBATE", "rank": Rank.FOUR},
                ],
                "money": 2,
                "hand": ["AC", "KS", "KH", "QC", "JC", "7S", "4S", "3S"],
                "discard_indices": [0, 5, 6, 7],
                "expected": {"money": 7},
            },
        },
        {
            "test_name": "test_mail_in_rebate_discarded_debuffed_card",
            "config": {
                "jokers": [
                    {"joker_type": "GROS_MICHEL"},
                    {"joker_type": "RIFF_RAFF"},
                    {"joker_type": "SHOOT_THE_MOON"},
                    {"joker_type": "MAIL_IN_REBATE", "rank": Rank.FOUR},
                ],
                "money": 2,
                "hand": ["AC", "KS", "KH", "QC", "JC", "7S", "4S,debuffed", "3S"],
                "discard_indices": [0, 5, 6, 7],
                "expected": {"money": 2},
            },
        },
        {
            "test_name": "test_mail_in_rebate_discarded_multiple",
            "config": {
                "jokers": [
                    {"joker_type": "GROS_MICHEL"},
                    {"joker_type": "RIFF_RAFF"},
                    {"joker_type": "SHOOT_THE_MOON"},
                    {"joker_type": "MAIL_IN_REBATE", "rank": Rank.KING},
                ],
                "money": 2,
                "hand": ["AC", "KS", "KH", "QC", "JC", "7S", "4S", "3S"],
                "discard_indices": [0, 1, 2, 3, 4],
                "expected": {"money": 12},
            },
        },
    ],
    "round_end": [
        {
            "test_name": "test_mime_retrigger_gold_cards",
            "config": {
                "jokers": [
                    {"joker_type": "MIME"},
                    {"joker_type": "GREEN_JOKER", "mult": 100},
                    {"joker_type": "BRAINSTORM"},
                    {"joker_type": "BLUEPRINT"},
                ],
                "hand": [
                    "AS",
                    "KH,gold,blueseal",
                ],
                "money": 0,
                "hands": 1,
                "consumable_slots": 4,
                "played_card_indices": [0],
                "expected": {
                    "custom": lambda b: [c.card.__class__ for c in b.consumables]
                    == [Planet, Planet, Planet],
                    "money": 9,
                },
            },
        },
    ],
    "scored": [
        {
            "test_name": "test_sixth_sense_scored_simple",
            "config": {
                "custom_setup": test_sixth_sense_scored_simple_custom_setup,
                "jokers": [
                    {"joker_type": "SIXTH_SENSE"},
                ],
                "played_card_indices": [0],
                "expected": {
                    "custom": lambda b: sum(
                        (card.suit is Suit.CLUBS and card.rank is Rank.SIX)
                        for card in b.deck_cards
                    )
                    == 1
                },
            },
        },
        {
            "test_name": "test_random_scored_1",
            "config": {
                "deck": "PLASMA",
                "poker_hand_levels": {"HIGH_CARD": 43},
                "jokers": [
                    {"joker_type": "BARON"},
                    {"joker_type": "BARON"},
                    {"joker_type": "BARON"},
                    {"joker_type": "MAIL_IN_REBATE"},
                    {"joker_type": "BRAINSTORM"},
                    {"joker_type": "GREEDY_JOKER", "edition": Edition.NEGATIVE},
                    {"joker_type": "GROS_MICHEL", "edition": Edition.NEGATIVE},
                ],
                "hand": [
                    "KH,steel,redseal",
                    "KH,steel,redseal",
                    "KH,steel,redseal",
                    "KC,steel,redseal",
                    "KC,steel,redseal",
                    "7C,blueseal",
                    "7C,gold,blueseal",
                    "4C",
                    "KD,steel,blueseal",
                ],
                "played_card_indices": [7],
                "expected": {"round_score": "1.084e22"},
            },
        },
        {
            "test_name": "test_random_scored_2",
            "config": {
                "deck": "PLASMA",
                "poker_hand_levels": {"HIGH_CARD": 2},
                "jokers": [
                    {"joker_type": "PHOTOGRAPH"},
                    {"joker_type": "BARON"},
                    {"joker_type": "INVISIBLE_JOKER"},
                    {"joker_type": "BRAINSTORM"},
                    {"joker_type": "HANGING_CHAD"},
                ],
                "hand": [
                    "QD,bonus",
                    "8S,bonus",
                    "KC,redseal",
                    "9C",
                    "8C",
                    "6C,blueseal",
                    "3C",
                    "2C,lucky",
                ],
                "played_card_indices": [0, 1],
                "expected": {"round_score": "44,521"},
            },
        },
        {
            "test_name": "test_random_scored_3",
            "config": {
                "deck": "PLASMA",
                "poker_hand_levels": {"HIGH_CARD": 121},
                "jokers": [
                    {"joker_type": "DNA"},
                    {"joker_type": "MIME"},
                    {"joker_type": "BARON"},
                    {"joker_type": "BARON"},
                    {"joker_type": "BLUEPRINT"},
                    {"joker_type": "BRAINSTORM"},
                ],
                "hand": [
                    "KS",
                    "KH,steel,redseal",
                    "KH,steel,redseal",
                    "KH,steel,redseal",
                    "KH,steel,redseal",
                    "KC,steel,redseal",
                    "KC,steel,redseal",
                    "KC,steel,redseal",
                    "KC,steel,redseal",
                    "KD,steel,blueseal",
                ],
                "played_card_indices": [1],
                "expected": {"round_score": "6.050e38"},
            },
        },
        {
            "test_name": "test_random_scored_4",
            "config": {
                "poker_hand_levels": {"THREE_OF_A_KIND": 14},
                "jokers": [
                    {
                        "joker_type": "CONSTELLATION",
                        "edition": Edition.NEGATIVE,
                        "eternal": True,
                        "xmult": 11.9,
                    },
                    {"joker_type": "SOCK_AND_BUSKIN", "eternal": True},
                    {"joker_type": "SOCK_AND_BUSKIN", "eternal": True},
                    {"joker_type": "HOLOGRAM", "eternal": True, "xmult": 5.75},
                    {"joker_type": "BRAINSTORM"},
                ],
                "hand": [
                    "KS,lucky,debuffed",
                    "KH,lucky",
                    "KH,glass,redseal",
                    "KH,lucky",
                    "KH,glass,redseal",
                    "KC,gold",
                    "KC",
                    "QD,gold,goldseal",
                    "JH,gold",
                    "8H,bonus",
                    "4H",
                ],
                "played_card_indices": [0, 5, 6, 9, 10],
                "expected": {"round_score": "8,264,713"},
            },
        },
        {
            "test_name": "test_random_scored_5",
            "config": {
                "poker_hand_levels": {"FULL_HOUSE": 2},
                "jokers": [
                    {"joker_type": "BASEBALL_CARD"},
                    {"joker_type": "CARD_SHARP"},
                    {"joker_type": "CONSTELLATION", "eternal": True, "xmult": 2.6},
                    {"joker_type": "OOPS_ALL_SIXES", "edition": Edition.POLYCHROME},
                    {"joker_type": "HOLOGRAM"},
                ],
                "hand": [
                    "AS",
                    "AC",
                    "TC",
                    "8S",
                    "8C",
                    "8D",
                    "5H",
                    "5D",
                ],
                "played_card_indices": [3, 4, 5, 6, 7],
                "expected": {"round_score": "11,727"},
            },
        },
        {
            "test_name": "test_random_scored_6",
            "config": {
                "poker_hand_levels": {"THREE_OF_A_KIND": 9},
                "jokers": [
                    {"joker_type": "POPCORN", "mult": 12},
                    {"joker_type": "THROWBACK"},
                ],
                "blinds_skipped": 2,
                "hand": [
                    "8C,mult",
                    "8C,mult",
                    "8D,glass",
                ],
                "played_card_indices": [0, 1, 2],
                "expected": {"round_score": "21,186"},
            },
        },
        {
            "test_name": "test_random_scored_7",
            "config": {
                "poker_hand_levels": {"HIGH_CARD": 8},
                "jokers": [
                    {"joker_type": "SHOOT_THE_MOON", "edition": Edition.HOLO},
                    {"joker_type": "BARON"},
                    {"joker_type": "RAISED_FIST"},
                ],
                "hand": [
                    "AD,steel",
                    "KC",
                    "QH",
                    "QS,steel",
                    "9S",
                    "6S,glass,redseal",
                    "6C",
                ],
                "played_card_indices": [4],
                "expected": {"round_score": "6,846"},
            },
        },
        {
            "test_name": "test_random_scored_8",
            "config": {
                "poker_hand_levels": {"HIGH_CARD": 8},
                "jokers": [
                    {"joker_type": "SHOOT_THE_MOON", "edition": Edition.HOLO},
                    {"joker_type": "BARON"},
                    {"joker_type": "RAISED_FIST"},
                ],
                "hand": [
                    "AD,steel",
                    "KC",
                    "QS,steel",
                    "QH",
                    "9S",
                    "6S,glass,redseal",
                    "6C",
                ],
                "played_card_indices": [4],
                "expected": {"round_score": "6,300"},
            },
        },
        {
            "test_name": "test_random_scored_9",
            "config": {
                "poker_hand_levels": {"HIGH_CARD": 8},
                "jokers": [
                    {"joker_type": "SHOOT_THE_MOON", "edition": Edition.HOLO},
                    {"joker_type": "BARON"},
                    {"joker_type": "RAISED_FIST"},
                ],
                "hand": [
                    "QH",
                    "QS,steel",
                    "KC",
                    "AD,steel",
                    "9S",
                    "6S,glass,redseal",
                    "6C",
                ],
                "played_card_indices": [4],
                "expected": {"round_score": "10,258"},
            },
        },
        {
            "test_name": "test_random_scored_10",
            "config": {
                "poker_hand_levels": {"HIGH_CARD": 8},
                "jokers": [
                    {"joker_type": "SHOOT_THE_MOON", "edition": Edition.HOLO},
                    {"joker_type": "BARON"},
                    {"joker_type": "RAISED_FIST"},
                ],
                "hand": [
                    "6C",
                    "6S,glass,redseal",
                    "QH",
                    "QS,steel",
                    "KC",
                    "AD,steel",
                    "9S",
                ],
                "played_card_indices": [6],
                "expected": {"round_score": "16,054"},
            },
        },
        {
            "test_name": "test_random_scored_11",
            "config": {
                "poker_hand_levels": {"FIVE_OF_A_KIND": 3},
                "jokers": [
                    {"joker_type": "CLEVER_JOKER"},
                    {"joker_type": "RAISED_FIST"},
                    {"joker_type": "SOCK_AND_BUSKIN", "perishable": True},
                    {"joker_type": "MERRY_ANDY", "perishable": True},
                    {"joker_type": "PHOTOGRAPH", "eternal": True},
                ],
                "hand": [
                    "KS,mult",
                    "KS",
                    "KH",
                    "KC",
                    "KD",
                    "QH",
                    "QC",
                ],
                "played_card_indices": [0, 1, 2, 3, 4],
                "expected": {"round_score": "33,640"},
            },
        },
        {
            "test_name": "test_random_scored_12",
            "config": {
                "jokers": [
                    {"joker_type": "RUNNER", "eternal": True},
                    {"joker_type": "GLUTTONOUS_JOKER", "eternal": True},
                    {"joker_type": "FORTUNE_TELLER", "eternal": True},
                    {"joker_type": "MADNESS", "xmult": 4.5},
                    {
                        "joker_type": "FLOWER_POT",
                        "edition": Edition.FOIL,
                        "eternal": True,
                    },
                ],
                "tarot_cards_used": 7,
                "hand": [
                    "AS",
                    "9H,glass",
                    "8D",
                    "7S",
                    "7C",
                    "6S,bonus",
                    "5S,bonus",
                    "3H",
                ],
                "played_card_indices": [1, 2, 4, 5, 6],
                "expected": {"round_score": "46,170"},
            },
        },
        {
            "test_name": "test_random_scored_13",
            "config": {
                "poker_hand_levels": {"FIVE_OF_A_KIND": 5},
                "jokers": [
                    {"joker_type": "DUSK"},
                    {"joker_type": "BLUEPRINT"},
                    {"joker_type": "TRIBOULET"},
                    {"joker_type": "THE_FAMILY"},
                    {"joker_type": "PERKEO"},
                ],
                "hand": [
                    "KS",
                    "KS,bonus",
                    "KH,steel",
                    "KH",
                    "KH,steel",
                    "KH,steel",
                    "KC,steel",
                    "QD",
                ],
                "played_card_indices": [0, 1, 2, 3, 4],
                "expected": {"round_score": "75,202,560"},
            },
        },
        {
            "test_name": "test_random_scored_14",
            "config": {
                "poker_hand_levels": {"FLUSH": 2},
                "jokers": [
                    {"joker_type": "GREEN_JOKER", "mult": 22},
                    {"joker_type": "EROSION"},
                    {"joker_type": "VAGABOND"},
                    {"joker_type": "THROWBACK"},
                    {"joker_type": "CREDIT_CARD"},
                ],
                "num_deck_cards_left": 46,
                "blinds_skipped": 1,
                "hand": [
                    "AH,debuffed",
                    "AH,bonus,debuffed",
                    "KH,debuffed",
                    "JH,debuffed",
                    "4H,wild,debuffed",
                ],
                "played_card_indices": [0, 1, 2, 3, 4],
                "expected": {
                    "round_score": "3,312",
                    "custom": lambda b: [c.card.__class__ for c in b.consumables]
                    == [Tarot],
                },
            },
        },
        {
            "test_name": "test_random_scored_15",
            "config": {
                "hand": ["AS", "KD", "QC", "JH", "TC", "4S", "4C", "2D"],
                "played_card_indices": [0, 1, 2, 3, 4],
                "expected": {"round_score": "324"},
            },
        },
        {
            "test_name": "test_random_scored_16",
            "config": {
                "poker_hand_levels": {"FLUSH": 13},
                "jokers": [
                    {"joker_type": "PHOTOGRAPH", "edition": Edition.FOIL},
                    {"joker_type": "SUPERNOVA"},
                    {"joker_type": "WALKIE_TALKIE", "edition": Edition.NEGATIVE},
                    {
                        "joker_type": "VAMPIRE",
                        "xmult": 8.0,
                    },
                    {"joker_type": "MIDAS_MASK", "eternal": True},
                    {"joker_type": "CONSTELLATION", "xmult": 3.0},
                ],
                "hand": ["QS,gold", "TS", "5S", "TH,mult", "8H", "4H", "3H", "QH,gold"],
                "poker_hand_times_played": {"FLUSH": 50},
                "played_card_indices": [3, 4, 5, 6, 7],
                "expected": {"round_score": "968,256"},
            },
        },
    ],
}


for test_type, test_cases in test_cases.items():
    if test_type == "round_end":
        continue
    for test_case in test_cases:
        test_name = test_case["test_name"]
        test_config = test_case["config"]
        setattr(
            TestBalatro,
            test_name,
            create_test_method(test_name, test_config, test_type),
        )

if __name__ == "__main__":
    unittest.main(verbosity=2)
