import argparse
import sys

from edu_game_model import EduGameModel
from student_agent import Strategy


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "a computational proof of the game-theoretic model "
            "for programming education"
        )
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
        "--seed", type=int, default=None, help="Random seed for reproducibility"
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
    args = parser.parse_args()

    strategy_map = {
        "q_learning": Strategy.Q_LEARNING,
        "tit_for_tat": Strategy.TIT_FOR_TAT,
        "grim_trigger": Strategy.GRIM_TRIGGER,
        "random": Strategy.RANDOM,
    }
    strategy = strategy_map[args.strategy]

    print(
        f"Running simulation: {args.agents} agents, {args.steps} steps, "
        f"strategy={args.strategy}"
    )

    model = EduGameModel(n_agents=args.agents, strategy=strategy, seed=args.seed)

    for i in range(args.steps):
        model.step()
        if (i + 1) % 100 == 0:
            df = model.datacollector.get_model_vars_dataframe()
            last = df.iloc[-1]
            print(
                f"Step {i + 1}: Master={last['master_count']}, "
                f"Dependent={last['dependent_count']}, "
                f"Mean payoff={last['mean_payoff']:.1f}"
            )

    if args.output:
        df = model.datacollector.get_model_vars_dataframe()
        df.to_csv(args.output, index=False)
        print(f"Results saved to {args.output}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
