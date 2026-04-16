from edu_game_model import EduGameModel
from payoff_config import Action
from student_agent import Strategy


class TestEduGameModel:
    def test_two_agents_complete_round(self):
        model = EduGameModel(n_agents=2, seed=42)
        model.step()

        assert model.num_agents == 2
        for agent in model.agents:
            assert agent.last_action is not None

    def test_baseline_converges_to_dependent(self):
        model = EduGameModel(n_agents=20, seed=42)

        for _ in range(500):
            model.step()

        master_count = sum(1 for a in model.agents if a.last_action == Action.MASTER)
        assert master_count <= 5

    def test_data_collector_records_counts(self):
        model = EduGameModel(n_agents=10, seed=42)
        model.step()

        df = model.datacollector.get_model_vars_dataframe()
        assert "master_count" in df.columns
        assert "dependent_count" in df.columns
        assert len(df) == 1

    def test_tit_for_tat_strategy(self):
        model = EduGameModel(n_agents=4, strategy=Strategy.TIT_FOR_TAT, seed=42)
        model.step()

        for agent in model.agents:
            assert agent.last_action == Action.MASTER

    def test_grim_trigger_defects_after_defection(self):
        model = EduGameModel(n_agents=2, strategy=Strategy.GRIM_TRIGGER, seed=42)
        model.step()

        model.agents[0].last_opponent_action = Action.DEPENDENT
        model.agents[1].last_opponent_action = Action.DEPENDENT

        model.step()

        for agent in model.agents:
            assert agent.last_action == Action.DEPENDENT

    def test_random_strategy(self):
        model = EduGameModel(n_agents=100, strategy=Strategy.RANDOM, seed=42)
        model.step()

        actions = [a.last_action for a in model.agents]
        has_master = Action.MASTER in actions
        has_dependent = Action.DEPENDENT in actions

        assert has_master and has_dependent
