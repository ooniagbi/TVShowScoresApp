import pandas as pd
import streamlit as st
from functions import fetch_poster, save_poster

# Read op data, initialize variables, and calculate needed values for op
op_data = pd.read_csv("openime.csv")

op_scores = []
series_posters = []
series_seasons = []
op_series_names = []

for index, row in op_data.iterrows():
    series_name = row["Name"]
    series_season = row["Season"]
    series_poster = row["Poster_URL"]
    op_scores.append(row["Score"])
    op_series_names.append(row["Name"])

    if pd.isna(row['Poster_URL']):
        poster = fetch_poster(series_name)
        save_poster(series_name=series_name, url=poster)
        series_posters.append(poster)
    series_posters.append(series_poster)
    series_seasons.append(series_season)

op_total = sum(op_scores)

# Page setup
st.set_page_config(layout="wide")
st.title("Openime's TV shows")
st.subheader(f"Openime's total: {op_total}")

# Display series in rows and columns
op_series_count = len(op_scores)
cols = st.columns(5)


def add_series_row(i, j):
    with cols[i]:
        if series_posters[j] is not None:
            st.image(series_posters[j])
        label_text = f'{op_series_names[j]} Season {series_seasons[j]}'
        st.link_button(label=label_text, url='https://www.google.com/search?q=' + op_series_names[j])
        st.metric(label="Score", value=op_scores[j], label_visibility="collapsed")


col_index = 0
series_index = 0

# While loop restarts for every new row of series
while series_index < op_series_count:
    if col_index < 5:
        add_series_row(col_index, series_index)
        col_index += 1
        series_index += 1
    else:
        col_index = 0
