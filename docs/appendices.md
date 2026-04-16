# Appendices

## Appendix A: Payoff Matrix Reference

| Game | Cooperate-Cooperate | Cooperate-Defect | Defect-Cooperate | Defect-Defect |
|---|---|---|---|---|
| Study Investment | (70, 70) | (30, 80) | (80, 30) | (40, 40) |
| AI Tool Adoption | (75, 75) | (45, 85) | (85, 45) | (50, 50) |
| **Combined (M vs P)** | **(80, 80)** | **(35, 90)** | **(90, 35)** | **(45, 45)** |

## Appendix B: Theoretical Bounds

| Parameter | Value | Description |
|---|---|---|
| `δ*` | ≈ 0.22 | Cooperation threshold (Grim Trigger). |
| `T` | 90 | Temptation to defect. |
| `R` | 80 | Reward for mutual cooperation. |
| `P` | 45 | Punishment for mutual defection. |
| `S` | 35 | Sucker's payoff. |

## Appendix C: Glossary

- **Nash Equilibrium:** A state where no player can improve their payoff by unilaterally changing strategy.
- **Pareto Optimality:** An outcome where no one can be made better off without making someone else worse off.
- **Mesa:** A Python framework for Agent-Based Modeling.
- **DataCollector:** A Mesa tool for capturing agent and model-level data during simulation.
- **Scheduler:** Controls the order in which agents take their steps (e.g., `RandomActivation`).
