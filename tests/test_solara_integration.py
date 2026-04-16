from src.edu_game_model import EduGameModel
from src.student_agent import Strategy
from src.visualization import model_params


def test_model_params_uses_seed_key() -> None:
    assert "seed" in model_params


def test_model_accepts_strategy_name_string() -> None:
    model = EduGameModel(n_agents=2, strategy="Q_LEARNING", seed=42)
    assert model.strategy == Strategy.Q_LEARNING
