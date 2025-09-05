import streamlit as st
import requests
import pandas as pd

# Cricbuzz API setup
url_search = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
url_player = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
url_batting = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
url_bowling = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling" 

api_headers = {
    "x-rapidapi-key": "39509eb435mshde3d740b1db062ep11fa7cjsn5ae8931e3c2b",
    "x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

st.set_page_config(page_title="Cricket Player Statistics", layout="wide")

# Title
st.title("🏏 Cricket Player Statistics")

# Initialize session state
if "players" not in st.session_state:
    st.session_state.players = {}
if "selected_player" not in st.session_state:
    st.session_state.selected_player = None

# Search box
col1, col2 = st.columns([4, 1])
with col1:
    player_name = st.text_input("Enter player name:", placeholder="e.g., Virat Kohli, KL Rahul, MS Dhoni")
with col2:
    search_btn = st.button("🔍 Search")

# Search action
if search_btn and player_name.strip():
    response = requests.get(url_search, headers=api_headers, params={"plrN": player_name})
    if response.status_code == 200:
        data = response.json()
        if "player" in data and len(data["player"]) > 0:
            st.session_state.players = {p["name"]: p["id"] for p in data["player"]}

# Show selectbox if players exist
if st.session_state.players:
    selected_player = st.selectbox("Select a player:", list(st.session_state.players.keys()))
    st.session_state.selected_player = selected_player

# If a player is selected, show profile
if st.session_state.selected_player:
    player_id = st.session_state.players[st.session_state.selected_player]
    player_resp = requests.get(url_player.format(player_id=player_id), headers=api_headers)

    if player_resp.status_code == 200:
        player_data = player_resp.json()

        # Player Header
        st.header(f"📊 {player_data.get('name', '')} - Player Profile")
        st.subheader(player_data.get("nickName", ""))

        # Tabs
        tab1, tab2, tab3 = st.tabs(["📋 Profile", "🏏 Batting Stats", "🎯 Bowling Stats"])

        # PROFILE TAB
        with tab1:
            st.subheader("📌 Personal Information")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Cricket Details**")
                st.write("Role:", player_data.get("role", "N/A"))
                st.write("Batting:", player_data.get("bat", "N/A"))
                st.write("Bowling:", player_data.get("bowl", "N/A"))
                st.write("International Team:", player_data.get("country", "N/A"))
            with col2:
                st.markdown("**Personal Details**")
                st.write("Date of Birth:", player_data.get("DoB", "N/A"))
                st.write("Birth Place:", player_data.get("birthPlace", "N/A"))
                st.write("Height:", player_data.get("height", "N/A"))

            with col3:
                teams = player_data.get("teams", [])
                if isinstance(teams, list):  
                    st.write("Teams Played For:", ", ".join(teams))
                elif isinstance(teams, str):  #
                    st.write("Teams Played For:", teams)
                else:
                    st.write("Teams Played For:", "N/A")

        # BATTING TAB
        with tab2:
            st.subheader("📈 Batting Statistics")
            bat_resp = requests.get(url_batting.format(player_id=player_id), headers=api_headers)
            if bat_resp.status_code == 200:
                bat_data = bat_resp.json()
                if "headers" in bat_data and "values" in bat_data:
                    table_header = bat_data['headers']
                    batting_stats = []
                    for row_data in bat_data['values']:
                        row = {}
                        for i, value in enumerate(row_data['values']):
                            row[table_header[i]] = value
                        batting_stats.append(row)

                    df = pd.DataFrame(batting_stats)
                    st.table(df)

        # BOWLING TAB
        with tab3:
            st.subheader("🎯 Bowling Statistics")
            bowl_resp = requests.get(url_bowling.format(player_id=player_id), headers=api_headers)
            if bowl_resp.status_code == 200:
                bowl_data = bowl_resp.json()
                if "headers" in bowl_data and "values" in bowl_data:
                    table_header = bowl_data['headers']
                    bowling_stats = []
                    for row_data in bowl_data['values']:
                        row = {}
                        for i, value in enumerate(row_data['values']):
                            row[table_header[i]] = value
                        bowling_stats.append(row)

                    df = pd.DataFrame(bowling_stats)
                    st.table(df)
