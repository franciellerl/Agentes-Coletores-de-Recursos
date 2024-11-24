import streamlit as st
import pandas as pd
import altair as alt
import time
from models import create_grid, add_river, add_mountains, distribute_resources
from agents import ReactiveAgent, StateBasedAgent, known_resources

st.title("Trabalho 1 IA - Francielle Rodrigues, João Sales, Pedro Lima")
num_ticks = st.slider("Select Number of Steps", min_value=1, max_value=100, value=20)
rows = st.slider("Select Grid Height", min_value=10, max_value=50, step=5, value=15)
cols = st.slider("Select Grid Width", min_value=10, max_value=50, step=5, value=15)
mountain_count = 10
time_limit = num_ticks
run_simulation = st.button("Run Simulation")

grid = create_grid(rows, cols)
grid = add_river(grid)
grid = add_mountains(grid, mountain_count)
rarity = {'Cristais Energéticos': 10, 'Blocos de Metal Raro': 5, 'Estruturas Antigas': 2}
grid = distribute_resources(grid, rarity)
start_position = (1, 1)

agents = [
    ReactiveAgent("Reativo1", start_position),
    StateBasedAgent("Baseado em Estado", start_position),
]

def prepare_dataframe(grid, agents):
    data = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            cell_type = grid[r][c]
            data.append({"x": c, "y": r, "tipo": cell_type})
    
    for agent_idx, agent in enumerate(agents):
        x, y = agent.pos
        data.append({"x": y, "y": x, "tipo": f"Agente {agent_idx}"})

    return pd.DataFrame(data)

color_scale = alt.Scale(
    domain=['Vazio', 'Rio', 'Montanha', 'Cristais Energéticos', 'Blocos de Metal Raro', 'Estruturas Antigas', 'Agente 0', 'Agente 1'],
    range=['white', '#1E90FF', '#8B4513', '#32CD32', '#FFD700', '#FF4500', 'magenta', 'cyan']
)

if run_simulation:
    tick = time.time()
    df_grid = prepare_dataframe(grid, agents)
    heatmap = (
        alt.Chart(df_grid)
        .mark_rect()
        .encode(
            x='x:O',
            y='y:O',
            color=alt.Color('tipo:N', scale=color_scale),
            tooltip=['x', 'y', 'tipo']
        )
        .properties(width=500, height=500)
    )

    chart_placeholder = st.empty()

    for turn in range(num_ticks):
    
        for agent in agents:
            agent.act(grid, turn, known_resources, agents)
     
        df_grid = prepare_dataframe(grid, agents)
        heatmap = (
            alt.Chart(df_grid)
            .mark_rect()
            .encode(
                x='x:O',
                y='y:O',
                color=alt.Color('tipo:N', scale=color_scale),
                tooltip=['x', 'y', 'tipo']
            )
            .properties(width=500, height=500)
        )
        
        chart_placeholder.altair_chart(heatmap, use_container_width=True)
        time.sleep(1)
