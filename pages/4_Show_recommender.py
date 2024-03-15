import streamlit as st
import pandas as pd
from recommender import get_similar_shows
from functions import fetch_poster

st.set_page_config(layout='wide')
st.title('Recommended shows')
st.subheader('Find similar shows below.')

shows = pd.read_csv('files/TMDB_tv_dataset_v3.csv')
shows = shows[shows['vote_count'] >= 300]
shows = shows[shows['vote_average'] >= 7.0]
show_titles = shows['name']

show_posters = []

my_expander = st.expander(label='Tap to select a show')
selected_show = my_expander.selectbox(label='Show titles', options=show_titles.values[:-3])

if my_expander.button(label='Recommend'):
    st.text('Top 5 similar shows:')
    rec_shows = get_similar_shows(selected_show)
    for show in rec_shows:
        poster = fetch_poster(show)
        show_posters.append(poster)

    # Display series in rows and columns
    show_count = len(rec_shows)
    cols = st.columns(5)


    def add_series_row(i, j):
        with cols[i]:
            if show_posters[j] is not None:
                st.image(show_posters[j])
            st.link_button(label=rec_shows[j], url='https://www.google.com/search?q=' + rec_shows[j])


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
