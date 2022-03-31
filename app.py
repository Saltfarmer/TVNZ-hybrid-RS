import streamlit as st
import pandas as pd
import numpy as np
import random


st.set_page_config(layout="wide")

df = pd.read_csv('TVNZ_movies_v3.csv')

# Choosing random default key in state session
if 'key' not in st.session_state:
  st.session_state['key'] = random.randint(0, len(df))

key = st.session_state['key']

st.title("TVNZ Recommendation System")
# create a cover and info column to display the selected book
cover, info = st.columns([3, 2])

with cover:
  # display the image
  st.image(df['image'].iloc[key])

with info:
  # display the book information
  st.title(df['title'].iloc[key])
  st.header("Genre : " + df['GenreType'].iloc[key])
  st.markdown(df['description'].iloc[key])  
  st.markdown(df['distributor'].iloc[key])  
  st.caption("genre : " + df['genre'].iloc[key])

user_review, rating_hist = st.columns([2, 2])

with user_review:
  st.title("User")
  st.markdown("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

with rating_hist:
  st.area_chart(chart_data)

