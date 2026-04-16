from __future__ import annotations

from typing import Optional

import pandas as pd

from src.batch_runner import run_comparison_batch
from src.student_agent import Strategy


def _find_col(df: pd.DataFrame, pattern: str) -> str | None:
    return next((c for c in df.columns if pattern in c and "mean" in c), None)


def compare_strategies(
    n_agents: int = 20,
    steps: int = 1000,
    n_runs: int = 5,
    seed: Optional[int] = None,
) -> dict[Strategy, pd.DataFrame]:
    """Run batch simulations for all strategies and return aggregated data."""
    return run_comparison_batch(
        n_agents=n_agents, steps=steps, n_runs=n_runs, seed=seed
    )


def summarize_results(
    results: dict[Strategy, pd.DataFrame],
    n_agents: int,
    final_steps: int | None = None,
) -> pd.DataFrame:
    """Summarize final-step statistics for each strategy."""
    rows = []
    for strategy, df in results.items():
        if df.empty:
            continue

        last_n = max(10, int(len(df) * 0.1)) if final_steps is None else final_steps
        tail = df.tail(last_n)

        master_col = _find_col(df, "master_count")
        payoff_col = _find_col(df, "mean_payoff")
        ratio_col = _find_col(df, "cooperation_ratio")

        master_mean = tail[master_col].mean() if master_col else 0.0
        master_std = tail[master_col].std() if master_col else 0.0
        payoff_mean = tail[payoff_col].mean() if payoff_col else 0.0
        payoff_std = tail[payoff_col].std() if payoff_col else 0.0
        ratio_mean = tail[ratio_col].mean() if ratio_col else master_mean / n_agents
        ratio_std = tail[ratio_col].std() if ratio_col else master_std / n_agents

        rows.append(
            {
                "strategy": strategy.name,
                "final_master_ratio": f"{ratio_mean:.2f} +/- {ratio_std:.2f}",
                "final_master_count": f"{master_mean:.1f} +/- {master_std:.1f}",
                "final_payoff": f"{payoff_mean:.1f} +/- {payoff_std:.1f}",
            }
        )

    return pd.DataFrame(rows)


def print_summary(results: dict[Strategy, pd.DataFrame], n_agents: int) -> None:
    """Print a formatted summary table to stdout."""
    df = summarize_results(results, n_agents)
    cols = ["Strategy", "Master Ratio", "Master Count", "Payoff"]
    fmt = "{:<15} {:>14} {:>14} {:>14}"
    print(fmt.format(*cols))
    print("-" * 60)
    for _, row in df.iterrows():
        print(
            f"{row['strategy']:<15} "
            f"{row['final_master_ratio']:>14} "
            f"{row['final_master_count']:>14} "
            f"{row['final_payoff']:>14}"
        )
    print()
