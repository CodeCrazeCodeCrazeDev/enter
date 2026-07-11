"""Unit and integration tests for Self-Improving RL Training."""

from __future__ import annotations

import pytest
from agent_harness.core.runtime.learning.rl_training import SelfImprovingRLTrainer, RLExperienceEpisode


def test_rl_training_steps():
    trainer = SelfImprovingRLTrainer(learning_rate=0.002)

    episode_1 = RLExperienceEpisode(
        episode_id="ep_001",
        goal="Solve high school math",
        trajectory_length=8,
        thinking_token_count=1200,
        raw_outcome_reward=1.0,
        tool_efficiency_ratio=0.85
    )

    episode_2 = RLExperienceEpisode(
        episode_id="ep_002",
        goal="Fetch raw HTML",
        trajectory_length=15,  # long, should receive penalty
        thinking_token_count=20,  # brief, should receive brevity penalty
        raw_outcome_reward=0.5,
        tool_efficiency_ratio=0.3
    )

    # Calculate individual integrated rewards
    reward_1 = trainer.calculate_integrated_reward(episode_1)
    reward_2 = trainer.calculate_integrated_reward(episode_2)

    # Episode 1 has detailed thinking and high efficiency -> should have positive adjustments
    assert reward_1 > 1.0

    # Episode 2 has long trajectory and tiny thinking -> should have negative adjustments
    assert reward_2 < 0.5

    # Record and update policy
    trainer.record_episode(episode_1)
    trainer.record_episode(episode_2)

    metrics = trainer.run_policy_update()
    assert metrics.loss >= 0.0
    assert metrics.policy_entropy > 0.0
    assert len(trainer.experience_pool) == 0  # Replay pool cleared after on-policy step
