import torch
from balatro import *

max_consumables = 20

blind_to_index = {blind: idx for idx, blind in enumerate(Blind)}
tag_to_index = {tag: idx for idx, tag in enumerate(Tag)}
hand_to_index = {hand: idx for idx, hand in enumerate(PokerHand)}

tarot_to_index = {tarot: idx for idx, tarot in enumerate(Tarot)}
planet_to_index = {planet: idx for idx, planet in enumerate(Planet)}
spectral_to_index = {spectral: idx for idx, spectral in enumerate(Spectral)}

card_to_index = {**tarot_to_index, **planet_to_index, **spectral_to_index}

def one_hot(index: int, num_classes: int) -> torch.FloatTensor:
    return torch.nn.functional.one_hot(torch.tensor(index), num_classes=num_classes).float()


def encode_ante_tags(ante_tags: list[tuple[Tag, PokerHand | None]]) -> torch.FloatTensor:
    encoded = []
    for i in range(0, 2):
        tag, hand = ante_tags[i]
        tag_encoded = one_hot(tag_to_index[tag], len(Tag))

        if hand is None:
            hand_encoded = torch.zeros(len(PokerHand), dtype=torch.float32)
        else:
            hand_encoded = one_hot(hand_to_index[hand], len(PokerHand))

        encoded.append(torch.cat([tag_encoded, hand_encoded]))

    return torch.cat(encoded, dim=0)

def encode_blind(blind: Blind) -> torch.FloatTensor:
    return one_hot(blind_to_index[blind], len(Blind))

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


def encode(run: Run) -> torch.FloatTensor:
    ante = encode_int(run.ante)
    ante_tags = encode_ante_tags(run.ante_tags)

    blind = encode_blind(run.blind)
    blind_reward = torch.tensor([float(run.blind_reward)], dtype=torch.float32)
    boss_blind = encode_blind(run.boss_blind)
    consumable_slots = encode_int(run.consumable_slots)
    consumables = encode_consumables(run.consumables)

    parts = [ante, ante_tags, blind, blind_reward, boss_blind, consumable_slots, consumables]
    return torch.cat(parts, dim=0)
