import os
import json
import argparse
import torch
from tensordict import TensorDict
import sys
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed

# Ensure 'spawn' start method to avoid forking issues with Torch
try:
    mp.set_start_method('spawn')
except RuntimeError:
    pass  # start method has already been set


def parse_seed_from_filename(replay_file: str) -> int:
    basename = os.path.basename(replay_file)
    if not basename.startswith('replay_') or not basename.endswith('.jsonl'):
        raise ValueError(f"Cannot parse seed from filename '{basename}'")
    seed_str = basename[len('replay_'):-len('.jsonl')]
    return int(seed_str)


def compute_total_reward(replay_file: str) -> tuple:
    # Delay heavy imports until inside worker
    import os, sys, json, torch
    from tensordict import TensorDict
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from env import BalatroEnv

    seed = parse_seed_from_filename(replay_file)
    env = BalatroEnv(worker_id=0, seed=seed, generate_replay=False)
    td = env.reset()
    total_reward = 0.0

    with open(replay_file, 'r') as f:
        for line in f:
            record = json.loads(line)
            action = {
                "action_type": torch.tensor(record["action_type"]),
                "param1": torch.tensor(record["param1"]),
                "param2": torch.tensor(record["param2"]),
            }
            td = env.step(TensorDict(action, batch_size=[]))["next"]
            total_reward += float(td["reward"].item())
            if td.get("done", False):
                break

    return replay_file, total_reward


def find_top_runs(runs_dir: str, top_n: int = 10, max_workers: int = None, verbose: bool = False):
    if not os.path.isdir(runs_dir):
        print(f"Error: runs directory '{runs_dir}' not found.")
        return

    all_files = [os.path.join(root, fname)
                 for root, _, files in os.walk(runs_dir)
                 for fname in files if fname.startswith('replay_') and fname.endswith('.jsonl')]
    print(f"Found {len(all_files)} files.")
    if not all_files:
        return

    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(compute_total_reward, f): f for f in all_files}
        for future in as_completed(futures):
            fpath = futures[future]
            try:
                file, total = future.result()
                results.append((file, total))
                if verbose:
                    print(f"Processed {os.path.basename(file)}: Total Reward = {total}")
            except Exception as e:
                print(f"Skipping {os.path.basename(fpath)} due to error: {e}")

    results.sort(key=lambda x: x[1], reverse=True)
    print(f"\nTop {top_n} runs:")
    for idx, (path, total) in enumerate(results[:top_n], 1):
        print(f"{idx}. {os.path.basename(path)} -> {total}")


def main():
    parser = argparse.ArgumentParser(description="Find top replay runs by total reward (multiprocess)")
    parser.add_argument("--runs_dir", type=str,
                        help="Directory containing replay JSONL files.")
    parser.add_argument("--top_n", type=int, default=10,
                        help="Number of top runs to display.")
    parser.add_argument("--workers", type=int,
                        help="Number of worker processes to use.")
    parser.add_argument("--verbose", action='store_true',
                        help="Print each processed file reward.")
    args = parser.parse_args()

    runs_dir = args.runs_dir or os.path.join(os.path.dirname(__file__), 'runs')
    find_top_runs(runs_dir, args.top_n, args.workers, args.verbose)

if __name__ == '__main__':
    main()

