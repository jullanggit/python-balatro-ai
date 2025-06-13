# PPO Setup Guide for Balatro AI

This guide will help you set up and run PPO (Proximal Policy Optimization) training for the Balatro AI using CleanRL as a base.

## Overview

The PPO implementation provides:
- **Composite Action Space**: Handles Balatro's complex action space with 17 action types and multiple parameters
- **Rich State Encoding**: ~10,500 dimensional state representation including cards, jokers, game state
- **Parallel Training**: Support for multiple environments running in parallel
- **Reward Engineering**: Sophisticated reward system based on game progress and strategy
- **Model Checkpointing**: Automatic saving and evaluation of trained models

## Quick Start

### 1. Basic Setup Verification

First, verify that the basic setup works:

```bash
cd ai
python test_basic_setup.py
```

You should see all tests pass. If not, check that the balatro package is properly accessible.

### 2. Install Dependencies

Create a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required packages:

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install tensordict torchrl numpy tensorboard
```

For GPU support (recommended):
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Optional dependencies for enhanced features:
```bash
pip install wandb  # For experiment tracking
pip install gymnasium  # For compatibility
```

### 3. Test Full Setup

Run the comprehensive test:

```bash
cd ai
python test_ppo_setup.py
```

This will test:
- Environment creation and stepping
- PPO agent functionality
- Training step mechanics
- Action space coverage

### 4. Start Training

Once all tests pass, start training:

```bash
# Quick test training (10K timesteps)
python ppo_balatro.py --total-timesteps 10000 --num-envs 2

# Full training run
python ppo_balatro.py --total-timesteps 500000 --num-envs 4
```

Or use the convenient launcher:

```bash
cd ..
python train_ppo.py --timesteps 500000 --envs 4
```

## Configuration Options

### Training Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--total-timesteps` | 500000 | Total training timesteps |
| `--num-envs` | 4 | Number of parallel environments |
| `--learning-rate` | 2.5e-4 | Learning rate for optimizer |
| `--num-steps` | 128 | Steps per environment per rollout |
| `--seed` | 1 | Random seed for reproducibility |

### PPO Hyperparameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--clip-coef` | 0.2 | PPO clipping coefficient |
| `--ent-coef` | 0.01 | Entropy regularization coefficient |
| `--vf-coef` | 0.5 | Value function loss coefficient |
| `--gamma` | 0.99 | Discount factor |
| `--gae-lambda` | 0.95 | GAE lambda parameter |
| `--update-epochs` | 4 | Number of PPO update epochs |

### Example Configurations

**Development/Testing:**
```bash
python ppo_balatro.py --total-timesteps 50000 --num-envs 2 --learning-rate 3e-4
```

**Stable Training:**
```bash
python ppo_balatro.py --total-timesteps 1000000 --num-envs 4 --learning-rate 1e-4 --clip-coef 0.1
```

**High Exploration:**
```bash
python ppo_balatro.py --total-timesteps 800000 --num-envs 6 --ent-coef 0.02 --clip-coef 0.3
```

## Monitoring Training

### TensorBoard

Training automatically logs metrics to TensorBoard:

```bash
tensorboard --logdir runs/
```

Open http://localhost:6006 to view:
- Episode rewards and lengths
- Policy and value losses
- Learning rate schedules
- Gradient norms and clipping

### Weights & Biases

For cloud-based experiment tracking:

```bash
python ppo_balatro.py --track --wandb-project-name "my-balatro-ai"
```

## Model Evaluation

### Evaluate Trained Models

```bash
# Evaluate a specific checkpoint
python ai/evaluate_ppo.py models/ppo_balatro_1000.pth --episodes 10

# Detailed evaluation with action logging
python ai/evaluate_ppo.py models/ppo_balatro_1000.pth --episodes 5 --render

# Save evaluation results
python ai/evaluate_ppo.py models/ppo_balatro_1000.pth --episodes 20 --save-results results.json
```

### Evaluation Metrics

The evaluation script reports:
- **Mean Episode Reward**: Average reward per episode
- **Episode Length**: Average number of steps per episode
- **Win Rate**: Percentage of episodes reaching ante 9
- **Final Scores**: Game scores achieved
- **Max/Min Rewards**: Performance range

## Understanding the Environment

### State Representation

The state is encoded as a 10,502-dimensional vector containing:
- **Hand Cards** (20 slots): Rank, suit, enhancements, seals, editions
- **Deck Cards** (100 slots): Remaining deck composition
- **Jokers** (15 slots): Joker types, editions, properties
- **Consumables** (20 slots): Tarots, planets, spectrals
- **Shop State**: Available cards, vouchers, packs, prices
- **Game Progress**: Ante, blind, money, scores
- **Poker Hand Info**: Levels and multipliers for each hand type

### Action Space

The agent chooses from a composite action space:

1. **Action Type** (17 options):
   - Game flow: SELECT_BLIND, SKIP_BLIND, CASH_OUT, NEXT_ROUND
   - Hand play: PLAY_HAND, DISCARD_HAND
   - Shop: BUY_SHOP_CARD, REDEEM_SHOP_VOUCHER, OPEN_SHOP_PACK, REROLL
   - Management: MOVE_JOKER, SELL_JOKER, USE_CONSUMABLE, SELL_CONSUMABLE
   - Packs: CHOOSE_PACK_ITEM, SKIP_PACK

2. **Param1** (Multi-binary, 20 bits): Indices for cards, jokers, or items
3. **Param2** (Multi-binary, 15 bits): Target positions or additional parameters

### Reward Structure

The reward system encourages effective play:

- **Score Progress**: `14.43 * log(score/goal)` for each hand played
- **Blind Completion**: 
  - Small Blind: +10 points
  - Big Blind: +15 points  
  - Boss Blind: +20 points
- **Game Victory**: Double total reward when reaching ante 9
- **Penalties**: -5 for invalid actions, -10 for errors

## Troubleshooting

### Common Issues

**Memory Errors:**
- Reduce `--num-envs` (try 2 or 1)
- The state representation is large (~40KB per environment)

**Training Instability:**
- Lower learning rate: `--learning-rate 1e-4`
- Increase clipping: `--clip-coef 0.3`
- Reduce batch size: `--num-steps 64`

**Slow Training:**
- Increase `--num-envs` if you have sufficient RAM
- Use GPU acceleration: ensure CUDA PyTorch is installed
- Monitor with `htop` or `nvidia-smi`

**Poor Performance:**
- Try different entropy coefficients: `--ent-coef 0.02`
- Adjust exploration: `--clip-coef 0.3`
- Increase training time: `--total-timesteps 2000000`

### Hardware Requirements

**Minimum:**
- 8GB RAM
- CPU with 4+ cores
- 5GB disk space

**Recommended:**
- 16GB+ RAM
- GPU with 8GB+ VRAM (RTX 3070 or better)
- SSD storage
- 8+ CPU cores

### Debugging

Enable detailed logging:
```bash
python ppo_balatro.py --total-timesteps 1000 --num-envs 1 --exp-name debug
```

Check environment behavior:
```bash
python ai/testing.py
```

Profile memory usage:
```bash
python -m memory_profiler ppo_balatro.py --total-timesteps 1000
```

## Advanced Usage

### Custom Reward Functions

Modify the reward calculation in `env.py`:

```python
# In the _step method, adjust reward calculation
if self.run.state == State.CASHING_OUT:
    # Custom reward for blind completion
    if blind == Blind.SMALL_BLIND:
        reward += 15.0  # Increased reward
    # Add custom logic here
```

### Curriculum Learning

Start with easier stakes and gradually increase difficulty:

```python
# Modify BalatroEnv.__init__ to accept stake parameter
def __init__(self, stake=Stake.WHITE, **kwargs):
    self.current_stake = stake
    # ... rest of initialization
```

### Multi-Objective Training

Add multiple reward components:

```python
# In reward calculation
score_reward = 14.43 * math.log(self.run.round_score/self.run.round_goal)
efficiency_reward = 10.0 / (self.steps_taken + 1)  # Favor shorter games
total_reward = score_reward + efficiency_reward
```

### Hyperparameter Tuning

Use the config system:

```python
from config import get_stable_training_config, PPOConfig

# Load predefined config
config = get_stable_training_config()

# Or create custom config
config = PPOConfig(
    total_timesteps=1000000,
    learning_rate=1e-4,
    num_envs=8,
    clip_coef=0.15
)
```

## Performance Benchmarks

Typical performance on different hardware:

| Hardware | Envs | SPS* | Time for 500K steps |
|----------|------|------|---------------------|
| CPU (8 cores) | 4 | 200 | ~40 minutes |
| RTX 3070 | 8 | 800 | ~10 minutes |
| RTX 4080 | 16 | 1600 | ~5 minutes |

*SPS = Steps Per Second

## Next Steps

After successful training:

1. **Analyze Results**: Use TensorBoard and evaluation scripts
2. **Hyperparameter Tuning**: Experiment with different settings
3. **Advanced Techniques**: Try curriculum learning or multi-objective training
4. **Competition**: Compare against human players or other AI approaches
5. **Deployment**: Create a playable interface for your trained agent

## Contributing

To contribute improvements:

1. Test thoroughly with `test_ppo_setup.py`
2. Maintain backward compatibility with existing configs
3. Document new features and parameters
4. Add unit tests for new components
5. Profile performance impact of changes

## Support

If you encounter issues:

1. Run the test scripts to isolate the problem
2. Check hardware requirements and resource usage
3. Try reducing complexity (fewer envs, shorter training)
4. Review the logs in `runs/` directory
5. Create an issue with full error logs and system info