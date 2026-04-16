from typing import Optional

import numpy as np
import pandas as pd

from edu_game_model import EduGameModel
from student_agent import Strategy


def run_batch(
    strategy: Strategy,
    n_agents: int = 20,
    steps: int = 1000,
    n_runs: int = 5,
    seed: Optional[int] = None,
) -> pd.DataFrame:
    """Run multiple independent simulations and concatenate results.

    Uses np.random.SeedSequence to spawn n_runs child RNGs from a single master seed,
    ensuring reproducibility while generating independent runs.
    """
    master_rng = np.random.default_rng(seed)
    runs_data: list[pd.DataFrame] = []

    for run_idx in range(n_runs):
        run_seed = master_rng.integers(0, 2**31)
        model = EduGameModel(
            n_agents=n_agents,
            strategy=strategy,
            seed=run_seed,
        )
        model.run_for(steps)

        df = model.datacollector.get_model_vars_dataframe().reset_index()
        df = df.copy()
        df["run"] = run_idx
        runs_data.append(df)

    return pd.concat(runs_data, ignore_index=True)


def aggregate_runs(
    df: pd.DataFrame, value_cols: list[str] | None = None
) -> pd.DataFrame:
    """Compute mean and std across runs for each step.

    Args:
        df: DataFrame with columns including 'run' and step-level metrics.
        value_cols: Columns to aggregate. Defaults to numeric columns excluding 'run'.

    Returns:
        DataFrame with 'step' and mean/std columns for each metric.
    """
    if value_cols is None:
        value_cols = [
            c
            for c in df.columns
            if c not in ("run", "index") and df[c].dtype in (int, float)
        ]

    agg = df.groupby("index")[value_cols].agg(["mean", "std"])
    agg.columns = ["_".join(col).strip() for col in agg.columns.values]
    agg = agg.reset_index()
    agg = agg.rename(columns={"index": "step"})
    return agg


def run_comparison_batch(
    n_agents: int = 20,
    steps: int = 1000,
    n_runs: int = 5,
    seed: Optional[int] = None,
) -> dict[Strategy, pd.DataFrame]:
    """Run batch simulations for all four strategies and aggregate results.

    Uses the same child seeds for each strategy so they start from identical
    conditions, making comparisons fair.
    """
    master_rng = np.random.default_rng(seed)

    results: dict[Strategy, pd.DataFrame] = {}
    for strategy in Strategy:
        strategy_runs: list[pd.DataFrame] = []
        for run_idx in range(n_runs):
            run_seed = master_rng.integers(0, 2**31)
            model = EduGameModel(
                n_agents=n_agents,
                strategy=strategy,
                seed=run_seed,
            )
            model.run_for(steps)

            df = model.datacollector.get_model_vars_dataframe().reset_index().copy()
            df["run"] = run_idx
            strategy_runs.append(df)

        combined = pd.concat(strategy_runs, ignore_index=True)
        results[strategy] = aggregate_runs(combined)

    return results
