#!/usr/bin/env python3
"""
Simple training launcher for PPO Balatro AI
"""

import os
import sys
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Train PPO agent for Balatro')
    parser.add_argument('--timesteps', type=int, default=500000, help='Total training timesteps')
    parser.add_argument('--envs', type=int, default=4, help='Number of parallel environments')
    parser.add_argument('--lr', type=float, default=2.5e-4, help='Learning rate')
    parser.add_argument('--seed', type=int, default=1, help='Random seed')
    parser.add_argument('--wandb', action='store_true', help='Enable Weights & Biases tracking')
    parser.add_argument('--exp-name', type=str, default='ppo_balatro', help='Experiment name')
    
    args = parser.parse_args()
    
    # Change to AI directory
    ai_dir = os.path.join(os.path.dirname(__file__), 'ai')
    os.chdir(ai_dir)
    
    # Build command
    cmd = [
        sys.executable, 'ppo_balatro.py',
        '--total-timesteps', str(args.timesteps),
        '--num-envs', str(args.envs),
        '--learning-rate', str(args.lr),
        '--seed', str(args.seed),
        '--exp-name', args.exp_name
    ]
    
    if args.wandb:
        cmd.extend(['--track', 'True'])
    
    print(f"Starting PPO training with command: {' '.join(cmd)}")
    print(f"Training for {args.timesteps:,} timesteps with {args.envs} environments")
    print(f"Learning rate: {args.lr}, Seed: {args.seed}")
    
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Run training
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\nTraining interrupted by user")
    except subprocess.CalledProcessError as e:
        print(f"Training failed with error: {e}")
        sys.exit(1)
    
    print("Training completed successfully!")

if __name__ == '__main__':
    main()