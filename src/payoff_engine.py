from src.payoff_config import Action, PayoffConfig


def compute_payoff(
    action_a: Action, action_b: Action, config: PayoffConfig | None = None
) -> tuple[int, int]:
    if config is None:
        config = PayoffConfig()
    return config.get_payoff(action_a, action_b)
