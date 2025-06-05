from typing import Dict
import torch
from balatro import Tag, PokerHand, Blind, Rank, Suit, Enhancement, Seal, Edition, Tarot, Planet, Spectral, Card, BalatroJoker, Consumable, Run

MAX_CONSUMABLES = 20
MAX_DECK_CARDS = 100
MAX_JOKERS = 15
MAX_HAND_CARDS = 20


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
CARD_TO_INDEX = {**_enum_to_index(Tarot), **_enum_to_index(Planet), **_enum_to_index(Spectral)}

def one_hot(dict: Dict, element) -> torch.FloatTensor:
    """
    returns a one-hot f32 tensor with the length of the dict,
    where only the element returned by dict[element] is 1
    """
    return torch.nn.functional.one_hot(torch.tensor(dict[element]), num_classes=len(dict)).float()

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

SIZE_CONSUMABLE = len(CARD_TO_INDEX) + 1
SIZE_CONSUMABLES = [MAX_CONSUMABLES, SIZE_CONSUMABLE]
def encode_consumables(consumables: list[Consumable]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, MAX_CONSUMABLES):
        if i < len(consumables):
            consumable = consumables[i]

            card = one_hot(CARD_TO_INDEX, consumable.card)
            is_negative = encode_bool(consumable.is_negative)

            features = torch.cat([card, is_negative])
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
    extra_chips = encode_int(card.extra_chips)
    is_debuffed = encode_bool(card.is_debuffed)
    is_face_down = encode_bool(card.is_face_down)

    features = torch.cat([rank, suit, enhancement, seal, edition, extra_chips, is_debuffed, is_face_down])
    return features.unsqueeze(0)

SIZE_HAND_CARDS = [MAX_HAND_CARDS, SIZE_CARD]
SIZE_DECK_CARDS = [MAX_DECK_CARDS, SIZE_CARD]
def encode_cards(cards: list[Card], max) -> torch.Tensor:
    encoded = []
    for i in range(max):
        if i < len(cards):
            card = cards[i]
            encoded.append(encode_card(card))
        else:
            encoded.append(torch.zeros(1, SIZE_CARD))

    return torch.cat(encoded)

SIZE_JOKER = len(JOKERS_TO_INDEX) + len(EDITION_TO_INDEX) + 6
SIZE_JOKERS = [MAX_JOKERS, SIZE_JOKER]
def encode_jokers(jokers: list[BalatroJoker]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, MAX_JOKERS):
        if i < len(jokers):
            joker = jokers[i]
            type = one_hot(JOKERS_TO_INDEX, joker.__class__)
            edition = one_hot(EDITION_TO_INDEX, joker.edition)
            is_eternal = encode_bool(joker.is_eternal)
            is_perishable = encode_bool(joker.is_perishable)
            is_rental = encode_bool(joker.is_rental)
            is_debuffed = encode_bool(joker.is_debuffed)
            is_flipped = encode_bool(joker.is_flipped)
            num_perishable_rounds_left = encode_int(joker.num_perishable_rounds_left)

            features = torch.cat([type, edition, is_eternal, is_perishable, is_rental, is_debuffed, is_flipped, num_perishable_rounds_left])
            encoded.append(features.unsqueeze(0))
        else:
            encoded.append(torch.zeros(1, SIZE_JOKER))
    return torch.cat(encoded)


# TODO: handle sellable
SIZE_ENCODED = 5 + SIZE_ANTE_TAGS[0]*SIZE_ANTE_TAGS[1] + 2 * len(BLIND_TO_INDEX) + SIZE_CONSUMABLES[0]*SIZE_CONSUMABLES[1] + SIZE_HAND_CARDS[0]*SIZE_HAND_CARDS[1] + SIZE_DECK_CARDS[0]*SIZE_DECK_CARDS[1] + SIZE_JOKERS[0]*SIZE_JOKERS[1]
def encode(run: Run) -> torch.FloatTensor:
    ante = encode_int(run.ante)
    ante_tags = encode_ante_tags(run.ante_tags)

    blind = one_hot(BLIND_TO_INDEX, run.blind)
    blind_reward = encode_int(run.blind_reward)
    boss_blind = one_hot(BLIND_TO_INDEX, run.boss_blind)
    consumable_slots = encode_int(run.consumable_slots)
    consumables = encode_consumables(run.consumables)
    if run.hand is None:
        hand_cards = torch.zeros(SIZE_HAND_CARDS[0], SIZE_HAND_CARDS[1])
    else:
        hand_cards = encode_cards(run.hand, MAX_HAND_CARDS)
    deck_cards_left = encode_cards(run.deck_cards_left, MAX_DECK_CARDS)
    discards = encode_int(run.discards)
    if run.hands is None:
        hands = encode_int(0)
    else:
        hands = encode_int(run.hands)
    jokers = encode_jokers(run.jokers)

    parts = [ante, ante_tags.view(-1), blind, blind_reward, boss_blind,
        consumable_slots, consumables.view(-1), hand_cards.view(-1),
        deck_cards_left.view(-1), discards, hands, jokers.view(-1)]
    encoded = torch.cat(parts, dim=0)
    assert len(encoded) == SIZE_ENCODED
    return encoded
