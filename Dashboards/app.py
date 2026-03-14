import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket Analytics Dashboard", page_icon="🏏", layout="wide")

st.title("🏏 International Cricket Analytics Dashboard")
st.markdown("Ball-by-ball analysis of ODI, T20I and Test matches (2005–2020)")

# Format selector
format_choice = st.selectbox("Select Format", ["ODI", "T20I", "Test"])

prefix = format_choice.lower().replace("t20i", "t20")

@st.cache_data
def load_data(fmt):
    batting = pd.read_csv(f'Data/{fmt}_batting_summary.csv')
    bowling = pd.read_csv(f'Data/{fmt}_bowling_summary.csv')
    teams   = pd.read_csv(f'Data/{fmt}_team_stats.csv')
    return batting, bowling, teams

batting, bowling, teams = load_data(prefix)

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric("Format", format_choice)
col2.metric("Total Batters", f"{len(batting):,}")
col3.metric("Total Teams", f"{len(teams):,}")

st.divider()

tab1, tab2, tab3 = st.tabs(["Batting", "Bowling", "Teams"])

with tab1:
    st.subheader(f"Top 20 Run Scorers — {format_choice}")
    top_bat = batting.sort_values('total_runs', ascending=False).head(20)
    fig = px.bar(top_bat, x='bat', y='total_runs', color='average',
                 color_continuous_scale='Blues',
                 labels={'bat': 'Player', 'total_runs': 'Runs', 'average': 'Average'})
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average vs Strike Rate")
    fig2 = px.scatter(batting[batting['innings'] >= 20], x='average', y='strike_rate',
                      size='total_runs', hover_name='bat', color='innings',
                      color_continuous_scale='Teal',
                      labels={'average': 'Batting Average', 'strike_rate': 'Strike Rate'})
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader(f"Top 20 Wicket Takers — {format_choice}")
    top_bowl = bowling.sort_values('wickets', ascending=False).head(20)
    fig3 = px.bar(top_bowl, x='bowl', y='wickets', color='econ',
                  color_continuous_scale='Reds',
                  labels={'bowl': 'Player', 'wickets': 'Wickets', 'econ': 'Economy'})
    fig3.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader(f"Team Win Rates — {format_choice}")
    fig4 = px.bar(teams.sort_values('win_pct', ascending=True),
                  x='win_pct', y='team', orientation='h',
                  color='win_pct', color_continuous_scale='Greens',
                  labels={'win_pct': 'Win %', 'team': 'Team'})
    st.plotly_chart(fig4, use_container_width=True)