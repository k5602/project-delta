from __future__ import annotations

from mesa.visualization import SolaraViz

from src.edu_game_model import EduGameModel
from src.student_agent import Strategy
from src.visualization import DashboardTabLayout, model_params


initial_model = EduGameModel(n_agents=20, strategy=Strategy.Q_LEARNING, seed=42)

page = SolaraViz(
    model=initial_model,
    components=[DashboardTabLayout],
    model_params=model_params,
    name="EduGame Dashboard",
)
page
