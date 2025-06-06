from typing import Dict, Any
import torch
from balatro import Tag, PokerHand, Blind, Rank, Suit, Enhancement, Seal, Edition, Tarot, Planet, Spectral, Card, BalatroJoker, Consumable, Run, Stake, State, Voucher, Pack

MAX_CONSUMABLES = 20
MAX_DECK_CARDS = 100
MAX_JOKERS = 15
MAX_HAND_CARDS = 20
MAX_TAGS = 20
MAX_SHOP_CARDS = 4
MAX_SHOP_VOUCHERS = 5
MAX_SHOP_PACKS = 2

def _enum_to_index(enum_class) -> Dict:
    """
    builds a dictionary of [Enum variant -> index]
    """
    return {item: idx for idx, item in enumerate(enum_class)}

def all_subclasses(cls: type) -> list[type]:
    """
    Recursively find every subclass of `cls`.
    """
    direct = cls.__subclasses__()  # immediate children
    out: list[type] = []
    for sub in direct:
        out.append(sub)
        out.extend(all_subclasses(sub))
    return out
all_jokers =  all_subclasses(BalatroJoker)
all_jokers.sort(key=lambda C: C.__name__)
JOKERS_TO_INDEX = _enum_to_index(all_jokers)

# x to Index conversions
TAG_TO_INDEX: Dict[Tag, int] = _enum_to_index(Tag)
POKERHAND_TO_INDEX: Dict[PokerHand, int] = _enum_to_index(PokerHand)
BLIND_TO_INDEX: Dict[Blind, int] = _enum_to_index(Blind)
RANK_TO_INDEX: Dict[Rank, int] = _enum_to_index(Rank)
SUIT_TO_INDEX: Dict[Suit, int] = _enum_to_index(Suit)
ENHANCEMENT_TO_INDEX: Dict[Enhancement, int] = _enum_to_index(Enhancement)
SEAL_TO_INDEX: Dict[Seal, int] = _enum_to_index(Seal)
EDITION_TO_INDEX: Dict[Edition, int] = _enum_to_index(Edition)
STAKE_TO_INDEX: Dict[Stake, int] = _enum_to_index(Stake)
STATE_TO_INDEX: Dict[State, int] = _enum_to_index(State)
VOUCHER_TO_INDEX: Dict[Voucher, int] = _enum_to_index(Voucher)
PACK_TO_INDEX: Dict[Pack, int] = _enum_to_index(Pack)
CONSUMABLE_TO_INDEX = {**_enum_to_index(Tarot), **_enum_to_index(Planet), **_enum_to_index(Spectral)}

def one_hot(dict: Dict, element) -> torch.FloatTensor:
    """
    returns a one-hot f32 tensor with the length of the dict,
    where only the element returned by dict[element] is 1
    """
    return one_hot_inner(dict, element).float()

def one_hot_inner(dict: Dict, element) -> torch.FloatTensor:
    """
    returns a one-hot tensor with the length of the dict,
    where only the element returned by dict[element] is 1
    """
    return torch.nn.functional.one_hot(torch.tensor(dict[element]), num_classes=len(dict))

SIZE_ANTE_TAGS = [2, len(TAG_TO_INDEX) + len(POKERHAND_TO_INDEX)]
def encode_ante_tags(ante_tags: list[tuple[Tag, PokerHand | None]]) -> torch.FloatTensor:
    encoded = []
    for i in range(2):
        tag, hand = ante_tags[i]
        tag_encoded = one_hot(TAG_TO_INDEX, tag)

        if hand is None:
            hand_encoded = torch.zeros(len(POKERHAND_TO_INDEX))
        else:
            hand_encoded = one_hot(POKERHAND_TO_INDEX, hand)

        encoded.append(torch.cat([tag_encoded, hand_encoded]).unsqueeze(0))

    return torch.cat(encoded)

def encode_int(int: int) -> torch.FloatTensor:
    return torch.tensor([float(int)])

def encode_bool(bool: bool) -> torch.FloatTensor:
    return torch.tensor([1.0 if bool else 0.0])

SIZE_CONSUMABLE = len(CONSUMABLE_TO_INDEX) + 2
def encode_consumable(consumable: Consumable) -> torch.FloatTensor:
    card = one_hot(CONSUMABLE_TO_INDEX, consumable.card)
    is_negative = encode_bool(consumable.is_negative)
    extra_sell_value = encode_int(consumable._extra_sell_value)

    return torch.cat([card, is_negative, extra_sell_value])

SIZE_CONSUMABLES = [MAX_CONSUMABLES, SIZE_CONSUMABLE]
def encode_consumables(consumables: list[Consumable]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, MAX_CONSUMABLES):
        if i < len(consumables):
            consumable = consumables[i]
            features = encode_consumable(consumable)
            encoded.append(features.unsqueeze(0))
        else:
            encoded.append(torch.zeros(1, SIZE_CONSUMABLE))
    return torch.cat(encoded)

SIZE_CARD = len(RANK_TO_INDEX) + len(SUIT_TO_INDEX) + len(ENHANCEMENT_TO_INDEX) + len(SEAL_TO_INDEX) + len(EDITION_TO_INDEX) + 3
def encode_card(card: Card) -> torch.Tensor:
    rank = one_hot(RANK_TO_INDEX, card.rank)
    suit = one_hot(SUIT_TO_INDEX, card.suit)

    if card.enhancement is None:
        enhancement = torch.zeros(len(ENHANCEMENT_TO_INDEX))
    else:
        enhancement = one_hot(ENHANCEMENT_TO_INDEX, card.enhancement)

    if card.seal is None:
        seal = torch.zeros(len(SEAL_TO_INDEX))
    else:
        seal = one_hot(SEAL_TO_INDEX, card.seal)

    edition = one_hot(EDITION_TO_INDEX, card.edition)
    chips = encode_int(card.chips)
    is_debuffed = encode_bool(card.is_debuffed)
    is_face_down = encode_bool(card.is_face_down)

    return torch.cat([rank, suit, enhancement, seal, edition, chips, is_debuffed, is_face_down])

SIZE_HAND_CARDS = [MAX_HAND_CARDS, SIZE_CARD]
SIZE_DECK_CARDS = [MAX_DECK_CARDS, SIZE_CARD]
def encode_cards(cards: list[Card], max) -> torch.Tensor:
    encoded = []
    for i in range(max):
        if i < len(cards):
            card = cards[i]
            encoded.append(encode_card(card).unsqueeze(0))
        else:
            encoded.append(torch.zeros(1, SIZE_CARD))

    return torch.cat(encoded)

SIZE_JOKER = len(JOKERS_TO_INDEX) + len(EDITION_TO_INDEX) + 7
def encode_joker(joker: BalatroJoker) -> torch.FloatTensor:
    type = one_hot(JOKERS_TO_INDEX, joker.__class__)
    edition = one_hot(EDITION_TO_INDEX, joker.edition)
    is_eternal = encode_bool(joker.is_eternal)
    is_perishable = encode_bool(joker.is_perishable)
    is_rental = encode_bool(joker.is_rental)
    is_debuffed = encode_bool(joker.is_debuffed)
    is_flipped = encode_bool(joker.is_flipped)
    num_perishable_rounds_left = encode_int(joker.num_perishable_rounds_left)
    extra_sell_value = encode_int(joker._extra_sell_value)

    return torch.cat([type, edition, is_eternal, is_perishable, is_rental, is_debuffed, is_flipped, num_perishable_rounds_left, extra_sell_value])

SIZE_JOKERS = [MAX_JOKERS, SIZE_JOKER]
def encode_jokers(jokers: list[BalatroJoker]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, MAX_JOKERS):
        if i < len(jokers):
            joker = jokers[i]
            features = encode_joker(joker)
            encoded.append(features.unsqueeze(0))
        else:
            encoded.append(torch.zeros(1, SIZE_JOKER))
    return torch.cat(encoded)

SIZE_POKERHAND_INFO = [len(PokerHand), 2]
def encode_poker_hand_info(info: dict[PokerHand, list[int]]) -> torch.FloatTensor:
    encoded = torch.zeros(SIZE_POKERHAND_INFO[0], SIZE_POKERHAND_INFO[1])
    for poker_hand in PokerHand:
        ints = info[poker_hand]
        index = POKERHAND_TO_INDEX[poker_hand]
        encoded[index] = torch.tensor(ints).float()

    return encoded


def multi_hot(lookup: Dict, elements: set) -> torch.FloatTensor:
    """
    returns a multi-hot Tensor with the length of the lookup Dict
    """
    vec = torch.zeros(len(lookup))
    for elem in elements:
        vec[lookup[elem]] = 1.0
    return vec

SIZE_TAGS = [MAX_TAGS, len(TAG_TO_INDEX)]
def encode_tags(tags: list[Tag]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, MAX_TAGS):
        if i < len(tags):
            encoded.append(one_hot(TAG_TO_INDEX, tags[i]).unsqueeze(0))
        else:
            encoded.append(torch.zeros(1, len(TAG_TO_INDEX)))
    return torch.cat(encoded)

SIZE_SHOP_PACK = len(PACK_TO_INDEX)
SIZE_SHOP_VOUCHER = len(VOUCHER_TO_INDEX)
def encode_enum_shop_item(enum:Any, dict: Dict[Any, int]) -> torch.FloatTensor:
    return one_hot(dict, enum)

SIZE_SHOP_CARD = 3 + max(SIZE_JOKER, SIZE_CONSUMABLE, SIZE_CARD)
def encode_shop_card(card: BalatroJoker | Consumable | Card) -> torch.FloatTensor:
    encoded = torch.zeros(SIZE_SHOP_CARD)
    # one_hot encode type and append encoded type with padding
    match card:
        case BalatroJoker():
            encoded[0] = 1.0
            encoded_joker = encode_joker(card)
            encoded[3:3+SIZE_JOKER] = encoded_joker
        case Consumable():
            encoded[1] = 1.0
            encoded_consumable = encode_consumable(card)
            encoded[3:3+SIZE_CONSUMABLE] = encoded_consumable
        case Card():
            encoded[2] = 1.0
            encoded_card = encode_card(card)
            encoded[3:3+SIZE_CARD] = encoded_card
        case _:
            raise Exception("wrong type")

    return encoded

SIZE_SHOP_PACKS = [MAX_SHOP_PACKS, SIZE_SHOP_PACK + 1]
SIZE_SHOP_VOUCHERS = [MAX_SHOP_VOUCHERS, SIZE_SHOP_VOUCHER + 1]
SIZE_SHOP_CARDS = [MAX_SHOP_CARDS, SIZE_SHOP_CARD + 1]
def encode_shop_items(items: list[tuple[Any, int]] | None, fn, element_size: int, max: int, dict: Dict[Any, int] | None = None) -> torch.FloatTensor:
    if items is None:
        return torch.zeros(max, element_size + 1)
    else:
        out = []
        for i in range(max):
            if i < len(items):
                item = items[i]
                inner_encoded = fn(item[0]) if dict is None else fn(item[0], dict)
                int_encoded = encode_int(item[1])
                encoded = torch.cat([inner_encoded, int_encoded]).unsqueeze(0)
                out.append(encoded)
            else:
                out.append(torch.zeros(1, element_size + 1))
        return torch.cat(out)


SIZE_ENCODED = 16 + len(POKERHAND_TO_INDEX) + SIZE_ANTE_TAGS[0]*SIZE_ANTE_TAGS[1] + 2 * len(BLIND_TO_INDEX) + SIZE_CONSUMABLES[0]*SIZE_CONSUMABLES[1] + SIZE_HAND_CARDS[0]*SIZE_HAND_CARDS[1] + SIZE_DECK_CARDS[0]*SIZE_DECK_CARDS[1] + MAX_HAND_CARDS + SIZE_JOKERS[0]*SIZE_JOKERS[1] + len(STAKE_TO_INDEX) + len(STATE_TO_INDEX) + SIZE_POKERHAND_INFO[0]*SIZE_POKERHAND_INFO[1] + SIZE_SHOP_CARDS[0]*SIZE_SHOP_CARDS[1] + SIZE_SHOP_PACKS[0]*SIZE_SHOP_PACKS[1] + SIZE_SHOP_VOUCHERS[0]*SIZE_SHOP_VOUCHERS[1] + SIZE_TAGS[0]*SIZE_TAGS[1] + len(VOUCHER_TO_INDEX)
def encode(run: Run) -> torch.FloatTensor:
    available_money = encode_int(run._available_money)
    discards_per_round = encode_int(run._discards_per_round)
    hands_per_round = encode_int(run._hands_per_round)
    most_played_hand = one_hot(POKERHAND_TO_INDEX, run._most_played_hand)
    ante = encode_int(run.ante)
    ante_tags = encode_ante_tags(run.ante_tags)

    blind = one_hot(BLIND_TO_INDEX, run.blind)
    blind_reward = encode_int(run.blind_reward)
    boss_blind = one_hot(BLIND_TO_INDEX, run.boss_blind)
    cash_out_total = torch.tensor([0 if run.cash_out_total is None else run.cash_out_total])
    consumable_slots = encode_int(run.consumable_slots)
    consumables = encode_consumables(run.consumables)
    hand_cards = torch.zeros(SIZE_HAND_CARDS[0], SIZE_HAND_CARDS[1]) if run.hand is None else encode_cards(run.hand, MAX_HAND_CARDS)
    deck_cards_left = encode_cards(run.deck_cards_left, MAX_DECK_CARDS)
    discards = encode_int(run.discards)
    forced_selected_card_index = torch.zeros(MAX_HAND_CARDS) if run.forced_selected_card_index is None else torch.nn.functional.one_hot(torch.tensor(run.forced_selected_card_index), MAX_HAND_CARDS)
    hand_size = encode_int(run.hand_size)
    hands = encode_int(0 if run.hands is None else run.hands)
    joker_slots = encode_int(run.joker_slots)
    jokers = encode_jokers(run.jokers)
    money = encode_int(run.money)
    # opened_pack
    pack_choices_left = encode_int(0 if run.hands is None else run.pack_choices_left)
    # pack_items
    poker_hand_info = encode_poker_hand_info(run.poker_hand_info)
    reroll_cost = encode_int(0 if run.reroll_cost is None else run.reroll_cost)
    round = encode_int(run.round)
    round_goal = torch.tensor([0 if run.round_goal is None else run.round_goal])
    round_score = torch.tensor([run.round_score], dtype=torch.float32)
    shop_cards = encode_shop_items(run.shop_cards, encode_shop_card, SIZE_SHOP_CARD, MAX_SHOP_CARDS)
    shop_packs = encode_shop_items(run.shop_packs, encode_enum_shop_item, SIZE_SHOP_PACK, MAX_SHOP_PACKS, PACK_TO_INDEX)
    shop_vouchers = encode_shop_items(run.shop_vouchers, encode_enum_shop_item, SIZE_SHOP_VOUCHER, MAX_SHOP_VOUCHERS, VOUCHER_TO_INDEX)
    stake = one_hot(STAKE_TO_INDEX, run.stake)
    state = one_hot(STATE_TO_INDEX, run.state)
    tags = encode_tags(run.tags)
    vouchers = multi_hot(VOUCHER_TO_INDEX, run.vouchers)

    parts = [available_money, discards_per_round, hands_per_round, most_played_hand,
        ante, ante_tags.view(-1), blind, blind_reward, boss_blind, cash_out_total, consumable_slots,
        consumables.view(-1), hand_cards.view(-1), deck_cards_left.view(-1),
        discards, forced_selected_card_index, hand_size, hands, joker_slots, jokers.view(-1), money,
        pack_choices_left, poker_hand_info.view(-1), reroll_cost, round, round_goal, round_score, shop_cards.view(-1),
        shop_vouchers.view(-1), shop_packs.view(-1), stake, state, tags.view(-1), vouchers]
    encoded = torch.cat(parts, dim=0)
    assert len(encoded) == SIZE_ENCODED
    return encoded
