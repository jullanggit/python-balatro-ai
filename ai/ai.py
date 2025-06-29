# This file is a modified version of the ppo implementation from CleanRL (https://github.com/vwxyzjn/cleanrl) and is licensed under the MIT License
#
# MIT License
#
# Copyright (c) 2019 CleanRL developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import random
import time
from dataclasses import dataclass

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from env import BalatroEnv, get_legal_action_type, get_legal_param1, get_legal_param2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions import Categorical, Bernoulli
from torchrl.envs import ParallelEnv
import tyro
from tensordict import TensorDict, TensorDictBase
# from torch.utils.tensorboard import SummaryWriter
from env import ActionType, PARAM1_LENGTH, PARAM2_LENGTH


@dataclass
class Args:
    exp_name: str = os.path.basename(__file__)[: -len(".py")]
    """the name of this experiment"""
    seed: int | None = None
    """seed of the experiment"""
    torch_deterministic: bool = True
    """if toggled, `torch.backends.cudnn.deterministic=False`"""
    cuda: bool = True
    """if toggled, cuda will be enabled by default"""
    track: bool = False
    """if toggled, this experiment will be tracked with Weights and Biases"""
    wandb_project_name: str = "cleanRL"
    """the wandb's project name"""
    wandb_entity: str | None = None
    """the entity (team) of wandb's project"""
    capture_video: bool = False
    """whether to capture videos of the agent performances (check out `videos` folder)"""

    # Algorithm specific arguments
    total_timesteps: int = 500000
    """total timesteps of the experiments"""
    learning_rate: float = 2.5e-4
    """the learning rate of the optimizer"""
    num_envs: int = 4
    """the number of parallel game environments"""
    num_steps: int = 128
    """the number of steps to run in each environment per policy rollout"""
    anneal_lr: bool = True
    """Toggle learning rate annealing for policy and value networks"""
    gamma: float = 0.99
    """the discount factor gamma"""
    gae_lambda: float = 0.95
    """the lambda for the general advantage estimation"""
    num_minibatches: int = 4
    """the number of mini-batches"""
    update_epochs: int = 4
    """the K epochs to update the policy"""
    norm_adv: bool = True
    """Toggles advantages normalization"""
    clip_coef: float = 0.2
    """the surrogate clipping coefficient"""
    clip_vloss: bool = True
    """Toggles whether or not to use a clipped loss for the value function, as per the paper."""
    ent_coef: float = 0.01
    """coefficient of the entropy"""
    vf_coef: float = 0.5
    """coefficient of the value function"""
    max_grad_norm: float = 0.5
    """the maximum norm for the gradient clipping"""
    target_kl: float | None = None
    """the target KL divergence threshold"""

    # to be filled in runtime
    batch_size: int = 0
    """the batch size (computed in runtime)"""
    minibatch_size: int = 0
    """the mini-batch size (computed in runtime)"""
    num_iterations: int = 0
    """the number of iterations (computed in runtime)"""


def layer_init(layer, std=np.sqrt(2), bias_const=0.0):
    torch.nn.init.orthogonal_(layer.weight, std)
    torch.nn.init.constant_(layer.bias, bias_const)
    return layer

def network_head(in_size: int, out_size: int, std):
    return nn.Sequential(
        layer_init(nn.Linear(in_size, in_size//2)),
        nn.SiLU(),
        layer_init(nn.Linear(in_size//2, out_size), std=std)
    )

class Agent(nn.Module):
    def __init__(self, envs):
        HIDDEN_SIZE = 1024
        super().__init__()
        self.shared = nn.Sequential(
            layer_init(nn.Linear(int(envs.observation_spec["observation"].shape[-1]), HIDDEN_SIZE)),
            #nn.LayerNorm(HIDDEN_SIZE),
            nn.SiLU(),
            layer_init(nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)),
            #nn.LayerNorm(HIDDEN_SIZE),
            nn.SiLU(),
            layer_init(nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)),
            #nn.LayerNorm(HIDDEN_SIZE),
            nn.SiLU(),
            # layer_init(nn.Linear(HIDDEN_SIZE, HIDDEN_SIZE)),
            # #nn.LayerNorm(HIDDEN_SIZE),
            # nn.SiLU(),
        )

        # critic
        self.value_head = network_head(HIDDEN_SIZE, 1, 0.1)
        # actor heads
        self.action_type_head = network_head(HIDDEN_SIZE , len(ActionType), 0.01)
        # param1 additionally takes the chosen action as input
        self.param1_head = network_head(HIDDEN_SIZE + len(ActionType) , PARAM1_LENGTH, std=0.01)
        # param2 additionally takes the chosen param1 as input
        self.param2_head = network_head(HIDDEN_SIZE + len(ActionType) + PARAM1_LENGTH, PARAM2_LENGTH, std=0.01)

    def get_value(self, x):
        hidden = self.shared(x)
        return self.value_head(hidden)

    def get_action_and_value(self, observation, snapshot_list, action: TensorDict | None = None):
        NEG_INF = -1e9

        shared = self.shared(observation)

        # get and sample action type distribution, based on shared
        action_type_logits = self.action_type_head(shared)
        legal_action_type_mask = get_legal_action_type(snapshot_list).to(action_type_logits.device)

        masked_action_type_logits = action_type_logits.masked_fill(~legal_action_type_mask, NEG_INF)
        action_type_distribution = Categorical(logits=masked_action_type_logits)
        action_type = action_type_distribution.sample() if action is None else action["action_type"]

        # append sampled action type to snapshots_list
        for i, snapshot in enumerate(snapshot_list):
            snapshot["action"] = ActionType(action_type[i].item())

        # concatenate the chosen action type with the shared state
        action_type_one_hot = torch.nn.functional.one_hot(action_type, num_classes=len(ActionType)).float()
        action_shared = torch.cat([shared, action_type_one_hot], dim=1)

        # get legal param1's
        legal_param1_mask, param1_min_samples, param1_max_samples = get_legal_param1(snapshot_list)

        # get and sample param1 distribution, based on shared + action type
        param1_logits = self.param1_head(action_shared)
        legal_param1_mask = legal_param1_mask.to(param1_logits.device)

        masked_param1_logits = param1_logits.masked_fill(~legal_param1_mask, NEG_INF)
        param1_distribution = Bernoulli(logits=masked_param1_logits)
        param1 = constrained_bernoulli(masked_param1_logits, param1_min_samples, param1_max_samples) if action is None else action["param1"]

        #param2
        legal_param2_mask, param2_min_samples, param2_max_samples = get_legal_param2(snapshot_list)

        # get and sample param2 distribution, based on shared + action type
        param2_logits = self.param2_head(torch.cat([action_shared, param1], dim=1))
        legal_param2_mask = legal_param2_mask.to(param2_logits.device)

        masked_param2_logits = param2_logits.masked_fill(~legal_param2_mask, NEG_INF)
        param2_distribution = Bernoulli(logits=masked_param2_logits)
        param2 = constrained_bernoulli(masked_param2_logits, param2_min_samples, param2_max_samples) if action is None else action["param2"]

        # calculate log probabilities
        action_type_logprob = action_type_distribution.log_prob(action_type)
        param1_logprob = param1_distribution.log_prob(param1).sum(dim=-1)
        param2_logprob = param2_distribution.log_prob(param2).sum(dim=-1)
        total_logprob = action_type_logprob + param1_logprob + param2_logprob

        # calculate entropies
        action_type_entropy = action_type_distribution.entropy()
        param1_entropy = param1_distribution.entropy().sum(dim=-1)
        param2_entropy = param2_distribution.entropy().sum(dim=-1)
        total_entropy = action_type_entropy + param1_entropy + param2_entropy

        sampled_action = TensorDict({
            "action_type": action_type,
            "param1": param1,
            "param2": param2,
        }, batch_size=[observation.shape[0]])

        return sampled_action, total_logprob, total_entropy, self.value_head(shared)

def constrained_bernoulli(logits: torch.Tensor, min_ones: torch.Tensor, max_ones: torch.Tensor) -> torch.Tensor:
    """
    Sample from the Bernoulli Distribution, enforcing min and max ones
    """
    batch_size, _ = logits.shape

    dist = Bernoulli(logits=logits)
    sample = dist.sample()
    probabilities = torch.sigmoid(logits)

    for i in range(batch_size):
        num_ones = int(sample[i].sum().item())
        if num_ones > max_ones[i]:
            # disable low-probabilitie ones
            ones_index = sample[i].nonzero(as_tuple=True)[0]
            num_to_disable = int(num_ones - max_ones[i])
            disable_weight = 1.0 - probabilities[i, ones_index]

            # guard: if all weights are zero, fallback to uniform
            if disable_weight.sum().item() <= 0.0:
                disable_weight = torch.ones_like(disable_weight, device=disable_weight.device)

            choice = torch.multinomial(disable_weight, num_to_disable, replacement=False)
            sample[i, ones_index[choice]] = 0.0

        elif num_ones < min_ones[i]:
            # enable high-probability zeros
            zeros_index = (1.0 - sample[i]).nonzero(as_tuple=True)[0]
            num_to_enable = int(min_ones[i]- num_ones)
            enable_weight = probabilities[i, zeros_index]

            # guard: if all weights are zero, fallback to uniform
            if enable_weight.sum().item() <= 0.0:
                enable_weight = torch.ones_like(enable_weight, device=enable_weight.device)

            choice = torch.multinomial(enable_weight, num_to_enable, replacement=False)
            sample[i, zeros_index[choice]] = 1.0

    return sample

if __name__ == "__main__":
    args = tyro.cli(Args)
    args.batch_size = int(args.num_envs * args.num_steps)
    args.minibatch_size = int(args.batch_size // args.num_minibatches)
    args.num_iterations = args.total_timesteps // args.batch_size
    # TODO: maybe add back
    # run_name = f"{args.env_id}__{args.exp_name}__{args.seed}__{int(time.time())}"
    # if args.track:
    #     import wandb
    #
    #     wandb.init(
    #         project=args.wandb_project_name,
    #         entity=args.wandb_entity,
    #         sync_tensorboard=True,
    #         config=vars(args),
    #         name=run_name,
    #         monitor_gym=True,
    #         save_code=True,
    #     )
    # writer = SummaryWriter(f"runs/{run_name}")
    # writer.add_text(
    #     "hyperparameters",
    #     "|param|value|\n|-|-|\n%s" % ("\n".join([f"|{key}|{value}|" for key, value in vars(args).items()])),
    # )

    # TRY NOT TO MODIFY: seeding
    random.seed(args.seed)
    np.random.seed(args.seed)
    if args.seed is not None:
        torch.manual_seed(args.seed)
    torch.backends.cudnn.deterministic = args.torch_deterministic

    device = torch.device("cuda" if torch.cuda.is_available() and args.cuda else "cpu")

    def make_env(i):
        return lambda seed=None if args.seed is None else args.seed + i, device=device: BalatroEnv(i, seed=seed, device=device)
    # env setup
    env_fns = [ make_env(i) for i in range(args.num_envs) ]
    envs = ParallelEnv(args.num_envs, env_fns)
    next = envs.reset(seed=args.seed) # reset early to initialize envs

    agent = Agent(envs).to(device)
    optimizer = optim.Adam(agent.parameters(), lr=args.learning_rate, eps=1e-5)

    # ALGO Logic: Storage setup
    obs = torch.zeros(args.num_steps, args.num_envs, envs.observation_spec["observation"].shape[-1]).to(device)
    actions = {
        "action_type": torch.zeros(args.num_steps, args.num_envs, dtype=torch.long, device=device),
        "param1": torch.zeros(args.num_steps, args.num_envs, *envs.action_spec["param1"].shape, dtype=torch.float32, device=device),
        "param2": torch.zeros(args.num_steps, args.num_envs, *envs.action_spec["param2"].shape, dtype=torch.float32, device=device),
    }
    logprobs = torch.zeros((args.num_steps, args.num_envs)).to(device)
    rewards = torch.zeros((args.num_steps, args.num_envs)).to(device)
    dones = torch.zeros((args.num_steps, args.num_envs)).to(device)
    values = torch.zeros((args.num_steps, args.num_envs)).to(device)

    # TRY NOT TO MODIFY: start the game
    global_step = 0
    start_time = time.time()
    next_obs = torch.Tensor(next["observation"]).to(device)
    next_done = torch.zeros(args.num_envs).to(device)

    iteration = 0
    # for iteration in range(1, args.num_iterations + 1):
    while True:
        iteration += 1
        snapshots = []

        update_start_time = time.time()

        # Annealing the rate if instructed to do so.
        # if args.anneal_lr:
        #     frac = 1.0 - (iteration - 1.0) / args.num_iterations
        #     lrnow = frac * args.learning_rate
        #     optimizer.param_groups[0]["lr"] = lrnow

        for step in range(0, args.num_steps):
            global_step += args.num_envs
            obs[step] = next_obs
            dones[step] = next_done

            # ALGO LOGIC: action logic
            with torch.no_grad():
                env_snapshots = envs.snapshot()

                # convert lists to tensors
                for snapshot in env_snapshots:
                    for key in ("buyable_shop_packs_mask", "buyable_shop_vouchers_mask", "buyable_shop_cards_mask"):
                        orig = snapshot[key]
                        LEN = len(orig)
                        new = torch.zeros(PARAM1_LENGTH, dtype=torch.bool, device=device)
                        if LEN > 0:
                            new[:LEN] = torch.tensor(orig, dtype=torch.bool, device=device)
                        snapshot[key] = new

                snapshots.append(env_snapshots)

                action_td, logprob, _, value = agent.get_action_and_value(next_obs, env_snapshots)
                values[step] = value.flatten()
            actions["action_type"][step] = action_td["action_type"]
            actions["param1"][step] = action_td["param1"]
            actions["param2"][step] = action_td["param2"]
            logprobs[step] = logprob

            # TRY NOT TO MODIFY: execute the game and log data.
            td = envs.step(action_td)
            next = td["next"]

            rewards[step] = next["reward"].detach().clone().view(-1)
            next_obs, next_done = torch.Tensor(next["observation"]).to(device), torch.Tensor(next_done).to(device)

            done_mask = next["done"].view(-1).to(torch.bool)
            if done_mask.all():
                next = envs.reset()

            infos = next.get("final_info", None)
            if infos is not None:
                for info in infos:
                    if info and "episode" in info:
                        print(f"global_step={global_step}, episodic_return={info['episode']['r']}")
                        # writer.add_scalar("charts/episodic_return", info["episode"]["r"], global_step)
                        # writer.add_scalar("charts/episodic_length", info["episode"]["l"], global_step)

        # bootstrap value if not done
        with torch.no_grad():
            next_value = agent.get_value(next_obs).reshape(1, -1)
            advantages = torch.zeros_like(rewards).to(device)
            lastgaelam = 0
            for t in reversed(range(args.num_steps)):
                if t == args.num_steps - 1:
                    nextnonterminal = 1.0 - next_done
                    nextvalues = next_value
                else:
                    nextnonterminal = 1.0 - dones[t + 1]
                    nextvalues = values[t + 1]
                delta = rewards[t] + args.gamma * nextvalues * nextnonterminal - values[t]
                advantages[t] = lastgaelam = delta + args.gamma * args.gae_lambda * nextnonterminal * lastgaelam
            returns = advantages + values

        # flatten the batch
        b_obs = obs.reshape(-1, envs.observation_spec["observation"].shape[-1])
        b_logprobs = logprobs.reshape(-1)
        b_actions = {
            "action_type": actions["action_type"].reshape(-1),
            "param1": actions["param1"].reshape(-1, envs.action_spec["param1"].shape[-1]),
            "param2": actions["param2"].reshape(-1, envs.action_spec["param2"].shape[-1]),
        }
        b_advantages = advantages.reshape(-1)
        b_returns = returns.reshape(-1)
        b_values = values.reshape(-1)
        b_snapshots = [snapshot for step_snapshots in snapshots for snapshot in step_snapshots]


        # Optimizing the policy and value network
        b_inds = np.arange(args.batch_size)
        clipfracs = []
        for epoch in range(args.update_epochs):
            np.random.shuffle(b_inds)
            for start in range(0, args.batch_size, args.minibatch_size):
                end = start + args.minibatch_size
                mb_inds = b_inds[start:end]
                mb_snaps = [b_snapshots[i] for i in mb_inds]

                _, newlogprob, entropy, newvalue = agent.get_action_and_value(
                    b_obs[mb_inds],
                    mb_snaps,
                    action = TensorDict(
                        {
                            "action_type": b_actions["action_type"][mb_inds],
                            "param1":      b_actions["param1"][mb_inds],
                            "param2":      b_actions["param2"][mb_inds],
                        },
                        batch_size=[len(mb_inds)],
                    )
                )

                logratio = newlogprob - b_logprobs[mb_inds]
                ratio = logratio.exp()

                with torch.no_grad():
                    # calculate approx_kl http://joschu.net/blog/kl-approx.html
                    old_approx_kl = (-logratio).mean()
                    approx_kl = ((ratio - 1) - logratio).mean()
                    clipfracs += [((ratio - 1.0).abs() > args.clip_coef).float().mean().item()]

                mb_advantages = b_advantages[mb_inds]
                if args.norm_adv:
                    mb_advantages = (mb_advantages - mb_advantages.mean()) / (mb_advantages.std() + 1e-8)

                # Policy loss
                pg_loss1 = -mb_advantages * ratio
                pg_loss2 = -mb_advantages * torch.clamp(ratio, 1 - args.clip_coef, 1 + args.clip_coef)
                pg_loss = torch.max(pg_loss1, pg_loss2).mean()

                # Value loss
                newvalue = newvalue.view(-1)
                if args.clip_vloss:
                    v_loss_unclipped = (newvalue - b_returns[mb_inds]) ** 2
                    v_clipped = b_values[mb_inds] + torch.clamp(
                        newvalue - b_values[mb_inds],
                        -args.clip_coef,
                        args.clip_coef,
                    )
                    v_loss_clipped = (v_clipped - b_returns[mb_inds]) ** 2
                    v_loss_max = torch.max(v_loss_unclipped, v_loss_clipped)
                    v_loss = 0.5 * v_loss_max.mean()
                else:
                    v_loss = 0.5 * ((newvalue - b_returns[mb_inds]) ** 2).mean()

                entropy_loss = entropy.mean()
                loss = pg_loss - args.ent_coef * entropy_loss + v_loss * args.vf_coef

                optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(agent.parameters(), args.max_grad_norm)
                optimizer.step()

            if args.target_kl is not None and approx_kl > args.target_kl:
                break

        y_pred, y_true = b_values.cpu().numpy(), b_returns.cpu().numpy()
        var_y = np.var(y_true)
        explained_var = np.nan if var_y == 0 else 1 - np.var(y_true - y_pred) / var_y

        # TRY NOT TO MODIFY: record rewards for plotting purposes
        print("learning_rate:", optimizer.param_groups[0]["lr"], global_step)
        print("value_loss:", v_loss.item(), global_step)
        print("policy_loss:", pg_loss.item(), global_step)
        print("entropy:", entropy_loss.item(), global_step)
        print("old_approx_kl:", old_approx_kl.item(), global_step)
        print("approx_kl:", approx_kl.item(), global_step)
        print("clipfrac:", np.mean(clipfracs), global_step)
        print("explained_variance:", explained_var, global_step)
        print("SPS:", int(global_step / (time.time() - start_time)))
        print("reward_per_step:", np.mean(rewards.cpu().numpy()) / args.num_steps, global_step)
        print("update_time_sec:", time.time() - update_start_time, global_step)
        # writer.add_scalar("charts/SPS", int(global_step / (time.time() - start_time)), global_step)

    envs.close()
    # writer.close()
