import csv
from utils import ROOT_DIR, write_pickle_file

INTERACTIONS_CSV_PATH = f"{ROOT_DIR}/data/mdp_interactions.csv"
OS_PATH = f'{ROOT_DIR}/results'

tracks_count = {}
tracks_positions = {}

with open(INTERACTIONS_CSV_PATH, 'r') as interactions_file:
    interactions_reader = csv.DictReader(interactions_file)
    for row in interactions_reader:
        track_uri = row['track_uri']
        pos = row['pos']

        tracks_count[track_uri] = tracks_count.get(track_uri, 0) + 1

        track_position_list = tracks_positions.get(track_uri)
        if track_position_list:
            tracks_positions[track_uri] = track_position_list.append(pos)
        else:
            tracks_positions[track_uri] = [pos]


write_pickle_file(
    filename=f'{OS_PATH}/tracks_interaction_count.pickle',
    data=tracks_count
)
write_pickle_file(
    filename=f'{OS_PATH}/tracks_interaction_positions.pickle',
    data=tracks_positions
)
