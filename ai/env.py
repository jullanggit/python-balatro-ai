from encode import _enum_to_index
import torch
from tensordict import TensorDict, TensorDictBase
from torch import nn, Tensor
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
import json
import uuid

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
    NO_OP = 17

# see __init__ for an explanation
PARAM1_LENGTH = max(MAX_HAND_CARDS, MAX_JOKERS, MAX_CONSUMABLES, MAX_SHOP_CARDS, MAX_SHOP_VOUCHERS, MAX_SHOP_PACKS, MAX_PACK_ITEMS)
PARAM2_LENGTH = max(MAX_JOKERS, 2, 1)

class BalatroEnv(EnvBase):
    batch_locked = False

    def __init__(self, worker_id: int, td_params=None, seed=None, device="cpu"):
        super().__init__(device=device, batch_size=[])
        self.worker_id = worker_id
        self.seed = seed
        self._init_run()
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

    def _init_run(self):
        """
        initializes run and logging
        """
        self.run = Run(Deck.RED, stake=Stake.WHITE, seed=self.seed)
        os.makedirs("runs", exist_ok=True)
        # unique filename
        self.replay_file = os.path.join(
            "runs", f"replay_{uuid.uuid4().hex}.jsonl"
        )
        open(self.replay_file, 'w').close()
        self.total_reward = 0.0


    def _reset(self, tensordict: TensorDict | None = None, **kwargs) -> TensorDict:
        self._init_run()
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

        # log actions
        record = {"action_type": action_type, "param1": tensordict["param1"].tolist(), "param2": tensordict["param2"].tolist()}
        with open(self.replay_file, 'a') as f:
            f.write(json.dumps(record) + "\n")

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
                # TODO: fix math domain error
                if self.run.state != State.PLAYING_BLIND:
                    if self.run.round_score > 0 and self.run.round_goal > 0:
                        # calculate score-based reward
                        # TODO: maybe add back /round_goal, as it does serve as a good cross-ante normalization,
                        #  but this returns negative rewards when not beating the round, which we dont want during early training
                        reward = 14.43 * math.log(self.run.round_score)
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
            elif action_type == ActionType.NO_OP.value:
                pass
            else:
                print(f"[WARNING] Unknown action_type: {action_type}")
                # negative reward for illegal choice
                reward = -5.0
        except Exception as e:
            # negative reward for illegal choice
            print(f"[STEP ERROR] {ActionType(action_type).name}({param1}, {param2}) → {e}")
            reward = -5.0

        obs = encode(self.run)
        done = self.run.state == State.GAME_OVER

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

    def snapshot(self) -> dict:
        return {
            "device": self.device,
            # action type
            "state": self.run.state,
            "len_jokers": len(self.run.jokers),
            "len_consumables": len(self.run.consumables),
            "can_reroll": self.run.reroll_cost is not None and self.run._available_money > self.run.reroll_cost,
            "can_discard": self.run.discards > 0,
            "can_skip_blind": self.run.blind == Blind.SMALL_BLIND or self.run.blind == Blind.BIG_BLIND,
            "can_reroll_boss_blind": (Voucher.DIRECTORS_CUT in self.run.vouchers or (Voucher.RETCON in self.run.vouchers and not self._rerolled_boss_blind)) and self._available_money >= 10,
            # param1
            "len_hand_cards": None if self.run.hand is None else len(self.run.hand),
            "forced_selected_card_index": self.run.forced_selected_card_index,
            "len_pack_items": None if self.run.pack_items is None else len(self.run.pack_items),
            # dont use tensors so we can send snapshots across threads
            "buyable_shop_cards_mask": [
                (cost <= self.run._available_money)
                for _, cost in (self.run.shop_cards or [])
            ],
            "buyable_shop_vouchers_mask": [
                (cost <= self.run._available_money)
                for _, cost in (self.run.shop_vouchers or [])
            ],
            "buyable_shop_packs_mask": [
                (cost <= self.run._available_money)
                for _, cost in (self.run.shop_packs or [])
            ],
        }



    def shop_item_mask(self, items) -> Tensor:
        mask = torch.zeros(PARAM1_LENGTH, dtype=torch.bool)
        if items is not None:
            for i, card in enumerate(items):
                _, cost = card
                if cost <= self.run._available_money:
                    mask[i] = True
        return mask

def add_action_types(mask, action_type: set):
    for elem in action_type:
        mask[elem.value] = True

def get_legal_action_type(snapshots):
    """
    takes an iterable of snapshot dicts
    returns a tensor of masks for legal actions (1 = legal, 0 = illegal)
    """
    masks = []
    for i, snapshot in enumerate(snapshots):
        device = snapshot["device"]

        move_and_sell = torch.zeros(len(ActionType), dtype=torch.bool, device=device)
        if snapshot["len_jokers"] > 0:
            add_action_type(move_and_sell, ActionType.SELL_JOKER)
        if snapshot["len_jokers"] > 1:
            add_action_type(move_and_sell, ActionType.MOVE_JOKER)
        if snapshot["len_consumables"] > 0:
            add_action_type(move_and_sell, ActionType.SELL_CONSUMABLE)
            add_action_type(move_and_sell, ActionType.USE_CONSUMABLE)

        # only allow no-op
        if snapshot["state"] == State.GAME_OVER:
            masks.append(torch.nn.functional.one_hot(torch.tensor(ActionType.NO_OP.value), len(ActionType)).to(torch.bool).to(device))
        elif snapshot["state"] == State.CASHING_OUT:
            masks.append(torch.nn.functional.one_hot(torch.tensor(ActionType.CASH_OUT.value), len(ActionType)).to(torch.bool).to(device))
        elif snapshot["state"] == State.IN_SHOP:
            in_shop = move_and_sell.detach().clone()
            add_action_type(in_shop, ActionType.NEXT_ROUND)

            if snapshot["buyable_shop_cards_mask"].any():
                add_action_type(in_shop, ActionType.BUY_SHOP_CARD)
            if snapshot["buyable_shop_vouchers_mask"].any():
                add_action_type(in_shop, ActionType.REDEEM_SHOP_VOUCHER)
            if snapshot["buyable_shop_packs_mask"].any():
                add_action_type(in_shop, ActionType.OPEN_SHOP_PACK)
            if snapshot["can_reroll"]:
                add_action_type(in_shop, ActionType.REROLL)

            masks.append(in_shop)
        elif snapshot["state"] == State.OPENING_PACK:
            opening_pack = move_and_sell.detach().clone()
            add_action_types(opening_pack, {
                ActionType.CHOOSE_PACK_ITEM, ActionType.SKIP_PACK
            })
            masks.append(opening_pack)
        elif snapshot["state"] == State.PLAYING_BLIND:
            playing_blind = move_and_sell.detach().clone()
            add_action_type(playing_blind, ActionType.PLAY_HAND) # if we haven't lost, we can always play a hand during a blind
            if snapshot["can_discard"]:
                add_action_type(playing_blind, ActionType.DISCARD_HAND)

            masks.append(playing_blind)
        elif snapshot["state"] == State.SELECTING_BLIND:
            selecting_blind = move_and_sell.detach().clone()
            add_action_type(selecting_blind, ActionType.SELECT_BLIND)
            if snapshot["can_skip_blind"]:
                add_action_type(selecting_blind, ActionType.SKIP_BLIND)

            if snapshot["can_reroll_boss_blind"]:
                add_action_type(selecting_blind, ActionType.REROLL_BOSS_BLIND)

            masks.append(selecting_blind)
        else:
            raise Exception("shouldnt happen")

        if masks[i].sum() == 0:
            print(snapshot)
            raise Exception("there should always be a legal action")

    return torch.stack(masks, dim=0)

def get_legal_param1(snapshots):
    """
    takes an iterable of snapshots
    returns a tensor of (mask, min_samples, max_samples)
    """
    masks, min_samples, max_samples = [], [], []
    def append(mask, min, max):
        masks.append(mask)
        min_samples.append(min)
        max_samples.append(max)

    for i, snapshot in enumerate(snapshots):
        action = snapshot["action"]
        device = snapshot["device"]

        if action == ActionType.NO_OP:
            # allow everything
            append(torch.ones(PARAM1_LENGTH, dtype=torch.bool, device=device), 0, PARAM1_LENGTH)
        elif action == ActionType.PLAY_HAND or action == ActionType.DISCARD_HAND:
            max_sample = 5

            len_hand_cards = snapshot["len_hand_cards"]
            mask = set_until(len_hand_cards, PARAM1_LENGTH, device)

            if snapshot["forced_selected_card_index"] is not None:
                max_sample = 4
                mask[snapshot["forced_selected_card_index"]] = False
            append(mask, 1, max_sample)

        elif action == ActionType.MOVE_JOKER or action == ActionType.SELL_JOKER:
            # TODO: handle eternal jokers for selling
            append(set_until(snapshot["len_jokers"], PARAM1_LENGTH, device), 1, 1)
        elif action == ActionType.USE_CONSUMABLE or action == ActionType.SELL_CONSUMABLE:
            # TODO: handle non-usable consumables (judgement, ankh etc., see below)
            append(set_until(snapshot["len_consumables"], PARAM1_LENGTH, device), 1, 1)
        elif action == ActionType.BUY_SHOP_CARD:
            append(snapshot["buyable_shop_cards_mask"], 1, 1)
        elif action == ActionType.REDEEM_SHOP_VOUCHER:
            append(snapshot["buyable_shop_vouchers_mask"], 1, 1)
        elif action == ActionType.OPEN_SHOP_PACK:
            append(snapshot["buyable_shop_packs_mask"], 1, 1)
        elif action == ActionType.CHOOSE_PACK_ITEM:
            # TODO: handle non-usable cards (jokers/judgement when joker slots full, ankh when empty, etc.)
            append(set_until(snapshot["len_pack_items"], PARAM1_LENGTH, device), 1, 1)
        else:
            append(torch.ones(PARAM1_LENGTH, dtype=torch.bool, device=device), 0, PARAM1_LENGTH)

        if masks[i].sum() == 0:
            print(snapshot)
            raise Exception("there should always be a legal param1 configuration")

    return (torch.stack(masks, dim=0), torch.Tensor(min_samples), torch.Tensor(max_samples))

def get_legal_param2(snapshots):
    """
    takes an iterable of snapshots
    returns a tensor of (mask, min_samples, max_samples)
    """
    masks, min_samples, max_samples = [], [], []
    def append(mask, min, max):
        masks.append(mask)
        min_samples.append(min)
        max_samples.append(max)

    for i, snapshot in enumerate(snapshots):
        action = snapshot["action"]
        device = snapshot["device"]
        #param1 = snapshot["param1"]

        # used as index/indices for:
        #   whether a bought shop item should be used
        if action == ActionType.NO_OP:
            # allow everything
            append(torch.ones(PARAM2_LENGTH, dtype=torch.bool, device=device), 0, PARAM2_LENGTH)
        elif action == ActionType.MOVE_JOKER:
            # TODO: handle eternal jokers for selling
            # TODO: maybe exclude param1 joker
            append(set_until(snapshot["len_jokers"], PARAM2_LENGTH, device), 1, 1)
        elif action == ActionType.USE_CONSUMABLE:
            # TODO: actually set min and max_samples and respect the used consumable
            append(set_until(snapshot["len_hand_cards"], PARAM2_LENGTH, device), 1, 3)
        elif action == ActionType.BUY_SHOP_CARD:
            # bool and_use
            append(torch.nn.functional.one_hot(torch.tensor(1), PARAM2_LENGTH).to(torch.bool).to(device), 0, 1)
        else:
            append(torch.ones(PARAM2_LENGTH, dtype=torch.bool, device=device), 0, PARAM2_LENGTH)

        if masks[i].sum() == 0:
            print(snapshot)
            raise Exception("there should always be a legal param2 configuration")

    return (torch.stack(masks, dim=0), torch.Tensor(min_samples), torch.Tensor(max_samples))

def set_until(set_until, total_len, device):
    mask = torch.zeros(total_len, dtype=torch.bool, device=device)
    mask[:set_until] = True
    return mask


def add_action_type(mask, action_type: ActionType):
    mask[action_type.value] = True
