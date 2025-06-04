import torch
from balatro import *

blind_to_index = {blind: idx for idx, blind in enumerate(Blind)}
tag_to_index = {tag: idx for idx, tag in enumerate(Tag)}
hand_to_index = {hand: idx for idx, hand in enumerate(PokerHand)}

def one_hot(index: int, num_classes: int) -> torch.Tensor:
    return torch.nn.functional.one_hot(torch.tensor(index), num_classes=num_classes).float()


def encode_ante_tags(ante_tags: list[tuple[Tag, PokerHand | None]]) -> torch.Tensor:
    encoded = []
    for i in range(0, 2):
        tag, hand = ante_tags[i]
        tag_encoded = one_hot(tag_to_index[tag], len(Tag))

        num_hands = len(PokerHand) + 1 # +1 for None
        if hand is None:
            hand_encoded = one_hot(num_hands-1, num_hands)
        else:
            hand_encoded = one_hot(hand_to_index[hand], num_hands)

        encoded.append(torch.cat([tag_encoded, hand_encoded]))

    return torch.cat(encoded, dim=0)

def encode_blind(blind: Blind) -> torch.Tensor:
    return one_hot(blind_to_index[blind], len(Blind))

def encode_int(int: int) -> torch.Tensor:
    return torch.tensor([float(int)], dtype=torch.float32)

# def encode_consumables(consumables: list[Consumable]) -> torch.Tensor:

def encode(run: Run) -> torch.Tensor:
    ante = encode_int(run.ante)
    ante_tags = encode_ante_tags(run.ante_tags)

    blind = encode_blind(run.blind)
    blind_reward = torch.tensor([float(run.blind_reward)], dtype=torch.float32)
    boss_blind = encode_blind(run.boss_blind)
    consumable_slots = encode_int(run.consumable_slots)

    parts = [ante, ante_tags, blind, blind_reward, boss_blind, consumable_slots]
    return torch.cat(parts, dim=0)
