if __name__ == "__main__":
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    import argparse
    from env import BalatroEnv, PARAM1_LENGTH, PARAM2_LENGTH, ActionType
    import json
    import torch
    from tensordict import TensorDict

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True, help="Path to replay JSONL file")
    args = parser.parse_args()

    # extract seed from filename
    basename = os.path.basename(args.file)
    parts = basename.replace('.jsonl','').split('_')
    # expected format: replay_{seed/timestamp}.jsonl
    seed = int(parts[1])

    env = BalatroEnv(worker_id=0, seed=seed, generate_replay=False)

    td = env.reset()
    print("Starting replay, initial obs:", td["observation"])

    with open(args.file) as f:
        for line in f:
            record = json.loads(line)
            # build tensordict for action
            action = {
                "action_type": torch.tensor(record["action_type"]),
                "param1": torch.tensor(record["param1"]),
                "param2": torch.tensor(record["param2"]),
            }
            td = env.step(TensorDict(action, batch_size=[]))["next"]
            # improve logging
            record["action_type"] = ActionType(record["action_type"])
            print("Step:", record, "Reward:", td["reward"].item(), "Total reward:", env.total_reward, "Done:", td["done"].item())
            if td["done"]:
                break
