from __future__ import annotations

import argparse
import sys

from batch_runner import aggregate_runs, run_batch
from comparison_engine import compare_strategies, print_summary
from edu_game_model import EduGameModel
from student_agent import Strategy
from visualization import plot_convergence


# this file grew unexpectedly large as I added more features, so it needs some refactoring after visualization step
# TODO!
def run_single(
    n_agents: int,
    steps: int,
    strategy: Strategy,
    seed: int | None,
    output: str | None,
) -> None:
    """Run a single simulation and print progress."""
    model = EduGameModel(n_agents=n_agents, strategy=strategy, seed=seed)
    model.run_for(steps)

    df = model.datacollector.get_model_vars_dataframe()
    last = df.iloc[-1]
    print(
        f"Final: Step {steps} — Master={last['master_count']}, "
        f"Dependent={last['dependent_count']}, "
        f"Mean payoff={last['mean_payoff']:.1f}"
    )

    if output:
        df.to_csv(output, index=False)
        print(f"Results saved to {output}")


def run_batch_mode(
    n_agents: int,
    steps: int,
    n_runs: int,
    strategy: Strategy,
    seed: int | None,
    output: str | None,
) -> None:
    """Run multiple independent simulations and aggregate."""
    print(
        f"Running {n_runs} batch runs: {n_agents} agents, {steps} steps, strategy={strategy.name}"
    )
    df = run_batch(strategy=strategy, n_agents=n_agents, steps=steps, n_runs=n_runs, seed=seed)
    agg = aggregate_runs(df)

    last_step = agg.iloc[-1]
    print(f"\nBatch summary (step {last_step['step']}):")
    for col in agg.columns:
        if col != "step":
            print(
                f"  {col}: {last_step[col]:.2f}"
                if isinstance(last_step[col], float)
                else f"  {col}: {last_step[col]}"
            )

    if output:
        agg.to_csv(output, index=False)
        print(f"Results saved to {output}")


def run_compare_mode(
    n_agents: int,
    steps: int,
    n_runs: int,
    seed: int | None,
) -> None:
    """Run all strategies and display comparison visualization."""
    print(f"Comparing all strategies: {n_agents} agents, {steps} steps, {n_runs} runs per strategy")
    results = compare_strategies(n_agents=n_agents, steps=steps, n_runs=n_runs, seed=seed)
    print_summary(results, n_agents)
    plot_convergence(results, n_agents)


def main() -> int:
    parser = argparse.ArgumentParser(
        description=("a computational proof of the game-theoretic model for programming education")
    )
    parser.add_argument(
        "-n", "--agents", type=int, default=20, help="Number of agents (default: 20)"
    )
    parser.add_argument(
        "-s",
        "--steps",
        type=int,
        default=1000,
        help="Number of simulation steps (default: 1000)",
    )
    parser.add_argument(
        "--seed", type=int, default=None, help="Master random seed for reproducibility"
    )
    parser.add_argument(
        "--strategy",
        type=str,
        choices=["q_learning", "tit_for_tat", "grim_trigger", "random"],
        default="q_learning",
        help="Agent strategy (default: q_learning)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV file for results",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=5,
        help="Number of batch runs (default: 5)",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Run in batch mode (multiple independent simulations)",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare all strategies with visualization",
    )
    args = parser.parse_args()

    strategy_map = {
        "q_learning": Strategy.Q_LEARNING,
        "tit_for_tat": Strategy.TIT_FOR_TAT,
        "grim_trigger": Strategy.GRIM_TRIGGER,
        "random": Strategy.RANDOM,
    }
    strategy = strategy_map[args.strategy]

    if args.compare:
        run_compare_mode(
            n_agents=args.agents,
            steps=args.steps,
            n_runs=args.runs,
            seed=args.seed,
        )
    elif args.batch:
        run_batch_mode(
            n_agents=args.agents,
            steps=args.steps,
            n_runs=args.runs,
            strategy=strategy,
            seed=args.seed,
            output=args.output,
        )
    else:
        run_single(
            n_agents=args.agents,
            steps=args.steps,
            strategy=strategy,
            seed=args.seed,
            output=args.output,
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
