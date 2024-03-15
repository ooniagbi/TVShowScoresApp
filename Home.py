import streamlit as st
import pandas as pd
import statistics
from functions import get_average, update_average, add_series

# Page setup
st.set_page_config(layout="wide")
st.title("Our TV shows Scores!")
st.subheader("A web application for the TV shows we watch together.")

# Read op data, initialize variables, and calculate needed values for op
op_data = pd.read_csv("openime.csv")
op_scores = []

averages = get_average()
old_op_average = float(averages[0])

for index, row in op_data.iterrows():
    op_scores.append(row["Score"])

new_op_average = round(statistics.mean(op_scores), 1)

if new_op_average != old_op_average:
    averages[0] = f'{new_op_average}' + '\n'
    update_average(averages)

op_delta = round(new_op_average - old_op_average, 1)

# Read ayaba data, initialize variables, and calculate needed values for ayaba
es_data = pd.read_csv("ayaba.csv")
es_scores = []

old_es_average = float(averages[1])

for index, row in es_data.iterrows():
    es_scores.append(row["Score"])

new_es_average = round(statistics.mean(es_scores), 1)

if new_es_average != old_es_average:
    averages[1] = f'{new_es_average}' + '\n'
    update_average(averages)

es_delta = round(new_es_average - old_es_average, 1)

# Page layout with streamlit columns
col1, col2 = st.columns(2)

with col1:
    st.image("images/openime.png")
    st.metric(label="**Openime's average**", value=new_op_average, delta=op_delta)
    st.link_button(label="See Openime's TV shows", url="/Openime's_series")

with col2:
    st.image("images/esther.png")
    st.metric(label="**Ayaba's average**", value=new_es_average, delta=es_delta)
    st.link_button(label="See Ayaba's TV shows", url="/Ayaba's_series")

# Add expander to add new series through the interface
my_expander = st.expander(label="Add a new TV show! 🌐️")

with my_expander.form(key="add_series", clear_on_submit=True, border=True):
    st.subheader("Add a new TV show you have watched")
    series_name = st.text_input(label="TV show name", label_visibility='visible')
    series_season = st.text_input(label="TV show season (Last season watched)", label_visibility='visible')
    series_owner = st.selectbox(label="Who recommended the TV show?", label_visibility='visible',
                                options=['Openime', 'Ayaba'])
    series_score = st.text_input(label="TV show score", label_visibility='visible')

    submitted = st.form_submit_button("Submit")
    if submitted:
        if add_series(series_name, series_season, series_owner, series_score) == 'Success':
            st.success(body='TV show added', icon="✅")


st.write("Created by Openime and Ayaba")
