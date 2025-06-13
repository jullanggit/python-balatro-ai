#!/usr/bin/env python3
"""
Evaluation script for trained PPO Balatro AI models
"""

import argparse
import torch
import numpy as np
from tensordict import TensorDict
import time
import os

from env import BalatroEnv, ActionType, PARAM1_LENGTH, PARAM2_LENGTH
from encode import SIZE_ENCODED
from ppo_balatro import Agent


def evaluate_model(model_path, num_episodes=10, render=False, seed=42):
    """
    Evaluate a trained PPO model
    
    Args:
        model_path: Path to the saved model
        num_episodes: Number of episodes to evaluate
        render: Whether to print game state (not implemented yet)
        seed: Random seed for evaluation
    """
    
    # Set up device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load the trained agent
    agent = Agent(SIZE_ENCODED, len(ActionType)).to(device)
    
    if os.path.exists(model_path):
        agent.load_state_dict(torch.load(model_path, map_location=device))
        print(f"Loaded model from {model_path}")
    else:
        print(f"Model file {model_path} not found!")
        return
    
    agent.eval()
    
    # Create environment
    env = BalatroEnv(seed=seed)
    
    # Evaluation metrics
    episode_rewards = []
    episode_lengths = []
    episode_scores = []
    wins = 0
    
    print(f"\nEvaluating for {num_episodes} episodes...")
    print("-" * 50)
    
    for episode in range(num_episodes):
        obs_dict = env.reset()
        obs = obs_dict["observation"].to(device)
        
        episode_reward = 0
        episode_length = 0
        done = False
        
        start_time = time.time()
        
        while not done:
            with torch.no_grad():
                # Get action from the agent
                action, _, _, _ = agent.get_action_and_value(obs.unsqueeze(0))
                
                # Extract action components
                action_dict = {
                    "action_type": action["action_type"][0],
                    "param1": action["param1"][0],
                    "param2": action["param2"][0]
                }
                
                # Create tensordict for environment
                action_td = TensorDict(action_dict, batch_size=[])
                td = TensorDict({"action": action_td}, batch_size=[])
                
                # Take step in environment
                try:
                    result = env.step(td)
                    obs = result["observation"].to(device)
                    reward = result["reward"].item()
                    done = result["done"].item()
                    
                    episode_reward += reward
                    episode_length += 1
                    
                    # Optional: Print action taken
                    if render and episode_length <= 20:  # Only print first 20 actions
                        action_name = ActionType(action_dict["action_type"].item()).name
                        param1_indices = torch.where(action_dict["param1"])[0].tolist()
                        param2_indices = torch.where(action_dict["param2"])[0].tolist()
                        print(f"  Step {episode_length}: {action_name}({param1_indices}, {param2_indices}) -> Reward: {reward:.2f}")
                    
                except Exception as e:
                    print(f"Error during episode {episode+1}, step {episode_length}: {e}")
                    done = True
                    episode_reward -= 10  # Penalty for error
                    
                # Safety check to prevent infinite episodes
                if episode_length >= 1000:
                    print(f"Episode {episode+1} reached maximum length, terminating...")
                    done = True
        
        # Check if this was a winning episode (ante 9 reached)
        if hasattr(env.run, 'ante') and env.run.ante >= 9:
            wins += 1
            
        # Get final score if available
        final_score = getattr(env.run, 'round_score', 0)
        
        episode_time = time.time() - start_time
        
        episode_rewards.append(episode_reward)
        episode_lengths.append(episode_length)
        episode_scores.append(final_score)
        
        print(f"Episode {episode+1:2d}: Reward: {episode_reward:8.2f}, Length: {episode_length:3d}, "
              f"Score: {final_score:6.0f}, Ante: {getattr(env.run, 'ante', 'N/A'):2}, "
              f"Time: {episode_time:.1f}s")
    
    # Calculate and display statistics
    print("-" * 50)
    print("EVALUATION RESULTS:")
    print(f"Episodes: {num_episodes}")
    print(f"Mean Reward: {np.mean(episode_rewards):.2f} ± {np.std(episode_rewards):.2f}")
    print(f"Mean Length: {np.mean(episode_lengths):.1f} ± {np.std(episode_lengths):.1f}")
    print(f"Mean Score: {np.mean(episode_scores):.0f} ± {np.std(episode_scores):.0f}")
    print(f"Win Rate: {wins}/{num_episodes} ({100*wins/num_episodes:.1f}%)")
    print(f"Max Reward: {np.max(episode_rewards):.2f}")
    print(f"Min Reward: {np.min(episode_rewards):.2f}")
    
    return {
        'episode_rewards': episode_rewards,
        'episode_lengths': episode_lengths,
        'episode_scores': episode_scores,
        'win_rate': wins / num_episodes,
        'mean_reward': np.mean(episode_rewards),
        'mean_length': np.mean(episode_lengths),
        'mean_score': np.mean(episode_scores)
    }


def main():
    parser = argparse.ArgumentParser(description='Evaluate trained PPO Balatro model')
    parser.add_argument('model_path', type=str, help='Path to the trained model (.pth file)')
    parser.add_argument('--episodes', type=int, default=10, help='Number of episodes to evaluate')
    parser.add_argument('--seed', type=int, default=42, help='Random seed for evaluation')
    parser.add_argument('--render', action='store_true', help='Print detailed game actions')
    parser.add_argument('--save-results', type=str, help='Save results to file (optional)')
    
    args = parser.parse_args()
    
    # Run evaluation
    results = evaluate_model(
        model_path=args.model_path,
        num_episodes=args.episodes,
        render=args.render,
        seed=args.seed
    )
    
    # Save results if requested
    if args.save_results:
        import json
        with open(args.save_results, 'w') as f:
            # Convert numpy arrays to lists for JSON serialization
            results_serializable = {
                'episode_rewards': [float(x) for x in results['episode_rewards']],
                'episode_lengths': [int(x) for x in results['episode_lengths']],
                'episode_scores': [float(x) for x in results['episode_scores']],
                'win_rate': float(results['win_rate']),
                'mean_reward': float(results['mean_reward']),
                'mean_length': float(results['mean_length']),
                'mean_score': float(results['mean_score']),
                'model_path': args.model_path,
                'num_episodes': args.episodes,
                'seed': args.seed
            }
            json.dump(results_serializable, f, indent=2)
        print(f"\nResults saved to {args.save_results}")


if __name__ == '__main__':
    main()