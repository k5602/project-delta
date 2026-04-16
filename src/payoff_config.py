from dataclasses import dataclass
from enum import Enum, auto


class Action(Enum):
    MASTER = auto()
    DEPENDENT = auto()

    def __repr__(self) -> str:
        return self.name[0]


@dataclass(frozen=True)
class PayoffConfig:
    R: int = 80
    T: int = 90
    S: int = 35
    P: int = 45

    def get_payoff(self, action_a: Action, action_b: Action) -> tuple[int, int]:
        if action_a is Action.MASTER and action_b is Action.MASTER:
            return (self.R, self.R)
        if action_a is Action.MASTER and action_b is Action.DEPENDENT:
            return (self.S, self.T)
        if action_a is Action.DEPENDENT and action_b is Action.MASTER:
            return (self.T, self.S)
        return (self.P, self.P)
