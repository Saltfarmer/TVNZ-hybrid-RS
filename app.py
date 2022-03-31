import streamlit as st
import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_authenticator as stauth

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

# #1. retrieve user credentials
# names = user['username'].tolist()
# passwords = user['ID'].astype(str).tolist()

# #2. create a hash for each passwords so that we do not send these in the clear
# hashed_passwords = stauth.Hasher(passwords).generate()

# #3. create the authenticator which will create an authentication session cookie with an expiry interval
# authenticator = stauth.Authenticate(names, names, hashed_passwords, 'streamlit-auth-0','streamlit-auth-0-key',cookie_expiry_days=1)

# #4. display the login form in the sidebar 
# name, authentication_status, username = authenticator.login('Login','sidebar')

# #5. the streamlit_authenticator library keeps state of the authentication status in streamlit's st.session_state['authentication_status']

# # > if the authentication succeeded (i.e. st.session_state['authentication_status'] == True)
# if st.session_state['authentication_status']:
#   # display name on the sidebar
#   with st.sidebar:
#     st.text(name)			

#   # set user id in session state
#   user_id = int(user[user['username'] == name]['ID'].iloc[0])
#   st.session_state['user'] = user_id
  
# # > if the authentication failed
# elif st.session_state['authentication_status'] == False:
#   # write an error message on the sidebar
#   with st.sidebar:
#     st.error('Username/password is incorrect')

# # > if there are no authentication attempts yet (e.g., first time visitors)
# elif st.session_state['authentication_status'] == None:
#   # write an warning message on the sidebar
#   with st.sidebar:			
#     st.warning('Please enter your username and password in the sidebar')

# # Showing recommendation according to random same cluster
# recom1 = content[content['k_means'] == content['k_means'].iloc[key]].sample(n=5)

# st.title("5 Recommendation based on description cluster and random category")
# columns = st.columns(5)

# def keychanger(keymaker):
#   st.session_state['key'] = keymaker

# for i in range(5):
#     with columns[i]:
#       keymaker = content[content['title'] == recom1['title'].iloc[i]].index.tolist()[0]
#       st.button(recom1['title'].iloc[i], on_click=keychanger, args=(keymaker, ))
#       st.markdown(recom1['GenreType'].iloc[i])
#       st.image(recom1['image'].iloc[i])

# rate = st.slider("Rating ", 1, 5, 3)
# comment = st.text_input("Your comment", " ")

# def record(data):
#   st.session_state['activities'].append(data, ignore_index=True)
#   st.write(len(st.session_state['activities']))

# st.button("Submit", on_click=record, args=(data,))

# st.write(data)

# # st.dataframe(st.session_state['activities'].tail())

st.write("**Add your own comment:**")
form = st.form("comment")
rate = form.slider("rate", 1, 5, 3)
username = form.text_input("Username")
comment = form.text_area("Comment")
submit = form.form_submit_button("Add comment")
