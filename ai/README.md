# Balatro AI Training with PPO

This directory contains the implementation of a Proximal Policy Optimization (PPO) agent for playing Balatro, based on CleanRL.

## Overview

The AI system consists of:
- **Environment** (`env.py`): TorchRL-based environment wrapper for Balatro
- **Encoding** (`encode.py`): State representation and action space encoding
- **PPO Agent** (`ppo_balatro.py`): Main PPO training implementation
- **Evaluation** (`evaluate_ppo.py`): Script to evaluate trained models

## Features

- **Complex Action Space**: Handles Balatro's composite action space with 17 different action types and multiple parameters
- **Rich State Representation**: Encodes game state including cards, jokers, consumables, shop items, and game progress
- **Reward Engineering**: Sophisticated reward system based on score progression, blind completion, and game wins
- **Parallel Training**: Supports multiple parallel environments for efficient training
- **Model Checkpointing**: Automatic model saving and evaluation capabilities

## Installation

1. Install dependencies:
```bash
pip install -r ../requirements.txt
```

2. Install the Balatro package:
```bash
cd .. && pip install -e .
```

## Quick Start

### Training

Use the simple training launcher:
```bash
python ../train_ppo.py --timesteps 500000 --envs 4
```

Or run the PPO script directly:
```bash
python ppo_balatro.py --total-timesteps 500000 --num-envs 4 --learning-rate 2.5e-4
```

### Evaluation

Evaluate a trained model:
```bash
python evaluate_ppo.py models/ppo_balatro_1000.pth --episodes 10
```

## Training Arguments

### Basic Arguments
- `--total-timesteps`: Total training timesteps (default: 500000)
- `--num-envs`: Number of parallel environments (default: 4)
- `--learning-rate`: Learning rate (default: 2.5e-4)
- `--seed`: Random seed (default: 1)

### PPO Hyperparameters
- `--num-steps`: Steps per environment per rollout (default: 128)
- `--num-minibatches`: Number of minibatches (default: 4)
- `--update-epochs`: PPO update epochs (default: 4)
- `--clip-coef`: PPO clipping coefficient (default: 0.2)
- `--ent-coef`: Entropy coefficient (default: 0.01)
- `--vf-coef`: Value function coefficient (default: 0.5)
- `--gamma`: Discount factor (default: 0.99)
- `--gae-lambda`: GAE lambda (default: 0.95)

### Tracking and Logging
- `--track`: Enable Weights & Biases tracking
- `--wandb-project-name`: W&B project name (default: "ppo-balatro")
- `--exp-name`: Experiment name

## Action Space

The agent handles a composite action space with three components:

1. **Action Type** (Categorical): 17 different actions including:
   - `SELECT_BLIND`, `SKIP_BLIND`, `REROLL_BOSS_BLIND`
   - `PLAY_HAND`, `DISCARD_HAND`
   - `BUY_SHOP_CARD`, `SELL_JOKER`, `USE_CONSUMABLE`
   - And more...

2. **Param1** (Multi-Binary): Indices for cards, jokers, or shop items
3. **Param2** (Multi-Binary): Additional parameters or target positions

## State Representation

The state is encoded as a large tensor (~4000+ dimensions) containing:
- Hand cards and deck composition
- Joker collection and properties
- Consumable items
- Shop state and available items
- Game progress (ante, blind, score)
- Poker hand statistics
- Available tags and vouchers

## Reward Structure

The reward system encourages:
- **Score Progress**: Logarithmic reward based on score/goal ratio
- **Blind Completion**: Bonus rewards for completing blinds (10/15/20 points)
- **Game Victory**: Double total reward when reaching ante 9
- **Error Penalties**: -5 points for invalid actions

## Model Architecture

The PPO agent uses a shared feature extraction network followed by separate heads:

```
Input (4000+ dims) → Linear(512) → Tanh → Linear(512) → Tanh → Linear(256) → Tanh
                                                                      ↓
                                                              Actor Heads:
                                                              - Action Type (17 classes)
                                                              - Param1 (Multi-binary)
                                                              - Param2 (Multi-binary)
                                                              
                                                              Critic Head:
                                                              - Value (1 output)
```

## Monitoring Training

### TensorBoard
```bash
tensorboard --logdir runs/
```

### Weights & Biases
```bash
python ppo_balatro.py --track --wandb-project-name "my-balatro-project"
```

## Common Issues and Solutions

### Memory Issues
- Reduce `--num-envs` if you encounter OOM errors
- The state representation is quite large (~4KB per state)

### Training Instability
- Lower learning rate (`--learning-rate 1e-4`)
- Increase clipping (`--clip-coef 0.3`)
- Adjust entropy coefficient (`--ent-coef 0.02`)

### Slow Training
- Increase `--num-envs` if you have sufficient memory
- Use GPU acceleration with `--cuda`

## File Structure

```
ai/
├── README.md           # This file
├── env.py             # Balatro environment wrapper
├── encode.py          # State encoding utilities
├── ppo_balatro.py     # Main PPO training script
├── evaluate_ppo.py    # Model evaluation script
├── testing.py         # Environment testing utilities
└── models/            # Saved model checkpoints
```

## Next Steps

1. **Hyperparameter Tuning**: Experiment with different learning rates, network sizes, and PPO parameters
2. **Reward Engineering**: Refine the reward function based on training results
3. **Curriculum Learning**: Start with easier stakes and gradually increase difficulty
4. **Multi-Objective Training**: Balance between score maximization and game completion
5. **Analysis**: Study the learned strategies and decision patterns

## Contributing

When modifying the training code:
1. Test with a small number of timesteps first
2. Monitor tensorboard logs for training stability
3. Evaluate models regularly to ensure learning progress
4. Save intermediate checkpoints for analysis