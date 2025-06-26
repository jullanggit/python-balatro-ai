import os
import json
import argparse
import torch
from tensordict import TensorDict

# Import environment
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from env import BalatroEnv, ActionType

def compute_total_reward(replay_file: str) -> float:
    """
    Replays a JSONL file and returns the total reward achieved.
    """
    # extract seed from filename
    basename = os.path.basename(replay_file)
    parts = basename.replace('.jsonl', '').split('_')
    # expected format: replay_{seed}.jsonl or replay_seed_timestamp.jsonl
    try:
        seed = int(parts[1])
    except (IndexError, ValueError):
        raise ValueError(f"Cannot parse seed from filename '{basename}' (expected 'replay_<seed>.jsonl').")

    env = BalatroEnv(worker_id=0, seed=seed, generate_replay=False)
    td = env.reset()

    with open(replay_file, 'r') as f:
        for line in f:
            record = json.loads(line)
            action = {
                "action_type": torch.tensor(record["action_type"]),
                "param1": torch.tensor(record["param1"]),
                "param2": torch.tensor(record["param2"]),
            }
            td = env.step(TensorDict(action, batch_size=[]))["next"]
            if td["done"]:
                break

    return env.total_reward


def find_top_runs(runs_dir: str, top_n: int = 10):
    """
    Searches through all JSONL replay files in runs_dir and prints the top_n runs by final total reward.
    """
    rewards = []  # list of tuples (filepath, total_reward)

    # Walk the directory for .jsonl files
    for root, _, files in os.walk(runs_dir):
        for fname in files:
            if fname.endswith('.jsonl'):
                path = os.path.join(root, fname)
                try:
                    total = compute_total_reward(path)
                    rewards.append((path, total))
                    print(f"Processed {fname}: Total Reward = {total}")
                except Exception as e:
                    print(f"Skipping {fname}: {e}")

    # Sort by reward descending
    rewards.sort(key=lambda x: x[1], reverse=True)

    print(f"\nTop {top_n} runs in '{runs_dir}' by total reward:")
    for i, (path, total) in enumerate(rewards[:top_n], start=1):
        print(f"{i}. {os.path.basename(path)} -> Total Reward: {total}")


def main():
    parser = argparse.ArgumentParser(description="Find top replay runs by total reward.")
    parser.add_argument(
        "--runs_dir", type=str, default="runs/",
        help="Directory containing replay JSONL files (default: runs/)."
    )
    parser.add_argument(
        "--top_n", type=int, default=10,
        help="Number of top runs to display (default: 10)."
    )
    args = parser.parse_args()

    find_top_runs(args.runs_dir, args.top_n)

if __name__ == "__main__":
    main()
