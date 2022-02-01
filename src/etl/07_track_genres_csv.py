import gzip
import csv
from ast import literal_eval

from constants import GENRES_FIELDS
from utils import ROOT_DIR, write_csv_file

TRACKS_DATA_FILE_PATH = f'{ROOT_DIR}/data/mdp_tracks.csv'
ARTIST_DATA_FILE_PATH = f'{ROOT_DIR}/data/external/artists.csv.gz'
OS_PATH = f'{ROOT_DIR}/data'

artist_dict = {}
with gzip.open(ARTIST_DATA_FILE_PATH, 'rt') as artist_file:
    artist_reader = csv.DictReader(artist_file)

    for row in artist_reader:
        artist_uri = row['artist_uri']

        genres = literal_eval(row['genres'])
        followers = int(row['followers'])
        popularity = int(row['popularity'])

        stored_genres = artist_dict.get(artist_uri)
        if stored_genres:
            genres = list(set(stored_genres + genres))

        artist_dict[artist_uri] = genres


tracks_genres = []
with open(TRACKS_DATA_FILE_PATH, 'rt') as tracks_file:
    tracks_reader = csv.DictReader(tracks_file)

    for row in tracks_reader:
        track_uri = row['track_uri']
        artist_uri = row['artist_uri'].replace('spotify:artist:', '')

        genres = artist_dict.get(artist_uri)
        if not genres:
            continue

        tracks_genres.append(
            {
                'track_uri': track_uri,
                'genres': genres
            }
        )


write_csv_file(
    filename=f'{OS_PATH}/mdp_track_genres.csv',
    field_headers=GENRES_FIELDS,
    data=tracks_genres
)
