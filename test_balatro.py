from typing import Any
import unittest

from balatro import *


class TestBalatro(unittest.TestCase):
    def run_balatro_test(self, test_config: dict[str, Any]) -> None:
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

        b = Balatro(
            deck,
            stake=stake,
        )
        b.select_blind()

        if "poker_hand_levels" in test_config:
            for poker_hand, level in test_config["poker_hand_levels"].items():
                b.poker_hand_info[PokerHand[poker_hand]][0] = level
            del test_config["poker_hand_levels"]
        if "poker_hand_times_played" in test_config:
            for poker_hand, times_played in test_config[
                "poker_hand_times_played"
            ].items():
                b.poker_hand_info[PokerHand[poker_hand]][1] = times_played
            del test_config["poker_hand_times_played"]

        if "num_deck_cards_left" in test_config:
            assert len(b.deck_cards) >= test_config["num_deck_cards_left"]
            b.deck_cards = b.deck_cards[: test_config["num_deck_cards_left"]]
            del test_config["num_deck_cards_left"]

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
            b.hand = hand
            del test_config["hand"]

        if "jokers" in test_config:
            for joker_config in test_config["jokers"]:
                joker = b._create_joker(JokerType[joker_config["joker_type"]])
                del joker_config["joker_type"]
                for attr, value in joker_config.items():
                    setattr(joker, attr, value)
                b._add_joker(joker)
            del test_config["jokers"]

        for attr, value in test_config.items():
            setattr(b, attr, value)

        b.play_hand(test_config["card_indices"])

        self.assertEqual(
            Balatro.format_number(b.round_score), test_config["expected_score"]
        )
        if "expected_consumable_types" in test_config:
            self.assertEqual(
                len(b.consumables), len(test_config["expected_consumable_types"])
            )
            for consumable, expected_consumable_type in zip(
                b.consumables, test_config["expected_consumable_types"]
            ):
                self.assertIsInstance(
                    consumable.consumable_type, expected_consumable_type
                )


def create_test_method(test_name, test_config):
    def test_method(self):
        self.run_balatro_test(test_config)

    test_method.__name__ = test_name
    return test_method


test_cases = [
    {
        "test_name": "test_random_1",
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
            "card_indices": [7],
            "expected_score": "1.084e22",
        },
    },
    {
        "test_name": "test_random_2",
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
            "card_indices": [0, 1],
            "expected_score": "44,521",
        },
    },
    {
        "test_name": "test_random_3",
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
            "card_indices": [1],
            "expected_score": "6.050e38",
        },
    },
    {
        "test_name": "test_random_4",
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
            "card_indices": [0, 5, 6, 9, 10],
            "expected_score": "8,264,713",
        },
    },
    {
        "test_name": "test_random_5",
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
            "card_indices": [3, 4, 5, 6, 7],
            "expected_score": "11,727",
        },
    },
    {
        "test_name": "test_random_6",
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
            "card_indices": [0, 1, 2],
            "expected_score": "21,186",
        },
    },
    {
        "test_name": "test_random_7",
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
            "card_indices": [4],
            "expected_score": "6,846",
        },
    },
    {
        "test_name": "test_random_8",
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
            "card_indices": [4],
            "expected_score": "6,300",
        },
    },
    {
        "test_name": "test_random_9",
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
            "card_indices": [4],
            "expected_score": "10,258",
        },
    },
    {
        "test_name": "test_random_10",
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
            "card_indices": [6],
            "expected_score": "16,054",
        },
    },
    {
        "test_name": "test_random_11",
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
            "card_indices": [0, 1, 2, 3, 4],
            "expected_score": "33,640",
        },
    },
    {
        "test_name": "test_random_12",
        "config": {
            "jokers": [
                {"joker_type": "RUNNER", "eternal": True},
                {"joker_type": "GLUTTONOUS_JOKER", "eternal": True},
                {"joker_type": "FORTUNE_TELLER", "eternal": True},
                {"joker_type": "MADNESS", "xmult": 4.5},
                {"joker_type": "FLOWER_POT", "edition": Edition.FOIL, "eternal": True},
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
            "card_indices": [1, 2, 4, 5, 6],
            "expected_score": "46,170",
        },
    },
    {
        "test_name": "test_random_13",
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
            "card_indices": [0, 1, 2, 3, 4],
            "expected_score": "75,202,560",
        },
    },
    {
        "test_name": "test_random_14",
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
            "card_indices": [0, 1, 2, 3, 4],
            "expected_score": "3,312",
            "expected_consumable_types": [Tarot],
        },
    },
]


for test_case in test_cases:
    test_name = test_case["test_name"]
    test_config = test_case["config"]
    setattr(TestBalatro, test_name, create_test_method(test_name, test_config))

if __name__ == "__main__":
    unittest.main(verbosity=2)
