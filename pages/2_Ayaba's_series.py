import pandas as pd
import streamlit as st
from functions import fetch_poster, save_poster

# Read ayaba data, initialize variables, and calculate needed values for op
ayaba_data = pd.read_csv("ayaba.csv")

ayaba_scores = []
series_posters = []
series_seasons = []
ayaba_series_names = []

for index, row in ayaba_data.iterrows():
    series_name = row["Name"]
    series_season = row["Season"]
    series_poster = row["Poster_URL"]
    ayaba_scores.append(row["Score"])
    ayaba_series_names.append(row["Name"])

    if pd.isna(row['Poster_URL']):
        poster = fetch_poster(series_name)
        save_poster(series_name=series_name, url=poster)
        series_posters.append(poster)
    series_posters.append(series_poster)
    series_seasons.append(series_season)

ayaba_total = sum(ayaba_scores)

# Page setup
st.set_page_config(layout="wide")
st.title("Ayaba's TV shows")
st.subheader(f"Ayaba's total: {ayaba_total}")

# Display series in rows and columns
ayaba_series_count = len(ayaba_scores)
cols = st.columns(5)


def add_movie_row(i, j):
    with cols[i]:
        if series_posters[j] is not None:
            st.image(series_posters[j])
        label_text = f'{ayaba_series_names[j]} Season {series_seasons[j]}'
        st.link_button(label=label_text, url='https://www.google.com/search?q=' + ayaba_series_names[j])
        st.metric(label="Score", value=ayaba_scores[j], label_visibility="collapsed")


col_index = 0
series_index = 0

# While loop restarts for every new row of series
while series_index < ayaba_series_count:
    if col_index < 5:
        add_movie_row(col_index, series_index)
        col_index += 1
        series_index += 1
    else:
        col_index = 0
