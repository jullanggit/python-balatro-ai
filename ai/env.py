import torch
from tensordict import TensorDict, TensorDictBase
from torch import nn
from enum import Enum
from encode import *
from torchrl.data import Composite, Categorical, Binary
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

# see __init__ for an explanation
PARAM1_LENGTH = max(MAX_HAND_CARDS, MAX_JOKERS, MAX_CONSUMABLES, MAX_SHOP_CARDS, MAX_SHOP_VOUCHERS, MAX_SHOP_PACKS) # TODO: add MAX_PACK_ITEMS to max()
PARAM2_LENGTH = max(MAX_JOKERS, 2, 1)

class BalatroEnv(EnvBase):
    batch_locked = False

    def __init__(self, td_params=None, seed=None, device="cpu"):
        super().__init__(device=device, batch_size=[])
        self.seed = seed
        self.run = Run(Deck.RED, stake=Stake.WHITE, seed=seed)
        self.observation_spec = Composite(
            observation=torch.empty(SIZE_ENCODED, dtype=torch.float32)
        )
        self.action_spec = Composite(
            {
                "action_type": Categorical(len(ActionType)),
                # used as index/indices for:
                #   hand cards (play_hand/discard)
                #   jokers (move_joker/sell_joker)
                #   consumables (use_consumable/sell_consumable)
                #   shop slots (buy_shop_card)
                #   shop vouchers (redeem_shop_voucher)
                #   shop packs (open_shop_pack)
                #   pack choices (choose_pack_item)
                "param1": Binary(PARAM1_LENGTH),
                # used as index/indices for:
                #   jokers (move_joker)
                #   consumable arguments (use_consumable)
                #   whether a bought shop item should be used
                "param2": Binary(PARAM2_LENGTH), # longest is useconsumable, which's second param has a max length of 2
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
        self.run = Run(Deck.RED, stake=Stake.WHITE, seed=self.seed)
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
        action_type = action["action_type"].item()
        param1_mask = action["param1"].squeeze().to(torch.bool)
        param1 = torch.arange(PARAM1_LENGTH)[param1_mask].tolist()
        param2_mask = action["param2"].squeeze().to(torch.bool)
        param2 = torch.arange(PARAM2_LENGTH)[param2_mask].tolist()

        reward = torch.tensor([0.0])

        # TODO: handle incorrect actions/params (with negative reward)
        try:
            if action_type == ActionType.SELECT_BLIND.value:
                self.run.select_blind()
            elif action_type == ActionType.SKIP_BLIND.value:
                self.run.skip_blind()
            elif action_type == ActionType.REROLL_BOSS_BLIND.value:
                self.run.reroll_boss_blind()
            elif action_type == ActionType.PLAY_HAND.value:
                self.run.play_hand(param1)
            elif action_type == ActionType.DISCARD_HAND.value:
                self.run.discard(param1)
            elif action_type == ActionType.CASH_OUT.value:
                self.run.cash_out()
            elif action_type == ActionType.MOVE_JOKER.value:
                self.run.move_joker(param1[0], param2[0])
            elif action_type == ActionType.SELL_JOKER.value:
                self.run.sell_joker(param1[0])
            elif action_type == ActionType.USE_CONSUMABLE.value:
                self.run.use_consumable(param1[0], param2)
            elif action_type == ActionType.SELL_CONSUMABLE.value:
                self.run.sell_consumable(param1[0])
            elif action_type == ActionType.BUY_SHOP_CARD.value:
                self.run.buy_shop_card(param1[0], bool(param2))
            elif action_type == ActionType.REDEEM_SHOP_VOUCHER.value:
                self.run.redeem_shop_voucher(param1[0])
            elif action_type == ActionType.OPEN_SHOP_PACK.value:
                self.run.open_shop_pack(param1[0])
            elif action_type == ActionType.REROLL.value:
                self.run.reroll()
            elif action_type == ActionType.NEXT_ROUND.value:
                self.run.next_round()
            elif action_type == ActionType.CHOOSE_PACK_ITEM.value:
                self.run.choose_pack_item(param1[0])
            elif action_type == ActionType.SKIP_PACK.value:
                self.run.skip_pack()
            else:
                print(f"[WARNING] Unknown action_type: {action_type}")
                # negative reward for illegal choice
                reward = torch.tensor([-5])
        except Exception as e:
            # negative reward for illegal choice
            print(f"[STEP ERROR] {ActionType(action_type).name}({param1}, {param2}) → {e}")
            reward = torch.tensor([-5])

        obs = encode(self.run)
        # TODO: actually do this
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
