import streamlit as st
import pandas as pd
import random
import string
import RollingXG as rolling

st.title("Rolling xG Graph")

uploaded_file = st.file_uploader("Choose Wyscout matches xlsx", accept_multiple_files=False, type=['xlsx'])

if uploaded_file:
   matches = pd.read_excel(uploaded_file, sheet_name=0)
   most_used_team = matches['Team'].mode().iloc[0]
   st.text("Team chosen: " + most_used_team)
   col1, col2 = st.columns(2)

   with col1:
      home_colour = st.color_picker("Primary Colour")

   with col2:
      away_colour = st.color_picker("Secondary Colour")
   
   game_split = st.number_input("GameSplits", min_value=1, value=10)

   image_file = st.file_uploader("Choose Logo (optional)", accept_multiple_files=False, type=['png'])

   if 'n_rows' not in st.session_state:
      st.session_state.n_rows = 0

   add = st.button(label="Add Event")

   eventsList = []
   if add:
      st.session_state.n_rows += 1
      st.experimental_rerun()

   eventTitleCol, eventDateCol = st.columns(2)

   for i in range(st.session_state.n_rows):
       #add text inputs here
      with eventTitleCol:
         eventTitle = st.text_input(label="Event " + str(i+1)  + " Name", key=i)
      with eventDateCol:
         eventDate = st.number_input(label="Event " + str(i+1)  + " Date", min_value=1)
      event = (eventTitle, eventDate)
      eventsList.append(event)

   if st.button("Create Rolling xG"):
      rolling.create_rolling_xg(matches, most_used_team, home_colour, away_colour, game_split, eventsList, image_file)
