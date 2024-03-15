import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MultiLabelBinarizer

shows = pd.read_csv('files/TMDB_tv_dataset_v3.csv')
shows.drop(columns=['original_language', 'adult', 'backdrop_path',
                    'first_air_date', 'last_air_date', 'homepage', 'in_production', 'original_name',
                    'poster_path', 'type', 'status', 'languages',
                    'origin_country', 'spoken_languages', 'production_countries',
                    'episode_run_time'], inplace=True)
shows = shows[shows['vote_count'] >= 300]
shows = shows[shows['vote_average'] >= 7.0]
shows['genres'] = shows['genres'].astype(str)
shows['networks'] = shows['networks'].astype(str)

ayaba_top_shows = pd.read_csv('ayaba.csv')
ayaba_top_shows = ayaba_top_shows[ayaba_top_shows['Score'] >= 8.5]

op_top_shows = pd.read_csv('openime.csv')
op_top_shows = op_top_shows[op_top_shows['Score'] >= 8.5]

# Initialize TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer(stop_words='english')

# Fit and transform the overview data
tfidf_matrix = tfidf_vectorizer.fit_transform(shows['overview'].values.astype('U'))

# Convert genres into list of genres
shows['genres'] = shows['genres'].apply(lambda x: x.split(', '))

# Initialize MultiLabelBinarizer for one-hot encoding genres
mlb_genres = MultiLabelBinarizer()

# One-hot encode genres
genres_encoded = pd.DataFrame(mlb_genres.fit_transform(shows['genres']), columns=mlb_genres.classes_, index=shows.index)

# Convert networks into list of networks
shows['networks'] = shows['networks'].apply(lambda x: x.split(', '))

# Initialize MultiLabelBinarizer for one-hot encoding networks
mlb_networks = MultiLabelBinarizer()

# One-hot encode networks
networks_encoded = pd.DataFrame(mlb_networks.fit_transform(shows['networks']), columns=mlb_networks.classes_,
                                index=shows.index)

# Combine TF-IDF matrix, one-hot encoded genres, and one-hot encoded networks
combined_features = pd.concat([genres_encoded, networks_encoded], axis=1)

# Calculate cosine similarity using combined features
cosine_sim_combined = cosine_similarity(combined_features, combined_features)


# Function to get the top similar shows using combined features
def get_similar_shows(show_name, cosine_sim=cosine_sim_combined, df=shows):
    try:
        idx = df[df['name'] == show_name].index[0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:6]
        movie_indices = [i[0] for i in sim_scores]

        # Ensure movie_indices are within bounds
        return df['name'].iloc[movie_indices].to_list()
    except IndexError:
        return ''


def return_default_rec_show_list():
    show_recs = []

    for idx, rw in op_top_shows.iterrows():
        show_name = rw['Name']
        rec_shows = get_similar_shows(show_name)
        for show in rec_shows:
            show_recs.append(show)

    for idx, rw in ayaba_top_shows.iterrows():
        show_name = rw['Name']
        rec_shows = get_similar_shows(show_name)
        for show in rec_shows:
            show_recs.append(show)

    # remove empty strings and duplicates from list and return list
    show_recs = list(dict.fromkeys(show_recs))
    show_recs = list(filter(None, show_recs))
    return show_recs


if __name__ == '__main__':
    print(len(return_default_rec_show_list()))
    print(return_default_rec_show_list())
