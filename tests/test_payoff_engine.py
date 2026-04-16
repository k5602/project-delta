from payoff_config import Action, PayoffConfig
from payoff_engine import compute_payoff


class TestPayoffEngine:
    def test_mutual_master_returns_reward(self):
        payoff = compute_payoff(Action.MASTER, Action.MASTER)
        assert payoff == (80, 80)

    def test_mutual_dependent_returns_punishment(self):
        payoff = compute_payoff(Action.DEPENDENT, Action.DEPENDENT)
        assert payoff == (45, 45)

    def test_master_dependent_returns_sucker_temptation(self):
        payoff = compute_payoff(Action.MASTER, Action.DEPENDENT)
        assert payoff == (35, 90)

    def test_dependent_master_returns_temptation_sucker(self):
        payoff = compute_payoff(Action.DEPENDENT, Action.MASTER)
        assert payoff == (90, 35)

    def test_custom_config(self):
        config = PayoffConfig(R=70, T=85, S=30, P=40)
        payoff = compute_payoff(Action.MASTER, Action.MASTER, config)
        assert payoff == (70, 70)

    def test_nash_equilibrium_property(self):
        payoff_pp = compute_payoff(Action.DEPENDENT, Action.DEPENDENT)
        payoff_mp = compute_payoff(Action.MASTER, Action.DEPENDENT)
        payoff_pm = compute_payoff(Action.DEPENDENT, Action.MASTER)

        assert payoff_pp[1] < payoff_mp[1]
        assert payoff_pp[0] < payoff_pm[0]

    def test_temptation_greater_than_reward(self):
        config = PayoffConfig()
        assert config.T > config.R

    def test_punishment_less_than_reward(self):
        config = PayoffConfig()
        assert config.P < config.R
