from collections import defaultdict
from typing import Optional

import numpy as np
import torch
import tqdm
from tensordict import TensorDict, TensorDictBase
from tensordict.nn import TensorDictModule
from torch import nn
from enum import Enum
from encode import *
from torchrl.data import Composite, Categorical
from torchrl.envs import (
    EnvBase,
)
from balatro import Deck, Stake, Run

class ActionType(Enum):
    SELECT_BLIND = 0
    SKIP_BLIND = 1
    REROLL_BOSS_BLIND = 2
    PLAY_HAND = 3
    DISCARD_HAND = 4
    CASH_OUT = 5
    MOVE_JOKER = 6
    SELL_JOKER = 7
    USE_CONSUMABLE = 8
    SELL_CONSUMABLE = 9
    BUY_SHOP_CARD = 10
    REDEEM_SHOP_VOUCHER = 11
    OPEN_SHOP_PACK = 12
    REROLL = 13
    NEXT_ROUND = 14
    CHOOSE_PACK_ITEM = 15
    SKIP_PACK = 16

class BalatroEnv(EnvBase):
    batch_locked = False

    def __init__(self, td_params=None, seed=None, device="cpu"):
        super().__init__(device=device, batch_size=[])
        self.run = Run(Deck.RED, stake=Stake.WHITE) if seed is None else Run(Deck.RED, stake=Stake.WHITE, seed=seed)
        self.observation_spec = Composite(
            observation=torch.empty(9645, dtype=torch.float32)
        )
        self.action_spec = Composite(
            {
                "action_type": Categorical(17, shape=(1,), dtype=torch.int64),
                "param1": Categorical(20, shape=(1,), dtype=torch.int64),
                "param2": Categorical(20, shape=(1,), dtype=torch.int64),
            }
        )
        self.reward_spec = Composite(
            reward=torch.empty(1)
        )
        self.done_spec = Composite(
            done=torch.empty(1, dtype=torch.bool),
            terminated=torch.empty(1, dtype=torch.bool),
        )

    def _reset(self, tensordict: TensorDict | None = None, **kwargs) -> TensorDict:
        self.run = Run(Deck.RED, stake=Stake.WHITE)
        obs = encode(self.run)
        return TensorDict(
            {
                "observation": obs,
                "reward": torch.zeros(1),
                "done": torch.zeros(1, dtype=torch.bool),
                "terminated": torch.zeros(1, dtype=torch.bool),
            },
            batch_size=[]
        )

    def _step(self, tensordict: TensorDict) -> TensorDict:
        action = tensordict["action"]
        action_type = action[0].item()
        param1 = action[1].item()
        param2 = action[2].item()

        try:
            if action_type == ActionType.SELECT_BLIND.value:
                self.run.select_blind()
            elif action_type == ActionType.SKIP_BLIND.value:
                self.run.skip_blind()
            elif action_type == ActionType.REROLL_BOSS_BLIND.value:
                self.run.reroll_boss_blind()
            elif action_type == ActionType.PLAY_HAND.value:
                self.run.play_hand([param1, param2])
            elif action_type == ActionType.DISCARD_HAND.value:
                self.run.discard([param1, param2])
            elif action_type == ActionType.CASH_OUT.value:
                self.run.cash_out()
            elif action_type == ActionType.MOVE_JOKER.value:
                self.run.move_joker(param1, param2)
            elif action_type == ActionType.SELL_JOKER.value:
                self.run.sell_joker(param1)
            elif action_type == ActionType.USE_CONSUMABLE.value:
                self.run.use_consumable(param1, [param2])
            elif action_type == ActionType.SELL_CONSUMABLE.value:
                self.run.sell_consumable(param1)
            elif action_type == ActionType.BUY_SHOP_CARD.value:
                self.run.buy_shop_card(param1, bool(param2))
            elif action_type == ActionType.REDEEM_SHOP_VOUCHER.value:
                self.run.redeem_shop_voucher(param1)
            elif action_type == ActionType.OPEN_SHOP_PACK.value:
                self.run.open_shop_pack(param1)
            elif action_type == ActionType.REROLL.value:
                self.run.reroll()
            elif action_type == ActionType.NEXT_ROUND.value:
                self.run.next_round()
            elif action_type == ActionType.CHOOSE_PACK_ITEM.value:
                self.run.choose_pack_item(param1)
            elif action_type == ActionType.SKIP_PACK.value:
                self.run.skip_pack()
            else:
                print(f"[WARNING] Unknown action_type: {action_type}")
        except Exception as e:
            print(f"[STEP ERROR] {ActionType(action_type).name}({param1}, {param2}) → {e}")

        obs = encode(self.run)
        reward = torch.tensor([0.0])
        done = torch.zeros(1, dtype=torch.bool)

        return TensorDict(
            {
                "observation": obs,
                "reward": reward,
                "done": done,
                "terminated": done,
            },
            batch_size=[],
        )

    def _set_seed(self, seed: int):
        self._seed = seed
        return seed