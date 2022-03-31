import streamlit as st
import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

content = pd.read_csv('TVNZ_movies_v3.csv')
user = pd.read_csv('user_data.csv')
rating = pd.read_csv('rating_data.csv')

combine = content.merge(rating.merge(user, left_on=['user_id'], right_on=['ID']), left_on=['ID'], right_on=['content_id'] ) 

# Choosing random default key in state session
if 'key' not in st.session_state:
  st.session_state['key'] = random.randint(0, len(content))

key = st.session_state['key']

st.title("TVNZ Recommendation System")
# create a cover and info column to display the selected book
cover, info = st.columns([3, 2])

with cover:
  # display the image
  st.image(content['image'].iloc[key])

with info:
  # display the book information
  st.title(content['title'].iloc[key])
  st.header("Genre : " + content['GenreType'].iloc[key])
  st.markdown(content['description'].iloc[key]) 
  st.caption("genre : " + content['genre'].iloc[key])

user_review, rating_hist = st.columns([3, 2])

# Create a data based on specific content
user_watch_content = combine[combine['content_id'] == content['ID'].iloc[key]]

# Create a sample comment to show
sample = user_watch_content.sample(1)

with user_review:
  st.title("Username : " + sample['username'].values[0])
  st.markdown(sample['comment'].values[0])

with rating_hist:
  st.title(f"Average rating : {user_watch_content['rating'].mean():.2f}")
  fig, ax = plt.subplots()
  sns.set_theme()
  sns.countplot(user_watch_content['rating'])
  st.pyplot(fig)

# Showing recommendation according to random same cluster
recom1 = content[content['k_means'] == content['k_means'].iloc[key]].sample(n=5)

st.title("5 Recommendation based on description cluster and random category")
columns = st.columns(5)

def keychanger(keymaker):
  st.session_state['key'] = keymaker

for i in range(5):
    with columns[i]:
      keymaker = content[content['title'] == recom1['title'].iloc[i]].index.tolist()[0]
      st.button(recom1['title'].iloc[i], on_click=keychanger, args=(keymaker, ))
      st.markdown(recom1['GenreType'].iloc[i])
      st.image(recom1['image'].iloc[i])