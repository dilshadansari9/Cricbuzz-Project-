import streamlit as st
import requests 
import pandas as pd 
st.title("⚡ Live Matches")
st.write("This page  shows live match updates from Cricbuzz API.") 



import requests

# url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"

headers = {
	"x-rapidapi-key": "39509eb435mshde3d740b1db062ep11fa7cjsn5ae8931e3c2b",
	"x-rapidapi-host": "cricbuzz-cricket.p.rapidapi.com"
}


response = requests.get(url, headers=headers)
data=response.json() 

# Actual extraction logic
matches = []

for type_match in data.get("typeMatches", []):
    for series_match in type_match.get("seriesMatches", []):
        series_data = series_match.get("seriesAdWrapper", {})
        series_id = series_data.get("seriesId")
        series_name = series_data.get("seriesName")

        for match in series_data.get("matches", []):
            info = match.get("matchInfo", {})
            match_id = info.get("matchId")
            match_desc = info.get("matchDesc")
            match_format = info.get("matchFormat")
            start_date = info.get("startDate")
            state=info.get('state')
            status = info.get("status")
            team1 = info.get("team1", {}).get("teamName")
            team2 = info.get("team2", {}).get("teamName")
            city=info.get("venueInfo", {}).get("city"),
            score=match.get('matchScore',{})
            venue_info=info.get("venueInfo", {}).get('city')          


            matches.append({
                "series_id": series_id,
                "series_name": series_name,
                "match_id": match_id,
                "desc": match_desc,
                "match_format": match_format,
                "team1": team1,
                "team2": team2,
                "venue": venue_info,
                "city":city, 
                "status": status,
                'score':score, 
                "state":state 
            })


            

df = pd.DataFrame(matches) 
# st.write(df) 


st.title("🏏 Cricbuzz Live Match Dashboard")
page=st.sidebar.radio("Select one option. ",['Live Score'])
# page= st.selectbox("Select a match",['Live Score'])

if page=='Live Score':
    match_names=[f"{match['team1']} vs {match['team2']} - {match['desc'] } status: {match['status']}" for match in matches] 
    selected=st.selectbox("Select Match: ",match_names) 
    selected_match = matches[match_names.index(selected)]   

    st.header(f'{selected_match['team1']} vs {selected_match['team2']}')
    st.write(f'**Series**: {selected_match['series_name']}') 
    st.write(f'**Match**: {selected_match['desc']}')
    st.write(f"**Venue:** {selected_match['venue']}")
    st.write(f"**City:** {selected_match['city']}") 
    st.write(f"**State:** {selected_match['state']}") 
    st.write(f"**Status:** {selected_match['status']}")
    st.write(f'match id: {selected_match['match_id']}')


    st.subheader("📊 Current Score")
    score = selected_match["score"] 
    if score:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{selected_match['team1']}**")
            t1 = score.get("team1Score", {}).get("inngs1", {})
            if t1:
                st.write(f"Innings: {t1.get('runs')}/{t1.get('wickets')} ({t1.get('overs')} overs)")
        with col2:
            st.markdown(f"**{selected_match['team2']}**")
            t2 = score.get("team2Score", {}).get("inngs1", {})
            if t2:
                st.write(f"Innings: {t2.get('runs')}/{t2.get('wickets')} ({t2.get('overs')} overs)")

    st.header("📊 Match Summary..")

    if st.button('Match summary'):
        col1,col2,col3=st.columns(3)
        with col1:
            st.write(f'**Match**: {selected_match['desc']}')
        with col2:
            st.write(f'**WInner**: {selected_match['status']}')
        with col3:
            st.write(f'**State**: {selected_match['state']}')
            

    if st.button("🏏 Get full info"):


        score_url = f"https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/{selected_match['match_id']}/hscard" 
        response = requests.get(score_url, headers=headers)
        score_data = response.json()


        for inning in score_data.get("scoreCard", []):
            batting_team = inning['batTeamDetails']['batTeamName']
            bowling_team = inning['bowlTeamDetails']['bowlTeamName']

            st.subheader(f"🏏 {batting_team} Batting & {bowling_team} Bowling")

            # ---------------- Batting ----------------
            batsmen_data = inning['batTeamDetails'].get('batsmenData', {})
            if batsmen_data:  
                batting_list = []
                for b_id, batsman in batsmen_data.items():
                    batting_list.append({
                        'Name': batsman['batName'],
                        'Runs': batsman['runs'],
                        'Balls': batsman['balls'],
                        '4s': batsman['fours'],
                        '6s': batsman['sixes'],
                        'SR': f"{float(batsman['strikeRate']):.2f}",
                        'Status': batsman['outDesc'] 
                    })
                df_batting = pd.DataFrame(batting_list)
                st.markdown(f"**Batting - {batting_team}**")
                st.table(df_batting)
            else:
                st.warning(f"Batting for {batting_team} not started yet.")

            # ---------------- Bowling ----------------
            bowlers_data = inning['bowlTeamDetails'].get('bowlersData', {})
            if bowlers_data:  
                bowling_list = []
                for bowler_id, bowler in bowlers_data.items():
                    bowling_list.append({
                        'Name': bowler['bowlName'],
                        'Overs': f"{float(bowler['overs']):.1f}",
                        'Maidens': bowler['maidens'],
                        'Runs': bowler['runs'],
                        'Wickets': bowler['wickets'],
                        'Economy': f"{float(bowler['economy']):.2f}"
                    })
                df_bowling = pd.DataFrame(bowling_list)
                st.markdown(f"**Bowling - {bowling_team}**")
                st.table(df_bowling)
            else:
                st.warning(f"Bowling for {bowling_team} not started yet.")

            st.markdown("---")

