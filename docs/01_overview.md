# 01 - Project Overview

This project implements a **Multi-Agent System (MAS)** using the **Mesa** framework. It serves as a computational proof of the game-theoretic model for programming education. The simulation demonstrates how individual rationality in a competitive academic environment can lead to collectively suboptimal outcomes -> a classic Prisoner's Dilemma.

## What the Simulation Does

- **Autonomous Population:** Instantiates `StudentAgent` entities using Mesa's `Agent` class.
- **Strategic Games:** Models the **Study Investment Game** and the **AI Tool Adoption Game**.
- **Learning Agents:** Implements **Q-Learning** within the agents' `step()` methods so they adapt based on payoffs and optimistic initial.
- **Scheduler:** Uses Mesa's `RandomActivation` to handle agent turns in each round.
- **Visualization:** Tracks strategy convergence over time (e.g., 1000 rounds) using Mesa's `DataCollector`.

## Why Mesa?

At first i thought of SPADE and intended to use FIPA-ACL for more realistic modelling but i've found it's overengineering for my case,so i chose **Mesa** as it is optimized for Agent-Based Modeling (ABM) on a single machine. It provides:
1.  **Synchronous Scheduling:** No need for complex XMPP server setups.
2.  **Built-in Data Collection:** Easier tracking of payoffs and strategy counts.
3.  **Performance:** Significantly faster execution for 1000+ rounds.

---

## Worked Example: One Complete Round

Trace of a single round in the `EduGameModel`:

**Setup:** Population of agents initialized.
**Model Step:**

1.  **Model-Level Broadcaster:** The `EduGameModel` provides the current `PayoffConfig` (R=80, T=90, S=35, P=45) as a property available to all agents.
2.  **Agent Actions:** The `RandomActivation` scheduler calls `step()` on every `StudentAgent`.
    - Ahmed explores and chooses "Master" (`M`).
    - Karim explores and chooses "Dependent" (`P`).
3.  **Pairing and Payoff:** The model pairs Mohamed and Karim randomly.
    - `PayoffEngine` calculates `(35, 90)`.
4.  **Learning:** Alice and Karim receive their payoffs and update their internal **Q-tables**.
5.  **Data Collection:** The `DataCollector` records the number of "Master" vs. "Dependent" choices in the population.

**Result:** Over many steps, the population stabilizes at the Nash Equilibrium `(P, P)`.
