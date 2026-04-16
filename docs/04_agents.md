# 04 - Agent Specifications

## 4.1 StudentAgent

In Mesa, all agents inherit from `mesa.Agent`.

### Internal State
- `unique_id`: Integer ID provided by Mesa.
- `q_table`: Dictionary mapping actions (`M`, `P`) to estimated values.
- `epsilon`: Exploration rate (decays per step).
- `last_action`: Stores the action taken in the current round.
- `last_payoff`: Stores the reward received for the action.

### Methods
- `step()`: Core logic called by the scheduler.
  1.  Retrieves `payoff_config` from `self.model`.
  2.  Selects action (ε-greedy or fixed strategy).
  3.  Stores action for the model to process.
- `update_q()`: Updates the Q-table after the model calculates the round payoff.
- `_tit_for_tat_action()`: Strategy-specific logic (uses `self.model.get_opponent_last_move()`).

---

## 4.2 Model-Level Logic (The "Professor")

In Mesa, the "Professor" and "Environment" roles from the SPADE architecture are consolidated into the `EduGameModel` class.

### EduGameModel (Inherits from `mesa.Model`)
- `schedule`: Instance of `RandomActivation`.
- `payoff_config`: Instance of `PayoffConfig`.
- `datacollector`: Mesa tool to track counts of `M` vs `P`.

### Model Step Workflow
1.  Shuffle and activate all agents (calls `agent.step()`).
2.  Collect actions from all agents.
3.  Shuffle agents again to create pairs.
4.  Compute payoffs for each pair.
5.  Assign payoffs back to agents.
6.  Call `agent.update_q()` (if using `SimultaneousActivation` or custom loop).
7.  Trigger `datacollector.collect(self)`.

---

## 4.4 DashboardAgent (Visualization)

Mesa provides a built-in interactive server (`ModularServer`) that can render:
- **Line Charts:** Real-time population distribution.
- **Grids/Networks:** If the simulation is expanded to include spatial interaction.
- **Payoff History:** Cumulative rewards per strategy type.
