# 03 - System Architecture & Communication

## System Diagram

```
┌─────────────────────────────────────────────────────┐
│                  Mesa Model Context                 │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │             EduGameModel (Controller)          │  │
│  │                                               │  │
│  │  - rng (numpy.random.default_rng)             │  │
│  │  - DataCollector (Payoffs/Distributions)    │  │
│  │  - PayoffConfig (Game Parameters)             │  │
│  └──────────────────────┬────────────────────────┘  │
│                         │ agents.shuffle_do("step") │
│                         ▼                           │
│  ┌─────────────┐      Pairs &      ┌───────────┐     │
│  │ StudentAgent│◄─── Payoffs ───► │ StudentAgent│   │
│  │  (Agent 1)  │                  │  (Agent 2) │    │
│  └─────────────┘                  └───────────┘    │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │            PayoffEngine (Core Logic)          │   │
│  │  (Stateless: computes payoff pairs)         │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Role |
|---|---|
| `EduGameModel` | Top-level controller. Manages simulation lifecycle, pairing, data collection, and time advancement. Uses `rng` (numpy RNG) for reproducible shuffling. |
| `StudentAgent` | Decision-maker. Inherits from `mesa.Agent`. Implements Q-learning with optimistic initialization (value=80). |
| `DataCollector` | Built-in Mesa tool. Logs model-level metrics each step via `model_reporters`. |
| `PayoffEngine` | Stateless function. Computes payoff pairs for given actions. |
| `batch_runner` | SeedSequence-based batch infrastructure. Runs multiple independent simulations. |
| `comparison_engine` | Runs all strategies under identical conditions for fair comparison. |
| `visualization` | Matplotlib-based convergence plotting with shaded std bands. |


## Interaction Protocol

### Round Sequence (one `model.step()` call)
1. **Action Selection**: `agents.shuffle_do("step")` → each `StudentAgent.select_action()` sets `last_action`
2. **Pairing**: Model shuffles agents and pairs them via `_pair_agents()`
3. **Payoff Computation**: `compute_payoff()` for each pair
4. **Feedback**: Each agent receives payoff and updates Q-table (`receive_payoff`)
5. **State Advance**: `agents.do("advance")` → each agent sets `last_opponent_action`
6. **Data Collection**: `datacollector.collect(self)` records metrics

### Time Advancement
```
model.run_for(1000)   # Run 1000 steps
model.steps             # Current step count
```