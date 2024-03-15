import streamlit as st
from recommender import return_default_rec_show_list
from functions import fetch_poster

st.set_page_config(layout="wide")
st.title("Recommended shows")
st.subheader("The recommendations below are based on the shows we've seen that we scored 8.5 or above.")

recommended_shows = return_default_rec_show_list()
show_posters = []

for show_name in recommended_shows[:10]:
    poster = fetch_poster(show_name)
    show_posters.append(poster)


# Display series in rows and columns
show_count = len(recommended_shows[:10])
cols = st.columns(5)


def add_series_row(i, j):
    with cols[i]:
        if show_posters[j] is not None:
            st.image(show_posters[j])
        st.link_button(label=recommended_shows[j], url='https://www.google.com/search?q=' + recommended_shows[j])


col_index = 0
series_index = 0

# While loop restarts for every new row of series
while series_index < show_count:
    if col_index < 5:
        add_series_row(col_index, series_index)
        col_index += 1
        series_index += 1
    else:
        col_index = 0
