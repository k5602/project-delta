from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from mesa.visualization import SolaraViz

from edu_game_model import EduGameModel
from student_agent import Strategy
from visualization import DashboardTabLayout, model_params


initial_model = EduGameModel(n_agents=20, strategy=Strategy.Q_LEARNING, seed=42)

page = SolaraViz(
    model=initial_model,
    components=[DashboardTabLayout],
    model_params=model_params,
    name="EduGame Dashboard",
)
page
