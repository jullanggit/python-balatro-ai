"""
Configuration file for PPO Balatro AI training
"""

import dataclasses
from typing import Optional


@dataclasses.dataclass
class PPOConfig:
    """PPO training configuration"""
    
    # Environment settings
    num_envs: int = 4
    seed: int = 1
    
    # Training settings
    total_timesteps: int = 500000
    learning_rate: float = 2.5e-4
    anneal_lr: bool = True
    
    # PPO hyperparameters
    num_steps: int = 128
    num_minibatches: int = 4
    update_epochs: int = 4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_coef: float = 0.2
    clip_vloss: bool = True
    ent_coef: float = 0.01
    vf_coef: float = 0.5
    max_grad_norm: float = 0.5
    norm_adv: bool = True
    target_kl: Optional[float] = None
    
    # Network architecture
    hidden_size: int = 512
    num_layers: int = 3
    
    # Logging and saving
    exp_name: str = "ppo_balatro"
    track: bool = False
    wandb_project_name: str = "ppo-balatro"
    wandb_entity: Optional[str] = None
    save_frequency: int = 100  # Save model every N updates
    
    # Hardware
    cuda: bool = True
    torch_deterministic: bool = True
    
    # Evaluation
    eval_frequency: int = 0  # Evaluate every N updates (0 = no evaluation)
    eval_episodes: int = 5
    
    @property
    def batch_size(self) -> int:
        return self.num_envs * self.num_steps
    
    @property
    def minibatch_size(self) -> int:
        return self.batch_size // self.num_minibatches
    
    @property
    def num_updates(self) -> int:
        return self.total_timesteps // self.batch_size


# Predefined configurations for different training scenarios

def get_quick_test_config() -> PPOConfig:
    """Configuration for quick testing (small scale)"""
    return PPOConfig(
        total_timesteps=10000,
        num_envs=2,
        num_steps=64,
        save_frequency=10,
        exp_name="quick_test"
    )


def get_development_config() -> PPOConfig:
    """Configuration for development and debugging"""
    return PPOConfig(
        total_timesteps=100000,
        num_envs=4,
        learning_rate=3e-4,
        num_steps=128,
        save_frequency=50,
        exp_name="development"
    )


def get_full_training_config() -> PPOConfig:
    """Configuration for full-scale training"""
    return PPOConfig(
        total_timesteps=2000000,
        num_envs=8,
        learning_rate=2.5e-4,
        num_steps=256,
        save_frequency=100,
        eval_frequency=100,
        exp_name="full_training"
    )


def get_high_exploration_config() -> PPOConfig:
    """Configuration emphasizing exploration"""
    return PPOConfig(
        total_timesteps=1000000,
        num_envs=6,
        learning_rate=3e-4,
        ent_coef=0.02,  # Higher entropy
        clip_coef=0.3,  # More permissive clipping
        exp_name="high_exploration"
    )


def get_stable_training_config() -> PPOConfig:
    """Configuration for stable, conservative training"""
    return PPOConfig(
        total_timesteps=1500000,
        num_envs=4,
        learning_rate=1e-4,  # Lower learning rate
        clip_coef=0.1,       # More conservative clipping
        ent_coef=0.005,      # Lower entropy
        max_grad_norm=0.3,   # More gradient clipping
        exp_name="stable_training"
    )


# Environment-specific reward configurations
@dataclasses.dataclass
class RewardConfig:
    """Reward function configuration"""
    
    # Score-based rewards
    score_log_base: float = 14.43
    
    # Blind completion rewards
    small_blind_reward: float = 10.0
    big_blind_reward: float = 15.0
    boss_blind_reward: float = 20.0
    
    # Penalties
    invalid_action_penalty: float = -5.0
    error_penalty: float = -10.0
    
    # Game completion
    ante_9_multiplier: float = 2.0  # Double reward on win
    
    # Time-based penalties (optional)
    time_penalty_per_step: float = 0.0


# Curriculum learning configurations
@dataclasses.dataclass
class CurriculumConfig:
    """Curriculum learning configuration"""
    
    # Start with easier stakes and gradually increase
    initial_stake: str = "WHITE"
    final_stake: str = "GOLD"
    
    # Timesteps to spend at each difficulty level
    timesteps_per_stake: int = 200000
    
    # Success rate threshold to advance to next stake
    success_rate_threshold: float = 0.3
    
    # Number of episodes to evaluate success rate
    evaluation_episodes: int = 100


def load_config_from_file(config_path: str) -> PPOConfig:
    """Load configuration from a JSON file"""
    import json
    
    with open(config_path, 'r') as f:
        config_dict = json.load(f)
    
    return PPOConfig(**config_dict)


def save_config_to_file(config: PPOConfig, config_path: str):
    """Save configuration to a JSON file"""
    import json
    
    with open(config_path, 'w') as f:
        json.dump(dataclasses.asdict(config), f, indent=2)