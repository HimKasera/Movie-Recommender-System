import streamlit as st
import pickle
import requests
from requests.utils import quote

# Load the movie data and similarity matrix
movie = pickle.load(open("movie_list.pkl", 'rb'))  # Assuming this is a DataFrame
similarity = pickle.load(open("similarity.pkl", 'rb'))

# Extract movie titles
movie_list = movie['title'].values

# OMDb API key
API_KEY = "93a38e5e"  # Replace with your API key

# Fetch movie details from OMDb API
def fetch_movie_details(movie_title):
    encoded_title = quote(movie_title)  # Encode title for URL
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={encoded_title}"  # Append the API key
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "title": data.get("Title", "Unknown"),
            "poster": data.get("Poster", "https://via.placeholder.com/150?text=No+Poster"),
        }
    else:
        return {"title": movie_title, "poster": "https://via.placeholder.com/150?text=No+Poster"}

# Recommendation function
def recommand(selected_movie):
    index = movie[movie['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommand_movie = [movie.iloc[i[0]].title for i in distances[1:6]]
    return recommand_movie

# Streamlit UI
st.header("Movie Recommender System")
selectvalue = st.selectbox("Select a movie from the dropdown", movie_list)

# Change the background color of the output area
st.markdown("""
    <style>
        .recommendation-output {
            background-color: #f0f8ff;  /* Light blue background */
            padding: 10px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

if st.button("Show Recommend"):
    movie_name = recommand(selectvalue)
    st.subheader("Recommended Movies:")

    # Create columns to display movie recommendations in a row
    cols = st.columns(5)  # Create 5 columns for 5 movie recommendations

    # Create a div with a class to apply the background color to the recommendations
    with st.container():
        st.markdown('<div class="recommendation-output">', unsafe_allow_html=True)  # Apply the background color here
        
        for i, name in enumerate(movie_name):
            details = fetch_movie_details(name)
            with cols[i]:  # Iterate through each column and display the movie in that column
                st.image(details["poster"], width=150)
                st.write(f"**{details['title']}**")
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close the div to end the background styling

# Run the app using: streamlit run app.py
