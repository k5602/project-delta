# Implementation Roadmap

## Phase 1: Core Engine (Days 1–2)
- [x] Implement `PayoffConfig` and `compute_payoff()` in `core/payoff_engine.py`.
- [x] Write unit tests for the Prisoner's Dilemma structure.
- [x] Verify Q-learning update logic in isolation.

## Phase 2: Mesa Setup (Days 3–4)
- [x] Install Mesa and define the `EduGameModel` skeleton.
- [x] Implement `StudentAgent` inheriting from `mesa.Agent`.
- [x] Configure `RandomActivation` scheduler.
- [x] Verify two agents can complete a step and receive payoffs.

## Phase 3: Population Simulation (Days 5–6)
- [x] Implement random pairing logic inside `EduGameModel.step()`.
- [x] Set up `DataCollector` to track counts of "M" and "P".
- [x] Scale to $N=20$ and run 1000 rounds.
- [x] Confirm baseline convergence to $(P, P)$.

## Phase 4: Strategy Variations (Days 7–8)
- [x] Implement Tit-for-Tat and Grim Trigger modes in `StudentAgent`.
- [x] Add CLI flags to `main.py` to switch strategy modes.
- [x] Compare convergence curves across different strategies.

## Phase 5: Visualization (Days 9–10)
- [ ] Use Mesa's `ModularServer` for a browser-based dashboard for the actual simulation and every round rewards.
- [ ] Add line charts for strategy distribution.
- [ ] Add grid visualization for spatial interaction (if applicable).
- [ ] Export simulation logs to CSV for report inclusion.
