from __future__ import annotations

import altair as alt
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import solara

from src.payoff_config import Action

update_counter = solara.reactive(0)

model_params = {
    "n_agents": solara.SliderInt(
        value=20, min=4, max=100, step=2, label="Number of Agents"
    ),
    "strategy": {
        "type": "Select",
        "values": ["Q_LEARNING", "TIT_FOR_TAT", "GRIM_TRIGGER", "RANDOM"],
        "value": "Q_LEARNING",
        "label": "Strategy",
    },
    "seed": {"type": "InputText", "value": 42, "label": "Random Seed"},
}


@solara.component  # noqa: N802
def NetworkGraph(model):  # noqa: N802
    """Circular network graph: agents=nodes (blue/red), pairings=edges."""
    update_counter.get()
    solara.use_effect(
        lambda: update_counter.set(update_counter.value + 1), [model.steps]
    )

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    g = nx.Graph()
    agents = list(model.agents)
    g.add_nodes_from([a.unique_id for a in agents])

    if hasattr(model, "_pairings"):
        for a, b in model._pairings:
            g.add_edge(a.unique_id, b.unique_id)

    pos = nx.circular_layout(g)

    node_colors = [
        "#2196F3" if a.last_action == Action.MASTER else "#F44336" for a in agents
    ]
    nx.draw_networkx_edges(g, pos, ax=ax, alpha=0.3, edge_color="gray")
    nx.draw_networkx_nodes(g, pos, ax=ax, node_color=node_colors, node_size=300)
    nx.draw_networkx_labels(g, pos, ax=ax, font_size=8)
    ax.set_title(f"Agents & Pairings (Step {model.steps})", fontsize=10)

    plt.close(fig)
    solara.FigureMatplotlib(fig)


@solara.component  # noqa: N802
def TimeSeriesChart(model, measure: str = "master_count"):  # noqa: N802
    """Altair line chart tracking a model metric over time."""
    update_counter.get()
    solara.use_effect(
        lambda: update_counter.set(update_counter.value + 1), [model.steps]
    )

    df = model.datacollector.get_model_vars_dataframe().reset_index()
    if df.empty:
        solara.Warning("No data collected yet")
        return

    col_name = next(
        (c for c in df.columns if measure in c and "mean" not in c and "std" not in c),
        measure,
    )
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("index:Q", title="Step"),
            y=alt.Y(f"{col_name}:Q", title=col_name),
        )
        .properties(width=400, height=200)
    )
    solara.FigureAltair(chart)


@solara.component  # noqa: N802
def QTableStats(model):  # noqa: N802
    """Bar chart of mean Q-values per (opponent_action, my_action) state."""
    update_counter.get()
    solara.use_effect(
        lambda: update_counter.set(update_counter.value + 1), [model.steps]
    )

    data = []
    for opp in [None, Action.MASTER, Action.DEPENDENT]:
        for my in [Action.MASTER, Action.DEPENDENT]:
            vals = [a.q_table.get((opp, my), 0) for a in model.agents]
            data.append(
                {
                    "opponent": str(opp) if opp else "None",
                    "my_action": my.name,
                    "mean_q": sum(vals) / len(vals) if vals else 0,
                }
            )

    df = pd.DataFrame(data)
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=alt.X("opponent:N", title="Opponent Last Action"),
            y=alt.Y("mean_q:Q", title="Mean Q-Value"),
            color=alt.Color(
                "my_action:N",
                title="My Action",
                scale=alt.Scale(
                    domain=["MASTER", "DEPENDENT"],
                    range=["#2196F3", "#F44336"],
                ),
            ),
        )
        .properties(width=350, height=200)
    )
    solara.FigureAltair(chart)


@solara.component  # noqa: N802
def DashboardTabLayout(model):  # noqa: N802
    """Tabbed layout combining all dashboard panels."""
    update_counter.get()
    tab, set_tab = solara.use_state("Network")
    tabs = ["Network", "Master Count", "Mean Payoff", "Q-Table Stats"]

    with solara.Row():
        solara.ToggleButtonsSingle(value=tab, on_value=set_tab, values=tabs)

    with solara.Row():
        if tab == "Network":
            NetworkGraph(model)
        elif tab == "Master Count":
            TimeSeriesChart(model, "master_count")
        elif tab == "Mean Payoff":
            TimeSeriesChart(model, "mean_payoff")
        elif tab == "Q-Table Stats":
            QTableStats(model)
