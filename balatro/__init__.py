from __future__ import annotations
import base64
from collections import Counter
from copy import deepcopy
from dataclasses import replace
import random as r

from .constants import *
from .classes import *
from .enums import *
from .jokers import *

__version__ = "1.0.0"


def format_number(number: float) -> str:
    assert number >= 0
    if number >= 1e11:
        return f"{number:.3e}".replace("+", "")
    if number >= 100 or number.is_integer():
        return f"{number:,.0f}"
    return f"{number:,.1f}" if number >= 10 else f"{number:,.2f}"


class Run:
    def __init__(
        self, deck: Deck, stake: Stake = Stake.WHITE, seed: str | None = None
    ) -> None:
        # TODO: seeding
        r.seed(seed)

        self._deck: Deck = deck
        self._stake: Stake = stake
        self._money: int = 14 if self._deck is Deck.YELLOW else 4
        self._ante: int = 1
        self._round: int = 0

        self._poker_hand_info: dict[PokerHand : list[int, int]] = {
            poker_hand: [1, 0] for poker_hand in PokerHand
        }
        self._vouchers: set[Voucher] = set()
        self._tags: list[Tag] = []

        self._full_deck: list[Card] = [
            (
                self._get_random_card()
                if self._deck is Deck.ERRATIC
                else Card(rank, suit)
            )
            for suit in Suit
            for rank in Rank
        ]

        self._jokers: list[BaseJoker] = []
        self._consumables: list[Consumable] = []

        match self._deck:
            case Deck.MAGIC:
                self._vouchers.add(Voucher.CRYSTAL_BALL)
                self._consumables.extend(
                    [Consumable(Tarot.THE_FOOL), Consumable(Tarot.THE_FOOL)]
                )
            case Deck.NEBULA:
                self._vouchers.add(Voucher.TELESCOPE)
            case Deck.GHOST:
                self._consumables.append(Consumable(Spectral.HEX))
            case Deck.ABANDONED:
                self._full_deck = [
                    card for card in self._full_deck if not self._is_face_card(card)
                ]
            case Deck.CHECKERED:
                self._full_deck = self._full_deck[:26] + deepcopy(self._full_deck[:26])
            case Deck.ZODIAC:
                self._vouchers.update(
                    [
                        Voucher.TAROT_MERCHANT,
                        Voucher.PLANET_MERCHANT,
                        Voucher.OVERSTOCK,
                    ]
                )

        self._played_hands: int = 0
        self._first_hand: bool | None = None
        self._first_discard: bool | None = None
        self._round_poker_hands: set[PokerHand] | None = None
        self._unused_discards: int = 0
        self._blinds_skipped: int = 0

        self._round_score: int | None = None
        self._round_goal: int | None = None
        self._chips: int | None = None
        self._mult: float | None = None
        self._hands: int | None = None
        self._discards: int | None = None
        self._hand_size: int | None = None
        self._hand: list[Card] | None = None
        self._deck_cards_left: list[Card] | None = None

        self._reroll_cost: int | None = None
        self._used_chaos: bool | None = None
        self._shop_cards: list[tuple[BaseJoker | Consumable | Card, int]] | None = None
        self._shop_vouchers: list[tuple[Voucher, int]] | None = None
        self._shop_packs: list[tuple[Pack, int]] | None = None
        self._planet_cards_used: set[Planet] = set()
        self._final_blinds_defeated: set[Blind] = set()
        self._finisher_blinds_defeated: set[Blind] = set()
        self._num_tarot_cards_used: int = 0
        self._fool_next: Tarot | Planet | None = None
        self._hand_size_penalty: int = 0
        self._num_ectoplasms_used: int = 0
        self._gros_michel_extinct: bool = False

        self._new_ante()

        self._state: State = State.SELECTING_BLIND

    def _repr_html_(self) -> str:
        match self._state:
            case State.IN_SHOP:
                return self._shop_display_str()
            case _:
                raise NotImplementedError

    def _add_card(self, card: Card) -> None:
        self._full_deck.append(card)
        for joker in self._jokers:
            joker._on_card_added(card)

    def _add_joker(self, joker: BaseJoker) -> None:
        self._jokers.append(joker)
        for other_joker in self._jokers:
            other_joker._on_jokers_moved()

    def _buy_shop_item(
        self, section_index: int, item_index: int
    ) -> tuple[BaseJoker | Consumable | Card | Pack | Voucher, int]:
        assert self._state is State.IN_SHOP

        assert section_index in [0, 1, 2]

        section_items = [self._shop_cards, self._shop_vouchers, self._shop_packs][
            section_index
        ]

        assert 0 <= item_index < len(section_items)

        item, cost = section_items[item_index]

        assert self._available_money >= cost

        match item:
            case BaseJoker():
                assert len(self._jokers) < self.joker_slots
            case Consumable():
                assert len(self._consumables) < self.consumable_slots

        self._money -= cost
        return section_items.pop(item_index)

    def _calculate_buy_cost(
        self, item: BaseJoker | Consumable | Card | Voucher | Pack, coupon: bool = False
    ) -> int:
        if coupon and not isinstance(item, Voucher):
            return 0

        edition_cost = 0
        discount_percent = (
            0.5
            if Voucher.LIQUIDATION in self._vouchers
            else 0.75 if Voucher.CLEARANCE_SALE in self._vouchers else 1.0
        )

        match item:
            case BaseJoker():
                base_cost = JOKER_BASE_COSTS[item.joker_type]
                edition_cost = EDITION_COSTS[item.edition]
            case Consumable():
                match item.card:
                    case Tarot():
                        base_cost = 3
                    case Planet():
                        if JokerType.ASTRONOMER in self._active_jokers:
                            return 0
                        base_cost = 3
                    case Spectral():
                        base_cost = 4
                edition_cost = EDITION_COSTS[
                    Edition.NEGATIVE if item.is_negative else Edition.BASE
                ]
            case Card():
                base_cost = 1
                edition_cost = EDITION_COSTS[item.edition]
            case Voucher():
                base_cost = 10
                discount_percent = 1.0
            case Pack():
                if (
                    item.name.endswith("CELESTIAL")
                    and JokerType.ASTRONOMER in self._active_jokers
                ):
                    return 0
                if item.name.startswith("MEGA"):
                    base_cost = 8
                elif item.name.startswith("JUMBO"):
                    base_cost = 6
                else:
                    base_cost = 4

        buy_cost = (base_cost + edition_cost) * discount_percent
        return max(round(buy_cost - 0.001), 1)

    def _calculate_sell_value(self, item: Sellable) -> int:
        return max(1, self._calculate_buy_cost(item) // 2) + item.extra_sell_value

    def _chance(self, hit: int, pool: int) -> bool:
        hit *= 2 ** self._active_jokers.count(JokerType.OOPS_ALL_SIXES)
        return hit >= pool or (r.randint(1, pool) <= hit)

    def _create_joker(
        self,
        joker_type: JokerType,
        edition: Edition = Edition.BASE,
        eternal: bool = False,
        perishable: bool = False,
        rental: bool = False,
    ) -> BaseJoker:
        joker = JOKER_CLASSES[joker_type](
            edition=edition,
            eternal=eternal,
            perishable=perishable,
            rental=rental,
        )
        joker._run = self
        joker._on_created()
        return joker

    def _deal(self) -> None:
        num_cards = min(len(self._deck_cards_left), self._hand_size - len(self._hand))
        if num_cards <= 0:
            return
        deal_indices = sorted(
            r.sample(range(len(self._deck_cards_left)), num_cards), reverse=True
        )
        for i in deal_indices:
            self._hand.append(self._deck_cards_left.pop(i))

        self._sort_hand()

    def _destroy_card(self, card: Card) -> None:
        try:
            self._full_deck.remove(card)
        except ValueError:
            pass
        for joker in self._jokers:
            joker._on_card_destroyed(card)

    def _destroy_joker(self, joker: BaseJoker) -> None:
        if joker.eternal:
            return
        try:
            i = self._jokers.index(joker)
            self._jokers.pop(i)
            for other_joker in self._jokers:
                other_joker._on_jokers_moved()
        except ValueError:
            pass

    def _end_round(
        self, last_poker_hand_played: PokerHand, saved: bool = False
    ) -> None:
        for held_card in self._hand:
            self._trigger_held_card_round_end(held_card, last_poker_hand_played)

            match held_card:
                case Seal.RED:
                    self._trigger_held_card_round_end(held_card, last_poker_hand_played)

            for joker in self._jokers:
                for _ in range(joker._on_card_held_retriggers(held_card)):
                    self._trigger_held_card_round_end(held_card, last_poker_hand_played)

        for deck_card in self._full_deck:
            deck_card.debuffed = False

        interest_amt = (
            0
            if self._deck is Deck.GREEN
            else (1 + self._active_jokers.count(JokerType.TO_THE_MOON))
        )
        interest = min(
            (
                20
                if Voucher.MONEY_TREE in self._vouchers
                else 10 if Voucher.SEED_MONEY in self._vouchers else 5
            )
            * interest_amt,
            (max(0, self._money) // 5 * interest_amt),
        )

        for joker in self._jokers:
            joker._on_round_ended()

        cash_out = (
            (0 if saved else BLIND_INFO[self._blind][2])
            + (2 if self._deck is Deck.GREEN else 1) * self._hands
            + (1 if self._deck is Deck.GREEN else 0) * self._discards
            + interest
        )
        self._money += cash_out

        self._round_score = None
        self._round_goal = None
        self._hands = None
        self._unused_discards += self._discards
        self._discards = None
        self._hand_size = None
        self._hand = None
        self._deck_cards_left = None
        self._chips = None
        self._mult = None
        self._first_hand = None
        self._first_discard = None
        self._round_poker_hands = None

        self._next_blind()

        self._populate_shop()
        self._state = State.IN_SHOP

    def _get_card_suits(self, card: Card, force_base_suit: bool = False) -> list[Suit]:
        if (card.debuffed and not force_base_suit) or card.is_stone_card:
            return []
        if card == Enhancement.WILD:
            return list(Suit)
        if JokerType.SMEARED_JOKER in self._active_jokers:
            red_suits, black_suits = [Suit.HEARTS, Suit.DIAMONDS], [
                Suit.SPADES,
                Suit.CLUBS,
            ]
            return red_suits if card.suit in red_suits else black_suits
        return [card.suit]

    def _get_poker_hands(self, played_cards: list[Card]) -> dict[PokerHand, set[int]]:
        poker_hands = {}

        flush_straight_len = 4 if (JokerType.FOUR_FINGERS in self._active_jokers) else 5
        max_straight_gap = 2 if (JokerType.SHORTCUT in self._active_jokers) else 1

        suit_counts = Counter()
        for played_card in played_cards:
            suit_counts.update(self._get_card_suits(played_card, force_base_suit=True))

        # flush check
        flush_suit, flush_suit_count = (
            suit_counts.most_common(1)[0] if suit_counts else (None, 0)
        )
        if flush_suit_count >= flush_straight_len:  # flush
            poker_hands[PokerHand.FLUSH] = [
                i
                for i, card in enumerate(played_cards)
                if flush_suit in self._get_card_suits(card, force_base_suit=True)
            ]

        rank_counts = Counter(
            played_card.rank
            for played_card in played_cards
            if not played_card.is_stone_card
        )

        # straight check
        if len(rank_counts) >= flush_straight_len:
            sorted_ranks = sorted(rank_counts)

            longest_straight = set()
            cur_straight = set()
            for i in range(len(sorted_ranks)):
                cur_straight.add(sorted_ranks[i])
                if len(cur_straight) > len(longest_straight):
                    longest_straight = cur_straight
                if (
                    i < len(sorted_ranks) - 1
                    and int(sorted_ranks[i + 1]) - int(sorted_ranks[i])
                    > max_straight_gap
                ):
                    cur_straight = set()

            if (
                int(min(longest_straight)) <= max_straight_gap + 1
                and Rank.ACE in rank_counts
            ):
                longest_straight.add(Rank.ACE)

            if len(longest_straight) >= flush_straight_len:  # straight
                straight = list(longest_straight)
                straight_indices = [
                    i for i, card in enumerate(played_cards) if card in straight
                ]
                if PokerHand.FLUSH in poker_hands:  # straight flush
                    poker_hands[PokerHand.STRAIGHT_FLUSH] = straight_indices
                poker_hands[PokerHand.STRAIGHT] = straight_indices

        # rank-matching checks
        for rank, n in rank_counts.most_common():
            if n == 5:  # 5oak
                poker_hands[PokerHand.FIVE_OF_A_KIND] = [0, 1, 2, 3, 4]
                if PokerHand.FLUSH in poker_hands:  # flush five
                    poker_hands[PokerHand.FLUSH_FIVE] = [0, 1, 2, 3, 4]
            if n >= 4:  # 4oak
                poker_hands[PokerHand.FOUR_OF_A_KIND] = [
                    i for i, card in enumerate(played_cards) if card.rank is rank
                ][:4]
            if n >= 3:  # 3oak
                poker_hands[PokerHand.THREE_OF_A_KIND] = [
                    i for i, card in enumerate(played_cards) if card.rank is rank
                ][:3]
            if n >= 2:  # pair
                if (
                    PokerHand.THREE_OF_A_KIND in poker_hands
                    and played_cards[poker_hands[PokerHand.THREE_OF_A_KIND][0]].rank
                    is not rank
                ):  # full house
                    poker_hands[PokerHand.FULL_HOUSE] = [0, 1, 2, 3, 4]
                    if PokerHand.FLUSH in poker_hands:  # flush house
                        poker_hands[PokerHand.FLUSH_HOUSE] = [0, 1, 2, 3, 4]
                if (
                    PokerHand.PAIR in poker_hands
                    and played_cards[poker_hands[PokerHand.PAIR][0]] != rank
                ):  # two pair
                    poker_hands[PokerHand.TWO_PAIR] = (
                        poker_hands[PokerHand.PAIR]
                        + [
                            i
                            for i, card in enumerate(played_cards)
                            if card.rank is rank
                        ][:2]
                    )
                poker_hands[PokerHand.PAIR] = [
                    i for i, card in enumerate(played_cards) if card.rank is rank
                ][:2]

        # high card
        if not rank_counts:
            # (all stone cards - default to high card)
            poker_hands[PokerHand.HIGH_CARD] = []
        else:
            poker_hands[PokerHand.HIGH_CARD] = [
                i
                for i, card in enumerate(played_cards)
                if card.rank is max(rank_counts)
            ][:1]

        return poker_hands

    def _get_random_card(
        self, allow_modifiers: bool = False, restricted_ranks: list[Rank] | None = None
    ) -> Card:
        ranks = restricted_ranks if restricted_ranks is not None else list(Rank)
        card = Card(r.choice(ranks), r.choice(list(Suit)))

        if allow_modifiers:
            raise NotImplementedError

        return card

    def _get_random_consumable(self, consumable_type: type) -> Consumable:
        match consumable_type.__name__:
            case Tarot.__name__:
                card_pool = list(Tarot)
            case Planet.__name__:
                card_pool = [
                    unlocked_poker_hand.planet
                    for unlocked_poker_hand in self._unlocked_poker_hands
                ]
            case Spectral.__name__:
                card_pool = list(Spectral)[:-2]
        shop_cards = (
            [
                shop_card[0].card
                for shop_card in self._shop_cards
                if isinstance(shop_card, tuple) and isinstance(shop_card[0], Consumable)
            ]
            if self._state is State.IN_SHOP
            else []
        )
        card = None
        while card is None or (
            JokerType.SHOWMAN not in self._active_jokers
            and (card in self._consumables or card in shop_cards)
        ):
            card = r.choice(card_pool)

        return Consumable(card)

    def _get_random_joker(
        self,
        rarity: Rarity | None = None,
        stickers: bool = False,
    ) -> BaseJoker:
        if rarity is None:
            rarity = r.choices(
                list(JOKER_BASE_RARITY_WEIGHTS),
                weights=JOKER_BASE_RARITY_WEIGHTS.values(),
                k=1,
            )[0]

        shop_joker_types = (
            [
                shop_card[0].joker_type
                for shop_card in self._shop_cards
                if isinstance(shop_card, tuple) and isinstance(shop_card[0], BaseJoker)
            ]
            if self._state is State.IN_SHOP
            else []
        )

        joker_type = None
        while (
            joker_type is None
            or (
                JokerType.SHOWMAN not in self._active_jokers
                and (joker_type in self._jokers or joker_type in shop_joker_types)
            )
            or (joker_type is JokerType.CAVENDISH and not self._gros_michel_extinct)
            or (
                joker_type is JokerType.GOLDEN_TICKET
                and not any(
                    card.enhancement is Enhancement.GOLD for card in self._full_deck
                )
            )
            or (
                joker_type is JokerType.STEEL_JOKER
                and not any(
                    card.enhancement is Enhancement.STEEL for card in self._full_deck
                )
            )
            or (
                joker_type is JokerType.STONE
                and not any(
                    card.enhancement is Enhancement.STONE for card in self._full_deck
                )
            )
            or (
                joker_type is JokerType.LUCKY_CAT
                and not any(
                    card.enhancement is Enhancement.LUCKY for card in self._full_deck
                )
            )
            or (
                joker_type is JokerType.GLASS_JOKER
                and not any(
                    card.enhancement is Enhancement.GLASS for card in self._full_deck
                )
            )
        ):
            joker_type = r.choice(JOKER_TYPE_RARITIES[rarity])

        edition_chances = (
            JOKER_BASE_EDITION_CHANCES_GLOW_UP
            if Voucher.GLOW_UP in self._vouchers
            else (
                JOKER_BASE_EDITION_CHANCES_HONE
                if Voucher.HONE in self._vouchers
                else JOKER_BASE_EDITION_CHANCES
            )
        )
        edition = r.choices(
            list(edition_chances), weights=edition_chances.values(), k=1
        )[0]

        if self._stake is not Stake.WHITE and stickers:
            raise NotImplementedError

        return self._create_joker(joker_type, edition=edition)

    def _is_face_card(self, card: Card) -> bool:
        return (
            card
            in [
                Rank.KING,
                Rank.QUEEN,
                Rank.JACK,
            ]
            or JokerType.PAREIDOLIA in self._active_jokers
        )

    def _lucky_check(self) -> bool:
        triggered = False
        if self._chance(1, 5):
            self._mult += 20
            triggered = True
        if self._chance(1, 15):
            self._money += 20
            triggered = True
        return triggered

    def _new_ante(self) -> None:
        self._ante_tags: list[
            tuple[Tag, PokerHand | None], tuple[Tag, PokerHand | None]
        ] = [None, None]
        for i in range(2):
            while (
                self._ante_tags[i] is None
                or self._ante == 1
                and self._ante_tags[i][0] in PROHIBITED_ANTE_1_TAGS
            ):
                tag = r.choice(list(Tag))
                extra = None

                if tag is Tag.ORBITAL:
                    extra = r.choice(self._unlocked_poker_hands)

                self._ante_tags[i] = (tag, extra)

        self._random_final_blind()

        self._blind: Blind = Blind.SMALL_BLIND

    def _next_blind(self) -> None:
        match self._blind:
            case Blind.SMALL_BLIND:
                self._blind = Blind.BIG_BLIND
            case Blind.BIG_BLIND:
                self._blind = self._final_blind
            case _:
                if self._is_finisher_ante:
                    self._finisher_blinds_defeated.add(self._blind)
                    if len(self._finisher_blinds_defeated) == 5:
                        self._finisher_blinds_defeated.clear()
                else:
                    self._final_blinds_defeated.add(self._blind)
                    if len(self._final_blinds_defeated) == 23:
                        self._final_blinds_defeated.clear()
                self._new_ante()

    def _open_pack(self, pack: Pack) -> None:
        if pack.name.startswith("MEGA"):
            choose = [2, 5]
        elif pack.name.startswith("JUMBO"):
            choose = [1, 5]
        else:
            choose = [1, 3]

        match pack:
            case Pack.BUFFOON | Pack.JUMBO_BUFFOON | Pack.MEGA_BUFFOON:
                choose[1] -= 1
                raise NotImplementedError
            case Pack.ARCANA | Pack.JUMBO_ARCANA | Pack.MEGA_ARCANA:
                raise NotImplementedError
            case Pack.CELESTIAL | Pack.JUMBO_CELESTIAL | Pack.MEGA_CELESTIAL:
                raise NotImplementedError
            case Pack.SPECTRAL | Pack.JUMBO_SPECTRAL | Pack.MEGA_SPECTRAL:
                choose[1] -= 1
                raise NotImplementedError
            case Pack.STANDARD | Pack.JUMBO_STANDARD | Pack.MEGA_STANDARD:
                raise NotImplementedError

    def _populate_shop(self) -> None:
        coupon = False
        if Tag.COUPON in self._tags:
            coupon = True
            self._tags.remove(Tag.COUPON)

        self._reroll_cost = (
            1
            if Voucher.REROLL_GLUT in self._vouchers
            else 3 if Voucher.REROLL_SURPLUS in self._vouchers else 5
        )
        if Tag.DSIX in self._tags:
            self._tags.remove(Tag.DSIX)
            self._reroll_cost = 0

        self._used_chaos = False

        self._populate_shop_cards(coupon=coupon)

        needed_vouchers = 0
        if self._shop_vouchers is None:
            self._shop_vouchers = []
            needed_vouchers = 1
        while Tag.VOUCHER in self._tags:
            self._tags.remove(Tag.VOUCHER)
            needed_vouchers += 1

        if needed_vouchers > 0:
            voucher_list = list(Voucher)
            possible_vouchers = []
            for base_voucher, upgraded_voucher in zip(
                voucher_list[:10], voucher_list[10:]
            ):
                if upgraded_voucher in self._vouchers:
                    continue
                possible_voucher = (
                    upgraded_voucher if base_voucher in self._vouchers else base_voucher
                )
                if possible_voucher in self._shop_vouchers:
                    continue
                possible_vouchers.append(possible_voucher)

            for _ in range(needed_vouchers):
                voucher = r.choice(possible_vouchers)
                buy_cost = self._calculate_buy_cost(voucher, coupon=coupon)
                self._shop_vouchers.append((voucher, buy_cost))
                possible_vouchers.remove(voucher)

        self._shop_packs = r.choices(
            list(SHOP_BASE_PACK_WEIGHTS),
            weights=SHOP_BASE_PACK_WEIGHTS.values(),
            k=2,
        )
        if self._round == 1:
            self._shop_packs[0] = Pack.BUFFOON
        for i, pack in enumerate(self._shop_packs):
            buy_cost = self._calculate_buy_cost(pack, coupon=coupon)
            self._shop_packs[i] = (pack, buy_cost)

    def _populate_shop_cards(self, coupon: bool = False) -> None:
        shop_card_weights = SHOP_BASE_CARD_WEIGHTS.copy()
        if Voucher.MAGIC_TRICK in self._vouchers:
            shop_card_weights[Card] = 4
        if Voucher.TAROT_TYCOON in self._vouchers:
            shop_card_weights[Tarot] = 32
        elif Voucher.TAROT_MERCHANT in self._vouchers:
            shop_card_weights[Tarot] = 9.6
        if Voucher.PLANET_TYCOON in self._vouchers:
            shop_card_weights[Planet] = 32
        elif Voucher.PLANET_MERCHANT in self._vouchers:
            shop_card_weights[Planet] = 9.6
        if self._deck is Deck.GHOST:
            shop_card_weights[Spectral] = 2

        self._shop_cards = r.choices(
            list(shop_card_weights),
            weights=shop_card_weights.values(),
            k=(
                4
                if Voucher.OVERSTOCK_PLUS in self._vouchers
                else 3 if Voucher.OVERSTOCK in self._vouchers else 2
            ),
        )
        joker_tags_used = 0
        for tag in self._tags:
            if tag is Tag.UNCOMMON or tag is Tag.RARE:
                self._shop_cards[joker_tags_used] = BaseJoker
                joker_tags_used += 1
                if joker_tags_used == 2:
                    break

        for i in range(len(self._shop_cards)):
            match self._shop_cards[i].__name__:
                case BaseJoker.__name__:
                    buy_cost = None

                    rarity = None
                    for tag in self._tags[:]:
                        if tag is Tag.UNCOMMON or tag is Tag.RARE:
                            self._tags.remove(tag)
                            rarity = Rarity[tag.name]
                            buy_cost = 0
                            break

                    joker = self._get_random_joker(
                        rarity=rarity,
                        stickers=True,
                    )

                    if joker.edition is Edition.BASE:
                        for tag in self._tags[:]:
                            if tag.name in Edition._member_map_:
                                self._tags.remove(tag)
                                joker.edition = Edition[tag.name]
                                buy_cost = 0
                                break

                    if buy_cost is None:
                        buy_cost = self._calculate_buy_cost(joker, coupon=coupon)
                    self._shop_cards[i] = (joker, buy_cost)
                case Tarot.__name__ | Planet.__name__ | Spectral.__name__:
                    consumable = self._get_random_consumable(self._shop_cards[i])
                    buy_cost = self._calculate_buy_cost(consumable, coupon=coupon)
                    self._shop_cards[i] = (consumable, buy_cost)
                case Card.__name__:
                    card = self._get_random_card(
                        allow_modifiers=(Voucher.ILLUSION in self._vouchers)
                    )
                    buy_cost = self._calculate_buy_cost(card, coupon=coupon)
                    self._shop_cards[i] = (card, buy_cost)

    def _random_final_blind(self) -> None:
        self._final_blind: Blind = None
        if self._is_finisher_ante:
            while (
                self._final_blind is None
                or self._final_blind in self._finisher_blinds_defeated
            ):
                self._final_blind = r.choice(list(BLIND_INFO)[-5:])
        else:
            while (
                self._final_blind is None
                or BLIND_INFO[self._final_blind][0] > self._ante
                or self._final_blind in self._final_blinds_defeated
            ):
                self._final_blind = r.choice(list(BLIND_INFO)[2:-5])

    def _shop_display_str(self) -> str:
        with open("resources/fonts/m6x11plus.ttf", "rb") as f:
            font_base64 = base64.b64encode(f.read()).decode("utf-8")

        reroll_cost = self.reroll_cost
        can_reroll = self._available_money >= reroll_cost

        html = f"""
        <style>
        @font-face {{
            font-family: 'm6x11plus';
            src: url(data:font/ttf;base64,{font_base64});
        }}
        * {{
            font-family: 'm6x11plus', monospace;
        }}
        </style>
        <div style='display: flex; flex-direction: column; width: 800px; background-color: #1d2829; border-radius: 20px;'>
            <div style='display: flex;'>
                <div style='width: 25%; padding: 10px; display: flex; flex-direction: column; justify-content: center; align-items: center;'>
                    <div style='text-align: center; margin-bottom: 10px; width: 100%; height: 50%;'>
                        <button style='background-color: #e35646; color: white; padding: 10px 10px; width: 100%; height: 100%; border-radius: 20px; font-size: 28px;'>Next<br/>Round</button>
                    </div>
                    <div style='text-align: center; width: 100%; height: 50%;'>
                        <button style='background-color: {'#5cb284' if can_reroll else '#4f4f4f'}; color: {'white' if can_reroll else '#646464'}; padding: 10px 10px; width: 100%; height: 100%; border-radius: 20px; font-size: 28px;'>Reroll<br><span style='font-size: 56px;'>${reroll_cost}</span></button>
                    </div>
                </div>
                <div style='width: 75%; background-color: #3a4b50; border-radius: 20px; padding: 10px; margin: 10px;'>
                    <div style='display: flex; flex-wrap: wrap; justify-content: center;'>
        """
        for item, cost in self._shop_cards:
            png_bytes = item._repr_png_()
            png_base64 = base64.b64encode(png_bytes).decode("utf-8")
            item_html = f"<img src='data:image/png;base64,{png_base64}'/>"

            html += f"""
                    <div style='display: flex; flex-direction: column; align-items: center; margin-right: 10px; padding-bottom: 20px; text-align: center;'>
                        <div style='width: 50px; background-color: #333b3d; border-radius: 25%; border: 3px solid black'><strong style='color: #d7af54; font-size:28px;'>${cost}</strong></div>
                        <div style='text-align: center;'>{item_html}</div>
                    </div>
            """
        html += """
                    </div>
                </div>
            </div>
            <div style='display: flex;'>
                <div style='width: 50%; border: 10px solid #3a4b50; border-radius: 20px; padding: 10px; margin: 10px;'>
                    <div style='display: flex; flex-wrap: wrap; justify-content: center;'>
        """
        for voucher, cost in self._shop_vouchers:
            png_bytes = voucher._repr_png_()
            png_base64 = base64.b64encode(png_bytes).decode("utf-8")
            voucher_html = f"<img src='data:image/png;base64,{png_base64}'/>"

            html += f"""
                        <div style='display: flex; flex-direction: column; align-items: center; margin-right: 10px; padding-bottom: 20px; text-align: center;'>
                            <div style='width: 50px; background-color: #333b3d; border-radius: 25%; border: 3px solid black'><strong style='color: #d7af54; font-size:28px;'>${cost}</strong></div>
                            <div style='text-align: center;'>{voucher_html}</div>
                        </div>
            """
        html += """
                    </div>
                </div>
                <div style='width: 50%; background-color: #3a4b50; border-radius: 20px; padding: 10px; margin: 10px;'>
                    <div style='display: flex; flex-wrap: wrap; justify-content: center;'>
        """
        for pack, cost in self._shop_packs:
            png_bytes = pack._repr_png_()
            png_base64 = base64.b64encode(png_bytes).decode("utf-8")
            pack_html = f"<img src='data:image/png;base64,{png_base64}' style='height: 220px;'/>"

            html += f"""
                        <div style='display: flex; flex-direction: column; align-items: center; margin-right: 10px; padding-bottom: 20px; text-align: center;'>
                            <div style='width: 50px; background-color: #333b3d; border-radius: 25%; border: 3px solid black'><strong style='color: #d7af54; font-size:28px;'>${cost}</strong></div>
                            <div style='text-align: center;'>{pack_html}</div>
                        </div>
            """
        html += """
                    </div>
                </div>
            </div>
        </div>
        """

        return html

    def _sort_hand(self, by_suit: bool = False) -> None:
        if by_suit:
            self._hand.sort(
                key=lambda card: (
                    card.is_stone_card,
                    list(Suit).index(card.suit),
                    list(Rank).index(card.rank),
                )
            )
        else:
            self._hand.sort(
                key=lambda card: (
                    card.is_stone_card,
                    list(Rank).index(card.rank),
                    list(Suit).index(card.suit),
                )
            )

    def _trigger_scored_card(
        self,
        scored_card: Card,
        played_cards: list[Card],
        scored_card_indices: list[int],
        poker_hands_played: list[PokerHand],
    ) -> None:
        self._chips += scored_card.chips

        match scored_card:
            case Enhancement.BONUS:
                self._chips += 30
            case Enhancement.MULT:
                self._mult += 4
            case Enhancement.GLASS:
                self._mult *= 2
            case Enhancement.LUCKY:
                if self._lucky_check():
                    for joker in self._jokers:
                        joker._on_lucky_card_triggered()

        match scored_card:
            case Seal.GOLD:
                self._money += 3

        match scored_card:
            case Edition.FOIL:
                self._chips += 50
            case Edition.HOLO:
                self._mult += 10
            case Edition.POLYCHROME:
                self._mult *= 1.5

        for joker in self._jokers:
            joker._on_card_scored(
                scored_card, played_cards, scored_card_indices, poker_hands_played
            )

    def _trigger_held_card(self, held_card: Card) -> None:
        match held_card:
            case Enhancement.STEEL:
                self._mult *= 1.5

        for joker in self._jokers:
            joker._on_card_held(held_card)

    def _trigger_held_card_round_end(
        self, held_card: Card, last_poker_hand_played: PokerHand
    ) -> None:
        match held_card:
            case Enhancement.GOLD:
                self._money += 3

        match held_card:
            case Seal.BLUE:
                if self.consumable_slots > len(self._consumables):
                    self._consumables.append(Consumable(last_poker_hand_played.planet))

    def _use_consumable(
        self, consumable: Consumable, selected_cards: list[Card]
    ) -> None:
        match consumable.card:
            case Tarot():
                match consumable.card:
                    case Tarot.THE_FOOL:
                        assert (
                            self._fool_next is not None
                            and self._fool_next is not Tarot.THE_FOOL
                        )

                        self._consumables.append(Consumable(self._fool_next))
                    case Tarot.THE_MAGICIAN:
                        assert 1 <= len(selected_cards) <= 2

                        for card in selected_cards:
                            card.enhancement = Enhancement.LUCKY
                    case Tarot.THE_HIGH_PRIESTESS:
                        for _ in range(
                            min(
                                2,
                                self.consumable_slots - len(self._consumables) + 1,
                            )
                        ):
                            self._consumables.append(
                                self._get_random_consumable(Planet)
                            )
                    case Tarot.THE_EMPRESS:
                        assert 1 <= len(selected_cards) <= 2

                        for card in selected_cards:
                            card.enhancement = Enhancement.MULT
                    case Tarot.THE_EMPEROR:
                        for _ in range(
                            min(
                                2,
                                self.consumable_slots - len(self._consumables) + 1,
                            )
                        ):
                            self._consumables.append(self._get_random_consumable(Tarot))
                    case Tarot.THE_HEIROPHANT:
                        assert 1 <= len(selected_cards) <= 2

                        for card in selected_cards:
                            card.enhancement = Enhancement.BONUS
                    case Tarot.THE_LOVERS:
                        assert len(selected_cards) == 1

                        selected_cards[0].enhancement = Enhancement.WILD
                    case Tarot.THE_CHARIOT:
                        assert len(selected_cards) == 1

                        selected_cards[0].enhancement = Enhancement.STEEL
                    case Tarot.JUSTICE:
                        assert len(selected_cards) == 1

                        selected_cards[0].enhancement = Enhancement.GLASS
                    case Tarot.THE_HERMIT:
                        self._money += max(0, min(20, self._money))
                    case Tarot.THE_WHEEL_OF_FORTUNE:
                        assert self._jokers

                        valid_jokers = [
                            joker
                            for joker in self._jokers
                            if joker.edition is Edition.BASE
                        ]

                        assert valid_jokers

                        if self._chance(1, 4):
                            r.choice(valid_jokers).edition = r.choices(
                                list(UPGRADED_EDITION_WEIGHTS),
                                weights=UPGRADED_EDITION_WEIGHTS.values(),
                                k=1,
                            )[0]
                    case Tarot.STRENGTH:
                        assert 1 <= len(selected_cards) <= 2

                        ranks = list(Rank)
                        for card in selected_cards:
                            card.rank = ranks[(ranks.index(card.rank) - 1) % 13]
                    case Tarot.THE_HANGED_MAN:
                        assert 1 <= len(selected_cards) <= 2

                        for card in selected_cards:
                            self._destroy_card(card)
                    case Tarot.DEATH:
                        assert len(selected_cards) == 2

                        left, right = selected_cards
                        left.suit = right.suit
                        left.rank = right.rank
                        left.enhancement = right.enhancement
                        left.seal = right.seal
                        left.edition = right.edition
                    case Tarot.TEMPERANCE:
                        assert self._jokers

                        self._money += min(
                            50,
                            sum(
                                self._calculate_sell_value(joker)
                                for joker in self._jokers
                            ),
                        )
                    case Tarot.THE_DEVIL:
                        assert len(selected_cards) == 1

                        selected_cards[0].enhancement = Enhancement.GOLD
                    case Tarot.THE_TOWER:
                        assert len(selected_cards) == 1

                        selected_cards[0].enhancement = Enhancement.STONE
                    case Tarot.THE_STAR:
                        assert 1 <= len(selected_cards) <= 3

                        for card in selected_cards:
                            card.suit = Suit.DIAMONDS
                    case Tarot.THE_MOON:
                        assert 1 <= len(selected_cards) <= 3

                        for card in selected_cards:
                            card.suit = Suit.CLUBS
                    case Tarot.THE_SUN:
                        assert 1 <= len(selected_cards) <= 3

                        for card in selected_cards:
                            card.suit = Suit.HEARTS
                    case Tarot.JUDGEMENT:
                        assert len(self._jokers) < self.joker_slots

                        self._add_joker(self._get_random_joker())
                    case Tarot.THE_WORLD:
                        assert 1 <= len(selected_cards) <= 3

                        for card in selected_cards:
                            card.suit = Suit.SPADES

                self._num_tarot_cards_used += 1
                self._fool_next = consumable.card
            case Planet():
                self._poker_hand_info[consumable.card.poker_hand][0] += 1

                for joker in self._jokers:
                    joker._on_planet_used()

                self._fool_next = consumable.card
            case Spectral():
                match consumable.card:
                    case Spectral.FAMILIAR:
                        assert self._hand is not None
                        assert len(self._hand) > 1

                        self._destroy_card(r.choice(self._hand))
                        for _ in range(3):
                            random_face_card = self._get_random_card(
                                restricted_ranks=[Rank.KING, Rank.QUEEN, Rank.JACK]
                            )
                            random_face_card.enhancement = r.choice(list(Enhancement))
                            self._add_card(random_face_card)
                            self._hand.append(random_face_card)
                    case Spectral.GRIM:
                        assert self._hand is not None
                        assert len(self._hand) > 1

                        self._destroy_card(r.choice(self._hand))
                        for _ in range(2):
                            random_ace = self._get_random_card(
                                restricted_ranks=[Rank.ACE]
                            )
                            random_ace.enhancement = r.choice(list(Enhancement))
                            self._add_card(random_ace)
                            self._hand.append(random_ace)
                    case Spectral.INCANTATION:
                        assert self._hand is not None
                        assert len(self._hand) > 1

                        self._destroy_card(r.choice(self._hand))
                        for _ in range(4):
                            random_numbered_card = self._get_random_card(
                                restricted_ranks=[
                                    Rank.TEN,
                                    Rank.NINE,
                                    Rank.EIGHT,
                                    Rank.SEVEN,
                                    Rank.SIX,
                                    Rank.FIVE,
                                    Rank.FOUR,
                                    Rank.THREE,
                                    Rank.TWO,
                                ]
                            )
                            random_numbered_card.enhancement = r.choice(
                                list(Enhancement)
                            )
                            self._add_card(random_numbered_card)
                            self._hand.append(random_numbered_card)
                    case Spectral.TALISMAN:
                        assert len(selected_cards) == 1

                        selected_cards[0].seal = Seal.GOLD
                    case Spectral.AURA:
                        assert len(selected_cards) == 1

                        selected_cards[0].edition = r.choices(
                            list(UPGRADED_EDITION_WEIGHTS),
                            weights=UPGRADED_EDITION_WEIGHTS.values(),
                            k=1,
                        )[0]
                    case Spectral.WRAITH:
                        assert len(self._jokers) < self.joker_slots

                        self._add_joker(self._get_random_joker(rarity=Rarity.RARE))
                        self._money = 0
                    case Spectral.SIGIL:
                        assert self._hand is not None
                        assert len(self._hand) > 1

                        random_suit = r.choice(list(Suit))
                        for card in self._hand:
                            card.suit = random_suit
                    case Spectral.OUIJA:
                        assert self._hand is not None
                        assert len(self._hand) > 1

                        random_rank = r.choice(list(Rank))
                        for card in self._hand:
                            card.rank = random_rank
                        self._hand_size_penalty += 1
                        if self._hand_size is not None:
                            self._hand_size -= 1
                    case Spectral.ECTOPLASM:
                        assert self._jokers

                        r.choice(self._jokers).edition = Edition.NEGATIVE
                        self._hand_size_penalty += 1 + self._num_ectoplasms_used
                        if self._hand_size is not None:
                            self._hand_size -= 1 + self._num_ectoplasms_used
                        self._num_ectoplasms_used += 1
                    case Spectral.IMMOLATE:
                        assert self._hand is not None
                        assert len(self._hand) > 1

                        for _ in range(5):
                            if not self._hand:
                                break
                            self._destroy_card(r.choice(self._hand))
                        self._money += 20
                    case Spectral.ANKH:
                        assert self._jokers

                        copied_joker = r.choice(self._jokers)
                        joker_copy = self._create_joker(
                            copied_joker.joker_type,
                            (
                                Edition.BASE
                                if copied_joker.edition is Edition.NEGATIVE
                                else copied_joker.edition
                            ),
                            copied_joker.eternal,
                            copied_joker.perishable,
                            copied_joker.rental,
                        )
                        self._add_joker(joker_copy)
                        for joker in self._jokers:
                            if joker is copied_joker or joker is joker_copy:
                                continue
                            self._destroy_joker(joker)
                    case Spectral.DEJA_VU:
                        assert len(selected_cards) == 1

                        selected_cards[0].seal = Seal.RED
                    case Spectral.HEX:
                        assert self._jokers

                        valid_jokers = [
                            joker
                            for joker in self._jokers
                            if joker.edition is Edition.BASE
                        ]

                        assert valid_jokers

                        random_joker = r.choice(valid_jokers)
                        random_joker.edition = Edition.POLYCHROME

                        for joker in self._jokers:
                            if joker is random_joker:
                                continue
                            self._destroy_joker(joker)
                    case Spectral.TRANCE:
                        assert len(selected_cards) == 1

                        selected_cards[0].seal = Seal.BLUE
                    case Spectral.MEDIUM:
                        assert len(selected_cards) == 1

                        selected_cards[0].seal = Seal.PURPLE
                    case Spectral.CRYPTID:
                        assert len(selected_cards) == 1

                        for _ in range(2):
                            card_copy = replace(selected_cards[0])
                            self._add_card(card_copy)
                            self._hand.append(card_copy)
                    case Spectral.THE_SOUL:
                        assert len(self._jokers) < self.joker_slots

                        self._add_joker(self._get_random_joker(rarity=Rarity.LEGENDARY))
                    case Spectral.BLACK_HOLE:
                        for poker_hand in PokerHand:
                            self._poker_hand_info[poker_hand][0] += 1

    def buy_and_use_shop_item(self, section_index: int, item_index: int) -> None:
        item, cost = self._buy_shop_item(section_index, item_index)
        try:
            self._use_consumable(item, [])
        except AssertionError:
            [self._shop_cards, self._shop_vouchers, self._shop_packs][
                section_index
            ].insert(item_index, (item, cost))
            self._money += cost

            assert False

    def buy_shop_item(self, section_index: int, item_index: int) -> None:
        item, cost = self._buy_shop_item(section_index, item_index)

        match item:
            case BaseJoker():
                self._add_joker(item)
            case Consumable():
                self._consumables.append(item)
            case Card():
                self._add_card(item)
            case Pack():
                self._state = State.OPENING_PACK_SHOP
                self._open_pack(item)
            case Voucher():
                self._vouchers.add(item)

    def discard(self, discard_indices: list[int]) -> None:
        assert self._state is State.PLAYING_BLIND

        assert self._discards > 0
        assert 1 <= len(discard_indices) <= 5
        assert all(0 <= i < len(self._hand) for i in discard_indices)
        assert len(set(discard_indices)) == len(discard_indices)

        for joker in self._jokers:
            joker._on_discard([self._hand[i] for i in discard_indices])

        for i in sorted(discard_indices, reverse=True):
            self._hand.pop(i)

        self._discards -= 1
        self._first_discard = False

        self._deal()

    def next_round(self) -> None:
        assert self._state is State.IN_SHOP

        self._reroll_cost = None
        self._used_chaos = None
        self._shop_cards = None
        self._shop_vouchers = None
        self._shop_packs = None

        self._state = State.SELECTING_BLIND

    def play_hand(self, card_indices: list[int]) -> None:
        assert self._state is State.PLAYING_BLIND

        assert 1 <= len(card_indices) <= 5
        assert all(0 <= i < len(self._hand) for i in card_indices)
        assert len(set(card_indices)) == len(card_indices)

        self._hands -= 1
        self._played_hands += 1

        played_cards = [self._hand[i] for i in card_indices]

        for i in sorted(card_indices, reverse=True):
            self._hand.pop(i)

        poker_hands = self._get_poker_hands(played_cards)
        poker_hands_played = sorted(poker_hands, reverse=True)
        poker_hand_card_indices = poker_hands[poker_hands_played[0]]
        scored_card_indices = (
            list(range(len(played_cards)))
            if JokerType.SPLASH in self._active_jokers
            else [
                i
                for i, card in enumerate(played_cards)
                if i in poker_hand_card_indices or card.is_stone_card
            ]
        )

        for joker in self._jokers:
            joker._on_hand_played(played_cards, scored_card_indices, poker_hands_played)

        self._poker_hand_info[poker_hands_played[0]][1] += 1

        poker_hand_level = self._poker_hand_info[poker_hands_played[0]][0]
        poker_hand_base_chips, poker_hand_base_mult = HAND_BASE_SCORE[
            poker_hands_played[0]
        ]
        poker_hand_chips_scaling, poker_hand_mult_scaling = HAND_SCALING[
            poker_hands_played[0]
        ]
        poker_hand_chips, poker_hand_mult = (
            poker_hand_base_chips + poker_hand_chips_scaling * (poker_hand_level - 1),
            poker_hand_base_mult + poker_hand_mult_scaling * (poker_hand_level - 1),
        )
        self._chips = poker_hand_chips
        self._mult = poker_hand_mult

        for i in scored_card_indices:
            scored_card = played_cards[i]

            self._trigger_scored_card(
                scored_card, played_cards, scored_card_indices, poker_hands_played
            )

            match scored_card:
                case Seal.RED:
                    self._trigger_scored_card(
                        scored_card,
                        played_cards,
                        scored_card_indices,
                        poker_hands_played,
                    )

            for joker in self._jokers:
                for _ in range(
                    joker._on_card_scored_retriggers(
                        scored_card,
                        played_cards,
                        scored_card_indices,
                        poker_hands_played,
                    )
                ):
                    self._trigger_scored_card(
                        scored_card,
                        played_cards,
                        scored_card_indices,
                        poker_hands_played,
                    )

        for held_card in self._hand:
            self._trigger_held_card(held_card)

            match held_card:
                case Seal.RED:
                    self._trigger_held_card(held_card)

            for joker in self._jokers:
                for _ in range(joker._on_card_held_retriggers(held_card)):
                    self._trigger_held_card(held_card)

        for joker in self._jokers:
            match joker:
                case Edition.FOIL:
                    self._chips += 50
                case Edition.HOLO:
                    self._mult += 10

            joker._on_independent(played_cards, scored_card_indices, poker_hands_played)

            for other_joker in self._jokers:
                other_joker._on_dependent(joker)

            match joker:
                case Edition.POLYCHROME:
                    self._mult *= 1.5

        if Voucher.OBSERVATORY in self._vouchers:
            for consumable in self._consumables:
                if consumable.card is poker_hands_played[0].planet:
                    self._mult *= 1.5

        self._mult = round(self._mult, 9)  # floating-point imprecision
        score = int(
            ((self._chips + self._mult) // 2) ** 2
            if self._deck is Deck.PLASMA
            else self._chips * self._mult
        )
        self._round_score += score

        if (
            JokerType.SIXTH_SENSE in self._active_jokers
            and self._first_hand
            and len(played_cards) == 1
            and played_cards[0] == Rank.SIX
        ):
            self._destroy_card(played_cards[0])
            if self.consumable_slots > len(self._consumables):
                self._consumables.append(self._get_random_consumable(Spectral))

        for i in scored_card_indices:
            scored_card = played_cards[i]
            match scored_card:
                case Enhancement.GLASS:
                    if self._chance(1, 4):
                        self._destroy_card(scored_card)

        self._round_poker_hands.add(poker_hands_played[0])
        self._first_hand = False

        for joker in self._jokers:
            joker._on_end_hand()

        return  # leave in when testing

        if self._round_score >= self._round_goal:
            self._end_round(poker_hands_played[0])
            return

        if self._hands == 0:  # game over
            if self._chips >= self._round_goal // 4:
                for joker in self._active_jokers:
                    if joker.joker_type is JokerType.MR_BONES:  # saved by mr. bones
                        self._destroy_joker(joker)
                        self._end_round(poker_hands_played[0], saved=True)
                        return

            self._round_score = None
            self._round_goal = None
            self._hands = None
            self._unused_discards += self._discards
            self._discards = None
            self._hand_size = None
            self._hand = None
            self._deck_cards_left = None
            self._chips = None
            self._mult = None
            self._first_hand = None
            self._first_discard = None
            self._round_poker_hands = None

            self._state = State.GAME_OVER
        else:
            self._deal()

    def rearrange_jokers(self, new_positions: list[int]) -> None:
        assert self._state is not State.GAME_OVER

        assert self._jokers
        assert sorted(new_positions) == list(range(len(self._jokers)))

        self._jokers = [self._jokers[i] for i in new_positions]

        for joker in self._jokers:
            joker._on_jokers_moved()

    def reroll(self) -> None:
        assert self._state is State.IN_SHOP

        reroll_cost = self.reroll_cost

        assert self._available_money >= reroll_cost

        for joker in self._jokers:
            joker._on_shop_rerolled()

        self._money -= reroll_cost

        if not self._used_chaos and JokerType.CHAOS_THE_CLOWN in self._active_jokers:
            self._used_chaos = True
        else:
            self._reroll_cost += 1

        self._populate_shop_cards()

    def select_blind(self) -> None:
        assert self._state is State.SELECTING_BLIND

        self._round += 1
        self._round_score = 0
        self._round_goal = (
            ANTE_BASE_CHIPS[self._ante] * BLIND_INFO[self._blind][1]
        ) * (2 if self._deck is Deck.PLASMA else 1)
        self._hands = self._starting_hands
        self._discards = self._starting_discards
        self._hand_size = self._starting_hand_size
        for active_joker in self._active_jokers:
            match active_joker:
                case JokerType.JUGGLER:
                    self._hand_size += 1
                case JokerType.TURTLE_BEAN:
                    self._hand_size += active_joker.hand_size_increase
                case JokerType.TROUBADOUR:
                    self._hand_size += 2
                    self._hands -= 1
                case JokerType.MERRY_ANDY:
                    self._discards += 3
                    self._hand_size -= 1
                case JokerType.STUNTMAN:
                    self._hand_size -= 2
        if self._hand_size <= 0 or self._hands <= 0:
            raise NotImplementedError

        for joker in self._jokers:
            joker._on_blind_selected()

        while Tag.JUGGLE in self._tags:
            self._tags.remove(Tag.JUGGLE)
            self._hands += 3

        self._hand = []
        self._deck_cards_left = self._full_deck.copy()
        self._round_poker_hands = set()
        self._first_hand = True
        self._first_discard = True

        self._deal()

        self._state = State.PLAYING_BLIND

    def sell_item(self, section_index: int, item_index: int) -> None:
        assert self._state is not State.GAME_OVER

        assert section_index in [0, 1]

        section_items = [self._jokers, self._consumables][section_index]

        assert 0 <= item_index < len(section_items)

        sold_item = section_items[item_index]
        joker_sold = isinstance(sold_item, BaseJoker)

        if joker_sold:
            assert not sold_item.eternal

        section_items.pop(item_index)

        for joker in self._jokers:
            joker._on_item_sold(sold_item)

            if joker_sold:
                joker._on_jokers_moved()

        self._money += self._calculate_sell_value(sold_item)

    def skip_blind(self) -> None:
        assert self._state is State.SELECTING_BLIND
        assert self._blind in [Blind.SMALL_BLIND, Blind.BIG_BLIND]

        self._blinds_skipped += 1

        tag, extra = self._ante_tags[self._blind is Blind.BIG_BLIND]

        num_tags = 1
        while tag is not Tag.DOUBLE and Tag.DOUBLE in self._tags:
            self._tags.remove(Tag.DOUBLE)
            num_tags += 1

        for _ in range(num_tags):
            match tag:
                case Tag.BOSS:
                    self._random_final_blind()
                case Tag.BUFFOON | Tag.CHARM | Tag.METEOR | Tag.ETHEREAL | Tag.STANDARD:
                    self._state = State.OPENING_PACK_TAG
                    self._open_pack(TAG_PACKS[tag])
                case Tag.HANDY:
                    self._money += 1 * self._played_hands
                case Tag.GARBAGE:
                    self._money += 1 * self._unused_discards
                case Tag.TOP_UP:
                    for _ in range(min(2, self.joker_slots - len(self._jokers))):
                        self._add_joker(self._get_random_joker(Rarity.COMMON))
                case Tag.SPEED:
                    self._money += 5 * self._blinds_skipped
                case Tag.ORBITAL:
                    self._poker_hand_info[extra][0] += 3
                case Tag.ECONOMY:
                    self._money += max(0, min(40, self._money))
                case _:
                    self._tags.append(tag)

        self._next_blind()

    def use_consumable(
        self, consumable_index: int, selected_card_indices: list[int] | None = None
    ) -> None:
        assert self._state is not State.GAME_OVER

        assert 0 <= consumable_index < len(self._consumables)

        if selected_card_indices is not None:
            assert self._hand is not None
            assert 1 <= len(selected_card_indices) <= 5
            assert all(0 <= i < len(self._hand) for i in selected_card_indices)
            assert len(set(selected_card_indices)) == len(selected_card_indices)

            selected_cards = [self._hand[i] for i in selected_card_indices]
        else:
            selected_cards = []

        consumable = self._consumables[consumable_index]
        self._use_consumable(consumable, selected_cards)
        self._consumables.pop(consumable_index)

    @property
    def _active_jokers(self) -> list[BaseJoker]:
        return [joker for joker in self._jokers if not joker.debuffed]

    @property
    def _available_money(self) -> int:
        return max(
            0,
            (
                (self._money + 20)
                if JokerType.CREDIT_CARD in self._active_jokers
                else self._money
            ),
        )

    @property
    def _is_finisher_ante(self) -> bool:
        return self._ante % 8 == 0

    @property
    def _starting_discards(self) -> int:
        starting_discards = (
            3
            + (
                2
                if Voucher.RECYCLOMANCY in self._vouchers
                else 1 if Voucher.WASTEFUL in self._vouchers else 0
            )
            + self._active_jokers.count(JokerType.DRUNKARD)
            - (Voucher.PETROGLYPH in self._vouchers)
        )

        if self._deck is Deck.RED:
            starting_discards += 1

        return starting_discards

    @property
    def _starting_hand_size(self) -> int:
        starting_hand_size = (
            8
            + (
                2
                if Voucher.PALETTE in self._vouchers
                else 1 if Voucher.PAINT_BRUSH in self._vouchers else 0
            )
            - self._hand_size_penalty
        )

        match self._deck:
            case Deck.PAINTED:
                starting_hand_size += 2

        return starting_hand_size

    @property
    def _starting_hands(self) -> int:
        starting_hands = (
            4
            + (
                2
                if Voucher.NACHO_TONG in self._vouchers
                else 1 if Voucher.GRABBER in self._vouchers else 0
            )
            - (Voucher.HIEROGLYPH in self._vouchers)
        )

        match self._deck:
            case Deck.BLUE:
                starting_hands += 1
            case Deck.BLACK:
                starting_hands -= 1

        return starting_hands

    @property
    def _unlocked_poker_hands(self) -> list[PokerHand]:
        return [
            poker_hand
            for i, poker_hand in enumerate(PokerHand)
            if i > 2 or self._poker_hand_info[poker_hand][1] > 0
        ]

    @property
    def ante(self) -> int:
        return self._ante

    @property
    def ante_tags(
        self,
    ) -> list[tuple[Tag, PokerHand | None], tuple[Tag, PokerHand | None]]:
        return self._ante_tags

    @property
    def blind(self) -> Blind:
        return self._blind

    @property
    def consumable_slots(self) -> int:
        consumable_slots = (
            2
            + sum(consumable.is_negative for consumable in self._consumables)
            + (Voucher.CRYSTAL_BALL in self._vouchers)
        )

        match self._deck:
            case Deck.MAGIC:
                consumable_slots += 1
            case Deck.NEBULA:
                consumable_slots -= 1

        return consumable_slots

    @property
    def consumables(self) -> list[Consumable]:
        return self._consumables

    @property
    def deck(self) -> Deck:
        return self._deck

    @property
    def discards(self) -> int | None:
        return self._discards

    @property
    def final_blind(self) -> Blind:
        return self._final_blind

    @property
    def full_deck(self) -> list[Card]:
        return self._full_deck

    @property
    def hand(self) -> list[Card] | None:
        return self._hand

    @property
    def hand_size(self) -> int | None:
        return self._hand_size

    @property
    def hands(self) -> int | None:
        return self._hands

    @property
    def joker_slots(self) -> int:
        joker_slots = (
            5
            + sum(joker.edition is Edition.NEGATIVE for joker in self._jokers)
            + (Voucher.ANTIMATTER in self._vouchers)
        )

        match self._deck:
            case Deck.BLACK:
                joker_slots += 1
            case Deck.PAINTED:
                joker_slots -= 1

        return joker_slots

    @property
    def jokers(self) -> list[BaseJoker]:
        return self._jokers

    @property
    def money(self) -> int:
        return self._money

    @property
    def poker_hand_info(self) -> dict[PokerHand : list[int, int]]:
        return self._poker_hand_info

    @property
    def reroll_cost(self) -> int | None:
        if self._reroll_cost is None:
            return None
        return (
            0
            if not self._used_chaos and JokerType.CHAOS_THE_CLOWN in self._active_jokers
            else self._reroll_cost
        )

    @property
    def round(self) -> int:
        return self._round

    @property
    def round_score(self) -> int:
        return self._round_score

    @property
    def shop_cards(self) -> list[tuple[BaseJoker | Consumable | Card, int]] | None:
        return self._shop_cards

    @property
    def shop_packs(self) -> list[tuple[Pack, int]] | None:
        return self._shop_packs

    @property
    def shop_vouchers(self) -> list[tuple[Voucher, int]] | None:
        return self._shop_vouchers

    @property
    def stake(self) -> Stake:
        return self._stake

    @property
    def state(self) -> State:
        return self._state

    @property
    def tags(self) -> list[Tag]:
        return self._tags

    @property
    def vouchers(self) -> set[Voucher]:
        return self._vouchers
