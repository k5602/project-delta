from itertools import pairwise

import mesa
import numpy as np

from payoff_config import Action, PayoffConfig
from payoff_engine import compute_payoff
from student_agent import Strategy, StudentAgent


class EduGameModel(mesa.Model):
    def __init__(
        self,
        n_agents: int,
        payoff_config: PayoffConfig | None = None,
        strategy: Strategy = Strategy.Q_LEARNING,
        seed: int | None = None,
    ) -> None:
        self.rng_ = (
            np.random.default_rng(seed) if seed is not None else np.random.default_rng()
        )
        super().__init__(rng=self.rng_)
        self.payoff_config = payoff_config or PayoffConfig()
        self.strategy = strategy
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "master_count": lambda m: sum(
                    1 for a in m.agents if a.last_action == Action.MASTER
                ),
                "dependent_count": lambda m: sum(
                    1 for a in m.agents if a.last_action == Action.DEPENDENT
                ),
                "mean_payoff": lambda m: (
                    sum(a.payoff for a in m.agents) / m.num_agents
                    if m.num_agents > 0
                    else 0
                ),
                "max_payoff": lambda m: max((a.payoff for a in m.agents), default=0),
                "min_payoff": lambda m: min((a.payoff for a in m.agents), default=0),
                "mean_q_master": lambda m: (
                    sum(a.q_table[(None, Action.MASTER)] for a in m.agents)
                    / m.num_agents
                    if m.num_agents > 0
                    else 0
                ),
                "cooperation_ratio": lambda m: (
                    sum(1 for a in m.agents if a.last_action == Action.MASTER)
                    / m.num_agents
                    if m.num_agents > 0
                    else 0.0
                ),
            }
        )

        for _ in range(n_agents):
            StudentAgent(self, strategy=strategy)

        self._pairings: list[tuple[StudentAgent, StudentAgent]] = []

    @property
    def num_agents(self) -> int:
        return len(self.agents)

    def _pair_agents(self):
        agents = list(self.agents)
        self.rng_.shuffle(agents)

        if len(agents) % 2 != 0:
            agents.append(agents[0])

        for a, b in pairwise(agents):
            yield (a, b)

    def step(self) -> None:
        self.agents.shuffle_do("step")

        self._pairings = list(self._pair_agents())

        for agent_a, agent_b in self._pairings:
            payoff_a, payoff_b = compute_payoff(
                agent_a.last_action, agent_b.last_action, self.payoff_config
            )

            agent_a.receive_payoff(payoff_a, agent_b.last_action)
            agent_b.receive_payoff(payoff_b, agent_a.last_action)

        self.agents.do("advance")
        self.datacollector.collect(self)
