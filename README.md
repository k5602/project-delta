# Project Delta

A computational proof of the game-theoretic model for programming education using multi-agent simulation based on a research i started last january.

## Overview

This project demonstrates how individual rationality in a competitive academic environment leads to collectively suboptimal outcomes - a classic **Prisoner's Dilemma**.

### The Game

|           | Master (M) | Dependent (P) |
|-----------|------------|---------------|
| **Master (M)**   | (80, 80)   | (35, 90)      |
| **Dependent (P)**| (90, 35)   | (45, 45)      |

- **M** (Master): Deep study + AI utility
- **P** (Dependent): Surface learning + AI dependency
- **Nash Equilibrium**: `(P, P)` - both defect
- **Pareto Optimal**: `(M, M)` - cooperation

## Installation

```bash
uv sync
```

## Usage

```bash
# Run simulation with Q-learning agents
uv run python main.py -n 20 -s 1000 --seed 42

# Compare strategies
uv run python main.py -n 20 -s 500 --compare --runs 5

# Export results to CSV
uv run python main.py -n 20 -s 1000 --output results.csv
```

### Interactive Dashboard

Launch the live SolaraViz dashboard:

```bash
uv run python main.py --serve
```

The dashboard provides:
- **Network graph** - agents as nodes (blue=Master, red=Dependent), edges = current pairings
- **Master Count** - time-series of Master/Dependent agent counts per step
- **Mean Payoff** - time-series of mean agent payoff per step
- **Q-Table Stats** - grouped bar chart of mean Q-values by (opponent_action, my_action) state

Sliders control `n_agents`, `strategy`, and `rng` (random seed).

### CLI Options

| Flag | Description | Default |
|------|-------------|---------|
| `-n, --agents` | Number of agents | 20 |
| `-s, --steps` | Simulation steps | 1000 |
| `--seed` | Random seed | None |
| `--strategy` | Agent strategy | q_learning |
| `--output` | CSV output path | None |
| `--runs` | Number of batch runs | 5 |
| `--batch` | Run in batch mode | False |
| `--compare` | Compare all strategies (print summary) | False |
| `--serve` | Launch SolaraViz interactive dashboard | False |

### Strategies

- `q_learning` - Q-learning with epsilon-greedy exploration (default)
- `tit_for_tat` - Cooperate initially, then mirror opponent
- `grim_trigger` - Cooperate until defection, then always defect
- `random` - Random action selection

## Testing

```bash
uv run pytest -v
```

## Theory

See [docs/](./docs/) for theoretical foundations:

- `01_overview.md` - Project overview
- `02_theory.md` - Game theory foundations
- `03_architecture.md` - System design
