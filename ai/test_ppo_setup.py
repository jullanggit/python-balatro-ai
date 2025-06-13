#!/usr/bin/env python3
"""
Test script to verify PPO setup works correctly
"""

import torch
import numpy as np
from tensordict import TensorDict
import sys
import os

# Add current directory to path for imports
sys.path.append(os.path.dirname(__file__))

from env import BalatroEnv, ActionType, PARAM1_LENGTH, PARAM2_LENGTH
from encode import SIZE_ENCODED
from ppo_balatro import Agent


def test_environment():
    """Test basic environment functionality"""
    print("Testing environment...")

    try:
        env = BalatroEnv(seed=42)
        print(f"✓ Environment created successfully")

        # Test reset
        reset_result = env.reset()
        print(f"✓ Environment reset successful")
        print(f"  - Observation shape: {reset_result['observation'].shape}")
        print(f"  - Expected shape: ({SIZE_ENCODED},)")
        assert reset_result['observation'].shape == (SIZE_ENCODED,), "Observation shape mismatch"

        # Test random action
        action_td = TensorDict({
            "action_type": torch.randint(0, len(ActionType), (1,)),
            "param1": torch.randint(0, 2, (PARAM1_LENGTH,)).bool(),
            "param2": torch.randint(0, 2, (PARAM2_LENGTH,)).bool()
        }, batch_size=[])
        td = TensorDict({"action": action_td}, batch_size=[])

        step_result = env.step(td)["next"]
        print(f"✓ Environment step successful")
        print(f"  - Reward: {step_result['reward'].item():.2f}")
        print(f"  - Done: {step_result['done'].item()}")

        return True

    except Exception as e:
        print(f"✗ Environment test failed: {e}")
        return False


def test_agent():
    """Test PPO agent functionality"""
    print("\nTesting PPO agent...")

    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        agent = Agent(SIZE_ENCODED, len(ActionType)).to(device)
        print(f"✓ Agent created successfully on {device}")

        # Test forward pass
        obs = torch.randn(1, SIZE_ENCODED).to(device)

        # Test get_value
        value = agent.get_value(obs)
        print(f"✓ Value function works, output shape: {value.shape}")

        # Test get_action_and_value
        action, logprob, entropy, value = agent.get_action_and_value(obs)
        print(f"✓ Action sampling works")
        print(f"  - Action type shape: {action['action_type'].shape}")
        print(f"  - Param1 shape: {action['param1'].shape}")
        print(f"  - Param2 shape: {action['param2'].shape}")
        print(f"  - Log prob shape: {logprob.shape}")
        print(f"  - Entropy shape: {entropy.shape}")
        print(f"  - Value shape: {value.shape}")

        # Test with specific action (for gradient computation test)
        test_action = {
            "action_type": torch.randint(0, len(ActionType), (1,)).to(device),
            "param1": torch.randint(0, 2, (1, PARAM1_LENGTH)).bool().to(device),
            "param2": torch.randint(0, 2, (1, PARAM2_LENGTH)).bool().to(device)
        }

        _, logprob2, entropy2, value2 = agent.get_action_and_value(obs, test_action)
        print(f"✓ Action evaluation works")

        return True

    except Exception as e:
        print(f"✗ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_training_step():
    """Test a single training step"""
    print("\nTesting training step...")

    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        env = BalatroEnv(seed=42)
        agent = Agent(SIZE_ENCODED, len(ActionType)).to(device)
        optimizer = torch.optim.Adam(agent.parameters(), lr=1e-4)

        # Get initial observation
        obs_dict = env.reset()
        obs = obs_dict["observation"].unsqueeze(0).to(device)

        # Get action from agent
        action, old_logprob, entropy, value = agent.get_action_and_value(obs)

        # Convert action for environment
        env_action = TensorDict({
            "action_type": action["action_type"][0].cpu(),
            "param1": action["param1"][0].cpu(),
            "param2": action["param2"][0].cpu()
        }, batch_size=[])
        env_td = TensorDict({"action": env_action}, batch_size=[])

        # Take step in environment
        result = env.step(env_td)["next"]
        reward = result["reward"].to(device)
        next_obs = result["observation"].unsqueeze(0).to(device)

        print(f"✓ Environment step completed")
        print(f"  - Reward: {reward.item():.4f}")

        # Compute a simple loss (not full PPO, just to test backprop)
        next_value = agent.get_value(next_obs)
        advantage = reward + 0.99 * next_value - value

        # Simple policy loss
        policy_loss = -(old_logprob * advantage.detach()).mean()
        value_loss = advantage.pow(2).mean()
        entropy_loss = entropy.mean()

        total_loss = policy_loss + 0.5 * value_loss - 0.01 * entropy_loss

        # Backward pass
        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        print(f"✓ Training step completed")
        print(f"  - Policy loss: {policy_loss.item():.4f}")
        print(f"  - Value loss: {value_loss.item():.4f}")
        print(f"  - Entropy: {entropy_loss.item():.4f}")
        print(f"  - Total loss: {total_loss.item():.4f}")

        return True

    except Exception as e:
        print(f"✗ Training step test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_action_space_coverage():
    """Test that all action types can be sampled"""
    print("\nTesting action space coverage...")

    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        agent = Agent(SIZE_ENCODED, len(ActionType)).to(device)

        # Sample many actions to see coverage
        obs = torch.randn(100, SIZE_ENCODED).to(device)
        action, _, _, _ = agent.get_action_and_value(obs)

        unique_actions = torch.unique(action["action_type"]).cpu().numpy()
        coverage = len(unique_actions) / len(ActionType)

        print(f"✓ Action space coverage test completed")
        print(f"  - Unique actions sampled: {len(unique_actions)}/{len(ActionType)}")
        print(f"  - Coverage: {coverage:.2%}")
        print(f"  - Actions sampled: {[ActionType(a).name for a in unique_actions[:5]]}...")

        if coverage < 0.5:
            print(f"⚠ Warning: Low action coverage, may indicate initialization issues")

        return True

    except Exception as e:
        print(f"✗ Action space coverage test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("PPO BALATRO SETUP VERIFICATION")
    print("=" * 60)

    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA device: {torch.cuda.get_device_name()}")
    print(f"Device: {'cuda' if torch.cuda.is_available() else 'cpu'}")

    tests = [
        ("Environment", test_environment),
        ("PPO Agent", test_agent),
        ("Training Step", test_training_step),
        ("Action Coverage", test_action_space_coverage)
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        success = test_func()
        results.append((test_name, success))

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    all_passed = True
    for test_name, success in results:
        status = "PASS" if success else "FAIL"
        print(f"{test_name:20}: {status}")
        if not success:
            all_passed = False

    print("-" * 60)
    if all_passed:
        print("🎉 All tests passed! PPO setup is working correctly.")
        print("\nYou can now start training with:")
        print("  python ppo_balatro.py --total-timesteps 10000 --num-envs 2")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print("Make sure all dependencies are installed correctly.")

    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
