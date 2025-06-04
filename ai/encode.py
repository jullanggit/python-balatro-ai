from typing import Dict
import torch
from balatro import *
from typing import Type, List

MAX_CONSUMABLES = 20
MAX_DECK_CARDS = 100
MAX_JOKERS = 15
MAX_HAND_CARDS = 20

def enum_to_index(enum_class) -> Dict:
    return {item: idx for idx, item in enumerate(enum_class)}

card_to_index = {**enum_to_index(Tarot), **enum_to_index(Planet), **enum_to_index(Spectral)}

def one_hot(index: int, num_classes: int) -> torch.FloatTensor:
    return torch.nn.functional.one_hot(torch.tensor(index), num_classes=num_classes).float()

def encode_ante_tags(ante_tags: list[tuple[Tag, PokerHand | None]]) -> torch.FloatTensor:
    encoded = []
    for i in range(2):
        tag, hand = ante_tags[i]
        tag_encoded = one_hot(enum_to_index(Tag)[tag], len(Tag))

        if hand is None:
            hand_encoded = torch.zeros(len(PokerHand), dtype=torch.float32)
        else:
            hand_encoded = one_hot(enum_to_index(PokerHand)[hand], len(PokerHand))

        encoded.append(torch.cat([tag_encoded, hand_encoded]).unsqueeze(0))

    return torch.cat(encoded)

def encode_blind(blind: Blind) -> torch.FloatTensor:
    return one_hot(enum_to_index(Blind)[blind], len(Blind))

def encode_int(int: int) -> torch.FloatTensor:
    return torch.tensor([float(int)], dtype=torch.float32)
def encode_bool(bool: bool) -> torch.FloatTensor:
    return torch.tensor([1.0 if bool else 0.0], dtype=torch.float32)

def encode_consumables(consumables: list[Consumable]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, MAX_CONSUMABLES):
        if i < len(consumables):
            consumable = consumables[i]

            card = one_hot(card_to_index[consumable.card], len(card_to_index))
            is_negative = encode_bool(consumable.is_negative)

            features = torch.cat(card, is_negative)
            encoded.append(features.unsqueeze(0))
        else:
            encoded.append(torch.zeros(1, len(card_to_index) + 1))
    return torch.cat(encoded)

def encode_cards(cards: list[Card], max) -> torch.Tensor:
    """
    tensor shape: [max, (len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3)]
    """

    encoded = []
    for i in range(max):
        if i < len(cards):
            card = cards[i]
            encoded.append(encode_card(card))
        else:
            encoded.append(torch.zeros(1, len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3))

    return torch.cat(encoded)


def encode_card(card: Card) -> torch.Tensor:
    """
    tensor shape: [len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3,]
    """

    rank = one_hot(enum_to_index(Rank)[card.rank], len(Rank))
    suit = one_hot(enum_to_index(Suit)[card.suit], len(Suit))

    enhancement_to_index = enum_to_index(Enhancement)
    if card.enhancement is None:
        enhancement = torch.zeros(len(enhancement_to_index))
    else:
        enhancement = one_hot(enhancement_to_index[card.enhancement], len(Enhancement))

    seal_to_index = enum_to_index(Seal)
    if card.seal is None:
        seal = torch.zeros(len(seal_to_index))
    else:
        seal = one_hot(seal_to_index[card.seal], len(Seal))

    edition = one_hot(enum_to_index(Edition)[card.edition], len(Edition))
    extra_chips = encode_int(card.extra_chips)
    is_debuffed = encode_bool(card.is_debuffed)
    is_face_down = encode_bool(card.is_face_down)

    features = torch.cat([rank, suit, enhancement, seal, edition, extra_chips, is_debuffed, is_face_down])
    return features.unsqueeze(0)

def all_subclasses(cls: Type) -> List[Type]:
    """
    Recursively find every subclass of `cls`.
    """
    direct = cls.__subclasses__()  # immediate children
    out: List[Type] = []
    for sub in direct:
        out.append(sub)
        out.extend(all_subclasses(sub))
    return out

all_jokers =  all_subclasses(BalatroJoker)
all_jokers.sort(key=lambda C: C.__name__)

jokers_to_index = enum_to_index(all_jokers)

def encode_jokers(jokers: list[BalatroJoker]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, MAX_JOKERS):
        if i < len(jokers):
            joker = jokers[i]
            type = one_hot(jokers_to_index[joker], len(all_jokers))
            edition = one_hot(enum_to_index(Edition)[joker.edition], len(Edition))
            is_eternal = encode_bool(joker.is_eternal)
            is_perishable = encode_bool(joker.is_perishable)
            is_rental = encode_bool(joker.is_rental)
            is_debuffed = encode_bool(joker.is_debuffed)
            is_flipped = encode_bool(joker.is_flipped)
            num_perishable_rounds_left = encode_int(joker.num_perishable_rounds_left)

            features = torch.cat([type, edition, is_eternal, is_perishable, is_rental, is_debuffed, is_flipped, num_perishable_rounds_left])
            encoded.append(features.unsqueeze(0))
        else:
            encoded.append(torch.zeros(1, len(all_jokers)+len(Edition)+5+1))
    return torch.cat(encoded)


# TODO: handle sellable
def encode(run: Run) -> torch.FloatTensor:
    ante = encode_int(run.ante)
    ante_tags = encode_ante_tags(run.ante_tags)

    blind = encode_blind(run.blind)
    blind_reward = encode_int(run.blind_reward)
    boss_blind = encode_blind(run.boss_blind)
    consumable_slots = encode_int(run.consumable_slots)
    consumables = encode_consumables(run.consumables)
    if run.hand is None:
        hand_cards = torch.zeros(MAX_HAND_CARDS, (len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3))
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
    return torch.cat(parts, dim=0)
