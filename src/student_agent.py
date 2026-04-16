from collections import defaultdict
from enum import Enum, auto
from typing import Optional

import mesa

from src.payoff_config import Action


class Strategy(Enum):
    Q_LEARNING = auto()
    TIT_FOR_TAT = auto()
    GRIM_TRIGGER = auto()
    RANDOM = auto()


class StudentAgent(mesa.Agent):
    def __init__(
        self,
        model: mesa.Model,
        strategy: Strategy = Strategy.Q_LEARNING,
        alpha: float = 0.1,
        gamma: float = 0.95,
        epsilon: float = 0.1,
    ) -> None:
        super().__init__(model)
        self.strategy = strategy
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

        self.q_table: dict[tuple[Optional[Action], Action], float] = defaultdict(
            lambda: 80.0
        )
        self.last_opponent_action: Optional[Action] = None
        self.last_action: Optional[Action] = None
        self.payoff: int = 0

    def _get_state(self) -> tuple[Optional[Action], Action]:
        return (self.last_opponent_action, self.last_action)

    def select_action(self) -> Action:
        if self.strategy == Strategy.RANDOM:
            return self.model.rng.choice(list(Action))

        if self.strategy == Strategy.TIT_FOR_TAT:
            if self.last_opponent_action is None:
                return Action.MASTER
            return self.last_opponent_action

        if self.strategy == Strategy.GRIM_TRIGGER:
            if self.last_opponent_action is None:
                return Action.MASTER
            if self.last_opponent_action == Action.DEPENDENT:
                return Action.DEPENDENT
            return Action.MASTER

        if self.strategy == Strategy.Q_LEARNING:
            if self.model.rng.random() < self.epsilon:
                return self.model.rng.choice(list(Action))

            state = (self.last_opponent_action, None)
            q_master = self.q_table[(state[0], Action.MASTER)]
            q_dependent = self.q_table[(state[0], Action.DEPENDENT)]

            if q_master >= q_dependent:
                return Action.MASTER
            return Action.DEPENDENT

        return Action.DEPENDENT

    def update_q(
        self, opponent_action: Action, reward: int, next_state: Optional[Action]
    ) -> None:
        if self.strategy != Strategy.Q_LEARNING:
            return

        state = self._get_state()

        best_next_q = max(
            self.q_table[(next_state, Action.MASTER)],
            self.q_table[(next_state, Action.DEPENDENT)],
        )

        self.q_table[state] += self.alpha * (
            reward + self.gamma * best_next_q - self.q_table[state]
        )

    def receive_payoff(self, payoff: int, opponent_action: Optional[Action]) -> None:
        self.payoff = payoff
        if opponent_action is not None:
            self.update_q(opponent_action, payoff, None)

    def step(self) -> None:
        self.last_action = self.select_action()

    def advance(self) -> None:
        self.last_opponent_action = self.last_action
