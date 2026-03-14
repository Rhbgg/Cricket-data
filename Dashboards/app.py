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
    batting  = pd.read_csv(f'Data/{fmt}_batting_summary.csv')
    bowling  = pd.read_csv(f'Data/{fmt}_bowling_summary.csv')
    teams    = pd.read_csv(f'Data/{fmt}_team_stats.csv')
    scoring  = pd.read_csv(f'Data/{fmt}_scoring_curve.csv')
    venue    = pd.read_csv(f'Data/{fmt}_venue_stats.csv')
    h2h      = pd.read_csv(f'Data/{fmt}_head_to_head.csv')
    year_bat = pd.read_csv(f'Data/{fmt}_year_batting.csv')
    return batting, bowling, teams, scoring, venue, h2h, year_bat

batting, bowling, teams, scoring, venue, h2h, year_bat = load_data(prefix)

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric("Format", format_choice)
col2.metric("Total Batters", f"{len(batting):,}")
col3.metric("Total Teams", f"{len(teams):,}")

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Batting", "Bowling", "Teams", "Scoring Curve", "Venues", "Head to Head"
])

with tab1:
    st.subheader(f"Top Run Scorers — {format_choice}")
    top_n = st.slider("Number of players", 5, 30, 20)
    top_bat = batting.sort_values('total_runs', ascending=False).head(top_n)
    fig = px.bar(top_bat, x='bat', y='total_runs', color='average',
                 color_continuous_scale='Blues',
                 labels={'bat': 'Player', 'total_runs': 'Runs', 'average': 'Average'})
    fig.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Average vs Strike Rate")
    min_innings = st.slider("Minimum innings", 5, 50, 20)
    fig2 = px.scatter(batting[batting['innings'] >= min_innings],
                      x='average', y='strike_rate',
                      size='total_runs', hover_name='bat', color='innings',
                      color_continuous_scale='Teal',
                      labels={'average': 'Batting Average', 'strike_rate': 'Strike Rate'})
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Player Search")
    player_list = sorted(batting['bat'].unique())
    selected_player = st.selectbox("Search for a player", player_list)
    player_data = batting[batting['bat'] == selected_player].iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Runs", f"{int(player_data['total_runs']):,}")
    c2.metric("Innings", f"{int(player_data['innings'])}")
    c3.metric("Average", f"{player_data['average']}")
    c4.metric("Strike Rate", f"{player_data['strike_rate']}")

    st.subheader("Player Runs by Year")
    player_years = year_bat[year_bat['bat'] == selected_player]
    if not player_years.empty:
        fig_yr = px.bar(player_years, x='year', y='runs',
                        labels={'year': 'Year', 'runs': 'Runs'},
                        color='sr', color_continuous_scale='Blues')
        st.plotly_chart(fig_yr, use_container_width=True)
    else:
        st.info("No year-wise data available for this player.")

with tab2:
    st.subheader(f"Top Wicket Takers — {format_choice}")
    top_n_bowl = st.slider("Number of bowlers", 5, 30, 20)
    top_bowl = bowling.sort_values('wickets', ascending=False).head(top_n_bowl)
    fig3 = px.bar(top_bowl, x='bowl', y='wickets', color='econ',
                  color_continuous_scale='Reds',
                  labels={'bowl': 'Player', 'wickets': 'Wickets', 'econ': 'Economy'})
    fig3.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Bowler Search")
    bowler_list = sorted(bowling['bowl'].unique())
    selected_bowler = st.selectbox("Search for a bowler", bowler_list)
    bowler_data = bowling[bowling['bowl'] == selected_bowler].iloc[0]
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Wickets", f"{int(bowler_data['wickets'])}")
    b2.metric("Runs Conceded", f"{int(bowler_data['runs']):,}")
    b3.metric("Economy", f"{bowler_data['econ']}")
    b4.metric("Average", f"{bowler_data['avg']}")

with tab3:
    st.subheader(f"Team Win Rates — {format_choice}")
    min_matches = st.slider("Minimum matches", 5, 50, 20)
    filtered_teams = teams[teams['matches'] >= min_matches].sort_values('win_pct', ascending=True)
    fig4 = px.bar(filtered_teams, x='win_pct', y='team', orientation='h',
                  color='win_pct', color_continuous_scale='Greens',
                  labels={'win_pct': 'Win %', 'team': 'Team'})
    st.plotly_chart(fig4, use_container_width=True)

with tab4:
    st.subheader(f"Scoring Curve — Runs per Over ({format_choice})")
    fig5 = px.line(scoring, x='over', y='rpo',
                   labels={'over': 'Over', 'rpo': 'Runs per Over'},
                   markers=True)
    fig5.update_traces(line_color='#7F77DD')
    st.plotly_chart(fig5, use_container_width=True)

with tab5:
    st.subheader(f"Venue Analysis — {format_choice}")
    top_venues = st.slider("Number of venues", 5, 30, 15)
    top_venue = venue.head(top_venues)
    fig6 = px.bar(top_venue, x='ground', y='matches', color='rpo',
                  color_continuous_scale='Oranges',
                  labels={'ground': 'Venue', 'matches': 'Matches', 'rpo': 'Runs per Over'})
    fig6.update_layout(xaxis_tickangle=-35)
    st.plotly_chart(fig6, use_container_width=True)

with tab6:
    st.subheader(f"Head to Head — {format_choice}")
    teams_list = sorted(h2h['team1'].unique())
    col_a, col_b = st.columns(2)
    with col_a:
        team1 = st.selectbox("Select Team 1", teams_list)
    with col_b:
        team2 = st.selectbox("Select Team 2", [t for t in teams_list if t != team1])

    h2h_filtered = h2h[
        ((h2h['team1'] == team1) & (h2h['team2'] == team2)) |
        ((h2h['team1'] == team2) & (h2h['team2'] == team1))
    ]

    if not h2h_filtered.empty:
        total_matches = h2h_filtered['matches'].sum()
        team1_wins = h2h_filtered[h2h_filtered['team1'] == team1]['wins'].sum()
        team2_wins = h2h_filtered[h2h_filtered['team1'] == team2]['wins'].sum()

        h1, h2c, h3 = st.columns(3)
        h1.metric("Total Matches", int(total_matches))
        h2c.metric(f"{team1} Wins", int(team1_wins))
        h3.metric(f"{team2} Wins", int(team2_wins))

        fig7 = px.bar(
            x=[team1, team2],
            y=[int(team1_wins), int(team2_wins)],
            color=[team1, team2],
            labels={'x': 'Team', 'y': 'Wins'}
        )
        st.plotly_chart(fig7, use_container_width=True)
    else:
        st.info("No head to head data found for this combination.")