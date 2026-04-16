from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt
import pandas as pd

from student_agent import Strategy


def plot_convergence(
    results: dict[Strategy, pd.DataFrame],
    n_agents: int,
    title: str | None = None,
    output_path: Optional[str] = None,
) -> None:
    """Plot convergence curves for all strategies with shaded ±1 std bands.

    Args:
        results: Dict mapping Strategy to aggregated DataFrame.
        n_agents: Number of agents (used for y-axis normalization).
        title: Plot title. Defaults to a descriptive title.
        output_path: If provided, saves the figure to this path
            (not used in show-only mode).
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    colors = {
        Strategy.Q_LEARNING: "#2196F3",
        Strategy.TIT_FOR_TAT: "#4CAF50",
        Strategy.GRIM_TRIGGER: "#FF9800",
        Strategy.RANDOM: "#9E9E9E",
    }
    labels = {
        Strategy.Q_LEARNING: "Q-Learning",
        Strategy.TIT_FOR_TAT: "Tit-for-Tat",
        Strategy.GRIM_TRIGGER: "Grim Trigger",
        Strategy.RANDOM: "Random",
    }
    linestyles = {
        Strategy.Q_LEARNING: "-",
        Strategy.TIT_FOR_TAT: "-",
        Strategy.GRIM_TRIGGER: "--",
        Strategy.RANDOM: ":",
    }

    for strategy, df in results.items():
        if df.empty:
            continue

        step_col = (
            "index"
            if "index" in df.columns
            else "Step"
            if "Step" in df.columns
            else "step"
        )
        ratio_mean_col = next(
            (c for c in df.columns if "cooperation_ratio" in c and "mean" in c), None
        )
        if ratio_mean_col is None:
            master_col = next(
                (c for c in df.columns if "master_count" in c and "mean" in c), None
            )
            ratio_mean_col = master_col
            std_col = next(
                (c for c in df.columns if "master_count" in c and "std" in c), None
            )
        else:
            std_col = next(
                (c for c in df.columns if "cooperation_ratio" in c and "std" in c), None
            )

        steps = df[step_col].values
        mean_vals = df[ratio_mean_col].values / n_agents
        color = colors.get(strategy, "#000000")
        label = labels.get(strategy, strategy.name)
        ls = linestyles.get(strategy, "-")

        ax.plot(steps, mean_vals, color=color, label=label, linestyle=ls, linewidth=2)

        if std_col is not None:
            std_vals = df[std_col].values / n_agents
            ax.fill_between(
                steps,
                mean_vals - std_vals,
                mean_vals + std_vals,
                color=color,
                alpha=0.15,
            )

    ax.set_xlabel("Step", fontsize=12)
    ax.set_ylabel("Cooperation Ratio (Master / N)", fontsize=12)
    ax.set_title(
        title or f"Strategy Convergence: Cooperation Ratio Over Time (N={n_agents})",
        fontsize=14,
    )
    ax.set_xlim(0, None)
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc="best", fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()
