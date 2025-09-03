import streamlit as st 
import pandas as pd 
import pymysql 

con=pymysql.connect(
    host="localhost",
    user="root",
    password="aiktc@1234",
    database="cricbuzz"
)

mycursor=con.cursor()

st.header("***CRUD Operation***")
st.subheader("Create, Read, Update and Delete player records.")

crud_list=['Read(View player)','Create(Add player)','Update(Edit Player)','Delete(Remove Player)']

select_opr=st.selectbox('Select Operation',crud_list)

if select_opr=="Read(View player)":
    st.header("View All Players")
    if st.button("Load All player"):
        select_query = """SELECT * FROM venues;"""  # dummy query
        mycursor.execute(select_query)
        rows = mycursor.fetchall()   # fetch results
        if rows:
            df = pd.DataFrame(rows, columns=[desc[0] for desc in mycursor.description])
            st.dataframe(df)
        else:
            st.warning("No records found.")


if select_opr=="Create(Add player)":
    st.header("Add New Player")
    col1,col2=st.columns([3,3])
    with col1:
        player_id = st.number_input('Player ID',min_value=1,step=1)
    with col2:
        player_name = st.text_input('Player Name',placeholder="e.g Virat Kohli")
    
    col3,col4=st.columns([3,3])
    with col3:
        innings = st.number_input("Innings",min_value=1,step=1) 
    with col4:
        runs = st.number_input("Runs",min_value=0) 
    
    col5,col6=st.columns([3,3])
    with col5:
        matches = st.number_input('Matches',min_value=1,step=1)
    with col6:
        average = st.number_input("Average",format="%.2f") 
        
    if st.button("Add Player"):
        # 1. Check if player already exists
        check_query = "SELECT * FROM dummy_player WHERE Player_id = %s"
        mycursor.execute(check_query, (player_id,))
        existing = mycursor.fetchone()
        
        if existing:
            st.warning(f"⚠️ Player with ID {player_id} already exists!")
        else:
            add_query = """
                INSERT INTO dummy_player (Player_id, Player_name, Innings, Runs, Matches, Average)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            mycursor.execute(add_query, (player_id, player_name, innings, runs, matches, average))
            con.commit()
            st.success(f"✅ Player {player_name} added successfully!")
