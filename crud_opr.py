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
        select_query = """SELECT * FROM dummy_player;"""  # dummy query
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
        player_id = st.number_input('Player ID', min_value=1, step=1)
    with col2:
        player_name = st.text_input('Player Name', placeholder="e.g Virat Kohli")
    
    col3,col4=st.columns([3,3])
    with col3:
        innings = st.number_input("Innings", min_value=1, step=1) 
    with col4:
        runs = st.number_input("Runs", min_value=0) 
    
    col5,col6=st.columns([3,3])
    with col5:
        matches = st.number_input('Matches', min_value=1, step=1)
    with col6:
        average = st.number_input("Average", format="%.2f") 
         
    if st.button("Add Player"):

        if not player_name.strip():
            st.error("❌ Player Name cannot be empty.")
        elif innings is None or runs is None or matches is None or average is None:
            st.error("❌ All fields must be filled in.")
        else:
            
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
                st.balloons()



if select_opr == "Update(Edit Player)":
    st.header("✏️ Update Player Record")

    player_id = st.number_input("Enter Player ID to update:", min_value=1, step=1)

    if st.button("Fetch Player"):

        select_player = "SELECT * FROM dummy_player WHERE Player_id=%s"
        mycursor.execute(select_player, (player_id,)) 
        existing = mycursor.fetchone() 
 
        if not existing:
            st.warning("⚠️ Player does not exist.")
        
        else:
            st.session_state['selected_player']=existing 
    if 'selected_player' in st.session_state:
            existing = st.session_state['selected_player'] 
            _, existing_name, existing_innings, existing_runs, existing_matches, existing_avg = existing=existing
            col1, col2 = st.columns([3, 3])
            with col1:
                new_name = st.text_input("Player Name", value=existing_name)
            with col2:
                new_innings = st.number_input("Innings", min_value=1, step=1, value=existing_innings)

            col3, col4 = st.columns([3, 3])
            with col3:
                new_runs = st.number_input("Runs", min_value=0, value=existing_runs)
            with col4:
                new_matches = st.number_input("Matches", min_value=1, step=1, value=existing_matches)

            new_average = st.number_input("Average", format="%.2f", value=float(existing_avg))
                
            if st.button("Update Player"):
                update_query = """
                    UPDATE dummy_player 
                    SET Player_name=%s, Innings=%s, Runs=%s, Matches=%s, Average=%s
                    WHERE Player_id=%s
                """
                mycursor.execute(update_query, (new_name, new_innings, new_runs, new_matches, new_average, player_id))
                con.commit()
                st.success(f"✅ Player {new_name} (ID: {player_id}) updated successfully!") 
                st.balloons()  



if select_opr == "Delete(Remove Player)":
    st.header("🗑️ Delete Player Record")
    st.warning("⚠️ This action cannot be undone!")

    # Step 1: Search Player
    search_name = st.text_input("🔍 Search player to delete:")

    if search_name:
        search_query = "SELECT Player_id, Player_name, Runs FROM dummy_player WHERE Player_name LIKE %s"
        search_query=search_query.strip()
        mycursor.execute(search_query, ("%" + search_name + "%",))
        results = mycursor.fetchall()

        if results:
            # Step 2: Select Player
            player_options = [f"{row[1]} (ID: {row[0]}) - {row[2]} runs" for row in results]
            selected = st.selectbox("⚠️ Select player to DELETE:", player_options)

            # Extract id and name
            selected_index = player_options.index(selected)
            player_id, player_name, player_runs = results[selected_index]

            st.error(f"🚨 You are about to delete: {player_name}")

            # Step 3: Final Confirmation
            confirm_text = st.text_input(f"Type 'DELETE {player_name}' to confirm:") 

            if confirm_text == f"DELETE {player_name}":
                if st.button("✅ Confirm Delete"):
                    delete_query = "DELETE FROM dummy_player WHERE Player_id = %s"
                    mycursor.execute(delete_query, (player_id,))
                    con.commit()
                    st.success(f"✅ Player {player_name} (ID: {player_id}) deleted successfully!")
            else:
                st.info("Type the confirmation text exactly to enable delete.")
        else:
            st.warning("No players found with that name.") 
            
            
            


