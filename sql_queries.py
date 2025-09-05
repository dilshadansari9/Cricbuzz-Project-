import streamlit as st
# import mysql.connector
import pymysql 
import pandas as pd

# --- Database Connection ---
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="aiktc@1234", 
        database="cricbuzz"
    )

# --- Store Queries One by One ---
queries = {
    "All players who represent India": """
        SELECT full_name, playing_role, batting_style, bowling_style
        FROM players
        WHERE country="India";
    """,

    "All cricket matches in the last 30 days": """
        SELECT md.match_description, md.team1_name, md.team2_name,
               v.venue_name, v.city, md.match_date
        FROM matches_details md
        JOIN venues v ON v.venue_id=md.venue_id
        WHERE match_date >= CURDATE() - INTERVAL 30 DAY
        ORDER BY match_date DESC;
    """,

    "Top 10 highest run scorers in ODI cricket": """
        SELECT p.full_name, pc.total_runs, pc.batting_avg, pc.centuries
        FROM player_career_stats pc
        JOIN players p ON p.player_id=pc.player_id
        JOIN formats f ON f.format_id=pc.format_id
        WHERE f.format_name="ODI"
        ORDER BY pc.total_runs DESC
        LIMIT 10;
    """,

    "All cricket venues with capacity > 50,000": """
        SELECT venue_name, city, country, capacity
        FROM venues
        WHERE capacity >= 50000
        ORDER BY capacity DESC;
    """,

    "Calculate how many matches each team has won": """
        SELECT t.team_name, COUNT(md.winner_team_id) AS total_wins
        FROM matches_details md
        JOIN teams t ON t.team_id=md.winner_team_id
        GROUP BY t.team_name
        ORDER BY total_wins DESC;
    """,

    "How many players belong to each playing role": """
        SELECT playing_role, COUNT(*) AS player_count
        FROM players
        GROUP BY playing_role;
    """,

    "All cricket series that started in 2024": """
        SELECT series_name, host_country, match_type, start_date, total_match
        FROM series
        WHERE YEAR(start_date)=2024;
    """,

    "All-rounders with 1000+ runs & 50+ wickets": """
        SELECT p.full_name, pc.total_runs, pc.total_wickets, f.format_name
        FROM player_career_stats pc
        JOIN players p ON p.player_id=pc.player_id
        JOIN formats f ON f.format_id=pc.format_id
        WHERE p.playing_role='All-rounder' AND pc.total_runs > 1000 AND pc.total_wickets > 50;
    """,

    "Details of the last 20 completed matches": """
        SELECT md.match_description, md.team1_name, md.team2_name,
               t.team_name AS winning_team, md.victory_margin, md.victory_type, v.venue_name
        FROM matches_details md
        JOIN venues v ON v.venue_id=md.venue_id
        JOIN teams t ON t.team_id=md.winner_team_id
        ORDER BY match_date DESC
        LIMIT 20;
    """,

    "Compare each player's performance across formats": """
        SELECT p.full_name,
               SUM(CASE WHEN f.format_name='Test' THEN pc.total_runs ELSE 0 END) AS test_runs,
               SUM(CASE WHEN f.format_name='ODI' THEN pc.total_runs ELSE 0 END) AS odi_runs,
               SUM(CASE WHEN f.format_name='T20I' THEN pc.total_runs ELSE 0 END) AS t20_runs,
               pc.batting_avg
        FROM player_career_stats pc
        JOIN players p ON p.player_id=pc.player_id
        JOIN formats f ON f.format_id=pc.format_id
        GROUP BY pc.player_id, p.full_name, pc.batting_avg
        HAVING COUNT(DISTINCT f.format_id) >= 2;
    """,

    "Batting partnerships (100+ runs consecutive batsmen)": """
        SELECT p1.full_name AS player_1, p2.full_name AS player_2,
               par.runs_scored, par.innings_no
        FROM batting_partnerships par
        JOIN players p1 ON p1.player_id = par.player1_id
        JOIN players p2 ON p2.player_id = par.player2_id
        WHERE par.runs_scored >= 100
          AND (par.batting_position1 - par.batting_position2 = 1)
        ORDER BY par.runs_scored DESC;
    """,

    "Examine bowling performance at different venues": """
        SELECT p.full_name AS bowler_name,
               v.venue_name,
               COUNT(pm.match_id) AS matches_played,
               SUM(pm.wickets_taken) AS total_wickets,
               SUM(pm.runs_conceded)/NULLIF(SUM(pm.overs_bowled),0) AS average_economy
        FROM player_match_stats pm
        JOIN players p ON p.player_id=pm.player_id
        JOIN venues v ON v.venue_id=pm.venue_id
        WHERE pm.overs_bowled >= 4
        GROUP BY p.player_id, p.full_name, v.venue_name
        HAVING COUNT(pm.match_id) >= 3;
    """
}

# --- Streamlit UI ---
st.header("***Get the details of the given Query***")

selected_query = st.selectbox("Select Query", queries.keys())

if st.button("Run Query"):
    conn = get_connection()
    cursor = conn.cursor() 
    cursor.execute(queries[selected_query])
    result = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(result, columns=columns)
    st.dataframe(df)
    conn.close() 
