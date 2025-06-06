import torch
from tensordict import TensorDict
from env import BalatroEnv, ActionType

def run_step(env, action_type, param1=0, param2=0):
    action = torch.tensor([action_type, param1, param2], dtype=torch.int64)
    td = TensorDict({"action": action}, batch_size=[])
    return env.step(td)

env = BalatroEnv()

print("RESETTING...")
td = env.reset()
print("Initial observation:", td["observation"].shape)

print("\nSTEP 1: SELECT_BLIND")
td = run_step(env, ActionType.SELECT_BLIND.value)

print("\nSTEP 2: PLAY_HAND([0, 1])")
td = run_step(env, ActionType.PLAY_HAND.value, 0, 1)

print("\nSTEP 3: DISCARD_HAND([6, 7])")
td = run_step(env, ActionType.DISCARD_HAND.value, 6, 7)

td = run_step(env, 20)
print("\nFinal observation:", td["next", "observation"].shape)
print("Reward:", td["next", "reward"].item())
print("Done:", td["next", "done"].item())
