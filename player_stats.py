import streamlit as st
import requests
import pandas as pd

# Cricbuzz API setup
url_search = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/search"
url_player = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}"
url_batting = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/batting"
url_bowling = "https://cricbuzz-cricket.p.rapidapi.com/stats/v1/player/{player_id}/bowling" 

headers = {
	"x-rapidapi-key": "39509eb435mshde3d740b1db062ep11fa7cjsn5ae8931e3c2b",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}

st.set_page_config(page_title="Cricket Player Statistics", layout="wide")

# Title
st.title("🏏 Cricket Player Statistics")

# Search box
col1, col2 = st.columns([4, 1])
with col1:
    player_name = st.text_input("Enter player name:", placeholder="e.g., Virat Kohli, KL Rahul, MS Dhoni")
with col2:
    search_btn = st.button("🔍 Search")

if search_btn and player_name.strip():
    response = requests.get(url_search, headers=headers, params={"plrN": player_name})
    
    if response.status_code == 200:
        data = response.json()
        if "player" in data and len(data["player"]) > 0:
            player_options = {p["name"]: p["id"] for p in data["player"]}
            selected_player = st.selectbox("Select a player:", list(player_options.keys()))
            
            player_id = player_options[selected_player]
            player_resp = requests.get(url_player.format(player_id=player_id), headers=headers)
            
            if player_resp.status_code == 200:
                player_data = player_resp.json()
                
                # Player Header
                st.header(f"📊 {player_data.get('name', '')} - Player Profile")
                st.subheader(player_data.get("nickName", ""))

                # Tabs
                tab1, tab2, tab3 = st.tabs(["📋 Profile", "🏏 Batting Stats", "🎯 Bowling Stats"])
                
                # ---------------- PROFILE TAB ----------------
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

                with tab2:
                    st.subheader("📈 Batting Statistics")
                    bat_resp = requests.get(url_batting.format(player_id=player_id), headers=headers)
                    
                    if bat_resp.status_code == 200:
                        bat_data = bat_resp.json()
                        batting_stats = [] 
                        table_header = bat_data['headers']
                        for row_data in bat_data['values']:
                            row = {}
                            for i, value in enumerate(row_data['values']):
                                row[table_header[i]] = value
                            batting_stats.append(row)

                        formatted_batting_stats = []
                        for row in batting_stats:
                            formatted_row = {
                                "Format": row["ROWHEADER"],
                                "Test": row["Test"],
                                "ODI": row["ODI"],
                                "T20": row["T20"],
                                "IPL": row["IPL"]
                            }
                            formatted_batting_stats.append(formatted_row)

                        df = pd.DataFrame(formatted_batting_stats)
                        # st.dataframe(df)
                        st.table(df)
                        st.write(f"For more Info visit here: {bat_data['appIndex']['webURL']}")
                        

                
                # ---------------- BOWLING STATS TAB ----------------
                with tab3:
                    st.subheader("🎯 Bowling Statistics")
                    bowl_resp = requests.get(url_bowling.format(player_id=player_id), headers=headers)
                    
                    if bowl_resp.status_code == 200:
                        bowl_data = bowl_resp.json()
                        bowling_stats = [] 
                        table_header = bowl_data['headers'] 
                        for row_data in bowl_data['values']:
                            row = {}
                            for i, value in enumerate(row_data['values']):
                                row[table_header[i]] = value
                            bowling_stats.append(row)

                        formatted_bowling_stats = []
                        for row in bowling_stats:
                            formatted_row = {
                                "Format": row["ROWHEADER"],
                                "Test": row["Test"],
                                "ODI": row["ODI"],
                                "T20": row["T20"],
                                "IPL": row["IPL"]
                            }
                            formatted_bowling_stats.append(formatted_row)

                        df = pd.DataFrame(formatted_bowling_stats)
                        # st.dataframe(df)
                        st.table(df)
                        st.write(f"For more Info visit here: {bowl_data['appIndex']['webURL']}")
