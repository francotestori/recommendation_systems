import os
import json
from utils import ROOT_DIR, write_csv_file
from constants import (
    PLAYLISTS_FIELDS,
    TRACKS_FIELDS,
    INTERACTIONS_FIELDS
)

MDP_DATA_PATH = f"{ROOT_DIR}/data/mdp"
OS_PATH = f'{ROOT_DIR}/results'

mdp_playlists = {}
mdp_tracks = {}
mdp_interactions = []

filenames = os.listdir(MDP_DATA_PATH)
for filename in sorted(filenames):
    if filename.startswith("mpd.slice.") and filename.endswith(".json"):
        print(filename)
        with open(f"{MDP_DATA_PATH}/{filename}", 'rt') as mdp_data_file:
            json_data = json.load(mdp_data_file)

            for playlist in json_data['playlists']:
                pid = playlist['pid']
                playlist['collaborative'] = int(playlist['collaborative'] == 'true')

                tracks = playlist.pop('tracks')

                if not mdp_playlists.get(pid):
                    mdp_playlists[pid] = playlist

                for track in tracks:
                    track['track_uri'] = track['track_uri'].replace("spotify:track:", "")
                    track_uri = track['track_uri']
                    pos = track.pop('pos')

                    if not mdp_tracks.get(track_uri):
                        mdp_tracks[track_uri] = track

                    mdp_interactions.append(
                        {
                            'pid': pid,
                            'track_uri': track_uri,
                            'pos': pos
                        }
                    )

write_csv_file(
    filename=f'{OS_PATH}/mdp_playlists.csv',
    field_headers=PLAYLISTS_FIELDS,
    data=mdp_playlists.values()
)
write_csv_file(
    filename=f'{OS_PATH}//results/mdp_tracks.csv',
    field_headers=TRACKS_FIELDS,
    data=mdp_tracks.values()
)
write_csv_file(
    filename=f'{OS_PATH}//results/mdp_interactions.csv',
    field_headers=INTERACTIONS_FIELDS,
    data=mdp_interactions
)
