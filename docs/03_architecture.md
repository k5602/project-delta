# 03 - System Architecture & Communication

## System Diagram

In Mesa, the simulation is managed by a central **Model** class, which contains the **Scheduler** (turns) and the **Space** (interaction rules).

```
┌─────────────────────────────────────────────────────┐
│                  Mesa Model Context                 │
│                                                     │
│  ┌───────────────────────────────────────────────┐  │
│  │             EduGameModel (Controller)          │  │
│  │                                               │  │
│  │  - Scheduler (RandomActivation)               │  │
│  │  - DataCollector (Payoffs/Distributions)      │  │
│  │  - PayoffConfig (Broadcaster)                 │  │
│  └──────────────────────┬────────────────────────┘  │
│                         │ Calls .step() on each     │
│                         ▼                           │
│  ┌─────────────┐      Pairs &      ┌───────────┐    │
│  │ StudentAgent│◄─── Payoffs ───► │ StudentAgent│   │
│  │  (Agent 1)  │                   │  (Agent 2) │   │
│  └─────────────┘                   └───────────┘    │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │            PayoffEngine (Core Logic)         │   │
│  │  (Stateless: computes payoff pairs)          │   │
│  └──────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

## Component Responsibilities

| Component | Role |
|---|---|
| `EduGameModel` | The top-level controller. Manages the simulation lifecycle, pairing, and data collection. |
| `StudentAgent` | Decision-maker. Inherits from `mesa.Agent`. Implements Q-learning in its `step()`. |
| `Scheduler` | Mesa's `RandomActivation`. Ensures each agent acts exactly once per round. |
| `DataCollector` | Built-in Mesa tool. Automatically logs population-wide strategy distributions. |
| `PayoffEngine` | Stateless logic. Used by the Model to determine rewards for paired actions. |

## Interaction Protocol

Mesa uses direct method calls and model properties, making it much easier to reason about the simulation state compared to asynchronous messaging systems SPADA .

### Round Sequence
1.  **Model Step:** The simulation advances to the next tick.
2.  **Scheduler:** Calls `step()` for every `StudentAgent`.
3.  **Decision:** Each agent queries the `model.payoff_config` and selects an action (`M` or `P`).
4.  **Pairing:** The model gathers all actions, pairs agents randomly, and computes payoffs via the `PayoffEngine`.
5.  **Feedback:** The model passes the payoff back to the agent (e.g., `agent.payoff = 45`).
6.  **Learning:** In the next step (or a separate `advance()` phase), agents update their Q-tables based on the received payoff.
