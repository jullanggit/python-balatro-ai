import unittest

from balatro import *


class TestBalatroRandom(unittest.TestCase):
    def test_random_1(self) -> None:
        b = Balatro(Deck.PLASMA)
        b.select_blind()
        b.poker_hand_info[PokerHand.HIGH_CARD][0] = 43
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.MAIL))
        b._add_joker(b._create_joker(JokerType.BRAINSTORM))
        b._add_joker(b._create_joker(JokerType.GREEDY_JOKER, edition=Edition.NEGATIVE))
        b._add_joker(b._create_joker(JokerType.GROS_MICHEL, edition=Edition.NEGATIVE))
        b.hand = [
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.RED_SEAL,
            ),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.RED_SEAL,
            ),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.RED_SEAL,
            ),
            Card(
                Suit.CLUBS, Rank.KING, enhancement=Enhancement.STEEL, seal=Seal.RED_SEAL
            ),
            Card(
                Suit.CLUBS, Rank.KING, enhancement=Enhancement.STEEL, seal=Seal.RED_SEAL
            ),
            Card(Suit.CLUBS, Rank.SEVEN, seal=Seal.BLUE_SEAL),
            Card(
                Suit.CLUBS,
                Rank.SEVEN,
                enhancement=Enhancement.GOLD,
                seal=Seal.BLUE_SEAL,
            ),
            Card(Suit.CLUBS, Rank.FOUR),
            Card(
                Suit.DIAMONDS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.BLUE_SEAL,
            ),
        ]
        b.play_hand([7])

        self.assertEqual(Balatro.format_number(b.round_score), "1.084e22")

    def test_random_2(self) -> None:
        b = Balatro(Deck.PLASMA)
        b.select_blind()
        b.poker_hand_info[PokerHand.HIGH_CARD][0] = 2
        b._add_joker(b._create_joker(JokerType.PHOTOGRAPH))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.INVISIBLE))
        b._add_joker(b._create_joker(JokerType.BRAINSTORM))
        b._add_joker(b._create_joker(JokerType.HANGING_CHAD))
        b.hand = [
            Card(Suit.DIAMONDS, Rank.QUEEN, enhancement=Enhancement.BONUS),
            Card(Suit.SPADES, Rank.EIGHT, enhancement=Enhancement.BONUS),
            Card(Suit.CLUBS, Rank.KING, seal=Seal.RED_SEAL),
            Card(Suit.CLUBS, Rank.NINE),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.SIX, seal=Seal.BLUE_SEAL),
            Card(Suit.CLUBS, Rank.THREE),
            Card(Suit.CLUBS, Rank.TWO, enhancement=Enhancement.LUCKY),
        ]
        b.play_hand([0, 1])

        self.assertEqual(Balatro.format_number(b.round_score), "44,521")

    def test_random_3(self) -> None:
        b = Balatro(Deck.PLASMA)
        b.select_blind()
        b.poker_hand_info[PokerHand.HIGH_CARD][0] = 121
        b._add_joker(b._create_joker(JokerType.DNA))
        b._add_joker(b._create_joker(JokerType.MIME))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.BLUEPRINT))
        b._add_joker(b._create_joker(JokerType.BRAINSTORM))
        b.hand = [
            Card(Suit.SPADES, Rank.KING),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.RED_SEAL,
            ),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.RED_SEAL,
            ),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.RED_SEAL,
            ),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.RED_SEAL,
            ),
            Card(
                Suit.CLUBS, Rank.KING, enhancement=Enhancement.STEEL, seal=Seal.RED_SEAL
            ),
            Card(
                Suit.CLUBS, Rank.KING, enhancement=Enhancement.STEEL, seal=Seal.RED_SEAL
            ),
            Card(
                Suit.CLUBS, Rank.KING, enhancement=Enhancement.STEEL, seal=Seal.RED_SEAL
            ),
            Card(
                Suit.CLUBS, Rank.KING, enhancement=Enhancement.STEEL, seal=Seal.RED_SEAL
            ),
            Card(
                Suit.DIAMONDS,
                Rank.KING,
                enhancement=Enhancement.STEEL,
                seal=Seal.BLUE_SEAL,
            ),
        ]
        b.play_hand([1])

        self.assertEqual(Balatro.format_number(b.round_score), "6.050e38")

    def test_random_4(self) -> None:
        b = Balatro(Deck.RED, stake=Stake.GOLD)
        b.select_blind()
        b.poker_hand_info[PokerHand.THREE_OF_A_KIND][0] = 14
        b._add_joker(
            b._create_joker(
                JokerType.CONSTELLATION, edition=Edition.NEGATIVE, eternal=True
            )
        )
        b.jokers[-1].xmult = 11.9
        b._add_joker(b._create_joker(JokerType.SOCK_AND_BUSKIN, eternal=True))
        b._add_joker(b._create_joker(JokerType.SOCK_AND_BUSKIN, eternal=True))
        b._add_joker(b._create_joker(JokerType.HOLOGRAM, eternal=True))
        b.jokers[-1].xmult = 5.75
        b._add_joker(b._create_joker(JokerType.BRAINSTORM))
        b.hand = [
            Card(Suit.SPADES, Rank.KING, enhancement=Enhancement.LUCKY, debuffed=True),
            Card(Suit.HEARTS, Rank.KING, enhancement=Enhancement.LUCKY),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.GLASS,
                seal=Seal.RED_SEAL,
            ),
            Card(Suit.HEARTS, Rank.KING, enhancement=Enhancement.LUCKY),
            Card(
                Suit.HEARTS,
                Rank.KING,
                enhancement=Enhancement.GLASS,
                seal=Seal.RED_SEAL,
            ),
            Card(Suit.CLUBS, Rank.KING, enhancement=Enhancement.GOLD),
            Card(Suit.CLUBS, Rank.KING),
            Card(
                Suit.DIAMONDS,
                Rank.QUEEN,
                enhancement=Enhancement.GOLD,
                seal=Seal.GOLD_SEAL,
            ),
            Card(Suit.HEARTS, Rank.JACK, enhancement=Enhancement.GOLD),
            Card(Suit.HEARTS, Rank.EIGHT, enhancement=Enhancement.BONUS),
            Card(Suit.HEARTS, Rank.FOUR),
        ]
        b.play_hand([0, 5, 6, 9, 10])

        self.assertEqual(Balatro.format_number(b.round_score), "8,264,713")

    def test_random_5(self) -> None:
        b = Balatro(Deck.RED, stake=Stake.GOLD)
        b.select_blind()
        b.poker_hand_info[PokerHand.FULL_HOUSE][0] = 2
        b._add_joker(b._create_joker(JokerType.BASEBALL))
        b._add_joker(b._create_joker(JokerType.CARD_SHARP))
        b._add_joker(b._create_joker(JokerType.CONSTELLATION, eternal=True))
        b.jokers[-1].xmult = 2.6
        b._add_joker(b._create_joker(JokerType.OOPS, edition=Edition.POLYCHROME))
        b._add_joker(b._create_joker(JokerType.HOLOGRAM))
        b.hand = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.CLUBS, Rank.ACE),
            Card(Suit.CLUBS, Rank.TEN),
            Card(Suit.SPADES, Rank.EIGHT),
            Card(Suit.CLUBS, Rank.EIGHT),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.HEARTS, Rank.FIVE),
            Card(Suit.DIAMONDS, Rank.FIVE),
        ]
        b.play_hand([3, 4, 5, 6, 7])

        self.assertEqual(Balatro.format_number(b.round_score), "11,727")

    def test_random_6(self) -> None:
        b = Balatro(Deck.YELLOW)
        b.select_blind()
        b.poker_hand_info[PokerHand.THREE_OF_A_KIND][0] = 9
        b._add_joker(b._create_joker(JokerType.POPCORN))
        b.jokers[-1].mult = 12
        b._add_joker(b._create_joker(JokerType.THROWBACK))
        b.blinds_skipped = 2
        b.hand = [
            Card(Suit.CLUBS, Rank.EIGHT, enhancement=Enhancement.MULT),
            Card(Suit.CLUBS, Rank.EIGHT, enhancement=Enhancement.MULT),
            Card(Suit.DIAMONDS, Rank.EIGHT, enhancement=Enhancement.GLASS),
        ]
        b.play_hand([0, 1, 2])

        self.assertEqual(Balatro.format_number(b.round_score), "21,186")

    def test_random_7(self) -> None:
        b = Balatro(Deck.YELLOW)
        b.select_blind()
        b.poker_hand_info[PokerHand.HIGH_CARD][0] = 8
        b._add_joker(b._create_joker(JokerType.SHOOT_THE_MOON, edition=Edition.HOLO))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.RAISED_FIST))
        b.hand = [
            Card(Suit.DIAMONDS, Rank.ACE, enhancement=Enhancement.STEEL),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.QUEEN, enhancement=Enhancement.STEEL),
            Card(Suit.SPADES, Rank.NINE),
            Card(
                Suit.SPADES, Rank.SIX, enhancement=Enhancement.GLASS, seal=Seal.RED_SEAL
            ),
            Card(Suit.CLUBS, Rank.SIX),
        ]
        b.play_hand([4])

        self.assertEqual(Balatro.format_number(b.round_score), "6,846")

    def test_random_8(self) -> None:
        b = Balatro(Deck.YELLOW)
        b.select_blind()
        b.poker_hand_info[PokerHand.HIGH_CARD][0] = 8
        b._add_joker(b._create_joker(JokerType.SHOOT_THE_MOON, edition=Edition.HOLO))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.RAISED_FIST))
        b.hand = [
            Card(Suit.DIAMONDS, Rank.ACE, enhancement=Enhancement.STEEL),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.SPADES, Rank.QUEEN, enhancement=Enhancement.STEEL),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.NINE),
            Card(
                Suit.SPADES, Rank.SIX, enhancement=Enhancement.GLASS, seal=Seal.RED_SEAL
            ),
            Card(Suit.CLUBS, Rank.SIX),
        ]
        b.play_hand([4])

        self.assertEqual(Balatro.format_number(b.round_score), "6,300")

    def test_random_9(self) -> None:
        b = Balatro(Deck.YELLOW)
        b.select_blind()
        b.poker_hand_info[PokerHand.HIGH_CARD][0] = 8
        b._add_joker(b._create_joker(JokerType.SHOOT_THE_MOON, edition=Edition.HOLO))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.RAISED_FIST))
        b.hand = [
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.QUEEN, enhancement=Enhancement.STEEL),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.ACE, enhancement=Enhancement.STEEL),
            Card(Suit.SPADES, Rank.NINE),
            Card(
                Suit.SPADES, Rank.SIX, enhancement=Enhancement.GLASS, seal=Seal.RED_SEAL
            ),
            Card(Suit.CLUBS, Rank.SIX),
        ]
        b.play_hand([4])

        self.assertEqual(Balatro.format_number(b.round_score), "10,258")

    def test_random_10(self) -> None:
        b = Balatro(Deck.YELLOW)
        b.select_blind()
        b.poker_hand_info[PokerHand.HIGH_CARD][0] = 8
        b._add_joker(b._create_joker(JokerType.SHOOT_THE_MOON, edition=Edition.HOLO))
        b._add_joker(b._create_joker(JokerType.BARON))
        b._add_joker(b._create_joker(JokerType.RAISED_FIST))
        b.hand = [
            Card(Suit.CLUBS, Rank.SIX),
            Card(
                Suit.SPADES, Rank.SIX, enhancement=Enhancement.GLASS, seal=Seal.RED_SEAL
            ),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.SPADES, Rank.QUEEN, enhancement=Enhancement.STEEL),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.ACE, enhancement=Enhancement.STEEL),
            Card(Suit.SPADES, Rank.NINE),
        ]
        b.play_hand([6])

        self.assertEqual(Balatro.format_number(b.round_score), "16,054")

    def test_random_11(self) -> None:
        b = Balatro(Deck.ERRATIC, stake=Stake.GOLD)
        b.select_blind()
        b.poker_hand_info[PokerHand.FIVE_OF_A_KIND][0] = 3
        b._add_joker(b._create_joker(JokerType.CLEVER))
        b._add_joker(b._create_joker(JokerType.RAISED_FIST))
        b._add_joker(b._create_joker(JokerType.SOCK_AND_BUSKIN, perishable=True))
        b._add_joker(b._create_joker(JokerType.MERRY_ANDY, perishable=True))
        b._add_joker(b._create_joker(JokerType.PHOTOGRAPH, eternal=True))
        b.hand = [
            Card(Suit.SPADES, Rank.KING, enhancement=Enhancement.MULT),
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.CLUBS, Rank.KING),
            Card(Suit.DIAMONDS, Rank.KING),
            Card(Suit.HEARTS, Rank.QUEEN),
            Card(Suit.CLUBS, Rank.QUEEN),
        ]
        b.play_hand([0, 1, 2, 3, 4])

        self.assertEqual(Balatro.format_number(b.round_score), "33,640")

    def test_random_12(self) -> None:
        b = Balatro(Deck.YELLOW, stake=Stake.GOLD)
        b.select_blind()
        b._add_joker(b._create_joker(JokerType.RUNNER, eternal=True))
        b._add_joker(b._create_joker(JokerType.GLUTTENOUS_JOKER, eternal=True))
        b._add_joker(b._create_joker(JokerType.FORTUNE_TELLER, eternal=True))
        b.tarot_cards_used = 7
        b._add_joker(b._create_joker(JokerType.MADNESS))
        b.jokers[-1].xmult = 4.5
        b._add_joker(
            b._create_joker(JokerType.FLOWER_POT, edition=Edition.FOIL, eternal=True)
        )
        b.hand = [
            Card(Suit.SPADES, Rank.ACE),
            Card(Suit.HEARTS, Rank.NINE, enhancement=Enhancement.GLASS),
            Card(Suit.DIAMONDS, Rank.EIGHT),
            Card(Suit.SPADES, Rank.SEVEN),
            Card(Suit.CLUBS, Rank.SEVEN),
            Card(Suit.SPADES, Rank.SIX, enhancement=Enhancement.BONUS),
            Card(Suit.SPADES, Rank.FIVE, enhancement=Enhancement.BONUS),
            Card(Suit.HEARTS, Rank.THREE),
        ]
        b.play_hand([1, 2, 4, 5, 6])

        self.assertEqual(Balatro.format_number(b.round_score), "46,170")

    def test_random_13(self) -> None:
        b = Balatro(Deck.MAGIC)
        b.select_blind()
        b.poker_hand_info[PokerHand.FIVE_OF_A_KIND][0] = 5
        b._add_joker(b._create_joker(JokerType.DUSK))
        b._add_joker(b._create_joker(JokerType.BLUEPRINT))
        b._add_joker(b._create_joker(JokerType.TRIBOULET))
        b._add_joker(b._create_joker(JokerType.FAMILY))
        b._add_joker(b._create_joker(JokerType.PERKEO))
        b.hand = [
            Card(Suit.SPADES, Rank.KING),
            Card(Suit.SPADES, Rank.KING, enhancement=Enhancement.BONUS),
            Card(Suit.HEARTS, Rank.KING, enhancement=Enhancement.STEEL),
            Card(Suit.HEARTS, Rank.KING),
            Card(Suit.HEARTS, Rank.KING, enhancement=Enhancement.STEEL),
            Card(Suit.HEARTS, Rank.KING, enhancement=Enhancement.STEEL),
            Card(Suit.CLUBS, Rank.KING, enhancement=Enhancement.STEEL),
            Card(Suit.DIAMONDS, Rank.QUEEN),
        ]
        b.play_hand([0, 1, 2, 3, 4])

        self.assertEqual(Balatro.format_number(b.round_score), "75,202,560")

    def test_random_14(self) -> None:
        b = Balatro(Deck.CHECKERED)
        b.deck_cards = b.deck_cards[:46]
        b.select_blind()
        b.poker_hand_info[PokerHand.FLUSH][0] = 2
        b.money = -15
        b._add_joker(b._create_joker(JokerType.GREEN_JOKER))
        b.jokers[-1].mult = 22
        b._add_joker(b._create_joker(JokerType.EROSION))
        b._add_joker(b._create_joker(JokerType.VAGABOND))
        b._add_joker(b._create_joker(JokerType.THROWBACK))
        b.blinds_skipped = 1
        b._add_joker(b._create_joker(JokerType.CREDIT_CARD))
        b.hand = [
            Card(Suit.HEARTS, Rank.ACE, debuffed=True),
            Card(Suit.HEARTS, Rank.ACE, enhancement=Enhancement.BONUS, debuffed=True),
            Card(Suit.HEARTS, Rank.KING, debuffed=True),
            Card(Suit.HEARTS, Rank.JACK, debuffed=True),
            Card(Suit.HEARTS, Rank.FOUR, enhancement=Enhancement.WILD, debuffed=True),
        ]
        b.play_hand([0, 1, 2, 3, 4])

        self.assertEqual(Balatro.format_number(b.round_score), "3,312")
        self.assertEqual(len(b.consumables), 1)
        self.assertIsInstance(b.consumables[0].consumable_type, Tarot)


if __name__ == "__main__":
    unittest.main(verbosity=2)
