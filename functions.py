import pandas
import pandas as pd
import requests
import os

api_key = os.environ['API_KEY_TMDB']
FILEPATH = 'files/averages.txt'


def get_tv_series_id(tv_series_name):
    tv_series = pd.read_csv("files/TMDB_tv_dataset_v3.csv")

    # find the row with the input tv series name
    tv_series_row = tv_series[tv_series['name'] == tv_series_name]

    # if the tv_series is not found, return an error message
    if tv_series_row.empty:
        return "TV Series name not found."

    # if the tv series is found, return the movie id
    else:
        return tv_series_row.iloc[0]['id']


def fetch_poster(series_name):
    series_id = get_tv_series_id(series_name)

    if series_id != "TV Series name not found.":
        response = requests.get(f'https://api.themoviedb.org/3/tv/{series_id}?api_key={api_key}')
        data = response.json()
        return "https://image.tmdb.org/t/p/w220_and_h330_face/" + data["poster_path"]


def get_average(filepath=FILEPATH):
    """ Reads a text file and returns the average
    """
    # with context manager ensures the file is closed even if the program runs into an error
    with open(filepath, 'r') as file_local:
        averages = file_local.readlines()
    return averages


def update_average(new_average, filepath=FILEPATH):
    """ Writes the average to a text file"""
    with open(filepath, 'w') as file_local:
        file_local.writelines(new_average)


def add_series(sr_name, sr_season, sr_owner, sr_score):
    new_series = {'Name': sr_name, 'Season': sr_season, 'Score': float(sr_score)}
    if sr_owner == 'Openime':
        df = pandas.read_csv('openime.csv')
        df.loc[len(df)] = new_series
        df.to_csv('openime.csv', index=False)
        return 'Success'
    elif sr_owner == 'Ayaba':
        df = pandas.read_csv('ayaba.csv')
        df.loc[len(df)] = new_series
        df.to_csv('ayaba.csv', index=False)
        return 'Success'


def save_poster(series_name, url):
    op_df = pandas.read_csv('openime.csv')
    es_df = pandas.read_csv('ayaba.csv', header=0)

    # Checks if name is in list of movies and updates the url
    updated_rows_es_df = es_df.loc[es_df['Name'] == series_name, 'Poster_URL']
    es_df.loc[es_df['Name'] == series_name, 'Poster_URL'] = url

    updated_rows_op_df = op_df.loc[op_df['Name'] == series_name, 'Poster_URL']
    op_df.loc[op_df['Name'] == series_name, 'Poster_URL'] = url

    if not updated_rows_es_df.empty:
        es_df.to_csv('ayaba.csv', index=False)

    if not updated_rows_op_df.empty:
        op_df.to_csv('openime.csv', index=False)


if __name__ == "__main__":
    print(fetch_poster('Game of Thrones'))
