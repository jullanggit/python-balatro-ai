from collections import defaultdict
from typing import Optional

import numpy as np
import torch
import tqdm
from tensordict import TensorDict, TensorDictBase
from tensordict.nn import TensorDictModule
from torch import nn
from enum import Enum

from torchrl.data import Bounded, Composite, Unbounded
from torchrl.envs import (
    CatTensors,
    EnvBase,
    Transform,
    TransformedEnv,
    UnsqueezeTransform,
)
from torchrl.envs.transforms.transforms import _apply_to_composite
from torchrl.envs.utils import check_env_specs, step_mdp
from balatro import Deck, Stake, Run

class BalatroEnv(EnvBase):
    batch_locked = False

    def __init__(self, td_params=None, seed=None, device="cpu"):
        super().__init__(device=device, batch_size=[])
        self.run = Run(Deck.RED, stake=Stake.WHITE, seed=seed)

    def _reset():
        raise Exception("not implemented")
    def _step(self, tensordict: TensorDict):
        action = tensordict["action"]
        # action = tensordict["action"]
        raise Exception("not implemented")
    def _set_seed():
        raise Exception("not implemented")

class ActionType(Enum):
    SELECT_BLIND = 0
    SKIP_BLIND = 1
    REROLL_BOSS_BLIND = 2
    PLAY_HAND = 3 # + indices to play
    DISCARD_HAND = 4 # + indices to discard
    CASH_OUT = 5
    MOVE_JOKER = 6 # + indices to be switched
    SELL_JOKER = 7 # + index to be sold
    USE_CONSUMABLE = 8 # + index to use + indices to be used on
    SELL_CONSUMABLE = 9 # + index to be sold
    BUY_SHOP_CARD = 10 # + index to be bought + whether to instantly use
    REDEEM_SHOP_VOUCHER = 11 # + index to be bought
    OPEN_SHOP_PACK = 12 # + index to be bought
    REROLL = 13
    NEXT_ROUND = 14
    CHOOSE_PACK_ITEM = 15 # + index to choose
    SKIP_PACK = 16

class Action:
    type: ActionType
    data: list[int]
