import torch
from balatro import *

max_consumables = 20
max_deck_cards = 100
max_jokers = 15
max_hand_cards = 20

def enum_to_index(enum_class):
    return {item: idx for idx, item in enumerate(enum_class)}

card_to_index = {**enum_to_index(Tarot), **enum_to_index(Planet), **enum_to_index(Spectral)}

def one_hot(index: int, num_classes: int) -> torch.FloatTensor:
    return torch.nn.functional.one_hot(torch.tensor(index), num_classes=num_classes).float()

def encode_ante_tags(ante_tags: list[tuple[Tag, PokerHand | None]]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, 2):
        tag, hand = ante_tags[i]
        tag_encoded = one_hot(enum_to_index(Tag)[tag], len(Tag))

        if hand is None:
            hand_encoded = torch.zeros(len(PokerHand), dtype=torch.float32)
        else:
            hand_encoded = one_hot(enum_to_index(PokerHand)[hand], len(PokerHand))

        encoded.append(torch.cat([tag_encoded, hand_encoded]))

    return torch.cat(encoded, dim=0)

def encode_blind(blind: Blind) -> torch.FloatTensor:
    return one_hot(enum_to_index(Blind)[blind], len(Blind))

def encode_int(int: int) -> torch.FloatTensor:
    return torch.tensor([float(int)], dtype=torch.float32)
def encode_bool(bool: bool) -> torch.FloatTensor:
    return torch.tensor([1.0 if bool else 0.0], dtype=torch.float32)

def encode_consumables(consumables: list[Consumable]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, max_consumables):
        if i < len(consumables):
            consumable = consumables[i]

            card = one_hot(card_to_index[consumable.card], len(card_to_index))
            is_negative = encode_bool(consumable.is_negative)

            encoded.append(card)
            encoded.append(is_negative)
        else:
            encoded.append(torch.zeros(len(card_to_index) + 1))
    return torch.cat(encoded, dim=0)

def encode_cards(cards: list[Card], max) -> torch.Tensor:
    """
    tensor shape: [max*(len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3),]
    """

    encoded = []
    for i in (0, max):
        if i < len(cards):
            card = cards[i]
            encoded.append(encode_card(card))
        else:
            encoded.append(torch.zeros(len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3))

    return torch.cat(encoded, dim=0)


def encode_card(card: Card) -> torch.Tensor:
    """
    tensor shape: [len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3,]
    """

    rank = one_hot(enum_to_index(Rank)[card.rank])
    suit = one_hot(enum_to_index(Suit)[card.suit])

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

    return torch.cat([rank, suit, enhancement, seal, edition, extra_chips, is_debuffed, is_face_down], dim=0)

def encode(run: Run) -> torch.FloatTensor:
    ante = encode_int(run.ante)
    ante_tags = encode_ante_tags(run.ante_tags)

    blind = encode_blind(run.blind)
    blind_reward = torch.tensor([float(run.blind_reward)], dtype=torch.float32)
    boss_blind = encode_blind(run.boss_blind)
    consumable_slots = encode_int(run.consumable_slots)
    consumables = encode_consumables(run.consumables)
    if run.hand is None:
        hand_cards = torch.zeros(max_hand_cards*(len(Rank)+len(Suit)+len(Enhancement)+len(Seal)+len(Edition)+3))
    else:
        hand_cards = encode_cards(run.hand, max_hand_cards)
    deck_cards_left = encode_cards(run.deck_cards_left, max_deck_cards)
    discards = encode_int(run.discards)
    if run.hands is None:
        hands = encode_int(0)
    else:
        hands = encode_int(run.hands)


    parts = [ante, ante_tags, blind, blind_reward, boss_blind, consumable_slots, consumables, hand_cards, deck_cards_left, discards, hands]
    return torch.cat(parts, dim=0)
