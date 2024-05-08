import streamlit as st
import pickle
import pandas as pd
import requests



movie_list = pickle.load(open('Movie_List.pkl','rb'))
similarity = pickle.load(open('Similarity_Matrix.pkl','rb'))
Name_of_Movie = movie_list['title'].values







def fetch_poster(movie_id):
    response = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=d035285557bb8fc5c6f07eae9f7dc434".format(movie_id))
    data = response.json()
    return "http://image.tmdb.org/t/p/w500"+data['poster_path']
 
def recommend(movie):
    recomended_Movies = []
    recommend_Movies_ID = []
    poster_path = []
    index = movie_list[movie_list['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
    for i in distances[1:6]:
        recomended_Movies.append(movie_list.iloc[i[0]].title)
        recommend_Movies_ID.append(movie_list.iloc[i[0]].movie_id)
    for i in recommend_Movies_ID:
        poster_path.append(fetch_poster(i))
    return recomended_Movies,recommend_Movies_ID,poster_path








st.title('Movie Recommender System')

selected_Movie_Name = st.selectbox(
    'Please select your movie name : ',
    Name_of_Movie
)

if st.button('Recommend'):
    NameList,IdList,poster = recommend(selected_Movie_Name)    
    st.header("If you are watching - {} ".format(selected_Movie_Name))
    st.header("You must watch : ")
    cols = st.columns(5)
    for i,path,name in zip(range(5),poster,NameList):
        cols[i].image(path)
        cols[i].write(name)