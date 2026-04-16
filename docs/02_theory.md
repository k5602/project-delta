# 02 - Theoretical Foundation

## 2.1 The Three Games

The simulation is built on three nested strategic games that model student choices.

### Game 1: Study Investment Game
| | Deep Study (D) | Surface Learning (S) |
|---|---|---|
| **Deep Study (D)** | (70, 70) | (30, 80) |
| **Surface Learning (S)** | (80, 30) | (40, 40) |
- **Nash Equilibrium:** `(S, S)` (Surface learning dominates).
- **Pareto Optimum:** `(D, D)` (Collectively better).

### Game 2: AI Tool Adoption Game
| | AI Utility (U) | AI Dependency (D) |
|---|---|---|
| **AI Utility (U)** | (75, 75) | (45, 85) |
| **AI Dependency (D)** | (85, 45) | (50, 50) |
- **Nash Equilibrium:** `(D, D)`.

### Game 3: Combined (Master vs. Dependent)
| | Master (M) | Dependent (P) |
|---|---|---|
| **Master (M)** | (80, 80) | (35, 90) |
| **Dependent (P)** | (90, 35) | (45, 45) |
- `M = Deep Study + AI Utility`
- `P = Surface Learning + AI Dependency`

## 2.2 Folk Theorem - Cooperation Threshold

Cooperation `(M, M)` is sustainable under "Grim Trigger" strategies if the discount factor `δ` (patience) is high enough:
`δ > (T - R) / (T - P) = (90 - 80) / (90 - 45) ≈ 0.22`

## 2.3 Tit-for-Tat

Agents can optionally switch to **Tit-for-Tat**: cooperate on the first round, then mirror the opponent's previous move. This strategy is more robust to noise than Grim Trigger.

## 2.4 Assumptions

| Assumption | Justification |
|---|---|
| **Binary strategy space** | Keeps the game tractable while capturing the core tension. |
| **Random pairing** | Mirrors anonymous peer interactions in large environments. |
| **Perfect information** | Agents observe the payoff structure before acting. |
| **Synchronous rounds** | Simplifies message sequencing in the MAS. |
| **Deterministic Learning** | Focuses on convergence properties of Q-learning. |
