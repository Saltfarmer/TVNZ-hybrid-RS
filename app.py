import streamlit as st
import pandas as pd
import numpy as np
import random
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit_authenticator as stauth

st.set_page_config(layout="wide")

content = pd.read_csv('TVNZ_metadata.csv')

# Use 5 users to speed it up
user = pd.read_csv('user_data.csv')
# rating = pd.read_csv('rating_data.csv')

# Choosing random default key in state session
if 'key' not in st.session_state:
  st.session_state['key'] = random.randint(0, len(content))

key = st.session_state['key']

if 'rating' not in st.session_state:
  st.session_state['rating'] = pd.read_csv('rating_data.csv')

rating = st.session_state['rating']

if 'user' not in st.session_state:
  st.session_state['user'] = 0

current_user_id = st.session_state['user']

combine = content.merge(rating.merge(user, left_on=['user_id'], right_on=['ID']), left_on=['ID'], right_on=['content_id'] ) 
combine = combine.drop(columns=['ID_x', 'ID_y'])

st.title("TVNZ Recommendation System")
# create a cover and info column to display the selected book
cover, info = st.columns([3, 2])

with cover:
  # display the image
  st.image(content['image'].iloc[key])

with info:
  # display the book information
  st.title(content['title'].iloc[key])
  st.markdown("## [Watch It](" + content['url'].iloc[key] + ")", unsafe_allow_html=True)
  st.markdown("### "+ content['description'].iloc[key])
  st.caption("genre : " + content['category'].iloc[key])

user_review, rating_hist = st.columns([3, 2])

# Create a data based on specific content
with st.expander("See what people thinks about this content"):
  user_watch_content = combine[combine['content_id'] == content['ID'].iloc[key]]
  if len(user_watch_content) == 0:
    st.title("No one review this content yet") 

  else:
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

def authenticate():
  # #1. retrieve user credentials
  names = user['username'].tolist()
  passwords = user['ID'].astype(str).tolist()

  # #2. create a hash for each passwords so that we do not send these in the clear
  hashed_passwords = stauth.Hasher(passwords).generate()

  # #3. create the authenticator which will create an authentication session cookie with an expiry interval
  authenticator = stauth.Authenticate(names, names, hashed_passwords, 'streamlit-auth-0','streamlit-auth-0-key',cookie_expiry_days=1)

  # #4. display the login form in the sidebar 
  name, authentication_status, username = authenticator.login('Login','sidebar')

  # #5. the streamlit_authenticator library keeps state of the authentication status in streamlit's st.session_state['authentication_status']

  # # > if the authentication succeeded (i.e. st.session_state['authentication_status'] == True)
  if st.session_state['authentication_status']:
  #   # display name on the sidebar
    with st.sidebar:
      st.title("Welcome " + user[user['username'] == name]['name'].iloc[0])			

  #   # set user id in session state
    user_id = int(user[user['username'] == name]['ID'].iloc[0])
    st.session_state['user'] = user_id
    
  # # > if the authentication failed
  elif st.session_state['authentication_status'] == False:
  #   # write an error message on the sidebar
    with st.sidebar:
      st.error('Username/password is incorrect')

  # # > if there are no authentication attempts yet (e.g., first time visitors)
  elif st.session_state['authentication_status'] == None:
  #   # write an warning message on the sidebar
    with st.sidebar:			
      st.warning('Please enter your username and password in the sidebar')

# User login is working but really fucking slow. Uncomment function call below to try use it
# authenticate()

def keychanger(keymaker):
  st.session_state['key'] = keymaker

def Jaccard_Similarity(doc1, doc2): 
    
  # List the unique words in a document
  words_doc1 = set(doc1.lower().split()) 
  words_doc2 = set(doc2.lower().split())
  
  # Find the intersection of words list of doc1 & doc2
  intersection = words_doc1.intersection(words_doc2)

  # Find the union of words list of doc1 & doc2
  union = words_doc1.union(words_doc2)
      
  # Calculate Jaccard similarity score 
  # using length of intersection set divided by length of union set
  return float(len(intersection)) / len(union)

similarity = []

for title in content['title']:
  similarity.append(Jaccard_Similarity(content['title'].iloc[key], title))

jac = pd.DataFrame(similarity, columns=['distance'])
top_jac = jac.sort_values(by=['distance'], ascending=False)[1:6].index

recom0 = content[content['ID'].isin(top_jac)]
# Showing recommendation according similar title

st.title("5 similar titles")
columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = content[content['title'] == recom0['title'].iloc[i]].index.tolist()[0]
      st.button(recom0['title'].iloc[i], key=0, on_click=keychanger, args=(keymaker, ))
      st.markdown(recom0['category'].iloc[i])
      st.image(recom0['image'].iloc[i])

# Showing recommendation according to random same cluster
recom1 = content[content['cluster'] == content['cluster'].iloc[key]].sample(n=5, replace=False)

st.title("5 Recommendation based on same description cluster and random category")
columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = content[content['title'] == recom1['title'].iloc[i]].index.tolist()[0]
      st.button(recom1['title'].iloc[i], key=1, on_click=keychanger, args=(keymaker, ))
      st.markdown(recom1['category'].iloc[i])
      st.image(recom1['image'].iloc[i])

# Showing recommendation according to random same cluster and category
cat = st.selectbox("Choose the genre", content['category'].unique().tolist(), index=content['category'].unique().tolist().index(content['category'].iloc[key]))
recom2 = content[(content['cluster'] == content['cluster'].iloc[key]) & (content['category'] == cat)].sample(n=5, replace=False)

st.title("5 Recommendation based on same description cluster and specific category")
columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = content[content['title'] == recom2['title'].iloc[i]].index.tolist()[0]
      st.button(recom2['title'].iloc[i], key=2, on_click=keychanger, args=(keymaker, ))
      st.markdown(recom2['category'].iloc[i])
      st.image(recom2['image'].iloc[i])

# Showing recommendation according to top 5 rating from user

st.title("Top 5 content based on user rating")
top5 = combine.groupby('content_id').mean().sort_values(by=['rating'], ascending=False).head(5).index
recom3 = content[content['ID'].isin(top5)]

columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = content[content['title'] == recom3['title'].iloc[i]].index.tolist()[0]
      st.button(recom3['title'].iloc[i], key=3, on_click=keychanger, args=(keymaker, ))
      st.markdown(recom3['category'].iloc[i])
      st.image(recom3['image'].iloc[i])

# Showing recommendation according to similar rating patterns from user

df = rating.pivot(index='content_id', columns='user_id', values='rating').fillna(0)

from sklearn.neighbors import NearestNeighbors

knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(df.values)
distances, indices = knn.kneighbors(df.values, n_neighbors=len(df))

recom4 = content[content['ID'].isin(indices[key][1:])]

st.title("Top 5 similar content based on user Rating")

columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = content[content['title'] == recom4['title'].iloc[i]].index.tolist()[0]
      st.button(recom4['title'].iloc[i], key=4, on_click=keychanger, args=(keymaker, ))
      st.markdown(recom4['category'].iloc[i])
      st.image(recom4['image'].iloc[i])

st.title("Top 5 most different content based on user Rating")

recom5 = content[content['ID'].isin(indices[key][-5:])]

columns = st.columns(5)

for i in range(5):
    with columns[i]:
      keymaker = content[content['title'] == recom5['title'].iloc[i]].index.tolist()[0]
      st.button(recom5['title'].iloc[i], key=5, on_click=keychanger, args=(keymaker, ))
      st.markdown(recom5['category'].iloc[i])
      st.image(recom5['image'].iloc[i])

# Feedback mechanism input part

with st.expander("Put your comments and review here"):
  rate = st.slider("Rating ", -5, 5, 0)
  comment = st.text_input("Your comment", " ", placeholder = "put your comment here and dont forget click enter before submit")

  data = {'rating' : rate, 'comment' : comment, 'user_id' : current_user_id, 'content_id' : content['ID'].iloc[key]}

  def record(data):
    st.session_state['rating'] = st.session_state['rating'].append(data, ignore_index=True)
    
  st.button("Submit", on_click=record, args=(data,))

# st.write(data)
# st.dataframe(st.session_state['rating'].tail())

st.info('Your privacy always comes first for us: We secure your data properly and only use them for our services. We will not share your data with third parties for marketing purposes, unless we have received your explicit permission. You decide whether we can use your data for additional TVNZ services. You can modify or delete your data for these services. You can read all about it in our privacy statement.')