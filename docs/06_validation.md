# 07 - Expected Results and Validation

## Baseline Condition
In a population of rational Q-learners, we expect:
- **Rounds 1–100:** High exploration, mixed strategies.
- **Rounds 100–400:** Gradual shift toward the dominant strategy `P`.
- **Rounds 400–1000:** Stabilization at ~90% `P` (Nash Equilibrium).
- **Average Payoff:** Stabilizes near 45 (collectively suboptimal).

## Comparison: Tit-for-Tat
If the population uses TfT:
- Cooperation should hold as long as agents are "patient" (`γ > 0.22`).
- This validates the **Folk Theorem** predictions.

## Validation Checklist
- [ ] Does baseline converge to `(P, P)`?
- [ ] Is the cooperation threshold verified at `δ ≈ 0.22`?
- [ ] Does Tit-for-Tat sustain higher average payoffs than Q-learning?
- [ ] Are results reproducible with a fixed `RANDOM_SEED`?

## Limitations
- **Binary Strategy:** Real behavior is more complex than a simple M/P choice.
- **Random Pairing:** Real social networks are not perfectly random.
