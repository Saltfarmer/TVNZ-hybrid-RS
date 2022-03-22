import streamlit as st
import pandas as pd
import numpy as np
import authenticate as a
import random


st.set_page_config(layout="wide")

df = pd.read_csv('TVNZ_movies_v3.csv')

st.dataframe(df.sample(5))

# create a cover and info column to display the selected book
cover, info = st.columns([2, 3])

# Choosing random default key in state session
if 'key' not in st.session_state:
  st.session_state['key'] = random.randint(0, len(df))

key = st.session_state['key']

with cover:
  # display the image
  st.image(df['image'].iloc[key])

with info:
  # display the book information
  st.header(df['title'].iloc[key])
  st.markdown(df['description'].iloc[key])  
  # st.markdown("# [Watch It](" + df['url'].iloc[key] + ")", unsafe_allow_html=True)
  st.caption("genre : " + df['genre'].iloc[key])

  