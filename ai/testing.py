import torch
from tensordict import TensorDict
from env import BalatroEnv, ActionType, PARAM1_LENGTH, PARAM2_LENGTH


def run_step(env, action_type, param1=None, param2=None):
    # Normalize params to lists of indices
    if param1 is None:
        param1_list = []
    elif isinstance(param1, int):
        param1_list = [param1]
    else:
        param1_list = list(param1)
    if param2 is None:
        param2_list = []
    elif isinstance(param2, int):
        param2_list = [param2]
    else:
        param2_list = list(param2)

    # Build binary masks
    mask1 = torch.zeros(PARAM1_LENGTH, dtype=torch.bool)
    for idx in param1_list:
        mask1[idx] = True
    mask2 = torch.zeros(PARAM2_LENGTH, dtype=torch.bool)
    for idx in param2_list:
        mask2[idx] = True

    # Construct nested action TensorDict
    action_td = TensorDict(
        {
            "action_type": torch.tensor(action_type, dtype=torch.int64),
            "param1": mask1,
            "param2": mask2,
        },
        batch_size=[]
    )
    td = TensorDict({"action": action_td}, batch_size=[])
    return env.step(td)


if __name__ == "__main__":
    env = BalatroEnv()

    print("RESETTING...")
    td_reset = env.reset()
    print("Initial observation:", td_reset["observation"].shape)

    print("\nSTEP 1: SELECT_BLIND")
    td1 = run_step(env, ActionType.SELECT_BLIND.value)

    print("\nSTEP 2: PLAY_HAND([0, 1])")
    td2 = run_step(env, ActionType.PLAY_HAND.value, param1=[0, 1])

    print("\nSTEP 3: DISCARD_HAND([6, 7])")
    td3 = run_step(env, ActionType.DISCARD_HAND.value, param1=[6, 7])

    print("\nSTEP 4: INVALID ACTION (20)")
    td4 = run_step(env, 20)

    # The EnvBase.step returns a tensordict with next-keys
    print("\nFinal observation:", td4.get(("next", "observation")).shape)
    print("Reward:", td4.get(("next", "reward")).item())
    print("Done:", td4.get(("next", "done")).item())
