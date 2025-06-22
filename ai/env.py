from encode import _enum_to_index
import torch
from tensordict import TensorDict, TensorDictBase
from torch import nn
from enum import Enum
from encode import *
from torchrl.data import Composite, Categorical, Binary
from torchrl.envs import (
    EnvBase,
)
from torchrl.data.tensor_specs import UnboundedContinuous
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from balatro import Deck, Stake, Run
from encode import one_hot
import math

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
PARAM1_LENGTH = max(MAX_HAND_CARDS, MAX_JOKERS, MAX_CONSUMABLES, MAX_SHOP_CARDS, MAX_SHOP_VOUCHERS, MAX_SHOP_PACKS, MAX_PACK_ITEMS)
PARAM2_LENGTH = max(MAX_JOKERS, 2, 1)

class BalatroEnv(EnvBase):
    batch_locked = False

    def __init__(self, td_params=None, seed=None, device="cpu"):
        super().__init__(device=device, batch_size=[])
        self.seed = seed
        self.run = Run(Deck.RED, stake=Stake.WHITE, seed=seed)
        self.observation_spec = Composite(
             observation=UnboundedContinuous(
                 shape=(SIZE_ENCODED,),
                 device=device,
                 dtype=torch.float32,
             )
        )
        self.action_spec = Composite(
            action_type = Categorical(len(ActionType)),
            # used as index/indices for:
            #   hand cards (play_hand/discard)
            #   jokers (move_joker/sell_joker)
            #   consumables (use_consumable/sell_consumable)
            #   shop slots (buy_shop_card)
            #   shop vouchers (redeem_shop_voucher)
            #   shop packs (open_shop_pack)
            #   pack choices (choose_pack_item)
            param1 = Binary(PARAM1_LENGTH),
            # used as index/indices for:
            #   jokers (move_joker)
            #   consumable arguments (use_consumable)
            #   whether a bought shop item should be used
            param2 = Binary(PARAM2_LENGTH), # longest is useconsumable, which's second param has a max length of 2
        )
        self.reward_spec = Composite(
            reward=UnboundedContinuous(
                shape=(1,),
                device=device,
                dtype=torch.float32,
            )
        )
        self.done_spec = Composite(
            done=Binary(1),
            terminated=Binary(1)
        )
        self.total_reward = 0.0

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
        action_type = tensordict["action_type"].item()
        param1_mask = tensordict["param1"].squeeze().to(torch.bool)
        param1 = torch.arange(PARAM1_LENGTH, device=param1_mask.device)[param1_mask].tolist()
        param2_mask = tensordict["param2"].squeeze().to(torch.bool)
        param2 = torch.arange(PARAM2_LENGTH, device=param2_mask.device)[param2_mask].tolist()

        reward: float = 0.0

        # TODO: handle incorrect actions/params (with negative reward)
        try:
            if action_type == ActionType.SELECT_BLIND.value:
                self.run.select_blind()
            elif action_type == ActionType.SKIP_BLIND.value:
                self.run.skip_blind()
            elif action_type == ActionType.REROLL_BOSS_BLIND.value:
                self.run.reroll_boss_blind()
            elif action_type == ActionType.PLAY_HAND.value:
                blind = self.run.blind
                self.run.play_hand(param1)
                if self.run.state != State.PLAYING_BLIND:
                    # calculate score-based reward
                    reward = 14.43 * math.log(self.run.round_score/self.run.round_goal)
                    # if round won
                    if self.run.state == State.CASHING_OUT:
                        # add blind reward
                        if blind == Blind.SMALL_BLIND:
                            reward += 10.0
                        elif blind == Blind.BIG_BLIND:
                            reward += 15.0
                        # boss blind
                        else:
                            reward += 20.0
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
                reward = -5.0
        except Exception as e:
            # negative reward for illegal choice
            print(f"[STEP ERROR] {ActionType(action_type).name}({param1}, {param2}) → {e}")
            reward = -5.0

        obs = encode(self.run)
        done = False

        self.total_reward += reward
        # double total_reward on win
        if self.run.ante == 9:
           reward += self.total_reward
           done = True

        return TensorDict(
            {
                "observation": obs,
                "reward": torch.tensor([reward]),
                "done": torch.tensor([done], dtype=torch.bool),
                "terminated": torch.tensor([done], dtype=torch.bool),
            },
            batch_size=[],
        )

    def _set_seed(self, seed: int):
        self._seed = seed
        return seed

    def get_legal_action_type(self):
        """
        returns a mask for legal actions (1 = legal, 0 = illegal)
        """
        move_and_sell = torch.zeros(len(ActionType), dtype=torch.bool)
        if len(self.run.jokers) > 0:
            add_action_type(move_and_sell, ActionType.SELL_JOKER)
        if len(self.run.jokers) > 1:
            add_action_type(move_and_sell, ActionType.MOVE_JOKER)
        if len(self.run.consumables) > 0:
            add_action_type(move_and_sell, ActionType.SELL_CONSUMABLE)
            add_action_type(move_and_sell, ActionType.USE_CONSUMABLE)

        if self.run.state == State.CASHING_OUT:
            return torch.nn.functional.one_hot(ActionType.CASH_OUT, len(ActionType), dtype=torch.bool)
        elif self.run.state == State.IN_SHOP:
            in_shop = move_and_sell.detach().clone()
            if self.run.shop_cards is not None and len(self.run.shop_cards) > 0:
                add_action_type(in_shop, ActionType.BUY_SHOP_CARD)
            if self.run.shop_vouchers is not None and len(self.run.shop_vouchers) > 0:
                add_action_type(in_shop, ActionType.REDEEM_SHOP_VOUCHER)
            if self.run.shop_packs is not None and len(self.run.shop_packs) > 0:
                add_action_type(in_shop, ActionType.OPEN_SHOP_PACK)
            if self.reroll_cost is not None and self.run._available_money > self.run.reroll_cost:
                add_action_type(in_shop, ActionType.REROLL)

            return in_shop
        elif self.run.state == State.OPENING_PACK:
            opening_pack = move_and_sell.detach().clone()
            add_action_types(opening_pack, {
                ActionType.CHOOSE_PACK_ITEM, ActionType.SKIP_PACK
            })
            return opening_pack
        elif self.run.state == State.PLAYING_BLIND:
            playing_blind = move_and_sell.detach().clone()
            add_action_type(playing_blind, ActionType.PLAY_HAND) # if we haven't lost, we can always play a hand during a blind
            if self.run.discards > 0:
                add_action_type(playing_blind, ActionType.DISCARD_HAND)

            return playing_blind
        elif self.run.state == State.SELECTING_BLIND:
            selecting_blind = move_and_sell.detach().clone()
            add_action_type(selecting_blind, ActionType.SELECT_BLIND)
            if self.run.blind == Blind.SMALL_BLIND or self.run.blind == Blind.BIG_BLIND:
                add_action_type(selecting_blind, ActionType.SKIP_BLIND)

            if (Voucher.DIRECTORS_CUT in self.run.vouchers or (Voucher.RETCON in self.run.vouchers and not self._rerolled_boss_blind)) and self._available_money >= 10:
                add_action_type(selecting_blind, ActionType.REROLL_BOSS_BLIND)

            return selecting_blind
    def get_legal_param1(self, action: ActionType):
        # used as index/indices for:
        #   hand cards (play_hand/discard)
        #   jokers (move_joker/sell_joker)
        #   consumables (use_consumable/sell_consumable)
        #   shop slots (buy_shop_card)
        #   shop vouchers (redeem_shop_voucher)
        #   shop packs (open_shop_pack)
        #   pack choices (choose_pack_item)
        if action == ActionType.PLAY_HAND or action == ActionType.DISCARD_HAND:
            # TODO: handle force-selected card
            len_hand_cards = len(self.run.hand)
            return set_until(len_hand_cards, PARAM1_LENGTH)
        elif action == ActionType.MOVE_JOKER or action == ActionType.SELL_JOKER:
            # TODO: handle eternal jokers for selling
            return set_until(len(self.run.jokers), PARAM1_LENGTH)
        elif action == ActionType.USE_CONSUMABLE or action == ActionType.SELL_CONSUMABLE:
            return set_until(len(self.run.consumables), PARAM1_LENGTH)
        elif action == ActionType.BUY_SHOP_CARD:
            mask = torch.zeros(PARAM1_LENGTH, dtype=torch.bool)
            if self.run.shop_cards is not None:
                for i, card in enumerate(self.run.shop_cards):
                    _, cost = card
                    if cost <= self.run._available_money:
                        mask[i] = True
            return mask


def set_until(set_until, total_len):
    mask = torch.zeros(total_len, dtype=torch.bool)
    mask[:set_until] = True
    return mask


def add_action_type(mask, action_type: ActionType):
    mask[action_type.value] = True

def add_action_types(mask, action_type: set):
    for elem in action_type:
        mask[elem.value] = True
