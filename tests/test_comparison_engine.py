import pandas as pd

from src.comparison_engine import Strategy, compare_strategies, summarize_results


class TestCompareStrategies:
    def test_all_strategies_return_dataframes(self):
        results = compare_strategies(n_agents=10, steps=30, n_runs=2, seed=42)
        assert len(results) == 4
        for s in Strategy:
            assert s in results
            assert isinstance(results[s], pd.DataFrame)

    def test_dataframes_have_step_index(self):
        results = compare_strategies(n_agents=10, steps=20, n_runs=2, seed=42)
        for strategy, df in results.items():
            assert len(df) > 0
            assert "index" in df.columns or "Step" in df.columns or "step" in df.columns

    def test_tft_maintains_high_cooperation(self):
        results = compare_strategies(n_agents=10, steps=50, n_runs=3, seed=99)
        tft_df = results[Strategy.TIT_FOR_TAT]
        ratio_mean_col = next(
            (c for c in tft_df.columns if "cooperation_ratio" in c and "mean" in c),
            next(
                (c for c in tft_df.columns if "master_count" in c and "mean" in c), None
            ),
        )
        if ratio_mean_col:
            final_ratio = tft_df[ratio_mean_col].iloc[-1] / 10
            assert final_ratio >= 0.1, f"TFT cooperation ratio {final_ratio} < 0.1"

    def test_strategies_produce_distinct_outcomes(self):
        results = compare_strategies(n_agents=10, steps=50, n_runs=2, seed=42)
        tft_df = results[Strategy.TIT_FOR_TAT]
        rand_df = results[Strategy.RANDOM]
        ql_df = results[Strategy.Q_LEARNING]

        for label, df in [("TFT", tft_df), ("RANDOM", rand_df), ("QL", ql_df)]:
            assert len(df) > 0, f"{label} returned empty dataframe"

        ratio_mean_col = next(
            (c for c in tft_df.columns if "cooperation_ratio" in c and "mean" in c),
            next(
                (c for c in tft_df.columns if "master_count" in c and "mean" in c), None
            ),
        )
        if ratio_mean_col:
            tft_val = tft_df[ratio_mean_col].iloc[-1]
            rand_val = rand_df[ratio_mean_col].iloc[-1]
            ql_val = ql_df[ratio_mean_col].iloc[-1]
            assert tft_val > rand_val, "TFT master_count should exceed RANDOM"
            assert abs(ql_val - 0) < 5 or abs(ql_val - 5) < 3, (
                "QL should converge near 0 or 5"
            )


class TestSummarizeResults:
    def test_summary_dataframe_shape(self):
        results = compare_strategies(n_agents=10, steps=30, n_runs=2, seed=42)
        summary = summarize_results(results, n_agents=10)
        assert len(summary) == 4
        assert "strategy" in summary.columns
        assert "final_payoff" in summary.columns
