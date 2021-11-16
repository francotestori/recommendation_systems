import csv
import gzip
from ast import literal_eval
from utils import ROOT_DIR, write_pickle_file, read_pickle_file
from models.base import ArtistMetadata, TrackGenre

TRACKS_INTERACTIONS_FILE_PATH = f'{ROOT_DIR}/results/tracks_interaction_count.pickle'
TRACKS_DATA_FILE_PATH = f'{ROOT_DIR}/results/mdp_tracks.csv'
ARTIST_DATA_FILE_PATH = f'{ROOT_DIR}/data/artists.csv.gz'
OS_PATH = f'{ROOT_DIR}/results'

popular_tracks = read_pickle_file(TRACKS_INTERACTIONS_FILE_PATH)

artist_metadata_dict = {}
with gzip.open(ARTIST_DATA_FILE_PATH, 'rt') as artist_file:
    artist_reader = csv.DictReader(artist_file)

    for row in artist_reader:
        artist_uri = row['artist_uri']

        genres = literal_eval(row['genres'])
        followers = int(row['followers'])
        popularity = int(row['popularity'])

        stored_metadata = artist_metadata_dict.get(artist_uri)
        if stored_metadata:
            genres = list(set(stored_metadata.genres + genres))
            followers = max(stored_metadata.followers, followers)
            popularity = max(stored_metadata.popularity, popularity)

        artist_metadata_dict[artist_uri] = ArtistMetadata(
            artist_uri=artist_uri,
            genres=genres,
            followers=followers,
            popularity=popularity
        )


tracks_genres = {}
with open(TRACKS_DATA_FILE_PATH, 'rt') as tracks_file:
    tracks_reader = csv.DictReader(tracks_file)

    for row in tracks_reader:
        track_uri = row['track_uri']
        artist_uri = row['artist_uri'].replace('spotify:artist:', '')
        interactions = popular_tracks[track_uri]

        artist_metadata = artist_metadata_dict.get(artist_uri)
        if not artist_metadata:
            continue

        tracks_genres[track_uri] = TrackGenre(
            track_uri=track_uri,
            genres=artist_metadata.genres,
            followers=artist_metadata.followers,
            popularity=artist_metadata.popularity,
            interactions=interactions
        )

write_pickle_file(f'{OS_PATH}/artists_genres.pickle', artist_metadata_dict)
write_pickle_file(f'{OS_PATH}/tracks_genres.pickle', tracks_genres)




