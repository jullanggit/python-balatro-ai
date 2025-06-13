import argparse
import os
import random
import time
from distutils.util import strtobool

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.distributions.categorical import Categorical
from torch.distributions.bernoulli import Bernoulli
from torch.utils.tensorboard import SummaryWriter

from env import BalatroEnv, ActionType, PARAM1_LENGTH, PARAM2_LENGTH
from encode import SIZE_ENCODED


def parse_args():
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp-name", type=str, default=os.path.basename(__file__).rstrip(".py"),
        help="the name of this experiment")
    parser.add_argument("--seed", type=int, default=1,
        help="seed of the experiment")
    parser.add_argument("--torch-deterministic", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help="if toggled, `torch.backends.cudnn.deterministic=False`")
    parser.add_argument("--cuda", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help="if toggled, cuda will be enabled by default")
    parser.add_argument("--track", type=lambda x: bool(strtobool(x)), default=False, nargs="?", const=True,
        help="if toggled, this experiment will be tracked with Weights and Biases")
    parser.add_argument("--wandb-project-name", type=str, default="ppo-balatro",
        help="the wandb's project name")
    parser.add_argument("--wandb-entity", type=str, default=None,
        help="the entity (team) of wandb's project")
    parser.add_argument("--capture-video", type=lambda x: bool(strtobool(x)), default=False, nargs="?", const=True,
        help="whether to capture videos of the agent performances (check out `videos` folder)")

    # Algorithm specific arguments
    parser.add_argument("--total-timesteps", type=int, default=500000,
        help="total timesteps of the experiments")
    parser.add_argument("--learning-rate", type=float, default=2.5e-4,
        help="the learning rate of the optimizer")
    parser.add_argument("--num-envs", type=int, default=4,
        help="the number of parallel game environments")
    parser.add_argument("--num-steps", type=int, default=128,
        help="the number of steps to run in each environment per policy rollout")
    parser.add_argument("--anneal-lr", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help="Toggle learning rate annealing for policy and value networks")
    parser.add_argument("--gamma", type=float, default=0.99,
        help="the discount factor gamma")
    parser.add_argument("--gae-lambda", type=float, default=0.95,
        help="the lambda for the general advantage estimation")
    parser.add_argument("--num-minibatches", type=int, default=4,
        help="the number of mini-batches")
    parser.add_argument("--update-epochs", type=int, default=4,
        help="the K epochs to update the policy")
    parser.add_argument("--norm-adv", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help="Toggles advantages normalization")
    parser.add_argument("--clip-coef", type=float, default=0.2,
        help="the surrogate clipping coefficient")
    parser.add_argument("--clip-vloss", type=lambda x: bool(strtobool(x)), default=True, nargs="?", const=True,
        help="Toggles whether or not to use a clipped loss for the value function, as per the paper.")
    parser.add_argument("--ent-coef", type=float, default=0.01,
        help="coefficient of the entropy")
    parser.add_argument("--vf-coef", type=float, default=0.5,
        help="coefficient of the value function")
    parser.add_argument("--max-grad-norm", type=float, default=0.5,
        help="the maximum norm for the gradient clipping")
    parser.add_argument("--target-kl", type=float, default=None,
        help="the target KL divergence threshold")
    args = parser.parse_args()
    args.batch_size = int(args.num_envs * args.num_steps)
    args.minibatch_size = int(args.batch_size // args.num_minibatches)
    # fmt: on
    return args


def make_env(seed):
    def thunk():
        env = BalatroEnv(seed=seed)
        return env
    return thunk


def layer_init(layer, std=np.sqrt(2), bias_const=0.0):
    torch.nn.init.orthogonal_(layer.weight, std)
    torch.nn.init.constant_(layer.bias, bias_const)
    return layer


class Agent(nn.Module):
    def __init__(self, observation_size, num_action_types):
        super().__init__()

        # Shared network for feature extraction
        self.network = nn.Sequential(
            layer_init(nn.Linear(observation_size, 512)),
            nn.Tanh(),
            layer_init(nn.Linear(512, 512)),
            nn.Tanh(),
            layer_init(nn.Linear(512, 256)),
            nn.Tanh(),
        )

        # Actor heads for composite action space
        self.actor_action_type = layer_init(nn.Linear(256, num_action_types), std=0.01)
        self.actor_param1 = layer_init(nn.Linear(256, PARAM1_LENGTH), std=0.01)
        self.actor_param2 = layer_init(nn.Linear(256, PARAM2_LENGTH), std=0.01)

        # Critic head
        self.critic = layer_init(nn.Linear(256, 1), std=1.0)

    def get_value(self, x):
        hidden = self.network(x)
        return self.critic(hidden)

    def get_action_and_value(self, x, action=None):
        hidden = self.network(x)

        # Get action type logits and distribution
        action_type_logits = self.actor_action_type(hidden)
        action_type_dist = Categorical(logits=action_type_logits)

        # Get param1 logits and distribution
        param1_logits = self.actor_param1(hidden)
        param1_dist = Bernoulli(logits=param1_logits)

        # Get param2 logits and distribution
        param2_logits = self.actor_param2(hidden)
        param2_dist = Bernoulli(logits=param2_logits)

        if action is None:
            # Sample actions
            action_type = action_type_dist.sample()
            param1 = param1_dist.sample()
            param2 = param2_dist.sample()
        else:
            action_type = action["action_type"]
            param1 = action["param1"]
            param2 = action["param2"]

        # Calculate log probabilities
        action_type_logprob = action_type_dist.log_prob(action_type)
        param1_logprob = param1_dist.log_prob(param1).sum(dim=-1)
        param2_logprob = param2_dist.log_prob(param2).sum(dim=-1)

        # Total log probability is sum of all components
        total_logprob = action_type_logprob + param1_logprob + param2_logprob

        # Calculate entropies
        action_type_entropy = action_type_dist.entropy()
        param1_entropy = param1_dist.entropy().sum(dim=-1)
        param2_entropy = param2_dist.entropy().sum(dim=-1)
        total_entropy = action_type_entropy + param1_entropy + param2_entropy

        # Package action
        sampled_action = {
            "action_type": action_type,
            "param1": param1,
            "param2": param2
        }

        return sampled_action, total_logprob, total_entropy, self.critic(hidden)


if __name__ == "__main__":
    args = parse_args()
    run_name = f"{args.exp_name}__{args.seed}__{int(time.time())}"
    if args.track:
        import wandb

        wandb.init(
            project=args.wandb_project_name,
            entity=args.wandb_entity,
            sync_tensorboard=True,
            config=vars(args),
            name=run_name,
            monitor_gym=True,
            save_code=True,
        )
    writer = SummaryWriter(f"runs/{run_name}")
    writer.add_text(
        "hyperparameters",
        "|param|value|\n|-|-|\n%s" % ("\n".join([f"|{key}|{value}|" for key, value in vars(args).items()])),
    )

    # TRY NOT TO MODIFY: seeding
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cudnn.deterministic = args.torch_deterministic

    device = torch.device("cuda" if torch.cuda.is_available() and args.cuda else "cpu")

    # env setup
    envs = [make_env(args.seed + i)() for i in range(args.num_envs)]

    agent = Agent(SIZE_ENCODED, len(ActionType)).to(device)
    optimizer = optim.Adam(agent.parameters(), lr=args.learning_rate, eps=1e-5)

    # ALGO Logic: Storage setup
    obs = torch.zeros((args.num_steps, args.num_envs) + (SIZE_ENCODED,)).to(device)
    actions_type = torch.zeros((args.num_steps, args.num_envs) + ()).to(device)
    actions_param1 = torch.zeros((args.num_steps, args.num_envs, PARAM1_LENGTH)).to(device)
    actions_param2 = torch.zeros((args.num_steps, args.num_envs, PARAM2_LENGTH)).to(device)
    logprobs = torch.zeros((args.num_steps, args.num_envs)).to(device)
    rewards = torch.zeros((args.num_steps, args.num_envs)).to(device)
    dones = torch.zeros((args.num_steps, args.num_envs)).to(device)
    values = torch.zeros((args.num_steps, args.num_envs)).to(device)

    # TRY NOT TO MODIFY: start the game
    global_step = 0
    start_time = time.time()
    next_obs = torch.stack([env.reset()["observation"] for env in envs]).to(device)
    next_done = torch.zeros(args.num_envs).to(device)
    num_updates = args.total_timesteps // args.batch_size

    # Episode tracking
    episode_rewards = []
    episode_lengths = []
    current_episode_rewards = [0.0] * args.num_envs
    current_episode_lengths = [0] * args.num_envs

    for update in range(1, num_updates + 1):
        # Annealing the rate if instructed to do so.
        if args.anneal_lr:
            frac = 1.0 - (update - 1.0) / num_updates
            lrnow = frac * args.learning_rate
            optimizer.param_groups[0]["lr"] = lrnow

        for step in range(0, args.num_steps):
            global_step += 1 * args.num_envs
            obs[step] = next_obs
            dones[step] = next_done

            # ALGO LOGIC: action logic
            with torch.no_grad():
                action, logprob, _, value = agent.get_action_and_value(next_obs)
                values[step] = value.flatten()
            actions_type[step] = action["action_type"]
            actions_param1[step] = action["param1"]
            actions_param2[step] = action["param2"]
            logprobs[step] = logprob

            # TRY NOT TO MODIFY: execute the game and log data.
            next_obs_list = []
            next_done_list = []
            reward_list = []

            for i, env in enumerate(envs):
                # Create action tensordict for this environment
                from tensordict import TensorDict
                action_td = TensorDict({
                    "action_type": action["action_type"][i],
                    "param1": action["param1"][i],
                    "param2": action["param2"][i]
                }, batch_size=[])
                td = TensorDict({"action": action_td}, batch_size=[])

                try:
                    result = env.step(td)["next"]
                    next_obs_list.append(result["observation"])
                    next_done_list.append(result["done"])
                    reward_list.append(result["reward"])
                except Exception as e:
                    print(f"Environment {i} error: {e}")
                    # Reset environment on error
                    reset_result = env.reset()
                    next_obs_list.append(reset_result["observation"])
                    next_done_list.append(torch.tensor([True]))
                    reward_list.append(torch.tensor([-10.0]))  # Penalty for error

            next_obs = torch.stack(next_obs_list).to(device)
            next_done = torch.stack(next_done_list).flatten().to(device)
            rewards[step] = torch.stack(reward_list).flatten().to(device)

            # Update episode tracking
            for i in range(args.num_envs):
                current_episode_rewards[i] += rewards[step][i].item()
                current_episode_lengths[i] += 1

                if next_done[i]:
                    episode_rewards.append(current_episode_rewards[i])
                    episode_lengths.append(current_episode_lengths[i])
                    current_episode_rewards[i] = 0.0
                    current_episode_lengths[i] = 0

                    # Reset environment
                    reset_result = envs[i].reset()
                    next_obs[i] = reset_result["observation"].to(device)

        # bootstrap value if not done
        with torch.no_grad():
            next_value = agent.get_value(next_obs).reshape(1, -1)
            advantages = torch.zeros_like(rewards).to(device)
            lastgaelam = 0
            for t in reversed(range(args.num_steps)):
                if t == args.num_steps - 1:
                    nextnonterminal = 1.0 - next_done.item()
                    nextvalues = next_value
                else:
                    nextnonterminal = 1.0 - dones[t + 1]
                    nextvalues = values[t + 1]
                delta = rewards[t] + args.gamma * nextvalues * nextnonterminal - values[t]
                advantages[t] = lastgaelam = delta + args.gamma * args.gae_lambda * nextnonterminal * lastgaelam
            returns = advantages + values

        # flatten the batch
        b_obs = obs.reshape((-1,) + (SIZE_ENCODED,))
        b_logprobs = logprobs.reshape(-1)
        b_actions_type = actions_type.reshape(-1)
        b_actions_param1 = actions_param1.reshape(-1, PARAM1_LENGTH)
        b_actions_param2 = actions_param2.reshape(-1, PARAM2_LENGTH)
        b_advantages = advantages.reshape(-1)
        b_returns = returns.reshape(-1)
        b_values = values.reshape(-1)

        # Optimizing the policy and value network
        b_inds = np.arange(args.batch_size)
        clipfracs = []
        for epoch in range(args.update_epochs):
            np.random.shuffle(b_inds)
            for start in range(0, args.batch_size, args.minibatch_size):
                end = start + args.minibatch_size
                mb_inds = b_inds[start:end]

                mb_actions = {
                    "action_type": b_actions_type[mb_inds],
                    "param1": b_actions_param1[mb_inds],
                    "param2": b_actions_param2[mb_inds]
                }

                _, newlogprob, entropy, newvalue = agent.get_action_and_value(b_obs[mb_inds], mb_actions)
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

            if args.target_kl is not None:
                if approx_kl > args.target_kl:
                    break

        y_pred, y_true = b_values.cpu().numpy(), b_returns.cpu().numpy()
        var_y = np.var(y_true)
        explained_var = np.nan if var_y == 0 else 1 - np.var(y_true - y_pred) / var_y

        # TRY NOT TO MODIFY: record rewards for plotting purposes
        writer.add_scalar("charts/learning_rate", optimizer.param_groups[0]["lr"], global_step)
        writer.add_scalar("losses/value_loss", v_loss.item(), global_step)
        writer.add_scalar("losses/policy_loss", pg_loss.item(), global_step)
        writer.add_scalar("losses/entropy", entropy_loss.item(), global_step)
        writer.add_scalar("losses/old_approx_kl", old_approx_kl.item(), global_step)
        writer.add_scalar("losses/approx_kl", approx_kl.item(), global_step)
        writer.add_scalar("losses/clipfrac", np.mean(clipfracs), global_step)
        writer.add_scalar("losses/explained_variance", explained_var, global_step)
        print(f"SPS: {int(global_step / (time.time() - start_time))}")
        writer.add_scalar("charts/SPS", int(global_step / (time.time() - start_time)), global_step)

        # Log episode rewards when available
        if episode_rewards:
            mean_episode_reward = np.mean(episode_rewards[-10:])  # Last 10 episodes
            mean_episode_length = np.mean(episode_lengths[-10:])
            writer.add_scalar("charts/episodic_return", mean_episode_reward, global_step)
            writer.add_scalar("charts/episodic_length", mean_episode_length, global_step)
            print(f"Update {update}, Global Step {global_step}, Mean Episode Reward: {mean_episode_reward:.4f}, Mean Episode Length: {mean_episode_length:.1f}")
        else:
            mean_reward = rewards.mean().item()
            print(f"Update {update}, Global Step {global_step}, Step Reward: {mean_reward:.4f}")

        # Save model checkpoint periodically
        if update % 100 == 0:
            os.makedirs("models", exist_ok=True)
            torch.save(agent.state_dict(), f"models/ppo_balatro_{update}.pth")
            print(f"Model saved at update {update}")

    # Close environments
    for env in envs:
        try:
            env.close()
        except:
            pass
    writer.close()
