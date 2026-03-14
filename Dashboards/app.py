import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Cricket Analytics Dashboard", page_icon="🏏", layout="wide")

st.title("🏏 International Cricket Analytics Dashboard")
st.markdown("Ball-by-ball analysis of ODI, T20I and Test matches (2005–2020)")

@st.cache_data
def load_data():
    batting = pd.read_csv('Data/odi_batting_summary.csv')
    bowling = pd.read_csv('Data/odi_bowling_summary.csv')
    teams   = pd.read_csv('Data/odi_team_stats.csv')
    return batting, bowling, teams
batting, bowling, teams = load_data()


col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", "1,962")
col2.metric("Total Balls", "1.05M")
col3.metric("Batters Tracked", "1,364")
col4.metric("Years Covered", "2005–2020")

st.divider()

tab1, tab2, tab3 = st.tabs(["Batting", "Bowling", "Teams"])

with tab1:
    st.subheader("Top 20 Run Scorers")
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
    st.subheader("Top 20 Wicket Takers")
    top_bowl = bowling.sort_values('wickets', ascending=False).head(20)
    fig3 = px.bar(top_bowl, x='bowl', y='wickets', color='econ',
                  color_continuous_scale='Reds',
                  labels={'bowl': 'Player', 'wickets': 'Wickets', 'econ': 'Economy'})
    fig3.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig3, use_container_width=True)

with tab3:
    st.subheader("Team Win Rates")
    fig4 = px.bar(teams.sort_values('win_pct', ascending=True),
                  x='win_pct', y='team', orientation='h',
                  color='win_pct', color_continuous_scale='Greens',
                  labels={'win_pct': 'Win %', 'team': 'Team'})
    st.plotly_chart(fig4, use_container_width=True)