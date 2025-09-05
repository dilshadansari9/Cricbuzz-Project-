import streamlit as st 
import runpy 


st.sidebar.title("Navigation")
option=st.sidebar.selectbox("Selcet the page.. ",["Introduction","Live Matches", "CRUD Operations",  "Player Stats", "SQL Queries"])

if option=='Introduction':
    st.title("🏏 Cricbuzz Project Dashboard")
    st.write(
        """
        Welcome to the **Cricbuzz Project Dashboard** 🎉  

        Use the sidebar to navigate between pages:  
        - **CRUD Operations**: Manage players and database records.  
        - **Live Matches**: Get real-time cricket match details.  
        - **Player Stats**: View batting & bowling statistics of players.  
        - **SQL Queries**: Run custom SQL queries on the cricket database.  
        """
    )

if option=="Live Matches":
    runpy.run_path('live_matches.py')
elif option=='CRUD Operations':
    runpy.run_path('crud_opr.py')

elif option=="Player Stats":
    runpy.run_path('player_stats.py')

elif option=="SQL Queries":
    runpy.run_path("sql_queries.py")