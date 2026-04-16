import pandas as pd

from src.batch_runner import aggregate_runs, run_batch, run_comparison_batch
from src.student_agent import Strategy


class TestRunBatch:
    def test_returns_dataframe_with_expected_columns(self):
        df = run_batch(
            strategy=Strategy.Q_LEARNING, n_agents=10, steps=50, n_runs=2, seed=42
        )
        assert isinstance(df, pd.DataFrame)
        assert "run" in df.columns
        assert "index" in df.columns
        assert len(df["run"].unique()) == 2

    def test_all_steps_collected(self):
        df = run_batch(
            strategy=Strategy.Q_LEARNING, n_agents=10, steps=100, n_runs=2, seed=42
        )
        assert df["index"].max() == 99

    def test_different_seeds_generate_different_seeds(self):
        import numpy as np

        master1 = np.random.default_rng(1)
        master2 = np.random.default_rng(2)

        seeds1 = [master1.integers(0, 2**31) for _ in range(5)]
        seeds2 = [master2.integers(0, 2**31) for _ in range(5)]

        assert seeds1 != seeds2, (
            "Different master seeds should produce different run seeds"
        )


class TestAggregateRuns:
    def test_aggregated_df_has_mean_and_std_columns(self):
        df = run_batch(
            strategy=Strategy.TIT_FOR_TAT, n_agents=10, steps=20, n_runs=3, seed=99
        )
        agg = aggregate_runs(df)
        assert "step" in agg.columns
        for col in agg.columns:
            if col != "step":
                assert "mean" in col or "std" in col

    def test_std_is_nan_for_single_run(self):
        df = run_batch(
            strategy=Strategy.RANDOM, n_agents=10, steps=10, n_runs=1, seed=42
        )
        agg = aggregate_runs(df)
        for col in agg.columns:
            if col != "index" and "std" in col:
                assert agg[col].isna().all()


class TestRunComparisonBatch:
    def test_all_strategies_produced(self):
        results = run_comparison_batch(n_agents=10, steps=20, n_runs=2, seed=42)
        assert len(results) == 4

    def test_strategies_have_mean_and_std(self):
        results = run_comparison_batch(n_agents=10, steps=20, n_runs=2, seed=42)
        for df in results.values():
            cols = df.columns.tolist()
            has_mean = any("mean" in c for c in cols)
            has_std = any("std" in c for c in cols)
            assert has_mean, "missing mean columns"
            assert has_std, "missing std columns"
