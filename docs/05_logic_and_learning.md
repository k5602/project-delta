# 05 - Game Logic and Learning

## 5.1 Payoff Engine

The `PayoffEngine` remains a stateless utility, shared across the simulation.

```python
@dataclass
class PayoffConfig:
    R: float = 80.0   # Mutual Master (cooperation)
    T: float = 90.0   # Temptation (defect while other cooperates)
    S: float = 35.0   # Sucker (cooperate while other defects)
    P: float = 45.0   # Mutual Dependent (mutual defection)
```

### Payoff Matrix Logic
Used by the `EduGameModel` to process pairings:
- **("M", "M")**: (R, R)
- **("M", "P")**: (S, T)
- **("P", "M")**: (T, S)
- **("P", "P")**: (P, P)

---

## 5.2 Learning Algorithms

### Q-Learning
Agents update their Q-table during the model step cycle.

```python
def update_q(self):
    # Retrieve the payoff assigned to us by the model in the current step
    reward = self.last_payoff

    # Bellman update
    best_next = max(self.q_table.values())
    self.q_table[self.last_action] += self.alpha * (
        reward + self.gamma * best_next - self.q_table[self.last_action]
    )

    # Decay exploration rate
    self.epsilon = max(0.01, self.epsilon * 0.995)
```

### Strategy Modes
Since Mesa models interaction through the `Model` class, strategies like **Tit-for-Tat** can easily access history via the model's data collection or by querying neighbors.

- **Tit-for-Tat:** Mirror the move of the last paired opponent.
- **Grim Trigger:** Switch to `P` forever if any paired opponent has ever played `P`.
